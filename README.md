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

## Doc Types

CacaoDocs introduces a **doc type** system — categories that change how docstrings are parsed and displayed. Types can be set explicitly with a `Type:` directive or auto-detected from decorators.

### Built-in Types

| Type | Description | Auto-detected from |
|------|------------|-------------------|
| `function` | Regular functions and methods | Default for all functions |
| `api` | REST API endpoints | `@app.get`, `@router.post`, `@app.route`, etc. |
| `class` | Python classes | Class definitions |
| `page` | Markdown documentation | `.md` files |
| `config` | Settings and environment variables | `Type: config` directive |
| `event` | Webhooks, signals, pub/sub | `Type: event` directive |

### Function (default)

Standard Google-style docstrings work out of the box:

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

### API Endpoints

API endpoints are **auto-detected** from Flask, FastAPI, and Django REST decorators. You can also use additional API-specific sections:

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

Supported frameworks for auto-detection:
- **FastAPI**: `@app.get`, `@app.post`, `@router.put`, `@router.delete`, etc.
- **Flask**: `@app.route`, `@blueprint.route`
- **Django REST**: `@api_view`

The HTTP method and route path are extracted automatically from the decorator.

### Config

Document application settings with type, default values, required flags, and environment variable mappings:

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

### Event

Document webhooks, signals, and event handlers:

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

### Custom Types

Define your own doc types in `cacao.yaml`:

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

Then use them in your docstrings:

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

## Features

- **Doc Types** — Function, API, Class, Page, Config, Event, and Custom types
- **Auto-Detection** — Flask/FastAPI/Django endpoints detected from decorators
- **Call Map** — Visualize function call relationships across your codebase
- **Interactive App** — Generated docs are a live Cacao app, not static HTML
- **Google-style Docstrings** — Extended with API, config, and event sections
- **Custom Types** — Define your own doc types via `cacao.yaml`

## Contributing

Contributions are welcome — issues, feature requests, and pull requests.

## License

MIT
