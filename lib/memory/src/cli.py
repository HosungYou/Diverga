"""
CLI command handlers for Diverga Memory System.

Provides formatted command output for SKILL.md integration.
Each command returns user-friendly formatted strings with:
- Emoji for visual clarity
- Tables for structured data
- ANSI colors (where supported)
- Clean, professional layout
"""

import os
import sys
import json
from pathlib import Path
from datetime import datetime, timedelta
from typing import Optional, List, Dict, Any

# Optional dependencies with fallbacks
try:
    from tabulate import tabulate
    HAS_TABULATE = True
except ImportError:
    HAS_TABULATE = False
    def tabulate(data, headers=None, tablefmt='simple'):
        """Fallback tabulate implementation."""
        if not data:
            return ""

        # Simple text-based table
        output = []
        if headers:
            output.append(" | ".join(str(h) for h in headers))
            output.append("-" * 60)

        for row in data:
            output.append(" | ".join(str(cell) for cell in row))

        return "\n".join(output)

try:
    import yaml
    HAS_YAML = True
except ImportError:
    HAS_YAML = False

try:
    from .memory_api import DivergeMemory
    from .schema import MemoryType, SearchScope, Priority
    from .database import MemoryDatabase
except ImportError:
    # Support direct imports when not used as package
    from memory_api import DivergeMemory
    from schema import MemoryType, SearchScope, Priority
    from database import MemoryDatabase


# ANSI Color codes
class Colors:
    """ANSI color codes for terminal output."""
    RESET = "\033[0m"
    BOLD = "\033[1m"
    DIM = "\033[2m"

    # Colors
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    MAGENTA = "\033[35m"
    CYAN = "\033[36m"
    WHITE = "\033[37m"

    # Bright colors
    BRIGHT_GREEN = "\033[92m"
    BRIGHT_YELLOW = "\033[93m"
    BRIGHT_BLUE = "\033[94m"
    BRIGHT_CYAN = "\033[96m"

    @classmethod
    def disable(cls):
        """Disable colors (for non-TTY output)."""
        for attr in dir(cls):
            if not attr.startswith('_') and attr.isupper():
                setattr(cls, attr, '')


# Disable colors if not in TTY
if not sys.stdout.isatty():
    Colors.disable()


# Emoji constants
EMOJI = {
    'search': '🔍',
    'status': '📊',
    'context': '📋',
    'history': '📜',
    'export': '💾',
    'stats': '📈',
    'success': '✅',
    'warning': '⚠️',
    'error': '❌',
    'info': 'ℹ️',
    'memory': '🧠',
    'decision': '🎯',
    'pattern': '🔄',
    'learning': '📚',
    'session': '🔗',
    'project': '📁',
    'time': '⏰',
}


def _get_memory() -> DivergeMemory:
    """Get or create default memory instance."""
    return DivergeMemory()


def _format_header(title: str, emoji: str = '') -> str:
    """Format section header with emoji."""
    if emoji:
        return f"\n{Colors.BOLD}{Colors.CYAN}{emoji} {title}{Colors.RESET}\n{'─' * 60}\n"
    return f"\n{Colors.BOLD}{Colors.CYAN}{title}{Colors.RESET}\n{'─' * 60}\n"


def _format_subheader(title: str) -> str:
    """Format subsection header."""
    return f"\n{Colors.BOLD}{title}{Colors.RESET}"


def _format_key_value(key: str, value: str, indent: int = 0) -> str:
    """Format key-value pair."""
    spacing = ' ' * indent
    return f"{spacing}{Colors.DIM}{key}:{Colors.RESET} {value}"


