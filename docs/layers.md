# Layer Architecture

Visual guide to the FUNCTIONcalled() four-layer system.

## Layer Diagram

```mermaid
flowchart TB
    subgraph APPLICATION["APPLICATION (body)"]
        direction LR
        A1[Apps]
        A2[Services]
        A3[Bridges]
    end

    subgraph INTERFACE["INTERFACE (skins)"]
        direction LR
        I1[UI Components]
        I2[Portals]
        I3[APIs]
    end

    subgraph LOGIC["LOGIC (breath)"]
        direction LR
        L1[Agents]
        L2[Scripts]
        L3[Processors]
    end

    subgraph CORE["CORE (bones)"]
        direction LR
        C1[Kernel]
        C2[Primitives]
        C3[Runtime]
    end

    APPLICATION --> INTERFACE
    APPLICATION --> LOGIC
    INTERFACE --> LOGIC
    LOGIC --> CORE
    INTERFACE --> CORE

    style CORE fill:#e8d4b8,stroke:#8b7355
    style LOGIC fill:#b8d4e8,stroke:#557b8b
    style INTERFACE fill:#d4e8b8,stroke:#7b8b55
    style APPLICATION fill:#e8b8d4,stroke:#8b5577
```

## Layer Descriptions

### Core (bones)
**Languages:** C, C++, Rust, Go

The foundation layer. Code here is:
- Low-level and performance-critical
- Rarely changed once stable
- Depended upon by all other layers

**Examples:**
- `core.router.network.c` — Network routing primitives
- `core.engine.compute.rs` — Compute engine kernel

---

### Interface (skins)
**Languages:** HTML, CSS, JavaScript, PHP

The boundary layer. Code here:
- Translates between internal and external
- Handles user interaction
- Defines API surfaces

**Examples:**
- `interface.portal.entry.html` — Main entry portal
- `interface.layout.dashboard.css` — Dashboard styling

---

### Logic (breath)
**Languages:** Python, Lua, Ruby

The intelligence layer. Code here:
- Processes and transforms data
- Makes decisions
- Implements business rules

**Examples:**
- `logic.agent.analysis.py` — Analysis agent
- `logic.script.migration.rb` — Migration script

---

### Application (body)
**Languages:** Swift, Objective-C, Java

The embodiment layer. Code here:
- Brings everything together
- Creates runnable artifacts
- Bridges to platform-specific APIs

**Examples:**
- `application.app.mobile.swift` — iOS mobile app
- `application.bridge.legacy.m` — Legacy system bridge

## Data Flow

```mermaid
flowchart LR
    User([User]) --> I[Interface]
    I --> L[Logic]
    L --> C[Core]
    C --> L
    L --> I
    I --> User

    External([External Systems]) --> I
    I --> External
```

## Layer Dependencies

| Layer | Can Depend On |
|-------|---------------|
| Core | (none) |
| Logic | Core |
| Interface | Core, Logic |
| Application | Core, Logic, Interface |

> **Rule:** Layers can only depend on layers below them. Core is the foundation; Application sits at the top.
