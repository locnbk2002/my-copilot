# Architecture

## Overview

`my-copilot` is a GitHub Copilot CLI plugin that provides a complete AI-assisted engineering workflow. It is purely configuration-driven — no build step, no runtime binary. All logic is expressed as Markdown skill files, agent definitions, Python hook scripts, and JSON configuration.

## Components

### Skills (`skills/`)

13 reusable workflow modules invoked via the `skill` tool:

| Skill                 | Purpose                                                                                           |
| --------------------- | ------------------------------------------------------------------------------------------------- |
| `plan`                | Implementation planning with research & validation (auto-brainstorm, challenge assessment)        |
| `execute`             | Wave-based phase execution with test/review gates; auto post-chain (test, fix, review, docs, git) |
| `test`                | Auto-detect & run tests with structured reporting                                                 |
| `fix`                 | Bug diagnosis & root cause analysis                                                               |
| `code-review`         | Scout → review → fix pipeline                                                                     |
| `docs`                | Initialize, update, and summarize documentation                                                   |
| `docs-seeker`         | Library/framework doc lookup via Context7 MCP                                                     |
| `git`                 | Conventional commits, security scanning, PR creation                                              |
| `brainstorm`          | Structured ideation with approach comparison                                                      |
| `scout`               | Parallel codebase exploration                                                                     |
| `research`            | Technical research & evaluation                                                                   |
| `sequential-thinking` | Step-by-step complex problem analysis                                                             |
| `tdd`                 | Red→green→refactor TDD cycle; `execute --tdd` applies per-phase TDD mode                          |

### Agents (`agents/`)

6 specialized sub-agents launched via the `task` tool:

| Agent           | Model             | Purpose                                                                                                         |
| --------------- | ----------------- | --------------------------------------------------------------------------------------------------------------- |
| `planner`       | Claude Opus 4.6   | Architecture & implementation planning                                                                          |
| `code-reviewer` | GPT 5.3 Codex     | Code review (infer: true)                                                                                       |
| `debugger`      | GPT 5.3 Codex     | Root cause analysis (infer: true)                                                                               |
| `researcher`    | Claude Haiku 4.5  | Deep technical research (infer: true)                                                                           |
| `multimodal`    | Gemini 3.1 Pro    | UI/screenshot analysis, visual debugging (infer: true)                                                          |
| `worker`        | Claude Sonnet 4.6 | Wave-scoped phase orchestrator — receives wave-limited phases, dispatches fresh sub-agent per phase by category |

### Hooks (`scripts/` + `hooks.json`)

Python scripts triggered on Copilot CLI lifecycle events:

| Hook             | Script                     | Trigger                                                                                                                                               |
| ---------------- | -------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------- |
| (shared utility) | `hook_utils.py`            | Imported by all hook scripts — provides `get_log_dir()`, `log_path()`, `append_log()`, `read_log_tail()`, `count_log_lines()`, and session management |
| `preToolUse`     | `scout-block.py`           | Security control before tool execution                                                                                                                |
| `preToolUse`     | `privacy-block.py`         | Privacy enforcement before tool execution                                                                                                             |
| `preToolUse`     | `log-subagent-launch.py`   | Log sub-agent startup                                                                                                                                 |
| `preToolUse`     | `comment-checker.py`       | Block code comments (uses `@code-yeongyu/comment-checker` AST binary with regex fallback)                                                             |
| `preToolUse`     | `todo-enforcer.py`         | Block git commit/push with pending plan phases                                                                                                        |
| `postToolUse`    | `tool-tracker.py`          | Track tool usage after execution                                                                                                                      |
| `postToolUse`    | `log-subagent-complete.py` | Log sub-agent completion                                                                                                                              |
| `postToolUse`    | `edit-validator.py`        | Track edit/create results and file sizes                                                                                                              |
| `postToolUse`    | `agent-babysitter.py`      | Detect stuck/looping sub-agents                                                                                                                       |
| `postToolUse`    | `auto-compact-reminder.py` | Log compaction reminder every 100 tool calls                                                                                                          |
| `sessionStart`   | `session-logger.py`        | Session lifecycle logging                                                                                                                             |
| `sessionEnd`     | `session-logger.py`        | Session lifecycle logging                                                                                                                             |
| `errorOccurred`  | `error-logger.py`          | Error tracking                                                                                                                                        |
| `errorOccurred`  | `context-recovery.py`      | Log recovery data on context exhaustion                                                                                                               |

#### Logging

All hook scripts write structured JSONL logs via `hook_utils.py`:

- **Log location**: `~/.local/share/.copilot/my-copilot/logs/<project-hash>/<session-id>/`
  - `<project-hash>` — 12-char SHA-256 of the project's absolute path
  - `<session-id>` — UUID assigned per Copilot CLI session
- **Session isolation**: each session's UUID is stored in a PPID-keyed file under `.sessions/` so concurrent sessions never share a log directory
- **Override for testing**: set `HOOK_LOG_BASE` env var to redirect log writes to a temp directory
- **Log files**:
  - `sessions.jsonl` — session start/end lifecycle events
  - `tools.jsonl` — per-tool-call tracking
  - `errors.jsonl` — error events
  - `subagents.jsonl` — sub-agent launch and completion events
  - `edit-health.jsonl` — edit/create file size and health checks
  - `model-fallback.jsonl` — model rate-limit fallback events
  - `context-recovery.jsonl` — context exhaustion recovery data
  - `compact-reminders.jsonl` — compaction reminder triggers
  - `agent-health.jsonl` — stuck/looping sub-agent detections

### MCP Server (`.mcp.json`)

Integrates Context7 for external documentation lookup:

- Tool: `@upstash/context7-mcp` (via npx)
- Exposes: `query-docs`, `resolve-library-id`
- Required by: `docs-seeker` skill

### Plugin Metadata (`.github/plugin/`)

- `plugin.json` — Declares agents, skills, hooks, MCP servers
- `marketplace.json` — Marketplace listing metadata

### Global Instructions (`.github/`)

- `copilot-instructions.md` — Master workflow rules applied to all sessions (at project root)

## Data Flow

```
User prompt
    │
    ▼
Copilot CLI (main context)
    │
    ├─► skill tool → skill (Markdown instructions loaded into context)
    │       │
    │       └─► task tool → sub-agent (explore / planner / researcher / ...)
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
- **Wave-based execution with category delegation**: `execute` computes dependency waves from plan.md. Each wave dispatches a fresh `worker` sub-agent with only that wave's phases. Worker reads `.github/my-copilot.jsonc` (or `~/.copilot/my-copilot.jsonc`) to resolve model+agent_type per phase category, then dispatches fresh sub-agents per phase (no shared context). After all waves complete, auto post-chain runs: test → fix (if needed) → review → docs → git commit.
- **SQL task tracking**: Session-scoped SQLite (`todos` table) tracks work across sub-agent invocations.
