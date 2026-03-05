"""Configuration loader for CacaoDocs."""
import os
from pathlib import Path
from typing import Any

import yaml

from .types import CustomDocTypeDef, CustomSectionDef


DEFAULT_CONFIG = {
    "title": "Documentation",
    "description": "API Documentation",
    "version": "1.0.0",
    "theme": "dark",
    "logo_url": "",
    "github_url": "",
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


def _parse_custom_doc_types(raw: dict[str, Any]) -> list[CustomDocTypeDef]:
    """Parse custom doc_types from config YAML.

    Args:
        raw: The doc_types dict from cacao.yaml.

    Returns:
        List of CustomDocTypeDef definitions.
    """
    result = []
    for name, definition in raw.items():
        sections = []
        for sec in definition.get("sections", []):
            if isinstance(sec, str):
                sections.append(CustomSectionDef(name=sec))
            elif isinstance(sec, dict):
                sections.append(CustomSectionDef(
                    name=sec.get("name", ""),
                    format=sec.get("format", "text"),
                ))
        result.append(CustomDocTypeDef(
            name=name,
            label=definition.get("label", name.replace("_", " ").title()),
            icon=definition.get("icon", "file"),
            sections=sections,
        ))
    return result


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
        for name in ["cacao.yaml", "cacao.yml", ".cacao.yaml", ".cacao.yml"]:
            if os.path.exists(name):
                config_path = name
                break

    if config_path and os.path.exists(config_path):
        with open(config_path, "r", encoding="utf-8") as f:
            user_config = yaml.safe_load(f) or {}

        if "exclude_patterns" in user_config:
            config["exclude_patterns"] = list(set(
                config["exclude_patterns"] + user_config["exclude_patterns"]
            ))
            del user_config["exclude_patterns"]

        # Parse custom doc_types into structured objects
        if "doc_types" in user_config:
            config["custom_doc_types"] = _parse_custom_doc_types(user_config["doc_types"])
            config["doc_types_raw"] = user_config.pop("doc_types")

        config.update(user_config)

    # Ensure custom_doc_types always exists
    if "custom_doc_types" not in config:
        config["custom_doc_types"] = []

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

# Theme: "dark" or "light"
theme: "dark"

# Optional: GitHub repository URL
# github_url: "https://github.com/username/repo"

# Optional: Custom logo URL
# logo_url: "/path/to/logo.png"

# Patterns to exclude from scanning
exclude_patterns:
  - "__pycache__"
  - ".venv"
  - "venv"
  - ".git"
  - "node_modules"
  - "build"
  - "dist"

# Custom doc types (optional)
# Define your own docstring categories with custom sections.
# doc_types:
#   cli_command:
#     label: "CLI Command"
#     icon: "terminal"
#     sections:
#       - name: "Usage"
#       - name: "Options"
#         format: args
#       - name: "Flags"
#         format: args
#       - name: "Examples"
#         format: code
#
#   database_model:
#     label: "Model"
#     icon: "database"
#     sections:
#       - name: "Fields"
#         format: args
#       - name: "Indexes"
#       - name: "Relations"
'''

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(config_content)
