---
name: mp-git
description: "Git operations with conventional commits, security scanning, and PR creation. Use for committing, pushing, creating PRs, git status."
argument-hint: "[cm|cp|pr|status]"
license: MIT
---

# Git Operations

Stage, commit with conventional messages, push, and create PRs — with security scanning.

## Invocation

```
mp-git [cm|cp|pr|status]

cm: Stage + commit with conventional message
cp: Commit + push
pr: Create pull request (requires `gh` CLI)
status: Show git status summary
```

## When to Use
- After implementing and reviewing changes
- As part of mp-execute post-execution workflow
- To create conventional commits with security checks
- To create pull requests

## Subcommands

### `mp-git cm` (commit)

Load: `references/commit-conventions.md` for conventional commit format.
Load: `references/security-scan.md` for pre-commit security checks.

1. **Status check** — Run `git status` to show staged/unstaged changes
2. **Staging** — If nothing staged: ask user what to stage, or `git add -A`
3. **Security scan** — Grep diff for secrets, API keys, tokens, .env contents
   - If found: WARN and ask user to confirm via `ask_user`
4. **Diff analysis** — Analyze staged diff for commit type:
   - `feat:` — new functionality
   - `fix:` — bug fix
   - `refactor:` — code restructuring
   - `docs:` — documentation changes
   - `test:` — adding/updating tests
   - `chore:` — maintenance, dependencies
5. **Split decision** — If changes span multiple concerns:
   - Ask user: "Split into multiple commits?" via `ask_user`
   - If yes: guide through selective staging (`git add -p` or specific files)
6. **Commit message** — Generate conventional format:
   ```
   <type>(<scope>): <description>
   
   <body>
   
   Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>
   ```
7. **Execute** — `git commit -m "..."`

### `mp-git cp` (commit + push)
1. Run `mp-git cm` workflow
2. Push: `git push`
3. If push fails (no upstream): `git push --set-upstream origin <branch>`

### `mp-git pr` (pull request)
1. Check `gh` CLI is available
2. Get current branch name
3. Analyze changes vs target branch (`git diff main..HEAD`)
4. Generate PR title (from commits) + body (summary of changes)
5. Create: `gh pr create --title "..." --body "..."`

### `mp-git status`
1. Run `git status --short`
2. Show formatted summary: staged, unstaged, untracked counts
3. Show recent commits: `git log --oneline -5`

## Rules
- ALWAYS include `Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>` trailer
- ALWAYS run security scan before committing
- Never commit .env files, secrets, or API keys
- Prefer atomic commits (one concern per commit)

## Related Skills
- `mp-code-review` — Run review before committing
- `mp-docs` — Update docs before committing
- `mp-execute` — Invokes this skill post-execution
