# Repository Analysis (Context7 Unavailable)

**Use when:** Library not found on Context7, or query returns no results.

**Speed:** Slower (2-5 min)
**Token usage:** High
**Accuracy:** Code-based

## When to Use

- Library not found by `context7-resolve-library-id`
- `context7-query-docs` returns empty/insufficient results
- Need to analyze unpublished or private package structure
- Documentation is incomplete on Context7

## Workflow

### 1. Find Repository
```
web_search: "[library] github repository site:github.com"
```
Verify: official org, active maintenance, has docs/ or README.

### 2. Fetch README and Docs
```
web_fetch: "https://raw.githubusercontent.com/{org}/{repo}/main/README.md"
web_fetch: "https://raw.githubusercontent.com/{org}/{repo}/main/docs/index.md"
```
Try both `main` and `master` branches.

### 3. Explore Documentation Structure
Use `web_fetch` on the GitHub API to list docs:
```
web_fetch: "https://api.github.com/repos/{org}/{repo}/contents/docs"
```
Then fetch key files in parallel.

### 4. Pack with Repomix (for deep analysis)
If available in the environment:
```bash
repomix --remote https://github.com/{org}/{repo} --output /tmp/repomix-output.xml
```
Then `view` the output file to extract documentation sections.

### 5. Present Findings
- Source: Repository analysis (not official docs)
- Include: Repository health (stars, last commit)
- Extract: Installation, usage, API, examples

## Fallback Chain

```
1. context7-resolve-library-id → not found
   ↓
2. web_fetch official docs/llms.txt
   e.g. https://nextjs.org/llms.txt
   ↓ not found
3. GitHub README + docs/ via web_fetch
   ↓ insufficient
4. repomix --remote (if available)
   ↓ unavailable
5. web_search + multiple web_fetch on tutorials/blog posts
```
