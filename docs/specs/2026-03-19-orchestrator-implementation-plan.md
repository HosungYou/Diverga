# Diverga Orchestrator Redesign Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Replace 3 overlapping agent dispatch skills (research-orchestrator, vs-arena, research-coordinator) with a clean 2-skill architecture: a new unified `/diverga:orchestrator` for Agent Teams execution, and a slimmed research-coordinator for research domain knowledge.

**Architecture:** "Clean Split" — WHAT (research-coordinator: paradigm detection, agent selection) separated from HOW (orchestrator: Agent Teams lifecycle, subagent dispatch). CLAUDE.md slimmed from 16.8KB to <5KB by extracting rules/tools to docs/. Legacy artifacts (33-agent routing.yaml, v8 roadmap) deleted.

**Tech Stack:** Markdown skills, JSON config, Python tests. No runtime code changes.

**Spec:** `docs/specs/2026-03-19-orchestrator-redesign.md`

**Working directory:** `/Volumes/External SSD/Projects/Diverga/Diverga-core`

---

### Task 1: Extract docs from CLAUDE.md

Create standalone docs for content being removed from CLAUDE.md. These preserve architectural knowledge without bloating every-session context.

**Files:**
- Read: `CLAUDE.md` (source of content to extract)
- Create: `docs/CHECKPOINT-RULES.md`
- Create: `docs/ARCHITECTURE.md`
- Create: `docs/MCP-TOOLS.md`

- [ ] **Step 1: Read current CLAUDE.md and identify extraction boundaries**

Read `CLAUDE.md` fully. Mark these sections for extraction:
- "Checkpoint enforcement Rules 1-6" (Rules 1-6 block, Korean enforcement text)
- "Hook Enforcement" section
- "MCP Tools" section (Diverga Server Tools table + Journal MCP Tools table)
- "VS Arena" detail section
- "Key Pipelines" section
- "Core Systems" table
- "Memory System" commands table

- [ ] **Step 2: Create docs/CHECKPOINT-RULES.md**

Extract checkpoint enforcement Rules 1-6 from CLAUDE.md. Include the Korean-language rule text as-is (bilingual is intentional). Include the checkpoint type definitions (REQUIRED/RECOMMENDED/OPTIONAL) with their behaviors.

Content structure:
```
# Checkpoint Enforcement Rules
## Checkpoint Types (3 levels)
## Rule 1: AskUserQuestion mandatory
## Rule 2: Prerequisite Gate
## Rule 3: Ad-hoc invocation
## Rule 4: Multi-agent dispatch
## Rule 5: Override Refusal
## Rule 6: MCP-First Verification
```

- [ ] **Step 3: Create docs/ARCHITECTURE.md**

Combine "Core Systems", "Key Pipelines", "Hook Enforcement", and "Memory System" sections into a single architecture reference.

Content structure:
```
# Diverga Architecture Reference
## System Overview (Clean Split: coordinator WHAT + orchestrator HOW)
## Core Systems (State, Hooks, Config, MCP, Memory)
## Key Pipelines (Humanization, Meta-Analysis, Systematic Review, Journal)
## Hook Enforcement (prereq-enforcer.mjs, REQUIRED hard-block, debug mode)
## Memory System (3-layer context, commands table)
```

- [ ] **Step 4: Create docs/MCP-TOOLS.md**

Extract MCP tools reference tables from CLAUDE.md.

Content structure:
```
# MCP Tools Reference
## Servers (.mcp.json)
## Diverga Server Tools (16 tools — table)
## Journal MCP Tools (6 tools — table)
## Humanizer MCP Tools (5 tools — table from plugin system)
```

- [ ] **Step 5: Commit extracted docs**

```bash
cd "/Volumes/External SSD/Projects/Diverga/Diverga-core"
git add docs/CHECKPOINT-RULES.md docs/ARCHITECTURE.md docs/MCP-TOOLS.md
git commit -m "docs: extract checkpoint rules, architecture, and MCP tools from CLAUDE.md

Preparation for CLAUDE.md slim-down (16.8KB -> <5KB).
Content preserved in standalone docs, no longer loaded every session.

Co-Authored-By: Claude Opus 4.6 (1M context) <noreply@anthropic.com>"
```

---

### Task 2: Delete legacy artifacts

Remove files identified in the legacy audit that cause confusion or ghost loading.

**Files:**
- Delete: `.claude/config/research-coordinator-routing.yaml`
- Delete: `UPGRADE_ROADMAP.md`

