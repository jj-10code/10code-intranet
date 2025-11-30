import { describe, it, expect } from 'vitest'
import { render, screen } from '@testing-library/react'
import { UserTable } from '@/components/shared/UserTable'
import type { User } from '@/types/models'

describe('UserTable', () => {
    const mockUsers: User[] = [
        {
            id: 1,
            email: 'john@10code.es',
            first_name: 'John',
            last_name: 'Doe',
            avatar_url: null,
            is_active: true,
            date_of_birth: '1990-01-01',
            roles: ['admin', 'employee'],
        },
        {
            id: 2,
            email: 'jane@10code.es',
            first_name: 'Jane',
            last_name: 'Smith',
            avatar_url: null,
            is_active: false,
            date_of_birth: '1985-05-15',
            roles: ['employee'],
        },
    ]

    it('renders users correctly', () => {
        render(<UserTable users={mockUsers} />)

        // Check headers
        expect(screen.getByText('Usuario')).toBeInTheDocument()
        expect(screen.getByText('Email')).toBeInTheDocument()
        expect(screen.getByText('Estado')).toBeInTheDocument()
        expect(screen.getByText('Roles')).toBeInTheDocument()

        // Check user data
        expect(screen.getByText('John Doe')).toBeInTheDocument()
        expect(screen.getByText('john@10code.es')).toBeInTheDocument()
        expect(screen.getByText('Jane Smith')).toBeInTheDocument()
        expect(screen.getByText('jane@10code.es')).toBeInTheDocument()
    })

    it('shows active/inactive badges correctly', () => {
        render(<UserTable users={mockUsers} />)

        expect(screen.getByText('Activo')).toBeInTheDocument()
        expect(screen.getByText('Inactivo')).toBeInTheDocument()
    })

    it('renders roles as badges', () => {
        render(<UserTable users={mockUsers} />)

        // Check role badges
        const adminBadge = screen.getByText('admin')
        const employeeBadges = screen.getAllByText('employee')

        expect(adminBadge).toBeInTheDocument()
        expect(employeeBadges).toHaveLength(2) // Both users have employee role
    })

    it('shows empty state when no users', () => {
        render(<UserTable users={[]} />)

        expect(screen.getByText('No se encontraron usuarios.')).toBeInTheDocument()
    })

    it('formats date of birth correctly', () => {
        render(<UserTable users={mockUsers} />)

        // Should show formatted dates
        expect(screen.getByText('1/1/1990')).toBeInTheDocument()
        expect(screen.getByText('15/5/1985')).toBeInTheDocument()
    })

    it('shows N/A for missing date of birth', () => {
        const userWithoutDob: User = {
            id: 3,
            email: 'test@10code.es',
            first_name: 'Test',
            last_name: 'User',
            avatar_url: null,
            is_active: true,
            date_of_birth: null,
            roles: [],
        }

        render(<UserTable users={[userWithoutDob]} />)

        expect(screen.getByText('N/A')).toBeInTheDocument()
    })
})