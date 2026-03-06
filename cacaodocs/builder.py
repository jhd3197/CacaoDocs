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
            {
                "name": a.name,
                "type": a.type,
                "description": a.description,
                "default": a.default,
                "required": a.required,
            }
            for a in docstring.args
        ],
        "returns": (
            {
                "type": docstring.returns.type,
                "description": docstring.returns.description,
            }
            if docstring.returns
            else None
        ),
        "raises": [
            {"type": r.type, "description": r.description} for r in docstring.raises
        ],
        "examples": docstring.examples,
        "attributes": [
            {
                "name": a.name,
                "type": a.type,
                "description": a.description,
                "default": a.default,
                "required": a.required,
            }
            for a in docstring.attributes
        ],
        "notes": docstring.notes,
    }

    # API sections
    if docstring.doc_type == DocType.API or docstring.http_method or docstring.path:
        result["http_method"] = docstring.http_method
        result["path"] = docstring.path
        result["path_params"] = [
            {
                "name": a.name,
                "type": a.type,
                "description": a.description,
                "default": a.default,
                "required": a.required,
            }
            for a in docstring.path_params
        ]
        result["query_params"] = [
            {
                "name": a.name,
                "type": a.type,
                "description": a.description,
                "default": a.default,
                "required": a.required,
            }
            for a in docstring.query_params
        ]
        result["request_body"] = [
            {
                "name": a.name,
                "type": a.type,
                "description": a.description,
                "default": a.default,
                "required": a.required,
            }
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
            {
                "name": h.name,
                "description": h.description,
                "required": h.required,
                "example": h.example,
            }
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
            {
                "name": f.name,
                "type": f.type,
                "description": f.description,
                "default": f.default,
                "required": f.required,
                "env_var": f.env_var,
            }
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
        "signature_hash": method.signature_hash,
        "body_hash": method.body_hash,
        "complexity": method.complexity,
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
        "signature_hash": func.signature_hash,
        "body_hash": func.body_hash,
        "complexity": func.complexity,
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
        "signature_hash": cls.signature_hash,
        "body_hash": cls.body_hash,
    }


def _serialize_module(module: ModuleDoc) -> dict[str, Any]:
    return {
        "name": module.name,
        "full_path": module.full_path,
        "file_path": module.file_path,
        "docstring": module.docstring,
        "classes": [_serialize_class(c) for c in module.classes],
        "functions": [_serialize_function(f) for f in module.functions],
        "todos": [
            {
                "tag": t.tag,
                "text": t.text,
                "file_path": t.file_path,
                "line_number": t.line_number,
                "module": t.module,
            }
            for t in module.todos
        ],
    }


def _serialize_page(page: PageDoc) -> dict[str, Any]:
    return {
        "title": page.title,
        "slug": page.slug,
        "content": page.content,
        "file_path": page.file_path,
        "order": page.order,
    }


def _compute_changes(
    old_data: dict[str, Any], new_data: dict[str, Any]
) -> list[dict[str, Any]]:
    """Compare old and new build data to detect function/endpoint changes.

    Returns a list of change records with keys:
        - full_path: The function/class identifier
        - name: Display name
        - doc_type: function, api, class, etc.
        - change: "new", "removed", "signature", "body", "signature+body"
    """
    changes: list[dict[str, Any]] = []

    def _index_items(data: dict[str, Any]) -> dict[str, dict[str, str]]:
        """Build a lookup: full_path -> {signature_hash, body_hash, name, doc_type}."""
        index: dict[str, dict[str, str]] = {}
        for item in data.get("functions", []):
            index[item["full_path"]] = {
                "signature_hash": item.get("signature_hash", ""),
                "body_hash": item.get("body_hash", ""),
                "name": item["name"],
                "doc_type": item.get("doc_type", "function"),
            }
        for item in data.get("api_endpoints", []):
            index[item["full_path"]] = {
                "signature_hash": item.get("signature_hash", ""),
                "body_hash": item.get("body_hash", ""),
                "name": item["name"],
                "doc_type": item.get("doc_type", "api"),
            }
        for item in data.get("classes", []):
            index[item["full_path"]] = {
                "signature_hash": item.get("signature_hash", ""),
                "body_hash": item.get("body_hash", ""),
                "name": item["name"],
                "doc_type": item.get("doc_type", "class"),
            }
            for method in item.get("methods", []):
                method_path = f"{item['full_path']}.{method['name']}"
                index[method_path] = {
                    "signature_hash": method.get("signature_hash", ""),
                    "body_hash": method.get("body_hash", ""),
                    "name": method["name"],
                    "doc_type": method.get("doc_type", "function"),
                }
        return index

    old_index = _index_items(old_data)
    new_index = _index_items(new_data)

    all_paths = set(old_index) | set(new_index)

    for path in sorted(all_paths):
        old = old_index.get(path)
        new = new_index.get(path)

        if new and not old:
            changes.append({
                "full_path": path,
                "name": new["name"],
                "doc_type": new["doc_type"],
                "change": "new",
            })
        elif old and not new:
            changes.append({
                "full_path": path,
                "name": old["name"],
                "doc_type": old["doc_type"],
                "change": "removed",
            })
        elif old and new:
            sig_changed = old["signature_hash"] != new["signature_hash"]
            body_changed = old["body_hash"] != new["body_hash"]
            if sig_changed and body_changed:
                change_type = "signature+body"
            elif sig_changed:
                change_type = "signature"
            elif body_changed:
                change_type = "body"
            else:
                continue
            changes.append({
                "full_path": path,
                "name": new["name"],
                "doc_type": new["doc_type"],
                "change": change_type,
            })

    return changes


