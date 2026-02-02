# Diverga Memory Lifecycle Hooks

Automatic context persistence and checkpoint tracking for Claude Code and Codex integration.

## Overview

The Lifecycle Hooks system provides three core hooks that seamlessly integrate research context into agent workflows:

1. **on_session_start**: Auto-load project context and relevant memories
2. **on_checkpoint_reached**: Save decisions and update project state
3. **on_session_end**: Generate summary and consolidate memories

## Quick Start

```python
from diverga.memory import MemoryHooks

# Initialize hooks
hooks = MemoryHooks()

# Session start
context = hooks.on_session_start(
    project_path="/path/to/project",
    session_id="session-123"
)
print(context.to_prompt())  # Inject into agent prompt

# Checkpoint reached
hooks.on_checkpoint_reached(
    checkpoint_id="CP_PARADIGM_SELECTION",
    stage="foundation",
    agent_id="diverga:a5",
    decision_data={
        "decision": "Selected qualitative paradigm",
        "rationale": "Focus on lived experiences"
    }
)

# Session end
hooks.on_session_end(
    session_id="session-123",
    agents_used=["diverga:a1", "diverga:a5"],
    decisions_made=["CP_PARADIGM_SELECTION"]
)
```

## Hook 1: on_session_start

**Purpose**: Load project context from memory and inject into agent prompts.

**When**: At the beginning of every agent session or when a new agent is invoked.

**What it does**:
1. Detects project from path or auto-detects from cwd
2. Loads research question, current stage, and project metadata
3. Retrieves last 5 decisions made
4. Finds relevant patterns and learnings (high-priority memories)
5. Lists active sessions
6. Returns `ContextInjection` object with formatted markdown

**Output**: `ContextInjection` object with `.to_prompt()` method.

### Example Output

```markdown
## Research Context (Auto-Loaded from Memory)

**Project**: AI-Assisted-Learning-Meta-Analysis
**Research Question**: How do AI chatbots improve language learning outcomes?
**Current Stage**: foundation

### Recent Decisions
- Selected qualitative paradigm (2024-02-01T10:30:00) - Focus on lived experiences
- Theoretical framework: Sociocultural theory (2024-02-01T09:15:00)
- Research question refined (2024-02-01T08:45:00)

### Relevant Context
**Pattern - Effective RQ structure**: Research questions in education should specify population, intervention, comparison, outcome (PICO framework)
**Learning - Paradigm alignment**: Qualitative paradigms require phenomenological or constructivist theoretical frameworks
**Pattern - Sample size**: Qualitative studies typically need 15-30 participants for saturation

---
Use this context. Do not re-ask for established information.
```

### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `project_path` | str | No | Path to project (auto-detects if None) |
| `session_id` | str | No | Session identifier (generates UUID if None) |
| `context_filters` | dict | No | Filters for memory retrieval |

### Usage in Agent Prompts

```python
# Claude Code agent invocation
context = hooks.on_session_start(project_path="/path/to/project")

agent_prompt = f"""
{context.to_prompt()}

[Your agent task here...]
"""

# Pass to agent
Task(
    subagent_type="diverga:a1",
    model="opus",
    prompt=agent_prompt
)
```

## Hook 2: on_checkpoint_reached

**Purpose**: Save decisions to memory, update project state, and log checkpoint.

**When**: When an agent reaches a human checkpoint (e.g., CP_PARADIGM_SELECTION).

**What it does**:
1. Extracts decision details from `decision_data` dictionary
2. Saves decision as memory with checkpoint metadata
3. Updates `.research/project-state.yaml` file
4. Logs checkpoint to active session tracker
5. Infers decision type from checkpoint ID

**Side Effects**:
- Creates new memory in database
- Updates project state file
- Logs to session tracker

### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `checkpoint_id` | str | Yes | Checkpoint identifier (e.g., "CP_PARADIGM_SELECTION") |
| `stage` | str | Yes | Research stage ("foundation", "design", "analysis", etc.) |
| `agent_id` | str | Yes | Agent that triggered checkpoint (e.g., "diverga:a5") |
| `decision_data` | dict | Yes | Decision details (see below) |
| `session_id` | str | No | Session identifier (uses latest if None) |
| `t_score` | float | No | VS methodology typicality score (0.0-1.0) |

### decision_data Structure

```python
{
    "decision": "Selected qualitative paradigm",  # Short description
    "rationale": "Focus on lived experiences and contextual meaning",
    "before_state": "Undecided between quantitative and qualitative",
    "after_state": "Qualitative paradigm confirmed",
    "options_considered": [
        "Quantitative (T=0.8) - Rejected due to emphasis on measurement",
        "Qualitative (T=0.5) - SELECTED",
        "Mixed methods (T=0.3) - Too complex for initial study"
    ],
    "metadata": {
        "user_rationale": "...",
        "alternatives_rejected": [...]
    }
}
```

