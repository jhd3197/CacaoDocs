# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

CacaoDocs v2 is a Sphinx-like CLI tool that scans Python files, parses Google-style docstrings, and generates static HTML documentation.

## Common Commands

### Building Documentation
```bash
cacaodocs build ./src -o ./docs         # Build docs from source directory
cacaodocs build ./my-project -o ./docs  # Build docs from any Python project
```

### Serving Documentation
```bash
cacaodocs serve ./docs                  # Serve docs locally on port 8000
cacaodocs serve ./docs -p 3000          # Use custom port
```

### Creating Configuration
```bash
cacaodocs init                          # Create default cacao.yaml
cacaodocs init -o myconfig.yaml         # Create with custom name
```

### Frontend Development
```bash
cd cacaodocs/frontend
npm install
npm start                   # Runs dev server on port 3005
npm run build               # Build for production
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
- **`builder.py`** - JSON builder + HTML generator
- **`config.py`** - YAML configuration loader
- **`types.py`** - Dataclasses for parsed documentation
- **`frontend/`** - React/TypeScript UI (Ant Design, FlexSearch)

### Data Flow
```
Python files → AST Scanner → Docstring Parser → JSON Builder → HTML Builder
     ↓                                                              ↓
Markdown files ──────────────────────────────────────────────→ Inject into
                                                               frontend build
```

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
github_url: "https://github.com/..."

theme:
  primary_color: "#8B4513"
  sidebar_bg_color: "#ffffff"
  # ... more theme options

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

### Frontend Routes
```
/              → Home (overview, stats)
/modules       → Module list
/modules/:id   → Module detail (classes, functions)
/classes       → Class list
/classes/:id   → Class detail (methods, attributes)
/functions     → Function list
/pages         → Markdown pages
/pages/:slug   → Page content
```

### Frontend Components
- **Layout/** - MainSidebar, SecondarySidebar, Layout wrapper
- **Pages/** - Home, Modules, Classes, Functions, Pages + Detail views
- **Search/** - GlobalSearch (Ctrl+K) with FlexSearch
