# FUNCTIONcalled() Repo Scaffold

This repository implements the FUNCTIONcalled() naming and metadata conventions.

## Structure

- **standards/**: specifications and schemas
- **tools/**: validators and registry builder scripts
- **examples/**: canonical metadata examples
- **registry/**: generated catalogues
- **core**, **interface**, **logic**, **application**: base layers for your project
- **archive/**: place for frozen history or old versions

## Naming Convention

Files follow the pattern: `{Layer}.{Role}.{Domain}.{Extension}`

**Repository name convention:**
- Use `call-{name}--{descriptor}` for repos following FUNCTIONcalled conventions
- Single hyphen (`-`) separates words within a segment
- Double hyphen (`--`) separates the function name from its descriptor

**Layers** (canonical | alias):
| Layer | Alias | Purpose |
|-------|-------|---------|
| `core` | `bones` | Foundation, kernel, structure |
| `interface` | `skins` | Portals, surfaces, UI |
| `logic` | `breath` | Scripts, intelligence, agents |
| `application` | `body` | Embodiment, apps, bridges |

**Version format:** Semantic versioning (e.g., `1.0.0`, `2.1.3-beta.1+build.456`)

## Installation

```bash
# Install all dependencies (jsonschema + semgrep)
make install-deps

# Or install individually
pip install jsonschema semgrep
```

## Usage

```bash
# Validate metadata sidecar files (.meta.json)
make validate

# Validate file naming conventions
make validate-naming

# Run semgrep rules for header comments
make semgrep

# Run ALL validators
make validate-all

# Build the registry
make registry

# Install pre-commit hook (runs all validators)
make hook-install
```

See `standards/FUNCTIONcalled_Spec_v1.0.md` for the full specification and `standards/FUNCTIONcalled_Metadata_Sidecar.v1.1.schema.json` for the metadata schema.

## Schema.org Integration

The metadata schema supports these Schema.org types for `schema:type`:
- `SoftwareSourceCode`, `SoftwareApplication`
- `CreativeWork`, `Dataset`, `Article`, `WebPage`
- `ImageObject`, `AudioObject`, `VideoObject`
- `TextDigitalDocument`

The `conformsTo` field accepts URI references to standards.

## Rosetta Stone Codex

Below is a mapping of file types to their roles and use-cases across the four layers:

| File Type | Technical Role | Symbolic Role | Use Case |
|-----------|---------------|--------------|---------|
| .c   | OS kernels, low-level logic | Stone tablets | Core patchbay engine |
| .cpp | Game engines, OOP systems | Forge/Craft | Narrative game engine |
| .css | Styling (web) | Vestments | Shrine visuals |
| .go  | Concurrent backend services | Messengers | APIs & sync |
| .html | Web structure | Temple/Portal | Ritual interfaces |
| .java | Android apps | Duality | Shrine apps (Android) |
| .js   | Frontend logic | Trickster/Magician | Transmutater / Shrine interactivity |
| .lua  | Lightweight scripts | Spirit/Breath | Embedded scripts |
| .m    | Legacy Apple hooks | Ancestor/Roots | Low-level Apple rituals |
| .php  | Server/CMS | Scribes/Archivists | Forum backend |
| .py   | AI/ML & scripts | Oracle/Seer | AI & storytelling |
| .rb   | Dynamic scripting | Alchemist | Generative hubs |
| .rs   | Secure concurrency | Guardian | Integrity engine |
| .swift| iOS apps | Phoenix | Shrine AR apps |

### Meta Pattern

- Systems languages (C, C++, Rust, Go) = Bones & blood vessels of the OS
- Web stack (HTML, CSS, JS, PHP) = Skins & portals
- Scripting & AI (Python, Lua, Ruby) = Breath & spirit
- Mobile (Swift, Obj-C, Java) = Embodiment in the physical hand-held world

## Projects Using FUNCTIONcalled()

*Is your project using FUNCTIONcalled()? [Submit a PR](https://github.com/YOUR_USERNAME/call-function--ontological/pulls) to add it here!*

<!-- Example format:
- [Project Name](https://github.com/user/repo) - Brief description
-->

## Documentation

- [Quick Start Guide](docs/quickstart.md) - Get started in 5 minutes
- [Full Specification](standards/FUNCTIONcalled_Spec_v1.0.md) - Complete naming spec
- [Layer Architecture](docs/layers.md) - Visual guide to the four layers
- [Migration Guide](docs/migration.md) - Adopt FUNCTIONcalled() in existing projects
- [Comparison](docs/comparison.md) - How it compares to BEM, Atomic Design, etc.
- [Case Study](docs/case-study.md) - Real-world adoption example

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines on how to contribute.

## License

MIT

