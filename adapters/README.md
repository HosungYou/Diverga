# Diverga CLI Adapters

This directory contains adapter templates for multi-CLI compatibility.

## Overview

Diverga v8.3.0 supports three CLI tools, each with different invocation patterns:

| CLI Tool | Native Support | Adapter Template |
|----------|----------------|------------------|
| Claude Code | Task tool subagents | `claude-settings.template.json` |
| Codex CLI | SKILL.md files (individual per agent) | `AGENTS.md.template` |
| OpenCode | oh-my-opencode | `oh-my-opencode.template.json` |

## Files

### `AGENTS.md.template`

Codex CLI bootstrap template. This file is copied to `~/.codex/diverga/AGENTS.md` during installation.

**Key Features:**
- Complete agent catalog (44 agents across 9 categories, A-I)
- Tool mapping (Claude Code tools to Codex equivalents)
- Checkpoint protocol documentation
- VS methodology reference
- Auto-trigger keywords
- Category I (ScholaRAG) integration with SCH_* checkpoints

**Note:** Codex CLI does not support native subagents like Claude Code's Task tool. Instead, each agent has its own individual SKILL.md file under `~/.codex/skills/diverga-*/SKILL.md`, and the main model follows skill instructions when activated.

### `oh-my-opencode.template.json`

OpenCode configuration for oh-my-opencode plugin compatibility.

**Key Features:**
- Full trigger configuration for all 44 agents (9 categories)
- Model routing (opus/sonnet/haiku)
- Checkpoint enforcement settings
- Command definitions
- Hook configurations
- Category I agent triggers (SCH_* checkpoints)

### `claude-settings.template.json`

Claude Code plugin settings template.

**Key Features:**
- Agent directory configuration
- Skill directory configuration
- Model routing
- Checkpoint levels
- Category definitions (A-I, 9 categories)

## Installation

Use the unified installer:

```bash
# Install for all CLI tools
curl -sSL https://raw.githubusercontent.com/HosungYou/Diverga/main/scripts/install-multi-cli.sh | bash

# Or install for specific CLI
./scripts/install-multi-cli.sh --claude
./scripts/install-multi-cli.sh --codex
./scripts/install-multi-cli.sh --opencode
```

### Codex CLI: Individual Skill Files

For Codex CLI, the installer creates individual SKILL.md files for each agent:

```
~/.codex/
└── skills/
    ├── diverga-a1/SKILL.md    # A1-ResearchQuestionRefiner
    ├── diverga-a2/SKILL.md    # A2-TheoreticalFrameworkArchitect
    ├── ...
    ├── diverga-i0/SKILL.md    # I0-ReviewPipelineOrchestrator
    ├── diverga-i1/SKILL.md    # I1-PaperRetrievalAgent
    ├── diverga-i2/SKILL.md    # I2-ScreeningAssistant
    ├── diverga-i3/SKILL.md    # I3-RAGBuilder
    ├── diverga-setup/SKILL.md
    ├── diverga-memory/SKILL.md
    └── diverga-help/SKILL.md
```

## CLI Compatibility Matrix

| Feature | Claude Code | Codex CLI | OpenCode |
|---------|-------------|-----------|----------|
| **Plugin System** | Native | Individual SKILL.md files | oh-my-opencode |
| **Task Tool (Subagents)** | Native | Not supported | Supported |
| **SKILL.md Format** | Native | Individual per agent | Compatible |
| **Agent Invocation** | `diverga:a1` | `$diverga-a1` / keyword trigger | `diverga:a1` |
| **Parallel Execution** | Full | Not supported | Full |
| **Model Routing** | opus/sonnet/haiku | gpt-5.3-codex/gpt-5.2-codex/gpt-5.1-codex-mini | opus/sonnet/haiku |
| **Agent Count** | 44 (9 categories) | 44 (9 categories) | 44 (9 categories) |
| **MCP Checkpoints** | 7 MCP tools | Not supported (behavioral) | Not supported (hook-based) |
| **Category I (ScholaRAG)** | Full with SCH_* MCP checkpoints | Behavioral SCH_* checkpoints | Hook-based SCH_* checkpoints |

## Category I: ScholaRAG Integration

Category I agents (I0-I3) provide PRISMA 2020 systematic review automation:

| Agent | Purpose | Checkpoint |
|-------|---------|------------|
| I0-ReviewPipelineOrchestrator | Pipeline coordination | All SCH_* |
| I1-PaperRetrievalAgent | Multi-database fetching | SCH_DATABASE_SELECTION |
| I2-ScreeningAssistant | AI-PRISMA screening | SCH_SCREENING_CRITERIA |
| I3-RAGBuilder | Vector database construction | SCH_RAG_READINESS |

These agents are available on all platforms but benefit most from Claude Code's MCP checkpoint enforcement.

## Customization

These templates can be customized for specific deployment scenarios:

1. Copy the template to your target location
2. Modify settings as needed
3. Restart the CLI tool to apply changes

## Version

Adapter templates version: 8.3.0 (2026-02-12)
