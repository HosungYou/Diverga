"""
Diverga Memory System - Context persistence for research workflows.

Main API:
    DivergeMemory - Primary interface for memory operations

Schema:
    Memory, MemoryIndex, MemoryContext - Memory data types
    Decision, Session, ProjectContext - Supporting data types
    MemoryType, DecisionType, Priority, SearchScope - Enums

Database:
    MemoryDatabase - SQLite storage backend

Embeddings:
    EmbeddingManager - Semantic search with multiple providers

Hooks:
    MemoryHooks - Lifecycle hooks for Claude Code/Codex integration
    ContextInjection - Context to inject into agent prompts

Usage:
    from diverga.memory import DivergeMemory, MemoryType, Priority

    # Initialize
    memory = DivergeMemory()

    # Store
    memory_id = memory.store(
        content="Used regression analysis",
        memory_type=MemoryType.DECISION,
        namespace="analysis.statistical",
        priority=Priority.HIGH
    )

    # Search (3-layer retrieval)
    results = memory.search("regression", limit=5)  # Layer 1: Compact
    context = memory.get_context(results[0].id)     # Layer 2: Context
    full = memory.retrieve([memory_id])              # Layer 3: Full details

    # Lifecycle hooks
    from diverga.memory import MemoryHooks

    hooks = MemoryHooks()
    context = hooks.on_session_start(project_path="/path/to/project")
    print(context.to_prompt())  # Inject into agent prompt
"""

from .memory_api import (
    DivergeMemory,
    DivergeMemoryConfig,
    get_default_memory,
    store,
    search,
    retrieve
)

from .schema import (
    Memory,
    MemoryIndex,
    MemoryContext,
    Decision,
    Session,
    ProjectContext,
    MemoryType,
    DecisionType,
    Priority,
    SearchScope
)

from .database import MemoryDatabase

from .embeddings import (
    EmbeddingManager,
    EmbeddingProvider,
    LocalEmbeddings,
    OpenAIEmbeddings,
    TFIDFEmbeddings
)

from .hooks import (
    MemoryHooks,
    ContextInjection,
    get_default_hooks,
    on_session_start,
    on_checkpoint_reached,
    on_session_end
)

from .config import (
    MemoryConfig,
    Config,
    get_config
)

__all__ = [
    # Main API
    'DivergeMemory',
    'DivergeMemoryConfig',
    'get_default_memory',
    'store',
    'search',
    'retrieve',

    # Schema types
    'Memory',
    'MemoryIndex',
    'MemoryContext',
    'Decision',
    'Session',
    'ProjectContext',

    # Enums
    'MemoryType',
    'DecisionType',
    'Priority',
    'SearchScope',

    # Backend components
    'MemoryDatabase',
    'EmbeddingManager',
    'EmbeddingProvider',
    'LocalEmbeddings',
    'OpenAIEmbeddings',
    'TFIDFEmbeddings',

    # Lifecycle hooks
    'MemoryHooks',
    'ContextInjection',
    'get_default_hooks',
    'on_session_start',
    'on_checkpoint_reached',
    'on_session_end',

    # Configuration
    'MemoryConfig',
    'Config',
    'get_config',
]

__version__ = '1.0.0'
