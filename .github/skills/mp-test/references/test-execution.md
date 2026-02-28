## Test Execution

### Execution Strategy

1. **Scoped tests** (when git diff available):
   - Get changed files: `git diff --name-only`
   - Find related test files (same name with `.test.` / `.spec.` / `_test.`)
   - Run only those tests for fast feedback

2. **Full suite** (when no scope or explicitly requested):
   - Run the full test command
   - Set appropriate timeout (default: 120s for `bash` initial_wait)

3. **Coverage mode** (when `--coverage`):
   - Add coverage flag to test command
   - Parse coverage output for summary percentage

### Output Parsing

Parse test runner output for structured reporting:
- **Pass/Fail counts**: Extract from summary line
- **Failed test names**: List each with file:line
- **Error messages**: Capture assertion messages
- **Duration**: Total test runtime

### Failure Handling

When tests fail:
1. Report failures with structured format
2. If `--fix` flag set:
   - Invoke `mp-fix` skill with failure details
   - Re-run only failed tests
   - Max 3 fix-rerun cycles
3. If not auto-fixing: report and stop

### Pre-check Commands

Before running tests, check for common issues:
- TypeScript: `npx tsc --noEmit` (typecheck without emitting)
- ESLint: `npx eslint --max-warnings 0` (if configured)
- Python: `python -m py_compile <changed_files>`
