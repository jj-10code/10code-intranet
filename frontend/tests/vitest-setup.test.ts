import { describe, it, expect } from 'vitest'

describe('Vitest Setup Verification', () => {
    it('should run a basic test', () => {
        expect(1 + 1).toBe(2)
    })

    it('should have globals available', () => {
        expect(describe).toBeDefined()
        expect(it).toBeDefined()
        expect(expect).toBeDefined()
    })

    it('should have jsdom environment', () => {
        expect(typeof window).toBe('object')
        expect(typeof document).toBe('object')
    })
})
