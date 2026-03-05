"""Build documentation as a Cacao app."""
import json
from pathlib import Path
from typing import Any

from .types import (
    ClassDoc,
    DocType,
    FunctionDoc,
    MethodDoc,
    ModuleDoc,
    PageDoc,
    ParsedDocstring,
)


def _serialize_docstring(docstring: ParsedDocstring) -> dict[str, Any]:
    result: dict[str, Any] = {
        "summary": docstring.summary,
        "description": docstring.description,
        "doc_type": docstring.doc_type.value,
        # Function sections
        "args": [
            {"name": a.name, "type": a.type, "description": a.description,
             "default": a.default, "required": a.required}
            for a in docstring.args
        ],
        "returns": (
            {"type": docstring.returns.type, "description": docstring.returns.description}
            if docstring.returns else None
        ),
        "raises": [
            {"type": r.type, "description": r.description} for r in docstring.raises
        ],
        "examples": docstring.examples,
        "attributes": [
            {"name": a.name, "type": a.type, "description": a.description,
             "default": a.default, "required": a.required}
            for a in docstring.attributes
        ],
        "notes": docstring.notes,
    }

    # API sections
    if docstring.doc_type == DocType.API or docstring.http_method or docstring.path:
        result["http_method"] = docstring.http_method
        result["path"] = docstring.path
        result["path_params"] = [
            {"name": a.name, "type": a.type, "description": a.description,
             "default": a.default, "required": a.required}
            for a in docstring.path_params
        ]
        result["query_params"] = [
            {"name": a.name, "type": a.type, "description": a.description,
             "default": a.default, "required": a.required}
            for a in docstring.query_params
        ]
        result["request_body"] = [
            {"name": a.name, "type": a.type, "description": a.description,
             "default": a.default, "required": a.required}
            for a in docstring.request_body
        ]
        result["responses"] = [
            {
                "status_code": r.status_code,
                "description": r.description,
                "fields": [
                    {"name": f.name, "type": f.type, "description": f.description}
                    for f in r.fields
                ],
            }
            for r in docstring.responses
        ]
        result["headers"] = [
            {"name": h.name, "description": h.description,
             "required": h.required, "example": h.example}
            for h in docstring.headers
        ]

    # Event sections
    if docstring.doc_type == DocType.EVENT or docstring.trigger or docstring.payload:
        result["trigger"] = docstring.trigger
        result["payload"] = [
            {"name": f.name, "type": f.type, "description": f.description}
            for f in docstring.payload
        ]

    # Config sections
    if docstring.doc_type == DocType.CONFIG or docstring.config_fields:
        result["config_fields"] = [
            {"name": f.name, "type": f.type, "description": f.description,
             "default": f.default, "required": f.required, "env_var": f.env_var}
            for f in docstring.config_fields
        ]

    # Custom sections
    if docstring.custom_sections:
        result["custom_sections"] = docstring.custom_sections

    return result


def _serialize_method(method: MethodDoc) -> dict[str, Any]:
    return {
        "name": method.name,
        "module": method.module,
        "signature": method.signature,
        "docstring": _serialize_docstring(method.docstring),
        "is_async": method.is_async,
        "is_classmethod": method.is_classmethod,
        "is_staticmethod": method.is_staticmethod,
        "is_property": method.is_property,
        "source": method.source,
        "line_number": method.line_number,
        "decorators": method.decorators,
        "calls": method.calls,
        "doc_type": method.doc_type.value,
    }


def _serialize_function(func: FunctionDoc) -> dict[str, Any]:
    return {
        "name": func.name,
        "module": func.module,
        "full_path": func.full_path,
        "signature": func.signature,
        "docstring": _serialize_docstring(func.docstring),
        "is_async": func.is_async,
        "source": func.source,
        "line_number": func.line_number,
        "decorators": func.decorators,
        "calls": func.calls,
        "doc_type": func.doc_type.value,
    }


def _serialize_class(cls: ClassDoc) -> dict[str, Any]:
    return {
        "name": cls.name,
        "module": cls.module,
        "full_path": cls.full_path,
        "docstring": _serialize_docstring(cls.docstring),
        "bases": cls.bases,
        "methods": [_serialize_method(m) for m in cls.methods],
        "source": cls.source,
        "line_number": cls.line_number,
        "decorators": cls.decorators,
        "doc_type": cls.doc_type.value,
    }


