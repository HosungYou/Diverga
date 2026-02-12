# Diverga Platform Limitations v8.3.0

**Last Updated**: 2026-02-12

---

## Overview

Diverga v8.3.0 is designed primarily for Claude Code, with adapters for Codex CLI and OpenCode. This document details which features are fully portable, partially portable, or exclusive to Claude Code.

---

## Features by Portability

### Not Portable (Claude Code Only)

| Feature | Why | Impact |
|---------|-----|--------|
| Parallel agent execution | Requires Task tool to spawn separate agent instances | Agents run sequentially on other platforms |
| MCP runtime checkpoints | Requires MCP protocol (7 tools: `diverga_check_prerequisites`, `diverga_mark_checkpoint`, etc.) | Behavioral enforcement only on other platforms |
| AskUserQuestion structured UI | Claude Code native tool with clickable options | Text-based prompts instead |
| HUD statusline | Claude Code UI extension showing project name, stage, checkpoint progress | No visual progress indicator |
| Agent model isolation | Each agent runs as a separate instance with its own model tier | Single model handles all agents |
| 3-layer auto-loading memory | Keyword-triggered + Task interceptor + CLI-based context loading | Manual file reading required |

### Partially Portable (Degraded Mode)

| Feature | Claude Code | Codex CLI / OpenCode | Quality Retention |
|---------|------------|----------------------|-------------------|
| Checkpoint enforcement | Tool-level blocking via MCP + AskUserQuestion | Prompt-level behavioral (model should stop and ask) | ~80% |
| Memory system | 3-layer auto-loading with lifecycle hooks | Manual file reading from `.research/` | ~60% |
| Agent dispatch | Dedicated subagent via `Task(subagent_type="diverga:*")` | Main model follows SKILL.md instructions | ~70% |
| Parallel execution | 5-10 concurrent agents via Task tool | Sequential only within main model | ~40% |
| Model tier routing | Automatic per-agent (opus/sonnet/haiku) | Single session model (gpt-5.3-codex or gpt-5.2-codex) | ~50% |
| Decision audit trail | MCP auto-records to `.research/decision-log.yaml` | Manual file write by model | ~75% |
| Prerequisite gate | MCP `diverga_check_prerequisites()` verifies before execution | Model reads `.research/decision-log.yaml` manually | ~65% |
| Agent prerequisite map | Enforced via MCP + prompt instructions | Prompt instructions only | ~70% |

### Fully Portable

| Feature | Method |
|---------|--------|
| VS methodology (T-Score, 3-Phase) | Text-based, platform-independent |
| 44 agent definitions | SKILL.md text files (same content across platforms) |
| Checkpoint protocol | Prompt instructions with emoji markers |
| Korean language support | Unicode text, no platform dependency |
| Auto-trigger keywords | Skill description matching (all platforms support keyword triggers) |
| Research type support | All paradigms (quantitative, qualitative, mixed methods) via prompts |
| `.research/` directory structure | Standard file system, readable on all platforms |
| Decision log format | YAML files, platform-independent |
| PRISMA 2020 workflow | Text-based stage management |
| Humanization pipeline | Text analysis and transformation (G5 -> G6 -> F5) |

---

## Degraded Mode Patterns

### Sequential Execution

**Claude Code** (parallel, faster):
```python
# Three agents run simultaneously as separate instances
Task(subagent_type="diverga:b1", model="sonnet", prompt="Search literature...")
Task(subagent_type="diverga:b2", model="sonnet", prompt="Appraise quality...")
Task(subagent_type="diverga:b3", model="haiku", prompt="Extract effect sizes...")
# All three complete independently, results aggregated
```

**Codex CLI / OpenCode** (sequential, slower but functional):
```
# Main model handles each agent's role in sequence

## Step 1: B1-SystematicLiteratureScout
[Model reads diverga-b1/SKILL.md instructions]
[Performs literature search]
[Records results]

## Step 2: B2-EvidenceQualityAppraiser
[Model reads diverga-b2/SKILL.md instructions]
[Uses B1 results as input]
[Performs quality appraisal]

## Step 3: B3-EffectSizeExtractor
[Model reads diverga-b3/SKILL.md instructions]
[Uses B1+B2 results as input]
[Extracts effect sizes]
```

### Checkpoint Alternative

**Claude Code** (MCP-enforced):
```
1. Agent calls diverga_check_prerequisites("c5")
2. MCP returns {approved: false, missing: ["CP_METHODOLOGY_APPROVAL"]}
3. System invokes AskUserQuestion with structured options:
   ┌──────────────────────────────────────────────┐
   │  CP_METHODOLOGY_APPROVAL                     │
   │                                               │
   │  [A] Approve quantitative design              │
   │  [B] Approve qualitative design               │
   │  [C] Approve mixed methods design             │
   │  [D] Need more information                    │
   └──────────────────────────────────────────────┘
4. User clicks option -> decision recorded via MCP
5. Agent proceeds only after tool-level approval
```

