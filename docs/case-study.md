# Case Study: Adopting FUNCTIONcalled()

A practical example of applying the FUNCTIONcalled() naming convention.

## The Problem

A mid-sized web application had accumulated technical debt over 3 years:

- 400+ files with inconsistent naming
- `utils/`, `helpers/`, `common/` directories with unclear ownership
- Developers struggled to find code during debugging
- New team members took weeks to navigate the codebase

**Common symptoms:**
```
src/
├── utils/
│   ├── helpers.js      # What does this help with?
│   ├── utils.js        # Utility for what?
│   └── common.js       # Common to what?
├── components/
│   ├── Button.tsx      # Which button? For what feature?
│   └── Modal.tsx       # Modal for what purpose?
└── services/
    └── api.js          # Which API? All APIs?
```

## The Solution

The team adopted FUNCTIONcalled() incrementally over 6 months.

### Phase 1: New Files (Month 1-2)

All new files followed the convention:

```
src/
├── logic/
│   └── logic.validator.email.ts
├── interface/
│   └── interface.modal.confirmation.tsx
└── (existing files unchanged)
```

**Result:** New files were immediately discoverable by name alone.

### Phase 2: Rename on Touch (Month 3-4)

When modifying files, developers renamed them:

```
# Before
utils/helpers.js

# After
logic/logic.util.string.ts
logic/logic.util.date.ts
logic/logic.util.format.ts
```

**Result:** The mysterious `helpers.js` became three focused utilities.

### Phase 3: Batch Migration (Month 5-6)

Critical modules were renamed systematically:

```
# Before
components/Button.tsx
components/Modal.tsx
services/api.js

# After
interface/interface.button.primary.tsx
interface/interface.button.secondary.tsx
interface/interface.modal.confirmation.tsx
interface/interface.modal.form.tsx
logic/logic.api.user.ts
logic/logic.api.product.ts
```

## Results

### Quantitative

| Metric | Before | After |
|--------|--------|-------|
| Time to find file (avg) | 45 sec | 12 sec |
| New dev onboarding | 3 weeks | 1 week |
| "Wrong file" commits | 8/month | 1/month |
| Files in "utils" | 47 | 0 |

### Qualitative

- **Search became trivial:** "I need the email validation logic" → search `logic.validator.email`
- **Ownership was clear:** Each file declared its layer and purpose
- **Code reviews improved:** Misplaced code was obvious from the filename
- **Documentation reduced:** Names explained what documentation used to

## Lessons Learned

1. **Start with new files.** Don't try to rename everything at once.
2. **Use the validator.** Automated feedback catches mistakes early.
3. **Document exceptions.** Framework-required names should be explicitly noted.
4. **Celebrate wins.** Share examples of the naming helping during debugging.

## Testimonials

> "I used to grep for 20 minutes to find where validation happened. Now I just open `logic.validator.*.ts`."
> — Senior Developer

> "The naming convention made code review faster. If a file is in `interface/` but does business logic, we catch it immediately."
> — Tech Lead

> "New hires say the codebase is the most navigable they've worked with."
> — Engineering Manager

---

*Have your own case study? [Submit it via GitHub Issues](https://github.com/YOUR_USERNAME/call-function--ontological/issues).*
