"""
Configuration management for Diverga Memory System.

Supports:
- Global configuration (~/.diverga/config/memory.yaml)
- Project-level overrides (.diverga/memory.yaml)
- Environment variable overrides (DIVERGA_MEMORY_*)
- Automatic default config creation
- Cross-platform path expansion
"""

import os
import yaml
from pathlib import Path
from typing import Any, Dict, Optional, Union
from dataclasses import dataclass, field, asdict


DEFAULT_CONFIG = {
    "memory_system": {
        "version": "1.0.0",
        "enabled": True,
    },
    "storage": {
        "global_path": "~/.diverga/memory",
        "project_relative_path": ".diverga/memory",
    },
    "embeddings": {
        "provider": "auto",  # auto | local | openai | tfidf
        "model": "all-MiniLM-L6-v2",
        "cache_enabled": True,
        "cache_path": "~/.cache/diverga_memory",
    },
    "search": {
        "default_limit": 10,
        "min_similarity": 0.3,
    },
    "export": {
        "default_format": "markdown",
        "output_dir": ".diverga/exports",
    },
    "logging": {
        "level": "info",
        "file": None,  # null = no file logging
    },
}


@dataclass
class MemorySystemConfig:
    """Memory system metadata."""
    version: str = "1.0.0"
    enabled: bool = True


@dataclass
class StorageConfig:
    """Storage paths configuration."""
    global_path: str = "~/.diverga/memory"
    project_relative_path: str = ".diverga/memory"


@dataclass
class EmbeddingsConfig:
    """Embeddings provider configuration."""
    provider: str = "auto"
    model: str = "all-MiniLM-L6-v2"
    cache_enabled: bool = True
    cache_path: str = "~/.cache/diverga_memory"


@dataclass
class SearchConfig:
    """Search behavior configuration."""
    default_limit: int = 10
    min_similarity: float = 0.3


@dataclass
class ExportConfig:
    """Export settings configuration."""
    default_format: str = "markdown"
    output_dir: str = ".diverga/exports"


@dataclass
class LoggingConfig:
    """Logging configuration."""
    level: str = "info"
    file: Optional[str] = None


@dataclass
class Config:
    """Complete memory system configuration."""
    memory_system: MemorySystemConfig = field(default_factory=MemorySystemConfig)
    storage: StorageConfig = field(default_factory=StorageConfig)
    embeddings: EmbeddingsConfig = field(default_factory=EmbeddingsConfig)
    search: SearchConfig = field(default_factory=SearchConfig)
    export: ExportConfig = field(default_factory=ExportConfig)
    logging: LoggingConfig = field(default_factory=LoggingConfig)

    def to_dict(self) -> Dict[str, Any]:
        """Convert config to dictionary."""
        return {
            "memory_system": asdict(self.memory_system),
            "storage": asdict(self.storage),
            "embeddings": asdict(self.embeddings),
            "search": asdict(self.search),
            "export": asdict(self.export),
            "logging": asdict(self.logging),
        }


