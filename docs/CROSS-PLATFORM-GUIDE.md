# Diverga Cross-Platform Guide v8.3.0

**Last Updated**: 2026-02-12

---

## Overview

Diverga v8.3.0 supports three CLI platforms for AI-assisted research. This guide covers installation, usage, and platform-specific considerations for each platform.

---

## Platform Comparison

| Feature | Claude Code | Codex CLI | OpenCode |
|---------|-------------|-----------|----------|
| **Native Plugin** | Yes | SKILL.md files | oh-my-opencode |
| **Parallel Agents** | Yes (Task tool) | No (sequential) | No (sequential) |
| **MCP Checkpoints** | Yes (7 tools) | No (text-based) | No (hook-based) |
| **Structured UI** | AskUserQuestion | Text prompts | Text prompts |
| **Model Routing** | opus/sonnet/haiku | gpt-5.3-codex/gpt-5.2-codex/gpt-5.1-codex-mini | Provider-dependent |
| **Agent Count** | 44 (native) | 44 (skill files) | 44 (trigger config) |
| **Compatibility** | 100% | ~75% | ~70% |

---

## Installation

### Claude Code (Recommended)

Claude Code provides full native support through the plugin system or local skills.

**Method 1: Local Skills (Most Reliable)**

```bash
# Step 1: Clone repository
git clone https://github.com/HosungYou/Diverga.git
cd Diverga

# Step 2: Create local skill copies
for skill_dir in skills/*/; do
  skill_name=$(basename "$skill_dir")
  cp -r "$skill_dir" ~/.claude/skills/diverga-${skill_name}
done

# Step 3: Restart Claude Code

# Step 4: Verify
/diverga-help       # Should display help guide
```

**Method 2: Plugin Marketplace**

```bash
# Step 1: Add to marketplace
/plugin marketplace add https://github.com/HosungYou/Diverga

# Step 2: Install
/plugin install diverga

# Step 3: Configure
/diverga-setup
```

### Codex CLI

Codex CLI uses SKILL.md files for skill discovery. Each Diverga agent is represented as an individual skill file.

**Method 1: Install Script (Recommended)**

```bash
curl -fsSL https://raw.githubusercontent.com/HosungYou/Diverga/main/scripts/install-multi-cli.sh | bash -s -- --codex
```

**Method 2: NPM Package**

```bash
npx @diverga/codex-setup
```

**Method 3: Manual Setup**

```bash
# Copy skill files to Codex skills directory
git clone https://github.com/HosungYou/Diverga.git
cp -r Diverga/.codex/skills/* ~/.codex/skills/
```

**Skill Discovery**:

Codex CLI discovers skills from `~/.codex/skills/diverga-*/SKILL.md`. After installation, verify with:

```bash
ls ~/.codex/skills/diverga-*/SKILL.md | wc -l
# Expected: 44+ skill files
```

**Directory Structure**:

```
~/.codex/
└── skills/
    ├── diverga-a1/SKILL.md      # A1-ResearchQuestionRefiner
    ├── diverga-a2/SKILL.md      # A2-TheoreticalFrameworkArchitect
    ├── diverga-a3/SKILL.md      # A3-DevilsAdvocate
    ├── ...
    ├── diverga-i0/SKILL.md      # I0-ReviewPipelineOrchestrator
    ├── diverga-i1/SKILL.md      # I1-PaperRetrievalAgent
    ├── diverga-i2/SKILL.md      # I2-ScreeningAssistant
    ├── diverga-i3/SKILL.md      # I3-RAGBuilder
    ├── diverga-setup/SKILL.md   # Setup wizard
    ├── diverga-memory/SKILL.md  # Memory system
    └── diverga-help/SKILL.md    # Help guide
```

### OpenCode

OpenCode uses the oh-my-opencode plugin for agent configuration.

**Method 1: Install Script**

```bash
curl -fsSL https://raw.githubusercontent.com/HosungYou/Diverga/main/scripts/install-multi-cli.sh | bash -s -- --opencode
```

**Method 2: Manual Setup**

1. Copy the adapter template:
   ```bash
   cp adapters/oh-my-opencode.template.json ~/.config/opencode/oh-my-opencode.json
   ```
2. Edit `oh-my-opencode.json` to configure trigger keywords and model routing.
3. Restart OpenCode.

**Configuration** (`oh-my-opencode.json`):

The configuration file defines trigger keywords, model routing, and checkpoint enforcement for all 44 agents. Each agent entry maps trigger patterns to the corresponding agent instructions.

---

## Usage Patterns

### Agent Invocation

**Claude Code**:
```python
Task(subagent_type="diverga:a1", model="opus", prompt="Refine my research question about AI in education")
```

**Codex CLI**:
Use trigger keywords in your prompt, OR invoke skills explicitly:
```
$diverga-a1    # Explicit skill invocation
$diverga-c5    # Meta-analysis agent
```
The model matches user queries to skill descriptions and activates the relevant agent.

**OpenCode**:
Use trigger keywords in your prompt, OR invoke commands:
```
/diverga-a1    # Explicit command invocation
/diverga-c5    # Meta-analysis agent
```

### Checkpoint Handling

**Claude Code** (MCP-enforced):
1. Agent calls `diverga_check_prerequisites(agent_id)` via MCP
2. System triggers `AskUserQuestion` with structured selection UI
3. User clicks an option to proceed
4. Decision recorded to `.research/decision-log.yaml`
5. Cannot be bypassed without user action

