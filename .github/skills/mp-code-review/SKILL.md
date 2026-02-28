---
name: mp-code-review
description: "Orchestrate structured code reviews with scout→review→fix pipeline and severity classification. Use for code review, PR review, quality gates, pre-commit checks."
argument-hint: "[scope] [--staged] [--branch main] [--strict]"
license: MIT
---

# Code Review Orchestration

Structured code review with scout→review→fix pipeline and severity classification.

**Note:** This SKILL orchestrates the review workflow. The `mp-code-reviewer` AGENT (`.github/agents/mp-code-reviewer.agent.md`) performs the actual review.

## Invocation

```
mp-code-review [scope] [--staged] [--branch main] [--strict]

Default: Review unstaged changes
--staged: Review staged changes only
--branch: Review diff against branch (default: main)
--strict: Require all Critical/High issues addressed before passing
```

## When to Use
- After implementing changes, before committing
- As part of mp-execute review gate
- Before creating a pull request
- For quality assessment of specific files

## Workflow

Load: `references/review-workflow.md` for detailed workflow.

### 1. Scope Detection
- Get diff: `git diff` (unstaged) or `git diff --staged` or `git diff main..HEAD`
- If no diff found: ask user what to review via `ask_user`

### 2. Scout Phase (pre-review)
Dispatch `task(agent_type="explore")` to scan for:
- Missing error handling in changed code
- Edge cases not covered by tests
- Security concerns (exposed secrets, injection vectors)
- Callers/dependents of changed functions

### 2.5. Visual Review (optional)
If user provides screenshots or mentions UI/visual changes:
- Dispatch `task(agent_type="mp-multimodal")` with the screenshot(s) + relevant component paths
- Feed visual findings into Review Phase as additional context

### 3. Review Phase
Dispatch `task(agent_type="mp-code-reviewer")` with:
- The diff
- Scout findings as context
- Project conventions (from `.github/copilot-instructions.md`)

### 4. Issue Classification
| Severity | Examples | Action |
|----------|----------|--------|
| **Critical** | Security vuln, data loss, breaking change | Must fix |
| **High** | Logic error, missing error handling, perf issue | Should fix |
| **Medium** | Code smell, missing docs, maintainability | Consider fixing |
| **Low** | Style, naming, minor optimization | Optional |

### 5. Fix Loop (if `--strict` or Critical issues)
- Invoke `mp-fix` skill for each Critical/High issue
- Re-run review on fixed code
- Max 2 fix-review iterations

### 6. Verdict
```
## Review Result: ✅ PASS (or ❌ NEEDS WORK)
- Files reviewed: N
- Issues: X Critical, Y High, Z Medium
- Recommendation: [Ready to commit / Needs work]
```

## Rules
- Always run scout phase before review — context improves review quality
- Critical issues ALWAYS block the review (even without `--strict`)
- Don't nitpick style or formatting — focus on bugs, security, logic
- Include positive observations alongside issues

## Related Skills & Agents
- `mp-code-reviewer` agent — Performs the actual code review
- `mp-multimodal` agent — UI/screenshot analysis for visual review
- `mp-fix` — Fixes Critical/High issues found during review
- `mp-execute` — Invokes this skill as review gate
- `mp-git` — Typically invoked after review passes
