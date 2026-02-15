# Diverga v9.0 Software Design Document (SDD)

**Version**: Draft 1.0
**Date**: 2026-02-15
**Author**: Hosung You + Claude Opus 4.6

---

## 1. Executive Summary

Diverga v9.0 is an **architecture release** that transitions the runtime from file-based YAML state to SQLite-backed atomic state, splits the monolithic MCP server into 3 specialized servers, and introduces an agent messaging system for pipeline coordination.

### Key Architectural Changes

| Component | v8.5.0 (Current) | v9.0.0 (Target) |
|-----------|-------------------|-------------------|
| State storage | YAML files (readFileSync/writeFileSync) | SQLite + YAML export |
| MCP servers | 1 monolithic (7 tools) | 3 specialized (checkpoint, memory, comm) |
| Agent communication | File system side-effects | MCP messaging (send/broadcast/mailbox) |
| Concurrency | Race-condition prone | ACID transactions + WAL mode |
| I-Pipeline | Sequential blocking | Parallel with dependency management |

---

## 2. Architecture Overview

### 2.1 Current Architecture (v8.5.0)

```
┌─────────────────────────────────────────────────────┐
│                  checkpoint-server.js                 │
│  ┌─────────────┬──────────────┬──────────────┐      │
│  │ checkPrereq │ markCheckpoint│ addDecision  │      │
│  │ cpStatus    │ priorityRead  │ priorityWrite│      │
│  │ projectStatus│              │              │      │
│  └─────┬───────┴──────┬───────┴──────┬───────┘      │
│        │              │              │               │
│  ┌─────▼──────────────▼──────────────▼─────┐        │
│  │     YAML Files (readFileSync/writeFileSync)│      │
│  │  checkpoints.yaml  decision-log.yaml     │        │
│  │  project-state.yaml priority-context.md  │        │
│  └─────────────────────────────────────────┘        │
└─────────────────────────────────────────────────────┘
```

**Problems:**
1. Single server with mixed concerns (checkpoints + state + context)
2. YAML read/write is not atomic — race conditions with parallel agents
3. No agent-to-agent communication mechanism
4. File locking not implemented

### 2.2 Target Architecture (v9.0.0)

```
┌──────────────────┐  ┌──────────────────┐  ┌──────────────────┐
│ checkpoint-server │  │  memory-server   │  │   comm-server    │
│                  │  │                  │  │                  │
│ checkPrerequisites│  │ readProjectState │  │ send             │
│ markCheckpoint   │  │ updateProjectState│  │ broadcast        │
│ checkpointStatus │  │ addDecision      │  │ mailbox          │
│                  │  │ listDecisions    │  │ acknowledge      │
│                  │  │ readPriority     │  │ registerAgent    │
│                  │  │ writePriority    │  │ createChannel    │
│                  │  │ exportToYaml     │  │ relayCheckpoint  │
└────────┬─────────┘  └────────┬─────────┘  └────────┬─────────┘
         │                     │                      │
         └─────────────────────┼──────────────────────┘
                               │
                    ┌──────────▼──────────┐
                    │   SQLite State      │
                    │   (sqlite-state.js) │
                    │                     │
                    │  Tables:            │
                    │  - checkpoints      │
                    │  - decisions        │
                    │  - project_state    │
                    │  - messages         │
                    │  - agents           │
                    │  - channels         │
                    │                     │
                    │  WAL mode           │
                    │  ACID transactions  │
                    └──────────┬──────────┘
                               │
                    ┌──────────▼──────────┐
                    │  YAML Export Layer   │
                    │  (researcher view)   │
                    │                     │
                    │  research/           │
                    │  ├── checkpoints.yaml│
                    │  ├── decision-log.yaml│
                    │  └── project-state.yaml│
                    └─────────────────────┘
```

---

## 3. Component Design

### 3.1 SQLite State Store (`mcp/lib/sqlite-state.js`)

**Purpose**: Atomic state management replacing YAML file I/O.

