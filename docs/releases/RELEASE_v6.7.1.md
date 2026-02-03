# Diverga v6.7.1 Release Notes

**Release Date**: 2026-01-31
**Type**: Documentation Synchronization
**Previous Version**: 6.7.0

---

## Overview

Diverga v6.7.1 is a documentation synchronization release that aligns all core documentation files with the v6.7.0 architecture. This release ensures consistent versioning, agent counts, and checkpoint definitions across CLAUDE.md, AGENTS.md, and all SKILL.md files.

**Core Achievement**: Complete documentation parity across 4 key files with 44 agents verified.

---

## What's Changed

### Version Alignment

| Document | Before | After |
|----------|--------|-------|
| `AGENTS.md` | v6.5 (37 agents stated) | **v6.7.0** (44 agents) |
| `skills/research-coordinator/SKILL.md` | v6.0.0 (27 agents) | **v6.7.0** (44 agents) |
| `skills/research-orchestrator/SKILL.md` | v2.0.0 (27 agents) | **v2.7.0** (44 agents) |
| `CLAUDE.md` | v6.7.0 | v6.7.0 (SCH_PRISMA_GENERATION added) |

### AGENTS.md Updates

**Previously Missing Agents Now Documented**:

| Agent | Name | Category | Model |
|-------|------|----------|-------|
| B5 | ParallelDocumentProcessor | Evidence | Opus |
| F5 | HumanizationVerifier | Quality | Haiku |
| G5 | AcademicStyleAuditor | Communication | Sonnet |
| G6 | AcademicStyleHumanizer | Communication | Opus |

**Updated Sections**:
- Agent Registry: 33 → 44 agents (9 categories)
- Model Routing: Updated counts (17 HIGH, 18 MEDIUM, 9 LOW)
- Auto-Trigger Keywords: B5, F5, G5, G6 keywords added
- Version History: v6.1-v6.7 additions documented

### research-coordinator SKILL.md Updates

**Major Additions**:
- Agent Catalog expanded from 27 to 44 agents
- Category I (ScholaRAG) agents fully documented
- ScholaRAG Integration section with:
  - Pipeline stages diagram
  - Human checkpoints table (SCH_*)
  - Cost optimization guide
  - Auto-trigger keywords

**New Checkpoints Added**:
| Checkpoint | Level | Agent |
|------------|-------|-------|
| CP_META_GATE | 🔴 | C5 |
| SCH_DATABASE_SELECTION | 🔴 | I1 |
| SCH_SCREENING_CRITERIA | 🔴 | I2 |

### research-orchestrator SKILL.md Updates

**Checkpoint System Expansion**:

```yaml
REQUIRED_CHECKPOINTS:
  - CP_RESEARCH_DIRECTION
  - CP_PARADIGM_SELECTION
  - CP_THEORY_SELECTION
  - CP_METHODOLOGY_APPROVAL
  - CP_META_GATE          # NEW
  - SCH_DATABASE_SELECTION  # NEW
  - SCH_SCREENING_CRITERIA  # NEW

RECOMMENDED_CHECKPOINTS:
  - CP_ANALYSIS_PLAN
  - CP_INTEGRATION_STRATEGY
  - CP_QUALITY_REVIEW
  - CP_HUMANIZATION_REVIEW  # NEW
  - META_TIER3_REVIEW       # NEW
  - META_ANOMALY_REVIEW     # NEW
  - SCH_RAG_READINESS       # NEW

OPTIONAL_CHECKPOINTS:
  - CP_VISUALIZATION_PREFERENCE
  - CP_RENDERING_METHOD
  - CP_HUMANIZATION_VERIFY  # NEW
  - META_PRETEST_CONFIRM    # NEW
  - SCH_PRISMA_GENERATION   # NEW
```

**Agent-Tier Reference**: Updated from 27 to 44 agents with complete model assignments.

### CLAUDE.md Updates

**Single Addition**:
- SCH_PRISMA_GENERATION checkpoint added to Human Checkpoints section

---

## Files Modified

| File | Lines Changed | Summary |
|------|---------------|---------|
| `AGENTS.md` | +64 / -0 | B5, F5, G5, G6 agents, version sync |
| `skills/research-coordinator/SKILL.md` | +138 / -0 | 44 agents, Category I, checkpoints |
| `skills/research-orchestrator/SKILL.md` | +67 / -0 | 44 agents, SCH_* checkpoints |
| `CLAUDE.md` | +1 / -0 | SCH_PRISMA_GENERATION |
| **Total** | **+270 / -0** | |

## Files Created

| File | Purpose |
|------|---------|
| `qa/reports/verification_report_v6.7.0.md` | Architecture verification report |
| `docs/releases/RELEASE_v6.7.1.md` | This release notes file |

---

## Verification Summary

All verification checks passed:

| Check | Expected | Actual | Status |
|-------|----------|--------|--------|
| Agent files in `agents/` | 44 | 44 | ✅ |
| Agent IDs in CLAUDE.md | 44 | 44 | ✅ |
| Agent IDs in AGENTS.md | 44 | 44 | ✅ |
| Agent IDs in SKILL.md | 44 | 44 | ✅ |
| Version consistency | v6.7.0 | v6.7.0 | ✅ |
| Checkpoints synced | 10+ | 10+ | ✅ |

---

## Migration Notes

### From v6.7.0

No migration required. This is a documentation-only release with no code changes or breaking changes.

### From v6.5.x or Earlier

If referencing AGENTS.md for agent counts:
- Update agent count expectations from 37 to 44
- Add Category I (I0-I3) to any agent detection logic

---

## Agent Count by Category (Final)

| Category | Name | Count |
|----------|------|-------|
| A | Foundation | 6 |
| B | Evidence | 5 |
| C | Design & Meta-Analysis | 7 |
| D | Data Collection | 4 |
| E | Analysis | 5 |
| F | Quality | 5 |
| G | Communication | 6 |
| H | Specialized | 2 |
| I | Systematic Review Automation | 4 |
| **Total** | | **44** |

---

## Model Routing (Final)

| Tier | Model | Count | Agents |
|------|-------|-------|--------|
| HIGH | Opus | 17 | A1, A2, A3, A5, B5, C1, C2, C3, C5, D4, E1, E2, E3, G3, G6, H1, H2, I0 |
| MEDIUM | Sonnet | 18 | A4, A6, B1, B2, C4, C6, C7, D1, D2, E5, F3, F4, G1, G2, G4, G5, I1, I2 |
| LOW | Haiku | 9 | B3, B4, D3, E4, F1, F2, F5, I3 |

---

## Contributors

- Architecture review and implementation by Claude Code
- Codex review (gpt-5.2-codex) for version consistency analysis

---

*This release is part of the Diverga v2.0.0 documentation review initiative.*
