# Architecture — v12.0.0

System architecture reference for Diverga.

**Clean Split: coordinator handles WHAT, orchestrator handles HOW.**

---

## Core Systems

| System | Implementation |
|--------|---------------|
| State | SQLite WAL mode (YAML fallback) |
| Hooks | prereq-enforcer.mjs (SQLite-based, hard-block for REQUIRED) |
| Config | config/agents.json (29 agents: 24 core + 5 VS Arena) |
| MCP | diverga-server.js (16 tools) + journal-server.js (6 tools) |
| Memory | 3-layer context with cross-session persistence |

---

## Key Pipelines

- **Humanization**: G5 (audit) -> G6 (transform) -> F5 (verify). Details: `docs/HUMANIZATION.md`
- **Meta-Analysis**: C5 (orchestrator with integrated data integrity + effect size + sensitivity)
- **Systematic Review**: I0 -> I1 (retrieval) -> I2 (screening) -> I3 (RAG)
- **Journal Matching**: G1 with journal MCP (search -> CP_JOURNAL_PRIORITIES -> rank -> CP_JOURNAL_SELECTION -> report)

---

## Hook Enforcement (v11.1)

The `prereq-enforcer.mjs` hook reads checkpoint state from SQLite (`diverga.db`) and enforces prerequisites:

| Missing Level | Behavior | Result |
|---------------|----------|--------|
| **REQUIRED** | **Hard block** | `continue: false` — agent CANNOT run |
| **RECOMMENDED** | Soft block | `continue: true` + warning in additionalContext |
| **OPTIONAL** | Pass through | No action |

### Debug Mode

```bash
DIVERGA_HOOK_DEBUG=1  # Enables verbose stderr logging
DIVERGA_RESEARCH_DIR=/path/to/project  # Override research directory detection
```

---

## Memory System

### 3-Layer Context

| Layer | Trigger | Description |
|-------|---------|-------------|
| Layer 1 | Keywords | "my research", "연구 진행", "where was I" auto-load context |
| Layer 2 | Task tool | `Task(subagent_type="diverga:*")` auto-injects context to agents |
| Layer 3 | CLI | `/diverga:memory context` for explicit full context |

### Key Commands

| Command | Description |
|---------|-------------|
| `/diverga:memory status` | Show project status |
| `/diverga:memory context` | Display full context |
| `/diverga:memory init` | Initialize new project |
| `/diverga:memory decision list` | List decisions |
| `/diverga:memory decision add` | Add decision |
| `/diverga:memory search "query"` | Semantic memory search |
| `/diverga:memory export --format md` | Export to Markdown |

### Context Keywords

**English**: "my research", "research status", "research progress", "where was I", "continue research", "remember", "memory", "context"

**Korean**: "내 연구", "연구 진행", "연구 상태", "어디까지", "지금 단계", "기억", "맥락"
