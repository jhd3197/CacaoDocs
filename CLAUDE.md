# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

CacaoDocs is a **Cacao plugin** that generates interactive documentation from Python docstrings. It is not a standalone tool — it depends on and extends the [Cacao](https://github.com/cacao-research/Cacao) web framework.

Instead of generating static HTML, CacaoDocs generates a Cacao app (`app.py`) that serves documentation with WebSocket-driven reactivity.

## Plugin Architecture

CacaoDocs is a plugin of Cacao. This means:

1. **Cacao owns `cacao.yaml`** — The config file is a Cacao framework feature. Cacao reads its own keys (`title`, `theme`, `port`, `debug`, `branding`) and CacaoDocs reads its plugin-specific keys (`description`, `version`, `github_url`, `doc_types`, `exclude_patterns`, etc.) from the same file.

2. **No duplicate YAML parsing** — CacaoDocs does NOT import PyYAML directly. It delegates all YAML loading to Cacao's config system:
   ```python
   import cacao as c
   raw = c.get_yaml_config()        # Full parsed cacao.yaml dict
   path = c.get_yaml_config_path()  # Path to the loaded file
   ```

3. **Cacao provides PyYAML** — Since Cacao >= 2.1.0 includes PyYAML as a required dependency, CacaoDocs does not need to declare it separately.

4. **Shared config, separate concerns** — A single `cacao.yaml` serves both:
   ```yaml
   # Cacao framework reads these:
   title: "My Project"
   theme: "dark"
   port: 1502

   # CacaoDocs plugin reads these:
   description: "API Documentation"
   version: "1.0.0"
   github_url: "https://github.com/..."
   exclude_patterns: [...]
   doc_types: { ... }
   ```

### Config Priority

For shared keys like `title` and `theme`:
- **Cacao framework** applies them at the app level (`c.config()` > `cacao.yaml`)
- **CacaoDocs** reads them from the raw YAML for its own rendering (e.g. theme color dicts for the docs UI)

### Important Rules

- **Never import `yaml` directly** — Always go through `cacao.config` or `c.get_yaml_config()`
- **Never duplicate Cacao's config discovery** — Don't search for `cacao.yaml` manually; Cacao handles file discovery
- **When adding new CacaoDocs config keys**, just add them to `cacao.yaml` — no need to create a separate config file
- **Minimum Cacao version is 2.0.16** — Provides LLM chat with streaming, plugin slot injection, extensions, and `get_yaml_config()`

## Common Commands

### Building Documentation
```bash
cacaodocs build ./src -o ./docs         # Build docs from source directory
cacaodocs build ./my-project -o ./docs  # Build docs from any Python project
```

### Serving Documentation
```bash
cacaodocs serve ./docs                  # Serve docs via Cacao (port 1502)
cacaodocs serve ./docs -p 3000          # Use custom port
```

### Creating Configuration
```bash
cacaodocs init                          # Create default cacao.yaml
cacaodocs init -o myconfig.yaml         # Create with custom name
```

### Installing Package
```bash
pip install -e .            # Install in editable mode
pip install cacaodocs       # Install from PyPI
```

## Architecture

### Package Structure (`cacaodocs/`)
- **`cli.py`** - Click CLI with `build`, `serve`, `init`, `export` commands
- **`scanner.py`** - File discovery + AST extraction + API decorator auto-detection
- **`parser.py`** - Docstring parser with Type: directive and all doc type sections
- **`builder.py`** - Generates a Cacao app from parsed documentation
- **`config.py`** - Config loader that delegates to Cacao's YAML system, then extracts CacaoDocs-specific keys
- **`types.py`** - Dataclasses and DocType enum for parsed documentation

### Data Flow
```
Python files -> AST Scanner -> Docstring Parser -> JSON Builder -> Cacao App Generator
     |              |                                                    |
     |         Auto-detect                                         app.py + data.json
     |         API decorators
Markdown files -------------------------------------------------------->
```

### Doc Types System (v0.4.0)
CacaoDocs supports 6 built-in doc types + custom types:

- **`function`** - Default. Args, Returns, Raises, Examples
- **`api`** - REST endpoints. Auto-detected from Flask/FastAPI/Django decorators. Method, Path, Path Params, Query Params, Request Body, Response(NNN), Headers
- **`class`** - Classes. Attributes, Methods
- **`page`** - Markdown pages
- **`config`** - Settings/env vars. Fields with type, default, required, env=
- **`event`** - Webhooks/signals. Trigger, Payload
- **`custom`** - User-defined via `doc_types:` in cacao.yaml

Auto-detection: Scanner checks decorators for `@app.get`, `@router.post`, `@app.route`, `@api_view`, etc. and sets doc_type=api automatically, extracting HTTP method and route path.

### Core Types (`types.py`)
- **`DocType`** - Enum: function, api, class, page, config, event, custom
- **`ParsedDocstring`** - All parsed sections across all doc types
- **`FunctionDoc`** / **`MethodDoc`** - Functions with doc_type field
- **`ClassDoc`** - Class with methods
- **`ModuleDoc`** - Python module
- **`PageDoc`** - Markdown page
- **`ResponseDoc`** - API response (status_code, fields)
- **`ConfigFieldDoc`** - Config field (type, default, required, env_var)
- **`CustomDocTypeDef`** / **`CustomSectionDef`** - User-defined types

### Configuration (`cacao.yaml`)
```yaml
# Cacao framework keys
title: "My Project"
theme: "dark"

# CacaoDocs plugin keys
description: "API Documentation"
version: "1.0.0"
github_url: "https://github.com/..."

exclude_patterns:
  - "__pycache__"
  - ".venv"

# Custom doc types (optional)
doc_types:
  cli_command:
    label: "CLI Command"
    icon: "terminal"
    sections:
      - name: "Usage"
        format: code
      - name: "Options"
        format: args
```

### Dependencies
- **cacao** (>=2.1.0) - Reactive web framework (provides PyYAML, config system, rendering)
- **click** - CLI framework
- **Markdown** - Markdown to HTML conversion
