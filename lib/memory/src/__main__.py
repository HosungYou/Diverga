#!/usr/bin/env python
"""
Diverga Memory System - CLI Entry Point

Allows running the memory module as a command-line tool:
    python -m diverga.memory search "query"
    python -m diverga.memory status
    python -m diverga.memory --help
    python -m diverga.memory --version

Supports all CLI commands:
- search: Semantic search across memories
- status: Memory system status and statistics
- context: Show current project context
- history: View recent session history
- export: Export memories to file (markdown/JSON/YAML)
- setup: Interactive setup wizard
- stats: Detailed memory statistics

Works standalone without Claude Code or Codex.
"""

import sys
import argparse
from pathlib import Path

# Add src directory to path for imports
src_path = Path(__file__).parent
if str(src_path) not in sys.path:
    sys.path.insert(0, str(src_path))

# Import CLI handlers
from cli import (
    cmd_search,
    cmd_status,
    cmd_context,
    cmd_history,
    cmd_export,
    cmd_setup,
    cmd_stats,
    EMOJI,
    Colors,
)

__version__ = "1.0.0"


def create_parser() -> argparse.ArgumentParser:
    """Create and configure argument parser."""
    parser = argparse.ArgumentParser(
        prog="diverga-memory",
        description="Diverga Memory System - Context-persistent research assistant",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s search "meta-analysis heterogeneity"
  %(prog)s search "regression" --scope global --limit 10
  %(prog)s search "learning" --type decision --scope project
  %(prog)s status
  %(prog)s context
  %(prog)s context --project "AI-Education-Meta-2025"
  %(prog)s history --limit 20
  %(prog)s history --from 2026-01-01 --to 2026-01-31
  %(prog)s export --format md
  %(prog)s export --format json --output ~/memories.json
  %(prog)s export --format yaml --scope global
  %(prog)s stats
  %(prog)s setup

Environment Variables:
  OPENAI_API_KEY    OpenAI API key for semantic embeddings (optional)
  DIVERGA_MEMORY_PATH    Custom memory storage path (optional)

For more information, visit: https://github.com/HosungYou/Diverga
        """,
    )

    # Global options
    parser.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s {__version__}",
        help="Show version and exit",
    )

    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Enable verbose output for debugging",
    )

    parser.add_argument(
        "--no-color",
        action="store_true",
        help="Disable colored output",
    )

    # Subcommands
    subparsers = parser.add_subparsers(
        dest="command",
        help="Command to execute",
        required=False,
    )

    # ========================================================================
    # SEARCH COMMAND
    # ========================================================================
    search_parser = subparsers.add_parser(
        "search",
        help="Search memories semantically across the knowledge base",
        aliases=["s"],
    )
    search_parser.add_argument(
        "query",
        help="Search query string (e.g., 'meta-analysis', 'effect size calculation')",
    )
    search_parser.add_argument(
        "--scope",
        choices=["project", "global", "both"],
        default="project",
        help="Search scope: project-specific, global, or both (default: project)",
    )
    search_parser.add_argument(
        "--limit", "-l",
        type=int,
        default=5,
        metavar="N",
        help="Maximum number of results to return (default: 5)",
    )
    search_parser.add_argument(
        "--type", "-t",
        dest="memory_type",
        metavar="TYPE",
        help="Filter by memory type: decision, pattern, learning, context",
    )

    # ========================================================================
    # STATUS COMMAND
    # ========================================================================
    status_parser = subparsers.add_parser(
        "status",
        help="Show current memory system status and statistics",
        aliases=["st"],
    )
    # No additional arguments for status

    # ========================================================================
    # CONTEXT COMMAND
    # ========================================================================
    context_parser = subparsers.add_parser(
        "context",
        help="Show current project context and recent decisions",
        aliases=["ctx"],
    )
    context_parser.add_argument(
        "--project", "-p",
        metavar="NAME",
        help="Project name (uses current project if not specified)",
    )

    # ========================================================================
    # HISTORY COMMAND
    # ========================================================================
    history_parser = subparsers.add_parser(
        "history",
        help="View recent session history with summaries",
        aliases=["h"],
    )
    history_parser.add_argument(
        "--limit", "-l",
        type=int,
        default=10,
        metavar="N",
        help="Maximum number of sessions to show (default: 10)",
    )
    history_parser.add_argument(
        "--from",
        dest="from_date",
        metavar="YYYY-MM-DD",
        help="Start date for filtering sessions",
    )
    history_parser.add_argument(
        "--to",
        dest="to_date",
        metavar="YYYY-MM-DD",
        help="End date for filtering sessions",
    )

    # ========================================================================
    # EXPORT COMMAND
    # ========================================================================
    export_parser = subparsers.add_parser(
        "export",
        help="Export memories to file (markdown/JSON/YAML)",
        aliases=["e"],
    )
    export_parser.add_argument(
        "--format", "-f",
        choices=["md", "json", "yaml"],
        default="md",
        help="Export format: md (markdown), json, or yaml (default: md)",
    )
    export_parser.add_argument(
        "--scope",
        choices=["project", "global", "both"],
        default="project",
        help="Export scope: project-specific, global, or both (default: project)",
    )
    export_parser.add_argument(
        "--output", "-o",
        metavar="PATH",
        help="Output file path (auto-generated in ~/Downloads if not specified)",
    )

    # ========================================================================
    # SETUP COMMAND
    # ========================================================================
    setup_parser = subparsers.add_parser(
        "setup",
        help="Interactive setup wizard for memory system configuration",
        aliases=["init"],
    )
    # No additional arguments for setup

    # ========================================================================
    # STATS COMMAND
    # ========================================================================
    stats_parser = subparsers.add_parser(
        "stats",
        help="Show detailed memory statistics and usage breakdown",
        aliases=["stat"],
    )
    # No additional arguments for stats

    return parser


def main() -> int:
    """
    Main entry point for the CLI.

    Returns:
        Exit code (0 for success, 1 for error)
    """
    parser = create_parser()

    # Handle no arguments - show help
    if len(sys.argv) == 1:
        parser.print_help()
        return 0

    args = parser.parse_args()

    # Apply color settings
    if args.no_color:
        Colors.disable()

    # Verbose mode not currently used, but parsed for future enhancement
    verbose = args.verbose

    try:
        # Route to appropriate command handler
        if args.command in ["search", "s"]:
            result = cmd_search(
                query=args.query,
                scope=args.scope,
                limit=args.limit,
                memory_type=args.memory_type,
            )
            print(result)
            return 0

        elif args.command in ["status", "st"]:
            result = cmd_status()
            print(result)
            return 0

        elif args.command in ["context", "ctx"]:
            result = cmd_context(project=args.project)
            print(result)
            return 0

        elif args.command in ["history", "h"]:
            result = cmd_history(
                limit=args.limit,
                from_date=args.from_date,
                to_date=args.to_date,
            )
            print(result)
            return 0

        elif args.command in ["export", "e"]:
            result = cmd_export(
                format=args.format,
                scope=args.scope,
                output=args.output,
            )
            print(result)
            return 0

        elif args.command in ["setup", "init"]:
            result = cmd_setup()
            print(result)
            return 0

        elif args.command in ["stats", "stat"]:
            result = cmd_stats()
            print(result)
            return 0

        else:
            # This shouldn't happen with argparse, but be safe
            print(f"{EMOJI['error']} Unknown command: {args.command}", file=sys.stderr)
            parser.print_help()
            return 1

    except KeyboardInterrupt:
        print(f"\n{EMOJI['error']} Operation cancelled by user", file=sys.stderr)
        return 130  # Standard exit code for SIGINT

    except Exception as e:
        print(
            f"{EMOJI['error']} {Colors.RED}Fatal error:{Colors.RESET} {str(e)}",
            file=sys.stderr,
        )
        if verbose:
            import traceback
            traceback.print_exc(file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
