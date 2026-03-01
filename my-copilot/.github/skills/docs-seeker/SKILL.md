---
name: docs-seeker
description: "Search library/framework documentation via Context7 MCP tools. Use for API docs, GitHub repository analysis, technical documentation lookup, latest library features."
argument-hint: "[library-name] [topic]"
---

# Documentation Discovery via Context7

## Overview

Documentation discovery using the built-in Context7 MCP tools:
- `context7-resolve-library-id` — find the library ID from a name
- `context7-query-docs` — fetch targeted documentation with a topic query

## Primary Workflow

**ALWAYS follow this order:**

### Step 1: Resolve Library ID

Call `context7-resolve-library-id` with the library name and your specific question:

```
context7-resolve-library-id(
  libraryName: "next.js",
  query: "How do I implement caching in Next.js?"
)
```

Returns a list of matching libraries with IDs like `/vercel/next.js`. Select the best match based on:
- Name similarity to query
- Source reputation (High > Medium > Low)
- Code snippet count (more = better coverage)
- Benchmark score

### Step 2: Query Documentation

Call `context7-query-docs` with the resolved library ID and a specific question:

```
context7-query-docs(
  libraryId: "/vercel/next.js",
  query: "caching strategies for App Router"
)
```

Returns targeted documentation and code examples for that topic.

### Step 3: Fallback — Repository Analysis

If Context7 has no results for a library:
Load: `references/repo-analysis.md`

## Query Types

### Topic-Specific (Fastest)
User asks about specific feature/component:
```
"How do I use date picker in shadcn?"
→ resolve: "shadcn/ui"
→ query: "date picker component usage"
```

### General Library
User asks for broad documentation:
```
"Documentation for Astro"
→ resolve: "astro"
→ query: "getting started overview concepts"
```

### Parallel Multi-Library
When comparing or integrating multiple libraries, call both tools in parallel:
```
Resolve "react-query" + resolve "swr" simultaneously
Then query both in parallel
```

## Execution Principles

1. **Resolve before querying** — always get the library ID first
2. **Be specific in queries** — "date picker usage examples" beats "date"
3. **Parallel when possible** — resolve multiple libraries in one response
4. **Fallback to repo analysis** — if Context7 returns no results

## References

- `references/repo-analysis.md` — Fallback: direct GitHub/web analysis when Context7 unavailable
