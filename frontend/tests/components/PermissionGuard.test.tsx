import { render, screen } from '@testing-library/react'
import { PermissionGuard } from '@/components/shared/PermissionGuard'
import { usePage } from '@inertiajs/react'
import { vi, describe, it, expect, beforeEach } from 'vitest'

// Mock usePage
vi.mock('@inertiajs/react', () => ({
    usePage: vi.fn(),
    Link: ({ children, ...props }: any) => <a {...props}>{children}</a>,
}))

describe('PermissionGuard', () => {
    beforeEach(() => {
        vi.clearAllMocks()
    })

    it('renders children when user has permission', () => {
        (usePage as any).mockReturnValue({
            props: {
                permissions: {
                    'test.permission': true,
                },
            },
        })

        render(
            <PermissionGuard permission="test.permission">
                <div>Protected Content</div>
            </PermissionGuard>
        )

        expect(screen.getByText('Protected Content')).toBeInTheDocument()
        expect(screen.queryByText('Acceso Denegado')).not.toBeInTheDocument()
    })

    it('renders default AccessDenied when user lacks permission', () => {
        (usePage as any).mockReturnValue({
            props: {
                permissions: {
                    'test.permission': false,
                },
            },
        })

        render(
            <PermissionGuard permission="test.permission">
                <div>Protected Content</div>
            </PermissionGuard>
        )

        expect(screen.queryByText('Protected Content')).not.toBeInTheDocument()
        expect(screen.getByText('Acceso Denegado')).toBeInTheDocument()
        expect(screen.getByText('Permiso requerido: test.permission')).toBeInTheDocument()
    })

    it('renders custom fallback when provided and user lacks permission', () => {
        (usePage as any).mockReturnValue({
            props: {
                permissions: {
                    'test.permission': false,
                },
            },
        })

        render(
            <PermissionGuard
                permission="test.permission"
                fallback={<div>Custom Fallback</div>}
            >
                <div>Protected Content</div>
            </PermissionGuard>
        )

        expect(screen.queryByText('Protected Content')).not.toBeInTheDocument()
        expect(screen.getByText('Custom Fallback')).toBeInTheDocument()
        expect(screen.queryByText('Acceso Denegado')).not.toBeInTheDocument()
    })
})
