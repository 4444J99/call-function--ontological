# Comparison with Other Naming Conventions

How FUNCTIONcalled() compares to other naming and organizational approaches.

## Quick Comparison Table

| Approach | Focus | Scope | Self-Describing |
|----------|-------|-------|-----------------|
| **FUNCTIONcalled()** | File names + structure | Full project | Yes |
| BEM | CSS class names | Styling only | Partial |
| Atomic Design | Component hierarchy | UI components | Partial |
| Clean Architecture | Dependency layers | Code organization | No |
| Domain-Driven Design | Business domains | System design | Partial |

## Detailed Comparisons

### BEM (Block Element Modifier)

**What it is:** CSS naming convention for class names.

```css
/* BEM */
.button {}
.button__icon {}
.button--primary {}
```

**Similarities:**
- Both use structured naming with separators
- Both aim for predictability

**Differences:**
| Aspect | BEM | FUNCTIONcalled() |
|--------|-----|------------------|
| Scope | CSS classes | All files |
| Structure | Block__Element--Modifier | Layer.Role.Domain.Ext |
| Focus | Component styling | System architecture |

**Can they coexist?** Yes. Use BEM for CSS class names, FUNCTIONcalled() for file names:
```
interface/interface.button.primary.css  # File name
.button--primary { }                     # Class name inside
```

---

### Atomic Design

**What it is:** UI component methodology (atoms, molecules, organisms, templates, pages).

```
components/
├── atoms/
│   └── Button.tsx
├── molecules/
│   └── SearchField.tsx
└── organisms/
    └── Header.tsx
```

**Similarities:**
- Both use layered organization
- Both aim to communicate component purpose

**Differences:**
| Aspect | Atomic Design | FUNCTIONcalled() |
|--------|---------------|------------------|
| Scope | UI components | All code |
| Layers | 5 (atoms→pages) | 4 (core→application) |
| Focus | Component size | System responsibility |

**Can they coexist?** Yes. Map Atomic to FUNCTIONcalled():
```
# Atomic: atoms/Button.tsx
# FUNCTIONcalled: interface/interface.atom.button.tsx

# Atomic: organisms/Header.tsx
# FUNCTIONcalled: interface/interface.organism.header.tsx
```

---

### Clean Architecture

**What it is:** Software architecture pattern with concentric dependency layers.

```
src/
├── entities/        # Enterprise business rules
├── use-cases/       # Application business rules
├── interface-adapters/  # Controllers, presenters
└── frameworks/      # Web, DB, external
```

**Similarities:**
- Both organize by responsibility
- Both have dependency direction rules

**Differences:**
| Aspect | Clean Architecture | FUNCTIONcalled() |
|--------|-------------------|------------------|
| Focus | Dependency rules | Naming + organization |
| Layers | 4+ (varies) | 4 (fixed) |
| Naming | Folder-based | File-based |

**Can they coexist?** Yes. Clean Architecture structures folders, FUNCTIONcalled() names files:
```
# Clean Architecture folder + FUNCTIONcalled file
use-cases/
└── logic.usecase.create-user.ts
```

---

### Domain-Driven Design (DDD)

**What it is:** Software design approach focused on business domains.

```
src/
├── domain/
│   ├── user/
│   │   ├── User.ts
│   │   └── UserRepository.ts
│   └── order/
│       └── Order.ts
└── application/
    └── services/
```

**Similarities:**
- Both aim to make code self-documenting
- Both consider system boundaries

**Differences:**
| Aspect | DDD | FUNCTIONcalled() |
|--------|-----|------------------|
| Focus | Business concepts | Technical roles |
| Organization | By domain | By layer |
| Naming | Entity names | Layer.Role.Domain |

**Can they coexist?** Yes. Use DDD domains as FUNCTIONcalled() domains:
```
# DDD: domain/user/User.ts
# FUNCTIONcalled: core/core.entity.user.ts

# DDD: application/services/UserService.ts
# FUNCTIONcalled: logic/logic.service.user.ts
```

---

## When to Use FUNCTIONcalled()

**Choose FUNCTIONcalled() when you need:**
- File names that explain themselves in search results
- Clear technical layer separation
- Convention that works for code AND non-code files
- Simple rules that scale across projects

**Consider alternatives when:**
- You only need CSS organization (BEM is more specialized)
- Business domain boundaries are more important than technical layers (DDD)
- You're working within a framework that enforces its own structure

## Hybrid Approaches

FUNCTIONcalled() is designed to complement, not replace:

```
# BEM + FUNCTIONcalled()
interface/interface.button.primary.css
  → .button--primary { }

# Atomic + FUNCTIONcalled()
interface/interface.atom.button.tsx
interface/interface.molecule.search-field.tsx

# Clean Architecture + FUNCTIONcalled()
entities/core.entity.user.ts
use-cases/logic.usecase.create-order.ts

# DDD + FUNCTIONcalled()
user-domain/core.entity.user.ts
user-domain/logic.repository.user.ts
```

## Summary

FUNCTIONcalled() is unique in focusing on **file-level self-documentation**. Other approaches handle class naming (BEM), component hierarchy (Atomic), architecture (Clean), or business modeling (DDD). They solve different problems and can work together.

The key question: **"Can someone understand this file's purpose from its name alone?"**

FUNCTIONcalled() says yes.
