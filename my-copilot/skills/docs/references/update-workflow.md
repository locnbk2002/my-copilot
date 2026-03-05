## Documentation Update Workflow

### Change Detection

1. **Get changed files:**
   ```bash
   git diff --name-only main..HEAD
   # or for recent changes:
   git diff --name-only HEAD~5
   ```

2. **Categorize changes:**
   | File Pattern | Docs to Update |
   |-------------|----------------|
   | `src/api/**`, `routes/**` | api-reference.md |
   | `package.json`, `requirements.txt` | getting-started.md |
   | `src/`, major refactor | architecture.md |
   | New feature, config changes | README.md |
   | `Dockerfile`, CI config | deployment-guide.md |

3. **Read changed files** to understand what changed

### Update Strategy

- **Additive**: Add new sections for new features/APIs
- **Corrective**: Fix outdated info (changed configs, renamed functions)
- **Removal**: Remove docs for deleted features (rare — confirm with user first)

### Rules

- Use `edit` tool (never `create` for existing docs)
- Preserve existing structure and formatting
- Don't rewrite entire docs — update only affected sections
- If unsure what to update, ask user via `ask_user`
