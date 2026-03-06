"""Tests for cacaodocs.scanner file discovery and AST extraction."""

import textwrap
from pathlib import Path

import pytest

from cacaodocs.scanner import (
    Scanner,
    _extract_http_method,
    _is_api_decorator,
    scan_directory,
)
from cacaodocs.types import DocType


class TestIsAPIDecorator:
    def test_flask_route(self):
        assert _is_api_decorator("app.route") is True
        assert _is_api_decorator("blueprint.route") is True

    def test_fastapi_methods(self):
        assert _is_api_decorator("app.get") is True
        assert _is_api_decorator("app.post") is True
        assert _is_api_decorator("router.delete") is True

    def test_django_api_view(self):
        assert _is_api_decorator("api_view") is True

    def test_non_api_decorator(self):
        assert _is_api_decorator("staticmethod") is False
        assert _is_api_decorator("property") is False


class TestExtractHttpMethod:
    def test_fastapi_style(self):
        assert _extract_http_method(["app.get"]) == "GET"
        assert _extract_http_method(["router.post"]) == "POST"
        assert _extract_http_method(["app.delete"]) == "DELETE"

    def test_no_method(self):
        assert _extract_http_method(["app.route"]) == ""
        assert _extract_http_method(["staticmethod"]) == ""


class TestScannerFileDiscovery:
    def test_find_python_files(self, tmp_path):
        (tmp_path / "main.py").write_text("# main")
        (tmp_path / "utils.py").write_text("# utils")
        (tmp_path / "readme.md").write_text("# readme")
        (tmp_path / "__pycache__").mkdir()
        (tmp_path / "__pycache__" / "cached.py").write_text("# cached")

        scanner = Scanner()
        files = list(scanner.find_python_files(tmp_path))
        names = [f.name for f in files]
        assert "main.py" in names
        assert "utils.py" in names
        assert "cached.py" not in names
        assert "readme.md" not in [f.name for f in files]

    def test_find_single_file(self, tmp_path):
        py_file = tmp_path / "single.py"
        py_file.write_text("# single")
        scanner = Scanner()
        files = list(scanner.find_python_files(py_file))
        assert len(files) == 1

    def test_find_markdown_files(self, tmp_path):
        (tmp_path / "guide.md").write_text("# Guide")
        (tmp_path / "notes.markdown").write_text("# Notes")
        (tmp_path / "code.py").write_text("# code")

        scanner = Scanner()
        files = list(scanner.find_markdown_files(tmp_path))
        names = [f.name for f in files]
        assert "guide.md" in names
        assert "notes.markdown" in names
        assert "code.py" not in names

    def test_exclude_patterns(self, tmp_path):
        (tmp_path / "good.py").write_text("# good")
        venv = tmp_path / ".venv"
        venv.mkdir()
        (venv / "bad.py").write_text("# bad")

        scanner = Scanner(exclude_patterns=[".venv"])
        files = list(scanner.find_python_files(tmp_path))
        names = [f.name for f in files]
        assert "good.py" in names
        assert "bad.py" not in names


