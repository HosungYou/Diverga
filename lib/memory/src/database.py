"""
SQLite database module for Claude Code memory system.

Cross-platform compatible memory storage with support for:
- Hierarchical namespaces
- Session tracking
- Full-text search
- Soft deletion
- Content versioning
"""

import sqlite3
import hashlib
import json
from contextlib import contextmanager
from datetime import datetime
from pathlib import Path
from typing import Optional, List, Dict, Any, Tuple


class MemoryDatabase:
    """
    SQLite-based memory storage with namespace support.

    Thread-safe using context managers for all operations.
    Supports cross-platform file paths and UTF-8 content.
    """

    def __init__(self, db_path: str):
        """
        Initialize database connection.

        Args:
            db_path: Path to SQLite database file. Will be created if not exists.
                    Parent directories will be created automatically.
        """
        self.db_path = Path(db_path).resolve()
        self.db_path.parent.mkdir(parents=True, exist_ok=True)

        # Initialize schema on first connection
        self.init_schema()

    @contextmanager
    def _get_connection(self):
        """
        Context manager for database connections.

        Ensures proper connection cleanup and UTF-8 encoding.
        """
        conn = sqlite3.connect(
            str(self.db_path),
            detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES
        )
        conn.row_factory = sqlite3.Row  # Enable column access by name
        conn.execute("PRAGMA foreign_keys = ON")  # Enable foreign key constraints
        try:
            yield conn
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()

    def init_schema(self) -> None:
        """
        Create database schema if not exists.

        Tables:
        - memories: Core memory storage with versioning
        - sessions: Session tracking with agent usage
        """
        with self._get_connection() as conn:
            cursor = conn.cursor()

            # Memories table with namespace hierarchy
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS memories (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    version INTEGER NOT NULL DEFAULT 1,
                    content_hash TEXT NOT NULL,
                    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

                    -- Classification
                    memory_type TEXT NOT NULL CHECK(memory_type IN (
                        'decision', 'pattern', 'insight', 'context',
                        'learning', 'skill', 'note'
                    )),
                    namespace TEXT NOT NULL,  -- e.g., 'project.feature.component'
                    priority INTEGER NOT NULL DEFAULT 5 CHECK(priority BETWEEN 1 AND 10),

                    -- Content
                    title TEXT NOT NULL,
                    content TEXT NOT NULL,
                    summary TEXT,

                    -- Metadata
                    agent_id TEXT,
                    session_id TEXT,
                    project_name TEXT,
                    tags TEXT,  -- JSON array
                    embedding BLOB,  -- Future: vector embeddings

                    -- Lifecycle
                    status TEXT NOT NULL DEFAULT 'active' CHECK(status IN (
                        'active', 'archived', 'deleted'
                    ))
                )
            """)

            # Sessions table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS sessions (
                    id TEXT PRIMARY KEY,
                    started_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
                    ended_at TIMESTAMP,
                    project_name TEXT,
                    summary TEXT,
                    agents_used TEXT,  -- JSON array
                    decision_count INTEGER DEFAULT 0,
                    memory_count INTEGER DEFAULT 0
                )
            """)

            # Indexes for performance
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_memories_namespace
                ON memories(namespace)
            """)
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_memories_type
                ON memories(memory_type)
            """)
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_memories_status
                ON memories(status)
            """)
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_memories_created
                ON memories(created_at DESC)
            """)
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_memories_session
                ON memories(session_id)
            """)

            # Full-text search index (FTS5)
            cursor.execute("""
                CREATE VIRTUAL TABLE IF NOT EXISTS memories_fts USING fts5(
                    title, content, summary, tags,
                    content='memories',
                    content_rowid='id'
                )
            """)

            # Triggers to keep FTS in sync
            cursor.execute("""
                CREATE TRIGGER IF NOT EXISTS memories_ai AFTER INSERT ON memories BEGIN
                    INSERT INTO memories_fts(rowid, title, content, summary, tags)
                    VALUES (new.id, new.title, new.content, new.summary, new.tags);
                END
            """)
            cursor.execute("""
                CREATE TRIGGER IF NOT EXISTS memories_ad AFTER DELETE ON memories BEGIN
                    INSERT INTO memories_fts(memories_fts, rowid, title, content, summary, tags)
                    VALUES('delete', old.id, old.title, old.content, old.summary, old.tags);
                END
            """)
            cursor.execute("""
                CREATE TRIGGER IF NOT EXISTS memories_au AFTER UPDATE ON memories BEGIN
                    INSERT INTO memories_fts(memories_fts, rowid, title, content, summary, tags)
                    VALUES('delete', old.id, old.title, old.content, old.summary, old.tags);
                    INSERT INTO memories_fts(rowid, title, content, summary, tags)
                    VALUES (new.id, new.title, new.content, new.summary, new.tags);
                END
            """)

    def _compute_hash(self, content: str) -> str:
        """Compute SHA-256 hash of content for deduplication."""
        return hashlib.sha256(content.encode('utf-8')).hexdigest()

    def store_memory(
        self,
        memory_type: str,
        namespace: str,
        title: str,
        content: str,
        summary: Optional[str] = None,
        priority: int = 5,
        agent_id: Optional[str] = None,
        session_id: Optional[str] = None,
        project_name: Optional[str] = None,
        tags: Optional[List[str]] = None,
        embedding: Optional[bytes] = None
    ) -> int:
        """
        Store a new memory.

        Args:
            memory_type: Type of memory (decision, pattern, insight, etc.)
            namespace: Hierarchical namespace (e.g., 'project.feature.component')
            title: Short descriptive title
            content: Full memory content
            summary: Optional summary for quick reference
            priority: Priority level 1-10 (10 = highest)
            agent_id: Agent that created this memory
            session_id: Session identifier
            project_name: Associated project name
            tags: List of tags for categorization
            embedding: Optional vector embedding (bytes)

        Returns:
            Memory ID (integer primary key)

        Raises:
            ValueError: If memory_type or priority is invalid
            sqlite3.Error: If database operation fails
        """
        valid_types = {'decision', 'pattern', 'insight', 'context', 'learning', 'skill', 'note'}
        if memory_type not in valid_types:
            raise ValueError(f"Invalid memory_type. Must be one of: {valid_types}")

        if not 1 <= priority <= 10:
            raise ValueError("Priority must be between 1 and 10")

        content_hash = self._compute_hash(content)
        tags_json = json.dumps(tags) if tags else None

        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO memories (
                    memory_type, namespace, title, content, summary,
                    priority, agent_id, session_id, project_name,
                    tags, embedding, content_hash
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                memory_type, namespace, title, content, summary,
                priority, agent_id, session_id, project_name,
                tags_json, embedding, content_hash
            ))
            return cursor.lastrowid

    def get_memory(self, memory_id: int) -> Optional[Dict[str, Any]]:
        """
        Retrieve a single memory by ID.

        Args:
            memory_id: Memory primary key

        Returns:
            Dictionary with memory fields, or None if not found
        """
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT * FROM memories WHERE id = ? AND status = 'active'
            """, (memory_id,))
            row = cursor.fetchone()

            if row is None:
                return None

            return self._row_to_dict(row)

    def search_memories(
        self,
        query: str,
        namespace: Optional[str] = None,
        memory_type: Optional[str] = None,
        limit: int = 10
    ) -> List[Dict[str, Any]]:
        """
        Full-text search across memories.

        Args:
            query: Search query (supports FTS5 syntax)
            namespace: Filter by namespace (supports prefix matching)
            memory_type: Filter by specific memory type
            limit: Maximum number of results

        Returns:
            List of matching memories ordered by relevance
        """
        with self._get_connection() as conn:
            cursor = conn.cursor()

            # Build query with optional filters
            sql = """
                SELECT m.*
                FROM memories m
                JOIN memories_fts ON m.id = memories_fts.rowid
                WHERE memories_fts MATCH ?
                AND m.status = 'active'
            """
            params = [query]

            if namespace:
                sql += " AND m.namespace LIKE ?"
                params.append(f"{namespace}%")

            if memory_type:
                sql += " AND m.memory_type = ?"
                params.append(memory_type)

            sql += " ORDER BY rank LIMIT ?"
            params.append(limit)

            cursor.execute(sql, params)
            rows = cursor.fetchall()

            return [self._row_to_dict(row) for row in rows]

    def update_memory(self, memory_id: int, **fields) -> bool:
        """
        Update memory fields.

        Args:
            memory_id: Memory ID to update
            **fields: Fields to update (title, content, summary, priority, etc.)

        Returns:
            True if updated, False if memory not found

        Note:
            Updates increment version and update updated_at timestamp.
            Content hash is recalculated if content changes.
        """
        allowed_fields = {
            'title', 'content', 'summary', 'priority', 'namespace',
            'tags', 'embedding', 'status', 'memory_type'
        }

        updates = {k: v for k, v in fields.items() if k in allowed_fields}
        if not updates:
            return False

        # Handle tags serialization
        if 'tags' in updates and isinstance(updates['tags'], list):
            updates['tags'] = json.dumps(updates['tags'])

        # Recalculate content hash if content changed
        if 'content' in updates:
            updates['content_hash'] = self._compute_hash(updates['content'])

        # Build SET clause
        set_clause = ', '.join(f"{k} = ?" for k in updates.keys())
        set_clause += ", version = version + 1, updated_at = CURRENT_TIMESTAMP"

        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(f"""
                UPDATE memories
                SET {set_clause}
                WHERE id = ? AND status = 'active'
            """, (*updates.values(), memory_id))

            return cursor.rowcount > 0

    def delete_memory(self, memory_id: int, hard_delete: bool = False) -> bool:
        """
        Delete a memory (soft delete by default).

        Args:
            memory_id: Memory ID to delete
            hard_delete: If True, permanently remove from database

        Returns:
            True if deleted, False if memory not found
        """
        with self._get_connection() as conn:
            cursor = conn.cursor()

            if hard_delete:
                cursor.execute("DELETE FROM memories WHERE id = ?", (memory_id,))
            else:
                cursor.execute("""
                    UPDATE memories
                    SET status = 'deleted', updated_at = CURRENT_TIMESTAMP
                    WHERE id = ?
                """, (memory_id,))

            return cursor.rowcount > 0

    def get_memories_by_namespace(
        self,
        namespace: str,
        include_children: bool = True,
        limit: int = 50
    ) -> List[Dict[str, Any]]:
        """
        Get all memories in a namespace.

        Args:
            namespace: Namespace to query
            include_children: If True, include child namespaces
            limit: Maximum results

        Returns:
            List of memories ordered by priority (descending) and recency
        """
        with self._get_connection() as conn:
            cursor = conn.cursor()

            if include_children:
                # Prefix match for hierarchical namespaces
                cursor.execute("""
                    SELECT * FROM memories
                    WHERE namespace LIKE ?
                    AND status = 'active'
                    ORDER BY priority DESC, created_at DESC
                    LIMIT ?
                """, (f"{namespace}%", limit))
            else:
                # Exact match
                cursor.execute("""
                    SELECT * FROM memories
                    WHERE namespace = ?
                    AND status = 'active'
                    ORDER BY priority DESC, created_at DESC
                    LIMIT ?
                """, (namespace, limit))

            rows = cursor.fetchall()
            return [self._row_to_dict(row) for row in rows]

    def record_session(
        self,
        session_id: str,
        project_name: Optional[str] = None,
        summary: Optional[str] = None,
        agents_used: Optional[List[str]] = None
    ) -> None:
        """
        Record a new session or update existing.

        Args:
            session_id: Unique session identifier
            project_name: Associated project
            summary: Session summary
            agents_used: List of agent IDs used
        """
        agents_json = json.dumps(agents_used) if agents_used else None

        with self._get_connection() as conn:
            cursor = conn.cursor()

            # Upsert (insert or replace)
            cursor.execute("""
                INSERT INTO sessions (id, project_name, summary, agents_used)
                VALUES (?, ?, ?, ?)
                ON CONFLICT(id) DO UPDATE SET
                    summary = excluded.summary,
                    agents_used = excluded.agents_used,
                    ended_at = CURRENT_TIMESTAMP
            """, (session_id, project_name, summary, agents_json))

    def get_recent_sessions(self, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Get recent sessions ordered by start time.

        Args:
            limit: Maximum number of sessions

        Returns:
            List of session dictionaries
        """
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT * FROM sessions
                ORDER BY started_at DESC
                LIMIT ?
            """, (limit,))

            rows = cursor.fetchall()
            return [self._row_to_dict(row) for row in rows]

    def get_session_memories(self, session_id: str) -> List[Dict[str, Any]]:
        """
        Get all memories created in a specific session.

        Args:
            session_id: Session identifier

        Returns:
            List of memories from that session
        """
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT * FROM memories
                WHERE session_id = ?
                AND status = 'active'
                ORDER BY created_at ASC
            """, (session_id,))

            rows = cursor.fetchall()
            return [self._row_to_dict(row) for row in rows]

    def get_statistics(self) -> Dict[str, Any]:
        """
        Get database statistics.

        Returns:
            Dictionary with counts by type, namespace, etc.
        """
        with self._get_connection() as conn:
            cursor = conn.cursor()

            stats = {}

            # Total counts
            cursor.execute("SELECT COUNT(*) FROM memories WHERE status = 'active'")
            stats['total_memories'] = cursor.fetchone()[0]

            cursor.execute("SELECT COUNT(*) FROM sessions")
            stats['total_sessions'] = cursor.fetchone()[0]

            # Counts by type
            cursor.execute("""
                SELECT memory_type, COUNT(*)
                FROM memories
                WHERE status = 'active'
                GROUP BY memory_type
            """)
            stats['by_type'] = dict(cursor.fetchall())

            # Top namespaces
            cursor.execute("""
                SELECT namespace, COUNT(*) as cnt
                FROM memories
                WHERE status = 'active'
                GROUP BY namespace
                ORDER BY cnt DESC
                LIMIT 10
            """)
            stats['top_namespaces'] = [
                {'namespace': row[0], 'count': row[1]}
                for row in cursor.fetchall()
            ]

            return stats

    def _row_to_dict(self, row: sqlite3.Row) -> Dict[str, Any]:
        """Convert SQLite Row to dictionary with JSON deserialization."""
        d = dict(row)

        # Deserialize JSON fields
        if d.get('tags'):
            try:
                d['tags'] = json.loads(d['tags'])
            except json.JSONDecodeError:
                d['tags'] = []

        if d.get('agents_used'):
            try:
                d['agents_used'] = json.loads(d['agents_used'])
            except json.JSONDecodeError:
                d['agents_used'] = []

        return d
