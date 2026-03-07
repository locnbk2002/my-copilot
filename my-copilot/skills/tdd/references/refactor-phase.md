# Refactor Phase — Clean Up Without Breaking

The goal: improve code quality while keeping all tests green. Zero behavior changes.

## Constraint: Tests Are the Contract

Any change that breaks a test is a behavior change — revert it.
Refactor operates ONLY within the boundaries defined by passing tests.

## Step 1: Identify Code Smells

Scan the implementation written in green phase for:

| Smell | Example | Fix |
|-------|---------|-----|
| Duplicated logic | Same condition checked 3 times | Extract helper function |
| Magic literals | `if status == 3:` | Named constant `STATUS_ACTIVE = 3` |
| Long function | >20 lines doing multiple things | Split into focused functions |
| Unclear name | `def proc(d):` | Rename to intent: `def process_order(data):` |
| Nested conditionals | `if a: if b: if c:` | Early returns or guard clauses |
| Dead code | Unused variable, unreachable branch | Delete it |
| Fake-it remnants | Hardcoded return value from green | Replace with real logic |

## Step 2: Apply in Small Batches

Refactor one smell at a time. After each batch:
```
test [test-file-path]
```
All tests must still pass. If any fail → revert the last change immediately.

**Batch size**: one logical change (one rename, one extraction, one deduplication).
Not: "I'll refactor the whole module."

## Step 3: Stop Conditions

Stop when ANY of the following is true:
- All identified smells from Step 1 are addressed
- Tests are failing and the failing change can't be trivially reverted
- No more obvious improvements without adding new functionality

**YAGNI check before each change**: "Does this improvement serve a current test requirement, or am I speculating about future needs?" If speculating — skip it.

## Step 4: Final Test Run

After all refactor batches complete:
```
test [test-file-path] --coverage
```

All tests must pass. Report any coverage delta (should be neutral — no new paths added).

## What Refactor Is NOT

- Not adding new features ("while I'm here I'll add caching")
- Not changing test files to fit the implementation (tests drive behavior)
- Not introducing new abstractions for hypothetical future requirements
- Not fixing unrelated code in other files

## Revert Protocol

If a refactor breaks tests and the fix isn't obvious within 2 minutes:
1. Revert the change (restore previous code)
2. Note the smell in the cycle report as "deferred — needs deeper analysis"
3. Continue with remaining batches

Do not spend time debugging a refactor — revert and move on.
