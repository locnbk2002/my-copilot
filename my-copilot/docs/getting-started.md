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
cd my-copilot
copilot plugin install ./my-copilot
```

## Status Line Setup (optional)

The plugin ships a custom status line script that displays real-time session info:

```
🌿 main | 🪟 🟢 ████░░░░░░ 42% | ⚡ 5 req | 📝 +10/-3
```

**What each segment shows:**

| Segment | Description |
|---------|-------------|
| `🌿 <branch>` | Current git branch |
| `🤖 <model>` | Active LLM model |
| `🪟 🟢/🟡/🔴 <bar> <pct>%` | Context window usage (green < 50%, yellow < 80%, red ≥ 80%) |
| `⚡ <n> req` | Premium requests used this session |
| `📝 +<n>/-<n>` | Lines added/removed (hidden when both are 0) |

### Prerequisites

The script requires `jq` for JSON parsing. If `jq` is not on your `PATH`, install it:

```bash
# Option A: package manager (requires root)
sudo apt-get install -y jq        # Debian/Ubuntu
brew install jq                   # macOS

# Option B: single static binary (no root needed)
mkdir -p ~/.local/bin
curl -sL https://github.com/jqlang/jq/releases/download/jq-1.7.1/jq-linux-amd64 \
  -o ~/.local/bin/jq && chmod +x ~/.local/bin/jq
```

### One-time config

After installing the plugin, add the following to `~/.copilot/config.json`:

```json
{
  "status_line": {
    "type": "command",
    "command": "~/.copilot/installed-plugins/my-copilot/my-copilot/scripts/status_line.sh"
  }
}
```

> **Note:** The script path matches the default plugin install location. If you installed to a custom path, adjust accordingly.

The script is updated automatically whenever you run `copilot plugin update my-copilot`.

---

## MCP Setup (Context7 — optional)

Context7 enables the `docs-seeker` skill to look up library/framework documentation.

1. Get an API key from <https://context7.com>
2. Find the installed plugin directory: `copilot plugin list`
3. Edit `.mcp.json` and replace `YOUR_CONTEXT7_API_KEY` with your key

## Verify Installation

After installing, confirm skills and agents are available:

```
/skills list
/agents list
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

## Execution & Wave-Based Dispatch

When running `execute`:

1. **Waves** — Phases are executed in dependency-sorted waves (parallel-safe groups)
2. **Fresh Worker per Wave** — Each wave dispatches a fresh `worker` sub-agent with only that wave's phases
3. **Per-Phase Delegation** — Worker dispatches fresh sub-agent per phase based on phase category
4. **Auto Post-Chain** — After all phases complete: test, fix (if needed), review, docs update, git commit (default ON; use `--skip-post` to opt-out)

### Category Configuration

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
      "agent_type": "task",
    },
    // Override 'complex' to use a premium model
    "complex": {
      "model": "claude-opus-4.6",
      "agent_type": "general-purpose",
    },
  },
}
```

### Built-in Category Defaults

| Category             | Model                  | Agent             | When to Use                  |
| -------------------- | ---------------------- | ----------------- | ---------------------------- |
| `visual-engineering` | `gemini-3-pro-preview` | `multimodal`      | Frontend, UI/UX, design      |
| `deep`               | `gpt-5.3-codex`        | `general-purpose` | Autonomous problem-solving   |
| `artistry`           | `gemini-3-pro-preview` | `general-purpose` | Creative solutions           |
| `quick`              | `claude-haiku-4.5`     | `task`            | Trivial, single-file changes |
| `general`            | `claude-sonnet-4.6`    | `general-purpose` | Standard work                |
| `complex`            | `claude-opus-4.6`      | `general-purpose` | Multi-system coordination    |
| `writing`            | `claude-sonnet-4.6`    | `general-purpose` | Documentation, prose         |