- [ ] **Step 1: Verify routing.yaml is unreferenced**

```bash
cd "/Volumes/External SSD/Projects/Diverga/Diverga-core"
grep -r "research-coordinator-routing" --include="*.md" --include="*.js" --include="*.json" --include="*.yaml" . | grep -v node_modules | grep -v ".git/"
```

Expected: no active references (only possibly in CHANGELOG.md historical notes, which is OK).

- [ ] **Step 2: Delete routing.yaml**

```bash
rm ".claude/config/research-coordinator-routing.yaml"
```

- [ ] **Step 3: Delete UPGRADE_ROADMAP.md**

```bash
rm "UPGRADE_ROADMAP.md"
```

- [ ] **Step 4: Commit deletions**

```bash
git add -A
git commit -m "chore: delete legacy routing.yaml (33-agent v6.0) and UPGRADE_ROADMAP.md (v8.0.1)

routing.yaml: referenced pre-consolidation 33 agents. agents.json is SSoT since v11.0.
UPGRADE_ROADMAP.md: v8.0.1 era roadmap referencing 44 agents. Never-released v8.1.0.

Co-Authored-By: Claude Opus 4.6 (1M context) <noreply@anthropic.com>"
```

---

### Task 3: Create new skills/orchestrator/SKILL.md

The core deliverable: a new unified orchestrator skill replacing research-orchestrator and vs-arena.

**Files:**
- Create: `skills/orchestrator/SKILL.md`
- Read: `skills/research-orchestrator/SKILL.md` (source of model routing, checkpoint gating)
- Read: `skills/vs-arena/SKILL.md` (source of VS Arena protocol)
- Read: `config/agents.json` (agent IDs, tiers, models)
- Read: `config/personas.json` (V1-V5 constraints)

- [ ] **Step 1: Create skills/orchestrator/ directory**

```bash
mkdir -p "/Volumes/External SSD/Projects/Diverga/Diverga-core/skills/orchestrator"
```

- [ ] **Step 2: Write skills/orchestrator/SKILL.md**

Create the new orchestrator skill. Structure:

```markdown
---
name: orchestrator
description: |
  Unified Agent Teams orchestrator for Diverga v12.0.0.
  Manages Agent Teams creation, VS Arena debate, and subagent dispatch.
  Single entry point for all parallel/debate workflows.
  Replaces research-orchestrator and vs-arena skills.
  Triggers: orchestrator, agent team, create team, parallel agents, debate,
  competing, collaborate, VS Arena
version: "12.0.0"
---

# Diverga Orchestrator

## Role
Execution layer (HOW). Receives agent IDs from research-coordinator or
user, decides execution strategy (Agent Teams vs subagents), manages
lifecycle.

Does NOT handle: paradigm detection, checkpoint enforcement, agent
selection logic. Those belong to research-coordinator (WHAT).

## Invocation
1. Explicit: /diverga:orchestrator
2. Natural language: "create team", "debate", "parallel agents"
3. Auto: research-coordinator delegates parallel/debate work

## Decision Logic
[Full decision tree from spec Section 4]

## Agent Teams Mode
[When enabled + env var set]
### Team Lifecycle
### VS Arena Protocol (7 stages)
### Scenario Templates (5 scenarios from spec)
### Custom Teams

## Subagent Mode (Fallback)
[When teams disabled or unavailable]
### VS Arena without cross-critique
### Sequential dispatch

## Model Routing (from agents.json)
[HIGH/MEDIUM/LOW tier table — 24 agents]

## Token Cost Awareness
[Cost confirmation prompt]

## Removed Modes
Autonomous modes (Sisyphus, OMC, ralph, ultrawork, ecomode) were removed
in v6.0. See CHANGELOG.md for history.
```

Key requirements:
- Total size target: ~10KB (half of old research-orchestrator + vs-arena combined)
- Include complete VS Arena 7-stage protocol from spec
- Include all 5 scenario templates from spec
- Include decision logic flowchart from spec
- Include subagent fallback with synthesis (no cross-critique) from spec
- Include custom team support examples from spec
- Model routing table: copy from agents.json (24 core agents only, not V1-V5)
- One-line Sisyphus/OMC removal notice (not 15 lines of null triggers)

- [ ] **Step 3: Commit new orchestrator**

