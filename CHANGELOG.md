# Changelog

All notable changes to Diverga (formerly Research Coordinator) will be documented in this file.

---

## [8.3.0] - 2026-02-12 (Cross-Platform Migration)

### Overview

**Diverga v8.3.0** - Cross-platform migration release bringing Codex CLI and OpenCode support up to parity with Claude Code v8.2.0 feature set. Introduces 47 individual skill files, GPT-5.3-Codex model routing, and comprehensive cross-platform documentation.

### Key Highlights

- **47 individual SKILL.md files** for Codex CLI (44 agents + 3 utilities)
- **GPT-5.3-Codex model routing** across all tiers (HIGH/MEDIUM/LOW)
- **44 total agents** (Category I: ScholaRAG agents added in v6.7)
- **Cross-platform compatibility improved**: Codex CLI ~40% → ~75%, OpenCode ~20% → ~70%
- **No breaking changes** for Claude Code users

### Platform Compatibility

| Platform | v8.2.0 | v8.3.0 | Improvement |
|----------|--------|--------|-------------|
| Claude Code | 100% | 100% | - |
| Codex CLI | ~40% | **~75%** | +35% |
| OpenCode | ~20% | **~70%** | +50% |

### New Features

- **feat(codex-cli)**: 47 individual skill files in `.codex/skills/diverga-*/`
  - 44 agent skills (A1-I3) + 3 utility skills (setup, memory, help)
  - YAML frontmatter with name, description (<500 chars), metadata
  - Codex CLI Degraded Mode instructions per skill
  - Text-based checkpoint protocol (replaces MCP runtime)
  - Tool mapping tables (Claude Code → Codex CLI)
  - Bilingual triggers (English + Korean)

- **feat(models)**: GPT-5.3-Codex model routing
  - HIGH tier: o3 → `gpt-5.3-codex` (most capable agentic coding model)
  - MEDIUM tier: gpt-4.1 → `gpt-5.2-codex`
  - LOW tier: gpt-4.1-mini → `gpt-5.1-codex-mini`

- **feat(templates)**: AGENTS.md.template v8.3.0 rewrite
  - 40 → 44 agents (Category I: I0-I3 ScholaRAG agents)
  - Full Agent Prerequisite Map
  - Checkpoint Dependency Order (Level 0-5)
  - SCH_* checkpoints for systematic review automation
  - Memory system reference (.research/ directory)

- **feat(opencode)**: oh-my-opencode.template.json v8.3.0
  - I0-I3 triggers with EN+KR keywords
  - Model routing for all 44 agents
  - SCH_* checkpoints in required/recommended sections

### CLI Tool Updates

- **feat(diverga-codex.cjs)**: v6.6.1 → v8.3.0
  - 44 agents (was 40), 9 categories (was 8)
  - New `prereq` command showing Agent Prerequisite Map
  - SCH_* checkpoints added
  - Fixed agent tier assignments (A3→HIGH, B5→HIGH, F5→LOW, G6→HIGH)

- **feat(install-multi-cli.sh)**: v6.6.2 → v8.3.0
  - Copies individual `.codex/skills/` directories
  - `.research/` directory initialization
  - Node.js >= 18 version check
  - Post-install verification

### New Documentation

| File | Description |
|------|-------------|
| `docs/RELEASE-NOTES-v8.3.0.md` | Comprehensive release notes |
| `docs/CROSS-PLATFORM-GUIDE.md` | Unified guide for all platforms |
| `docs/PLATFORM-LIMITATIONS.md` | Detailed limitation specs with workarounds |

### Updated Documentation

| File | Changes |
|------|---------|
| `docs/CODEX-SKILL-SYSTEM.md` | v6.6.2 → v8.3.0, individual skills, GPT-5.3-Codex |
| `adapters/README.md` | Cross-platform compatibility table |
| `CLAUDE.md` | Research Coordinator v8.3.0 integration |

### Known Limitations (Codex CLI / OpenCode)

- No parallel agent execution (sequential only)
- No MCP runtime checkpoints (text-based behavioral enforcement)
- No AskUserQuestion structured UI (text prompts)
- No HUD statusline
- Single model session (no per-agent model isolation)