def _detect_breaking_changes(
    old_data: dict[str, Any], new_data: dict[str, Any]
) -> list[dict[str, Any]]:
    """Detect breaking vs non-breaking signature changes between builds.

    Compares function arguments to classify changes as:
        - arg_removed: An argument was removed
        - arg_renamed: An argument name changed
        - type_changed: An argument's type annotation changed
        - required_arg_added: A new argument without a default was added
        - optional_arg_added: A new argument with a default was added (non-breaking)
        - return_type_changed: Return type annotation changed
    """
    breaking: list[dict[str, Any]] = []

    def _index_with_args(data: dict[str, Any]) -> dict[str, dict[str, Any]]:
        index: dict[str, dict[str, Any]] = {}
        for lst in ("functions", "api_endpoints"):
            for item in data.get(lst, []):
                ds = item.get("docstring", {})
                index[item["full_path"]] = {
                    "name": item["name"],
                    "doc_type": item.get("doc_type", "function"),
                    "args": {
                        a["name"]: a for a in ds.get("args", [])
                    },
                    "returns": ds.get("returns"),
                    "signature": item.get("signature", ""),
                    "signature_hash": item.get("signature_hash", ""),
                }
        return index

    old_idx = _index_with_args(old_data)
    new_idx = _index_with_args(new_data)

    for path in set(old_idx) & set(new_idx):
        old = old_idx[path]
        new = new_idx[path]

        if old["signature_hash"] == new["signature_hash"]:
            continue

        details: list[dict[str, str]] = []

        old_args = old["args"]
        new_args = new["args"]

        # Removed args
        for name in old_args:
            if name not in new_args:
                details.append({"type": "arg_removed", "arg": name, "breaking": True})

        # New args
        for name in new_args:
            if name not in old_args:
                has_default = new_args[name].get("default") is not None
                if has_default:
                    details.append({"type": "optional_arg_added", "arg": name, "breaking": False})
                else:
                    details.append({"type": "required_arg_added", "arg": name, "breaking": True})

        # Type changes on existing args
        for name in old_args:
            if name in new_args:
                old_type = old_args[name].get("type", "")
                new_type = new_args[name].get("type", "")
                if old_type and new_type and old_type != new_type:
                    details.append({
                        "type": "type_changed",
                        "arg": name,
                        "from": old_type,
                        "to": new_type,
                        "breaking": True,
                    })

        # Return type change
        old_ret = old.get("returns") or {}
        new_ret = new.get("returns") or {}
        if old_ret.get("type") and new_ret.get("type") and old_ret["type"] != new_ret["type"]:
            details.append({
                "type": "return_type_changed",
                "from": old_ret["type"],
                "to": new_ret["type"],
                "breaking": True,
            })

        if details:
            is_breaking = any(d.get("breaking") for d in details)
            breaking.append({
                "full_path": path,
                "name": new["name"],
                "doc_type": new["doc_type"],
                "is_breaking": is_breaking,
                "details": details,
            })

    return breaking


def _compute_coverage(json_data: dict[str, Any]) -> dict[str, Any]:
    """Compute documentation coverage scores.

    Returns per-function scores and a project-wide summary.
    """
    items: list[dict[str, Any]] = []
    total_score = 0.0
    count = 0

    for lst in ("functions", "api_endpoints"):
        for func in json_data.get(lst, []):
            ds = func.get("docstring", {})
            score = 0.0
            checks = {
                "has_docstring": bool(ds.get("summary")),
                "has_args_documented": True,
                "has_returns": False,
                "has_examples": bool(ds.get("examples")),
            }

            # Check if all actual params are documented
            sig = func.get("signature", "")
            # Count params from signature (rough: count commas + 1, minus self)
            doc_args = {a["name"] for a in ds.get("args", [])}

            # Check returns
            checks["has_returns"] = ds.get("returns") is not None

            # Score: docstring=40%, args=30%, returns=20%, examples=10%
            if checks["has_docstring"]:
                score += 40
            if checks["has_args_documented"] and doc_args:
                score += 30
            elif not doc_args and not sig.strip("()"):
                # No params to document
                score += 30
            if checks["has_returns"]:
                score += 20
            if checks["has_examples"]:
                score += 10

            items.append({
                "full_path": func.get("full_path", func["name"]),
                "name": func["name"],
                "doc_type": func.get("doc_type", "function"),
                "score": score,
                "checks": checks,
            })
            total_score += score
            count += 1

    for cls in json_data.get("classes", []):
        ds = cls.get("docstring", {})
        score = 0.0
        checks = {
            "has_docstring": bool(ds.get("summary")),
            "has_attributes": bool(ds.get("attributes")),
            "has_methods_documented": False,
        }

        # Check if methods have docstrings
        methods = cls.get("methods", [])
        documented_methods = sum(
            1 for m in methods if m.get("docstring", {}).get("summary")
        )
        if methods:
            checks["has_methods_documented"] = documented_methods == len(methods)

        if checks["has_docstring"]:
            score += 50
        if checks["has_attributes"]:
            score += 25
        if checks["has_methods_documented"]:
            score += 25
        elif not methods:
            score += 25

        items.append({
            "full_path": cls.get("full_path", cls["name"]),
            "name": cls["name"],
            "doc_type": "class",
            "score": score,
            "checks": checks,
        })
        total_score += score
        count += 1

    return {
        "project_score": round(total_score / count, 1) if count else 0,
        "total_items": count,
        "fully_documented": sum(1 for i in items if i["score"] == 100),
        "undocumented": sum(1 for i in items if i["score"] == 0),
        "items": items,
    }


