---
applyTo: "**/*"
---

# File Naming Conventions

When creating new files:

- Use **kebab-case** for file names (e.g., `user-service.ts`, `auth-middleware.js`)
- Names should be **long and descriptive** — self-documenting so LLMs can understand purpose from the name alone when using `grep` or `glob`
- Match **language conventions**: PascalCase for C#/Java classes, snake_case for Python modules
- Prefer descriptive names over short abbreviated ones
- **Never** use generic names like `utils.ts`, `helpers.js`, `temp.md`, `misc.py`
