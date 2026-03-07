"""CacaoDocs drop-in plugin for existing Cacao apps.

Usage:
    import cacao as c
    import cacaodocs

    c.config(title="My App", theme="dark")

    docs = cacaodocs.plug("./src")

    with c.app_shell(brand="My App"):
        with c.nav_sidebar():
            c.nav_item("Home", key="home", icon="home")
            docs.sidebar()  # injects doc nav items

        with c.shell_content():
            with c.nav_panel("home"):
                c.text("Welcome!")
            docs.panels()   # injects doc nav panels

Alternatively, plug() auto-injects into the sidebar slot if no manual
calls are needed:

    cacaodocs.plug("./src", auto_inject=True)
"""

from __future__ import annotations

from pathlib import Path
from typing import Any


class DocsPlugin:
    """Runtime docs plugin that provides sidebar and panel rendering."""

    def __init__(self, data: dict[str, Any], nav_key: str = "docs"):
        self.data = data
        self.nav_key = nav_key

        # Filter to items with docstrings (same logic as generated app)
        self.pages = data.get("pages", [])
        self.config = data.get("config", {})

        def _has_ds(item: dict) -> bool:
            ds = item.get("docstring")
            if not ds:
                return False
            if isinstance(ds, dict):
                return bool(ds.get("summary") or ds.get("description"))
            return bool(str(ds).strip())

        all_modules = data.get("modules", [])
        self.modules = [
            m
            for m in all_modules
            if m.get("docstring")
            or any(_has_ds(c) for c in m.get("classes", []))
            or any(_has_ds(f) for f in m.get("functions", []))
        ]
        self.classes = [c for c in data.get("classes", []) if _has_ds(c)]
        self.functions = [
            f for f in data.get("functions", []) if _has_ds(f) and not f.get("hidden")
        ]
        self.api_endpoints = [
            e
            for e in data.get("api_endpoints", [])
            if _has_ds(e) and not e.get("hidden")
        ]

        # Filter methods
        for cls in self.classes:
            cls["methods"] = [
                m
                for m in cls.get("methods", [])
                if (_has_ds(m) or m["name"] == "__init__") and not m.get("hidden")
            ]

    def sidebar(self) -> None:
        """Render sidebar nav items for documentation."""
        import cacao as c

        if self.modules:
            with c.nav_group("Modules", icon="folder"):
                for mod in self.modules:
                    label = (
                        mod["full_path"] if mod["name"] == "__init__" else mod["name"]
                    )
                    count = len(mod.get("classes", [])) + len(mod.get("functions", []))
                    c.nav_item(
                        label,
                        key=f"{self.nav_key}_mod_{mod['full_path']}",
                        icon="file",
                        badge=str(count),
                    )

        if self.classes:
            c.nav_item(
                "Types",
                key=f"{self.nav_key}_types",
                icon="box",
                badge=str(len(self.classes)),
            )

        if self.api_endpoints:
            c.nav_item(
                "API Reference",
                key=f"{self.nav_key}_api",
                icon="code",
                badge=str(len(self.api_endpoints)),
            )

        if self.pages:
            with c.nav_group("Pages", icon="book"):
                for page in self.pages:
                    c.nav_item(
                        page["title"],
                        key=f"{self.nav_key}_page_{page['slug']}",
                        icon="book",
                    )

    def panels(self) -> None:
        """Render all documentation nav panels."""
        import cacao as c

        METHOD_COLORS = {
            "GET": "success",
            "POST": "info",
            "PUT": "warning",
            "PATCH": "warning",
            "DELETE": "danger",
        }

        def _render_args_table(args: list, label: str = "Parameters") -> None:
            if not args:
                return
            c.spacer(3)
            c.title(label, level=4)
            c.spacer(1)
            table_data = []
            for arg in args:
                row = {"Name": arg["name"]}
                if arg.get("type"):
                    row["Type"] = arg["type"]
                row["Description"] = arg.get("description", "")
                if arg.get("default"):
                    row["Default"] = arg["default"]
                if arg.get("required"):
                    row["Required"] = "Yes"
                table_data.append(row)
            c.table(table_data, paginate=False, sortable=False)

        def _render_docstring(ds: dict) -> None:
            if ds.get("summary"):
                c.text(ds["summary"], size="lg")
            if ds.get("description"):
                c.spacer(2)
                c.text(ds["description"], color="muted")

            doc_type = ds.get("doc_type", "function")

            if doc_type == "api":
                method = ds.get("http_method", "")
                path = ds.get("path", "")
                if method or path:
                    c.spacer(2)
                    with c.row(gap=2, wrap=True):
                        if method:
                            c.badge(method, color=METHOD_COLORS.get(method, "default"))
                        if path:
                            c.code(path, language="text")
                _render_args_table(ds.get("path_params", []), "Path Parameters")
                _render_args_table(ds.get("query_params", []), "Query Parameters")
                _render_args_table(ds.get("request_body", []), "Request Body")

            _render_args_table(ds.get("args", []), "Parameters")

            ret = ds.get("returns")
            if ret:
                c.spacer(3)
                c.title("Returns", level=4)
                c.spacer(1)
                parts = []
                if ret.get("type"):
                    parts.append(ret["type"])
                if ret.get("description"):
                    parts.append(ret["description"])
                c.text(" — ".join(parts) if parts else "")

            raises = ds.get("raises", [])
            if raises:
                c.spacer(3)
                c.title("Raises", level=4)
                c.spacer(1)
                for r in raises:
                    c.text(f"{r['type']}: {r.get('description', '')}")

            _render_args_table(ds.get("attributes", []), "Attributes")

            examples = ds.get("examples", [])
            if examples:
                c.spacer(3)
                c.title("Examples", level=4)
                c.spacer(1)
                for ex in examples:
                    c.code(ex, language="python")

        def _render_function(func: dict) -> None:
            name = func["name"]
            sig = func.get("signature", "()")
            ds = func.get("docstring", {})
            doc_type = func.get("doc_type", "function")

            c.divider()
            c.spacer(2)
            c.anchor(func.get("full_path", name))

            if doc_type == "api":
                method = ds.get("http_method", "")
                path = ds.get("path", "")
                if method or path:
                    with c.row(gap=2, wrap=True):
                        if method:
                            c.badge(method, color=METHOD_COLORS.get(method, "default"))
                        c.text(path or name, size="lg")
                else:
                    c.code(f"def {name}{sig}", language="python")
            else:
                prefix = "async " if func.get("is_async") else ""
                c.code(f"{prefix}def {name}{sig}", language="python")

            # Badges
            badges = []
            if doc_type != "function":
                badges.append((doc_type, "info"))
            if func.get("is_async"):
                badges.append(("async", "warning"))
            if func.get("is_deprecated"):
                since = func.get("deprecation_since", "")
                badges.append(
                    (f"DEPRECATED since {since}" if since else "DEPRECATED", "danger")
                )
            if badges:
                c.spacer(1)
                with c.row(gap=2, wrap=True):
                    for label, color in badges:
                        c.badge(label, color=color)

            c.spacer(2)
            _render_docstring(ds)

            if func.get("source"):
                c.spacer(2)
                with c.tabs():
                    with c.tab(f"src_{name}", "Source Code"):
                        c.code(func["source"], language="python", line_numbers=True)

        # --- Module panels ---
        for mod in self.modules:
            with c.nav_panel(f"{self.nav_key}_mod_{mod['full_path']}"):
                label = mod["full_path"] if mod["name"] == "__init__" else mod["name"]
                c.title(label, level=2)
                if mod.get("docstring"):
                    c.spacer(2)
                    c.text(mod["docstring"])
                for func in mod.get("functions", []):
                    _render_function(func)

        # --- Types panel ---
        if self.classes:
            with c.nav_panel(f"{self.nav_key}_types"):
                c.title("Types Reference", level=2)
                c.text(f"{len(self.classes)} classes.", color="muted")
                c.spacer(4)
                for cls in self.classes:
                    c.anchor(f"type_{cls['full_path']}")
                    with c.card():
                        c.code(f"class {cls['name']}", language="python")
                        c.spacer(2)
                        _render_docstring(cls["docstring"])
                        for method in cls.get("methods", []):
                            _render_function(method)
                    c.spacer(3)

        # --- API panel ---
        if self.api_endpoints:
            with c.nav_panel(f"{self.nav_key}_api"):
                c.title("API Reference", level=2)
                c.text(f"{len(self.api_endpoints)} endpoints.", color="muted")
                c.spacer(4)
                for ep in self.api_endpoints:
                    ds = ep.get("docstring", {})
                    c.anchor(f"ep_{ep['full_path']}")
                    with c.card():
                        method = ds.get("http_method", "")
                        path = ds.get("path", "")
                        with c.row(gap=3, wrap=True):
                            if method:
                                c.badge(
                                    method, color=METHOD_COLORS.get(method, "default")
                                )
                            c.title(path or ep["name"], level=3)
                        c.spacer(2)
                        _render_docstring(ds)
                        if ep.get("source"):
                            c.spacer(3)
                            with c.tabs():
                                with c.tab(f"src_{ep['name']}", "Source Code"):
                                    c.code(
                                        ep["source"],
                                        language="python",
                                        line_numbers=True,
                                    )
                    c.spacer(3)

        # --- Page panels ---
        for page in self.pages:
            with c.nav_panel(f"{self.nav_key}_page_{page['slug']}"):
                c.title(page["title"], level=2)
                c.spacer(2)
                c.html(page.get("content", ""))


