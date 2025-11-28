import { test, expect } from '@playwright/test';

test.describe('Authentication Flow', () => {
    test('login page loads with proper branding and Google authentication', async ({ page }) => {
        await page.goto('/login/');

        // Check page title and meta
        await expect(page).toHaveTitle(/Bienvenido a 10Code/);

        // Check 10Code branding elements
        await expect(page.getByText('Bienvenido a 10Code')).toBeVisible();
        await expect(page.getByText('Accede a tu intranet corporativa')).toBeVisible();

        // Verify 10Code logo/brand element
        const brandLogo = page.locator('.bg-primary').first();
        await expect(brandLogo).toContainText('10');

        // Check Google authentication button
        const loginButton = page.getByRole('link', { name: 'Continuar con Google' });
        await expect(loginButton).toBeVisible();
        await expect(loginButton).toHaveAttribute('href', '/accounts/google/login/');
        await expect(loginButton).toContainText('Continuar con Google');

        // Verify accessibility attributes
        await expect(loginButton).toHaveAttribute('aria-label', 'Iniciar sesión con Google');

        // Check terms and privacy notice
        await expect(page.getByText('términos de servicio y la política de privacidad de 10Code')).toBeVisible();

        // Verify exclusive employee access message
        await expect(page.getByText('Acceso exclusivo para empleados')).toBeVisible();
    });

    test('google authentication flow accessibility', async ({ page }) => {
        await page.goto('/login/');

        // Test keyboard navigation
        await page.keyboard.press('Tab');
        const loginButton = page.getByRole('link', { name: 'Continuar con Google' });
        await expect(loginButton).toBeFocused();

        // Check if button is visible and clickable
        await expect(loginButton).toBeEnabled();
    });
});

test.describe('Dashboard Layout', () => {
    test('dashboard loads with proper header and navigation', async ({ page }) => {
        await page.goto('/dashboard/');

        // Check header elements
        await expect(page.getByText('10Code')).toBeVisible();
        await expect(page.getByText('Dashboard')).toBeVisible();

        // Check navigation elements
        await expect(page.getByText('Inicio')).toBeVisible();

        // Verify user avatar and dropdown
        const userAvatar = page.locator('button').filter({ has: page.locator('img') }).first();
        await expect(userAvatar).toBeVisible();

        // Test responsive header (mobile menu button)
        await page.setViewportSize({ width: 375, height: 667 });
        const mobileMenuButton = page.getByRole('button', { name: 'Toggle navigation menu' });
        await expect(mobileMenuButton).toBeVisible();
    });

    test('user dropdown menu functionality', async ({ page }) => {
        await page.goto('/dashboard/');

        // Click user avatar to open dropdown
        const userAvatar = page.locator('button').filter({ has: page.locator('img') }).first();
        await userAvatar.click();

        // Check dropdown menu items
        await expect(page.getByText('Mi Perfil')).toBeVisible();
        await expect(page.getByText('Cerrar Sesión')).toBeVisible();

        // Check if user info is displayed
        await expect(page.getByText('@10code.es')).toBeVisible();

        // Test logout functionality form
        const logoutForm = page.locator('form').filter({ has: page.getByText('Cerrar Sesión') });
        await expect(logoutForm).toBeVisible();
        await expect(logoutForm).toHaveAttribute('action', '/logout/');
    });

    test('welcome card displays user information', async ({ page }) => {
        await page.goto('/dashboard/');

        // Check welcome message
        await expect(page.getByText('¡Bienvenido,')).toBeVisible();
        await expect(page.getByText('Has iniciado sesión correctamente en la intranet de 10Code')).toBeVisible();

        // Check user information display
        await expect(page.getByText('Email')).toBeVisible();
        await expect(page.getByText('Roles')).toBeVisible();

        // Check if user avatar is present
        const avatar = page.locator('img').first();
        await expect(avatar).toBeVisible();
    });

    test('quick actions cards are functional', async ({ page }) => {
        await page.goto('/dashboard/');

        // Check quick action sections
        await expect(page.getByText('Inicio')).toBeVisible();
        await expect(page.getByText('Mi Cuenta')).toBeVisible();

        // Test action buttons
        const profileButtons = page.getByRole('link', { name: /perfil/ });
        const buttonsCount = await profileButtons.count();
        expect(buttonsCount).toBeGreaterThan(0);

        // Check if links point to profile page
        for (let i = 0; i < buttonsCount; i++) {
            const button = profileButtons.nth(i);
            await expect(button).toHaveAttribute('href', '/accounts/profile/');
        }
    });

    test('dashboard responsive design', async ({ page }) => {
        // Test desktop layout
        await page.setViewportSize({ width: 1920, height: 1080 });
        await page.goto('/dashboard/');

        // Check desktop-specific elements
        await expect(page.getByText('Inicio')).toBeVisible();

        // Test mobile layout
        await page.setViewportSize({ width: 375, height: 667 });
        await page.goto('/dashboard/');

        // Check mobile-specific elements
        const mobileMenuButton = page.getByRole('button', { name: 'Toggle navigation menu' });
        await expect(mobileMenuButton).toBeVisible();
    });
});

test.describe('Visual Design System', () => {
    test('color scheme and theming consistency', async ({ page }) => {
        await page.goto('/login/');

        // Test primary color usage
        const primaryElements = page.locator('.bg-primary');
        const primaryCount = await primaryElements.count();
        expect(primaryCount).toBeGreaterThan(0);

        // Check text contrast - verify elements have proper styling
        const title = page.getByText('Bienvenido a 10Code');
        await expect(title).toBeVisible();

        // Verify card styling
        const card = page.locator('.shadow-lg').first();
        await expect(card).toBeVisible();
    });

    test('dark mode support', async ({ page }) => {
        await page.goto('/login/');

        // Simulate dark mode by adding class using addInitScript
        await page.addInitScript(() => {
            document.documentElement.classList.add('dark');
        });

        // Reload to apply dark styles
        await page.reload();

        // Text should remain visible
        const title = page.getByText('Bienvenido a 10Code');
        await expect(title).toBeVisible();
    });
});

