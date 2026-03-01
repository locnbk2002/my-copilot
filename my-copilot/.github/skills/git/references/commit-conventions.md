## Conventional Commits

### Format
```
<type>(<scope>): <description>

[optional body]

[optional footer]
Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>
```

### Types

| Type | When to Use |
|------|------------|
| `feat` | New feature or capability |
| `fix` | Bug fix |
| `refactor` | Code change that neither fixes a bug nor adds a feature |
| `docs` | Documentation only changes |
| `test` | Adding or updating tests |
| `chore` | Maintenance (deps, config, build) |
| `perf` | Performance improvement |
| `ci` | CI/CD changes |
| `style` | Formatting, whitespace (no code change) |
| `revert` | Reverting a previous commit |

### Scope

Optional, in parentheses. Use the module or feature area:
- `feat(auth): add JWT token refresh`
- `fix(api): handle null user response`
- `docs(readme): update installation steps`

### Description

- Use imperative mood: "add" not "added" or "adds"
- Don't capitalize first letter
- No period at end
- Max 72 characters

### Body

- Explain WHY, not WHAT (the diff shows what)
- Wrap at 72 characters
- Use bullet points for multiple items

### Breaking Changes

Use `!` after type or `BREAKING CHANGE:` footer:
```
feat(api)!: change response format to JSON:API

BREAKING CHANGE: Response envelope changed from {data: ...} to {data: {attributes: ...}}
```

### Multi-concern Detection

If staged changes touch multiple concerns, suggest splitting:
- Different directories = likely different concerns
- Mix of src + test = OK (same concern)
- Mix of feat + fix = suggest splitting
- Mix of docs + code = suggest splitting

## Phase Commit Pattern (--atomic)

When `--atomic` is set and plan phases are detected:

```
feat(phase-1): implement model fallback hook
feat(phase-2): add --discuss mode to plan
docs(phase-7): update execution workflow docs
```

Scope uses `phase-N` when matched to a plan phase.
When no plan match, use directory/module name:

```
feat(scripts): add model-fallback hook
feat(plan): add discuss workflow and modes
chore(config): update hooks.json for new hooks
```

## Auto-Grouping Heuristics (--atomic)

Priority order:
1. **Plan phase file paths** — match staged files to phase "Related Code Files"
2. **Directory prefix** — group by first 2 path segments
3. **File type** — separate: scripts/, skills/, agents/, config files

Each group → one commit. All commits get Co-authored-by trailer.

## Pre-commit / Pre-push Rules

- **Pre-commit**: Run project linter before committing
- **Pre-push**: Run tests — **DO NOT** ignore failing tests to pass builds or CI
- **DO NOT** commit confidential information (`.env` files, API keys, database credentials)
- Keep commits focused on actual code changes
- Create clean, professional commit messages without AI references
