# Diverga Memory Configuration System

Comprehensive configuration management for the Diverga Memory System with multi-layer override support.

## Quick Start

```python
from config import get_config

# Load configuration (auto-merges global + project + env)
config = get_config()

# Get values using dot notation
provider = config.get('embeddings.provider')  # "auto"
limit = config.get('search.default_limit')    # 10

# Set values
config.set('embeddings.provider', 'openai')
config.set('search.default_limit', 20)

# Save configuration
config.save()  # Save to project config
config.save(global_config=True)  # Save to global config

# Get resolved paths
storage_path = config.get_resolved_path('storage.global_path')
# Returns: /Users/username/.diverga/memory (absolute path)
```

## Configuration Locations

### 1. Global Configuration (Lowest Priority)

**Location:** `~/.diverga/config/memory.yaml`

**Purpose:** User-wide defaults for all projects

**Auto-created:** Yes, on first run with default values

### 2. Project Configuration (Medium Priority)

**Location:** `.diverga/memory.yaml` (in project root)

**Purpose:** Project-specific overrides

**Auto-created:** No, created when you call `config.save()`

### 3. Environment Variables (Highest Priority)

**Format:** `DIVERGA_MEMORY_<SECTION>_<KEY>`

**Purpose:** Runtime overrides (e.g., CI/CD, testing)

**Examples:**
```bash
export DIVERGA_MEMORY_EMBEDDINGS_PROVIDER=openai
export DIVERGA_MEMORY_SEARCH_DEFAULT_LIMIT=20
export DIVERGA_MEMORY_MEMORY_SYSTEM_ENABLED=false
```

## Priority Order (Merge Strategy)

```
Environment Variables (highest)
       ↓
Project Config (.diverga/memory.yaml)
       ↓
Global Config (~/.diverga/config/memory.yaml)
       ↓
Built-in Defaults (lowest)
```

Higher priority configs override lower priority values.

## Default Configuration

```yaml
memory_system:
  version: "1.0.0"
  enabled: true

storage:
  global_path: "~/.diverga/memory"
  project_relative_path: ".diverga/memory"

embeddings:
  provider: "auto"  # auto | local | openai | tfidf
  model: "all-MiniLM-L6-v2"
  cache_enabled: true
  cache_path: "~/.cache/diverga_memory"

search:
  default_limit: 10
  min_similarity: 0.3

export:
  default_format: "markdown"
  output_dir: ".diverga/exports"

logging:
  level: "info"
  file: null  # null = no file logging
```

## API Reference

### MemoryConfig Class

#### Constructor

```python
config = MemoryConfig(project_root=None)
```

**Parameters:**
- `project_root` (Path, optional): Project directory. Defaults to current working directory.

#### Methods

##### `load() -> Config`

Load and merge all configurations (global + project + env).

```python
config = MemoryConfig()
config.load()
```

**Returns:** Typed `Config` object

##### `get(key: str, default: Any = None) -> Any`

Get configuration value using dot notation.

```python
provider = config.get('embeddings.provider')
limit = config.get('search.default_limit')
missing = config.get('nonexistent.key', 'default_value')
```

**Parameters:**
- `key`: Dot-notation path (e.g., `"embeddings.provider"`)
- `default`: Value to return if key not found

**Returns:** Configuration value or default

##### `set(key: str, value: Any) -> None`

Set configuration value using dot notation.

```python
config.set('embeddings.provider', 'openai')
config.set('search.min_similarity', 0.5)
config.set('memory_system.enabled', False)
```

**Parameters:**
- `key`: Dot-notation path
- `value`: Value to set (auto-typed)

##### `save(global_config: bool = False) -> None`

Save current configuration to file.

```python
config.save()  # Save to .diverga/memory.yaml (project)
config.save(global_config=True)  # Save to ~/.diverga/config/memory.yaml
```

**Parameters:**
- `global_config`: If True, save to global config. If False, save to project config.

##### `reset_to_defaults() -> None`

Reset all configuration to built-in defaults.

```python
config.reset_to_defaults()
```

##### `ensure_default_config_exists() -> None`

Create global config file if it doesn't exist.

```python
config.ensure_default_config_exists()
```

##### `get_resolved_path(path_key: str) -> Path`

Get expanded absolute path from configuration.

```python
storage_path = config.get_resolved_path('storage.global_path')
# Returns: /Users/username/.diverga/memory

cache_path = config.get_resolved_path('embeddings.cache_path')
# Returns: /Users/username/.cache/diverga_memory
```

