## After All Phases Complete

### 1. Documentation

If implementation changed APIs or behavior:

- Invoke `mp-docs` skill (if available)
- Or update README.md, relevant docs manually

### 2. Git Commit

If changes are ready:

- Invoke `mp-git` skill (if available)
- Or stage, write conventional commit message, commit

### 3. Summary Report

Output to user:

- Phases completed (with links to phase files)
- Files modified/created
- Tests passing (count)
- Known issues or follow-ups

### 4. Plan Status

Update plan.md frontmatter:

- `status: completed`
- Record completion date
