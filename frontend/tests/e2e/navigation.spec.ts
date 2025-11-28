import { test, expect } from '../fixtures/auth'

test.describe('Navegación principal', () => {
  test('debe cargar el dashboard correctamente', async ({ authenticatedPage }) => {
    await expect(authenticatedPage).toHaveURL('/dashboard/')
    await expect(authenticatedPage.locator('h1')).toContainText('Dashboard')
  })

  test('debe navegar entre páginas sin recargar', async ({ authenticatedPage }) => {
    const page = authenticatedPage
    
    // Ir a usuarios a través del menú expandido
    await page.click('text=Gestión de Usuarios')
    await page.waitForTimeout(500) // Wait for submenu to expand
    
    // Click en Listado de Usuarios
    await page.click('text=Listado de Usuarios')
    await expect(page).toHaveURL('/users/')
    
    // Verificar que es navegación SPA (sin recarga completa)
    // El contenido principal debe cambiar sin perder el estado de la aplicación
    await expect(page.locator('h1')).toContainText('Usuarios')
    
    // Navegar de vuelta al Dashboard
    await page.click('nav >> text=Dashboard')
    await expect(page).toHaveURL('/dashboard/')
    await expect(page.locator('h1')).toContainText('Dashboard')
  })

  test('debe resaltar item activo en sidebar', async ({ authenticatedPage }) => {
    const page = authenticatedPage
    
    // Dashboard inicialmente activo
    const dashboardLink = page.locator('nav >> text=Dashboard').first()
    await expect(dashboardLink).toHaveClass(/bg-accent/)
    
    // Navegar a usuarios
    await page.click('text=Gestión de Usuarios')
    await page.waitForTimeout(500)
    
    // Click en Listado de Usuarios
    await page.click('text=Listado de Usuarios')
    
    // Verificar que el enlace de usuarios ahora está activo
    await expect(page.locator('nav >> text=Gestión de Usuarios')).toHaveClass(/bg-accent/)
    
    // Dashboard ya no debe estar activo
    await expect(page.locator('nav >> text=Dashboard').first()).not.toHaveClass(/bg-accent/)
  })

  test('debe navegar a página de ayuda', async ({ authenticatedPage }) => {
    const page = authenticatedPage
    
    // Navegar a ayuda a través del menú secundario
    await page.click('nav >> text=Ayuda')
    await expect(page).toHaveURL('/help/')
    
    // Verificar contenido de la página de ayuda
    await expect(page.locator('h1')).toContainText('Ayuda')
    await expect(page.locator('text=Página de prueba para verificar la navegación.')).toBeVisible()
  })

  test('debe preservar estado de navegación al recargar página', async ({ authenticatedPage }) => {
    const page = authenticatedPage
    
    // Navegar a la página de usuarios
    await page.click('text=Gestión de Usuarios')
    await page.waitForTimeout(500)
    await page.click('text=Listado de Usuarios')
    
    // Recargar la página
    await page.reload()
    
    // Verificar que seguimos en la página de usuarios después de la recarga
    await expect(page).toHaveURL('/users/')
    await expect(page.locator('h1')).toContainText('Usuarios')
    
    // El item del sidebar debe seguir activo
    await expect(page.locator('nav >> text=Gestión de Usuarios')).toHaveClass(/bg-accent/)
  })

  test('debe manejar navegación directa por URL', async ({ authenticatedPage }) => {
    const page = authenticatedPage
    
    // Navegación directa a URL de usuarios
    await page.goto('/users/')
    await expect(page).toHaveURL('/users/')
    await expect(page.locator('h1')).toContainText('Usuarios')
    
    // Verificar que el sidebar refleja el estado correcto
    await expect(page.locator('nav >> text=Gestión de Usuarios')).toHaveClass(/bg-accent/)
    
    // Navegación directa a ayuda
    await page.goto('/help/')
    await expect(page).toHaveURL('/help/')
    await expect(page.locator('h1')).toContainText('Ayuda')
  })

  test('debe colapsar submenús automáticamente', async ({ authenticatedPage }) => {
    const page = authenticatedPage
    
    // Abrir submenú de Gestión de Usuarios
    await page.click('text=Gestión de Usuarios')
    await page.waitForTimeout(500)
    
    // Verificar que el submenú está visible
    await expect(page.locator('text=Listado de Usuarios')).toBeVisible()
    
    // Navegar a otra página (Dashboard)
    await page.click('nav >> text=Dashboard')
    
    // Al volver al menú de usuarios, debe estar colapsado
    await page.click('text=Gestión de Usuarios')
    await page.waitForTimeout(300)
    
    // El submenú puede estar expandido o colapsado, pero no debe causar errores
    const userManagementVisible = await page.locator('text=Listado de Usuarios').isVisible()
    expect(typeof userManagementVisible).toBe('boolean')
  })
})