**Parameters:**
- `path_key`: Dot-notation key for path value

**Returns:** Resolved absolute `Path` object

**Handles:**
- Tilde expansion (`~` → `/Users/username`)
- Environment variables (`$HOME`, `%APPDATA%`)
- Relative paths (converted to absolute)

## Environment Variable Reference

### Format

```
DIVERGA_MEMORY_<SECTION>_<KEY>=value
```

### Examples

#### Simple Section Keys

```bash
# embeddings.provider
export DIVERGA_MEMORY_EMBEDDINGS_PROVIDER=openai

# embeddings.model
export DIVERGA_MEMORY_EMBEDDINGS_MODEL=text-embedding-3-small

# search.default_limit
export DIVERGA_MEMORY_SEARCH_DEFAULT_LIMIT=25

# search.min_similarity
export DIVERGA_MEMORY_SEARCH_MIN_SIMILARITY=0.7
```

#### Multi-Word Section Keys

```bash
# memory_system.enabled
export DIVERGA_MEMORY_MEMORY_SYSTEM_ENABLED=false

# memory_system.version
export DIVERGA_MEMORY_MEMORY_SYSTEM_VERSION=2.0.0
```

### Type Conversion

Environment variables are automatically converted to appropriate types:

| Value | Type | Example |
|-------|------|---------|
| `true`, `yes`, `1` | `bool` | `DIVERGA_MEMORY_EMBEDDINGS_CACHE_ENABLED=true` |
| `false`, `no`, `0` | `bool` | `DIVERGA_MEMORY_MEMORY_SYSTEM_ENABLED=false` |
| `null`, `none`, `` | `None` | `DIVERGA_MEMORY_LOGGING_FILE=null` |
| Integer number | `int` | `DIVERGA_MEMORY_SEARCH_DEFAULT_LIMIT=10` |
| Decimal number | `float` | `DIVERGA_MEMORY_SEARCH_MIN_SIMILARITY=0.3` |
| Anything else | `str` | `DIVERGA_MEMORY_EMBEDDINGS_PROVIDER=openai` |

## Configuration Sections

### `memory_system`

System-level settings.

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| `version` | str | "1.0.0" | Config schema version |
| `enabled` | bool | true | Enable/disable memory system |

### `storage`

Storage path configuration.

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| `global_path` | str | "~/.diverga/memory" | Global memory storage |
| `project_relative_path` | str | ".diverga/memory" | Project-relative path |

### `embeddings`

Embedding provider settings.

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| `provider` | str | "auto" | Provider: `auto`, `local`, `openai`, `tfidf` |
| `model` | str | "all-MiniLM-L6-v2" | Model name for embeddings |
| `cache_enabled` | bool | true | Enable embedding cache |
| `cache_path` | str | "~/.cache/diverga_memory" | Cache directory |

**Provider Options:**
- `auto`: Auto-detect best available provider
- `local`: Use local sentence-transformers
- `openai`: Use OpenAI embeddings (requires `OPENAI_API_KEY`)
- `tfidf`: Use TF-IDF (no ML dependencies)

### `search`

Search behavior configuration.

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| `default_limit` | int | 10 | Default number of search results |
| `min_similarity` | float | 0.3 | Minimum similarity threshold (0.0-1.0) |

### `export`

Export settings.

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| `default_format` | str | "markdown" | Default export format |
| `output_dir` | str | ".diverga/exports" | Export output directory |

### `logging`

Logging configuration.

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| `level` | str | "info" | Log level: `debug`, `info`, `warning`, `error` |
| `file` | str\|null | null | Log file path (null = no file logging) |

## Usage Examples

### Example 1: Basic Usage

```python
from config import get_config

config = get_config()
print(f"Provider: {config.get('embeddings.provider')}")
print(f"Storage: {config.get_resolved_path('storage.global_path')}")
```

### Example 2: Custom Project Config

```python
from config import get_config

config = get_config()

# Override for this project
config.set('embeddings.provider', 'openai')
config.set('embeddings.model', 'text-embedding-3-small')
config.set('search.min_similarity', 0.5)

# Save to project config
config.save()
```

### Example 3: Environment-Based Config

```bash
# Terminal 1: Development (local embeddings)
export DIVERGA_MEMORY_EMBEDDINGS_PROVIDER=local
python your_script.py

# Terminal 2: Production (OpenAI embeddings)
export DIVERGA_MEMORY_EMBEDDINGS_PROVIDER=openai
export DIVERGA_MEMORY_SEARCH_MIN_SIMILARITY=0.7
python your_script.py
```

