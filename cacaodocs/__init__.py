"""CacaoDocs - Generate documentation from Python docstrings, powered by Cacao."""

from .scanner import Scanner, scan_directory
from .parser import DocstringParser
from .config import load_config, create_default_config
from .builder import build_docs
from .types import (
    DocType,
    ModuleDoc,
    ClassDoc,
    FunctionDoc,
    MethodDoc,
    PageDoc,
    ParsedDocstring,
    ArgDoc,
    ReturnDoc,
    RaiseDoc,
    ResponseDoc,
    HeaderDoc,
    PayloadFieldDoc,
    ConfigFieldDoc,
    CustomDocTypeDef,
    CustomSectionDef,
    DocumentationData,
)

__version__ = "0.4.0"

__all__ = [
    "build_docs",
    "Scanner",
    "scan_directory",
    "DocstringParser",
    "load_config",
    "create_default_config",
    "DocType",
    "ModuleDoc",
    "ClassDoc",
    "FunctionDoc",
    "MethodDoc",
    "PageDoc",
    "ParsedDocstring",
    "ArgDoc",
    "ReturnDoc",
    "RaiseDoc",
    "ResponseDoc",
    "HeaderDoc",
    "PayloadFieldDoc",
    "ConfigFieldDoc",
    "CustomDocTypeDef",
    "CustomSectionDef",
    "DocumentationData",
]
