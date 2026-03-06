"""File discovery and AST parsing for Python source files."""

import ast
import fnmatch
import hashlib
import os
import re
from pathlib import Path
from typing import Any, Generator

from .parser import DocstringParser
from .types import (
    ClassDoc,
    DocType,
    FunctionDoc,
    MethodDoc,
    ModuleDoc,
    PageDoc,
    TodoDoc,
)

# Decorator patterns that indicate an API endpoint
API_DECORATOR_PATTERNS = [
    # Flask
    re.compile(r"^(?:\w+\.)?route$"),
    # FastAPI / Starlette
    re.compile(r"^(?:\w+\.)?(?:get|post|put|delete|patch|options|head|trace)$"),
    # Django REST Framework
    re.compile(r"^api_view$"),
    # Generic
    re.compile(r"^(?:\w+\.)?endpoint$"),
]

# HTTP methods extractable from decorator names
HTTP_METHOD_FROM_DECORATOR = {
    "get": "GET",
    "post": "POST",
    "put": "PUT",
    "delete": "DELETE",
    "patch": "PATCH",
    "options": "OPTIONS",
    "head": "HEAD",
    "trace": "TRACE",
}


def _is_api_decorator(name: str) -> bool:
    """Check if a decorator name matches known API patterns."""
    return any(p.match(name) for p in API_DECORATOR_PATTERNS)


def _extract_http_method(decorators: list[str]) -> str:
    """Try to extract HTTP method from decorator names."""
    for dec in decorators:
        # FastAPI-style: app.get, router.post, etc.
        last_part = dec.rsplit(".", 1)[-1].lower()
        if last_part in HTTP_METHOD_FROM_DECORATOR:
            return HTTP_METHOD_FROM_DECORATOR[last_part]
    return ""


def _extract_route_path(node: ast.expr) -> str:
    """Try to extract the route path from a decorator call's arguments."""
    if isinstance(node, ast.Call) and node.args:
        first_arg = node.args[0]
        if isinstance(first_arg, ast.Constant) and isinstance(first_arg.value, str):
            return first_arg.value
    return ""


def _hash_signature(node: ast.FunctionDef | ast.AsyncFunctionDef) -> str:
    """Hash the function signature: name, args, defaults, return annotation, decorators."""
    parts = [node.name]
    parts.append(ast.dump(node.args))
    if node.returns:
        parts.append(ast.dump(node.returns))
    for d in node.decorator_list:
        parts.append(ast.dump(d))
    return hashlib.sha256("|".join(parts).encode()).hexdigest()[:16]


def _hash_body(node: ast.FunctionDef | ast.AsyncFunctionDef) -> str:
    """Hash the function body (excluding the docstring)."""
    body = list(node.body)
    # Skip the docstring node (first Expr with a Constant string)
    if (
        body
        and isinstance(body[0], ast.Expr)
        and isinstance(body[0].value, ast.Constant)
        and isinstance(body[0].value.value, str)
    ):
        body = body[1:]
    parts = [ast.dump(stmt) for stmt in body]
    return hashlib.sha256("\n".join(parts).encode()).hexdigest()[:16]


def _hash_class_signature(node: ast.ClassDef) -> str:
    """Hash the class signature: name, bases, decorators."""
    parts = [node.name]
    for base in node.bases:
        parts.append(ast.dump(base))
    for d in node.decorator_list:
        parts.append(ast.dump(d))
    return hashlib.sha256("|".join(parts).encode()).hexdigest()[:16]


def _cyclomatic_complexity(node: ast.AST) -> int:
    """Calculate cyclomatic complexity of an AST node.

    Starts at 1 and increments for each branch point.
    """
    complexity = 1
    for child in ast.walk(node):
        if isinstance(child, (ast.If, ast.While, ast.For, ast.AsyncFor)):
            complexity += 1
        elif isinstance(child, ast.ExceptHandler):
            complexity += 1
        elif isinstance(child, ast.With, ):
            complexity += 1
        elif isinstance(child, ast.Assert):
            complexity += 1
        elif isinstance(child, ast.BoolOp):
            # each `and`/`or` adds a branch
            complexity += len(child.values) - 1
        elif isinstance(child, ast.IfExp):
            complexity += 1
        elif isinstance(child, (ast.ListComp, ast.SetComp, ast.GeneratorExp, ast.DictComp)):
            complexity += sum(1 for _ in child.generators)
    return complexity


