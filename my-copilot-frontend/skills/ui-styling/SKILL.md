---
name: ui-styling
description: "Style UIs with shadcn/ui components (Radix UI + Tailwind CSS). Use for accessible components, themes, dark mode, responsive layouts, design systems, color customization."
argument-hint: "[component or layout]"
license: MIT
---

# UI Styling Skill

Build beautiful, accessible UIs combining shadcn/ui components and Tailwind CSS utility styling.

## References

- shadcn/ui: https://ui.shadcn.com/llms.txt
- Tailwind CSS: https://tailwindcss.com/docs
- Radix UI: https://radix-ui.com

## When to Use

- Building UI with React-based frameworks (Next.js, Vite, Remix, Astro)
- Implementing accessible components (dialogs, forms, tables, navigation)
- Styling with utility-first CSS approach
- Creating responsive, mobile-first layouts
- Implementing dark mode and theme customization
- Building design systems with consistent tokens
- Rapid prototyping with immediate visual feedback
- Adding complex UI patterns (data tables, charts, command palettes)

## Core Stack

### Component Layer: shadcn/ui

- Pre-built accessible components via Radix UI primitives
- Copy-paste distribution model (components live in your codebase)
- TypeScript-first with full type safety
- Composable primitives for complex UIs
- CLI-based installation and management

### Styling Layer: Tailwind CSS

- Utility-first CSS framework
- Build-time processing with zero runtime overhead
- Mobile-first responsive design
- Consistent design tokens (colors, spacing, typography)
- Automatic dead code elimination

## Quick Start

### shadcn/ui + Tailwind Setup

```bash
npx shadcn@latest init
```

CLI prompts for framework, TypeScript, paths, and theme. Configures both shadcn/ui and Tailwind CSS.

```bash
# Add components
npx shadcn@latest add button card dialog form table
```

```tsx
import { Button } from "@/components/ui/button";
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card";

export function Dashboard() {
  return (
    <div className="container mx-auto p-6 grid gap-6 md:grid-cols-2 lg:grid-cols-3">
      <Card className="hover:shadow-lg transition-shadow">
        <CardHeader>
          <CardTitle className="text-2xl font-bold">Analytics</CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          <p className="text-muted-foreground">View your metrics</p>
          <Button variant="default" className="w-full">
            View Details
          </Button>
        </CardContent>
      </Card>
    </div>
  );
}
```

### Tailwind-Only Setup (Vite)

```bash
npm install -D tailwindcss @tailwindcss/vite
```

```javascript
// vite.config.ts
import tailwindcss from "@tailwindcss/vite";
export default { plugins: [tailwindcss()] };
```

```css
/* src/index.css */
@import "tailwindcss";
```

## Component Library Guide

**Key categories:**

- Form & input: Button, Input, Select, Checkbox, Date Picker, Form validation
- Layout & navigation: Card, Tabs, Accordion, Navigation Menu
- Overlays & dialogs: Dialog, Drawer, Popover, Toast, Command
- Feedback & status: Alert, Progress, Skeleton
- Display: Table, Data Table, Avatar, Badge

Full docs: https://ui.shadcn.com/docs/components

## Theme & Customization

**Dark mode with next-themes:**

```bash
npm install next-themes
```

```tsx
// app/layout.tsx
import { ThemeProvider } from "next-themes";
export default function Layout({ children }) {
  return <ThemeProvider attribute="class">{children}</ThemeProvider>;
}
```

**CSS variables** (in `globals.css`):

```css
@layer base {
  :root {
    --background: 0 0% 100%;
    --foreground: 222.2 84% 4.9%;
    --primary: 221.2 83.2% 53.3%;
  }
  .dark {
    --background: 222.2 84% 4.9%;
    --foreground: 210 40% 98%;
  }
}
```

## Common Patterns

**Form with validation (react-hook-form + zod):**

```tsx
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import * as z from "zod";
import {
  Form,
  FormField,
  FormItem,
  FormLabel,
  FormControl,
  FormMessage,
} from "@/components/ui/form";

const schema = z.object({
  email: z.string().email(),
  password: z.string().min(8),
});

export function LoginForm() {
  const form = useForm({ resolver: zodResolver(schema) });
  return (
    <Form {...form}>
      <form onSubmit={form.handleSubmit(console.log)} className="space-y-6">
        <FormField
          control={form.control}
          name="email"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Email</FormLabel>
              <FormControl>
                <input type="email" {...field} />
              </FormControl>
              <FormMessage />
            </FormItem>
          )}
        />
        <Button type="submit" className="w-full">
          Sign In
        </Button>
      </form>
    </Form>
  );
}
```

**Responsive layout with dark mode:**

```tsx
<div className="min-h-screen bg-white dark:bg-gray-900">
  <div className="container mx-auto px-4 py-8">
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      <Card className="bg-white dark:bg-gray-800 border-gray-200 dark:border-gray-700">
        <CardContent className="p-6">
          <h3 className="text-xl font-semibold text-gray-900 dark:text-white">
            Content
          </h3>
        </CardContent>
      </Card>
    </div>
  </div>
</div>
```

## Best Practices

1. **Component Composition**: Build complex UIs from simple, composable primitives
2. **Utility-First**: Use Tailwind classes directly; extract components only for true repetition
3. **Mobile-First**: Start with mobile styles, layer responsive variants (`sm:`, `md:`, `lg:`)
4. **Accessibility-First**: Leverage Radix UI primitives, add focus states, use semantic HTML
5. **Design Tokens**: Use consistent spacing scale, color palettes, typography system
6. **Dark Mode**: Apply `dark:` variants to all themed elements
7. **Performance**: Leverage automatic CSS purging; avoid dynamic class names in strings
8. **TypeScript**: Use full type safety for better DX