### Migration Guide

v8.2.0 → v8.3.0 migration:

**Claude Code users** (no breaking changes):
- Optional: Update AGENTS.md with `cp AGENTS.md.template AGENTS.md`
- All existing workflows continue to work

**Codex CLI users** (new platform support):
```bash
curl -sSL https://raw.githubusercontent.com/HosungYou/Diverga/main/scripts/install-multi-cli.sh | bash -s -- --codex
```

**OpenCode users** (new platform support):
```bash
curl -sSL https://raw.githubusercontent.com/HosungYou/Diverga/main/scripts/install-multi-cli.sh | bash -s -- --opencode
```

### File Summary

| Category | Count | Description |
|----------|-------|-------------|
| New Codex Skills | 47 | `.codex/skills/diverga-*/SKILL.md` |
| Updated Templates | 3 | AGENTS.md.template, oh-my-opencode.template.json, claude-settings |
| Updated CLI Tools | 2 | diverga-codex.cjs, install-multi-cli.sh |
| New Documentation | 3 | RELEASE-NOTES-v8.3.0.md, CROSS-PLATFORM-GUIDE.md, PLATFORM-LIMITATIONS.md |
| Updated Documentation | 3 | CODEX-SKILL-SYSTEM.md, adapters/README.md, CLAUDE.md |
| **Total** | **58+** | |

---

## [8.1.0] - 2026-02-09 (Checkpoint Enforcement Strengthening)

### Overview

**Diverga v8.1.0** - Checkpoint enforcement overhaul ensuring AskUserQuestion tool
is called at every human decision point. Fixes ad-hoc and multi-agent invocation
scenarios where checkpoints were silently skipped.

### Critical Changes

- **feat(enforcement)**: Mandatory AskUserQuestion tool usage at all checkpoints
  - Text-based questions no longer count as checkpoint compliance
  - Structured options with bilingual labels (EN/KR)

- **feat(prerequisites)**: Agent Prerequisite Map with dependency ordering
  - No-skip policy: REQUIRED checkpoints cannot be bypassed
  - Ad-hoc agent calls now verify prerequisites before execution

- **feat(multi-agent)**: Parallel agent checkpoint coordination
  - Union of prerequisites collected across simultaneously triggered agents
  - Dependency-ordered sequential AskUserQuestion calls
  - Parallel execution only after all prerequisites cleared

### Files Added

| File | Description |
|------|-------------|
| `.claude/references/checkpoint-templates.md` | AskUserQuestion parameter templates for 22 checkpoints |

### Files Modified (Key)

| File | Changes |
|------|---------|
| `CLAUDE.md` | Enforcement Protocol, Agent Prerequisite Map, Dependency Order, Multi-Agent rules |
| `skills/research-coordinator/SKILL.md` | Enforcement rules overhaul, Multi-Agent Dispatch Protocol |
| `skills/{25 agents}/SKILL.md` | Checkpoint Execution Block inserted after frontmatter |
| `.opencode/plugins/diverga/types.ts` | `prerequisites` field added to AgentInfo |
| `.opencode/plugins/diverga/agents.ts` | Prerequisites data for all agents |
| `.opencode/plugins/diverga/checkpoints.ts` | Missing checkpoint definitions added |
| `.opencode/plugins/diverga/hooks/checkpoint-enforcer.ts` | AGENT_PREREQUISITES mapping + multi-agent union logic |
| `scripts/install.sh` | Version bump to 8.1.0 |
| `README.md` | Version badge update |

### Migration Guide

v8.0.x → v8.1.0 migration:
- **Existing installations**: Re-run `scripts/install.sh` to get updated skills
- **No breaking changes**: All existing workflows continue to work
- **New behavior**: AskUserQuestion tool will now fire at checkpoints
  that previously only showed text questions
- **Researcher impact**: More structured decision prompts with clickable options

---

## [8.0.2] - 2026-02-07 (Doctor Diagnostics Skill)

### New Features

