# CacaoDocs

A documentation generator for Python projects, powered by [Cacao](https://github.com/cacao-research/Cacao).

CacaoDocs scans your Python source code, parses docstrings, and generates an interactive documentation app with WebSocket-driven reactivity. No static HTML — your docs are a live app.

## Links

- **PyPI:** [cacaodocs](https://pypi.org/project/cacaodocs/)
- **GitHub:** [CacaoDocs](https://github.com/jhd3197/CacaoDocs)

## Installation

```bash
pip install cacaodocs
```

## Quick Start

```bash
# Initialize config (optional)
cacaodocs init

# Build docs from your source directory
cacaodocs build ./src -o ./docs

# Serve the generated docs
cacaodocs serve ./docs
```

## How Docstrings Work

CacaoDocs uses **Google-style docstrings** with one addition: a `Type:` directive that tells the parser what kind of thing you're documenting. If you don't specify a type, it defaults to `function`.

Here's the idea — you write normal docstrings, and CacaoDocs figures out what sections to parse based on the type:

| Type | What it's for | How it's detected |
|------|--------------|-------------------|
| `function` | Regular functions and methods | Default — no directive needed |
| `api` | REST API endpoints | Auto-detected from decorators like `@app.get`, `@router.post`, `@app.route` |
| `class` | Python classes | Detected from class definitions |
| `page` | Markdown documentation pages | `.md` files in your source directory |
| `config` | App settings and env vars | Set with `Type: config` |
| `event` | Webhooks, signals, pub/sub | Set with `Type: event` |
| Custom | Anything you define | Set with `Type: your_type_name` |

### Function (default)

The most common type. Just write standard Google-style docstrings — no `Type:` directive needed:

```python
def hash_password(password: str, salt: str = None) -> str:
    """Hash a password using bcrypt.

    Args:
        password (str): The plaintext password.
        salt (str): Optional salt. Generated if not provided.

    Returns:
        str: The hashed password string.

    Raises:
        ValueError: If password is empty or too short.

    Examples:
        >>> hash_password("mysecretpass")
        '$2b$12$...'
    """
```

**Available sections:** `Args`, `Returns`, `Raises`, `Examples`, `Notes`

### API Endpoints

API endpoints are **auto-detected** from Flask, FastAPI, and Django REST decorators — you don't need to add `Type: api`. CacaoDocs sees `@app.get(...)` and knows it's an API endpoint, extracting the HTTP method and route path for you.

```python
@app.get("/users/{user_id}")
def get_user(user_id: int):
    """Get a user by ID.

    Path Params:
        user_id (int): The user's unique identifier.

    Query Params:
        include (str): Comma-separated fields to include.

    Response (200):
        id (int): The user ID.
        name (str): Full name.
        email (str): Email address.

    Response (404):
        detail (str): User not found.
    """
```

**Auto-detected decorators:**
- **FastAPI**: `@app.get`, `@app.post`, `@router.put`, `@router.delete`, `@router.patch`
- **Flask**: `@app.route`, `@blueprint.route`
- **Django REST**: `@api_view`

**Available sections:** `Path Params`, `Query Params`, `Request Body`, `Headers`, `Response (NNN)`

### Config

For documenting application settings and environment variables. Use `Type: config` to enable config-specific parsing:

```python
def load_settings():
    """Application settings.

    Type: config

    Fields:
        DEBUG (bool, default=False): Enable debug mode.
        SECRET_KEY (str, required, env=APP_SECRET): Secret key for signing.
        DATABASE_URL (str, required, env=DATABASE_URL): PostgreSQL connection string.
        PORT (int, default=8000): Server port.
    """
```

Each field supports modifiers inside the parentheses:
- **type** — `str`, `int`, `bool`, etc.
- **`default=value`** — Default value
- **`required`** — Marks the field as required
- **`env=VAR_NAME`** — Maps to an environment variable

### Event

For documenting webhooks, signals, and event-driven patterns. Use `Type: event`:

```python
def on_user_signup(data: dict):
    """User signup event.

    Type: event

    Trigger: When a new user completes registration.

    Payload:
        user_id (int): The new user ID.
        email (str): The user's email.
        plan (str): Selected subscription plan.
    """
```

**Available sections:** `Trigger` (inline directive), `Payload`

### Custom Types

You can define your own doc types in `cacao.yaml`. Each custom type gets its own sections and display settings:

```yaml
doc_types:
  cli_command:
    label: "CLI Command"
    icon: "terminal"
    sections:
      - name: "Usage"
        format: code
      - name: "Options"
        format: args
      - name: "Flags"
        format: args

  database_model:
    label: "Model"
    icon: "database"
    sections:
      - name: "Fields"
        format: args
      - name: "Indexes"
      - name: "Relations"
```

Then use them with the `Type:` directive:

```python
def deploy():
    """Deploy the application.

    Type: cli_command

    Usage:
        deploy --env production --tag v1.2.3

    Options:
        env (str): Target environment.
        tag (str): Version tag to deploy.
    """
```

## Configuration

Create a `cacao.yaml` in your project root:

```yaml
title: "My Project"
description: "API Documentation"
version: "1.0.0"
theme: "dark"
github_url: "https://github.com/username/repo"

exclude_patterns:
  - "__pycache__"
  - ".venv"
  - "node_modules"
```

## Deploy to GitHub Pages

CacaoDocs can export a static version of your docs and deploy them to GitHub Pages. Add this workflow to `.github/workflows/docs.yml`:

```yaml
name: Deploy Docs to GitHub Pages

on:
  push:
    branches: [main]
  workflow_dispatch:

permissions:
  contents: read
  pages: write
  id-token: write

concurrency:
  group: pages
  cancel-in-progress: true

jobs:
  build-and-deploy:
    runs-on: ubuntu-latest
    environment:
      name: github-pages
      url: ${{ steps.deployment.outputs.page_url }}

    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"

      - name: Install dependencies
        run: |
          pip install cacaodocs
          pip install "cacao>=2.1.0"

      - name: Build docs
        run: cacaodocs build ./src -o ./_build

      - name: Export static site
        run: cacaodocs export ./_build -o ./dist --base-path /${{ github.event.repository.name }}

      - name: Upload Pages artifact
        uses: actions/upload-pages-artifact@v3
        with:
          path: dist

      - name: Deploy to GitHub Pages
        uses: actions/deploy-pages@v4
```

**Setup steps:**
1. Go to your repo's **Settings > Pages**
2. Set **Source** to **GitHub Actions**
3. Push the workflow file to `main` — it will build and deploy automatically

> **Note:** Change `./src` in the build step to wherever your Python source code lives. The `--base-path` flag is needed so links work correctly under `https://username.github.io/repo-name/`.

## The `@doc()` Decorator

Instead of (or in addition to) docstrings, you can use the `@doc()` decorator to define documentation as structured data. This avoids fragile docstring parsing entirely — CacaoDocs reads the keyword arguments directly from the AST.

```python
from cacaodocs import doc

@doc(
    description="Fetch a user by ID.",
    args={"user_id": {"type": "int", "description": "The user's unique identifier"}},
    returns={"type": "User", "description": "The matching user"},
    raises={"NotFoundError": "If user doesn't exist"},
    deprecated="2.0",
    category="Users",
    version="1.0",
)
def get_user(user_id: int) -> User:
    ...
```

The decorator is a **runtime no-op** — it just returns your function unchanged. Zero overhead. CacaoDocs reads the keyword arguments at scan time via AST, so there's nothing to parse or misparse.

### Decorator vs Docstring

You can use either approach, or both. When both exist, **decorator values win**.

```python
# Decorator only — no docstring needed
@doc(description="Add two numbers.", args={"a": "First", "b": "Second"}, returns="The sum")
def add(a, b):
    return a + b

# Supplement mode — docstring provides the basics, decorator adds metadata
@doc(category="Utils", version="3.0", deprecated=True)
def helper():
    """Reticulate the splines.

    Args:
        count (int): Number of splines.
    """
    ...
```

### Supported kwargs

**General:**

| Kwarg | Type | Description |
|-------|------|-------------|
| `description` | `str` | Summary text |
| `doc_type` | `str` | Override type: `"api"`, `"config"`, `"event"`, etc. |
| `deprecated` | `bool \| str` | `True` or a since-version string like `"2.0"` |
| `category` | `str` | Sidebar group name |
| `version` | `str` | Version when added |
| `hidden` | `bool` | Exclude from generated docs |

**Function sections:**

| Kwarg | Simple syntax | Full syntax |
|-------|--------------|-------------|
| `args` | `{"name": "desc"}` | `{"name": {"type": "str", "description": "...", "default": "x"}}` |
| `returns` | `"description"` | `{"type": "User", "description": "..."}` |
| `raises` | `{"ValueError": "when bad"}` | — |
| `examples` | `["example()"]` | — |
| `notes` | `["Note text"]` | — |
| `attributes` | Same as `args` | Same as `args` |

**API sections:**

| Kwarg | Type | Description |
|-------|------|-------------|
| `method` | `str` | HTTP method (`"GET"`, `"POST"`, etc.) |
| `path` | `str` | Route path (`"/users/{id}"`) |
| `path_params` | `dict` | Same format as `args` |
| `query_params` | `dict` | Same format as `args` |
| `request_body` | `dict` | Same format as `args` |
| `responses` | `dict` | `{200: "OK"}` or `{200: {"description": "...", "fields": {...}}}` |
| `headers` | `dict` | `{"Auth": "desc"}` or `{"Auth": {"description": "...", "required": True}}` |

**Event sections:**

| Kwarg | Type | Description |
|-------|------|-------------|
| `trigger` | `str` | Event trigger name |
| `payload` | `dict` | `{"field": {"type": "int", "description": "..."}}` |

**Config sections:**

| Kwarg | Type | Description |
|-------|------|-------------|
| `config_fields` | `dict` | `{"KEY": {"type": "bool", "default": "false", "env": "APP_KEY"}}` |

## Features

- **`@doc()` Decorator** — Structured metadata as an alternative to docstrings
- **Doc Types** — Function, API, Class, Page, Config, Event, and Custom types
- **Auto-Detection** — Flask/FastAPI/Django endpoints detected from decorators
- **Deprecation Tracking** — From decorators, docstrings, or `@doc(deprecated="2.0")`
- **Call Map** — Visualize function call relationships across your codebase
- **Dashboard** — Coverage scores, complexity hotspots, TODOs, dead code detection
- **Interactive App** — Generated docs are a live Cacao app, not static HTML
- **Google-style Docstrings** — Extended with API, config, and event sections
- **Custom Types** — Define your own doc types via `cacao.yaml`
- **Static Export** — Deploy to GitHub Pages or any static host

## Contributing

Contributions are welcome — issues, feature requests, and pull requests.

## License

MIT