**Codex CLI / OpenCode** (text-based):
1. Agent displays checkpoint marker in text output
2. Presents options as lettered choices:
   ```
   CHECKPOINT: CP_RESEARCH_DIRECTION
   Choose your research direction:

   [A] Quantitative approach (T=0.65)
   [B] Qualitative approach (T=0.40)
   [C] Mixed methods (T=0.35)

   Which direction would you like to proceed?
   ```
3. Model waits for user response before continuing
4. Behavioral enforcement (model should wait, but technically could continue)

### Memory System

**All platforms** use the `.research/` directory for persistent state:

```
.research/
├── project-state.yaml     # Project metadata and current stage
├── decision-log.yaml      # Human decisions at checkpoints
├── checkpoints.yaml       # Checkpoint completion states
├── baselines/             # Stable research foundations
├── changes/               # Active work and archive
└── sessions/              # Session records
```

**Claude Code**: 3-layer auto-loading (keyword-triggered, Task interceptor, CLI-based)

**Codex CLI / OpenCode**: Manual file reading. The model reads `.research/decision-log.yaml` when context is needed:
```
# When user says "where was I?" or "continue research":
# Model reads .research/project-state.yaml for current stage
# Model reads .research/decision-log.yaml for past decisions
```

### Sequential Execution (Codex CLI / OpenCode)

Where Claude Code runs agents in parallel via Task tool, Codex CLI and OpenCode must run agents sequentially within the main model context.

**Claude Code** (parallel):
```python
# Three agents run simultaneously
Task(subagent_type="diverga:b1", model="sonnet", prompt="...")  # Parallel
Task(subagent_type="diverga:b2", model="sonnet", prompt="...")  # Parallel
Task(subagent_type="diverga:b3", model="haiku", prompt="...")   # Parallel
```

**Codex CLI / OpenCode** (sequential):
```
Step 1: Activate B1-SystematicLiteratureScout
  → Complete literature search
  → Record results

Step 2: Activate B2-EvidenceQualityAppraiser
  → Appraise evidence quality using B1 results
  → Record appraisal

Step 3: Activate B3-EffectSizeExtractor
  → Extract effect sizes from appraised papers
  → Record extractions
```

The model follows each agent's SKILL.md instructions in sequence, carrying context between steps.

---

## VS Methodology (All Platforms)

VS (Verbalized Sampling) methodology works identically across all platforms since it is entirely text-based.

### T-Score (Typicality Score)

| T-Score | Label | Meaning |
|---------|-------|---------|
| >= 0.7 | Common | Highly typical, safe but limited novelty |
| 0.4-0.7 | Moderate | Balanced risk-novelty |
| 0.2-0.4 | Innovative | Novel, requires strong justification |
| < 0.2 | Experimental | Highly novel, high risk/reward |

### VS Process (3 Phases)

```
Phase 1: Context & Modal Identification
  Identify the "obvious" recommendation that most AI tools would give

Phase 2: Divergent Exploration
  Direction A (T~0.6): Safe but differentiated
  Direction B (T~0.4): Balanced novelty
  Direction C (T<0.3): Innovative/experimental

Phase 3: Human Selection (CHECKPOINT)
  Present ALL options with T-Scores
  WAIT for human decision
  Execute ONLY selected direction
```

This process is text-based and works on every platform without degradation.

---

## Troubleshooting

### Claude Code

| Issue | Solution |
|-------|----------|
| Skills not found | Run `ls ~/.claude/skills/diverga-*` to verify installation |
| Plugin not loading | Try local skills method instead of marketplace |
| Checkpoints skipped | Verify MCP server is running; check `.research/` state files |
| Hyphen vs colon | Use `/diverga-help` (hyphen) for reliability |

### Codex CLI

| Issue | Solution |
|-------|----------|
| Skills not loading | Check `~/.codex/skills/` directory exists and contains SKILL.md files |
| Checkpoints skipped | Reinforce checkpoint behavior in AGENTS.md context; checkpoints are behavioral, not tool-enforced |
| Wrong model used | Codex uses session model; tier routing in SKILL.md is advisory only |
| Agent not activating | Ensure trigger keywords in SKILL.md description match user query |
| Prerequisite not checked | Verify `.research/decision-log.yaml` is readable; add prerequisite reminders to SKILL.md |

### OpenCode

| Issue | Solution |
|-------|----------|
| Triggers not firing | Check `oh-my-opencode.json` configuration; verify keyword mappings |
| Hooks not working | Verify hook paths in config; ensure scripts are executable |
| Memory not loading | Manually read `.research/project-state.yaml` at session start |
| Agent instructions missing | Ensure oh-my-opencode plugin has full agent definitions |

### All Platforms

| Issue | Solution |
|-------|----------|
| `.research/` missing | Run `/diverga-setup` or manually create the directory structure |
| Decision log corrupted | Check YAML syntax in `.research/decision-log.yaml` |
| Context lost between sessions | Verify `.research/project-state.yaml` is being updated |

---

## Related Documents

- [PLATFORM-LIMITATIONS.md](PLATFORM-LIMITATIONS.md) - Detailed feature portability analysis
- [CODEX-SKILL-SYSTEM.md](CODEX-SKILL-SYSTEM.md) - Codex CLI skill system documentation
- [SETUP.md](SETUP.md) - Initial setup guide
- [TROUBLESHOOTING.md](TROUBLESHOOTING.md) - General troubleshooting
