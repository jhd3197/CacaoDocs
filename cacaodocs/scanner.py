"""File discovery and AST parsing for Python source files."""
import ast
import fnmatch
import os
from pathlib import Path
from typing import Generator

from .parser import DocstringParser
from .types import (
    ClassDoc,
    FunctionDoc,
    MethodDoc,
    ModuleDoc,
    PageDoc,
    ParsedDocstring,
)


class Scanner:
    """Scans Python files and extracts documentation using AST.

    Args:
        exclude_patterns: Glob patterns to exclude from scanning.
    """

    def __init__(self, exclude_patterns: list[str] | None = None):
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
        self.parser = DocstringParser()

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
            # Filter out excluded directories
            dirs[:] = [
                d
                for d in dirs
                if not any(fnmatch.fnmatch(d, p) for p in self.exclude_patterns)
            ]

            for file in files:
                if file.endswith(".py"):
                    file_path = Path(root) / file
                    # Check file against exclude patterns
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
            # Filter out excluded directories
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
            # Return empty module doc for files with syntax errors
            return ModuleDoc(
                name=file_path.stem,
                full_path=self._get_module_path(file_path, base_path),
                file_path=str(file_path),
                docstring="",
                classes=[],
                functions=[],
            )

        # Get module docstring
        module_docstring = ast.get_docstring(tree) or ""

        # Calculate module path
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

        return ModuleDoc(
            name=file_path.stem,
            full_path=module_path,
            file_path=str(file_path),
            docstring=module_docstring,
            classes=classes,
            functions=functions,
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
            import markdown
        except ImportError:
            markdown = None

        with open(file_path, "r", encoding="utf-8", errors="replace") as f:
            content = f.read()

        # Extract title from first heading or filename
        title = file_path.stem.replace("_", " ").replace("-", " ").title()
        lines = content.split("\n")
        for line in lines:
            if line.startswith("# "):
                title = line[2:].strip()
                break

        # Calculate slug from relative path
        try:
            rel_path = file_path.relative_to(base_path)
            slug = str(rel_path.with_suffix("")).replace("\\", "/").replace(" ", "-").lower()
        except ValueError:
            slug = file_path.stem.replace(" ", "-").lower()

        # Convert markdown to HTML if available
        if markdown:
            html_content = markdown.markdown(
                content,
                extensions=["fenced_code", "tables", "codehilite", "toc"],
            )
        else:
            html_content = f"<pre>{content}</pre>"

        # Determine order from filename if it starts with a number
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

        # Convert path to module notation
        parts = list(rel_path.parts)

        # Remove .py extension from last part
        if parts[-1].endswith(".py"):
            parts[-1] = parts[-1][:-3]

        # Remove __init__ from path
        if parts[-1] == "__init__":
            parts = parts[:-1]

        return ".".join(parts) if parts else file_path.stem

    def _extract_class(self, node: ast.ClassDef, module: str, source: str) -> ClassDoc:
        """Extract documentation from a class definition."""
        docstring = ast.get_docstring(node) or ""
        parsed = self.parser.parse(docstring)

        # Get base classes
        bases = []
        for base in node.bases:
            bases.append(self._get_name(base))

        # Get decorators
        decorators = [self._get_decorator_name(d) for d in node.decorator_list]

        # Extract methods
        methods = []
        for item in node.body:
            if isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef)):
                method_doc = self._extract_method(item, module, source)
                methods.append(method_doc)

        # Get source code
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
        )

    def _extract_function(
        self, node: ast.FunctionDef | ast.AsyncFunctionDef, module: str, source: str
    ) -> FunctionDoc:
        """Extract documentation from a function definition."""
        docstring = ast.get_docstring(node) or ""
        parsed = self.parser.parse(docstring)

        # Get decorators
        decorators = [self._get_decorator_name(d) for d in node.decorator_list]

        # Build signature
        signature = self._build_signature(node)

        # Get source code
        func_source = ast.get_source_segment(source, node) or ""

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
        )

    def _extract_method(
        self, node: ast.FunctionDef | ast.AsyncFunctionDef, module: str, source: str
    ) -> MethodDoc:
        """Extract documentation from a method definition."""
        docstring = ast.get_docstring(node) or ""
        parsed = self.parser.parse(docstring)

        # Get decorators
        decorators = [self._get_decorator_name(d) for d in node.decorator_list]

        # Check for special method types
        is_classmethod = "classmethod" in decorators
        is_staticmethod = "staticmethod" in decorators
        is_property = "property" in decorators or any(
            ".setter" in d or ".getter" in d or ".deleter" in d for d in decorators
        )

        # Build signature
        signature = self._build_signature(node)

        # Get source code
        method_source = ast.get_source_segment(source, node) or ""

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
        )

    def _build_signature(self, node: ast.FunctionDef | ast.AsyncFunctionDef) -> str:
        """Build a function signature string."""
        args = node.args
        parts = []

        # Positional-only args (Python 3.8+)
        if hasattr(args, "posonlyargs"):
            for arg in args.posonlyargs:
                parts.append(self._format_arg(arg))
            if args.posonlyargs:
                parts.append("/")

        # Regular args
        num_defaults = len(args.defaults)
        num_args = len(args.args)
        for i, arg in enumerate(args.args):
            default_idx = i - (num_args - num_defaults)
            if default_idx >= 0:
                default = args.defaults[default_idx]
                parts.append(f"{self._format_arg(arg)}={self._get_default(default)}")
            else:
                parts.append(self._format_arg(arg))

        # *args
        if args.vararg:
            parts.append(f"*{self._format_arg(args.vararg)}")
        elif args.kwonlyargs:
            parts.append("*")

        # Keyword-only args
        num_kw_defaults = len(args.kw_defaults)
        for i, arg in enumerate(args.kwonlyargs):
            if args.kw_defaults[i] is not None:
                parts.append(
                    f"{self._format_arg(arg)}={self._get_default(args.kw_defaults[i])}"
                )
            else:
                parts.append(self._format_arg(arg))

        # **kwargs
        if args.kwarg:
            parts.append(f"**{self._format_arg(args.kwarg)}")

        # Return annotation
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
            # Union type with | syntax
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
    path: str | Path, exclude_patterns: list[str] | None = None
) -> tuple[list[ModuleDoc], list[PageDoc]]:
    """Scan a directory for Python and Markdown files.

    Args:
        path: Directory path to scan.
        exclude_patterns: Patterns to exclude.

    Returns:
        Tuple of (modules, pages) lists.
    """
    scanner = Scanner(exclude_patterns)
    base_path = Path(path)

    modules = []
    pages = []

    # Scan Python files
    for py_file in scanner.find_python_files(base_path):
        module_doc = scanner.scan_module(py_file, base_path)
        modules.append(module_doc)

    # Scan Markdown files
    for md_file in scanner.find_markdown_files(base_path):
        page_doc = scanner.scan_markdown(md_file, base_path)
        pages.append(page_doc)

    # Sort modules by path
    modules.sort(key=lambda m: m.full_path)

    # Sort pages by order then title
    pages.sort(key=lambda p: (p.order, p.title))

    return modules, pages
