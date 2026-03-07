## Framework Detection

### Detection Order

1. **Check project root files:**
   - `package.json` → read `scripts.test`, check `devDependencies` for jest/vitest/mocha/playwright/cypress
   - `pyproject.toml` → check `[tool.pytest]` section
   - `setup.py` / `setup.cfg` → unittest/pytest
   - `go.mod` → Go testing
   - `Cargo.toml` → Rust testing
   - `pom.xml` / `build.gradle` → JUnit/TestNG
   - `Gemfile` → RSpec/Minitest

2. **Check for test directories:**
   - `__tests__/`, `test/`, `tests/`, `spec/`
   - `*_test.go`, `*_test.py`, `*.test.ts`, `*.spec.ts`

3. **Check for config files:**
   - `jest.config.*`, `vitest.config.*`, `pytest.ini`, `.mocharc.*`
   - `playwright.config.*`, `cypress.config.*`

### Framework Commands

| Framework  | Run All            | Run Specific              | Coverage                    |
| ---------- | ------------------ | ------------------------- | --------------------------- |
| jest       | `npx jest`         | `npx jest <path>`         | `npx jest --coverage`       |
| vitest     | `npx vitest run`   | `npx vitest run <path>`   | `npx vitest run --coverage` |
| pytest     | `python -m pytest` | `python -m pytest <path>` | `python -m pytest --cov`    |
| go test    | `go test ./...`    | `go test <pkg>`           | `go test -cover ./...`      |
| cargo test | `cargo test`       | `cargo test <name>`       | `cargo tarpaulin`           |

### Fallback

If no framework detected, check for npm scripts: `npm run test` (most common).
If nothing found, inform user and ask for test command.
