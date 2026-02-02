"""
Example usage of Diverga Memory Configuration System.

Run with: python3 examples/config_example.py
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from config import get_config
from memory_api import DivergeMemory, DivergeMemoryConfig


def example_basic_usage():
    """Example 1: Basic configuration usage."""
    print("=" * 60)
    print("Example 1: Basic Configuration Usage")
    print("=" * 60)

    # Load configuration
    config = get_config()

    # Get values
    print(f"Embeddings provider: {config.get('embeddings.provider')}")
    print(f"Search limit: {config.get('search.default_limit')}")
    print(f"Min similarity: {config.get('search.min_similarity')}")

    # Get resolved paths
    storage_path = config.get_resolved_path('storage.global_path')
    cache_path = config.get_resolved_path('embeddings.cache_path')

    print(f"\nResolved paths:")
    print(f"  Storage: {storage_path}")
    print(f"  Cache: {cache_path}")


def example_custom_config():
    """Example 2: Creating custom project configuration."""
    print("\n" + "=" * 60)
    print("Example 2: Custom Project Configuration")
    print("=" * 60)

    config = get_config()

    # Customize for this project
    config.set('embeddings.provider', 'openai')
    config.set('embeddings.model', 'text-embedding-3-small')
    config.set('search.min_similarity', 0.6)
    config.set('search.default_limit', 20)

    print("Modified configuration:")
    print(f"  Provider: {config.get('embeddings.provider')}")
    print(f"  Model: {config.get('embeddings.model')}")
    print(f"  Min similarity: {config.get('search.min_similarity')}")
    print(f"  Default limit: {config.get('search.default_limit')}")

    # Save to project config
    # config.save()  # Uncomment to actually save
    print("\n(Skipped save in example)")


def example_memory_integration():
    """Example 3: Integration with DivergeMemory."""
    print("\n" + "=" * 60)
    print("Example 3: Integration with DivergeMemory")
    print("=" * 60)

    # Load config
    config = get_config()

    # Create memory config from our config
    memory_config = DivergeMemoryConfig(
        global_path=str(config.get_resolved_path('storage.global_path')),
        enable_embeddings=config.get('embeddings.cache_enabled'),
        embedding_cache=config.get('embeddings.cache_enabled')
    )

    # Initialize memory
    memory = DivergeMemory(config=memory_config)

    print(f"Memory initialized with config-based settings")
    print(f"  Storage path: {memory_config.global_path}")
    print(f"  Embeddings enabled: {memory_config.enable_embeddings}")

    # You can now use memory normally
    # memory.store(content="Example memory", ...)


def example_environment_overrides():
    """Example 4: Environment variable usage."""
    print("\n" + "=" * 60)
    print("Example 4: Environment Variable Overrides")
    print("=" * 60)

    print("Set environment variables like this:")
    print()
    print("  export DIVERGA_MEMORY_EMBEDDINGS_PROVIDER=openai")
    print("  export DIVERGA_MEMORY_SEARCH_MIN_SIMILARITY=0.7")
    print("  export DIVERGA_MEMORY_SEARCH_DEFAULT_LIMIT=25")
    print()
    print("Then load config - env vars will override file config:")
    print()
    print("  config = get_config()")
    print("  provider = config.get('embeddings.provider')  # 'openai'")


def example_multi_project():
    """Example 5: Multi-project configuration."""
    print("\n" + "=" * 60)
    print("Example 5: Multi-Project Configuration")
    print("=" * 60)

    print("Project A (.diverga/memory.yaml):")
    print("  embeddings:")
    print("    provider: openai")
    print("    model: text-embedding-3-small")
    print("  search:")
    print("    min_similarity: 0.7")
    print()
    print("Project B (.diverga/memory.yaml):")
    print("  embeddings:")
    print("    provider: local")
    print("    model: all-MiniLM-L6-v2")
    print("  search:")
    print("    min_similarity: 0.3")
    print()
    print("Each project loads its own config automatically!")


def example_config_types():
    """Example 6: Working with different config types."""
    print("\n" + "=" * 60)
    print("Example 6: Configuration Types")
    print("=" * 60)

    config = get_config()

    # Boolean
    enabled = config.get('memory_system.enabled')
    print(f"Boolean: {enabled} (type: {type(enabled).__name__})")

    # Integer
    limit = config.get('search.default_limit')
    print(f"Integer: {limit} (type: {type(limit).__name__})")

    # Float
    similarity = config.get('search.min_similarity')
    print(f"Float: {similarity} (type: {type(similarity).__name__})")

    # String
    provider = config.get('embeddings.provider')
    print(f"String: {provider} (type: {type(provider).__name__})")

    # None/null
    log_file = config.get('logging.file')
    print(f"None: {log_file} (type: {type(log_file).__name__})")


def main():
    """Run all examples."""
    print("\nDiverga Memory Configuration System - Examples\n")

    example_basic_usage()
    example_custom_config()
    example_memory_integration()
    example_environment_overrides()
    example_multi_project()
    example_config_types()

    print("\n" + "=" * 60)
    print("All examples completed!")
    print("=" * 60)
    print("\nFor more information, see CONFIG.md")


if __name__ == "__main__":
    main()
