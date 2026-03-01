# Validate Workflow

Interview the user with critical questions to validate assumptions, confirm decisions, and surface potential issues in an implementation plan before coding begins.

## Plan Resolution

1. If arguments provided → Use that path
2. Else check for active plan in `plans/` directory
3. If no plan found → Ask user to specify path or run `plan --hard` first

## Configuration

Default: 3-8 questions per session.

## Workflow

### Step 1: Read Plan Files
- `plan.md` - Overview and phases list
- `phase-*.md` - All phase files
- Look for decision points, assumptions, risks, tradeoffs

### Step 2: Extract Question Topics
Load: `references/validate-question-framework.md`

### Step 3: Generate Questions
For each detected topic, formulate a concrete question with 2-4 options.
Mark recommended option with "(Recommended)" suffix.

### Step 4: Interview User
Use `ask_user` tool.
- Ask 3-8 questions total
- Group related questions thematically
- Focus on: assumptions, risks, tradeoffs, architecture

### Step 5: Document Answers
Add or append `## Validation Log` section in `plan.md`.
Load: `references/validate-question-framework.md` for recording format.

### Step 6: Propagate Changes to Phases
Auto-propagate validation decisions to affected phase files.
Add marker: `<!-- Updated: Validation Session N - {change} -->`

## Output
- Number of questions asked
- Key decisions confirmed
- Phase propagation results
- Recommendation: proceed or revise

## Next Steps (MANDATORY)
After validation, remind user:

> **Best Practice:** Start a fresh conversation before implementing.
> Read `{ABSOLUTE_PATH_TO_PLAN_DIR}/plan.md` to re-hydrate context.
> Then implement phase by phase.
>
> **Why fresh context?** Planning context can bias implementation decisions.

## Important Notes
- Only ask about genuine decision points
- If plan is simple, fewer than min questions is okay
- Prioritize questions that could change implementation significantly
