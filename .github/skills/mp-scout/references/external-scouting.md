# External Scouting with Specific Models

Use specific models with large context windows (1M+ tokens) for faster, broader searches.

## Model Selection

```
SCALE <= 3  → gemini-3-pro-preview  (1M+ token context, fast for broad sweeps)
SCALE 4-5   → gpt-5.3-codex         (large context, code-optimized)
SCALE >= 6  → Use internal scouting instead
```

## How It Works

Use the `task` tool with the `model` parameter to target a specific model — no CLI tools required.

## Large Context Model — gemini-3-pro-preview (SCALE <= 3)

Spawn parallel `explore` agents using `model: "gemini-3-pro-preview"`:

```
Agent 1: task(agent_type="explore", model="gemini-3-pro-preview",
              prompt="Scout src/auth/, src/middleware/ for authentication files. List paths with brief descriptions.")
Agent 2: task(agent_type="explore", model="gemini-3-pro-preview",
              prompt="Scout src/api/, src/routes/ for authentication endpoints.")
Agent 3: task(agent_type="explore", model="gemini-3-pro-preview",
              prompt="Scout tests/ for authentication-related test files.")
```

## Grok-Code Model (SCALE 4-5)

Spawn parallel `explore` agents using `model: "gpt-5.3-codex"` (codex-optimized for code search):

```
Agent 1: task(agent_type="explore", model="gpt-5.3-codex",
              prompt="Scout db/, migrations/ for database migration files. List paths with descriptions.")
Agent 2: task(agent_type="explore", model="gpt-5.3-codex",
              prompt="Scout lib/, src/ for database schema and ORM files.")
Agent 3: task(agent_type="explore", model="gpt-5.3-codex",
              prompt="Scout config/ for database configuration files.")
Agent 4: task(agent_type="explore", model="gpt-5.3-codex",
              prompt="Scout tests/ for database-related test files.")
```

Spawn all in a single response for parallel execution.

## Prompt Guidelines

- Be specific about directories to search
- Request file paths with descriptions
- Set clear scope boundaries
- Ask for patterns/relationships if relevant

## Example Workflow

User: "Find database migration files" (SCALE=3 → gemini-3-pro-preview)

Spawn 3 parallel agents in one response:
```
Agent 1: task(agent_type="explore", model="gemini-3-pro-preview", prompt="Scout db/, migrations/ for migration files")
Agent 2: task(agent_type="explore", model="gemini-3-pro-preview", prompt="Scout lib/, src/ for database schema files")
Agent 3: task(agent_type="explore", model="gemini-3-pro-preview", prompt="Scout config/ for database configuration")
```

## Reading File Content

When needing to read file content, use chunking to stay within context limits (<150K tokens safe zone).

### Step 1: Get Line Counts
```bash
wc -l path/to/file1.ts path/to/file2.ts path/to/file3.ts
```

### Step 2: Calculate Chunks
- **Target:** ~500 lines per chunk (safe for most files)
- **Max files per agent:** 3-5 small files OR 1 large file chunked

**Chunking formula:**
```
chunks = ceil(total_lines / 500)
lines_per_chunk = ceil(total_lines / chunks)
```

### Step 3: Spawn Parallel Agents with Model

**Small files (<500 lines each):**
```
Agent 1: task(agent_type="explore", model="gemini-3-pro-preview",
              prompt="Read and summarize file1.ts and file2.ts")
Agent 2: task(agent_type="explore", model="gemini-3-pro-preview",
              prompt="Read and summarize file3.ts and file4.ts")
```

**Large file (>500 lines) — use `view` with view_range:**
```
Agent 1: task(agent_type="explore", model="gemini-3-pro-preview",
              prompt="Read lines 1-500 of large-file.ts using view tool with view_range [1,500]")
Agent 2: task(agent_type="explore", model="gemini-3-pro-preview",
              prompt="Read lines 501-1000 of large-file.ts using view tool with view_range [501,1000]")
```

### Chunking Decision Tree
```
File < 500 lines     → Read entire file
File 500-1500 lines  → Split into 2-3 chunks
File > 1500 lines    → Split into ceil(lines/500) chunks
```

Spawn all in a single response for parallel execution.

## Timeout and Error Handling

- Set 3-minute timeout per agent
- Skip timed-out agents
- Don't restart failed agents
- On persistent failures, fall back to internal scouting (`internal-scouting.md`)
