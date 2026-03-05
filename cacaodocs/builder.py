"""Build documentation output from scanned modules."""
import json
import os
import shutil
from dataclasses import asdict
from pathlib import Path
from typing import Any

from .types import (
    ClassDoc,
    DocumentationData,
    FunctionDoc,
    MethodDoc,
    ModuleDoc,
    PageDoc,
    ParsedDocstring,
)


def _serialize_docstring(docstring: ParsedDocstring) -> dict[str, Any]:
    """Serialize a ParsedDocstring to a JSON-compatible dict."""
    return {
        "summary": docstring.summary,
        "description": docstring.description,
        "args": [
            {
                "name": arg.name,
                "type": arg.type,
                "description": arg.description,
                "default": arg.default,
            }
            for arg in docstring.args
        ],
        "returns": (
            {"type": docstring.returns.type, "description": docstring.returns.description}
            if docstring.returns
            else None
        ),
        "raises": [
            {"type": r.type, "description": r.description} for r in docstring.raises
        ],
        "examples": docstring.examples,
        "attributes": [
            {
                "name": attr.name,
                "type": attr.type,
                "description": attr.description,
                "default": attr.default,
            }
            for attr in docstring.attributes
        ],
        "notes": docstring.notes,
    }


def _serialize_method(method: MethodDoc) -> dict[str, Any]:
    """Serialize a MethodDoc to a JSON-compatible dict."""
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
    }


def _serialize_function(func: FunctionDoc) -> dict[str, Any]:
    """Serialize a FunctionDoc to a JSON-compatible dict."""
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
    }


def _serialize_class(cls: ClassDoc) -> dict[str, Any]:
    """Serialize a ClassDoc to a JSON-compatible dict."""
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
    }


def _serialize_module(module: ModuleDoc) -> dict[str, Any]:
    """Serialize a ModuleDoc to a JSON-compatible dict."""
    return {
        "name": module.name,
        "full_path": module.full_path,
        "file_path": module.file_path,
        "docstring": module.docstring,
        "classes": [_serialize_class(c) for c in module.classes],
        "functions": [_serialize_function(f) for f in module.functions],
    }


def _serialize_page(page: PageDoc) -> dict[str, Any]:
    """Serialize a PageDoc to a JSON-compatible dict."""
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
    """Build JSON documentation structure.

    Args:
        modules: List of parsed module documentation.
        pages: List of parsed markdown pages.
        config: Configuration dictionary.

    Returns:
        Complete documentation data as a dictionary.
    """
    # Flatten classes and functions for easier frontend access
    all_classes = []
    all_functions = []

    for module in modules:
        for cls in module.classes:
            all_classes.append(_serialize_class(cls))
        for func in module.functions:
            all_functions.append(_serialize_function(func))

    return {
        "modules": [_serialize_module(m) for m in modules],
        "classes": all_classes,
        "functions": all_functions,
        "pages": [_serialize_page(p) for p in pages],
        "config": config,
    }


def build_html(json_data: dict[str, Any], output_dir: str | Path) -> None:
    """Build HTML documentation from JSON data.

    Args:
        json_data: Documentation data from build_json.
        output_dir: Output directory for HTML files.
    """
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    # Find the frontend build directory
    frontend_build = Path(__file__).parent / "frontend" / "build"

    if not frontend_build.exists():
        raise FileNotFoundError(
            f"Frontend build not found at {frontend_build}. "
            "Run 'npm run build' in cacaodocs/frontend first."
        )

    # Copy all static files from frontend build
    for item in frontend_build.iterdir():
        dest = output_dir / item.name
        if item.is_dir():
            if dest.exists():
                shutil.rmtree(dest)
            shutil.copytree(item, dest)
        else:
            shutil.copy2(item, dest)

    # Write data.js with the JSON data
    data_js_content = f"window.globalData = {json.dumps(json_data, indent=2)};"
    data_js_path = output_dir / "data.js"
    with open(data_js_path, "w", encoding="utf-8") as f:
        f.write(data_js_content)

    # Also update configs key for backwards compatibility
    if "config" in json_data:
        json_data["configs"] = json_data["config"]

    # Write the final data.js
    data_js_content = f"window.globalData = {json.dumps(json_data, indent=2)};"
    with open(data_js_path, "w", encoding="utf-8") as f:
        f.write(data_js_content)


def build_docs(
    source: str | Path,
    output: str | Path,
    config: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Build complete documentation from source directory.

    Args:
        source: Source directory containing Python/Markdown files.
        output: Output directory for generated documentation.
        config: Optional configuration dictionary.

    Returns:
        The generated JSON documentation data.
    """
    from .scanner import scan_directory
    from .config import load_config

    # Load config
    if config is None:
        config = load_config()

    # Scan source files
    exclude_patterns = config.get("exclude_patterns", [])
    modules, pages = scan_directory(source, exclude_patterns)

    # Build JSON
    json_data = build_json(modules, pages, config)

    # Build HTML output
    build_html(json_data, output)

    return json_data