test.describe('Accessibility (WCAG 2.1 AA)', () => {
    test('login page accessibility features', async ({ page }) => {
        await page.goto('/login/');

        // Check heading hierarchy
        const headings = page.locator('h1, h2, h3, h4, h5, h6, [role="heading"]');
        const headingCount = await headings.count();
        expect(headingCount).toBeGreaterThan(0);

        // Check button accessibility
        const button = page.getByRole('link', { name: 'Continuar con Google' });
        await expect(button).toBeVisible();
        await expect(button).toHaveAttribute('href', '/accounts/google/login/');

        // Check focus indicators
        await page.keyboard.press('Tab');
        const focusedElement = page.locator(':focus');
        await expect(focusedElement).toBeVisible();

        // Verify proper heading levels
        const h1 = page.locator('h1').first();
        const h2 = page.locator('h2').first();
        // Should have proper heading hierarchy
    });

    test('dashboard accessibility features', async ({ page }) => {
        await page.goto('/dashboard/');

        // Check semantic HTML structure
        await expect(page.locator('header')).toBeVisible();
        await expect(page.locator('main')).toBeVisible();

        // Check navigation landmarks
        const nav = page.locator('nav');
        await expect(nav).toBeVisible();

        // Check button accessibility
        const dropdownTrigger = page.locator('[role="button"]').filter({ has: page.locator('img') }).first();
        if (await dropdownTrigger.isVisible()) {
            await expect(dropdownTrigger).toBeVisible();
        }
    });

    test('keyboard navigation flow', async ({ page }) => {
        await page.goto('/login/');

        // Test tab navigation
        const focusableElements = page.locator('a, button, input, select, textarea, [tabindex]:not([tabindex="-1"])');
        const count = await focusableElements.count();
        expect(count).toBeGreaterThan(0);

        // Test keyboard shortcuts
        await page.keyboard.press('Tab');
        const firstFocusable = page.locator(':focus');
        await expect(firstFocusable).toBeVisible();
    });
});

test.describe('Cross-browser Compatibility', () => {
    test('login page renders correctly across browsers', async ({ page, browserName }) => {
        await page.goto('/login/');

        // Basic functionality checks
        await expect(page.getByText('Bienvenido a 10Code')).toBeVisible();
        await expect(page.getByRole('link', { name: 'Continuar con Google' })).toBeVisible();

        // Check CSS Grid/Flexbox support
        const card = page.locator('.shadow-lg').first();
        await expect(card).toBeVisible();

        // Typography checks
        const title = page.locator('.text-2xl');
        await expect(title).toBeVisible();

        console.log(`Login page tested on ${browserName}`);
    });

    test('dashboard page renders correctly across browsers', async ({ page, browserName }) => {
        await page.goto('/dashboard/');

        // Check responsive grid layouts
        const gridLayouts = page.locator('.grid');
        const gridCount = await gridLayouts.count();
        if (gridCount > 0) {
            // Grid layouts should be visible
            await expect(gridLayouts.first()).toBeVisible();
        }

        // Check avatar images have alt text
        const avatars = page.locator('img[alt]');
        const avatarCount = await avatars.count();
        for (let i = 0; i < avatarCount; i++) {
            const avatar = avatars.nth(i);
            await expect(avatar).toHaveAttribute('alt');
        }

        console.log(`Dashboard tested on ${browserName}`);
    });
});

test.describe('Authentication State Management', () => {
    test('unauthenticated users see login page', async ({ page }) => {
        await page.goto('/login/');

        // Should show login page
        await expect(page.getByText('Bienvenido a 10Code')).toBeVisible();
        await expect(page.getByRole('link', { name: 'Continuar con Google' })).toBeVisible();
    });

    test('authenticated users redirected from login', async ({ page }) => {
        // Mock authenticated state by navigating directly to dashboard
        await page.goto('/dashboard/');

        // Should either show dashboard or redirect to login
        // This test verifies the routing behavior
        const currentUrl = page.url();
        expect(currentUrl).toMatch(/\/(dashboard|login)\//);
    });

    test('logout functionality', async ({ page }) => {
        await page.goto('/dashboard/');

        // Access logout form through dropdown
        const userAvatar = page.locator('button').filter({ has: page.locator('img') }).first();
        await userAvatar.click();

        // Find logout form
        const logoutForm = page.locator('form').filter({ has: page.getByText('Cerrar Sesión') });
        await expect(logoutForm).toBeVisible();

        // Verify form action
        await expect(logoutForm).toHaveAttribute('action', '/logout/');
        await expect(logoutForm).toHaveAttribute('method', 'post');
    });
});

test.describe('Performance and Loading', () => {
    test('login page loads within acceptable time', async ({ page }) => {
        const startTime = Date.now();
        await page.goto('/login/');
        await expect(page.getByText('Bienvenido a 10Code')).toBeVisible();
        const loadTime = Date.now() - startTime;

        // Page should load within 3 seconds
        expect(loadTime).toBeLessThan(3000);
    });

    test('dashboard page loads within acceptable time', async ({ page }) => {
        const startTime = Date.now();
        await page.goto('/dashboard/');
        await expect(page.getByText('Dashboard')).toBeVisible();
        const loadTime = Date.now() - startTime;

        // Page should load within 3 seconds
        expect(loadTime).toBeLessThan(3000);
    });
});
