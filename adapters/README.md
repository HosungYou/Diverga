# Diverga CLI Adapters

This directory contains adapter templates for multi-CLI compatibility.

## Overview

Diverga supports three CLI tools, each with different invocation patterns:

| CLI Tool | Native Support | Adapter Template |
|----------|----------------|------------------|
| Claude Code | Task tool subagents | `claude-settings.template.json` |
| Codex CLI | SKILL.md files (2025.12) | `AGENTS.md.template` |
| OpenCode | oh-my-opencode | `oh-my-opencode.template.json` |

## Files

### `AGENTS.md.template`

Codex CLI bootstrap template. This file is copied to `~/.codex/diverga/AGENTS.md` during installation.

**Key Features:**
- Complete agent catalog (40 agents)
- Tool mapping (Claude Code tools to Codex equivalents)
- Checkpoint protocol documentation
- VS methodology reference
- Auto-trigger keywords

**Note:** Codex CLI does not support native subagents like Claude Code's Task tool. Instead, agents are invoked by reading skill files and following their instructions.

### `oh-my-opencode.template.json`

OpenCode configuration for oh-my-opencode plugin compatibility.

**Key Features:**
- Full trigger configuration for all 40 agents
- Model routing (opus/sonnet/haiku)
- Checkpoint enforcement settings
- Command definitions
- Hook configurations

### `claude-settings.template.json`

Claude Code plugin settings template.

**Key Features:**
- Agent directory configuration
- Skill directory configuration
- Model routing
- Checkpoint levels
- Category definitions

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

## CLI Compatibility Matrix

| Feature | Claude Code | Codex CLI | OpenCode |
|---------|-------------|-----------|----------|
| **Plugin System** | Native | 2025.12 Skills | oh-my-opencode |
| **Task Tool (Subagents)** | Native | Not supported | Supported |
| **SKILL.md Format** | Native | 2025.12 Added | Compatible |
| **Agent Invocation** | `diverga:a1` | Read skill file | `diverga:a1` |
| **Parallel Execution** | Full | Not supported | Full |
| **Model Routing** | opus/sonnet/haiku | o1/gpt-4/gpt-3.5 | opus/sonnet/haiku |

## Customization

These templates can be customized for specific deployment scenarios:

1. Copy the template to your target location
2. Modify settings as needed
3. Restart the CLI tool to apply changes

## Version

Adapter templates version: 6.6.2 (2026-01-29)
