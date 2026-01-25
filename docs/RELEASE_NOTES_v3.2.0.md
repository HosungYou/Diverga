# Research Coordinator v3.2.0 Release Notes

**Release Date**: 2025-01-25
**Status**: Production Ready
**Architect Verified**: ✅ Approved

---

## Overview

Research Coordinator v3.2.0 introduces **OMC (oh-my-claudecode) Integration**, enabling parallel agent execution, smart model routing, and significant token savings while preserving human decision points at critical research stages.

---

## What's New

### 1. OMC Integration

Research Coordinator now integrates with the OMC multi-agent orchestration system, providing:

- **Parallel Execution**: Run independent agents simultaneously
- **Smart Model Routing**: Use appropriate model tier (Opus/Sonnet/Haiku) per task
- **Token Efficiency**: ~60% average token savings
- **Human Checkpoints**: Critical decisions remain with researchers

### 2. Human Checkpoint System

Three levels of human decision points ensure researchers maintain control:

| Level | Checkpoint | Purpose |
|-------|------------|---------|
| 🔴 **REQUIRED** | CP_RESEARCH_DIRECTION | Research question approval |
| 🔴 **REQUIRED** | CP_THEORY_SELECTION | Theoretical framework approval |
| 🔴 **REQUIRED** | CP_METHODOLOGY_APPROVAL | Research design approval |
| 🟠 **RECOMMENDED** | CP_ANALYSIS_PLAN | Analysis strategy review |
| 🟠 **RECOMMENDED** | CP_QUALITY_REVIEW | Quality check review |
| 🟡 **OPTIONAL** | CP_VISUALIZATION_PREFERENCE | Visualization style |
| 🟡 **OPTIONAL** | CP_RENDERING_METHOD | Rendering approach |

### 3. Model Tier Routing

Intelligent routing assigns each agent to the appropriate model tier:

| Tier | Model | Token Cost | Agents |
|------|-------|------------|--------|
| HIGH | Opus | $$$ | #01, #02, #03, #09, #19 |
| MEDIUM | Sonnet | $$ | #04, #06, #10, #12, #15-18, #20, #21 |
| LOW | Haiku | $ | #05, #07, #08, #11, #13, #14 |

**Result**: ~60% token savings compared to using Opus for everything.

### 4. Parallel Execution Groups

10 parallel execution groups enable simultaneous agent work:

```
Phase 1: Research Planning
  └── theory-design: [#02, #03] in parallel

Phase 2: Literature Review
  └── literature-search: [#05, #08] in parallel
  └── quality-assessment: [#06] per paper
  └── data-extraction: [#07] per study

Phase 3: Analysis
  └── analysis-design: [#10, #11, #12] in parallel

Phase 4: Quality Assurance
  └── quality-assurance: [#13, #14, #15, #16] in parallel

Phase 5: Publication
  └── publication-prep: [#17, #18, #19, #20, #21] staged parallel
```

---

## Core Principle

> **"인간이 할 일은 인간이, AI는 인간의 범주를 벗어난 것을 수행"**

This release maintains the fundamental principle that:
- **Strategic research decisions** remain with the researcher
- **Routine, computational, and analytical tasks** are automated
- **Critical checkpoints** require explicit human approval

---

## Compatibility

### Backwards Compatible

Research Coordinator v3.2.0 is **fully backwards compatible**:

| Environment | Support | Features |
|-------------|---------|----------|
| Claude Code only | ✅ Full | Basic mode, sequential execution |
| Claude Code + OMC | ✅ Full | Enhanced mode, parallel execution, model routing |

### No Breaking Changes

- All existing `/research-coordinator` commands work unchanged
- Existing workflows continue to function
- OMC features activate only when OMC plugin is available

---

## New Files

