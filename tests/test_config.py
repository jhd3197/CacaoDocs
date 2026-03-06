"""Tests for cacaodocs.config configuration loading."""

import pytest

from cacaodocs.config import (
    DEFAULT_CONFIG,
    _merge_from_yaml,
    _parse_custom_doc_types,
    create_default_config,
)
from cacaodocs.types import CustomDocTypeDef


class TestDefaultConfig:
    def test_has_required_keys(self):
        assert "title" in DEFAULT_CONFIG
        assert "description" in DEFAULT_CONFIG
        assert "version" in DEFAULT_CONFIG
        assert "theme" in DEFAULT_CONFIG
        assert "exclude_patterns" in DEFAULT_CONFIG

    def test_default_exclude_patterns(self):
        patterns = DEFAULT_CONFIG["exclude_patterns"]
        assert "__pycache__" in patterns
        assert ".venv" in patterns
        assert ".git" in patterns


class TestParseCustomDocTypes:
    def test_parse_dict_sections(self):
        raw = {
            "cli_command": {
                "label": "CLI Command",
                "icon": "terminal",
                "sections": [
                    {"name": "Usage", "format": "code"},
                    {"name": "Options", "format": "args"},
                ],
            }
        }
        result = _parse_custom_doc_types(raw)
        assert len(result) == 1
        assert result[0].name == "cli_command"
        assert result[0].label == "CLI Command"
        assert result[0].icon == "terminal"
        assert len(result[0].sections) == 2
        assert result[0].sections[0].name == "Usage"
        assert result[0].sections[0].format == "code"

    def test_parse_string_sections(self):
        raw = {
            "simple_type": {
                "sections": ["Overview", "Details"],
            }
        }
        result = _parse_custom_doc_types(raw)
        assert result[0].sections[0].name == "Overview"
        assert result[0].sections[0].format == "text"

    def test_default_label(self):
        raw = {"my_type": {"sections": []}}
        result = _parse_custom_doc_types(raw)
        assert result[0].label == "My Type"

    def test_empty_dict(self):
        assert _parse_custom_doc_types({}) == []


class TestMergeFromYaml:
    def test_simple_keys(self):
        config = DEFAULT_CONFIG.copy()
        yaml_data = {
            "title": "My API",
            "description": "API docs",
            "version": "2.0.0",
            "github_url": "https://github.com/test",
        }
        _merge_from_yaml(config, yaml_data)
        assert config["title"] == "My API"
        assert config["description"] == "API docs"
        assert config["version"] == "2.0.0"
        assert config["github_url"] == "https://github.com/test"

    def test_exclude_patterns_merge(self):
        config = DEFAULT_CONFIG.copy()
        original_count = len(config["exclude_patterns"])
        yaml_data = {"exclude_patterns": ["custom_dir", "*.tmp"]}
        _merge_from_yaml(config, yaml_data)
        assert "custom_dir" in config["exclude_patterns"]
        assert "*.tmp" in config["exclude_patterns"]
        assert len(config["exclude_patterns"]) >= original_count

    def test_theme_override(self):
        config = DEFAULT_CONFIG.copy()
        _merge_from_yaml(config, {"theme": "light"})
        assert config["theme"] == "light"

    def test_doc_types_parsed(self):
        config = DEFAULT_CONFIG.copy()
        yaml_data = {
            "doc_types": {
                "model": {
                    "label": "Model",
                    "sections": [{"name": "Fields", "format": "args"}],
                }
            }
        }
        _merge_from_yaml(config, yaml_data)
        assert "custom_doc_types" in config
        assert len(config["custom_doc_types"]) == 1
        assert isinstance(config["custom_doc_types"][0], CustomDocTypeDef)

    def test_none_yaml_data(self):
        config = DEFAULT_CONFIG.copy()
        _merge_from_yaml(config, None)
        assert config["title"] == DEFAULT_CONFIG["title"]

    def test_chat_config(self):
        config = DEFAULT_CONFIG.copy()
        yaml_data = {"chat": True, "chat_config": {"model": "gpt-4"}}
        _merge_from_yaml(config, yaml_data)
        assert config["chat"] is True
        assert config["chat_config"]["model"] == "gpt-4"

    def test_page_order(self):
        config = DEFAULT_CONFIG.copy()
        yaml_data = {"page_order": ["intro", "setup", "api"]}
        _merge_from_yaml(config, yaml_data)
        assert config["page_order"] == ["intro", "setup", "api"]


class TestCreateDefaultConfig:
    def test_creates_file(self, tmp_path):
        output = tmp_path / "cacao.yaml"
        create_default_config(output)
        assert output.exists()
        content = output.read_text()
        assert "title:" in content
        assert "description:" in content
        assert "exclude_patterns:" in content
