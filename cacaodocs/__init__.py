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


def doc(
    doc_type: str = "",
    deprecated: "bool | str" = False,
    category: str = "",
    version: str = "",
    hidden: bool = False,
):
    """CacaoDocs metadata decorator.

    This is a runtime no-op — it just returns the decorated function unchanged.
    CacaoDocs reads the keyword arguments from the AST at scan time.

    Args:
        doc_type: Override auto-detected doc type ("api", "config", "event", etc.).
        deprecated: True for deprecated, or a version string (e.g. "2.0") for since.
        category: Group name for sidebar categorization.
        version: Version when this function/method was added.
        hidden: If True, exclude from generated documentation.
    """
    def _identity(fn):
        return fn
    return _identity


__all__ = [
    "build_docs",
    "doc",
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