# Pattern for TODO/FIXME/HACK/XXX in comments
_TODO_PATTERN = re.compile(
    r"#\s*(TODO|FIXME|HACK|XXX)\b[:\s]*(.*)", re.IGNORECASE
)


def _extract_todos(source: str, file_path: str, module_path: str) -> list[TodoDoc]:
    """Extract TODO/FIXME/HACK/XXX comments from source code."""
    todos = []
    for i, line in enumerate(source.splitlines(), start=1):
        match = _TODO_PATTERN.search(line)
        if match:
            todos.append(TodoDoc(
                tag=match.group(1).upper(),
                text=match.group(2).strip(),
                file_path=file_path,
                line_number=i,
                module=module_path,
            ))
    return todos


def _ast_to_value(node: ast.expr) -> Any:
    """Recursively convert an AST node to a Python value.

    Supports constants, lists, dicts, and nested combinations.
    Returns None for unsupported node types.
    """
    if isinstance(node, ast.Constant):
        return node.value
    if isinstance(node, ast.Name):
        return {"True": True, "False": False, "None": None}.get(node.id)
    if isinstance(node, ast.List):
        return [_ast_to_value(el) for el in node.elts]
    if isinstance(node, ast.Tuple):
        return tuple(_ast_to_value(el) for el in node.elts)
    if isinstance(node, ast.Dict):
        return {
            _ast_to_value(k): _ast_to_value(v)
            for k, v in zip(node.keys, node.values)
            if k is not None
        }
    if isinstance(node, ast.UnaryOp) and isinstance(node.op, ast.USub):
        val = _ast_to_value(node.operand)
        if isinstance(val, (int, float)):
            return -val
    return None


def _extract_doc_decorator(node: ast.FunctionDef | ast.AsyncFunctionDef) -> dict[str, Any]:
    """Extract metadata from @doc(...) or @cacaodocs.doc(...) decorator.

    Returns a dict of keyword args found on the decorator (empty if not present).
    Supports nested dicts, lists, and constants.
    """
    for d in node.decorator_list:
        if not isinstance(d, ast.Call):
            continue
        func = d.func
        is_doc = False
        if isinstance(func, ast.Name) and func.id == "doc":
            is_doc = True
        elif isinstance(func, ast.Attribute) and func.attr == "doc":
            if isinstance(func.value, ast.Name) and func.value.id == "cacaodocs":
                is_doc = True

        if not is_doc:
            continue

        result: dict[str, Any] = {}
        for kw in d.keywords:
            if kw.arg is None:
                continue
            result[kw.arg] = _ast_to_value(kw.value)
        return result
    return {}


