#!/usr/bin/env python3
"""
Tests for validate_meta.py - the metadata sidecar validator.

Run with: python -m pytest tools/test_validate_meta.py -v
"""

import json
import subprocess
import sys
import tempfile
from pathlib import Path

import pytest


SCHEMA_PATH = "standards/FUNCTIONcalled_Metadata_Sidecar.v1.1.schema.json"
VALIDATOR_PATH = "tools/validate_meta.py"


def run_validator(meta_content: dict, schema_path: str = SCHEMA_PATH) -> tuple[int, str, str]:
    """
    Write metadata to a temp file and run the validator.

    Returns:
        (return_code, stdout, stderr)
    """
    with tempfile.NamedTemporaryFile(mode='w', suffix='.meta.json', delete=False) as f:
        json.dump(meta_content, f)
        temp_path = f.name

    try:
        result = subprocess.run(
            [sys.executable, VALIDATOR_PATH, '--schema', schema_path, temp_path],
            capture_output=True,
            text=True
        )
        return result.returncode, result.stdout, result.stderr
    finally:
        Path(temp_path).unlink(missing_ok=True)


class TestLightProfile:
    """Tests for the 'light' metadata profile."""

    def test_valid_light_profile(self):
        """Valid light profile with all required fields."""
        meta = {
            "profile": "light",
            "name": "core.router.network.c",
            "identifier": "urn:uuid:123e4567-e89b-12d3-a456-426614174000",
            "version": "1.0.0"
        }
        returncode, stdout, stderr = run_validator(meta)
        assert returncode == 0, f"Validator failed: {stdout}"
        assert "✅" in stdout

    def test_light_profile_with_optional_fields(self):
        """Light profile with optional fields should also pass."""
        meta = {
            "profile": "light",
            "name": "interface.portal.entry.html",
            "identifier": "urn:uuid:123e4567-e89b-12d3-a456-426614174000",
            "version": "1.0.0",
            "license": "MIT",
            "inLanguage": "en"
        }
        returncode, stdout, stderr = run_validator(meta)
        assert returncode == 0, f"Validator failed: {stdout}"

    def test_light_profile_missing_name(self):
        """Light profile missing 'name' should fail."""
        meta = {
            "profile": "light",
            "identifier": "urn:uuid:123e4567-e89b-12d3-a456-426614174000",
            "version": "1.0.0"
        }
        returncode, stdout, stderr = run_validator(meta)
        assert returncode == 1
        assert "❌" in stdout
        assert "name" in stdout.lower()

    def test_light_profile_missing_identifier(self):
        """Light profile missing 'identifier' should fail."""
        meta = {
            "profile": "light",
            "name": "test.file.ext",
            "version": "1.0.0"
        }
        returncode, stdout, stderr = run_validator(meta)
        assert returncode == 1
        assert "identifier" in stdout.lower()

    def test_light_profile_missing_version(self):
        """Light profile missing 'version' should fail."""
        meta = {
            "profile": "light",
            "name": "test.file.ext",
            "identifier": "urn:uuid:123e4567-e89b-12d3-a456-426614174000"
        }
        returncode, stdout, stderr = run_validator(meta)
        assert returncode == 1
        assert "version" in stdout.lower()