def _format_timestamp(dt: datetime) -> str:
    """Format datetime to human-readable string."""
    now = datetime.now()
    diff = now - dt

    if diff < timedelta(minutes=1):
        return f"{Colors.BRIGHT_GREEN}just now{Colors.RESET}"
    elif diff < timedelta(hours=1):
        minutes = int(diff.total_seconds() / 60)
        return f"{Colors.GREEN}{minutes}m ago{Colors.RESET}"
    elif diff < timedelta(days=1):
        hours = int(diff.total_seconds() / 3600)
        return f"{Colors.YELLOW}{hours}h ago{Colors.RESET}"
    elif diff < timedelta(days=7):
        days = int(diff.total_seconds() / 86400)
        return f"{Colors.CYAN}{days}d ago{Colors.RESET}"
    else:
        return f"{Colors.DIM}{dt.strftime('%Y-%m-%d')}{Colors.RESET}"


def _format_priority(priority: Priority) -> str:
    """Format priority with color."""
    colors = {
        Priority.CRITICAL: Colors.RED,
        Priority.HIGH: Colors.YELLOW,
        Priority.MEDIUM: Colors.CYAN,
        Priority.LOW: Colors.DIM,
    }
    color = colors.get(priority, Colors.RESET)
    return f"{color}{priority.value}{Colors.RESET}"


def _format_memory_type(memory_type: MemoryType) -> str:
    """Format memory type with emoji."""
    emojis = {
        MemoryType.DECISION: EMOJI['decision'],
        MemoryType.PATTERN: EMOJI['pattern'],
        MemoryType.LEARNING: EMOJI['learning'],
        MemoryType.CONTEXT: EMOJI['context'],
    }
    emoji = emojis.get(memory_type, EMOJI['memory'])
    return f"{emoji} {memory_type.value}"


# ============================================================================
# CLI COMMAND HANDLERS
# ============================================================================

def cmd_search(
    query: str,
    scope: str = "project",
    limit: int = 5,
    memory_type: Optional[str] = None
) -> str:
    """
    Search memories semantically.

    Args:
        query: Search query string
        scope: Search scope (project/global/both)
        limit: Maximum results to return
        memory_type: Optional filter by memory type

    Returns:
        Formatted search results with similarity scores

    Example:
        /diverga:memory search "meta-analysis heterogeneity"
        /diverga:memory search "regression" --scope global --limit 10
    """
    try:
        memory = _get_memory()

        # Parse scope
        scope_enum = SearchScope.PROJECT
        if scope.lower() == "global":
            scope_enum = SearchScope.GLOBAL
        elif scope.lower() == "both":
            scope_enum = SearchScope.BOTH

        # Parse memory type filter
        memory_types = None
        if memory_type:
            try:
                memory_types = [MemoryType(memory_type.lower())]
            except ValueError:
                pass

        # Perform search
        results = memory.search(
            query=query,
            scope=scope_enum,
            memory_types=memory_types,
            limit=limit
        )

        # Format output
        output = _format_header(f"Search Results: \"{query}\"", EMOJI['search'])

        if not results:
            output += f"{EMOJI['info']} No results found.\n"
            output += f"\n{Colors.DIM}Try:\n"
            output += f"  • Broadening your search query\n"
            output += f"  • Using --scope both to search all memories\n"
            output += f"  • Checking if memories exist with /diverga:memory status{Colors.RESET}\n"
            return output

        output += f"Found {Colors.BOLD}{len(results)}{Colors.RESET} result(s)\n\n"

        # Table data
        table_data = []
        for idx, result in enumerate(results, 1):
            # Format similarity score
            similarity = ""
            if result.similarity_score is not None:
                score_pct = int(result.similarity_score * 100)
                if score_pct >= 80:
                    similarity = f"{Colors.BRIGHT_GREEN}{score_pct}%{Colors.RESET}"
                elif score_pct >= 60:
                    similarity = f"{Colors.GREEN}{score_pct}%{Colors.RESET}"
                elif score_pct >= 40:
                    similarity = f"{Colors.YELLOW}{score_pct}%{Colors.RESET}"
                else:
                    similarity = f"{Colors.DIM}{score_pct}%{Colors.RESET}"

            # Truncate title
            title = result.title or result.preview or "(no title)"
            if len(title) > 50:
                title = title[:47] + "..."

            table_data.append([
                f"{Colors.DIM}#{idx}{Colors.RESET}",
                f"{Colors.BOLD}ID:{Colors.RESET} {result.id}",
                _format_memory_type(result.memory_type),
                title,
                _format_priority(result.priority),
                similarity
            ])

        output += tabulate(
            table_data,
            headers=['#', 'ID', 'Type', 'Title', 'Priority', 'Match'],
            tablefmt='simple'
        )

        output += f"\n\n{Colors.DIM}Use /diverga:memory context <id> to see full details{Colors.RESET}\n"

        return output

    except Exception as e:
        return f"{EMOJI['error']} {Colors.RED}Search failed:{Colors.RESET} {str(e)}\n"


