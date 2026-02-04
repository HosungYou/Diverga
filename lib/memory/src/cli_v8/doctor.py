"""
Diverga Memory System v8.0 - Doctor (System Diagnostics)

OpenClaw-style system diagnostics for research projects.

Usage:
    diverga doctor           # Run full diagnostics
    diverga doctor --fix     # Attempt to fix issues
    diverga doctor --verbose # Detailed output

Author: Diverga Project
Version: 8.0.0
"""

from __future__ import annotations

import sys
import sqlite3
from pathlib import Path
from typing import List, Dict, Any, Optional

try:
    import yaml
except ImportError:
    yaml = None


class DiagnosticResult:
    """Result of a single diagnostic check."""

    def __init__(self, name: str, passed: bool, message: str,
                 fixable: bool = False, fix_command: Optional[str] = None):
        self.name = name
        self.passed = passed
        self.message = message
        self.fixable = fixable
        self.fix_command = fix_command

    @property
    def icon(self) -> str:
        if self.passed:
            return "✅"
        elif self.fixable:
            return "⚠️"
        else:
            return "❌"

    def __str__(self) -> str:
        return f"{self.icon} {self.message}"


class DivergaDoctor:
    """
    System diagnostics for Diverga Memory System.

    Checks:
    - Python version
    - Required dependencies
    - Project structure
    - YAML file validity
    - Database accessibility
    - Sync status
    - Embedding configuration
    """

    def __init__(self, project_root: Optional[Path] = None):
        """
        Initialize doctor with project root.

        Args:
            project_root: Project root directory (defaults to cwd)
        """
        self.project_root = Path(project_root) if project_root else Path.cwd()
        self.results: List[DiagnosticResult] = []

    def run_all_checks(self, verbose: bool = False) -> Dict[str, Any]:
        """
        Run all diagnostic checks.

        Args:
            verbose: Show detailed output

        Returns:
            Dict with diagnostic summary
        """
        self.results = []

        # Core checks
        self._check_python_version()
        self._check_dependencies()
        self._check_project_structure()
        self._check_yaml_files()
        self._check_database()
        self._check_sync_status()
        self._check_embeddings()

        # Calculate summary
        passed = sum(1 for r in self.results if r.passed)
        warnings = sum(1 for r in self.results if not r.passed and r.fixable)
        errors = sum(1 for r in self.results if not r.passed and not r.fixable)

        return {
            "total": len(self.results),
            "passed": passed,
            "warnings": warnings,
            "errors": errors,
            "results": self.results,
            "overall": self._get_overall_status(passed, warnings, errors)
        }

    def _get_overall_status(self, passed: int, warnings: int, errors: int) -> str:
        """Get overall status string."""
        if errors > 0:
            return "🔴 ERRORS"
        elif warnings > 0:
            return "🟡 FUNCTIONAL (with warnings)"
        else:
            return "🟢 HEALTHY"

    def _check_python_version(self):
        """Check Python version (3.10+ required)."""
        version = sys.version_info
        version_str = f"{version.major}.{version.minor}.{version.micro}"

        if version >= (3, 10):
            self.results.append(DiagnosticResult(
                "python_version",
                True,
                f"Python {version_str} detected (3.10+ required)"
            ))
        else:
            self.results.append(DiagnosticResult(
                "python_version",
                False,
                f"Python {version_str} detected (3.10+ required)",
                fixable=False
            ))

    def _check_dependencies(self):
        """Check required dependencies."""
        # Check PyYAML
        if yaml is not None:
            self.results.append(DiagnosticResult(
                "pyyaml",
                True,
                "PyYAML installed"
            ))
        else:
            self.results.append(DiagnosticResult(
                "pyyaml",
                False,
                "PyYAML not installed",
                fixable=True,
                fix_command="pip install pyyaml>=6.0"
            ))

        # Check numpy (optional but recommended)
        try:
            import numpy
            self.results.append(DiagnosticResult(
                "numpy",
                True,
                f"NumPy {numpy.__version__} installed"
            ))
        except ImportError:
            self.results.append(DiagnosticResult(
                "numpy",
                False,
                "NumPy not installed (optional, for vector search)",
                fixable=True,
                fix_command="pip install numpy>=1.24.0"
            ))

        # Check sentence-transformers (optional)
        try:
            import sentence_transformers
            self.results.append(DiagnosticResult(
                "sentence_transformers",
                True,
                f"sentence-transformers installed"
            ))
        except ImportError:
            self.results.append(DiagnosticResult(
                "sentence_transformers",
                False,
                "sentence-transformers not installed (optional, for embeddings)",
                fixable=True,
                fix_command="pip install sentence-transformers>=2.2"
            ))

    def _check_project_structure(self):
        """Check .research/ directory structure."""
        research_dir = self.project_root / ".research"

        if not research_dir.exists():
            self.results.append(DiagnosticResult(
                "research_dir",
                False,
                ".research/ directory not found",
                fixable=True,
                fix_command="diverga setup"
            ))
            return

        self.results.append(DiagnosticResult(
            "research_dir",
            True,
            ".research/ directory found"
        ))

        # Check key files
        key_files = [
            ("project-state.yaml", "Project state"),
            ("decision-log.yaml", "Decision log"),
        ]

        for filename, description in key_files:
            filepath = research_dir / filename
            if filepath.exists():
                self.results.append(DiagnosticResult(
                    f"file_{filename}",
                    True,
                    f"{description} found"
                ))
            else:
                self.results.append(DiagnosticResult(
                    f"file_{filename}",
                    False,
                    f"{description} not found",
                    fixable=True,
                    fix_command="diverga setup"
                ))

    def _check_yaml_files(self):
        """Check YAML file validity."""
        if yaml is None:
            return

        research_dir = self.project_root / ".research"
        yaml_files = [
            "project-state.yaml",
            "decision-log.yaml",
            "checkpoints.yaml"
        ]

        for filename in yaml_files:
            filepath = research_dir / filename
            if not filepath.exists():
                continue

            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    data = yaml.safe_load(f)

                if data is not None:
                    self.results.append(DiagnosticResult(
                        f"yaml_{filename}",
                        True,
                        f"{filename} is valid YAML"
                    ))
                else:
                    self.results.append(DiagnosticResult(
                        f"yaml_{filename}",
                        False,
                        f"{filename} is empty",
                        fixable=True
                    ))
            except yaml.YAMLError as e:
                self.results.append(DiagnosticResult(
                    f"yaml_{filename}",
                    False,
                    f"{filename} has invalid YAML: {e}",
                    fixable=False
                ))

    def _check_database(self):
        """Check SQLite database accessibility."""
        # Check default DB path
        default_db_path = Path.home() / ".diverga" / "memory.db"

        # Check project-specific DB path
        state_file = self.project_root / ".research" / "project-state.yaml"
        db_path = None

        if state_file.exists() and yaml is not None:
            try:
                with open(state_file, 'r', encoding='utf-8') as f:
                    state = yaml.safe_load(f) or {}
                    db_path = state.get('metadata', {}).get('db_path')
            except Exception:
                pass

        if db_path:
            db_path = Path(db_path)
            if db_path.exists():
                try:
                    conn = sqlite3.connect(str(db_path))
                    cursor = conn.cursor()
                    cursor.execute("SELECT COUNT(*) FROM memories")
                    count = cursor.fetchone()[0]
                    conn.close()
                    self.results.append(DiagnosticResult(
                        "database",
                        True,
                        f"Database accessible ({count} memories)"
                    ))
                except Exception as e:
                    self.results.append(DiagnosticResult(
                        "database",
                        False,
                        f"Database error: {e}",
                        fixable=False
                    ))
            else:
                self.results.append(DiagnosticResult(
                    "database",
                    False,
                    f"Database not found at {db_path}",
                    fixable=True,
                    fix_command="diverga setup --db"
                ))
        else:
            self.results.append(DiagnosticResult(
                "database",
                False,
                "No database configured (optional)",
                fixable=True,
                fix_command="diverga setup --db"
            ))

    def _check_sync_status(self):
        """Check YAML → DB sync status."""
        if yaml is None:
            return

        research_dir = self.project_root / ".research"
        log_file = research_dir / "decision-log.yaml"
        state_file = research_dir / "project-state.yaml"

        if not log_file.exists():
            return

        try:
            with open(log_file, 'r', encoding='utf-8') as f:
                log_data = yaml.safe_load(f) or {}

            decisions = log_data.get('decisions', [])
            if not decisions:
                return

            # Check last synced
            last_synced = None
            if state_file.exists():
                with open(state_file, 'r', encoding='utf-8') as f:
                    state = yaml.safe_load(f) or {}
                    last_synced = state.get('metadata', {}).get('last_synced_decision_id')

            if last_synced is None:
                pending = len(decisions)
            else:
                pending = 0
                found = False
                for dec in decisions:
                    if found:
                        pending += 1
                    elif dec.get('id') == last_synced:
                        found = True

            if pending == 0:
                self.results.append(DiagnosticResult(
                    "sync_status",
                    True,
                    "All decisions synced to database"
                ))
            else:
                self.results.append(DiagnosticResult(
                    "sync_status",
                    False,
                    f"{pending} decisions need sync",
                    fixable=True,
                    fix_command="diverga sync"
                ))
        except Exception as e:
            self.results.append(DiagnosticResult(
                "sync_status",
                False,
                f"Error checking sync status: {e}",
                fixable=False
            ))

    def _check_embeddings(self):
        """Check embedding configuration."""
        try:
            import sentence_transformers
            has_embeddings = True
        except ImportError:
            has_embeddings = False

        if has_embeddings:
            self.results.append(DiagnosticResult(
                "embeddings",
                True,
                "Vector embeddings available"
            ))
        else:
            self.results.append(DiagnosticResult(
                "embeddings",
                False,
                "Vector embeddings disabled (sentence-transformers not installed)",
                fixable=True,
                fix_command="pip install -r lib/memory/requirements-embeddings.txt"
            ))


