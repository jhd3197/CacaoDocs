"""Configuration loader for CacaoDocs."""
import os
from pathlib import Path
from typing import Any

import yaml


DEFAULT_CONFIG = {
    "title": "Documentation",
    "description": "API Documentation",
    "version": "1.0.0",
    "theme": {
        "primary_color": "#8B4513",
        "secondary_color": "#D2691E",
        "bg_color": "#faf8f5",
        "text_color": "#1a202c",
        "highlight_code_bg_color": "#fff8f0",
        "highlight_code_border_color": "#8B4513",
        "sidebar_bg_color": "#ffffff",
        "sidebar_text_color": "#1a202c",
        "sidebar_highlight_bg_color": "#8B4513",
        "sidebar_highlight_text_color": "#ffffff",
        "secondary_sidebar_bg_color": "#f5f0eb",
        "secondary_sidebar_text_color": "#1a202c",
        "secondary_sidebar_highlight_bg_color": "#8B4513",
        "secondary_sidebar_highlight_text_color": "#ffffff",
        "home_page_welcome_bg_1": "#8B4513",
        "home_page_welcome_bg_2": "#D2691E",
        "home_page_welcome_text_color": "#ffffff",
        "home_page_card_bg_color": "#ffffff",
        "home_page_card_text_color": "#1a202c",
        "code_bg_color": "#f5f0eb",
    },
    "logo_url": "",
    "github_url": "",
    "footer_text": "Built with CacaoDocs",
    "google_analytics_id": "",
    "clarity_id": "",
    "exclude_patterns": [
        "__pycache__",
        ".venv",
        "venv",
        ".git",
        "node_modules",
        ".tox",
        ".pytest_cache",
        "__pypackages__",
        "build",
        "dist",
        "*.egg-info",
    ],
}


def load_config(config_path: str | Path | None = None) -> dict[str, Any]:
    """Load configuration from YAML file.

    Args:
        config_path: Path to cacao.yaml config file. If None, searches
            in current directory.

    Returns:
        Merged configuration dictionary with defaults.
    """
    config = DEFAULT_CONFIG.copy()

    if config_path is None:
        # Search for config in current directory
        for name in ["cacao.yaml", "cacao.yml", ".cacao.yaml", ".cacao.yml"]:
            if os.path.exists(name):
                config_path = name
                break

    if config_path and os.path.exists(config_path):
        with open(config_path, "r", encoding="utf-8") as f:
            user_config = yaml.safe_load(f) or {}

        # Deep merge theme settings
        if "theme" in user_config:
            config["theme"] = {**config["theme"], **user_config["theme"]}
            del user_config["theme"]

        # Merge exclude patterns
        if "exclude_patterns" in user_config:
            config["exclude_patterns"] = list(set(
                config["exclude_patterns"] + user_config["exclude_patterns"]
            ))
            del user_config["exclude_patterns"]

        # Merge remaining config
        config.update(user_config)

    return config


def create_default_config(output_path: str | Path = "cacao.yaml") -> None:
    """Create a default configuration file.

    Args:
        output_path: Path where to write the config file.
    """
    config_content = '''# CacaoDocs Configuration
title: "My Project Documentation"
description: "API and module documentation"
version: "1.0.0"

# Theme customization
theme:
  primary_color: "#8B4513"
  secondary_color: "#D2691E"

# Optional: GitHub repository URL
# github_url: "https://github.com/username/repo"

# Optional: Custom logo URL
# logo_url: "/path/to/logo.png"

# Optional: Analytics
# google_analytics_id: "G-XXXXXXXXXX"
# clarity_id: "xxxxxxxxxx"

# Patterns to exclude from scanning
exclude_patterns:
  - "__pycache__"
  - ".venv"
  - "venv"
  - ".git"
  - "node_modules"
  - "build"
  - "dist"
'''

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(config_content)