def _serialize_module(module: ModuleDoc) -> dict[str, Any]:
    return {
        "name": module.name,
        "full_path": module.full_path,
        "file_path": module.file_path,
        "docstring": module.docstring,
        "classes": [_serialize_class(c) for c in module.classes],
        "functions": [_serialize_function(f) for f in module.functions],
    }


def _serialize_page(page: PageDoc) -> dict[str, Any]:
    return {
        "title": page.title,
        "slug": page.slug,
        "content": page.content,
        "file_path": page.file_path,
        "order": page.order,
    }


def build_json(
    modules: list[ModuleDoc], pages: list[PageDoc], config: dict[str, Any]
) -> dict[str, Any]:
    """Build JSON documentation structure."""
    all_classes = []
    all_functions = []

    for module in modules:
        for cls in module.classes:
            all_classes.append(_serialize_class(cls))
        for func in module.functions:
            all_functions.append(_serialize_function(func))

    # Separate API endpoints from regular functions
    api_endpoints = [f for f in all_functions if f["doc_type"] == "api"]
    regular_functions = [f for f in all_functions if f["doc_type"] != "api"]

    return {
        "modules": [_serialize_module(m) for m in modules],
        "classes": all_classes,
        "functions": regular_functions,
        "api_endpoints": api_endpoints,
        "pages": [_serialize_page(p) for p in pages],
        "config": config,
    }


