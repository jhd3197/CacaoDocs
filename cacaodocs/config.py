"""Configuration loader for CacaoDocs.

CacaoDocs is a plugin of Cacao. The cacao.yaml file is owned by the Cacao
framework — Cacao reads its own keys (title, theme, port, etc.) and CacaoDocs
reads its plugin-specific keys (description, version, github_url, doc_types,
exclude_patterns, etc.) from the same file.

Config loading is delegated to Cacao's config system via:
    import cacao as c
    raw = c.get_yaml_config()       # full parsed cacao.yaml
    path = c.get_yaml_config_path() # path to the file

CacaoDocs then extracts the keys it cares about on top of what Cacao already
handled. This avoids duplicating YAML parsing and keeps one config file.
"""
from __future__ import annotations

from pathlib import Path
from typing import Any

from .types import CustomDocTypeDef, CustomSectionDef


DEFAULT_CONFIG: dict[str, Any] = {
    "title": "Documentation",
    "description": "API Documentation",
    "version": "1.0.0",
    "theme": "dark",
    "logo_url": "",
    "github_url": "",
    "footer_text": "",
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


def _merge_from_yaml(config: dict[str, Any], yaml_data: dict[str, Any]) -> None:
    """Merge raw cacao.yaml data into the CacaoDocs config dict.

    Cacao owns: title, theme, host, port, debug, branding
    CacaoDocs owns: description, version, github_url, logo_url, footer_text,
                    exclude_patterns, doc_types, theme (extended colors dict),
                    google_analytics_id, clarity_id

    For shared keys (title, theme), Cacao's values take priority at the
    framework level, but CacaoDocs still reads them for its own rendering
    (e.g. theme color dicts for the docs UI).
    """
    if not yaml_data:
        return

    # Simple string/scalar keys CacaoDocs cares about
    for key in ("title", "description", "version", "github_url", "logo_url",
                "footer_text", "google_analytics_id", "clarity_id",
                "chat", "page_order"):
        if key in yaml_data:
            config[key] = yaml_data[key]

    # Chat / AI config
    if "chat_config" in yaml_data and isinstance(yaml_data["chat_config"], dict):
        config["chat_config"] = yaml_data["chat_config"]

    # Theme — can be a string or a dict of color overrides
    if "theme" in yaml_data:
        config["theme"] = yaml_data["theme"]

    # Exclude patterns — merge with defaults
    if "exclude_patterns" in yaml_data:
        config["exclude_patterns"] = list(set(
            config["exclude_patterns"] + yaml_data["exclude_patterns"]
        ))

    # Custom doc types
    if "doc_types" in yaml_data:
        config["custom_doc_types"] = _parse_custom_doc_types(yaml_data["doc_types"])
        config["doc_types_raw"] = yaml_data["doc_types"]


def load_config(config_path: str | Path | None = None) -> dict[str, Any]:
    """Load configuration from cacao.yaml via Cacao's config system.

    Uses Cacao's built-in YAML loader to read the shared cacao.yaml file,
    then extracts CacaoDocs-specific settings on top of defaults.

    If a specific config_path is provided (e.g. via CLI --config flag),
    it reads that file directly. Otherwise, it delegates discovery to Cacao.

    Args:
        config_path: Path to cacao.yaml config file. If None, uses
            Cacao's config discovery (searches cwd for cacao.yaml/yml).

    Returns:
        Merged configuration dictionary with defaults.
    """
    config = DEFAULT_CONFIG.copy()

    if config_path is not None:
        # Explicit path — read it directly via Cacao's loader
        from cacao.config import load_config_file
        yaml_data = load_config_file(config_path)
    else:
        # Let Cacao find and load the config file
        import cacao as c
        yaml_data = c.get_yaml_config()

    _merge_from_yaml(config, yaml_data)

    # Ensure custom_doc_types always exists
    if "custom_doc_types" not in config:
        config["custom_doc_types"] = []

    return config


def create_default_config(output_path: str | Path = "cacao.yaml") -> None:
    """Create a default cacao.yaml configuration file.

    The generated file contains both Cacao framework settings and
    CacaoDocs plugin settings in a single shared config.

    Args:
        output_path: Path where to write the config file.
    """
    config_content = '''# Cacao Configuration
# This file is read by Cacao and its plugins (e.g. CacaoDocs).

# --- Cacao Framework Settings ---
# These are read by the Cacao framework directly.
title: "My Project Documentation"
theme: "dark"
# port: 1502
# debug: false
# branding: true

# --- CacaoDocs Plugin Settings ---
# These are read by CacaoDocs for documentation generation.
description: "API and module documentation"
version: "1.0.0"

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

# Page ordering (optional)
# Control the order of Markdown pages in the sidebar by slug.
# Pages not listed appear after these, in their default order.
# page_order:
#   - "getting-started"
#   - "configuration"
#   - "api-reference"

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