**Codex CLI / OpenCode** (text-based):
```
1. Model reads SKILL.md prerequisite instructions
2. Model checks .research/decision-log.yaml for prior decisions
3. If prerequisite missing, model displays:

   CHECKPOINT: CP_METHODOLOGY_APPROVAL

   Your methodology needs approval before proceeding.
   Please choose:

   [A] Approve quantitative design (T=0.65)
   [B] Approve qualitative design (T=0.40)
   [C] Approve mixed methods design (T=0.35)

   Which approach would you like to proceed with?

4. Model waits for user text response
5. Model writes decision to .research/decision-log.yaml
6. Model proceeds with agent task
```

### Memory System Alternative

**Claude Code** (3-layer auto-loading):
```
Layer 1 (Keyword): User says "where was I?" ->
  System auto-loads .research/project-state.yaml

Layer 2 (Task): Task(subagent_type="diverga:*") ->
  Context auto-injected into agent prompt

Layer 3 (CLI): /diverga:memory context ->
  Full context display with decision history
```

**Codex CLI / OpenCode** (manual file reading):
```
# Model must explicitly read context files when needed:

1. At session start:
   - Read .research/project-state.yaml for current stage
   - Read .research/decision-log.yaml for past decisions

2. When user asks about progress:
   - Read .research/checkpoints.yaml for checkpoint states
   - Read .research/sessions/ for recent session records

3. When recording decisions:
   - Write to .research/decision-log.yaml manually
   - Update .research/project-state.yaml with new stage
```

---

## Category I (ScholaRAG) Platform Considerations

Category I agents (I0-I3) have additional platform considerations:

| Feature | Claude Code | Codex CLI / OpenCode |
|---------|------------|----------------------|
| Pipeline orchestration (I0) | Dedicated opus agent manages stages | Main model follows stage instructions |
| Paper retrieval (I1) | Parallel API calls via agent | Sequential API calls |
| Screening (I2) | MCP checkpoint for SCH_SCREENING_CRITERIA | Text-based checkpoint |
| RAG building (I3) | Agent runs embedding pipeline | Model guides user through CLI commands |
| SCH_* checkpoints | MCP-enforced, auto-recorded | Behavioral, manual recording |

---

## Recommendations

| Use Case | Recommended Platform | Reason |
|----------|---------------------|--------|
| Full research lifecycle | Claude Code | 100% feature compatibility, parallel agents, MCP checkpoints |
| Budget-conscious researchers | Codex CLI | Lower cost models, functional with degraded features |
| Open-source preference | OpenCode | Open-source platform, ~70% compatibility |
| Meta-analysis workflows | Claude Code | Parallel agents critical for C5->C6->C7 pipeline |
| Simple methodology consultation | Any platform | VS methodology and agent knowledge are fully portable |
| Literature review automation | Claude Code | I-category agents benefit from parallel execution and MCP checkpoints |
| Quick effect size calculation | Any platform | B3/C5 agents work well on all platforms |
| Humanization pipeline | Claude Code (preferred) | G5->G6->F5 sequential pipeline works on all, but benefits from agent isolation |

---

## Migration Between Platforms

### From Codex CLI to Claude Code

1. Your `.research/` directory is fully compatible -- no migration needed
2. Install Diverga on Claude Code (see [CROSS-PLATFORM-GUIDE.md](CROSS-PLATFORM-GUIDE.md))
3. All past decisions in `decision-log.yaml` are automatically recognized
4. Checkpoints upgrade from behavioral to MCP-enforced

### From Claude Code to Codex CLI

1. Your `.research/` directory is fully compatible
2. Install Codex skills (see [CROSS-PLATFORM-GUIDE.md](CROSS-PLATFORM-GUIDE.md))
3. Checkpoint enforcement downgrades from MCP to behavioral
4. Parallel execution becomes sequential
5. Review `.research/decision-log.yaml` to confirm all decisions are persisted

---

## Related Documents

- [CROSS-PLATFORM-GUIDE.md](CROSS-PLATFORM-GUIDE.md) - Installation and usage guide for all platforms
- [CODEX-SKILL-SYSTEM.md](CODEX-SKILL-SYSTEM.md) - Codex CLI skill system details
- [../adapters/README.md](../adapters/README.md) - Adapter templates for multi-CLI support
