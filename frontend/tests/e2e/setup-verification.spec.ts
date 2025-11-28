import { test, expect } from '@playwright/test';

/**
 * Simple smoke test to verify Playwright setup
 * This test ensures the configuration is working correctly
 */
test.describe('Playwright Setup Verification', () => {
    test('playwright is configured correctly', async ({ page }) => {
        // This is a simple smoke test to verify the setup
        // It tests that we can navigate to the base URL
        await page.goto('/');

        // Verify page loaded
        await expect(page).not.toHaveTitle('');

        console.log('✓ Playwright setup verified successfully!');
    });
});