```bash
git add skills/orchestrator/SKILL.md
git commit -m "feat: create unified /diverga:orchestrator skill

Replaces research-orchestrator + vs-arena with single entry point.
- Agent Teams lifecycle (create, manage, cleanup)
- VS Arena debate with real cross-critique via Teams mailbox
- Subagent fallback with orchestrator-synthesized comparison
- 5 scenario templates: VS Arena, SR pipeline, cross-method, review, custom
- Decision logic: teams vs subagents based on config + env var

Co-Authored-By: Claude Opus 4.6 (1M context) <noreply@anthropic.com>"
```

---

### Task 4: Slim down research-coordinator/SKILL.md

Remove duplicated content (routing tables, checkpoint enforcement, version history, VS Arena details) and add orchestrator delegation.

**Files:**
- Modify: `skills/research-coordinator/SKILL.md`

- [ ] **Step 1: Read current research-coordinator/SKILL.md**

Read the full 726-line file. Identify sections to remove:
- "Multi-Agent Dispatch Protocol" (lines 58-85) — moved to orchestrator
- "Model Routing" section with Agent-Model Mapping table — moved to orchestrator
- "Task Tool Usage" code blocks — moved to orchestrator
- "VS-Research Methodology" VS process detail — kept briefly, detail in orchestrator
- "Version History" section — replaced with 1-line CHANGELOG reference
- "What Was Removed in v6.0" (Sisyphus, Iron Law, OMC) — replaced with 1-line note
- "Systematic Review Automation" pipeline diagram — kept, but remove delegation code blocks

- [ ] **Step 2: Rewrite research-coordinator/SKILL.md**

Target: ~12KB (down from 28.3KB). Keep:
- Frontmatter (update version to "12.0.0")
- Checkpoint enforcement rules (reference docs/CHECKPOINT-RULES.md for detail)
- Paradigm detection section
- Agent Catalog (24 agents) — keep as reference table
- Checkpoint types and required/recommended/optional tables
- Quick Start section
- Systematic Review checkpoint summary (no code blocks)

Add new section:
```markdown
## Orchestrator Delegation

When parallel execution or inter-agent debate is needed:
1. Determine which agents to invoke
2. Delegate to /diverga:orchestrator with agent IDs and context
3. Orchestrator handles Agent Teams vs subagent decision

Do NOT dispatch agents directly when:
- Multiple agents need to communicate (use orchestrator)
- VS Arena debate is triggered (use orchestrator)
- I0 systematic review pipeline needs parallel fetchers (use orchestrator)
```

Replace removed sections with:
```markdown
## Reference
- Checkpoint enforcement rules: docs/CHECKPOINT-RULES.md
- Model routing and execution: /diverga:orchestrator
- Architecture and systems: docs/ARCHITECTURE.md
- Autonomous modes removed in v6.0: see CHANGELOG.md
```

- [ ] **Step 3: Verify size**

```bash
wc -c "/Volumes/External SSD/Projects/Diverga/Diverga-core/skills/research-coordinator/SKILL.md"
```

Expected: < 15,000 bytes (down from 28,317).

- [ ] **Step 4: Commit slimmed coordinator**

```bash
git add skills/research-coordinator/SKILL.md
git commit -m "refactor: slim research-coordinator from 28KB to ~12KB

Removed: model routing tables (-> orchestrator), VS detail (-> orchestrator),
Multi-Agent Dispatch Protocol (-> orchestrator), version history (-> CHANGELOG),
Sisyphus/OMC removal docs (-> 1-line reference).
Added: orchestrator delegation section.

Co-Authored-By: Claude Opus 4.6 (1M context) <noreply@anthropic.com>"
```

---

### Task 5: Rewrite CLAUDE.md

Slim from 16.8KB to <5KB. Keep only what every session needs.

**Files:**
- Modify: `CLAUDE.md`
- Read: `docs/CHECKPOINT-RULES.md` (verify content was extracted)
- Read: `docs/ARCHITECTURE.md` (verify content was extracted)
- Read: `docs/MCP-TOOLS.md` (verify content was extracted)

- [ ] **Step 1: Read current CLAUDE.md**

Read the full file. Confirm that all extracted content from Task 1 is now in docs/.

- [ ] **Step 2: Rewrite CLAUDE.md**

New structure (target <5KB):

