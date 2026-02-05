---
name: setup
description: |
  Diverga v8.0 initial configuration wizard. Simplified 3-step setup.
  Sets up checkpoints, HUD, and language preferences.
  Triggers: setup, configure, 설정, install
version: "8.0.0"
---

# /diverga-setup

**Version**: 8.0.0
**Trigger**: `/diverga-setup` or `/diverga:setup`

## Description

Simplified 3-step configuration wizard for Diverga v8.0.

**Changes from v7.0**:
- Removed LLM selection (Claude Code is already authenticated)
- Removed API key configuration (not needed)
- Added HUD configuration
- Simplified to 3 steps (was 9)

## Workflow

When user invokes `/diverga-setup`, execute this interactive wizard:

### Step 1: Welcome + Project Detection

First, detect if there's an existing `.research/` directory:

```bash
# Check for existing project
if [[ -d ".research" ]]; then
  echo "✅ Existing Diverga project detected"
  PROJECT_EXISTS="true"
else
  echo "📁 New project setup"
  PROJECT_EXISTS="false"
fi
```

Display welcome message:

```
╔══════════════════════════════════════════════════════════════════╗
║                    Welcome to Diverga v8.0                       ║
║         AI Research Assistant for the Complete Lifecycle         ║
╚══════════════════════════════════════════════════════════════════╝

프로젝트 확인 중...
→ [Existing project detected / New project setup]
```

If existing project:
```
┌─────────────────────────────────────────────────────────────────┐
│ ✅ 기존 프로젝트 감지됨                                          │
├─────────────────────────────────────────────────────────────────┤
│ Project: [project_name]                                         │
│ Stage: [current_stage]                                          │
│ Last updated: [timestamp]                                       │
│                                                                 │
│ 설정을 업데이트하시겠습니까?                                     │
└─────────────────────────────────────────────────────────────────┘
```

### Step 2: Settings (Single Screen)

Use AskUserQuestion tool with multiple questions:

**Question 1: Checkpoint Level**

```
question: "🚦 체크포인트 레벨을 선택하세요"
header: "Checkpoints"
multiSelect: false
options:
  - label: "Full (권장)"
    description: "모든 11개 체크포인트 활성화. AI가 모든 중요 결정에서 멈추고 확인을 요청합니다."
  - label: "Minimal"
    description: "패러다임 & 방법론 체크포인트만. 빠른 진행, 핵심 결정만 확인."
  - label: "Off"
    description: "자율 모드. 체크포인트 없이 진행. 연구에 권장하지 않음."
```

**Question 2: HUD Display**

```
question: "📊 HUD 표시를 활성화하시겠습니까?"
header: "HUD"
multiSelect: false
options:
  - label: "활성화 (권장)"
    description: "터미널 하단에 연구 진행 상태를 항상 표시합니다."
  - label: "비활성화"
    description: "깔끔한 인터페이스. HUD 없이 진행합니다."
```

**Question 3: Language**

```
question: "🌐 응답 언어를 선택하세요"
header: "Language"
multiSelect: false
options:
  - label: "Auto (입력에 맞춤)"
    description: "사용자 입력 언어에 맞춰 응답합니다."
  - label: "English"
    description: "항상 영어로 응답합니다."
  - label: "한국어"
    description: "항상 한국어로 응답합니다."
```

### Step 3: Apply Configuration

After collecting preferences:

1. **Create config directory**:
```bash
mkdir -p ~/.claude/plugins/diverga/config
mkdir -p .research
```

2. **Install local skill symlinks** (if not already done):
```bash
DIVERGA_PATH=""
if [[ -d "$HOME/.claude/plugins/cache/diverga" ]]; then
  DIVERGA_PATH=$(find "$HOME/.claude/plugins/cache/diverga" -type d -name "skills" | head -1)
elif [[ -d "/Volumes/External SSD/Projects/Diverga/skills" ]]; then
  DIVERGA_PATH="/Volumes/External SSD/Projects/Diverga/skills"
elif [[ -d "./Diverga/skills" ]]; then
  DIVERGA_PATH="$(pwd)/Diverga/skills"
fi

if [[ -n "$DIVERGA_PATH" ]]; then
  mkdir -p ~/.claude/skills
  count=0
  for skill_dir in "$DIVERGA_PATH"/*/; do
    skill_name=$(basename "$skill_dir")
    target="$HOME/.claude/skills/diverga-${skill_name}"
    [[ -L "$target" ]] && rm "$target"
    ln -sf "$skill_dir" "$target"
    ((count++))
  done
  echo "✅ Created $count local skill symlinks"
fi
```