- **feat(skill)**: Added `/diverga:doctor` system diagnostics skill
  - 5-layer diagnostic checks: Plugin Health, Skill Sync, Config Validity, API Keys, Project State
  - OpenClaw-style Check-Report-Fix pattern: every issue includes actionable fix command
  - Read-only diagnostics — no file modifications
  - Referenced from `/diverga` dashboard Quick Actions

### Files Added

| File | Description |
|------|-------------|
| `skills/doctor/SKILL.md` | Doctor diagnostics skill definition |

---

## [8.0.1-patch3] - 2026-02-07 (8-Dimension Diagnostic Sweep & Deep Fix)

### Overview

Comprehensive 8-dimension diagnostic sweep using multi-agent parallel analysis (version audit, agent definitions audit, build/TS diagnostics, code quality review, security review, architecture review, documentation consistency, test coverage analysis). Found and fixed 16+ issues across the entire codebase.

### Critical Fixes

- **fix(types)**: Added Category I ('I') to `CategoryId` union type, `CATEGORIES` record, and `CATEGORY_TOOLS` record in `src/agents/types.ts`
- **fix(definitions)**: Registered I0-I3 agents in `AGENT_MAPPINGS` and `AGENT_CONFIGS` in `src/agents/definitions.ts` (40→44 agents)
- **fix(index)**: Updated VERSION from '6.5.0' to '8.0.1', converted CJS `require()` to ESM `import()`, added category 'I' support in `src/index.ts`

### Version Synchronization (8 additional files)

| File | Old Version | New Version |
|------|-------------|-------------|
| `lib/index.ts` | 6.0.0 | 8.0.1 |
| `lib/agents/discovery.ts` | 6.0.0 | 8.0.1 |
| `packages/codex-setup/src/index.ts` | 6.6.1 | 8.0.1 |
| `.opencode/plugins/diverga/index.ts` | 6.6.1 | 8.0.1 |
| `.opencode/plugins/diverga/hooks/context-manager.ts` | 6.0.0 | 8.0.1 |

### Library Fixes (lib/)

- **fix(lib/types)**: Added Category I to `CATEGORIES` in `lib/agents/types.ts`
- **fix(lib/parser)**: Updated regex from `[A-H]` to `[A-I]` in `lib/agents/parser.ts` to recognize Category I agents
- **fix(lib/index)**: Converted CJS `require()` to async ESM `import()` in `initializeDiverga()`

### Documentation Fixes

- **fix(AGENTS.md)**: Updated version references from v6.7.0 to v8.0.1 in section headers
- **fix(.codex/AGENTS.md)**: Updated agent count to 44, added Category I section with I0-I3
- **fix(README.md)**: Updated agent count from 40 to 44, BibTeX version from 6.7.0 to 8.0.1
- **fix(.opencode)**: Updated agent count from 40 to 44
- **fix(lib/memory)**: Updated IMPLEMENTATION_SUMMARY.md agent count from 40 to 44

### Diagnostic Findings (Advisory)

| Dimension | Agent | Key Finding |
|-----------|-------|-------------|
| Architecture | arch-reviewer (opus) | Dual registry (src/ vs lib/) confirmed; lib/ is legacy |
| Security | security-reviewer (opus) | 5 findings, overall LOW risk; path traversal in prompt-loader |
| Code Quality | code-reviewer (opus) | 12 issues; dead code in src/, fragile YAML parser |
| Test Coverage | qa-tester (sonnet) | 168 tests, zero TypeScript test coverage |

### Verification

- `tsc --noEmit`: 0 errors
- Stale version grep (6.0.0/6.5.0/6.6.1): 0 matches in source
- Stale agent count grep (40/33 agents): 0 matches
- 14 files changed, 137 insertions, 40 deletions

---

## [8.0.1] - 2026-02-05 (Installation Bug Fixes)

### Bug Fixes

- **fix(install)**: Fixed `ensure_repo()` stdout capture bug where log messages were mixed with path output
- **fix(install)**: Changed skill installation from symlinks to file copies - symlinks to `/tmp/` broke after temporary directory cleanup

### Technical Details

