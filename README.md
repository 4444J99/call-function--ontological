# FUNCTIONcalled()

**A self-documenting naming convention for code, media, and knowledge systems.**

---

## The Problem

Codebases become unnavigable. Files named `utils.js`, `helpers.py`, and `common.ts` proliferate. Developers spend more time *finding* code than *writing* it.

```
src/
├── utils/
│   ├── helpers.js      # What does this help?
│   ├── utils.js        # Utility for what?
│   └── common.js       # Common to whom?
└── components/
    └── Modal.tsx       # Which modal? For what?
```

Search results show filenames stripped of context. Editor tabs become meaningless. New team members take weeks to navigate. The implicit structure of your system remains invisible.

---

## The Approach

**FUNCTIONcalled()** makes names *autological* — self-describing without external lookup.

Every file follows one pattern:

```
{Layer}.{Role}.{Domain}.{Extension}
```

**Four layers** map to how systems naturally organize:

| Layer | Purpose | Languages |
|-------|---------|-----------|
| `core` | Foundation, kernel, primitives | C, C++, Rust, Go |
| `interface` | Portals, surfaces, UI | HTML, CSS, JS, PHP |
| `logic` | Scripts, intelligence, agents | Python, Lua, Ruby |
| `application` | Apps, services, bridges | Swift, Obj-C, Java |

**Examples:**
```
core.router.network.c           # Network routing primitives
interface.modal.confirmation.tsx # Confirmation dialog component
logic.validator.email.py        # Email validation logic
application.app.mobile.swift    # Mobile app entry point
```

Now search for "validator" and find `logic.validator.email.py`. The name tells you: it's logic layer, it validates, it's about email, it's Python.

---

## The Outcome

- **Instant navigation** — Find files by what they *do*, not where they *are*
- **Self-documenting structure** — New developers understand the system from filenames alone
- **Explicit architecture** — The four-layer model surfaces implicit design decisions
- **Universal application** — Works for code, images, audio, documents, any file type

```
project/
├── core/
│   └── core.engine.compute.rs
├── interface/
│   ├── interface.button.primary.tsx
│   └── interface.layout.dashboard.css
├── logic/
│   ├── logic.agent.analysis.py
│   └── logic.validator.email.ts
└── application/
    └── application.app.mobile.swift
```

---

## Quick Start

```bash
# Clone and setup
git clone https://github.com/YOUR_USERNAME/call-function--ontological.git
cd call-function--ontological

# Install dependencies
make install-deps

# Validate your files
make validate-all

# Build the registry
make registry
```

Create a file following the convention:
```bash
# logic/logic.util.string.py
```

Add a metadata sidecar (optional):
```json
{
  "profile": "light",
  "name": "logic.util.string.py",
  "identifier": "urn:uuid:YOUR-UUID",
  "version": "1.0.0"
}
```

See the [Quick Start Guide](docs/quickstart.md) for a complete walkthrough.

---

## Repository Structure

```
├── core/           # Foundation layer templates
├── interface/      # Interface layer templates
├── logic/          # Logic layer templates
├── application/    # Application layer templates
├── examples/       # Canonical naming examples
├── standards/      # Specification and schemas
├── tools/          # Validators and registry builder
├── docs/           # Guides and documentation
└── registry/       # Generated resource catalogue
```

---

## Tooling

```bash
make validate        # Validate metadata sidecars
make validate-naming # Validate file naming
make validate-all    # Run all validators
make registry        # Build resource registry
make hook-install    # Install pre-commit validation
```

---

## Documentation

| Guide | Description |
|-------|-------------|
| [Quick Start](docs/quickstart.md) | Get started in 5 minutes |
| [Full Specification](standards/FUNCTIONcalled_Spec_v1.0.md) | Complete naming rules and rationale |
| [Layer Architecture](docs/layers.md) | Visual guide with dependency rules |
| [Migration Guide](docs/migration.md) | Adopt in existing projects |
| [Comparison](docs/comparison.md) | vs. BEM, Atomic Design, Clean Architecture |
| [Case Study](docs/case-study.md) | Real-world adoption example |

---

## The Symbolic Layer (Optional)

Each layer has an archetypal alias for metaphorical contexts:

| Canonical | Alias | Metaphor |
|-----------|-------|----------|
| `core` | `bones` | Foundation, structure, integrity |
| `interface` | `skins` | Portals, surfaces, aesthetics |
| `logic` | `breath` | Intelligence, spirit, generative power |
| `application` | `body` | Embodiment, lived experience |

Use canonical names for production. Use aliases when the symbolic resonates.

---

## Projects Using FUNCTIONcalled()

*Using FUNCTIONcalled()? [Submit a PR](https://github.com/YOUR_USERNAME/call-function--ontological/pulls) to add your project.*

<!--
- [Project Name](https://github.com/user/repo) - Description
-->

---

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## License

MIT
