## Phase Execution Algorithm (Wave-Based)

Main execute session reads only plan.md phase table — never full phase file content.
Each wave dispatches a fresh worker sub-agent with only that wave's phases.

---

### Step 1: Load Plan & Compute Waves

```
1. Read plan.md Phases table ONLY (Status + Depends On columns)
   - Do NOT read individual phase-XX-*.md files in main session
2. Skip phases with Status = "Done"
3. Build dependency graph:
   - From plan.md "Depends On" column
   - Also: SELECT todo_id, depends_on FROM todo_deps (if SQL available)
   - Build adjacency list: phase → [dependency phases]
4. Compute waves:
   - Wave 1: phases with no pending dependencies (or all deps Done)
   - Wave N+1: phases whose only remaining pending deps are in Waves 1..N
5. Validate: if circular dependency detected → report error, STOP execution
```

**Output:** ordered list of waves, e.g. `[[1,2,3], [4,5], [6]]`

---

### Step 2: Dispatch Wave

For each wave (execute waves in order; never skip ahead):

```
1. For each phase in wave:
   sql: UPDATE todos SET status = 'in_progress' WHERE id = 'phase-XX'

2. If wave size > 5 phases: split into sub-waves of max 5; dispatch sub-waves sequentially

3. Dispatch: task(
     agent_type = "worker",
     mode = "background",
     description = "Execute wave: phases {N,M,...}",
     prompt = """
       Execute these plan phases. Each phase is independent within this wave.

       Plan directory: <plan_dir>
       Work context: <project_root>
       Reports: <plan_dir>/reports/
       Phases to execute (this wave only): <comma-separated phase numbers>

       ## Dispatch Instructions
       - Read only the listed phase-XX-*.md files from the plan directory
       - Dispatch each phase as a fresh background sub-agent (no shared context between phases)
       - Do NOT read or reference phases outside this list
       - Report completion status per phase

       ## Previous Wave Output (optional — pass only if >0 waves completed)
       Files modified in prior waves (for conflict awareness, max 20 lines):
       <brief list of files modified so far, if any>
     """
   ) → returns agent_id

4. Collect result: read_agent(agent_id, wait=True, timeout=300)
```

**`--phase N` flag:** skip wave computation; dispatch single worker with `phases: N` only.

**Legacy `--direct` mode:** skip worker; use complexity-based direct execution (see SKILL.md Complexity Assessment).

---

### Step 3: State Sync (After Each Wave)

After worker returns for a wave:

```
1. Parse worker execution report → extract per-phase completion status

2. For each completed phase:
   - Edit plan.md: find phase row in Phases table, change Status Pending → Done
     (use exact string match on the phase row)
   - Edit phase-XX-*.md: mark todo checkboxes - [ ] → - [x]
   - sql: UPDATE todos SET status = 'done' WHERE id = 'phase-XX'

3. For blocked phases:
   - Edit plan.md: update Status to Blocked
   - sql: UPDATE todos SET status = 'blocked' WHERE id = 'phase-XX'
   - Note reason in phase file if available

4. Track: append completed phase numbers to "files modified so far" list
   (to pass as optional context to next wave dispatch — max 20 lines)
```

State sync is idempotent — safe to run multiple times.

---

### Step 4: Budget Check (Every 3 Phases)

After syncing state, if `completed_count % 3 == 0`:

```
1. bash: wc -l < logs/tools.jsonl 2>/dev/null || echo 0
2. Evaluate:
   - < 200 tool calls  → ✅ Healthy, continue
   - 200–400 tool calls → ⚠️ Heavy — output warning, continue
   - > 400 tool calls  → 🔴 Critical — ask_user: recommend fresh session
3. If > 400 and remaining phases ≤ 2: suggest finishing current session
4. If > 400 and remaining phases > 2: strongly recommend fresh session + state sync ensures resume works
```

---

### Step 5: Next Wave or Post-Chain

```
If more waves remain AND no blocking errors:
  → Go to Step 2 with next wave

If all waves complete:
  → Load references/post-execution.md and run post-execution chain

If a wave is fully blocked (all phases blocked):
  → Report to user, stop execution
```

---

### Verification Gate (Per Wave)

After state sync (Step 3), before proceeding to next wave:

```
1. Run project test suite: bash (project test command)
2. Run linter/typecheck if configured
3. If any fail → invoke fix skill or debugger agent
4. Max 3 retry attempts before marking phase as blocked
5. Skip if --skip-tests flag set
```

---

### Resume Support

If starting a fresh session mid-execution:
1. Read plan.md Phases table — phases with Status = "Done" are already complete
2. Re-compute waves from remaining Pending/Blocked phases
3. Resume from Wave 1 of remaining phases
4. State sync-back (Step 3) ensures plan.md is always current