3. **Generate configuration file**:

`~/.claude/plugins/diverga/config/diverga-config.json`:
```json
{
  "version": "8.0.0",
  "human_checkpoints": {
    "level": "<full|minimal|off>",
    "enabled": true,
    "required": ["CP_PARADIGM_SELECTION", "CP_METHODOLOGY_APPROVAL"],
    "optional": ["CP_THEORY_SELECTION", "CP_VARIABLE_DEFINITION"]
  },
  "hud": {
    "enabled": true,
    "preset": "research"
  },
  "language": "auto",
  "model_routing": {
    "high": "opus",
    "medium": "sonnet",
    "low": "haiku"
  }
}
```

4. **Initialize HUD state** (if HUD enabled):
```bash
# Create HUD state file
cat > .research/hud-state.json << 'EOF'
{
  "version": "1.0.0",
  "enabled": true,
  "preset": "research",
  "last_updated": "$(date -u +%Y-%m-%dT%H:%M:%SZ)",
  "cache": {
    "project_name": "",
    "current_stage": "foundation",
    "checkpoints_completed": 0,
    "checkpoints_total": 11,
    "memory_health": 100
  }
}
EOF
```

5. **Setup HUD statusline** (if HUD enabled):

**IMPORTANT**: When user selects "활성화 (권장)" for HUD, automatically configure statusLine:

```bash
mkdir -p ~/.claude/hud

# Copy HUD script from Diverga installation
DIVERGA_HUD_SRC=""
if [[ -f "/Volumes/External SSD/Projects/Diverga/dist/hud/diverga-hud.mjs" ]]; then
  DIVERGA_HUD_SRC="/Volumes/External SSD/Projects/Diverga/dist/hud/diverga-hud.mjs"
elif [[ -f "$HOME/.claude/plugins/cache/diverga/dist/hud/diverga-hud.mjs" ]]; then
  DIVERGA_HUD_SRC="$HOME/.claude/plugins/cache/diverga/dist/hud/diverga-hud.mjs"
elif [[ -f "./Diverga/dist/hud/diverga-hud.mjs" ]]; then
  DIVERGA_HUD_SRC="$(pwd)/Diverga/dist/hud/diverga-hud.mjs"
fi

# Copy or create HUD script
if [[ -n "$DIVERGA_HUD_SRC" ]]; then
  cp "$DIVERGA_HUD_SRC" ~/.claude/hud/diverga-hud.mjs
  chmod +x ~/.claude/hud/diverga-hud.mjs
  echo "✅ HUD script installed"
elif [[ ! -f ~/.claude/hud/diverga-hud.mjs ]]; then
  echo "⚠️ HUD script not found. Run /diverga-hud setup to install."
fi

# AUTO-CONFIGURE settings.json statusLine
SETTINGS_FILE="$HOME/.claude/settings.json"
if [[ -f "$SETTINGS_FILE" ]]; then
  # Check if statusLine already configured
  if ! grep -q "statusLine" "$SETTINGS_FILE"; then
    # Add statusLine configuration using jq or manual edit
    if command -v jq &> /dev/null; then
      jq '. + {"statusLine": {"type": "command", "command": "node ~/.claude/hud/diverga-hud.mjs"}}' "$SETTINGS_FILE" > "${SETTINGS_FILE}.tmp" && mv "${SETTINGS_FILE}.tmp" "$SETTINGS_FILE"
      echo "✅ HUD statusLine configured in settings.json"
    else
      echo "⚠️ jq not found. Please add manually to settings.json:"
      echo '  "statusLine": {"type": "command", "command": "node ~/.claude/hud/diverga-hud.mjs"}'
    fi
  else
    echo "✅ statusLine already configured"
  fi
else
  # Create settings.json with statusLine
  cat > "$SETTINGS_FILE" << 'SETTINGS_EOF'
{
  "statusLine": {
    "type": "command",
    "command": "node ~/.claude/hud/diverga-hud.mjs"
  }
}
SETTINGS_EOF
  echo "✅ Created settings.json with HUD statusLine"
fi

echo ""
echo "🔄 HUD가 활성화되었습니다. Claude Code를 재시작하면 statusLine이 표시됩니다."
```

