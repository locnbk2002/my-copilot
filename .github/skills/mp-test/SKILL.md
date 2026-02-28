---
name: mp-test
description: "Run tests with auto-detection, structured reporting, and optional auto-fix. Use for test execution, coverage analysis, CI validation, regression checking."
argument-hint: "[scope] [--type unit|integration|e2e] [--coverage] [--fix]"
license: MIT
---

# Testing & QA

Auto-detect test framework, run tests, report results, and optionally auto-fix failures.

## Invocation

```
mp-test [scope] [--type unit|integration|e2e] [--coverage] [--fix]

Default: Auto-detect test framework, run relevant tests
--type: Specific test type (unit, integration, e2e)
--coverage: Include coverage analysis
--fix: Auto-fix failing tests (invoke mp-fix)
```

## When to Use
- After implementing changes to verify correctness
- As part of mp-execute verification gate
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
- Invoke `mp-fix` skill or `mp-debugger` agent
- Re-run affected tests
- Report fix results

## Related Skills & Agents
- `mp-fix` — Fix failing tests
- `mp-debugger` agent — Deep debugging for complex test failures
- `mp-execute` — Invokes this skill as verification gate
