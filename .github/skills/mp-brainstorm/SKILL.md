---
name: mp-brainstorm
description: "Structured brainstorming with approach comparison, risk assessment, and handoff to planning. Use for ideation, technical exploration, approach evaluation, solution discovery."
argument-hint: "[topic] [--visual] [--report]"
license: MIT
---

# Structured Brainstorming

Explore approaches, compare tradeoffs, and converge on a recommendation.

## Invocation

```
mp-brainstorm [topic] [--visual] [--report]

Default: Interactive brainstorming session
--visual: Include Mermaid diagrams in output
--report: Generate formal brainstorm report to plans/brainstorm-{topic}.md
```

## When to Use
- Before planning, when the approach is unclear
- To evaluate multiple technical options
- When exploring new problem spaces
- To make informed architecture decisions

## Workflow

### 1. Context Gathering
- Read project README, architecture docs
- Dispatch `task(agent_type="explore")` to understand relevant codebase areas
- Ask clarifying questions via `ask_user` (constraints, goals, non-goals)

### 2. Discovery
- Identify constraints (technical, business, time)
- Map existing patterns and conventions
- Research alternatives via `web_search` or `mp-docs-seeker` skill

### 3. Ideation
Generate 2-4 approaches for the topic. For each:
- **Description**: What is the approach?
- **Pros**: Advantages
- **Cons**: Disadvantages
- **Effort**: Relative (Low/Medium/High)
- **Risk**: What could go wrong?
- **YAGNI/KISS/DRY alignment**: Does it pass the holy trinity?

### 4. Debate & Challenge
- Play devil's advocate against each approach
- Ask "What could go wrong?" for each
- Identify hidden dependencies and second-order effects
- Check for premature optimization or over-engineering

### 5. Recommendation
- Rank approaches by value/effort ratio
- Recommend one approach with clear rationale
- If `--report`: write formal report to `plans/brainstorm-{topic}.md`
- If `--visual`: include Mermaid architecture diagram

### 6. Handoff
- Ask user: "Want to plan this with `mp-plan`?" via `ask_user`
- If yes: provide the chosen approach as context for planning

## Output Format

```markdown
## Brainstorm: {Topic}

### Approaches

| # | Approach | Effort | Risk | Recommendation |
|---|---------|--------|------|---------------|
| 1 | {name} | Low | Low | ⭐ Recommended |
| 2 | {name} | Medium | Medium | Alternative |
| 3 | {name} | High | Low | Over-engineered |

### Approach 1: {name} ⭐
**Description:** ...
**Pros:** ...
**Cons:** ...
**Risk:** ...

### Approach 2: {name}
...

### Recommendation
{Approach N} because {rationale}. Aligns with YAGNI/KISS/DRY because {why}.

### Next Steps
- Plan with `mp-plan` to create implementation roadmap
```

## Rules
- Always generate at least 2 approaches (one simple, one thorough)
- Be honest about tradeoffs — no "this is perfect" answers
- Favor simpler approaches unless complexity is justified
- Include effort and risk for every approach

## Related Skills
- `mp-plan` — Create implementation plan from chosen approach
- `mp-research` — Deep research on specific technologies
- `mp-docs-seeker` — Look up library documentation
- `mp-sequential-thinking` — Step-by-step analysis of complex tradeoffs
