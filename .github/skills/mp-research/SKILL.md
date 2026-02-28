---
name: mp-research
description: "Research technical solutions, analyze architectures, gather requirements thoroughly. Use for technology evaluation, best practices research, solution design, scalability/security/maintainability analysis."
license: MIT
argument-hint: "[topic]"
---

# Research

## Research Methodology

Always honoring **YAGNI**, **KISS**, and **DRY** principles.
**Be honest, be brutal, straight to the point, and be concise.**

### Phase 1: Scope Definition

Clearly define the research scope:
- Identify key terms and concepts to investigate
- Determine recency requirements (how current must information be)
- Establish evaluation criteria for sources
- Set boundaries for research depth

### Phase 2: Systematic Information Gathering

Employ a multi-source research strategy:

1. **Search Strategy**:
   - Use `web_search` tool for all searches — run multiple searches in parallel (up to 5 simultaneous calls)
   - Craft precise search queries with relevant keywords
   - Include terms like "best practices", "2025", "latest", "security", "performance"
   - Search for official documentation, GitHub repositories, and authoritative blogs
   - Prioritize results from recognized authorities (official docs, major tech companies, respected developers)
   - **IMPORTANT**: Perform at most **5 searches total**, think carefully before each one

2. **Deep Content Analysis**:
   - Use `web_fetch` to read key pages found in search results
   - For GitHub repositories, use the `mp-docs-seeker` skill (`.github/skills/mp-docs-seeker/SKILL.md`) to fetch documentation via Context7 MCP tools
   - Analyze README files from popular GitHub repositories
   - Review changelogs and release notes for version-specific information

3. **Large Context Searches**:
   - For broad topic sweeps, use `task` tool with `model: "gpt-5.3-codex"` (large context, code-optimized):
     ```
     task(agent_type="mp-researcher", model="gpt-5.3-codex",
          prompt="Research [topic] comprehensively. Cover: official docs, best practices, security, performance, comparisons.")
     ```

4. **Cross-Reference Validation**:
   - Verify information across multiple independent sources
   - Check publication dates to ensure currency
   - Identify consensus vs. controversial approaches
   - Note any conflicting information or debates

### Phase 3: Analysis and Synthesis

Analyze gathered information by:
- Identifying common patterns and best practices
- Evaluating pros and cons of different approaches
- Assessing maturity and stability of technologies
- Recognizing security implications and performance considerations
- Determining compatibility and integration requirements

### Phase 4: Report Generation

Save the report to the output path provided by the caller, or default to `plans/reports/`.

Get timestamp:
```bash
date +%y%m%d-%H%M
```

Report filename: `{output-path}/researcher-{timestamp}-{topic-slug}.md`

Report structure:

```markdown
# Research Report: [Topic]

**Date**: YYYY-MM-DD
**Sources consulted**: N
**Search terms**: [list]

## Executive Summary
[2-3 paragraphs: key findings and recommendations]

## Key Findings

### 1. Technology Overview
[Comprehensive description]

### 2. Current State & Trends
[Latest developments, version info, adoption trends]

### 3. Best Practices
[Recommended practices with explanations]

### 4. Security Considerations
[Security implications, vulnerabilities, mitigations]

### 5. Performance Insights
[Performance characteristics, optimization techniques]

## Comparative Analysis
[Comparison of solutions/approaches if applicable]

## Implementation Recommendations

### Quick Start
[Step-by-step getting started]

### Code Examples
[Relevant snippets with explanations]

### Common Pitfalls
[Mistakes to avoid]

## Resources & References

### Official Documentation
- [links]

### Recommended Reading
- [links with descriptions]

## Unresolved Questions
- [anything needing clarification]
```

## Quality Standards

- **Accuracy**: Verified across multiple sources
- **Currency**: Prioritize information from last 12 months unless historical context needed
- **Completeness**: Cover all requested aspects
- **Actionability**: Practical, implementable recommendations
- **Attribution**: Always cite sources with links

## Special Considerations

- For security topics: check recent CVEs and security advisories
- For performance topics: look for benchmarks and real-world case studies
- For new technologies: assess community adoption and support levels
- Always note deprecation warnings and migration paths

## Output Requirements

1. Save report to provided output path (or `plans/reports/` default)
2. Include timestamp in report header
3. Use code blocks with appropriate syntax highlighting
4. Conclude with specific, actionable next steps

**IMPORTANT**: Sacrifice grammar for concision.
**IMPORTANT**: List unresolved questions at the end.
**IMPORTANT**: You do NOT implement code — report findings only.