def _build_reverse_call_map(json_data: dict[str, Any]) -> dict[str, list[str]]:
    """Invert the call graph: for each function, who calls it.

    Returns a dict mapping function name -> list of callers.
    """
    called_by: dict[str, list[str]] = {}

    for lst in ("functions", "api_endpoints"):
        for func in json_data.get(lst, []):
            caller = func.get("full_path", func["name"])
            for callee in func.get("calls", []):
                called_by.setdefault(callee, []).append(caller)

    for cls in json_data.get("classes", []):
        for method in cls.get("methods", []):
            caller = f"{cls.get('full_path', cls['name'])}.{method['name']}"
            for callee in method.get("calls", []):
                called_by.setdefault(callee, []).append(caller)

    # Sort each list for determinism
    return {k: sorted(v) for k, v in sorted(called_by.items())}


def _collect_todos(json_data: dict[str, Any]) -> list[dict[str, Any]]:
    """Collect all TODOs from all modules into a flat list."""
    todos: list[dict[str, Any]] = []
    for module in json_data.get("modules", []):
        todos.extend(module.get("todos", []))
    return todos


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

    # Apply page_order from config if provided
    page_order = config.get("page_order", [])
    if page_order:
        order_map = {slug: i for i, slug in enumerate(page_order)}
        pages = sorted(
            pages,
            key=lambda p: (
                order_map.get(p.slug, len(page_order)),
                p.order,
                p.title,
            ),
        )

    json_data = {
        "modules": [_serialize_module(m) for m in modules],
        "classes": all_classes,
        "functions": regular_functions,
        "api_endpoints": api_endpoints,
        "pages": [_serialize_page(p) for p in pages],
        "config": config,
    }

    # Coverage scores
    json_data["coverage"] = _compute_coverage(json_data)

    # Reverse call map
    json_data["called_by"] = _build_reverse_call_map(json_data)

    # Flat TODO list
    json_data["todos"] = _collect_todos(json_data)

    return json_data


def _chunk_documentation(json_data: dict[str, Any]) -> list[dict[str, str]]:
    """Convert documentation JSON into text chunks for embedding.

    Each chunk has: text, source (identifier), type (function/class/api/page).
    """
    chunks: list[dict[str, str]] = []

    for func in json_data.get("functions", []):
        ds = func.get("docstring", {})
        parts = [f"Function: {func['name']}"]
        if func.get("signature"):
            parts[0] += func["signature"]
        if ds.get("summary"):
            parts.append(ds["summary"])
        if ds.get("description"):
            parts.append(ds["description"])
        for arg in ds.get("args", []):
            parts.append(
                f"  param {arg['name']}: {arg.get('type', '')} - {arg.get('description', '')}"
            )
        ret = ds.get("returns")
        if ret:
            parts.append(
                f"  returns: {ret.get('type', '')} - {ret.get('description', '')}"
            )
        for ex in ds.get("examples", []):
            parts.append(f"  example: {ex}")
        chunks.append(
            {
                "text": "\n".join(parts),
                "source": func.get("full_path", func["name"]),
                "type": "function",
            }
        )

    for ep in json_data.get("api_endpoints", []):
        ds = ep.get("docstring", {})
        method = ds.get("http_method", "")
        path = ds.get("path", "")
        parts = [f"API: {method} {path}"]
        if ds.get("summary"):
            parts.append(ds["summary"])
        if ds.get("description"):
            parts.append(ds["description"])
        for param in ds.get("path_params", []) + ds.get("query_params", []):
            parts.append(
                f"  param {param['name']}: {param.get('type', '')} - {param.get('description', '')}"
            )
        chunks.append(
            {
                "text": "\n".join(parts),
                "source": f"{method} {path}"
                if method
                else ep.get("full_path", ep["name"]),
                "type": "api",
            }
        )

    for cls in json_data.get("classes", []):
        ds = cls.get("docstring", {})
        parts = [f"Class: {cls['name']}"]
        if ds.get("summary"):
            parts.append(ds["summary"])
        if ds.get("description"):
            parts.append(ds["description"])
        for attr in ds.get("attributes", []):
            parts.append(
                f"  attr {attr['name']}: {attr.get('type', '')} - {attr.get('description', '')}"
            )
        for m in cls.get("methods", []):
            mds = m.get("docstring", {})
            parts.append(f"  method {m['name']}: {mds.get('summary', '')}")
        chunks.append(
            {
                "text": "\n".join(parts),
                "source": cls.get("full_path", cls["name"]),
                "type": "class",
            }
        )

    for page in json_data.get("pages", []):
        # Split long pages into ~2000 char paragraphs
        content = page.get("content", "")
        # Strip HTML tags for embedding
        import re

        clean = re.sub(r"<[^>]+>", " ", content)
        clean = re.sub(r"\s+", " ", clean).strip()
        if not clean:
            continue
        # Chunk long pages
        max_chunk = 2000
        if len(clean) <= max_chunk:
            chunks.append(
                {
                    "text": f"Page: {page['title']}\n{clean}",
                    "source": page["title"],
                    "type": "page",
                }
            )
        else:
            sentences = clean.split(". ")
            current = f"Page: {page['title']}\n"
            for sent in sentences:
                if len(current) + len(sent) > max_chunk:
                    chunks.append(
                        {
                            "text": current.strip(),
                            "source": page["title"],
                            "type": "page",
                        }
                    )
                    current = f"Page: {page['title']} (cont.)\n"
                current += sent + ". "
            if current.strip():
                chunks.append(
                    {
                        "text": current.strip(),
                        "source": page["title"],
                        "type": "page",
                    }
                )

    return chunks


