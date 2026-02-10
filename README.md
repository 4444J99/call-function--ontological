[![ORGAN-I: Theory](https://img.shields.io/badge/ORGAN--I-Theory-1a237e?style=flat-square)](https://github.com/organvm-i-theoria)
[![Python](https://img.shields.io/badge/python-3.x-blue?style=flat-square)]()
[![Tests](https://img.shields.io/badge/tests-85%2B%20passing-brightgreen?style=flat-square)]()
[![License](https://img.shields.io/badge/license-MIT-blue?style=flat-square)](LICENSE)

# FUNCTIONcalled()

**A universal, self-documenting naming convention for files across codebases, media archives, and knowledge systems.**

Every file follows a single canonical pattern: `{Layer}.{Role}.{Domain}.{Extension}`. Four layers — core, interface, logic, application — map to symbolic categories that make filenames *autological*: a file's name tells you what it is, where it lives in the architecture, and why it exists.

This is not a style guide. It is an ontological claim: **naming is architecture**. A file that cannot declare its own role in a system is a file that will be misplaced, misunderstood, or forgotten. FUNCTIONcalled() gives every artifact in a project a coordinate system — a way to locate itself in relation to everything else.

---

## Table of Contents

- [Motivation](#motivation)
- [The Four-Layer Ontology](#the-four-layer-ontology)
- [Architecture](#architecture)
- [Validation Toolchain](#validation-toolchain)
- [Metadata Sidecar System](#metadata-sidecar-system)
- [Documentation](#documentation)
- [Getting Started](#getting-started)
- [Integration & CI/CD](#integration--cicd)
- [Project Status](#project-status)
- [License & Author](#license--author)

---

## Motivation

Every codebase develops a naming problem. Files accumulate. Folders nest without principle. `utils.py` proliferates. Six months later, the person who wrote the code cannot explain the structure to a newcomer — or to themselves.

Existing approaches (BEM for CSS, Atomic Design for components, Clean Architecture for layers, Domain-Driven Design for boundaries) each solve one slice of the problem within one domain. None of them provide a **cross-domain, cross-language, cross-media** naming grammar that works for a Python module, a MIDI file, a design token, and a blog post with equal precision.

FUNCTIONcalled() starts from a different premise. Instead of organizing files by technology or framework convention, it organizes them by **ontological role** — what a file *is* in the system, independent of what language it happens to be written in. The result is a naming convention that:

- Works across programming languages, media types, and documentation formats
- Makes directory structures self-documenting without requiring external maps
- Enables machine validation (regex, JSON Schema, semgrep) alongside human readability
- Scales from a single-developer project to a multi-organ institutional system

The formal specification, validation tools, and metadata system in this repository are the reference implementation of that premise.

## The Four-Layer Ontology

The naming convention is built on four canonical layers. Each layer carries a symbolic metaphor that anchors its purpose beyond any single technology:

| Layer | Symbolic Name | Role | Typical Languages |
|-------|--------------|------|-------------------|
| **Core** | Bones | Foundational structures, system-level primitives, compiled artifacts | C, C++, Rust, Go |
| **Interface** | Skins | Surfaces that users touch — markup, styling, client-side interaction | HTML, CSS, JavaScript, PHP |
| **Logic** | Breath | Scripted reasoning, glue code, orchestration, dynamic behavior | Python, Lua, Ruby |
| **Application** | Body | Assembled programs, platform-specific builds, deliverable executables | Java, Objective-C, Swift |

These are not arbitrary groupings. They reflect a philosophical taxonomy: **bones** are what persists when everything else is stripped away; **skins** are what the world sees; **breath** is what animates; **body** is the assembled whole. A file named `core.validator.naming.py` declares itself as a foundational validation component in the naming domain — before you open it, before you read a docstring, before you check a README.

The layer system is deliberately language-suggestive rather than language-prescriptive. A Python file that performs low-level binary parsing might legitimately belong to the core layer. A Rust file that serves as a CLI entry point might belong to the application layer. The symbolic mapping provides the default; the developer's judgment provides the override.

The full layer taxonomy, including Mermaid diagrams showing inter-layer relationships, is documented in `docs/layers.md`. The Rosetta Codex (`docs/rosetta-codex.md`) maps 14 specific file types across all four layers, showing how the same conceptual role manifests in different technological contexts.

## Architecture

The repository contains 82 files (~53KB) organized into five functional areas:

```
call-function--ontological/
├── standards/
│   └── FUNCTIONcalled_Spec_v1.0.md    # Formal specification (9 sections)
├── tools/
│   ├── validate_naming.py              # Regex-based filename validator
│   ├── validate_meta.py                # JSON Schema metadata validator
│   └── build_registry.py              # Registry builder (SHA256 hashes)
├── templates/
│   ├── core/                          # C, C++, Rust, Go templates
│   ├── interface/                     # HTML, CSS, JS, PHP templates
│   ├── logic/                         # Python, Lua, Ruby templates
│   └── application/                   # Java, ObjC, Swift templates
├── registry/
│   └── registry.json                  # 18 tracked resources with hashes
├── docs/
│   ├── quickstart.md                  # 5-minute onboarding
│   ├── layers.md                      # Layer taxonomy + Mermaid diagrams
│   ├── rosetta-codex.md               # 14 file types × 4 worldviews
│   ├── migration.md                   # 3 adoption strategies
│   ├── comparison.md                  # vs BEM, Atomic, Clean, DDD
│   └── case-study.md                  # Applied naming walkthrough
├── tests/
│   ├── test_validate_naming.py        # 60+ naming validation tests
│   └── test_validate_meta.py          # 25+ metadata validation tests
├── prompts/                           # LLM integration templates
│   ├── claude.md
│   ├── chatgpt.md
│   └── cursor.md
└── .github/
    └── workflows/                     # CI pipeline (naming + meta + pytest)
```

### The Formal Specification

`standards/FUNCTIONcalled_Spec_v1.0.md` is the canonical document. Its nine sections define:

1. **Naming Syntax** — the `{Layer}.{Role}.{Domain}.{Extension}` grammar with EBNF-style production rules
2. **Folder Structure** — canonical directory layout keyed to layers
3. **Commit Message Templates** — structured commit formats that reference layer and domain
4. **Inline Header Comments** — required comment blocks at the top of every file declaring layer, role, and domain
5. **Symbolic Metaphor Layer** — the bones/skins/breath/body mapping and its rationale
6. **Scope of Application** — where the convention applies (code, media, documentation) and where it does not
7. **Versioning** — how the spec itself evolves (semantic versioning, backward compatibility guarantees)
8. **Extension Points** — how to add new layers or roles without breaking existing names
9. **Glossary** — precise definitions of all terms used in the specification

Every other artifact in the repository — tools, templates, tests, documentation — derives from this specification.

## Validation Toolchain

The convention is enforced, not merely suggested. Three validation mechanisms operate at different levels:

**`validate_naming.py`** — A regex-based filename checker that parses the `{Layer}.{Role}.{Domain}.{Extension}` pattern and verifies each segment against the specification's allowed values. Supports glob patterns for batch validation across entire directory trees. Tested by 60+ unit tests covering valid names, edge cases, malformed inputs, and boundary conditions.

**`validate_meta.py`** — A JSON Schema validator for `.meta.json` sidecar files (see below). Uses `jsonschema` with Draft 2020-12 support to validate both light (4-field) and full (9-field) metadata profiles. Tested by 25+ unit tests covering schema compliance, missing fields, type mismatches, and optional field handling.

**Semgrep Rules** — Four custom semgrep rules that validate inline header comments in source files. These catch files that have correct names but missing or malformed header declarations — the gap between naming compliance and documentation compliance.

All three validators run in CI via GitHub Actions on every push and pull request. A failing name or metadata check blocks merge.

## Metadata Sidecar System

FUNCTIONcalled() treats filenames as the primary self-documentation mechanism, but filenames have limits. They cannot carry provenance, authorship, creation dates, or semantic type information without becoming unwieldy.

The metadata sidecar system solves this by pairing files with companion `.meta.json` documents. A file named `core.validator.naming.py` may have a sidecar `core.validator.naming.py.meta.json` that carries structured metadata *without modifying the original file*.

Two profiles are defined:

| Profile | Fields | Use Case |
|---------|--------|----------|
| **Light** | layer, role, domain, description | Minimal annotation for quick adoption |
| **Full** | Light fields + author, created, version, schema_type, tags | Complete provenance for registries and knowledge systems |

The `schema_type` field supports [Schema.org](https://schema.org) types, enabling metadata to bridge from project-internal naming into the linked data ecosystem. A sidecar with `"schema_type": "SoftwareSourceCode"` is a file that knows what it is in both the FUNCTIONcalled() ontology and the broader web of structured data.

The **Registry Builder** (`tools/build_registry.py`) scans all `.meta.json` files, computes SHA256 content hashes, and outputs `registry/registry.json` — a single manifest of every tracked resource in the project. The current registry tracks 18 resources.

## Documentation

Six guides accompany the specification, each targeting a different reader:

| Guide | Audience | Content |
|-------|----------|---------|
| **Quickstart** (`docs/quickstart.md`) | New adopters | 5-minute path from zero to first named file |
| **Layers** (`docs/layers.md`) | Architects | Deep dive into the four-layer taxonomy with Mermaid relationship diagrams |
| **Rosetta Codex** (`docs/rosetta-codex.md`) | Polyglot developers | 14 file types mapped across all four layers — shows how the same role manifests in different languages |
| **Migration** (`docs/migration.md`) | Teams with existing projects | Three adoption strategies: greenfield, incremental rename, parallel convention |
| **Comparison** (`docs/comparison.md`) | Evaluators | FUNCTIONcalled() vs BEM, Atomic Design, Clean Architecture, and Domain-Driven Design |
| **Case Study** (`docs/case-study.md`) | Portfolio reviewers | Applied walkthrough showing the convention in a real project structure |

Additionally, LLM prompt templates in `prompts/` provide integration points for Claude, ChatGPT, and Cursor — enabling AI coding assistants to generate FUNCTIONcalled()-compliant file names and metadata sidecars from natural language descriptions.

## Getting Started

**Prerequisites:** Python 3.x, pip

```bash
# Clone the repository
git clone https://github.com/organvm-i-theoria/call-function--ontological.git
cd call-function--ontological

# Install validation dependencies
pip install jsonschema pytest

# Run the full test suite
pytest tests/ -v

# Validate filenames in a directory
python tools/validate_naming.py path/to/your/project/

# Validate metadata sidecars
python tools/validate_meta.py path/to/your/project/
```

To adopt the convention in an existing project, start with `docs/quickstart.md` for the 5-minute path, or `docs/migration.md` for a structured adoption strategy. The specification itself (`standards/FUNCTIONcalled_Spec_v1.0.md`) is the authoritative reference for all naming rules.

## Integration & CI/CD

The GitHub Actions workflow (`.github/workflows/`) runs on every push and pull request:

1. **Naming Validation** — `validate_naming.py` checks all tracked files against the naming grammar
2. **Metadata Validation** — `validate_meta.py` checks all `.meta.json` sidecars against JSON Schema (Draft 2020-12)
3. **Header Comment Validation** — Semgrep rules verify inline header declarations
4. **Test Suite** — pytest runs all 85+ tests
5. **Registry Build** — `build_registry.py` regenerates `registry/registry.json` with current SHA256 hashes

This pipeline ensures that the naming convention is not a suggestion that erodes over time, but a structural invariant enforced on every change.

## Project Status

| Attribute | Value |
|-----------|-------|
| **Version** | 1.0.0 |
| **Files** | 82 |
| **Size** | ~53KB |
| **Tests** | 85+ passing |
| **Registry Entries** | 18 tracked resources |
| **CI** | GitHub Actions (push + PR) |
| **Documentation Status** | DEPLOYED |

This repository is part of **ORGAN-I (Theory)** within the [organvm system](https://github.com/organvm-i-theoria) — the epistemological and ontological foundation layer. FUNCTIONcalled() addresses a core ORGAN-I concern: how do we name things such that the names themselves carry structural knowledge? The answer is a formal specification, a validation toolchain, and a metadata system that together make naming a first-class architectural decision.

## License & Author

MIT License. See [LICENSE](LICENSE) for details.

Created and maintained by [@4444J99](https://github.com/4444J99).

---

<sub>Part of the [ORGAN-I: Theory](https://github.com/organvm-i-theoria) system — epistemology, recursion, ontology.</sub>