def _apply_doc_meta(parsed: "ParsedDocstring", meta: dict[str, Any]) -> None:
    """Overlay @doc() decorator metadata onto a ParsedDocstring.

    Decorator values override docstring-parsed values. Supports simplified
    syntax that gets converted to proper types.

    Simplified syntax examples:
        description="Fetch a user"
        args={"user_id": "The user ID"}
        args={"user_id": {"type": "int", "description": "ID", "default": "0"}}
        returns="User object"
        returns={"type": "User", "description": "The user object"}
        raises={"NotFoundError": "When user not found"}
        examples=["get_user(42)"]
        method="GET"
        path="/users/{user_id}"
        path_params={"user_id": "The user ID"}
        query_params={"page": {"type": "int", "description": "Page number", "default": "1"}}
        request_body={"name": {"type": "str", "description": "User name"}}
        responses={200: "Success", 404: {"description": "Not found", "fields": {...}}}
        headers={"Authorization": {"description": "Bearer token", "required": True}}
        trigger="user.created"
        payload={"user_id": {"type": "int", "description": "The user ID"}}
        config_fields={"DEBUG": {"type": "bool", "default": "false", "env": "APP_DEBUG"}}
    """
    from .types import (
        ArgDoc, ReturnDoc, RaiseDoc, ResponseDoc, HeaderDoc,
        PayloadFieldDoc, ConfigFieldDoc, DocType,
    )

    # --- Simple string fields ---
    if "description" in meta and meta["description"]:
        parsed.summary = str(meta["description"])
    if "method" in meta:
        parsed.http_method = str(meta["method"]).upper()
    if "path" in meta:
        parsed.path = str(meta["path"])
    if "trigger" in meta:
        parsed.trigger = str(meta["trigger"])
    if "doc_type" in meta:
        try:
            parsed.doc_type = DocType(meta["doc_type"])
        except ValueError:
            pass

    # --- Args: dict of name -> str | dict ---
    if "args" in meta and isinstance(meta["args"], dict):
        parsed.args = []
        for name, val in meta["args"].items():
            if isinstance(val, str):
                parsed.args.append(ArgDoc(name=str(name), type="", description=val))
            elif isinstance(val, dict):
                parsed.args.append(ArgDoc(
                    name=str(name),
                    type=val.get("type", ""),
                    description=val.get("description", ""),
                    default=val.get("default"),
                    required=val.get("required"),
                ))

    # --- Returns: str | dict ---
    if "returns" in meta:
        val = meta["returns"]
        if isinstance(val, str):
            parsed.returns = ReturnDoc(type="", description=val)
        elif isinstance(val, dict):
            parsed.returns = ReturnDoc(
                type=val.get("type", ""),
                description=val.get("description", ""),
            )

    # --- Raises: dict of type -> str ---
    if "raises" in meta and isinstance(meta["raises"], dict):
        parsed.raises = [
            RaiseDoc(type=str(k), description=str(v))
            for k, v in meta["raises"].items()
        ]

    # --- Examples: list of str ---
    if "examples" in meta and isinstance(meta["examples"], list):
        parsed.examples = [str(e) for e in meta["examples"]]

    # --- Notes: list of str ---
    if "notes" in meta and isinstance(meta["notes"], list):
        parsed.notes = [str(n) for n in meta["notes"]]

    # --- Attributes: dict (same format as args) ---
    if "attributes" in meta and isinstance(meta["attributes"], dict):
        parsed.attributes = []
        for name, val in meta["attributes"].items():
            if isinstance(val, str):
                parsed.attributes.append(ArgDoc(name=str(name), type="", description=val))
            elif isinstance(val, dict):
                parsed.attributes.append(ArgDoc(
                    name=str(name),
                    type=val.get("type", ""),
                    description=val.get("description", ""),
                    default=val.get("default"),
                    required=val.get("required"),
                ))

    # --- API: path_params, query_params, request_body (same format as args) ---
    for key in ("path_params", "query_params", "request_body"):
        if key in meta and isinstance(meta[key], dict):
            items = []
            for name, val in meta[key].items():
                if isinstance(val, str):
                    items.append(ArgDoc(name=str(name), type="", description=val))
                elif isinstance(val, dict):
                    items.append(ArgDoc(
                        name=str(name),
                        type=val.get("type", ""),
                        description=val.get("description", ""),
                        default=val.get("default"),
                        required=val.get("required"),
                    ))
            setattr(parsed, key, items)

    # --- Responses: dict of status_code -> str | dict ---
    if "responses" in meta and isinstance(meta["responses"], dict):
        parsed.responses = []
        for code, val in meta["responses"].items():
            if isinstance(val, str):
                parsed.responses.append(ResponseDoc(
                    status_code=int(code), description=val,
                ))
            elif isinstance(val, dict):
                fields = []
                for fname, fval in val.get("fields", {}).items():
                    if isinstance(fval, str):
                        fields.append(ArgDoc(name=str(fname), type="", description=fval))
                    elif isinstance(fval, dict):
                        fields.append(ArgDoc(
                            name=str(fname),
                            type=fval.get("type", ""),
                            description=fval.get("description", ""),
                        ))
                parsed.responses.append(ResponseDoc(
                    status_code=int(code),
                    description=val.get("description", ""),
                    fields=fields,
                ))

    # --- Headers: dict of name -> str | dict ---
    if "headers" in meta and isinstance(meta["headers"], dict):
        parsed.headers = []
        for name, val in meta["headers"].items():
            if isinstance(val, str):
                parsed.headers.append(HeaderDoc(name=str(name), description=val))
            elif isinstance(val, dict):
                parsed.headers.append(HeaderDoc(
                    name=str(name),
                    description=val.get("description", ""),
                    required=bool(val.get("required", False)),
                    example=val.get("example", ""),
                ))

    # --- Payload: dict of name -> dict (event type) ---
    if "payload" in meta and isinstance(meta["payload"], dict):
        parsed.payload = []
        for name, val in meta["payload"].items():
            if isinstance(val, str):
                parsed.payload.append(PayloadFieldDoc(
                    name=str(name), type="", description=val,
                ))
            elif isinstance(val, dict):
                parsed.payload.append(PayloadFieldDoc(
                    name=str(name),
                    type=val.get("type", ""),
                    description=val.get("description", ""),
                ))

    # --- Config fields: dict of name -> dict ---
    if "config_fields" in meta and isinstance(meta["config_fields"], dict):
        parsed.config_fields = []
        for name, val in meta["config_fields"].items():
            if isinstance(val, str):
                parsed.config_fields.append(ConfigFieldDoc(
                    name=str(name), type="", description=val,
                ))
            elif isinstance(val, dict):
                parsed.config_fields.append(ConfigFieldDoc(
                    name=str(name),
                    type=val.get("type", ""),
                    description=val.get("description", ""),
                    default=val.get("default"),
                    required=bool(val.get("required", False)),
                    env_var=val.get("env", ""),
                ))


