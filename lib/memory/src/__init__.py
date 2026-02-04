"""
Diverga Memory System v8.0 - Source modules

v8.0 Additions:
- database: SQLite storage with FTS5 and vector support
- sync_dao: YAML → DB synchronization with idempotency
- doc_generator: Researcher-friendly Markdown generation
"""

from .models import *
from .context_trigger import *
from .task_interceptor import *
from .checkpoint_trigger import *
from .fs_state import *
from .dual_tree import *
from .archive import *
from .decision_log import *
from .session_hooks import *
from .schema import *
from .templates import *
from .artifact_generator import *
from .cli import *
from .migration import *

# v8.0 additions
from .database import MemoryDatabase
from .sync_dao import SyncDAO, sync_project
from .doc_generator import DocGenerator, generate_docs
from .hybrid_search import HybridSearch, create_hybrid_search
from .paper_lineage import PaperLineage, generate_prisma_mermaid

# Optional imports (may not be available if dependencies missing)
try:
    from .local_embedder import LocalEmbedder, is_embeddings_available
except ImportError:
    LocalEmbedder = None
    is_embeddings_available = lambda: False
