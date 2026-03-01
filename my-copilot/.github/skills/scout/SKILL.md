---
name: scout
description: "Fast codebase scouting using parallel agents. Use for file discovery, task context gathering, quick searches across directories."
argument-hint: "[search-target] [ext]"
---

# Scout

Fast, token-efficient codebase scouting using parallel agents to find files needed for tasks.

## Arguments
- Default: Scout using built-in `explore` subagents in parallel (`./references/internal-scouting.md`)
- `ext`: Scout using specific models with large context windows (Gemini/Grok-code) (`./references/external-scouting.md`)

## When to Use

- Beginning work on feature spanning multiple directories
- User mentions needing to "find", "locate", or "search for" files
- Starting debugging session requiring file relationships understanding
- User asks about project structure or where functionality lives
- Before changes that might affect multiple codebase parts

## Quick Start

1. Analyze user prompt to identify search targets
2. Use `grep` and `glob` tools to find relevant files and estimate codebase scale
3. Spawn parallel agents with divided directories
4. Collect results into concise report

## Workflow

### 1. Analyze Task
- Parse user prompt for search targets
- Identify key directories, patterns, file types, lines of code
- Determine optimal SCALE value (number of subagents to spawn)

### 2. Divide and Conquer
- Split codebase into logical segments per agent
- Assign each agent specific directories or patterns
- Ensure no overlap, maximize coverage

### 3. Register Scout Todos
- **Skip if:** Agent count ≤ 2 (overhead exceeds benefit)
- Check existing todos in session SQL database first
- If not found, INSERT a todo per agent with scope metadata
- See `references/task-management-scouting.md` for SQL patterns

### 4. Spawn Parallel Agents
Load appropriate reference based on decision tree:
- **Internal (Default):** `references/internal-scouting.md` (explore subagents via `task` tool)
- **External:** `references/external-scouting.md` (Gemini / Grok-code via `task` tool with model parameter)

**Notes:**
- Update todo status to `in_progress` before spawning each agent
- Give each subagent detailed instructions with exact directories or files to search
- Each subagent has limited context — keep scope focused
- Number of subagents depends on codebase size and search complexity
- Each subagent must return a detailed summary report

### 5. Collect Results
- Timeout: 3 minutes per agent (skip non-responders)
- Mark completed todos `done`; log timed-out agents in report
- Aggregate findings into single report
- List unresolved questions at end

## Report Format

```markdown
# Scout Report

## Relevant Files
- `path/to/file.ts` - Brief description
- ...

## Unresolved Questions
- Any gaps in findings
```

## References

- `references/internal-scouting.md` - Using `explore` subagents via `task` tool
- `references/external-scouting.md` - Using Gemini / Grok-code models via `task` tool with model parameter
- `references/task-management-scouting.md` - SQL todo patterns for scout coordination
