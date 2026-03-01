## After All Phases Complete

### 0. Final State Sync

Ensure all phase statuses are reflected in plan files before wrapping up:
- Update plan.md frontmatter: `status: completed` if all phases done, `status: in-progress` if any blocked
- Verify all completed phase rows show `Done` in the Status column
- Record completion date in plan.md if desired

(Per-phase sync already handled during execution by step 3.5 in execution-workflow.md)

### 1. Documentation

If implementation changed APIs or behavior:

- Invoke `mp-docs` skill (if available)
- Or update README.md, relevant docs manually

### 2. Git Commit

If changes are ready:

- Invoke `mp-git cm --atomic` for phase-aware atomic commits
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
