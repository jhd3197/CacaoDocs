# cacaodocs/__init__.py
"""CacaoDocs - Generate beautiful documentation from Python docstrings."""

from .cli import cli, main
from .builder import build_docs, build_json, build_html
from .scanner import Scanner, scan_directory
from .parser import DocstringParser
from .config import load_config, create_default_config
from .types import (
    ModuleDoc,
    ClassDoc,
    FunctionDoc,
    MethodDoc,
    PageDoc,
    ParsedDocstring,
    ArgDoc,
    ReturnDoc,
    RaiseDoc,
    DocumentationData,
)

__version__ = "0.2.0"

__all__ = [
    # CLI
    "cli",
    "main",
    # Builder
    "build_docs",
    "build_json",
    "build_html",
    # Scanner
    "Scanner",
    "scan_directory",
    # Parser
    "DocstringParser",
    # Config
    "load_config",
    "create_default_config",
    # Types
    "ModuleDoc",
    "ClassDoc",
    "FunctionDoc",
    "MethodDoc",
    "PageDoc",
    "ParsedDocstring",
    "ArgDoc",
    "ReturnDoc",
    "RaiseDoc",
    "DocumentationData",
]
