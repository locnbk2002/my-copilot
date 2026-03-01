---
name: execute
description: "Execute implementation plans phase-by-phase with test/review gates. Use for plan execution, phased implementation, automated workflow with verification steps."
argument-hint: "[plan-path] [--phase N] [--skip-tests] [--skip-review] [--skip-post] [--direct]"
license: MIT
---

# Execution Engine

Execute implementation plans phase-by-phase with automated test and review gates.

## Invocation

```
execute [plan-path] [--phase N] [--skip-tests] [--skip-review] [--skip-post] [--direct]

Default: Execute all phases with category-aware delegation via worker
--phase N:      Execute only phase N
--skip-tests:   Skip test verification
--skip-review:  Skip code review gate
--skip-post:    Skip entire post-execution chain (test, fix, review, docs, git)
--direct:       Legacy mode — skip worker, execute phases directly (for plans without Category tags)
```

## When to Use

- After `plan` creates a plan with phases
- To systematically execute phased implementation
- For complex features requiring multiple steps with verification

## Core Workflow (Per Phase)

execute is a **thin orchestrator** — it reads, dispatches, and tracks. It NEVER edits files or writes implementations in main context.

Load: `references/execution-workflow.md` for the detailed per-phase algorithm.

### Phase Execution Steps

1. **Load Plan** — Read `plan.md` phase table and specific `phase-XX-*.md` file
2. **Check Dependencies** — Query SQL `todo_deps` or plan.md "Depends On" column; skip phases with Status = "Done"
3. **Mark In Progress** — `UPDATE todos SET status = 'in_progress' WHERE id = 'phase-XX'`
4. **Dispatch** — `task(agent_type="worker", mode="background")` with plan path, phase range, and work context paths → returns `agent_id`
   - worker handles: config resolution, category-to-agent mapping, wave execution, fresh context per phase
   - Collect result: `read_agent(agent_id, wait=True, timeout=300)`
   - **Legacy `--direct` mode**: Skip worker; use complexity-based approach (see Complexity Assessment below)
5. **Sync Status** — Update plan.md phase Status column and phase-XX.md checkboxes (see State Sync-Back)
6. **Verify** — Run existing tests via `bash`; if `test` skill available, invoke it; if tests fail → invoke `fix` or `debugger`
7. **Review** (skip if `--skip-review`) — Dispatch `task(agent_type="code-reviewer")` on changed files
8. **Mark Done** — `UPDATE todos SET status = 'done' WHERE id = 'phase-XX'`
8.5. **Budget Check** (every 3 phases) — If `completed_count % 3 == 0`: run Context Budget Monitoring check (see Context Budget Monitoring)
9. **Next Phase** — Query next ready todo and continue

**RULE:** Steps 1–3, 5–9 happen in main context (reads, SQL updates, syncs). Step 4 (ALL implementation) happens in sub-agent context ONLY.

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

After all phases complete, automatically run in sequence:

1. **Test** — Invoke `test` skill; skip if `--skip-tests` or `--skip-post`
2. **Fix** — If tests fail, invoke `fix` skill; max 2 attempts then log warning and continue; skip if `--skip-tests` or `--skip-post`
3. **Review** — Dispatch `task(agent_type="code-reviewer")` on all changed files; skip if `--skip-review` or `--skip-post`
4. **Docs** — Invoke `docs` skill if implementation changed APIs/behavior; skip if `--skip-post`
5. **Git** — Invoke `git cm --atomic` for conventional commit; skip if `--skip-post`
6. **Plan Status** — Update plan.md: `status: completed`
7. **Summary Report** — Output: phases completed, files modified/created, test status (pass/fail/skipped), review findings, post-execution status per step (✅/⚠️/❌)

**Opt-out:** `--skip-post` skips steps 1-5 entirely (manual post-execution).
**Fault tolerance:** Each step runs independently; failure logs warning but does NOT block subsequent steps.
**Flag interaction:** `--skip-tests` skips steps 1-2; `--skip-review` skips step 3; `--skip-post` skips steps 1-5.

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

- NEVER skip the verification gate unless `--skip-tests` is explicitly set
- Each phase MUST complete fully before moving to the next
- ALWAYS dispatch `worker` (and all implementation sub-agents) with `mode: "background"`; collect results via `read_agent(agent_id, wait=True, timeout=300)`
- If a phase fails verification 3 times, mark it `blocked` and report to user
- Always update SQL todo status (source of truth for progress)
- Post-execution chain is fault-tolerant: log failures, continue to next step
- `--skip-post` takes precedence over all other post-execution flags
- For parallel subagent dispatch, ensure no file conflicts between agents
