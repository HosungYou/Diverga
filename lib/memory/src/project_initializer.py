"""
Diverga Memory System v8.0 - Project Initializer

Automatically initializes research project structure from detected intent.
Creates .research/ directory and initial state files.

Author: Diverga Project
Version: 8.0.0
"""

import os
import json
import yaml
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, Any

from .intent_detector import IntentResult, ResearchType
from .doc_generator import DocGenerator


def get_timestamp() -> str:
    """Get current UTC timestamp in ISO format."""
    return datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")


def sanitize_name(name: str) -> str:
    """Sanitize project name for filesystem use."""
    # Remove special characters
    name = name.replace('"', '').replace("'", '').replace('/', '-')
    # Replace spaces with hyphens
    name = '-'.join(name.split())
    # Truncate to reasonable length
    return name[:50]


def generate_project_name(intent: IntentResult) -> str:
    """Generate project name from intent."""
    if intent.topic:
        return sanitize_name(intent.topic)

    # Fallback names based on research type
    type_names = {
        ResearchType.SYSTEMATIC_REVIEW: "Systematic-Review",
        ResearchType.META_ANALYSIS: "Meta-Analysis",
        ResearchType.LITERATURE_REVIEW: "Literature-Review",
        ResearchType.EXPERIMENTAL: "Experimental-Study",
        ResearchType.QUALITATIVE: "Qualitative-Study",
        ResearchType.MIXED_METHODS: "Mixed-Methods-Study",
    }

    base_name = type_names.get(intent.research_type, "Research-Project")
    date_suffix = datetime.now().strftime("%Y%m%d")

    return f"{base_name}-{date_suffix}"


