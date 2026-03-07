# Red Phase — Write Failing Tests

The goal: prove requirements are testable and currently unimplemented.

## Step 1: Identify Test Subjects

From the scope (requirement text, phase file, user story):

1. Extract nouns → candidate classes/functions/endpoints
2. Extract verbs → candidate behaviors to assert
3. Extract acceptance criteria → test cases (1 test minimum per criterion)

**Example mapping:**

```
Requirement: "User can log in with email and password"
→ Test subjects: login function, session creation
→ Test cases: valid credentials → session created, wrong password → error, unknown email → error
```

## Step 2: Detect Test Framework

Reuse detection logic from `test` skill's `references/framework-detection.md`:

- `package.json` scripts/devDeps → jest / vitest / mocha / playwright
- `pyproject.toml` / `setup.cfg` → pytest / unittest
- `go.mod` → go test
- Existing test files patterns: `*.test.ts`, `*.spec.js`, `test_*.py`, `*_test.go`

If no framework detected: `ask_user` — "No test framework found. Which should I use?"

## Step 3: Write Test File(s)

### Placement convention (follow existing patterns first)

- TypeScript/JavaScript: `src/**/__tests__/`, `src/**/*.test.ts`, `tests/`
- Python: `tests/test_*.py` alongside source
- Go: `*_test.go` in same package

### Naming convention

- Jest/Vitest: `describe('[Unit]', () => { it('should [behavior] when [condition]', ...) })`
- pytest: `def test_[behavior]_when_[condition]():`
- Go: `func Test[Behavior](t *testing.T)`

### What makes a good red test

- Tests ONE behavior per test case (single assertion where possible)
- Uses real inputs/outputs — no mocks of the subject under test
- Fails for the RIGHT reason (function missing or returns wrong value, not import error)
- Has a clear failure message so green phase knows exactly what to implement

### What to avoid

- Don't test implementation details — test observable behavior
- Don't write more tests than needed for current requirements (YAGNI)
- Don't mock things that don't exist yet — let the test fail naturally

## Step 4: Verify Tests Fail

Run `test` skill on the new test files only:

```
test [test-file-path] --type unit
```

**Expected outcome**: ALL new tests fail with meaningful errors, not setup/import errors.

### Failure gate logic

| Test result                                | Action                                     |
| ------------------------------------------ | ------------------------------------------ |
| All new tests FAIL                         | ✅ Proceed to green phase                  |
| Some new tests PASS                        | ⚠️ `ask_user` — may be already implemented |
| Tests fail with ImportError/ModuleNotFound | ❌ Fix test infrastructure first, re-run   |
| Tests fail with syntax error               | ❌ Fix test file, re-run                   |

### ask_user template (when tests already pass)

```
Test '[test name]' passes before any implementation.
This requirement may already be covered. Options:
1. "Continue anyway" — keep test, proceed to green
2. "Skip this test" — remove test, write a different one
3. "Abort" — stop TDD cycle, investigate first
```
