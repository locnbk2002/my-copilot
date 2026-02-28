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
| `mp-plan` | Plan implementations with research, red-team, and validation phases |
| `mp-execute` | Execute plans phase-by-phase with test/review gates |
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

### Agents (4)

| Agent | Description |
|-------|-------------|
| `mp-planner` | Research + plan phases (Opus model) |
| `mp-code-reviewer` | Review code changes and PRs (infer: true) |
| `mp-debugger` | Root cause analysis and debugging (infer: true) |
| `mp-researcher` | Deep technical research (infer: true, Haiku model) |

### Hooks

All hooks merged in `hooks.json` (security, audit, subagent lifecycle monitoring).

## Workflow

```
mp-brainstorm → mp-plan → mp-execute → mp-test → mp-fix → mp-code-review → mp-docs → mp-git
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
- [Code Standards](docs/code-standards.md)

## License

MIT

