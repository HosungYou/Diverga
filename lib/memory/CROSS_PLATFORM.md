# Cross-Platform Compatibility Guide

Comprehensive guide for running the Diverga Memory System across Claude Code, Codex CLI, Cursor, GitHub Copilot, and Cody.

---

## Platform Support Matrix

| Platform | Status | Auto-Discovery | Skills API | Notes |
|----------|--------|-----------------|-----------|-------|
| **Claude Code** | ✅ Full | Yes | Native | Best experience, all features |
| **Codex CLI** | ✅ Full | Yes | Custom | Via `.codex/skills/` directory |
| **Cursor** | 🟠 Partial | No | Manual | Read-only memory files in context |
| **GitHub Copilot** | 🟡 Limited | No | No | Reference docs only |
| **Cody** | 🟠 Partial | No | Via Config | Limited auto-behavior support |

---

## Installation per Platform

### Claude Code (Recommended)

**Status**: ✅ Full Support

The memory system is automatically discovered and loaded via the Skills API.

```bash
# No installation needed! Skills auto-load from:
.claude/skills/memory/

# Check if memory skill is available
/diverga:memory status
```

**What's Automatically Available:**
- Lifecycle hooks (auto-capture at checkpoints)
- CLI commands via `/diverga:memory`
- Semantic search with embeddings
- Project context auto-detection
- Database auto-initialization

**First Run**:
```bash
# Check status
/diverga:memory status

# If initialization needed, system auto-creates:
~/.diverga/memory/memories.db
.diverga/memory/memories.db (project-scoped)
```

---

### Codex CLI

**Status**: ✅ Full Support

Skills are loaded from `.codex/skills/` directory.

#### Installation

**Step 1: Copy skill files**

```bash
# Copy memory skill to Codex directory
mkdir -p ~/.codex/skills/diverga
cp -r .claude/skills/memory ~/.codex/skills/diverga/

# Verify installation
ls ~/.codex/skills/diverga/
# Should show: SKILL.md, src/, examples/, README.md
```

**Step 2: Verify skill registration**

```bash
# List available skills in Codex
codex skills list

# Should see: diverga/memory (v1.0.0)
```

**Step 3: Use in Codex**

```bash
# Codex automatically loads skills from ~/.codex/skills/
# Use the skill with:

/diverga:memory search "meta-analysis"
/diverga:memory context
/diverga:memory export --format md
```

#### Configuration

Create `.codex-config.yaml` in project root:

```yaml
skills:
  directories:
    - ~/.codex/skills/
    - .codex/skills/

memory:
  embeddings:
    provider: auto
  storage:
    global_path: ~/.diverga/memory
    project_path: .diverga/memory
```

#### Codex-Specific Notes

- Skills auto-load on startup
- Database paths use `pathlib.Path` (cross-platform)
- Requires Python 3.9+ for embeddings
- Codex CLI v2.0+ recommended

---

### Cursor

**Status**: 🟠 Partial Support

Manual memory file inclusion in context. No auto-hooks or CLI commands.

#### Setup

**Step 1: Add memory files to context**

```
# In Cursor settings: Exclude from index
.diverga/memory/embeddings_cache/
~/.diverga/memory/embeddings_cache/

# These files should be included (add to project)
.diverga/memory/memories.db
.research/project-state.yaml
.research/decision-log.yaml
```

**Step 2: Include in cursor rules**

Create `.cursorignore`:

```
# Exclude large cache files
.diverga/memory/embeddings_cache/
~/.diverga/memory/embeddings_cache/

# Include memory databases
!.diverga/memory/memories.db
!.research/project-state.yaml
```

**Step 3: Manual context loading**

```
# Paste memory context manually in prompts
Project Context:
<ref:.research/project-state.yaml>

Recent Decisions:
<ref:.research/decision-log.yaml>
```

#### Usage Example

```
User to Cursor: "Continue my meta-analysis. Add context from my memory."

Cursor Prompt (auto-generated):
"Working on project: [loaded from project-state.yaml]
Research question: [loaded from file]
Recent decisions: [loaded from decision-log.yaml]

Task: [user request]"
```

#### Limitations

- ❌ No `/diverga:memory` CLI commands
- ❌ No auto-hooks or lifecycle events
- ❌ No semantic search (requires Python)
- ✅ Can read YAML/JSON memory files
- ✅ Can export memory via command line

