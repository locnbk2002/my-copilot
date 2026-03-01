# Getting Started

## Requirements

- GitHub Copilot CLI
- Python 3 (for hook scripts)
- Node.js + npx (for Context7 MCP, optional)

## Installation

### Option 1: Marketplace (recommended)

```bash
copilot plugin marketplace add locnbk2002/locnbk2002-marketplace
copilot plugin install locnbk2002-marketplace@my-copilot
```

### Option 2: Direct GitHub

```bash
copilot plugin install locnbk2002/my-copilot
```

### Option 3: Local (development)

```bash
git clone https://github.com/locnbk2002/my-copilot
cd my-copilot
copilot plugin install ./my-copilot
```

## MCP Setup (Context7 — optional)

Context7 enables the `docs-seeker` skill to look up library/framework documentation.

1. Get an API key from https://context7.com
2. Find the installed plugin directory: `copilot plugin list`
3. Edit `.mcp.json` and replace `YOUR_CONTEXT7_API_KEY` with your key

## Verify Installation

After installing, confirm skills and agents are available:

```bash
copilot skill list        # Should show skills
copilot agent list        # Should show planner, debugger, etc.
```

## Using Skills

Invoke any skill via the Copilot CLI chat:

```
Use the skill tool to invoke "plan" skill, then help me plan: <feature description>
```

## Using Agents

Agents are invoked automatically by skills, or directly via the `task` tool in code.

## Hook Configuration

Hooks run automatically on tool use and session events. No configuration needed — `hooks.json` is loaded by the plugin. Hook scripts require Python 3 on `PATH`.

## Category Configuration

Plan phases are tagged with work categories. `worker` resolves each category to an optimized model and agent type. You can override the defaults via config files.

### Config File Locations

- **Project-level**: `.github/my-copilot.jsonc` (add to your project repo)
- **User-level (global)**: `~/.copilot/my-copilot.jsonc` (applies to all projects)

Project config takes precedence over user config; user config takes precedence over built-in defaults.

### Example Config

```jsonc
{
  "categories": {
    // Override the 'quick' category to use a faster model
    "quick": {
      "model": "gpt-5-mini",
      "agent_type": "task"
    },
    // Override 'complex' to use a premium model
    "complex": {
      "model": "claude-opus-4.6",
      "agent_type": "general-purpose"
    }
  }
}
```

### Built-in Category Defaults

| Category | Model | Agent | When to Use |
|----------|-------|-------|-------------|
| `visual-engineering` | `gemini-3-pro-preview` | `multimodal` | Frontend, UI/UX, design |
| `deep` | `gpt-5.3-codex` | `general-purpose` | Autonomous problem-solving |
| `artistry` | `gemini-3-pro-preview` | `general-purpose` | Creative solutions |
| `quick` | `claude-haiku-4.5` | `task` | Trivial, single-file changes |
| `general` | `claude-sonnet-4.6` | `general-purpose` | Standard work |
| `complex` | `claude-opus-4.6` | `general-purpose` | Multi-system coordination |
| `writing` | `claude-sonnet-4.6` | `general-purpose` | Documentation, prose |
