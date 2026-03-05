# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

CacaoDocs is a Sphinx-like CLI tool that scans Python files, parses Google-style docstrings, and generates interactive documentation apps powered by [Cacao](https://github.com/cacao-research/Cacao).

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
- **`scanner.py`** - File discovery + AST extraction for Python/Markdown files
- **`parser.py`** - Google-style docstring parser
- **`builder.py`** - Generates a Cacao app from parsed documentation
- **`config.py`** - YAML configuration loader
- **`types.py`** - Dataclasses for parsed documentation

### Data Flow
```
Python files → AST Scanner → Docstring Parser → JSON Builder → Cacao App Generator
     ↓                                                              ↓
Markdown files ──────────────────────────────────────────────→ app.py + data.json
```

The generated `app.py` uses Cacao's `app_shell` with `nav_sidebar` for navigation, rendering modules, classes, functions, and pages as interactive panels.

### Core Types (`types.py`)
- **`ModuleDoc`** - Python module (name, path, docstring, classes, functions)
- **`ClassDoc`** - Class with methods and docstring
- **`FunctionDoc`** - Standalone function with signature and docstring
- **`MethodDoc`** - Class method with decorators
- **`PageDoc`** - Markdown page converted to HTML
- **`ParsedDocstring`** - Parsed docstring with args, returns, raises, examples

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
  - "node_modules"
```

### Google-Style Docstrings
CacaoDocs parses Google-style docstrings:

```python
def example_function(name: str, count: int = 1) -> list[str]:
    """Short summary line.

    Longer description that can span
    multiple lines.

    Args:
        name: The name to use.
        count: Number of times to repeat.

    Returns:
        List of repeated names.

    Raises:
        ValueError: If count is negative.

    Examples:
        >>> example_function("hello", 2)
        ['hello', 'hello']
    """
```

### Old Code
Previous React-based frontend code is preserved in `old/` for reference.

### Dependencies
- **cacao** (>=2.0.0) - Reactive web framework for rendering docs
- **click** - CLI framework
- **PyYAML** - Configuration loading
- **Markdown** - Markdown to HTML conversion
