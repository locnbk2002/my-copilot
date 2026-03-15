# Domain Plugins Install Guide

Domain plugins extend my-copilot with specialized agents and skills for frontend, backend, and DevOps workflows.

## Prerequisites

- GitHub Copilot CLI installed
- Base `my-copilot` plugin installed:
  ```sh
  copilot plugin marketplace add locnbk2002/my-copilot
  copilot plugin install my-copilot@my-copilot
  ```

## Install Domain Plugins

### Frontend Plugin

8 skills: React/Next.js, UI/UX design, Tailwind/shadcn, TanStack, web frameworks.
2 agents: `frontend-developer` (claude-sonnet-4.6), `ui-ux-designer` (gemini-3-pro-preview).

```sh
copilot plugin install my-copilot@my-copilot-frontend
```

### Backend Plugin

4 skills: APIs, databases (PostgreSQL/MongoDB), Better Auth, payment integration.
1 agent: `backend-developer` (claude-sonnet-4.6).

```sh
copilot plugin install my-copilot@my-copilot-backend
```

### DevOps Plugin

2 skills: Docker/K8s/Cloudflare/GCP CI/CD, git worktrees.
No dedicated agent — worker uses `general-purpose` for `Category: devops`.

```sh
copilot plugin install my-copilot@my-copilot-devops
```

## Configure Category Routing

Copy the example config to your project:

```sh
cp .github/my-copilot.jsonc.example .github/my-copilot.jsonc
```

> Note: if `.github/my-copilot.jsonc` contains API keys for model providers, add it to `.gitignore`.

Customize model/agent mappings as needed. The domain categories added by plugins:

| Category    | Default Agent      | Default Model        | Plugin Required     |
| ----------- | ------------------ | -------------------- | ------------------- |
| `frontend`  | frontend-developer | claude-sonnet-4.6    | my-copilot-frontend |
| `ui-design` | ui-ux-designer     | gemini-3-pro-preview | my-copilot-frontend |
| `backend`   | backend-developer  | claude-sonnet-4.6    | my-copilot-backend  |
| `devops`    | general-purpose    | claude-sonnet-4.6    | my-copilot-devops   |

## Use in Plans

Tag plan phases with domain categories to route to the right agent:

```markdown
## Phase 2 — Build Dashboard UI

- Category: frontend
- Effort: 3h
- Skills: frontend-development, react-best-practices

## Phase 3 — Design System Audit

- Category: ui-design
- Effort: 1h

## Phase 4 — REST API Implementation

- Category: backend
- Effort: 2h
- Skills: backend-development, databases

## Phase 5 — Deploy to Cloudflare

- Category: devops
- Effort: 1h
- Skills: devops
```

Run with:

```sh
copilot execute plan.md
```

The worker agent reads your `.github/my-copilot.jsonc` and dispatches each phase to the correct domain agent.

## Fallback Behavior

If a domain plugin is not installed, the worker falls back to `general-purpose` + `claude-sonnet-4.6` for unknown categories. Install the plugin to get the specialized agent.
