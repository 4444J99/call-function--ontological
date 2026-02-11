"""Tests for the Aristotelian four-causes analysis module.

Verifies that analyze_four_causes produces valid Material, Formal,
Efficient, and Final causes for various function schemas.
"""

from __future__ import annotations

import pytest

from core.four_causes import CauseAnalysis, FourCausesReport, analyze_four_causes


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

PARAMETERLESS_SCHEMA: dict = {
    "name": "get_time",
    "description": "Get the current server time",
}

CREATE_SCHEMA: dict = {
    "name": "create_user",
    "description": "Create a new user account",
    "parameters": {
        "type": "object",
        "properties": {
            "username": {"type": "string", "description": "Desired username"},
            "email": {"type": "string", "description": "Email address"},
            "role": {"type": "string", "enum": ["admin", "user", "guest"]},
        },
        "required": ["username", "email"],
    },
}


class TestFourCausesBasics:
    """Basic structure tests."""

    def test_returns_report(self) -> None:
        result = analyze_four_causes(WEATHER_SCHEMA)
        assert isinstance(result, FourCausesReport)

    def test_function_name(self) -> None:
        result = analyze_four_causes(WEATHER_SCHEMA)
        assert result.function_name == "get_weather"

    def test_all_four_causes_present(self) -> None:
        result = analyze_four_causes(WEATHER_SCHEMA)
        assert len(result.all_causes) == 4

    def test_cause_types(self) -> None:
        result = analyze_four_causes(WEATHER_SCHEMA)
        types = {c.cause_type for c in result.all_causes}
        assert types == {"material", "formal", "efficient", "final"}

    def test_missing_name_raises(self) -> None:
        with pytest.raises(ValueError, match="name"):
            analyze_four_causes({"description": "no name"})


class TestMaterialCause:
    """Tests for material cause analysis."""

    def test_weather_has_parameters(self) -> None:
        result = analyze_four_causes(WEATHER_SCHEMA)
        assert "2 parameter" in result.material.summary
        assert result.material.confidence == "high"

    def test_parameterless_is_empty(self) -> None:
        result = analyze_four_causes(PARAMETERLESS_SCHEMA)
        assert "no parameters" in result.material.summary.lower()
        assert result.material.confidence == "high"

    def test_material_evidence_includes_params(self) -> None:
        result = analyze_four_causes(WEATHER_SCHEMA)
        evidence_text = " ".join(result.material.evidence)
        assert "location" in evidence_text
        assert "unit" in evidence_text

    def test_required_params_noted(self) -> None:
        result = analyze_four_causes(CREATE_SCHEMA)
        evidence_text = " ".join(result.material.evidence)
        assert "username" in evidence_text
        assert "email" in evidence_text


class TestFormalCause:
    """Tests for formal cause analysis."""

    def test_schema_type_noted(self) -> None:
        result = analyze_four_causes(WEATHER_SCHEMA)
        assert "object" in result.formal.summary.lower()

    def test_enum_constraints_noted(self) -> None:
        result = analyze_four_causes(WEATHER_SCHEMA)
        assert "enum" in result.formal.summary.lower()

    def test_required_constraints_noted(self) -> None:
        result = analyze_four_causes(WEATHER_SCHEMA)
        assert "required" in result.formal.summary.lower()


class TestEfficientCause:
    """Tests for efficient cause analysis."""

    def test_caller_mentioned(self) -> None:
        result = analyze_four_causes(WEATHER_SCHEMA)
        assert "caller" in result.efficient.summary.lower() or "trigger" in result.efficient.summary.lower()

    def test_verb_extracted(self) -> None:
        result = analyze_four_causes(WEATHER_SCHEMA)
        evidence_text = " ".join(result.efficient.evidence)
        assert "get" in evidence_text.lower()


class TestFinalCause:
    """Tests for final cause analysis."""

    def test_with_description_high_confidence(self) -> None:
        result = analyze_four_causes(WEATHER_SCHEMA)
        assert result.final.confidence == "high"
        assert "weather" in result.final.summary.lower()

    def test_without_description_low_confidence(self) -> None:
        result = analyze_four_causes({"name": "xyz_action"})
        assert result.final.confidence == "low"

    def test_purpose_category_inferred(self) -> None:
        result = analyze_four_causes(WEATHER_SCHEMA)
        assert "retrieval" in result.final.summary.lower()

    def test_create_purpose(self) -> None:
        result = analyze_four_causes(CREATE_SCHEMA)
        assert "creation" in result.final.summary.lower()


class TestSerialization:
    """Tests for to_dict serialization."""

    def test_to_dict_structure(self) -> None:
        result = analyze_four_causes(WEATHER_SCHEMA)
        d = result.to_dict()
        assert "function_name" in d
        assert "material" in d
        assert "formal" in d
        assert "efficient" in d
        assert "final" in d

    def test_cause_dict_structure(self) -> None:
        result = analyze_four_causes(WEATHER_SCHEMA)
        d = result.to_dict()
        for cause_key in ("material", "formal", "efficient", "final"):
            cause = d[cause_key]
            assert "cause_type" in cause
            assert "summary" in cause
            assert "evidence" in cause
            assert "confidence" in cause
