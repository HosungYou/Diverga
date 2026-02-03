# Codex CLI Skill System: Technical Documentation

**Version**: 6.6.2
**Last Updated**: 2026-01-30
**Status**: Verified Working

---

## Executive Summary

Diverga v6.6.2 introduces full **Codex CLI compatibility** through the SKILL.md-based skill loading system. This document explains:

1. How Codex CLI discovers and loads skills
2. Why AGENTS.md alone is insufficient
3. The solution implemented in Diverga
4. Key differences between Codex CLI and Claude Code
5. Recommendations for users

---

## The Problem: AGENTS.md is Not Enough

### Initial Misconception

Many developers assume that placing an `AGENTS.md` file in their project root will enable skill/agent functionality in Codex CLI. **This is incorrect.**

### AGENTS.md vs SKILL.md

| Feature | AGENTS.md | SKILL.md |
|---------|-----------|----------|
| **Purpose** | Passive documentation | Active skill definition |
| **Loading** | Context injection only | Skill system activation |
| **Behavior** | Guidelines for model behavior | Callable skill with triggers |
| **Structure** | Free-form Markdown | YAML frontmatter required |
| **Discovery** | Read during session | Explicit skill discovery |

**AGENTS.md** provides context and guidance to the model but does NOT register capabilities in the skill system.

**SKILL.md** is the actual skill definition file that Codex CLI discovers and loads into its active skill registry.

---

## How Codex CLI Skill Loading Works

### Discovery Paths

Codex CLI looks for SKILL.md files in these locations:

1. **Global**: `~/.codex/skills/<skill-name>/SKILL.md`
2. **Project-local**: `.codex/skills/<skill-name>/SKILL.md`

### SKILL.md Format

```yaml
---
name: skill-name
description: Short description (max 500 chars) that determines trigger keywords
metadata:
  short-description: Brief label
  version: X.Y.Z
---

# Skill Title

[Skill instructions and content follow...]
```

### Key Requirements

| Field | Required | Constraint |
|-------|----------|------------|
| `name` | Yes | Max 100 characters |
| `description` | Yes | Max 500 characters, includes trigger keywords |
| `metadata` | Optional | Additional metadata |

### Activation Methods

1. **Explicit**: Use `$skill-name` or `/skills` command
2. **Implicit**: Model matches user query to skill description keywords
3. **Context**: Skill activates when relevant context detected

---

## Diverga Solution: .codex/skills/ Directory

### Structure Created

```
.codex/
└── skills/
    ├── research-coordinator/
    │   └── SKILL.md         # Main coordinator (40 agents)
    ├── meta-analysis/
    │   └── SKILL.md         # C5-MetaAnalysisMaster agent
    └── checkpoint-system/
        └── SKILL.md         # Human checkpoint enforcement
```

### Skill Definitions

#### research-coordinator/SKILL.md

```yaml
---
name: research-coordinator
description: AI research assistant with 40 specialized agents, VS methodology,
             and human checkpoints. Triggers on meta-analysis, systematic review,
             research question, theoretical framework, literature review, PRISMA,
             qualitative, phenomenology, grounded theory, mixed methods, effect size
metadata:
  short-description: Diverga Research Coordinator v6.6.2
  version: 6.6.2
---
```

#### meta-analysis/SKILL.md

```yaml
---
name: meta-analysis
description: Meta-analysis specialist for effect size extraction, heterogeneity
             analysis, and PRISMA workflow. Triggers on meta-analysis, effect size,
             Hedges g, Cohen d, I-squared, heterogeneity, forest plot, funnel plot
metadata:
  short-description: C5-MetaAnalysisMaster Agent
  version: 6.6.2
---
```

#### checkpoint-system/SKILL.md

```yaml
---
name: checkpoint-system
description: Human checkpoint enforcement for research decisions. Ensures AI stops
             at critical decision points and waits for human approval. Use when
             research direction, methodology, or analysis decisions are needed.
metadata:
  short-description: Human Checkpoint Enforcement
  version: 6.6.2
---
```

---

## Verification: QUANT-005 Test Results

### Test Scenario

The QUANT-005 test verified that Codex CLI properly:
1. Discovers skills from `.codex/skills/`
2. Activates skills based on trigger keywords
3. Displays checkpoint markers (🔴/🟠/🟡)
4. Presents VS T-Score options
5. Supports Korean language

### Turn 1 Results

**User Query**: "AI 튜터링 시스템이 학생 성취도에 미치는 효과에 대한 메타분석을 수행하려고 합니다."

**Codex Response**:
```
✅ meta-analysis 스킬(C5-MetaAnalysisMaster) 사용 — 효과크기 통일 체크포인트 진행

🔴 CHECKPOINT: CP_EFFECT_SIZE_SELECTION
효과크기 지표 옵션입니다:

[A] Cohen's d (T=0.65) - 가장 일반적
[B] Hedges' g (T=0.40) - 소표본 편향 보정, 메타분석 표준 ⭐
[C] Glass's Δ (T=0.25) - 대조군 SD만 사용

어떤 지표로 통일하시겠습니까?
```

