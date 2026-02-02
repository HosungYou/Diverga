# Diverga Memory System

Context persistence for research workflows with 3-layer token-efficient retrieval.

## Installation

```bash
pip install sentence-transformers  # Optional: for semantic search
pip install scikit-learn           # Fallback: for TF-IDF search
```

## Quick Start

```python
from memory_api import DivergeMemory, MemoryType, Priority

# Initialize (auto-detects project)
memory = DivergeMemory()

# Store memory
memory_id = memory.store(
    content="Used regression analysis for hypothesis testing",
    memory_type=MemoryType.DECISION,
    namespace="analysis.statistical",
    priority=Priority.HIGH,
    tags=["regression", "hypothesis"]
)

# Search (3-layer retrieval)
results = memory.search("regression", limit=5)  # Layer 1: Compact
context = memory.get_context(results[0].id)     # Layer 2: Context
full = memory.retrieve([memory_id])              # Layer 3: Full details
```

## Architecture

### Components

| Module | Purpose |
|--------|---------|
| `memory_api.py` | Main API interface |
| `schema.py` | Data structures and enums |
| `database.py` | SQLite storage backend |
| `embeddings.py` | Semantic search with multiple providers |

### Storage Paths

- **Project-scoped**: `.diverga/memory/` (auto-detected)
- **Global**: `~/.diverga/memory/` (fallback)

Project detection looks for:
- `.diverga/` directory
- `.research/` directory  
- `.git/` directory

### Database Schema

**memories table**:
- Full-text search (FTS5)
- Hierarchical namespaces
- Session tracking
- Soft deletion
- Priority levels (1-10)

**sessions table**:
- Session summaries
- Agent usage tracking
- Project associations

## API Reference

### DivergeMemory Class

#### Write Operations

```python
# Store memory
memory_id = memory.store(
    content: str,
    memory_type: MemoryType = MemoryType.LEARNING,
    namespace: str = "general",
    priority: Priority = Priority.MEDIUM,
    title: Optional[str] = None,
    tags: Optional[List[str]] = None,
    agent_id: Optional[str] = None,
    session_id: Optional[str] = None,
    project_name: Optional[str] = None
) -> str

# Record decision
decision_id = memory.record_decision(
    stage: str,
    agent_id: str,
    decision_type: DecisionType,
    description: str,
    before_state: Optional[str] = None,
    after_state: Optional[str] = None,
    rationale: str = "",
    t_score: Optional[float] = None
) -> str

# Save session
session_id = memory.save_session(
    session_id: str,
    summary: str,
    agents_used: List[str],
    decisions: Optional[List[str]] = None
) -> str
```

#### Read Operations (3-Layer Retrieval)

```python
# Layer 1: Compact search results (token-efficient)
results: List[MemoryIndex] = memory.search(
    query: str,
    scope: SearchScope = SearchScope.BOTH,
    memory_types: Optional[List[MemoryType]] = None,
    limit: int = 10
)

# Layer 2: Surrounding context
context: MemoryContext = memory.get_context(memory_id: str)

# Layer 3: Full details
full_memories: List[Memory] = memory.retrieve(memory_ids: List[str])
```

#### Convenience Methods

```python
# Project context summary
proj_context = memory.get_project_context(project_name: Optional[str] = None)

# Recent decisions
decisions = memory.get_recent_decisions(project_name: Optional[str] = None, limit: int = 10)

# Session history
sessions = memory.get_session_history(limit: int = 10)
```

### Enums

```python
class MemoryType(str, Enum):
    LEARNING = "learning"
    DECISION = "decision"
    ISSUE = "issue"
    PROBLEM = "problem"
    PATTERN = "pattern"
    SOLUTION = "solution"
    CONTEXT = "context"

class DecisionType(str, Enum):
    ARCHITECTURE = "architecture"
    DESIGN = "design"
    IMPLEMENTATION = "implementation"
    REFACTORING = "refactoring"
    DEBUGGING = "debugging"
    OPTIMIZATION = "optimization"

class Priority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class SearchScope(str, Enum):
    PROJECT = "project"  # Current project only
    GLOBAL = "global"    # All projects
    BOTH = "both"        # Project + global
```

### Data Structures

```python
@dataclass
class MemoryIndex:
    """Layer 1: Compact reference (token-efficient)"""
    id: str
    title: Optional[str]
    memory_type: MemoryType
    priority: Priority
    tags: List[str]
    created_at: datetime
    similarity_score: Optional[float] = None
    preview: Optional[str] = None

@dataclass
class MemoryContext:
    """Layer 2: Surrounding context"""
    memory: Memory
    related_memories: List[MemoryIndex]
    session_context: Optional[str] = None
    project_context: Optional[str] = None

@dataclass
class Memory:
    """Layer 3: Complete details"""
    id: str
    content: str
    memory_type: MemoryType
    namespace: str
    priority: Priority
    title: Optional[str]
    tags: List[str]
    agent_id: Optional[str]
    session_id: Optional[str]
    project_name: Optional[str]
    created_at: datetime
    updated_at: datetime
    metadata: Dict[str, Any]
    embedding: Optional[List[float]]
```

## Embedding Providers

The system supports multiple embedding providers with automatic fallback:

1. **LocalEmbeddings** (sentence-transformers) - Best quality, offline
2. **OpenAIEmbeddings** (API) - Good quality, requires API key
3. **TFIDFEmbeddings** (scikit-learn) - Basic similarity, always works

Provider auto-detection tries in this order.

