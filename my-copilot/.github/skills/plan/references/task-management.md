# Task Management Integration

## Session-Scoped Reality

Copilot session todos are stored in the **session SQL database** (`todos` and `todo_deps` tables).
Plan files (`plan.md`, `phase-XX.md` with checkboxes) are the **persistent** layer.

The **hydration pattern** bridges sessions:

```
┌──────────────────┐  Hydrate   ┌───────────────────┐
│ Plan Files       │ ─────────► │ SQL Todos         │
│ (persistent)     │            │ (session-scoped)  │
│ [ ] Phase 1      │            │ pending           │
│ [ ] Phase 2      │            │ pending           │
└──────────────────┘            └───────────────────┘
                                        │ Work
                                        ▼
┌──────────────────┐  Sync-back ┌───────────────────┐
│ Plan Files       │ ◄───────── │ Todo Updates      │
│ (updated)        │            │ (completed)       │
│ [x] Phase 1      │            │ done              │
│ [ ] Phase 2      │            │ in_progress       │
└──────────────────┘            └───────────────────┘
```

- **Hydrate:** Read plan files → INSERT todos per unchecked `[ ]` item
- **Work:** UPDATE todo status to `in_progress`/`done` in real-time
- **Sync-back:** Update `[ ]` → `[x]` in phase files, update plan.md frontmatter status

## When to Create Todos

**Default:** On — auto-hydrate after plan files are written
**Skip with:** `--no-tasks` flag in planning request
**3-Task Rule:** <3 phases → skip todos (overhead exceeds benefit)

| Scenario | Todos? | Why |
|----------|--------|-----|
| Multi-phase feature (3+ phases) | Yes | Track progress |
| Complex dependencies between phases | Yes | Automatic ordering |
| Single-phase quick fix | No | Just do it directly |
| Trivial 1-2 step plan | No | Overhead not worth it |

## Todo Creation Patterns

### Phase-Level INSERT

```sql
INSERT INTO todos (id, title, description, status) VALUES
  ('phase-01-setup', 'Setup environment and dependencies',
   'Install packages, configure env, setup database. See phase-01-setup.md', 'pending');
```

### Critical Step INSERT

For high-risk/complex steps within phases:

```sql
INSERT INTO todos (id, title, description, status) VALUES
  ('phase-03-oauth', 'Implement OAuth2 token refresh',
   'Handle token expiry, refresh flow, error recovery. See phase-03-api.md', 'pending');

INSERT INTO todo_deps (todo_id, depends_on) VALUES ('phase-03-oauth', 'phase-02-db');
```

## Naming Conventions

**id**: kebab-case with phase prefix: `phase-01-setup`, `phase-03-oauth`

**title** (imperative): Action verb + deliverable, <60 chars
- "Setup database migrations", "Implement OAuth2 flow", "Create user profile endpoints"

**description**: 1-2 sentences, concrete deliverables, reference phase file

## Dependency Chains

```sql
-- Phase 1 (no deps)
INSERT INTO todo_deps ... -- none

-- Phase 2 depends on Phase 1
INSERT INTO todo_deps (todo_id, depends_on) VALUES ('phase-02', 'phase-01');

-- Phase 3 depends on Phase 2
INSERT INTO todo_deps (todo_id, depends_on) VALUES ('phase-03', 'phase-02');
```

## Query Ready Todos

```sql
-- Find todos with no pending dependencies (ready to start)
SELECT t.* FROM todos t
WHERE t.status = 'pending'
AND NOT EXISTS (
    SELECT 1 FROM todo_deps td
    JOIN todos dep ON td.depends_on = dep.id
    WHERE td.todo_id = t.id AND dep.status != 'done'
);
```

## Cross-Session Resume

In a new session with an existing plan:
1. Read plan files to find unchecked `[ ]` phase items
2. Re-insert todos for unchecked items only (skip `[x]` items = done)
3. Rebuild dependency chain from phase order
4. Continue implementation from where left off

## Quality Checks

After todo hydration, verify:
- Dependency chain has no cycles
- All phases have corresponding todos
- Todo count matches unchecked `[ ]` items in plan files
- Output: `✓ Hydrated [N] phase todos + [M] critical step todos with dependency chain`