```markdown
# Diverga v12.0.0 -- Research Methodology AI Assistant

## Quick Start
[3 example prompts, 5 auto-steps]

## Agents (29 = 24 core + 5 VS Arena)
[Compact 2-column table: ID | Name | Cat | Model]

## Model Routing
| Tier | Model | When |
| HIGH | opus | Architecture, complex design |
| MEDIUM | sonnet | Standard tasks, search, writing |
| LOW | haiku | Quick validation, code gen, RAG |

## Checkpoint Types
| Level | Behavior |
| REQUIRED | System STOPS. Cannot proceed without approval. |
| RECOMMENDED | System PAUSES. Suggests approval. |
| OPTIONAL | System ASKS. Defaults available. |

## Paradigm Detection
[Keyword lists for quant/qual/mixed, 3 lines each]

## Reference
- Checkpoint enforcement rules: docs/CHECKPOINT-RULES.md
- Architecture and systems: docs/ARCHITECTURE.md
- MCP tools reference: docs/MCP-TOOLS.md
- Agent Teams orchestration: /diverga:orchestrator
- Full agent details: AGENTS.md
```

Do NOT include: Rules 1-6, hook enforcement, MCP tool tables, memory commands, pipeline details, VS Arena config, core systems table.

- [ ] **Step 3: Verify size**

```bash
wc -c "/Volumes/External SSD/Projects/Diverga/Diverga-core/CLAUDE.md"
```

Expected: < 5,000 bytes.

- [ ] **Step 4: Commit slim CLAUDE.md**

```bash
git add CLAUDE.md
git commit -m "refactor: slim CLAUDE.md from 16.8KB to <5KB

Extracted to docs/: checkpoint rules, architecture, MCP tools, hooks.
Remaining: agent table, model routing, checkpoint types, paradigm detection.
Reduces every-session token load from ~4,200 to ~1,250.

Co-Authored-By: Claude Opus 4.6 (1M context) <noreply@anthropic.com>"
```

---

### Task 6: Update setup skill (merge Agent Teams + VS Arena)

Replace separate Step 4 (VS Arena) with merged Agent Teams & VS Arena step.

**Files:**
- Modify: `skills/setup/SKILL.md`

- [ ] **Step 1: Read current setup/SKILL.md**

Read the full file. Locate Step 4 (VS Arena Configuration).

- [ ] **Step 2: Replace Step 4 with merged Agent Teams & VS Arena**

Replace the current Step 4 (VS Arena Configuration) with:

```markdown
### Step 4: Agent Teams & VS Arena

question: "Configure multi-agent collaboration mode"
header: "Agent Teams"
options:
  - label: "Agent Teams + VS Arena (Recommended)"
    description: "Full parallel execution with inter-agent communication.
                  VS Arena debates use real cross-critique between personas.
                  Requires Claude Code v2.1.32+. Higher token usage."
  - label: "Subagents + Classic VS (Default)"
    description: "Agents run as subagents. VS Arena generates options from
                  single agent (no cross-critique). Lower cost."
  - label: "Disabled"
    description: "No multi-agent features. Single agent execution only."
```

Update config generation logic:
- "Agent Teams + VS Arena": `agent_teams.enabled=true`, `vs_arena.enabled=true`, `vs_arena.cross_critique=true`, add `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1` to settings.json env
- "Subagents + Classic VS": `agent_teams.enabled=false`, `vs_arena.enabled=true`, `vs_arena.cross_critique=false`
- "Disabled": both false

Update version in frontmatter to "12.0.0".

Update completion message: replace "New in v11.1" with "New in v12.0" mentioning Agent Teams orchestrator.

- [ ] **Step 3: Commit setup update**

```bash
git add skills/setup/SKILL.md
git commit -m "feat: merge Agent Teams + VS Arena into setup Step 4

Replaces separate VS Arena step with unified multi-agent collaboration toggle.
Three modes: Agent Teams + VS Arena / Subagents + Classic VS / Disabled.
Sets CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1 in settings.json when enabled.

Co-Authored-By: Claude Opus 4.6 (1M context) <noreply@anthropic.com>"
```

---

### Task 7: Update config/diverga-config.json

Ensure clean config structure with agent_teams and vs_arena sections.

**Files:**
- Modify: `config/diverga-config.json`

- [ ] **Step 1: Read current config**

Read `config/diverga-config.json`.

- [ ] **Step 2: Update config**

Update to:
```json
{
  "version": "12.0.0",
  "human_checkpoints": {
    "enabled": true,
    "required": [
      "CP_PARADIGM",
      "CP_METHODOLOGY"
    ],
    "optional": [
      "CP_THEORY",
      "CP_DATA_VALIDATION"
    ]
  },
  "default_paradigm": "auto",
  "language": "en",
  "model_routing": {
    "high": "opus",
    "medium": "sonnet",
    "low": "haiku"
  },
  "vs_arena": {
    "enabled": false,
    "team_size": 3,
    "cross_critique": false
  },
  "agent_teams": {
    "enabled": false
  }
}
```

