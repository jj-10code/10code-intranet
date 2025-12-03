import '@testing-library/jest-dom'
import { cleanup } from '@testing-library/react'
import React from 'react'
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
            flash: [],
        },
        url: '/dashboard/',
    })),
    Link: ({ children, ...props }: { children: React.ReactNode;[key: string]: unknown }) =>
        React.createElement('a', props, children),
    Head: ({ title }: { title?: string }) => React.createElement('title', {}, title),
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

// Mock de useTheme hook
vi.mock('@/hooks/use-theme', () => ({
    useTheme: vi.fn(() => ({
        theme: 'system',
        setTheme: vi.fn(),
    })),
}))

// Mock de use-mobile hook
vi.mock('@/hooks/use-mobile', () => ({
    useIsMobile: vi.fn(() => false),
}))

// Mock completo de sidebar con importOriginal
vi.mock('@/components/ui/sidebar', async (importOriginal) => {
    const actual = await importOriginal() as unknown
    return {
        ...(actual as object),
        useSidebar: vi.fn(() => ({
            isMobile: false,
            state: 'expanded',
            open: true,
            setOpen: vi.fn(),
            openMobile: false,
            setOpenMobile: vi.fn(),
            toggleSidebar: vi.fn(),
        })),
    }
})

// Mock de componentes adicionales necesarios
vi.mock('@/components/layout/app-sidebar', () => ({
    AppSidebar: ({ children }: { children: React.ReactNode }) => children,
}))

vi.mock('@/components/layout/app-header', () => ({
    AppHeader: ({ children }: { children: React.ReactNode }) => children,
}))

vi.mock('@/components/ui/dropdown-menu', () => ({
    DropdownMenu: ({ children }: { children: React.ReactNode }) => children,
    DropdownMenuContent: ({ children }: { children: React.ReactNode }) => children,
    DropdownMenuItem: ({ children, onClick }: { children: React.ReactNode; onClick?: () => void }) =>
        React.createElement('div', { onClick, role: 'menuitem', tabIndex: -1 }, children),
    DropdownMenuTrigger: ({ children }: { children: React.ReactNode }) => children,
}))

vi.mock('@tabler/icons-react', () => ({
    IconSun: () => React.createElement('svg', { 'data-testid': 'icon-sun' }),
    IconMoon: () => React.createElement('svg', { 'data-testid': 'icon-moon' }),
    IconChevronDown: () => React.createElement('svg', { 'data-testid': 'icon-chevron-down' }),
    IconDashboard: () => React.createElement('svg', { 'data-testid': 'icon-dashboard' }),
    IconUsers: () => React.createElement('svg', { 'data-testid': 'icon-users' }),
    IconCirclePlusFilled: () => React.createElement('svg', { 'data-testid': 'icon-circle-plus' }),
    IconMail: () => React.createElement('svg', { 'data-testid': 'icon-mail' }),
    IconHelp: () => React.createElement('svg', { 'data-testid': 'icon-help' }),
    IconCheck: () => React.createElement('svg', { 'data-testid': 'icon-check' }),
}))

// Mock de pointer capture para Radix UI
window.HTMLElement.prototype.hasPointerCapture = vi.fn()
window.HTMLElement.prototype.setPointerCapture = vi.fn()
window.HTMLElement.prototype.releasePointerCapture = vi.fn()
window.HTMLElement.prototype.scrollIntoView = vi.fn()
window.Element.prototype.scrollIntoView = vi.fn()