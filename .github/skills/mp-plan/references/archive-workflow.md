# Archive Workflow

## Your mission
Read and analyze the plans, then write journal entries and archive specific plans or all plans in the `plans` directory.

## Plan Resolution
1. If arguments provided → Use that path
2. Else read all plans in the `plans` directory

## Workflow

### Step 1: Read Plan Files

Read the plan directory:
- `plan.md` - Overview and phases list
- `phase-*.md` - 20 first lines of each phase file to understand the progress and status

### Step 2: Summarize the plans and offer to document journal entries
Use `ask_user` tool to ask if user wants to write journal entries.
Skip this step if user selects "No".
If user selects "Yes":
- Analyze the information from previous steps.
- Use `task` tool with `agent_type: "general-purpose"` in parallel to document each plan.
- Write journal entries to `./docs/journals/` directory using bash/create tools.
- Journal entries should be concise and focused on the most important events, key changes, impacts, and decisions.

### Step 3: Ask user to confirm archiving
Use `ask_user` tool to present options:
- Archive all completed plans
- Select specific plans to archive
- Cancel

Use `ask_user` to ask if user wants to delete permanently or move to `./plans/archive` directory.

### Step 4: Archive the plans
Start archiving based on the user's choice:
```bash
# Move to archive
mv ./plans/<plan-dir> ./plans/archive/

# Or delete permanently
rm -rf ./plans/<plan-dir>
```

### Step 5: Ask if user wants to commit the changes
Use `ask_user` with these options:
- Stage and commit the changes (`git add -A && git commit -m "chore: archive plans"`)
- Commit and push (`git add -A && git commit -m "chore: archive plans" && git push`)
- Skip for now

## Output
After archiving the plans, provide summary:
- Number of plans archived
- Number of plans deleted permanently
- Table of plans that are archived or deleted (title, status, created date)
- Table of journal entries that are created (title, date)

## Important Notes
- Only ask questions about genuine decision points
- Sacrifice grammar for concision
- List any unresolved questions at the end
- Ensure token efficiency while maintaining high quality
