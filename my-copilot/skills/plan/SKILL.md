---
name: plan
description: "Plan implementations, design architectures, create technical roadmaps with detailed phases. Use for feature planning, system design, solution architecture, implementation strategy, phase documentation."
argument-hint: "[task] [--auto|--fast|--hard|--parallel|--two] [--discuss] [--skip-brainstorm] [--no-tasks] [--validate auto|prompt|off] OR archive|red-team|validate"
license: MIT
---

# Planning

Create detailed technical implementation plans through research, codebase analysis, solution design, and comprehensive documentation.

## Default (No Arguments)

If invoked with a task description, proceed with planning workflow. If invoked WITHOUT arguments or with unclear intent, use `ask_user` to present available operations:

| Operation | Description |
|-----------|-------------|
| `(default)` | Create implementation plan for a task |
| `archive` | Write journal entry & archive plans |
| `red-team` | Adversarial plan review |
| `validate` | Critical questions interview |

Present as options via `ask_user` with question "What would you like to do?".

## Workflow Modes

Default: `--auto` (analyze task complexity and auto-pick mode).

| Flag | Mode | Research | Red Team | Validation |
|------|------|----------|----------|------------|
| `--auto` | Auto-detect | Follows mode | Follows mode | Follows mode |
| `--fast` | Fast | Skip | Skip | Skip |
| `--hard` | Hard | 2 researchers | Yes | Optional |
| `--parallel` | Parallel | 2 researchers | Yes | Optional |
| `--two` | Two approaches | 2+ researchers | After selection | After selection |
| `--discuss` | Modifier | — | — | — |
| `--skip-brainstorm` | Modifier | — | — | — |

`--discuss`: Interview user for preferences before research; saves to `preferences.md`; combinable with any mode.
`--skip-brainstorm`: Skip pre-research brainstorm; go straight to research.

Add `--no-tasks` to skip todo creation in any mode.

Load: `references/workflow-modes.md` for auto-detection logic, per-mode workflows.

## When to Use

- Planning new feature implementations
- Architecting system designs
- Evaluating technical approaches
- Creating implementation roadmaps
- Breaking down complex requirements

## Core Responsibilities & Rules

Always honoring **YAGNI**, **KISS**, and **DRY** principles.
**Be honest, be brutal, straight to the point, and be concise.**

## Context Engineering

The planner is a **thin orchestrator** — keep main context lean; delegate heavy work to subagents.

**Context budget: aim for <30% usage in main planner context.**

### Principles

1. **Isolate researchers** — each researcher subagent gets a focused, minimal prompt. Never pass full plan context to researchers; pass only the specific question.
2. **Progressive disclosure** — read only what's needed now. Don't load all reference files upfront; load per-section as workflow progresses.
3. **Write findings externally** — researchers write reports to `plans/reports/`; planner reads summaries, not full content.
4. **Compress before chaining** — summarize researcher outputs before passing to next phase agent.

### If `<usage-awareness>` is Injected

Use context % to adapt behavior:

| Context % | Behavior |
|-----------|----------|
| <70% | Normal — proceed with full research phase |
| 70-89% [WARNING] | Skip optional steps (red-team, validate); spawn fewer researchers |
| ≥90% [CRITICAL] | Fast mode only — skip research, create minimal plan from available context |

### 0. Pre-Research Brainstorm
Load: inline (no reference file)
**Skip if:** `--fast`, `--two`, `--skip-brainstorm`, or user provided explicit approach

### 1. Research & Analysis
Load: `references/research-phase.md`
**Skip if:** Fast mode or provided with researcher reports

### 2. Codebase Understanding
Load: `references/codebase-understanding.md`
**Skip if:** Provided with scout reports

### 3. Solution Design
Load: `references/solution-design.md`

### 4. Plan Creation & Organization
Load: `references/plan-organization.md`

### 5. Task Breakdown & Output Standards
Load: `references/output-standards.md`

### 6. Category Tagging
Load: `references/category-defaults.md` from `.github/skills/execute/references/` for the full category list and auto-tagging rules.
Auto-tag each phase with a category based on phase content and intent (see `output-standards.md` → Phase Category Tagging).

## Workflow Process

0. **Pre-Research Brainstorm (default ON, skip in --fast/--two/--skip-brainstorm)** → If user didn't provide explicit approach: generate 2-3 lightweight approaches inline (table: approach | effort | risk | recommendation), ask user to pick via `ask_user`, feed chosen approach as context for research. See Pre-Research Brainstorm section below.
1. **Mode Detection** → Auto-detect or use explicit flag (see `workflow-modes.md`)
1.5. **Discuss Phase (if --discuss)** → Load `references/discuss-workflow.md`. Interview user, save preferences to `{plan-dir}/preferences.md`, include preference summary in researcher prompts.
1.75. **Post-Discuss Brainstorm (if --discuss + brainstorm not skipped)** → After discuss, run brainstorm with user preferences as context for approach generation.
2. **Research Phase** → Spawn researcher agents (skip in fast mode)
3. **Codebase Analysis** → Read docs, explore codebase if needed
4. **Plan Documentation** → Write comprehensive plan via general-purpose subagent
4.5. **Paralysis Check** (skip in --fast) → If thresholds exceeded, run Analysis Paralysis Guard
5. **Red Team Review** → Invoke `plan:red-team` subskill (hard/parallel/two modes)
6. **Post-Plan Validation** → Invoke `plan:validate` subskill (hard/parallel/two modes)
7. **Hydrate Todos** → Create SQL todos from phases (default on, `--no-tasks` to skip)
8. **Summary** → Output plan file path and next steps
9. **Execute Prompt** (MANDATORY — never skip) → After todos hydrated, ask user via `ask_user`: "Plan ready at {plan-dir}. Execute now?" Options: ["Yes, execute now", "No, I'll run it later"]. If yes: invoke `execute {plan-dir}` immediately. If no: output reference command `execute {plan-dir}` and stop.

