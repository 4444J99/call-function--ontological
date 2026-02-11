"""Tests for the grounding module.

Verifies that known function-call schemas map to expected ontological
categories with correct applicability and coverage.
"""

from __future__ import annotations

import pytest

from core.grounding import GroundingReport, ground_function
from core.ontology import Domain


# Shared test fixtures.
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

MINIMAL_SCHEMA: dict = {
    "name": "ping",
}

NO_DESC_SCHEMA: dict = {
    "name": "do_something",
    "parameters": {
        "type": "object",
        "properties": {
            "value": {"type": "integer"},
        },
    },
}


class TestGroundingBasics:
    """Basic grounding report structure."""

    def test_returns_grounding_report(self) -> None:
        result = ground_function(WEATHER_SCHEMA)
        assert isinstance(result, GroundingReport)

    def test_function_name_preserved(self) -> None:
        result = ground_function(WEATHER_SCHEMA)
        assert result.function_name == "get_weather"

    def test_twelve_mappings(self) -> None:
        result = ground_function(WEATHER_SCHEMA)
        assert len(result.mappings) == 12

    def test_missing_name_raises(self) -> None:
        with pytest.raises(ValueError, match="name"):
            ground_function({"description": "no name"})


class TestWeatherSchemaGrounding:
    """Verify grounding for the well-specified weather schema."""

    @pytest.fixture()
    def report(self) -> GroundingReport:
        return ground_function(WEATHER_SCHEMA)

    def test_material_cause_applies(self, report: GroundingReport) -> None:
        material = next(m for m in report.mappings if m.concept.key == "material_cause")
        assert material.applies is True
        assert "location" in material.anchor

    def test_formal_cause_applies(self, report: GroundingReport) -> None:
        formal = next(m for m in report.mappings if m.concept.key == "formal_cause")
        assert formal.applies is True

    def test_efficient_cause_applies(self, report: GroundingReport) -> None:
        efficient = next(m for m in report.mappings if m.concept.key == "efficient_cause")
        assert efficient.applies is True

    def test_final_cause_applies(self, report: GroundingReport) -> None:
        final = next(m for m in report.mappings if m.concept.key == "final_cause")
        assert final.applies is True

    def test_dasein_applies(self, report: GroundingReport) -> None:
        dasein = next(m for m in report.mappings if m.concept.key == "dasein")
        assert dasein.applies is True

    def test_representamen_applies(self, report: GroundingReport) -> None:
        rep = next(m for m in report.mappings if m.concept.key == "representamen")
        assert rep.applies is True

    def test_telos_bridge_applies_with_description(self, report: GroundingReport) -> None:
        bridge = next(m for m in report.mappings if m.concept.key == "telos_bridge")
        assert bridge.applies is True

    def test_high_coverage(self, report: GroundingReport) -> None:
        assert report.coverage_ratio >= 0.9


class TestMinimalSchemaGrounding:
    """Verify grounding for a minimal schema with only a name."""

    @pytest.fixture()
    def report(self) -> GroundingReport:
        return ground_function(MINIMAL_SCHEMA)

    def test_material_cause_does_not_apply(self, report: GroundingReport) -> None:
        material = next(m for m in report.mappings if m.concept.key == "material_cause")
        assert material.applies is False

    def test_telos_bridge_does_not_apply(self, report: GroundingReport) -> None:
        bridge = next(m for m in report.mappings if m.concept.key == "telos_bridge")
        assert bridge.applies is False

    def test_lower_coverage_than_full_schema(self, report: GroundingReport) -> None:
        full_report = ground_function(WEATHER_SCHEMA)
        assert report.coverage_ratio < full_report.coverage_ratio


class TestDomainFiltering:
    """Verify domain-based filtering."""

    def test_aristotelian_mappings(self) -> None:
        report = ground_function(WEATHER_SCHEMA)
        aristotelian = report.mappings_by_domain(Domain.ARISTOTELIAN)
        assert len(aristotelian) == 4

    def test_heideggerian_mappings(self) -> None:
        report = ground_function(WEATHER_SCHEMA)
        heideggerian = report.mappings_by_domain(Domain.HEIDEGGERIAN)
        assert len(heideggerian) == 3

    def test_peircean_mappings(self) -> None:
        report = ground_function(WEATHER_SCHEMA)
        peircean = report.mappings_by_domain(Domain.PEIRCEAN)
        assert len(peircean) == 3

    def test_synthetic_mappings(self) -> None:
        report = ground_function(WEATHER_SCHEMA)
        synthetic = report.mappings_by_domain(Domain.SYNTHETIC)
        assert len(synthetic) == 2


class TestGroundingSerialization:
    """Verify to_dict serialization."""

    def test_to_dict_structure(self) -> None:
        report = ground_function(WEATHER_SCHEMA)
        d = report.to_dict()
        assert "function_name" in d
        assert "applicable_count" in d
        assert "total_concepts" in d
        assert "coverage_ratio" in d
        assert "mappings" in d
        assert len(d["mappings"]) == 12

    def test_mapping_dict_structure(self) -> None:
        report = ground_function(WEATHER_SCHEMA)
        d = report.to_dict()
        mapping = d["mappings"][0]
        assert "concept" in mapping
        assert "key" in mapping
        assert "domain" in mapping
        assert "applies" in mapping
        assert "anchor" in mapping
        assert "explanation" in mapping
