"""Google-style docstring parser."""
import re
from typing import Optional

from .types import ArgDoc, ParsedDocstring, RaiseDoc, ReturnDoc


class DocstringParser:
    """Parser for Google-style docstrings.

    Parses docstrings following Google's Python style guide:
    https://google.github.io/styleguide/pyguide.html#38-comments-and-docstrings
    """

    # Section headers recognized by the parser
    SECTION_HEADERS = [
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
    ]

    def __init__(self):
        # Build regex pattern for section headers
        headers_pattern = "|".join(self.SECTION_HEADERS)
        self.section_pattern = re.compile(
            rf"^\s*({headers_pattern}):\s*$", re.MULTILINE | re.IGNORECASE
        )
        # Pattern for argument lines: name (type): description
        # or name: description
        self.arg_pattern = re.compile(
            r"^\s{4,}(\*{0,2}\w+)"  # arg name with optional * or **
            r"(?:\s*\(([^)]+)\))?"  # optional type in parens
            r"\s*:\s*"  # colon separator
            r"(.*)$"  # description
        )
        # Pattern for type annotation in return
        self.return_type_pattern = re.compile(r"^([^:]+):\s*(.*)$")

    def parse(self, docstring: Optional[str]) -> ParsedDocstring:
        """Parse a Google-style docstring.

        Args:
            docstring: The docstring to parse.

        Returns:
            ParsedDocstring with extracted information.
        """
        if not docstring:
            return ParsedDocstring()

        # Normalize indentation
        lines = docstring.expandtabs(4).splitlines()
        docstring = self._dedent(lines)

        # Split into summary and rest
        summary, rest = self._split_summary(docstring)

        # Find all sections
        sections = self._split_sections(rest)

        # Parse each section
        args = []
        attributes = []
        returns = None
        raises = []
        examples = []
        notes = []
        description_parts = []

        for section_name, section_content in sections:
            section_lower = section_name.lower()

            if section_lower in ("args", "arguments"):
                args = self._parse_args(section_content)
            elif section_lower == "attributes":
                attributes = self._parse_args(section_content)
            elif section_lower in ("returns", "return", "yields", "yield"):
                returns = self._parse_returns(section_content)
            elif section_lower in ("raises", "raise", "exceptions"):
                raises = self._parse_raises(section_content)
            elif section_lower in ("examples", "example"):
                examples = self._parse_examples(section_content)
            elif section_lower in ("notes", "note"):
                notes = self._parse_notes(section_content)
            elif section_name == "":
                # This is description content
                description_parts.append(section_content.strip())

        description = "\n\n".join(description_parts)

        return ParsedDocstring(
            summary=summary,
            description=description,
            args=args,
            returns=returns,
            raises=raises,
            examples=examples,
            attributes=attributes,
            notes=notes,
        )

    def _dedent(self, lines: list[str]) -> str:
        """Remove common leading whitespace from lines."""
        if not lines:
            return ""

        # Find minimum indentation (ignoring empty lines)
        min_indent = float("inf")
        for line in lines[1:]:  # Skip first line
            stripped = line.lstrip()
            if stripped:
                indent = len(line) - len(stripped)
                min_indent = min(min_indent, indent)

        if min_indent == float("inf"):
            min_indent = 0

        # Dedent all lines
        result = [lines[0].strip()]
        for line in lines[1:]:
            if line.strip():
                result.append(line[int(min_indent):])
            else:
                result.append("")

        return "\n".join(result)

    def _split_summary(self, docstring: str) -> tuple[str, str]:
        """Split docstring into summary and rest."""
        # Find first blank line or section header
        lines = docstring.split("\n")
        summary_lines = []
        rest_start = 0

        for i, line in enumerate(lines):
            stripped = line.strip()
            if not stripped:
                rest_start = i + 1
                break
            # Check if it's a section header
            if self.section_pattern.match(line):
                rest_start = i
                break
            summary_lines.append(stripped)
            rest_start = i + 1

        summary = " ".join(summary_lines)
        rest = "\n".join(lines[rest_start:])
        return summary, rest

    def _split_sections(self, text: str) -> list[tuple[str, str]]:
        """Split text into sections based on headers."""
        if not text.strip():
            return []

        sections = []
        lines = text.split("\n")
        current_section = ""
        current_content = []

        for line in lines:
            match = self.section_pattern.match(line)
            if match:
                # Save previous section
                if current_content or current_section:
                    sections.append((current_section, "\n".join(current_content)))
                current_section = match.group(1)
                current_content = []
            else:
                current_content.append(line)

        # Save last section
        if current_content or current_section:
            sections.append((current_section, "\n".join(current_content)))

        return sections

    def _parse_args(self, content: str) -> list[ArgDoc]:
        """Parse Args section content."""
        args = []
        lines = content.split("\n")
        current_arg = None
        current_desc_lines = []

        for line in lines:
            match = self.arg_pattern.match(line)
            if match:
                # Save previous arg
                if current_arg:
                    current_arg.description = " ".join(current_desc_lines).strip()
                    args.append(current_arg)

                name = match.group(1)
                type_hint = match.group(2) or ""
                desc = match.group(3) or ""

                # Check for default value in type hint
                default = None
                if "=" in type_hint:
                    type_hint, default = type_hint.split("=", 1)
                    type_hint = type_hint.strip()
                    default = default.strip()

                current_arg = ArgDoc(
                    name=name,
                    type=type_hint.strip(),
                    description="",
                    default=default,
                )
                current_desc_lines = [desc] if desc else []
            elif current_arg and line.strip():
                # Continuation of description
                current_desc_lines.append(line.strip())

        # Save last arg
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

        # Try to parse type: description format
        match = self.return_type_pattern.match(first_line)
        if match:
            type_hint = match.group(1).strip()
            desc = match.group(2).strip()
            # Get rest of description from following lines
            if len(lines) > 1:
                rest = " ".join(line.strip() for line in lines[1:] if line.strip())
                if rest:
                    desc = f"{desc} {rest}" if desc else rest
            return ReturnDoc(type=type_hint, description=desc)

        # Just description, no type
        desc = " ".join(line.strip() for line in lines if line.strip())
        return ReturnDoc(type="", description=desc)

    def _parse_raises(self, content: str) -> list[RaiseDoc]:
        """Parse Raises section content."""
        raises = []
        lines = content.split("\n")
        current_raise = None
        current_desc_lines = []

        for line in lines:
            match = self.arg_pattern.match(line)
            if match:
                # Save previous
                if current_raise:
                    current_raise.description = " ".join(current_desc_lines).strip()
                    raises.append(current_raise)

                exc_type = match.group(1)
                desc = match.group(3) or ""
                current_raise = RaiseDoc(type=exc_type, description="")
                current_desc_lines = [desc] if desc else []
            elif line.strip():
                # Check if it's just an exception type
                stripped = line.strip()
                if stripped and not current_raise:
                    # Try to parse as "ExceptionType: description"
                    if ":" in stripped:
                        exc_type, desc = stripped.split(":", 1)
                        current_raise = RaiseDoc(
                            type=exc_type.strip(), description=desc.strip()
                        )
                        current_desc_lines = []
                elif current_raise:
                    current_desc_lines.append(stripped)

        # Save last
        if current_raise:
            current_raise.description = " ".join(current_desc_lines).strip()
            raises.append(current_raise)

        return raises

    def _parse_examples(self, content: str) -> list[str]:
        """Parse Examples section content."""
        examples = []
        lines = content.split("\n")
        current_example = []

        for line in lines:
            if line.strip().startswith(">>>") or current_example:
                current_example.append(line)
            elif line.strip() and not current_example:
                # Non-code example text
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
