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
Before implementation, use the `mp-plan` skill or delegate to `mp-planner` agent to create a plan with TODO tasks tracked in the SQL `todos` table (via `sql` tool).

Use multiple `mp-researcher` agents in parallel to research different technical topics; feed results back to `mp-planner`.

### 2. Implementation
- Use `mp-execute` skill to execute plans phase-by-phase with verification gates
- Write clean, readable, maintainable code following established architectural patterns
- Handle edge cases and error scenarios
- **DO NOT** create new "enhanced" copies — update existing files directly
- After modifying code, run the compile/build command to check for errors

### 3. Testing
- Use `mp-test` skill for auto-detected test execution with structured reporting
- Test error scenarios and validate performance requirements
- **DO NOT** ignore failing tests or use fake data/mocks to pass builds
- Use `mp-fix` skill to diagnose and fix failures, then re-run until all pass

### 4. Code Review
Use `mp-code-review` skill for structured scout→review→fix pipeline, or `mp-code-reviewer` agent for quick reviews.

### 5. Integration & Documentation
- Follow the plan; ensure seamless integration with existing code
- Maintain backward compatibility; document breaking changes
- Use `mp-docs` skill to update documentation based on code changes

### 6. Git & Release
Use `mp-git` skill for conventional commits with security scanning and PR creation.

### 7. Debugging
When bugs are reported, use `mp-fix` skill or delegate to `mp-debugger` agent. Fix, then re-run tests.

## Skills Catalog

Invoke via the `skill` tool:

| Skill | Purpose |
|-------|---------|
| `mp-plan` | Implementation planning, task breakdown |
| `mp-execute` | Execute plans phase-by-phase with test/review gates |
| `mp-test` | Auto-detect and run tests with structured reporting |
| `mp-fix` | Diagnose and fix bugs with root cause analysis |
| `mp-code-review` | Structured scout→review→fix pipeline |
| `mp-docs` | Initialize, update, and summarize documentation |
| `mp-git` | Conventional commits, security scanning, PR creation |
| `mp-brainstorm` | Structured ideation with approach comparison |
| `mp-scout` | Fast codebase exploration and search |
| `mp-research` | Technical research and evaluation |
| `mp-docs-seeker` | API/library documentation lookup (Context7) |
| `mp-sequential-thinking` | Step-by-step analysis of complex problems |

## Complete Workflow

| Step | Skill/Agent | Purpose |
|------|-------------|---------|
| 1. Brainstorm (optional) | `mp-brainstorm` | Explore approaches before planning |
| 2. Plan | `mp-plan` | Create implementation plan with phases |
| 3. Execute | `mp-execute` | Execute plan phases with test/review gates |
| 4. Test | `mp-test` | Run and verify tests |
| 5. Fix (if needed) | `mp-fix` | Debug and fix failures |
| 6. Review | `mp-code-review` | Structured code review |
| 7. Docs | `mp-docs` | Update documentation |
| 8. Commit | `mp-git` | Conventional commit with security scan |

## Sub-Agent Teams

Launch via the `task` tool with `agent_type`:

| Agent | `agent_type` | Purpose |
|-------|-------------|---------|
| Planner | `mp-planner` | Research + plan phases |
| Researcher | `mp-researcher` | Deep technical research |
| Code Reviewer | `mp-code-reviewer` | Review code changes |
| Debugger | `mp-debugger` | Root cause analysis, debugging |
| Explorer | `explore` | Fast codebase search |
| Task Runner | `task` | Build/test/lint commands |

**Model selection** (pass via `model` parameter):
- Heavy reasoning / architecture: `claude-opus-4.6`
- Standard implementation: `claude-sonnet-4.6`
- Fast/cheap searches: `claude-haiku-4.5`
- Alternative: `gemini-3-pro-preview`, `gpt-5.3-codex`

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