**Database Schema**:

```sql
-- Schema version tracking
CREATE TABLE IF NOT EXISTS schema_version (
  version INTEGER PRIMARY KEY,
  applied_at TEXT DEFAULT (datetime('now'))
);

-- Checkpoints
CREATE TABLE IF NOT EXISTS checkpoints (
  cp_id TEXT PRIMARY KEY,
  level TEXT CHECK(level IN ('required', 'recommended', 'optional')),
  status TEXT CHECK(status IN ('pending', 'approved', 'skipped')) DEFAULT 'pending',
  decision TEXT,
  rationale TEXT,
  approved_by TEXT DEFAULT 'user',
  created_at TEXT DEFAULT (datetime('now')),
  updated_at TEXT DEFAULT (datetime('now'))
);

-- Decisions (append-only with versioning)
CREATE TABLE IF NOT EXISTS decisions (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  decision_id TEXT NOT NULL,
  version INTEGER DEFAULT 1,
  checkpoint_id TEXT,
  selected TEXT NOT NULL,
  rationale TEXT,
  context TEXT, -- JSON
  created_at TEXT DEFAULT (datetime('now')),
  superseded_by INTEGER REFERENCES decisions(id)
);

-- Project state (key-value with JSON values)
CREATE TABLE IF NOT EXISTS project_state (
  key TEXT PRIMARY KEY,
  value TEXT NOT NULL, -- JSON
  updated_at TEXT DEFAULT (datetime('now'))
);

-- Messages
CREATE TABLE IF NOT EXISTS messages (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  message_id TEXT UNIQUE NOT NULL,
  from_agent TEXT NOT NULL,
  to_agent TEXT, -- NULL for broadcasts
  channel TEXT, -- NULL for direct messages
  content TEXT NOT NULL, -- JSON
  type TEXT DEFAULT 'data' CHECK(type IN ('data', 'status', 'checkpoint', 'error', 'progress')),
  priority TEXT DEFAULT 'normal' CHECK(priority IN ('low', 'normal', 'high', 'urgent')),
  status TEXT DEFAULT 'sent' CHECK(status IN ('sent', 'delivered', 'acknowledged')),
  created_at TEXT DEFAULT (datetime('now'))
);

-- Registered agents
CREATE TABLE IF NOT EXISTS agents (
  agent_id TEXT PRIMARY KEY,
  role TEXT,
  model TEXT,
  capabilities TEXT, -- JSON array
  registered_at TEXT DEFAULT (datetime('now')),
  last_seen TEXT DEFAULT (datetime('now'))
);

-- Channels
CREATE TABLE IF NOT EXISTS channels (
  name TEXT PRIMARY KEY,
  members TEXT NOT NULL, -- JSON array of agent_ids
  created_by TEXT NOT NULL,
  status TEXT DEFAULT 'active' CHECK(status IN ('active', 'archived')),
  created_at TEXT DEFAULT (datetime('now'))
);

-- Indexes
CREATE INDEX IF NOT EXISTS idx_messages_to ON messages(to_agent, status);
CREATE INDEX IF NOT EXISTS idx_messages_channel ON messages(channel);
CREATE INDEX IF NOT EXISTS idx_decisions_cp ON decisions(checkpoint_id);
```

**API**:

```javascript
export function createStateStore(dbPath) {
  // Opens SQLite with WAL mode
  // Returns object with methods:
  return {
    // Checkpoints
    markCheckpoint(cpId, decision, rationale),
    getCheckpoint(cpId),
    listCheckpoints(),
    isCheckpointApproved(cpId),
    getCheckpointsByLevel(level),

    // Decisions
    addDecision(cpId, selected, rationale, context?),
    listDecisions(),
    getDecision(decisionId),
    amendDecision(decisionId, newSelected, newRationale),

    // Project state
    getProjectState(),
    updateProjectState(updates),
    setStage(stageName),
    getStage(),

    // YAML export
    exportCheckpointsYaml(),
    exportDecisionLogYaml(),
    exportProjectStateYaml(),
    exportAll(outputDir),

    // Migration
    migrateFromYaml(researchDir),

    // Lifecycle
    close()
  };
}
```

