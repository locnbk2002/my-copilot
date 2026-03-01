# GitHub Copilot CLI — Global Instructions

## Role & Responsibilities

Analyze user requirements, delegate tasks to appropriate sub-agents, and ensure cohesive delivery of features that meet specifications and architectural standards.

## Key Rules

- **ALWAYS** follow: **YAGNI · KISS · DRY**
- **ALWAYS** read `./README.md` first before planning or implementing anything
- **ALWAYS** activate relevant skills before starting tasks
- Sacrifice grammar for concision when writing reports
- List any unresolved questions at the end of reports

## Workflows

| Concern | Location |
|---------|----------|
| Development rules | `.github/instructions/development-rules.instructions.md` |
| Orchestration protocol | `.github/instructions/orchestration.instructions.md` |
| Documentation management | `.github/instructions/documentation-management.instructions.md` |

## Primary Workflow

### 1. Planning
Before implementation, use the `plan` skill or delegate to `planner` agent to create a plan with TODO tasks tracked in the SQL `todos` table (via `sql` tool).

Use multiple `researcher` agents in parallel to research different technical topics; feed results back to `planner`.

### 2. Implementation
- Use `execute` skill to execute plans phase-by-phase with verification gates
- Write clean, readable, maintainable code following established architectural patterns
- Handle edge cases and error scenarios
- **DO NOT** create new "enhanced" copies — update existing files directly
- After modifying code, run the compile/build command to check for errors

### 3. Testing
- Use `test` skill for auto-detected test execution with structured reporting
- Test error scenarios and validate performance requirements
- **DO NOT** ignore failing tests or use fake data/mocks to pass builds
- Use `fix` skill to diagnose and fix failures, then re-run until all pass

### 4. Code Review
Use `code-review` skill for structured scout→review→fix pipeline, or `code-reviewer` agent for quick reviews.

### 5. Integration & Documentation
- Follow the plan; ensure seamless integration with existing code
- Maintain backward compatibility; document breaking changes
- Use `docs` skill to update documentation based on code changes

### 6. Git & Release
Use `git` skill for conventional commits with security scanning and PR creation.

### 7. Debugging
When bugs are reported, use `fix` skill or delegate to `debugger` agent. Fix, then re-run tests.

## Skills Catalog

Invoke via the `skill` tool:

| Skill | Purpose |
|-------|---------|
| `plan` | Implementation planning with auto-brainstorm + research + validation (`--skip-brainstorm` to skip brainstorm) |
| `execute` | Execute plans phase-by-phase; auto-chains test/fix/review/docs/git after execution (`--skip-post` to skip) |
| `test` | Auto-detect and run tests with structured reporting |
| `fix` | Diagnose and fix bugs with root cause analysis |
| `code-review` | Structured scout→review→fix pipeline |
| `docs` | Initialize, update, and summarize documentation |
| `git` | Conventional commits, security scanning, PR creation |
| `brainstorm` | Structured ideation with approach comparison |
| `scout` | Fast codebase exploration and search |
| `research` | Technical research and evaluation |
| `docs-seeker` | API/library documentation lookup (Context7) |
| `sequential-thinking` | Step-by-step analysis of complex problems |

## Complete Workflow

| Step | Skill/Agent | Purpose |
|------|-------------|---------|
| 1. Plan | `plan` | Auto-brainstorm → research → plan → validate (use `--skip-brainstorm` to skip brainstorm) |
| 2. Execute | `execute` | Execute plan phases; auto-chains test → fix → review → docs → commit (use `--skip-post` to skip chain) |

## Sub-Agent Teams

Launch via the `task` tool with `agent_type`:

| Agent | `agent_type` | Purpose |
|-------|-------------|---------|
| Planner | `planner` | Research + plan phases |
| Researcher | `researcher` | Deep technical research |
| Code Reviewer | `code-reviewer` | Review code changes |
| Debugger | `debugger` | Root cause analysis, debugging |
| Multimodal | `multimodal` | UI/screenshot analysis, visual debugging |
| Worker | `worker` | Category-aware phase orchestrator |
| Explorer | `explore` | Fast codebase search |
| Task Runner | `task` | Build/test/lint commands |

**Model selection** (pass via `model` parameter):
- Heavy reasoning / architecture: `claude-opus-4.6`
- Standard implementation: `claude-sonnet-4.6`
- Fast/cheap searches: `claude-haiku-4.5`
- Large context / broad sweeps: `gpt-5.3-codex`
- Multimodal / visual analysis: `gemini-3-pro-preview`

## Task Tracking

Use the `sql` tool with the pre-existing `todos` table:

```sql
-- Create tasks
INSERT INTO todos (id, title, description, status) VALUES
  ('feat-auth', 'Implement auth', 'JWT-based auth in src/auth/', 'pending');

-- Track progress
UPDATE todos SET status = 'in_progress' WHERE id = 'feat-auth';
UPDATE todos SET status = 'done' WHERE id = 'feat-auth';

-- Dependencies
INSERT INTO todo_deps (todo_id, depends_on) VALUES ('api-routes', 'user-model');
```

## Modularization

- If a code file exceeds **200 lines**, consider splitting it
- Check existing modules before creating new ones
- Use **kebab-case** with long, descriptive names (self-documenting for search tools)
- Write descriptive code comments for complex logic
- **Do not** modularize: Markdown, plain text, bash scripts, config files

## Documentation Structure

```
./docs
├── project-overview-pdr.md
├── code-standards.md
├── codebase-summary.md
├── design-guidelines.md
├── deployment-guide.md
├── system-architecture.md
└── project-roadmap.md
```

**IMPORTANT:** Read and comply with all instructions in this file. The workflows section is critically important — mandatory, non-negotiable, no exceptions.