def _embed_chunks(
    chunks: list[dict[str, str]], embedding_model: str
) -> dict[str, Any] | None:
    """Embed text chunks using Prompture's embedding driver.

    Returns the embeddings dict, or None if embedding fails.
    """
    if not chunks:
        return None

    try:
        from prompture.drivers.embedding_registry import get_embedding_driver_for_model  # type: ignore[import-not-found]
    except ImportError:
        return None

    try:
        driver = get_embedding_driver_for_model(embedding_model)
        texts = [c["text"] for c in chunks]
        result = driver.embed(texts, {})
        embeddings = result.get("embeddings", [])
        if not embeddings:
            return None

        return {
            "model": embedding_model,
            "dimensions": result.get("meta", {}).get("dimensions", len(embeddings[0])),
            "chunks": [
                {
                    "text": chunks[i]["text"],
                    "source": chunks[i]["source"],
                    "type": chunks[i]["type"],
                    "embedding": embeddings[i],
                }
                for i in range(len(chunks))
            ],
        }
    except Exception as e:
        import logging

        logging.getLogger("cacaodocs").warning("Embedding failed: %s", e)
        return None


def _is_light_color(hex_color: str) -> bool:
    """Check if a hex color is light based on luminance."""
    hex_color = hex_color.lstrip("#")
    if len(hex_color) == 3:
        hex_color = "".join(c * 2 for c in hex_color)
    try:
        r, g, b = (
            int(hex_color[0:2], 16),
            int(hex_color[2:4], 16),
            int(hex_color[4:6], 16),
        )
        luminance = (0.299 * r + 0.587 * g + 0.114 * b) / 255
        return luminance > 0.5
    except (ValueError, IndexError):
        return False


