[![ORGAN-I: Theoria](https://img.shields.io/badge/ORGAN--I-Theoria-311b92?style=flat-square)](https://github.com/organvm-i-theoria)
[![Python](https://img.shields.io/badge/python-3.x-blue?style=flat-square)]()
[![Tests](https://img.shields.io/badge/tests-85%2B%20passing-brightgreen?style=flat-square)]()
[![License](https://img.shields.io/badge/license-MIT-blue?style=flat-square)](LICENSE)

# FUNCTIONcalled()

**A universal, self-documenting naming convention for files across codebases, media archives, and knowledge systems.**

Every file follows a single canonical pattern: `{Layer}.{Role}.{Domain}.{Extension}`. Four layers — core, interface, logic, application — map to symbolic categories that make filenames *autological*: a file's name tells you what it is, where it lives in the architecture, and why it exists.

This is not a style guide. It is an ontological claim: **naming is architecture**. A file that cannot declare its own role in a system is a file that will be misplaced, misunderstood, or forgotten. FUNCTIONcalled() gives every artifact in a project a coordinate system — a way to locate itself in relation to everything else.

---

## Table of Contents

- [Theoretical Purpose](#theoretical-purpose)
- [The Four-Layer Ontology](#the-four-layer-ontology)
- [Technical Architecture](#technical-architecture)
- [The Formal Specification](#the-formal-specification)
- [Validation Toolchain](#validation-toolchain)
- [Metadata Sidecar System](#metadata-sidecar-system)
- [Registry and Content Hashing](#registry-and-content-hashing)
- [Documentation Ecosystem](#documentation-ecosystem)
- [LLM Integration](#llm-integration)
- [Installation and Quick Start](#installation-and-quick-start)
- [CI/CD Pipeline](#cicd-pipeline)
- [Migration Strategies](#migration-strategies)
- [Comparison with Existing Conventions](#comparison-with-existing-conventions)
- [Cross-Organ Context](#cross-organ-context)
- [Project Status](#project-status)
- [Related Work](#related-work)
- [Contributing](#contributing)
- [License and Author](#license-and-author)

---

## Theoretical Purpose

Every codebase develops a naming problem. Files accumulate. Folders nest without principle. `utils.py` proliferates. Six months later, the person who wrote the code cannot explain the structure to a newcomer — or to themselves.

Existing approaches — BEM for CSS, Atomic Design for UI components, Clean Architecture for dependency layers, Domain-Driven Design for business boundaries — each solve one slice of the problem within one domain. None of them provide a **cross-domain, cross-language, cross-media** naming grammar that works for a Python module, a MIDI file, a design token, and a blog post with equal precision.

FUNCTIONcalled() starts from a different premise. Instead of organizing files by technology or framework convention, it organizes them by **ontological role** — what a file *is* in the system, independent of what language it happens to be written in. The philosophical claim is precise: if a name cannot encode its own structural position, then the naming system has failed its most basic responsibility. A file named `core.validator.naming.py` declares itself as a foundational validation component in the naming domain — before you open it, before you read a docstring, before you check a README.

This places FUNCTIONcalled() squarely within ORGAN-I's epistemological concerns. ORGAN-I (Theoria) is the theory layer of the organvm system — the organ responsible for epistemology, recursion, and ontology. The question "how should we name things?" is not a style preference; it is a question about how knowledge is structured, retrieved, and transmitted. A naming convention that carries structural information *in the name itself* is a naming convention that treats every filename as a proposition about the system's architecture. The convention is autological: it names the act of naming as a first-class architectural decision.

The result is a naming convention that:

- Works across programming languages, media types, and documentation formats
- Makes directory structures self-documenting without requiring external maps or wikis
- Enables machine validation (regex, JSON Schema, semgrep) alongside human readability
- Scales from a single-developer project to a multi-organ institutional system
- Bridges from project-internal naming into the linked data ecosystem via Schema.org types

The formal specification, validation tools, and metadata system in this repository are the reference implementation of that premise.

## The Four-Layer Ontology

The naming convention is built on four canonical layers. Each layer carries a symbolic metaphor that anchors its purpose beyond any single technology:

| Layer | Canonical | Alias | Role | Typical Languages |
|-------|-----------|-------|------|-------------------|
| **Core** | `core` | `bones` | Foundational structures, system-level primitives, compiled artifacts | C, C++, Rust, Go |
| **Interface** | `interface` | `skins` | Surfaces that users touch — markup, styling, client-side interaction | HTML, CSS, JavaScript, PHP |
| **Logic** | `logic` | `breath` | Scripted reasoning, glue code, orchestration, dynamic behavior | Python, Lua, Ruby |
| **Application** | `application` | `body` | Assembled programs, platform-specific builds, deliverable executables | Java, Objective-C, Swift |

These are not arbitrary groupings. They reflect a philosophical taxonomy rooted in how systems naturally organize:

- **Bones** are what persists when everything else is stripped away. Every system needs a foundation: the low-level primitives that everything else builds upon. These rarely change and must be stable.
- **Skins** are what the world sees. Systems need boundaries where they meet users or other systems. Interfaces are the surfaces that translate between internal and external.
- **Breath** is what animates. Between foundation and interface lies the intelligence: decision-making, processing, transformation. This is where complexity lives.
- **Body** is the assembled whole. Systems must be embodied in runnable form: apps, services, executables that bring everything together.

The layer system is deliberately language-suggestive rather than language-prescriptive. A Python file that performs low-level binary parsing might legitimately belong to the core layer. A Rust file that serves as a CLI entry point might belong to the application layer. The symbolic mapping provides the default; the developer's judgment provides the override.

### Symbolic Worldviews

The four-layer metaphor is transposable across different symbolic systems, documented in the Rosetta Codex (`docs/rosetta-codex.md`):

| Layer | Organism | Machine | Temple | Cosmos |
|-------|----------|---------|--------|--------|
| Core | Bones | Engine | Foundation | Earth |
| Interface | Skin | Shell | Portal | Air |
| Logic | Breath | Program | Ritual | Fire |
| Application | Body | Vehicle | Shrine | Water |

Choose the worldview that resonates with your project's character. The convention works identically regardless of which metaphor you adopt.

### Layer Dependencies

Layers follow a strict dependency hierarchy — no back-edges permitted:

| Layer | Can Depend On |
|-------|---------------|
| Core | (none) |
| Logic | Core |
| Interface | Core, Logic |
| Application | Core, Logic, Interface |

This mirrors the no-back-edge invariant enforced across the organvm system: flow is directional. Core is the foundation; Application sits at the top. A core module that depends on an interface component is a structural violation, not a style preference.

The full layer taxonomy, including Mermaid diagrams showing inter-layer relationships and data flow patterns, is documented in `docs/layers.md`.

## Technical Architecture

The repository contains 82 files (~60KB) organized into six functional areas:

```
call-function--ontological/
├── standards/
│   ├── FUNCTIONcalled_Spec_v1.0.md          # Formal specification (9 sections)
│   ├── FUNCTIONcalled_Metadata_Sidecar.v1.1.schema.json  # JSON Schema (Draft 2020-12)
│   ├── registry.schema.json                  # Registry output schema
│   └── registry.example.json                 # Example registry structure
├── tools/
│   ├── validate_naming.py                    # Regex-based filename validator
│   ├── validate_meta.py                      # JSON Schema metadata validator
│   ├── registry-builder.py                   # Registry builder (SHA256 hashes)
│   ├── llm-prompt.md                         # LLM integration templates
│   ├── semgrep/functioncalled.yaml           # 4 semgrep rules for header comments
│   ├── test_validate_naming.py               # 60+ naming validation tests
│   └── test_validate_meta.py                 # 25+ metadata validation tests
├── core/                                     # Layer templates: C, C++, Rust, Go
│   ├── template.{c,cpp,rs,go}
│   └── template.{c,cpp,rs,go}.meta.json
├── interface/                                # Layer templates: HTML, CSS, JS, PHP
│   ├── template.{html,css,js,php}
│   └── template.{html,css,js,php}.meta.json
├── logic/                                    # Layer templates: Python, Lua, Ruby
│   ├── template.{py,lua,rb}
│   └── template.{py,lua,rb}.meta.json
├── application/                              # Layer templates: Java, Obj-C, Swift
│   ├── template.{java,m,swift}
│   └── template.{java,m,swift}.meta.json
├── examples/                                 # Fully annotated reference examples
│   ├── interface.portal.entry.html           # HTML portal with sidecar
│   ├── interface.icon.brand.svg              # SVG asset with sidecar
│   ├── logic.agent.analysis.py               # Python agent with sidecar
│   └── logic.audio.notification.txt          # Audio reference with sidecar
├── registry/
│   └── registry.json                         # 18 tracked resources with SHA256 hashes
├── docs/
│   ├── quickstart.md                         # 5-minute onboarding
│   ├── layers.md                             # Layer taxonomy + Mermaid diagrams
│   ├── rosetta-codex.md                      # 14 file types x 4 worldviews
│   ├── migration.md                          # 3 adoption strategies
│   ├── comparison.md                         # vs BEM, Atomic, Clean, DDD
│   └── case-study.md                         # Applied naming walkthrough
├── .github/workflows/validate.yml            # CI pipeline (push + PR)
├── Makefile                                  # 7 make targets for validation
├── CHANGELOG.md                              # Semantic versioning history
├── CONTRIBUTING.md                           # Contribution guidelines
└── CODE_OF_CONDUCT.md                        # Community standards
```

Each of the four layer directories contains starter template files with header comments describing the role for that language, paired with `.meta.json` sidecar files that provide machine-readable metadata. The `examples/` directory contains fully annotated reference implementations showing the convention applied to real file types — an HTML portal, an SVG brand icon, a Python analysis agent, and an audio notification reference.

## The Formal Specification

`standards/FUNCTIONcalled_Spec_v1.0.md` is the canonical document. Its nine sections define the complete convention:

1. **Core Principle and Naming Syntax** — the `{Layer}.{Role}.{Domain}.{Extension}` grammar, EBNF-style production rules, and the autological principle ("names must be self-descriptive")
2. **Layer Names** — canonical names (`core`, `interface`, `logic`, `application`) with accepted aliases (`bones`, `skins`, `breath`, `body`); canonical names take precedence in production systems
3. **Role and Domain** — explicit function and subsystem segments; naming rules (lowercase alphanumeric, hyphens within segments, dots between segments)
4. **Cross-Layer Files** — guidelines for files that serve multiple layers; preference for logic layer for shared utilities; prohibition on a "shared" or "common" layer
5. **Folder Structure Convention** — canonical directory layout keyed to layers, with both canonical and alias variants
6. **Commit Message Template** — structured format `[layer:role] action — scope` for version control consistency
7. **Inline Header Comment Template** — required comment blocks at the top of every file declaring Layer, Role, Domain, Responsibility, Inputs, Outputs, and Invariants
8. **Symbolic Metaphor Layer** — the bones/skins/breath/body mapping and transposable worldviews (organism, machine, temple, cosmos)
9. **Scope and FAQ** — where the convention applies (code, media, documentation, collections), how to handle test files, framework constraints, and team adoption

Every other artifact in the repository — tools, templates, tests, documentation — derives from this specification. The spec itself follows semantic versioning, with backward compatibility guarantees for the naming grammar.

## Validation Toolchain

The convention is enforced, not merely suggested. Three validation mechanisms operate at different levels of the development workflow:

### Filename Validation (`validate_naming.py`)

A regex-based filename checker that parses the `{Layer}.{Role}.{Domain}.{Extension}` pattern and verifies each segment against the specification's allowed values. Key capabilities:

- **Glob pattern support** for batch validation across entire directory trees
- **Alias normalization** — automatically resolves `bones` to `core`, `skins` to `interface`, etc.
- **Configurable exclusions** — dotfiles, READMEs, Makefiles, schema files, and framework-required names are excluded by default
- **Directory-level exclusions** — `.git`, `tools`, `standards`, `registry`, `archive`, and `docs` directories are skipped
- **Verbose mode** for auditing skipped files alongside validated ones

Tested by 60+ unit tests covering valid names, edge cases (multi-segment roles, alias layers, optional prefixes), malformed inputs, and boundary conditions.

```bash
# Validate all files in a directory
python tools/validate_naming.py --root path/to/your/project/

# Validate specific files
python tools/validate_naming.py path/to/logic.agent.analysis.py

# Verbose output (show skipped and valid files)
python tools/validate_naming.py --root . -v
```

### Metadata Validation (`validate_meta.py`)

A JSON Schema validator for `.meta.json` sidecar files using `jsonschema` with Draft 2020-12 support. Validates both light (4-field) and full (9-field) metadata profiles, checking:

- **Profile-conditional required fields** — light profile requires `profile`, `name`, `identifier`, `version`; full profile additionally requires `schema:type`, `conformsTo`, `encodingFormat`, `dateCreated`, `dateModified`
- **Semantic version format** — version strings must match semver pattern including pre-release and build metadata
- **Schema.org type enumeration** — `schema:type` must be one of ten valid Schema.org types
- **URI format validation** — `conformsTo` entries must be valid URIs

Tested by 25+ unit tests covering schema compliance, missing fields, type mismatches, and optional field handling.

```bash
# Validate specific sidecar files
python tools/validate_meta.py path/to/file.meta.json

# Validate with custom schema location
python tools/validate_meta.py --schema standards/FUNCTIONcalled_Metadata_Sidecar.v1.1.schema.json file.meta.json
```

### Semgrep Rules (`tools/semgrep/functioncalled.yaml`)

Four custom semgrep rules that validate inline header comments in source files across 13 languages (Python, C, C++, JavaScript, TypeScript, Go, Rust, Java, Ruby, Lua, PHP, HTML, Swift):

| Rule | Severity | Purpose |
|------|----------|---------|
| `functioncalled-header-comment` | INFO | Detects and confirms valid FUNCTIONcalled header comments |
| `functioncalled-missing-layer` | WARNING | Catches headers with Role but missing Layer declaration |
| `functioncalled-incomplete-header` | WARNING | Catches headers with Layer but missing Role or Domain |
| `functioncalled-invalid-layer` | WARNING | Catches non-canonical layer names (not core/interface/logic/application or their aliases) |

These rules catch the gap between naming compliance and documentation compliance — files that have correct names but missing or malformed header declarations.

All three validators run in CI via GitHub Actions on every push and pull request. A failing name or metadata check blocks merge.

## Metadata Sidecar System

FUNCTIONcalled() treats filenames as the primary self-documentation mechanism, but filenames have limits. They cannot carry provenance, authorship, creation dates, or semantic type information without becoming unwieldy.

The metadata sidecar system solves this by pairing files with companion `.meta.json` documents. A file named `logic.agent.analysis.py` has a sidecar `logic.agent.analysis.py.meta.json` that carries structured metadata *without modifying the original file*.

Two profiles are defined, governed by the JSON Schema at `standards/FUNCTIONcalled_Metadata_Sidecar.v1.1.schema.json`:

| Profile | Required Fields | Use Case |
|---------|----------------|----------|
| **Light** | `profile`, `name`, `identifier`, `version` | Minimal annotation for quick adoption |
| **Full** | Light fields + `schema:type`, `conformsTo`, `encodingFormat`, `dateCreated`, `dateModified` | Complete provenance for registries and knowledge systems |

### Schema.org Bridge

The `schema:type` field supports ten Schema.org types: `SoftwareSourceCode`, `SoftwareApplication`, `CreativeWork`, `Dataset`, `ImageObject`, `AudioObject`, `VideoObject`, `TextDigitalDocument`, `WebPage`, and `Article`. This bridges from project-internal naming into the linked data ecosystem. A sidecar with `"schema:type": "SoftwareSourceCode"` is a file that knows what it is in both the FUNCTIONcalled() ontology and the broader web of structured data.

Additional optional fields include `creator`, `dc:subject` (Dublin Core subject), `programmingLanguage`, `license`, and `inLanguage` — enabling rich metadata without requiring changes to the source files themselves.

### Example: Light Profile Sidecar

```json
{
  "profile": "light",
  "name": "logic.agent.analysis.py",
  "identifier": "urn:uuid:a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "version": "1.0.0"
}
```

### Example: Full Profile Sidecar

```json
{
  "profile": "full",
  "name": "interface.portal.entry.html",
  "identifier": "urn:uuid:f9e8d7c6-b5a4-3210-fedc-ba0987654321",
  "version": "1.0.0",
  "schema:type": "WebPage",
  "conformsTo": ["https://github.com/organvm-i-theoria/call-function--ontological"],
  "encodingFormat": "text/html",
  "dateCreated": "2025-08-18T00:00:00Z",
  "dateModified": "2025-08-18T00:00:00Z"
}
```

## Registry and Content Hashing

The **Registry Builder** (`tools/registry-builder.py`) scans all `.meta.json` files in the repository, computes SHA256 content hashes for each paired source file, and outputs `registry/registry.json` — a single manifest of every tracked resource in the project.

The current registry tracks 18 resources across all four layers plus the examples directory. Each entry records the resource name, file path, metadata sidecar path, and SHA256 hash:

```json
{
  "resources": [
    {
      "name": "logic.agent.analysis.py",
      "path": "examples/logic.agent.analysis.py",
      "meta": "examples/logic.agent.analysis.py.meta.json",
      "hash": "0e7695fedf864378ec33f92da41815fb..."
    }
  ]
}
```

The registry serves as the project's internal source of truth for tracked artifacts, analogous to `registry-v2.json` at the organvm system level. The SHA256 hashes enable integrity verification — detecting unauthorized modifications, ensuring reproducibility, and providing audit trails for content that participates in cross-organ workflows.

The registry is rebuilt automatically on every CI run, ensuring it stays synchronized with the actual file state.

## Documentation Ecosystem

Six guides accompany the specification, each targeting a different reader and use case:

| Guide | Audience | Content |
|-------|----------|---------|
| **Quickstart** (`docs/quickstart.md`) | New adopters | 5-minute path from zero to first named file — create, annotate, validate, register |
| **Layers** (`docs/layers.md`) | Architects | Deep dive into the four-layer taxonomy with Mermaid relationship diagrams and data flow patterns |
| **Rosetta Codex** (`docs/rosetta-codex.md`) | Polyglot developers | 14 file types mapped across all four layers — shows how the same conceptual role manifests in C, Python, HTML, Swift, and 10 other languages |
| **Migration** (`docs/migration.md`) | Teams with existing projects | Three adoption strategies: new-files-only (zero disruption), rename-on-touch (gradual), batch migration (systematic) |
| **Comparison** (`docs/comparison.md`) | Evaluators | FUNCTIONcalled() vs BEM, Atomic Design, Clean Architecture, and Domain-Driven Design — with hybrid approach examples |
| **Case Study** (`docs/case-study.md`) | Portfolio reviewers | Applied walkthrough showing a 400-file codebase migrated over 6 months, with quantitative before/after metrics |

The Rosetta Codex in particular deserves attention. It maps 14 programming languages to both their technical roles and their symbolic roles within the four-layer system: C as "stone tablets" (core), Python as "oracle/seer" (logic), HTML as "temple/portal" (interface), Swift as "phoenix" (application). This is not mere decoration — it provides mnemonic anchors that help developers internalize the layer system through metaphorical reasoning rather than rote memorization.

## LLM Integration

FUNCTIONcalled() includes integration templates for three major AI coding assistants, enabling LLMs to generate convention-compliant file names and metadata sidecars from natural language descriptions:

- **Claude Code** — `CLAUDE.md` system prompt additions with Makefile targets and layer reference
- **ChatGPT / Custom GPTs** — instruction block format with naming verification prompt
- **Cursor AI** — `.cursorrules` YAML configuration for automated naming enforcement

The LLM prompt template (`tools/llm-prompt.md`) provides a reusable system prompt addition that teaches any LLM the naming pattern, the four layers, the header comment format, and a self-verification checklist. This closes the loop: the convention is enforced by validators for human-written code and by prompt engineering for AI-generated code.

## Installation and Quick Start

**Prerequisites:** Python 3.x, pip

```bash
# Clone the repository
git clone https://github.com/organvm-i-theoria/call-function--ontological.git
cd call-function--ontological

# Install validation dependencies
make install-deps
# Or manually: pip install jsonschema pytest semgrep

# Run the full test suite (85+ tests)
python -m pytest tools/ -v

# Validate filenames in a directory
python tools/validate_naming.py --root path/to/your/project/

# Validate metadata sidecars
python tools/validate_meta.py path/to/your/project/*.meta.json

# Run all validators (naming + metadata + semgrep)
make validate-all

# Build the content registry
make registry
```

### Create Your First FUNCTIONcalled() File

```bash
# 1. Create a Python utility with proper naming
mkdir -p logic
cat > logic/logic.util.string.py << 'PYEOF'
"""
Layer: logic | Role: util | Domain: string
Responsibility: String manipulation utilities
Inputs: Raw string values
Outputs: Transformed strings
"""

def capitalize_words(text: str) -> str:
    """Capitalize each word in the input text."""
    return ' '.join(word.capitalize() for word in text.split())

def snake_to_title(text: str) -> str:
    """Convert snake_case to Title Case."""
    return ' '.join(word.capitalize() for word in text.split('_'))
PYEOF

# 2. Create a metadata sidecar
cat > logic/logic.util.string.py.meta.json << 'JSONEOF'
{
  "profile": "light",
  "name": "logic.util.string.py",
  "identifier": "urn:uuid:REPLACE-WITH-UUIDGEN-OUTPUT",
  "version": "1.0.0"
}
JSONEOF

# 3. Validate both
python tools/validate_naming.py logic/logic.util.string.py
python tools/validate_meta.py logic/logic.util.string.py.meta.json

# 4. Rebuild the registry to include your new file
make registry
```

### Makefile Targets

The Makefile provides seven targets for common operations:

| Target | Command | Purpose |
|--------|---------|---------|
| `validate` | `make validate` | Validate all `.meta.json` files against JSON Schema |
| `validate-naming` | `make validate-naming` | Check all files follow `{Layer}.{Role}.{Domain}.{ext}` |
| `semgrep` | `make semgrep` | Validate header comments with 4 semgrep rules |
| `validate-all` | `make validate-all` | Run all three validators sequentially |
| `registry` | `make registry` | Rebuild `registry/registry.json` with SHA256 hashes |
| `hook-install` | `make hook-install` | Install pre-commit hook running all validators |
| `install-deps` | `make install-deps` | Install `jsonschema` and `semgrep` via pip |

## CI/CD Pipeline

The GitHub Actions workflow (`.github/workflows/validate.yml`) runs on every push to `main` and every pull request targeting `main`:

1. **Environment Setup** — Python 3.11, pip cache for fast dependency installation
2. **Metadata Validation** — `make validate` checks all `.meta.json` sidecars against JSON Schema
3. **Naming Validation** — `make validate-naming` checks all tracked files against the naming grammar
4. **Test Suite** — `pytest tools/ -v` runs all 85+ unit tests for both validators
5. **Registry Build** — `make registry` regenerates `registry/registry.json` with current SHA256 hashes
6. **Artifact Upload** — the built registry is uploaded as a GitHub Actions artifact (5-day retention)

This pipeline ensures that the naming convention is not a suggestion that erodes over time, but a structural invariant enforced on every change. A failing name or metadata check blocks merge, preventing convention drift.

The pre-commit hook (installed via `make hook-install`) provides the same validation locally, catching issues before they reach CI. It validates staged `.meta.json` files, checks staged file names, and runs semgrep rules if semgrep is installed.

## Migration Strategies

FUNCTIONcalled() can be adopted incrementally. The migration guide (`docs/migration.md`) documents three strategies:

### Strategy 1: New Files Only

Apply the convention only to new files while leaving existing code unchanged. Zero disruption, gradual adoption. Configure your IDE to suggest FUNCTIONcalled() names for new files and update `CONTRIBUTING.md` to require the convention going forward.

### Strategy 2: Rename on Touch

Rename files when you modify them for other reasons. When you open a file to fix a bug or add a feature, rename it following the convention and update all imports in the same commit. Natural adoption that spreads work over time.

### Strategy 3: Batch Migration

Dedicate time to rename groups of related files systematically. Create a mapping of old names to new names, use IDE refactoring tools for safe renames, and validate thoroughly. The case study documents a 400-file codebase migrated over 6 months using a combination of all three strategies.

### Common Mappings

| Existing Pattern | FUNCTIONcalled() Equivalent |
|------------------|-----------------------------|
| `src/utils/helpers.py` | `logic/logic.util.helpers.py` |
| `components/Button.tsx` | `interface/interface.component.button.tsx` |
| `lib/auth.js` | `logic/logic.service.auth.js` |
| `app/main.swift` | `application/application.app.main.swift` |
| `kernel/memory.c` | `core/core.kernel.memory.c` |

Framework-specific guidance is provided for React/Next.js, Django, and iOS (Swift) projects.

## Comparison with Existing Conventions

FUNCTIONcalled() occupies a unique position in the naming convention landscape. The comparison guide (`docs/comparison.md`) provides detailed analysis against four established approaches:

| Approach | Focus | Scope | Self-Describing | Coexists with FC? |
|----------|-------|-------|-----------------|-------------------|
| **FUNCTIONcalled()** | File names + structure | Full project | Yes | — |
| **BEM** | CSS class names | Styling only | Partial | Yes |
| **Atomic Design** | Component hierarchy | UI components | Partial | Yes |
| **Clean Architecture** | Dependency layers | Code organization | No | Yes |
| **Domain-Driven Design** | Business domains | System design | Partial | Yes |

The key differentiator: FUNCTIONcalled() is the only convention that operates at the file-name level and works across all file types — code, media, documentation, and data assets. Every other approach is either domain-specific (BEM for CSS), scope-limited (Atomic for UI), or folder-based (Clean Architecture). FUNCTIONcalled() makes the file name itself the carrier of structural information.

All four approaches can coexist with FUNCTIONcalled(). Use BEM for CSS class names inside FUNCTIONcalled()-named CSS files. Use Atomic Design's component hierarchy as the Role segment. Use Clean Architecture's dependency layers as folder structure while FUNCTIONcalled() names the files. Use DDD's bounded contexts as Domain segments.

## Cross-Organ Context

This repository is part of **ORGAN-I (Theoria)** within the [organvm system](https://github.com/organvm-i-theoria) — the epistemological and ontological foundation layer. FUNCTIONcalled() addresses a core ORGAN-I concern: how do we name things such that the names themselves carry structural knowledge?

Within the eight-organ architecture:

| Organ | Domain | Relationship to FUNCTIONcalled() |
|-------|--------|----------------------------------|
| **I — Theoria** | Theory, epistemology, ontology | **Home organ.** FUNCTIONcalled() is a theory of naming as architecture. |
| **II — Poiesis** | Art, generative work | Creative assets (images, audio, 3D) benefit from cross-media naming grammar. |
| **III — Ergon** | Commerce, SaaS products | Production codebases can adopt the convention for cross-language consistency. |
| **IV — Taxis** | Orchestration, governance | The registry system mirrors ORGAN-IV's concern with tracking and routing. |
| **V — Logos** | Public process, essays | Documentation files can carry FUNCTIONcalled() names and metadata sidecars. |

The naming convention's layer dependency rule (core cannot depend on interface; flow is directional) mirrors the organvm system's invariant that ORGAN-III cannot depend on ORGAN-II. Both express the same principle: architectural layering requires strict directional flow.

The Rosetta Codex's mapping of 14 file types to symbolic roles (C as "stone tablets," Python as "oracle/seer") reflects ORGAN-I's broader project of making technical structures legible through ontological and symbolic frameworks. The convention does not merely organize files; it proposes a theory of how files *relate to each other* across languages, media types, and institutional boundaries.

## Project Status

| Attribute | Value |
|-----------|-------|
| **Version** | 1.0.0 |
| **Files** | 82 |
| **Size** | ~60KB |
| **Tests** | 85+ passing |
| **Registry Entries** | 18 tracked resources |
| **Supported Languages** | 14 (C, C++, Rust, Go, HTML, CSS, JS, PHP, Python, Lua, Ruby, Java, Obj-C, Swift) |
| **Semgrep Rules** | 4 (header comment validation) |
| **Documentation Guides** | 6 (quickstart, layers, rosetta codex, migration, comparison, case study) |
| **CI** | GitHub Actions (push + PR) |
| **Documentation Status** | DEPLOYED |

## Related Work

- **[recursive-engine](https://github.com/organvm-i-theoria/recursive-engine)** — ORGAN-I's flagship repository; recursive computation framework that shares FUNCTIONcalled()'s concern with self-referential structure
- **[agentic-titan](https://github.com/organvm-iv-taxis/agentic-titan)** — ORGAN-IV orchestration system; the registry pattern in FUNCTIONcalled() anticipates the kind of artifact tracking that orchestration systems require
- **[Schema.org](https://schema.org)** — The linked data vocabulary that FUNCTIONcalled() bridges to via the `schema:type` field in metadata sidecars
- **[JSON Schema Draft 2020-12](https://json-schema.org/draft/2020-12/json-schema-core)** — The validation standard used for metadata sidecar schemas
- **[Semgrep](https://semgrep.dev)** — The static analysis engine used for header comment validation rules

## Contributing

Contributions are welcome. See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

Key areas for contribution:

- **New layer templates** — starter files for additional languages within the four canonical layers
- **Semgrep rules** — additional static analysis rules for convention compliance
- **Migration tooling** — automated rename scripts for popular frameworks
- **Documentation** — case studies, framework-specific adoption guides, additional Rosetta Codex entries
- **IDE integrations** — plugins or snippets for VS Code, JetBrains, Vim/Neovim

All contributions should follow the FUNCTIONcalled() naming convention and include appropriate metadata sidecars. The commit message format is `[layer:role] action — scope`.

## License and Author

MIT License. See [LICENSE](LICENSE) for details.

Created and maintained by [@4444J99](https://github.com/4444J99).

---

<sub>Part of the [ORGAN-I: Theoria](https://github.com/organvm-i-theoria) system — epistemology, recursion, ontology.</sub>