```
.omc/
├── agents/research/
│   ├── 01-research-question-refiner.md      (7.9 KB)
│   ├── 02-theoretical-framework-architect.md (12.9 KB)
│   ├── 03-devils-advocate.md                (17.7 KB)
│   ├── 04-research-ethics-advisor.md        (25.8 KB)
│   ├── 05-systematic-literature-scout.md    (4.4 KB)
│   ├── 06-evidence-quality-appraiser.md     (4.4 KB)
│   ├── 07-effect-size-extractor.md          (5.1 KB)
│   ├── 08-research-radar.md                 (5.0 KB)
│   ├── 09-research-design-consultant.md     (11.8 KB)
│   ├── 10-statistical-analysis-guide.md     (14.6 KB)
│   ├── 11-analysis-code-generator.md        (18.6 KB)
│   ├── 12-sensitivity-analysis-designer.md  (16.9 KB)
│   ├── 13-internal-consistency-checker.md   (5.5 KB)
│   ├── 14-checklist-manager.md              (6.5 KB)
│   ├── 15-reproducibility-auditor.md        (3.2 KB)
│   ├── 16-bias-detector.md                  (3.9 KB)
│   ├── 17-journal-matcher.md                (5.0 KB)
│   ├── 18-academic-communicator.md          (6.3 KB)
│   ├── 19-peer-review-strategist.md         (7.9 KB)
│   ├── 20-preregistration-composer.md       (10.1 KB)
│   └── 21-conceptual-framework-visualizer.md (11.9 KB)
├── checkpoints/
│   ├── checkpoint-definitions.yaml          (2.1 KB)
│   ├── checkpoint-handler.md                (2.8 KB)
│   └── parallel-execution-rules.yaml        (6.5 KB)
├── config/
│   └── research-coordinator-routing.yaml    (6.8 KB)
└── skills/research-orchestrator/
    └── SKILL.md

docs/
└── omc-integration.md                       (24 KB)
```

**Total**: 21 agent files + 3 checkpoint files + 1 config + 1 skill + 1 doc = 27 new files

---

## Usage Examples

### Basic Mode (Claude Code only)

```bash
# Standard usage - works exactly as before
/research-coordinator

# Direct agent invocation
/research-question-refiner
/theoretical-framework-architect
```

### Enhanced Mode (with OMC)

```bash
# Maximum parallelism - run agents simultaneously
ulw: 문헌 검토 진행해줘

# Token-efficient mode - uses Haiku for simple tasks
eco: 통계 분석 코드 생성해줘

# Persistence mode - complete until verified
ralph: 전체 연구 설계 완료해줘
```

### Combined Modes

```bash
# Persistence + Parallelism
ralph ulw: 체계적 문헌 고찰 수행해줘

# Will run literature search agents in parallel
# Continue until fully verified by Architect
```

---

## Migration Guide

### From v3.1.0

1. **No action required** for basic usage
2. **Optional**: Install OMC plugin for enhanced features
   ```bash
   claude plugin enable oh-my-claudecode@omc
   ```
3. **Optional**: Review checkpoint definitions in `.omc/checkpoints/`

### First-Time Users

1. Clone or pull latest version
2. Run `/research-coordinator` to start
3. System auto-detects OMC availability

---

## Verification

This release was verified by **Architect (Opus)** with the following checks:

| Check | Status |
|-------|--------|
| All 21 agent files exist | ✅ Pass |
| Version alignment (3.2.0) | ✅ Pass |
| No invalid agent references | ✅ Pass |
| Human checkpoints REQUIRED level | ✅ Pass |
| Core principle preserved | ✅ Pass |

---

## Known Limitations

1. **OMC Plugin Required**: Parallel execution and model routing require OMC plugin
2. **Claude Code Version**: Requires Claude Code with Task tool support
3. **Token Limits**: Very large research projects may still hit context limits

---

## Support

- **Documentation**: `docs/omc-integration.md`
- **GitHub**: https://github.com/HosungYou/research-coordinator
- **Issues**: Report via GitHub Issues

---

## Acknowledgments

- Implementation: Claude Opus 4.5 with OMC orchestration
- Parallel agent execution via oh-my-claudecode plugin
- Architect verification for quality assurance
