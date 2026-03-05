## Pre-Commit Security Scan

### What to Check

Scan `git diff --staged` for:

1. **API Keys & Tokens:**
   - Patterns: `API_KEY`, `SECRET`, `TOKEN`, `PASSWORD`, `PRIVATE_KEY`
   - Base64-encoded secrets (long alphanumeric strings)
   - AWS: `AKIA[A-Z0-9]{16}`
   - GitHub: `ghp_[A-Za-z0-9]{36}`, `ghs_[A-Za-z0-9]{36}`

2. **Environment Files:**
   - `.env`, `.env.local`, `.env.production`
   - Files containing `DB_PASSWORD`, `DATABASE_URL` with credentials

3. **Private Keys:**
   - `-----BEGIN RSA PRIVATE KEY-----`
   - `-----BEGIN OPENSSH PRIVATE KEY-----`
   - `-----BEGIN EC PRIVATE KEY-----`

4. **Hardcoded Credentials:**
   - `password = "..."` or `pwd = "..."`
   - Connection strings with embedded passwords
   - `Basic [base64]` auth headers

### Scan Implementation

```bash
# Check staged diff for secrets
git diff --staged | grep -iE "(API_KEY|SECRET|TOKEN|PASSWORD|PRIVATE_KEY|AKIA[A-Z0-9]{16}|ghp_|ghs_|BEGIN.*PRIVATE KEY)" || true
```

### Response Protocol

- **If secrets found**: STOP, show the match, ask user to confirm via `ask_user`
- **If .env staged**: WARN, suggest adding to .gitignore
- **If clean**: proceed with commit silently (no "security scan passed" output)
