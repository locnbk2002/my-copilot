---
name: tdd
description: "Test-Driven Development cycle: red (write failing tests) → green (implement to pass) → refactor (clean up). Use for TDD-first feature development, requirement-driven testing, and disciplined implementation."
argument-hint: "[scope|requirements] [--red|--green|--refactor] [--skip-refactor]"
license: MIT
---

# TDD — Red → Green → Refactor

Write failing tests first, implement the minimum to pass them, then clean up.

## Invocation

```
tdd [scope|requirements] [--red|--green|--refactor] [--skip-refactor]

Default:           Full cycle — red → green → refactor
--red:             Write failing tests only, stop
--green:           Implement to pass tests only (assumes red done)
--refactor:        Refactor only (assumes green done)
--skip-refactor:   Run red → green, skip refactor phase
```

## When to Use

- Starting a new feature with clear requirements — write tests before any code
- Ensuring a requirement is fully specified before implementing it
- As a discipline check — if you can't write a failing test, the requirement isn't clear enough
- Refactoring existing code safely with a test harness

## Workflow

### 1. Parse Scope
- If argument is a file path: read it (phase file, requirements doc, user story)
- If argument is text: treat as requirement description
- If no argument: `ask_user` — "What feature/requirement should I write tests for?"

### 2. Red Phase
Load: `references/red-phase.md`

1. Identify test subjects from scope (functions, endpoints, behaviors)
2. Write failing tests using project's existing test framework
3. Run tests via `test` skill — ALL new tests MUST fail
4. **Failure gate**: if any new test already passes → `ask_user`:
   "Test '[name]' already passes — requirement may be implemented. How to proceed?"
   Options: ["Continue anyway", "Skip this test", "Abort"]

If `--red` only: stop here, report tests written.

### 3. Green Phase
Load: `references/green-phase.md`

1. Implement minimal code to make failing tests pass — no extras
2. Run tests — ALL must pass
3. **Pass gate**: if tests fail → invoke `fix` skill (max 3 iterations)
4. If still failing after 3 attempts → report to user, stop

If `--green` only: start here (assumes red done).

### 4. Refactor Phase
Load: `references/refactor-phase.md`

Skip if `--skip-refactor`.

1. Identify code smells: duplication, unclear names, long functions
2. Apply minimal improvements — zero behavior changes
3. Run tests after each batch — must stay green
4. If refactor breaks tests → revert the batch, warn user

If `--refactor` only: start here (assumes green done).

### 5. Cycle Report

```
## TDD Cycle Report
- Scope: [description]
- Red: [N] tests written, all failed ✅
- Green: [N] tests passing, [N] tests total ✅ / [failed] ❌
- Refactor: [changes made] / skipped
- Files modified: [list]
```

## Rules

- NEVER write implementation code before tests exist (in red phase)
- NEVER skip the failure gate — tests that don't fail first aren't TDD tests
- NEVER add extra functionality in green phase — minimal implementation only
- NEVER change behavior during refactor — tests are the contract
- Always use the project's existing test framework (see `test` skill for detection)

## Related Skills & Agents

- `test` — Test execution (used in all phase gates)
- `fix` — Fix failing tests in green phase (max 3 iterations)
- `execute --tdd` — Apply TDD cycle per phase during plan execution
