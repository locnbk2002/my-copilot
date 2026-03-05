# Nyquist Validation

Map test files to plan requirements. Ensure test "sampling rate" covers requirements sufficiently.

## Trigger

Runs when `--nyquist` flag is set. Runs before test execution (or standalone if no other flags).

## Algorithm

### Step 1: Find Plan

1. Check for plan path argument
2. If none: scan `plans/` for most recent directory with `plan.md`
3. If no plan found: output "⚠️ No plan found — skipping Nyquist validation" and continue

### Step 2: Extract Requirements

For each `phase-XX-*.md` in the plan directory:
1. Extract **Success Criteria** section — each bullet = one requirement
2. Extract **Requirements > Functional** section — each item = one requirement
3. Extract unchecked todo items `- [ ] ...` — each = one requirement

Normalize: lowercase, strip markdown, tokenize into keywords (filter stop words).

### Step 3: Scan Test Files

Use glob patterns to find test files in project:
- `**/*.test.ts`, `**/*.test.js`, `**/*.test.tsx`
- `**/*.spec.ts`, `**/*.spec.js`
- `**/test_*.py`, `**/*_test.py`
- `**/*_test.go`, `**/*Test.java`

For each test file:
1. Read first 100 lines (test names are at top level)
2. Extract test names: `describe(`, `it(`, `test(`, `def test_`, `func Test`
3. Tokenize test names + file path → keywords

### Step 4: Map Requirements to Tests

For each requirement:
1. Get requirement keywords (nouns, verbs — ignore: the, a, is, are, for, to, with)
2. Score each test file: count keyword overlaps between requirement and test keywords
3. If score ≥ 2: mark requirement as covered by that test file (best score wins)
4. Record: requirement → test file, confidence (High: ≥4 matches, Medium: 2-3 matches)

### Step 5: Generate Coverage Report

Output structured markdown:

```markdown
## Nyquist Coverage Report

**Plan:** {plan-dir-name}
**Coverage:** {tested}/{total} requirements ({percentage}%)

### ✅ Covered Requirements ({N})
| Requirement | Test File | Confidence |
|-------------|-----------|------------|
| {req summary, max 60 chars} | {relative test path} | High/Medium |

### ❌ Uncovered Requirements ({N})
| Requirement | Source Phase | Suggested Test Name |
|-------------|-------------|---------------------|
| {req summary} | phase-0N | test_{snake_case_req_name} |

### ⚠️ Orphan Tests ({N})
Tests found but not matched to any plan requirement:
| Test File | Inferred Purpose |
|-----------|-----------------|
| {test path} | {inferred from filename} |
```

### Step 6: Coverage Gate

- Coverage ≥ 80%: proceed with test execution (log report)
- Coverage < 80%: `ask_user`:
  - "Only {X}% of requirements have passing tests. What to do?"
  - Options: "Run tests anyway (Recommended)", "Generate missing test stubs first", "Abort"
- If standalone (`--nyquist` only): output report only, no gate check needed

## Notes

- Keyword matching is heuristic — false negatives are acceptable (better than false positives)
- Orphan tests are not failures — they may test non-plan features
- Coverage % = covered_requirements / total_requirements (not line coverage)