### Example 4: Integration with DivergeMemory

```python
from config import get_config
from memory_api import DivergeMemory, DivergeMemoryConfig

# Load memory config
config = get_config()

# Create memory system config
memory_config = DivergeMemoryConfig(
    global_path=str(config.get_resolved_path('storage.global_path')),
    enable_embeddings=config.get('embeddings.cache_enabled'),
    embedding_cache=config.get('embeddings.cache_enabled')
)

# Initialize memory
memory = DivergeMemory(config=memory_config)
```

### Example 5: Multiple Projects with Different Configs

```
~/research/
├── project-a/
│   └── .diverga/
│       └── memory.yaml  # Uses OpenAI embeddings
└── project-b/
    └── .diverga/
        └── memory.yaml  # Uses local embeddings
```

**project-a/.diverga/memory.yaml:**
```yaml
embeddings:
  provider: openai
  model: text-embedding-3-small
search:
  min_similarity: 0.7
```

**project-b/.diverga/memory.yaml:**
```yaml
embeddings:
  provider: local
  model: all-MiniLM-L6-v2
search:
  min_similarity: 0.3
```

## Cross-Platform Path Handling

The config system automatically handles platform-specific paths:

### Unix/Linux/macOS

```yaml
storage:
  global_path: "~/.diverga/memory"
  # Expands to: /Users/username/.diverga/memory

embeddings:
  cache_path: "~/.cache/diverga_memory"
  # Expands to: /Users/username/.cache/diverga_memory
```

### Windows

```yaml
storage:
  global_path: "%APPDATA%/diverga/memory"
  # Expands to: C:\Users\username\AppData\Roaming\diverga\memory

embeddings:
  cache_path: "%LOCALAPPDATA%/diverga_memory"
  # Expands to: C:\Users\username\AppData\Local\diverga_memory
```

The `get_resolved_path()` method handles all expansions automatically.

## Testing

Run the test suite:

```bash
python3 test_config.py
```

Expected output:
```
============================================================
Diverga Memory Configuration System - Test Suite
============================================================
Test: Basic config loading...
✅ PASSED

Test: Dot notation access...
✅ PASSED

...

============================================================
Results: 10 passed, 0 failed
============================================================

🎉 All tests passed!
```

## Troubleshooting

### Config not loading

**Problem:** `get_config()` returns defaults

**Solution:** Check file locations and permissions
```python
config = MemoryConfig()
print(f"Global config: {config._global_config_path}")
print(f"Project config: {config._project_config_path}")
```

### Environment variables not working

**Problem:** Env vars not overriding config

**Solution:** Check naming convention
```bash
# ❌ Wrong
export MEMORY_EMBEDDINGS_PROVIDER=openai

# ✅ Correct
export DIVERGA_MEMORY_EMBEDDINGS_PROVIDER=openai
```

### Path expansion issues

**Problem:** Paths contain `~` or `$HOME`

**Solution:** Use `get_resolved_path()` instead of `get()`
```python
# ❌ Wrong (returns string with ~)
path = config.get('storage.global_path')

# ✅ Correct (returns absolute Path)
path = config.get_resolved_path('storage.global_path')
```

## Implementation Details

### Config Object Structure

The `Config` dataclass contains nested configuration objects:

```python
@dataclass
class Config:
    memory_system: MemorySystemConfig
    storage: StorageConfig
    embeddings: EmbeddingsConfig
    search: SearchConfig
    export: ExportConfig
    logging: LoggingConfig
```

This provides:
- Type safety
- IDE autocomplete
- Runtime validation
- Easy serialization

### Merge Algorithm

Configs are merged using deep dictionary merge:

1. Start with defaults
2. Merge global config (if exists)
3. Merge project config (if exists)
4. Apply environment variable overrides

Each merge preserves nested structure while allowing partial overrides.

## Best Practices

1. **Use global config for user preferences**
   - Embedding provider choice
   - Default search limits
   - Cache settings

2. **Use project config for project-specific settings**
   - Custom similarity thresholds
   - Project-specific storage paths
   - Export formats

3. **Use environment variables for runtime overrides**
   - CI/CD pipelines
   - Testing environments
   - Temporary overrides

4. **Always use `get_resolved_path()` for paths**
   - Handles cross-platform differences
   - Expands variables automatically
   - Returns absolute paths

5. **Call `ensure_default_config_exists()` on first run**
   - Creates global config if missing
   - Provides good defaults
   - Reduces user setup burden
