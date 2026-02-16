---
name: diverga-setup
description: |
  Diverga v8.4.0 initial configuration wizard for Codex CLI.
  Simplified 2-step setup: Checkpoint Level + HUD preferences.
  LLM selection removed (Codex CLI is already authenticated).
  Triggers: setup, configure, install, first-time setup, 설정
metadata:
  short-description: Setup-Wizard
  version: 9.0.0
---

# Diverga Setup Wizard (Codex CLI)

**Version**: 8.4.0

## Overview

First-time setup wizard for Diverga on Codex CLI. Configures checkpoint preferences and project structure in 2 steps. LLM selection is not needed since Codex CLI provides its own model.

## Codex CLI Degraded Mode
This runs in Codex CLI's single-model mode. Key differences from Claude Code:
- No AskUserQuestion UI - uses text prompts for decisions
- No MCP tools - uses file-based configuration
- No HUD statusline - status via text output only

## Prerequisites

None. This is the pipeline entry point. Run before any agent.

## Checkpoint Protocol

Setup itself acts as a checkpoint gate. When asking the user for checkpoint level:
1. STOP and clearly mark: "CHECKPOINT: SETUP_CHECKPOINT_LEVEL"
2. Present options: [A] Full / [B] Minimal / [C] Off
3. WAIT for user response before continuing
4. Log decision: write to `.research/decision-log.yaml` using write_file

## Pipeline Position

```
diverga-setup (YOU ARE HERE)
  → diverga-memory init (if new project)
  → User describes research
  → Agent auto-trigger (A1, B1, C5, I0, etc.)
```

## Workflow

### Step 0: Project Detection
Check for existing project:
- If `.research/` exists: "Existing project detected. Upgrade to v8.4.0?"
- If `config/diverga-config.json` exists with older version: "Upgrade from vX.Y.Z?"
- Otherwise: "New project setup"

Check: read_file(".research/project-state.yaml") or read_file("config/diverga-config.json")

### Step 1: Welcome + Checkpoint Level

Display:
```
========================================
   Welcome to Diverga v8.4.0
   AI Research Assistant for Codex CLI
========================================
```

Ask user:
```
Select checkpoint level - how often should AI stop and ask for confirmation?

[A] Full (Recommended) - All 11 checkpoints enabled. AI stops at every critical decision.
[B] Minimal - Paradigm & Methodology checkpoints only. Faster progress.
[C] Off - Autonomous mode. No checkpoints. Not recommended for research.
```

WAIT for user response.

### Step 2: Project Initialization

After checkpoint selection:
1. Create `.research/` directory structure:
   ```
   .research/
   ├── baselines/
   │   ├── literature/
   │   ├── methodology/
   │   └── framework/
   ├── changes/
   │   ├── current/
   │   └── archive/
   ├── sessions/
   ├── project-state.yaml
   ├── decision-log.yaml
   └── checkpoints.yaml
   ```

2. Write configuration:
   - write_file(".research/project-state.yaml") with version, checkpoint level
   - write_file(".research/decision-log.yaml") with empty decisions list
   - write_file(".research/checkpoints.yaml") with checkpoint configuration

3. Log the checkpoint decision:
   - read_file(".research/decision-log.yaml")
   - Append: `{ checkpoint: "SETUP_CHECKPOINT_LEVEL", decision: "[selected]", timestamp: "..." }`
   - write_file(".research/decision-log.yaml")

4. Display completion:
   ```
   Setup complete!
   - Checkpoint level: [selected level]
   - Project structure: .research/ created
   - Next: describe your research to get started, or run diverga-memory init
   ```

## Configuration Files

### project-state.yaml
```yaml
version: "8.4.0"
platform: "codex-cli"
checkpoint_level: "full"  # full | minimal | off
created: "YYYY-MM-DD"
current_stage: null
paradigm: null
research_question: null
```

### decision-log.yaml
```yaml
decisions: []
# Each decision:
#   - checkpoint: "CP_NAME"
#     decision: "selected option"
#     rationale: "user's reasoning"
#     timestamp: "ISO datetime"
```

## Tool Mapping (Codex)
| Claude Code | Codex CLI |
|-------------|-----------|
| Read | read_file |
| Write | write_file |
| Bash | shell |
| AskUserQuestion | Text prompt + wait |

## Related Skills
- **diverga-help**: Show all agents and commands
- **diverga-memory**: Memory system management
