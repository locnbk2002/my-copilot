---
name: mp-docs
description: "Initialize, update, and summarize project documentation based on code changes. Use for docs generation, README updates, API documentation, architecture docs."
argument-hint: "[init|update|summarize]"
license: MIT
---

# Documentation Management

Initialize standard docs structure, update docs based on code changes, or generate project summaries.

## Invocation

```
mp-docs [init|update|summarize]

init: Initialize standard docs structure for project
update: Update existing docs based on code changes
summarize: Generate project summary/README
```

## When to Use
- After implementing features (update docs)
- Starting a new project (init docs structure)
- Before release (summarize project)
- As part of mp-execute post-execution workflow

## Subcommands

### `mp-docs init`

1. Detect project type (from package.json, go.mod, Cargo.toml, etc.)
2. Create standard `docs/` structure:
   ```
   docs/
   ├── README.md              # Project overview
   ├── architecture.md        # System architecture
   ├── getting-started.md     # Setup & development guide
   └── api-reference.md       # API documentation (if applicable)
   ```
3. Populate with auto-detected info (dependencies, scripts, project structure)
4. Use `task(agent_type="explore")` to scan codebase for structure

### `mp-docs update`

Load: `references/update-workflow.md` for detection and update logic.

1. Get recent changes: `git diff main..HEAD` or `git log --oneline -10`
2. Identify what docs need updating:
   - New APIs or endpoints → update api-reference.md
   - New dependencies → update getting-started.md
   - Architecture changes → update architecture.md
   - New features → update README.md
3. Dispatch `task(agent_type="explore")` to read changed files
4. Update affected docs in-place (`edit` tool, not `create`)

### `mp-docs summarize`

1. Read project structure, README, key files
2. Generate a concise project summary
3. Output to user or update README.md

## Related Skills

- `mp-docs-seeker` — Look up external library/API documentation
- `mp-execute` — Invokes this skill post-execution
- `mp-git` — Typically invoked after docs are updated
