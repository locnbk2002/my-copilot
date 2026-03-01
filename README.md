# locnbk2002-marketplace

A GitHub Copilot CLI plugin marketplace.

## Available Plugins

| Plugin                      | Description                                   | Version |
| --------------------------- | --------------------------------------------- | ------- |
| [my-copilot](./my-copilot/) | AI engineering workflow — 12 skills, 6 agents | 0.0.2   |

## Installation

### Add Marketplace

```sh
copilot plugin marketplace add locnbk2002/locnbk2002-marketplace
```

### Install a Plugin

```sh
copilot plugin install locnbk2002-marketplace@my-copilot
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
