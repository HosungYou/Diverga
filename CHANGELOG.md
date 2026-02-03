# Changelog

All notable changes to Diverga (formerly Research Coordinator) will be documented in this file.

---

## [7.0.0] - 2026-02-03 (Memory System Global Deployment)

### Overview

**Diverga Memory System v7.0** - Complete research context persistence system with 3-layer context loading, checkpoint auto-trigger, cross-session continuity, and research documentation automation.

This release introduces a comprehensive Python library (`lib/memory/`) that enables researchers to maintain context across sessions, enforce human-in-the-loop decisions at critical checkpoints, and auto-generate research documentation.

### New Features

#### 1. 3-Layer Context System

| Layer | Trigger | Purpose |
|-------|---------|---------|
| **Layer 1: Keyword-Triggered** | "my research", "연구 진행" | Auto-load context when researcher asks |
| **Layer 2: Task Interceptor** | `Task(subagent_type="diverga:*")` | Inject full context into agent prompts |
| **Layer 3: CLI** | `/diverga:memory context` | Explicit context access |

**Bilingual Support**: 15 English + 15 Korean trigger keywords

#### 2. Checkpoint Auto-Trigger System

```yaml
Checkpoint Levels:
  🔴 REQUIRED:    Must complete before proceeding
  🟠 RECOMMENDED: Strongly suggested
  🟡 OPTIONAL:    Can skip with defaults
```

17 standard checkpoints across research workflow:
- `CP_RESEARCH_DIRECTION`, `CP_PARADIGM_SELECTION`, `CP_THEORY_SELECTION`
- `CP_METHODOLOGY_APPROVAL`, `CP_DATABASE_SELECTION`, `CP_SCREENING_CRITERIA`
- ScholaRAG-specific: `SCH_DATABASE_SELECTION`, `SCH_SCREENING_CRITERIA`, etc.

#### 3. Cross-Session Persistence

- **Session Tracking**: UUID-based session management
- **Decision Audit Trail**: Append-only, immutable decision log with versioning
- **Stage Archiving**: Timestamped archives with auto-generated summaries

#### 4. Dual-Tree Filesystem Structure

```
.research/
├── baselines/           # STABLE TREE (verified foundations)
│   ├── literature/
│   ├── methodology/
│   └── framework/
├── changes/
│   ├── current/         # WORKING TREE (in-progress)
│   └── archive/         # Completed stages
├── sessions/
├── project-state.yaml
├── decision-log.yaml
└── checkpoints.yaml
```

#### 5. Research Documentation System

- **Schema-driven artifacts**: YAML schemas define artifact dependencies
- **Jinja2-like templates**: Protocol, PRISMA diagram, manuscript templates
- **Auto-generation**: Generate artifacts based on research context

#### 6. Migration Support (v6.8 → v7.0)

```bash
# Preview changes
/diverga:memory migrate --dry-run

# Execute migration
/diverga:memory migrate
```

### New Files

#### Core Library (`lib/memory/src/`)

| File | Purpose | Lines |
|------|---------|-------|
| `models.py` | Data models (ResearchContext, Checkpoint, Decision) | ~250 |
| `context_trigger.py` | Layer 1: Keyword-triggered context | ~460 |
| `task_interceptor.py` | Layer 2: Agent context injection | ~290 |
| `checkpoint_trigger.py` | Checkpoint auto-trigger | ~300 |
| `fs_state.py` | Filesystem state management | ~200 |
| `dual_tree.py` | Dual-tree structure | ~250 |
| `archive.py` | Stage archiving | ~200 |
| `decision_log.py` | Decision audit trail | ~280 |
| `session_hooks.py` | Session lifecycle | ~250 |
| `schema.py` | Research schema definitions | ~300 |
| `templates.py` | Template engine | ~280 |
| `artifact_generator.py` | Artifact generation | ~300 |
| `cli.py` | CLI commands | ~760 |
| `migration.py` | v6.8 → v7.0 migration | ~350 |
| `memory_api.py` | Unified facade API (23 methods) | ~400 |

#### Templates (`templates/`)

| Directory | Files | Purpose |
|-----------|-------|---------|
| `systematic-review/` | 8 files | PRISMA 2020 templates |
| `meta-analysis/` | 4 files | Meta-analysis templates |
| `checkpoints/` | 1 file | 17 checkpoint definitions |

