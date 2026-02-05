#!/bin/bash
#
# Diverga Universal Installer
# Automatically detects and installs for Codex CLI, OpenCode, and Claude Code
#
# Usage:
#   curl -sSL https://raw.githubusercontent.com/HosungYou/Diverga/main/scripts/install.sh | bash
#   ./scripts/install.sh [codex|opencode|claude-code|all]
#

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Configuration
REPO_URL="https://github.com/HosungYou/Diverga.git"
VERSION="8.0.0"

# Print banner
print_banner() {
    echo -e "${CYAN}"
    echo "╔═══════════════════════════════════════════════════════════════╗"
    echo "║           Diverga Universal Installer v${VERSION}              ║"
    echo "║     Multi-Agent Research Coordinator for AI Coding Tools      ║"
    echo "╚═══════════════════════════════════════════════════════════════╝"
    echo -e "${NC}"
}

# Logging functions
log_info() { echo -e "${BLUE}[INFO]${NC} $1"; }
log_success() { echo -e "${GREEN}[✓]${NC} $1"; }
log_warn() { echo -e "${YELLOW}[!]${NC} $1"; }
log_error() { echo -e "${RED}[✗]${NC} $1"; }

# Detect available platforms
detect_platforms() {
    local platforms=()

    if command -v codex &> /dev/null || [ -d "$HOME/.codex" ]; then
        platforms+=("codex")
    fi

    if command -v opencode &> /dev/null || [ -d "$HOME/.opencode" ]; then
        platforms+=("opencode")
    fi

    if command -v claude &> /dev/null || [ -d "$HOME/.claude" ]; then
        platforms+=("claude-code")
    fi

    echo "${platforms[@]}"
}

# Clone or update repository
ensure_repo() {
    local tmp_dir="/tmp/diverga-install-$$"

    log_info "Fetching Diverga repository..."

    if [ -d "$tmp_dir" ]; then
        rm -rf "$tmp_dir"
    fi

    git clone --depth 1 "$REPO_URL" "$tmp_dir" 2>/dev/null || {
        log_error "Failed to clone repository"
        exit 1
    }

    echo "$tmp_dir"
}

# Install for Codex CLI
install_codex() {
    local src_dir="$1"
    local dest_dir="$HOME/.codex/diverga"

    log_info "Installing Diverga for Codex CLI..."

    mkdir -p "$dest_dir"

    cp -r "$src_dir/.codex/"* "$dest_dir/" 2>/dev/null || true
    cp "$src_dir/CLAUDE.md" "$dest_dir/" 2>/dev/null || true
    cp "$src_dir/AGENTS.md" "$dest_dir/" 2>/dev/null || true

    chmod +x "$dest_dir/diverga-codex.cjs" 2>/dev/null || true

    if node "$dest_dir/diverga-codex.cjs" help &>/dev/null; then
        log_success "Codex CLI installation complete: $dest_dir"
        echo ""
        echo "  Usage:"
        echo "    node ~/.codex/diverga/diverga-codex.cjs setup"
        echo "    node ~/.codex/diverga/diverga-codex.cjs list"
        echo ""
    else
        log_warn "Codex installation completed but verification failed"
    fi
}

# Install for OpenCode
install_opencode() {
    local src_dir="$1"
    local dest_dir="$HOME/.opencode/plugins/diverga"
    local plugin_src="$src_dir/.opencode/plugins/diverga"

    log_info "Installing Diverga for OpenCode..."

    if [ ! -d "$plugin_src" ]; then
        log_error "OpenCode plugin source not found"
        return 1
    fi

    mkdir -p "$dest_dir"

    if command -v npm &> /dev/null; then
        log_info "Building TypeScript plugin..."

        cd "$plugin_src"
        npm install --silent 2>/dev/null || true
        npm run build --silent 2>/dev/null || {
            log_warn "Build failed, copying source files instead"
            cp -r "$plugin_src/"* "$dest_dir/"
            return 0
        }

        cp -r "$plugin_src/dist/"* "$dest_dir/" 2>/dev/null || true
        cp "$plugin_src/package.json" "$dest_dir/" 2>/dev/null || true

        log_success "OpenCode installation complete (compiled): $dest_dir"
    else
        log_warn "npm not found, copying source files..."
        cp -r "$plugin_src/"* "$dest_dir/"
        log_success "OpenCode installation complete (source): $dest_dir"
    fi

    echo ""
    echo "  Usage:"
    echo "    opencode \"diverga:list\""
    echo "    opencode \"diverga:setup\""
    echo ""
}