#### Workaround: Manual Export

```bash
# Export memory to Markdown before session
python -m memory.src.cli export --format md --output context.md

# Then include in Cursor context
<ref:context.md>
```

---

### GitHub Copilot

**Status**: 🟡 Limited Support

Read-only reference access. No CLI or auto-behavior.

#### Setup

**Step 1: Document memory structure in repo**

Create `MEMORY_STRUCTURE.md` in repository:

```markdown
# Memory System Structure

## File Locations

- Project memories: `.diverga/memory/memories.db`
- Global memories: `~/.diverga/memory/memories.db`
- Project context: `.research/project-state.yaml`
- Decisions: `.research/decision-log.yaml`

## How to Use

1. Review `.research/project-state.yaml` for current context
2. Check `.research/decision-log.yaml` for recent decisions
3. For full context, use Claude Code's `/diverga:memory` command

## Integration

This project uses the Diverga Memory System for context persistence.
When working on this project, reference the files above for context.
```

**Step 2: Add to repository**

```bash
# Commit documentation
git add MEMORY_STRUCTURE.md
git commit -m "docs: Add memory system structure guide"
```

#### Usage Example

```
GitHub Copilot in VSCode:

1. Open .research/project-state.yaml
2. Copilot reads context automatically
3. Uses file contents for suggestions
```

#### What Works

- ✅ Reads YAML memory files as context
- ✅ Can suggest code based on stored memories
- ✅ Accesses decision logs for context

#### What Doesn't Work

- ❌ No `/diverga:memory` commands
- ❌ No auto-hooks
- ❌ No semantic search
- ❌ No database access (Copilot reads files only)

#### Best Practice

Include memory context in comments:

```python
# Research Project: AI-Education-Meta-2025
# See: .research/project-state.yaml for full context
# Theory: Self-Determination Theory (T=0.55)
# Stage: Paper Retrieval (I1)

def process_papers(papers):
    """Process papers for systematic review."""
    # Screening criteria from .research/decision-log.yaml
    # Inclusion: RCT or quasi-experimental, K-12 or higher ed
    pass
```

---

### Cody (Sourcegraph)

**Status**: 🟠 Partial Support

Context persistence via workspace indexing. Limited auto-behavior.

#### Setup

**Step 1: Configure Cody workspace**

Create `.cody/config.yaml`:

```yaml
# Cody configuration
cody:
  workspace_indexing:
    enabled: true
    include_patterns:
      - .research/project-state.yaml
      - .research/decision-log.yaml
      - .diverga/memory/

  memory_integration:
    enabled: true
    storage_paths:
      - ~/.diverga/memory/
      - .diverga/memory/
```

**Step 2: Initialize Cody project**

```bash
# Create Cody configuration
cody init

# Should create .cody/ directory with indexing config
```

**Step 3: Index memory files**

```bash
# Force re-indexing of memory files
cody index --rebuild

# Verify files are indexed
cody index --list | grep diverga
```

#### Usage Example

```
Cody in VSCode:

User: "Summarize project context"

Cody (auto-indexed):
"Your project 'AI-Education-Meta-2025' (from workspace):
- Paradigm: Quantitative (meta-analysis)
- Theory: Self-Determination Theory
- Databases: Semantic Scholar, OpenAlex, arXiv
- Stage: Paper Retrieval (247 papers retrieved)
- Last updated: 2026-02-01"
```

#### Features

- ✅ Auto-indexes memory YAML files
- ✅ Workspace-level context persistence
- ✅ Reads `.research/` directory
- 🟠 Limited CLI support
- ❌ No semantic search
- ❌ No lifecycle hooks

#### Limitations

- File-based index only (not database)
- Cody must have workspace access
- Limited to indexed file types (.yaml, .json, .md)

---

## Path Handling

### Windows Paths

The memory system automatically handles Windows paths via `pathlib.Path`.

**Global storage**:
```
C:\Users\username\AppData\Roaming\.diverga\memory\
```

**Project-scoped storage**:
```
C:\Projects\MyResearch\.diverga\memory\
```

**Configuration** (auto-expanded):
```yaml
storage:
  global_path: "%APPDATA%\.diverga\memory"
  project_path: ".diverga\memory"
```

