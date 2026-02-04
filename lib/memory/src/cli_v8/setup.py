"""
Diverga Memory System v8.0 - Setup Wizard

OpenClaw-style interactive setup wizard for researchers.

Usage:
    diverga setup              # Interactive setup
    diverga setup --db         # Enable database
    diverga setup --embeddings # Enable vector embeddings
    diverga setup --test       # Test mode (no changes)

Author: Diverga Project
Version: 8.0.0
"""

from __future__ import annotations

import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Optional, Dict, Any
from datetime import datetime

try:
    import yaml
except ImportError:
    yaml = None


@dataclass
class SetupConfig:
    """Configuration from setup wizard."""

    project_name: str = ""
    research_question: str = ""
    paradigm: str = "quantitative"  # quantitative, qualitative, mixed
    enable_db: bool = True
    enable_embeddings: bool = False
    db_path: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for YAML serialization."""
        return {
            "project_name": self.project_name,
            "research_question": self.research_question,
            "paradigm": self.paradigm,
            "enable_db": self.enable_db,
            "enable_embeddings": self.enable_embeddings,
            "db_path": self.db_path,
        }


class SetupWizard:
    """
    Interactive setup wizard for Diverga Memory System.

    Creates project structure and configuration.
    """

    def __init__(self, project_root: Optional[Path] = None):
        """
        Initialize setup wizard.

        Args:
            project_root: Project root directory
        """
        self.project_root = Path(project_root) if project_root else Path.cwd()
        self.config = SetupConfig()

    def run_interactive(self) -> bool:
        """
        Run interactive setup wizard.

        Returns:
            True if setup completed successfully
        """
        print()
        print("🔬 Diverga Research Project Setup")
        print("=" * 55)
        print()
        print("Welcome! Let's set up your research project.")
        print()

        # Step 1: Project Information
        self._get_project_info()

        # Step 2: Research Paradigm
        self._get_paradigm()

        # Step 3: Optional Features
        self._get_optional_features()

        # Confirmation
        print()
        print("=" * 55)
        print("Configuration Summary:")
        print(f"  Project Name: {self.config.project_name}")
        print(f"  Research Question: {self.config.research_question}")
        print(f"  Paradigm: {self.config.paradigm}")
        print(f"  Database: {'Enabled' if self.config.enable_db else 'Disabled'}")
        print(f"  Embeddings: {'Enabled' if self.config.enable_embeddings else 'Disabled'}")
        print()

        confirm = input("Create project with these settings? [Y/n] ").strip().lower()
        if confirm and confirm not in ['y', 'yes', '']:
            print("Setup cancelled.")
            return False

        # Create project
        return self._create_project()

    def run_with_args(self, args: List[str]) -> bool:
        """
        Run setup with command-line arguments.

        Args:
            args: Command-line arguments

        Returns:
            True if setup completed successfully
        """
        # Parse arguments
        if "--name" in args:
            idx = args.index("--name")
            if idx + 1 < len(args):
                self.config.project_name = args[idx + 1]

        if "--question" in args:
            idx = args.index("--question")
            if idx + 1 < len(args):
                self.config.research_question = args[idx + 1]

        if "--paradigm" in args:
            idx = args.index("--paradigm")
            if idx + 1 < len(args):
                self.config.paradigm = args[idx + 1]

        self.config.enable_db = "--db" in args or "--no-db" not in args
        self.config.enable_embeddings = "--embeddings" in args

        if "--test" in args:
            print("Test mode: Would create project with:")
            print(f"  Name: {self.config.project_name}")
            print(f"  Question: {self.config.research_question}")
            print(f"  Paradigm: {self.config.paradigm}")
            return True

        # If missing required info, run interactive
        if not self.config.project_name or not self.config.research_question:
            return self.run_interactive()

        return self._create_project()

    def _get_project_info(self):
        """Get project name and research question."""
        print("[1/3] 📋 Project Information")
        print("-" * 40)
        print()

        # Project name
        while not self.config.project_name:
            name = input("Project name: ").strip()
            if name:
                self.config.project_name = name
            else:
                print("  Please enter a project name.")

        # Research question
        while not self.config.research_question:
            question = input("Research question: ").strip()
            if question:
                self.config.research_question = question
            else:
                print("  Please enter your research question.")

        print()

    def _get_paradigm(self):
        """Get research paradigm."""
        print("[2/3] 🧪 Research Paradigm")
        print("-" * 40)
        print()
        print("Select your research paradigm:")
        print("  [Q] Quantitative (experiments, surveys, meta-analysis)")
        print("  [L] Qualitative (interviews, case studies, phenomenology)")
        print("  [M] Mixed Methods (sequential, convergent, embedded)")
        print()

        while True:
            choice = input("Paradigm [Q/L/M]: ").strip().upper()
            if choice in ['Q', 'QUANTITATIVE']:
                self.config.paradigm = "quantitative"
                break
            elif choice in ['L', 'QUALITATIVE']:
                self.config.paradigm = "qualitative"
                break
            elif choice in ['M', 'MIXED']:
                self.config.paradigm = "mixed"
                break
            elif choice == '':
                # Default to quantitative
                self.config.paradigm = "quantitative"
                break
            else:
                print("  Please enter Q, L, or M.")

        print()

    def _get_optional_features(self):
        """Get optional feature selections."""
        print("[3/3] ⚙️ Optional Features")
        print("-" * 40)
        print()

        # Database
        db_choice = input("Enable database search? [Y/n] ").strip().lower()
        self.config.enable_db = db_choice in ['', 'y', 'yes']

        # Embeddings
        embed_choice = input("Enable vector embeddings (requires 500MB download)? [y/N] ").strip().lower()
        self.config.enable_embeddings = embed_choice in ['y', 'yes']

        print()

    def _create_project(self) -> bool:
        """
        Create project structure and files.

        Returns:
            True if successful
        """
        try:
            # Create .research directory
            research_dir = self.project_root / ".research"
            research_dir.mkdir(parents=True, exist_ok=True)

            # Create subdirectories
            (research_dir / "baselines" / "literature").mkdir(parents=True, exist_ok=True)
            (research_dir / "baselines" / "methodology").mkdir(parents=True, exist_ok=True)
            (research_dir / "baselines" / "framework").mkdir(parents=True, exist_ok=True)
            (research_dir / "changes" / "current").mkdir(parents=True, exist_ok=True)
            (research_dir / "changes" / "archive").mkdir(parents=True, exist_ok=True)
            (research_dir / "sessions").mkdir(parents=True, exist_ok=True)

            # Create docs directory
            docs_dir = self.project_root / "docs"
            docs_dir.mkdir(exist_ok=True)

            # Create project-state.yaml
            self._create_project_state(research_dir)

            # Create decision-log.yaml
            self._create_decision_log(research_dir)

            # Create checkpoints.yaml
            self._create_checkpoints(research_dir)

            # Initialize database if enabled
            if self.config.enable_db:
                self._init_database()

            # Install embeddings if enabled
            if self.config.enable_embeddings:
                self._install_embeddings()

            # Generate initial docs
            self._generate_docs()

            # Print success message
            self._print_success()

            return True

        except Exception as e:
            print(f"\n❌ Setup failed: {e}")
            return False

    def _create_project_state(self, research_dir: Path):
        """Create project-state.yaml."""
        now = datetime.utcnow().isoformat() + "Z"

        state = {
            "version": "8.0",
            "project_name": self.config.project_name,
            "research_question": self.config.research_question,
            "paradigm": self.config.paradigm,
            "current_stage": "foundation",
            "created": now,
            "last_updated": now,
            "metadata": {
                "diverga_version": "8.0.0",
            }
        }

        if self.config.enable_db:
            db_path = Path.home() / ".diverga" / "memory.db"
            db_path.parent.mkdir(parents=True, exist_ok=True)
            state["metadata"]["db_path"] = str(db_path)

        if self.config.enable_embeddings:
            state["metadata"]["embeddings_enabled"] = True
            state["metadata"]["embedding_model"] = "all-MiniLM-L6-v2"

        filepath = research_dir / "project-state.yaml"
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write("# Diverga Project State v8.0\n")
            f.write("# Auto-generated by setup wizard\n\n")
            yaml.dump(state, f, allow_unicode=True, default_flow_style=False)

    def _create_decision_log(self, research_dir: Path):
        """Create decision-log.yaml."""
        now = datetime.utcnow().isoformat() + "Z"

        log = {
            "version": "8.0",
            "project": self.config.project_name,
            "created": now,
            "last_updated": now,
            "decisions": []
        }

        filepath = research_dir / "decision-log.yaml"
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write("# Diverga Decision Log v8.0\n")
            f.write("# This file records all human decisions made during the research process\n")
            f.write("# Decisions are APPEND-ONLY and immutable\n\n")
            yaml.dump(log, f, allow_unicode=True, default_flow_style=False)

    def _create_checkpoints(self, research_dir: Path):
        """Create checkpoints.yaml."""
        checkpoints = {
            "version": "8.0",
            "checkpoints": {
                "CP_RESEARCH_DIRECTION": {"level": "required", "status": "pending"},
                "CP_PARADIGM_SELECTION": {"level": "required", "status": "passed"},
                "CP_THEORY_SELECTION": {"level": "required", "status": "pending"},
                "CP_METHODOLOGY_APPROVAL": {"level": "required", "status": "pending"},
            }
        }

        filepath = research_dir / "checkpoints.yaml"
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write("# Diverga Checkpoints v8.0\n")
            f.write("# Human-in-the-loop checkpoint states\n\n")
            yaml.dump(checkpoints, f, allow_unicode=True, default_flow_style=False)

    def _init_database(self):
        """Initialize SQLite database."""
        try:
            from ..database import MemoryDatabase

            db_path = Path.home() / ".diverga" / "memory.db"
            db_path.parent.mkdir(parents=True, exist_ok=True)

            # Initialize DB (creates schema)
            db = MemoryDatabase(str(db_path))
            print(f"  ✅ Database created at {db_path}")
        except Exception as e:
            print(f"  ⚠️ Database creation warning: {e}")

    def _install_embeddings(self):
        """Install sentence-transformers if needed."""
        try:
            import sentence_transformers
            print("  ✅ sentence-transformers already installed")
        except ImportError:
            print("  Installing sentence-transformers...")
            import subprocess
            result = subprocess.run(
                [sys.executable, "-m", "pip", "install", "sentence-transformers>=2.2"],
                capture_output=True,
                text=True
            )
            if result.returncode == 0:
                print("  ✅ sentence-transformers installed")
            else:
                print(f"  ⚠️ Installation warning: {result.stderr[:100]}")

    def _generate_docs(self):
        """Generate initial documentation."""
        try:
            from ..doc_generator import DocGenerator

            generator = DocGenerator(self.project_root)
            results = generator.generate_all()

            for doc, success in results.items():
                if success:
                    print(f"  ✅ Generated docs/{doc}")
        except Exception as e:
            print(f"  ⚠️ Doc generation warning: {e}")

    def _print_success(self):
        """Print success message and next steps."""
        print()
        print("✅ Project created successfully!")
        print()
        print("📁 Generated structure:")
        print(f"  {self.project_root.name}/")
        print("  ├── .research/                 ← System files (hidden)")
        print("  │   ├── project-state.yaml     ← Project metadata")
        print("  │   ├── decision-log.yaml      ← Decision history")
        print("  │   └── checkpoints.yaml       ← Checkpoint states")
        print("  │")
        print("  └── docs/                      ← Researcher-friendly docs")
        print("      ├── PROJECT_STATUS.md      ← Progress overview")
        print("      └── DECISION_LOG.md        ← Decision history")
        print()
        print("🚀 Ready to start! Try:")
        print("  - Ask about your research methodology")
        print("  - Record decisions with 'diverga decision add'")
        print("  - Check status with 'diverga status'")
        print()


def run_setup(args: List[str], project_root: Optional[Path] = None):
    """
    Run setup wizard.

    Args:
        args: Command-line arguments
        project_root: Project root directory
    """
    wizard = SetupWizard(project_root)

    if args:
        wizard.run_with_args(args)
    else:
        wizard.run_interactive()
