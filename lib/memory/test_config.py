"""
Test suite for Diverga Memory Configuration System.

Run with: python3 test_config.py
"""

import sys
import os
from pathlib import Path

# Add src to path
sys.path.insert(0, 'src')

from config import get_config, MemoryConfig, DEFAULT_CONFIG


def test_basic_loading():
    """Test basic config loading."""
    print("Test: Basic config loading...")
    config = get_config()

    assert config.get('embeddings.provider') == 'auto'
    assert config.get('search.default_limit') == 10
    assert config.get('search.min_similarity') == 0.3
    assert config.get('memory_system.version') == '1.0.0'
    print("✅ PASSED")


def test_dot_notation():
    """Test dot notation access."""
    print("\nTest: Dot notation access...")
    config = get_config()

    # Nested access
    assert config.get('embeddings.provider') == 'auto'
    assert config.get('storage.global_path') == '~/.diverga/memory'

    # Default values
    assert config.get('nonexistent.key', 'default') == 'default'
    print("✅ PASSED")


def test_set_get():
    """Test setting and getting values."""
    print("\nTest: Set/get operations...")
    config = get_config()

    config.set('embeddings.provider', 'openai')
    assert config.get('embeddings.provider') == 'openai'

    config.set('search.default_limit', 25)
    assert config.get('search.default_limit') == 25

    # Reset
    config.reset_to_defaults()
    assert config.get('embeddings.provider') == 'auto'
    print("✅ PASSED")


def test_env_overrides():
    """Test environment variable overrides."""
    print("\nTest: Environment variable overrides...")

    # Clean environment
    for key in list(os.environ.keys()):
        if key.startswith('DIVERGA_MEMORY_'):
            del os.environ[key]

    # Test simple override
    os.environ['DIVERGA_MEMORY_EMBEDDINGS_PROVIDER'] = 'tfidf'
    config = get_config()
    assert config.get('embeddings.provider') == 'tfidf'

    # Test nested key override
    os.environ['DIVERGA_MEMORY_MEMORY_SYSTEM_ENABLED'] = 'false'
    config = get_config()
    assert config.get('memory_system.enabled') == False

    # Test number overrides
    os.environ['DIVERGA_MEMORY_SEARCH_DEFAULT_LIMIT'] = '30'
    os.environ['DIVERGA_MEMORY_SEARCH_MIN_SIMILARITY'] = '0.8'
    config = get_config()
    assert config.get('search.default_limit') == 30
    assert config.get('search.min_similarity') == 0.8

    # Cleanup
    for key in list(os.environ.keys()):
        if key.startswith('DIVERGA_MEMORY_'):
            del os.environ[key]

    print("✅ PASSED")


def test_path_expansion():
    """Test path expansion."""
    print("\nTest: Path expansion...")
    config = get_config()

    # Test tilde expansion
    global_path = config.get_resolved_path('storage.global_path')
    assert global_path.is_absolute()
    assert '~' not in str(global_path)

    # Test cache path
    cache_path = config.get_resolved_path('embeddings.cache_path')
    assert cache_path.is_absolute()

    print("✅ PASSED")


def test_save_load():
    """Test saving and loading config."""
    print("\nTest: Save/load configuration...")
    config = get_config()

    # Modify config
    config.set('embeddings.provider', 'openai')
    config.set('search.default_limit', 50)

    # Save to project config
    config.save(global_config=False)
    assert config._project_config_path.exists()

    # Load fresh config
    config2 = get_config()
    assert config2.get('embeddings.provider') == 'openai'
    assert config2.get('search.default_limit') == 50

    # Cleanup
    if config._project_config_path.exists():
        config._project_config_path.unlink()

    print("✅ PASSED")


def test_config_merging():
    """Test configuration merging."""
    print("\nTest: Configuration merging...")

    # Create global config
    config = get_config()
    config.set('embeddings.provider', 'global_value')
    config.save(global_config=True)

    # Create project config
    config2 = get_config()
    config2.set('embeddings.provider', 'project_value')
    config2.save(global_config=False)

    # Load should prefer project over global
    config3 = get_config()
    assert config3.get('embeddings.provider') == 'project_value'

    # Cleanup
    if config2._project_config_path.exists():
        config2._project_config_path.unlink()

    # Reset global config
    config.reset_to_defaults()
    config.save(global_config=True)

    print("✅ PASSED")


def test_global_config_creation():
    """Test global config auto-creation."""
    print("\nTest: Global config creation...")
    config = get_config()
    config.ensure_default_config_exists()

    global_config_path = Path.home() / '.diverga' / 'config' / 'memory.yaml'
    assert global_config_path.exists()

    print("✅ PASSED")


def test_config_types():
    """Test configuration type conversion."""
    print("\nTest: Type conversion...")
    config = get_config()

    # Test bool
    config.set('memory_system.enabled', True)
    assert isinstance(config.get('memory_system.enabled'), bool)

    # Test int
    config.set('search.default_limit', 10)
    assert isinstance(config.get('search.default_limit'), int)

    # Test float
    config.set('search.min_similarity', 0.3)
    assert isinstance(config.get('search.min_similarity'), float)

    # Test string
    config.set('embeddings.provider', 'auto')
    assert isinstance(config.get('embeddings.provider'), str)

    # Test None
    config.set('logging.file', None)
    assert config.get('logging.file') is None

    print("✅ PASSED")


def test_integration_with_memory():
    """Test integration with DivergeMemory."""
    print("\nTest: Integration with DivergeMemory...")

    from memory_api import DivergeMemory, DivergeMemoryConfig

    config = get_config()

    # Create memory config from our config
    memory_config = DivergeMemoryConfig(
        global_path=str(config.get_resolved_path('storage.global_path')),
        enable_embeddings=config.get('embeddings.cache_enabled'),
        embedding_cache=config.get('embeddings.cache_enabled')
    )

    # Initialize memory
    memory = DivergeMemory(config=memory_config)

    print("✅ PASSED")


def run_all_tests():
    """Run all tests."""
    print("=" * 60)
    print("Diverga Memory Configuration System - Test Suite")
    print("=" * 60)

    tests = [
        test_basic_loading,
        test_dot_notation,
        test_set_get,
        test_env_overrides,
        test_path_expansion,
        test_save_load,
        test_config_merging,
        test_global_config_creation,
        test_config_types,
        test_integration_with_memory,
    ]

    passed = 0
    failed = 0

    for test in tests:
        try:
            test()
            passed += 1
        except Exception as e:
            print(f"❌ FAILED: {e}")
            failed += 1

    print("\n" + "=" * 60)
    print(f"Results: {passed} passed, {failed} failed")
    print("=" * 60)

    if failed == 0:
        print("\n🎉 All tests passed!")
        return 0
    else:
        print(f"\n⚠️  {failed} test(s) failed")
        return 1


if __name__ == "__main__":
    exit_code = run_all_tests()
    sys.exit(exit_code)
