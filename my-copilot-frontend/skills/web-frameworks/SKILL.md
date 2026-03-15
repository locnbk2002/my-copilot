---
name: web-frameworks
description: "Build with Next.js (App Router, RSC, SSR, ISR), Turborepo monorepos, and RemixIcon. Use for React apps, server rendering, build optimization, caching strategies, shared dependencies."
argument-hint: "[framework] [feature]"
license: MIT
---

# Web Frameworks

Comprehensive guide for modern full-stack web applications using Next.js, Turborepo, and RemixIcon.

## Overview

**Next.js** — React framework with SSR, SSG, RSC, and optimization features
**Turborepo** — High-performance monorepo build system for JavaScript/TypeScript
**RemixIcon** — Icon library with 3,100+ outlined and filled style icons

## Stack Selection Guide

### Single Application: Next.js + RemixIcon

Use for standalone applications: e-commerce, marketing, SaaS, documentation, blogs.

```bash
npx create-next-app@latest my-app
cd my-app
npm install remixicon
```

### Monorepo: Next.js + Turborepo + RemixIcon

Use for multiple applications with shared code: microfrontends, multi-tenant platforms, design systems.

```bash
npx create-turbo@latest my-monorepo
```

### Framework Features Comparison

| Feature     | Next.js               | Turborepo                | RemixIcon                  |
| ----------- | --------------------- | ------------------------ | -------------------------- |
| Primary Use | Web framework         | Build system             | UI icons                   |
| Best For    | SSR/SSG apps          | Monorepos                | Consistent iconography     |
| Performance | Built-in optimization | Caching & parallel tasks | Lightweight fonts/SVG      |
| TypeScript  | Full support          | Full support             | Type definitions available |

## Quick Start

### Next.js Application

```bash
npx create-next-app@latest my-app
cd my-app
npm install remixicon
npm run dev
```

```tsx
// app/layout.tsx
import "remixicon/fonts/remixicon.css";
```

### Turborepo Monorepo

```bash
npx create-turbo@latest my-monorepo
cd my-monorepo
npm run dev   # Run all apps
npm run build # Build all packages
```

Structure:

```
apps/web/          # Customer-facing Next.js app
apps/admin/        # Admin dashboard
packages/ui/       # Shared components with RemixIcon
packages/config/   # Shared configs
turbo.json         # Pipeline configuration
```

### RemixIcon Integration

```tsx
// Webfont (HTML/CSS)
<i className="ri-home-line"></i>
<i className="ri-search-fill ri-2x"></i>

// React component
import { RiHomeLine, RiSearchFill } from "@remixicon/react"
<RiHomeLine size={24} />
<RiSearchFill size={32} color="blue" />
```

## Common Patterns

### Pattern 1: Full-Stack Monorepo Structure

```
my-monorepo/
├── apps/
│   ├── web/              # Customer-facing Next.js app
│   ├── admin/            # Admin dashboard Next.js app
│   └── docs/             # Documentation site
├── packages/
│   ├── ui/               # Shared UI with RemixIcon
│   ├── api-client/       # API client library
│   ├── config/           # ESLint, TypeScript configs
│   └── types/            # Shared TypeScript types
└── turbo.json
```

**turbo.json:**

```json
{
  "$schema": "https://turbo.build/schema.json",
  "pipeline": {
    "build": { "dependsOn": ["^build"], "outputs": [".next/**", "dist/**"] },
    "dev": { "cache": false, "persistent": true },
    "lint": {},
    "test": { "dependsOn": ["build"] }
  }
}
```

### Pattern 2: Shared Component Library

```tsx
// packages/ui/src/button.tsx
import { RiLoader4Line } from "@remixicon/react";
export function Button({ children, loading, icon }) {
  return (
    <button>
      {loading ? <RiLoader4Line className="animate-spin" /> : icon}
      {children}
    </button>
  );
}

// apps/web/app/page.tsx
import { Button } from "@repo/ui/button";
import { RiHomeLine } from "@remixicon/react";
export default function Page() {
  return <Button icon={<RiHomeLine />}>Home</Button>;
}
```

### Pattern 3: Optimized Data Fetching (Next.js)

```tsx
// app/posts/[slug]/page.tsx
export async function generateStaticParams() {
  const posts = await getPosts();
  return posts.map((post) => ({ slug: post.slug }));
}

async function getPost(slug: string) {
  const res = await fetch(`https://api.example.com/posts/${slug}`, {
    next: { revalidate: 3600 },
  });
  if (!res.ok) return null;
  return res.json();
}

export default async function Post({ params }: { params: { slug: string } }) {
  const post = await getPost(params.slug);
  if (!post) notFound();
  return <article>{post.content}</article>;
}
```

## Best Practices

**Next.js:**

- Default to Server Components; use Client Components only when needed (`use client`)
- Implement proper loading (`loading.tsx`) and error (`error.tsx`) states
- Use `next/image` for automatic optimization
- Set metadata via Metadata API for SEO
- Leverage caching: `force-cache`, `revalidate`, `no-store`

**Turborepo:**

- Structure with clear separation (`apps/`, `packages/`)
- Define task dependencies correctly (`^build` for topological)
- Configure outputs for proper caching
- Enable remote caching for team collaboration
- Use `--filter` to run tasks on changed packages only

**RemixIcon:**

- Use line style for minimal interfaces, fill for emphasis
- Maintain 24x24 grid alignment for crisp rendering
- Provide `aria-label` for icon-only buttons
- Use `currentColor` for flexible theming
- Prefer `@remixicon/react` package for React projects

## Resources

- Next.js: https://nextjs.org/docs/llms.txt
- Turborepo: https://turbo.build/repo/docs
- RemixIcon: https://remixicon.com