def cmd_status() -> str:
    """
    Show current memory system status.

    Returns:
        Memory count by type, storage location, embedding provider, recent activity

    Example:
        /diverga:memory status
    """
    try:
        memory = _get_memory()

        output = _format_header("Memory System Status", EMOJI['status'])

        # Storage location
        output += _format_subheader("Storage")
        output += f"\n{_format_key_value('Location', str(memory.memory_dir), 2)}\n"
        output += f"{_format_key_value('Scope', memory.scope, 2)}\n"

        # Check if database exists
        if memory.db_path.exists():
            db_size = memory.db_path.stat().st_size
            db_size_mb = db_size / (1024 * 1024)
            output += f"{_format_key_value('Database', f'{db_size_mb:.2f} MB', 2)}\n"

        # Get statistics
        stats = memory.db.get_statistics()

        # Memory counts
        output += _format_subheader("\nMemories")
        output += f"\n{_format_key_value('Total', str(stats['total_memories']), 2)}\n"

        if stats.get('by_type'):
            output += f"\n{Colors.DIM}  By Type:{Colors.RESET}\n"
            for mem_type, count in stats['by_type'].items():
                emoji = EMOJI.get(mem_type, EMOJI['memory'])
                output += f"    {emoji} {mem_type:<12} {Colors.BOLD}{count}{Colors.RESET}\n"

        # Sessions
        output += _format_subheader("\nSessions")
        output += f"\n{_format_key_value('Total', str(stats['total_sessions']), 2)}\n"

        recent_sessions = memory.get_session_history(limit=3)
        if recent_sessions:
            output += f"\n{Colors.DIM}  Recent:{Colors.RESET}\n"
            for session in recent_sessions:
                started = datetime.fromisoformat(session['started_at'])
                output += f"    {EMOJI['session']} {session['id']} - {_format_timestamp(started)}\n"

        # Embeddings
        output += _format_subheader("\nEmbeddings")
        if memory.embeddings:
            output += f"\n{_format_key_value('Provider', 'OpenAI (text-embedding-3-small)', 2)}\n"
            output += f"{_format_key_value('Status', f'{Colors.BRIGHT_GREEN}Enabled{Colors.RESET}', 2)}\n"
        else:
            output += f"\n{_format_key_value('Status', f'{Colors.YELLOW}Disabled (text search only){Colors.RESET}', 2)}\n"

        # Top namespaces
        if stats.get('top_namespaces'):
            output += _format_subheader("\nTop Namespaces")
            for ns_data in stats['top_namespaces'][:5]:
                namespace = ns_data['namespace']
                count = ns_data['count']
                output += f"\n  {Colors.CYAN}{namespace}{Colors.RESET}: {Colors.BOLD}{count}{Colors.RESET} memories"

        output += "\n"
        return output

    except Exception as e:
        return f"{EMOJI['error']} {Colors.RED}Status check failed:{Colors.RESET} {str(e)}\n"


