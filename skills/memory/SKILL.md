---
name: memory
description: |
  DIVERGA Memory System - Persistent context preservation for research lifecycle continuity.
  Provides semantic search, project-scoped context, decision audit trails, and lifecycle hooks.
  Triggers: remember, memory, context, recall, session, checkpoint, decision, persist
  한국어: 기억, 맥락, 세션, 체크포인트
version: "6.9.0"
---

# DIVERGA Memory System

**Persistent context preservation for complete research lifecycle continuity**

## Overview

The DIVERGA Memory System eliminates the re-explanation burden by maintaining persistent research context across sessions, projects, and decision points. Unlike traditional AI assistants that lose context between conversations, DIVERGA Memory provides **semantic search**, **project-scoped context**, **decision audit trails**, and **lifecycle hooks** that automatically capture critical information at key research milestones.

### Core Value Proposition

1. **No Re-Explanation**: Tell your research question once, never repeat it
2. **Cross-Session Continuity**: Resume exactly where you left off
3. **Decision Traceability**: Audit trail of every critical choice
4. **Smart Context Loading**: Automatically loads relevant memories when needed
5. **Multi-Project Support**: Isolated memory spaces per research project

### Memory Types

| Type | Scope | Persistence | Example |
|------|-------|-------------|---------|
| **Project Context** | Single project | Permanent | Research question, paradigm, methodology |
| **Session Memory** | Single conversation | 7 days | Current stage, recent decisions |
| **Decision Log** | Project-wide | Permanent | Theory selection, checkpoint approvals |
| **Research Notes** | Project-wide | Permanent | Literature insights, analysis findings |
| **Tool Preferences** | Global | Permanent | Default databases, citation style |

---

## CLI Commands

### Core Commands

```bash
# Search memories semantically
/diverga:memory search "meta-analysis heterogeneity"

# Show current memory status
/diverga:memory status

# Show active project context
/diverga:memory context

# View session history
/diverga:memory history

# Export memories to file
/diverga:memory export --format md
/diverga:memory export --format json
/diverga:memory export --format yaml

# Clear session memory (keeps project context)
/diverga:memory clear session

# Archive project memory
/diverga:memory archive "AI-Education-Meta-2025"
```

### Advanced Commands

```bash
# Query specific memory type
/diverga:memory search --type decision "theory selection"
/diverga:memory search --type context "research question"

# Filter by date range
/diverga:memory history --from 2026-01-01 --to 2026-01-31

# Export specific project
/diverga:memory export --project "AI-Education-Meta-2025" --format md

# Merge memories from multiple sessions
/diverga:memory merge session-123 session-456

# Show memory statistics
/diverga:memory stats
```

---

## Auto-Behavior (Lifecycle Hooks)

The Memory System automatically captures context at critical lifecycle events WITHOUT manual intervention.

### Session Lifecycle

```
session_start
  ↓
[Auto-Load] Retrieve project context, recent decisions, active checkpoints
  ↓
[Present] "Resuming research on: {research_question}. Last checkpoint: {checkpoint_id}"
```

**Example**:
```
User starts conversation → System detects project ID in working directory
  → Auto-loads: Research question, paradigm, methodology, last 5 decisions
  → Shows: "Welcome back! Resuming meta-analysis on AI-assisted learning.
            Last session: Data extraction (C6) with 15/50 papers completed."
```

### Checkpoint Reached

```
checkpoint_triggered (e.g., CP_THEORY_SELECTION)
  ↓
[Capture] User selection, alternatives presented, T-Scores, timestamp
  ↓
[Store] Decision log entry with full context
  ↓
[Link] Associate with research stage, agent, and project
```

**Example**:
```
User selects Self-Determination Theory (T=0.55) at CP_THEORY_SELECTION
  → Auto-save: {
      "checkpoint": "CP_THEORY_SELECTION",
      "decision": "Self-Determination Theory",
      "alternatives": ["Social Cognitive Theory", "Activity Theory"],
      "t_score": 0.55,
      "rationale": "User prioritizes motivation constructs",
      "timestamp": "2026-02-01T14:30:00Z"
    }
  → Context update: project-state.yaml adds theoretical_framework
```

### Session End