def _generate_app_code(json_data: dict[str, Any]) -> str:
    """Generate the Cacao app Python code for the documentation."""
    config = json_data.get("config", {})
    title = config.get("title", "Documentation")
    description = config.get("description", "")
    raw_theme = config.get("theme", "dark")
    # Theme can be a dict of colors (from cacao.yaml) — normalize to "dark"/"light"
    if isinstance(raw_theme, dict):
        # Guess from bg_color: light backgrounds → "light", else "dark"
        bg = raw_theme.get("bg_color", "#000")
        theme = "light" if _is_light_color(bg) else "dark"
    else:
        theme = raw_theme
    version = config.get("version", "")

    # Remove non-serializable items from config before embedding
    safe_config = {k: v for k, v in config.items() if k not in ("custom_doc_types",)}
    safe_data = {**json_data, "config": safe_config}
    data_json = json.dumps(safe_data, ensure_ascii=False, default=str)

    # Chat configuration
    chat_enabled = config.get("chat", False)
    chat_config = config.get("chat_config", {})
    chat_default_model = chat_config.get("default_model", "openai/gpt-4o-mini")
    chat_models = chat_config.get(
        "models",
        [
            "openai/gpt-4o-mini",
            "openai/gpt-4o",
            "claude/claude-sonnet-4-20250514",
            "groq/llama-3.1-8b-instant",
            "ollama/llama3.1:8b",
        ],
    )
    embedding_model = chat_config.get(
        "embedding_model", "openai/text-embedding-3-small"
    )
    top_k = chat_config.get("top_k", 5)
    chat_system_prompt = chat_config.get(
        "system_prompt",
        f"You are a helpful assistant that answers questions about the {title} library. "
        "Be concise and reference specific functions, classes, or modules when relevant.",
    )

    if chat_enabled:
        _chat_state_block = f"""# --- Chat State ---
_chat_api_key = c.signal("", name="chat_api_key")
_chat_model = c.signal({chat_default_model!r}, name="chat_model")
_chat_system_prompt = c.signal({chat_system_prompt!r}, name="chat_system_prompt")
_chat_messages = c.signal([], name="chat_messages")
_show_chat = c.signal(False, name="show_chat")

c.bind("update_chat_api_key", _chat_api_key)
c.bind("update_chat_model", _chat_model)
c.bind("update_chat_system_prompt", _chat_system_prompt)"""

        _chat_nav_item = ""

        _chat_panel_block = f"""
        # --- Chat (Floating Bubble + Modal) ---
        with c.modal(title="Ask about {title}", signal=_show_chat, size="lg"):
            c.input("API Key", signal=_chat_api_key, type="password",
                    placeholder="sk-... (optional for Ollama)",
                    on_change="update_chat_api_key")
            with c.row(gap=3):
                c.select("Model", options={chat_models!r},
                         signal=_chat_model, on_change="update_chat_model")
            c.spacer(2)
            c.chat(
                signal=_chat_messages,
                on_send="chat_send",
                on_clear="chat_clear",
                height="400px",
                show_clear=True,
                persist=True,
                placeholder="Ask about functions, classes, usage...",
            )
        c.html(\'\'\'<style>
.cacaodocs-fab {{
    position: fixed;
    bottom: 24px;
    right: 24px;
    width: 56px;
    height: 56px;
    border-radius: 50%;
    background: var(--c-primary, #6366f1);
    color: white;
    border: none;
    cursor: pointer;
    box-shadow: 0 4px 14px rgba(0,0,0,0.3);
    display: flex;
    align-items: center;
    justify-content: center;
    z-index: 999;
    transition: transform 0.2s, box-shadow 0.2s;
}}
.cacaodocs-fab:hover {{
    transform: scale(1.08);
    box-shadow: 0 6px 20px rgba(0,0,0,0.4);
}}
.cacaodocs-fab svg {{
    width: 24px;
    height: 24px;
    fill: none;
    stroke: currentColor;
    stroke-width: 2;
    stroke-linecap: round;
    stroke-linejoin: round;
}}
</style>
<button class="cacaodocs-fab" onclick="window.dispatchEvent(new CustomEvent(\'cacao:signal\', {{detail: {{name: \'show_chat\', value: true}}}}));" aria-label="Open chat">
    <svg viewBox="0 0 24 24"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/></svg>
</button>\'\'\')"""

        # Generate the static JavaScript for RAG + LLM chat
        _chat_static_script = (
            """
// --- CacaoDocs AI Chat (RAG + LLM) ---
(function() {
  const EMBEDDING_MODEL = """
            + json.dumps(embedding_model)
            + """;
  const TOP_K = """
            + str(top_k)
            + """;
  const SYSTEM_PROMPT = """
            + json.dumps(chat_system_prompt)
            + """;

  let _embeddings = null;
  let _embeddingsLoading = false;
  let _ollamaAvailable = null; // null = unknown, true/false after check

  // Check if Ollama is running locally
  async function checkOllama() {
    if (_ollamaAvailable !== null) return _ollamaAvailable;
    try {
      const resp = await fetch('http://localhost:11434/api/tags', {signal: AbortSignal.timeout(2000)});
      _ollamaAvailable = resp.ok;
    } catch {
      _ollamaAvailable = false;
    }
    return _ollamaAvailable;
  }

  // Load embeddings on demand
  async function loadEmbeddings() {
    if (_embeddings) return _embeddings;
    if (_embeddingsLoading) {
      while (_embeddingsLoading) await new Promise(r => setTimeout(r, 50));
      return _embeddings;
    }
    _embeddingsLoading = true;
    try {
      const base = window.__CACAO_BASE_PATH__ || '.';
      const resp = await fetch(base + '/embeddings.json');
      if (resp.ok) {
        _embeddings = await resp.json();
      }
    } catch (e) {
      console.warn('[CacaoDocs] Could not load embeddings:', e);
    }
    _embeddingsLoading = false;
    return _embeddings;
  }

  // --- Keyword search (always works, no API needed) ---
  function keywordSearch(query, chunks, topK) {
    const words = query.toLowerCase().split(/\\s+/).filter(w => w.length > 2);
    if (!words.length || !chunks.length) return [];

    const scored = chunks.map(chunk => {
      const text = chunk.text.toLowerCase();
      let score = 0;
      for (const w of words) {
        // Count occurrences, weight exact word matches higher
        const regex = new RegExp('\\\\b' + w.replace(/[.*+?^${}()|[\\]\\\\]/g, '\\\\$&'), 'gi');
        const matches = (text.match(regex) || []).length;
        score += matches * 2;
        // Partial matches
        if (text.includes(w)) score += 1;
      }
      // Boost if source/type matches a query word
      const src = (chunk.source || '').toLowerCase();
      for (const w of words) {
        if (src.includes(w)) score += 3;
      }
      return {score, text: chunk.text, source: chunk.source, type: chunk.type};
    });

    return scored.filter(s => s.score > 0).sort((a, b) => b.score - a.score).slice(0, topK);
  }

  // --- Vector search (needs embedding API) ---
  function cosineSim(a, b) {
    let dot = 0, na = 0, nb = 0;
    for (let i = 0; i < a.length; i++) {
      dot += a[i] * b[i];
      na += a[i] * a[i];
      nb += b[i] * b[i];
    }
    na = Math.sqrt(na);
    nb = Math.sqrt(nb);
    return (na && nb) ? dot / (na * nb) : 0;
  }

  async function embedQuery(text, apiKey) {
    const parts = EMBEDDING_MODEL.split('/');
    const provider = parts[0];
    const model = parts.slice(1).join('/');

    if (provider === 'ollama') {
      if (!await checkOllama()) return null;
      const resp = await fetch('http://localhost:11434/api/embed', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({model: model, input: [text]}),
      });
      const data = await resp.json();
      return data.embeddings?.[0] || null;
    } else if (provider === 'openai') {
      if (!apiKey) return null;
      const resp = await fetch('https://api.openai.com/v1/embeddings', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': 'Bearer ' + apiKey,
        },
        body: JSON.stringify({model: model, input: [text]}),
      });
      const data = await resp.json();
      return data.data?.[0]?.embedding || null;
    }
    return null;
  }

  // RAG search: try vector search, fall back to keyword search
  async function ragSearch(query, apiKey) {
    const emb = await loadEmbeddings();
    const chunks = emb?.chunks || [];
    if (!chunks.length) return [];

    // Try vector search first (if embeddings have vectors and API is reachable)
    if (chunks[0]?.embedding) {
      try {
        const queryVec = await embedQuery(query, apiKey);
        if (queryVec) {
          const scored = chunks.map(c => ({
            score: cosineSim(queryVec, c.embedding),
            text: c.text, source: c.source, type: c.type,
          }));
          scored.sort((a, b) => b.score - a.score);
          return scored.slice(0, TOP_K);
        }
      } catch (e) {
        console.warn('[CacaoDocs] Vector search failed, using keyword search:', e);
      }
    }

    // Fallback: keyword search (always works)
    return keywordSearch(query, chunks, TOP_K);
  }

  // Determine API endpoint and headers for a model
  function getProviderConfig(modelStr, apiKey) {
    const parts = modelStr.split('/');
    const provider = parts[0];
    const model = parts.slice(1).join('/');

    if (provider === 'ollama') {
      return {
        url: 'http://localhost:11434/api/chat',
        headers: {'Content-Type': 'application/json'},
        body: (msgs) => JSON.stringify({model: model, messages: msgs, stream: true}),
        parseStream: 'ollama',
      };
    } else if (provider === 'openai') {
      return {
        url: 'https://api.openai.com/v1/chat/completions',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': 'Bearer ' + (apiKey || ''),
        },
        body: (msgs) => JSON.stringify({model: model, messages: msgs, stream: true}),
        parseStream: 'openai',
      };
    } else if (provider === 'claude') {
      return {
        url: 'https://api.anthropic.com/v1/messages',
        headers: {
          'Content-Type': 'application/json',
          'x-api-key': apiKey || '',
          'anthropic-version': '2023-06-01',
          'anthropic-dangerous-direct-browser-access': 'true',
        },
        body: (msgs) => {
          const sysMsg = msgs.find(m => m.role === 'system');
          const chatMsgs = msgs.filter(m => m.role !== 'system');
          const payload = {model: model, messages: chatMsgs, max_tokens: 4096, stream: true};
          if (sysMsg) payload.system = sysMsg.content;
          return JSON.stringify(payload);
        },
        parseStream: 'claude',
      };
    } else if (provider === 'groq') {
      return {
        url: 'https://api.groq.com/openai/v1/chat/completions',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': 'Bearer ' + (apiKey || ''),
        },
        body: (msgs) => JSON.stringify({model: model, messages: msgs, stream: true}),
        parseStream: 'openai',
      };
    }
    // Fallback: assume OpenAI-compatible
    return {
      url: 'https://api.openai.com/v1/chat/completions',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + (apiKey || ''),
      },
      body: (msgs) => JSON.stringify({model: model, messages: msgs, stream: true}),
      parseStream: 'openai',
    };
  }

  // Stream LLM response
  async function streamChat(messages, modelStr, apiKey, signalName) {
    const ws = window.Cacao?.ws;
    const config = getProviderConfig(modelStr, apiKey);

    const resp = await fetch(config.url, {
      method: 'POST',
      headers: config.headers,
      body: config.body(messages),
    });

    if (!resp.ok) {
      const err = await resp.text();
      throw new Error(err || resp.statusText);
    }

    const reader = resp.body.getReader();
    const decoder = new TextDecoder();
    let fullText = '';
    let buffer = '';

    while (true) {
      const {done, value} = await reader.read();
      if (done) break;

      buffer += decoder.decode(value, {stream: true});
      const lines = buffer.split('\\n');
      buffer = lines.pop() || '';

      for (const line of lines) {
        const trimmed = line.trim();
        if (!trimmed || trimmed === 'data: [DONE]') continue;

        let delta = '';
        if (config.parseStream === 'ollama') {
          try {
            const obj = JSON.parse(trimmed);
            delta = obj.message?.content || '';
          } catch {}
        } else if (config.parseStream === 'openai') {
          if (trimmed.startsWith('data: ')) {
            try {
              const obj = JSON.parse(trimmed.slice(6));
              delta = obj.choices?.[0]?.delta?.content || '';
            } catch {}
          }
        } else if (config.parseStream === 'claude') {
          if (trimmed.startsWith('data: ')) {
            try {
              const obj = JSON.parse(trimmed.slice(6));
              if (obj.type === 'content_block_delta') {
                delta = obj.delta?.text || '';
              }
            } catch {}
          }
        }

        if (delta) {
          fullText += delta;
          if (ws) ws.dispatchChat({type: 'chat_delta', signal: signalName, delta: delta});
        }
      }
    }

    if (ws) ws.dispatchChat({type: 'chat_done', signal: signalName});
    return fullText;
  }

  // Expose for handlers
  window.__cacaoDocs = {
    ragSearch,
    streamChat,
    loadEmbeddings,
    checkOllama,
    SYSTEM_PROMPT,
  };
})();
"""
        )

        _chat_send_handler = """async function(signals, event) {
    const text = (event.text || '').trim();
    if (!text) return;

    const signalName = 'chat_messages';
    const msgs = signals.get(signalName) || [];
    signals.set(signalName, [...msgs, {role: 'user', content: text}]);

    const apiKey = signals.get('chat_api_key') || '';
    const model = signals.get('chat_model') || 'openai/gpt-4o-mini';
    const systemPrompt = signals.get('chat_system_prompt') || window.__cacaoDocs.SYSTEM_PROMPT;

    // Check if LLM is reachable
    const isOllamaModel = model.startsWith('ollama/');
    if (isOllamaModel) {
      const ollamaOk = await window.__cacaoDocs.checkOllama();
      if (!ollamaOk) {
        const updated = signals.get(signalName) || [];
        signals.set(signalName, [...updated, {role: 'error', content:
          'Ollama is not running locally. To use local AI:\\n\\n' +
          '1. Install Ollama: https://ollama.com/download\\n' +
          '2. Run: ollama pull ' + model.split('/')[1] + '\\n' +
          '3. Start Ollama and refresh this page\\n\\n' +
          'Or enter an API key and switch to a cloud model (OpenAI, Claude, Groq).'}]);
        return;
      }
    } else if (!apiKey) {
      const updated = signals.get(signalName) || [];
      signals.set(signalName, [...updated, {role: 'error', content:
        'Please enter an API key in Settings for ' + model + '.'}]);
      return;
    }

    try {
      // RAG: find relevant documentation
      let contextStr = '';
      try {
        const results = await window.__cacaoDocs.ragSearch(text, apiKey);
        if (results.length > 0) {
          contextStr = '\\n\\nRelevant documentation:\\n' +
            results.map(r => '[' + r.type + '] ' + r.source + ':\\n' + r.text).join('\\n---\\n');
        }
      } catch (e) {
        console.warn('[CacaoDocs] RAG search failed, continuing without context:', e);
      }

      // Build messages for LLM
      const llmMessages = [
        {role: 'system', content: systemPrompt + contextStr},
      ];
      // Add recent chat history (last 10 messages)
      const recent = (signals.get(signalName) || []).slice(-10);
      for (const m of recent) {
        if (m.role === 'user' || m.role === 'assistant') {
          llmMessages.push({role: m.role, content: m.content});
        }
      }

      const fullResponse = await window.__cacaoDocs.streamChat(
        llmMessages, model, apiKey, signalName
      );

      const updated = signals.get(signalName) || [];
      signals.set(signalName, [...updated, {role: 'assistant', content: fullResponse}]);

    } catch (e) {
      const updated = signals.get(signalName) || [];
      signals.set(signalName, [...updated, {role: 'error', content: String(e)}]);
      if (window.Cacao?.ws) {
        window.Cacao.ws.dispatchChat({type: 'chat_done', signal: signalName});
      }
    }
  }"""

        _chat_clear_handler = """function(signals, event) {
    signals.set('chat_messages', []);
    try { localStorage.removeItem('cacao-chat-chat_messages'); } catch {}
  }"""

        # Register static handlers and scripts in app code
        _chat_static_registration = f"""
# --- Static Chat Handlers (for GitHub Pages / static export) ---
c.static_script({_chat_static_script!r})
c.static_handler("chat_send", {_chat_send_handler!r})
c.static_handler("chat_clear", {_chat_clear_handler!r})"""
    else:
        _chat_state_block = ""
        _chat_nav_item = ""
        _chat_panel_block = ""
        _chat_static_registration = ""

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

