# Quick Start Guide

Get started with FUNCTIONcalled() in 5 minutes.

## 1. Understand the Pattern

Every file follows this naming convention:

```
{Layer}.{Role}.{Domain}.{Extension}
```

**Layers:**
- `core` — foundation, kernel, low-level
- `interface` — UI, portals, surfaces
- `logic` — scripts, agents, intelligence
- `application` — apps, services, bridges

## 2. Create Your First File

Let's create a simple Python utility:

```bash
# Create the file with proper naming
touch logic/logic.util.string.py
```

Add content:

```python
# logic/logic.util.string.py
"""
Layer: logic | Role: util | Domain: string
Responsibility: String manipulation utilities
"""

def capitalize_words(text: str) -> str:
    return ' '.join(word.capitalize() for word in text.split())
```

## 3. Add Metadata (Optional)

Create a sidecar file `logic.util.string.py.meta.json`:

```json
{
  "profile": "light",
  "name": "logic.util.string.py",
  "identifier": "urn:uuid:YOUR-UUID-HERE",
  "version": "1.0.0"
}
```

Generate a UUID: `python -c "import uuid; print(uuid.uuid4())"`

## 4. Validate Your Work

```bash
# Install dependencies (first time only)
make install-deps

# Validate all metadata files
make validate

# Validate naming conventions
make validate-naming

# Run everything
make validate-all
```

## 5. Build the Registry

```bash
make registry
cat registry/registry.json
```

Your file should now appear in the registry!

## Next Steps

- Read the [full specification](../standards/FUNCTIONcalled_Spec_v1.0.md)
- See [migration guide](migration.md) for existing projects
- Check [CONTRIBUTING.md](../CONTRIBUTING.md) for contribution guidelines
