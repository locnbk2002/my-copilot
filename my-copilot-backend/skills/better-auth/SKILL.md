---
name: better-auth
description: "Add authentication with Better Auth (TypeScript). Use for email/password, OAuth providers (Google, GitHub), 2FA/MFA, passkeys/WebAuthn, sessions, RBAC, rate limiting."
argument-hint: "[auth-method or feature]"
license: MIT
---

# Better Auth Skill

Better Auth is a comprehensive, framework-agnostic authentication/authorization framework for TypeScript with built-in email/password, social OAuth, and a powerful plugin ecosystem for advanced features.

**Security:** Never store plaintext passwords; use bcrypt/argon2 (Better Auth handles this automatically via its built-in password hashing).

## When to Use

- Implementing auth in TypeScript/JavaScript applications
- Adding email/password or social OAuth authentication
- Setting up 2FA, passkeys, magic links, advanced auth features
- Building multi-tenant apps with organization support
- Managing sessions and user lifecycle
- Working with any framework (Next.js, Nuxt, SvelteKit, Remix, Astro, Hono, Express, etc.)

## Quick Start

### Installation

```bash
npm install better-auth
# or pnpm/yarn/bun add better-auth
```

### Environment Setup

Create `.env`:

```env
BETTER_AUTH_SECRET=<generated-secret-32-chars-min>
BETTER_AUTH_URL=http://localhost:3000
```

### Basic Server Setup

Create `auth.ts` (root, lib/, utils/, or under src/app/server/):

```ts
import { betterAuth } from "better-auth";

export const auth = betterAuth({
  database: {
    // configure your DB adapter here
  },
  emailAndPassword: {
    enabled: true,
    autoSignIn: true,
  },
  socialProviders: {
    github: {
      clientId: process.env.GITHUB_CLIENT_ID!,
      clientSecret: process.env.GITHUB_CLIENT_SECRET!,
    },
  },
});
```

### Database Schema

```bash
npx @better-auth/cli generate  # Generate schema/migrations
npx @better-auth/cli migrate   # Apply migrations (Kysely only)
```

### Mount API Handler

**Next.js App Router:**

```ts
// app/api/auth/[...all]/route.ts
import { auth } from "@/lib/auth";
import { toNextJsHandler } from "better-auth/next-js";

export const { POST, GET } = toNextJsHandler(auth);
```

**Other frameworks:** Use `auth.handler(request)` or framework-specific adapter from Better Auth docs.

### Client Setup

Create `auth-client.ts`:

```ts
import { createAuthClient } from "better-auth/client";

export const authClient = createAuthClient({
  baseURL: process.env.NEXT_PUBLIC_BETTER_AUTH_URL || "http://localhost:3000",
});
```

### Basic Usage

```ts
// Sign up
await authClient.signUp.email({
  email: "user@example.com",
  password: "secure123",
  name: "John Doe",
});

// Sign in
await authClient.signIn.email({
  email: "user@example.com",
  password: "secure123",
});

// OAuth
await authClient.signIn.social({ provider: "github" });

// Session
const { data: session } = authClient.useSession(); // React/Vue/Svelte
const { data: session } = await authClient.getSession(); // Vanilla JS
```

## Feature Selection Matrix

| Feature                      | Plugin Required      | Use Case               |
| ---------------------------- | -------------------- | ---------------------- |
| Email/Password               | No (built-in)        | Basic auth             |
| OAuth (GitHub, Google, etc.) | No (built-in)        | Social login           |
| Email Verification           | No (built-in)        | Verify email addresses |
| Password Reset               | No (built-in)        | Forgot password flow   |
| Two-Factor Auth (2FA/TOTP)   | Yes (`twoFactor`)    | Enhanced security      |
| Passkeys/WebAuthn            | Yes (`passkey`)      | Passwordless auth      |
| Magic Link                   | Yes (`magicLink`)    | Email-based login      |
| Username Auth                | Yes (`username`)     | Username login         |
| Organizations/Multi-tenant   | Yes (`organization`) | Team/org features      |
| Rate Limiting                | No (built-in)        | Prevent abuse          |
| Session Management           | No (built-in)        | User sessions          |

## Auth Method Selection Guide

**Choose Email/Password when:**

- Building standard web app with traditional auth
- Need full control over user credentials
- Targeting users who prefer email-based accounts

**Choose OAuth when:**

- Want quick signup with minimal friction
- Users already have social accounts
- Need access to social profile data

**Choose Passkeys when:**

- Want passwordless experience
- Targeting modern browsers/devices
- Security is top priority

**Choose Magic Link when:**

- Want passwordless without WebAuthn complexity
- Targeting email-first users
- Need temporary access links

**Combine Multiple Methods when:**

- Want flexibility for different user preferences
- Building enterprise apps with various auth requirements
- Need progressive enhancement (start simple, add more options)

## Core Architecture

Better Auth uses client-server architecture:

1. **Server** (`better-auth`): Handles auth logic, database ops, API routes
2. **Client** (`better-auth/client`): Provides hooks/methods for frontend
3. **Plugins**: Extend both server/client functionality

## Implementation Checklist

- [ ] Install `better-auth` package
- [ ] Set environment variables (SECRET, URL)
- [ ] Create auth server instance with database config
- [ ] Run schema migration (`npx @better-auth/cli generate`)
- [ ] Mount API handler in framework
- [ ] Create client instance
- [ ] Implement sign-up/sign-in UI
- [ ] Add session management to components
- [ ] Set up protected routes/middleware
- [ ] Add plugins as needed (regenerate schema after)
- [ ] Test complete auth flow
- [ ] Configure email sending (verification/reset)
- [ ] Enable rate limiting for production
- [ ] Set up error handling

## Reference Documentation

- Email/Password Authentication — Email/password setup, verification, password reset, username auth
- OAuth Providers — Social login setup, provider configuration, token management
- Database Integration — Database adapters, schema setup, migrations
- Advanced Features — 2FA/MFA, passkeys, magic links, organizations, rate limiting, session management

## Resources

- Docs: https://www.better-auth.com/docs
- GitHub: https://github.com/better-auth/better-auth
- Plugins: https://www.better-auth.com/docs/plugins
- Examples: https://www.better-auth.com/docs/examples