### Example

```python
hooks.on_checkpoint_reached(
    checkpoint_id="CP_PARADIGM_SELECTION",
    stage="foundation",
    agent_id="diverga:a5",
    decision_data={
        "decision": "Selected qualitative paradigm",
        "rationale": "Focus on lived experiences and contextual meaning",
        "before_state": "Undecided between quantitative and qualitative",
        "after_state": "Qualitative paradigm confirmed",
        "options_considered": [
            "Quantitative (T=0.8)",
            "Qualitative (T=0.5) - SELECTED",
            "Mixed methods (T=0.3)"
        ]
    },
    t_score=0.5
)
```

### Project State Update

After checkpoint, `.research/project-state.yaml` is updated:

```yaml
current_stage: foundation
last_checkpoint: CP_PARADIGM_SELECTION
last_updated: 2024-02-01T10:30:00

CP_PARADIGM_SELECTION:
  decision: Selected qualitative paradigm
  rationale: Focus on lived experiences and contextual meaning
  before_state: Undecided between quantitative and qualitative
  after_state: Qualitative paradigm confirmed
  options_considered:
    - Quantitative (T=0.8)
    - Qualitative (T=0.5) - SELECTED
    - Mixed methods (T=0.3)
```

## Hook 3: on_session_end

**Purpose**: Generate session summary, save session record, and consolidate memories.

**When**: At the end of an agent session or when all tasks are complete.

**What it does**:
1. Generates AI-powered session summary (if embeddings available)
2. Saves session record with agents used and decisions made
3. Consolidates similar memories (deduplication using embeddings)
4. Cleans up active session tracker

**Side Effects**:
- Creates session record in database
- Potentially merges duplicate memories
- Removes from active session tracker

### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `session_id` | str | Yes | Session identifier |
| `agents_used` | list[str] | Yes | List of agent IDs used (e.g., ["diverga:a1", "diverga:a5"]) |
| `decisions_made` | list[str] | Yes | List of checkpoint IDs reached |
| `auto_summarize` | bool | No | Generate AI summary (default: True) |

### Example

```python
hooks.on_session_end(
    session_id="session-123",
    agents_used=["diverga:a1", "diverga:a5", "diverga:c2"],
    decisions_made=["CP_PARADIGM_SELECTION", "CP_THEORY_SELECTION"]
)
```

### Session Summary Format

```
Session session-123 | Agents: diverga:a1, diverga:a5, diverga:c2 | Decisions: 2 | Key checkpoints: CP_PARADIGM_SELECTION, CP_THEORY_SELECTION | Memories created: 8
```

## Checkpoint Registry

The system recognizes these checkpoints:

### Foundation Stage

| Checkpoint ID | Level | Agents | Decision Type |
|---------------|-------|--------|---------------|
| `CP_RESEARCH_DIRECTION` | Required | diverga:a1 | architecture |
| `CP_PARADIGM_SELECTION` | Required | diverga:a5 | architecture |
| `CP_THEORY_SELECTION` | Required | diverga:a2 | architecture |

### Design Stage

| Checkpoint ID | Level | Agents | Decision Type |
|---------------|-------|--------|---------------|
| `CP_METHODOLOGY_APPROVAL` | Required | diverga:c1, c2, c3 | design |
| `CP_SAMPLING_STRATEGY` | Recommended | diverga:d1 | design |

### Analysis Stage

| Checkpoint ID | Level | Agents | Decision Type |
|---------------|-------|--------|---------------|
| `CP_ANALYSIS_PLAN` | Required | diverga:e1, e2, e3 | implementation |

### Quality Stage

| Checkpoint ID | Level | Agents | Decision Type |
|---------------|-------|--------|---------------|
| `CP_QUALITY_REVIEW` | Recommended | diverga:f3, f4 | debugging |

### Publication Stage

| Checkpoint ID | Level | Agents | Decision Type |
|---------------|-------|--------|---------------|
| `CP_JOURNAL_SELECTION` | Optional | diverga:g1 | design |
| `CP_HUMANIZATION_REVIEW` | Recommended | diverga:g5, g6 | refactoring |

### Systematic Review Stage

| Checkpoint ID | Level | Agents | Decision Type |
|---------------|-------|--------|---------------|
| `SCH_DATABASE_SELECTION` | Required | diverga:i1 | design |
| `SCH_SCREENING_CRITERIA` | Required | diverga:i2 | design |
| `SCH_RAG_READINESS` | Recommended | diverga:i3 | implementation |
| `SCH_QUALITY_GATES` | Optional | diverga:i0 | debugging |

