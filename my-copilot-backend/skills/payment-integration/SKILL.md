---
name: payment-integration
description: "Integrate payments with payOS (VietQR, Vietnamese banks), Polar, Stripe, Paddle (MoR subscriptions), Creem.io (licensing). Checkout, webhooks, subscriptions, QR codes, multi-provider orders."
argument-hint: "[provider] [task]"
license: MIT
---

# Payment Integration

Production-proven payment processing with payOS (Vietnamese banks, VietQR), Polar (global SaaS), Stripe (global infrastructure), Paddle (MoR subscriptions), and Creem.io (MoR + licensing).

## When to Use

- Payment gateway integration (checkout, processing)
- Subscription management (trials, upgrades, billing)
- Webhook handling (notifications, idempotency)
- QR code payments (VietQR, NAPAS)
- Software licensing (device activation)
- Multi-provider order management
- Revenue splits and commissions

## Platform Selection

| Platform     | Best For                                                        |
| ------------ | --------------------------------------------------------------- |
| **payOS**    | Vietnamese market, VND, bank transfers, VietQR, QR payments     |
| **Polar**    | Global SaaS, subscriptions, automated benefits (GitHub/Discord) |
| **Stripe**   | Enterprise payments, Connect platforms, custom checkout         |
| **Paddle**   | MoR subscriptions, global tax compliance, churn prevention      |
| **Creem.io** | MoR + licensing, revenue splits, no-code checkout               |

## Quick Reference

### payOS

- Overview — Auth (clientId, apiKey, checksumKey), supported banks (ACB, BIDV, MB, OCB, VPBank, KienlongBank), Bảo Kim e-wallet
- API — Payment link creation, transaction query
- Checkout — Hosted page (redirect) or embedded form
- Webhooks — HMAC-SHA256 signature verification, `payOS.webhooks.verify()`
- SDK — Node.js (`@payos/node`), Python, PHP, Java, Go, .NET Core
- QR Codes — VietQR generation via payment links
- Best Practices — Production patterns
- External: https://payos.vn/docs/llms.txt

### Polar

- Overview — Auth, MoR concept
- Products — Pricing models
- Checkouts — Checkout flows
- Subscriptions — Lifecycle management
- Webhooks — Event handling
- Benefits — Automated delivery
- SDK — Multi-language SDKs
- Best Practices — Production patterns

### Stripe

- Best Practices — Integration design
- SDKs — Server SDKs
- Stripe.js — Payment Element
- CLI — Local testing
- External: https://docs.stripe.com/llms.txt

### Paddle

- Overview — MoR, auth, entity IDs
- API — Products, prices, transactions
- Paddle.js — Checkout overlay/inline
- Subscriptions — Trials, upgrades, pause
- Webhooks — SHA256 verification
- SDK — Node, Python, PHP, Go
- Best Practices — Production patterns
- External: https://developer.paddle.com/llms.txt

### Creem.io

- Overview — MoR, auth, global support
- API — Products, checkout sessions
- Checkouts — No-code links, storefronts
- Subscriptions — Trials, seat-based
- Licensing — Device activation
- Webhooks — Signature verification
- SDK — Next.js, Better Auth
- External: https://docs.creem.io/llms.txt

### Multi-Provider

- Multi-provider order management patterns — Unified orders, currency conversion

## Key Capabilities

| Platform     | Highlights                                                                                                             |
| ------------ | ---------------------------------------------------------------------------------------------------------------------- |
| **payOS**    | VietQR/bank transfers, ACB/BIDV/MB/OCB/VPBank/KienlongBank + Bảo Kim, HMAC-SHA256 webhooks, hosted + embedded checkout |
| **Polar**    | MoR, subscriptions, usage billing, benefits, 300 req/min                                                               |
| **Stripe**   | CheckoutSessions, Billing, Connect, Payment Element                                                                    |
| **Paddle**   | MoR, overlay/inline checkout, Retain (churn prevention), tax                                                           |
| **Creem.io** | MoR, licensing, revenue splits, no-code checkout                                                                       |

## Implementation

See provider documentation for step-by-step guides per platform.

**General flow:** auth → products → checkout → webhooks → events

## Security

Always verify webhook signatures with HMAC before processing events. Never process webhook events without signature verification. Reference provider-specific verification docs for each platform.

- **Stripe**: Use `stripe.webhooks.constructEvent(payload, sig, secret)` — throws if invalid
- **Paddle**: Verify SHA256 HMAC signature from `Paddle-Signature` header
- **Polar**: Verify webhook secret from `webhook-id` + `webhook-timestamp` + `webhook-signature` headers
- **payOS**: Verify HMAC-SHA256 signature — sort payload keys alphabetically, concat as `key=value&...`, hash with `checksumKey`, compare with `signature` field; use `payOS.webhooks.verify(webhookData)`
- **Creem.io**: Verify HMAC SHA256 signature per Creem webhook docs

Implement idempotency keys for all payment operations to prevent duplicate processing on retries.
