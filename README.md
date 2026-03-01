# my-copilot

A complete AI engineering workflow plugin for GitHub Copilot CLI — 12 skills, 4 agents, hooks, and MCP config covering the full development lifecycle from planning to git commit.

## Installation

```bash
# Option 1: Via marketplace (recommended)
copilot plugin marketplace add locnbk2002/my-copilot
copilot plugin install my-copilot@my-copilot

# Option 2: Direct GitHub install
copilot plugin install locnbk2002/my-copilot

# Option 3: Local install (for development)
copilot plugin install ./my-copilot
```

## What's Included

### Skills (12)

| Skill | Description |
|-------|-------------|
| `mp-plan` | Plan implementations with auto-brainstorm, research, red-team, and validation phases (`--skip-brainstorm` to skip brainstorm) |
| `mp-execute` | Execute plans phase-by-phase with auto post-execution chain: test → fix → review → docs → commit (`--skip-post` to skip chain) |
| `mp-test` | Auto-detect and run tests with structured reporting |
| `mp-fix` | Diagnose and fix bugs with root cause analysis |
| `mp-code-review` | Structured scout→review→fix pipeline |
| `mp-docs` | Initialize, update, and summarize documentation |
| `mp-docs-seeker` | Search library/framework documentation via Context7 |
| `mp-git` | Conventional commits, security scanning, PR creation |
| `mp-brainstorm` | Structured ideation with approach comparison |
| `mp-scout` | Fast codebase exploration using parallel agents |
| `mp-research` | Comprehensive technical research and evaluation |
| `mp-sequential-thinking` | Step-by-step analysis for complex problems |

### Agents (6)

| Agent | Description |
|-------|-------------|
| `mp-planner` | Research + plan phases (Opus model) |
| `mp-code-reviewer` | Review code changes and PRs (infer: true) |
| `mp-debugger` | Root cause analysis and debugging (infer: true) |
| `mp-researcher` | Deep technical research (infer: true, Haiku model) |
| `mp-multimodal` | UI/screenshot analysis, visual debugging (infer: true, Gemini model) |
| `mp-worker` | Category-aware phase orchestrator — delegates phases to sub-agents by category |

### Hooks

All hooks merged in `hooks.json` (security, audit, subagent lifecycle monitoring).

## Category System

Plan phases are tagged with work categories that map to optimized models. `mp-worker` reads the category and dispatches to the right sub-agent automatically.

| Category | Default Model | Agent | Use Case |
|----------|---------------|-------|----------|
| `visual-engineering` | `gemini-3-pro-preview` | `mp-multimodal` | Frontend, UI/UX, design |
| `deep` | `gpt-5.3-codex` | `general-purpose` | Autonomous problem-solving |
| `artistry` | `gemini-3-pro-preview` | `general-purpose` | Creative solutions |
| `quick` | `claude-haiku-4.5` | `task` | Trivial tasks, single-file |
| `general` | `claude-sonnet-4.6` | `general-purpose` | Standard work |
| `complex` | `claude-opus-4.6` | `general-purpose` | Multi-system coordination |
| `writing` | `claude-sonnet-4.6` | `general-purpose` | Documentation, prose |

Customize via `.github/my-copilot.jsonc` (project) or `~/.copilot/my-copilot.jsonc` (global).

## Workflow

Two-step automated workflow:

```
User → mp-plan   (auto: brainstorm → research → plan → validate)
         └── opt-out: --skip-brainstorm to skip brainstorm step

User → mp-execute (auto: implement → test → fix → review → docs → commit)
         └── opt-out: --skip-post to skip post-execution chain
```

## MCP Setup (Context7)

The plugin ships with `.mcp.json` pre-configured for the Context7 MCP server. You need to add your own API key.

1. Get an API key from https://context7.com
2. Edit `.mcp.json` and replace `YOUR_CONTEXT7_API_KEY` with your key

```bash
# After installing the plugin, find the installed location:
copilot plugin list
# Edit .mcp.json in the installed plugin directory
```

## Requirements

- GitHub Copilot CLI
- Python 3 (for hook scripts)
- Node.js + npx (for Context7 MCP server, optional)

## Documentation

- [Getting Started](docs/getting-started.md)
- [Architecture](docs/architecture.md)
- [Flow Diagram](docs/my-copilot-flow.md)
- [Code Standards](docs/code-standards.md)

## License

MIT

