# LLM Prompt for FUNCTIONcalled() Code Generation

Use this prompt when working with AI code generators to ensure they follow the FUNCTIONcalled() naming convention.

## System Prompt Addition

Add this to your system prompt or project instructions:

---

## FUNCTIONcalled() Naming Convention

When creating files in this project, follow the FUNCTIONcalled() naming convention:

**Pattern:** `{Layer}.{Role}.{Domain}.{Extension}`

**Layers:**
- `core` — Foundation, kernel, low-level primitives (C, C++, Rust, Go)
- `interface` — UI, portals, surfaces, APIs (HTML, CSS, JS, PHP)
- `logic` — Scripts, agents, business logic (Python, Lua, Ruby)
- `application` — Apps, services, bridges (Swift, Obj-C, Java)

**Examples:**
```
core.router.network.c        # Network routing in C
interface.button.primary.tsx # Primary button component
logic.validator.email.py     # Email validation logic
application.app.mobile.swift # Mobile app entry point
```

**Rules:**
1. Use lowercase alphanumeric characters
2. Separate segments with dots (.)
3. Use hyphens within segments if needed (e.g., `date-time` not `datetime` for clarity)
4. Place files in the corresponding layer directory (core/, interface/, logic/, application/)

**For new files, always:**
1. Determine the primary layer based on the file's core responsibility
2. Identify the role (what it does) and domain (what context)
3. Name the file following the pattern
4. Add a header comment with Layer/Role/Domain information

**Header comment template:**
```
Layer: {layer} | Role: {role} | Domain: {domain}
Responsibility: {what it does}
Inputs: {inputs}
Outputs: {outputs}
```

---

## Claude Code Specific

For Claude Code, add this to your `CLAUDE.md`:

```markdown
## Naming Convention

Follow the FUNCTIONcalled() naming convention for all new files:

Pattern: `{Layer}.{Role}.{Domain}.{Extension}`

Layers: core, interface, logic, application

Always place files in the appropriate layer directory and include a header comment.
```

## ChatGPT/Custom GPT

For ChatGPT or custom GPTs, add to your instructions:

```
When creating code files for this project, use the FUNCTIONcalled() naming convention:

1. Determine the layer (core/interface/logic/application)
2. Name files as: layer.role.domain.extension
3. Place in the corresponding layer directory
4. Add a header comment documenting layer/role/domain

Example: A Python utility for string manipulation becomes:
- File: logic/logic.util.string.py
- Header: Layer: logic | Role: util | Domain: string
```

## Cursor AI

For Cursor, add to your `.cursorrules`:

```
naming_convention: FUNCTIONcalled
file_pattern: "{layer}.{role}.{domain}.{ext}"
layers:
  core: foundation, kernel, low-level
  interface: UI, portals, APIs
  logic: scripts, agents, business logic
  application: apps, services
require_header_comment: true
```

## Verification Prompt

After generating code, ask:

```
Verify this file follows FUNCTIONcalled():
1. Does the filename match {Layer}.{Role}.{Domain}.{Extension}?
2. Is the layer appropriate for the file's responsibility?
3. Does the header comment include Layer/Role/Domain?
```
