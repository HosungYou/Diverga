#!/bin/bash
#
# Diverga OpenCode Installer
# Installs Diverga for OpenCode
#
# Usage:
#   curl -sSL https://raw.githubusercontent.com/HosungYou/Diverga/main/scripts/install-opencode.sh | bash
#

set -e

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m'

REPO_URL="https://github.com/HosungYou/Diverga.git"
DEST_DIR="$HOME/.config/opencode/plugins/diverga"

echo -e "${CYAN}"
echo "╔═══════════════════════════════════════════════════════════════╗"
echo "║              Diverga Installer for OpenCode                   ║"
echo "╚═══════════════════════════════════════════════════════════════╝"
echo -e "${NC}"

# Clone repository
echo -e "${BLUE}[INFO]${NC} Cloning Diverga repository..."
TMP_DIR="/tmp/diverga-opencode-$$"
git clone --depth 1 "$REPO_URL" "$TMP_DIR" 2>/dev/null

PLUGIN_SRC="$TMP_DIR/.opencode/plugins/diverga"

# Check source exists
if [ ! -d "$PLUGIN_SRC" ]; then
    echo -e "${YELLOW}[!]${NC} OpenCode plugin not found in repository"
    rm -rf "$TMP_DIR"
    exit 1
fi

# Install
echo -e "${BLUE}[INFO]${NC} Installing to $DEST_DIR..."
mkdir -p "$DEST_DIR"

# Try to build if npm is available
if command -v npm &> /dev/null; then
    echo -e "${BLUE}[INFO]${NC} Building TypeScript plugin..."
    cd "$PLUGIN_SRC"
    
    if npm install --silent 2>/dev/null && npm run build --silent 2>/dev/null; then
        # Copy compiled files
        cp -r "$PLUGIN_SRC/dist/"* "$DEST_DIR/" 2>/dev/null || true
        cp "$PLUGIN_SRC/package.json" "$DEST_DIR/" 2>/dev/null || true
        echo -e "${GREEN}[✓]${NC} TypeScript build successful"
    else
        echo -e "${YELLOW}[!]${NC} Build failed, copying source files..."
        cp -r "$PLUGIN_SRC/"* "$DEST_DIR/"
    fi
else
    echo -e "${YELLOW}[!]${NC} npm not found, copying source files..."
    cp -r "$PLUGIN_SRC/"* "$DEST_DIR/"
fi

# Cleanup
rm -rf "$TMP_DIR"

echo ""
echo -e "${GREEN}[✓]${NC} Installation complete!"
echo ""
echo "Usage:"
echo "  opencode \"diverga:list\""
echo "  opencode \"diverga:agent A1\""
echo "  opencode \"diverga:checkpoint\""
echo ""
echo "Documentation: https://github.com/HosungYou/Diverga"
