## Fix Workflow

### Error Classification

| Type | Indicators | Typical Fix |
|------|-----------|-------------|
| Import/Module | `Cannot find module`, `ModuleNotFoundError` | Fix import path, install dependency |
| Type Error | `TypeError`, `is not a function` | Fix type mismatch, add null check |
| Logic Error | Wrong output, assertion failure | Fix conditional, algorithm, data flow |
| Runtime Error | `ReferenceError`, `NullPointerException` | Add guard clause, initialize variable |
| Config Error | `ENOENT`, missing env var | Fix path, add config, set default |
| Async Error | `Unhandled Promise`, race condition | Add await, fix timing, add lock |

### Fix Strategy

1. **Read the error** — understand exactly what went wrong
2. **Find the source** — trace to the root file and line
3. **Understand context** — read surrounding code (±20 lines)
4. **Plan the fix** — decide minimal change needed
5. **Apply the fix** — use `edit` tool
6. **Verify** — re-run the specific test

### Iteration Protocol

- **Attempt 1**: Apply the most likely fix based on error analysis
- **Attempt 2**: If first fix didn't work, dispatch `debugger` for deeper analysis
- **Attempt 3**: Try alternative approach based on debugger findings
- **After 3 attempts**: Mark as blocked, report to user with full context

### When Invoked by test

The fix skill receives:
- Test framework name
- Specific test file and line
- Error message and stack trace
- Expected vs actual values

Use this structured input to skip the error analysis step and go straight to root cause.