#### Documentation

| File | Purpose |
|------|---------|
| `lib/memory/README.md` | Comprehensive library documentation |
| `skills/memory/SKILL.md` | Skill definition for Claude Code |

### API Reference

**MemoryAPI** - 23 methods:

```python
from lib.memory import MemoryAPI

memory = MemoryAPI(project_root=Path("."))

# Context
memory.should_load_context("What's my research status?")  # True
memory.display_context()  # Formatted context string
memory.intercept_task("diverga:a1", prompt)  # Enriched prompt

# Session
memory.start_session()  # Returns session_id
memory.end_session()  # Saves session data

# Checkpoint
memory.check_checkpoint("a1", "task_start")  # Returns injection if triggered
memory.record_checkpoint("CP_RESEARCH_DIRECTION", "approved")

# Decision
memory.add_decision(checkpoint="CP_RESEARCH_DIRECTION",
                   selected="Meta-analysis",
                   rationale="Need quantitative synthesis")
memory.amend_decision("dec-001", new_selected="...", new_rationale="...")

# Project
memory.initialize_project(name, question, paradigm)
memory.get_project_state()
memory.archive_stage("foundation", summary="Research direction finalized")
```

### CLI Commands

| Command | Description |
|---------|-------------|
| `/diverga:memory status` | Show project status |
| `/diverga:memory context` | Display full context |
| `/diverga:memory init --name NAME --question Q --paradigm P` | Initialize project |
| `/diverga:memory decision list` | List decisions |
| `/diverga:memory decision add` | Add decision |
| `/diverga:memory archive [STAGE]` | Archive stage |
| `/diverga:memory migrate` | Run migration |

### Breaking Changes

- **New directory structure**: `.research/` replaces `.diverga/memory/` for project state
- **Checkpoint format**: Updated YAML schema for checkpoint definitions
- **Decision log schema**: Added `context` and `metadata` fields

### Migration Guide

1. **Automatic Migration**: Run `/diverga:memory migrate` on existing projects
2. **Backup Created**: `.research-backup-v68-{timestamp}/` before migration
3. **Rollback Available**: `migrate --rollback` if issues occur

### Technical Details

**Python 3.8+ Compatible**: Uses `from __future__ import annotations`

**Dependencies**: Only stdlib (no external packages required)
- `pathlib`, `dataclasses`, `uuid`, `json`, `datetime`
- Optional: `yaml` (PyYAML) for enhanced YAML handling

**Korean Text Support**: UTF-8 encoding throughout, `ensure_ascii=False`

### Verification

```
✅ All 15 modules import successfully
✅ MemoryAPI instantiated - version 7.0.0
✅ 23 API methods available
✅ Templates render correctly
✅ Checkpoint triggers function
## [6.9.2] - 2026-02-03 (Marketplace Cache Fix)

### Overview

**Critical fix** for marketplace cache synchronization issue. When users installed Diverga via `/plugin install`, Claude Code's marketplace was pulling an outdated cached version that lacked the `version` field fix from v6.9.1.

### The Problem

```
/plugin install diverga     → (no content)
/diverga:help               → Unknown skill: diverga:help
/diverga-help               → Unknown skill: diverga-help

BUT Plugin shows as "Installed" with all skills listed!
```

### Root Cause

| Issue | Description |
|-------|-------------|
| **Marketplace Cache Lag** | GitHub marketplace doesn't update immediately after push |
| **Stale Commit** | Plugin install pulled `08b1ebb` (old) instead of `efc024a` (fixed) |
| **Missing Version Field** | Old cached version didn't have `version` in SKILL.md |

### Timeline of Discovery

```
Phase 1: Initial Investigation (2+ hours)
├─ Plugin shows installed ✅
├─ Skills listed in /plugin ✅
├─ But /diverga:help → Unknown skill ❌
└─ Compared with oh-my-claudecode (works)

Phase 2: SKILL.md Analysis (1 hour)
├─ Both OMC and Diverga have same structure
├─ Hypothesis: version field needed?
└─ Added version to all 51 files

Phase 3: Symlink Workaround (1 hour)
├─ Created ~/.claude/skills/diverga-xxx symlinks
├─ /diverga-help (hyphen) works! ✅
└─ /diverga:help (colon) still fails ❌

Phase 4: Cache Investigation (1 hour)
├─ Removed and reinstalled plugin
├─ Plugin shows installed with skills
└─ Still "Unknown skill" ❌

