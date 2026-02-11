"""Tests for the 12 ontological concepts.

Verifies that all concepts instantiate correctly, have required fields,
belong to valid domains, and pass validation.
"""

from __future__ import annotations

import pytest

from core.ontology import (
    ALL_CONCEPTS,
    CONCEPTS_BY_DOMAIN,
    CONCEPTS_BY_KEY,
    DASEIN,
    EFFICIENT_CAUSE,
    FINAL_CAUSE,
    FORMAL_CAUSE,
    GROUNDING,
    INTERPRETANT,
    MATERIAL_CAUSE,
    OBJECT,
    REPRESENTAMEN,
    TELOS_BRIDGE,
    VORHANDENHEIT,
    ZUHANDENHEIT,
    Domain,
    OntologicalConcept,
)


class TestConceptCount:
    """Verify the complete set of 12 concepts."""

    def test_exactly_twelve_concepts(self) -> None:
        assert len(ALL_CONCEPTS) == 12

    def test_all_keys_unique(self) -> None:
        keys = [c.key for c in ALL_CONCEPTS]
        assert len(keys) == len(set(keys))

    def test_all_names_unique(self) -> None:
        names = [c.name for c in ALL_CONCEPTS]
        assert len(names) == len(set(names))


class TestConceptFields:
    """Verify that every concept has required non-empty fields."""

    @pytest.mark.parametrize("concept", ALL_CONCEPTS, ids=lambda c: c.key)
    def test_has_name(self, concept: OntologicalConcept) -> None:
        assert concept.name
        assert isinstance(concept.name, str)
        assert concept.name.strip() == concept.name

    @pytest.mark.parametrize("concept", ALL_CONCEPTS, ids=lambda c: c.key)
    def test_has_domain(self, concept: OntologicalConcept) -> None:
        assert isinstance(concept.domain, Domain)

    @pytest.mark.parametrize("concept", ALL_CONCEPTS, ids=lambda c: c.key)
    def test_has_description(self, concept: OntologicalConcept) -> None:
        assert concept.description
        assert len(concept.description) > 10  # Non-trivial description.

    @pytest.mark.parametrize("concept", ALL_CONCEPTS, ids=lambda c: c.key)
    def test_has_key(self, concept: OntologicalConcept) -> None:
        assert concept.key
        assert "_" in concept.key or concept.key.isalpha()

    @pytest.mark.parametrize("concept", ALL_CONCEPTS, ids=lambda c: c.key)
    def test_validate_passes(self, concept: OntologicalConcept) -> None:
        assert concept.validate() is True


class TestConceptDomains:
    """Verify domain assignments."""

    def test_aristotelian_count(self) -> None:
        aristotelian = CONCEPTS_BY_DOMAIN[Domain.ARISTOTELIAN]
        assert len(aristotelian) == 4

    def test_heideggerian_count(self) -> None:
        heideggerian = CONCEPTS_BY_DOMAIN[Domain.HEIDEGGERIAN]
        assert len(heideggerian) == 3

    def test_peircean_count(self) -> None:
        peircean = CONCEPTS_BY_DOMAIN[Domain.PEIRCEAN]
        assert len(peircean) == 3

    def test_synthetic_count(self) -> None:
        synthetic = CONCEPTS_BY_DOMAIN[Domain.SYNTHETIC]
        assert len(synthetic) == 2

    def test_material_cause_is_aristotelian(self) -> None:
        assert MATERIAL_CAUSE.domain == Domain.ARISTOTELIAN

    def test_dasein_is_heideggerian(self) -> None:
        assert DASEIN.domain == Domain.HEIDEGGERIAN

    def test_representamen_is_peircean(self) -> None:
        assert REPRESENTAMEN.domain == Domain.PEIRCEAN

    def test_grounding_is_synthetic(self) -> None:
        assert GROUNDING.domain == Domain.SYNTHETIC


class TestConceptSerialization:
    """Verify to_dict serialization."""

    def test_to_dict_has_all_keys(self) -> None:
        d = MATERIAL_CAUSE.to_dict()
        assert "name" in d
        assert "domain" in d
        assert "description" in d
        assert "key" in d

    def test_domain_serialized_as_string(self) -> None:
        d = MATERIAL_CAUSE.to_dict()
        assert isinstance(d["domain"], str)
        assert d["domain"] == "aristotelian"


class TestConceptLookups:
    """Verify lookup dictionaries."""

    def test_by_key_contains_all(self) -> None:
        assert len(CONCEPTS_BY_KEY) == 12

    def test_by_key_lookup(self) -> None:
        assert CONCEPTS_BY_KEY["material_cause"] is MATERIAL_CAUSE
        assert CONCEPTS_BY_KEY["dasein"] is DASEIN
        assert CONCEPTS_BY_KEY["representamen"] is REPRESENTAMEN
        assert CONCEPTS_BY_KEY["telos_bridge"] is TELOS_BRIDGE


class TestConceptValidation:
    """Verify that invalid concepts raise errors."""

    def test_empty_name_raises(self) -> None:
        concept = OntologicalConcept(
            name="", domain=Domain.ARISTOTELIAN, description="test", key="test"
        )
        with pytest.raises(ValueError, match="name"):
            concept.validate()

    def test_empty_description_raises(self) -> None:
        concept = OntologicalConcept(
            name="Test", domain=Domain.ARISTOTELIAN, description="", key="test"
        )
        with pytest.raises(ValueError, match="description"):
            concept.validate()


class TestConceptImmutability:
    """Verify that frozen dataclasses cannot be mutated."""

    def test_cannot_set_name(self) -> None:
        with pytest.raises(AttributeError):
            MATERIAL_CAUSE.name = "Changed"  # type: ignore[misc]

    def test_cannot_set_domain(self) -> None:
        with pytest.raises(AttributeError):
            MATERIAL_CAUSE.domain = Domain.PEIRCEAN  # type: ignore[misc]