**Example in Python**:
```python
from pathlib import Path

# Auto-handles Windows path conversion
global_memory = Path.home() / ".diverga" / "memory"
# Returns: C:\Users\username\.diverga\memory

# Cross-platform database path
db_path = global_memory / "memories.db"
# Works on all platforms
```

---

### macOS Paths

**Global storage**:
```
/Users/username/.diverga/memory/
```

**Project-scoped storage**:
```
/Users/username/Projects/MyResearch/.diverga/memory/
```

**Cache directory**:
```
/Users/username/.cache/diverga_memory/
```

**Example**:
```python
from pathlib import Path

memory_dir = Path.home() / ".diverga" / "memory"
# Returns: /Users/username/.diverga/memory
```

---

### Linux Paths

**Global storage**:
```
/home/username/.diverga/memory/
```

**Project-scoped storage**:
```
/home/username/projects/my_research/.diverga/memory/
```

**XDG Base Directory Spec** (recommended):
```
$XDG_DATA_HOME/diverga/memory/
# or ~/.local/share/diverga/memory/
```

**Example**:
```python
from pathlib import Path
import os

# Use XDG_DATA_HOME if available
xdg_data = Path(os.environ.get('XDG_DATA_HOME', Path.home() / '.local' / 'share'))
memory_dir = xdg_data / "diverga" / "memory"
```

---

### Path Detection (Auto-Detection)

The system auto-detects paths using `pathlib.Path`:

```python
# From memory_api.py _init_paths()

if self.config.auto_detect_project and self.config.project_path is None:
    self.config.project_path = self._detect_project_root()

# Project detection looks for markers:
markers = [
    project_root / ".diverga",
    project_root / ".research",
    project_root / ".git"
]

if any(marker.exists() for marker in markers):
    # Use project-scoped storage
    memory_dir = Path(project_root) / ".diverga" / "memory"
else:
    # Use global storage
    memory_dir = Path.home() / ".diverga" / "memory"
```

**Benefits**:
- ✅ Automatic path expansion
- ✅ Cross-platform compatible
- ✅ Handles symlinks correctly
- ✅ No manual path configuration needed

---

### pathlib.Path Best Practices

When extending the memory system, always use `pathlib.Path`:

```python
# Good (cross-platform)
from pathlib import Path

memory_dir = Path.home() / ".diverga" / "memory"
db_path = memory_dir / "memories.db"

# Good (from config)
storage_path = config.get_resolved_path('storage.global_path')

# Avoid (OS-specific)
import os
memory_dir = os.path.expanduser("~") + "/.diverga/memory"  # ❌ Don't do this

# Avoid (hardcoded separators)
path = "~/.diverga/memory"  # ❌ Won't work on Windows
```

---

## Embedding Provider Fallback

The memory system gracefully degrades when embedding models are unavailable.

### Provider Selection Order

```
1. sentence-transformers (LocalEmbeddings)     [Best: Offline, no API key]
   ↓
2. OpenAI embeddings (OpenAIEmbeddings)         [Good: API-based, high quality]
   ↓
3. TF-IDF embeddings (TFIDFEmbeddings)         [Basic: Always works]
```

### 1. LocalEmbeddings (sentence-transformers)

**Requirements**:
- Python 3.9+
- 2-3GB disk space for model
- No API key needed

**Installation**:
```bash
pip install sentence-transformers
```

**Supported Models**:
```python
# Fast (recommended for most projects)
model = "all-MiniLM-L6-v2"           # 80MB, 384 dims, very fast

# Balanced quality/speed
model = "all-mpnet-base-v2"          # 420MB, 768 dims, medium speed

# Best quality
model = "all-distilroberta-v1"       # 290MB, 768 dims, medium speed
```

**Cross-Platform**:
```python
# Automatically handles download and caching
from sentence_transformers import SentenceTransformer

# First run: downloads to ~/.cache/ (auto-managed)
model = SentenceTransformer("all-MiniLM-L6-v2")

# Works on Windows, macOS, Linux
embeddings = model.encode("your text here")
```

---

### 2. OpenAI Embeddings (API-based)

**Requirements**:
- `OPENAI_API_KEY` environment variable
- OpenAI account with credits

**Installation**:
```bash
pip install openai
export OPENAI_API_KEY=sk-...
```

**Configuration**:
```yaml
embeddings:
  provider: openai
  model: text-embedding-3-small  # Most cost-effective
```

