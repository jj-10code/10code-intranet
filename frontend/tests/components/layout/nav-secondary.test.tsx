import React from 'react'
import { describe, it, expect, vi } from 'vitest'
import { render, screen } from '@testing-library/react'
import { NavSecondary } from '../../../src/components/layout/nav-secondary'
import { SidebarProvider } from '../../../src/components/ui/sidebar'
import { IconHelp } from '@tabler/icons-react'

// Mock usePage from inertia
vi.mock('@inertiajs/react', async (importOriginal) => {
    const actual = await importOriginal<any>()
    return {
        ...actual,
        usePage: () => ({
            url: '/help/',
            props: { auth: { user: {} } }
        }),
        Link: ({ children, href, className }: any) => <a href={href} className={className}>{children}</a>
    }
})

const mockItems = [
    {
        title: 'Ayuda',
        url: '/help/',
        icon: IconHelp,
    },
    {
        title: 'Otro',
        url: '/other/',
        icon: IconHelp,
    },
]

describe('NavSecondary', () => {
    const renderWithProvider = (component: React.ReactElement) => {
        return render(
            <SidebarProvider>
                {component}
            </SidebarProvider>
        )
    }

    it('renderiza items correctamente', () => {
        renderWithProvider(<NavSecondary items={mockItems} />)
        expect(screen.getByText('Ayuda')).toBeInTheDocument()
        expect(screen.getByText('Otro')).toBeInTheDocument()
    })

    it('marca el item activo basado en la URL', () => {
        renderWithProvider(<NavSecondary items={mockItems} />)

        // El item de Ayuda debería tener la clase de activo (bg-accent)
        // Buscamos el botón padre del texto "Ayuda" (que es un link <a>)
        const helpButton = screen.getByText('Ayuda').closest('a')
        expect(helpButton).toHaveClass('bg-accent')
        expect(helpButton).toHaveClass('text-accent-foreground')

        // El item Otro NO debería tener la clase activo
        const otherButton = screen.getByText('Otro').closest('a')
        expect(otherButton).not.toHaveClass('bg-accent')
    })
})
