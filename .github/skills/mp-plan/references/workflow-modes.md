# Workflow Modes

## Auto-Detection (Default: `--auto`)

When no flag specified, analyze task and pick mode:

| Signal | Mode | Rationale |
|--------|------|-----------|
| Simple task, clear scope, no unknowns | fast | Skip research overhead |
| Complex task, unfamiliar domain, new tech | hard | Research needed |
| 3+ independent features/layers/modules | parallel | Enable concurrent agents |
| Ambiguous approach, multiple valid paths | two | Compare alternatives |

Use `ask_user` if detection is uncertain.

## Fast Mode (`--fast`)

No research. Analyze → Plan → Hydrate Todos.

1. Read codebase docs (`codebase-summary.md`, `code-standards.md`, `system-architecture.md`)
2. Use a `general-purpose` subagent to create plan
3. Hydrate todos (unless `--no-tasks`)
4. Output plan path summary

**Why fast?** Simple tasks don't need research overhead.

## Hard Mode (`--hard`)

Research → Scout → Plan → Red Team → Validate → Hydrate Todos.

1. Spawn max 2 `explore` agents in parallel (different aspects, max 5 searches each)
2. Read codebase docs; run explore agents to search codebase if docs are stale/missing
3. Gather research + scout findings → pass to `general-purpose` subagent for plan creation
4. Post-plan red team review (see Red Team Review section below)
5. Post-plan validation (see Validation section below)
6. Hydrate todos (unless `--no-tasks`)

**Why hard?** Thorough planning needs research and adversarial review.

## Parallel Mode (`--parallel`)

Research → Scout → Plan with file ownership → Red Team → Validate → Hydrate Todos with dependency graph.

1. Same as Hard mode steps 1-3
2. Planner creates phases with:
   - **Exclusive file ownership** per phase (no overlap)
   - **Dependency matrix** (which phases run concurrently vs sequentially)
   - **Conflict prevention** strategy
3. plan.md includes: dependency graph, execution strategy, file ownership matrix
4. Hydrate todos: `todo_deps` for sequential deps, no blockers for parallel groups
5. Post-plan red team review
6. Post-plan validation

### Parallel Phase Requirements
- Each phase self-contained, no runtime deps on other phases
- Clear file boundaries — each file modified in ONE phase only
- Group by: architectural layer, feature domain, or technology stack
- Example: Phases 1-3 parallel (DB/API/UI), Phase 4 sequential (integration tests)

## Two-Approach Mode (`--two`)

Research → Scout → Plan 2 approaches → Compare → Hydrate Todos.

1. Same as Hard mode steps 1-3
2. Planner creates 2 implementation approaches with:
   - Clear trade-offs (pros/cons each)
   - Recommended approach with rationale
3. User selects approach via `ask_user`
4. Post-plan red team review on selected approach
5. Post-plan validation
6. Hydrate todos for selected approach (unless `--no-tasks`)

## Todo Hydration Per Mode

| Mode | Todo Granularity | Dependency Pattern |
|------|------------------|--------------------|
| fast | Phase-level only | Sequential chain |
| hard | Phase + critical steps | Sequential + step deps |
| parallel | Phase + steps + ownership | Parallel groups + sequential deps |
| two | After user selects approach | Sequential chain |

All modes: See `task-management.md` for SQL insert patterns.

## Post-Plan Red Team Review

Adversarial review that spawns hostile reviewers to find flaws before validation.

**Available in:** hard, parallel, two modes. **Skipped in:** fast mode.

**Invocation:** Use the `skill` tool to invoke `mp-plan:red-team` with the plan directory path:
```
skill("mp-plan:red-team")  // then pass plan path as context
```

Or run inline using `task` tool with `agent_type: "code-review"` to review the plan documents.

**Sequence:** Red team runs BEFORE validation because:
1. Red team may change the plan
2. Validation should confirm the FINAL plan

## Post-Plan Validation

| Mode | Behavior |
|------|----------|
| `prompt` | Use `ask_user`: "Validate this plan with interview?" → Yes (Recommended) / No |
| `auto` | Automatically invoke `mp-plan:validate` inline |
| `off` | Skip validation |

**Invocation:** Use the `skill` tool to invoke `mp-plan:validate`, or run inline workflow from `references/validate-workflow.md`.

**Available in:** hard, parallel, two modes. **Skipped in:** fast mode.

## Summary Output (MANDATORY)

After plan creation, MUST output:
- Absolute path to plan directory
- Brief summary of phases
- Next steps for implementation

> **Best Practice:** Start a fresh conversation before implementing.
> Read `plan.md` to re-hydrate context, then proceed phase by phase.

**Why absolute path?** Ensures the plan can be located in a new session.
This reminder is **NON-NEGOTIABLE** — always output after presenting the plan.

## Pre-Creation Check

Before creating a new plan, use `ask_user` to confirm:
- "Continue with existing plan?" if one is detected in the plans directory
- "Create new plan or activate existing?" if multiple plans exist
