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


def doc(**kwargs):
    """CacaoDocs metadata decorator.

    A runtime no-op — returns the decorated function unchanged.
    CacaoDocs reads all keyword arguments from the AST at scan time,
    so this works as a full docstring replacement or supplement.

    Decorator values override anything parsed from the docstring.

    Kwargs:
        description (str): Summary/description of the function.
        doc_type (str): Override doc type ("api", "config", "event", etc.).
        deprecated (bool | str): True or a since-version string (e.g. "2.0").
        category (str): Group name for sidebar categorization.
        version (str): Version when this was added.
        hidden (bool): Exclude from generated documentation.

        args (dict): Arguments. ``{"name": "desc"}`` or
            ``{"name": {"type": "str", "description": "...", "default": "x"}}``.
        returns (str | dict): Return value. ``"desc"`` or
            ``{"type": "User", "description": "..."}``.
        raises (dict): Exceptions. ``{"ValueError": "when invalid"}``.
        examples (list[str]): Usage examples.
        notes (list[str]): Additional notes.
        attributes (dict): Class/object attributes (same format as args).

        method (str): HTTP method ("GET", "POST", etc.).
        path (str): Route path ("/users/{id}").
        path_params (dict): Path parameters (same format as args).
        query_params (dict): Query parameters (same format as args).
        request_body (dict): Request body fields (same format as args).
        responses (dict): Responses by status code.
            ``{200: "Success", 404: {"description": "...", "fields": {...}}}``.
        headers (dict): HTTP headers.
            ``{"Authorization": {"description": "...", "required": True}}``.

        trigger (str): Event trigger name.
        payload (dict): Event payload fields.
            ``{"user_id": {"type": "int", "description": "..."}}``.

        config_fields (dict): Config/env var fields.
            ``{"DEBUG": {"type": "bool", "default": "false", "env": "APP_DEBUG"}}``.

    Example::

        @doc(
            description="Fetch a user by ID.",
            args={"user_id": "The user's unique identifier"},
            returns={"type": "User", "description": "The matching user"},
            raises={"NotFoundError": "If user doesn't exist"},
            deprecated="2.0",
            category="Users",
        )
        def get_user(user_id: int) -> User:
            ...
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