def _lazy_version() -> str:
    from . import __version__

    return __version__


def plug(
    source: str | Path,
    config: dict[str, Any] | None = None,
    nav_key: str = "docs",
    auto_inject: bool = False,
) -> DocsPlugin:
    """Register CacaoDocs as a drop-in plugin in the current Cacao app.

    Scans the source directory, registers with Cacao's plugin system,
    and returns a DocsPlugin with sidebar() and panels() methods.

    Args:
        source: Source directory containing Python/Markdown files.
        config: Optional config dict (defaults to cacao.yaml).
        nav_key: Key prefix for nav items (default "docs").
        auto_inject: If True, auto-inject sidebar via plugin slot system
            instead of requiring manual .sidebar() calls.

    Returns:
        DocsPlugin instance — call .sidebar() and .panels() in your app.
    """
    import cacao as c

    from .config import load_config
    from .parser import DocstringParser
    from .scanner import scan_directory
    from .builder import build_json

    if config is None:
        config = load_config()

    custom_types = config.get("custom_doc_types", [])
    parser = DocstringParser(custom_types=custom_types) if custom_types else None
    exclude_patterns = config.get("exclude_patterns", [])

    modules, pages = scan_directory(source, exclude_patterns, parser)
    json_data = build_json(modules, pages, config)

    docs = DocsPlugin(json_data, nav_key=nav_key)

    # Register as Cacao plugin
    plugin = c.register_plugin(
        "cacaodocs",
        version=_lazy_version(),
        description="Documentation plugin",
    )
    plugin.on(
        "on_ready",
        lambda: (
            c.notify(
                "Documentation loaded",
                f"{len(docs.functions)} functions, {len(docs.classes)} classes, "
                f"{len(docs.api_endpoints)} endpoints",
                variant="success",
            ),
            c.emit(
                "docs:loaded",
                {
                    "functions": len(docs.functions),
                    "classes": len(docs.classes),
                    "endpoints": len(docs.api_endpoints),
                    "pages": len(docs.pages),
                },
            ),
        ),
    )

    # Auto-inject sidebar via plugin slot system
    if auto_inject:
        plugin.inject("sidebar", lambda: docs.sidebar())

    return docs
