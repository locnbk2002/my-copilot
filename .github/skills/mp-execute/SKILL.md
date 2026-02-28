---
name: mp-execute
description: "Execute implementation plans phase-by-phase with test/review gates. Use for plan execution, phased implementation, automated workflow with verification steps."
argument-hint: "[plan-path] [--phase N] [--skip-tests] [--skip-review] [--direct]"
license: MIT
---

# Execution Engine

Execute implementation plans phase-by-phase with automated test and review gates.

## Invocation

```
mp-execute [plan-path] [--phase N] [--skip-tests] [--skip-review] [--direct]

Default: Execute all phases with category-aware delegation via mp-worker
--phase N:      Execute only phase N
--skip-tests:   Skip test verification
--skip-review:  Skip code review gate
--direct:       Skip mp-worker, execute phases directly (legacy mode / plans without categories)
```

## When to Use

- After `mp-plan` creates a plan with phases
- To systematically execute phased implementation
- For complex features requiring multiple steps with verification

## Core Workflow (Per Phase)

Load: `references/execution-workflow.md` for the detailed per-phase algorithm.

### Phase Execution Steps

1. **Load Plan** — Read `plan.md` and the specific `phase-XX-*.md` file
2. **Check Dependencies** — Query SQL `todo_deps` to ensure prerequisite phases are done
3. **Mark In Progress** — `UPDATE todos SET status = 'in_progress' WHERE id = 'phase-XX'`
4. **Implement** — Check if phases have a `Category` field:
   - **Category present** (default): Dispatch `task(agent_type="mp-worker")` with plan path, phase range, and work context paths. mp-worker reads config and delegates each phase to the appropriate sub-agent by category.
   - **No category OR `--direct` flag**: Use complexity-based approach:
     - Simple changes (< 3 files): use `edit`/`create` tools directly
     - Medium changes (3-10 files): dispatch `task(agent_type="explore")` first, then implement
     - Complex changes (10+ files): break into sub-tasks, dispatch parallel `task(agent_type="general-purpose")` subagents
5. **Verify** — Run existing tests via `bash` tool; if `mp-test` skill is available, invoke it; if tests fail → invoke `mp-fix` skill or `mp-debugger` agent
6. **Review** (skip if `--skip-review`) — Dispatch `task(agent_type="mp-code-reviewer")` on changed files; if Critical issues found → fix and re-verify
7. **Mark Done** — `UPDATE todos SET status = 'done' WHERE id = 'phase-XX'`
8. **Next Phase** — Query next ready todo and continue

## Post-Execution

Load: `references/post-execution.md` for the checklist.

After all phases complete:

1. **Documentation** — Invoke `mp-docs` skill if implementation changed APIs or behavior
2. **Git Commit** — Invoke `mp-git` skill for conventional commit
3. **Plan Status** — Update plan.md frontmatter: `status: completed`
4. **Summary Report** — Output: phases completed, files modified/created, test status, known issues

## Complexity Assessment (Direct Mode Only)

| Complexity | Criteria | Strategy |
|-----------|----------|----------|
| Simple | < 3 files, straightforward | Execute directly |
| Medium | 3-10 files, requires analysis | Explore subagents first, then implement |
| Complex | 10+ files, architectural | Break into sub-tasks, parallel subagents |

## Related Skills & Agents

- `mp-plan` — Creates the plans this skill executes
- `mp-worker` agent — Category-aware phase orchestrator (delegates to sub-agents by category)
- `mp-test` — Verification gate after each phase
- `mp-code-review` — Review gate after each phase
- `mp-fix` — Fix failures found during verification
- `mp-debugger` agent — Deep debugging for complex failures
- `mp-docs` — Post-execution documentation
- `mp-git` — Post-execution git commit

## Rules

- NEVER skip the verification gate unless `--skip-tests` is explicitly set
- Each phase MUST complete fully before moving to the next
- If a phase fails verification 3 times, mark it `blocked` and report to user
- Always update SQL todo status (source of truth for progress)
- For parallel subagent dispatch, ensure no file conflicts between agents
