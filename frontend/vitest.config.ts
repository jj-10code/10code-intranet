import { defineConfig } from 'vitest/config'
import react from '@vitejs/plugin-react'
import path from 'path'

export default defineConfig({
    plugins: [react()],
    test: {
        globals: true,
        environment: 'jsdom',
        setupFiles: ['./tests/setup.ts'],
        css: true,
        // Include only Vitest test files (not Playwright .spec.ts files)
        include: ['**/*.{test,spec}.{ts,tsx}'],
        exclude: [
            'node_modules/',
            'dist/',
            'tests/e2e/**', // Exclude Playwright E2E tests
            'playwright-report/',
            'playwright.config.ts',
        ],
        typecheck: {
            tsconfig: './tsconfig.test.json',
        },
        coverage: {
            provider: 'v8',
            reporter: ['text', 'json', 'html'],
            exclude: [
                'node_modules/',
                'tests/',
                '**/*.d.ts',
                '**/*.config.*',
                '**/mockData',
                'src/main.tsx',
            ],
        },
    },
    resolve: {
        alias: {
            '@': path.resolve(__dirname, './src'),
        },
    },
})
