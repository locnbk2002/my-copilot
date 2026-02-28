# Category Defaults

Category-to-model mapping used by `mp-worker` to delegate plan phases to sub-agents.

## Config Resolution Order (highest wins)

```
.github/my-copilot.jsonc      ← project-level (version-controlled)
    ↓
~/.copilot/my-copilot.jsonc   ← user-level (personal overrides)
    ↓
Built-in defaults (below)     ← fallback
```

## Built-in Category Defaults

| Category | Model | Agent Type | Purpose |
|----------|-------|------------|---------|
| `visual-engineering` | `gemini-3-pro-preview` | `mp-multimodal` | Frontend, UI/UX, design, styling, animation |
| `deep` | `gpt-5.3-codex` | `general-purpose` | Autonomous problem-solving, complex multi-file |
| `artistry` | `gemini-3-pro-preview` | `general-purpose` | Creative, unconventional solutions |
| `quick` | `claude-haiku-4.5` | `task` | Trivial tasks, typos, single-file edits |
| `general` | `claude-sonnet-4.6` | `general-purpose` | Standard moderate-effort work |
| `complex` | `claude-opus-4.6` | `general-purpose` | Multi-system, architecture decisions |
| `writing` | `claude-sonnet-4.6` | `general-purpose` | Docs, README, prose, technical writing |

## How mp-worker Resolves Config

1. Check if `.github/my-copilot.jsonc` exists → read it via `view` tool
2. Check if `~/.copilot/my-copilot.jsonc` exists → read it via `bash: cat ~/.copilot/my-copilot.jsonc`
3. Merge: project config overrides user config overrides built-in defaults
4. For each plan phase, look up `Category` field → resolve `model` + `agent_type`
5. Dispatch: `task(agent_type=resolved_agent, model=resolved_model, prompt=phase_content)`

## Category Auto-Tagging Rules (for mp-plan)

When the planner creates phases, auto-select category based on phase content:

| Phase Content Signals | Category |
|-----------------------|----------|
| UI, CSS, component, layout, design, frontend, styling | `visual-engineering` |
| Architecture, system design, multi-file, complex logic | `complex` |
| Creative, experimental, unconventional | `artistry` |
| Typo, config, single file, minor fix | `quick` |
| Test, build, lint, database, API implementation | `general` |
| Autonomous exploration, goal-driven, open-ended | `deep` |
| Docs, README, changelog, technical writing, prose | `writing` |
| Default (no clear signal) | `general` |

## Config Schema

```jsonc
{
  "categories": {
    "<category-name>": {
      "description": "string (optional)",   // Human-readable purpose
      "model": "string (required)",          // Model ID
      "agent_type": "string (optional)"      // Sub-agent type (default: general-purpose)
    }
  }
}
```

## Customization Examples

### Override a category's model

```jsonc
// .github/my-copilot.jsonc
{
  "categories": {
    "quick": {
      "model": "claude-sonnet-4.6"   // Use Sonnet instead of Haiku for quick tasks
    }
  }
}
```

### Add a custom category

```jsonc
{
  "categories": {
    "data-engineering": {
      "description": "ETL pipelines, data modeling, SQL optimization",
      "model": "gpt-5.3-codex",
      "agent_type": "general-purpose"
    }
  }
}
```

### User-level global override

Create `~/.copilot/my-copilot.jsonc` with the same structure. Project config takes precedence.