# Install for Claude Code
install_claude_code() {
    local src_dir="$1"
    local dest_dir="$HOME/.claude/plugins/diverga"

    log_info "Installing Diverga for Claude Code..."

    mkdir -p "$dest_dir"

    if [ -d "$src_dir/.claude" ]; then
        cp -r "$src_dir/.claude/"* "$HOME/.claude/" 2>/dev/null || true
    fi

    if [ -d "$src_dir/skills" ]; then
        mkdir -p "$HOME/.claude/skills"
        cp -r "$src_dir/skills/"* "$HOME/.claude/skills/" 2>/dev/null || true
    fi

    cp "$src_dir/CLAUDE.md" "$dest_dir/" 2>/dev/null || true
    cp "$src_dir/AGENTS.md" "$dest_dir/" 2>/dev/null || true

    # === HUD Auto-Setup (v8.0 New Feature) ===
    log_info "Setting up Diverga HUD..."

    # 1. Install HUD script
    mkdir -p "$HOME/.claude/hud"
    if [ -f "$src_dir/dist/hud/diverga-hud.mjs" ]; then
        cp "$src_dir/dist/hud/diverga-hud.mjs" "$HOME/.claude/hud/"
        chmod +x "$HOME/.claude/hud/diverga-hud.mjs"
        log_success "HUD script installed: ~/.claude/hud/diverga-hud.mjs"
    else
        log_warn "HUD script not found in distribution"
    fi

    # 2. Configure settings.json for statusLine
    local settings_file="$HOME/.claude/settings.json"
    if [ -f "$settings_file" ]; then
        # Check if statusLine already configured
        if ! grep -q "statusLine" "$settings_file"; then
            # Add statusLine using jq if available
            if command -v jq &> /dev/null; then
                jq '. + {"statusLine": {"type": "command", "command": "node ~/.claude/hud/diverga-hud.mjs"}}' "$settings_file" > "${settings_file}.tmp" && mv "${settings_file}.tmp" "$settings_file"
                log_success "HUD statusLine configured in settings.json"
            else
                log_warn "jq not found. Add manually to ~/.claude/settings.json:"
                echo '    "statusLine": {"type": "command", "command": "node ~/.claude/hud/diverga-hud.mjs"}'
            fi
        else
            log_info "statusLine already configured in settings.json"
        fi
    else
        # Create settings.json with statusLine
        cat > "$settings_file" << 'SETTINGS_EOF'
{
  "statusLine": {
    "type": "command",
    "command": "node ~/.claude/hud/diverga-hud.mjs"
  }
}
SETTINGS_EOF
        log_success "Created settings.json with HUD statusLine"
    fi

    # 3. Create local skill symlinks
    log_info "Creating skill symlinks..."
    mkdir -p "$HOME/.claude/skills"
    local count=0
    for skill_dir in "$src_dir/skills/"*/; do
        if [ -d "$skill_dir" ]; then
            skill_name=$(basename "$skill_dir")
            target="$HOME/.claude/skills/diverga-${skill_name}"
            [ -L "$target" ] && rm "$target"
            ln -sf "$skill_dir" "$target"
            ((count++))
        fi
    done
    log_success "Created $count skill symlinks"

    log_success "Claude Code installation complete: $dest_dir"
    echo ""
    echo -e "${CYAN}  🔬 Diverga HUD is now active!${NC}"
    echo "  Restart Claude Code to see the statusline."
    echo ""
    echo "  Quick Start:"
    echo "    \"I want to conduct a systematic review on AI in education\""
    echo "    /diverga-help"
    echo ""
}

# Cleanup
cleanup() {
    local tmp_dir="$1"
    if [ -d "$tmp_dir" ]; then
        rm -rf "$tmp_dir"
    fi
}

# Main installation logic
main() {
    print_banner

    local target_platform="${1:-auto}"
    local tmp_dir=""

    tmp_dir=$(ensure_repo)
    trap "cleanup '$tmp_dir'" EXIT

    if [ "$target_platform" = "auto" ] || [ "$target_platform" = "all" ]; then
        local detected=($(detect_platforms))

        if [ ${#detected[@]} -eq 0 ]; then
            log_warn "No supported platforms detected"
            echo ""
            echo "Supported platforms:"
            echo "  - Codex CLI (codex command or ~/.codex directory)"
            echo "  - OpenCode (opencode command or ~/.opencode directory)"
            echo "  - Claude Code (claude command or ~/.claude directory)"
            echo ""
            echo "Install manually with:"
            echo "  ./install.sh codex"
            echo "  ./install.sh opencode"
            echo "  ./install.sh claude-code"
            exit 0
        fi

        log_info "Detected platforms: ${detected[*]}"
        echo ""

        for platform in "${detected[@]}"; do
            case "$platform" in
                codex) install_codex "$tmp_dir" ;;
                opencode) install_opencode "$tmp_dir" ;;
                claude-code) install_claude_code "$tmp_dir" ;;
            esac
            echo ""
        done
    else
        case "$target_platform" in
            codex) install_codex "$tmp_dir" ;;
            opencode) install_opencode "$tmp_dir" ;;
            claude-code|claude) install_claude_code "$tmp_dir" ;;
            *)
                log_error "Unknown platform: $target_platform"
                echo "Supported: codex, opencode, claude-code, all, auto"
                exit 1
                ;;
        esac
    fi

    echo -e "${GREEN}"
    echo "═══════════════════════════════════════════════════════════════"
    echo "              Installation Complete!"
    echo "═══════════════════════════════════════════════════════════════"
    echo -e "${NC}"
    echo ""
    echo "Documentation: https://github.com/HosungYou/Diverga"
    echo "Issues: https://github.com/HosungYou/Diverga/issues"
    echo ""
}

main "$@"