def run_doctor(args: List[str], project_root: Optional[Path] = None):
    """
    Run doctor diagnostics.

    Args:
        args: Command-line arguments
        project_root: Project root directory
    """
    verbose = "--verbose" in args or "-v" in args
    fix = "--fix" in args

    print("\n🔍 Diverga System Diagnostics v8.0")
    print("=" * 40)
    print()

    doctor = DivergaDoctor(project_root)
    summary = doctor.run_all_checks(verbose)

    # Print results
    for result in summary['results']:
        print(result)
        if verbose and result.fix_command and not result.passed:
            print(f"   Fix: {result.fix_command}")

    print()
    print("-" * 40)
    print(f"Overall: {summary['overall']}")
    print(f"Passed: {summary['passed']}/{summary['total']}")
    if summary['warnings'] > 0:
        print(f"Warnings: {summary['warnings']}")
    if summary['errors'] > 0:
        print(f"Errors: {summary['errors']}")
    print()

    # Show recommendations
    fixable = [r for r in summary['results'] if not r.passed and r.fixable]
    if fixable:
        print("Recommendations:")
        for i, r in enumerate(fixable, 1):
            print(f"  {i}. {r.fix_command}")
        print()

    # Run fixes if requested
    if fix and fixable:
        print("Running fixes...")
        for r in fixable:
            if r.fix_command and r.fix_command.startswith("pip install"):
                import subprocess
                print(f"  Running: {r.fix_command}")
                subprocess.run(r.fix_command.split(), check=False)
        print()
        print("Re-run 'diverga doctor' to verify fixes.")
