# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This repository implements the **FUNCTIONcalled()** naming and metadata convention — a system for self-documenting file names and metadata sidecars. The core principle is that names should be **autological** (self-descriptive), containing their purpose, role, and context without requiring external lookup.

## Naming Convention

**Repository names:** Use `call-{name}--{descriptor}` format
- Single hyphen (`-`) separates words within a segment
- Double hyphen (`--`) separates the function name from its descriptor

**File names:** Pattern `{Layer}.{Role}.{Domain}.{Extension}`
- Versions must follow semver format (e.g., `1.0.0`, `2.1.3-beta.1`)

## Commands

```bash
# Install dependencies
make install-deps          # Installs jsonschema + semgrep

# Validate metadata files
make validate              # Validates *.meta.json against the schema

# Validate file naming conventions
make validate-naming       # Checks files follow {Layer}.{Role}.{Domain}.{ext}

# Run semgrep rules
make semgrep               # Validates header comments structure

# Run ALL validators
make validate-all          # Runs validate + validate-naming + semgrep

# Build the registry
make registry              # Scans for .meta.json files, outputs registry/registry.json

# Install pre-commit hook
make hook-install          # Runs all validators on git commit
```

To validate specific files directly:
```bash
python tools/validate_meta.py path/to/file.meta.json
python tools/validate_naming.py path/to/file.ext
```

## Architecture

### Layer System

Files follow the naming pattern `{Layer}.{Role}.{Domain}.{Extension}`. The four canonical layers are:

| Layer | Alias | Purpose | Languages |
|-------|-------|---------|-----------|
| `core` | `bones` | Foundation, kernel, structure | C, C++, Rust, Go |
| `interface` | `skins` | Portals, surfaces, UI | HTML, CSS, JS, PHP |
| `logic` | `breath` | Scripts, intelligence, agents | Python, Lua, Ruby |
| `application` | `body` | Embodiment, apps, bridges | Swift, Obj-C, Java |

Each layer directory contains starter `template.*` files with header comments describing the role.

### Metadata Sidecar Pattern

Any file can have a companion metadata sidecar named `{filename}.meta.json`. The schema supports two profiles:

- **light**: Minimal required fields (`profile`, `name`, `identifier`, `version`)
- **full**: Extended fields including `schema:type`, `conformsTo`, `encodingFormat`, `dateCreated`, `dateModified`

Schema: `standards/FUNCTIONcalled_Metadata_Sidecar.v1.1.schema.json`

### Registry

The registry builder (`tools/registry-builder.py`) walks the repo, finds all `.meta.json` files, and generates `registry/registry.json` — a catalog of all tracked resources with paths and optional SHA256 hashes.

## Commit Message Format

```
[layer:role] action — scope
```

Example: `[breath:agent] improve inference — caching`
