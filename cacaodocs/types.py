"""Data structures for parsed documentation."""
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class ArgDoc:
    """Represents a function/method argument."""
    name: str
    type: str
    description: str
    default: Optional[str] = None


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


@dataclass
class ParsedDocstring:
    """Parsed Google-style docstring."""
    summary: str = ""
    description: str = ""
    args: list[ArgDoc] = field(default_factory=list)
    returns: Optional[ReturnDoc] = None
    raises: list[RaiseDoc] = field(default_factory=list)
    examples: list[str] = field(default_factory=list)
    attributes: list[ArgDoc] = field(default_factory=list)
    notes: list[str] = field(default_factory=list)


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


@dataclass
class ModuleDoc:
    """Represents a Python module."""
    name: str
    full_path: str  # e.g., "cacao.server.signal"
    file_path: str
    docstring: str
    classes: list[ClassDoc] = field(default_factory=list)
    functions: list[FunctionDoc] = field(default_factory=list)


@dataclass
class PageDoc:
    """Represents a Markdown documentation page."""
    title: str
    slug: str
    content: str  # HTML from markdown
    file_path: str
    order: int = 0


@dataclass
class DocumentationData:
    """Complete documentation data structure."""
    modules: list[ModuleDoc] = field(default_factory=list)
    pages: list[PageDoc] = field(default_factory=list)
    config: dict = field(default_factory=dict)
