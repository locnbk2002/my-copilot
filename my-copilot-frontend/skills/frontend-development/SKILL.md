---
name: frontend-development
description: "Build React/TypeScript frontends with modern patterns. Use for components, Suspense, lazy loading, useSuspenseQuery, TanStack Router, performance optimization."
argument-hint: "[component or feature]"
license: MIT
---

# Frontend Development Guidelines

Comprehensive guide for modern React development: Suspense-based data fetching, lazy loading, file organization, and performance optimization.

## When to Use

- Creating new components or pages
- Building new features
- Fetching data with TanStack Query
- Setting up routing with TanStack Router
- Performance optimization
- TypeScript best practices

---

## New Component Checklist

- [ ] `React.FC<Props>` pattern with TypeScript
- [ ] Lazy load if heavy component: `React.lazy(() => import(...))`
- [ ] Wrap in `<Suspense fallback={...}>` for loading states
- [ ] Use `useSuspenseQuery` for data fetching
- [ ] `useCallback` for event handlers passed to children
- [ ] `useMemo` for expensive computations
- [ ] Default export at bottom
- [ ] No early returns with loading spinners
- [ ] No `any` types — strict TypeScript

## New Feature Checklist

- [ ] Create `features/{feature-name}/` directory
- [ ] Create subdirectories: `api/`, `components/`, `hooks/`, `helpers/`, `types/`
- [ ] Create API service file: `api/{feature}Api.ts`
- [ ] Set up TypeScript types in `types/`
- [ ] Create route file and lazy load feature components
- [ ] Use Suspense boundaries
- [ ] Export public API from feature `index.ts`

---

## File Structure

```
src/
  features/
    my-feature/
      api/
        myFeatureApi.ts       # API service
      components/
        MyFeature.tsx         # Main component
        SubComponent.tsx      # Related components
      hooks/
        useMyFeature.ts       # Custom hooks
      helpers/
        myFeatureHelpers.ts   # Utilities
      types/
        index.ts              # TypeScript types
      index.ts                # Public exports
  components/
    SuspenseLoader/           # Reusable loader
  routes/
    my-route/
      index.tsx               # Route component
```

---

## Core Patterns

### Loading States — No Early Returns

```typescript
// NEVER — causes layout shift
if (isLoading) return <LoadingSpinner />;

// ALWAYS — consistent layout
<Suspense fallback={<Skeleton />}>
  <Content />
</Suspense>
```

### Data Fetching with useSuspenseQuery

```typescript
const { data } = useSuspenseQuery({
  queryKey: ["feature", id],
  queryFn: () => featureApi.getFeature(id),
});
// No isLoading check needed — Suspense handles it
```

### Routing with TanStack Router

```typescript
import { createFileRoute } from "@tanstack/react-router";
import { lazy } from "react";

const MyPage = lazy(() => import("@/features/my-feature/components/MyPage"));

export const Route = createFileRoute("/my-route/")({
  component: MyPage,
  loader: () => ({ crumb: "My Route" }),
});
```

### Component Template

```typescript
import React, { useState, useCallback, useMemo } from 'react';
import { useSuspenseQuery } from '@tanstack/react-query';
import { featureApi } from '../api/featureApi';
import type { FeatureData } from '../types';

interface MyComponentProps {
  id: number;
  onAction?: () => void;
}

export const MyComponent: React.FC<MyComponentProps> = ({ id, onAction }) => {
  const [state, setState] = useState<string>('');

  const { data } = useSuspenseQuery({
    queryKey: ['feature', id],
    queryFn: () => featureApi.getFeature(id),
  });

  const handleAction = useCallback(() => {
    setState('updated');
    onAction?.();
  }, [onAction]);

  const processed = useMemo(() => data.items.filter(Boolean), [data.items]);

  return <div>{/* render */}</div>;
};

export default MyComponent;
```

---

## Performance Patterns

| Pattern              | When to Use                                     |
| -------------------- | ----------------------------------------------- |
| `React.lazy()`       | Routes, DataGrid, charts, editors               |
| `useMemo`            | Expensive filter/sort/map operations            |
| `useCallback`        | Event handlers passed as props                  |
| `React.memo`         | Components that re-render often with same props |
| Debounce (300-500ms) | Search inputs                                   |

---

## TypeScript Standards

- Strict mode, no `any` type
- Explicit return types on functions
- Use `import type` for type-only imports
- Component prop interfaces with JSDoc comments
- Generic types for reusable components

---

## Core Principles

1. **Lazy Load Everything Heavy**: Routes, DataGrid, charts, editors
2. **Suspense for Loading**: Use boundaries, not early returns
3. **useSuspenseQuery**: Primary data fetching pattern
4. **Features are Organized**: api/, components/, hooks/, helpers/ subdirs
5. **No Early Returns**: Prevents layout shift
6. **TypeScript Strict**: No `any`, explicit types everywhere
