# Contributing to FUNCTIONcalled()

Thank you for your interest in contributing to the FUNCTIONcalled() naming convention project.

## How to Contribute

### Reporting Issues

- Use GitHub Issues to report bugs or suggest enhancements
- Check existing issues before creating a new one
- Provide clear reproduction steps for bugs

### Submitting Pull Requests

1. Fork the repository
2. Create a feature branch from `main`
3. Make your changes following the conventions below
4. Run all validators before committing
5. Submit a pull request with a clear description

## Development Setup

```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/call-function--ontological.git
cd call-function--ontological

# Create virtual environment
python -m venv .venv
source .venv/bin/activate

# Install dependencies
make install-deps

# Install pre-commit hook
make hook-install
```

## Coding Standards

### File Naming

All files in layer directories must follow the FUNCTIONcalled() naming convention:

```
{Layer}.{Role}.{Domain}.{Extension}
```

Layers: `core`, `interface`, `logic`, `application` (or aliases: `bones`, `skins`, `breath`, `body`)

### Metadata Sidecars

When adding new tracked files, create a companion `.meta.json` sidecar:

```json
{
  "profile": "light",
  "name": "layer.role.domain.ext",
  "identifier": "urn:uuid:YOUR-UUID-HERE",
  "version": "1.0.0"
}
```

### Commit Messages

Follow the commit message format from the spec:

```
[layer:role] action — scope
```

Examples:
- `[logic:agent] add caching — inference`
- `[interface:portal] fix layout — mobile`
- `[core:router] refactor — network`

## Testing

Before submitting a PR, ensure all validators pass:

```bash
# Run all validators
make validate-all

# Run tests
source .venv/bin/activate
python -m pytest tools/
```

## Questions?

Open an issue for any questions about contributing.