def cmd_context(project: Optional[str] = None) -> str:
    """
    Show current project context.

    Args:
        project: Optional project name (uses current if None)

    Returns:
        Current project context in readable format

    Example:
        /diverga:memory context
        /diverga:memory context --project "AI-Education-Meta-2025"
    """
    try:
        memory = _get_memory()

        project_name = project or memory._get_project_name() or "Unknown"

        output = _format_header(f"Project Context: {project_name}", EMOJI['context'])

        # Get project context
        context = memory.get_project_context(project)

        # Summary
        output += _format_subheader("Summary")
        output += f"\n{_format_key_value('Project', context['project_name'], 2)}\n"
        output += f"{_format_key_value('Total Memories', str(context['total_memories']), 2)}\n"
        output += f"{_format_key_value('Last Updated', context['last_updated'], 2)}\n"

        # Recent decisions
        if context['recent_decisions']:
            output += _format_subheader("\nRecent Decisions")
            for decision in context['recent_decisions'][:5]:
                title = decision.title or "(no title)"
                if len(title) > 60:
                    title = title[:57] + "..."
                output += f"\n  {EMOJI['decision']} {title}"
                output += f"\n    {Colors.DIM}{_format_timestamp(decision.created_at)}{Colors.RESET}"

        # Key patterns
        if context['key_patterns']:
            output += _format_subheader("\nKey Patterns")
            for pattern in context['key_patterns'][:5]:
                title = pattern.title or pattern.preview or "(no title)"
                if len(title) > 60:
                    title = title[:57] + "..."
                output += f"\n  {EMOJI['pattern']} {title}"
                output += f"\n    {Colors.DIM}Priority: {_format_priority(pattern.priority)}{Colors.RESET}"

        # Active sessions
        if context['active_sessions']:
            output += _format_subheader("\nActive Sessions")
            for session in context['active_sessions']:
                output += f"\n  {EMOJI['session']} {session['id']}"
                if session.get('summary'):
                    summary = session['summary'][:60]
                    output += f"\n    {Colors.DIM}{summary}{Colors.RESET}"

        output += "\n"
        return output

    except Exception as e:
        return f"{EMOJI['error']} {Colors.RED}Context retrieval failed:{Colors.RESET} {str(e)}\n"


def cmd_history(limit: int = 10, from_date: Optional[str] = None, to_date: Optional[str] = None) -> str:
    """
    Show recent session history.

    Args:
        limit: Maximum number of sessions to show
        from_date: Optional start date (YYYY-MM-DD)
        to_date: Optional end date (YYYY-MM-DD)

    Returns:
        Recent sessions with summaries

    Example:
        /diverga:memory history
        /diverga:memory history --limit 20
        /diverga:memory history --from 2026-01-01 --to 2026-01-31
    """
    try:
        memory = _get_memory()

        output = _format_header("Session History", EMOJI['history'])

        sessions = memory.get_session_history(limit=limit)

        if not sessions:
            output += f"{EMOJI['info']} No sessions found.\n"
            return output

        output += f"Showing {Colors.BOLD}{len(sessions)}{Colors.RESET} session(s)\n\n"

        for idx, session in enumerate(sessions, 1):
            # Parse timestamps
            started = datetime.fromisoformat(session['started_at'])
            ended = None
            if session.get('ended_at'):
                ended = datetime.fromisoformat(session['ended_at'])

            # Filter by date if specified
            if from_date:
                from_dt = datetime.fromisoformat(from_date)
                if started < from_dt:
                    continue
            if to_date:
                to_dt = datetime.fromisoformat(to_date)
                if started > to_dt:
                    continue

            # Session header
            output += f"{Colors.BOLD}Session #{idx}: {session['id']}{Colors.RESET}\n"

            # Timing
            output += f"  {EMOJI['time']} Started: {_format_timestamp(started)}"
            if ended:
                duration = ended - started
                hours = int(duration.total_seconds() / 3600)
                minutes = int((duration.total_seconds() % 3600) / 60)
                if hours > 0:
                    output += f" | Duration: {hours}h {minutes}m"
                else:
                    output += f" | Duration: {minutes}m"
            output += "\n"

            # Project
            if session.get('project_name'):
                output += f"  {EMOJI['project']} Project: {session['project_name']}\n"

            # Summary
            if session.get('summary'):
                summary = session['summary']
                if len(summary) > 100:
                    summary = summary[:97] + "..."
                output += f"  {Colors.DIM}Summary: {summary}{Colors.RESET}\n"

            # Agents used
            if session.get('agents_used'):
                agents = session['agents_used']
                if isinstance(agents, list) and agents:
                    agents_str = ", ".join(agents[:3])
                    if len(agents) > 3:
                        agents_str += f" +{len(agents) - 3} more"
                    output += f"  {Colors.DIM}Agents: {agents_str}{Colors.RESET}\n"

            output += "\n"

        return output

    except Exception as e:
        return f"{EMOJI['error']} {Colors.RED}History retrieval failed:{Colors.RESET} {str(e)}\n"


