# FUNCTIONcalled() Specification v1.0

## 0. Purpose
FUNCTIONcalled() defines a universal, self-documenting naming and structuring convention.  
It ensures that every element is named by what it is and what it does — across code, media, or knowledge systems.

## 1. Core Principle
> **Names must be autological (self-descriptive).**  
A name contains its own purpose, role, and context, so that no external lookup is required.

## 2. Naming Syntax
```
{Layer}.{Role}.{Domain}.{Extension}
```
- **Layer** → the archetypal tier the object belongs to  
  - `bones` = core / foundation / kernel  
  - `skins` = interface / portal / surface  
  - `breath` = logic / script / intelligence  
  - `body` = application / embodiment  
- **Role** → the explicit function of the element (e.g. `router`, `layout`, `agent`, `app`)  
- **Domain** → the subsystem, feature, or context (e.g. `network`, `archive`, `engine`, `user`)  
- **Extension** → the file type (`.c`, `.py`, `.html`, `.json`, `.png`, `.pdf`, etc.)

Optional fields:  
- **Target** (platform) → e.g. `web`, `cli`, `ios`, `android`  
- **Version** → `.vNN` (applied when format requires explicit versioning)

## 3. Examples
```
bones.router.network.c
skins.layout.dashboard.css
skins.portal.entry.html
breath.agent.analysis.py
breath.script.runtime.lua
body.app.mobile.swift
body.bridge.legacy.m
```

## 4. Folder Structure Convention
```
system/
├─ bones/
│  ├─ router/
│  │  └─ bones.router.network.c
│  └─ engine/
│     └─ bones.engine.core.rs
├─ skins/
│  ├─ layout/
│  │  └─ skins.layout.dashboard.css
│  └─ portal/
│     └─ skins.portal.entry.html
├─ breath/
│  ├─ agent/
│  │  └─ breath.agent.analysis.py
│  └─ script/
│     └─ breath.script.runtime.lua
└─ body/
   ├─ mobile/
   │  └─ body.app.mobile.swift
   └─ legacy/
      └─ body.bridge.legacy.m
```

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

