#!/bin/bash
#
# Diverga Multi-CLI Installer
# Installs Diverga for Claude Code, Codex CLI, and OpenCode
#
# Usage:
#   curl -sSL https://raw.githubusercontent.com/HosungYou/Diverga/main/scripts/install-multi-cli.sh | bash
#
#   # Or install specific CLI only:
#   curl -sSL https://raw.githubusercontent.com/HosungYou/Diverga/main/scripts/install-multi-cli.sh | bash -s -- --claude
#   curl -sSL https://raw.githubusercontent.com/HosungYou/Diverga/main/scripts/install-multi-cli.sh | bash -s -- --codex
#   curl -sSL https://raw.githubusercontent.com/HosungYou/Diverga/main/scripts/install-multi-cli.sh | bash -s -- --opencode
#

set -e

GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m'

REPO_URL="https://github.com/HosungYou/Diverga.git"
VERSION="6.6.2"

# Parse arguments
INSTALL_CLAUDE=false
INSTALL_CODEX=false
INSTALL_OPENCODE=false

if [ $# -eq 0 ]; then
    # Default: install all
    INSTALL_CLAUDE=true
    INSTALL_CODEX=true
    INSTALL_OPENCODE=true
else
    while [[ $# -gt 0 ]]; do
        case $1 in
            --claude)
                INSTALL_CLAUDE=true
                shift
                ;;
            --codex)
                INSTALL_CODEX=true
                shift
                ;;
            --opencode)
                INSTALL_OPENCODE=true
                shift
                ;;
            --all)
                INSTALL_CLAUDE=true
                INSTALL_CODEX=true
                INSTALL_OPENCODE=true
                shift
                ;;
            *)
                echo -e "${RED}[ERROR]${NC} Unknown option: $1"
                echo "Usage: $0 [--claude] [--codex] [--opencode] [--all]"
                exit 1
                ;;
        esac
    done
fi

echo -e "${CYAN}"
echo "================================================================"
echo "       Diverga Multi-CLI Installer v${VERSION}"
echo "       Multi-agent Research Coordinator"
echo "================================================================"
echo -e "${NC}"

# Clone repository
echo -e "${BLUE}[INFO]${NC} Cloning Diverga repository..."
TMP_DIR="/tmp/diverga-multi-$$"
git clone --depth 1 "$REPO_URL" "$TMP_DIR" 2>/dev/null

# Track successful installations
INSTALLED_CLIS=()

# ============================================================
# Claude Code Installation
# ============================================================
if [ "$INSTALL_CLAUDE" = true ]; then
    echo ""
    echo -e "${CYAN}[1/3] Installing for Claude Code...${NC}"

    CLAUDE_DEST="$HOME/.claude/plugins/diverga"
    mkdir -p "$CLAUDE_DEST"

    # Copy agents (for Task tool subagent support)
    if [ -d "$TMP_DIR/agents" ]; then
        cp -r "$TMP_DIR/agents" "$CLAUDE_DEST/"
    fi

    # Copy skills
    if [ -d "$TMP_DIR/skills" ]; then
        cp -r "$TMP_DIR/skills" "$CLAUDE_DEST/"
    fi

    # Copy core files
    cp "$TMP_DIR/CLAUDE.md" "$CLAUDE_DEST/" 2>/dev/null || true
    cp "$TMP_DIR/PLUGIN.md" "$CLAUDE_DEST/" 2>/dev/null || true
    cp "$TMP_DIR/AGENTS.md" "$CLAUDE_DEST/" 2>/dev/null || true

    # Copy adapter settings
    if [ -f "$TMP_DIR/adapters/claude-settings.template.json" ]; then
        cp "$TMP_DIR/adapters/claude-settings.template.json" "$CLAUDE_DEST/settings.json"
    fi

    echo -e "${GREEN}[+]${NC} Claude Code: $CLAUDE_DEST"
    INSTALLED_CLIS+=("Claude Code")
fi

