---
name: setup
description: |
  Diverga v8.0 initial configuration wizard. Simplified 2-step setup.
  Sets up checkpoints and HUD preferences.
  Triggers: setup, configure, 설정, install
version: "9.0.0"
---

# /diverga:setup

**Version**: 8.4.0
**Trigger**: `/diverga:setup`

## Description

Diverga v8.0 simplified setup wizard. 2 steps: Checkpoint Level + HUD.
LLM selection removed (Claude Code is already authenticated).

## Workflow

When user invokes `/diverga:setup`, execute this interactive wizard:

### Step 0: Project Detection

Check for existing project:
- If `.research/` exists → "Existing project detected. Upgrade to v8.4.0?"
- If `config/diverga-config.json` exists with older version → "Upgrade from vX.Y.Z to v8.4.0?"
- Otherwise → "New project setup"

### Step 1: Welcome + Checkpoint Level

Display welcome message, then ask checkpoint level using AskUserQuestion:

```
╔══════════════════════════════════════════════════════════════════╗
║                    Welcome to Diverga v8.4.0                    ║
║         AI Research Assistant for the Complete Lifecycle         ║
╚══════════════════════════════════════════════════════════════════╝
```

```
question: "Select checkpoint level - how often should AI stop and ask for confirmation on research decisions?"
header: "Checkpoints"
options:
  - label: "Full (Recommended)"
    description: "All 11 checkpoints enabled. AI stops at every critical decision."
  - label: "Minimal"
    description: "Paradigm & Methodology checkpoints only. Faster progress, key decisions confirmed."
  - label: "Off"
    description: "Autonomous mode. No checkpoints. Not recommended for research."
```

### Step 2: HUD Configuration

```
question: "Enable Diverga HUD statusline?"
header: "HUD"
options:
  - label: "Research (Recommended)"
    description: "Shows project name, stage, checkpoint progress, memory health."
  - label: "Minimal"
    description: "Compact display with stage and progress only."
  - label: "Off"
    description: "No HUD display."
```

### Step 3: Generate Configuration & Complete

After collecting all preferences, generate `config/diverga-config.json`:

```json
{
  "version": "8.4.0",
  "human_checkpoints": {
    "enabled": true,
    "level": "<full|minimal|off>",
    "required": ["CP_PARADIGM", "CP_METHODOLOGY", ...],
    "optional": [...]
  },
  "hud": {
    "enabled": true,
    "preset": "<research|minimal|off>"
  },
  "language": "en",
  "model_routing": {
    "high": "opus",
    "medium": "sonnet",
    "low": "haiku"
  }
}
```

Display completion:

```
╔══════════════════════════════════════════════════════════════════╗
║                   Diverga v8.4.0 Setup Complete!                ║
╠══════════════════════════════════════════════════════════════════╣
║  Configuration saved to: config/diverga-config.json             ║
║                                                                  ║
║  Quick Start:                                                    ║
║  • Just describe your research in natural language               ║
║  • "I want to conduct a systematic review on AI in education"    ║
║  • Diverga will auto-detect and guide you with checkpoints       ║
║                                                                  ║
║  Commands:                                                       ║
║  • /diverga:help     - View all 44 agents                       ║
║  • /diverga:memory   - Memory system commands                    ║
╚══════════════════════════════════════════════════════════════════╝
```

## Error Handling

If config directory doesn't exist, create it:
```bash
mkdir -p config
```