{_chat_state_block}

{_chat_static_registration}

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
            c.nav_item("Types", key="types_ref", icon="box",
                        badge=str(len(_CLASSES)))

        # API Endpoints section
        if _API_ENDPOINTS:
            c.nav_item("API Reference", key="api_ref", icon="code",
                        badge=str(len(_API_ENDPOINTS)))

        c.nav_item("Call Map", key="callmap", icon="code")

        if _PAGES:
            with c.nav_group("Pages", icon="book"):
                for page in _PAGES:
                    c.nav_item(page["title"], key=f"page_{{page['slug']}}", icon="book")

{_chat_nav_item}

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

        # --- Types Reference Panel ---
        if _CLASSES:
            with c.nav_panel("types_ref"):
                with c.layout("sidebar", sidebar_width="260px") as _tl:
                    with _tl.side():
                        c.title("Types", level=3)
                        c.spacer(2)
                        # Group classes by module
                        _cls_by_mod = {{}}
                        for cls in _CLASSES:
                            mod = cls.get("module", "")
                            _cls_by_mod.setdefault(mod, []).append(cls)

                        with c.subnav(searchable=True):
                            for mod, classes in _cls_by_mod.items():
                                if mod:
                                    c.subnav_group(mod)
                                for cls in classes:
                                    method_count = len(cls.get("methods", []))
                                    c.subnav_item(
                                        cls["name"],
                                        badge=str(method_count),
                                        target=f'type_{{cls["full_path"]}}',
                                    )

                    with _tl.main():
                        c.title("Types Reference", level=2)
                        c.text(f"{{len(_CLASSES)}} classes across the codebase.", color="muted")
                        c.spacer(4)

                        for cls in _CLASSES:
                            c.raw_html(f'<div id="type_{{cls["full_path"]}}"></div>')
                            with c.card():
                                _render_class_detail(cls)
                            c.spacer(3)

        # --- API Reference Panel ---
        if _API_ENDPOINTS:
            with c.nav_panel("api_ref"):
                with c.layout("sidebar", sidebar_width="260px") as _al:
                    with _al.side():
                        c.title("Endpoints", level=3)
                        c.spacer(2)
                        # Group by path prefix (first path segment)
                        _ep_groups = {{}}
                        for ep in _API_ENDPOINTS:
                            ds = ep.get("docstring", {{}})
                            path = ds.get("path", "")
                            prefix = "/" + path.strip("/").split("/")[0] if path.strip("/") else "/"
                            _ep_groups.setdefault(prefix, []).append(ep)

                        _TAG_COLORS = {{"GET": "success", "POST": "info", "PUT": "warning", "PATCH": "warning", "DELETE": "danger"}}
                        with c.subnav(searchable=True):
                            for prefix, eps in _ep_groups.items():
                                c.subnav_group(prefix)
                                for ep in eps:
                                    ds = ep.get("docstring", {{}})
                                    method = ds.get("http_method", "GET")
                                    path = ds.get("path", ep["name"])
                                    c.subnav_item(
                                        path,
                                        tag=method,
                                        tag_color=_TAG_COLORS.get(method),
                                        target=f'ep_{{ep["full_path"]}}',
                                    )

                    with _al.main():
                        c.title("API Reference", level=2)
                        c.text(f"{{len(_API_ENDPOINTS)}} endpoints.", color="muted")
                        c.spacer(3)

                        # Summary table
                        _method_counts = {{}}
                        for ep in _API_ENDPOINTS:
                            m = ep.get("docstring", {{}}).get("http_method", "GET")
                            _method_counts[m] = _method_counts.get(m, 0) + 1
                        with c.row(gap=3, wrap=True):
                            for m, count in sorted(_method_counts.items()):
                                c.metric(m, count)
                        c.spacer(4)

                        for ep in _API_ENDPOINTS:
                            ds = ep.get("docstring", {{}})
                            method = ds.get("http_method", "")
                            path = ds.get("path", "")

                            c.raw_html(f'<div id="ep_{{ep["full_path"]}}"></div>')
                            with c.card():
                                # Header with method badge + path
                                with c.row(gap=3, wrap=True):
                                    if method:
                                        c.badge(method, color=_METHOD_COLORS.get(method, "default"))
                                    c.title(path or ep["name"], level=3)

                                if ep.get("module"):
                                    c.text(f'{{ep["module"]}}.{{ep["name"]}}', size="sm", color="muted")

                                c.spacer(2)
                                _render_docstring(ds)

                                # Source
                                if ep.get("source"):
                                    c.spacer(3)
                                    with c.tabs():
                                        with c.tab("src_" + ep["name"], "Source Code"):
                                            c.code(ep["source"], language="python")
                            c.spacer(3)

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

