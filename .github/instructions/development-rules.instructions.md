---
applyTo: "**/*"
---

# Development Rules

**ALWAYS** follow: **YAGNI (You Aren't Gonna Need It) · KISS (Keep It Simple, Stupid) · DRY (Don't Repeat Yourself)**

**ALWAYS** activate relevant skills before starting tasks.

## General

- **File Naming**: Use kebab-case with meaningful, descriptive names. Long names are fine — they must be self-documenting so LLMs can understand purpose from the name alone when using `grep` or `glob`.
- **File Size Management**: Keep individual code files under **200 lines**
  - Split large files into smaller, focused components/modules
  - Use composition over inheritance for complex widgets
  - Extract utility functions into separate modules
  - Create dedicated service classes for business logic
- For docs/API lookup, activate the `mp-docs-seeker` skill (Context7)
- Use `gh` bash command to interact with GitHub features
- Use `psql` bash command to query Postgres for debugging
- Use `mp-sequential-thinking` skill for step-by-step analysis, debugging, and complex reasoning
- **Follow** codebase structure and code standards in `./docs` during implementation
- **Do not** simulate or mock implementations — always write real code

## Code Quality Guidelines

- Read and follow codebase structure and code standards in `./docs`
- Don't be overly harsh on style/formatting, but **ensure no syntax errors and code is compilable**
- Prioritize functionality and readability over strict style enforcement
- Use reasonable code quality standards that enhance developer productivity
- Use try/catch error handling and follow security standards
- Use the `code-review` agent (via `task` tool) to review code after every implementation

## Pre-commit / Pre-push Rules

- Run linting before commit
- Run tests before push — **DO NOT** ignore failing tests to pass builds or CI
- Keep commits focused on actual code changes
- **DO NOT** commit confidential information (dotenv files, API keys, database credentials, etc.)
- Create clean, professional commit messages without AI references
- Use **conventional commit format** (e.g., `feat:`, `fix:`, `chore:`, `docs:`)

## Code Implementation

- Write clean, readable, and maintainable code
- Follow established architectural patterns
- Implement features according to specifications
- Handle edge cases and error scenarios
- **DO NOT** create new "enhanced" files — update existing files directly

## Tool Reference

| Need | Tool |
|------|------|
| Read a file | `view` |
| Create a new file | `create` |
| Edit an existing file | `edit` |
| Find files by name | `glob` |
| Search file contents | `grep` |
| Run shell commands | `bash` |
| Fetch a URL | `web_fetch` |
| Search the web | `web_search` |
| Track tasks | `sql` (todos table) |
| Launch sub-agents | `task` |
| Invoke a skill | `skill` |
