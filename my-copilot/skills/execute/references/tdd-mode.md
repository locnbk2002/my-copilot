# TDD Mode — Per-Phase TDD Execution

Activated when `execute` is invoked with `--tdd`. Applies to worker dispatch only — wave computation and post-execution chain are unchanged.

## How It Works

When `--tdd` is set, execute passes `tdd_mode=true` to the worker dispatch prompt. Worker then executes each phase in 3 sub-phases instead of direct implementation.

## Worker Dispatch Prompt Addition (when tdd_mode=true)

Append to the standard worker prompt:

```
## TDD Mode (tdd_mode=true)

Execute this phase using Test-Driven Development. Follow this order strictly:

### Sub-phase 1: Red
1. Read phase requirements and identify test subjects (functions, endpoints, behaviors)
2. Write failing tests using the project's existing test framework
3. Run tests — ALL new tests MUST fail
4. Failure gate: if any new test already passes, use ask_user:
   "Test '[name]' passes before implementation. Requirement may exist. Continue TDD?"
   Options: ["Continue", "Skip this test", "Abort phase"]
5. If --skip-tests: skip gate, proceed to green

### Sub-phase 2: Green
1. Implement minimal code to pass the failing tests — nothing more
2. Run tests — ALL must pass
3. Pass gate: if tests fail, invoke fix skill (max 3 iterations)
4. If still failing after 3 attempts: mark phase blocked, report to user

### Sub-phase 3: Refactor
1. Scan implementation for smells: duplication, magic literals, unclear names
2. Apply improvements in small batches — zero behavior changes
3. Run tests after each batch — must stay green
4. If a batch breaks tests: revert it, continue with next batch

References for detailed guidance per sub-phase:
- tdd skill: references/red-phase.md
- tdd skill: references/green-phase.md
- tdd skill: references/refactor-phase.md
```

## Phase Report Format (TDD mode)

Worker reports per-phase TDD status:

```markdown
### Phase N — TDD Summary
- Red: [N] tests written, all failed ✅ / [N] already passing ⚠️
- Green: [N]/[N] tests passing ✅ / blocked after 3 fix attempts ❌
- Refactor: [N] batches applied ✅ / [N] batches reverted ⚠️ / skipped
- Files modified: [list]
```

## Flag Interactions

| Flag combination | Behavior |
|-----------------|----------|
| `--tdd` | Full TDD per phase: red → green → refactor |
| `--tdd --skip-refactor` | TDD per phase but skip refactor sub-phase (red → green only) |
| `--tdd --skip-tests` | Skip all test gates (red failure confirmation, green/refactor pass gates); sub-phases still run but no test execution |
| `--tdd --phase N` | TDD mode for phase N only |
| `--tdd --skip-post` | TDD per phase; skip post-execution chain (requires confirmation) |

## When Not to Use --tdd

- Phases tagged `writing` or `documentation` — no meaningful tests to write
- Phases that only update config files — tests don't apply
