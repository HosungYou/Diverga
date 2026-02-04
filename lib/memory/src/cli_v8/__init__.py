"""
Diverga Memory System v8.0 - CLI Package

OpenClaw-style command-line interface for researchers.

Commands:
    diverga doctor  - System diagnostics
    diverga setup   - Initial setup wizard
    diverga sync    - YAML → DB synchronization
    diverga search  - Hybrid search (FTS5 + vector)
    diverga status  - Project status
    diverga flush   - Manual memory flush

Author: Diverga Project
Version: 8.0.0
"""

import sys
from pathlib import Path
from typing import List, Optional

from .doctor import run_doctor
from .setup import run_setup, SetupConfig


def main(args: Optional[List[str]] = None):
    """
    CLI entry point for Diverga Memory System v8.0.

    Args:
        args: Command-line arguments (defaults to sys.argv[1:])
    """
    if args is None:
        args = sys.argv[1:]

    if not args:
        print_help()
        return

    command = args[0].lower()
    remaining_args = args[1:]

    if command == "doctor":
        run_doctor(remaining_args)
    elif command == "setup":
        run_setup(remaining_args)
    elif command == "help" or command == "--help" or command == "-h":
        print_help()
    elif command == "version" or command == "--version" or command == "-v":
        print_version()
    else:
        print(f"Unknown command: {command}")
        print("Run 'diverga help' for usage information.")
        sys.exit(1)


def print_help():
    """Print CLI help message."""
    help_text = """
🔬 Diverga Memory System v8.0
=============================

Commands:
  doctor           System diagnostics
  setup            Initial setup wizard
  status           Project status
  sync             YAML → DB synchronization
  search <query>   Hybrid search
  decision list    List decisions
  decision add     Add new decision
  flush            Manual memory flush
  export           Export to Markdown/JSON

Options:
  -h, --help       Show this help
  -v, --version    Show version

Examples:
  diverga doctor              # Check system health
  diverga setup               # Run setup wizard
  diverga setup --db          # Setup with database
  diverga setup --embeddings  # Setup with vector search
  diverga sync                # Sync YAML to database
  diverga search "meta-analysis methods"

Documentation:
  https://github.com/HosungYou/Diverga
"""
    print(help_text)


def print_version():
    """Print version information."""
    from .. import __version__
    print(f"Diverga Memory System v{__version__}")


__all__ = [
    "main",
    "run_doctor",
    "run_setup",
    "SetupConfig",
]
