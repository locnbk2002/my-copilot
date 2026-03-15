---
name: backend-development
description: "Build backends with Node.js, Python, Go (NestJS, FastAPI, Django). Use for REST/GraphQL/gRPC APIs, auth (OAuth, JWT), databases, microservices, security (OWASP), Docker/K8s."
argument-hint: "[framework] [task]"
license: MIT
---

# Backend Development Skill

Production-ready backend development with modern technologies, best practices, and proven patterns.

## When to Use

- Designing RESTful, GraphQL, or gRPC APIs
- Building authentication/authorization systems
- Optimizing database queries and schemas
- Implementing caching and performance optimization
- OWASP Top 10 security mitigation
- Designing scalable microservices
- Testing strategies (unit, integration, E2E)
- CI/CD pipelines and deployment
- Monitoring and debugging production systems

## Technology Selection Guide

**Languages:** Node.js/TypeScript (full-stack), Python (data/ML), Go (concurrency), Rust (performance)
**Frameworks:** NestJS, FastAPI, Django, Express, Hono, Gin
**Databases:** PostgreSQL (ACID), MongoDB (flexible schema), Redis (caching)
**APIs:** REST (simple), GraphQL (flexible), gRPC (performance)

## Reference Navigation

**Core Technologies:**

- Backend technologies — Languages, frameworks, databases, message queues, ORMs
- API design — REST, GraphQL, gRPC patterns and best practices

**Security & Authentication:**

- OWASP Top 10 2025 security best practices, input validation: https://owasp.org/www-project-top-ten/
- Authentication — OAuth 2.1, JWT, RBAC, MFA, session management

**Performance & Architecture:**

- Performance — Caching, query optimization, load balancing, scaling
- Architecture — Microservices, event-driven, CQRS, saga patterns

**Quality & Operations:**

- Testing — Testing strategies, frameworks, tools, CI/CD testing
- Code quality — SOLID principles, design patterns, clean code
- DevOps — Docker, Kubernetes, deployment strategies, monitoring
- Debugging — Debugging strategies, profiling, logging, production debugging

## Key Best Practices (2025)

**Security:** Argon2id passwords, parameterized queries (98% SQL injection reduction), OAuth 2.1 + PKCE, rate limiting, security headers

**Performance:** Redis caching (90% DB load reduction), database indexing (30% I/O reduction), CDN (50%+ latency cut), connection pooling

**Testing:** 70-20-10 pyramid (unit-integration-E2E), Vitest 50% faster than Jest, contract testing for microservices, 83% migrations fail without tests

**DevOps:** Blue-green/canary deployments, feature flags (90% fewer failures), Kubernetes 84% adoption, Prometheus/Grafana monitoring, OpenTelemetry tracing

## Quick Decision Matrix

| Need                | Choose           |
| ------------------- | ---------------- |
| Fast development    | Node.js + NestJS |
| Data/ML integration | Python + FastAPI |
| High concurrency    | Go + Gin         |
| Max performance     | Rust + Axum      |
| ACID transactions   | PostgreSQL       |
| Flexible schema     | MongoDB          |
| Caching             | Redis            |
| Internal services   | gRPC             |
| Public APIs         | GraphQL/REST     |
| Real-time events    | Kafka            |

## Implementation Checklist

**API:** Choose style → Design schema → Validate input → Add auth → Rate limiting → Documentation → Error handling

**Database:** Choose DB → Design schema → Create indexes → Connection pooling → Migration strategy → Backup/restore → Test performance

**Security:** OWASP Top 10 → Parameterized queries → OAuth 2.1 + JWT → Security headers → Rate limiting → Input validation → Argon2id passwords

**Testing:** Unit 70% → Integration 20% → E2E 10% → Load tests → Migration tests → Contract tests (microservices)

**Deployment:** Docker → CI/CD → Blue-green/canary → Feature flags → Monitoring → Logging → Health checks

## Resources

- OWASP Top 10: https://owasp.org/www-project-top-ten/
- OAuth 2.1: https://oauth.net/2.1/
- OpenTelemetry: https://opentelemetry.io/
