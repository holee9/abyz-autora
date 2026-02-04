#!/usr/bin/env python3
"""
Abyz-AutoRA Word Document Merger
Merge Word templates with JSON data for medical device certification documents.

Usage:
    python merge_doc.py --template <path> --json <path> --output <path>
"""

import argparse
import json
import sys
import re
import unicodedata
from pathlib import Path
from datetime import datetime
from mailmerge import MailMerge
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


# Security constants
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
MAX_RECURSION_DEPTH = 10
INVALID_FILENAME_CHARS = r'[<>:"/\\|?*\x00-\x1f]'
# Preserve Korean characters (Hangul U+AC00 to U+D7A3)
ALLOWED_UNICODE_PREFIX = r'a-zA-Z0-9._-\uAC00-\uD7A3\u1100-\u11FF\u3131-\u318E\uA960-\uA97C\uD7B0-\uD7FB'


class DocumentMerger:
    """Handle Word document merging with JSON data."""

    REQUIRED_FIELDS = ['model_id', 'trade_name', 'classification']

    def __init__(self, template_path: str, json_path: str, base_dir: str = "/data/medical-auth"):
        self.template_path = Path(template_path)
        self.json_path = Path(json_path)
        self.base_dir = Path(base_dir).resolve()
        self.data = None

        # Validate paths BEFORE resolving (prevent symlink attacks)
        self._validate_paths()

    def _validate_paths(self):
        """Ensure paths are within the expected base directory."""
        for path_str in [self.template_path, self.json_path]:
            # Check for path traversal attempt in original path
            path_obj = Path(path_str)
            if '..' in path_obj.parts:
                raise ValueError(f"Path traversal attempt detected: {path_str}")

            # Resolve to check for symlinks
            resolved = path_obj.resolve()

            # Check if resolved path is within base_dir
            try:
                resolved.relative_to(self.base_dir)
            except ValueError:
                raise ValueError(f"Path outside base directory: {resolved} is outside {self.base_dir}")

    def _sanitize_filename(self, filename: str) -> str:
        """Remove invalid characters from filename while preserving Korean."""
        # Normalize Unicode to NFC form
        normalized = unicodedata.normalize('NFC', filename)

        # Only remove truly invalid filesystem characters
        safe = re.sub(INVALID_FILENAME_CHARS, '_', normalized)

        # Limit filename length ( filesystem limit is 255, but reserve space for extension)
        if len(safe.encode('utf-8')) > 200:
            name, ext = Path(safe).stem, Path(safe).suffix
            safe = name[:100] + ext

        return safe

    def _check_file_size(self, file_path: Path) -> None:
        """Validate file size to prevent DoS."""
        size = file_path.stat().st_size
        if size > MAX_FILE_SIZE:
            raise ValueError(f"File too large: {size} bytes (max {MAX_FILE_SIZE})")

    def load_json(self) -> dict:
        """Load and validate JSON data."""
        if not self.json_path.exists():
            raise FileNotFoundError(f"Specs file not found: {self.json_path}")

        # Check file size
        self._check_file_size(self.json_path)

        # Try multiple encodings
        content = None
        for encoding in ['utf-8', 'utf-8-sig', 'euc-kr', 'cp949']:
            try:
                with open(self.json_path, 'r', encoding=encoding) as f:
                    content = f.read()
                break
            except UnicodeDecodeError:
                continue

        if content is None:
            raise ValueError(f"Failed to decode JSON file with any supported encoding")

        self.data = json.loads(content)
        self._validate_data()
        return self.data

    def _validate_data(self):
        """Validate required fields in JSON data."""
        model_info = self.data.get('model_info', {})
        for field in self.REQUIRED_FIELDS:
            if field not in model_info:
                raise ValueError(f"Missing required field: model_info.{field}")

        logger.info(f"Validated data for model: {model_info.get('model_id')}")

    def merge(self, output_path: str) -> Path:
        """Merge template with data and save to output."""
        if not self.template_path.exists():
            raise FileNotFoundError(f"Template not found: {self.template_path}")

        # Check template file size
        self._check_file_size(self.template_path)

        if self.data is None:
            self.load_json()

        # Flatten nested JSON for mailmerge
        flat_data = self._flatten_data(self.data)

        # Sanitize output filename
        output = Path(output_path)
        safe_filename = self._sanitize_filename(output.name)
        safe_output = output.parent / safe_filename

        # Create output directory if needed
        safe_output.parent.mkdir(parents=True, exist_ok=True)

        # Perform merge
        logger.info(f"Merging template: {self.template_path.name}")
        document = MailMerge(str(self.template_path))

        # Get merge fields for logging
        merge_fields = document.get_merge_fields()
        logger.debug(f"Template fields: {merge_fields}")

        if not merge_fields:
            logger.warning("Template has no merge fields - output may be empty")

        document.merge(**flat_data)
        document.write(str(safe_output))

        logger.info(f"Document saved: {safe_output}")
        return safe_output

    def _flatten_data(self, data: dict, parent_key: str = '', sep: str = '_',
                      depth: int = 0) -> dict:
        """Flatten nested dictionary for mailmerge with recursion limit."""
        if depth > MAX_RECURSION_DEPTH:
            raise ValueError(f"JSON nesting too deep (>{MAX_RECURSION_DEPTH} levels)")

        items = []
        for k, v in data.items():
            # Sanitize key names for mailmerge
            safe_key = re.sub(r'[^\w]', '_', str(k))
            new_key = f"{parent_key}{sep}{safe_key}" if parent_key else safe_key

            if isinstance(v, dict):
                items.extend(self._flatten_data(v, new_key, sep, depth + 1).items())
            else:
                items.append((new_key, v))
        return dict(items)


def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description='Merge Word template with JSON data'
    )
    parser.add_argument(
        '--template', '-t',
        required=True,
        help='Path to Word template file (.docx)'
    )
    parser.add_argument(
        '--json', '-j',
        required=True,
        help='Path to JSON data file (specs.json)'
    )
    parser.add_argument(
        '--output', '-o',
        required=True,
        help='Path to output file (.docx)'
    )
    parser.add_argument(
        '--base-dir', '-b',
        default='/data/medical-auth',
        help='Base directory for path validation (default: /data/medical-auth)'
    )
    return parser.parse_args()


def main():
    """Main entry point."""
    args = parse_args()

    try:
        merger = DocumentMerger(args.template, args.json, args.base_dir)
        merger.merge(args.output)
        return 0
    except Exception as e:
        logger.error(f"Merge failed: {e}")
        return 1


if __name__ == '__main__':
    sys.exit(main())
