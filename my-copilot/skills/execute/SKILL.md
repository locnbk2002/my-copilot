---
name: execute
description: "Execute implementation plans phase-by-phase with test/review gates. Use for plan execution, phased implementation, automated workflow with verification steps."
argument-hint: "[plan-path] [--phase N] [--skip-tests] [--skip-review] [--skip-commit] [--skip-post] [--direct]"
license: MIT
---

# Execution Engine

Execute implementation plans phase-by-phase with automated test and review gates.

## Invocation

```
execute [plan-path] [--phase N] [--skip-tests] [--skip-review] [--skip-commit] [--skip-post] [--direct]

Default: Execute all phases with category-aware delegation via worker
--phase N:      Execute only phase N
--skip-tests:   Skip test verification
--skip-review:  Skip code review gate
--skip-commit:  Skip only git commit step (runs test, fix, review, docs)
--skip-post:    Skip entire post-execution chain (requires confirmation via ask_user)
--direct:       Legacy mode — skip worker, execute phases directly (for plans without Category tags)
```

## When to Use

- After `plan` creates a plan with phases
- To systematically execute phased implementation
- For complex features requiring multiple steps with verification

## Core Workflow (Wave-Based Dispatch)

execute is a **thin orchestrator** — it reads plan.md, computes waves, dispatches per-wave, and tracks status. It NEVER edits files or reads full phase content in main context.

Load: `references/execution-workflow.md` for the detailed wave-dispatch algorithm.

**Main session context budget: aim for <20% usage throughout. Never accumulate phase file content.**

### Phase Execution Steps

1. **Load Plan** — Read ONLY `plan.md` phase table (Status + Depends On columns). Do NOT read individual phase-XX-*.md files.
2. **Compute Waves** — Build dependency graph from plan.md Phases table:
   - Wave 1: phases with no dependencies (or all deps Status = "Done")
   - Wave N+1: phases whose only pending deps are in Waves 1..N
   - Skip phases with Status = "Done"; validate: circular deps → error and stop
3. **Dispatch Wave** — For each wave (in dependency order):
   - Mark each phase in wave: `UPDATE todos SET status = 'in_progress' WHERE id = 'phase-XX'`
   - Dispatch ONE `task(agent_type="worker", mode="background")` per wave with:
     - `plan_dir`: path to plan directory
     - `phases`: comma-separated phase numbers for THIS WAVE ONLY
     - `work_context`: project root path
   - If wave has >5 phases: split into sub-waves of max 5 phases each
   - Collect result: `read_agent(agent_id, wait=True, timeout=300)`
   - **`--phase N` flag**: dispatch single worker for phase N only (skip wave computation)
   - **Legacy `--direct` mode**: skip worker; use complexity-based approach (see Complexity Assessment below)
4. **Sync Status** — After each wave completes, update plan.md Status column and phase-XX.md checkboxes (see State Sync-Back)
5. **Budget Check** (every 3 phases) — If `completed_count % 3 == 0`: run Context Budget Monitoring check
6. **Next Wave** — Proceed to next wave only after current wave fully completes and status is synced
7. **Post-Execution** — After all waves done: invoke post-execution chain (see Post-Execution section)

**RULE:** Steps 1–2, 4–7 happen in main context (reads plan.md ONLY, SQL updates, syncs). Step 3 (ALL implementation) happens in worker/sub-agent context ONLY.

## Dispatch Granularity

- Default: one worker per wave (worker handles parallelism within wave via fresh sub-agents per phase)
- If wave has >5 phases: split into sub-waves of 3-5 phases, dispatch sequentially
- `--phase N`: dispatch single worker for single phase N (skips wave computation)
- Worker receives ONLY its wave's phases — never the full plan or prior wave content

## State Sync-Back

After each phase (or wave) completes, sync status back to plan files:

1. **Update plan.md** — Find phase row in the Phases table, change `Pending` → `Done` (or `Blocked`)
   - Use `edit` tool with exact string match on the phase row
2. **Update phase file** — Mark completed todo checkboxes: `- [ ]` → `- [x]`
3. **Resume support** — On invocation, scan plan.md Phases table first:
   - Skip phases with Status = "Done" (already complete)
   - Resume from first "Pending" phase
   - Re-attempt "Blocked" phases only if user explicitly requests

State sync is idempotent — running it twice produces the same result.

## Context Budget Monitoring

After every 3 completed phases, check context health before dispatching the next wave.

### Budget Check Algorithm

1. Count tool calls: `bash: wc -l < logs/tools.jsonl 2>/dev/null || echo 0`
2. Evaluate threshold:

