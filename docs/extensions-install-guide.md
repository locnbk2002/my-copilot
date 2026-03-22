# Extensions Install Guide

Extensions add custom tools, hooks, and event listeners to the Copilot CLI. They are **not installed like plugins** — there is no `copilot plugin install` command. Instead, extensions are file-based and auto-discovered by the CLI at startup.

## Extensions vs Plugins

|                | Plugins                               | Extensions                              |
| -------------- | ------------------------------------- | --------------------------------------- |
| Install method | `copilot plugin install <name>`       | Place file in `.github/extensions/`     |
| Scope          | Marketplace-distributed skills/agents | Local JS process (tools, hooks, events) |
| Language       | YAML/Markdown skill files             | JavaScript (`.mjs` only)                |
| Reload         | Restart CLI                           | `/reload` or `extensions_reload` tool   |

## How Extensions Are Discovered

The CLI scans two locations at startup:

1. **Project-scoped** — `.github/extensions/<name>/extension.mjs` at the **git root**
2. **User-scoped** — `~/.copilot/extensions/<name>/extension.mjs` (applies to all repos)

> ⚠️ The scan is **not recursive**. The `.github/extensions/` folder must be at the git root, not inside any subdirectory.

## File Structure

```
<git-root>/
└── .github/
    └── extensions/
        └── context-reporter/       ← subdirectory name = extension name
            └── extension.mjs       ← required entry point (must be .mjs)
```

## Installing an Extension

### Option 1 — Project-scoped (committed to repo)

1. Create the folder under the **git root**:
   ```sh
   mkdir -p .github/extensions/my-extension
   ```
2. Add `extension.mjs` (see skeleton below).
3. Reload:
   ```sh
   # In the CLI chat, type:
   /reload
   ```

### Option 2 — User-scoped (persists across all repos)

1. Create the folder:
   ```sh
   mkdir -p ~/.copilot/extensions/my-extension
   ```
2. Add `extension.mjs`.
3. Reload with `/reload`.

### Minimal `extension.mjs` skeleton

```js
import { joinSession } from "@github/copilot-sdk/extension";

const session = await joinSession({
  hooks: {
    onSessionStart: async () => {
      await session.log("my-extension loaded");
    },
  },
  tools: [],
});
```

- `@github/copilot-sdk` is **automatically resolved** — do not run `npm install`.
- Only ES module syntax is supported (`.mjs`, use `import`/`export`).

## Verifying the Extension Loaded

After `/reload`, the CLI lists all loaded extensions. You can also ask Copilot:

> "List loaded extensions"

A healthy extension shows `ready [project]` or `ready [user]` with a PID.

## Lifecycle

| Event                 | Behavior                                           |
| --------------------- | -------------------------------------------------- |
| CLI starts            | All extensions auto-discovered and launched        |
| `/clear` or `/reload` | Extensions stopped and re-launched                 |
| CLI exits             | Extensions receive SIGTERM, then SIGKILL after 5 s |
| Name collision        | Project extension shadows user extension           |

## Currently Installed Extensions

| Name               | Scope   | Purpose                                                  |
| ------------------ | ------- | -------------------------------------------------------- |
| `context-reporter` | project | Injects real context-window usage % after each tool call |