class ProjectInitializer:
    """
    Initializes Diverga research project structure.

    Creates:
    - .research/ directory
    - .research/project-state.yaml
    - .research/decision-log.yaml
    - .research/checkpoints.yaml
    - .research/hud-state.json
    - .research/baselines/
    - .research/changes/
    - .research/sessions/
    - docs/ directory with auto-generated documentation
    """

    # Standard checkpoint definitions
    CHECKPOINTS = [
        "CP_RESEARCH_DIRECTION",
        "CP_PARADIGM_SELECTION",
        "CP_SCOPE_DEFINITION",
        "CP_THEORY_SELECTION",
        "CP_VARIABLE_DEFINITION",
        "CP_METHODOLOGY_APPROVAL",
        "CP_DATABASE_SELECTION",
        "CP_SEARCH_STRATEGY",
        "CP_SAMPLE_PLANNING",
        "CP_SCREENING_CRITERIA",
        "CP_RAG_READINESS",
        "CP_DATA_EXTRACTION",
        "CP_ANALYSIS_PLAN",
        "CP_QUALITY_GATES",
        "CP_PEER_REVIEW",
        "CP_PUBLICATION_READY"
    ]

    def __init__(self, project_root: str = "."):
        """
        Initialize ProjectInitializer.

        Args:
            project_root: Root directory for the project (default: current directory)
        """
        self.project_root = Path(project_root).resolve()
        self.research_dir = self.project_root / ".research"

    def is_initialized(self) -> bool:
        """Check if project is already initialized."""
        return self.research_dir.exists() and (self.research_dir / "project-state.yaml").exists()

    def initialize(
        self,
        intent: Optional[IntentResult] = None,
        project_name: Optional[str] = None,
        research_question: Optional[str] = None,
        paradigm: Optional[str] = None,
        hud_enabled: bool = True
    ) -> Dict[str, Any]:
        """
        Initialize a new research project.

        Args:
            intent: Detected intent from user message
            project_name: Override project name
            research_question: Override research question
            paradigm: Override paradigm (quantitative, qualitative, mixed)
            hud_enabled: Whether to enable HUD

        Returns:
            Dict with initialization results
        """
        results = {
            "success": False,
            "project_root": str(self.project_root),
            "research_dir": str(self.research_dir),
            "created_files": [],
            "errors": []
        }

        # Derive values from intent if not provided
        if intent:
            if not project_name:
                project_name = generate_project_name(intent)
            if not research_question and intent.topic:
                research_question = f"Research on: {intent.topic}"
            if not paradigm:
                paradigm = intent.paradigm

        # Defaults
        project_name = project_name or "Untitled-Project"
        research_question = research_question or "Research question to be defined"
        paradigm = paradigm or "auto"

        try:
            # Create directory structure
            self._create_directories(results)

            # Create project state
            self._create_project_state(project_name, research_question, paradigm, results)

            # Create decision log
            self._create_decision_log(project_name, results)

            # Create checkpoints
            self._create_checkpoints(results)

            # Create HUD state
            if hud_enabled:
                self._create_hud_state(project_name, results)

            # Generate docs
            self._generate_docs(results)

            results["success"] = True

        except Exception as e:
            results["errors"].append(str(e))

        return results

    def _create_directories(self, results: Dict[str, Any]) -> None:
        """Create the .research/ directory structure."""
        directories = [
            self.research_dir,
            self.research_dir / "baselines" / "literature",
            self.research_dir / "baselines" / "methodology",
            self.research_dir / "baselines" / "framework",
            self.research_dir / "changes" / "current",
            self.research_dir / "changes" / "archive",
            self.research_dir / "sessions",
            self.project_root / "docs",
        ]

        for dir_path in directories:
            dir_path.mkdir(parents=True, exist_ok=True)
            results["created_files"].append(str(dir_path))

    def _create_project_state(
        self,
        project_name: str,
        research_question: str,
        paradigm: str,
        results: Dict[str, Any]
    ) -> None:
        """Create project-state.yaml."""
        state = {
            "version": "8.0.0",
            "project_name": project_name,
            "name": project_name,  # Alias
            "research_question": research_question,
            "paradigm": paradigm,
            "current_stage": "foundation",
            "created_at": get_timestamp(),
            "last_updated": get_timestamp(),
            "timeline": {
                "start_date": datetime.now().strftime("%Y-%m-%d"),
                "target_end": None,
                "milestones": []
            },
            "methodology": {
                "design": None,
                "data_collection": [],
                "analysis": []
            },
            "references": {
                "key_papers": [],
                "frameworks": []
            },
            "metadata": {}
        }

        state_path = self.research_dir / "project-state.yaml"
        with open(state_path, 'w', encoding='utf-8') as f:
            yaml.dump(state, f, allow_unicode=True, default_flow_style=False, sort_keys=False)

        results["created_files"].append(str(state_path))

    def _create_decision_log(self, project_name: str, results: Dict[str, Any]) -> None:
        """Create decision-log.yaml."""
        log = {
            "version": "8.0.0",
            "project": project_name,
            "created_at": get_timestamp(),
            "decisions": []
        }

        log_path = self.research_dir / "decision-log.yaml"
        with open(log_path, 'w', encoding='utf-8') as f:
            yaml.dump(log, f, allow_unicode=True, default_flow_style=False, sort_keys=False)

        results["created_files"].append(str(log_path))

    def _create_checkpoints(self, results: Dict[str, Any]) -> None:
        """Create checkpoints.yaml."""
        checkpoints = {
            "version": "8.0.0",
            "completed": [],
            "pending": self.CHECKPOINTS.copy(),
            "skipped": [],
            "details": {}
        }

        checkpoints_path = self.research_dir / "checkpoints.yaml"
        with open(checkpoints_path, 'w', encoding='utf-8') as f:
            yaml.dump(checkpoints, f, allow_unicode=True, default_flow_style=False, sort_keys=False)

        results["created_files"].append(str(checkpoints_path))

    def _create_hud_state(self, project_name: str, results: Dict[str, Any]) -> None:
        """Create hud-state.json."""
        hud_state = {
            "version": "1.0.0",
            "enabled": True,
            "preset": "research",
            "last_updated": get_timestamp(),
            "cache": {
                "project_name": project_name,
                "current_stage": "foundation",
                "checkpoints_completed": 0,
                "checkpoints_total": len(self.CHECKPOINTS),
                "memory_health": 100
            }
        }

        hud_path = self.research_dir / "hud-state.json"
        with open(hud_path, 'w', encoding='utf-8') as f:
            json.dump(hud_state, f, indent=2)

        results["created_files"].append(str(hud_path))

    def _generate_docs(self, results: Dict[str, Any]) -> None:
        """Generate docs/ documentation files."""
        try:
            generator = DocGenerator(self.project_root)
            doc_results = generator.generate_all()

            for filename, success in doc_results.items():
                if success:
                    results["created_files"].append(f"docs/{filename}")
                else:
                    results["errors"].append(f"Failed to generate docs/{filename}")

        except Exception as e:
            results["errors"].append(f"Docs generation error: {e}")


