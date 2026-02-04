"""
Diverga Memory System v8.0 - Document Generator

Auto-generates researcher-friendly Markdown documents from project data.
These documents provide human-readable views of the research state.

Generated Documents:
- docs/DECISION_LOG.md - Human-readable decision history
- docs/PROJECT_STATUS.md - Current project status
- docs/RESEARCH_AUDIT.md - Audit trail for IRB/reproducibility

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

    def generate_all(self) -> Dict[str, bool]:
        """
        Generate all documentation files.

        Returns:
            Dict mapping document name to success status
        """
        self.docs_dir.mkdir(exist_ok=True)

        results = {}

        # Generate each document
        results['DECISION_LOG.md'] = self.update_decision_log()
        results['PROJECT_STATUS.md'] = self.update_project_status()
        results['RESEARCH_AUDIT.md'] = self.update_audit_trail()

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