Phase 5: Root Cause Found (30 min)
├─ Checked cache SKILL.md - NO version field!
├─ Marketplace pulled OLD cached version
└─ Solution: Manual cache update + wait for marketplace
```

### Changes

#### 1. Comprehensive Troubleshooting Guide

New `docs/TROUBLESHOOTING-PLUGIN.md` with:
- Complete 6+ hour debugging journey
- Three identified root causes
- Multiple solution approaches
- Diagnostic commands
- SKILL.md format reference

#### 2. Updated Setup Wizard

`/diverga-setup` now includes automatic symlink installation:
```bash
# Automatically creates 51 symlinks during setup
~/.claude/skills/diverga-help → /path/to/skills/help/
```

#### 3. GitHub Action for SKILL.md Validation

`.github/workflows/validate-skills.yml` validates:
- All SKILL.md files have required fields
- Version follows semver format
- Skill count matches expected (51)

### Solutions Provided

| Solution | Method | Reliability |
|----------|--------|-------------|
| **A** | Update marketplace → Reinstall | Recommended |
| **B** | Manual cache copy | Quick fix |
| **C** | Local symlinks | Most reliable |

### Key Learnings

1. **SKILL.md requires `version` field** - Undocumented requirement discovered through debugging
2. **Marketplace has cache lag** - Wait ~10-15 min after push or click "Update marketplace"
3. **Two skill loading systems** - Plugin (colon) vs Local (hyphen) use different paths

### Verification

After fix:
```
/diverga:help     ✅ Works (colon prefix)
/diverga-help     ✅ Works (hyphen prefix)
## [6.9.1] - 2026-02-03 (Plugin Discovery Fix)

### Overview

**Critical bug fix release** resolving "Unknown skill" errors that prevented Claude Code from discovering Diverga skills. After comprehensive debugging, three root causes were identified and fixed.

### The Problem

```
❯ /diverga:help
Unknown skill: diverga:help
```

### Root Causes Identified

| Issue | Severity | Status |
|-------|----------|--------|
| Missing `version` field in SKILL.md | 🔴 CRITICAL | ✅ Fixed |
| Orphaned skill directories (`.claude/skills/`, `.codex/skills/`) | 🟡 MEDIUM | ✅ Fixed |
| Plugin cache vs local skills loading | 🟠 HIGH | ✅ Workaround |

### Changes Made

#### 1. SKILL.md Version Field

Added `version: "6.9.0"` to all 51 SKILL.md files:

**Before:**
```yaml
---
name: a1
description: |
  VS-Enhanced Research Question Refiner...
---
```

**After:**
```yaml
---
name: a1
description: |
  VS-Enhanced Research Question Refiner...
version: "6.9.0"
---
```

#### 2. Orphaned Directory Cleanup

| Directory | Action | Impact |
|-----------|--------|--------|
| `.claude/skills/` | 🗑️ Deleted | -48,000 lines |
| `.codex/skills/` | 🗑️ Deleted | -400 lines |
| `skills/` | ✅ Kept | Canonical location |

**Total**: 150 files changed, 48 insertions(+), 50,430 deletions(-)

#### 3. Local Skills Symlink Installation

Created 51 symlinks in `~/.claude/skills/` for reliable skill discovery:

```bash
~/.claude/skills/diverga-help → ~/.claude/plugins/cache/diverga/.../skills/help/
~/.claude/skills/diverga-memory → ~/.claude/plugins/cache/diverga/.../skills/memory/
# ... (51 total)
```

### Skill Access Methods

| Method | Command | Status |
|--------|---------|--------|
| **Hyphen prefix** (Recommended) | `/diverga-help` | ✅ Works reliably |
| Colon prefix (Plugin) | `/diverga:help` | ⚠️ Requires plugin load |

### Installation

```bash
# Create local skill symlinks
cd /path/to/Diverga
for skill_dir in skills/*/; do
  skill_name=$(basename "$skill_dir")
  ln -sf "$(pwd)/$skill_dir" ~/.claude/skills/diverga-${skill_name}
done

# Restart Claude Code
```

### Verification

```
/diverga-help       ✅ Should display help guide
/diverga-memory     ✅ Should show memory system
/diverga-a1         ✅ Should show Research Question Refiner
```

### Git Commit

