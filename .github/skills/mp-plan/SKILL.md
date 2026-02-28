---
name: mp-plan
description: "Plan implementations, design architectures, create technical roadmaps with detailed phases. Use for feature planning, system design, solution architecture, implementation strategy, phase documentation."
argument-hint: "[task] OR archive|red-team|validate"
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
Load: `references/category-defaults.md` from `.github/skills/mp-execute/references/` for the full category list and auto-tagging rules.
Auto-tag each phase with a category based on phase content and intent (see `output-standards.md` → Phase Category Tagging).

## Workflow Process

1. **Mode Detection** → Auto-detect or use explicit flag (see `workflow-modes.md`)
2. **Research Phase** → Spawn researcher agents (skip in fast mode)
3. **Codebase Analysis** → Read docs, explore codebase if needed
4. **Plan Documentation** → Write comprehensive plan via general-purpose subagent
5. **Red Team Review** → Invoke `mp-plan:red-team` subskill (hard/parallel/two modes)
6. **Post-Plan Validation** → Invoke `mp-plan:validate` subskill (hard/parallel/two modes)
7. **Hydrate Todos** → Create SQL todos from phases (default on, `--no-tasks` to skip)
8. **Summary** → Output plan file path and next steps

## Output Requirements

- DO NOT implement code - only create plans
- Respond with plan file path and summary
- Ensure self-contained plans with necessary context
- Include code snippets/pseudocode when clarifying
- Fully respect the project's `./docs/development-rules.md` file if present

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
| `mp-plan archive` | `references/archive-workflow.md` | Archive plans + write journal entries |
| `mp-plan red-team` | `references/red-team-workflow.md` | Adversarial plan review with hostile reviewers |
| `mp-plan validate` | `references/validate-workflow.md` | Validate plan with critical questions interview |

## Quality Standards

- Thorough and specific, consider long-term maintainability
- Research thoroughly when uncertain
- Address security and performance concerns
- Detailed enough for junior developers
- Validate against existing codebase patterns

**Remember:** Plan quality determines implementation success. Be comprehensive and consider all solution aspects.
