## Post-Execution Auto Chain

Runs automatically after all phases complete (default ON).
Each step dispatches as a fresh sub-agent via `task` tool — keeps main session context lean.

### --skip-post Confirmation

Before skipping, prompt user via `ask_user`:

> "Skipping post-chain (test, fix, review, docs, commit). No automated verification. Continue?"
> Options: ["Yes, skip post-chain", "No, run post-chain"]

If user selects "No": run chain normally. Only skip if user explicitly confirms.

### Step 0: Collect Changed Files + Final State Sync

Before dispatching chain:

- Gather changed files: `bash: git diff --name-only HEAD~{N}` (N = commits in this execution) OR aggregate "files modified" from worker reports
- Store as `changed_files` list (passed to each sub-agent as context)
- Update plan.md frontmatter: `status: completed` if all phases done, `status: in-progress` if any blocked
- Verify all completed phase rows show `Done` in the Status column

(Per-phase sync already handled during execution by step 3.5 in execution-workflow.md)

### Step 1: Test

**Skip if:** `--skip-tests` or `--skip-post`

Dispatch:

```
task(prompt="Run test suite. Work context: {project_root}. Changed files: {changed_files}. Do not stage or commit anything.", mode="background")
```

Collect: `read_agent(agent_id, wait=True, timeout=300)`

**On pass:** skip Step 2, proceed to Step 3
**On failure:** proceed to Step 2

### Step 2: Fix (Conditional)

Only runs if Step 1 found test failures.

**Skip if:** `--skip-tests` or `--skip-post`

Dispatch:

```
task(prompt="Fix failing tests. Failures: {test_output}. Work context: {project_root}. Do not commit.", mode="background")
```

Collect: `read_agent(agent_id, wait=True, timeout=300)`

- Max 2 attempts; after each fix re-dispatch a test sub-agent (Step 1 pattern)
- If still failing after 2 attempts: log "⚠️ Tests still failing after 2 fix attempts — manual intervention required", continue to Step 3

### Step 3: Review

**Skip if:** `--skip-review` or `--skip-post`

Dispatch:

```
task(agent_type="code-reviewer", prompt="Review changed files: {changed_files}. Work context: {project_root}.", mode="background")
```

Collect: `read_agent(agent_id, wait=True, timeout=300)`

**On failure:** log warning, continue to Step 4

### Step 4: Docs

**Skip if:** `--skip-post`

Dispatch:

```
task(prompt="Update docs if APIs/interfaces/public behavior changed. Changed files: {changed_files}. Work context: {project_root}.", mode="background")
```

Collect: `read_agent(agent_id, wait=True, timeout=300)`

**On failure:** log warning, continue to Step 5

### Step 5: Git Commit (Ask User First)

**Skip if:** `--skip-commit` or `--skip-post`

Before dispatching, ask user:

```
ask_user(
  question="Execution complete. Commit changes?",
  choices=["Yes, commit now", "No, skip commit"]
)
```

- If "No": log "⚠️ Commit skipped — run `git commit` manually to commit", continue to Step 6
- If "Yes": dispatch:

```
task(prompt="Create atomic conventional commit for changes in {project_root}. Do NOT stage .env, credentials, or secret files.", mode="background")
```

Collect: `read_agent(agent_id, wait=True, timeout=300)`

**On failure:** log warning, continue to Step 6

### Step 6: Summary Report

Runs in main session (output only — no file edits):

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
- Failures log a ⚠️ warning with the error, then continue to next step
- If `task` dispatch itself fails (tool error): log warning, continue to next step
- If `read_agent` times out (>300s): log "⚠️ Step {N} timed out after 300s", continue
- Never abort the chain mid-execution (except on explicit user cancellation)
- Only `--skip-post` (confirmed), `--skip-tests`, `--skip-review`, `--skip-commit` flags can prevent steps from running
