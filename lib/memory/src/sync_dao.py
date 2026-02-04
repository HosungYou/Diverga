"""
Diverga Memory System v8.0 - Sync Data Access Object

This module provides YAML → DB synchronization with idempotency.
Decisions are synced from decision-log.yaml to SQLite for search/indexing.

YAML remains the source of truth. DB is a read index.

Author: Diverga Project
Version: 8.0.0
"""

from __future__ import annotations

import yaml
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, Any, List, TYPE_CHECKING

if TYPE_CHECKING:
    from .database import MemoryDatabase


class SyncDAO:
    """
    Data Access Object for YAML → DB synchronization.

    Provides idempotent sync operations that:
    - Use external_id for duplicate detection
    - Track last_synced_decision_id in project-state.yaml
    - Never modify YAML (read-only source of truth)

    Attributes:
        db: MemoryDatabase instance
    """

    def __init__(self, db: "MemoryDatabase"):
        """
        Initialize SyncDAO with database connection.

        Args:
            db: MemoryDatabase instance for storage
        """
        self.db = db

    def sync_decisions(self, yaml_path: Path, project_root: Optional[Path] = None) -> Dict[str, Any]:
        """
        Sync decisions from decision-log.yaml to database.

        This operation is IDEMPOTENT - running multiple times
        produces the same result. Existing decisions are skipped.

        Args:
            yaml_path: Path to decision-log.yaml
            project_root: Project root directory (for marker update)

        Returns:
            Dict with sync results:
                - synced: Number of new decisions synced
                - skipped: Number of existing decisions skipped
                - errors: Number of sync errors
                - last_id: Last decision ID processed
        """
        if not yaml_path.exists():
            return {
                "synced": 0,
                "skipped": 0,
                "errors": 0,
                "last_id": None,
                "message": f"Decision log not found: {yaml_path}"
            }

        try:
            with open(yaml_path, 'r', encoding='utf-8') as f:
                log_data = yaml.safe_load(f) or {}
        except Exception as e:
            return {
                "synced": 0,
                "skipped": 0,
                "errors": 1,
                "last_id": None,
                "message": f"Failed to read decision log: {e}"
            }

        decisions = log_data.get('decisions', [])
        if not decisions:
            return {
                "synced": 0,
                "skipped": 0,
                "errors": 0,
                "last_id": None,
                "message": "No decisions to sync"
            }

        synced = 0
        skipped = 0
        errors = 0
        last_id = None

        for dec in decisions:
            decision_id = dec.get('id', '')
            if not decision_id:
                errors += 1
                continue

            last_id = decision_id

            # Check if already synced (idempotent)
            existing = self.db.get_memory_by_external_id(decision_id)
            if existing:
                skipped += 1
                continue

            try:
                # Build content from decision
                content = self._build_decision_content(dec)

                # Store in database
                self.db.store_memory(
                    memory_type='decision',
                    namespace=f"decisions.{dec.get('checkpoint', 'unknown')}",
                    title=dec.get('checkpoint', 'Unknown Checkpoint'),
                    content=content,
                    summary=dec.get('decision', {}).get('selected', ''),
                    priority=8,  # Decisions are high priority
                    session_id=dec.get('metadata', {}).get('session_id'),
                    project_name=log_data.get('project', ''),
                    tags=['decision', dec.get('checkpoint', ''), dec.get('stage', '')],
                    external_id=decision_id
                )
                synced += 1
            except Exception as e:
                print(f"Warning: Failed to sync decision {decision_id}: {e}")
                errors += 1

        # Update sync marker in project-state.yaml
        if project_root and last_id:
            self._update_sync_marker(project_root, last_id)

        return {
            "synced": synced,
            "skipped": skipped,
            "errors": errors,
            "last_id": last_id,
            "message": f"Synced {synced} decisions, skipped {skipped}, errors {errors}"
        }

    def sync_sessions(self, sessions_dir: Path) -> Dict[str, Any]:
        """
        Sync session records from .research/sessions/ to database.

        Args:
            sessions_dir: Path to sessions directory

        Returns:
            Dict with sync results
        """
        if not sessions_dir.exists() or not sessions_dir.is_dir():
            return {
                "synced": 0,
                "skipped": 0,
                "errors": 0,
                "message": "Sessions directory not found"
            }

        synced = 0
        skipped = 0
        errors = 0

        for session_file in sessions_dir.glob("*.yaml"):
            try:
                with open(session_file, 'r', encoding='utf-8') as f:
                    session_data = yaml.safe_load(f) or {}

                session_id = session_data.get('session_id', session_file.stem)

                # Check if already synced
                existing = self.db.get_memory_by_external_id(f"session_{session_id}")
                if existing:
                    skipped += 1
                    continue

                # Build session summary
                summary = session_data.get('summary', '')
                if not summary:
                    summary = self._build_session_summary(session_data)

                # Store session as memory
                self.db.store_memory(
                    memory_type='context',
                    namespace='sessions',
                    title=f"Session {session_id}",
                    content=summary,
                    summary=session_data.get('focus', ''),
                    session_id=session_id,
                    tags=['session'],
                    external_id=f"session_{session_id}"
                )

                # Also record in sessions table
                self.db.record_session(
                    session_id=session_id,
                    project_name=session_data.get('project_name'),
                    summary=summary,
                    agents_used=session_data.get('agents_used', [])
                )

                synced += 1
            except Exception as e:
                print(f"Warning: Failed to sync session {session_file}: {e}")
                errors += 1

        return {
            "synced": synced,
            "skipped": skipped,
            "errors": errors,
            "message": f"Synced {synced} sessions, skipped {skipped}, errors {errors}"
        }

    def get_sync_status(self, project_root: Path) -> Dict[str, Any]:
        """
        Get current synchronization status.

        Args:
            project_root: Project root directory

        Returns:
            Dict with sync status:
                - last_synced_decision_id: Last synced decision
                - pending_count: Decisions waiting to be synced
                - db_decision_count: Decisions in database
        """
        state_file = project_root / ".research" / "project-state.yaml"
        log_file = project_root / ".research" / "decision-log.yaml"

        last_synced = None
        if state_file.exists():
            try:
                with open(state_file, 'r', encoding='utf-8') as f:
                    state = yaml.safe_load(f) or {}
                    last_synced = state.get('metadata', {}).get('last_synced_decision_id')
            except Exception:
                pass

        yaml_decisions = []
        if log_file.exists():
            try:
                with open(log_file, 'r', encoding='utf-8') as f:
                    log_data = yaml.safe_load(f) or {}
                    yaml_decisions = log_data.get('decisions', [])
            except Exception:
                pass

        # Count pending (decisions after last_synced)
        pending_count = 0
        found_last = last_synced is None
        for dec in yaml_decisions:
            if found_last:
                pending_count += 1
            elif dec.get('id') == last_synced:
                found_last = True

        # Get DB stats
        db_stats = self.db.get_statistics()
        db_decision_count = db_stats.get('by_type', {}).get('decision', 0)

        return {
            "last_synced_decision_id": last_synced,
            "yaml_decision_count": len(yaml_decisions),
            "pending_count": pending_count,
            "db_decision_count": db_decision_count,
            "in_sync": pending_count == 0
        }

    def _build_decision_content(self, decision: Dict[str, Any]) -> str:
        """
        Build searchable content from decision dictionary.

        Args:
            decision: Decision dictionary from YAML

        Returns:
            Formatted content string
        """
        parts = []

        # Checkpoint info
        parts.append(f"Checkpoint: {decision.get('checkpoint', '')}")
        parts.append(f"Stage: {decision.get('stage', '')}")

        # Selected option
        selected = decision.get('decision', {}).get('selected', '')
        parts.append(f"Selected: {selected}")

        # Rationale
        rationale = decision.get('rationale', '')
        if rationale:
            parts.append(f"Rationale: {rationale}")

        # Alternatives
        alternatives = decision.get('decision', {}).get('alternatives', [])
        if alternatives:
            parts.append("Alternatives considered:")
            for alt in alternatives:
                if isinstance(alt, dict):
                    opt = alt.get('option', '')
                    reason = alt.get('rejection_reason', alt.get('reason', ''))
                    parts.append(f"  - {opt}: {reason}")
                else:
                    parts.append(f"  - {alt}")

        # Context
        context = decision.get('context', {})
        rq = context.get('research_question', '')
        if rq:
            parts.append(f"Research Question: {rq}")

        return "\n".join(parts)

    def _build_session_summary(self, session_data: Dict[str, Any]) -> str:
        """
        Build summary from session data.

        Args:
            session_data: Session dictionary from YAML

        Returns:
            Formatted summary string
        """
        parts = []

        if session_data.get('focus'):
            parts.append(f"Focus: {session_data['focus']}")

        if session_data.get('checkpoints_completed'):
            parts.append(f"Checkpoints: {', '.join(session_data['checkpoints_completed'])}")

        if session_data.get('decisions_made'):
            parts.append(f"Decisions: {len(session_data['decisions_made'])}")

        if session_data.get('agents_used'):
            parts.append(f"Agents: {', '.join(session_data['agents_used'])}")

        return " | ".join(parts) if parts else "No summary available"

    def _update_sync_marker(self, project_root: Path, last_id: str) -> None:
        """
        Update last_synced_decision_id in project-state.yaml.

        Args:
            project_root: Project root directory
            last_id: Last synced decision ID
        """
        state_file = project_root / ".research" / "project-state.yaml"

        try:
            state = {}
            if state_file.exists():
                with open(state_file, 'r', encoding='utf-8') as f:
                    state = yaml.safe_load(f) or {}

            # Update metadata
            if 'metadata' not in state:
                state['metadata'] = {}
            state['metadata']['last_synced_decision_id'] = last_id
            state['metadata']['last_sync_time'] = datetime.utcnow().isoformat() + "Z"

            # Ensure directory exists
            state_file.parent.mkdir(parents=True, exist_ok=True)

            with open(state_file, 'w', encoding='utf-8') as f:
                yaml.dump(state, f, allow_unicode=True, default_flow_style=False)
        except Exception as e:
            print(f"Warning: Failed to update sync marker: {e}")


def sync_project(project_root: Path, db: "MemoryDatabase") -> Dict[str, Any]:
    """
    Convenience function to sync entire project.

    Args:
        project_root: Project root directory
        db: MemoryDatabase instance

    Returns:
        Dict with combined sync results
    """
    sync = SyncDAO(db)

    # Sync decisions
    decision_log = project_root / ".research" / "decision-log.yaml"
    decision_result = sync.sync_decisions(decision_log, project_root)

    # Sync sessions
    sessions_dir = project_root / ".research" / "sessions"
    session_result = sync.sync_sessions(sessions_dir)

    return {
        "decisions": decision_result,
        "sessions": session_result,
        "total_synced": decision_result['synced'] + session_result['synced'],
        "total_skipped": decision_result['skipped'] + session_result['skipped'],
        "total_errors": decision_result['errors'] + session_result['errors']
    }