def _generate_app_code(json_data: dict[str, Any]) -> str:
    """Generate the Cacao app Python code for the documentation."""
    config = json_data.get("config", {})
    title = config.get("title", "Documentation")
    description = config.get("description", "")
    theme = config.get("theme", "dark")
    version = config.get("version", "")

    # Remove non-serializable items from config before embedding
    safe_config = {k: v for k, v in config.items()
                   if k not in ("custom_doc_types",)}
    safe_data = {**json_data, "config": safe_config}
    data_json = json.dumps(safe_data, ensure_ascii=False, default=str)

    code = f'''"""Auto-generated documentation app powered by CacaoDocs + Cacao."""
import json
import cacao as c

# --- Documentation Data ---
_DATA = json.loads({data_json!r})

_PAGES = _DATA["pages"]
_CONFIG = _DATA["config"]


def _has_docstring(item):
    """Check if an item has a meaningful docstring."""
    ds = item.get("docstring")
    if not ds:
        return False
    if isinstance(ds, dict):
        return bool(ds.get("summary") or ds.get("description"))
    if isinstance(ds, str):
        return bool(ds.strip())
    return False


# Filter: only items with actual docstrings
_ALL_MODULES = _DATA["modules"]
_CONTENT_MODULES = [m for m in _ALL_MODULES
                    if m.get("docstring")
                    or any(_has_docstring(c) for c in m.get("classes", []))
                    or any(_has_docstring(f) for f in m.get("functions", []))]

_CLASSES = [c for c in _DATA["classes"] if _has_docstring(c)]
_FUNCTIONS = [f for f in _DATA["functions"] if _has_docstring(f)]
_API_ENDPOINTS = [e for e in _DATA.get("api_endpoints", []) if _has_docstring(e)]

# Filter methods within classes
for cls in _CLASSES:
    cls["methods"] = [m for m in cls.get("methods", [])
                      if _has_docstring(m) or m["name"] == "__init__"]

for mod in _CONTENT_MODULES:
    mod["classes"] = [c for c in mod.get("classes", []) if _has_docstring(c)]
    mod["functions"] = [f for f in mod.get("functions", []) if _has_docstring(f)]
    for cls in mod["classes"]:
        cls["methods"] = [m for m in cls.get("methods", [])
                          if _has_docstring(m) or m["name"] == "__init__"]

# --- App Config ---
c.config(
    title={title!r},
    theme={theme!r},
)

# --- Helpers ---

_METHOD_COLORS = {{
    "GET": "success",
    "POST": "info",
    "PUT": "warning",
    "PATCH": "warning",
    "DELETE": "danger",
    "OPTIONS": "default",
    "HEAD": "default",
}}


def _render_args_table(args, label="Parameters"):
    """Render a list of args as a table."""
    if not args:
        return
    c.spacer(3)
    c.title(label, level=4)
    c.spacer(1)
    table_data = []
    for arg in args:
        row = {{"Name": arg["name"]}}
        if arg.get("type"):
            row["Type"] = arg["type"]
        row["Description"] = arg.get("description", "")
        if arg.get("default"):
            row["Default"] = arg["default"]
        if arg.get("required"):
            row["Required"] = "Yes"
        if arg.get("env_var"):
            row["Env Var"] = arg["env_var"]
        table_data.append(row)
    c.table(table_data, paginate=False, sortable=False)


def _render_docstring(docstring):
    """Render a parsed docstring."""
    if docstring.get("summary"):
        c.text(docstring["summary"], size="lg")

    if docstring.get("description"):
        c.spacer(2)
        c.text(docstring["description"], color="muted")

    doc_type = docstring.get("doc_type", "function")

    # --- API-specific rendering ---
    if doc_type == "api":
        # Method + Path badge
        method = docstring.get("http_method", "")
        path = docstring.get("path", "")
        if method or path:
            c.spacer(2)
            with c.row(gap=2, wrap=True):
                if method:
                    c.badge(method, color=_METHOD_COLORS.get(method, "default"))
                if path:
                    c.code(path, language="text")

        _render_args_table(docstring.get("path_params", []), "Path Parameters")
        _render_args_table(docstring.get("query_params", []), "Query Parameters")
        _render_args_table(docstring.get("request_body", []), "Request Body")

        # Headers
        headers = docstring.get("headers", [])
        if headers:
            c.spacer(3)
            c.title("Headers", level=4)
            c.spacer(1)
            table_data = []
            for h in headers:
                row = {{"Name": h["name"], "Description": h.get("description", "")}}
                if h.get("required"):
                    row["Required"] = "Yes"
                if h.get("example"):
                    row["Example"] = h["example"]
                table_data.append(row)
            c.table(table_data, paginate=False, sortable=False)

        # Responses
        responses = docstring.get("responses", [])
        if responses:
            c.spacer(3)
            c.title("Responses", level=4)
            c.spacer(1)
            for resp in responses:
                status = resp.get("status_code", "")
                desc = resp.get("description", "")
                color = "success" if 200 <= status < 300 else "warning" if 300 <= status < 400 else "danger"
                with c.card(f"{{status}} {{desc}}"):
                    c.badge(str(status), color=color)
                    if desc:
                        c.text(desc, color="muted")
                    fields = resp.get("fields", [])
                    if fields:
                        _render_args_table(fields, "Fields")

    # --- Event-specific rendering ---
    elif doc_type == "event":
        trigger = docstring.get("trigger", "")
        if trigger:
            c.spacer(2)
            c.title("Trigger", level=4)
            c.text(trigger)

        payload = docstring.get("payload", [])
        if payload:
            _render_args_table(payload, "Payload")

    # --- Config-specific rendering ---
    elif doc_type == "config":
        config_fields = docstring.get("config_fields", [])
        if config_fields:
            _render_args_table(config_fields, "Configuration Fields")

    # --- Standard function/class rendering ---
    _render_args_table(docstring.get("args", []), "Parameters")

    # Returns
    ret = docstring.get("returns")
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

    # Raises
    raises = docstring.get("raises", [])
    if raises:
        c.spacer(3)
        c.title("Raises", level=4)
        c.spacer(1)
        for r in raises:
            c.text(f'{{r["type"]}}: {{r.get("description", "")}}')

    # Attributes
    _render_args_table(docstring.get("attributes", []), "Attributes")

    # Examples
    examples = docstring.get("examples", [])
    if examples:
        c.spacer(3)
        c.title("Examples", level=4)
        c.spacer(1)
        for ex in examples:
            c.code(ex, language="python")

    # Notes
    notes = docstring.get("notes", [])
    if notes:
        c.spacer(3)
        for note in notes:
            c.alert(note, type="info")

    # Custom sections
    custom = docstring.get("custom_sections", {{}})
    for section_name, section_content in custom.items():
        c.spacer(3)
        c.title(section_name, level=4)
        c.spacer(1)
        c.text(section_content)


def _render_function_block(func):
    """Render a function as a section."""
    name = func["name"]
    sig = func.get("signature", "()")
    decorators = func.get("decorators", [])
    doc_type = func.get("doc_type", "function")

    c.divider()
    c.spacer(2)

    # For API endpoints, show method + path as header
    ds = func.get("docstring", {{}})
    if doc_type == "api":
        method = ds.get("http_method", "")
        path = ds.get("path", "")
        if method or path:
            with c.row(gap=2, wrap=True):
                if method:
                    c.badge(method, color=_METHOD_COLORS.get(method, "default"))
                c.text(f"{{path or name}}", size="lg")
        else:
            c.code(f"def {{name}}{{sig}}", language="python")
    else:
        prefix = "async " if func.get("is_async") else ""
        c.code(f"{{prefix}}def {{name}}{{sig}}", language="python")

    # Badges row
    badges = []
    if doc_type != "function":
        badges.append((doc_type, "info"))
    for dec in decorators:
        badges.append(("@" + dec, "default"))
    if func.get("is_async"):
        badges.append(("async", "warning"))
    if func.get("is_classmethod"):
        badges.append(("classmethod", "info"))
    if func.get("is_staticmethod"):
        badges.append(("staticmethod", "info"))
    if func.get("is_property"):
        badges.append(("property", "success"))

    if badges:
        c.spacer(1)
        with c.row(gap=2, wrap=True):
            for label, color in badges:
                c.badge(label, color=color)

    c.spacer(2)
    _render_docstring(ds)

    # Calls
    calls = func.get("calls", [])
    if calls:
        c.spacer(2)
        c.title("Calls", level=4)
        c.spacer(1)
        with c.row(gap=2, wrap=True):
            for call_name in calls:
                c.badge(call_name, color="default")

    # Source
    if func.get("source"):
        c.spacer(2)
        with c.tabs():
            with c.tab("src_" + name, "Source Code"):
                c.code(func["source"], language="python")

    c.spacer(3)


def _render_class_detail(cls):
    """Render full class documentation."""
    bases_str = ""
    if cls.get("bases"):
        bases_str = f'({{", ".join(cls["bases"])}})'

    c.code(f'class {{cls["name"]}}{{bases_str}}', language="python")

    if cls.get("decorators"):
        c.spacer(1)
        with c.row(gap=2, wrap=True):
            for dec in cls["decorators"]:
                c.badge(f"@{{dec}}", color="info")

    c.spacer(2)
    _render_docstring(cls["docstring"])

    init_method = next((m for m in cls.get("methods", []) if m["name"] == "__init__"), None)
    if init_method:
        c.spacer(3)
        c.title("Constructor", level=3)
        _render_function_block(init_method)

    methods = [m for m in cls.get("methods", []) if not m["name"].startswith("_")]
    if methods:
        c.spacer(2)
        c.title("Methods", level=3)
        for method in methods:
            _render_function_block(method)

    private_methods = [m for m in cls.get("methods", [])
                       if m["name"].startswith("_") and m["name"] != "__init__"]
    if private_methods:
        c.spacer(2)
        with c.tabs():
            with c.tab("private", f"Private Methods ({{len(private_methods)}})"):
                for method in private_methods:
                    _render_function_block(method)


# =============================================================================
# Build the App
# =============================================================================

_default_key = "home"

with c.app_shell(brand={title!r}, default=_default_key, theme_dark="dark", theme_light="light"):
    with c.nav_sidebar():
        c.nav_item("Home", key="home", icon="home")

        if _CONTENT_MODULES:
            with c.nav_group("Modules", icon="folder"):
                for mod in _CONTENT_MODULES:
                    label = mod["full_path"] if mod["name"] == "__init__" else mod["name"]
                    badge_count = str(len(mod.get("classes", [])) + len(mod.get("functions", [])))
                    c.nav_item(label, key=f"mod_{{mod['full_path']}}", icon="file", badge=badge_count)

        if _CLASSES:
            with c.nav_group("Classes", icon="box"):
                for cls in _CLASSES:
                    method_count = str(len(cls.get("methods", [])))
                    c.nav_item(cls["name"], key=f"cls_{{cls['full_path']}}", icon="box", badge=method_count)

        # API Endpoints section
        if _API_ENDPOINTS:
            with c.nav_group("API", icon="code"):
                for ep in _API_ENDPOINTS:
                    ds = ep.get("docstring", {{}})
                    method = ds.get("http_method", "")
                    path = ds.get("path", "")
                    label = f"{{method}} {{path}}" if method and path else ep["name"]
                    c.nav_item(label, key=f"api_{{ep['full_path']}}", icon="code")

        c.nav_item("Call Map", key="callmap", icon="code")

        if _PAGES:
            with c.nav_group("Pages", icon="book"):
                for page in _PAGES:
                    c.nav_item(page["title"], key=f"page_{{page['slug']}}", icon="book")

    with c.shell_content():

        # --- Home ---
        with c.nav_panel("home"):
            c.title({title!r})
            if {description!r}:
                c.text({description!r}, size="lg", color="muted")
            c.spacer(4)

            with c.row(wrap=True, gap=4):
                c.metric("Modules", len(_CONTENT_MODULES))
                c.metric("Classes", len(_CLASSES))
                c.metric("Functions", len(_FUNCTIONS))
                if _API_ENDPOINTS:
                    c.metric("API Endpoints", len(_API_ENDPOINTS))
                if _PAGES:
                    c.metric("Pages", len(_PAGES))

            if {version!r}:
                c.spacer(3)
                c.badge(f"v{{{version!r}}}", color="info")

            # Quick overview
            if _CONTENT_MODULES:
                c.spacer(4)
                c.title("Modules", level=3)
                c.spacer(2)
                for mod in _CONTENT_MODULES:
                    label = mod["full_path"] if mod["name"] == "__init__" else mod["name"]
                    with c.card(label):
                        if mod.get("docstring"):
                            first_line = mod["docstring"].split("\\n")[0].strip()
                            c.text(first_line, color="muted")
                        with c.row(gap=2):
                            if mod.get("classes"):
                                c.badge(f'{{len(mod["classes"])}} classes', color="info")
                            if mod.get("functions"):
                                c.badge(f'{{len(mod["functions"])}} functions', color="default")

            # API overview on home
            if _API_ENDPOINTS:
                c.spacer(4)
                c.title("API Endpoints", level=3)
                c.spacer(2)
                table_data = []
                for ep in _API_ENDPOINTS:
                    ds = ep.get("docstring", {{}})
                    method = ds.get("http_method", "")
                    path = ds.get("path", "")
                    table_data.append({{
                        "Method": method,
                        "Path": path,
                        "Summary": ds.get("summary", ""),
                    }})
                c.table(table_data, paginate=False)

        # --- Module Panels ---
        for mod in _CONTENT_MODULES:
            with c.nav_panel(f"mod_{{mod['full_path']}}"):
                mod_label = mod["full_path"] if mod["name"] == "__init__" else mod["name"]
                c.title(mod_label, level=2)

                if mod.get("file_path"):
                    c.text(mod["file_path"], size="sm", color="muted")

                if mod.get("docstring"):
                    c.spacer(2)
                    c.text(mod["docstring"])

                if mod.get("classes"):
                    c.spacer(4)
                    c.title("Classes", level=3)
                    c.spacer(2)
                    for cls in mod["classes"]:
                        with c.card(f'class {{cls["name"]}}'):
                            _render_docstring(cls["docstring"])
                            pub_methods = [m for m in cls.get("methods", []) if not m["name"].startswith("_")]
                            if pub_methods:
                                c.spacer(2)
                                c.badge(f"{{len(pub_methods)}} methods", color="info")

                if mod.get("functions"):
                    c.spacer(4)
                    c.title("Functions", level=3)
                    for func in mod["functions"]:
                        _render_function_block(func)

        # --- Class Panels ---
        for cls in _CLASSES:
            with c.nav_panel(f"cls_{{cls['full_path']}}"):
                c.title(cls["name"], level=2)
                if cls.get("module"):
                    c.text(cls["module"], size="sm", color="muted")
                c.spacer(3)
                _render_class_detail(cls)

        # --- API Endpoint Panels ---
        for ep in _API_ENDPOINTS:
            with c.nav_panel(f"api_{{ep['full_path']}}"):
                ds = ep.get("docstring", {{}})
                method = ds.get("http_method", "")
                path = ds.get("path", "")

                # Header with method badge + path
                with c.row(gap=3, wrap=True):
                    if method:
                        c.badge(method, color=_METHOD_COLORS.get(method, "default"))
                    c.title(path or ep["name"], level=2)

                if ep.get("module"):
                    c.text(f'{{ep["module"]}}.{{ep["name"]}}', size="sm", color="muted")

                c.spacer(3)
                _render_docstring(ds)

                # Source
                if ep.get("source"):
                    c.spacer(3)
                    with c.tabs():
                        with c.tab("src_" + ep["name"], "Source Code"):
                            c.code(ep["source"], language="python")

        # --- Call Map Panel ---
        with c.nav_panel("callmap"):
            c.title("Call Map", level=2)
            c.text("Function and method call relationships across the codebase.", color="muted")
            c.spacer(3)

            _all_known = set()
            _call_entries = []

            for func in _FUNCTIONS:
                _all_known.add(func["full_path"])
                _all_known.add(func["name"])
            for ep in _API_ENDPOINTS:
                _all_known.add(ep["full_path"])
                _all_known.add(ep["name"])
            for cls in _CLASSES:
                _all_known.add(cls["full_path"])
                for m in cls.get("methods", []):
                    _all_known.add(f'{{cls["full_path"]}}.{{m["name"]}}')
                    _all_known.add(m["name"])

            all_funcs = _FUNCTIONS + _API_ENDPOINTS
            for func in all_funcs:
                calls = func.get("calls", [])
                if calls:
                    internal = [c for c in calls if c in _all_known or c.split(".")[-1] in _all_known]
                    external = [c for c in calls if c not in internal]
                    if internal or external:
                        _call_entries.append({{
                            "caller": func["full_path"],
                            "internal": internal,
                            "external": external,
                        }})

            for cls in _CLASSES:
                for m in cls.get("methods", []):
                    calls = m.get("calls", [])
                    if calls:
                        caller = f'{{cls["full_path"]}}.{{m["name"]}}'
                        internal = [c for c in calls if c in _all_known or c.split(".")[-1] in _all_known]
                        external = [c for c in calls if c not in internal]
                        if internal or external:
                            _call_entries.append({{
                                "caller": caller,
                                "internal": internal,
                                "external": external,
                            }})

            if _call_entries:
                table_data = []
                for entry in _call_entries:
                    table_data.append({{
                        "Caller": entry["caller"],
                        "Internal Calls": ", ".join(entry["internal"]) if entry["internal"] else "—",
                        "External Calls": str(len(entry["external"])),
                    }})
                c.table(table_data, searchable=True, page_size=20)

                c.spacer(4)
                c.title("Details", level=3)
                c.spacer(2)
                for entry in _call_entries:
                    if entry["internal"]:
                        with c.card(entry["caller"]):
                            c.title("Calls (internal)", level=4)
                            with c.row(gap=2, wrap=True):
                                for call_name in entry["internal"]:
                                    c.badge(call_name, color="info")
                            if entry["external"]:
                                c.spacer(2)
                                c.title("Calls (external)", level=4)
                                with c.row(gap=2, wrap=True):
                                    for call_name in entry["external"][:15]:
                                        c.badge(call_name, color="default")
                                    if len(entry["external"]) > 15:
                                        c.text(f'... and {{len(entry["external"]) - 15}} more', size="sm", color="muted")
            else:
                c.text("No call relationships found.", color="muted")

        # --- Page Panels ---
        for page in _PAGES:
            with c.nav_panel(f"page_{{page['slug']}}"):
                c.title(page["title"], level=2)
                c.spacer(2)
                c.html(page.get("content", ""))
'''

    return code


def build_docs(
    source: str | Path,
    output: str | Path,
    config: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Build documentation from source directory.

    Scans Python/Markdown files and generates a Cacao app.

    Args:
        source: Source directory containing Python/Markdown files.
        output: Output directory for the generated Cacao app.
        config: Optional configuration dictionary.

    Returns:
        The generated JSON documentation data.
    """
    from .scanner import scan_directory
    from .config import load_config
    from .parser import DocstringParser

    if config is None:
        config = load_config()

    # Create parser with custom doc types
    custom_types = config.get("custom_doc_types", [])
    parser = DocstringParser(custom_types=custom_types) if custom_types else None

    exclude_patterns = config.get("exclude_patterns", [])
    modules, pages = scan_directory(source, exclude_patterns, parser)

    json_data = build_json(modules, pages, config)

    output_dir = Path(output)
    output_dir.mkdir(parents=True, exist_ok=True)

    app_code = _generate_app_code(json_data)
    app_path = output_dir / "app.py"

    with open(app_path, "w", encoding="utf-8") as f:
        f.write(app_code)

    data_path = output_dir / "data.json"
    with open(data_path, "w", encoding="utf-8") as f:
        json.dump(json_data, f, indent=2, ensure_ascii=False, default=str)

    return json_data
