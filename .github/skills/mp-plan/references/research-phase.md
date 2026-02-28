# Research & Analysis Phase

**When to skip:** If provided with researcher reports, skip this phase.

## Core Activities

### Parallel Researcher Agents
- Spawn multiple `explore` agents (via `task` tool with `agent_type: "explore"`) in parallel
- Each agent investigates a specific aspect or approach
- Wait for all agents to report back before proceeding

### Sequential Thinking
- Use the `mp-sequential-thinking` skill (`.github/skills/mp-sequential-thinking/SKILL.md`) for structured, reflective problem-solving
- Apply when analyzing complex multi-step problems or debugging unknown root causes
- Use visible thought markers (Thought N/N) when reasoning needs to be transparent

### Documentation Research
- Use the `mp-docs-seeker` skill (`.github/skills/mp-docs-seeker/SKILL.md`) to find library/framework documentation via Context7 MCP tools
- Use `web_search` for general research and latest information
- Fetch documentation pages directly with `web_fetch` when needed

### GitHub Analysis
- Use `gh` command to read and analyze:
  - GitHub Actions logs
  - Pull requests
  - Issues and discussions
- Extract relevant technical context from GitHub resources
- Use GitHub MCP tools (search_code, list_issues, pull_request_read) for deeper analysis

### Remote Repository Analysis
When given a GitHub repository URL and Context7 has no results, use `mp-docs-seeker` fallback (`repo-analysis.md`) or:
```bash
repomix --remote <github-repo-url>
```

### Debugger Delegation
- Use `task` tool with `agent_type: "general-purpose"` for root cause analysis
- Use when investigating complex issues or bugs

## Best Practices

- Research breadth before depth
- Document findings for synthesis phase
- Identify multiple approaches for comparison
- Consider edge cases during research
- Note security implications early
