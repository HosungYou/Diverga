# Diverga Memory System - CLI Usage Guide

The Diverga Memory System CLI allows you to interact with memory storage directly from the command line, without requiring Claude Code or Codex.

## Installation

The CLI is part of the memory module. Install it with:

```bash
pip install -r requirements.txt
```

## Running as a Module

Use Python's `-m` flag to run the CLI:

```bash
python -m diverga.memory <command> [options]
# or
python3 -m diverga.memory <command> [options]
```

Or, if you're in the memory directory:

```bash
python -m src <command> [options]
```

## Global Options

- `--help, -h`: Show help for any command
- `--version`: Display CLI version
- `--verbose, -v`: Enable verbose output for debugging
- `--no-color`: Disable colored terminal output

## Commands

### Search: Find memories semantically

Search across your knowledge base using natural language queries.

**Usage:**
```bash
python -m src search <query> [--scope {project|global|both}] [--limit N] [--type TYPE]
```

**Arguments:**
- `query` (required): Your search query
- `--scope`: Search scope - "project" (current project), "global" (all), or "both" (default: project)
- `--limit, -l`: Maximum results to return (default: 5)
- `--type, -t`: Filter by memory type - "decision", "pattern", "learning", or "context"

**Examples:**
```bash
# Search project memories for "meta-analysis"
python -m src search "meta-analysis"

# Search globally for regression-related content, up to 10 results
python -m src search "regression" --scope global --limit 10

# Search for decisions about learning outcomes
python -m src search "learning outcomes" --type decision

# Use short alias
python -m src s "effect size" --limit 3
```

### Status: Show memory system status

Display current memory system statistics, database location, embedding provider status, and recent sessions.

**Usage:**
```bash
python -m src status
```

**Examples:**
```bash
# Check memory system health
python -m src status

# Check with alias
python -m src st
```

### Context: Show project context

Display current project context including recent decisions, key patterns, and active sessions.

**Usage:**
```bash
python -m src context [--project NAME]
```

**Arguments:**
- `--project, -p`: Optional project name (uses current project if not specified)

**Examples:**
```bash
# Show context for current project
python -m src context

# Show context for a specific project
python -m src context --project "AI-Education-Meta-2025"

# Use short alias
python -m src ctx --project MyProject
```

### History: View recent sessions

Display session history with timestamps, summaries, and agents used.

**Usage:**
```bash
python -m src history [--limit N] [--from YYYY-MM-DD] [--to YYYY-MM-DD]
```

**Arguments:**
- `--limit, -l`: Number of sessions to show (default: 10)
- `--from`: Start date for filtering (YYYY-MM-DD format)
- `--to`: End date for filtering (YYYY-MM-DD format)

**Examples:**
```bash
# Show last 10 sessions
python -m src history

# Show last 20 sessions
python -m src history --limit 20

# Show sessions from January 2026
python -m src history --from 2026-01-01 --to 2026-01-31

# Use short alias
python -m src h --limit 15
```

### Export: Export memories to file

Export all memories to a file in your preferred format.

**Usage:**
```bash
python -m src export [--format {md|json|yaml}] [--scope {project|global|both}] [--output PATH]
```

**Arguments:**
- `--format, -f`: Output format - "md" (markdown), "json", or "yaml" (default: md)
- `--scope`: Export scope - "project" (current), "global" (all), or "both" (default: project)
- `--output, -o`: Output file path (auto-generated in ~/Downloads if not specified)

**Examples:**
```bash
# Export current project as markdown
python -m src export

# Export as JSON to custom location
python -m src export --format json --output /path/to/memories.json

# Export all memories as YAML
python -m src export --format yaml --scope global

# Use short alias
python -m src e --format json --output ~/my_memories.json
```

### Setup: Interactive setup wizard

Run the setup wizard to configure the memory system.

**Usage:**
```bash
python -m src setup
```

**Examples:**
```bash
# Run setup wizard
python -m src setup

# Use short alias
python -m src init
```

### Stats: Show detailed statistics

Display detailed statistics about memory usage, breakdown by type, and namespace information.

**Usage:**
```bash
python -m src stats
```

**Examples:**
```bash
# Show statistics
python -m src stats

# Use short alias
python -m src stat
```

