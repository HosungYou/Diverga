# Diverga Orchestrator Redesign Spec

**Date**: 2026-03-19
**Author**: Hosung You + Claude Opus 4.6
**Version**: v12.0.0 (target)
**Status**: Approved

---

## 1. Problem Statement

The current Diverga plugin (v11.3.1) has 3 overlapping skills for agent dispatch:

| Skill | Size | Role | Problem |
|-------|------|------|---------|
| `research-coordinator` | 28.3KB (726 lines) | Agent catalog, paradigm detection, checkpoints, pipelines, VS | Tries to do everything |
| `research-orchestrator` | 13.1KB (352 lines) | Execution flow, model routing, checkpoint gating | Duplicates coordinator's checkpoint lists |
| `vs-arena` | 6.2KB | Multi-persona methodology debate | Uses MCP tools in subagents (doesn't work) |

### Root Causes of Failure

1. **Role confusion**: 3 skills duplicate checkpoint lists, agent routing tables, and model tier assignments
2. **CLAUDE.md overload**: 16.8KB (~4,200 tokens) loaded every session — includes checkpoint enforcement rules, hook debug info, and MCP tool reference that are only needed during agent execution
3. **Cache desync**: Diverga-core is v11.3.1 but cached plugin is v11.1.1. `agent_teams` config exists in source but not in the running plugin
4. **routing.yaml ghost**: Deleted 33-agent routing file still exists in `.claude/config/`, potentially loaded by reference system
5. **VS Arena broken**: Cross-critique uses `diverga_message_send` MCP tool inside subagents, but subagents cannot access MCP servers

---

## 2. Design Decision: "Clean Split" Architecture

### Principle

Separate WHAT (domain knowledge) from HOW (execution strategy). Minimize CLAUDE.md. Single orchestrator entry point for all Agent Teams work.

### Architecture

```
CLAUDE.md (< 5KB)
  Agent list table + model routing + checkpoint type definitions only
  No enforcement rules, no MCP tool lists, no hook details

/diverga:orchestrator (NEW skill — replaces research-orchestrator + vs-arena)
  Agent Teams creation and management
  VS Arena debate (Teams mode + subagent fallback)
  Scenario evaluation (when to use Teams vs subagents)
  Single entry point for ALL parallel/debate workflows
  Triggers: explicit /diverga:orchestrator call, natural language team requests,
            auto-invocation when coordinator determines teams would help

/diverga:research-coordinator (SLIMMED — 28KB -> ~12KB)
  Paradigm detection + checkpoint flow only
  Agent selection ("which agent to call")
  Delegates execution to orchestrator when parallel/debate needed
  Removes: model routing tables, checkpoint enforcement rules, version history

docs/ (moved from CLAUDE.md)
  CHECKPOINT-RULES.md — Rules 1-6 detail
  ARCHITECTURE.md — Full system structure
  MCP-TOOLS.md — 16+6 tool reference
  HOOKS.md — Hook enforcement detail
```

### Why Not "Single Entry Point" (Approach B)

A single all-in-one orchestrator would grow to 30KB+, loading research domain knowledge even when only Teams management is needed. Clean Split keeps the orchestrator domain-agnostic and reusable.

---

## 3. File Changes

### DELETE

| File | Reason |
|------|--------|
| `.claude/config/research-coordinator-routing.yaml` | 33-agent v6.0 ghost. agents.json is SSoT |
| `UPGRADE_ROADMAP.md` | v8.0.1 era, references 44 agents. Never-released v8.1.0 roadmap |
| `skills/research-orchestrator/SKILL.md` | Replaced by new orchestrator |
| `skills/vs-arena/SKILL.md` | Absorbed into new orchestrator |

### CREATE

| File | Purpose |
|------|---------|
| `skills/orchestrator/SKILL.md` | New unified Agent Teams orchestrator |
| `docs/CHECKPOINT-RULES.md` | Moved from CLAUDE.md |
| `docs/ARCHITECTURE.md` | System structure (preserves architectural knowledge) |
| `docs/MCP-TOOLS.md` | Moved from CLAUDE.md |
| `docs/specs/2026-03-19-orchestrator-redesign.md` | This document |

### REWRITE

| File | Change |
|------|--------|
| `CLAUDE.md` | Slim from 16.8KB to < 5KB. Remove checkpoint rules, MCP lists, hook details |
| `skills/research-coordinator/SKILL.md` | Slim from 28.3KB to ~12KB. Remove routing tables, version history, VS details |
| `skills/setup/SKILL.md` | Add Step 5: Agent Teams toggle |
| `config/diverga-config.json` | Ensure `agent_teams` section with env var control |

### KEEP (no changes)

| File | Reason |
|------|--------|
| `config/agents.json` | Correct SSoT with 29 agents |
| `AGENTS.md` | Correct v11.0 documentation |
| `CHANGELOG.md` | Accurate historical record |
| `agents/*.md` | 29 agent definitions (24 core + 5 VS Arena) |
| `skills/humanize/SKILL.md` | OMC defense kept (1 location is fine) |

---

## 4. New `/diverga:orchestrator` Skill Design

### Skill Metadata

```yaml
Location: skills/orchestrator/SKILL.md
Name: orchestrator
Triggers:
  en: ["orchestrator", "agent team", "create team", "parallel agents",
       "debate", "competing", "collaborate", "VS Arena"]
  ko: ["오케스트레이터", "에이전트 팀", "팀 생성", "병렬", "토론"]
```

### Relationship with research-coordinator

```
research-coordinator (WHAT)          orchestrator (HOW)
  - Paradigm detection                - Agent Teams lifecycle
  - Agent selection by trigger        - Team creation / cleanup
  - Checkpoint flow management        - Subagent dispatch
  - "Which agents to call"            - "How to run them"
       |                                    ^
       |  delegates parallel/debate work    |
       +------------------------------------+

Entry points:
  User says research topic --> research-coordinator (auto-trigger)
                               --> orchestrator (if teams needed)
  User says /diverga:orchestrator --> orchestrator (direct)
  User says "create a team" --> orchestrator (natural language)

No circular dependency: coordinator calls orchestrator, never reverse.
Orchestrator does NOT call coordinator. It receives agent IDs and executes.
```

### Invocation Modes

```
1. Explicit:     /diverga:orchestrator
2. Natural lang: "Create a team to debate methodology options"
                 "Run VS Arena for this research question"
                 "Fetch papers from 3 databases in parallel"
3. Auto-invoke:  research-coordinator delegates when parallel/debate needed
```

### Prerequisite Handling

```
Orchestrator does NOT enforce research checkpoints itself.
It trusts the caller (coordinator or user) to have resolved prerequisites.

When called directly by user:
  - If research context exists (.research/), read it for context
  - If no context, proceed without checkpoint gating
  - Orchestrator's own checkpoints: only token cost confirmation

When called by coordinator:
  - Coordinator has already resolved all prerequisites
  - Orchestrator receives: agent IDs + context + execution mode
```

### Decision Logic

```
Request received
  |
  v
Check config.agent_teams.enabled
  |
  +-- false --> Always use subagents (Task with run_in_background)
  |
  +-- true --> Check CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS env var
       |
       +-- not set --> Subagent fallback + warn user
       |
       +-- set --> Evaluate scenario
            |
            +-- Inter-agent debate needed? --> Agent Teams
            |     (VS Arena, cross-method comparison, competing hypotheses)
            |
            +-- Parallel independent work? --> Agent Teams
            |     (multi-DB fetch, parallel review, concurrent analysis)
            |
            +-- Sequential pipeline? --> Subagents
            |     (G5->G6->F5 humanize, single agent tasks)
            |
            +-- Simple single agent? --> Direct Task dispatch
```

### Agent Teams Scenarios

| Scenario | Team Name | Teammates | When |
|----------|-----------|-----------|------|
| VS Arena Debate | `vs-arena-{topic}` | 3 of V1-V5 personas | CP_METHODOLOGY_APPROVAL or explicit request |
| Systematic Review | `sr-pipeline-{topic}` | I1 x3 (per DB) | I0 pipeline with multi-DB fetch |
| Cross-Method | `method-compare-{topic}` | C1+C2+C3 or subset | Competing design recommendations |
| Parallel Review | `review-{topic}` | 2-5 domain agents | Quality review from multiple angles |
| Custom | `{user-specified}` | User-specified | Explicit /diverga:orchestrator call |

### VS Arena in Teams Mode

```
Stage 1: Context Collection (from diverga_project_status or user input)
Stage 2: Persona Selection (3 of V1-V5 based on paradigm)
Stage 3: Team Creation
         TeamCreate("vs-arena-{topic}")
         Spawn 3 persona teammates
Stage 4: Independent Research (each persona investigates independently)
Stage 5: Cross-Critique (teammates message each other directly via mailbox)
Stage 6: Synthesis + Checkpoint (lead collects, presents at CP_METHODOLOGY_APPROVAL)
Stage 7: Cleanup (TeamDelete after user selection)
```

### Subagent Fallback (when Teams unavailable)

```
Same stages, but:
- Stage 3: Task(subagent_type="diverga:v{N}", run_in_background=true)
- Stage 5: SKIP cross-critique (subagents cannot message each other)
           Orchestrator synthesizes: reads all 3 outputs, identifies
           overlaps and contradictions, presents unified comparison
- Stage 6: Lead presents synthesized comparison at checkpoint
```

Cross-critique is permanently disabled in subagent mode. This is a known
limitation, not a bug. The orchestrator compensates by performing its own
synthesis of competing recommendations.

### Custom Team Support

Users can request custom teams via natural language:

```
User: "/diverga:orchestrator create a team with C1 and C2 to compare
       quantitative designs for my RCT study"

Orchestrator parses:
  - agents: [C1, C2]
  - purpose: competing design recommendations
  - team_name: "design-compare-rct"
  - teammate_count: 2

User: "Have 3 agents review my methodology section from different angles"

Orchestrator infers:
  - agents: [X1 (ethics), B2 (quality), G2 (publication readiness)]
  - purpose: parallel review
  - team_name: "review-methodology"
  - teammate_count: 3
```

Maximum teammates: 5 (per Claude Code best practices).
If user requests more, orchestrator suggests splitting into phases.

### Token Cost Awareness

```
Before creating a team, orchestrator states:
"Agent Teams will spawn N independent sessions, each consuming separate tokens.
Estimated additional cost: ~{N * avg_tokens} tokens.
Proceed? [Y] Yes / [S] Use subagents instead / [N] Cancel"

Skip this prompt if user explicitly requested teams.
```

---

## 5. Setup Changes

### Current step structure -> New structure

```
Current (v11.3.1):                   New (v12.0.0):
  Step 0: Project Detection            Step 0: Project Detection (unchanged)
  Step 1: Checkpoint Level             Step 1: Checkpoint Level (unchanged)
  Step 2: OpenAlex Email               Step 2: OpenAlex Email (unchanged)
  Step 3: HUD Configuration            Step 3: HUD Configuration (unchanged)
  Step 4: VS Arena Configuration       Step 4: Agent Teams & VS Arena (MERGED)
  Step 5: Generate Configuration       Step 5: Generate Configuration (unchanged)
```

VS Arena is now part of Agent Teams. Step 4 merges both into one question.

### New Step 4: Agent Teams & VS Arena

```
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

When "Agent Teams + VS Arena" selected:
- Set `config.agent_teams.enabled = true`
- Set `config.vs_arena.enabled = true`
- Set `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1` in user's settings.json env

When "Subagents + Classic VS" selected:
- Set `config.agent_teams.enabled = false`
- Set `config.vs_arena.enabled = true` (classic mode)

When "Disabled" selected:
- Set `config.agent_teams.enabled = false`
- Set `config.vs_arena.enabled = false`

Config output:
```json
{
  "agent_teams": {
    "enabled": true
  },
  "vs_arena": {
    "enabled": true,
    "team_size": 3,
    "cross_critique": true
  }
}
```

---

## 6. CLAUDE.md Slim-Down Plan

### Remove from CLAUDE.md (move to docs/)

- Checkpoint enforcement Rules 1-6 (2,800 bytes) -> docs/CHECKPOINT-RULES.md
- Hook enforcement section (1,200 bytes) -> docs/HOOKS.md
- MCP Tools tables: diverga (16 tools) + journal (6 tools) (2,500 bytes) -> docs/MCP-TOOLS.md
- Memory system commands table (800 bytes) -> docs/MEMORY-COMMANDS.md
- VS Arena detail (1,000 bytes) -> orchestrator skill
- Key Pipelines section (500 bytes) -> docs/ARCHITECTURE.md
- Core Systems table (400 bytes) -> docs/ARCHITECTURE.md

### Keep in CLAUDE.md

- Agent overview table (29 agents, ~1,200 bytes)
- Model routing table (3 tiers, ~200 bytes)
- Checkpoint types table (3 levels, ~300 bytes)
- Quick start (3 examples, ~300 bytes)
- Paradigm detection keywords (~500 bytes)
- One-line references to docs/ files (~200 bytes)

**Target**: < 5KB (~1,250 tokens). Down from 16.8KB (~4,200 tokens).

---

## 7. Legacy Artifact Cleanup

### Priority 1: Delete immediately

| Artifact | Path | Issue |
|----------|------|-------|
| routing.yaml | `.claude/config/research-coordinator-routing.yaml` | 33-agent ghost from v6.0 |
| UPGRADE_ROADMAP.md | `UPGRADE_ROADMAP.md` | v8.0.1 era, references 44 agents |
| Old orchestrator | `skills/research-orchestrator/` | Replaced by new `skills/orchestrator/` |
| Old vs-arena | `skills/vs-arena/` | Absorbed into orchestrator |

### Priority 2: Reduce defensive cruft

| File | Current | After |
|------|---------|-------|
| `skills/research-orchestrator/SKILL.md` | 15 lines of Sisyphus/OMC/ralph null triggers | DELETED (file removed) |
| `skills/research-coordinator/SKILL.md` | 30 lines of "What Was Removed in v6.0" | 1-line note: "Autonomous modes removed in v6.0. See CHANGELOG.md" |
| `skills/humanize/SKILL.md` | 8 lines of OMC defense | KEEP (single location is acceptable) |

### Priority 3: Reference files audit

38 reference files (532KB) should be reviewed separately. Not in scope for this release, but flagged for future cleanup.

---

## 8. Version Strategy

- This release: **v12.0.0** (breaking change: skill names, CLAUDE.md structure)
- Semver justification: removing `research-orchestrator` and `vs-arena` as standalone skills is a breaking change for users who invoke them directly

---

## 9. Implementation Order

1. Create `docs/CHECKPOINT-RULES.md`, `docs/ARCHITECTURE.md`, `docs/MCP-TOOLS.md` (extract from CLAUDE.md)
2. Delete legacy files (routing.yaml, UPGRADE_ROADMAP.md)
3. Create new `skills/orchestrator/SKILL.md`
4. Slim down `skills/research-coordinator/SKILL.md`
5. Rewrite `CLAUDE.md` (< 5KB)
6. Update `skills/setup/SKILL.md` (add Agent Teams step)
7. Update `config/diverga-config.json`
8. Delete old `skills/research-orchestrator/`, `skills/vs-arena/`
9. Update `AGENTS.md` and `package.json` version
10. Test: plugin install + verify skill loading
11. Deploy + release notes