def _detect_deprecation(
    node: ast.FunctionDef | ast.AsyncFunctionDef,
    docstring: str,
) -> tuple[bool, str, str]:
    """Detect deprecation from decorators or docstring.

    Checks for @deprecated, @deprecate, warnings.warn(DeprecationWarning),
    and 'Deprecated:' in the docstring.

    Returns (is_deprecated, message, since).
    """
    # Check decorators
    for d in node.decorator_list:
        name = ""
        if isinstance(d, ast.Name):
            name = d.id
        elif isinstance(d, ast.Attribute):
            name = d.attr
        elif isinstance(d, ast.Call):
            if isinstance(d.func, ast.Name):
                name = d.func.id
            elif isinstance(d.func, ast.Attribute):
                name = d.func.attr

        if name.lower() in ("deprecated", "deprecate"):
            msg = ""
            since = ""
            if isinstance(d, ast.Call):
                # Extract message from positional args
                if d.args:
                    first = d.args[0]
                    if isinstance(first, ast.Constant) and isinstance(first.value, str):
                        msg = first.value
                # Extract since= keyword arg
                for kw in d.keywords:
                    if kw.arg == "since" and isinstance(kw.value, ast.Constant):
                        since = str(kw.value.value)
            return True, msg, since

    # Check docstring for deprecation lines
    if docstring:
        import re
        for line in docstring.splitlines():
            stripped = line.strip()
            # ".. deprecated:: 2.0" (Sphinx style)
            sphinx = re.match(r'\.\.\s+deprecated::\s*(.+)', stripped, re.IGNORECASE)
            if sphinx:
                return True, "", sphinx.group(1).strip()
            # "Deprecated since 2.0: message" or "Deprecated since 2.0"
            since_match = re.match(r'deprecated\s+since\s+([^:]+?)(?::\s*(.*))?$', stripped, re.IGNORECASE)
            if since_match:
                since = since_match.group(1).strip()
                msg = (since_match.group(2) or "").strip()
                return True, msg, since
            # "Deprecated: message"
            if stripped.lower().startswith("deprecated:"):
                msg = stripped[len("deprecated:"):].strip()
                return True, msg, ""
            if stripped.lower() == "deprecated" or stripped.lower() == "deprecated.":
                return True, "", ""

    return False, "", ""


def _hash_class_body(node: ast.ClassDef) -> str:
    """Hash the class body (all statements)."""
    body = list(node.body)
    if (
        body
        and isinstance(body[0], ast.Expr)
        and isinstance(body[0].value, ast.Constant)
        and isinstance(body[0].value.value, str)
    ):
        body = body[1:]
    parts = [ast.dump(stmt) for stmt in body]
    return hashlib.sha256("\n".join(parts).encode()).hexdigest()[:16]


