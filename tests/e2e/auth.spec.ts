import { test, expect } from '@playwright/test';

test('login page has google login button', async ({ page }) => {
    await page.goto('/login/');
    await expect(page).toHaveTitle(/Iniciar Sesión/);
    const loginButton = page.getByRole('link', { name: 'Login con Google' });
    await expect(loginButton).toBeVisible();
    await expect(loginButton).toHaveAttribute('href', '/accounts/google/login/');
});

test('redirects to dashboard if already logged in', async ({ page }) => {
    // This test would require a way to seed the session or mock the auth state.
    // For now, we just verify the login page behavior.
});
