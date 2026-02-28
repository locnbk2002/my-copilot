# Architecture

## Overview

`my-copilot` is a GitHub Copilot CLI plugin that provides a complete AI-assisted engineering workflow. It is purely configuration-driven — no build step, no runtime binary. All logic is expressed as Markdown skill files, agent definitions, Python hook scripts, and JSON configuration.

## Components

### Skills (`.github/skills/`)

12 reusable workflow modules invoked via the `skill` tool:

| Skill | Purpose |
|-------|---------|
| `mp-plan` | Implementation planning with research & validation |
| `mp-execute` | Phase-by-phase plan execution with test gates |
| `mp-test` | Auto-detect & run tests with structured reporting |
| `mp-fix` | Bug diagnosis & root cause analysis |
| `mp-code-review` | Scout → review → fix pipeline |
| `mp-docs` | Initialize, update, and summarize documentation |
| `mp-docs-seeker` | Library/framework doc lookup via Context7 MCP |
| `mp-git` | Conventional commits, security scanning, PR creation |
| `mp-brainstorm` | Structured ideation with approach comparison |
| `mp-scout` | Parallel codebase exploration |
| `mp-research` | Technical research & evaluation |
| `mp-sequential-thinking` | Step-by-step complex problem analysis |

### Agents (`.github/agents/`)

6 specialized sub-agents launched via the `task` tool:

| Agent | Model | Purpose |
|-------|-------|---------|
| `mp-planner` | Claude Opus 4.6 | Architecture & implementation planning |
| `mp-code-reviewer` | Claude Sonnet 4.6 | Code review (infer: true) |
| `mp-debugger` | Claude Sonnet 4.6 | Root cause analysis (infer: true) |
| `mp-researcher` | Claude Haiku 4.5 | Deep technical research (infer: true) |
| `mp-multimodal` | Gemini 3 Pro | UI/screenshot analysis, visual debugging (infer: true) |
| `mp-worker` | Claude Sonnet 4.6 | Category-aware phase orchestrator — delegates phases to sub-agents by category |

### Hooks (`.github/scripts/` + `hooks.json`)

Python scripts triggered on Copilot CLI lifecycle events:

| Hook | Script | Trigger |
|------|--------|---------|
| `preToolUse` | `scout-block.py` | Security control before tool execution |
| `preToolUse` | `privacy-block.py` | Privacy enforcement before tool execution |
| `preToolUse` | `log-subagent-launch.py` | Log sub-agent startup |
| `preToolUse` | `comment-checker.py` | Block code comments (uses `@code-yeongyu/comment-checker` AST binary with regex fallback) |
| `preToolUse` | `todo-enforcer.py` | Block git commit/push with pending plan phases |
| `postToolUse` | `tool-tracker.py` | Track tool usage after execution |
| `postToolUse` | `log-subagent-complete.py` | Log sub-agent completion |
| `postToolUse` | `edit-validator.py` | Track edit/create results and file sizes |
| `postToolUse` | `agent-babysitter.py` | Detect stuck/looping sub-agents |
| `postToolUse` | `auto-compact-reminder.py` | Log compaction reminder every 100 tool calls |
| `sessionStart` | `session-logger.py` | Session lifecycle logging |
| `sessionEnd` | `session-logger.py` | Session lifecycle logging |
| `errorOccurred` | `error-logger.py` | Error tracking |
| `errorOccurred` | `context-recovery.py` | Log recovery data on context exhaustion |

### MCP Server (`.mcp.json`)

Integrates Context7 for external documentation lookup:
- Tool: `@upstash/context7-mcp` (via npx)
- Exposes: `query-docs`, `resolve-library-id`
- Required by: `mp-docs-seeker` skill

### Plugin Metadata (`.github/plugin/`)

- `plugin.json` — Declares agents, skills, hooks, MCP servers
- `marketplace.json` — Marketplace listing metadata

### Global Instructions (`.github/`)

- `copilot-instructions.md` — Master workflow rules applied to all sessions
- `instructions/development-rules.instructions.md` — YAGNI·KISS·DRY, file conventions
- `instructions/orchestration.instructions.md` — Sub-agent delegation protocol
- `instructions/documentation-management.instructions.md` — Docs workflow

## Data Flow

```
User prompt
    │
    ▼
Copilot CLI (main context)
    │
    ├─► skill tool → mp-* skill (Markdown instructions loaded into context)
    │       │
    │       └─► task tool → sub-agent (explore / mp-planner / mp-researcher / ...)
    │                │
    │                └─► bash / grep / glob / edit / create / view tools
    │
    ├─► preToolUse hooks → Python scripts (security, privacy, logging)
    ├─► postToolUse hooks → Python scripts (tracking, logging)
    └─► MCP tools → Context7 server (external docs lookup)
```

## Key Design Decisions

- **Configuration-only**: No compiled code — skills/agents are Markdown; hooks are Python scripts. Easy to extend without a build pipeline.
- **Skill-based modularity**: Each concern is a separate skill directory with its own references, enabling independent evolution.
- **Security-first hooks**: Privacy and security checks run on every tool call before execution.
- **Model tiering**: Expensive Opus model reserved for planning; Haiku for fast research; Sonnet for standard work; `gpt-5.3-codex` for large context sweeps; Gemini for visual/multimodal.
- **Category-based delegation**: Plan phases are tagged with work categories (visual-engineering, deep, artistry, quick, general, complex, writing). `mp-worker` reads `.github/my-copilot.jsonc` (or `~/.copilot/my-copilot.jsonc`) to resolve model+agent_type per category and dispatches each phase to the appropriate sub-agent.
- **SQL task tracking**: Session-scoped SQLite (`todos` table) tracks work across sub-agent invocations.