**Design Decisions**:
- `better-sqlite3` for synchronous API (matches current sync behavior)
- WAL mode for concurrent read access
- ACID transactions for write safety
- Decision log is append-only with version chain (superseded_by)

### 3.2 Checkpoint Server (`mcp/servers/checkpoint-server.js`)

**Purpose**: Prerequisite checking and checkpoint marking.

**Tools** (3):
| Tool | Parameters | Description |
|------|-----------|-------------|
| `diverga_check_prerequisites` | `agent_id` | Check if agent's prerequisites are met |
| `diverga_mark_checkpoint` | `cp_id, decision, rationale` | Mark checkpoint as approved |
| `diverga_checkpoint_status` | `cp_id?` | Get checkpoint status (single or all) |

**Dependencies**: sqlite-state.js, agent-prerequisite-map.json

### 3.3 Memory Server (`mcp/servers/memory-server.js`)

**Purpose**: Project state, decisions, priority context.

**Tools** (7):
| Tool | Parameters | Description |
|------|-----------|-------------|
| `diverga_read_project_state` | — | Read full project state |
| `diverga_update_project_state` | `updates` | Merge updates into state |
| `diverga_add_decision` | `cp_id, decision, rationale` | Add decision to log |
| `diverga_list_decisions` | `filter?` | Query decision history |
| `diverga_read_priority` | — | Read priority context |
| `diverga_write_priority` | `content, max_chars?` | Write priority context |
| `diverga_export_yaml` | `output_dir?` | Export state as YAML |

**Dependencies**: sqlite-state.js

### 3.4 Comm Server (`mcp/servers/comm-server.js`)

**Purpose**: Agent-to-agent messaging for pipeline coordination.

**Tools** (7):
| Tool | Parameters | Description |
|------|-----------|-------------|
| `diverga_send` | `from, to, content, type?, priority?` | Send direct message |
| `diverga_broadcast` | `from, content, type?, exclude_self?` | Broadcast to all agents |
| `diverga_mailbox` | `agent_id, include_read?, type?` | Read agent's mailbox |
| `diverga_acknowledge` | `message_id` | Acknowledge message receipt |
| `diverga_register_agent` | `agent_id, role?, model?` | Register agent for messaging |
| `diverga_create_channel` | `name, members` | Create named channel |
| `diverga_relay_checkpoint` | `cp_id, decision, from, to_agents` | Relay checkpoint decision |

**Dependencies**: sqlite-state.js, messaging.js

### 3.5 Messaging Layer (`mcp/lib/messaging.js`)

**Purpose**: Message routing, channel management, checkpoint relay.

**Key Design**:
- Messages stored in SQLite via state store
- Channels for named groups (e.g., "scholarag-pipeline")
- Progress tracking for long-running pipelines
- Checkpoint relay for team coordination
- Message ordering guaranteed by auto-increment ID

---

## 4. Migration Strategy

### 4.1 Backward Compatibility