```
efc024a fix(plugin): add required version field and remove orphaned skill directories
```

### Full Release Notes

See: `docs/releases/RELEASE_v6.9.1.md`

---

## [6.7.1] - 2026-01-31 (Documentation Synchronization)

### Overview

**Documentation sync release** aligning AGENTS.md, SKILL.md, and CLAUDE.md to v6.7.0 architecture. Ensures consistent agent counts (44), version strings, and checkpoint definitions across all core files.

### Version Alignment

| Document | Before | After |
|----------|--------|-------|
| `AGENTS.md` | v6.5 (37 agents) | **v6.7.0** (44 agents) |
| `skills/research-coordinator/SKILL.md` | v6.0.0 (27 agents) | **v6.7.0** (44 agents) |
| `skills/research-orchestrator/SKILL.md` | v2.0.0 (27 agents) | **v2.7.0** (44 agents) |
| `CLAUDE.md` | v6.7.0 | v6.7.0 + SCH_PRISMA_GENERATION |

### Agents Added to Documentation

| Agent | Name | Category | Model |
|-------|------|----------|-------|
| B5 | ParallelDocumentProcessor | Evidence | Opus |
| F5 | HumanizationVerifier | Quality | Haiku |
| G5 | AcademicStyleAuditor | Communication | Sonnet |
| G6 | AcademicStyleHumanizer | Communication | Opus |

### Checkpoints Synchronized

- CP_META_GATE (🔴) - Meta-analysis gate failure
- SCH_DATABASE_SELECTION (🔴) - Database selection for retrieval
- SCH_SCREENING_CRITERIA (🔴) - PRISMA criteria approval
- SCH_RAG_READINESS (🟠) - RAG system ready
- SCH_PRISMA_GENERATION (🟡) - PRISMA diagram generation

### Files Modified

| File | Changes |
|------|---------|
| `AGENTS.md` | v6.5→v6.7.0, 37→44 agents, B5/F5/G5/G6 |
| `skills/research-coordinator/SKILL.md` | v6.0.0→v6.7.0, Category I, SCH_* |
| `skills/research-orchestrator/SKILL.md` | v2.0.0→v2.7.0, 44 agents |
| `CLAUDE.md` | SCH_PRISMA_GENERATION checkpoint |

### Files Created

| File | Purpose |
|------|---------|
| `qa/reports/verification_report_v6.7.0.md` | Architecture verification |
| `docs/releases/RELEASE_v6.7.1.md` | Detailed release notes |

### No Breaking Changes

Documentation-only release with no code or behavioral changes.

---

## [6.7.0] - 2026-01-30 (Systematic Review Automation)

### Overview

Diverga v6.7.0 introduces **Category I: Systematic Review Automation** with 4 new agents (I0-I3) for PRISMA 2020 compliant literature review pipelines. Expands from 40 to 44 agents across 9 categories.

**Core Theme**: "Automate systematic reviews with human checkpoints at every critical decision"

### New Category: I - Systematic Review Automation (4 agents)

| Agent | Name | Model | Purpose |
|-------|------|-------|---------|
| **I0** | ScholarAgentOrchestrator | Opus | Pipeline coordination, stage management |
| **I1** | PaperRetrievalAgent | Sonnet | Multi-database fetching (Semantic Scholar, OpenAlex, arXiv) |
| **I2** | ScreeningAssistant | Sonnet | AI-PRISMA 6-dimension screening |
| **I3** | RAGBuilder | Haiku | Vector database construction (zero cost) |

### New Human Checkpoints

| Checkpoint | Level | Trigger |
|------------|-------|---------|
| SCH_DATABASE_SELECTION | 🔴 REQUIRED | User specifies databases for paper retrieval |
| SCH_SCREENING_CRITERIA | 🔴 REQUIRED | User approves inclusion/exclusion criteria |
| SCH_RAG_READINESS | 🟠 RECOMMENDED | Before RAG queries begin |
| SCH_PRISMA_GENERATION | 🟡 OPTIONAL | Before generating PRISMA flow diagram |

### New Workflows

| Workflow | Stages | Description |
|----------|--------|-------------|
| `automated-systematic-review` | I0→I1→I2→I3 | Full PRISMA 2020 pipeline |
| `knowledge-repository-build` | I0→I1→I3 | Broad corpus (5K-15K papers, 50% threshold) |

### Agent Auto-Trigger Keywords