| Issue | Cause | Fix |
|-------|-------|-----|
| Install script path corruption | `log_info` stdout captured in `$(ensure_repo)` | Redirect log to stderr with `>&2` |
| Skills broken after reboot | Symlinks pointed to `/tmp/diverga-install-*/` | Use `cp -r` instead of `ln -sf` |

### Installation Verification

After installing v8.0.1:
```bash
# Skills should be directories, not symlinks
ls -la ~/.claude/skills/diverga-a1
# Should show: drwxr-xr-x (directory), NOT lrwxr-xr-x -> /tmp/...
```

---

## [8.0.0] - 2026-02-04 (Project Visibility & HUD Enhancement)

### Overview

**Diverga v8.0** - Project Visibility Enhancement with independent HUD, simplified setup, natural language project initialization, and auto-generated research documentation.

This release introduces major improvements to researcher experience:
- **File Structure Redesign**: `.research/` for system files, `docs/` for researcher-visible documentation
- **Independent HUD**: Standalone statusline display completely separate from oh-my-claudecode
- **Simplified Setup**: 3-step wizard (down from 9 steps)
- **Natural Language Start**: "I want to conduct a systematic review on AI" → auto-initialize project

### New Features

#### 1. File Structure Redesign

| Directory | Purpose | Visibility |
|-----------|---------|------------|
| `.research/` | System files (state, decisions, checkpoints) | Hidden |
| `docs/` | Researcher documentation (auto-generated) | Visible |

**New docs/ structure (7 files)**:

```
docs/
├── PROJECT_STATUS.md       # Progress overview with visual indicators
├── DECISION_LOG.md         # Human-readable decision history
├── RESEARCH_AUDIT.md       # IRB/reproducibility audit trail
├── METHODOLOGY.md          # Research design summary (NEW)
├── TIMELINE.md             # Milestones and deadlines (NEW)
├── REFERENCES.md           # Key papers and frameworks (NEW)
└── README.md               # Project overview (NEW)
```

**Auto-synchronization**: When decisions are made or checkpoints completed, `docs/` files update automatically.

#### 2. Independent Diverga HUD

Completely independent statusline display for research progress - no oh-my-claudecode dependency.

**HUD Presets**:

| Preset | Display | Use Case |
|--------|---------|----------|
| `research` (default) | Stage, Checkpoints, Memory | Daily research |
| `checkpoint` | Detailed checkpoint status | Decision sessions |
| `memory` | Memory health focus | Debugging |
| `minimal` | Stage only | Clean interface |

**Display Examples**:

```
research:   🔬 AI-Ethics-HR │ Stage: foundation │ ●●○○○○○○○○○ (2/11) │ 🧠 95%
checkpoint: 🔬 AI-Ethics-HR │ Stage: foundation
            Checkpoints: ●●○○○○○○○○○ (2/11)
             ✅ CP_RESEARCH_DIRECTION │ ✅ CP_PARADIGM_SELECTION
             🔴 CP_SCOPE_DEFINITION (pending)
minimal:    🔬 AI-Ethics-HR │ foundation
```

**StatusLine Integration**:

```json
// ~/.claude/settings.json
{
  "statusLine": {
    "type": "command",
    "command": "node ~/.claude/hud/diverga-hud.mjs"
  }
}
```

#### 3. Simplified Setup (3 Steps)

| Step | Content | Changes from v7.0 |
|------|---------|-------------------|
| 1 | Welcome + Project Detection | Same |
| 2 | Checkpoint Level + HUD + Language | Combined 6 steps into 1 |
| 3 | Apply & Complete | Same |

**Removed**:
- LLM selection (Claude Code already authenticated)
- API key configuration (not needed)
- Paradigm selection (auto-detect or ask during research)

**New Options**:
- HUD enable/disable
- HUD preset selection

#### 4. Natural Language Project Initialization

**Detection Patterns**:

| Language | Patterns |
|----------|----------|
| English | "systematic review on/about {topic}", "meta-analysis on {topic}", "literature review about {topic}" |
| Korean | "체계적 문헌고찰", "체계적 리뷰", "메타분석", "메타 분석", "문헌고찰" |