class TestScanModule:
    def test_scan_simple_function(self, tmp_path):
        code = textwrap.dedent('''\
            def greet(name: str) -> str:
                """Say hello.

                Args:
                    name (str): The name.

                Returns:
                    str: Greeting message.
                """
                return f"Hello, {name}"
        ''')
        py_file = tmp_path / "hello.py"
        py_file.write_text(code)

        scanner = Scanner()
        module = scanner.scan_module(py_file, tmp_path)
        assert module.name == "hello"
        assert len(module.functions) == 1
        func = module.functions[0]
        assert func.name == "greet"
        assert func.docstring.summary == "Say hello."
        assert len(func.docstring.args) == 1
        assert func.docstring.returns is not None
        assert func.is_async is False

    def test_scan_async_function(self, tmp_path):
        code = textwrap.dedent('''\
            async def fetch(url: str) -> dict:
                """Fetch data from URL."""
                pass
        ''')
        py_file = tmp_path / "fetcher.py"
        py_file.write_text(code)

        scanner = Scanner()
        module = scanner.scan_module(py_file, tmp_path)
        assert module.functions[0].is_async is True

    def test_scan_class(self, tmp_path):
        code = textwrap.dedent('''\
            class User:
                """A user model.

                Attributes:
                    name (str): The name.
                """

                def __init__(self, name: str):
                    """Initialize user."""
                    self.name = name

                def greet(self) -> str:
                    """Say hi."""
                    return f"Hi, {self.name}"
        ''')
        py_file = tmp_path / "models.py"
        py_file.write_text(code)

        scanner = Scanner()
        module = scanner.scan_module(py_file, tmp_path)
        assert len(module.classes) == 1
        cls = module.classes[0]
        assert cls.name == "User"
        assert len(cls.methods) == 2

    def test_scan_api_decorator_detection(self, tmp_path):
        code = textwrap.dedent('''\
            from fastapi import FastAPI
            app = FastAPI()

            @app.get("/users/{user_id}")
            def get_user(user_id: int):
                """Get a user by ID."""
                pass
        ''')
        py_file = tmp_path / "routes.py"
        py_file.write_text(code)

        scanner = Scanner()
        module = scanner.scan_module(py_file, tmp_path)
        func = module.functions[0]
        assert func.doc_type == DocType.API
        assert func.docstring.http_method == "GET"
        assert func.docstring.path == "/users/{user_id}"

    def test_scan_syntax_error(self, tmp_path):
        py_file = tmp_path / "broken.py"
        py_file.write_text("def broken(:\n    pass")

        scanner = Scanner()
        module = scanner.scan_module(py_file, tmp_path)
        assert module.name == "broken"
        assert module.classes == []
        assert module.functions == []

    def test_module_path_calculation(self, tmp_path):
        pkg = tmp_path / "mypackage"
        pkg.mkdir()
        (pkg / "__init__.py").write_text("")
        (pkg / "utils.py").write_text("def helper(): pass")

        scanner = Scanner()
        module = scanner.scan_module(pkg / "utils.py", tmp_path)
        assert module.full_path == "mypackage.utils"

    def test_init_module_path(self, tmp_path):
        pkg = tmp_path / "mypackage"
        pkg.mkdir()
        (pkg / "__init__.py").write_text('"""Package init."""')

        scanner = Scanner()
        module = scanner.scan_module(pkg / "__init__.py", tmp_path)
        assert module.full_path == "mypackage"


class TestScanMarkdown:
    def test_scan_markdown(self, tmp_path):
        md = tmp_path / "guide.md"
        md.write_text("# Getting Started\n\nWelcome to the guide.")

        scanner = Scanner()
        page = scanner.scan_markdown(md, tmp_path)
        assert page.title == "Getting Started"
        assert page.slug == "guide"
        assert "Welcome" in page.content

    def test_numbered_page_order(self, tmp_path):
        md = tmp_path / "03-config.md"
        md.write_text("# Configuration\n\nConfig docs.")

        scanner = Scanner()
        page = scanner.scan_markdown(md, tmp_path)
        assert page.order == 3

    def test_slug_from_nested_path(self, tmp_path):
        subdir = tmp_path / "pages"
        subdir.mkdir()
        md = subdir / "my guide.md"
        md.write_text("# My Guide\n\nContent.")

        scanner = Scanner()
        page = scanner.scan_markdown(md, tmp_path)
        assert "pages/my-guide" in page.slug


class TestScanDirectory:
    def test_scan_directory(self, tmp_path):
        (tmp_path / "app.py").write_text('"""App module."""\ndef main(): pass')
        (tmp_path / "README.md").write_text("# README\n\nHello.")

        modules, pages = scan_directory(str(tmp_path))
        assert len(modules) == 1
        assert len(pages) == 1
        assert modules[0].name == "app"
        assert pages[0].title == "README"
