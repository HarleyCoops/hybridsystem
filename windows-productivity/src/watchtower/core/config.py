"""
Watchtower Windows - Configuration Management
Handles loading, saving, and managing user configuration.
"""

import json
import os
from datetime import datetime
from pathlib import Path
from typing import Optional

from watchtower.types import (
    WatchtowerConfig,
    EnergyWindow,
)


def get_config_path() -> Path:
    """Get the path to the configuration file."""
    if os.name == "nt":  # Windows
        base = Path(os.environ.get("APPDATA", Path.home()))
    else:
        base = Path.home()

    config_dir = base / ".watchtower"
    config_dir.mkdir(parents=True, exist_ok=True)
    return config_dir / "config.json"


def get_data_dir() -> Path:
    """Get the data directory path."""
    if os.name == "nt":  # Windows
        base = Path(os.environ.get("APPDATA", Path.home()))
    else:
        base = Path.home()

    data_dir = base / ".watchtower"
    data_dir.mkdir(parents=True, exist_ok=True)
    return data_dir


def get_config() -> WatchtowerConfig:
    """Get the current configuration, loading from file or using defaults."""
    config_path = get_config_path()

    if config_path.exists():
        try:
            with open(config_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            return WatchtowerConfig.model_validate(data)
        except (json.JSONDecodeError, ValueError):
            # Invalid config, return defaults
            return WatchtowerConfig()

    # No config file, create with defaults
    config = WatchtowerConfig()
    save_config(config)
    return config


def save_config(config: WatchtowerConfig) -> None:
    """Save configuration to file."""
    config_path = get_config_path()
    with open(config_path, "w", encoding="utf-8") as f:
        json.dump(config.model_dump(), f, indent=2, default=str)


def update_config(updates: dict) -> WatchtowerConfig:
    """Update configuration with partial values."""
    config = get_config()
    config_dict = config.model_dump()

    # Deep merge updates
    def deep_merge(base: dict, updates: dict) -> dict:
        for key, value in updates.items():
            if key in base and isinstance(base[key], dict) and isinstance(value, dict):
                deep_merge(base[key], value)
            else:
                base[key] = value
        return base

    merged = deep_merge(config_dict, updates)
    new_config = WatchtowerConfig.model_validate(merged)
    save_config(new_config)
    return new_config


def reset_config() -> WatchtowerConfig:
    """Reset configuration to defaults."""
    config = WatchtowerConfig()
    save_config(config)
    return config


def ensure_directories() -> None:
    """Ensure all required directories exist."""
    config = get_config()
    data_dir = get_data_dir()

    dirs = [
        data_dir,
        data_dir / "sessions",
    ]

    for dir_path in dirs:
        dir_path.mkdir(parents=True, exist_ok=True)


def is_in_peak_window(config: Optional[WatchtowerConfig] = None) -> tuple[bool, Optional[EnergyWindow]]:
    """Check if we're currently in a peak energy window."""
    if config is None:
        config = get_config()

    current_hour = datetime.now().hour

    for window in config.energy_windows:
        if window.start <= current_hour < window.end:
            return True, window

    return False, None


def get_coaching_voice(
    context: str,
    config: Optional[WatchtowerConfig] = None
) -> str:
    """Get the appropriate coaching voice based on context."""
    if config is None:
        config = get_config()

    voices = {
        "avoidance": config.voices.discipline,
        "burnout": config.voices.wisdom,
        "scattered": config.voices.leadership,
    }

    return voices.get(context, config.voices.wisdom)


def get_category_name(priority: str, config: Optional[WatchtowerConfig] = None) -> str:
    """Get the display name for a task category."""
    if config is None:
        config = get_config()

    categories = {
        "deep": config.categories.deep,
        "standard": config.categories.standard,
        "light": config.categories.light,
        "someday": config.categories.someday,
    }

    return categories.get(priority, priority)
