# Frontend E2E Testing with Playwright

This directory contains end-to-end tests for the 10Code Intranet frontend.

## Structure

```
tests/
├── e2e/           # End-to-end tests
├── components/    # Component tests (future)
└── fixtures/      # Test fixtures and helpers
```

## Running Tests

```bash
# Run all E2E tests
pnpm test:e2e

# Run tests with UI mode (interactive)
pnpm test:e2e:ui

# Debug tests
pnpm test:e2e:debug

# View test report
pnpm test:e2e:report
```

## Configuration

- **Config file**: `playwright.config.ts`
- **Base URL**: `http://localhost:8000` (Django backend)
- **Browsers**: Chromium, Firefox, Mobile Chrome (Pixel 5)

## Environment Variables

- `PLAYWRIGHT_TEST_BASE_URL`: Override the base URL for tests (default: `http://localhost:8000`)
- `CI`: Set to enable CI-specific configuration (retries, workers, reporters)

## Test Files

### `e2e/auth.spec.ts`
Comprehensive authentication and dashboard tests covering:
-Authentication flow with Google OAuth
- Dashboard layout and navigation
- Visual design system
- Accessibility (WCAG 2.1 AA)
- Cross-browser compatibility
- Performance metrics

### `e2e/setup-verification.spec.ts`
Simple smoke test to verify Playwright configuration.

## Writing Tests

Tests should be placed in the appropriate subdirectory:
- `e2e/` - Full user flows and integration tests
- `components/` - Component-level tests (future)
- `fixtures/` - Shared test data and helpers

Follow Playwright best practices:
- Use semantic selectors (`getByRole`, `getByText`, etc.)
- Test user flows, not implementation details
- Keep tests independent and idempotent
- Use proper waiting strategies (avoid arbitrary timeouts)

## CI/CD Integration

The configuration is optimized for CI environments:
- Automatic retries on failure (2 retries in CI)
- Sequential execution in CI (parallel locally)
- GitHub Actions reporter in CI
- Screenshots on failure
- Traces on first retry