```
session_end
  ↓
[Summarize] Extract key decisions, progress, next steps
  ↓
[Store] Session summary with semantic embedding
  ↓
[Update] Project status, checkpoint progress
```

**Example**:
```
Session lasted 45 minutes, completed 3 checkpoints
  → Auto-generate summary:
    "Completed: Literature search strategy design (B1)
     Decisions: Selected Semantic Scholar + OpenAlex databases
     Next: Begin paper retrieval (I1) with 2015-2025 date range
     Checkpoint: 🔴 SCH_DATABASE_SELECTION approved"
  → Store summary with embeddings for future search
```

### Other Lifecycle Hooks

| Hook | Trigger | Auto-Capture |
|------|---------|--------------|
| `agent_completed` | Agent finishes task | Agent output, time taken, success/failure |
| `checkpoint_bypassed` | User skips 🟡 optional checkpoint | Skip reason, default values used |
| `error_occurred` | System error | Error type, context, recovery action |
| `export_completed` | Document export | Export type, file location, timestamp |
| `project_archived` | Project moved to archive | Final state snapshot |

---

## Configuration

### Location

Global configuration: `~/.diverga/config/memory.yaml`

Project-specific overrides: `.research/memory-config.yaml`

### Default Configuration

```yaml
# ~/.diverga/config/memory.yaml

memory:
  # Storage backend
  backend: local  # Options: local, cloud, hybrid
  storage_path: ~/.diverga/memory/

  # Semantic search
  embeddings:
    model: text-embedding-3-small  # OpenAI embeddings
    dimension: 1536
    similarity_threshold: 0.7

  # Auto-behavior settings
  lifecycle_hooks:
    session_start: true
    session_end: true
    checkpoint_reached: true
    agent_completed: true

  # Retention policies
  retention:
    session_memory: 7d      # 7 days
    project_context: permanent
    decision_log: permanent
    research_notes: permanent

  # Export defaults
  export:
    default_format: markdown
    include_timestamps: true
    include_metadata: true

  # Privacy settings
  privacy:
    anonymize_on_export: false
    include_user_inputs: true
    redact_api_keys: true
```

### Project-Specific Overrides

```yaml
# .research/memory-config.yaml

memory:
  # Override global settings for this project
  export:
    default_format: json  # This project prefers JSON

  # Custom retention for sensitive data
  retention:
    session_memory: 1d  # Delete after 1 day

  # Privacy for IRB-regulated research
  privacy:
    anonymize_on_export: true
    include_user_inputs: false  # Redact user inputs
```

---

## Data Structure

### Project Context Schema

```yaml
# .research/project-state.yaml

project:
  id: "AI-Education-Meta-2025"
  created: "2026-01-15T10:00:00Z"
  last_updated: "2026-02-01T14:30:00Z"

research:
  question: "How effective are AI-assisted learning interventions?"
  paradigm: quantitative
  type: meta-analysis
  domain: education

methodology:
  design: meta-analytic
  databases: [semantic_scholar, openalex, arxiv]
  date_range: [2015, 2025]
  inclusion_criteria:
    - "RCT or quasi-experimental"
    - "K-12 or higher education"
    - "AI-assisted learning intervention"
  exclusion_criteria:
    - "Non-English"
    - "Conference abstracts only"

theoretical_framework:
  name: "Self-Determination Theory"
  t_score: 0.55
  rationale: "Prioritizes motivation constructs"

current_stage:
  category: "I: Systematic Review Automation"
  agent: "I1-PaperRetrievalAgent"
  checkpoint: "SCH_DATABASE_SELECTION"
  status: "approved"

progress:
  papers_retrieved: 247
  papers_screened: 0
  papers_included: 0
  data_extracted: 0
```

### Decision Log Schema

```yaml
# .research/decision-log.yaml

decisions:
  - id: "dec-001"
    timestamp: "2026-01-15T10:30:00Z"
    checkpoint: "CP_PARADIGM_SELECTION"
    decision: "quantitative"
    alternatives: ["qualitative", "mixed-methods"]
    rationale: "Need effect size aggregation for meta-analysis"
    agent: "A5-ParadigmWorldviewAdvisor"

  - id: "dec-002"
    timestamp: "2026-01-20T14:00:00Z"
    checkpoint: "CP_THEORY_SELECTION"
    decision: "Self-Determination Theory"
    alternatives: ["Social Cognitive Theory", "Activity Theory"]
    t_score: 0.55
    rationale: "Motivation constructs align with research focus"
    agent: "A2-TheoreticalFrameworkArchitect"

  - id: "dec-003"
    timestamp: "2026-02-01T14:30:00Z"
    checkpoint: "SCH_DATABASE_SELECTION"
    decision: ["semantic_scholar", "openalex", "arxiv"]
    alternatives: ["pubmed", "eric", "web_of_science"]
    rationale: "API access + automated PDF retrieval"
    agent: "I1-PaperRetrievalAgent"
```

