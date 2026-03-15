---
name: worktree
description: "Create isolated git worktree for parallel development in monorepos."
argument-hint: "[feature-description] OR [project] [feature]"
license: MIT
---

# Git Worktree

Create an isolated git worktree for parallel feature development without stashing or switching branches.

## When to Use

- Develop multiple features in parallel
- Monorepo isolation — work in one package without affecting others
- Test a branch without stashing current work
- Run my-copilot /team with isolated agent workspaces

## Create a Worktree

```bash
git worktree add <path> <branch>
```

**New feature branch:**

```bash
git worktree add ../feat-my-feature feat/my-feature
# Creates branch feat/my-feature + working tree at ../feat-my-feature
```

**Existing branch:**

```bash
git worktree add ../hotfix-123 hotfix/issue-123
```

## List Worktrees

```bash
git worktree list
```

## Remove a Worktree

```bash
git worktree remove ../feat-my-feature
git branch -d feat/my-feature  # optional: delete the branch too
```

## Prune Stale References

```bash
git worktree prune
```

Use after manually deleting worktree directories.

## Install Dependencies After Creation

Based on project context, run in the new worktree directory:

| Lock file           | Command                           |
| ------------------- | --------------------------------- |
| `bun.lock`          | `bun install`                     |
| `pnpm-lock.yaml`    | `pnpm install`                    |
| `yarn.lock`         | `yarn install`                    |
| `package-lock.json` | `npm install`                     |
| `poetry.lock`       | `poetry install`                  |
| `requirements.txt`  | `pip install -r requirements.txt` |
| `Cargo.toml`        | `cargo build`                     |
| `go.mod`            | `go mod download`                 |

## my-copilot Team Workflow

When using the `/team` skill, each team member works in an isolated worktree:

1. Lead creates worktrees for each feature agent
2. Agents push commits to their worktree branch
3. Lead reviews and merges after completion

```bash
# Lead sets up agent worktrees
git worktree add ../agent-feat-auth feat/auth
git worktree add ../agent-feat-api feat/api

# After agents finish
git worktree remove ../agent-feat-auth
git worktree remove ../agent-feat-api
```

## Branch Naming Convention

| Prefix            | Use case          |
| ----------------- | ----------------- |
| `feat/<slug>`     | New features      |
| `fix/<slug>`      | Bug fixes         |
| `refactor/<slug>` | Refactoring       |
| `docs/<slug>`     | Documentation     |
| `test/<slug>`     | Tests / coverage  |
| `chore/<slug>`    | Maintenance, deps |

**Slug rules:** kebab-case, max 50 chars.
Examples: `feat/add-auth`, `fix/login-redirect`, `refactor/api-client`
