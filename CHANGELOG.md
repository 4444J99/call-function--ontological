# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Validator test suites for `validate_meta.py` and `validate_naming.py`
- Template metadata sidecars for all layer templates
- Source files for example metadata sidecars
- Clarified canonical vs alias layer naming in spec

### Changed
- Renamed example files to follow strict `{Layer}.{Role}.{Domain}.{ext}` convention
- Updated spec §2, §3, §4 to prioritize canonical layer names over aliases

## [1.0.0] - 2025-08-18

### Added
- Initial FUNCTIONcalled() specification v1.0
- Four-layer system: core, interface, logic, application
- Metadata sidecar schema (light and full profiles)
- Validation tools: `validate_meta.py`, `validate_naming.py`
- Registry builder: `registry-builder.py`
- Semgrep rules for header comment validation
- Template files for each layer
- Makefile with validation targets