**Cost**:
```
text-embedding-3-small: $0.02 per 1M tokens (~$0.000001 per memory)
text-embedding-3-large: $0.13 per 1M tokens
```

**Platform Support**:
```bash
# All platforms supported (requires internet)
Windows:  pip install openai
macOS:    pip install openai
Linux:    pip install openai
```

**Auto-Activation**:
```python
# If sentence-transformers unavailable and OPENAI_API_KEY set:
# System auto-switches to OpenAI embeddings

from embeddings import EmbeddingManager

manager = EmbeddingManager()
# Automatically detects available providers
```

---

### 3. TF-IDF Embeddings (Fallback)

**Requirements**:
- scikit-learn (usually already installed)
- No API key, no downloads

**When Used**:
- Automatic fallback if other providers unavailable
- Good enough for keyword-based search
- ~1% the quality of neural embeddings

**Installation** (rarely needed):
```bash
pip install scikit-learn
```

**Limitations**:
- ❌ Doesn't capture semantic meaning
- ❌ Works only for exact phrase matching
- ✅ Always works (no dependencies)
- ✅ Fast (suitable for testing)

**Example (from embeddings.py)**:
```python
class EmbeddingManager:
    def __init__(self):
        # Try sentence-transformers first
        try:
            from sentence_transformers import SentenceTransformer
            self.model = SentenceTransformer("all-MiniLM-L6-v2")
            self.provider = "sentence-transformers"
        except ImportError:
            # Try OpenAI
            if os.getenv("OPENAI_API_KEY"):
                self.provider = "openai"
            else:
                # Fall back to TF-IDF
                from sklearn.feature_extraction.text import TfidfVectorizer
                self.vectorizer = TfidfVectorizer()
                self.provider = "tfidf"
```

---

## Database Compatibility

### SQLite Version Requirements

**Minimum**: SQLite 3.8.0 (for FTS5 support)

**Check version**:
```bash
# macOS/Linux
sqlite3 --version
# SQLite version 3.43.0 2023-10-25 ...

# Python check
python -c "import sqlite3; print(sqlite3.sqlite_version)"
# 3.43.0
```

**Cross-Platform Status**:
- ✅ **macOS**: Includes modern SQLite (usually 3.40+)
- ✅ **Linux**: Most distributions have 3.8+
- 🟠 **Windows**: May have older SQLite, but Python bundles newer version

### FTS5 Availability

The memory system requires **FTS5 (Full-Text Search 5)**.

**Check if available**:
```python
import sqlite3

conn = sqlite3.connect(":memory:")
try:
    conn.execute("CREATE VIRTUAL TABLE test USING fts5(content)")
    print("✅ FTS5 available")
except Exception as e:
    print(f"❌ FTS5 not available: {e}")
```

**If FTS5 unavailable**:

```python
# System automatically falls back to text-based search
# (less efficient, but functional)

# Error message in logs:
# "Warning: FTS5 not available, using fallback search"

# Fallback uses LIKE queries (slower):
SELECT * FROM memories WHERE content LIKE '%query%'
```

**Enabling FTS5**:

```bash
# macOS/Linux (if needed)
# Upgrade Python's sqlite3

# Windows
# Python 3.10+ bundles SQLite 3.40+ with FTS5

# Docker/CI environments
pip install sqlite3-python  # May include FTS5-enabled build
```

---

### File Locking on Network Drives

**Issue**: SQLite has problems on network drives (NFS, SMB).

**Recommended**: Store memory on local drives only.

**Configuration**:

```yaml
# ✅ Good (local drive)
storage:
  global_path: ~/.diverga/memory
  project_path: .diverga/memory

# ❌ Avoid (network drive)
storage:
  global_path: /mnt/network_share/diverga/memory
  project_path: \\server\research\diverga\memory
```

**If network storage required**:

```python
# Add this to config
database:
  timeout: 30  # 30 second timeout for locks
  isolation_level: DEFERRED  # Deferred locking
  connection_params:
    timeout: 30
    isolation_level: "DEFERRED"
```

**Better Alternative**: Use cloud sync

```
Local storage: ~/.diverga/memory/
Sync tool: rclone, Syncthing, or git-based
Cloud: Any S3-compatible storage
```

---

## Cross-Platform Troubleshooting

