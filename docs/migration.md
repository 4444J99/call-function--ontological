# Migration Guide

How to adopt FUNCTIONcalled() in existing projects.

## Overview

FUNCTIONcalled() can be adopted incrementally. You don't need to rename everything at once.

## Strategy 1: New Files Only

Start by applying the convention to new files while leaving existing code unchanged.

**Approach:**
1. Configure your IDE/editor to suggest FUNCTIONcalled() names for new files
2. Use the naming validator in "warn" mode for existing files
3. Update CONTRIBUTING.md to require the convention for new code

**Pros:** Zero disruption, gradual adoption
**Cons:** Inconsistent codebase during transition

## Strategy 2: Rename on Touch

Rename files when you modify them for other reasons.

**Approach:**
1. When you open a file to fix a bug or add a feature, rename it
2. Update all imports/references in the same commit
3. Track progress with the naming validator

**Example commit message:**
```
[logic:util] rename helpers.py → logic.util.string.py

- Adopt FUNCTIONcalled naming convention
- Update imports in 3 files
```

**Pros:** Natural, spreads work over time
**Cons:** Slower adoption, requires discipline

## Strategy 3: Batch Migration

Dedicate time to rename groups of related files.

**Approach:**
1. Identify a module or feature to migrate
2. Create a mapping of old names → new names
3. Use automated refactoring tools
4. Validate and test thoroughly

**Tools that help:**
```bash
# Find files that don't match the convention
python tools/validate_naming.py --root src/

# Use your IDE's refactoring tools for safe renames
# VS Code: F2 on file in explorer
# JetBrains: Shift+F6
```

## Mapping Existing Structures

### Common Patterns

| Existing Pattern | FUNCTIONcalled Equivalent |
|------------------|---------------------------|
| `src/utils/helpers.py` | `logic/logic.util.helpers.py` |
| `components/Button.tsx` | `interface/interface.component.button.tsx` |
| `lib/auth.js` | `logic/logic.service.auth.js` |
| `app/main.swift` | `application/application.app.main.swift` |
| `kernel/memory.c` | `core/core.kernel.memory.c` |

### Framework-Specific Guidance

**React/Next.js:**
```
pages/           → interface/
components/      → interface/
lib/             → logic/
utils/           → logic/
```

**Django:**
```
models.py        → core/ or logic/ (depending on complexity)
views.py         → interface/
services/        → logic/
management/      → application/
```

**iOS (Swift):**
```
ViewControllers/ → application/
Views/           → interface/
Models/          → core/
Services/        → logic/
```

## Creating Metadata Sidecars

For tracked files, create metadata incrementally:

```bash
# Generate a template sidecar
cat > myfile.ext.meta.json << 'EOF'
{
  "profile": "light",
  "name": "layer.role.domain.ext",
  "identifier": "urn:uuid:$(uuidgen)",
  "version": "1.0.0"
}
EOF
```

Or use the VS Code snippets in `.vscode/functioncalled.code-snippets`.

## Validation During Migration

Run validators to track progress:

```bash
# See which files need migration
make validate-naming 2>&1 | grep "❌"

# Count remaining non-compliant files
make validate-naming 2>&1 | grep -c "❌"
```

## CI Integration

Add gradual enforcement to CI:

```yaml
# .github/workflows/validate.yml
- name: Validate naming (warn only)
  run: make validate-naming || true  # Don't fail build yet

- name: Validate metadata (strict)
  run: make validate  # Fail on invalid metadata
```

As migration progresses, switch to strict mode:

```yaml
- name: Validate naming (strict)
  run: make validate-naming  # Now fails on non-compliant files
```

## Measuring Progress

Track adoption metrics:

```bash
# Total files in layer directories
find core interface logic application -type f | wc -l

# Compliant files (passes validator)
# Run validator and count successes

# Percentage adopted
# compliant / total * 100
```

## Common Challenges

### "We have too many files to rename"

Start small. Pick one module. Prove the value. Expand gradually.

### "Our framework requires specific names"

Apply FUNCTIONcalled() where you have control. Document exceptions. Use the convention for the Domain segment even when Layer/Role are constrained.

### "Renames break git history"

Use `git mv` for renames. Git is good at tracking file moves. Consider using `git log --follow` to see full history.

### "Team members are resistant"

Focus on new code first. Let the benefits speak for themselves. A single well-named file in search results is a powerful example.
