---
name: fix
description: "Diagnose and fix bugs with root cause analysis, minimal patches, and verification. Use for bug fixing, test failures, error resolution, debugging."
argument-hint: "[description] [--quick] [--file path]"
license: MIT
---

# Bug Fixing

Analyze errors, find root cause, apply minimal fix, and verify.

## Invocation

```
fix [description] [--quick] [--file path]

Default: Analyze error, find root cause, fix, verify
--quick: Skip deep analysis, apply obvious fix
--file: Focus on specific file
```

## When to Use
- After test failures (standalone or invoked by test)
- When error messages need diagnosis
- For debugging issues found during code review
- As part of execute failure recovery

## Workflow

Load: `references/fix-workflow.md` for detailed workflow.

### 1. Error Analysis
- Read error message/stack trace (from test output, user description, or terminal)
- Identify affected file(s) and line(s)
- Classify error type: type error, logic error, runtime error, import error

### 2. Complexity Assessment
| Complexity | Criteria | Strategy |
|-----------|----------|----------|
| Simple | Typo, import, type error | Fix directly |
| Medium | Logic error, missing edge case | Use `debugger` agent for root cause |
| Complex | Architectural issue, multi-file | Create mini-plan, fix systematically |

### 3. Root Cause (skip if `--quick`)
- Dispatch `task(agent_type="debugger")` for root cause analysis
- Or use `sequential-thinking` skill for step-by-step reasoning

### 4. Fix Implementation
- Apply minimal change to fix the root cause
- Follow existing code patterns
- Don't introduce new dependencies unless necessary

### 5. Verification
- Re-run the failing test
- Run related tests to check for regressions
- If still failing → iterate (max 3 attempts)

### 6. Report
```
## Fix Applied
- Root cause: [description]
- Fix: [what was changed]
- Tests: X/Y passing
- Files modified: [list]
```

## Rules
- Apply MINIMAL changes — fix the bug, don't refactor
- Max 3 fix-verify iterations before asking user for help
- Always verify fix with tests
- Never introduce new dependencies just to fix a bug

## Related Skills & Agents
- `debugger` agent — Deep root cause analysis
- `sequential-thinking` — Step-by-step reasoning for complex bugs
- `test` — Invokes this skill via `--fix` flag
- `execute` — Invokes this skill when verification fails