### Turn 2 Results

**User Query**: "Hedges' g를 사용하겠습니다. F통계량에서 Hedges' g로 어떻게 변환하나요?"

**Codex Response**:
```
✅ C5-MetaAnalysisMaster 활성화됨
- 다단계 게이트 검증 시스템
- 효과크기 변환 및 계산
- PRISMA 2020 워크플로우

F에서 Hedges' g 변환은 **설계와 df**가 중요합니다...

**1) 두 독립집단 비교 (df1=1, t‑test와 동치)**
- t = √F
- d = t × √(1/n1 + 1/n2)
- J = 1 − 3/(4·df − 1), df = n1 + n2 − 2
- g = J × d
```

### Verification Summary

| Verification Point | QUANT-004 (No SKILL.md) | QUANT-005 (With SKILL.md) |
|--------------------|-------------------------|---------------------------|
| Skill activation message | ❌ Not present | ✅ "✅ meta-analysis 스킬 사용" |
| Checkpoint marker | ❌ Not present | ✅ "🔴 CHECKPOINT: CP_EFFECT_SIZE_SELECTION" |
| VS T-Score options | ❌ Not present | ✅ [A] T=0.65, [B] T=0.40 ⭐, [C] T=0.25 |
| Behavioral halt | ❌ Continued without asking | ✅ "어떤 지표로 통일하시겠습니까?" |
| Korean language | ✅ Supported | ✅ Supported |

---

## Claude Code vs Codex CLI: Feature Comparison

### Capability Matrix

| Feature | Claude Code | Codex CLI |
|---------|-------------|-----------|
| **Skill Loading** | Native plugin system | SKILL.md files |
| **Task Tool** | ✅ Full support | ❌ Not available |
| **AskUserQuestion Tool** | ✅ Clickable UI | ❌ Text-only |
| **Checkpoint Enforcement** | ✅ Tool-level blocking | ⚠️ Behavioral only |
| **Agent Dispatch** | ✅ `Task(subagent_type="diverga:a1")` | ❌ Main model handles all |
| **Parallel Agents** | ✅ Multiple Task calls | ❌ Sequential only |
| **Context Persistence** | ✅ Full session context | ✅ Session context |
| **VS Methodology** | ✅ T-Score options | ✅ T-Score options |
| **Korean Support** | ✅ Full | ✅ Full |

### What This Means

| Aspect | Claude Code | Codex CLI |
|--------|-------------|-----------|
| **Checkpoint Blocking** | System prevents proceeding | Model chooses to wait |
| **Agent Execution** | Dedicated agent instances | Main model follows instructions |
| **User Interaction** | Rich UI components | Plain text prompts |
| **Reliability** | Tool-enforced behavior | Prompt-guided behavior |

---

## Recommendations

### For Full Diverga Experience

**Use Claude Code** when you need:
- Tool-level checkpoint enforcement (cannot bypass)
- 40 specialized agents via Task tool
- AskUserQuestion with clickable options
- Parallel agent execution
- Highest reliability research workflows

### For Basic Research Assistance

**Codex CLI works well** for:
- Effect size calculations and conversions
- Literature review guidance
- Methodology consultation
- VS methodology (creative alternatives)
- Korean language support

### Installation Guide

#### Claude Code (Recommended)

```bash
# Full plugin installation
/plugin marketplace add https://github.com/HosungYou/Diverga
/plugin install diverga
```

#### Codex CLI (Basic Support)

```bash
# Option 1: NPM package (recommended)
npx @diverga/codex-setup

# Option 2: Shell script
curl -fsSL https://raw.githubusercontent.com/HosungYou/Diverga/main/scripts/install-multi-cli.sh | bash -s -- --codex

# Option 3: Manual
# Copy .codex/skills/ to your project or ~/.codex/skills/
```

---

## Technical Notes

### Why Behavioral vs Tool-Level Matters

**Tool-Level Checkpoint (Claude Code)**:
```
System: 🔴 CHECKPOINT triggered
→ Claude Code UI blocks further input
→ User MUST click option to continue
→ Impossible to bypass without user action
```

**Behavioral Checkpoint (Codex CLI)**:
```
Model: 🔴 CHECKPOINT displayed
→ Model asks "어떤 방향으로 진행하시겠습니까?"
→ Model SHOULD wait for response
→ Technically model could continue (rare, but possible)
```

### SKILL.md Best Practices

1. **Keep description under 500 characters** - Codex truncates longer descriptions
2. **Include all trigger keywords** - These determine when skill activates
3. **Use clear activation messages** - "✅ Skill 활성화됨" helps users confirm loading
4. **Provide behavioral instructions** - Clear "DO" and "DON'T" sections

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 6.6.2 | 2026-01-30 | Initial Codex SKILL.md implementation |
| - | - | QUANT-005 verification complete |
| - | - | Documentation created |

---

## Related Documents

- [README.md](../README.md) - Main Diverga documentation
- [CHANGELOG.md](../CHANGELOG.md) - Version history
- [qa/protocol/test_quant_005.yaml](../qa/protocol/test_quant_005.yaml) - Test protocol
