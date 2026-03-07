"""Data structures for parsed documentation."""

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Optional


class DocType(str, Enum):
    """Built-in documentation types.

    Each type changes how docstrings are parsed and displayed.
    """

    FUNCTION = "function"
    API = "api"
    CLASS = "class"
    PAGE = "page"
    CONFIG = "config"
    EVENT = "event"
    CUSTOM = "custom"


# --- Shared doc atoms ---


@dataclass
class ArgDoc:
    """Represents a function/method argument or parameter."""

    name: str
    type: str
    description: str
    default: Optional[str] = None
    required: Optional[bool] = None


@dataclass
class ReturnDoc:
    """Represents return value documentation."""

    type: str
    description: str


@dataclass
class RaiseDoc:
    """Represents an exception that may be raised."""

    type: str
    description: str


# --- API-specific types ---


@dataclass
class ResponseDoc:
    """Represents an API response for a specific status code."""

    status_code: int
    description: str
    fields: list[ArgDoc] = field(default_factory=list)


@dataclass
class HeaderDoc:
    """Represents an HTTP header."""

    name: str
    description: str
    required: bool = False
    example: str = ""


# --- Event-specific types ---


@dataclass
class PayloadFieldDoc:
    """Represents a field in an event payload."""

    name: str
    type: str
    description: str


# --- Config-specific types ---


@dataclass
class ConfigFieldDoc:
    """Represents a configuration field or env var."""

    name: str
    type: str
    description: str
    default: Optional[str] = None
    required: bool = False
    env_var: str = ""


# --- Custom type definition ---


@dataclass
class CustomSectionDef:
    """Definition for a custom section in a user-defined doc type."""

    name: str
    format: str = "text"  # "text", "args", "code", "list"


@dataclass
class CustomDocTypeDef:
    """User-defined doc type from cacao.yaml."""

    name: str
    label: str
    icon: str = "file"
    sections: list[CustomSectionDef] = field(default_factory=list)


# --- Parsed docstring (extended) ---


@dataclass
class ParsedDocstring:
    """Parsed docstring with sections for all doc types."""

    summary: str = ""
    description: str = ""
    doc_type: DocType = DocType.FUNCTION

    # Function sections
    args: list[ArgDoc] = field(default_factory=list)
    returns: Optional[ReturnDoc] = None
    raises: list[RaiseDoc] = field(default_factory=list)
    examples: list[str] = field(default_factory=list)
    attributes: list[ArgDoc] = field(default_factory=list)
    notes: list[str] = field(default_factory=list)

    # API sections
    http_method: str = ""
    path: str = ""
    path_params: list[ArgDoc] = field(default_factory=list)
    query_params: list[ArgDoc] = field(default_factory=list)
    request_body: list[ArgDoc] = field(default_factory=list)
    responses: list[ResponseDoc] = field(default_factory=list)
    headers: list[HeaderDoc] = field(default_factory=list)

    # Event sections
    trigger: str = ""
    payload: list[PayloadFieldDoc] = field(default_factory=list)

    # Config sections
    config_fields: list[ConfigFieldDoc] = field(default_factory=list)

    # Custom sections (name -> content)
    custom_sections: dict[str, Any] = field(default_factory=dict)


# --- Document-level types ---


@dataclass
class MethodDoc:
    """Represents a class method."""

    name: str
    module: str
    signature: str
    docstring: ParsedDocstring
    is_async: bool
    is_classmethod: bool
    is_staticmethod: bool
    is_property: bool
    source: str
    line_number: int
    decorators: list[str] = field(default_factory=list)
    calls: list[str] = field(default_factory=list)
    doc_type: DocType = DocType.FUNCTION
    signature_hash: str = ""
    body_hash: str = ""
    body_statement_hashes: list[str] = field(default_factory=list)
    call_graph_hash: str = ""
    complexity: int = 1
    cognitive_weight: int = 0
    is_deprecated: bool = False
    deprecation_message: str = ""
    deprecation_since: str = ""
    category: str = ""
    version: str = ""
    hidden: bool = False


@dataclass
class FunctionDoc:
    """Represents a standalone function."""

    name: str
    module: str
    full_path: str
    signature: str
    docstring: ParsedDocstring
    is_async: bool
    source: str
    line_number: int
    decorators: list[str] = field(default_factory=list)
    calls: list[str] = field(default_factory=list)
    doc_type: DocType = DocType.FUNCTION
    signature_hash: str = ""
    body_hash: str = ""
    body_statement_hashes: list[str] = field(default_factory=list)
    call_graph_hash: str = ""
    complexity: int = 1
    cognitive_weight: int = 0
    is_deprecated: bool = False
    deprecation_message: str = ""
    deprecation_since: str = ""
    category: str = ""
    version: str = ""
    hidden: bool = False


@dataclass
class ClassDoc:
    """Represents a class."""

    name: str
    module: str
    full_path: str
    docstring: ParsedDocstring
    bases: list[str]
    methods: list[MethodDoc]
    source: str
    line_number: int
    decorators: list[str] = field(default_factory=list)
    doc_type: DocType = DocType.CLASS
    signature_hash: str = ""
    body_hash: str = ""


@dataclass
class TodoDoc:
    """A TODO/FIXME/HACK comment found in source code."""

    tag: str  # "TODO", "FIXME", "HACK", "XXX"
    text: str
    file_path: str
    line_number: int
    module: str = ""


@dataclass
class ModuleDoc:
    """Represents a Python module."""

    name: str
    full_path: str  # e.g., "cacao.server.signal"
    file_path: str
    docstring: str
    classes: list[ClassDoc] = field(default_factory=list)
    functions: list[FunctionDoc] = field(default_factory=list)
    todos: list[TodoDoc] = field(default_factory=list)


@dataclass
class PageDoc:
    """Represents a Markdown documentation page."""

    title: str
    slug: str
    content: str  # HTML from markdown
    file_path: str
    order: int = 0
    doc_type: DocType = DocType.PAGE


@dataclass
class DocumentationData:
    """Complete documentation data structure."""

    modules: list[ModuleDoc] = field(default_factory=list)
    pages: list[PageDoc] = field(default_factory=list)
    config: dict = field(default_factory=dict)