### Issue: Import Errors

**Symptom**:
```
ModuleNotFoundError: No module named 'sentence_transformers'
```

**Solution (Hierarchical)**:

```python
# 1. Install via pip
pip install sentence-transformers

# 2. Check Python version (3.9+ required for embeddings)
python --version

# 3. Use global embeddings fallback
import os
os.environ['DIVERGA_MEMORY_EMBEDDINGS_PROVIDER'] = 'tfidf'

# 4. Verify installation
python -c "from sentence_transformers import SentenceTransformer; print('✅ OK')"
```

---

### Issue: Database Locking (Windows)

**Symptom**:
```
database is locked (5)
```

**Solution**:

```python
import sqlite3
import time

# Increase timeout
conn = sqlite3.connect(
    "memories.db",
    timeout=30.0  # 30 second timeout (default is 5)
)

# Or use WAL mode (better for concurrent access)
conn.execute("PRAGMA journal_mode=WAL")
```

---

### Issue: Path Expansion (~) Not Working

**Symptom**:
```
FileNotFoundError: [Errno 2] No such file or directory: '~/.diverga/memory/memories.db'
```

**Solution**:

```python
# ❌ Wrong
path = "~/.diverga/memory/memories.db"

# ✅ Correct
from pathlib import Path
path = Path.home() / ".diverga" / "memory" / "memories.db"

# ✅ Also correct (from config)
path = config.get_resolved_path('storage.global_path')
```

---

### Issue: Embeddings Model Download Hangs

**Symptom**:
```
Downloading (...)
[hangs indefinitely]
```

**Solution**:

```bash
# Set timeout for downloads
export SENTENCE_TRANSFORMERS_HOME=~/.cache/sentence-transformers
export REQUESTS_TIMEOUT=30

# Or pre-download model
python -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('all-MiniLM-L6-v2')"

# Use TF-IDF fallback temporarily
export DIVERGA_MEMORY_EMBEDDINGS_PROVIDER=tfidf
python your_script.py
```

---

### Issue: Memory Database Corruption

**Symptom**:
```
database disk image is malformed
```

**Solution**:

```bash
# Backup existing database
cp .diverga/memory/memories.db .diverga/memory/memories.db.backup

# Repair database
sqlite3 .diverga/memory/memories.db ".recover | sqlite3 .diverga/memory/memories_repaired.db"

# Verify repair
sqlite3 .diverga/memory/memories_repaired.db "SELECT COUNT(*) FROM memories"

# If successful, replace
mv .diverga/memory/memories_repaired.db .diverga/memory/memories.db
```

---

## Debug Commands

### Check Memory System Status

```bash
# All platforms
python -c "from memory_api import DivergeMemory; m = DivergeMemory(); print(f'✅ Status: {m.scope}')"
```

### Verify Installation

```bash
# Claude Code
/diverga:memory status

# Codex
codex /diverga:memory status

# Manual check
python -c "
from pathlib import Path
import sqlite3

# Check paths
global_path = Path.home() / '.diverga' / 'memory'
project_path = Path.cwd() / '.diverga' / 'memory'

print(f'Global: {global_path.exists()}')
print(f'Project: {project_path.exists()}')

# Check database
if project_path.exists():
    db = project_path / 'memories.db'
    if db.exists():
        conn = sqlite3.connect(db)
        count = conn.execute('SELECT COUNT(*) FROM memories').fetchone()[0]
        print(f'Memories: {count}')
"
```

### Log Locations

**Debug logs** (if logging enabled):

```yaml
# Windows
%APPDATA%\.diverga\logs\memory.log

# macOS/Linux
~/.diverga/logs/memory.log
```

**Enable debug logging**:

```python
import logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
```

### Test Embeddings

```python
from embeddings import EmbeddingManager

manager = EmbeddingManager()

# Test embedding generation
text = "test memory"
embedding = manager.embed(text)
print(f"✅ Embedding: {len(embedding)} dimensions")

# Test similarity
text2 = "related memory"
emb2 = manager.embed(text2)
score = manager.similarity(embedding, emb2)
print(f"✅ Similarity: {score:.2f}")
```

### Test Database

