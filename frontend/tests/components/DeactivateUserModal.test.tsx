import { describe, it, expect, vi, beforeEach } from 'vitest'
import { render, screen } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { DeactivateUserModal } from '@/components/shared/DeactivateUserModal'
import { router } from '@inertiajs/react'

vi.mock('@inertiajs/react', () => ({
    router: {
        post: vi.fn(),
    },
}))

describe('DeactivateUserModal', () => {
    const mockUser = {
        id: 1,
        email: 'john@10code.es',
        first_name: 'John',
        last_name: 'Doe',
        avatar_url: null,
        is_active: true,
        date_of_birth: '1990-01-01',
        roles: ['employee'],
    }

    const mockOnOpenChange = vi.fn()

    beforeEach(() => {
        vi.clearAllMocks()
    })

    it('renders with user data', () => {
        render(
            <DeactivateUserModal
                user={mockUser}
                open={true}
                onOpenChange={mockOnOpenChange}
            />
        )

        expect(screen.getByText(/Desactivar Usuario/i)).toBeInTheDocument()
        expect(screen.getByText(/John Doe/i)).toBeInTheDocument()
        expect(screen.getByText(/john@10code.es/i)).toBeInTheDocument()
    })

    it('calls router.post on confirm with reason', async () => {
        const user = userEvent.setup()

        render(
            <DeactivateUserModal
                user={mockUser}
                open={true}
                onOpenChange={mockOnOpenChange}
            />
        )

        const textarea = screen.getByLabelText(/Motivo de desactivación/i)
        await user.type(textarea, 'Baja temporal por excedencia')

        const confirmButton = screen.getByRole('button', { name: /Confirmar Desactivación/i })
        await user.click(confirmButton)

        expect(router.post).toHaveBeenCalledWith(
            '/users/1/deactivate',
            { reason: 'Baja temporal por excedencia' },
            expect.objectContaining({
                onSuccess: expect.any(Function),
                onFinish: expect.any(Function),
            })
        )
    })

    it('disables confirm button when reason is empty', () => {
        render(
            <DeactivateUserModal
                user={mockUser}
                open={true}
                onOpenChange={mockOnOpenChange}
            />
        )

        const confirmButton = screen.getByRole('button', { name: /Confirmar Desactivación/i })
        expect(confirmButton).toBeDisabled()
    })

    it('enables confirm button when reason is provided', async () => {
        const user = userEvent.setup()

        render(
            <DeactivateUserModal
                user={mockUser}
                open={true}
                onOpenChange={mockOnOpenChange}
            />
        )

        const textarea = screen.getByLabelText(/Motivo de desactivación/i)
        await user.type(textarea, 'Test reason')

        const confirmButton = screen.getByRole('button', { name: /Confirmar Desactivación/i })
        expect(confirmButton).not.toBeDisabled()
    })

    it('calls onOpenChange when cancel button is clicked', async () => {
        const user = userEvent.setup()

        render(
            <DeactivateUserModal
                user={mockUser}
                open={true}
                onOpenChange={mockOnOpenChange}
            />
        )

        const cancelButton = screen.getByRole('button', { name: /Cancelar/i })
        await user.click(cancelButton)

        expect(mockOnOpenChange).toHaveBeenCalledWith(false)
    })

    it('shows loading state when submitting', async () => {
        const user = userEvent.setup()

        // Mock router.post to not call callbacks immediately
        const mockPost = vi.fn()
        vi.mocked(router.post).mockImplementation(mockPost)

        render(
            <DeactivateUserModal
                user={mockUser}
                open={true}
                onOpenChange={mockOnOpenChange}
            />
        )

        const textarea = screen.getByLabelText(/Motivo de desactivación/i)
        await user.type(textarea, 'Test reason')

        const confirmButton = screen.getByRole('button', { name: /Confirmar Desactivación/i })
        await user.click(confirmButton)

        // Button text should change to loading state
        expect(screen.getByRole('button', { name: /Desactivando.../i })).toBeInTheDocument()
    })
})
