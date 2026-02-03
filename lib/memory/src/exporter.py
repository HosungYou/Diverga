"""
Memory Export System for Diverga Memory.

Supports multiple export formats:
- Markdown (human-readable)
- JSON (machine-readable)
- YAML (config-friendly)

Provides filtering by date range, type, namespace, and more.
"""

import json
import yaml
from datetime import datetime
from pathlib import Path
from typing import Optional, List, Dict, Any
from dataclasses import asdict

try:
    from .schema import Memory, Decision, Session, MemoryType, DecisionType, Priority
    from .database import MemoryDatabase
except ImportError:
    from schema import Memory, Decision, Session, MemoryType, DecisionType, Priority
    from database import MemoryDatabase


class MemoryExporter:
    """
    Export memories to various formats with filtering capabilities.

    Supports:
    - Markdown (human-readable research notes)
    - JSON (machine-readable, full schema)
    - YAML (config-friendly, compact)

    Usage:
        exporter = MemoryExporter(db_path=".diverga/memory/memories.db")

        # Export all memories to Markdown
        path = exporter.export_markdown(
            output_path="./exports/memories.md"
        )

        # Export filtered memories to JSON
        path = exporter.export_json(
            output_path="./exports/decisions.json",
            memory_type=MemoryType.DECISION,
            start_date=datetime(2026, 1, 1)
        )
    """

    def __init__(self, db_path: str):
        """
        Initialize exporter with database connection.

        Args:
            db_path: Path to SQLite database file
        """
        self.db = MemoryDatabase(db_path)

    def _fetch_memories(
        self,
        memory_type: Optional[MemoryType] = None,
        namespace: Optional[str] = None,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        priority: Optional[Priority] = None,
        tags: Optional[List[str]] = None
    ) -> List[Dict[str, Any]]:
        """
        Fetch memories with filtering.

        Args:
            memory_type: Filter by memory type
            namespace: Filter by namespace (supports wildcards)
            start_date: Filter memories after this date
            end_date: Filter memories before this date
            priority: Filter by priority level
            tags: Filter by tags (ANY match)

        Returns:
            List of memory dictionaries
        """
        with self.db._get_connection() as conn:
            cursor = conn.cursor()

            # Build query
            query = "SELECT * FROM memories WHERE status = 'active'"
            params = []

            if memory_type:
                query += " AND memory_type = ?"
                params.append(memory_type.value if isinstance(memory_type, MemoryType) else memory_type)

            if namespace:
                if "%" in namespace or "_" in namespace:
                    query += " AND namespace LIKE ?"
                else:
                    query += " AND (namespace = ? OR namespace LIKE ?)"
                    params.extend([namespace, f"{namespace}.%"])

            if start_date:
                query += " AND created_at >= ?"
                params.append(start_date.isoformat())

            if end_date:
                query += " AND created_at <= ?"
                params.append(end_date.isoformat())

            if priority:
                priority_value = priority.value if isinstance(priority, Priority) else priority
                # Map priority to numeric value (1=critical, 10=low)
                priority_map = {"critical": 1, "high": 3, "medium": 5, "low": 8}
                if priority_value in priority_map:
                    query += " AND priority <= ?"
                    params.append(priority_map[priority_value])

            if tags:
                # Tags stored as JSON array
                tag_conditions = " OR ".join(["json_extract(tags, '$') LIKE ?" for _ in tags])
                query += f" AND ({tag_conditions})"
                params.extend([f'%"{tag}"%' for tag in tags])

            query += " ORDER BY created_at DESC"

            cursor.execute(query, params)
            rows = cursor.fetchall()

            # Convert to dictionaries
            memories = []
            for row in rows:
                memory_dict = dict(row)
                # Parse JSON fields
                tags_val = memory_dict.get('tags')
                memory_dict['tags'] = json.loads(tags_val) if tags_val else []
                metadata_val = memory_dict.get('metadata')
                memory_dict['metadata'] = json.loads(metadata_val) if metadata_val else {}
                memories.append(memory_dict)

            return memories

    def _fetch_decisions(
        self,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> List[Dict[str, Any]]:
        """Fetch decision records."""
        with self.db._get_connection() as conn:
            cursor = conn.cursor()

            query = "SELECT * FROM decisions"
            params = []

            if start_date or end_date:
                query += " WHERE"
                if start_date:
                    query += " created_at >= ?"
                    params.append(start_date.isoformat())
                if end_date:
                    if start_date:
                        query += " AND"
                    query += " created_at <= ?"
                    params.append(end_date.isoformat())

            query += " ORDER BY created_at DESC"

            cursor.execute(query, params)
            rows = cursor.fetchall()

            decisions = []
            for row in rows:
                decision_dict = dict(row)
                decision_dict['metadata'] = json.loads(decision_dict.get('metadata', '{}'))
                decisions.append(decision_dict)

            return decisions

    def _fetch_sessions(
        self,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> List[Dict[str, Any]]:
        """Fetch session records."""
        with self.db._get_connection() as conn:
            cursor = conn.cursor()

            query = "SELECT * FROM sessions"
            params = []

            if start_date or end_date:
                query += " WHERE"
                if start_date:
                    query += " started_at >= ?"
                    params.append(start_date.isoformat())
                if end_date:
                    if start_date:
                        query += " AND"
                    query += " started_at <= ?"
                    params.append(end_date.isoformat())

            query += " ORDER BY started_at DESC"

            cursor.execute(query, params)
            rows = cursor.fetchall()

            sessions = []
            for row in rows:
                session_dict = dict(row)
                session_dict['agents_used'] = json.loads(session_dict.get('agents_used', '[]'))
                session_dict['decisions'] = json.loads(session_dict.get('decisions', '[]'))
                session_dict['metadata'] = json.loads(session_dict.get('metadata', '{}'))
                sessions.append(session_dict)

            return sessions

    def export_markdown(
        self,
        output_path: str,
        memory_type: Optional[MemoryType] = None,
        namespace: Optional[str] = None,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        priority: Optional[Priority] = None,
        tags: Optional[List[str]] = None,
        include_decisions: bool = True,
        include_sessions: bool = True
    ) -> str:
        """
        Export memories to Markdown format.

        Args:
            output_path: Where to save the Markdown file
            memory_type: Filter by memory type
            namespace: Filter by namespace
            start_date: Filter memories after this date
            end_date: Filter memories before this date
            priority: Filter by priority
            tags: Filter by tags
            include_decisions: Include decision records
            include_sessions: Include session summaries

        Returns:
            Path to created file
        """
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        # Fetch data
        memories = self._fetch_memories(
            memory_type=memory_type,
            namespace=namespace,
            start_date=start_date,
            end_date=end_date,
            priority=priority,
            tags=tags
        )

        decisions = []
        sessions = []

        if include_decisions:
            decisions = self._fetch_decisions(start_date=start_date, end_date=end_date)

        if include_sessions:
            sessions = self._fetch_sessions(start_date=start_date, end_date=end_date)

        # Build Markdown
        md_lines = []

        # Header
        md_lines.append("# DIVERGA Memory Export")
        md_lines.append(f"Exported: {datetime.now().isoformat()}")

        # Extract project name from memories
        project_names = set(m.get('project_name') for m in memories if m.get('project_name'))
        if project_names:
            md_lines.append(f"Project: {', '.join(project_names)}")

        md_lines.append(f"Total Memories: {len(memories)}")
        md_lines.append("")
        md_lines.append("---")
        md_lines.append("")

        # Decisions section
        if decisions:
            md_lines.append("## Decisions")
            md_lines.append("")

            for decision in decisions:
                decision_id = decision.get('id', 'Unknown')
                stage = decision.get('stage', 'Unknown')
                agent_id = decision.get('agent_id', 'Unknown')
                decision_type = decision.get('decision_type', 'Unknown')
                description = decision.get('description', '')
                before_state = decision.get('before_state')
                after_state = decision.get('after_state')
                rationale = decision.get('rationale', '')
                t_score = decision.get('t_score')
                created_at = decision.get('created_at', '')

                md_lines.append(f"### D{decision_id:03d}: {description[:50]}...")
                md_lines.append(f"- **Date**: {created_at}")
                md_lines.append(f"- **Agent**: {agent_id}")
                md_lines.append(f"- **Stage**: {stage}")
                md_lines.append(f"- **Type**: {decision_type}")
                if t_score is not None:
                    md_lines.append(f"- **T-Score**: {t_score:.2f}")
                md_lines.append("")

                md_lines.append("**Description**:")
                md_lines.append(description)
                md_lines.append("")

                if before_state or after_state:
                    if before_state:
                        md_lines.append(f"**Before**: {before_state}")
                    if after_state:
                        md_lines.append(f"**After**: {after_state}")
                    md_lines.append("")

                if rationale:
                    md_lines.append("**Rationale**:")
                    md_lines.append(rationale)
                    md_lines.append("")

                md_lines.append("---")
                md_lines.append("")

        # Sessions section
        if sessions:
            md_lines.append("## Sessions")
            md_lines.append("")

            for session in sessions:
                session_id = session.get('id', 'Unknown')
                summary = session.get('summary', 'No summary')
                agents_used = session.get('agents_used', [])
                decisions_made = session.get('decisions', [])
                started_at = session.get('started_at', '')
                ended_at = session.get('ended_at')

                md_lines.append(f"### Session {session_id} ({started_at})")

                if ended_at:
                    # Calculate duration
                    try:
                        start = datetime.fromisoformat(started_at)
                        end = datetime.fromisoformat(ended_at)
                        duration = end - start
                        minutes = int(duration.total_seconds() / 60)
                        md_lines.append(f"- **Duration**: {minutes} minutes")
                    except:
                        pass

                if agents_used:
                    md_lines.append(f"- **Agents Used**: {', '.join(agents_used)}")

                if decisions_made:
                    md_lines.append(f"- **Decisions**: {len(decisions_made)}")

                md_lines.append("")
                md_lines.append("**Summary**:")
                md_lines.append(summary)
                md_lines.append("")
                md_lines.append("---")
                md_lines.append("")

        # Memories section
        if memories:
            md_lines.append("## Memories")
            md_lines.append("")

            # Group by type
            memories_by_type = {}
            for memory in memories:
                mem_type = memory.get('memory_type', 'unknown')
                if mem_type not in memories_by_type:
                    memories_by_type[mem_type] = []
                memories_by_type[mem_type].append(memory)

            for mem_type, mem_list in memories_by_type.items():
                md_lines.append(f"### {mem_type.upper()}")
                md_lines.append("")

                for memory in mem_list:
                    title = memory.get('title', 'Untitled')
                    content = memory.get('content', '')
                    namespace = memory.get('namespace', '')
                    priority = memory.get('priority', 5)
                    tags = memory.get('tags', [])
                    created_at = memory.get('created_at', '')

                    md_lines.append(f"#### {title}")
                    md_lines.append(f"- **Namespace**: `{namespace}`")
                    md_lines.append(f"- **Priority**: {priority}/10")
                    if tags:
                        md_lines.append(f"- **Tags**: {', '.join(tags)}")
                    md_lines.append(f"- **Created**: {created_at}")
                    md_lines.append("")
                    md_lines.append(content)
                    md_lines.append("")
                    md_lines.append("---")
                    md_lines.append("")

        # Write to file
        output_path.write_text("\n".join(md_lines), encoding='utf-8')

        return str(output_path)

    def export_json(
        self,
        output_path: str,
        memory_type: Optional[MemoryType] = None,
        namespace: Optional[str] = None,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        priority: Optional[Priority] = None,
        tags: Optional[List[str]] = None,
        include_decisions: bool = True,
        include_sessions: bool = True,
        pretty: bool = True
    ) -> str:
        """
        Export memories to JSON format.

        Args:
            output_path: Where to save the JSON file
            memory_type: Filter by memory type
            namespace: Filter by namespace
            start_date: Filter memories after this date
            end_date: Filter memories before this date
            priority: Filter by priority
            tags: Filter by tags
            include_decisions: Include decision records
            include_sessions: Include session summaries
            pretty: Pretty-print JSON (indentation)

        Returns:
            Path to created file
        """
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        # Fetch data
        memories = self._fetch_memories(
            memory_type=memory_type,
            namespace=namespace,
            start_date=start_date,
            end_date=end_date,
            priority=priority,
            tags=tags
        )

        decisions = []
        sessions = []

        if include_decisions:
            decisions = self._fetch_decisions(start_date=start_date, end_date=end_date)

        if include_sessions:
            sessions = self._fetch_sessions(start_date=start_date, end_date=end_date)

        # Build JSON structure
        export_data = {
            "meta": {
                "exported_at": datetime.now().isoformat(),
                "total_memories": len(memories),
                "total_decisions": len(decisions),
                "total_sessions": len(sessions)
            },
            "memories": memories,
            "decisions": decisions,
            "sessions": sessions
        }

        # Extract project name
        project_names = set(m.get('project_name') for m in memories if m.get('project_name'))
        if project_names:
            export_data["meta"]["projects"] = list(project_names)

        # Write to file
        indent = 2 if pretty else None
        output_path.write_text(
            json.dumps(export_data, indent=indent, ensure_ascii=False),
            encoding='utf-8'
        )

        return str(output_path)

    def export_yaml(
        self,
        output_path: str,
        memory_type: Optional[MemoryType] = None,
        namespace: Optional[str] = None,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        priority: Optional[Priority] = None,
        tags: Optional[List[str]] = None,
        include_decisions: bool = True,
        include_sessions: bool = True
    ) -> str:
        """
        Export memories to YAML format.

        Args:
            output_path: Where to save the YAML file
            memory_type: Filter by memory type
            namespace: Filter by namespace
            start_date: Filter memories after this date
            end_date: Filter memories before this date
            priority: Filter by priority
            tags: Filter by tags
            include_decisions: Include decision records
            include_sessions: Include session summaries

        Returns:
            Path to created file
        """
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        # Fetch data
        memories = self._fetch_memories(
            memory_type=memory_type,
            namespace=namespace,
            start_date=start_date,
            end_date=end_date,
            priority=priority,
            tags=tags
        )

        decisions = []
        sessions = []

        if include_decisions:
            decisions = self._fetch_decisions(start_date=start_date, end_date=end_date)

        if include_sessions:
            sessions = self._fetch_sessions(start_date=start_date, end_date=end_date)

        # Build YAML structure
        export_data = {
            "meta": {
                "exported_at": datetime.now().isoformat(),
                "total_memories": len(memories),
                "total_decisions": len(decisions),
                "total_sessions": len(sessions)
            },
            "memories": memories,
            "decisions": decisions,
            "sessions": sessions
        }

        # Extract project name
        project_names = set(m.get('project_name') for m in memories if m.get('project_name'))
        if project_names:
            export_data["meta"]["projects"] = list(project_names)

        # Write to file
        output_path.write_text(
            yaml.dump(export_data, allow_unicode=True, sort_keys=False),
            encoding='utf-8'
        )

        return str(output_path)

    def export_all(
        self,
        scope: str = "all",
        format: str = "markdown",
        output_dir: str = "./diverga-exports",
        **filters
    ) -> str:
        """
        Export all memories with auto-generated filename.

        Args:
            scope: Export scope ("all", "recent", "decisions", "sessions")
            format: Export format ("markdown", "json", "yaml")
            output_dir: Directory to save exports
            **filters: Additional filter arguments

        Returns:
            Path to created file
        """
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)

        # Generate filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        extensions = {
            "markdown": "md",
            "json": "json",
            "yaml": "yaml"
        }
        ext = extensions.get(format, "md")
        filename = f"diverga_export_{scope}_{timestamp}.{ext}"
        output_path = output_dir / filename

        # Apply scope filters
        if scope == "recent":
            # Last 7 days
            from datetime import timedelta
            filters['start_date'] = datetime.now() - timedelta(days=7)
        elif scope == "decisions":
            filters['memory_type'] = MemoryType.DECISION
        elif scope == "sessions":
            filters['include_decisions'] = False
            filters['include_sessions'] = True

        # Export based on format
        if format == "markdown":
            return self.export_markdown(str(output_path), **filters)
        elif format == "json":
            return self.export_json(str(output_path), **filters)
        elif format == "yaml":
            return self.export_yaml(str(output_path), **filters)
        else:
            raise ValueError(f"Unsupported format: {format}")