def cmd_export(
    format: str = "md",
    scope: str = "project",
    output: Optional[str] = None
) -> str:
    """
    Export memories to file.

    Args:
        format: Output format (md/json/yaml)
        scope: Export scope (project/global/both)
        output: Optional output path (auto-generated if None)

    Returns:
        Success message with file path

    Example:
        /diverga:memory export --format md
        /diverga:memory export --format json --output ~/memories.json
        /diverga:memory export --format yaml --scope global
    """
    try:
        memory = _get_memory()

        output_path = output
        if not output_path:
            # Auto-generate filename
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            project = memory._get_project_name() or "global"
            extension = format.lower()
            filename = f"diverga_memory_{project}_{timestamp}.{extension}"
            output_path = str(Path.home() / "Downloads" / filename)

        # Get all memories based on scope
        if scope.lower() == "project":
            project_name = memory._get_project_name()
        elif scope.lower() == "global":
            project_name = None
        else:
            project_name = None  # Both

        # Get project context
        context = memory.get_project_context(project_name)

        # Get all memories (simplified - get recent)
        all_memories = memory.db.get_memories_by_namespace(
            namespace="",
            include_children=True,
            limit=1000
        )

        # Filter by project if needed
        if project_name:
            all_memories = [m for m in all_memories if m.get('project_name') == project_name]

        # Export based on format
        if format.lower() == "json":
            export_data = {
                'exported_at': datetime.now().isoformat(),
                'project': context['project_name'],
                'total_memories': len(all_memories),
                'memories': all_memories
            }
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(export_data, f, indent=2, default=str)

        elif format.lower() == "yaml":
            if not HAS_YAML:
                return f"{EMOJI['error']} {Colors.RED}YAML export requires PyYAML:{Colors.RESET} pip install pyyaml\n"

            export_data = {
                'exported_at': datetime.now().isoformat(),
                'project': context['project_name'],
                'total_memories': len(all_memories),
                'memories': all_memories
            }
            with open(output_path, 'w', encoding='utf-8') as f:
                yaml.dump(export_data, f, default_flow_style=False, allow_unicode=True)

        else:  # Markdown (default)
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(f"# Diverga Memory Export\n\n")
                f.write(f"**Project:** {context['project_name']}\n")
                f.write(f"**Exported:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"**Total Memories:** {len(all_memories)}\n\n")

                f.write(f"---\n\n")

                # Group by type
                by_type = {}
                for mem in all_memories:
                    mem_type = mem.get('memory_type', 'other')
                    if mem_type not in by_type:
                        by_type[mem_type] = []
                    by_type[mem_type].append(mem)

                for mem_type, memories in sorted(by_type.items()):
                    f.write(f"## {mem_type.title()}\n\n")

                    for mem in memories:
                        f.write(f"### {mem.get('title', '(no title)')}\n\n")
                        f.write(f"- **ID:** {mem['id']}\n")
                        f.write(f"- **Created:** {mem['created_at']}\n")
                        f.write(f"- **Priority:** {mem.get('priority', 'N/A')}\n")
                        f.write(f"- **Namespace:** {mem['namespace']}\n")

                        if mem.get('tags'):
                            tags = mem['tags']
                            if isinstance(tags, list):
                                f.write(f"- **Tags:** {', '.join(tags)}\n")

                        f.write(f"\n{mem['content']}\n\n")
                        f.write(f"---\n\n")

        # Format success message
        output_msg = _format_header("Export Complete", EMOJI['export'])
        output_msg += f"{EMOJI['success']} Successfully exported {Colors.BOLD}{len(all_memories)}{Colors.RESET} memories\n\n"
        output_msg += f"{_format_key_value('Format', format.upper(), 2)}\n"
        output_msg += f"{_format_key_value('Scope', scope, 2)}\n"
        output_msg += f"{_format_key_value('File', output_path, 2)}\n"

        # File size
        file_size = Path(output_path).stat().st_size
        file_size_kb = file_size / 1024
        output_msg += f"{_format_key_value('Size', f'{file_size_kb:.1f} KB', 2)}\n"

        return output_msg

    except Exception as e:
        return f"{EMOJI['error']} {Colors.RED}Export failed:{Colors.RESET} {str(e)}\n"


def cmd_setup() -> str:
    """
    Interactive setup wizard for memory system.

    Returns:
        Setup instructions and status

    Example:
        /diverga:memory setup
    """
    output = _format_header("Memory System Setup", EMOJI['info'])

    output += f"{Colors.BOLD}Configuration{Colors.RESET}\n\n"
    output += f"The Diverga Memory System stores data in:\n"
    output += f"  • Project-scoped: {Colors.CYAN}.diverga/memory/{Colors.RESET}\n"
    output += f"  • Global: {Colors.CYAN}~/.diverga/memory/{Colors.RESET}\n\n"

    output += f"{Colors.BOLD}Embedding Provider{Colors.RESET}\n\n"
    output += f"For semantic search, set your OpenAI API key:\n"
    output += f"  {Colors.DIM}export OPENAI_API_KEY='your-api-key'{Colors.RESET}\n\n"

    output += f"Without embeddings, the system uses text-based search (still functional).\n\n"

    output += f"{Colors.BOLD}Verification{Colors.RESET}\n\n"
    output += f"Run {Colors.CYAN}/diverga:memory status{Colors.RESET} to verify setup.\n"

    return output


def cmd_stats() -> str:
    """
    Show detailed memory statistics.

    Returns:
        Detailed statistics about memory usage, patterns, etc.

    Example:
        /diverga:memory stats
    """
    try:
        memory = _get_memory()
        stats = memory.db.get_statistics()

        output = _format_header("Detailed Statistics", EMOJI['stats'])

        # Overview
        output += _format_subheader("Overview")
        output += f"\n{_format_key_value('Total Memories', str(stats['total_memories']), 2)}\n"
        output += f"{_format_key_value('Total Sessions', str(stats['total_sessions']), 2)}\n"

        # Memory types breakdown
        if stats.get('by_type'):
            output += _format_subheader("\nMemory Types Distribution")

            table_data = []
            total = sum(stats['by_type'].values())
            for mem_type, count in sorted(stats['by_type'].items(), key=lambda x: x[1], reverse=True):
                percentage = (count / total * 100) if total > 0 else 0
                emoji = EMOJI.get(mem_type, EMOJI['memory'])
                bar_length = int(percentage / 5)  # Scale to 20 chars max
                bar = '█' * bar_length + '░' * (20 - bar_length)

                table_data.append([
                    f"{emoji} {mem_type}",
                    count,
                    f"{percentage:.1f}%",
                    bar
                ])

            output += "\n" + tabulate(
                table_data,
                headers=['Type', 'Count', '%', 'Distribution'],
                tablefmt='simple'
            )

        # Top namespaces
        if stats.get('top_namespaces'):
            output += _format_subheader("\n\nTop Namespaces")

            table_data = []
            for ns_data in stats['top_namespaces']:
                namespace = ns_data['namespace']
                count = ns_data['count']
                table_data.append([namespace, count])

            output += "\n" + tabulate(
                table_data,
                headers=['Namespace', 'Count'],
                tablefmt='simple'
            )

        # Storage info
        if memory.db_path.exists():
            output += _format_subheader("\n\nStorage")
            db_size = memory.db_path.stat().st_size / (1024 * 1024)
            output += f"\n{_format_key_value('Database Size', f'{db_size:.2f} MB', 2)}\n"
            output += f"{_format_key_value('Location', str(memory.db_path), 2)}\n"

        output += "\n"
        return output

    except Exception as e:
        return f"{EMOJI['error']} {Colors.RED}Stats retrieval failed:{Colors.RESET} {str(e)}\n"


# ============================================================================
# MAIN (for standalone usage)
# ============================================================================

def main():
    """
    Main entry point for standalone CLI usage.

    Usage:
        python cli.py search "query"
        python cli.py status
        python cli.py context
        python cli.py history
        python cli.py export --format md
        python cli.py stats
    """
    import argparse

    parser = argparse.ArgumentParser(
        description="Diverga Memory System CLI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s search "meta-analysis"
  %(prog)s search "regression" --scope global --limit 10
  %(prog)s status
  %(prog)s context
  %(prog)s history --limit 20
  %(prog)s export --format json --output ~/memories.json
  %(prog)s stats
        """
    )

    subparsers = parser.add_subparsers(dest='command', help='Command to execute')

    # search
    search_parser = subparsers.add_parser('search', help='Search memories')
    search_parser.add_argument('query', help='Search query')
    search_parser.add_argument('--scope', default='project', choices=['project', 'global', 'both'])
    search_parser.add_argument('--limit', type=int, default=5)
    search_parser.add_argument('--type', dest='memory_type', help='Filter by memory type')

    # status
    subparsers.add_parser('status', help='Show memory system status')

    # context
    context_parser = subparsers.add_parser('context', help='Show project context')
    context_parser.add_argument('--project', help='Project name')

    # history
    history_parser = subparsers.add_parser('history', help='Show session history')
    history_parser.add_argument('--limit', type=int, default=10)
    history_parser.add_argument('--from', dest='from_date', help='Start date (YYYY-MM-DD)')
    history_parser.add_argument('--to', dest='to_date', help='End date (YYYY-MM-DD)')

    # export
    export_parser = subparsers.add_parser('export', help='Export memories')
    export_parser.add_argument('--format', default='md', choices=['md', 'json', 'yaml'])
    export_parser.add_argument('--scope', default='project', choices=['project', 'global', 'both'])
    export_parser.add_argument('--output', help='Output file path')

    # stats
    subparsers.add_parser('stats', help='Show detailed statistics')

    # setup
    subparsers.add_parser('setup', help='Setup wizard')

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return

    # Execute command
    if args.command == 'search':
        result = cmd_search(args.query, args.scope, args.limit, args.memory_type)
    elif args.command == 'status':
        result = cmd_status()
    elif args.command == 'context':
        result = cmd_context(args.project)
    elif args.command == 'history':
        result = cmd_history(args.limit, args.from_date, args.to_date)
    elif args.command == 'export':
        result = cmd_export(args.format, args.scope, args.output)
    elif args.command == 'stats':
        result = cmd_stats()
    elif args.command == 'setup':
        result = cmd_setup()
    else:
        result = f"Unknown command: {args.command}"

    print(result)


if __name__ == '__main__':
    main()
