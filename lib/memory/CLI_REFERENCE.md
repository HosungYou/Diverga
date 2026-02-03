# Diverga Memory System - CLI Reference

## Overview

The CLI module (`src/cli.py`) provides user-friendly command handlers for the Diverga Memory System. Each command returns formatted output designed for both interactive terminal use and SKILL.md integration.

## Installation

```bash
pip install -r requirements.txt
```

**Dependencies:**
- `tabulate>=0.9.0` - Table formatting (optional, has fallback)
- `pyyaml>=6.0` - YAML export support (optional)

## Commands

### 1. Search

Search memories semantically or via text.

```bash
python src/cli.py search "meta-analysis"
python src/cli.py search "regression" --scope global --limit 10
python src/cli.py search "chatbot" --type decision
```

**Parameters:**
- `query` (required) - Search query string
- `--scope` - Search scope: `project` (default), `global`, `both`
- `--limit` - Maximum results (default: 5)
- `--type` - Filter by memory type: `decision`, `pattern`, `learning`, etc.

**Output:**
- Table with ID, type, title, priority, and similarity scores
- Color-coded match percentages (green = high, yellow = medium, dim = low)
- Helpful tips if no results found

**Python API:**
```python
from cli import cmd_search
result = cmd_search(query="meta-analysis", scope="project", limit=5)
print(result)
```

---

### 2. Status

Show current memory system status.

```bash
python src/cli.py status
```

**Parameters:** None

**Output:**
- Storage location and scope (project/global)
- Database size
- Memory count by type (with emoji)
- Recent sessions
- Embedding provider status
- Top namespaces

**Python API:**
```python
from cli import cmd_status
result = cmd_status()
print(result)
```

---

### 3. Context

Show current project context.

```bash
python src/cli.py context
python src/cli.py context --project "AI-Education-Meta-2025"
```

**Parameters:**
- `--project` - Project name (optional, uses current if omitted)

**Output:**
- Project summary (name, total memories, last updated)
- Recent decisions (up to 5)
- Key patterns (high priority learnings)
- Active sessions

**Python API:**
```python
from cli import cmd_context
result = cmd_context(project="AI-Education-Meta-2025")
print(result)
```

---

### 4. History

Show recent session history.

```bash
python src/cli.py history
python src/cli.py history --limit 20
python src/cli.py history --from 2026-01-01 --to 2026-01-31
```

**Parameters:**
- `--limit` - Maximum sessions to show (default: 10)
- `--from` - Start date filter (YYYY-MM-DD)
- `--to` - End date filter (YYYY-MM-DD)

**Output:**
- Session ID, start time, duration
- Project association
- Summary text
- Agents used

**Python API:**
```python
from cli import cmd_history
result = cmd_history(limit=20, from_date="2026-01-01", to_date="2026-01-31")
print(result)
```

---

### 5. Export

Export memories to file.

```bash
python src/cli.py export --format md
python src/cli.py export --format json --output ~/memories.json
python src/cli.py export --format yaml --scope global
```

**Parameters:**
- `--format` - Output format: `md` (default), `json`, `yaml`
- `--scope` - Export scope: `project` (default), `global`, `both`
- `--output` - Output file path (auto-generated if omitted)

**Output:**
- Success message with file details
- File size and location
- Total memories exported

**Formats:**
- **Markdown**: Grouped by type, readable
- **JSON**: Structured data with metadata
- **YAML**: Hierarchical format (requires PyYAML)

**Python API:**
```python
from cli import cmd_export
result = cmd_export(format="json", scope="project", output="~/export.json")
print(result)
```

---

### 6. Stats

Show detailed statistics.

```bash
python src/cli.py stats
```

**Parameters:** None

**Output:**
- Overview (total memories, sessions)
- Memory types distribution (table with percentages and bars)
- Top namespaces (frequency table)
- Storage information (size, location)

**Python API:**
```python
from cli import cmd_stats
result = cmd_stats()
print(result)
```

---

### 7. Setup

Interactive setup wizard.

```bash
python src/cli.py setup
```

**Parameters:** None