{_chat_panel_block}
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

    # Compare against previous build to detect changes + breaking changes
    data_path = output_dir / "data.json"
    if data_path.exists():
        try:
            with open(data_path, "r", encoding="utf-8") as f:
                old_data = json.load(f)
            changes = _compute_changes(old_data, json_data)
            if changes:
                json_data["changes"] = changes
            breaking = _detect_breaking_changes(old_data, json_data)
            if breaking:
                json_data["breaking_changes"] = breaking
        except (json.JSONDecodeError, KeyError):
            pass

    # Append to changelog
    changelog_path = output_dir / "changelog.json"
    changes_list = json_data.get("changes", [])
    breaking_list = json_data.get("breaking_changes", [])
    if changes_list or breaking_list:
        from datetime import datetime, timezone

        existing_changelog: list[dict[str, Any]] = []
        if changelog_path.exists():
            try:
                with open(changelog_path, "r", encoding="utf-8") as f:
                    existing_changelog = json.load(f)
            except (json.JSONDecodeError, ValueError):
                pass

        entry: dict[str, Any] = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "changes": changes_list,
        }
        if breaking_list:
            entry["breaking_changes"] = breaking_list

        existing_changelog.append(entry)

        with open(changelog_path, "w", encoding="utf-8") as f:
            json.dump(existing_changelog, f, indent=2, ensure_ascii=False, default=str)

    # Embedding step (if chat is enabled)
    chat_enabled = config.get("chat", False)
    if chat_enabled:
        chat_config = config.get("chat_config", {})
        embedding_model = chat_config.get(
            "embedding_model", "openai/text-embedding-3-small"
        )

        chunks = _chunk_documentation(json_data)
        if chunks:
            import logging

            logger = logging.getLogger("cacaodocs")
            logger.info(
                "Embedding %d documentation chunks with %s...",
                len(chunks),
                embedding_model,
            )

            embeddings = _embed_chunks(chunks, embedding_model)
            if embeddings:
                emb_path = output_dir / "embeddings.json"
                with open(emb_path, "w", encoding="utf-8") as f:
                    json.dump(embeddings, f, ensure_ascii=False)
                json_data["_embedding_stats"] = {
                    "chunks": len(chunks),
                    "model": embedding_model,
                    "dimensions": embeddings.get("dimensions", 0),
                }
            else:
                logger.warning(
                    "Embedding failed. Chat will work without RAG context. "
                    "Ensure %s is available (e.g. `ollama pull %s`).",
                    embedding_model,
                    embedding_model.split("/", 1)[-1]
                    if "/" in embedding_model
                    else embedding_model,
                )

    app_code = _generate_app_code(json_data)
    app_path = output_dir / "app.py"

    with open(app_path, "w", encoding="utf-8") as f:
        f.write(app_code)

    data_path = output_dir / "data.json"
    with open(data_path, "w", encoding="utf-8") as f:
        json.dump(json_data, f, indent=2, ensure_ascii=False, default=str)

    return json_data
