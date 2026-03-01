# Code Standards

## Principles

Follow **YAGNI · KISS · DRY** on all changes.

## File Naming

- Use **kebab-case** for all files (e.g., `user-service.ts`, `auth-middleware.js`)
- Names must be **long and descriptive** — self-documenting for LLM search tools
- Match language conventions: PascalCase for C#/Java classes, snake_case for Python modules
- **Never** use generic names: `utils.ts`, `helpers.js`, `temp.md`, `misc.py`

## File Size

- Keep code files under **200 lines**
- Split large files into focused modules
- Extract utilities into separate files
- Create dedicated service classes for business logic

## Markdown & Skill Files

- Skill files (`SKILL.md`) must follow the structure: name, description, argument-hint, invocation, subcommands
- Reference files go in `references/` subdirectory of each skill
- Agent files use front-matter: `name`, `description`, `model`, `tools`, `infer`
- Keep skill instructions concise and actionable

## Python Hook Scripts

- All hook scripts must handle missing/malformed input gracefully
- Use `sys.exit(0)` to allow tool execution; `sys.exit(1)` to block
- Hooks have a 5-second timeout (`errorOccurred` hooks: 10 seconds)
- Log to stderr or a log file, not stdout

## JSON Configuration

- `plugin.json` — use relative paths from repo root
- `hooks.json` — provide both `bash` and `powershell` variants for cross-platform support
- `.mcp.json` — never commit real API keys; use placeholder values

## Git Commits

Use **conventional commit format**:

```
feat: add brainstorm skill
fix: correct timeout in hook scripts
chore: update plugin metadata
docs: initialize docs structure
```

## Comments

Only comment code that needs clarification. Do not over-comment obvious logic.

## Error Handling

- Use try/catch (or try/except in Python) for all external calls
- Never swallow exceptions silently — log them
- Hook scripts must not raise unhandled exceptions