**Research Types Detected**:
- `systematic_review` (체계적 문헌고찰)
- `meta_analysis` (메타분석)
- `literature_review` (문헌고찰)
- `experimental` (실험연구)
- `qualitative` (질적연구)
- `mixed_methods` (혼합연구)

**Flow**:
```
User: "I want to conduct a systematic review on AI in education"
        │
        ▼
  Intent Detection (confidence: 0.9)
        │
        ▼
  Confirmation Prompt (bilingual)
        │
   [Yes] → Auto-create .research/ and docs/
   [No]  → Continue as normal conversation
```

#### 5. Project Detection & Loading

**Session Start Behavior**:

```
┌─────────────────────────────────────────────────────────────────┐
│ Session Start                                                    │
│        │                                                        │
│        ▼                                                        │
│ .research/ exists?                                              │
│        │                                                        │
│   YES ─┼─ NO                                                    │
│        │     │                                                  │
│        ▼     ▼                                                  │
│ Auto-load    Research intent detected?                          │
│ Show banner       │                                             │
│        │     YES ─┼─ NO                                         │
│        │          │     │                                       │
│        ▼          ▼     ▼                                       │
│ Continue      Initialize  Normal                                │
│ project       prompt      conversation                          │
└─────────────────────────────────────────────────────────────────┘
```

**Project Load Banner**:

```
┌─────────────────────────────────────────────────────────────────┐
│ ✅ 프로젝트 로드됨: AI-Ethics-HR                                 │
├─────────────────────────────────────────────────────────────────┤
│ 🔬 Stage: foundation │ ●●○○○○○○○○○ (2/11) │ 🧠 100%             │
│                                                                 │
│ 마지막 세션: 2026-02-04                                         │
└─────────────────────────────────────────────────────────────────┘
```

### New Files

#### HUD System (`lib/hud/`)

| File | Purpose | Lines |
|------|---------|-------|
| `colors.ts` | ANSI color utilities, HUD_COLORS palette | ~80 |
| `state.ts` | HUD state management, STAGES definition | ~180 |
| `presets.ts` | 4 preset configurations (research, checkpoint, memory, minimal) | ~120 |
| `core.ts` | HUDRenderer class, rendering logic | ~200 |
| `index.ts` | Main exports, DivergaHUD facade | ~50 |

#### HUD Wrapper (`~/.claude/hud/`)

| File | Purpose | Lines |
|------|---------|-------|
| `diverga-hud.mjs` | Standalone Node.js statusLine script | ~250 |

#### Memory System Extensions (`lib/memory/src/`)

| File | Purpose | Lines |
|------|---------|-------|
| `intent_detector.py` | Natural language research intent detection | ~430 |
| `project_initializer.py` | Auto-project initialization from intent | ~440 |

#### Skill Definition (`skills/hud/`)

| File | Purpose |
|------|---------|
| `SKILL.md` | HUD skill definition for Claude Code |

### Modified Files

| File | Changes |
|------|---------|
| `lib/memory/src/doc_generator.py` | Extended from 3 to 7 docs, added STAGES, progress bar, timestamp helpers |
| `lib/memory/src/memory_api.py` | Added HUD integration, docs sync, intent detection, project init methods |
| `skills/setup/SKILL.md` | Simplified from 9 steps to 3, removed LLM selection, added HUD |
| `CLAUDE.md` | Updated to v8.0, added v8.0 Key Features section |

### API Reference

**New MemoryAPI Methods**:

```python
from lib.memory import MemoryAPI

memory = MemoryAPI(project_root=Path("."))

# HUD Integration
memory.refresh_hud()                    # Update HUD cache

# Documentation Sync
memory.sync_docs()                      # Sync all docs
memory.sync_doc("PROJECT_STATUS.md")    # Sync single doc

# Intent Detection
result = memory.detect_research_intent("I want to do a meta-analysis")
# Returns: {"is_research": True, "type": "meta_analysis", "topic": ..., "confidence": 0.9}

# Project Initialization
memory.should_init_project("systematic review on AI")  # (True, IntentResult)
memory.initialize_from_message("systematic review on AI in education")
memory.get_load_banner()                # Formatted project banner

# Auto-sync Hooks (internal)
memory._on_state_change()               # Triggered on state updates
memory._on_decision_added(decision_id)  # Triggered after add_decision()
memory._on_checkpoint_completed(cp_id)  # Triggered after record_checkpoint()
```