class TestFullProfile:
    """Tests for the 'full' metadata profile."""

    def test_valid_full_profile(self):
        """Valid full profile with all required fields."""
        meta = {
            "profile": "full",
            "name": "logic.agent.analysis.py",
            "identifier": "urn:uuid:123e4567-e89b-12d3-a456-426614174001",
            "version": "0.4.1",
            "schema:type": "SoftwareSourceCode",
            "conformsTo": [
                "https://schema.org/SoftwareSourceCode"
            ],
            "encodingFormat": "text/x-python",
            "dateCreated": "2025-08-18T00:00:00Z",
            "dateModified": "2025-08-18T00:00:00Z"
        }
        returncode, stdout, stderr = run_validator(meta)
        assert returncode == 0, f"Validator failed: {stdout}"
        assert "✅" in stdout

    def test_full_profile_missing_schema_type(self):
        """Full profile missing 'schema:type' should fail."""
        meta = {
            "profile": "full",
            "name": "logic.agent.analysis.py",
            "identifier": "urn:uuid:123e4567-e89b-12d3-a456-426614174001",
            "version": "0.4.1",
            "conformsTo": ["https://schema.org/SoftwareSourceCode"],
            "encodingFormat": "text/x-python",
            "dateCreated": "2025-08-18T00:00:00Z",
            "dateModified": "2025-08-18T00:00:00Z"
        }
        returncode, stdout, stderr = run_validator(meta)
        assert returncode == 1
        assert "schema:type" in stdout

    def test_full_profile_missing_conformsTo(self):
        """Full profile missing 'conformsTo' should fail."""
        meta = {
            "profile": "full",
            "name": "logic.agent.analysis.py",
            "identifier": "urn:uuid:123e4567-e89b-12d3-a456-426614174001",
            "version": "0.4.1",
            "schema:type": "SoftwareSourceCode",
            "encodingFormat": "text/x-python",
            "dateCreated": "2025-08-18T00:00:00Z",
            "dateModified": "2025-08-18T00:00:00Z"
        }
        returncode, stdout, stderr = run_validator(meta)
        assert returncode == 1
        assert "conformsTo" in stdout

    def test_full_profile_missing_dates(self):
        """Full profile missing date fields should fail."""
        meta = {
            "profile": "full",
            "name": "logic.agent.analysis.py",
            "identifier": "urn:uuid:123e4567-e89b-12d3-a456-426614174001",
            "version": "0.4.1",
            "schema:type": "SoftwareSourceCode",
            "conformsTo": ["https://schema.org/SoftwareSourceCode"],
            "encodingFormat": "text/x-python"
        }
        returncode, stdout, stderr = run_validator(meta)
        assert returncode == 1
        assert "dateCreated" in stdout or "dateModified" in stdout


class TestVersionValidation:
    """Tests for semver version string validation."""

    def test_valid_semver_versions(self):
        """Various valid semver versions should pass."""
        valid_versions = [
            "0.0.1",
            "1.0.0",
            "2.1.3",
            "10.20.30",
            "1.0.0-alpha",
            "1.0.0-alpha.1",
            "1.0.0-beta.2",
            "1.0.0-rc.1",
            "1.0.0+build.123",
            "1.0.0-alpha+build.456"
        ]
        for version in valid_versions:
            meta = {
                "profile": "light",
                "name": "test.role.domain.ext",
                "identifier": "urn:uuid:123e4567-e89b-12d3-a456-426614174000",
                "version": version
            }
            returncode, stdout, stderr = run_validator(meta)
            assert returncode == 0, f"Version '{version}' should be valid: {stdout}"

    def test_invalid_semver_versions(self):
        """Invalid semver versions should fail."""
        invalid_versions = [
            "1",
            "1.0",
            "v1.0.0",
            "1.0.0.0",
            "01.0.0",  # Leading zero
            "1.01.0",  # Leading zero
        ]
        for version in invalid_versions:
            meta = {
                "profile": "light",
                "name": "test.role.domain.ext",
                "identifier": "urn:uuid:123e4567-e89b-12d3-a456-426614174000",
                "version": version
            }
            returncode, stdout, stderr = run_validator(meta)
            assert returncode == 1, f"Version '{version}' should be invalid"


