import { renderHook } from '@testing-library/react'
import { usePermissions } from '@/hooks/usePermissions'
import { usePage } from '@inertiajs/react'
import { vi, describe, it, expect, beforeEach } from 'vitest'

// Mock usePage
vi.mock('@inertiajs/react', () => ({
    usePage: vi.fn(),
}))

describe('usePermissions', () => {
    beforeEach(() => {
        vi.clearAllMocks()
    })

    it('can returns true if permission exists and is true', () => {
        (usePage as any).mockReturnValue({
            props: {
                permissions: {
                    'test.permission': true,
                },
            },
        })

        const { result } = renderHook(() => usePermissions())
        expect(result.current.can('test.permission')).toBe(true)
    })

    it('can returns false if permission exists and is false', () => {
        (usePage as any).mockReturnValue({
            props: {
                permissions: {
                    'test.permission': false,
                },
            },
        })

        const { result } = renderHook(() => usePermissions())
        expect(result.current.can('test.permission')).toBe(false)
    })

    it('can returns false if permission does not exist', () => {
        (usePage as any).mockReturnValue({
            props: {
                permissions: {},
            },
        })

        const { result } = renderHook(() => usePermissions())
        expect(result.current.can('test.permission')).toBe(false)
    })

    it('canAny returns true if at least one permission is true', () => {
        (usePage as any).mockReturnValue({
            props: {
                permissions: {
                    'perm.1': true,
                    'perm.2': false,
                },
            },
        })

        const { result } = renderHook(() => usePermissions())
        expect(result.current.canAny(['perm.1', 'perm.2'])).toBe(true)
    })

    it('canAny returns false if no permissions are true', () => {
        (usePage as any).mockReturnValue({
            props: {
                permissions: {
                    'perm.1': false,
                    'perm.2': false,
                },
            },
        })

        const { result } = renderHook(() => usePermissions())
        expect(result.current.canAny(['perm.1', 'perm.2'])).toBe(false)
    })

    it('canAll returns true if all permissions are true', () => {
        (usePage as any).mockReturnValue({
            props: {
                permissions: {
                    'perm.1': true,
                    'perm.2': true,
                },
            },
        })

        const { result } = renderHook(() => usePermissions())
        expect(result.current.canAll(['perm.1', 'perm.2'])).toBe(true)
    })

    it('canAll returns false if at least one permission is false', () => {
        (usePage as any).mockReturnValue({
            props: {
                permissions: {
                    'perm.1': true,
                    'perm.2': false,
                },
            },
        })

        const { result } = renderHook(() => usePermissions())
        expect(result.current.canAll(['perm.1', 'perm.2'])).toBe(false)
    })
})
