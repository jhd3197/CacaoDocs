# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

CacaoDocs is a documentation generator that scans Python files, parses docstrings, and generates interactive documentation apps powered by [Cacao](https://github.com/cacao-research/Cacao).

Instead of generating static HTML, CacaoDocs generates a Cacao app (`app.py`) that serves documentation with WebSocket-driven reactivity.

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
- **`cli.py`** - Click CLI with `build`, `serve`, `init` commands
- **`scanner.py`** - File discovery + AST extraction + API decorator auto-detection
- **`parser.py`** - Docstring parser with Type: directive and all doc type sections
- **`builder.py`** - Generates a Cacao app from parsed documentation
- **`config.py`** - YAML configuration loader with custom doc type parsing
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
title: "My Project"
description: "API Documentation"
version: "1.0.0"
theme: "dark"
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
- **cacao** (>=2.0.8) - Reactive web framework for rendering docs
- **click** - CLI framework
- **PyYAML** - Configuration loading
- **Markdown** - Markdown to HTML conversion