class TestSchemaTypes:
    """Tests for schema:type enum validation."""

    def test_valid_schema_types(self):
        """Valid schema:type values should pass."""
        valid_types = [
            "SoftwareSourceCode",
            "SoftwareApplication",
            "CreativeWork",
            "Dataset",
            "ImageObject",
            "AudioObject",
            "VideoObject",
            "TextDigitalDocument",
            "WebPage",
            "Article"
        ]
        for schema_type in valid_types:
            meta = {
                "profile": "full",
                "name": "test.role.domain.ext",
                "identifier": "urn:uuid:123e4567-e89b-12d3-a456-426614174000",
                "version": "1.0.0",
                "schema:type": schema_type,
                "conformsTo": ["https://schema.org/Thing"],
                "encodingFormat": "application/octet-stream",
                "dateCreated": "2025-01-01T00:00:00Z",
                "dateModified": "2025-01-01T00:00:00Z"
            }
            returncode, stdout, stderr = run_validator(meta)
            assert returncode == 0, f"schema:type '{schema_type}' should be valid: {stdout}"

    def test_invalid_schema_type(self):
        """Invalid schema:type should fail."""
        meta = {
            "profile": "full",
            "name": "test.role.domain.ext",
            "identifier": "urn:uuid:123e4567-e89b-12d3-a456-426614174000",
            "version": "1.0.0",
            "schema:type": "InvalidType",
            "conformsTo": ["https://schema.org/Thing"],
            "encodingFormat": "application/octet-stream",
            "dateCreated": "2025-01-01T00:00:00Z",
            "dateModified": "2025-01-01T00:00:00Z"
        }
        returncode, stdout, stderr = run_validator(meta)
        assert returncode == 1
        assert "schema:type" in stdout


class TestProfileValidation:
    """Tests for profile field validation."""

    def test_invalid_profile(self):
        """Invalid profile value should fail."""
        meta = {
            "profile": "invalid",
            "name": "test.role.domain.ext",
            "identifier": "urn:uuid:123e4567-e89b-12d3-a456-426614174000",
            "version": "1.0.0"
        }
        returncode, stdout, stderr = run_validator(meta)
        assert returncode == 1
        assert "profile" in stdout.lower()

    def test_missing_profile(self):
        """Missing profile field should fail."""
        meta = {
            "name": "test.role.domain.ext",
            "identifier": "urn:uuid:123e4567-e89b-12d3-a456-426614174000",
            "version": "1.0.0"
        }
        returncode, stdout, stderr = run_validator(meta)
        assert returncode == 1
        assert "profile" in stdout.lower()


class TestEdgeCases:
    """Edge case tests."""

    def test_empty_object(self):
        """Empty JSON object should fail."""
        meta = {}
        returncode, stdout, stderr = run_validator(meta)
        assert returncode == 1

    def test_additional_properties_allowed(self):
        """Additional properties should be allowed (additionalProperties: true)."""
        meta = {
            "profile": "light",
            "name": "test.role.domain.ext",
            "identifier": "urn:uuid:123e4567-e89b-12d3-a456-426614174000",
            "version": "1.0.0",
            "customField": "custom value",
            "anotherCustom": 123
        }
        returncode, stdout, stderr = run_validator(meta)
        assert returncode == 0, f"Additional properties should be allowed: {stdout}"

    def test_creator_as_string(self):
        """Creator can be a single string."""
        meta = {
            "profile": "light",
            "name": "test.role.domain.ext",
            "identifier": "urn:uuid:123e4567-e89b-12d3-a456-426614174000",
            "version": "1.0.0",
            "creator": "Single Author"
        }
        returncode, stdout, stderr = run_validator(meta)
        assert returncode == 0

    def test_creator_as_array(self):
        """Creator can be an array of strings."""
        meta = {
            "profile": "light",
            "name": "test.role.domain.ext",
            "identifier": "urn:uuid:123e4567-e89b-12d3-a456-426614174000",
            "version": "1.0.0",
            "creator": ["Author One", "Author Two"]
        }
        returncode, stdout, stderr = run_validator(meta)
        assert returncode == 0

    def test_dc_subject_as_string(self):
        """dc:subject can be a single string."""
        meta = {
            "profile": "light",
            "name": "test.role.domain.ext",
            "identifier": "urn:uuid:123e4567-e89b-12d3-a456-426614174000",
            "version": "1.0.0",
            "dc:subject": "single-subject"
        }
        returncode, stdout, stderr = run_validator(meta)
        assert returncode == 0

    def test_dc_subject_as_array(self):
        """dc:subject can be an array of strings."""
        meta = {
            "profile": "light",
            "name": "test.role.domain.ext",
            "identifier": "urn:uuid:123e4567-e89b-12d3-a456-426614174000",
            "version": "1.0.0",
            "dc:subject": ["subject-one", "subject-two"]
        }
        returncode, stdout, stderr = run_validator(meta)
        assert returncode == 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
