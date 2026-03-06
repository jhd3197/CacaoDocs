"""Tests for cacaodocs.parser docstring parsing."""

from cacaodocs.parser import DocstringParser
from cacaodocs.types import CustomDocTypeDef, CustomSectionDef, DocType


class TestParserEmpty:
    def test_none_docstring(self):
        parser = DocstringParser()
        result = parser.parse(None)
        assert result.summary == ""
        assert result.doc_type == DocType.FUNCTION

    def test_empty_docstring(self):
        parser = DocstringParser()
        result = parser.parse("")
        assert result.summary == ""


class TestParserSummary:
    def test_single_line(self):
        parser = DocstringParser()
        result = parser.parse("Get a user by ID.")
        assert result.summary == "Get a user by ID."

    def test_multiline_summary(self):
        parser = DocstringParser()
        result = parser.parse("Get a user\nby their ID.")
        assert result.summary == "Get a user by their ID."

    def test_summary_with_description(self):
        parser = DocstringParser()
        result = parser.parse("Summary line.\n\nMore details here.")
        assert result.summary == "Summary line."
        assert "More details" in result.description


class TestTypeDirective:
    def test_explicit_api_type(self):
        parser = DocstringParser()
        result = parser.parse("Type: api\nGet users endpoint.")
        assert result.doc_type == DocType.API

    def test_explicit_config_type(self):
        parser = DocstringParser()
        result = parser.parse("Type: config\nApp settings.")
        assert result.doc_type == DocType.CONFIG

    def test_explicit_event_type(self):
        parser = DocstringParser()
        result = parser.parse("Type: event\nUser signup event.")
        assert result.doc_type == DocType.EVENT

    def test_hint_type_fallback(self):
        parser = DocstringParser()
        result = parser.parse("Get users.", hint_type=DocType.API)
        assert result.doc_type == DocType.API

    def test_explicit_overrides_hint(self):
        parser = DocstringParser()
        result = parser.parse("Type: config\nSomething.", hint_type=DocType.API)
        assert result.doc_type == DocType.CONFIG

    def test_unknown_type_keeps_line(self):
        parser = DocstringParser()
        result = parser.parse("Type: nonexistent\nSummary here.")
        assert result.doc_type == DocType.FUNCTION
        assert "nonexistent" in result.summary or "Type" in result.summary


class TestDirectives:
    def test_method_directive(self):
        parser = DocstringParser()
        result = parser.parse("Type: api\nMethod: POST\nPath: /users\nCreate a user.")
        assert result.http_method == "POST"
        assert result.path == "/users"

    def test_trigger_directive(self):
        parser = DocstringParser()
        result = parser.parse("Type: event\nTrigger: When user signs up\nUser signup.")
        assert result.trigger == "When user signs up"


class TestArgsSection:
    def test_simple_args(self):
        parser = DocstringParser()
        docstring = """\
Do something.

Args:
    name (str): The user's name.
    age (int): The user's age."""
        result = parser.parse(docstring)
        assert len(result.args) == 2
        assert result.args[0].name == "name"
        assert result.args[0].type == "str"
        assert result.args[0].description == "The user's name."
        assert result.args[1].name == "age"

    def test_args_with_default(self):
        parser = DocstringParser()
        docstring = """\
Do something.

Args:
    limit (int=10): Max items."""
        result = parser.parse(docstring)
        assert result.args[0].default == "10"
        assert result.args[0].type == "int"

    def test_args_with_required(self):
        parser = DocstringParser()
        docstring = """\
Do something.

Args:
    name (str, required): The user name."""
        result = parser.parse(docstring)
        assert result.args[0].required is True

    def test_multiline_arg_description(self):
        parser = DocstringParser()
        docstring = """\
Do something.

Args:
    name (str): The user's name.
        Must be non-empty."""
        result = parser.parse(docstring)
        assert "Must be non-empty" in result.args[0].description


class TestReturnsSection:
    def test_typed_return(self):
        parser = DocstringParser()
        docstring = """\
Get user.

Returns:
    dict: The user object."""
        result = parser.parse(docstring)
        assert result.returns is not None
        assert result.returns.type == "dict"
        assert result.returns.description == "The user object."

    def test_untyped_return(self):
        parser = DocstringParser()
        docstring = """\
Get user.

Returns:
    The user object."""
        result = parser.parse(docstring)
        assert result.returns is not None
        assert result.returns.description == "The user object."


