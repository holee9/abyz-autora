#!/bin/bash
# Abyz-AutoRA Folder Structure Setup
# Creates the required directory structure on NAS mount point

set -e

BASE_DIR="/data/medical-auth"

echo "Creating Abyz-AutoRA folder structure at $BASE_DIR"

# Create main directories
mkdir -p "$BASE_DIR/01_Templates"
mkdir -p "$BASE_DIR/02_Projects"
mkdir -p "$BASE_DIR/03_Logs"

# Create example project structure
EXAMPLE_PROJECT="$BASE_DIR/02_Projects/X-ray_Detector/DX-2026"
mkdir -p "$EXAMPLE_PROJECT/assets"
mkdir -p "$EXAMPLE_PROJECT/requests"
mkdir -p "$EXAMPLE_PROJECT/output"
mkdir -p "$EXAMPLE_PROJECT/_Error"

# Create example specs.json
cat > "$EXAMPLE_PROJECT/specs.json" << 'EOF'
{
  "model_info": {
    "model_id": "DX-2026",
    "trade_name": "Abyz-Ray Pro",
    "classification": "Class IIb",
    "manufacturing_date": "2026-01"
  },
  "tech_specs": {
    "resolution": "3072 x 3072",
    "pixel_pitch": "140 um",
    "input_voltage": "DC 24V",
    "power_consumption": "50W max",
    "dimension": "300 x 300 x 50 mm"
  },
  "manufacturer": {
    "name": "Abyz-Lab Inc.",
    "address": "Suwon-si, Gyeonggi-do, Korea",
    "contact": "contact@abyz-lab.com"
  },
  "certifications": {
    "iso_13485": true,
    "iso_9001": true,
    "ce_mark": "Pending"
  }
}
EOF

# Create .gitkeep files
touch "$BASE_DIR/01_Templates/.gitkeep"
touch "$BASE_DIR/03_Logs/.gitkeep"

# Set permissions
chmod -R 755 "$BASE_DIR/02_Projects"

echo "Folder structure created successfully!"
echo ""
echo "Structure:"
tree "$BASE_DIR" 2>/dev/null || find "$BASE_DIR" -type d | sort
echo ""
echo "Example specs.json created at: $EXAMPLE_PROJECT/specs.json"
