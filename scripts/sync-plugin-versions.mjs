#!/usr/bin/env node
/**
 * Syncs versions across all version-bearing files whenever a plugin bumps.
 * Runs automatically after `changeset version` via the npm `version` script.
 *
 * For each plugin it syncs:
 *   package.json  ──► plugin.json          (version field)
 *   package.json  ──► marketplace.json     (plugins[].version)
 *   package.json  ──► README.md            (version column in the Plugins table)
 *
 * marketplace.json metadata.version tracks the base my-copilot plugin version.
 *
 * IMPORTANT: skill counts in plugin.json / marketplace.json descriptions are
 * NOT auto-synced — update them manually whenever skills are added or removed.
 */
import { readFileSync, writeFileSync } from 'fs';
import { join, dirname } from 'path';
import { fileURLToPath } from 'url';

const __dirname = dirname(fileURLToPath(import.meta.url));
const root = join(__dirname, '..');

const plugins = [
  'my-copilot',
  'my-copilot-backend',
  'my-copilot-frontend',
  'my-copilot-devops',
  'my-copilot-mobile',
];

// ── 1. Sync package.json → plugin.json ────────────────────────────────────
const versions = {};
for (const plugin of plugins) {
  const pkgPath = join(root, plugin, 'package.json');
  const pluginJsonPath = join(root, plugin, 'plugin.json');

  const pkg = JSON.parse(readFileSync(pkgPath, 'utf8'));
  const pluginJson = JSON.parse(readFileSync(pluginJsonPath, 'utf8'));
  versions[plugin] = pkg.version;

  if (pluginJson.version !== pkg.version) {
    pluginJson.version = pkg.version;
    writeFileSync(pluginJsonPath, JSON.stringify(pluginJson, null, 2) + '\n');
    console.log(`  Synced ${plugin}/plugin.json → v${pkg.version}`);
  }
}

// ── 2. Sync package.json → marketplace.json ───────────────────────────────
const marketplacePath = join(root, '.github/plugin/marketplace.json');
const marketplace = JSON.parse(readFileSync(marketplacePath, 'utf8'));
let marketplaceChanged = false;

for (const entry of marketplace.plugins) {
  const v = versions[entry.name];
  if (v && entry.version !== v) {
    entry.version = v;
    marketplaceChanged = true;
    console.log(`  Synced marketplace.json ${entry.name} → v${v}`);
  }
}

// metadata.version tracks the base my-copilot plugin version
if (marketplace.metadata.version !== versions['my-copilot']) {
  marketplace.metadata.version = versions['my-copilot'];
  marketplaceChanged = true;
  console.log(`  Synced marketplace.json metadata.version → v${versions['my-copilot']}`);
}

if (marketplaceChanged) {
  writeFileSync(marketplacePath, JSON.stringify(marketplace, null, 2) + '\n');
}

// ── 3. Sync package.json → README.md version column ──────────────────────
const readmePath = join(root, 'README.md');
let readme = readFileSync(readmePath, 'utf8');
let readmeChanged = false;

for (const plugin of plugins) {
  const v = versions[plugin];
  // Match table rows like: | [my-copilot-xxx](./my-copilot-xxx/) | ... | 0.x.x   |
  const pattern = new RegExp(
    `(\\| \\[${plugin}\\]\\([^)]+\\)\\s*\\|[^|]+\\|\\s*)\\d+\\.\\d+\\.\\d+(\\s*\\|)`,
    'g'
  );
  const updated = readme.replace(pattern, `$1${v}$2`);
  if (updated !== readme) {
    readme = updated;
    readmeChanged = true;
    console.log(`  Synced README.md ${plugin} → v${v}`);
  }
}

if (readmeChanged) {
  writeFileSync(readmePath, readme);
}