## Output Requirements

- DO NOT implement code - only create plans
- Respond with plan file path and summary
- Ensure self-contained plans with necessary context
- Include code snippets/pseudocode when clarifying
- Fully respect the project's `./docs/development-rules.md` file if present

## Analysis Paralysis Guard

After research phase and during plan creation, check for over-planning. Skip in `--fast` mode.

| Trigger | Threshold | Signal |
|---------|-----------|--------|
| Research rounds | > 2 | 3+ researcher agents spawned |
| Phase count | > 10 | Plan has many phases |
| Approach comparisons | > 3 | In `--two` mode with many options |
| Plan size | > 150 lines | plan.md getting too large |

**When triggered:** Use `ask_user` with message:
> "⚠️ Plan complexity detected ({trigger reason}). What would you like to do?"

Options:
1. "Start executing now (Recommended)" → Stop planning, output plan path, ready for execute
2. "Continue planning" → Proceed, add `<!-- ⚠️ Complexity warning acknowledged -->` note in plan.md
3. "Simplify the plan" → Suggest merging phases with similar scope, removing P3 phases

**Check timing:** After research, before finalizing phase list (step 4.5 in workflow).

## Task Management

Plan files = persistent. Todos = session-scoped (SQL). Hydration bridges the gap.

**Default:** Auto-hydrate todos after plan files are written. Skip with `--no-tasks`.
**3-Task Rule:** <3 phases → skip todo creation.

Load: `references/task-management.md` for hydration pattern and todo tracking.

### Hydration Workflow
1. Write plan.md + phase files (persistent layer)
2. Insert a todo per phase into session SQL `todos` table
3. Chain dependencies via `todo_deps`
4. Mark todos `in_progress` as work proceeds, `done` when complete

## Subcommands

| Subcommand | Reference | Purpose |
|------------|-----------|---------|
| `plan archive` | `references/archive-workflow.md` | Archive plans + write journal entries |
| `plan red-team` | `references/red-team-workflow.md` | Adversarial plan review with hostile reviewers |
| `plan validate` | `references/validate-workflow.md` | Validate plan with critical questions interview |

## Quality Standards

- Thorough and specific, consider long-term maintainability
- Research thoroughly when uncertain
- Address security and performance concerns
- Detailed enough for junior developers
- Validate against existing codebase patterns

**Remember:** Plan quality determines implementation success. Be comprehensive and consider all solution aspects.

## Execute Handoff

After plan creation completes (Step 9 — MANDATORY, never skip):

```
ask_user(
  question="Plan ready at {plan-dir}. Execute now?",
  choices=["Yes, execute now", "No, I'll run it later"]
)
```

- **If "Yes"**: invoke `execute {plan-dir}` immediately in the same session
- **If "No"**: output: `Run when ready: execute {plan-dir}` and stop

**Skip if:** User already provided explicit follow-up instruction (e.g. "just plan, don't execute").

---

## Pre-Research Brainstorm

Auto-runs before research when no explicit approach is provided. Skip in `--fast`, `--two`, or `--skip-brainstorm`.

For deeper exploration before planning, use the standalone `brainstorm` skill.

### Ambiguity Detection

Skip brainstorm if user message contains solution-specific language such as:
- "use X for Y" (e.g., "use Redis for caching")
- "implement with Z" (e.g., "implement with JWT")
- "approach: ..." or "solution: ..."
- "via X", "using X", "with X architecture"

If ambiguity detected (no explicit approach): run brainstorm inline.

### Brainstorm Format

Generate 2-3 approaches inline using this table format:

| # | Approach | Effort | Risk | Challenge | Recommendation |
|---|---------|--------|------|-----------|---------------|
| 1 | {name} ⭐ | Low | Low | {1-line devil's advocate risk} | Recommended |
| 2 | {name} | Medium | Medium | {1-line devil's advocate risk} | Alternative |
| 3 | {name} | High | Low | {1-line devil's advocate risk} | Over-engineered |

After the table, add a brief description per approach:

```
**1. {name}:** {what it does}. {key tradeoff}.
**2. {name}:** {what it does}. {key tradeoff}.
**3. {name}:** {what it does}. {key tradeoff}.
```

Then ask user:
```
ask_user(
  question="Which approach should the plan be based on?",
  choices=["1: {approach 1 name} (Recommended)", "2: {approach 2 name}", "3: {approach 3 name}"]
)
```

After user picks, inject into each researcher agent's prompt:
```
## Chosen Approach
{approach name}: {approach description}
Key challenge: {challenge from table}
```

### Mode Behavior

| Mode | Brainstorm |
|------|-----------|
| `--fast` | ❌ Skip |
| `--two` | ❌ Skip (inherently multi-approach) |
| `--hard` | ✅ Run (before research) |
| `--parallel` | ✅ Run (before research) |
| `--discuss` modifier | ✅ Run after discuss (step 1.75) |
| `--skip-brainstorm` | ❌ Skip |
