## Phase Execution Algorithm

### Step 1: Load Phase

- Read the phase file (e.g., `phase-01-setup.md`)
- Extract: objectives, tasks, acceptance criteria, estimated complexity
- If the phase file contains code snippets/pseudocode, use them as implementation guidance

### Step 2: Dispatch Strategy

**Default (recommended) — Category-aware dispatch:**
- Check if phase has `Category` field in its Overview section
- If yes: Dispatch `task(agent_type="worker", mode="background")` with plan directory path and work context → get `agent_id`, then `read_agent(agent_id, wait=True, timeout=300)`
  - worker handles: config resolution, category→agent mapping, wave execution, fresh context
  - Main session does NOT edit any files — delegates entirely to worker
- If no Category field OR `--direct` flag: fall through to Legacy Direct Mode below

**Legacy Direct Mode (`--direct` or no Category):**
- **Simple** (< 3 files, straightforward): Execute directly with edit/create tools
- **Medium** (3-10 files, requires analysis): Dispatch explore subagents first, then implement
- **Complex** (10+ files, architectural): Break into sub-tasks, dispatch parallel general-purpose subagents

**Rule:** Default (non-direct) path NEVER edits files in main session context. All editing happens in sub-agents.

### Step 3: Implementation Pattern

For each task in the phase:

1. Read relevant source files
2. Plan the change (mentally or via sequential-thinking)
3. Make the change (edit/create)
4. Verify the change (run affected tests)

### Step 3.5: State Sync

After worker returns (or after direct mode implementation):

1. Read worker report → extract per-phase completion status
2. For each completed phase:
   - Edit `plan.md`: find phase row in Phases table, update Status column from `Pending` to `Done`
   - Edit `phase-XX-*.md`: find each todo checkbox in Todo List, mark `- [ ]` → `- [x]`
3. For blocked phases: update Status to `Blocked` in plan.md, note reason in phase file
4. State sync is idempotent — safe to run multiple times

### Step 4: Verification Gate

After all tasks complete:

- Run project test suite via `bash` tool
- Run linter/typecheck if configured
- Check for regressions
- If any fail → debug with debugger agent or fix skill
- Max 3 retry attempts before marking phase as blocked

### Step 5: Review Gate (optional)

- Dispatch `task(agent_type="code-reviewer")` on `git diff`
- Address Critical/High severity findings
- Skip Medium/Low unless user requests or `--strict` is set

### Step 6: Finalization

- Update SQL todo status to 'done'
- Log completion summary
- Move to next phase or report completion
