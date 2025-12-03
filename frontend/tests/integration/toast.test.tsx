import { render, screen, waitFor } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { vi, describe, it, expect, beforeEach } from 'vitest'
import { toast } from 'sonner'
import UserCreate from '@/pages/users/Create'
import { DeactivateUserModal } from '@/components/shared/DeactivateUserModal'

// Mock de sonner
vi.mock('sonner', () => ({
    toast: {
        success: vi.fn(),
        error: vi.fn(),
    },
    Toaster: () => null,
}))

// Mock de componentes UI
vi.mock('@/components/layout/app-layout', () => ({
    AppLayout: ({ children }: { children: React.ReactNode }) => <div>{children}</div>,
}))

vi.mock('@/components/ui/dialog', () => ({
    Dialog: ({ children, open }: { children: React.ReactNode; open: boolean }) => open ? <div>{children}</div> : null,
    DialogContent: ({ children }: { children: React.ReactNode }) => <div>{children}</div>,
    DialogHeader: ({ children }: { children: React.ReactNode }) => <div>{children}</div>,
    DialogTitle: ({ children }: { children: React.ReactNode }) => <div>{children}</div>,
    DialogDescription: ({ children }: { children: React.ReactNode }) => <div>{children}</div>,
    DialogFooter: ({ children }: { children: React.ReactNode }) => <div>{children}</div>,
}))

vi.mock('@/components/ui/card', () => ({
    Card: ({ children }: { children: React.ReactNode }) => <div>{children}</div>,
    CardHeader: ({ children }: { children: React.ReactNode }) => <div>{children}</div>,
    CardTitle: ({ children }: { children: React.ReactNode }) => <div>{children}</div>,
    CardDescription: ({ children }: { children: React.ReactNode }) => <div>{children}</div>,
    CardContent: ({ children }: { children: React.ReactNode }) => <div>{children}</div>,
}))

vi.mock('@/components/ui/input', () => ({
    Input: (props: any) => <input {...props} />,
}))

vi.mock('@/components/ui/label', () => ({
    Label: ({ children, htmlFor }: { children: React.ReactNode; htmlFor?: string }) => <label htmlFor={htmlFor}>{children}</label>,
}))

vi.mock('@/components/ui/checkbox', () => ({
    Checkbox: (props: any) => <input type="checkbox" {...props} />,
}))

vi.mock('@/components/ui/button', () => ({
    Button: ({ children, onClick, type }: { children: React.ReactNode; onClick?: () => void; type?: 'button' | 'submit' | 'reset' }) => (
        <button onClick={onClick} type={type}>{children}</button>
    ),
}))

// Mock de Inertia router
const { mockPost } = vi.hoisted(() => ({
    mockPost: vi.fn(),
}))

vi.mock('@inertiajs/react', async (importOriginal) => {
    const actual = await importOriginal() as any
    return {
        ...actual,
        Head: ({ title }: { title: string }) => <title>{title}</title>,
        usePage: () => ({
            props: {
                auth: { user: { id: 1, name: 'Test', email: 'test@example.com' } },
                flash: [],
                permissions: {
                    can_assign_roles: true,
                    'accounts.add_user': true
                }
            }
        }),
        useForm: () => ({
            data: {
                email: 'test@example.com',
                first_name: 'Test',
                last_name: 'User',
                date_of_birth: '1990-01-01',
                roles: [],
            },
            setData: vi.fn(),
            post: mockPost,
            processing: false,
            errors: {},
        }),
        router: {
            post: mockPost,
        },
    }
})

describe('Toast Notifications Integration', () => {
    beforeEach(() => {
        vi.clearAllMocks()
    })

    describe('User Creation', () => {
        it('shows success toast on successful user creation', async () => {
            mockPost.mockImplementation((url, { onSuccess }) => {
                onSuccess()
            })

            render(
                <UserCreate
                    available_roles={[]}
                    permissions={{ can_assign_roles: true }}
                />
            )

            const submitButton = screen.getByText('Crear Usuario')
            await userEvent.click(submitButton)

            expect(toast.success).toHaveBeenCalledWith('Usuario creado exitosamente')
        })

        it('shows error toast on failed user creation', async () => {
            const errors = { email: 'Email already exists' }
            mockPost.mockImplementation((url, { onError }) => {
                onError(errors)
            })

            render(
                <UserCreate
                    available_roles={[]}
                    permissions={{ can_assign_roles: true }}
                />
            )

            const submitButton = screen.getByText('Crear Usuario')
            await userEvent.click(submitButton)

            expect(toast.error).toHaveBeenCalledWith('Error al crear usuario', expect.objectContaining({
                description: 'Email already exists'
            }))
        })
    })

    describe('User Deactivation', () => {
        it('shows success toast on successful deactivation', async () => {
            mockPost.mockImplementation((url, data, { onSuccess }) => {
                onSuccess()
            })

            const user = {
                id: 1,
                first_name: 'John',
                last_name: 'Doe',
                email: 'john@example.com',
                roles: [],
                is_active: true,
                date_of_birth: '1990-01-01',
                avatar_url: null,
            }

            render(
                <DeactivateUserModal
                    user={user}
                    open={true}
                    onOpenChange={vi.fn()}
                />
            )

            const reasonInput = screen.getByLabelText(/motivo/i)
            await userEvent.type(reasonInput, 'Test reason')

            const confirmButton = screen.getByText('Confirmar Desactivación')
            await userEvent.click(confirmButton)

            expect(toast.success).toHaveBeenCalledWith('Usuario desactivado exitosamente')
        })

        it('shows error toast on failed deactivation', async () => {
            mockPost.mockImplementation((url, data, { onError }) => {
                onError()
            })

            const user = {
                id: 1,
                first_name: 'John',
                last_name: 'Doe',
                email: 'john@example.com',
                roles: [],
                is_active: true,
                date_of_birth: '1990-01-01',
                avatar_url: null,
            }

            render(
                <DeactivateUserModal
                    user={user}
                    open={true}
                    onOpenChange={vi.fn()}
                />
            )

            const reasonInput = screen.getByLabelText(/motivo/i)
            await userEvent.type(reasonInput, 'Test reason')

            const confirmButton = screen.getByText('Confirmar Desactivación')
            await userEvent.click(confirmButton)

            expect(toast.error).toHaveBeenCalledWith('Error al desactivar usuario')
        })
    })
})
