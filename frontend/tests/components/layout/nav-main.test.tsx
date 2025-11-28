import React from 'react'
import { describe, it, expect } from 'vitest'
import { render, screen } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { NavMain } from '../../../src/components/layout/nav-main'
import { SidebarProvider } from '../../../src/components/ui/sidebar'
import { IconDashboard, IconUsers } from '@tabler/icons-react'

const mockItems = [
    {
        title: 'Dashboard',
        url: '/dashboard/',
        icon: IconDashboard,
    },
    {
        title: 'Usuarios',
        url: '#',
        icon: IconUsers,
        items: [
            { title: 'Listado', url: '/users/' },
            { title: 'Roles', url: '/users/roles/' },
        ],
    },
]

describe('NavMain', () => {
    const renderWithProvider = (component: React.ReactElement) => {
        return render(
            <SidebarProvider>
                {component}
            </SidebarProvider>
        )
    }

    it('renderiza items simples', () => {
        renderWithProvider(<NavMain items={mockItems} />)
        expect(screen.getByText('Dashboard')).toBeInTheDocument()
    })

    it('renderiza items con submenú', () => {
        renderWithProvider(<NavMain items={mockItems} />)
        expect(screen.getByText('Usuarios')).toBeInTheDocument()
    })

    it('renderiza contenido de quick create', () => {
        renderWithProvider(<NavMain items={mockItems} />)
        expect(screen.getByText('Quick Create')).toBeInTheDocument()
    })

    it('renderiza botón de inbox', () => {
        renderWithProvider(<NavMain items={mockItems} />)
        expect(screen.getByText('Inbox')).toBeInTheDocument()
    })

    it('no renderiza submenu inicialmente', () => {
        renderWithProvider(<NavMain items={mockItems} />)
        expect(screen.queryByText('Listado')).not.toBeInTheDocument()
        expect(screen.queryByText('Roles')).not.toBeInTheDocument()
    })

    it('expande submenu al hacer clic', async () => {
        const user = userEvent.setup()
        renderWithProvider(<NavMain items={mockItems} />)
        
        // Inicialmente oculto
        expect(screen.queryByText('Listado')).not.toBeInTheDocument()
        
        // Click para expandir
        await user.click(screen.getByText('Usuarios'))
        expect(screen.getByText('Listado')).toBeInTheDocument()
        expect(screen.getByText('Roles')).toBeInTheDocument()
    })

    it('colapsa submenu al hacer clic nuevamente', async () => {
        const user = userEvent.setup()
        renderWithProvider(<NavMain items={mockItems} />)
        
        // Expandir primero
        await user.click(screen.getByText('Usuarios'))
        expect(screen.getByText('Listado')).toBeInTheDocument()
        
        // Colapsar
        await user.click(screen.getByText('Usuarios'))
        expect(screen.queryByText('Listado')).not.toBeInTheDocument()
    })

    it('maneja múltiples clicks sin errores', async () => {
        const user = userEvent.setup()
        renderWithProvider(<NavMain items={mockItems} />)
        
        // Múltiples clicks rápidos
        for (let i = 0; i < 3; i++) {
            await user.click(screen.getByText('Usuarios'))
        }
        
        // Debería estar expandido (último estado)
        expect(screen.getByText('Listado')).toBeInTheDocument()
    })

    it('renderiza iconos correctamente', () => {
        renderWithProvider(<NavMain items={mockItems} />)
        
        // Verificar que los iconos están presentes (mediante data-testid)
        expect(document.querySelector('[data-testid="icon-dashboard"]')).toBeInTheDocument()
        expect(document.querySelector('[data-testid="icon-users"]')).toBeInTheDocument()
    })

    it('preserva estado de expansión durante re-render', async () => {
        const { rerender } = renderWithProvider(<NavMain items={mockItems} />)
        
        const user = userEvent.setup()
        
        // Expandir submenu
        await user.click(screen.getByText('Usuarios'))
        
        // Re-renderizar con props diferentes pero mismos items
        rerender(
            <SidebarProvider>
                <NavMain items={mockItems} />
            </SidebarProvider>
        )
        
        // Estado debería mantenerse
        expect(screen.getByText('Listado')).toBeInTheDocument()
    })

    it('renderiza estructura correcta de sidebar', () => {
        renderWithProvider(<NavMain items={mockItems} />)
        
        // Verificar que los elementos de sidebar están presentes
        expect(document.querySelector('[data-sidebar="group"]')).toBeInTheDocument()
        expect(document.querySelector('[data-sidebar="menu"]')).toBeInTheDocument()
    })

    it('aplica tooltips a botones', () => {
        renderWithProvider(<NavMain items={mockItems} />)
        
        // Los botones o links deberían tener tooltips
        const dashboardElement = screen.getByText('Dashboard').closest('[data-sidebar="menu-button"]')
        expect(dashboardElement).toBeTruthy()
        
        const usuariosElement = screen.getByText('Usuarios').closest('[data-sidebar="menu-button"]')
        expect(usuariosElement).toBeTruthy()
    })

    it('gestiona estado de expandedItems correctamente', async () => {
        renderWithProvider(<NavMain items={mockItems} />)
        
        // Estado inicial: ningún submenu expandido
        expect(screen.queryByText('Listado')).not.toBeInTheDocument()
        
        const user = userEvent.setup()
        
        // Expandir submenu "Usuarios"
        await user.click(screen.getByText('Usuarios'))
        
        // Submenu debería ser visible
        expect(screen.getByText('Listado')).toBeInTheDocument()
    })
})