class Scanner:
    """Scans Python files and extracts documentation using AST.

    Args:
        exclude_patterns: Glob patterns to exclude from scanning.
        parser: Optional pre-configured DocstringParser.
    """

    def __init__(
        self,
        exclude_patterns: list[str] | None = None,
        parser: DocstringParser | None = None,
    ):
        self.exclude_patterns = exclude_patterns or [
            "__pycache__",
            ".venv",
            "venv",
            ".git",
            "node_modules",
            "*.pyc",
            "build",
            "dist",
        ]
        self.parser = parser or DocstringParser()

    def find_python_files(self, path: str | Path) -> Generator[Path, None, None]:
        """Find all Python files in a directory.

        Args:
            path: Directory path to search.

        Yields:
            Path objects for each Python file found.
        """
        path = Path(path)

        if path.is_file():
            if path.suffix == ".py":
                yield path
            return

        for root, dirs, files in os.walk(path):
            dirs[:] = [
                d
                for d in dirs
                if not any(fnmatch.fnmatch(d, p) for p in self.exclude_patterns)
            ]

            for file in files:
                if file.endswith(".py"):
                    file_path = Path(root) / file
                    rel_path = str(file_path.relative_to(path))
                    if not any(
                        fnmatch.fnmatch(rel_path, p) or fnmatch.fnmatch(file, p)
                        for p in self.exclude_patterns
                    ):
                        yield file_path

    def find_markdown_files(self, path: str | Path) -> Generator[Path, None, None]:
        """Find all Markdown files in a directory.

        Args:
            path: Directory path to search.

        Yields:
            Path objects for each Markdown file found.
        """
        path = Path(path)

        if path.is_file():
            if path.suffix in (".md", ".markdown"):
                yield path
            return

        for root, dirs, files in os.walk(path):
            dirs[:] = [
                d
                for d in dirs
                if not any(fnmatch.fnmatch(d, p) for p in self.exclude_patterns)
            ]

            for file in files:
                if file.endswith((".md", ".markdown")):
                    file_path = Path(root) / file
                    rel_path = str(file_path.relative_to(path))
                    if not any(
                        fnmatch.fnmatch(rel_path, p) or fnmatch.fnmatch(file, p)
                        for p in self.exclude_patterns
                    ):
                        yield file_path

    def scan_module(self, file_path: Path, base_path: Path) -> ModuleDoc:
        """Scan a Python module and extract documentation.

        Args:
            file_path: Path to the Python file.
            base_path: Base path for calculating module name.

        Returns:
            ModuleDoc with extracted documentation.
        """
        with open(file_path, "r", encoding="utf-8", errors="replace") as f:
            source = f.read()

        try:
            tree = ast.parse(source, filename=str(file_path))
        except SyntaxError:
            return ModuleDoc(
                name=file_path.stem,
                full_path=self._get_module_path(file_path, base_path),
                file_path=str(file_path),
                docstring="",
                classes=[],
                functions=[],
            )

        module_docstring = ast.get_docstring(tree) or ""
        module_path = self._get_module_path(file_path, base_path)

        classes = []
        functions = []

        for node in ast.iter_child_nodes(tree):
            if isinstance(node, ast.ClassDef):
                class_doc = self._extract_class(node, module_path, source)
                classes.append(class_doc)
            elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                func_doc = self._extract_function(node, module_path, source)
                functions.append(func_doc)

        todos = _extract_todos(source, str(file_path), module_path)

        return ModuleDoc(
            name=file_path.stem,
            full_path=module_path,
            file_path=str(file_path),
            docstring=module_docstring,
            classes=classes,
            functions=functions,
            todos=todos,
        )

    def scan_markdown(self, file_path: Path, base_path: Path) -> PageDoc:
        """Scan a Markdown file and extract content.

        Args:
            file_path: Path to the Markdown file.
            base_path: Base path for calculating slug.

        Returns:
            PageDoc with extracted content.
        """
        try:
            import markdown  # type: ignore[import-untyped]
        except ImportError:
            markdown = None

        with open(file_path, "r", encoding="utf-8", errors="replace") as f:
            content = f.read()

        title = file_path.stem.replace("_", " ").replace("-", " ").title()
        lines = content.split("\n")
        for line in lines:
            if line.startswith("# "):
                title = line[2:].strip()
                break

        try:
            rel_path = file_path.relative_to(base_path)
            slug = (
                str(rel_path.with_suffix(""))
                .replace("\\", "/")
                .replace(" ", "-")
                .lower()
            )
        except ValueError:
            slug = file_path.stem.replace(" ", "-").lower()

        if markdown:
            html_content = markdown.markdown(
                content,
                extensions=["fenced_code", "tables", "codehilite", "toc"],
            )
        else:
            html_content = f"<pre>{content}</pre>"

        order = 0
        if file_path.stem[0].isdigit():
            try:
                order = int("".join(c for c in file_path.stem if c.isdigit()))
            except ValueError:
                pass

        return PageDoc(
            title=title,
            slug=slug,
            content=html_content,
            file_path=str(file_path),
            order=order,
        )

    def _get_module_path(self, file_path: Path, base_path: Path) -> str:
        """Calculate the module path (e.g., 'cacao.server.signal')."""
        try:
            rel_path = file_path.relative_to(base_path)
        except ValueError:
            return file_path.stem

        parts = list(rel_path.parts)
        if parts[-1].endswith(".py"):
            parts[-1] = parts[-1][:-3]
        if parts[-1] == "__init__":
            parts = parts[:-1]

        return ".".join(parts) if parts else file_path.stem

    def _detect_doc_type(
        self, node: ast.FunctionDef | ast.AsyncFunctionDef
    ) -> tuple[DocType, str, str]:
        """Auto-detect doc type from decorators.

        Returns:
            Tuple of (doc_type, http_method, route_path).
        """
        decorators = []
        for d in node.decorator_list:
            dec_name = self._get_decorator_name(d)
            decorators.append(dec_name)
            if _is_api_decorator(dec_name):
                method = _extract_http_method(decorators)
                path = _extract_route_path(d)
                return DocType.API, method, path

        return DocType.FUNCTION, "", ""

    def _extract_class(self, node: ast.ClassDef, module: str, source: str) -> ClassDoc:
        """Extract documentation from a class definition."""
        docstring = ast.get_docstring(node) or ""
        parsed = self.parser.parse(docstring, hint_type=DocType.CLASS)

        bases = [self._get_name(base) for base in node.bases]
        decorators = [self._get_decorator_name(d) for d in node.decorator_list]

        methods = []
        for item in node.body:
            if isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef)):
                method_doc = self._extract_method(item, module, source)
                methods.append(method_doc)

        class_source = ast.get_source_segment(source, node) or ""

        return ClassDoc(
            name=node.name,
            module=module,
            full_path=f"{module}.{node.name}",
            docstring=parsed,
            bases=bases,
            methods=methods,
            source=class_source,
            line_number=node.lineno,
            decorators=decorators,
            signature_hash=_hash_class_signature(node),
            body_hash=_hash_class_body(node),
        )

    def _extract_function(
        self, node: ast.FunctionDef | ast.AsyncFunctionDef, module: str, source: str
    ) -> FunctionDoc:
        """Extract documentation from a function definition."""
        docstring = ast.get_docstring(node) or ""
        decorators = [self._get_decorator_name(d) for d in node.decorator_list]

        # Extract @doc(...) decorator metadata
        doc_meta = _extract_doc_decorator(node)

        # Auto-detect doc type from decorators (decorator override wins)
        detected_type, http_method, route_path = self._detect_doc_type(node)
        if doc_meta.get("doc_type"):
            try:
                detected_type = DocType(doc_meta["doc_type"])
            except ValueError:
                pass
        parsed = self.parser.parse(docstring, hint_type=detected_type)

        # Fill in method/path from decorator if not in docstring
        if detected_type == DocType.API:
            if not parsed.http_method and http_method:
                parsed.http_method = http_method
            if not parsed.path and route_path:
                parsed.path = route_path

        # Overlay @doc() metadata onto parsed docstring (decorator wins)
        if doc_meta:
            _apply_doc_meta(parsed, doc_meta)

        signature = self._build_signature(node)
        func_source = ast.get_source_segment(source, node) or ""
        calls = self._extract_calls(node)
        is_deprecated, dep_msg, dep_since = _detect_deprecation(node, docstring)

        # @doc(deprecated=...) overrides docstring/decorator detection
        if "deprecated" in doc_meta:
            dep_val = doc_meta["deprecated"]
            if isinstance(dep_val, str) and dep_val:
                is_deprecated, dep_since = True, dep_val
            else:
                is_deprecated = bool(dep_val)

        return FunctionDoc(
            name=node.name,
            module=module,
            full_path=f"{module}.{node.name}",
            signature=signature,
            docstring=parsed,
            is_async=isinstance(node, ast.AsyncFunctionDef),
            source=func_source,
            line_number=node.lineno,
            decorators=decorators,
            calls=calls,
            doc_type=parsed.doc_type,
            signature_hash=_hash_signature(node),
            body_hash=_hash_body(node),
            complexity=_cyclomatic_complexity(node),
            is_deprecated=is_deprecated,
            deprecation_message=dep_msg,
            deprecation_since=dep_since,
            category=str(doc_meta.get("category", "")),
            version=str(doc_meta.get("version", "")),
            hidden=bool(doc_meta.get("hidden", False)),
        )

    def _extract_method(
        self, node: ast.FunctionDef | ast.AsyncFunctionDef, module: str, source: str
    ) -> MethodDoc:
        """Extract documentation from a method definition."""
        docstring = ast.get_docstring(node) or ""
        decorators = [self._get_decorator_name(d) for d in node.decorator_list]

        # Extract @doc(...) decorator metadata
        doc_meta = _extract_doc_decorator(node)

        # Auto-detect doc type (decorator override wins)
        detected_type, http_method, route_path = self._detect_doc_type(node)
        if doc_meta.get("doc_type"):
            try:
                detected_type = DocType(doc_meta["doc_type"])
            except ValueError:
                pass
        parsed = self.parser.parse(docstring, hint_type=detected_type)

        if detected_type == DocType.API:
            if not parsed.http_method and http_method:
                parsed.http_method = http_method
            if not parsed.path and route_path:
                parsed.path = route_path

        # Overlay @doc() metadata onto parsed docstring (decorator wins)
        if doc_meta:
            _apply_doc_meta(parsed, doc_meta)

        is_classmethod = "classmethod" in decorators
        is_staticmethod = "staticmethod" in decorators
        is_property = "property" in decorators or any(
            ".setter" in d or ".getter" in d or ".deleter" in d for d in decorators
        )

        signature = self._build_signature(node)
        method_source = ast.get_source_segment(source, node) or ""
        calls = self._extract_calls(node)
        is_deprecated, dep_msg, dep_since = _detect_deprecation(node, docstring)

        # @doc(deprecated=...) overrides docstring/decorator detection
        if "deprecated" in doc_meta:
            dep_val = doc_meta["deprecated"]
            if isinstance(dep_val, str) and dep_val:
                is_deprecated, dep_since = True, dep_val
            else:
                is_deprecated = bool(dep_val)

        return MethodDoc(
            name=node.name,
            module=module,
            signature=signature,
            docstring=parsed,
            is_async=isinstance(node, ast.AsyncFunctionDef),
            is_classmethod=is_classmethod,
            is_staticmethod=is_staticmethod,
            is_property=is_property,
            source=method_source,
            line_number=node.lineno,
            decorators=decorators,
            calls=calls,
            doc_type=parsed.doc_type,
            signature_hash=_hash_signature(node),
            body_hash=_hash_body(node),
            complexity=_cyclomatic_complexity(node),
            is_deprecated=is_deprecated,
            deprecation_message=dep_msg,
            deprecation_since=dep_since,
            category=str(doc_meta.get("category", "")),
            version=str(doc_meta.get("version", "")),
            hidden=bool(doc_meta.get("hidden", False)),
        )

    def _extract_calls(self, node: ast.FunctionDef | ast.AsyncFunctionDef) -> list[str]:
        """Extract function/method calls from a function body."""
        calls = []
        seen = set()

        for child in ast.walk(node):
            if isinstance(child, ast.Call):
                name = self._get_call_name(child.func)
                if name and name not in seen:
                    seen.add(name)
                    calls.append(name)

        return sorted(calls)

    def _get_call_name(self, node: ast.expr) -> str | None:
        """Get the name of a function being called."""
        if isinstance(node, ast.Name):
            return node.id
        elif isinstance(node, ast.Attribute):
            value = self._get_call_name(node.value)
            if value:
                return f"{value}.{node.attr}"
            return node.attr
        elif isinstance(node, ast.Subscript):
            return self._get_call_name(node.value)
        return None

    def _build_signature(self, node: ast.FunctionDef | ast.AsyncFunctionDef) -> str:
        """Build a function signature string."""
        args = node.args
        parts = []

        if hasattr(args, "posonlyargs"):
            for arg in args.posonlyargs:
                parts.append(self._format_arg(arg))
            if args.posonlyargs:
                parts.append("/")

        num_defaults = len(args.defaults)
        num_args = len(args.args)
        for i, arg in enumerate(args.args):
            default_idx = i - (num_args - num_defaults)
            if default_idx >= 0:
                default = args.defaults[default_idx]
                parts.append(f"{self._format_arg(arg)}={self._get_default(default)}")
            else:
                parts.append(self._format_arg(arg))

        if args.vararg:
            parts.append(f"*{self._format_arg(args.vararg)}")
        elif args.kwonlyargs:
            parts.append("*")

        len(args.kw_defaults)
        for i, arg in enumerate(args.kwonlyargs):
            if args.kw_defaults[i] is not None:
                parts.append(
                    f"{self._format_arg(arg)}={self._get_default(args.kw_defaults[i])}"  # type: ignore[arg-type]
                )
            else:
                parts.append(self._format_arg(arg))

        if args.kwarg:
            parts.append(f"**{self._format_arg(args.kwarg)}")

        signature = f"({', '.join(parts)})"
        if node.returns:
            signature += f" -> {self._get_annotation(node.returns)}"

        return signature

    def _format_arg(self, arg: ast.arg) -> str:
        """Format a function argument with optional type annotation."""
        if arg.annotation:
            return f"{arg.arg}: {self._get_annotation(arg.annotation)}"
        return arg.arg

    def _get_annotation(self, node: ast.expr) -> str:
        """Get string representation of a type annotation."""
        if isinstance(node, ast.Constant):
            return repr(node.value)
        elif isinstance(node, ast.Name):
            return node.id
        elif isinstance(node, ast.Attribute):
            return f"{self._get_annotation(node.value)}.{node.attr}"
        elif isinstance(node, ast.Subscript):
            value = self._get_annotation(node.value)
            slice_val = self._get_annotation(node.slice)
            return f"{value}[{slice_val}]"
        elif isinstance(node, ast.Tuple):
            elts = ", ".join(self._get_annotation(e) for e in node.elts)
            return elts
        elif isinstance(node, ast.List):
            elts = ", ".join(self._get_annotation(e) for e in node.elts)
            return f"[{elts}]"
        elif isinstance(node, ast.BinOp) and isinstance(node.op, ast.BitOr):
            left = self._get_annotation(node.left)
            right = self._get_annotation(node.right)
            return f"{left} | {right}"
        else:
            return ast.unparse(node) if hasattr(ast, "unparse") else "..."

    def _get_default(self, node: ast.expr) -> str:
        """Get string representation of a default value."""
        if isinstance(node, ast.Constant):
            return repr(node.value)
        elif isinstance(node, ast.Name):
            return node.id
        elif isinstance(node, (ast.List, ast.Tuple, ast.Dict)):
            return ast.unparse(node) if hasattr(ast, "unparse") else "..."
        else:
            return ast.unparse(node) if hasattr(ast, "unparse") else "..."

    def _get_name(self, node: ast.expr) -> str:
        """Get name from an AST node."""
        if isinstance(node, ast.Name):
            return node.id
        elif isinstance(node, ast.Attribute):
            return f"{self._get_name(node.value)}.{node.attr}"
        elif isinstance(node, ast.Subscript):
            return f"{self._get_name(node.value)}[...]"
        else:
            return ast.unparse(node) if hasattr(ast, "unparse") else "..."

    def _get_decorator_name(self, node: ast.expr) -> str:
        """Get name of a decorator."""
        if isinstance(node, ast.Name):
            return node.id
        elif isinstance(node, ast.Attribute):
            return f"{self._get_name(node.value)}.{node.attr}"
        elif isinstance(node, ast.Call):
            return self._get_decorator_name(node.func)
        else:
            return ast.unparse(node) if hasattr(ast, "unparse") else "..."


def scan_directory(
    path: str | Path,
    exclude_patterns: list[str] | None = None,
    parser: DocstringParser | None = None,
) -> tuple[list[ModuleDoc], list[PageDoc]]:
    """Scan a directory for Python and Markdown files.

    Args:
        path: Directory path to scan.
        exclude_patterns: Patterns to exclude.
        parser: Optional pre-configured DocstringParser.

    Returns:
        Tuple of (modules, pages) lists.
    """
    scanner = Scanner(exclude_patterns, parser)
    base_path = Path(path)

    modules = []
    pages = []

    for py_file in scanner.find_python_files(base_path):
        module_doc = scanner.scan_module(py_file, base_path)
        modules.append(module_doc)

    for md_file in scanner.find_markdown_files(base_path):
        page_doc = scanner.scan_markdown(md_file, base_path)
        pages.append(page_doc)

    modules.sort(key=lambda m: m.full_path)
    pages.sort(key=lambda p: (p.order, p.title))

    return modules, pages