def initialize_from_intent(
    intent: IntentResult,
    project_root: str = "."
) -> Dict[str, Any]:
    """
    Convenience function to initialize project from detected intent.

    Args:
        intent: Detected research intent
        project_root: Root directory for the project

    Returns:
        Initialization results
    """
    initializer = ProjectInitializer(project_root)
    return initializer.initialize(intent=intent)


def initialize_project(
    project_name: str,
    research_question: str = "",
    paradigm: str = "auto",
    project_root: str = ".",
    hud_enabled: bool = True
) -> Dict[str, Any]:
    """
    Initialize a new research project with explicit parameters.

    Args:
        project_name: Name of the project
        research_question: Main research question
        paradigm: Research paradigm (quantitative, qualitative, mixed, auto)
        project_root: Root directory for the project
        hud_enabled: Whether to enable HUD

    Returns:
        Initialization results
    """
    initializer = ProjectInitializer(project_root)
    return initializer.initialize(
        project_name=project_name,
        research_question=research_question,
        paradigm=paradigm,
        hud_enabled=hud_enabled
    )


def is_project_initialized(project_root: str = ".") -> bool:
    """Check if a Diverga project is already initialized."""
    initializer = ProjectInitializer(project_root)
    return initializer.is_initialized()


def get_project_banner(project_root: str = ".") -> str:
    """
    Get project load banner for display.

    Returns formatted banner showing project status when loading an existing project.
    """
    research_dir = Path(project_root) / ".research"
    state_path = research_dir / "project-state.yaml"

    if not state_path.exists():
        return ""

    try:
        with open(state_path, 'r', encoding='utf-8') as f:
            state = yaml.safe_load(f) or {}

        project_name = state.get('project_name', state.get('name', 'Unknown'))
        stage = state.get('current_stage', 'foundation')
        last_updated = state.get('last_updated', 'Unknown')

        # Load checkpoints
        checkpoints_path = research_dir / "checkpoints.yaml"
        checkpoints_count = 0
        total_checkpoints = 16

        if checkpoints_path.exists():
            with open(checkpoints_path, 'r', encoding='utf-8') as f:
                checkpoints = yaml.safe_load(f) or {}
                completed = checkpoints.get('completed', [])
                checkpoints_count = len(completed)

        # Format timestamp
        try:
            dt = datetime.fromisoformat(last_updated.replace('Z', '+00:00'))
            time_str = dt.strftime("%Y-%m-%d")
        except:
            time_str = last_updated

        # Generate progress bar
        filled = int((checkpoints_count / total_checkpoints) * 11)
        progress = "●" * filled + "○" * (11 - filled)

        banner = f"""
┌─────────────────────────────────────────────────────────────────┐
│ ✅ 프로젝트 로드됨: {project_name:<44} │
├─────────────────────────────────────────────────────────────────┤
│ 🔬 Stage: {stage:<12} │ {progress} ({checkpoints_count}/{total_checkpoints}) │ 🧠 100%│
│                                                                 │
│ 마지막 세션: {time_str:<50} │
└─────────────────────────────────────────────────────────────────┘
""".strip()

        return banner

    except Exception as e:
        return f"Error loading project: {e}"


if __name__ == "__main__":
    # Test initialization
    from intent_detector import detect_intent

    test_msg = "I want to conduct a systematic review on AI in education"
    intent = detect_intent(test_msg)

    print("Test Intent Detection:")
    print(f"  Type: {intent.research_type.value}")
    print(f"  Topic: {intent.topic}")
    print(f"  Paradigm: {intent.paradigm}")

    # Don't actually initialize in test
    print("\nProject initialization would create:")
    print("  .research/project-state.yaml")
    print("  .research/decision-log.yaml")
    print("  .research/checkpoints.yaml")
    print("  .research/hud-state.json")
    print("  .research/baselines/")
    print("  .research/changes/")
    print("  .research/sessions/")
    print("  docs/PROJECT_STATUS.md")
    print("  docs/DECISION_LOG.md")
    print("  docs/METHODOLOGY.md")
    print("  docs/TIMELINE.md")
    print("  docs/REFERENCES.md")
    print("  docs/RESEARCH_AUDIT.md")
    print("  docs/README.md")
