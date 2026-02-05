"""
Diverga Memory System v8.0 - Document Generator

Auto-generates researcher-friendly Markdown documents from project data.
These documents provide human-readable views of the research state.

Generated Documents (v8.0 Extended):
- docs/PROJECT_STATUS.md   - Progress tracking (auto-generated)
- docs/DECISION_LOG.md     - Decision audit trail (auto-generated)
- docs/RESEARCH_AUDIT.md   - IRB/reproducibility audit (auto-generated)
- docs/METHODOLOGY.md      - Research methodology summary (auto-generated)
- docs/TIMELINE.md         - Research timeline and milestones (auto-generated)
- docs/REFERENCES.md       - Key references (auto-generated)
- docs/README.md           - Project overview (editable by researcher)

Author: Diverga Project
Version: 8.0.0
"""

from __future__ import annotations

import yaml
from datetime import datetime
from pathlib import Path
from typing import Optional, List, Dict, Any, TYPE_CHECKING

if TYPE_CHECKING:
    from .decision_log import DecisionLog
    from .fs_state import FilesystemState


# Stage definitions for progress display
STAGES = {
    "foundation": {"order": 1, "name": "Foundation", "checkpoints": ["CP_RESEARCH_DIRECTION", "CP_PARADIGM_SELECTION", "CP_SCOPE_DEFINITION"]},
    "theory": {"order": 2, "name": "Theory", "checkpoints": ["CP_THEORY_SELECTION", "CP_VARIABLE_DEFINITION"]},
    "methodology": {"order": 3, "name": "Methodology", "checkpoints": ["CP_METHODOLOGY_APPROVAL"]},
    "design": {"order": 4, "name": "Design", "checkpoints": ["CP_DATABASE_SELECTION", "CP_SEARCH_STRATEGY", "CP_SAMPLE_PLANNING"]},
    "execution": {"order": 5, "name": "Execution", "checkpoints": ["CP_SCREENING_CRITERIA", "CP_RAG_READINESS", "CP_DATA_EXTRACTION"]},
    "analysis": {"order": 6, "name": "Analysis", "checkpoints": ["CP_ANALYSIS_PLAN"]},
    "validation": {"order": 7, "name": "Validation", "checkpoints": ["CP_QUALITY_GATES", "CP_PEER_REVIEW", "CP_PUBLICATION_READY"]}
}


