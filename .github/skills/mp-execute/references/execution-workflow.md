## Phase Execution Algorithm

### Step 1: Load Phase

- Read the phase file (e.g., `phase-01-setup.md`)
- Extract: objectives, tasks, acceptance criteria, estimated complexity
- If the phase file contains code snippets/pseudocode, use them as implementation guidance

### Step 2: Complexity Assessment

- **Simple** (< 3 files, straightforward changes): Execute directly
- **Medium** (3-10 files, requires analysis): Dispatch explore subagents first, then implement
- **Complex** (10+ files, architectural changes): Break into sub-tasks, dispatch parallel subagents

### Step 3: Implementation Pattern

For each task in the phase:

1. Read relevant source files
2. Plan the change (mentally or via mp-sequential-thinking)
3. Make the change (edit/create)
4. Verify the change (run affected tests)

### Step 4: Verification Gate

After all tasks complete:

- Run project test suite via `bash` tool
- Run linter/typecheck if configured
- Check for regressions
- If any fail → debug with mp-debugger agent or mp-fix skill
- Max 3 retry attempts before marking phase as blocked

### Step 5: Review Gate (optional)

- Dispatch `task(agent_type="mp-code-reviewer")` on `git diff`
- Address Critical/High severity findings
- Skip Medium/Low unless user requests or `--strict` is set

### Step 6: Finalization

- Update SQL todo status to 'done'
- Log completion summary
- Move to next phase or report completion
