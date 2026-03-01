## Review Workflow

### Diff Acquisition

```bash
# Unstaged changes (default)
git diff

# Staged changes
git diff --staged

# Branch diff
git diff main..HEAD

# Specific files
git diff -- src/auth.ts src/middleware.ts
```

### Scout Phase Details

Before sending to the reviewer, gather context:

1. **Changed functions**: Extract function names from diff
2. **Callers**: Use `grep` to find all callers of changed functions
3. **Related tests**: Check if tests exist for changed code
4. **Recent changes**: `git log --oneline -5 -- <changed_files>`

Format scout findings as:
```
## Scout Report
- Functions changed: [list]
- Callers found: [count] across [N] files
- Test coverage: [existing tests found / not found]
- Recent activity: [last N commits touching these files]
- Concerns: [list any red flags]
```

### Review Request Format

Send to code-reviewer agent:
```
Review these code changes.

## Diff
<paste diff>

## Scout Findings
<paste scout report>

## Project Conventions
- Follow YAGNI, KISS, DRY
- [any project-specific rules from copilot-instructions.md]

Focus on: bugs, security, logic errors. Skip style nitpicks.
```

### Verdict Logic

- If ANY Critical issue: ❌ NEEDS WORK (always)
- If `--strict` and ANY High issue: ❌ NEEDS WORK
- If only Medium/Low: ✅ PASS (with notes)
- If no issues: ✅ PASS

### Fix Loop Protocol

When issues need fixing:
1. Group issues by file
2. Fix highest severity first
3. After fixes, re-run ONLY the review (skip scout — context unchanged)
4. Max 2 iterations to prevent infinite loops
5. If still failing after 2 iterations, report to user