### Recommended Models

| Use Case | Model | Size | Speed | Dimensions |
|----------|-------|------|-------|------------|
| Fast | all-MiniLM-L6-v2 | ~80MB | Fast | 384 |
| Balanced | all-mpnet-base-v2 | ~420MB | Medium | 768 |
| Best | all-distilroberta-v1 | ~290MB | Medium | 768 |

## Testing

```bash
# Run tests
python test_api.py

# Expected output:
# ✅ All tests passed!
```

## Integration with Diverga

This memory system is designed for Diverga agents to maintain research context:

```python
# In agent code
from memory import DivergeMemory, MemoryType, Priority

memory = DivergeMemory()

# Record research decision
memory.record_decision(
    stage="design",
    agent_id="diverga:c1",
    decision_type=DecisionType.DESIGN,
    description="Chose mixed methods sequential explanatory design",
    rationale="Quantitative results need qualitative depth",
    t_score=0.42  # Innovative choice (VS methodology)
)

# Later: Retrieve project context
context = memory.get_project_context()
print(f"Project has {context['total_memories']} memories")
print(f"Recent decisions: {len(context['recent_decisions'])}")
```

## Token Efficiency

The 3-layer retrieval design minimizes token usage:

| Layer | Data Size | Tokens (approx) | Use When |
|-------|-----------|-----------------|----------|
| Layer 1 (Index) | ~100 chars | 25 | Browsing results |
| Layer 2 (Context) | ~500 chars | 125 | Need surrounding context |
| Layer 3 (Full) | Full content | Varies | Need complete details |

Example: Search 10 results → ~250 tokens vs. retrieving full memories → ~2500+ tokens

## CLI Usage

The memory system includes a command-line interface for interactive usage:

```bash
# Install dependencies
pip install -r requirements.txt

# Search memories
python src/cli.py search "meta-analysis"
python src/cli.py search "regression" --scope global --limit 10

# Show status
python src/cli.py status

# Show project context
python src/cli.py context
python src/cli.py context --project "AI-Education-Meta-2025"

# View session history
python src/cli.py history
python src/cli.py history --limit 20
python src/cli.py history --from 2026-01-01 --to 2026-01-31

# Export memories
python src/cli.py export --format md
python src/cli.py export --format json --output ~/memories.json
python src/cli.py export --format yaml --scope global

# Show statistics
python src/cli.py stats

# Setup wizard
python src/cli.py setup
```

### CLI Features

- Emoji indicators for visual clarity
- ANSI color output (auto-disabled for non-TTY)
- Formatted tables with alignment
- Human-readable timestamps
- Similarity scores with color coding
- Export to multiple formats (Markdown, JSON, YAML)

### SKILL.md Integration

The CLI commands are designed to be called from SKILL.md patterns:

```yaml
# In SKILL.md
- pattern: "/diverga:memory search (.+)"
  behavior: |
    from cli import cmd_search
    result = cmd_search(match.group(1))
    output(result)
```

Each command returns a formatted string ready for display to users.

## Troubleshooting

### "Unknown skill: diverga:memory" Error

**Problem**: Claude Code shows `Unknown skill: diverga:memory` when invoking the skill.

**Cause**: The `SKILL.md` frontmatter format is incompatible with Claude Code's skill parser.

**Incorrect Format** (causes the error):
```yaml
---
name: memory
command: /diverga:memory           # ❌ This field breaks parsing
version: 1.0.0
description: Some description
category: system                   # ❌ Extra fields not supported
model_tier: medium                 # ❌
triggers:                          # ❌
  - "remember"
  - "memory"
dependencies:                      # ❌
  required:
    - tabulate>=0.9.0
---
```

**Correct Format**:
```yaml
---
name: memory
description: |
  DIVERGA Memory System - Persistent context preservation.
  Triggers: remember, memory, context, recall
version: "1.0.0"
---
```

**Key Rules for SKILL.md Frontmatter**:
1. Only use `name`, `description`, and `version` fields
2. Put triggers and other metadata in the `description` field as text
3. Use quoted version numbers (e.g., `"1.0.0"` not `1.0.0`)
4. Do NOT include `command`, `category`, `model_tier`, `triggers`, `dependencies`, or other extra fields

**Solution**:
```bash
# 1. Edit the source SKILL.md
nano "/Volumes/External SSD/Projects/Diverga/.claude/skills/memory/SKILL.md"

# 2. Simplify the frontmatter to only name, description, version

# 3. Copy to plugin directory
cp "/Volumes/External SSD/Projects/Diverga/.claude/skills/memory/SKILL.md" \
   ~/.claude/plugins/diverga/.claude/skills/memory/SKILL.md

# 4. Restart Claude Code
/exit
```

### Skill Changes Not Reflected

**Problem**: After editing `SKILL.md`, Claude Code still uses the old version.

**Solution**:
1. Copy the updated file to `~/.claude/plugins/diverga/.claude/skills/memory/SKILL.md`
2. Restart Claude Code with `/exit` and start a new session

### Plugin Not Installed

**Problem**: Diverga skills not available at all.

**Solution**:
```bash
# Re-install from source
rm -rf ~/.claude/plugins/diverga/
cp -r "/Volumes/External SSD/Projects/Diverga" ~/.claude/plugins/diverga

# Or via marketplace
/plugin marketplace add https://github.com/HosungYou/Diverga
/plugin install diverga
```

## Version

1.0.0 - Initial release with 3-layer retrieval, semantic search, project detection, and CLI
