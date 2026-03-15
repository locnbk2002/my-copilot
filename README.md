# my-copilot

A GitHub Copilot CLI plugin marketplace.

## Available Plugins

| Plugin                                        | Description                                                    | Version |
| --------------------------------------------- | -------------------------------------------------------------- | ------- |
| [my-copilot](./my-copilot/)                   | AI engineering workflow — 15 skills, 6 agents                  | 0.1.0   |
| [my-copilot-frontend](./my-copilot-frontend/) | Frontend domain — 8 skills (React, Next.js, UI/UX, TanStack)   | 0.1.0   |
| [my-copilot-backend](./my-copilot-backend/)   | Backend domain — 4 skills (APIs, databases, auth, payments)    | 0.1.0   |
| [my-copilot-devops](./my-copilot-devops/)     | DevOps domain — 2 skills (Docker, K8s, Cloudflare, GCP, CI/CD) | 0.1.0   |

## Installation

### Add Marketplace

```sh
copilot plugin marketplace add locnbk2002/my-copilot
```

### Install a Plugin

```sh
copilot plugin install my-copilot@my-copilot
```

## Adding a New Plugin

1. Create a directory: `my-new-plugin/`
2. Add `.github/plugin/plugin.json` with the plugin manifest
3. Add skills in `.github/skills/`, agents in `.github/agents/`
4. Register the plugin in `.github/plugin/marketplace.json` plugins array
5. Add a row to the [Available Plugins](#available-plugins) table above

See [my-copilot/README.md](./my-copilot/README.md) for a reference plugin structure.

## License

MIT
