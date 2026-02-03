# Configuration Quick Start

## 30-Second Setup

```python
from config import get_config

# Load config (auto-merges global + project + env)
config = get_config()

# Get values
provider = config.get('embeddings.provider')
limit = config.get('search.default_limit')

# Set values
config.set('embeddings.provider', 'openai')

# Save
config.save()  # Project config
```

## Common Tasks

### Get configuration value

```python
value = config.get('section.key')
value = config.get('section.key', default='fallback')
```

### Set configuration value

```python
config.set('embeddings.provider', 'openai')
config.set('search.min_similarity', 0.7)
```

### Get resolved absolute path

```python
path = config.get_resolved_path('storage.global_path')
# Returns: /Users/username/.diverga/memory
```

### Save configuration

```python
config.save()  # Save to .diverga/memory.yaml
config.save(global_config=True)  # Save to ~/.diverga/config/memory.yaml
```

### Reset to defaults

```python
config.reset_to_defaults()
```

## Environment Variables

Override any config value with environment variables:

```bash
export DIVERGA_MEMORY_EMBEDDINGS_PROVIDER=openai
export DIVERGA_MEMORY_SEARCH_MIN_SIMILARITY=0.7
export DIVERGA_MEMORY_SEARCH_DEFAULT_LIMIT=20
```

Format: `DIVERGA_MEMORY_<SECTION>_<KEY>=value`

## Integration with DivergeMemory

```python
from config import get_config
from memory_api import DivergeMemory, DivergeMemoryConfig

# Load config
config = get_config()

# Create memory config
memory_config = DivergeMemoryConfig(
    global_path=str(config.get_resolved_path('storage.global_path')),
    enable_embeddings=config.get('embeddings.cache_enabled'),
    embedding_cache=config.get('embeddings.cache_enabled')
)

# Initialize memory
memory = DivergeMemory(config=memory_config)
```

## Configuration Sections

| Section | Key | Default | Description |
|---------|-----|---------|-------------|
| `embeddings` | `provider` | `auto` | Provider: auto/local/openai/tfidf |
| `embeddings` | `model` | `all-MiniLM-L6-v2` | Embedding model name |
| `embeddings` | `cache_enabled` | `true` | Enable cache |
| `embeddings` | `cache_path` | `~/.cache/diverga_memory` | Cache directory |
| `search` | `default_limit` | `10` | Default result count |
| `search` | `min_similarity` | `0.3` | Similarity threshold (0-1) |
| `storage` | `global_path` | `~/.diverga/memory` | Global storage |
| `storage` | `project_relative_path` | `.diverga/memory` | Project path |
| `logging` | `level` | `info` | Log level |
| `logging` | `file` | `null` | Log file (null = no file) |

## Priority Order (Highest to Lowest)

1. **Environment variables** - `DIVERGA_MEMORY_*`
2. **Project config** - `.diverga/memory.yaml`
3. **Global config** - `~/.diverga/config/memory.yaml`
4. **Built-in defaults**

## File Locations

| Config Type | Path |
|-------------|------|
| Global | `~/.diverga/config/memory.yaml` |
| Project | `.diverga/memory.yaml` (in project root) |

## Full Documentation

See [CONFIG.md](CONFIG.md) for complete reference.

## Examples

See [examples/config_example.py](examples/config_example.py) for working examples.

## Testing

Run tests:
```bash
python3 test_config.py
```
