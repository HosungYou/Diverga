---
name: diverga-memory
description: |
  Diverga Memory System v7.0 for Codex CLI - Context-persistent research support.
  3-Layer context, checkpoint auto-trigger, cross-session continuity, decision audit trail.
  Commands: status, context, init, decision list/add, archive, migrate.
  Triggers: memory, remember, context, recall, checkpoint, decision, persist,
  기억, 맥락, 세션, 체크포인트
metadata:
  short-description: Memory-System
  version: 9.0.0
---

# Diverga Memory System (Codex CLI)

**Version**: 8.4.0

## Overview

Human-centered research context persistence with 3-Layer Context System, Checkpoint Auto-Trigger, Cross-Session Continuity, and Decision Audit Trail. Adapted for Codex CLI's file-based operation.

## Codex CLI Degraded Mode
This runs in Codex CLI's single-model mode. Key differences from Claude Code:
- No MCP tools - all state via file read/write
- No Layer 1 keyword triggers - must use explicit commands
- No Layer 2 Task interceptor - context loaded manually
- Layer 3 CLI commands work via text prompts

## Prerequisites

Requires `diverga-setup` to have been run first (`.research/` directory must exist).
If `.research/` does not exist, prompt: "Run diverga-setup first to initialize your project."

## Checkpoint Protocol

Memory commands that modify state should log to decision-log:
1. After `decision add`: write to `.research/decision-log.yaml` using write_file
2. After `archive`: log stage completion to `.research/decision-log.yaml`
3. After `init`: log project initialization

When any agent calls memory for context loading:
1. read_file(".research/project-state.yaml") — load current state
2. read_file(".research/decision-log.yaml") — load all prior decisions
3. Return context to the calling agent workflow

## Pipeline Position

```
diverga-setup → diverga-memory (YOU ARE HERE) → Agent execution
                     ↑                              ↓
                     └── context reload ←── decision logging
```

## Context Loading Keywords

When user mentions these keywords, load project context automatically:

**English**: "my research", "research status", "where was I", "continue research", "what stage"
**Korean**: "내 연구", "연구 진행", "연구 상태", "어디까지", "지금 단계"

Action: read_file(".research/project-state.yaml") and read_file(".research/decision-log.yaml")

## Commands

### status
Show project status.
```
Action: read_file(".research/project-state.yaml")
Display: version, stage, paradigm, research question, checkpoint progress
```

### context
Display full project context.
```
Action:
  1. read_file(".research/project-state.yaml")
  2. read_file(".research/decision-log.yaml")
  3. read_file(".research/priority-context.md") if exists
Display: Complete project state with all decisions and current progress
```

### init
Initialize new project.
```
Action:
  1. Ask for research topic/question
  2. Create .research/ directory structure via shell("mkdir -p ...")
  3. write_file(".research/project-state.yaml") with initial state
  4. write_file(".research/decision-log.yaml") with empty decisions
  5. write_file(".research/checkpoints.yaml") with defaults
```

### decision list
List all recorded decisions.
```
Action: read_file(".research/decision-log.yaml")
Display: Table of checkpoint decisions with timestamps
```

### decision add
Record a new decision.
```
Action:
  1. Ask for checkpoint name, decision, and rationale
  2. read_file(".research/decision-log.yaml")
  3. Append new decision entry
  4. write_file(".research/decision-log.yaml")
```

### archive [STAGE]
Archive completed stage.
```
Action:
  1. shell("mv .research/changes/current/* .research/changes/archive/STAGE/")
  2. Update project-state.yaml with new current stage
```

### migrate
Run migration from older versions.
```
Action:
  1. read_file("config/diverga-config.json") or read_file(".research/project-state.yaml")
  2. Detect version and apply migration steps
  3. Update to v8.4.0 format
```

## Priority Context (Compression Resilience)

Priority context is a 500-character summary stored at `.research/priority-context.md`.
Format: `Project: {name} | Paradigm: {paradigm} | RQ: {question} | Checkpoints: ... | Last: {decision}`

Auto-updated when decisions are recorded.

## Project Structure

```
.research/
├── baselines/           # Stable research foundations
│   ├── literature/
│   ├── methodology/
│   └── framework/
├── changes/
│   ├── current/         # Active work
│   └── archive/         # Completed stages
├── sessions/            # Session records
├── project-state.yaml   # Project metadata
├── decision-log.yaml    # All decisions
├── checkpoints.yaml     # Checkpoint states
└── priority-context.md  # 500-char summary
```

## Tool Mapping (Codex)
| Claude Code | Codex CLI |
|-------------|-----------|
| Read | read_file |
| Write | write_file |
| Bash | shell |
| MCP state tools | read_file/write_file on .research/ files |

## Related Skills
- **diverga-setup**: First-time configuration
- **diverga-help**: Show all agents and commands
