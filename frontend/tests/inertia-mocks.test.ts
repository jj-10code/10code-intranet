import { describe, it, expect, vi } from 'vitest'
import { usePage } from '@inertiajs/react'

describe('Inertia Mocks Verification', () => {
    it('should have usePage mock working', () => {
        const page = usePage()

        expect(page).toBeDefined()
        expect(page.props).toBeDefined()

        // Type assertion for test mock
        const auth = (page.props as any).auth
        expect(auth).toBeDefined()
        expect(auth.user).toEqual({
            id: 1,
            name: 'Test User',
            email: 'test@10code.es',
            avatar: null,
        })
    })

    it('should have correct URL', () => {
        const page = usePage()
        expect(page.url).toBe('/dashboard/')
    })

    it('should be a mocked function', () => {
        expect(vi.isMockFunction(usePage)).toBe(true)
    })
})

describe('Window Mocks Verification', () => {
    it('should have matchMedia mock', () => {
        const mediaQuery = window.matchMedia('(prefers-color-scheme: dark)')

        expect(mediaQuery).toBeDefined()
        expect(mediaQuery.matches).toBe(false)
        expect(typeof mediaQuery.addEventListener).toBe('function')
    })
})