class MemoryConfig:
    """
    Configuration manager for Diverga Memory System.

    Handles:
    - Loading global and project-specific configs
    - Merging configurations (project overrides global)
    - Environment variable overrides
    - Path expansion (cross-platform)
    - Default config creation
    """

    def __init__(self, project_root: Optional[Path] = None):
        """
        Initialize configuration manager.

        Args:
            project_root: Project directory for project-specific config.
                         If None, uses current working directory.
        """
        self.project_root = Path(project_root or os.getcwd()).resolve()
        self._config: Optional[Config] = None
        self._global_config_path = self._get_global_config_path()
        self._project_config_path = self.project_root / ".diverga" / "memory.yaml"

    @staticmethod
    def _get_global_config_path() -> Path:
        """Get platform-appropriate global config path."""
        if os.name == "nt":  # Windows
            base = Path(os.environ.get("APPDATA", "~")).expanduser()
        else:  # Unix-like
            base = Path.home()

        return base / ".diverga" / "config" / "memory.yaml"

    @staticmethod
    def _expand_path(path_str: str) -> Path:
        """
        Expand path string to absolute Path object.

        Handles:
        - ~ expansion (home directory)
        - Environment variables (%APPDATA%, $HOME, etc.)
        - Relative paths
        """
        if not path_str:
            return Path()

        # Expand environment variables
        expanded = os.path.expandvars(path_str)
        # Expand user home directory
        path = Path(expanded).expanduser()

        return path

    def _load_yaml(self, path: Path) -> Dict[str, Any]:
        """Load YAML configuration file."""
        if not path.exists():
            return {}

        try:
            with open(path, "r", encoding="utf-8") as f:
                content = yaml.safe_load(f) or {}
                return content
        except yaml.YAMLError as e:
            raise ValueError(f"Invalid YAML in {path}: {e}")

    def _save_yaml(self, path: Path, data: Dict[str, Any]) -> None:
        """Save configuration to YAML file."""
        path.parent.mkdir(parents=True, exist_ok=True)

        with open(path, "w", encoding="utf-8") as f:
            yaml.safe_dump(data, f, default_flow_style=False, sort_keys=False)

    def _merge_configs(
        self, base: Dict[str, Any], override: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Deep merge two configuration dictionaries.

        Args:
            base: Base configuration
            override: Override configuration (takes precedence)

        Returns:
            Merged configuration dictionary
        """
        result = base.copy()

        for key, value in override.items():
            if (
                key in result
                and isinstance(result[key], dict)
                and isinstance(value, dict)
            ):
                result[key] = self._merge_configs(result[key], value)
            else:
                result[key] = value

        return result

    def _apply_env_overrides(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """
        Apply environment variable overrides.

        Environment variables format: DIVERGA_MEMORY_<SECTION>_<KEY>
        Example: DIVERGA_MEMORY_EMBEDDINGS_PROVIDER=openai

        Supports multi-word sections with underscores:
        DIVERGA_MEMORY_MEMORY_SYSTEM_ENABLED=false → config["memory_system"]["enabled"]
        """
        env_prefix = "DIVERGA_MEMORY_"

        for env_key, env_value in os.environ.items():
            if not env_key.startswith(env_prefix):
                continue

            # Parse environment variable
            key_path = env_key[len(env_prefix):].lower().split("_")

            if len(key_path) < 2:
                continue

            # Convert string value to appropriate type
            value = self._parse_env_value(env_value)

            # Try to find the best matching section
            # Try progressively longer section names (e.g., "memory_system" before "memory")
            for section_len in range(min(3, len(key_path)), 0, -1):
                section_key = "_".join(key_path[:section_len])

                if section_key in config and isinstance(config[section_key], dict):
                    # Found matching section
                    remaining_keys = key_path[section_len:]
                    if remaining_keys:
                        final_key = "_".join(remaining_keys)
                        config[section_key][final_key] = value
                    break

        return config

    @staticmethod
    def _parse_env_value(value: str) -> Union[str, int, float, bool, None]:
        """Parse environment variable value to appropriate type."""
        # Boolean
        if value.lower() in ("true", "yes", "1"):
            return True
        if value.lower() in ("false", "no", "0"):
            return False

        # None/null
        if value.lower() in ("null", "none", ""):
            return None

        # Number
        try:
            if "." in value:
                return float(value)
            return int(value)
        except ValueError:
            pass

        # String (default)
        return value

    def _dict_to_config(self, data: Dict[str, Any]) -> Config:
        """Convert dictionary to typed Config object."""
        return Config(
            memory_system=MemorySystemConfig(**data.get("memory_system", {})),
            storage=StorageConfig(**data.get("storage", {})),
            embeddings=EmbeddingsConfig(**data.get("embeddings", {})),
            search=SearchConfig(**data.get("search", {})),
            export=ExportConfig(**data.get("export", {})),
            logging=LoggingConfig(**data.get("logging", {})),
        )

    def load(self) -> Config:
        """
        Load and merge all configurations.

        Priority (highest to lowest):
        1. Environment variables (DIVERGA_MEMORY_*)
        2. Project config (.diverga/memory.yaml)
        3. Global config (~/.diverga/config/memory.yaml)
        4. Defaults

        Returns:
            Merged configuration object
        """
        # Start with defaults
        config_dict = DEFAULT_CONFIG.copy()

        # Load global config
        global_config = self._load_yaml(self._global_config_path)
        if global_config:
            config_dict = self._merge_configs(config_dict, global_config)

        # Load project config
        project_config = self._load_yaml(self._project_config_path)
        if project_config:
            config_dict = self._merge_configs(config_dict, project_config)

        # Apply environment variable overrides
        config_dict = self._apply_env_overrides(config_dict)

        # Convert to typed config
        self._config = self._dict_to_config(config_dict)

        return self._config

    def get(self, key: str, default: Any = None) -> Any:
        """
        Get configuration value using dot notation.

        Args:
            key: Configuration key (e.g., "embeddings.provider")
            default: Default value if key not found

        Returns:
            Configuration value

        Examples:
            >>> config.get("embeddings.provider")
            "auto"
            >>> config.get("search.default_limit")
            10
        """
        if self._config is None:
            self.load()

        parts = key.split(".")
        value = self._config.to_dict()

        try:
            for part in parts:
                value = value[part]
            return value
        except (KeyError, TypeError):
            return default

    def set(self, key: str, value: Any) -> None:
        """
        Set configuration value using dot notation.

        Args:
            key: Configuration key (e.g., "embeddings.provider")
            value: Value to set

        Examples:
            >>> config.set("embeddings.provider", "openai")
            >>> config.set("search.min_similarity", 0.5)
        """
        if self._config is None:
            self.load()

        parts = key.split(".")
        config_dict = self._config.to_dict()

        # Navigate to the parent dictionary
        current = config_dict
        for part in parts[:-1]:
            if part not in current:
                current[part] = {}
            current = current[part]

        # Set the value
        current[parts[-1]] = value

        # Rebuild typed config
        self._config = self._dict_to_config(config_dict)

    def save(self, global_config: bool = False) -> None:
        """
        Save current configuration to file.

        Args:
            global_config: If True, save to global config.
                          If False, save to project config.
        """
        if self._config is None:
            raise ValueError("No configuration loaded. Call load() first.")

        config_dict = self._config.to_dict()

        if global_config:
            self._save_yaml(self._global_config_path, config_dict)
        else:
            self._save_yaml(self._project_config_path, config_dict)

    def reset_to_defaults(self) -> None:
        """Reset configuration to defaults."""
        self._config = self._dict_to_config(DEFAULT_CONFIG.copy())

    def ensure_default_config_exists(self) -> None:
        """Create default global config if it doesn't exist."""
        if not self._global_config_path.exists():
            self._save_yaml(self._global_config_path, DEFAULT_CONFIG)

    def get_resolved_path(self, path_key: str) -> Path:
        """
        Get expanded and resolved path from configuration.

        Args:
            path_key: Configuration key for path (e.g., "storage.global_path")

        Returns:
            Resolved absolute Path object
        """
        path_str = self.get(path_key)
        if not path_str:
            raise ValueError(f"Path key '{path_key}' not found in configuration")

        return self._expand_path(path_str).resolve()

    def __repr__(self) -> str:
        """String representation of configuration."""
        if self._config is None:
            return "MemoryConfig(unloaded)"

        return (
            f"MemoryConfig(\n"
            f"  global={self._global_config_path},\n"
            f"  project={self._project_config_path},\n"
            f"  enabled={self._config.memory_system.enabled}\n"
            f")"
        )


# Convenience function for quick config access
def get_config(project_root: Optional[Path] = None) -> MemoryConfig:
    """
    Get or create configuration manager.

    Args:
        project_root: Project directory (defaults to current working directory)

    Returns:
        MemoryConfig instance with loaded configuration
    """
    config = MemoryConfig(project_root)
    config.ensure_default_config_exists()
    config.load()
    return config


if __name__ == "__main__":
    # Demo usage
    config = get_config()

    print("Configuration loaded:")
    print(f"  Embeddings provider: {config.get('embeddings.provider')}")
    print(f"  Search limit: {config.get('search.default_limit')}")
    print(f"  Global storage: {config.get_resolved_path('storage.global_path')}")
    print(f"\nFull config:\n{config._config.to_dict()}")