class TestRaisesSection:
    def test_raises(self):
        parser = DocstringParser()
        docstring = """\
Get user.

Raises:
    ValueError: If ID is invalid.
    KeyError: If user not found."""
        result = parser.parse(docstring)
        assert len(result.raises) == 2
        assert result.raises[0].type == "ValueError"
        assert result.raises[1].type == "KeyError"


class TestExamplesSection:
    def test_examples(self):
        parser = DocstringParser()
        docstring = """\
Get user.

Examples:
    >>> get_user(1)
    {'name': 'Alice'}"""
        result = parser.parse(docstring)
        assert len(result.examples) == 1
        assert "get_user(1)" in result.examples[0]


class TestAPIDocstring:
    def test_full_api_docstring(self):
        parser = DocstringParser()
        docstring = """\
Type: api
Method: GET
Path: /users/{user_id}
Get a user by ID.

Path Params:
    user_id (int, required): The user ID.

Query Params:
    fields (str): Comma-separated field names.

Headers:
    Authorization (required): Bearer token.

Response (200):
    Success response.
    id (int): User ID.
    name (str): User name.

Response (404):
    Not found."""
        result = parser.parse(docstring)
        assert result.doc_type == DocType.API
        assert result.http_method == "GET"
        assert result.path == "/users/{user_id}"
        assert len(result.path_params) == 1
        assert result.path_params[0].name == "user_id"
        assert len(result.query_params) == 1
        assert len(result.headers) == 1
        assert result.headers[0].required is True
        assert len(result.responses) == 2
        assert result.responses[0].status_code == 200
        assert len(result.responses[0].fields) == 2
        assert result.responses[1].status_code == 404


class TestRequestBody:
    def test_request_body(self):
        parser = DocstringParser()
        docstring = """\
Type: api
Method: POST
Path: /users
Create a user.

Request Body:
    name (str): User name.
    email (str): User email."""
        result = parser.parse(docstring)
        assert len(result.request_body) == 2
        assert result.request_body[0].name == "name"


class TestConfigDocstring:
    def test_config_fields(self):
        parser = DocstringParser()
        docstring = """\
Type: config
App configuration.

Fields:
    DEBUG (bool, required, env=DEBUG): Enable debug mode.
    PORT (int, default=8080): Server port.
    SECRET_KEY (str, required, env=APP_SECRET): Secret key."""
        result = parser.parse(docstring)
        assert result.doc_type == DocType.CONFIG
        assert len(result.config_fields) == 3
        assert result.config_fields[0].name == "DEBUG"
        assert result.config_fields[0].required is True
        assert result.config_fields[0].env_var == "DEBUG"
        assert result.config_fields[1].default == "8080"
        assert result.config_fields[2].env_var == "APP_SECRET"


class TestEventDocstring:
    def test_event_payload(self):
        parser = DocstringParser()
        docstring = """\
Type: event
Trigger: When a user signs up
User signup event.

Payload:
    user_id (int): The user ID.
    email (str): The email."""
        result = parser.parse(docstring)
        assert result.doc_type == DocType.EVENT
        assert result.trigger == "When a user signs up"
        assert len(result.payload) == 2
        assert result.payload[0].name == "user_id"


class TestCustomTypes:
    def test_custom_type_parsing(self):
        custom = CustomDocTypeDef(
            name="cli_command",
            label="CLI Command",
            sections=[
                CustomSectionDef(name="Usage", format="code"),
                CustomSectionDef(name="Options", format="args"),
            ],
        )
        parser = DocstringParser(custom_types=[custom])
        docstring = """\
Type: custom
Run the build command.

Usage:
    cacaodocs build ./src

Options:
    output (str): Output directory."""
        result = parser.parse(docstring)
        assert result.doc_type == DocType.CUSTOM
        assert "Usage" in result.custom_sections or len(result.args) > 0


class TestNotesSection:
    def test_notes(self):
        parser = DocstringParser()
        docstring = """\
Do something.

Notes:
    This is an important note."""
        result = parser.parse(docstring)
        assert len(result.notes) == 1
        assert "important note" in result.notes[0]


class TestAttributesSection:
    def test_attributes(self):
        parser = DocstringParser()
        docstring = """\
A class.

Attributes:
    name (str): The name.
    value (int): The value."""
        result = parser.parse(docstring)
        assert len(result.attributes) == 2
        assert result.attributes[0].name == "name"
