import '@testing-library/jest-dom'
import { cleanup } from '@testing-library/react'
import { afterEach, vi } from 'vitest'

// Cleanup después de cada test
afterEach(() => {
    cleanup()
})

// Mock de Inertia
vi.mock('@inertiajs/react', () => ({
    usePage: vi.fn(() => ({
        props: {
            auth: {
                user: {
                    id: 1,
                    name: 'Test User',
                    email: 'test@10code.es',
                    avatar: null,
                },
            },
        },
        url: '/dashboard/',
    })),
    Link: vi.fn(({ children, ...props }: any) => {
        // Return a mock element
        return { type: 'a', props: { ...props, children } }
    }),
    Head: vi.fn(({ title }: any) => {
        // Return a mock element
        return { type: 'title', props: { children: title } }
    }),
    router: {
        visit: vi.fn(),
        reload: vi.fn(),
    },
}))

// Mock de window.matchMedia para dark mode
Object.defineProperty(window, 'matchMedia', {
    writable: true,
    value: vi.fn().mockImplementation(query => ({
        matches: false,
        media: query,
        onchange: null,
        addListener: vi.fn(),
        removeListener: vi.fn(),
        addEventListener: vi.fn(),
        removeEventListener: vi.fn(),
        dispatchEvent: vi.fn(),
    })),
})