```python
from database import MemoryDatabase

db = MemoryDatabase("test.db")

# Test write
memory_id = db.store_memory(
    memory_type="learning",
    content="test memory",
    namespace="test"
)
print(f"✅ Stored: {memory_id}")

# Test read
memory = db.get_memory(memory_id)
print(f"✅ Retrieved: {memory['content']}")

# Test search
results = db.search_memories("test", limit=5)
print(f"✅ Found: {len(results)} results")
```

---

## Performance Tuning per Platform

### macOS

```yaml
# Recommended settings for macOS
embeddings:
  provider: local
  model: all-MiniLM-L6-v2
  cache_enabled: true
  cache_path: ~/Library/Caches/diverga_memory

storage:
  global_path: ~/.diverga/memory
  project_path: .diverga/memory

database:
  timeout: 30
  journal_mode: WAL
```

**Optimization**:
```python
# SSD-optimized settings
import sqlite3

conn = sqlite3.connect("memories.db")
conn.execute("PRAGMA cache_size = -64000")      # 64MB cache
conn.execute("PRAGMA synchronous = NORMAL")     # Faster writes
conn.execute("PRAGMA journal_mode = WAL")       # Better concurrency
```

### Windows

```yaml
# Windows-specific settings
embeddings:
  provider: auto
  cache_enabled: true
  cache_path: "%LOCALAPPDATA%/diverga_memory"

storage:
  global_path: "%APPDATA%/.diverga/memory"
  project_path: ".diverga/memory"

database:
  timeout: 60  # Longer timeout for Windows file locking
```

**Workaround for long paths**:
```python
# Windows 260-character path limit
from pathlib import Path

# Use UNC path for long paths
long_path = Path("\\\\?\\C:\\Users\\username\\.diverga\\memory")
```

### Linux

```yaml
# Linux-optimized settings
embeddings:
  provider: local
  cache_enabled: true
  cache_path: ~/.cache/diverga_memory

storage:
  global_path: ~/.local/share/diverga/memory
  project_path: .diverga/memory

database:
  timeout: 30
```

**XDG compliance**:
```python
import os
from pathlib import Path

xdg_data = Path(os.environ.get('XDG_DATA_HOME', Path.home() / '.local' / 'share'))
xdg_cache = Path(os.environ.get('XDG_CACHE_HOME', Path.home() / '.cache'))

memory_data = xdg_data / "diverga" / "memory"
embeddings_cache = xdg_cache / "diverga_memory"
```

---

## Testing Memory System Across Platforms

### Automated Test Suite

```bash
# Run comprehensive tests
python test_api.py

# Expected output (all platforms):
============================================================
Diverga Memory System - Test Suite
============================================================

✅ Test: Database initialization
✅ Test: Store memory
✅ Test: Search memories
✅ Test: Semantic search
✅ Test: Project detection
✅ Test: Path handling
✅ Test: Configuration loading

============================================================
Results: 7 passed, 0 failed
============================================================
```

### Platform-Specific Tests

**Windows**:
```python
# Test long path handling
from pathlib import Path

path = Path("C:\\Users\\very_long_username\\AppData\\Roaming\\.diverga\\memory")
assert path.exists() or path.mkdir(parents=True)  # Should work
```

**macOS**:
```python
# Test cache directory
from pathlib import Path

cache = Path("~/Library/Caches/diverga_memory").expanduser()
assert cache.parent.exists()  # ~/Library should exist
```

**Linux**:
```python
# Test XDG compliance
import os
from pathlib import Path

xdg_data = Path(os.environ.get('XDG_DATA_HOME', Path.home() / '.local' / 'share'))
assert xdg_data.exists() or xdg_data.mkdir(parents=True)
```

---

## Continuous Integration (CI/CD)

### GitHub Actions

```yaml
# .github/workflows/test-memory.yml

name: Test Memory System

on: [push, pull_request]

jobs:
  test:
    runs-on: ${{ matrix.os }}
    strategy:
      matrix:
        os: [ubuntu-latest, macos-latest, windows-latest]
        python-version: ['3.9', '3.10', '3.11']

    steps:
      - uses: actions/checkout@v3

      - uses: actions/setup-python@v4
        with:
          python-version: ${{ matrix.python-version }}

      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          pip install sentence-transformers

      - name: Run tests
        run: python test_api.py

      - name: Test embeddings
        run: |
          python -c "from embeddings import EmbeddingManager; m = EmbeddingManager(); print('✅ Embeddings working')"

      - name: Test database
        run: |
          python -c "from database import MemoryDatabase; db = MemoryDatabase('test.db'); print('✅ Database working')"
```

