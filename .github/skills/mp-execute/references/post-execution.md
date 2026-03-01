## Post-Execution Auto Chain

Runs automatically after all phases complete (unless `--skip-post`).

### Step 0: Final State Sync

Before starting post-execution chain:
- Update plan.md frontmatter: `status: completed` if all phases done, `status: in-progress` if any blocked
- Verify all completed phase rows show `Done` in the Status column

(Per-phase sync already handled during execution by step 3.5 in execution-workflow.md)

### Step 1: Test

Invoke `mp-test` skill to run the project test suite.

**Skip if:** `--skip-tests` or `--skip-post`
**On failure:** proceed to Step 2 (Fix)
**On pass:** skip Step 2, proceed to Step 3

### Step 2: Fix (Conditional)

Only runs if Step 1 found test failures.

Invoke `mp-fix` skill with the failing test output as context.
- Max 2 fix attempts
- After each fix: re-run tests to verify
- If still failing after 2 attempts: log warning "⚠️ Tests still failing after 2 fix attempts — manual intervention required", continue to Step 3

**Skip if:** `--skip-tests` or `--skip-post`

### Step 3: Review

Dispatch `task(agent_type="mp-code-reviewer")` targeting all files changed in this execution.

**Skip if:** `--skip-review` or `--skip-post`
**On failure:** log warning, continue to Step 4

### Step 4: Docs

Invoke `mp-docs` skill if implementation changed APIs, interfaces, or public behavior.

**Skip if:** `--skip-post`
**On failure:** log warning, continue to Step 5

### Step 5: Git Commit

Invoke `mp-git cm --atomic` for phase-aware atomic commits.

**Skip if:** `--skip-post`
**On failure:** log warning, continue to Step 6

### Step 6: Summary Report

Output to user:

```
## Execution Summary

### Phases Completed
- Phase 1: {name} ✅
- Phase 2: {name} ✅

### Files Modified/Created
- {file path} — {action}

### Post-Execution Chain
- Test: ✅ Passed (N tests) / ⚠️ Skipped / ❌ Failed
- Fix: ✅ Fixed / ⚠️ Skipped / ❌ Could not fix (manual intervention required)
- Review: ✅ No critical issues / ⚠️ Skipped / ❌ Critical findings (see review output)
- Docs: ✅ Updated / ⚠️ Skipped / ❌ Failed
- Git: ✅ Committed ({hash}) / ⚠️ Skipped / ❌ Failed

### Context Budget
{✅ Healthy / ⚠️ Heavy / 🔴 Critical} ({N} tool calls)
```

### Fault Tolerance Rules

- Each step runs independently regardless of previous step outcome
- Failures log a ⚠️ warning with the error, then continue
- Only `--skip-post`, `--skip-tests`, `--skip-review` flags can prevent steps from running
- Never abort the chain mid-execution (except on explicit user cancellation)
