---
applyTo: "**/*"
---

# Orchestration Protocol

## Delegation Context (MANDATORY)

When spawning sub-agents via the `task` tool, **ALWAYS** include in the prompt:

1. **Work Context Path**: The git root of the primary files being worked on
2. **Reports Path**: `{work_context}/plans/reports/`
3. **Plans Path**: `{work_context}/plans/`

**Example prompt:**
```
Fix parser bug.
Work context: /path/to/project
Reports: /path/to/project/plans/reports/
Plans: /path/to/project/plans/
```

**Rule:** If CWD differs from the work context (editing files in a different project), use the **work context paths**, not CWD paths.

---

## Sequential Chaining

Chain sub-agents when tasks have dependencies or require outputs from previous steps:

- **Planning → Implementation → Testing → Review**: Use for feature development
- **Research → Design → Code → Documentation**: Use for new system components
- Each agent completes fully before the next begins
- Pass context and outputs between agents in the chain

## Parallel Execution

Spawn multiple sub-agents simultaneously for independent tasks:

- **Code + Tests + Docs**: When implementing separate, non-conflicting components
- **Multiple features**: Different agents working on isolated features
- **Careful coordination**: Ensure no file conflicts or shared resource contention
- **Merge strategy**: Plan integration points before parallel execution begins

---

## Agent Reference

Launch via the `task` tool:

```python
task(
  agent_type="planner",   # or explore, task, general-purpose, researcher, debugger, multimodal
  description="Plan auth feature",
  prompt="...",
  model="claude-sonnet-4.6"  # optional
)
```

| Agent | `agent_type` | Best For |
|-------|-------------|----------|
| Planner | `planner` | Architecture, implementation plans |
| Researcher | `researcher` | Deep technical research, library evaluation |
| Code Reviewer | `code-reviewer` | Reviewing diffs and PRs |
| Debugger | `debugger` | Root cause analysis, debugging |
| Multimodal | `multimodal` | UI/screenshot analysis, visual debugging |
| Worker | `worker` | Category-aware phase orchestrator |
| Explorer | `explore` | Fast codebase search and questions |
| Task Runner | `task` | Build, test, lint commands |
| General Purpose | `general-purpose` | Complex multi-step tasks |

**Model selection** (via `model` parameter):

| Use Case | Model |
|----------|-------|
| Heavy reasoning, architecture | `claude-opus-4.6` |
| Standard implementation | `claude-sonnet-4.6` |
| Fast/cheap search | `claude-haiku-4.5` |
| Large context / broad sweeps | `gpt-5.3-codex` |
| Multimodal / visual analysis | `gemini-3-pro-preview` |

---

## Task Tracking with SQL

Use the `sql` tool to manage todos across the session:

```sql
-- Create tasks with dependency tracking
INSERT INTO todos (id, title, description, status) VALUES
  ('plan-auth', 'Plan auth module', 'JWT auth in src/auth/', 'pending'),
  ('impl-auth', 'Implement auth', 'Based on plan-auth output', 'pending');

INSERT INTO todo_deps (todo_id, depends_on) VALUES ('impl-auth', 'plan-auth');

-- Query ready todos (no pending dependencies)
SELECT t.* FROM todos t
WHERE t.status = 'pending'
AND NOT EXISTS (
  SELECT 1 FROM todo_deps td
  JOIN todos dep ON td.depends_on = dep.id
  WHERE td.todo_id = t.id AND dep.status != 'done'
);

-- Update status as you work
UPDATE todos SET status = 'in_progress' WHERE id = 'plan-auth';
UPDATE todos SET status = 'done' WHERE id = 'plan-auth';
```

---

## Plans Directory Structure

Save plans in `./plans` with timestamp and descriptive name:

```
plans/
└── 20251101-1505-authentication-implementation/
    ├── plan.md                          # Overview, phases, progress
    ├── research/
    │   └── researcher-01-report.md
    ├── reports/
    │   ├── scout-report.md
    │   └── researcher-report.md
    ├── phase-01-setup-environment.md
    ├── phase-02-implement-database.md
    ├── phase-03-implement-api-endpoints.md
    └── phase-04-write-tests.md
```

### Plan File Guidelines

**`plan.md`** (overview): Keep under 80 lines. List phases with status, links to phase files, key dependencies.

**`phase-XX-name.md`** (detail): Include —
- Context links (reports, docs, files)
- Overview (priority, status, description)
- Key insights from research
- Functional and non-functional requirements
- Architecture and data flow
- Related code files (modify / create / delete)
- Numbered implementation steps
- Todo checklist
- Success criteria and definition of done
- Risk assessment and mitigation
- Security considerations
- Next steps and dependencies
