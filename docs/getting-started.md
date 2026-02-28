# Getting Started

## Requirements

- GitHub Copilot CLI
- Python 3 (for hook scripts)
- Node.js + npx (for Context7 MCP, optional)

## Installation

### Option 1: Marketplace (recommended)

```bash
copilot plugin marketplace add locnbk2002/my-copilot
copilot plugin install my-copilot@my-copilot
```

### Option 2: Direct GitHub

```bash
copilot plugin install locnbk2002/my-copilot
```

### Option 3: Local (development)

```bash
git clone https://github.com/locnbk2002/my-copilot
copilot plugin install ./my-copilot
```

## MCP Setup (Context7 — optional)

Context7 enables the `mp-docs-seeker` skill to look up library/framework documentation.

1. Get an API key from https://context7.com
2. Find the installed plugin directory: `copilot plugin list`
3. Edit `.mcp.json` and replace `YOUR_CONTEXT7_API_KEY` with your key

## Verify Installation

After installing, confirm skills and agents are available:

```bash
copilot skill list        # Should show mp-* skills
copilot agent list        # Should show mp-planner, mp-debugger, etc.
```

## Using Skills

Invoke any skill via the Copilot CLI chat:

```
Use the skill tool to invoke "mp-plan" skill, then help me plan: <feature description>
```

## Using Agents

Agents are invoked automatically by skills, or directly via the `task` tool in code.

## Hook Configuration

Hooks run automatically on tool use and session events. No configuration needed — `hooks.json` is loaded by the plugin. Hook scripts require Python 3 on `PATH`.
