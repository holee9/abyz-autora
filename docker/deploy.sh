#!/bin/bash
# Abyz-AutoRA Deployment Script for Raspberry Pi
# This script helps deploy the system on a Raspberry Pi

set -e

echo "==================================="
echo "Abyz-AutoRA Deployment Script"
echo "==================================="
echo ""

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Check if running on Raspberry Pi
check_architecture() {
    ARCH=$(uname -m)
    echo "Detected architecture: $ARCH"

    if [[ "$ARCH" == "aarch64" || "$ARCH" == "arm64" ]]; then
        echo -e "${GREEN}✓ ARM64 detected (Raspberry Pi)${NC}"
        return 0
    else
        echo -e "${YELLOW}⚠ Warning: Not running on ARM64${NC}"
        read -p "Continue anyway? (y/N) " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            exit 1
        fi
    fi
}

# Check Docker installation
check_docker() {
    if ! command -v docker &> /dev/null; then
        echo -e "${RED}✗ Docker not found${NC}"
        echo "Installing Docker..."
        curl -fsSL https://get.docker.com | sh
        sudo usermod -aG docker $USER
        echo -e "${GREEN}✓ Docker installed${NC}"
    else
        echo -e "${GREEN}✓ Docker found: $(docker --version)${NC}"
    fi

    if ! command -v docker-compose &> /dev/null && ! docker compose version &> /dev/null; then
        echo -e "${RED}✗ Docker Compose not found${NC}"
        echo "Installing Docker Compose..."
        sudo apt-get update && sudo apt-get install -y docker-compose-plugin
    else
        echo -e "${GREEN}✓ Docker Compose found${NC}"
    fi
}

# Setup NAS mount
setup_nas_mount() {
    echo ""
    echo "==================================="
    echo "NAS Mount Configuration"
    echo "==================================="

    read -p "Enter NAS mount path (default: /mnt/medical-auth): " NAS_PATH
    NAS_PATH=${NAS_PATH:-/mnt/medical-auth}

    if [ ! -d "$NAS_PATH" ]; then
        echo "Creating directory: $NAS_PATH"
        sudo mkdir -p "$NAS_PATH"
    fi

    # Update .env file
    if [ -f ".env" ]; then
        sed -i "s|NAS_PATH=.*|NAS_PATH=$NAS_PATH|" .env
    else
        echo "NAS_PATH=$NAS_PATH" > .env
    fi

    echo -e "${GREEN}✓ NAS path configured: $NAS_PATH${NC}"
}

# Setup folder structure
setup_folders() {
    echo ""
    echo "Setting up folder structure..."
    chmod +x ../scripts/setup_folder_structure.sh
    sudo ../scripts/setup_folder_structure.sh
}

# Start containers
start_containers() {
    echo ""
    echo "Starting Docker containers..."
    docker compose up -d

    echo ""
    echo -e "${GREEN}✓ Containers started${NC}"
    docker compose ps
}

# Show access info
show_info() {
    echo ""
    echo "==================================="
    echo -e "${GREEN}Deployment Complete!${NC}"
    echo "==================================="
    echo ""
    echo "Access n8n at: http://localhost:5678"
    echo "Default credentials:"
    echo "  Username: admin"
    echo "  Password: (see .env file)"
    echo ""
    echo "Next steps:"
    echo "  1. Import workflow from ../workflow/medical-doc-automation.json"
    echo "  2. Place template files in: $NAS_PATH/01_Templates/"
    echo "  3. Create project folders with specs.json"
    echo "  4. Drop .docx files in requests/ folder to trigger automation"
    echo ""
}

# Main execution
main() {
    check_architecture
    check_docker
    setup_nas_mount
    setup_folders
    start_containers
    show_info
}

# Run main
main "$@"