| Client | v8.5 Behavior | v9.0 Behavior | Migration |
|--------|---------------|---------------|-----------|
| SKILL.md agents | Call single MCP server | Call 3 specialized servers | Update MCP config in .mcp.json |
| YAML readers | Read research/*.yaml | Same files, auto-exported from SQLite | Transparent |
| Tests | Test YAML I/O | Test SQLite + YAML export | New test suites |

### 4.2 Migration Path

```
Phase 1: Add SQLite layer alongside YAML (non-breaking)
  - sqlite-state.js wraps YAML operations
  - Existing YAML paths continue to work
  - New SQLite DB auto-created on first use

Phase 2: Split MCP servers
  - Create 3 server files
  - Update .mcp.json configuration
  - Old single server deprecated but functional

Phase 3: Enable messaging
  - comm-server.js activated
  - I0 Team Lead uses messaging instead of file polling
  - Pipeline coordination via channels

Phase 4: Remove YAML primary storage
  - SQLite is sole source of truth
  - YAML files generated on-demand via exportAll()
  - research/ directory still human-readable
```

### 4.3 MCP Configuration

**Current (.mcp.json)**:
```json
{
  "mcpServers": {
    "diverga": {
      "command": "node",
      "args": ["mcp/checkpoint-server.js"]
    }
  }
}
```

**v9.0 (.mcp.json)**:
```json
{
  "mcpServers": {
    "diverga-checkpoint": {
      "command": "node",
      "args": ["mcp/servers/checkpoint-server.js"]
    },
    "diverga-memory": {
      "command": "node",
      "args": ["mcp/servers/memory-server.js"]
    },
    "diverga-comm": {
      "command": "node",
      "args": ["mcp/servers/comm-server.js"]
    }
  }
}
```

---

## 5. Data Flow

### 5.1 Checkpoint Flow (v9.0)

```
Agent A1 starts execution
    │
    ▼
checkpoint-server.checkPrerequisites("a1")
    │
    ├─ SQLite: SELECT * FROM checkpoints WHERE cp_id IN (prerequisites)
    │
    ▼
All prerequisites approved? ──No──→ Return { approved: false, missing: [...] }
    │
   Yes
    │
    ▼
Agent executes, reaches CP_RESEARCH_DIRECTION
    │
    ▼
AskUserQuestion (via SKILL.md prompt)
    │
    ▼
User selects option
    │
    ▼
checkpoint-server.markCheckpoint("CP_RESEARCH_DIRECTION", "Meta-analysis", "Need synthesis")
    │
    ├─ SQLite: INSERT OR REPLACE INTO checkpoints ...
    ├─ SQLite: INSERT INTO decisions ...
    ├─ YAML export: research/checkpoints.yaml updated
    │
    ▼
comm-server.relayCheckpoint("CP_RESEARCH_DIRECTION", "Meta-analysis", "a1", ["a2","b1"])
    │
    ├─ SQLite: INSERT INTO messages (type='checkpoint', priority='high') ...
    │
    ▼
Dependent agents receive checkpoint notification in their mailbox
```

### 5.2 I-Pipeline Flow (v9.0 with Teams)

```
I0 (Team Lead) starts
    │
    ▼
comm-server.createChannel("scholarag-pipeline", ["i1-ss","i1-oa","i1-arxiv","i2","i3"])
    │
    ▼
TeamCreate("scholarag-pipeline")
    │
    ├─ Task(i1, "Semantic Scholar") → comm-server.registerAgent("i1-ss", {role:"fetcher"})
    ├─ Task(i1, "OpenAlex")        → comm-server.registerAgent("i1-oa", {role:"fetcher"})
    └─ Task(i1, "arXiv")           → comm-server.registerAgent("i1-arxiv", {role:"fetcher"})
    │
    ▼ (parallel execution)
    │
Each I1 instance:
    ├─ Fetches papers
    ├─ comm-server.send("i1-ss", "i0", { papers: 847, source: "semantic_scholar" })
    └─ comm-server.reportProgress("i1-ss", { stage: "fetch", percent: 100 })
    │
    ▼
I0 checks: comm-server.getProgress("scholarag-pipeline")
    │ All 3 fetchers at 100%
    ▼
I0 triggers deduplication + I2 screening
    │
    ▼
I2: comm-server.send("i2", "i0", { screened: 312, included: 89 })
    │
    ▼
I0 triggers I3 RAG building
```

---

## 6. Testing Strategy

### 6.1 Test Pyramid

```
         ╱╲
        ╱  ╲        E2E Tests (5)
       ╱    ╲       - Full pipeline I0→I3
      ╱──────╲      - Checkpoint workflow
     ╱        ╲
    ╱ Integration╲  Integration Tests (30)
   ╱   Tests     ╲  - Server↔SQLite
  ╱                ╲ - Messaging↔Channels
 ╱──────────────────╲ - Migration YAML→SQLite
╱                    ╲
╱    Unit Tests       ╲ Unit Tests (120+)
╱  (per component)     ╲ - sqlite-state.js
╱──────────────────────╲ - messaging.js
                         - Each server's tools
```

### 6.2 Test Files

| File | Tests | Component |
|------|-------|-----------|
| `mcp/test/sqlite-state-v9.test.js` | ~43 | SQLite state layer |
| `mcp/test/checkpoint-server-v9.test.js` | ~40 | Split checkpoint server |
| `mcp/test/memory-server-v9.test.js` | ~40 | Memory server |
| `mcp/test/comm-server-v9.test.js` | ~40 | Comm server |
| `mcp/test/messaging-v9.test.js` | ~45 | Messaging layer |
| `mcp/test/generate.test.js` | ~20 | DX: generate.js |
| `mcp/test/sync-version.test.js` | ~15 | DX: sync-version.js |
| `mcp/test/doctor.test.js` | ~12 | DX: doctor.js |
| **Total** | **~255** | |

### 6.3 TDD Workflow

```
Phase 1 (Current): RED — Write all failing tests
Phase 2: GREEN — Implement minimal code to pass tests
Phase 3: REFACTOR — Optimize while keeping tests green
Phase 4: INTEGRATION — Wire servers together, run full suite
Phase 5: MIGRATION — Test YAML→SQLite migration path
```

---

## 7. Dependencies

### New Dependencies

| Package | Version | Purpose | Size |
|---------|---------|---------|------|
| `better-sqlite3` | ^11.0.0 | Synchronous SQLite3 bindings | ~2MB |

### Why better-sqlite3?

1. **Synchronous API** — matches existing sync file I/O pattern
2. **WAL mode** — concurrent reads during writes
3. **Performance** — 10-100x faster than file-based YAML for reads
4. **Transactions** — ACID guarantees for state consistency
5. **No external server** — embedded, zero-config
6. **Mature** — 10M+ weekly downloads, actively maintained

### Alternatives Considered

| Option | Rejected Because |
|--------|-----------------|
| sql.js (WASM) | Slower, larger bundle, no WAL |
| node:sqlite (built-in) | Async-only, experimental in Node 22+ |
| LevelDB | No SQL, harder to query decisions |
| JSON file with flock | Still file-based, no ACID |

---

## 8. Risk Assessment

| Risk | Probability | Impact | Mitigation |
|------|------------|--------|------------|
| better-sqlite3 native build fails | Low | High | Fallback to YAML mode |
| SQLite file corruption | Very Low | High | WAL mode + backup on export |
| MCP server split breaks existing | Medium | Medium | Deprecation period with old server |
| Message queue grows unbounded | Low | Low | Auto-prune messages > 30 days |
| Researcher YAML files stale | Medium | Low | Auto-export on every write |

---

## 9. Success Criteria

1. All 255+ tests pass (RED→GREEN)
2. Existing 120 checkpoint tests still pass (backward compat)
3. YAML export matches current YAML format exactly
4. I-pipeline runs 40%+ faster with parallel fetching via messaging
5. No race conditions under concurrent agent access
6. `npm run doctor` shows 9/9 (or more) checks passing
7. Migration from v8.5 YAML to v9.0 SQLite is lossless

---

## 10. Timeline

| Phase | Duration | Deliverable |
|-------|----------|-------------|
| TDD RED | 1 day | 255+ failing tests |
| sqlite-state.js GREEN | 2 days | SQLite layer passing 43 tests |
| Server split GREEN | 2 days | 3 servers passing 120 tests |
| Messaging GREEN | 2 days | Messaging passing 45 tests |
| Integration | 1 day | Full pipeline test |
| Migration | 1 day | YAML→SQLite migration |
| **Total** | **~9 days** | v9.0.0-alpha |