| Tool Calls | Status | Action |
|-----------|--------|--------|
| < 200 | ✅ Healthy | Continue normally |
| 200–400 | ⚠️ Heavy | Output: "Context is heavy ({N} tool calls). Consider running `/compact`." |
| > 400 | 🔴 Critical | `ask_user`: "Session has {N} tool calls. Recommend starting a fresh session. Continue?" |

3. If > 400 and remaining phases ≤ 2: suggest finishing in current session
4. If > 400 and remaining phases > 2: strongly recommend fresh session
5. Log result in execution summary: ✅/⚠️/🔴 with tool call count

### Integration with Existing Hooks

`auto-compact-reminder.py` fires every 100 tool calls at hook level (passive, log only).
This budget check is workflow-level — active and phase-aware. Both coexist:
- Hook: fires automatically, writes to `logs/compact-reminders.jsonl`
- Budget check: runs between phases, prompts user if critical

### Fresh Session Resume

If user starts a fresh session mid-execution:
1. State sync-back (from Core Workflow step 5) keeps plan.md updated with "Done" statuses
2. User runs `execute {plan-path}` in new session
3. execute reads plan.md, skips phases with Status = "Done", resumes from next "Pending"

## Post-Execution (Auto Chain — Default ON)

Load: `references/post-execution.md` for the detailed algorithm.

After all phases complete, automatically run in sequence (each step dispatched as a fresh sub-agent via `task` tool to keep main session context lean):

1. **Test** — Dispatch fresh sub-agent; skip if `--skip-tests` or `--skip-post`
2. **Fix** — If tests fail, dispatch fresh sub-agent; max 2 attempts then log warning and continue; skip if `--skip-tests` or `--skip-post`
3. **Review** — Dispatch `task(agent_type="code-reviewer")` on all changed files; skip if `--skip-review` or `--skip-post`
4. **Docs** — Dispatch fresh sub-agent if implementation changed APIs/behavior; skip if `--skip-post`
5. **Git** — Ask user "Commit changes?" before dispatching; if yes, dispatch fresh sub-agent for `git cm --atomic`; skip (no prompt) if `--skip-commit` or `--skip-post`
6. **Plan Status** — Update plan.md: `status: completed` (runs in main session — trivial edit)
7. **Summary Report** — Output: phases completed, files modified/created, test status (pass/fail/skipped), review findings, post-execution status per step (✅/⚠️/❌)

**Opt-out:** `--skip-post` skips steps 1-5 entirely — requires confirmation via `ask_user`:
> "Skipping post-chain (test, fix, review, docs, commit). No automated verification. Continue?"
> Options: ["Yes, skip post-chain", "No, run post-chain"]
If user selects "No", run post-chain normally.

**Fault tolerance:** Each step runs independently; failure logs warning but does NOT block subsequent steps.
**Flag interaction:** `--skip-tests` skips steps 1-2; `--skip-review` skips step 3; `--skip-commit` skips step 5; `--skip-post` skips steps 1-5 (with confirmation).

## Complexity Assessment (Direct Mode Only — Legacy)

| Complexity | Criteria | Strategy |
|-----------|----------|----------|
| Simple | < 3 files, straightforward | Execute directly |
| Medium | 3-10 files, requires analysis | Explore subagents first, then implement |
| Complex | 10+ files, architectural | Break into sub-tasks, parallel subagents |

## Related Skills & Agents

- `plan` — Creates the plans this skill executes
- `worker` agent — Category-aware phase orchestrator (delegates to sub-agents by category)
- `test` — Verification gate after each phase
- `code-review` — Review gate after each phase
- `fix` — Fix failures found during verification
- `debugger` agent — Deep debugging for complex failures
- `docs` — Post-execution documentation
- `git` — Post-execution git commit

## Rules

- NEVER read full phase-XX.md content in main session — only plan.md phase table
- NEVER dispatch one worker for ALL phases — dispatch per-wave only
- Main session context budget: aim for <20% usage throughout
- NEVER skip the verification gate unless `--skip-tests` is explicitly set
- Each wave MUST complete fully before moving to the next wave
- ALWAYS dispatch `worker` (and all implementation sub-agents) with `mode: "background"`; collect results via `read_agent(agent_id, wait=True, timeout=300)`
- If a phase fails verification 3 times, mark it `blocked` and report to user
- Always update SQL todo status (source of truth for progress)
- Post-execution chain is fault-tolerant: log failures, continue to next step
- `--skip-post` requires confirmation via `ask_user` before skipping; if user declines, run chain normally
- `--skip-post` takes precedence over all other post-execution flags (after confirmation)
- `--skip-commit` skips only git step; all other post-chain steps still run
- For parallel subagent dispatch, ensure no file conflicts between agents
