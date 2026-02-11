"""Integration tests for the full OntologicalAnalyzer pipeline.

Verifies that the analyzer correctly orchestrates all sub-analyses
and produces a coherent FullAnalysis result.
"""

from __future__ import annotations

import json

import pytest

from application.analyzer import FullAnalysis, OntologicalAnalyzer
from application.grounding_report import (
    format_json_report,
    format_summary,
    format_text_report,
)


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

WEATHER_JSON: str = json.dumps(WEATHER_SCHEMA)


class TestAnalyzerPipeline:
    """End-to-end analyzer tests."""

    @pytest.fixture()
    def analyzer(self) -> OntologicalAnalyzer:
        return OntologicalAnalyzer()

    def test_analyze_dict(self, analyzer: OntologicalAnalyzer) -> None:
        result = analyzer.analyze(WEATHER_SCHEMA)
        assert isinstance(result, FullAnalysis)

    def test_analyze_json_string(self, analyzer: OntologicalAnalyzer) -> None:
        result = analyzer.analyze(WEATHER_JSON)
        assert isinstance(result, FullAnalysis)

    def test_analyze_json_method(self, analyzer: OntologicalAnalyzer) -> None:
        result = analyzer.analyze_json(WEATHER_JSON)
        assert isinstance(result, FullAnalysis)

    def test_function_name_consistent(self, analyzer: OntologicalAnalyzer) -> None:
        result = analyzer.analyze(WEATHER_SCHEMA)
        assert result.function_name == "get_weather"
        assert result.four_causes.function_name == "get_weather"
        assert result.dasein.function_name == "get_weather"
        assert result.semiotics.function_name == "get_weather"
        assert result.grounding.function_name == "get_weather"

    def test_all_sub_analyses_present(self, analyzer: OntologicalAnalyzer) -> None:
        result = analyzer.analyze(WEATHER_SCHEMA)
        assert result.four_causes is not None
        assert result.dasein is not None
        assert result.semiotics is not None
        assert result.grounding is not None

    def test_missing_name_raises(self, analyzer: OntologicalAnalyzer) -> None:
        with pytest.raises(ValueError, match="name"):
            analyzer.analyze({"description": "no name"})

    def test_invalid_json_raises(self, analyzer: OntologicalAnalyzer) -> None:
        with pytest.raises(json.JSONDecodeError):
            analyzer.analyze("not valid json {{{")


class TestFullAnalysisSerialization:
    """Test FullAnalysis serialization methods."""

    @pytest.fixture()
    def result(self) -> FullAnalysis:
        return OntologicalAnalyzer().analyze(WEATHER_SCHEMA)

    def test_to_dict(self, result: FullAnalysis) -> None:
        d = result.to_dict()
        assert "function_name" in d
        assert "four_causes" in d
        assert "dasein" in d
        assert "semiotics" in d
        assert "grounding" in d

    def test_to_json(self, result: FullAnalysis) -> None:
        j = result.to_json()
        parsed = json.loads(j)
        assert parsed["function_name"] == "get_weather"

    def test_to_json_roundtrip(self, result: FullAnalysis) -> None:
        j = result.to_json()
        parsed = json.loads(j)
        assert parsed == result.to_dict()


class TestReportFormatters:
    """Test report formatting functions."""

    @pytest.fixture()
    def result(self) -> FullAnalysis:
        return OntologicalAnalyzer().analyze(WEATHER_SCHEMA)

    def test_text_report_not_empty(self, result: FullAnalysis) -> None:
        text = format_text_report(result)
        assert len(text) > 100

    def test_text_report_contains_sections(self, result: FullAnalysis) -> None:
        text = format_text_report(result)
        assert "ARISTOTELIAN" in text
        assert "HEIDEGGERIAN" in text
        assert "PEIRCEAN" in text
        assert "GROUNDING" in text

    def test_text_report_contains_function_name(self, result: FullAnalysis) -> None:
        text = format_text_report(result)
        assert "get_weather" in text

    def test_json_report_valid(self, result: FullAnalysis) -> None:
        j = format_json_report(result)
        parsed = json.loads(j)
        assert parsed["function_name"] == "get_weather"

    def test_summary_not_empty(self, result: FullAnalysis) -> None:
        s = format_summary(result)
        assert len(s) > 50
        assert "get_weather" in s

    def test_summary_includes_coverage(self, result: FullAnalysis) -> None:
        s = format_summary(result)
        assert "coverage" in s.lower() or "/" in s


class TestMultipleSchemas:
    """Test that the analyzer handles diverse schemas correctly."""

    @pytest.fixture()
    def analyzer(self) -> OntologicalAnalyzer:
        return OntologicalAnalyzer()

    def test_minimal_schema(self, analyzer: OntologicalAnalyzer) -> None:
        result = analyzer.analyze({"name": "ping"})
        assert result.function_name == "ping"
        assert result.grounding.applicable_count > 0

    def test_complex_schema(self, analyzer: OntologicalAnalyzer) -> None:
        schema = {
            "name": "search_products",
            "description": "Search the product catalog",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "Search query"},
                    "category": {
                        "type": "string",
                        "enum": ["electronics", "clothing", "food"],
                    },
                    "max_price": {"type": "number", "description": "Maximum price"},
                    "in_stock": {"type": "boolean", "description": "Only in-stock items"},
                },
                "required": ["query"],
            },
        }
        result = analyzer.analyze(schema)
        assert result.function_name == "search_products"
        assert len(result.four_causes.all_causes) == 4
        assert result.grounding.coverage_ratio > 0.8

    def test_stateless_across_calls(self, analyzer: OntologicalAnalyzer) -> None:
        """Verify the analyzer is stateless between calls."""
        r1 = analyzer.analyze({"name": "func_a", "description": "First function"})
        r2 = analyzer.analyze({"name": "func_b", "description": "Second function"})
        assert r1.function_name == "func_a"
        assert r2.function_name == "func_b"