**Intent Detector Functions**:

```python
from lib.memory.src.intent_detector import (
    detect_intent,           # Full intent detection
    should_initialize_project,  # Check if should init
    get_suggested_prompt,    # Confirmation prompt
    ResearchType,           # Enum of research types
    IntentResult            # Detection result dataclass
)

result = detect_intent("체계적 문헌고찰을 하고 싶어요")
# IntentResult(is_research_intent=True, research_type=ResearchType.SYSTEMATIC_REVIEW,
#              topic=None, confidence=0.9, paradigm="quantitative", ...)
```

**Project Initializer Functions**:

```python
from lib.memory.src.project_initializer import (
    initialize_project,      # Explicit initialization
    initialize_from_intent,  # Initialize from IntentResult
    is_project_initialized,  # Check if already initialized
    get_project_banner       # Get load banner
)

results = initialize_project(
    project_name="AI-Education-Review",
    research_question="How does AI improve learning outcomes?",
    paradigm="quantitative",
    hud_enabled=True
)
# Creates: .research/, docs/, all state files
```

### CLI Commands

| Command | Description |
|---------|-------------|
| `/diverga-hud status` | Show HUD status |
| `/diverga-hud preset <name>` | Change preset (research, checkpoint, memory, minimal) |
| `/diverga-hud enable` | Enable HUD |
| `/diverga-hud disable` | Disable HUD |
| `/diverga-hud setup` | Setup HUD statusline |

### Breaking Changes

- **Setup wizard simplified**: `/diverga-setup` now has 3 steps instead of 9
- **LLM selection removed**: No longer asks for LLM provider (uses Claude Code's model)
- **API key configuration removed**: Not needed in Claude Code context

### Migration Guide

v7.0 → v8.0 migration is **automatic**:

1. Existing `.research/` directories are preserved
2. `docs/` directory created automatically on first state change
3. HUD can be enabled via `/diverga-hud setup`
4. No manual migration required

**To enable v8.0 features on existing project**:

```bash
# Enable HUD (optional)
/diverga-hud setup

# Generate docs/ files
# (Automatic on next decision or checkpoint)
```

### Technical Details

**HUD System**:
- TypeScript source in `lib/hud/`
- Pure Node.js runtime script (`~/.claude/hud/diverga-hud.mjs`)
- No external dependencies
- YAML parsing for project state

**Intent Detection**:
- Bilingual support (English + Korean)
- Regex-based pattern matching
- Confidence scoring (0.0 - 1.0)
- Topic extraction from context

**Project State Files**:

| File | Format | Purpose |
|------|--------|---------|
| `.research/project-state.yaml` | YAML | Project metadata |
| `.research/decision-log.yaml` | YAML | Decision history |
| `.research/checkpoints.yaml` | YAML | Checkpoint states |
| `.research/hud-state.json` | JSON | HUD configuration |

### Verification

```
✅ Intent detector tested: "systematic review on AI" → Type: systematic_review, Confidence: 0.9
✅ HUD files exist: colors.ts, state.ts, presets.ts, core.ts, index.ts
✅ HUD wrapper exists: ~/.claude/hud/diverga-hud.mjs
✅ Doc generator has 7 files: PROJECT_STATUS, DECISION_LOG, RESEARCH_AUDIT, METHODOLOGY, TIMELINE, REFERENCES, README
✅ Memory API has new methods: refresh_hud, sync_docs, detect_research_intent, initialize_from_message
✅ Setup skill simplified: 3 steps, HUD option added
```

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
| **I0** | ReviewPipelineOrchestrator | Opus | Pipeline coordination, stage management |
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
| `.claude/skills/research-agents/I0-review-pipeline-orchestrator/SKILL.md` | Orchestrator skill |
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

