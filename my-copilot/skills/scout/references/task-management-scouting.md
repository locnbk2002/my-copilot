# Scout Task Management Patterns

Track parallel scout agent execution via session SQL todos (`todos` and `todo_deps` tables).

## When to Create Todos

| Agents | Create Todos? | Rationale |
|--------|--------------|-----------|
| ≤ 2    | No           | Overhead exceeds benefit, finishes quickly |
| ≥ 3    | Yes          | Meaningful coordination, progress monitoring |

## Todo Registration Flow

```sql
-- Check for existing scout todos first
SELECT * FROM todos WHERE id LIKE 'scout-%' AND status != 'done';
-- Found?  → Reuse existing
-- Empty?  → INSERT per agent (see schema below)
```

## SQL Schema

```sql
INSERT INTO todos (id, title, description, status) VALUES
  ('scout-1-of-6',
   'Scout src/auth/ for auth files',
   'Search src/auth/, src/middleware/ for authentication-related files. agentType=explore scope=src/auth/,src/middleware/ scale=6 agentIndex=1 totalAgents=6 toolMode=internal effort=3m',
   'pending');
```

### Required Info in Description

Encode agent metadata in the description field:
- `agentType` — `explore` (internal) or `explore+model` (external with specific model)
- `scope` — Comma-separated directory boundaries for this agent
- `scale` — Total SCALE value determined in analysis
- `agentIndex` / `totalAgents` — Position tracking (e.g., 3 of 6)
- `toolMode` — `internal` or `external`
- `effort` — Always `3m` (fixed timeout)

### ID Convention

Use `scout-{agentIndex}-of-{totalAgents}` for easy querying:
- `scout-1-of-6`, `scout-2-of-6`, ..., `scout-6-of-6`

## Todo Lifecycle

```sql
-- Step 3: INSERT per agent
INSERT INTO todos (id, title, description, status) VALUES ('scout-1-of-6', ..., 'pending');

-- Step 4: Before spawning agent
UPDATE todos SET status = 'in_progress' WHERE id = 'scout-1-of-6';

-- Step 5: Agent returns report
UPDATE todos SET status = 'done' WHERE id = 'scout-1-of-6';

-- Step 5: Agent times out (3m) — mark blocked with note
UPDATE todos SET status = 'blocked', description = description || ' [TIMEOUT]' WHERE id = 'scout-3-of-6';
```

## Examples

### Internal Scouting (SCALE=6)

```sql
-- Register 6 scout todos
INSERT INTO todos (id, title, description, status) VALUES
  ('scout-1-of-6', 'Scout src/auth/ for auth files',
   'Search src/auth/, src/middleware/. agentType=explore scale=6 agentIndex=1 totalAgents=6 toolMode=internal effort=3m', 'pending'),
  ('scout-2-of-6', 'Scout src/api/ for auth endpoints',
   'Search src/api/, src/routes/. agentType=explore scale=6 agentIndex=2 totalAgents=6 toolMode=internal effort=3m', 'pending'),
  ('scout-3-of-6', 'Scout tests/ for auth tests',
   'Search tests/. agentType=explore scale=6 agentIndex=3 totalAgents=6 toolMode=internal effort=3m', 'pending');
-- ... repeat for agents 4-6
```

### External Scouting (SCALE=3, gpt-5.3-codex)

```sql
INSERT INTO todos (id, title, description, status) VALUES
  ('scout-1-of-3', 'Scout db/ for migrations via gpt-5.3-codex model',
   'Search db/, migrations/. agentType=explore model=gpt-5.3-codex scale=3 agentIndex=1 totalAgents=3 toolMode=external effort=3m', 'pending');
```

## Query Helpers

```sql
-- All scout todos for this session
SELECT id, title, status FROM todos WHERE id LIKE 'scout-%';

-- Count by status
SELECT status, COUNT(*) FROM todos WHERE id LIKE 'scout-%' GROUP BY status;

-- Timed out agents
SELECT id, title FROM todos WHERE id LIKE 'scout-%' AND status = 'blocked';
```

## Quality Check Output

After registration: `✓ Registered [N] scout todos ([internal|external] mode, SCALE={scale})`

## Error Handling

If INSERT fails: log warning, continue without todo tracking. Scouting remains fully functional — todos add observability, not functionality.