### Session Memory Schema

```json
// ~/.diverga/memory/sessions/session-2026-02-01-143000.json

{
  "session_id": "session-2026-02-01-143000",
  "project_id": "AI-Education-Meta-2025",
  "started": "2026-02-01T14:30:00Z",
  "ended": "2026-02-01T15:15:00Z",
  "duration_minutes": 45,

  "agents_invoked": [
    {
      "agent": "I1-PaperRetrievalAgent",
      "model": "sonnet",
      "task": "Database selection validation",
      "duration_seconds": 120,
      "success": true
    }
  ],

  "checkpoints_reached": [
    {
      "checkpoint": "SCH_DATABASE_SELECTION",
      "status": "approved",
      "timestamp": "2026-02-01T14:45:00Z"
    }
  ],

  "summary": {
    "text": "Completed database selection for systematic review. Approved Semantic Scholar, OpenAlex, and arXiv. Next: Begin paper retrieval.",
    "embedding": [0.123, -0.456, ...]  // Vector embedding for search
  },

  "next_steps": [
    "Run I1-PaperRetrievalAgent to fetch papers",
    "Review retrieved papers count",
    "Proceed to I2-ScreeningAssistant"
  ]
}
```

---

## Cross-Platform Compatibility

The DIVERGA Memory System is designed to work across multiple AI coding platforms:

### Supported Platforms

| Platform | Status | Notes |
|----------|--------|-------|
| **Claude Code** | ✅ Full Support | Native integration via Skills API |
| **Codex** | ✅ Full Support | Skills loaded from `.codex/skills/` |
| **Cursor** | 🟠 Partial Support | Manual memory file reading |
| **GitHub Copilot** | 🟡 Limited Support | Read-only access to memory files |
| **Cody** | 🟠 Partial Support | Context persistence via workspace |

### Platform-Specific Notes

**Claude Code**:
- Memory system auto-activates via `research-coordinator` skill
- Lifecycle hooks fully functional
- CLI commands work natively

**Codex**:
- Skills loaded from `.codex/skills/memory/`
- Requires `codex-skills` package installed
- Lifecycle hooks via Codex API

**Cursor**:
- Manual memory loading: Include `.research/project-state.yaml` in context
- No auto-lifecycle hooks (manual triggers only)
- Export commands work via shell

**GitHub Copilot**:
- Read-only memory access
- No auto-behavior (treat as reference documentation)
- Manual context inclusion in prompts

**Cody**:
- Context persistence via Sourcegraph workspace
- Memory files indexed automatically
- Limited lifecycle hook support

### Cross-Platform Best Practices

1. **File-Based Storage**: Use YAML/JSON files (not platform-specific databases)
2. **Standard Paths**: Keep memory in `.research/` and `~/.diverga/`
3. **Manual Fallback**: Provide CLI export commands for platforms without auto-hooks
4. **Documentation**: Include memory schemas in `CLAUDE.md` for universal access

---

## Usage Examples

### Example 1: Starting New Project

```bash
User: "I want to start a meta-analysis on AI chatbots in language learning"

# System auto-detects new project → Creates memory structure
Memory System: [Creating project context...]
  → Project ID: AI-Chatbots-Language-2026
  → Research question stored
  → Paradigm detection: quantitative (meta-analysis keyword)
  → Checkpoint: 🔴 CP_PARADIGM_SELECTION pending

# User confirms paradigm
User: "Yes, quantitative meta-analysis"

Memory System: [Saving decision...]
  → Decision logged: dec-001 (paradigm = quantitative)
  → Project state updated
  → Next: Theory selection (A2 agent)
```

### Example 2: Resuming Session

