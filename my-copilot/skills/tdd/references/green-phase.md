# Green Phase — Minimal Implementation

The goal: make ALL failing tests pass with the least code possible.

## Constraints (strictly enforced)

- Implement ONLY what the failing tests require — nothing more
- No optimization, no abstraction, no "while I'm here" extras
- No new dependencies unless the test explicitly requires them
- If in doubt: write the simplest code that could possibly work

## Step 1: Read Context Before Writing

1. Read the failing test files to understand exactly what's expected
2. Read adjacent source files (same module/package) to match existing patterns
3. Check imports needed — use what's already in the project

## Step 2: Implementation Strategies (in order)

### Fake it till you make it
Start with hardcoded return values if tests only check one case:
```python
def get_user(id):
    return {"id": 1, "name": "Alice"}  # make the first test pass
```

### Obvious implementation
When the correct solution is clear, just write it:
```python
def get_user(id):
    return db.query("SELECT * FROM users WHERE id = ?", id)
```

### Triangulation
When multiple test cases force generalization — let the tests drive the generality.
Add implementation complexity only when a new failing test requires it.

## Step 3: Run Tests

```
test [test-file-path] --type unit
```

**Expected outcome**: ALL tests pass (including tests that were passing before red phase).

### Pass gate logic

| Test result | Action |
|-------------|--------|
| All tests PASS | ✅ Proceed to refactor phase |
| Some tests FAIL | ❌ Invoke `fix` skill — analyze failure, apply minimal fix |
| Fix attempt 1 fails | ❌ Try again (max 3 total attempts) |
| Still failing after 3 | 🛑 Report to user with failure details, stop |

### fix skill invocation
```
fix "[failing test name]: [error message]"
```
Pass the exact test output so `fix` has context.

## Step 4: Scope Check Before Stopping

Before declaring green phase done, verify:
- [ ] All tests in the red phase test file(s) pass
- [ ] No previously passing tests are now broken (no regressions)
- [ ] Implementation is in the right file/module (not test file)
- [ ] No TODOs or placeholder returns remain (unless test allows them)

## What Green Is NOT

- Not the final implementation — refactor comes next
- Not the place to add error handling "just in case" — tests will demand it if needed
- Not the place to add logging, metrics, or docs — those aren't in the failing tests
