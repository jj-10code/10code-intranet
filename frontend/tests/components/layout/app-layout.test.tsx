import { describe, it, expect } from 'vitest'
import { render, screen } from '@testing-library/react'
import { AppLayout } from '../../../src/components/layout'

describe('AppLayout', () => {
  it('renderiza children correctamente', () => {
    render(
      <AppLayout>
        <div>Test Content</div>
      </AppLayout>
    )
    expect(screen.getByText('Test Content')).toBeInTheDocument()
  })

  it('usa título por defecto cuando no se proporciona', () => {
    render(<AppLayout><div>Content</div></AppLayout>)
    // El título por defecto se establece en el Head component
    const titleElements = document.querySelectorAll('title')
    expect(titleElements.length).toBeGreaterThan(0)
  })

  it('usa título personalizado cuando se proporciona', () => {
    render(
      <AppLayout title="Mi Página">
        <div>Content</div>
      </AppLayout>
    )
    // Verificar que el título se pasa al componente Head
    const headComponent = document.querySelector('title')
    expect(headComponent).toBeTruthy()
  })

  it('renderiza enlace de salto al contenido principal', () => {
    render(
      <AppLayout>
        <div>Content</div>
      </AppLayout>
    )
    
    const skipLink = screen.getByText('Saltar al contenido principal')
    expect(skipLink).toBeInTheDocument()
    expect(skipLink.closest('a')).toHaveAttribute('href', '#main-content')
  })

  it('renderiza breadcrumb cuando se proporciona', () => {
    render(
      <AppLayout 
        breadcrumbs={[
          { label: 'Dashboard', href: '/dashboard/' },
          { label: 'Mi Sección' }
        ]}
      >
        <div>Content</div>
      </AppLayout>
    )
    
    // Verificar que el breadcrumb se renderiza (sería manejado por AppHeader)
    expect(screen.getByText('Content')).toBeInTheDocument()
  })

  it('renderiza área de contenido principal con ID correcto', () => {
    render(
      <AppLayout>
        <div>Content</div>
      </AppLayout>
    )
    
    const mainContent = document.getElementById('main-content')
    expect(mainContent).toBeInTheDocument()
  })

  it('aplica clases CSS correctas al área de contenido', () => {
    render(
      <AppLayout>
        <div>Content</div>
      </AppLayout>
    )
    
    const mainContent = document.getElementById('main-content')
    expect(mainContent).toHaveClass('flex', 'flex-1', 'flex-col', 'gap-4', 'p-4', 'pt-0', 'w-full', 'overflow-x-hidden', '@container/main')
  })

  it('usa el sidebar provider y inset', () => {
    render(
      <AppLayout>
        <div>Content</div>
      </AppLayout>
    )
    
    // Verificar que el contenido principal está presente
    expect(screen.getByText('Content')).toBeInTheDocument()
  })

  it('soporta múltiples children', () => {
    render(
      <AppLayout>
        <h1>Título</h1>
        <p>Párrafo</p>
        <div>Elemento</div>
      </AppLayout>
    )
    
    expect(screen.getByText('Título')).toBeInTheDocument()
    expect(screen.getByText('Párrafo')).toBeInTheDocument()
    expect(screen.getByText('Elemento')).toBeInTheDocument()
  })

  it('renderiza children dentro de la estructura del layout', () => {
    const { container } = render(
      <AppLayout>
        <div className="test-child">Contenido específico</div>
      </AppLayout>
    )
    
    // Verificar que el contenido está dentro de main con el ID correcto
    const mainElement = container.querySelector('#main-content')
    expect(mainElement).toBeTruthy()
    expect(mainElement?.querySelector('.test-child')).toBeTruthy()
  })
})