Changes:
- Version: "11.3.1" -> "12.0.0"
- Remove `llm_provider` and `llm_api_key_env` (Claude Code handles auth)
- Remove `auto_activate` and `scenarios` from agent_teams (orchestrator decides internally)
- Keep `agent_teams.enabled` as the single toggle

- [ ] **Step 3: Commit config update**

```bash
git add config/diverga-config.json
git commit -m "chore: update diverga-config.json for v12.0.0

Remove llm_provider/api_key (Claude Code handles auth).
Simplify agent_teams to single enabled toggle.

Co-Authored-By: Claude Opus 4.6 (1M context) <noreply@anthropic.com>"
```

---

### Task 8: Delete old skills

Remove research-orchestrator and vs-arena directories (replaced by orchestrator).

**Files:**
- Delete: `skills/research-orchestrator/SKILL.md` (and directory)
- Delete: `skills/vs-arena/SKILL.md` (and directory)

- [ ] **Step 1: Delete old skill directories**

```bash
cd "/Volumes/External SSD/Projects/Diverga/Diverga-core"
rm -rf skills/research-orchestrator
rm -rf skills/vs-arena
```

- [ ] **Step 2: Verify no references remain**

```bash
grep -r "research-orchestrator" --include="*.md" --include="*.json" skills/ CLAUDE.md AGENTS.md | head -20
grep -r "/vs-arena" --include="*.md" --include="*.json" skills/ CLAUDE.md AGENTS.md | head -20
```

Expected: No active references (CHANGELOG.md historical notes are OK).

- [ ] **Step 3: Commit deletions**

```bash
git add -A
git commit -m "feat!: remove research-orchestrator and vs-arena skills

BREAKING: /diverga:research-orchestrator and /diverga:vs-arena no longer exist.
Use /diverga:orchestrator for all Agent Teams and VS Arena functionality.

Co-Authored-By: Claude Opus 4.6 (1M context) <noreply@anthropic.com>"
```

---

### Task 9: Update tests

Update test expectations for new skill structure (34 skills, not 35).

**Files:**
- Modify: `tests/test_skill_structure.py`
- Modify: `tests/test_version_consistency.py`

- [ ] **Step 1: Update test_skill_structure.py**

Changes to `tests/test_skill_structure.py`:

In `SYSTEM_SKILLS` list (line 38-50):
- Remove: `"research-orchestrator"`
- Remove: `"vs-arena"`
- Add: `"orchestrator"`
- Result: 10 system skills (was 11)

In `test_agent_skill_count`: keep at 24.

In `test_system_skill_count` (line 125-133): change 11 to 10.

In `test_total_skill_count` (line 135-143): change 35 to 34.

- [ ] **Step 2: Update test_version_consistency.py**

Changes to `tests/test_version_consistency.py`:

Line 23: Change `EXPECTED_VERSION = "11.1.0"` to `EXPECTED_VERSION = "12.0.0"`

Line 158 (`test_skill_count_matches_expected`): change 35 to 34.

- [ ] **Step 3: Run tests**

```bash
cd "/Volumes/External SSD/Projects/Diverga/Diverga-core"
python -m pytest tests/test_skill_structure.py tests/test_version_consistency.py -v 2>&1 | head -60
```

Expected: Some tests will fail because version hasn't been bumped in all files yet. That's OK — Task 10 handles version sync.

- [ ] **Step 4: Commit test updates**

```bash
git add tests/test_skill_structure.py tests/test_version_consistency.py
git commit -m "test: update skill structure and version tests for v12.0.0

Skill count: 35 -> 34 (removed research-orchestrator, vs-arena; added orchestrator).
System skills: 11 -> 10.
Expected version: 11.1.0 -> 12.0.0.

Co-Authored-By: Claude Opus 4.6 (1M context) <noreply@anthropic.com>"
```

---

### Task 10: Version bump and metadata sync

Update version across all manifests and skill frontmatters.

**Files:**
- Modify: `package.json` (version field)
- Modify: `plugin.json` (version field)
- Modify: `.claude-plugin/plugin.json` (version field)
- Modify: `.claude-plugin/marketplace.json` (version field)
- Modify: `pyproject.toml` (version field)
- Modify: `config/agents.json` (version field)
- Modify: All `skills/*/SKILL.md` (frontmatter version)
- Modify: `AGENTS.md` (version reference)

- [ ] **Step 1: Update package.json version**