6. **Display completion message**:

```
╔══════════════════════════════════════════════════════════════════╗
║                   Diverga 설정 완료! ✅                          ║
╠══════════════════════════════════════════════════════════════════╣
║  설정이 저장되었습니다.                                          ║
║                                                                  ║
║  📁 Config: ~/.claude/plugins/diverga/config/diverga-config.json ║
║  📁 Project: .research/                                          ║
║                                                                  ║
║  시작하려면:                                                     ║
║  • "AI 윤리에 대한 체계적 문헌고찰을 하고 싶어요"                 ║
║  • "메타분석 연구를 시작할게요: [주제]"                          ║
║                                                                  ║
║  명령어:                                                         ║
║  • /diverga-status  - 프로젝트 상태                              ║
║  • /diverga-hud     - HUD 설정                                   ║
║  • /diverga-help    - 전체 도움말                                ║
╚══════════════════════════════════════════════════════════════════╝
```

## Checkpoint Levels

| Level | Checkpoints | Description |
|-------|-------------|-------------|
| **Full** | 11 | All checkpoints active. AI stops at every critical decision. |
| **Minimal** | 2 | CP_PARADIGM_SELECTION + CP_METHODOLOGY_APPROVAL only. |
| **Off** | 0 | No checkpoints. Not recommended for research. |

## Configuration File Schema

```json
{
  "version": "8.0.0",
  "human_checkpoints": {
    "level": "full",
    "enabled": true,
    "required": [
      "CP_RESEARCH_DIRECTION",
      "CP_PARADIGM_SELECTION",
      "CP_SCOPE_DEFINITION",
      "CP_THEORY_SELECTION",
      "CP_VARIABLE_DEFINITION",
      "CP_METHODOLOGY_APPROVAL",
      "CP_DATABASE_SELECTION",
      "CP_SCREENING_CRITERIA",
      "CP_ANALYSIS_PLAN",
      "CP_QUALITY_GATES",
      "CP_PUBLICATION_READY"
    ],
    "optional": []
  },
  "hud": {
    "enabled": true,
    "preset": "research"
  },
  "language": "auto",
  "model_routing": {
    "high": "opus",
    "medium": "sonnet",
    "low": "haiku"
  }
}
```

## Error Handling

### No Write Permission

```
❌ 설정 파일을 저장할 수 없습니다.

권한을 확인해주세요:
  ls -la ~/.claude/plugins/diverga/config/
```

### Existing Configuration

If config exists, ask before overwriting:

```
question: "기존 설정이 있습니다. 덮어쓰시겠습니까?"
header: "Config"
options:
  - label: "예, 새 설정으로 교체"
    description: "기존 설정을 백업하고 새 설정을 적용합니다."
  - label: "아니요, 유지"
    description: "기존 설정을 유지합니다."
```

## Migration from v7.0

If `diverga-config.json` exists with v7.0 format:

1. Backup existing config to `diverga-config.v7.backup.json`
2. Migrate settings:
   - `llm_provider` → removed (not needed in v8.0)
   - `llm_api_key_env` → removed
   - `human_checkpoints` → kept, add `level` field
   - `default_paradigm` → kept in project-state.yaml
   - `language` → kept
   - `model_routing` → kept

## Notes

- **LLM Selection Removed**: Claude Code already provides authenticated access to Claude models. No API key configuration needed.
- **HUD Integration**: New in v8.0. Provides statusline display of research progress.
- **Simplified Flow**: 3 steps instead of 9. Faster setup experience.
- **Project Detection**: Automatically detects existing `.research/` directory.
