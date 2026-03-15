#!/usr/bin/env node
/**
 * Syncs version from each plugin's package.json → plugin.json
 * Runs automatically after `changeset version` via the npm `version` script.
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
];

for (const plugin of plugins) {
  const pkgPath = join(root, plugin, 'package.json');
  const pluginJsonPath = join(root, plugin, 'plugin.json');

  const pkg = JSON.parse(readFileSync(pkgPath, 'utf8'));
  const pluginJson = JSON.parse(readFileSync(pluginJsonPath, 'utf8'));

  if (pluginJson.version !== pkg.version) {
    pluginJson.version = pkg.version;
    writeFileSync(pluginJsonPath, JSON.stringify(pluginJson, null, 2) + '\n');
    console.log(`  Synced ${plugin}/plugin.json → v${pkg.version}`);
  }
}
