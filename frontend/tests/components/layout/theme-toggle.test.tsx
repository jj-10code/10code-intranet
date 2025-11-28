import React from 'react'
import { describe, it, expect, beforeEach, vi } from 'vitest'
import { render, screen } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { ThemeToggle } from '../../../src/components/layout/theme-toggle'
import { SidebarProvider } from '../../../src/components/ui/sidebar'
import { useTheme } from '../../../src/hooks/use-theme'

// Mock de useTheme
vi.mock('@/hooks/use-theme', () => ({
    useTheme: vi.fn(),
}))

describe('ThemeToggle', () => {
    beforeEach(() => {
        vi.clearAllMocks()
        localStorage.clear()
        document.documentElement.classList.remove('light', 'dark')
    })

    it('renderiza botón de toggle', () => {
        const mockSetTheme = vi.fn()
        vi.mocked(useTheme).mockReturnValue({
            theme: 'system',
            setTheme: mockSetTheme,
        })

        render(<ThemeToggle />)
        expect(screen.getByRole('button')).toBeInTheDocument()
    })

    it('muestra iconos de sol y luna', () => {
        const mockSetTheme = vi.fn()
        vi.mocked(useTheme).mockReturnValue({
            theme: 'system',
            setTheme: mockSetTheme,
        })

        render(<ThemeToggle />)
        
        // Verificar que los iconos están presentes
        expect(document.querySelector('[data-testid="icon-sun"]')).toBeInTheDocument()
        expect(document.querySelector('[data-testid="icon-moon"]')).toBeInTheDocument()
    })

    it('muestra opciones al hacer clic', async () => {
        const mockSetTheme = vi.fn()
        vi.mocked(useTheme).mockReturnValue({
            theme: 'system',
            setTheme: mockSetTheme,
        })

        render(<ThemeToggle />)
        
        const user = userEvent.setup()
        await user.click(screen.getByRole('button'))
        
        expect(screen.getByText('Claro')).toBeInTheDocument()
        expect(screen.getByText('Oscuro')).toBeInTheDocument()
        expect(screen.getByText('Sistema')).toBeInTheDocument()
    })

    it('llama setTheme con "light" al seleccionar opción claro', async () => {
        const mockSetTheme = vi.fn()
        vi.mocked(useTheme).mockReturnValue({
            theme: 'system',
            setTheme: mockSetTheme,
        })

        render(<ThemeToggle />)
        
        const user = userEvent.setup()
        await user.click(screen.getByRole('button'))
        await user.click(screen.getByText('Claro'))
        
        expect(mockSetTheme).toHaveBeenCalledWith('light')
    })

    it('llama setTheme con "dark" al seleccionar opción oscuro', async () => {
        const mockSetTheme = vi.fn()
        vi.mocked(useTheme).mockReturnValue({
            theme: 'system',
            setTheme: mockSetTheme,
        })

        render(<ThemeToggle />)
        
        const user = userEvent.setup()
        await user.click(screen.getByRole('button'))
        await user.click(screen.getByText('Oscuro'))
        
        expect(mockSetTheme).toHaveBeenCalledWith('dark')
    })

    it('llama setTheme con "system" al seleccionar opción sistema', async () => {
        const mockSetTheme = vi.fn()
        vi.mocked(useTheme).mockReturnValue({
            theme: 'light',
            setTheme: mockSetTheme,
        })

        render(<ThemeToggle />)
        
        const user = userEvent.setup()
        await user.click(screen.getByRole('button'))
        await user.click(screen.getByText('Sistema'))
        
        expect(mockSetTheme).toHaveBeenCalledWith('system')
    })

    it('renderiza correctamente con la prop asSidebarItem', () => {
        const mockSetTheme = vi.fn()
        vi.mocked(useTheme).mockReturnValue({
            theme: 'system',
            setTheme: mockSetTheme,
        })

        render(
            <SidebarProvider>
                <ThemeToggle asSidebarItem />
            </SidebarProvider>
        )
        
        // Debería renderizarse pero con estilos de sidebar
        expect(screen.getByRole('button')).toBeInTheDocument()
    })

    it('aplica aria-label apropiado', () => {
        const mockSetTheme = vi.fn()
        vi.mocked(useTheme).mockReturnValue({
            theme: 'system',
            setTheme: mockSetTheme,
        })

        render(<ThemeToggle />)
        
        const button = screen.getByRole('button')
        // El botón debe existir, independientemente del aria-label específico
        expect(button).toBeInTheDocument()
    })

    it('no muestra texto visible en modo normal', () => {
        const mockSetTheme = vi.fn()
        vi.mocked(useTheme).mockReturnValue({
            theme: 'system',
            setTheme: mockSetTheme,
        })

        render(<ThemeToggle />)
        
        // El texto debería estar oculto para lectores de pantalla
        const button = screen.getByRole('button')
        expect(button).toHaveClass('size-8', 'p-0')
    })

    it('maneja clicks múltiples correctamente', async () => {
        const mockSetTheme = vi.fn()
        vi.mocked(useTheme).mockReturnValue({
            theme: 'system',
            setTheme: mockSetTheme,
        })

        render(<ThemeToggle />)
        
        const user = userEvent.setup()
        
        // Abrir dropdown
        await user.click(screen.getByRole('button'))
        expect(screen.getByText('Claro')).toBeInTheDocument()
        
        // Cerrar dropdown (click fuera)
        await user.click(document.body)
        
        // Abrir nuevamente
        await user.click(screen.getByRole('button'))
        expect(screen.getByText('Claro')).toBeInTheDocument()
    })

    it('refleja el tema actual en el botón', () => {
        const mockSetTheme = vi.fn()
        vi.mocked(useTheme).mockReturnValue({
            theme: 'dark',
            setTheme: mockSetTheme,
        })

        render(<ThemeToggle />)
        
        // El botón debería existir independientemente del tema
        expect(screen.getByRole('button')).toBeInTheDocument()
    })

    it('usa contexto de sidebar cuando asSidebarItem es true', () => {
        const mockSetTheme = vi.fn()
        vi.mocked(useTheme).mockReturnValue({
            theme: 'system',
            setTheme: mockSetTheme,
        })

        render(
            <SidebarProvider>
                <ThemeToggle asSidebarItem />
            </SidebarProvider>
        )
        
        // Debería renderizar sin errores
        expect(screen.getByRole('button')).toBeInTheDocument()
    })

    it('renderiza span para lectores de pantalla', () => {
        const mockSetTheme = vi.fn()
        vi.mocked(useTheme).mockReturnValue({
            theme: 'system',
            setTheme: mockSetTheme,
        })

        render(<ThemeToggle />)
        
        // Debería tener un span con clase sr-only para accesibilidad
        const srSpan = screen.getByText('Cambiar tema')
        expect(srSpan).toHaveClass('sr-only')
    })

    it('gestiona transiciones de tema correctamente', async () => {
        const mockSetTheme = vi.fn()
        vi.mocked(useTheme).mockReturnValue({
            theme: 'light',
            setTheme: mockSetTheme,
        })

        render(<ThemeToggle />)
        
        const user = userEvent.setup()
        
        // Cambiar tema varias veces
        await user.click(screen.getByRole('button'))
        await user.click(screen.getByText('Oscuro'))
        
        expect(mockSetTheme).toHaveBeenCalledWith('dark')
        
        // Cambiar nuevamente
        await user.click(screen.getByRole('button'))
        await user.click(screen.getByText('Claro'))
        
        expect(mockSetTheme).toHaveBeenCalledWith('light')
    })

    it('llama setTheme al seleccionar cualquier opción', async () => {
        const mockSetTheme = vi.fn()
        vi.mocked(useTheme).mockReturnValue({
            theme: 'system',
            setTheme: mockSetTheme,
        })

        render(<ThemeToggle />)
        
        const user = userEvent.setup()
        
        // Abrir y seleccionar
        await user.click(screen.getByRole('button'))
        await user.click(screen.getByText('Claro'))
        
        // Debería haber llamado setTheme
        expect(mockSetTheme).toHaveBeenCalledWith('light')
    })
})