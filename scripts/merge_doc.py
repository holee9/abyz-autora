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


# Filename sanitization for security
INVALID_FILENAME_CHARS = r'[<>:"/\\|?*\x00-\x1f]'


class DocumentMerger:
    """Handle Word document merging with JSON data."""

    REQUIRED_FIELDS = ['model_id', 'trade_name', 'classification']

    def __init__(self, template_path: str, json_path: str, base_dir: str = "/data/medical-auth"):
        self.template_path = Path(template_path).resolve()
        self.json_path = Path(json_path).resolve()
        self.base_dir = Path(base_dir).resolve()
        self.data = None

        # Validate paths are within base directory (prevent path traversal)
        self._validate_paths()

    def _validate_paths(self):
        """Ensure paths are within the expected base directory."""
        for path in [self.template_path, self.json_path]:
            try:
                path.relative_to(self.base_dir)
            except ValueError:
                raise ValueError(f"Path traversal detected: {path} is outside {self.base_dir}")

    def _sanitize_filename(self, filename: str) -> str:
        """Remove invalid characters from filename."""
        return re.sub(INVALID_FILENAME_CHARS, '_', filename)

    def load_json(self) -> dict:
        """Load and validate JSON data."""
        if not self.json_path.exists():
            raise FileNotFoundError(f"Specs file not found: {self.json_path}")

        with open(self.json_path, 'r', encoding='utf-8') as f:
            self.data = json.load(f)

        self._validate_data()
        return self.data

    def _validate_data(self):
        """Validate required fields in JSON data."""
        # Check model_info
        model_info = self.data.get('model_info', {})
        for field in self.REQUIRED_FIELDS:
            if field not in model_info:
                raise ValueError(f"Missing required field: model_info.{field}")

        logger.info(f"Validated data for model: {model_info.get('model_id')}")

    def merge(self, output_path: str) -> Path:
        """Merge template with data and save to output."""
        if not self.template_path.exists():
            raise FileNotFoundError(f"Template not found: {self.template_path}")

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

        # Log available merge fields for debugging
        logger.debug(f"Template fields: {document.get_merge_fields()}")

        document.merge(**flat_data)
        document.write(str(safe_output))

        logger.info(f"Document saved: {safe_output}")
        return safe_output

    def _flatten_data(self, data: dict, parent_key: str = '', sep: str = '_') -> dict:
        """Flatten nested dictionary for mailmerge."""
        items = []
        for k, v in data.items():
            new_key = f"{parent_key}{sep}{k}" if parent_key else k
            if isinstance(v, dict):
                items.extend(self._flatten_data(v, new_key, sep=sep).items())
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
