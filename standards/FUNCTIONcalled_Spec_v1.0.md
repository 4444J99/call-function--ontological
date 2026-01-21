# FUNCTIONcalled() Specification v1.0

## 0. Purpose
FUNCTIONcalled() defines a universal, self-documenting naming and structuring convention.  
It ensures that every element is named by what it is and what it does — across code, media, or knowledge systems.

## 1. Core Principle
> **Names must be autological (self-descriptive).**
A name contains its own purpose, role, and context, so that no external lookup is required.

### 1.1 Why Four Layers?

The four-layer model emerges from observing how systems naturally organize:

1. **Core** — Every system needs a foundation: the low-level primitives that everything else builds upon. These rarely change and must be stable.

2. **Interface** — Systems need boundaries where they meet users or other systems. Interfaces are the "surfaces" that translate between internal and external.

3. **Logic** — Between foundation and interface lies the intelligence: decision-making, processing, transformation. This is where complexity lives.

4. **Application** — Finally, systems must be embodied in runnable form: apps, services, executables that bring everything together.

This is not prescriptive but descriptive — most software naturally falls into these categories. The naming convention makes this implicit structure explicit.

## 2. Naming Syntax
```
{Layer}.{Role}.{Domain}.{Extension}
```

### 2.1 Layer Names

**Canonical names** (preferred):

| Canonical | Alias | Purpose | Typical Languages |
|-----------|-------|---------|-------------------|
| `core` | `bones` | Foundation, kernel, structure | C, C++, Rust, Go |
| `interface` | `skins` | Portals, surfaces, UI | HTML, CSS, JS, PHP |
| `logic` | `breath` | Scripts, intelligence, agents | Python, Lua, Ruby |
| `application` | `body` | Embodiment, apps, bridges | Swift, Obj-C, Java |

> **Precedence**: Canonical names take precedence. Aliases are accepted for symbolic/metaphorical contexts but canonical names should be used in production systems.

### 2.2 Role and Domain

- **Role** → the explicit function of the element (e.g. `router`, `layout`, `agent`, `app`)
- **Domain** → the subsystem, feature, or context (e.g. `network`, `archive`, `engine`, `user`)
- **Extension** → the file type (`.c`, `.py`, `.html`, `.json`, `.png`, `.pdf`, etc.)

**Naming rules**:
- Use lowercase alphanumeric characters
- Use hyphens (`-`) within a segment if needed (avoid dots within Role/Domain)
- Role and Domain can have multiple segments separated by dots for sub-categorization

### 2.3 Cross-Layer Files

Some files serve multiple layers (e.g., a utility used by both logic and interface). Guidelines:

- **Choose the primary layer** based on where the file's core responsibility lies
- **Prefer logic layer** for shared utilities, as it represents "intelligence" that can be consumed by others
- **Avoid creating a "shared" or "common" layer** — this defeats the purpose of explicit categorization
- If a file truly spans layers, consider splitting it into layer-specific modules

Optional fields:
- **Target** (platform) → e.g. `web`, `cli`, `ios`, `android`
- **Version** → `.vNN` (applied when format requires explicit versioning)

## 3. Examples

### Canonical naming (preferred)
```
core.router.network.c
interface.layout.dashboard.css
interface.portal.entry.html
logic.agent.analysis.py
logic.script.runtime.lua
application.app.mobile.swift
application.bridge.legacy.m
```

### Alias naming (symbolic/metaphorical contexts)
```
bones.router.network.c
skins.layout.dashboard.css
breath.agent.analysis.py
body.app.mobile.swift
```

## 4. Folder Structure Convention

### Using canonical layer names (recommended)
```
project/
├─ core/
│  ├─ router/
│  │  └─ core.router.network.c
│  └─ engine/
│     └─ core.engine.compute.rs
├─ interface/
│  ├─ layout/
│  │  └─ interface.layout.dashboard.css
│  └─ portal/
│     └─ interface.portal.entry.html
├─ logic/
│  ├─ agent/
│  │  └─ logic.agent.analysis.py
│  └─ script/
│     └─ logic.script.runtime.lua
└─ application/
   ├─ mobile/
   │  └─ application.app.mobile.swift
   └─ legacy/
      └─ application.bridge.legacy.m
```

### Using alias layer names (alternative)
```
project/
├─ bones/       # equivalent to core/
├─ skins/       # equivalent to interface/
├─ breath/      # equivalent to logic/
└─ body/        # equivalent to application/
```

> **Note**: Choose one naming style (canonical or alias) and use it consistently within a project.

## 5. Commit Message Template
Format: `[layer:role] action — scope`

Example: `[breath:agent] improve inference — caching`

## 6. Inline Header Comment Template
```
Layer: {layer} | Role: {role} | Domain: {domain}
Responsibility: {what it does}
Inputs: {inputs}
Outputs: {outputs}
Invariants: {rules/constraints}
```

## 7. Symbolic Metaphor (Optional)
The four layers correspond to archetypal metaphors:
- **Bones** = foundation, structure, integrity  
- **Skins** = portals, interfaces, aesthetics  
- **Breath** = intelligence, logic, generative power  
- **Body** = application, embodiment, lived experience

These metaphors can be swapped (machine, temple, organism, cosmos) depending on context.

## 8. Scope of Application
FUNCTIONcalled() is extensible across:
- Codebases (multi-language, multi-platform)
- Media archives (images, audio, video, 3D assets)
- Knowledge systems (papers, notes, schemas)
- Collections & museums (artifacts, taxonomy)

## 9. Frequently Asked Questions

### Why not just use folders for organization?

Folders provide hierarchy but lose context when files are viewed in isolation (search results, editor tabs, logs). FUNCTIONcalled() names are self-contained — you know what a file is just from its name.

### How do I handle files that don't fit the four layers?

First, reconsider whether the file truly doesn't fit. Most code falls into one of the four categories when you identify its primary responsibility. If it genuinely doesn't fit, you can:
- Place it in `logic/` as a utility
- Create a project-specific extension layer (document it clearly)

### What about test files?

Test files mirror the structure of what they test:
- `logic.agent.analysis.test.py` tests `logic.agent.analysis.py`
- Place tests alongside source files or in a parallel `tests/` directory

### Can I use this with existing projects?

Yes. FUNCTIONcalled() can be adopted incrementally:
1. Start with new files
2. Rename files as you modify them
3. Use the naming validator to track progress

### What if my team disagrees on which layer a file belongs to?

This is valuable — the disagreement reveals ambiguity in the code's purpose. Use the discussion to clarify the file's responsibility. If consensus is impossible, the file may need to be split.

### How does this work with frameworks that enforce their own structure?

Adapt FUNCTIONcalled() to work within framework constraints:
- Use the convention for files you control
- Document framework-mandated exceptions
- Apply the naming to the "Domain" segment even if Layer/Role are constrained

