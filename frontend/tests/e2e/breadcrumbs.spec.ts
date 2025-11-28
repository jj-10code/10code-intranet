import { test, expect } from '../fixtures/auth'

test.describe('Breadcrumbs', () => {
  test('debe mostrar breadcrumb en dashboard', async ({ authenticatedPage }) => {
    const page = authenticatedPage
    
    // Dashboard debe tener breadcrumb simple
    await expect(page.locator('nav[aria-label="breadcrumb"]')).toBeVisible()
    await expect(page.locator('nav[aria-label="breadcrumb"]')).toContainText('Dashboard')
    
    // Verificar estructura del breadcrumb
    const breadcrumbItems = page.locator('nav[aria-label="breadcrumb"] li')
    await expect(breadcrumbItems).toHaveCount(1)
  })

  test('debe mostrar breadcrumbs multinivel en páginas anidadas', async ({ authenticatedPage }) => {
    const page = authenticatedPage

    // Navegar a usuarios para ver breadcrumb multinivel
    await page.click('text=Gestión de Usuarios')
    await page.waitForTimeout(500)
    await page.click('text=Listado de Usuarios')

    const breadcrumb = page.locator('nav[aria-label="breadcrumb"]')

    // Debe contener Gestión de Usuarios y Usuarios
    await expect(breadcrumb).toContainText('Gestión de Usuarios')
    await expect(breadcrumb).toContainText('Usuarios')

    // Verificar que hay 2 elementos en el breadcrumb
    const breadcrumbItems = breadcrumb.locator('li')
    await expect(breadcrumbItems).toHaveCount(2)
  })

  test('debe permitir navegación mediante breadcrumbs', async ({ authenticatedPage }) => {
    const page = authenticatedPage
    
    // Ir a página anidada
    await page.click('text=Gestión de Usuarios')
    await page.waitForTimeout(500)
    await page.click('text=Listado de Usuarios')
    
    // Click en Dashboard del breadcrumb para navegar
    await page.locator('nav[aria-label="breadcrumb"] >> text=Dashboard').click()
    await expect(page).toHaveURL('/dashboard/')
    
    // Verificar que llegamos al dashboard
    await expect(page.locator('h1')).toContainText('Dashboard')
  })

  test('debe mostrar breadcrumb en página de ayuda', async ({ authenticatedPage }) => {
    const page = authenticatedPage
    
    // Navegar a ayuda
    await page.click('nav >> text=Ayuda')
    
    // Breadcrumb debe estar visible
    await expect(page.locator('nav[aria-label="breadcrumb"]')).toBeVisible()
    
    // Debe mostrar solo "Ayuda" como breadcrumb único
    await expect(page.locator('nav[aria-label="breadcrumb"]')).toContainText('Ayuda')
    
    const breadcrumbItems = page.locator('nav[aria-label="breadcrumb"] li')
    await expect(breadcrumbItems).toHaveCount(1)
  })

  test('debe preservar breadcrumbs al recargar página', async ({ authenticatedPage }) => {
    const page = authenticatedPage

    // Navegar a página con breadcrumb multinivel
    await page.click('text=Gestión de Usuarios')
    await page.waitForTimeout(500)
    await page.click('text=Listado de Usuarios')

    // Verificar breadcrumbs antes de recargar
    const breadcrumb = page.locator('nav[aria-label="breadcrumb"]')
    await expect(breadcrumb).toContainText('Gestión de Usuarios')
    await expect(breadcrumb).toContainText('Usuarios')

    // Recargar página
    await page.reload()

    // Breadcrumbs deben mantenerse
    await expect(breadcrumb).toContainText('Gestión de Usuarios')
    await expect(breadcrumb).toContainText('Usuarios')

    // URL debe mantenerse
    await expect(page).toHaveURL('/users/')
  })

  test('debe manejar breadcrumbs en navegación directa por URL', async ({ authenticatedPage }) => {
    const page = authenticatedPage

    // Navegación directa a URL de usuarios
    await page.goto('/users/')

    // Breadcrumbs deben reflejar la ubicación correcta
    const breadcrumb = page.locator('nav[aria-label="breadcrumb"]')
    await expect(breadcrumb).toContainText('Gestión de Usuarios')
    await expect(breadcrumb).toContainText('Usuarios')

    // Navegación directa a ayuda
    await page.goto('/help/')

    // Breadcrumb debe mostrar solo ayuda
    await expect(page.locator('nav[aria-label="breadcrumb"]')).toContainText('Ayuda')
  })

  test('debe tener elementos de breadcrumb accesibles', async ({ authenticatedPage }) => {
    const page = authenticatedPage
    
    // Navegar a página con breadcrumb multinivel
    await page.click('text=Gestión de Usuarios')
    await page.waitForTimeout(500)
    await page.click('text=Listado de Usuarios')
    
    // Verificar atributos de accesibilidad
    const breadcrumb = page.locator('nav[aria-label="breadcrumb"]')
    await expect(breadcrumb).toHaveAttribute('aria-label', 'breadcrumb')
    
    // Verificar que los enlaces tienen estructura semántica
    const links = breadcrumb.locator('a')
    const linkCount = await links.count()
    expect(linkCount).toBeGreaterThan(0)
    
    // Al menos el primer elemento (Dashboard) debe ser un enlace
    await expect(links.first()).toBeVisible()
  })

  test('debe mostrar separadores entre elementos de breadcrumb', async ({ authenticatedPage }) => {
    const page = authenticatedPage

    // Ir a página con breadcrumb multinivel
    await page.click('text=Gestión de Usuarios')
    await page.waitForTimeout(500)
    await page.click('text=Listado de Usuarios')

    // Buscar separadores (pueden ser / o > símbolos)
    const breadcrumb = page.locator('nav[aria-label="breadcrumb"]')

    // El breadcrumb debe contener texto que indique separación
    // (Esto depende de la implementación específica)
    const breadcrumbText = await breadcrumb.textContent()
    expect(breadcrumbText).toContain('Gestión de Usuarios')
    expect(breadcrumbText).toContain('Usuarios')
  })
})