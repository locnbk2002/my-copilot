# Discuss Workflow

Runs before research phase when `--discuss` flag is set. Captures user preferences to guide planning.

## When to Run

Before spawning researcher agents, after mode detection.

## Interview Questions

Ask via `ask_user`, one at a time. Allow user to skip any question.

1. "What are your tech stack preferences for this implementation? (e.g., 'prefer TypeScript over JavaScript', 'use PostgreSQL', 'avoid ORMs')"
2. "Any design pattern preferences? (e.g., 'repository pattern', 'functional over OOP', 'prefer composition')"
3. "Preferred error handling approach? (e.g., 'use Result types', 'try-catch with custom errors', 'let it crash + recover')"
4. "Testing philosophy? (e.g., 'TDD', 'integration tests over unit', '80% coverage minimum')"
5. "Code style preferences? (e.g., 'verbose over clever', 'minimal comments', 'strict typing')"
6. "Any hard constraints? (e.g., 'must ship by Friday', 'no new dependencies', 'backward compatible only')"
7. "Performance priorities? (e.g., 'optimize for latency', 'memory over speed', 'no premature optimization')"
8. "Anything else the plan should respect? (free text — optional)"

## Save Format

Save responses to `{plan-dir}/preferences.md`:

```markdown
# Implementation Preferences

Captured via `--discuss` mode on {YYYY-MM-DD}.

## Tech Stack
{answer or "No preference"}

## Design Patterns
{answer or "No preference"}

## Error Handling
{answer or "No preference"}

## Testing
{answer or "No preference"}

## Code Style
{answer or "No preference"}

## Constraints
{answer or "No preference"}

## Performance
{answer or "No preference"}

## Additional Notes
{answer or "None"}
```

## Feeding Into Research

When spawning researcher agents (`researcher`, `explore` via `task`), append to prompt:

```
## User Preferences (respect these in research and recommendations)
{2-3 line summary of non-skipped preferences}
```

When writing plan phase files, add a "## Constraints" or "## Preferences" section referencing the relevant preferences.

## Combinability

`--discuss` is a modifier — combine with any mode:
- `--discuss --fast` → interview, then fast plan (no research)
- `--discuss --hard` → interview, then hard plan (with research)
- `--discuss --two` → interview, then two-approach plan
- `--discuss --parallel` → interview, then parallel plan

## Graceful Handling

- If user skips all questions: proceed normally, skip preferences.md creation
- If plan-dir doesn't exist yet: save preferences.md after plan-dir is created
- Preferences are advisory — code-standards.md and system architecture always take precedence
