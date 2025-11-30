import { describe, it, expect, vi } from 'vitest'
import { render, screen } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { UserPagination } from '@/components/shared/UserPagination'
import { router } from '@inertiajs/react'

vi.mock('@inertiajs/react', () => ({
    router: {
        get: vi.fn(),
    },
}))

vi.mock('@tabler/icons-react', () => ({
    IconChevronLeft: () => <span>IconChevronLeft</span>,
    IconChevronRight: () => <span>IconChevronRight</span>,
}))

describe('UserPagination', () => {
    const mockFilters = {
        search: '',
        is_active: '',
        role: '',
    }

    beforeEach(() => {
        vi.clearAllMocks()
    })

    it('renders pagination info', () => {
        const pagination = {
            current_page: 2,
            total_pages: 5,
            has_next: true,
            has_previous: true,
        }

        render(<UserPagination pagination={pagination} filters={mockFilters} />)

        expect(screen.getByText('Página 2 de 5')).toBeInTheDocument()
        expect(screen.getByText('Anterior')).toBeInTheDocument()
        expect(screen.getByText('Siguiente')).toBeInTheDocument()
    })

    it('disables previous button on first page', () => {
        const pagination = {
            current_page: 1,
            total_pages: 3,
            has_next: true,
            has_previous: false,
        }

        render(<UserPagination pagination={pagination} filters={mockFilters} />)

        const prevButton = screen.getByText('Anterior')
        expect(prevButton).toBeDisabled()
    })

    it('disables next button on last page', () => {
        const pagination = {
            current_page: 3,
            total_pages: 3,
            has_next: false,
            has_previous: true,
        }

        render(<UserPagination pagination={pagination} filters={mockFilters} />)

        const nextButton = screen.getByText('Siguiente')
        expect(nextButton).toBeDisabled()
    })

    it('calls router.get when navigation buttons are clicked', async () => {
        const user = userEvent.setup()
        const pagination = {
            current_page: 2,
            total_pages: 5,
            has_next: true,
            has_previous: true,
        }

        render(<UserPagination pagination={pagination} filters={mockFilters} />)

        // Click previous button
        const prevButton = screen.getByText('Anterior')
        await user.click(prevButton)

        expect(router.get).toHaveBeenCalledWith('/users', {
            ...mockFilters,
            page: '1',
        }, {
            preserveState: true,
            preserveScroll: true,
        })

        // Click next button
        const nextButton = screen.getByText('Siguiente')
        await user.click(nextButton)

        expect(router.get).toHaveBeenCalledWith('/users', {
            ...mockFilters,
            page: '3',
        }, {
            preserveState: true,
            preserveScroll: true,
        })
    })

    it('preserves filters when navigating', async () => {
        const user = userEvent.setup()
        const pagination = {
            current_page: 1,
            total_pages: 3,
            has_next: true,
            has_previous: false,
        }
        const filtersWithValues = {
            search: 'john',
            is_active: 'true',
            role: 'admin',
        }

        render(<UserPagination pagination={pagination} filters={filtersWithValues} />)

        const nextButton = screen.getByText('Siguiente')
        await user.click(nextButton)

        expect(router.get).toHaveBeenCalledWith('/users', {
            search: 'john',
            is_active: 'true',
            role: 'admin',
            page: '2',
        }, {
            preserveState: true,
            preserveScroll: true,
        })
    })

    it('does not render when only one page', () => {
        const pagination = {
            current_page: 1,
            total_pages: 1,
            has_next: false,
            has_previous: false,
        }

        const { container } = render(<UserPagination pagination={pagination} filters={mockFilters} />)

        expect(container.firstChild).toBeNull()
    })
})