Change `"version": "11.3.1"` to `"version": "12.0.0"`.

Also update `"files"` array — remove old skill references:
```json
"files": [
  "dist",
  "README.md",
  "CLAUDE.md"
]
```

(The plugin system uses skills/ directory directly, not the npm files array.)

- [ ] **Step 2: Update plugin.json and marketplace.json**

Update version to "12.0.0" in:
- `plugin.json`
- `.claude-plugin/plugin.json`
- `.claude-plugin/marketplace.json` (plugins[0].version)

- [ ] **Step 3: Update pyproject.toml**

Change version to "12.0.0".

- [ ] **Step 4: Update config/agents.json**

Change `"version": "11.1.0"` to `"version": "12.0.0"`.

- [ ] **Step 5: Update all SKILL.md frontmatter versions**

```bash
cd "/Volumes/External SSD/Projects/Diverga/Diverga-core"
for skill_dir in skills/*/; do
  skill_file="${skill_dir}SKILL.md"
  if [ -f "$skill_file" ]; then
    # macOS sed syntax
    sed -i '' 's/version: "11\.[0-9]*\.[0-9]*"/version: "12.0.0"/g' "$skill_file"
  fi
done
```

Verify:
```bash
grep -r 'version:' skills/*/SKILL.md | grep -v "12.0.0"
```

Expected: no results (all should show 12.0.0).

- [ ] **Step 6: Update AGENTS.md version reference**

Update the version line in AGENTS.md header to reflect v12.0.0.

- [ ] **Step 7: Run full test suite**

```bash
cd "/Volumes/External SSD/Projects/Diverga/Diverga-core"
python -m pytest tests/test_skill_structure.py tests/test_version_consistency.py tests/test_agent_consistency.py -v
```

Expected: ALL PASS.

- [ ] **Step 8: Commit version bump**

```bash
git add -A
git commit -m "chore: bump version to 12.0.0 across all manifests

package.json, plugin.json, marketplace.json, pyproject.toml,
agents.json, AGENTS.md, and all 34 SKILL.md frontmatters.

Co-Authored-By: Claude Opus 4.6 (1M context) <noreply@anthropic.com>"
```

---

### Task 11: Final verification and deploy

**Files:**
- Read: All modified files (verification)

- [ ] **Step 1: Verify file structure**

```bash
cd "/Volumes/External SSD/Projects/Diverga/Diverga-core"

# New files exist
ls skills/orchestrator/SKILL.md
ls docs/CHECKPOINT-RULES.md
ls docs/ARCHITECTURE.md
ls docs/MCP-TOOLS.md

# Old files deleted
test ! -f .claude/config/research-coordinator-routing.yaml && echo "routing.yaml: DELETED OK"
test ! -f UPGRADE_ROADMAP.md && echo "UPGRADE_ROADMAP: DELETED OK"
test ! -d skills/research-orchestrator && echo "research-orchestrator: DELETED OK"
test ! -d skills/vs-arena && echo "vs-arena: DELETED OK"
```

- [ ] **Step 2: Verify CLAUDE.md size**

```bash
wc -c CLAUDE.md
```

Expected: < 5,000 bytes.

- [ ] **Step 3: Verify skill count**

```bash
ls -d skills/*/SKILL.md | wc -l
```

Expected: 34 (24 agent + 10 system).

- [ ] **Step 4: Run all tests**

```bash
python -m pytest tests/ -v --tb=short 2>&1 | tail -30
```

Expected: ALL PASS.

- [ ] **Step 5: Verify git status is clean**

```bash
git status
git log --oneline -8
```

Expected: clean working tree, 8 new commits for this release.

- [ ] **Step 6: Tag release (do NOT push yet)**

```bash
git tag -a v12.0.0 -m "v12.0.0: Orchestrator Redesign

BREAKING CHANGES:
- /diverga:research-orchestrator removed (use /diverga:orchestrator)
- /diverga:vs-arena removed (use /diverga:orchestrator)
- CLAUDE.md restructured (<5KB, details moved to docs/)

NEW:
- /diverga:orchestrator: unified Agent Teams + subagent dispatch
- Setup Step 4: merged Agent Teams & VS Arena toggle
- VS Arena cross-critique via Agent Teams mailbox (when enabled)

CLEANUP:
- Deleted 33-agent routing.yaml (v6.0 ghost)
- Deleted UPGRADE_ROADMAP.md (v8.0.1 era)
- research-coordinator slimmed from 28KB to ~12KB"
```

Wait for user confirmation before `git push origin main --tags`.
