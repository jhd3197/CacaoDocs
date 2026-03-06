"""Tests for cacaodocs.types dataclasses and enums."""

from cacaodocs.types import (
    ArgDoc,
    ClassDoc,
    ConfigFieldDoc,
    CustomDocTypeDef,
    CustomSectionDef,
    DocType,
    DocumentationData,
    FunctionDoc,
    HeaderDoc,
    MethodDoc,
    ModuleDoc,
    PageDoc,
    ParsedDocstring,
    PayloadFieldDoc,
    RaiseDoc,
    ResponseDoc,
    ReturnDoc,
)


class TestDocType:
    def test_enum_values(self):
        assert DocType.FUNCTION == "function"
        assert DocType.API == "api"
        assert DocType.CLASS == "class"
        assert DocType.PAGE == "page"
        assert DocType.CONFIG == "config"
        assert DocType.EVENT == "event"
        assert DocType.CUSTOM == "custom"

    def test_enum_from_value(self):
        assert DocType("function") is DocType.FUNCTION
        assert DocType("api") is DocType.API

    def test_is_string(self):
        assert isinstance(DocType.FUNCTION, str)


class TestArgDoc:
    def test_defaults(self):
        arg = ArgDoc(name="x", type="int", description="A number")
        assert arg.default is None
        assert arg.required is None

    def test_with_all_fields(self):
        arg = ArgDoc(name="x", type="int", description="A number", default="0", required=True)
        assert arg.default == "0"
        assert arg.required is True


class TestParsedDocstring:
    def test_defaults(self):
        p = ParsedDocstring()
        assert p.summary == ""
        assert p.doc_type == DocType.FUNCTION
        assert p.args == []
        assert p.returns is None
        assert p.responses == []
        assert p.custom_sections == {}

    def test_api_fields(self):
        p = ParsedDocstring(
            doc_type=DocType.API,
            http_method="GET",
            path="/users",
        )
        assert p.http_method == "GET"
        assert p.path == "/users"


class TestResponseDoc:
    def test_creation(self):
        r = ResponseDoc(status_code=200, description="OK")
        assert r.fields == []


class TestConfigFieldDoc:
    def test_creation(self):
        f = ConfigFieldDoc(name="DEBUG", type="bool", description="Enable debug")
        assert f.default is None
        assert f.required is False
        assert f.env_var == ""


class TestCustomDocTypeDef:
    def test_creation(self):
        ct = CustomDocTypeDef(
            name="cli_command",
            label="CLI Command",
            icon="terminal",
            sections=[CustomSectionDef(name="Usage", format="code")],
        )
        assert ct.sections[0].format == "code"


class TestDocumentationData:
    def test_defaults(self):
        d = DocumentationData()
        assert d.modules == []
        assert d.pages == []
        assert d.config == {}
