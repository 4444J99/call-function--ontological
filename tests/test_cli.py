"""Tests for the CLI entry point.

Verifies that CLI commands (analyze, report, concepts) run without error
and produce expected output structures.
"""

from __future__ import annotations

import json
import tempfile
from pathlib import Path

import pytest

from tools.cli import build_parser, main


WEATHER_SCHEMA: dict = {
    "name": "get_weather",
    "description": "Get the current weather for a location",
    "parameters": {
        "type": "object",
        "properties": {
            "location": {"type": "string", "description": "City name"},
            "unit": {"type": "string", "enum": ["celsius", "fahrenheit"]},
        },
        "required": ["location"],
    },
}


@pytest.fixture()
def schema_file(tmp_path: Path) -> Path:
    """Create a temporary JSON schema file for testing."""
    filepath = tmp_path / "test_schema.json"
    filepath.write_text(json.dumps(WEATHER_SCHEMA))
    return filepath


class TestParserConstruction:
    """Test that the argument parser builds correctly."""

    def test_parser_creates(self) -> None:
        parser = build_parser()
        assert parser is not None

    def test_parser_prog_name(self) -> None:
        parser = build_parser()
        assert parser.prog == "ontological"


class TestAnalyzeCommand:
    """Test the 'analyze' command."""

    def test_analyze_produces_json(self, schema_file: Path, capsys: pytest.CaptureFixture[str]) -> None:
        import sys
        original_argv = sys.argv
        sys.argv = ["ontological", "analyze", str(schema_file)]
        try:
            main()
        finally:
            sys.argv = original_argv
        captured = capsys.readouterr()
        parsed = json.loads(captured.out)
        assert parsed["function_name"] == "get_weather"


class TestReportCommand:
    """Test the 'report' command."""

    def test_report_produces_text(self, schema_file: Path, capsys: pytest.CaptureFixture[str]) -> None:
        import sys
        original_argv = sys.argv
        sys.argv = ["ontological", "report", str(schema_file)]
        try:
            main()
        finally:
            sys.argv = original_argv
        captured = capsys.readouterr()
        assert "ONTOLOGICAL ANALYSIS" in captured.out
        assert "get_weather" in captured.out


class TestConceptsCommand:
    """Test the 'concepts' command."""

    def test_concepts_lists_twelve(self, capsys: pytest.CaptureFixture[str]) -> None:
        import sys
        original_argv = sys.argv
        sys.argv = ["ontological", "concepts"]
        try:
            main()
        finally:
            sys.argv = original_argv
        captured = capsys.readouterr()
        assert "12 concepts" in captured.out
        assert "Material Cause" in captured.out
        assert "Telos Bridge" in captured.out


class TestNoCommand:
    """Test behavior when no command is provided."""

    def test_no_command_exits(self) -> None:
        import sys
        original_argv = sys.argv
        sys.argv = ["ontological"]
        try:
            with pytest.raises(SystemExit) as exc_info:
                main()
            assert exc_info.value.code == 1
        finally:
            sys.argv = original_argv


class TestMissingFile:
    """Test behavior when the JSON file does not exist."""

    def test_missing_file_exits(self) -> None:
        import sys
        original_argv = sys.argv
        sys.argv = ["ontological", "analyze", "/nonexistent/path.json"]
        try:
            with pytest.raises(SystemExit) as exc_info:
                main()
            assert exc_info.value.code == 1
        finally:
            sys.argv = original_argv