**Output:**
- Configuration paths
- Embedding provider setup instructions
- Verification steps

**Python API:**
```python
from cli import cmd_setup
result = cmd_setup()
print(result)
```

---

## Output Formatting

### Visual Elements

| Element | Purpose | Example |
|---------|---------|---------|
| Emoji | Visual category indicators | 🔍 (search), 📊 (status), 🎯 (decision) |
| ANSI Colors | Highlighting and emphasis | Red (errors), Green (success), Cyan (headers) |
| Tables | Structured data | Search results, statistics |
| Timestamps | Human-readable time | "just now", "5m ago", "3d ago" |

### Color Coding

- **Green** - Success, high similarity, recent
- **Yellow** - Warning, medium priority/similarity
- **Red** - Error, critical priority
- **Cyan** - Headers, informational
- **Dim** - Secondary information, metadata

### Emoji Reference

| Emoji | Meaning |
|-------|---------|
| 🔍 | Search |
| 📊 | Status |
| 📋 | Context |
| 📜 | History |
| 💾 | Export |
| 📈 | Statistics |
| ✅ | Success |
| ⚠️  | Warning |
| ❌ | Error |
| ℹ️  | Information |
| 🧠 | Memory |
| 🎯 | Decision |
| 🔄 | Pattern |
| 📚 | Learning |
| 🔗 | Session |
| 📁 | Project |
| ⏰ | Time |

## Integration with SKILL.md

The CLI is designed to be called from SKILL.md patterns. Each function returns a formatted string ready for display.

### Example Integration

```yaml
# In SKILL.md patterns section
patterns:
  - pattern: "/diverga:memory search (.+)"
    behavior: |
      from memory.src.cli import cmd_search
      query = match.group(1)
      result = cmd_search(query)
      output(result)

  - pattern: "/diverga:memory status"
    behavior: |
      from memory.src.cli import cmd_status
      result = cmd_status()
      output(result)

  - pattern: "/diverga:memory context"
    behavior: |
      from memory.src.cli import cmd_context
      result = cmd_context()
      output(result)
```

### Error Handling

All commands use try-except blocks and return user-friendly error messages:

```python
try:
    # Command logic
    return formatted_result
except Exception as e:
    return f"❌ Command failed: {str(e)}\n"
```

## Testing

Run the test suite to verify all commands work:

```bash
python test_cli.py
```

Expected output:
```
✅ Passed: 6
❌ Failed: 0
Total: 6

🎉 All tests passed!
```

## Standalone Usage

The CLI can be used standalone from the terminal:

```bash
# Make executable
chmod +x src/cli.py

# Run directly
python src/cli.py search "query"
python src/cli.py status
```

### Help Text

```bash
python src/cli.py --help
python src/cli.py search --help
python src/cli.py export --help
```

## Fallback Behavior

### No Tabulate

If `tabulate` is not installed, the CLI uses a simple fallback implementation:

```
# | ID | Type | Priority
--------------------------------
1 | mem-123 | decision | high
2 | mem-456 | pattern | medium
```

### No PyYAML

YAML export requires PyYAML. If not installed:

```
❌ YAML export requires PyYAML: pip install pyyaml
```

### No Embeddings

If no embedding provider is available, search falls back to text-based FTS:

```
⚠️ Embeddings disabled
Falling back to text-based search only.
```

## Performance

| Command | Speed | Database Queries |
|---------|-------|------------------|
| `search` | Fast | 1-2 (FTS + filter) |
| `status` | Fast | 3-4 (stats + sessions) |
| `context` | Medium | 5-6 (context + related) |
| `history` | Fast | 1 (sessions) |
| `export` | Slow | 1-2 (all memories) |
| `stats` | Fast | 3-4 (aggregations) |
| `setup` | Instant | 0 (display only) |

## API Stability

The CLI functions are designed to be stable interfaces:

- Function signatures won't change in minor versions
- Output format may be enhanced but structure preserved
- New optional parameters may be added
- Backwards compatibility maintained

## Version

1.0.0 - Initial release

## License

MIT License - Part of Diverga Memory System
