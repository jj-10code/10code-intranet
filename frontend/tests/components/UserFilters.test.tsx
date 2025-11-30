import { describe, it, expect, vi, beforeEach } from 'vitest'
import { render, screen, waitFor } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { UserFilters } from '@/components/shared/UserFilters'
import { router } from '@inertiajs/react'

vi.mock('@inertiajs/react', () => ({
    router: {
        get: vi.fn(),
    },
}))

describe('UserFilters', () => {
    const mockFilters = {
        search: '',
        is_active: '',
        role: '',
    }

    beforeEach(() => {
        vi.clearAllMocks()
    })

    it('renders all filter controls', () => {
        render(<UserFilters filters={mockFilters} />)

        expect(screen.getByLabelText('Buscar usuarios')).toBeInTheDocument()
        expect(screen.getByText('Estado')).toBeInTheDocument()
        expect(screen.getByText('Rol')).toBeInTheDocument()
    })

    it('shows current filter values', () => {
        const filtersWithValues = {
            search: 'john',
            is_active: 'true',
            role: 'admin',
        }

        render(<UserFilters filters={filtersWithValues} />)

        const searchInput = screen.getByLabelText('Buscar usuarios') as HTMLInputElement
        expect(searchInput.value).toBe('john')

        // Check that the select buttons show the correct values
        expect(screen.getByText('Activos')).toBeInTheDocument()
        expect(screen.getByText('Administrador')).toBeInTheDocument()
    })

    it('calls router.get when select values change', async () => {
        const user = userEvent.setup()

        render(<UserFilters filters={mockFilters} />)

        // Change is_active filter - get all comboboxes and use first one
        const comboboxes = screen.getAllByRole('combobox')
        const statusSelect = comboboxes[0]
        await user.click(statusSelect)
        await user.click(screen.getByText('Activos'))

        expect(router.get).toHaveBeenCalledWith('/users', {
            ...mockFilters,
            is_active: 'true',
        }, {
            preserveState: true,
            preserveScroll: true,
        })

        // Change role filter - use second combobox
        const roleSelect = comboboxes[1]
        await user.click(roleSelect)
        await user.click(screen.getByText('Administrador'))

        expect(router.get).toHaveBeenCalledWith('/users', {
            ...mockFilters,
            role: 'admin',
        }, {
            preserveState: true,
            preserveScroll: true,
        })
    })

    it('debounces search input', async () => {
        const user = userEvent.setup()

        render(<UserFilters filters={mockFilters} />)

        const searchInput = screen.getByLabelText('Buscar usuarios')

        // Type quickly
        await user.type(searchInput, 'john')

        // Should not call router.get immediately
        expect(router.get).not.toHaveBeenCalled()

        // Wait for debounce
        await waitFor(() => {
            expect(router.get).toHaveBeenCalledWith('/users', {
                ...mockFilters,
                search: 'john',
            }, {
                preserveState: true,
                preserveScroll: true,
            })
        }, { timeout: 400 })
    })

    it('preserves other filters when changing one', async () => {
        const user = userEvent.setup()
        const filtersWithValues = {
            search: 'existing',
            is_active: 'true',
            role: 'admin',
        }

        render(<UserFilters filters={filtersWithValues} />)

        // Change role filter - use second combobox
        const comboboxes = screen.getAllByRole('combobox')
        const roleSelect = comboboxes[1]
        await user.click(roleSelect)
        await user.click(screen.getByText('Empleado'))

        expect(router.get).toHaveBeenCalledWith('/users', {
            search: 'existing',
            is_active: 'true',
            role: 'employee',
        }, {
            preserveState: true,
            preserveScroll: true,
        })
    })
})