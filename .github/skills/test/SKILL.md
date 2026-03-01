---
name: test
description: "Run tests with auto-detection, structured reporting, and optional auto-fix. Use for test execution, coverage analysis, CI validation, regression checking."
argument-hint: "[scope] [--type unit|integration|e2e] [--coverage] [--fix] [--nyquist]"
license: MIT
---

# Testing & QA

Auto-detect test framework, run tests, report results, and optionally auto-fix failures.

## Invocation

```
test [scope] [--type unit|integration|e2e] [--coverage] [--fix] [--nyquist]

Default: Auto-detect test framework, run relevant tests
--type: Specific test type (unit, integration, e2e)
--coverage: Include coverage analysis
--fix: Auto-fix failing tests (invoke fix)
--nyquist:  Map tests to plan requirements, report coverage gaps before running
```

## When to Use
- After implementing changes to verify correctness
- As part of execute verification gate
- Before committing to ensure no regressions
- To get structured test reports

## Workflow

Load: `references/framework-detection.md` for auto-detection logic.
Load: `references/test-execution.md` for execution and reporting.

### 1. Detect Framework
Auto-detect from project files:
- `package.json` → jest/vitest/mocha/playwright
- `setup.py`/`pyproject.toml` → pytest/unittest
- `go.mod` → `go test`
- `Cargo.toml` → `cargo test`
- `*.test.*`/`*.spec.*` file patterns

### 2. Scope Analysis
What to test:
- If recent changes exist (`git diff`): test affected modules
- If scope specified: test that scope
- If no scope: run full test suite

### 3. Pre-check
Before running tests:
- Typecheck/lint (if configured): `npm run typecheck`, `tsc --noEmit`
- Build check: ensure project compiles

### 3.5. Nyquist Validation (if `--nyquist`)

Load: `references/nyquist-validation.md` for mapping algorithm.

1. Extract requirements from plan files (Success Criteria, Functional Requirements, todos)
2. Scan test files across common frameworks
3. Map requirements to tests via keyword matching
4. Generate coverage report (covered / uncovered / orphan)
5. If coverage < 80%: `ask_user` — "Only {X}% of requirements have tests. Continue running tests?" with options: Run anyway / Generate stubs first / Abort

If `--nyquist` only (no scope or test type given): report only, do not run tests.

### 4. Execute Tests
Run via `bash` tool:
- Capture output (stdout + stderr)
- Parse results (pass/fail counts)
- If `--coverage`: run with coverage flag

### 5. Report
Structured output:
```
## Test Results
- Framework: [detected]
- Tests: X passed, Y failed, Z skipped
- Coverage: XX.X% (if requested)

### Failures (if any)
1. `file:line` — Error description
```

### 6. Auto-fix (if `--fix`)
- Analyze failure messages
- Invoke `fix` skill or `debugger` agent
- Re-run affected tests
- Report fix results

## Related Skills & Agents
- `fix` — Fix failing tests
- `debugger` agent — Deep debugging for complex test failures
- `execute` — Invokes this skill as verification gate
