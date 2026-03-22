# Runtime Awareness

Monitor context window utilization in real-time to optimize copilot-cli sessions.

## Overview

Runtime awareness provides visibility into context window usage to guide compaction decisions and session management.

## How to Check Context Usage

### Option 1: context-reporter Extension (Recommended — Automatic)

Injects real context usage into conversation automatically after each model call. No manual check needed.

**Install:**
```bash
mkdir -p ~/.copilot/extensions/context-reporter
cp .github/extensions/context-reporter/extension.mjs ~/.copilot/extensions/context-reporter/
# Restart session or run /reload
```

**Output** (in `<usage-awareness>` block after each tool call):
- `Context: 45% (90K/200K tokens)` — normal
- `Context: 72% [WARNING] (144K/200K tokens) — consider /compact`
- `Context: 93% [CRITICAL] (186K/200K tokens) — start fresh session`

Data source: `session.usage_info` streaming event — exact, zero latency, session-scoped.

---

### Option 2: statusLine `context` Module (Experimental)

Requires experimental mode (`--experimental` flag or `/experimental` command):

```
copilot --experimental
```

In the status bar, enable the `context` module to see real-time context %.

The statusLine is configurable via your copilot-cli config. Built-in modules include:
`workDir` · `gitBranch` · `model` · **`context`** · `speed` · `cost` · `duration` · `lines`

### Option 3: `/context` Slash Command

Run `/context` inside any copilot session to get a context visualization on demand. No setup required.

---

## Thresholds and Actions

### Context Window

| Utilization | Status   | Action                                |
| ----------- | -------- | ------------------------------------- |
| < 70%       | Normal   | Continue                              |
| 70–80%      | Warning  | Plan compaction strategy              |
| 80–90%      | High     | Execute compaction                    |
| > 90%       | Critical | Immediate compaction or session reset |

---

## Compaction Strategies

When context approaches limits:

1. **Summarize** — ask the model to compress conversation history into a compact summary
2. **Externalize** — write intermediate results to files; reference rather than repeat
3. **Sub-agent isolation** — delegate subtasks to fresh sub-agents with scoped context
4. **Selective loading** — load only relevant reference files, not entire codebases

---

## Configuration: statusLine `context` Module

To set up the `context` module in your statusLine config:

```json
{
  "statusLine": {
    "modules": ["context", "model", "gitBranch"]
  }
}
```

See copilot-cli experimental docs for full statusLine configuration options.

---

## Recommendations by Session Phase

| Phase         | Context % | Recommended Action                     |
| ------------- | --------- | -------------------------------------- |
| Early session | 0–50%     | Load all needed context upfront        |
| Mid session   | 50–70%    | Be selective about what you load       |
| Late session  | 70–80%    | Summarize history, externalize results |
| Near limit    | > 80%     | Sub-agent delegation, compaction       |
| Critical      | > 90%     | Session reset with summarized handoff  |