## Environment Variables

- `OPENAI_API_KEY`: OpenAI API key for semantic embeddings (optional but recommended)
- `DIVERGA_MEMORY_PATH`: Custom path for memory storage (optional)

**Example:**
```bash
export OPENAI_API_KEY="sk-..."
python -m src search "advanced topic" --scope global
```

## Command Aliases

Most commands have short aliases for convenience:

| Command | Alias |
|---------|-------|
| search | s |
| status | st |
| context | ctx |
| history | h |
| export | e |
| setup | init |
| stats | stat |

**Example:**
```bash
# These are equivalent:
python -m src search "test"
python -m src s "test"
```

## Memory Storage Locations

- **Project-scoped memories**: `.diverga/memory/` (in your project root)
- **Global memories**: `~/.diverga/memory/` (in your home directory)

## Scope Explained

When using `--scope` with search or export commands:

- **project** (default): Only memories for the current project
- **global**: All memories across all projects
- **both**: Project + global memories (global takes precedence for duplicates)

## Examples: Common Workflows

### Backup all memories before starting a new project
```bash
python -m src export --format json --scope global --output ~/backups/diverga_backup_$(date +%Y%m%d).json
```

### Search for decision patterns across all projects
```bash
python -m src search "methodology" --scope global --limit 20 --type decision
```

### Review session history from last month
```bash
python -m src history --limit 50 --from 2025-12-01 --to 2025-12-31
```

### Check system health after configuration changes
```bash
python -m src status
python -m src stats
```

### Export project memories for archiving
```bash
python -m src export --format md --scope project --output ./archive/project_memories.md
```

## Troubleshooting

### "No memories found" on search
- Check if you're using the right `--scope` (try `--scope both`)
- Verify memories exist with `python -m src status`
- Try a broader search query

### Embedding provider warnings
The system warns if no embedding provider is available:
- Install with: `pip install openai` and set `OPENAI_API_KEY`
- Or install: `pip install sentence-transformers`
- Text-based search still works without embeddings

### Database errors
- Ensure `.diverga/` directory exists and is writable
- Check `~/.diverga/` permissions if using global scope
- Try `python -m src status` to diagnose issues

### Color issues
Use `--no-color` if terminal colors cause display problems:
```bash
python -m src status --no-color
```

## Integration with Scripts

The CLI can be integrated into shell scripts:

```bash
#!/bin/bash

# Backup before archiving
python -m src export --format json --scope both --output ./backup.json

# Check status
python -m src status

# Search for recent decisions
python -m src search "decision" --type decision --limit 5
```

## Return Codes

The CLI returns standard exit codes:
- `0`: Success
- `1`: Error
- `130`: User interrupted (Ctrl+C)

You can check the exit code in scripts:
```bash
python -m src search "test"
if [ $? -eq 0 ]; then
    echo "Search successful"
else
    echo "Search failed"
fi
```

## Tips and Best Practices

1. **Regular backups**: Export memories weekly
   ```bash
   python -m src export --format json --scope global --output ~/backups/memory_$(date +%Y%m%d).json
   ```

2. **Use meaningful search queries**: More specific queries yield better results
   ```bash
   # Good: specific and descriptive
   python -m src search "heterogeneity in meta-analysis with random effects"

   # Less effective: too vague
   python -m src search "analysis"
   ```

3. **Organize by memory type**: Filter searches by type to narrow results
   ```bash
   # Find decisions about methodology
   python -m src search "methodology" --type decision

   # Find patterns in data analysis
   python -m src search "regression" --type pattern
   ```

4. **Track global decisions**: Use `--scope global` for cross-project insights
   ```bash
   # See how you've approached similar problems before
   python -m src search "effect size calculation" --scope global --type decision
   ```

5. **Check session history regularly**: Monitor your research workflow
   ```bash
   # See what you accomplished this week
   python -m src history --limit 20
   ```

## For More Information

- GitHub: https://github.com/HosungYou/Diverga
- Memory API Documentation: See `README.md` in memory module
- Research Coordinator: See `.claude/skills/research-coordinator/`

---

**Last Updated**: February 2026
**CLI Version**: 1.0.0
**Memory Module**: v1.0.0