## Integration with Claude Code

### Automatic Hook Invocation

Claude Code can automatically invoke hooks based on workflow events:

```python
# In Claude Code skill definition (.claude/skills/research-coordinator/SKILL.md)

## Hooks

When agent session starts:
```python
from diverga.memory import on_session_start

context = on_session_start()
# Inject context.to_prompt() into agent prompt
```

When checkpoint reached:
```python
from diverga.memory import on_checkpoint_reached

on_checkpoint_reached(
    checkpoint_id="CP_PARADIGM_SELECTION",
    stage="foundation",
    agent_id="diverga:a5",
    decision_data=decision_data
)
```

When session ends:
```python
from diverga.memory import on_session_end

on_session_end(
    session_id=session_id,
    agents_used=agents_used,
    decisions_made=decisions_made
)
```
```

### Manual Hook Invocation

Users can also manually trigger hooks:

```bash
# Python CLI
python -m diverga.memory.hooks session_start --project-path /path/to/project

python -m diverga.memory.hooks checkpoint_reached \
  --checkpoint-id CP_PARADIGM_SELECTION \
  --stage foundation \
  --agent diverga:a5 \
  --decision "Selected qualitative paradigm"

python -m diverga.memory.hooks session_end \
  --session-id session-123 \
  --agents diverga:a1,diverga:a5 \
  --decisions CP_PARADIGM_SELECTION
```

## Configuration

Hooks are configured via `hooks.yaml`:

```yaml
# Enable/disable hooks
hooks:
  - id: "session_start"
    enabled: true
  - id: "checkpoint_reached"
    enabled: true
  - id: "session_end"
    enabled: true

# Context injection settings
context_injection:
  max_recent_decisions: 5
  max_relevant_memories: 3
  memory_types:
    - "decision"
    - "pattern"
    - "learning"

# Memory consolidation
consolidation:
  enabled: true
  similarity_threshold: 0.85
```

## Advanced Usage

### Custom Context Filters

```python
context = hooks.on_session_start(
    project_path="/path/to/project",
    context_filters={
        "memory_types": ["decision", "pattern"],
        "stages": ["foundation", "design"],
        "max_age_days": 7  # Last 7 days only
    }
)
```

### Batch Checkpoint Processing

```python
# Process multiple checkpoints in sequence
checkpoints = [
    ("CP_PARADIGM_SELECTION", "foundation", "diverga:a5", {...}),
    ("CP_THEORY_SELECTION", "foundation", "diverga:a2", {...}),
    ("CP_METHODOLOGY_APPROVAL", "design", "diverga:c2", {...})
]

for checkpoint_id, stage, agent_id, decision_data in checkpoints:
    hooks.on_checkpoint_reached(
        checkpoint_id=checkpoint_id,
        stage=stage,
        agent_id=agent_id,
        decision_data=decision_data
    )
```

### Custom Session Summarization

```python
hooks.on_session_end(
    session_id="session-123",
    agents_used=["diverga:a1", "diverga:a5"],
    decisions_made=["CP_PARADIGM_SELECTION"],
    auto_summarize=False  # Skip AI summary, use simple format
)
```

## Testing

Run the demo script to test hooks:

```bash
cd /Volumes/External SSD/Projects/Diverga/.claude/skills/memory/src
python hooks.py
```

Expected output:
```
=== Diverga Memory Hooks Demo ===

1. Session Start
## Research Context (Auto-Loaded from Memory)
...

2. Checkpoint Reached
✓ Checkpoint logged and decision saved

3. Session End
✓ Session summary generated and saved

=== Demo Complete ===
```

## Error Handling

Hooks fail gracefully with informative warnings:

```python
try:
    context = hooks.on_session_start()
except Exception as e:
    print(f"Warning: Failed to load context: {e}")
    # Continue without context injection
```

## Performance Considerations

- **Session Start**: ~50-100ms (database queries)
- **Checkpoint Reached**: ~20-50ms (insert + file write)
- **Session End**: ~100-300ms (summary generation + consolidation)

For high-frequency checkpoints, consider batching:

```python
# Batch mode (future enhancement)
hooks.batch_mode = True
# ... multiple checkpoints ...
hooks.flush_batch()  # Write all at once
```

## Future Enhancements

- [ ] AI-powered session summaries using LLM
- [ ] Semantic memory consolidation using embeddings
- [ ] Real-time context updates during session
- [ ] Multi-project context synthesis
- [ ] Hook plugins for custom workflows

## See Also

- [Memory API Documentation](./README.md)
- [Schema Reference](./src/schema.py)
- [Database Schema](./src/database.py)
- [Diverga Agent System](../../AGENTS.md)