```bash
User: "Continue where we left off"

# System auto-loads context
Memory System: [Loading project context...]
  → Project: AI-Chatbots-Language-2026
  → Research Question: "How effective are AI chatbots for L2 speaking?"
  → Last session: 2026-01-28 (3 days ago)
  → Last checkpoint: SCH_DATABASE_SELECTION (approved)
  → Next: Paper retrieval (I1 agent)

Claude Code: "Welcome back! Resuming your meta-analysis on AI chatbots
for second language speaking skills. You last approved database
selection (Semantic Scholar + OpenAlex + arXiv). Ready to begin
paper retrieval with I1-PaperRetrievalAgent?"
```

### Example 3: Semantic Search

```bash
User: "/diverga:memory search heterogeneity meta-analysis"

# System searches across all memory types
Memory System: [Searching memories...]
  → Found 3 results (similarity > 0.7)

Results:
1. [Decision Log] dec-015 (2026-01-25)
   "Selected random-effects model due to expected heterogeneity"
   Similarity: 0.89

2. [Session Summary] session-2026-01-22
   "Discussed Q-statistic and I² for heterogeneity assessment"
   Similarity: 0.82

3. [Research Note] note-007
   "Literature shows high heterogeneity in chatbot effect sizes"
   Similarity: 0.76
```

### Example 4: Exporting Memories

```bash
User: "/diverga:memory export --format md"

# System generates markdown report
Memory System: [Generating export...]
  → Format: Markdown
  → Project: AI-Chatbots-Language-2026
  → Output: ~/Downloads/diverga-memory-export-2026-02-01.md

Export includes:
- Project context (research question, paradigm, methodology)
- Decision log (15 decisions with rationales)
- Session summaries (8 sessions)
- Research notes (23 notes)
- Checkpoint history (12 checkpoints)

File saved: ~/Downloads/diverga-memory-export-2026-02-01.md
```

---

## Privacy & Security

### Data Storage

- **Local-First**: All memory stored locally by default (`~/.diverga/memory/`)
- **No Cloud Sync**: Unless explicitly enabled in config
- **Encryption**: Optional encryption for sensitive projects

### Redaction Features

```yaml
# .research/memory-config.yaml

privacy:
  anonymize_on_export: true  # Replace user names with [USER]
  redact_api_keys: true      # Remove API keys from logs
  include_user_inputs: false # Exclude verbatim user messages

  # Custom redaction patterns
  redaction_patterns:
    - pattern: '\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b'  # Emails
      replacement: '[EMAIL]'
    - pattern: '\b\d{3}-\d{2}-\d{4}\b'  # SSN
      replacement: '[REDACTED]'
```

### GDPR Compliance

- **Right to Access**: `/diverga:memory export` provides full data dump
- **Right to Deletion**: `/diverga:memory clear session --all` deletes all memories
- **Right to Portability**: JSON/YAML export formats for data transfer
- **Consent**: Memory system requires explicit activation (not enabled by default)

---

## Troubleshooting

### Memory Not Loading

```bash
# Check memory status
/diverga:memory status

# Verify project context file exists
ls -la .research/project-state.yaml

# Re-initialize if corrupted
/diverga:memory repair --project AI-Chatbots-Language-2026
```

### Search Returns No Results

```bash
# Check embedding model configuration
/diverga:memory stats

# Lower similarity threshold
/diverga:memory search "query" --threshold 0.5

# Rebuild search index
/diverga:memory reindex
```

### Large Memory Footprint

```bash
# Show memory size
/diverga:memory stats --verbose

# Archive old sessions
/diverga:memory archive --before 2026-01-01

# Clean expired sessions
/diverga:memory cleanup
```

---

## Version History

- **v1.0.0** (2026-02-01): Initial release with semantic search, lifecycle hooks, cross-platform support

---

## Related Skills

- `/diverga:setup` - Configure DIVERGA Memory System
- `/diverga:a1` - Research Question Refiner (uses memory for context)
- `/diverga:i0` - Scholar Agent Orchestrator (systematic review memory)

---

## License

MIT License - See LICENSE file in repository

---

## Support

- **GitHub Issues**: https://github.com/HosungYou/Diverga/issues
- **Documentation**: https://github.com/HosungYou/Diverga/wiki/Memory-System
- **Discord**: https://discord.gg/diverga (Community support)