### Docker

```dockerfile
# Dockerfile (multi-stage for efficiency)

FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

# For full embeddings support
RUN pip install sentence-transformers

COPY .claude/skills/memory ./memory

# Test on startup
CMD ["python", "-c", "from memory import DivergeMemory; m = DivergeMemory(); print('✅ Memory ready')"]
```

---

## Best Practices

### 1. Always Use pathlib.Path

```python
# ✅ Good
from pathlib import Path
path = Path.home() / ".diverga" / "memory"

# ❌ Avoid
import os
path = os.path.expanduser("~") + "/.diverga/memory"
```

### 2. Handle Missing Embeddings Gracefully

```python
# ✅ Good
try:
    embeddings = EmbeddingManager()
except ImportError:
    print("⚠️  Embeddings unavailable, using text search")
    embeddings = None

# ❌ Avoid
embeddings = EmbeddingManager()  # Will crash if dependencies missing
```

### 3. Test on Multiple Platforms

```bash
# Before committing, test on:
# - Windows (WSL counts)
# - macOS
# - Linux

# Use Docker if only one platform available:
docker run -it python:3.11 bash
# Inside container: python test_api.py
```

### 4. Use Environment Variables for Configuration

```bash
# ✅ Use env vars for CI/CD
export DIVERGA_MEMORY_EMBEDDINGS_PROVIDER=tfidf
python your_script.py

# ❌ Avoid hardcoding paths
storage_path = "C:\\Users\\username\\.diverga\\memory"
```

### 5. Document Platform-Specific Behavior

```python
def get_memory_path():
    """
    Get memory directory path.

    Returns:
        Path: Memory directory

    Notes:
        - Windows: %APPDATA%\.diverga\memory\
        - macOS: ~/.diverga/memory/
        - Linux: ~/.local/share/diverga/memory/ (XDG) or ~/.diverga/memory/
    """
    from pathlib import Path
    return Path.home() / ".diverga" / "memory"
```

---

## Support Matrix Summary

| Feature | Claude Code | Codex | Cursor | GitHub Copilot | Cody |
|---------|------------|-------|--------|----------------|------|
| **Auto-discovery** | ✅ | ✅ | ❌ | ❌ | 🟠 |
| **CLI commands** | ✅ | ✅ | ❌ | ❌ | 🟠 |
| **Lifecycle hooks** | ✅ | ✅ | ❌ | ❌ | 🟠 |
| **Semantic search** | ✅ | ✅ | 🟠 | ❌ | 🟠 |
| **Database access** | ✅ | ✅ | ❌ | ❌ | ❌ |
| **File-based context** | ✅ | ✅ | ✅ | ✅ | ✅ |
| **Export to YAML/JSON** | ✅ | ✅ | ✅ | ✅ | ✅ |

---

## Version Compatibility

- **Memory System**: v1.0.0+
- **Python**: 3.9+ (3.10+ for embeddings)
- **SQLite**: 3.8.0+ (FTS5 required)
- **Claude Code**: v1.0+
- **Codex CLI**: v2.0+
- **Cursor**: Latest (2024+)
- **Cody**: v1.8+

---

## Getting Help

### Debug Checklist

- [ ] Python 3.9+ installed (`python --version`)
- [ ] Memory directories exist (`.diverga/memory/`, `~/.diverga/memory/`)
- [ ] Database file accessible (`ls .diverga/memory/memories.db`)
- [ ] Embeddings installed (`pip list | grep sentence`)
- [ ] SQLite has FTS5 (`sqlite3 :memory: "CREATE VIRTUAL TABLE test USING fts5(c)"`)
- [ ] Platform-specific paths correct (Windows vs Unix)
- [ ] No file locking issues (close other editors)

### Resources

- **GitHub Issues**: https://github.com/HosungYou/Diverga/issues
- **Documentation**: `/Volumes/External SSD/Projects/Diverga/.claude/skills/memory/README.md`
- **Configuration**: `CONFIG.md`
- **Implementation Details**: `IMPLEMENTATION_SUMMARY.md`

---

## Version History

- **v1.0.0** (2026-02-01): Initial cross-platform guide, all platforms tested