class DocGenerator:
    """
    Auto-generate researcher-friendly Markdown documents.

    These documents are intended for:
    - Human review of project state
    - IRB compliance documentation
    - Reproducibility audits
    - Team collaboration

    Attributes:
        project_root: Root directory of the research project
        docs_dir: Directory for generated documents
    """

    def __init__(self, project_root: Path):
        """
        Initialize DocGenerator with project root.

        Args:
            project_root: Root directory of the research project
        """
        self.project_root = Path(project_root)
        self.docs_dir = self.project_root / "docs"

    def _format_timestamp(self, ts: Optional[str] = None) -> str:
        """Format timestamp for display."""
        if ts:
            try:
                dt = datetime.fromisoformat(ts.replace('Z', '+00:00'))
                return dt.strftime("%Y-%m-%d %H:%M")
            except:
                return ts
        return datetime.now().strftime("%Y-%m-%d %H:%M")

    def _get_progress_bar(self, completed: int, total: int, width: int = 11) -> str:
        """Generate progress bar string."""
        filled = int((completed / total) * width) if total > 0 else 0
        return "●" * filled + "○" * (width - filled)

    def generate_all(self) -> Dict[str, bool]:
        """
        Generate all documentation files (v8.0 extended - 7 files).

        Returns:
            Dict mapping document name to success status
        """
        self.docs_dir.mkdir(exist_ok=True)

        results = {}

        # Generate each document (v8.0 extended set)
        results['PROJECT_STATUS.md'] = self.update_project_status()
        results['DECISION_LOG.md'] = self.update_decision_log()
        results['RESEARCH_AUDIT.md'] = self.update_audit_trail()
        results['METHODOLOGY.md'] = self.update_methodology()
        results['TIMELINE.md'] = self.update_timeline()
        results['REFERENCES.md'] = self.update_references()
        results['README.md'] = self.update_readme(overwrite=False)

        return results

    def update_decision_log(self, decision_log: Optional["DecisionLog"] = None) -> bool:
        """
        Generate/update DECISION_LOG.md from decision-log.yaml.

        Args:
            decision_log: Optional DecisionLog instance

        Returns:
            True if successful
        """
        try:
            # Load decision log
            log_file = self.project_root / ".research" / "decision-log.yaml"
            if not log_file.exists():
                return False

            with open(log_file, 'r', encoding='utf-8') as f:
                log_data = yaml.safe_load(f) or {}

            decisions = log_data.get('decisions', [])
            project_name = log_data.get('project', 'Unknown Project')

            # Generate Markdown
            md = self._render_decision_log_md(decisions, project_name)

            # Write file
            self.docs_dir.mkdir(exist_ok=True)
            output_file = self.docs_dir / "DECISION_LOG.md"
            output_file.write_text(md, encoding='utf-8')

            return True
        except Exception as e:
            print(f"Error generating DECISION_LOG.md: {e}")
            return False

    def update_project_status(self, fs_state: Optional["FilesystemState"] = None) -> bool:
        """
        Generate/update PROJECT_STATUS.md from project-state.yaml.

        Args:
            fs_state: Optional FilesystemState instance

        Returns:
            True if successful
        """
        try:
            # Load project state
            state_file = self.project_root / ".research" / "project-state.yaml"
            if not state_file.exists():
                return False

            with open(state_file, 'r', encoding='utf-8') as f:
                state = yaml.safe_load(f) or {}

            # Generate Markdown
            md = self._render_status_md(state)

            # Write file
            self.docs_dir.mkdir(exist_ok=True)
            output_file = self.docs_dir / "PROJECT_STATUS.md"
            output_file.write_text(md, encoding='utf-8')

            return True
        except Exception as e:
            print(f"Error generating PROJECT_STATUS.md: {e}")
            return False

    def update_audit_trail(self, sync_result: Optional[Dict] = None) -> bool:
        """
        Generate/update RESEARCH_AUDIT.md for reproducibility.

        Args:
            sync_result: Optional sync result to include

        Returns:
            True if successful
        """
        try:
            # Load project state
            state_file = self.project_root / ".research" / "project-state.yaml"
            log_file = self.project_root / ".research" / "decision-log.yaml"

            state = {}
            if state_file.exists():
                with open(state_file, 'r', encoding='utf-8') as f:
                    state = yaml.safe_load(f) or {}

            decisions = []
            if log_file.exists():
                with open(log_file, 'r', encoding='utf-8') as f:
                    log_data = yaml.safe_load(f) or {}
                    decisions = log_data.get('decisions', [])

            # Generate Markdown
            md = self._render_audit_md(state, decisions, sync_result)

            # Write file
            self.docs_dir.mkdir(exist_ok=True)
            output_file = self.docs_dir / "RESEARCH_AUDIT.md"
            output_file.write_text(md, encoding='utf-8')

            return True
        except Exception as e:
            print(f"Error generating RESEARCH_AUDIT.md: {e}")
            return False

    def _render_decision_log_md(self, decisions: List[Dict], project_name: str) -> str:
        """
        Render decision log as Markdown.

        Args:
            decisions: List of decision dictionaries
            project_name: Project name

        Returns:
            Markdown string
        """
        now = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")

        lines = [
            "# Research Decision Log",
            "",
            f"**Project**: {project_name}",
            f"**Last Updated**: {now}",
            "",
            "---",
            ""
        ]

        if not decisions:
            lines.append("*No decisions recorded yet.*")
        else:
            for dec in decisions:
                dec_id = dec.get('id', 'unknown')
                timestamp = dec.get('timestamp', '')[:10]  # Date only
                checkpoint = dec.get('checkpoint', 'Unknown')
                selected = dec.get('decision', {}).get('selected', '')
                rationale = dec.get('rationale', '')
                alternatives = dec.get('decision', {}).get('alternatives', [])
                is_amendment = dec.get('metadata', {}).get('is_amendment', False)

                # Decision header
                if is_amendment:
                    amends = dec.get('amends', '')
                    lines.append(f"## {dec_id}: {checkpoint} (Amendment of {amends}) ({timestamp})")
                else:
                    lines.append(f"## {dec_id}: {checkpoint} ({timestamp})")

                lines.append("")
                lines.append(f"**Checkpoint**: {checkpoint}")
                lines.append(f"**Selected**: {selected}")
                lines.append("")

                # Rationale
                if rationale:
                    lines.append("### Rationale")
                    lines.append(rationale)
                    lines.append("")

                # Alternatives
                if alternatives:
                    lines.append("### Alternatives Considered")
                    lines.append("")
                    lines.append("| Option | Rejection Reason |")
                    lines.append("|--------|------------------|")
                    for alt in alternatives:
                        if isinstance(alt, dict):
                            opt = alt.get('option', '')
                            reason = alt.get('rejection_reason', alt.get('reason', 'N/A'))
                            lines.append(f"| {opt} | {reason} |")
                        else:
                            lines.append(f"| {alt} | N/A |")
                    lines.append("")

                lines.append("---")
                lines.append("")

        return "\n".join(lines)

    def _render_status_md(self, state: Dict) -> str:
        """
        Render project status as Markdown.

        Args:
            state: Project state dictionary

        Returns:
            Markdown string
        """
        now = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")

        project_name = state.get('project_name', 'Unknown Project')
        research_question = state.get('research_question', 'Not defined')
        paradigm = state.get('paradigm', 'Not set')
        current_stage = state.get('current_stage', 'foundation')
        last_updated = state.get('last_updated', 'Unknown')

        # Stage progress indicator
        stages = ['foundation', 'evidence', 'design', 'data', 'analysis', 'synthesis', 'publication']
        try:
            stage_idx = stages.index(current_stage)
            progress = "●" * (stage_idx + 1) + "○" * (len(stages) - stage_idx - 1)
        except ValueError:
            progress = "?" * len(stages)

        lines = [
            "# Project Status",
            "",
            f"**Generated**: {now}",
            "",
            "---",
            "",
            "## Overview",
            "",
            f"- **Project**: {project_name}",
            f"- **Research Question**: {research_question}",
            f"- **Paradigm**: {paradigm}",
            f"- **Current Stage**: {current_stage}",
            f"- **Last Updated**: {last_updated}",
            "",
            "## Progress",
            "",
            f"```",
            f"[{progress}] Stage: {current_stage}",
            f"```",
            "",
            "### Stage Legend",
            "",
            "| Stage | Description |",
            "|-------|-------------|",
            "| foundation | Research question, theoretical framework |",
            "| evidence | Literature review, evidence synthesis |",
            "| design | Methodology, sampling, instruments |",
            "| data | Data collection |",
            "| analysis | Data analysis |",
            "| synthesis | Results integration, interpretation |",
            "| publication | Writing, peer review, publication |",
            ""
        ]

        # Metadata section
        metadata = state.get('metadata', {})
        if metadata:
            lines.extend([
                "## Metadata",
                ""
            ])
            for key, value in metadata.items():
                lines.append(f"- **{key}**: {value}")
            lines.append("")

        return "\n".join(lines)

    def _render_audit_md(self, state: Dict, decisions: List[Dict],
                          sync_result: Optional[Dict] = None) -> str:
        """
        Render audit trail as Markdown.

        Args:
            state: Project state dictionary
            decisions: List of decisions
            sync_result: Optional sync result

        Returns:
            Markdown string
        """
        now = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")

        project_name = state.get('project_name', 'Unknown Project')

        lines = [
            "# Research Audit Trail",
            "",
            f"**Project**: {project_name}",
            f"**Generated**: {now}",
            "",
            "---",
            "",
            "## Purpose",
            "",
            "This document provides an audit trail for research reproducibility,",
            "IRB compliance, and transparent decision documentation.",
            "",
            "## Decision Summary",
            "",
            f"- **Total Decisions**: {len(decisions)}",
        ]

        # Count by checkpoint
        checkpoint_counts: Dict[str, int] = {}
        for dec in decisions:
            cp = dec.get('checkpoint', 'unknown')
            checkpoint_counts[cp] = checkpoint_counts.get(cp, 0) + 1

        if checkpoint_counts:
            lines.extend([
                "",
                "### Decisions by Checkpoint",
                "",
                "| Checkpoint | Count |",
                "|------------|-------|"
            ])
            for cp, count in sorted(checkpoint_counts.items()):
                lines.append(f"| {cp} | {count} |")
            lines.append("")

        # Amendment summary
        amendments = [d for d in decisions if d.get('metadata', {}).get('is_amendment')]
        lines.extend([
            "### Amendments",
            "",
            f"- **Total Amendments**: {len(amendments)}",
            ""
        ])

        if amendments:
            lines.extend([
                "| Amendment ID | Original ID | Timestamp |",
                "|--------------|-------------|-----------|"
            ])
            for a in amendments:
                lines.append(f"| {a.get('id')} | {a.get('amends')} | {a.get('timestamp', '')[:10]} |")
            lines.append("")

        # Sync status
        if sync_result:
            lines.extend([
                "## Database Sync",
                "",
                f"- **Synced**: {sync_result.get('synced', 0)}",
                f"- **Skipped**: {sync_result.get('skipped', 0)}",
                f"- **Errors**: {sync_result.get('errors', 0)}",
                f"- **Last ID**: {sync_result.get('last_id', 'N/A')}",
                ""
            ])

        # Timeline
        if decisions:
            lines.extend([
                "## Timeline",
                "",
                "```mermaid",
                "timeline",
                f"    title Research Decision Timeline - {project_name}"
            ])

            # Group by date
            by_date: Dict[str, List[str]] = {}
            for dec in decisions:
                date = dec.get('timestamp', '')[:10]
                cp = dec.get('checkpoint', 'unknown')
                if date not in by_date:
                    by_date[date] = []
                by_date[date].append(cp)

            for date in sorted(by_date.keys()):
                checkpoints = by_date[date]
                lines.append(f"    {date} : {', '.join(checkpoints)}")

            lines.extend([
                "```",
                ""
            ])

        # Footer
        lines.extend([
            "---",
            "",
            "*This audit trail is auto-generated by Diverga Memory System v8.0.*",
            "*For research reproducibility and transparency.*"
        ])

        return "\n".join(lines)


    def update_methodology(self) -> bool:
        """
        Generate/update METHODOLOGY.md from project-state.yaml.

        Returns:
            True if successful
        """
        try:
            # Load project state
            state_file = self.project_root / ".research" / "project-state.yaml"
            log_file = self.project_root / ".research" / "decision-log.yaml"

            state = {}
            if state_file.exists():
                with open(state_file, 'r', encoding='utf-8') as f:
                    state = yaml.safe_load(f) or {}

            decisions = []
            if log_file.exists():
                with open(log_file, 'r', encoding='utf-8') as f:
                    log_data = yaml.safe_load(f) or {}
                    decisions = log_data.get('decisions', [])

            md = self._render_methodology_md(state, decisions)

            self.docs_dir.mkdir(exist_ok=True)
            output_file = self.docs_dir / "METHODOLOGY.md"
            output_file.write_text(md, encoding='utf-8')

            return True
        except Exception as e:
            print(f"Error generating METHODOLOGY.md: {e}")
            return False

    def update_timeline(self) -> bool:
        """
        Generate/update TIMELINE.md from project-state.yaml.

        Returns:
            True if successful
        """
        try:
            state_file = self.project_root / ".research" / "project-state.yaml"
            checkpoints_file = self.project_root / ".research" / "checkpoints.yaml"

            state = {}
            if state_file.exists():
                with open(state_file, 'r', encoding='utf-8') as f:
                    state = yaml.safe_load(f) or {}

            checkpoints = {}
            if checkpoints_file.exists():
                with open(checkpoints_file, 'r', encoding='utf-8') as f:
                    checkpoints = yaml.safe_load(f) or {}

            md = self._render_timeline_md(state, checkpoints)

            self.docs_dir.mkdir(exist_ok=True)
            output_file = self.docs_dir / "TIMELINE.md"
            output_file.write_text(md, encoding='utf-8')

            return True
        except Exception as e:
            print(f"Error generating TIMELINE.md: {e}")
            return False

    def update_references(self) -> bool:
        """
        Generate/update REFERENCES.md from project-state.yaml.

        Returns:
            True if successful
        """
        try:
            state_file = self.project_root / ".research" / "project-state.yaml"

            state = {}
            if state_file.exists():
                with open(state_file, 'r', encoding='utf-8') as f:
                    state = yaml.safe_load(f) or {}

            md = self._render_references_md(state)

            self.docs_dir.mkdir(exist_ok=True)
            output_file = self.docs_dir / "REFERENCES.md"
            output_file.write_text(md, encoding='utf-8')

            return True
        except Exception as e:
            print(f"Error generating REFERENCES.md: {e}")
            return False

    def update_readme(self, overwrite: bool = False) -> bool:
        """
        Generate/update README.md (editable by researcher).

        Only creates if doesn't exist or overwrite=True.

        Args:
            overwrite: Force overwrite existing README

        Returns:
            True if successful
        """
        try:
            output_file = self.docs_dir / "README.md"

            # Don't overwrite existing README unless explicitly requested
            if output_file.exists() and not overwrite:
                return True

            state_file = self.project_root / ".research" / "project-state.yaml"

            state = {}
            if state_file.exists():
                with open(state_file, 'r', encoding='utf-8') as f:
                    state = yaml.safe_load(f) or {}

            md = self._render_readme_md(state)

            self.docs_dir.mkdir(exist_ok=True)
            output_file.write_text(md, encoding='utf-8')

            return True
        except Exception as e:
            print(f"Error generating README.md: {e}")
            return False

    def _render_methodology_md(self, state: Dict, decisions: List[Dict]) -> str:
        """Render METHODOLOGY.md content."""
        now = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")

        paradigm = state.get('paradigm', 'Not selected')
        methodology = state.get('methodology', {})

        # Paradigm descriptions
        paradigm_desc = {
            "quantitative": "This research follows a quantitative paradigm, emphasizing objective measurement, statistical analysis, and hypothesis testing.",
            "qualitative": "This research follows a qualitative paradigm, emphasizing interpretive understanding, rich description, and contextual analysis.",
            "mixed": "This research employs a mixed methods approach, integrating both quantitative and qualitative data collection and analysis."
        }

        lines = [
            "# Research Methodology",
            "",
            f"> **Auto-generated** from `.research/project-state.yaml`",
            f"> Last updated: {now}",
            "",
            "## Research Paradigm",
            "",
            f"**Selected Paradigm**: {paradigm}",
            "",
            paradigm_desc.get(paradigm.lower(), "_Paradigm description not available._"),
            "",
        ]

        # Design section
        design = methodology.get('design', 'Not specified')
        lines.extend([
            "## Research Design",
            "",
            f"**Design Type**: {design}",
            "",
        ])

        # Method decisions from log
        method_decisions = [d for d in decisions if any(x in d.get('checkpoint', '') for x in ['METHODOLOGY', 'DESIGN', 'SAMPLE', 'PARADIGM'])]

        if method_decisions:
            lines.extend([
                "### Key Methodological Decisions",
                "",
            ])
            for d in method_decisions:
                checkpoint = d.get('checkpoint', 'Unknown')
                selected = d.get('decision', {}).get('selected', d.get('selected', 'Unknown'))
                lines.append(f"- **{checkpoint}**: {selected}")
            lines.append("")

        # Data collection
        data_collection = methodology.get('data_collection', [])
        if data_collection:
            lines.extend([
                "## Data Collection",
                "",
            ])
            for method in data_collection:
                lines.append(f"- {method}")
            lines.append("")

        # Analysis plan
        analysis = methodology.get('analysis', [])
        if analysis:
            lines.extend([
                "## Analysis Plan",
                "",
            ])
            for method in analysis:
                lines.append(f"- {method}")
            lines.append("")

        lines.extend([
            "---",
            "",
            "*This file is auto-generated. Do not edit directly.*"
        ])

        return "\n".join(lines)

    def _render_timeline_md(self, state: Dict, checkpoints: Dict) -> str:
        """Render TIMELINE.md content."""
        now = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")

        timeline = state.get('timeline', {})
        milestones = timeline.get('milestones', [])

        lines = [
            "# Research Timeline",
            "",
            f"> **Auto-generated** from `.research/project-state.yaml`",
            f"> Last updated: {now}",
            "",
            "## Project Timeline",
            "",
            "| Field | Date |",
            "|-------|------|",
            f"| Start Date | {timeline.get('start_date', 'Not set')} |",
            f"| Target End | {timeline.get('target_end', 'Not set')} |",
            f"| Current Phase | {state.get('current_stage', 'foundation').title()} |",
            "",
            "## Milestones",
            "",
        ]

        if milestones:
            lines.extend([
                "| Milestone | Target Date | Status |",
                "|-----------|-------------|--------|",
            ])
            for m in milestones:
                name = m.get('name', 'Unnamed')
                target = m.get('target_date', 'TBD')
                status = "✅" if m.get('completed') else "⬜"
                lines.append(f"| {name} | {target} | {status} |")
        else:
            lines.append("_No milestones defined yet._")

        lines.append("")

        # Checkpoint progress timeline
        lines.extend([
            "## Checkpoint Progress Timeline",
            "",
        ])

        completed = checkpoints.get('completed', [])
        details = checkpoints.get('details', {})

        if completed:
            lines.extend([
                "| Checkpoint | Completed |",
                "|------------|----------|",
            ])
            for cp in completed:
                cp_detail = details.get(cp, {})
                completed_at = self._format_timestamp(cp_detail.get('completed_at'))
                lines.append(f"| {cp} | {completed_at} |")
        else:
            lines.append("_No checkpoints completed yet._")

        lines.extend([
            "",
            "---",
            "",
            "*This file is auto-generated. Do not edit directly.*"
        ])

        return "\n".join(lines)

    def _render_references_md(self, state: Dict) -> str:
        """Render REFERENCES.md content."""
        now = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")

        references = state.get('references', {})
        key_papers = references.get('key_papers', [])
        frameworks = references.get('frameworks', [])

        lines = [
            "# Key References",
            "",
            f"> **Auto-generated** from `.research/project-state.yaml`",
            f"> Last updated: {now}",
            "",
            "## Key Papers",
            "",
        ]

        if key_papers:
            for i, paper in enumerate(key_papers, 1):
                if isinstance(paper, dict):
                    authors = paper.get('authors', 'Unknown')
                    year = paper.get('year', 'n.d.')
                    title = paper.get('title', 'Untitled')
                    source = paper.get('source', '')
                    lines.append(f"{i}. {authors} ({year}). *{title}*. {source}")
                    lines.append("")
                else:
                    lines.append(f"{i}. {paper}")
                    lines.append("")
        else:
            lines.append("_No key papers recorded yet._")
            lines.append("")

        lines.extend([
            "## Theoretical Frameworks",
            "",
        ])

        if frameworks:
            for framework in frameworks:
                if isinstance(framework, dict):
                    name = framework.get('name', 'Unknown')
                    description = framework.get('description', '')
                    lines.extend([
                        f"### {name}",
                        "",
                        description,
                        "",
                    ])
                else:
                    lines.append(f"- {framework}")
        else:
            lines.append("_No frameworks documented yet._")

        lines.extend([
            "",
            "## How to Add References",
            "",
            "Add references to `.research/project-state.yaml`:",
            "",
            "```yaml",
            "references:",
            "  key_papers:",
            '    - authors: "Smith, J. & Jones, M."',
            "      year: 2023",
            '      title: "Research Paper Title"',
            '      source: "Journal Name, 10(2), 100-120"',
            "  frameworks:",
            '    - name: "Framework Name"',
            '      description: "Brief description of the framework"',
            "```",
            "",
            "---",
            "",
            "*This file is auto-generated. Do not edit directly.*"
        ])

        return "\n".join(lines)

    def _render_readme_md(self, state: Dict) -> str:
        """Render README.md content (editable template)."""
        project_name = state.get('project_name', state.get('name', 'Untitled Project'))
        research_question = state.get('research_question', 'Not defined')

        lines = [
            f"# {project_name}",
            "",
            "## Research Question",
            "",
            research_question,
            "",
            "## Overview",
            "",
            "_Add your project overview here._",
            "",
            "## Getting Started",
            "",
            "This project uses Diverga v8.0 for research project management.",
            "",
            "### Quick Status",
            "",
            "See [PROJECT_STATUS.md](PROJECT_STATUS.md) for current progress.",
            "",
            "### Key Documents",
            "",
            "| Document | Description |",
            "|----------|-------------|",
            "| [PROJECT_STATUS.md](PROJECT_STATUS.md) | Progress tracking (auto-generated) |",
            "| [DECISION_LOG.md](DECISION_LOG.md) | Decision audit trail (auto-generated) |",
            "| [METHODOLOGY.md](METHODOLOGY.md) | Research methodology (auto-generated) |",
            "| [TIMELINE.md](TIMELINE.md) | Timeline and milestones (auto-generated) |",
            "| [REFERENCES.md](REFERENCES.md) | Key references (auto-generated) |",
            "| [RESEARCH_AUDIT.md](RESEARCH_AUDIT.md) | IRB/reproducibility audit (auto-generated) |",
            "",
            "## Notes",
            "",
            "_Add your notes here._",
            "",
            "---",
            "",
            "_Generated by Diverga v8.0_"
        ]

        return "\n".join(lines)


def generate_docs(project_root: Path) -> Dict[str, bool]:
    """
    Convenience function to generate all docs.

    Args:
        project_root: Project root directory

    Returns:
        Dict mapping document name to success status
    """
    generator = DocGenerator(project_root)
    return generator.generate_all()


def sync_docs(project_root: str = ".") -> Dict[str, bool]:
    """
    Sync all documentation files (alias for generate_docs).

    Args:
        project_root: Project root directory

    Returns:
        Dict mapping document name to success status
    """
    generator = DocGenerator(Path(project_root))
    return generator.generate_all()


def sync_project_status(project_root: str = ".") -> bool:
    """Sync PROJECT_STATUS.md only."""
    generator = DocGenerator(Path(project_root))
    return generator.update_project_status()


def sync_decision_log(project_root: str = ".") -> bool:
    """Sync DECISION_LOG.md only."""
    generator = DocGenerator(Path(project_root))
    return generator.update_decision_log()
