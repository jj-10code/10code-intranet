import { render, screen, fireEvent } from '@testing-library/react'
import { AccessDenied } from '@/components/shared/AccessDenied'
import { vi, describe, it, expect, beforeEach } from 'vitest'

describe('AccessDenied', () => {
    beforeEach(() => {
        vi.clearAllMocks()
    })

    it('renders default message', () => {
        render(<AccessDenied />)
        expect(screen.getByText('Acceso Denegado')).toBeInTheDocument()
        expect(screen.getByText('No tienes permisos para acceder a esta sección')).toBeInTheDocument()
    })

    it('renders custom message', () => {
        render(<AccessDenied message="Custom error message" />)
        expect(screen.getByText('Custom error message')).toBeInTheDocument()
    })

    it('renders permission when provided', () => {
        render(<AccessDenied permission="test.permission" />)
        expect(screen.getByText('Permiso requerido: test.permission')).toBeInTheDocument()
    })

    it('renders navigation buttons', () => {
        render(<AccessDenied />)
        expect(screen.getByText('Volver Atrás')).toBeInTheDocument()
        expect(screen.getByText('Ir al Dashboard')).toBeInTheDocument()
    })

    it('calls window.history.back when back button is clicked', () => {
        const backSpy = vi.spyOn(window.history, 'back')
        render(<AccessDenied />)

        fireEvent.click(screen.getByText('Volver Atrás'))
        expect(backSpy).toHaveBeenCalled()
    })

    it('dashboard link points to /dashboard', () => {
        render(<AccessDenied />)
        const link = screen.getByText('Ir al Dashboard').closest('a')
        expect(link).toHaveAttribute('href', '/dashboard')
    })
})
