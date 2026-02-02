"""
Memory API - Main interface for Diverga Memory System.

Provides a high-level API for storing, searching, and retrieving
research context with 3-layer token-efficient retrieval.
"""

import os
import uuid
from datetime import datetime
from pathlib import Path
from typing import Optional, List, Dict, Any
from dataclasses import dataclass, asdict

try:
    from .database import MemoryDatabase
    from .embeddings import EmbeddingManager
    from .schema import (
        Memory, MemoryIndex, MemoryContext, Decision, Session, ProjectContext,
        MemoryType, DecisionType, Priority, SearchScope
    )
except ImportError:
    # Support direct imports when not used as package
    from database import MemoryDatabase
    from embeddings import EmbeddingManager
    from schema import (
        Memory, MemoryIndex, MemoryContext, Decision, Session, ProjectContext,
        MemoryType, DecisionType, Priority, SearchScope
    )


@dataclass
class DivergeMemoryConfig:
    """Configuration for DivergeMemory system."""
    project_path: Optional[str] = None
    global_path: Optional[str] = None
    enable_embeddings: bool = True
    embedding_cache: bool = True
    auto_detect_project: bool = True


class DivergeMemory:
    """
    Main Memory API for Diverga research context persistence.

    Features:
    - 3-layer token-efficient retrieval (Index → Context → Full)
    - Automatic project detection
    - Semantic search with embeddings
    - Decision tracking
    - Session management

    Usage:
        memory = DivergeMemory()

        # Store memory
        memory_id = memory.store(
            content="Used regression analysis for hypothesis testing",
            memory_type=MemoryType.DECISION,
            namespace="analysis.statistical",
            priority=Priority.HIGH
        )

        # Search (Layer 1: Compact results)
        results = memory.search("regression analysis", limit=5)

        # Get context (Layer 2: Surrounding context)
        context = memory.get_context(results[0].id)

        # Retrieve full (Layer 3: Complete details)
        full_memory = memory.retrieve([memory_id])
    """

    def __init__(
        self,
        project_path: Optional[str] = None,
        config: Optional[DivergeMemoryConfig] = None
    ):
        """
        Initialize Memory API.

        Args:
            project_path: Path to project (auto-detects if None)
            config: Configuration object
        """
        self.config = config or DivergeMemoryConfig(project_path=project_path)

        # Initialize paths
        self._init_paths()

        # Initialize database
        self.db = MemoryDatabase(str(self.db_path))

        # Initialize embeddings (optional)
        self.embeddings = None
        if self.config.enable_embeddings:
            try:
                cache_dir = self.memory_dir / "embeddings_cache" if self.config.embedding_cache else None
                self.embeddings = EmbeddingManager(cache_dir=cache_dir)
            except Exception as e:
                print(f"Warning: Embeddings disabled due to: {e}")
                print("Falling back to text-based search only.")

    def _init_paths(self):
        """Initialize project and global paths."""
        # Detect project path
        if self.config.auto_detect_project and self.config.project_path is None:
            self.config.project_path = self._detect_project_root()

        # Set paths
        if self.config.project_path:
            # Project-scoped memory
            self.memory_dir = Path(self.config.project_path) / ".diverga" / "memory"
            self.scope = "project"
        else:
            # Global memory
            global_path = self.config.global_path or str(Path.home() / ".diverga" / "memory")
            self.memory_dir = Path(global_path)
            self.scope = "global"

        self.memory_dir.mkdir(parents=True, exist_ok=True)
        self.db_path = self.memory_dir / "memories.db"

    def _detect_project_root(self) -> Optional[str]:
        """
        Detect project root by looking for markers.

        Searches up from cwd for:
        - .diverga/ directory
        - .research/ directory
        - .git/ directory

        Returns:
            Project root path or None
        """
        cwd = Path.cwd()

        for parent in [cwd] + list(cwd.parents):
            markers = [
                parent / ".diverga",
                parent / ".research",
                parent / ".git"
            ]

            if any(marker.exists() for marker in markers):
                return str(parent)

        return None

    # WRITE OPERATIONS

    def store(
        self,
        content: str,
        memory_type: MemoryType = MemoryType.LEARNING,
        namespace: str = "general",
        priority: Priority = Priority.MEDIUM,
        title: Optional[str] = None,
        tags: Optional[List[str]] = None,
        agent_id: Optional[str] = None,
        session_id: Optional[str] = None,
        project_name: Optional[str] = None
    ) -> str:
        """
        Store a new memory.

        Args:
            content: Memory content
            memory_type: Type of memory
            namespace: Hierarchical namespace (e.g., 'project.analysis.statistical')
            priority: Priority level
            title: Optional short title
            tags: Optional tags for categorization
            agent_id: Agent that created this memory
            session_id: Session identifier
            project_name: Associated project

        Returns:
            Memory ID (string)
        """
        # Generate title if not provided
        if title is None:
            title = content[:100].strip()

        # Generate embedding if available
        embedding = None
        if self.embeddings:
            try:
                embedding_list = self.embeddings.embed(content)
                # Convert to bytes for database storage
                import json
                embedding = json.dumps(embedding_list).encode('utf-8')
            except Exception as e:
                print(f"Warning: Failed to generate embedding: {e}")

        # Convert priority enum to integer (1-10 scale)
        priority_map = {
            Priority.LOW: 3,
            Priority.MEDIUM: 5,
            Priority.HIGH: 8,
            Priority.CRITICAL: 10
        }
        priority_int = priority_map.get(priority, 5)

        # Use project_name from detection if not provided
        if project_name is None:
            project_name = self._get_project_name()

        # Store in database using existing interface
        db_id = self.db.store_memory(
            memory_type=memory_type.value,
            namespace=namespace,
            title=title,
            content=content,
            summary=None,  # Could generate summary in future
            priority=priority_int,
            agent_id=agent_id,
            session_id=session_id,
            project_name=project_name,
            tags=tags,
            embedding=embedding
        )

        # Return ID as string
        return str(db_id)

    def record_decision(
        self,
        stage: str,
        agent_id: str,
        decision_type: DecisionType,
        description: str,
        before_state: Optional[str] = None,
        after_state: Optional[str] = None,
        rationale: str = "",
        t_score: Optional[float] = None,
        **kwargs
    ) -> str:
        """
        Record an architectural or research decision.

        Args:
            stage: Research stage (e.g., 'design', 'analysis')
            agent_id: Agent making the decision
            decision_type: Type of decision
            description: Decision description
            before_state: State before decision
            after_state: State after decision
            rationale: Justification for decision
            t_score: Typicality score (VS methodology)
            **kwargs: Additional metadata

        Returns:
            Decision ID (stored as memory)
        """
        # Build decision content
        content_parts = [description]
        if before_state:
            content_parts.append(f"\nBefore: {before_state}")
        if after_state:
            content_parts.append(f"\nAfter: {after_state}")
        if rationale:
            content_parts.append(f"\nRationale: {rationale}")
        if t_score is not None:
            content_parts.append(f"\nT-Score: {t_score:.2f}")

        content = "\n".join(content_parts)

        # Store as memory with decision tags
        tags = [decision_type.value, stage, "decision"]
        if t_score is not None:
            if t_score >= 0.7:
                tags.append("common")
            elif t_score >= 0.4:
                tags.append("moderate")
            elif t_score >= 0.2:
                tags.append("innovative")
            else:
                tags.append("experimental")

        decision_id = self.store(
            content=content,
            memory_type=MemoryType.DECISION,
            namespace=f"decisions.{stage}",
            priority=Priority.HIGH,
            title=description,
            tags=tags,
            agent_id=agent_id
        )

        return decision_id

    def save_session(
        self,
        session_id: str,
        summary: str,
        agents_used: List[str],
        decisions: Optional[List[str]] = None,
        **kwargs
    ) -> str:
        """
        Save or update a session record.

        Args:
            session_id: Unique session ID
            summary: Session summary
            agents_used: List of agent IDs used
            decisions: List of decision IDs made
            **kwargs: Additional metadata

        Returns:
            Session ID
        """
        # Use existing database method
        self.db.record_session(
            session_id=session_id,
            project_name=self._get_project_name(),
            summary=summary,
            agents_used=agents_used
        )
        return session_id

    # READ OPERATIONS (3-LAYER RETRIEVAL)

    def search(
        self,
        query: str,
        scope: SearchScope = SearchScope.BOTH,
        memory_types: Optional[List[MemoryType]] = None,
        limit: int = 10
    ) -> List[MemoryIndex]:
        """
        LAYER 1: Search memories (compact results).

        Returns minimal information for token efficiency.

        Args:
            query: Search query
            scope: Search scope (project/global/both)
            memory_types: Filter by memory types
            limit: Maximum results

        Returns:
            List of MemoryIndex objects (compact)
        """
        # Determine search scope
        project_name = self._get_project_name() if scope != SearchScope.GLOBAL else None

        # Semantic search if embeddings available
        if self.embeddings and query:
            try:
                return self._semantic_search(query, project_name, memory_types, limit)
            except Exception as e:
                print(f"Warning: Semantic search failed: {e}")
                print("Falling back to text search.")

        # Fallback to text search
        return self._text_search(query, project_name, memory_types, limit)

    def get_context(self, memory_id: str) -> Optional[MemoryContext]:
        """
        LAYER 2: Get memory with surrounding context.

        Returns the memory plus related memories and session context.

        Args:
            memory_id: Memory ID (string or int)

        Returns:
            MemoryContext object or None
        """
        # Convert to int if string
        try:
            mem_id = int(memory_id)
        except (ValueError, TypeError):
            mem_id = memory_id

        # Get the memory
        memory = self.db.get_memory(mem_id)
        if not memory:
            return None

        # Find related memories (same namespace)
        parent_namespace = memory['namespace'].rsplit('.', 1)[0] if '.' in memory['namespace'] else memory['namespace']
        related = self.db.get_memories_by_namespace(
            namespace=parent_namespace,
            include_children=True,
            limit=5
        )

        # Convert to MemoryIndex, exclude current memory
        related_indices = [
            self._memory_to_index(m) for m in related
            if str(m['id']) != str(memory_id)
        ][:3]

        # Get session context if available
        session_context = None
        if memory.get('session_id'):
            session_memories = self.db.get_session_memories(memory['session_id'])
            session_context = f"Session with {len(session_memories)} memories"

        return MemoryContext(
            memory=self._dict_to_memory(memory),
            related_memories=related_indices,
            session_context=session_context,
            project_context=self._get_project_name()
        )

    def retrieve(self, memory_ids: List[str]) -> List[Memory]:
        """
        LAYER 3: Retrieve full memory details.

        Returns complete memory objects with all fields.

        Args:
            memory_ids: List of memory IDs

        Returns:
            List of Memory objects
        """
        memories = []
        for memory_id in memory_ids:
            memory_dict = self.db.get_memory(memory_id)
            if memory_dict:
                memories.append(self._dict_to_memory(memory_dict))
        return memories

    # CONVENIENCE METHODS

    def get_project_context(self, project_name: Optional[str] = None) -> Dict[str, Any]:
        """
        Get high-level project context summary.

        Args:
            project_name: Project name (uses current if None)

        Returns:
            Dictionary with project context summary
        """
        project_name = project_name or self._get_project_name()

        # Get all memories from root namespace
        all_memories = self.db.get_memories_by_namespace(
            namespace="",
            include_children=True,
            limit=1000
        )

        # Filter by project name if specified
        if project_name:
            all_memories = [m for m in all_memories if m.get('project_name') == project_name]

        # Get recent decisions (memories with type='decision')
        recent_decisions = [
            m for m in all_memories
            if m.get('memory_type') == 'decision'
        ][:5]

        # Get key patterns (high priority learnings and patterns)
        key_patterns = [
            m for m in all_memories
            if m.get('memory_type') in ['pattern', 'learning'] and m.get('priority', 0) >= 7
        ][:5]

        # Get active sessions
        all_sessions = self.db.get_recent_sessions(limit=10)
        active_sessions = [
            s for s in all_sessions
            if s.get('project_name') == project_name and s.get('ended_at') is None
        ]

        return {
            'project_name': project_name or "Unknown",
            'total_memories': len(all_memories),
            'recent_decisions': [self._memory_to_index(d) for d in recent_decisions],
            'key_patterns': [self._memory_to_index(m) for m in key_patterns],
            'active_sessions': active_sessions,
            'last_updated': datetime.now().isoformat()
        }

    def get_recent_decisions(
        self,
        project_name: Optional[str] = None,
        limit: int = 10
    ) -> List[Dict[str, Any]]:
        """Get recent decisions for a project (as memory dictionaries)."""
        project_name = project_name or self._get_project_name()

        # Search for decision memories
        decision_memories = self.db.search_memories(
            memory_type='decision',
            project_name=project_name,
            limit=limit
        )

        return decision_memories

    def get_session_history(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get recent session history."""
        return self.db.get_recent_sessions(limit)

    # HELPER METHODS

    def _get_project_name(self) -> Optional[str]:
        """Get current project name from path."""
        if self.scope == "project" and self.config.project_path:
            return Path(self.config.project_path).name
        return None

    def _semantic_search(
        self,
        query: str,
        project_name: Optional[str],
        memory_types: Optional[List[MemoryType]],
        limit: int
    ) -> List[MemoryIndex]:
        """Perform semantic search using embeddings."""
        # Generate query embedding
        query_embedding = self.embeddings.embed(query)

        # Get candidate memories
        candidates = self.db.search_memories(
            memory_types=memory_types,
            project_name=project_name,
            limit=100  # Get more candidates for ranking
        )

        # Filter candidates with embeddings
        candidates_with_embeddings = [
            (c, c['embedding']) for c in candidates
            if c.get('embedding')
        ]

        if not candidates_with_embeddings:
            # No embeddings available, fallback
            return self._text_search(query, project_name, memory_types, limit)

        # Calculate similarities
        similarities = []
        for candidate, embedding in candidates_with_embeddings:
            try:
                score = self.embeddings.similarity(query_embedding, embedding)
                similarities.append((candidate, score))
            except Exception:
                continue

        # Sort by similarity
        similarities.sort(key=lambda x: x[1], reverse=True)

        # Convert to MemoryIndex
        results = []
        for memory_dict, score in similarities[:limit]:
            index = self._memory_to_index(memory_dict)
            index.similarity_score = score
            results.append(index)

        return results

    def _text_search(
        self,
        query: str,
        project_name: Optional[str],
        memory_types: Optional[List[MemoryType]],
        limit: int
    ) -> List[MemoryIndex]:
        """Perform text-based search using database FTS."""
        # database.py only supports single memory_type, use first if provided
        memory_type = None
        if memory_types and len(memory_types) > 0:
            memory_type = memory_types[0].value

        try:
            memories = self.db.search_memories(
                query,
                memory_type=memory_type,
                limit=limit
            )
        except Exception as e:
            # Fallback to namespace-based retrieval if FTS fails
            print(f"FTS search failed, using fallback: {e}")
            memories = self.db.get_memories_by_namespace(
                namespace="",
                include_children=True,
                limit=limit
            )

        # Filter by project_name after retrieval if needed
        if project_name:
            memories = [m for m in memories if m.get('project_name') == project_name]

        return [self._memory_to_index(m) for m in memories[:limit]]

    def _memory_to_index(self, memory_dict: Dict[str, Any]) -> MemoryIndex:
        """Convert database row to MemoryIndex."""
        # Convert integer priority back to enum
        priority_int = memory_dict.get('priority', 5)
        if priority_int >= 9:
            priority = Priority.CRITICAL
        elif priority_int >= 7:
            priority = Priority.HIGH
        elif priority_int >= 4:
            priority = Priority.MEDIUM
        else:
            priority = Priority.LOW

        # Handle datetime conversion
        created_at = memory_dict['created_at']
        if isinstance(created_at, str):
            created_at = datetime.fromisoformat(created_at)
        elif not isinstance(created_at, datetime):
            created_at = datetime.now()

        return MemoryIndex(
            id=str(memory_dict['id']),
            title=memory_dict.get('title'),
            memory_type=MemoryType(memory_dict['memory_type']),
            priority=priority,
            tags=memory_dict.get('tags', []),
            created_at=created_at,
            preview=memory_dict.get('content', '')[:100]
        )

    def _dict_to_memory(self, memory_dict: Dict[str, Any]) -> Memory:
        """Convert database row to Memory object."""
        # Convert integer priority back to enum
        priority_int = memory_dict.get('priority', 5)
        if priority_int >= 9:
            priority = Priority.CRITICAL
        elif priority_int >= 7:
            priority = Priority.HIGH
        elif priority_int >= 4:
            priority = Priority.MEDIUM
        else:
            priority = Priority.LOW

        # Deserialize embedding from bytes if present
        embedding = None
        if memory_dict.get('embedding'):
            try:
                import json
                embedding = json.loads(memory_dict['embedding'].decode('utf-8'))
            except Exception:
                pass

        # Handle datetime conversion
        created_at = memory_dict['created_at']
        if isinstance(created_at, str):
            created_at = datetime.fromisoformat(created_at)
        elif not isinstance(created_at, datetime):
            created_at = datetime.now()

        updated_at = memory_dict['updated_at']
        if isinstance(updated_at, str):
            updated_at = datetime.fromisoformat(updated_at)
        elif not isinstance(updated_at, datetime):
            updated_at = datetime.now()

        return Memory(
            id=str(memory_dict['id']),
            content=memory_dict['content'],
            memory_type=MemoryType(memory_dict['memory_type']),
            namespace=memory_dict['namespace'],
            priority=priority,
            title=memory_dict.get('title'),
            tags=memory_dict.get('tags', []),
            agent_id=memory_dict.get('agent_id'),
            session_id=memory_dict.get('session_id'),
            project_name=memory_dict.get('project_name'),
            created_at=created_at,
            updated_at=updated_at,
            metadata={},  # Database doesn't store metadata separately
            embedding=embedding
        )



# Convenience functions for quick usage

_default_memory = None


def get_default_memory() -> DivergeMemory:
    """Get or create default memory instance."""
    global _default_memory
    if _default_memory is None:
        _default_memory = DivergeMemory()
    return _default_memory


def store(content: str, **kwargs) -> str:
    """Convenience function to store memory using default instance."""
    return get_default_memory().store(content, **kwargs)


def search(query: str, **kwargs) -> List[MemoryIndex]:
    """Convenience function to search using default instance."""
    return get_default_memory().search(query, **kwargs)


def retrieve(memory_ids: List[str]) -> List[Memory]:
    """Convenience function to retrieve using default instance."""
    return get_default_memory().retrieve(memory_ids)