| Agent | English Keywords | Korean Keywords |
|-------|------------------|-----------------|
| `diverga:i0` | "systematic review", "PRISMA", "literature review automation" | "체계적 문헌고찰", "프리즈마" |
| `diverga:i1` | "fetch papers", "retrieve papers", "database search" | "논문 수집", "논문 검색" |
| `diverga:i2` | "screen papers", "PRISMA screening", "inclusion criteria" | "논문 스크리닝", "선별" |
| `diverga:i3` | "build RAG", "vector database", "embed documents" | "RAG 구축", "벡터 DB" |

### New Files

| Path | Purpose |
|------|---------|
| `.claude/skills/research-agents/I0-scholar-agent-orchestrator/SKILL.md` | Orchestrator skill |
| `.claude/skills/research-agents/I1-paper-retrieval-agent/SKILL.md` | Paper retrieval skill |
| `.claude/skills/research-agents/I2-screening-assistant/SKILL.md` | Screening skill |
| `.claude/skills/research-agents/I3-rag-builder/SKILL.md` | RAG builder skill |

### Modified Files

| File | Changes |
|------|---------|
| `CLAUDE.md` | v6.7.0, 44 agents, 9 categories, Category I section |
| `agent-registry.yaml` | v6.7.0, Category I agents, new checkpoints, workflows |

### Model Routing (Updated)

| Tier | Model | Agents (44 total) |
|------|-------|-------------------|
| HIGH | Opus | A1, A2, A3, A5, B5, C1, C2, C3, C5, D4, E1, E2, E3, G3, G6, H1, H2, **I0** (17) |
| MEDIUM | Sonnet | A4, A6, B1, B2, C4, C6, C7, D1, D2, E5, F3, F4, G1, G2, G4, G5, **I1**, **I2** (18) |
| LOW | Haiku | B3, B4, D3, E4, F1, F2, F5, **I3** (8) |

### Category Summary (v6.7.0)

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
| **I** | **Systematic Review Automation** | **4** |
| **Total** | | **44** |

### No Breaking Changes

Existing workflows continue unchanged. Category I agents are additive.

---

## [6.6.3] - 2026-01-30 (Codex CLI SKILL.md Implementation)

### Overview

**SKILL.md files now enable actual skill loading in Codex CLI.** Previously, AGENTS.md provided only passive documentation. Now `.codex/skills/` directory contains proper SKILL.md files that Codex CLI discovers and activates.

### Key Discovery

**AGENTS.md ≠ SKILL.md**

| Feature | AGENTS.md | SKILL.md |
|---------|-----------|----------|
| Purpose | Passive documentation | Active skill definition |
| Loading | Context injection only | Skill system activation |
| Structure | Free-form Markdown | YAML frontmatter required |

### New Files

```
.codex/skills/
├── research-coordinator/
│   └── SKILL.md         # Main coordinator (40 agents)
├── meta-analysis/
│   └── SKILL.md         # C5-MetaAnalysisMaster
└── checkpoint-system/
    └── SKILL.md         # Human checkpoint enforcement
```

### QUANT-005 Test Verification

| Verification Point | Before (QUANT-004) | After (QUANT-005) |
|--------------------|---------------------|-------------------|
| Skill activation | ❌ Not present | ✅ "✅ meta-analysis 스킬 사용" |
| Checkpoint marker | ❌ Not present | ✅ "🔴 CHECKPOINT: CP_EFFECT_SIZE_SELECTION" |
| VS T-Score options | ❌ Not present | ✅ [A] T=0.65, [B] T=0.40 ⭐, [C] T=0.25 |
| Behavioral halt | ❌ Continued | ✅ "어떤 지표로 통일하시겠습니까?" |

### Documentation

- `docs/CODEX-SKILL-SYSTEM.md` - Full technical documentation
- Claude Code vs Codex CLI comparison
- Installation recommendations

### Claude Code Recommendation

Claude Code is **recommended** for full Diverga functionality:
- ✅ Task tool support (40 specialized agents)
- ✅ AskUserQuestion tool (clickable UI)
- ✅ Tool-level checkpoint enforcement
- ✅ Parallel agent execution

Codex CLI now **supported** with SKILL.md files:
- ⚠️ Behavioral checkpoints only (model-voluntary)
- ⚠️ Main model handles all work (no dedicated agents)

---

