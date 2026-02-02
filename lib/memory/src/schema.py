"""
Data schema for Diverga Memory System.

Defines the structure for memories, decisions, sessions, and context.
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, Dict, Any, List
from enum import Enum


class MemoryType(str, Enum):
    """Types of memories that can be stored."""
    LEARNING = "learning"
    DECISION = "decision"
    ISSUE = "issue"
    PROBLEM = "problem"
    PATTERN = "pattern"
    SOLUTION = "solution"
    CONTEXT = "context"


class DecisionType(str, Enum):
    """Types of architectural decisions."""
    ARCHITECTURE = "architecture"
    DESIGN = "design"
    IMPLEMENTATION = "implementation"
    REFACTORING = "refactoring"
    DEBUGGING = "debugging"
    OPTIMIZATION = "optimization"


class Priority(str, Enum):
    """Priority levels for memories."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class SearchScope(str, Enum):
    """Scope for memory search."""
    PROJECT = "project"  # Current project only
    GLOBAL = "global"    # All projects
    BOTH = "both"        # Project + global


@dataclass
class Memory:
    """Complete memory record with full details."""
    id: str
    content: str
    memory_type: MemoryType
    namespace: str
    priority: Priority
    title: Optional[str]
    tags: List[str]
    agent_id: Optional[str]
    session_id: Optional[str]
    project_name: Optional[str]
    created_at: datetime
    updated_at: datetime
    metadata: Dict[str, Any] = field(default_factory=dict)
    embedding: Optional[List[float]] = None


@dataclass
class MemoryIndex:
    """Compact memory reference for search results (token-efficient)."""
    id: str
    title: Optional[str]
    memory_type: MemoryType
    priority: Priority
    tags: List[str]
    created_at: datetime
    similarity_score: Optional[float] = None
    preview: Optional[str] = None  # First 100 chars


@dataclass
class MemoryContext:
    """Surrounding context for a memory (medium detail)."""
    memory: Memory
    related_memories: List[MemoryIndex]
    session_context: Optional[str] = None
    project_context: Optional[str] = None


@dataclass
class Decision:
    """Architectural decision record."""
    id: str
    stage: str
    agent_id: str
    decision_type: DecisionType
    description: str
    before_state: Optional[str]
    after_state: Optional[str]
    rationale: str
    t_score: Optional[float]
    created_at: datetime
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class Session:
    """Session record with summary and decisions."""
    id: str
    summary: str
    agents_used: List[str]
    decisions: List[str]  # Decision IDs
    started_at: datetime
    ended_at: Optional[datetime]
    project_name: Optional[str]
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ProjectContext:
    """High-level project context summary."""
    project_name: str
    total_memories: int
    recent_decisions: List[Decision]
    key_patterns: List[MemoryIndex]
    active_sessions: List[Session]
    last_updated: datetime
