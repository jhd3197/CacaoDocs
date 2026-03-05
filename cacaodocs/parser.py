"""CacaoDocs docstring parser.

Parses Google-style docstrings extended with CacaoDocs doc types.
Supports built-in types (function, api, config, event) and custom types.
"""
import re
from typing import Any, Optional

from .types import (
    ArgDoc,
    ConfigFieldDoc,
    CustomDocTypeDef,
    DocType,
    HeaderDoc,
    ParsedDocstring,
    PayloadFieldDoc,
    RaiseDoc,
    ResponseDoc,
    ReturnDoc,
)


class DocstringParser:
    """Parser for CacaoDocs-style docstrings.

    Extends Google-style with doc type directives and API/config/event sections.
    """

    # All recognized section headers across all doc types
    SECTION_HEADERS = [
        # Standard (function/class)
        "Args",
        "Arguments",
        "Attributes",
        "Returns",
        "Return",
        "Yields",
        "Yield",
        "Raises",
        "Raise",
        "Exceptions",
        "Examples",
        "Example",
        "Notes",
        "Note",
        "See Also",
        "References",
        "Warnings",
        "Warning",
        "Todo",
        # API sections
        "Path Params",
        "Path Parameters",
        "Query Params",
        "Query Parameters",
        "Request Body",
        "Body",
        "Headers",
        # Event sections
        "Payload",
        "Trigger",
        # Config sections
        "Fields",
        "Config",
        "Configuration",
    ]

    # Response sections are matched separately: "Response (200):", "Response (404):", etc.
    RESPONSE_PATTERN = re.compile(r"^\s*Response\s*\((\d{3})\)\s*:\s*$", re.IGNORECASE)

    # Type directive: "Type: api" at the start of the docstring body
    TYPE_DIRECTIVE_PATTERN = re.compile(r"^\s*Type\s*:\s*(\w+)\s*$", re.IGNORECASE)

    # Method directive: "Method: GET"
    METHOD_DIRECTIVE_PATTERN = re.compile(r"^\s*Method\s*:\s*(\w+)\s*$", re.IGNORECASE)

    # Path directive: "Path: /users/{id}"
    PATH_DIRECTIVE_PATTERN = re.compile(r"^\s*Path\s*:\s*(.+)\s*$", re.IGNORECASE)

    # Trigger directive: "Trigger: When a user signs up"
    TRIGGER_DIRECTIVE_PATTERN = re.compile(r"^\s*Trigger\s*:\s*(.+)\s*$", re.IGNORECASE)

    def __init__(self, custom_types: list[CustomDocTypeDef] | None = None):
        self.custom_types = {ct.name: ct for ct in (custom_types or [])}

        # Add custom section headers
        all_headers = list(self.SECTION_HEADERS)
        for ct in (custom_types or []):
            for section in ct.sections:
                if section.name not in all_headers:
                    all_headers.append(section.name)

        # Build regex pattern for section headers
        headers_pattern = "|".join(re.escape(h) for h in all_headers)
        self.section_pattern = re.compile(
            rf"^\s*({headers_pattern}):\s*$", re.MULTILINE | re.IGNORECASE
        )

        # Pattern for argument lines: name (type): description
        self.arg_pattern = re.compile(
            r"^\s{4,}(\*{0,2}\w+)"  # arg name with optional * or **
            r"(?:\s*\(([^)]+)\))?"  # optional type in parens
            r"\s*:\s*"  # colon separator
            r"(.*)$"  # description
        )
        # Pattern for type annotation in return
        self.return_type_pattern = re.compile(r"^([^:]+):\s*(.*)$")

    def parse(self, docstring: Optional[str], hint_type: DocType | None = None) -> ParsedDocstring:
        """Parse a docstring into structured sections.

        Args:
            docstring: The raw docstring text.
            hint_type: Doc type hint from auto-detection (decorator analysis).
                The explicit Type: directive in the docstring takes precedence.

        Returns:
            ParsedDocstring with all parsed sections.
        """
        if not docstring:
            return ParsedDocstring()

        # Normalize indentation
        lines = docstring.expandtabs(4).splitlines()
        docstring = self._dedent(lines)

        # Extract Type: directive and other top-level directives
        doc_type, docstring = self._extract_type_directive(docstring, hint_type)

        # Extract Method/Path/Trigger directives
        directives, docstring = self._extract_directives(docstring)

        # Split into summary and rest
        summary, rest = self._split_summary(docstring)

        # Find all sections (including Response(NNN) sections)
        sections, response_sections = self._split_sections(rest)

        # Parse each section based on doc type
        result = ParsedDocstring(
            summary=summary,
            doc_type=doc_type,
            http_method=directives.get("method", ""),
            path=directives.get("path", ""),
            trigger=directives.get("trigger", ""),
        )

        description_parts = []

        for section_name, section_content in sections:
            self._parse_section(section_name, section_content, result, description_parts)

        # Parse response sections
        for status_code, content in response_sections:
            desc_lines = []
            fields = []
            for line in content.split("\n"):
                match = self.arg_pattern.match(line)
                if match:
                    fields.append(ArgDoc(
                        name=match.group(1),
                        type=match.group(2) or "",
                        description=match.group(3) or "",
                    ))
                elif line.strip() and not fields:
                    desc_lines.append(line.strip())
            result.responses.append(ResponseDoc(
                status_code=status_code,
                description=" ".join(desc_lines),
                fields=fields,
            ))

        result.description = "\n\n".join(description_parts)

        # For custom types, parse remaining sections into custom_sections
        if doc_type == DocType.CUSTOM and doc_type.value in self.custom_types:
            # Already handled in _parse_section
            pass

        return result

    def _extract_type_directive(self, docstring: str, hint: DocType | None) -> tuple[DocType, str]:
        """Extract the Type: directive from the docstring."""
        lines = docstring.split("\n")
        new_lines = []
        explicit_type = None

        for line in lines:
            match = self.TYPE_DIRECTIVE_PATTERN.match(line)
            if match and explicit_type is None:
                type_str = match.group(1).lower()
                try:
                    explicit_type = DocType(type_str)
                except ValueError:
                    # Could be a custom type
                    if type_str in self.custom_types:
                        explicit_type = DocType.CUSTOM
                    else:
                        # Unknown type, keep line and default
                        new_lines.append(line)
            else:
                new_lines.append(line)

        doc_type = explicit_type or hint or DocType.FUNCTION
        return doc_type, "\n".join(new_lines)

    def _extract_directives(self, docstring: str) -> tuple[dict[str, str], str]:
        """Extract Method:, Path:, Trigger: directives."""
        lines = docstring.split("\n")
        new_lines = []
        directives: dict[str, str] = {}

        for line in lines:
            m = self.METHOD_DIRECTIVE_PATTERN.match(line)
            if m and "method" not in directives:
                directives["method"] = m.group(1).upper()
                continue
            m = self.PATH_DIRECTIVE_PATTERN.match(line)
            if m and "path" not in directives:
                directives["path"] = m.group(1).strip()
                continue
            m = self.TRIGGER_DIRECTIVE_PATTERN.match(line)
            if m and "trigger" not in directives:
                directives["trigger"] = m.group(1).strip()
                continue
            new_lines.append(line)

        return directives, "\n".join(new_lines)

    def _split_summary(self, docstring: str) -> tuple[str, str]:
        """Split docstring into summary and rest."""
        lines = docstring.split("\n")
        summary_lines = []
        rest_start = 0

        for i, line in enumerate(lines):
            stripped = line.strip()
            if not stripped:
                rest_start = i + 1
                break
            if self.section_pattern.match(line) or self.RESPONSE_PATTERN.match(line):
                rest_start = i
                break
            summary_lines.append(stripped)
            rest_start = i + 1

        summary = " ".join(summary_lines)
        rest = "\n".join(lines[rest_start:])
        return summary, rest

    def _split_sections(self, text: str) -> tuple[list[tuple[str, str]], list[tuple[int, str]]]:
        """Split text into named sections and response sections."""
        if not text.strip():
            return [], []

        sections: list[tuple[str, str]] = []
        response_sections: list[tuple[int, str]] = []
        lines = text.split("\n")
        current_section = ""
        current_content: list[str] = []
        current_response_code: int | None = None

        for line in lines:
            # Check for Response(NNN): pattern
            resp_match = self.RESPONSE_PATTERN.match(line)
            if resp_match:
                # Save previous
                self._save_current(
                    current_section, current_content, current_response_code,
                    sections, response_sections,
                )
                current_response_code = int(resp_match.group(1))
                current_section = ""
                current_content = []
                continue

            # Check for regular section header
            match = self.section_pattern.match(line)
            if match:
                self._save_current(
                    current_section, current_content, current_response_code,
                    sections, response_sections,
                )
                current_section = match.group(1)
                current_response_code = None
                current_content = []
            else:
                current_content.append(line)

        # Save last
        self._save_current(
            current_section, current_content, current_response_code,
            sections, response_sections,
        )

        return sections, response_sections

    def _save_current(
        self,
        section: str,
        content: list[str],
        response_code: int | None,
        sections: list[tuple[str, str]],
        response_sections: list[tuple[int, str]],
    ):
        """Helper to save current section or response section."""
        if not content and not section and response_code is None:
            return
        text = "\n".join(content)
        if response_code is not None:
            response_sections.append((response_code, text))
        elif content or section:
            sections.append((section, text))

    def _parse_section(
        self,
        section_name: str,
        content: str,
        result: ParsedDocstring,
        description_parts: list[str],
    ):
        """Parse a single section and populate the result."""
        section_lower = section_name.lower()

        # Standard function sections
        if section_lower in ("args", "arguments"):
            result.args = self._parse_args(content)
        elif section_lower == "attributes":
            result.attributes = self._parse_args(content)
        elif section_lower in ("returns", "return", "yields", "yield"):
            result.returns = self._parse_returns(content)
        elif section_lower in ("raises", "raise", "exceptions"):
            result.raises = self._parse_raises(content)
        elif section_lower in ("examples", "example"):
            result.examples = self._parse_examples(content)
        elif section_lower in ("notes", "note"):
            result.notes = self._parse_notes(content)

        # API sections
        elif section_lower in ("path params", "path parameters"):
            result.path_params = self._parse_args(content)
        elif section_lower in ("query params", "query parameters"):
            result.query_params = self._parse_args(content)
        elif section_lower in ("request body", "body"):
            result.request_body = self._parse_args(content)
        elif section_lower == "headers":
            result.headers = self._parse_headers(content)

        # Event sections
        elif section_lower == "payload":
            result.payload = self._parse_payload(content)

        # Config sections
        elif section_lower in ("fields", "config", "configuration"):
            result.config_fields = self._parse_config_fields(content)

        # Description (no section name)
        elif section_name == "":
            stripped = content.strip()
            if stripped:
                description_parts.append(stripped)

        # Custom sections
        else:
            result.custom_sections[section_name] = content.strip()

    def _dedent(self, lines: list[str]) -> str:
        """Remove common leading whitespace from lines."""
        if not lines:
            return ""

        min_indent = float("inf")
        for line in lines[1:]:
            stripped = line.lstrip()
            if stripped:
                indent = len(line) - len(stripped)
                min_indent = min(min_indent, indent)

        if min_indent == float("inf"):
            min_indent = 0

        result = [lines[0].strip()]
        for line in lines[1:]:
            if line.strip():
                result.append(line[int(min_indent):])
            else:
                result.append("")

        return "\n".join(result)

    def _parse_args(self, content: str) -> list[ArgDoc]:
        """Parse Args-style section content."""
        args = []
        lines = content.split("\n")
        current_arg = None
        current_desc_lines: list[str] = []

        for line in lines:
            match = self.arg_pattern.match(line)
            if match:
                if current_arg:
                    current_arg.description = " ".join(current_desc_lines).strip()
                    args.append(current_arg)

                name = match.group(1)
                type_hint = match.group(2) or ""
                desc = match.group(3) or ""

                default = None
                required = None
                if "=" in type_hint:
                    type_hint, default = type_hint.split("=", 1)
                    type_hint = type_hint.strip()
                    default = default.strip()
                # Check for "required" marker
                if "required" in type_hint.lower():
                    required = True
                    type_hint = re.sub(r",?\s*required", "", type_hint, flags=re.IGNORECASE).strip()

                current_arg = ArgDoc(
                    name=name,
                    type=type_hint.strip(),
                    description="",
                    default=default,
                    required=required,
                )
                current_desc_lines = [desc] if desc else []
            elif current_arg and line.strip():
                current_desc_lines.append(line.strip())

        if current_arg:
            current_arg.description = " ".join(current_desc_lines).strip()
            args.append(current_arg)

        return args

    def _parse_returns(self, content: str) -> Optional[ReturnDoc]:
        """Parse Returns section content."""
        content = content.strip()
        if not content:
            return None

        lines = content.split("\n")
        first_line = lines[0].strip()

        match = self.return_type_pattern.match(first_line)
        if match:
            type_hint = match.group(1).strip()
            desc = match.group(2).strip()
            if len(lines) > 1:
                rest = " ".join(line.strip() for line in lines[1:] if line.strip())
                if rest:
                    desc = f"{desc} {rest}" if desc else rest
            return ReturnDoc(type=type_hint, description=desc)

        desc = " ".join(line.strip() for line in lines if line.strip())
        return ReturnDoc(type="", description=desc)

    def _parse_raises(self, content: str) -> list[RaiseDoc]:
        """Parse Raises section content."""
        raises = []
        lines = content.split("\n")
        current_raise = None
        current_desc_lines: list[str] = []

        for line in lines:
            match = self.arg_pattern.match(line)
            if match:
                if current_raise:
                    current_raise.description = " ".join(current_desc_lines).strip()
                    raises.append(current_raise)
                exc_type = match.group(1)
                desc = match.group(3) or ""
                current_raise = RaiseDoc(type=exc_type, description="")
                current_desc_lines = [desc] if desc else []
            elif line.strip():
                stripped = line.strip()
                if stripped and not current_raise:
                    if ":" in stripped:
                        exc_type, desc = stripped.split(":", 1)
                        current_raise = RaiseDoc(
                            type=exc_type.strip(), description=desc.strip()
                        )
                        current_desc_lines = []
                elif current_raise:
                    current_desc_lines.append(stripped)

        if current_raise:
            current_raise.description = " ".join(current_desc_lines).strip()
            raises.append(current_raise)

        return raises

    def _parse_examples(self, content: str) -> list[str]:
        """Parse Examples section content."""
        examples = []
        lines = content.split("\n")
        current_example: list[str] = []

        for line in lines:
            if line.strip().startswith(">>>") or current_example:
                current_example.append(line)
            elif line.strip() and not current_example:
                current_example.append(line)

        if current_example:
            examples.append("\n".join(current_example))

        return examples

    def _parse_notes(self, content: str) -> list[str]:
        """Parse Notes section content."""
        content = content.strip()
        if not content:
            return []
        return [content]

    def _parse_headers(self, content: str) -> list[HeaderDoc]:
        """Parse Headers section content."""
        headers = []
        for line in content.split("\n"):
            match = self.arg_pattern.match(line)
            if match:
                name = match.group(1)
                meta = match.group(2) or ""
                desc = match.group(3) or ""
                required = "required" in meta.lower()
                headers.append(HeaderDoc(
                    name=name,
                    description=desc.strip(),
                    required=required,
                ))
        return headers

    def _parse_payload(self, content: str) -> list[PayloadFieldDoc]:
        """Parse Payload section content."""
        fields = []
        for line in content.split("\n"):
            match = self.arg_pattern.match(line)
            if match:
                fields.append(PayloadFieldDoc(
                    name=match.group(1),
                    type=match.group(2) or "",
                    description=match.group(3) or "",
                ))
        return fields

    def _parse_config_fields(self, content: str) -> list[ConfigFieldDoc]:
        """Parse Config/Fields section content."""
        fields = []
        lines = content.split("\n")
        current_field = None
        current_desc_lines: list[str] = []

        for line in lines:
            match = self.arg_pattern.match(line)
            if match:
                if current_field:
                    current_field.description = " ".join(current_desc_lines).strip()
                    fields.append(current_field)

                name = match.group(1)
                meta = match.group(2) or ""
                desc = match.group(3) or ""

                default = None
                required = False
                env_var = ""
                type_hint = meta

                # Parse meta: "str, required, env=MY_VAR, default=foo"
                if meta:
                    parts = [p.strip() for p in meta.split(",")]
                    type_parts = []
                    for part in parts:
                        lower = part.lower()
                        if lower == "required":
                            required = True
                        elif lower.startswith("env="):
                            env_var = part[4:].strip()
                        elif lower.startswith("default="):
                            default = part[8:].strip()
                        else:
                            type_parts.append(part)
                    type_hint = ", ".join(type_parts)

                current_field = ConfigFieldDoc(
                    name=name,
                    type=type_hint.strip(),
                    description="",
                    default=default,
                    required=required,
                    env_var=env_var,
                )
                current_desc_lines = [desc] if desc else []
            elif current_field and line.strip():
                current_desc_lines.append(line.strip())

        if current_field:
            current_field.description = " ".join(current_desc_lines).strip()
            fields.append(current_field)

        return fields