# ============================================================
# Codex CLI Installation
# ============================================================
if [ "$INSTALL_CODEX" = true ]; then
    echo ""
    echo -e "${CYAN}[2/3] Installing for Codex CLI...${NC}"

    CODEX_DEST="$HOME/.codex/diverga"
    CODEX_SKILLS="$HOME/.codex/skills/diverga"
    mkdir -p "$CODEX_DEST"
    mkdir -p "$CODEX_SKILLS"

    # Copy Codex-specific files
    if [ -d "$TMP_DIR/.codex" ]; then
        cp -r "$TMP_DIR/.codex/"* "$CODEX_DEST/" 2>/dev/null || true
    fi

    # Copy skills for Codex
    if [ -d "$TMP_DIR/skills/research-agents" ]; then
        cp -r "$TMP_DIR/skills/research-agents/"* "$CODEX_SKILLS/" 2>/dev/null || true
    fi

    # Copy adapter template
    if [ -f "$TMP_DIR/adapters/AGENTS.md.template" ]; then
        cp "$TMP_DIR/adapters/AGENTS.md.template" "$CODEX_DEST/AGENTS.md"
    fi

    # Copy core docs
    cp "$TMP_DIR/CLAUDE.md" "$CODEX_DEST/" 2>/dev/null || true
    cp "$TMP_DIR/AGENTS.md" "$CODEX_DEST/" 2>/dev/null || true

    # Make CLI helper executable
    chmod +x "$CODEX_DEST/diverga-codex.cjs" 2>/dev/null || true

    echo -e "${GREEN}[+]${NC} Codex CLI: $CODEX_DEST"
    echo -e "${GREEN}[+]${NC} Codex Skills: $CODEX_SKILLS"
    INSTALLED_CLIS+=("Codex CLI")
fi

# ============================================================
# OpenCode Installation
# ============================================================
if [ "$INSTALL_OPENCODE" = true ]; then
    echo ""
    echo -e "${CYAN}[3/3] Installing for OpenCode...${NC}"

    OPENCODE_DEST="$HOME/.config/opencode/plugins/diverga"
    mkdir -p "$OPENCODE_DEST"

    # Copy OpenCode-specific files
    if [ -d "$TMP_DIR/.opencode" ]; then
        cp -r "$TMP_DIR/.opencode/"* "$(dirname $OPENCODE_DEST)/" 2>/dev/null || true
    fi

    # Copy skills
    if [ -d "$TMP_DIR/skills" ]; then
        cp -r "$TMP_DIR/skills" "$OPENCODE_DEST/"
    fi

    # Copy agents
    if [ -d "$TMP_DIR/agents" ]; then
        cp -r "$TMP_DIR/agents" "$OPENCODE_DEST/"
    fi

    # Copy adapter template
    if [ -f "$TMP_DIR/adapters/oh-my-opencode.template.json" ]; then
        cp "$TMP_DIR/adapters/oh-my-opencode.template.json" "$(dirname $OPENCODE_DEST)/oh-my-opencode.json"
    fi

    # Try to build if npm is available
    if command -v npm &> /dev/null && [ -f "$OPENCODE_DEST/package.json" ]; then
        echo -e "${BLUE}[INFO]${NC} Building TypeScript plugin..."
        cd "$OPENCODE_DEST"
        if npm install --silent 2>/dev/null && npm run build --silent 2>/dev/null; then
            echo -e "${GREEN}[+]${NC} TypeScript build successful"
        fi
    fi

    echo -e "${GREEN}[+]${NC} OpenCode: $OPENCODE_DEST"
    INSTALLED_CLIS+=("OpenCode")
fi

# ============================================================
# Cleanup and Summary
# ============================================================
rm -rf "$TMP_DIR"

echo ""
echo -e "${GREEN}================================================================${NC}"
echo -e "${GREEN}       Installation Complete!${NC}"
echo -e "${GREEN}================================================================${NC}"
echo ""

# Show installed CLIs
echo -e "${BLUE}Installed for:${NC}"
for cli in "${INSTALLED_CLIS[@]}"; do
    echo -e "  ${GREEN}[+]${NC} $cli"
done

# Show usage
echo ""
echo -e "${BLUE}Quick Start:${NC}"

if [ "$INSTALL_CLAUDE" = true ]; then
    echo ""
    echo "  Claude Code:"
    echo "    claude \"Help me design a research study\""
    echo "    # Uses Task(subagent_type=\"diverga:a1\", ...)"
fi

if [ "$INSTALL_CODEX" = true ]; then
    echo ""
    echo "  Codex CLI:"
    echo "    node ~/.codex/diverga/diverga-codex.cjs setup"
    echo "    node ~/.codex/diverga/diverga-codex.cjs list"
fi

if [ "$INSTALL_OPENCODE" = true ]; then
    echo ""
    echo "  OpenCode:"
    echo "    opencode \"diverga:list\""
    echo "    opencode \"diverga:agent A1\""
fi

echo ""
echo -e "${BLUE}Documentation:${NC} https://github.com/HosungYou/Diverga"
echo ""
