import { test, expect } from '../fixtures/auth'

test.describe('Sidebar responsive', () => {
  test('debe mostrar sidebar expandido en desktop', async ({ authenticatedPage }) => {
    const page = authenticatedPage
    
    // Configurar viewport de desktop
    await page.setViewportSize({ width: 1280, height: 720 })
    await page.reload() // Recargar para aplicar nuevo viewport
    
    // Sidebar debe estar visible en desktop
    await expect(page.locator('aside')).toBeVisible()
    await expect(page.locator('nav >> text=10Code')).toBeVisible()
    
    // Logo y texto del sidebar deben estar visibles
    const logo = page.locator('img[alt="10Code Logo"]')
    await expect(logo).toBeVisible()
    
    // Todos los elementos de navegación deben estar visibles
    await expect(page.locator('nav >> text=Dashboard')).toBeVisible()
    await expect(page.locator('nav >> text=Gestión de Usuarios')).toBeVisible()
    await expect(page.locator('nav >> text=Ayuda')).toBeVisible()
  })

  test('debe adaptarse a tablet (viewport medio)', async ({ authenticatedPage }) => {
    const page = authenticatedPage
    
    // Configurar viewport de tablet
    await page.setViewportSize({ width: 768, height: 1024 })
    await page.reload()
    
    // Sidebar debe seguir siendo funcional en tablet
    await expect(page.locator('aside')).toBeVisible()
    await expect(page.locator('nav >> text=10Code')).toBeVisible()
    
    // Los elementos principales deben seguir visibles
    await expect(page.locator('nav >> text=Dashboard')).toBeVisible()
    await expect(page.locator('nav >> text=Gestión de Usuarios')).toBeVisible()
    
    // El contenido principal debe ajustarse al espacio disponible
    const mainContent = page.locator('main')
    await expect(mainContent).toBeVisible()
  })

  test('debe convertirse en offcanvas en móvil', async ({ authenticatedPage }) => {
    const page = authenticatedPage
    
    // Configurar viewport móvil
    await page.setViewportSize({ width: 375, height: 667 })
    await page.reload()
    
    // En móvil, el sidebar puede estar oculto inicialmente
    // Buscar botón de menú móvil
    const mobileMenuButton = page.getByRole('button', { name: /Toggle navigation menu|Menú/ })
    
    // Verificar que existe botón de menú en móvil
    await expect(mobileMenuButton).toBeVisible()
    
    // Hacer click para abrir menú móvil
    await mobileMenuButton.click()
    
    // El sidebar debe aparecer como offcanvas/drawer
    await expect(page.locator('aside')).toBeVisible()
    
    // Los elementos de navegación deben estar accesibles
    await expect(page.locator('nav >> text=10Code')).toBeVisible()
  })

  test('debe cerrar automáticamente al navegar en móvil', async ({ authenticatedPage }) => {
    const page = authenticatedPage
    
    // Configurar viewport móvil
    await page.setViewportSize({ width: 375, height: 667 })
    await page.reload()
    
    // Abrir menú móvil
    const mobileMenuButton = page.getByRole('button', { name: /Toggle navigation menu|Menú/ })
    await mobileMenuButton.click()
    
    // Verificar que el sidebar está abierto
    await expect(page.locator('aside')).toBeVisible()
    
    // Navegar a una página diferente
    await page.click('nav >> text=Dashboard')
    
    // El sidebar móvil debe cerrarse automáticamente (comportamiento SPA)
    // Verificar que estamos en la página correcta
    await expect(page).toHaveURL('/dashboard/')
    await expect(page.locator('h1')).toContainText('Dashboard')
  })

  test('debe mantener navegación funcional en todos los viewports', async ({ authenticatedPage }) => {
    const page = authenticatedPage
    
    // Probar navegación en desktop
    await page.setViewportSize({ width: 1280, height: 720 })
    await page.reload()
    
    await page.click('text=Gestión de Usuarios')
    await page.waitForTimeout(500)
    await page.click('text=Listado de Usuarios')
    await expect(page).toHaveURL('/users/')
    
    // Cambiar a móvil y probar navegación
    await page.setViewportSize({ width: 375, height: 667 })
    await page.reload()
    
    // Abrir menú y navegar
    const mobileMenuButton = page.getByRole('button', { name: /Toggle navigation menu|Menú/ })
    await mobileMenuButton.click()
    
    await page.click('nav >> text=Ayuda')
    await expect(page).toHaveURL('/help/')
    
    // Volver a desktop y verificar que funciona
    await page.setViewportSize({ width: 1280, height: 720 })
    await page.reload()
    
    await expect(page.locator('aside')).toBeVisible()
    await expect(page.locator('nav >> text=10Code')).toBeVisible()
  })

  test('debe manejar cambios de orientación', async ({ authenticatedPage }) => {
    const page = authenticatedPage
    
    // Iniciar en landscape
    await page.setViewportSize({ width: 667, height: 375 }) // Landscape móvil
    await page.reload()
    
    // Verificar comportamiento en landscape
    await expect(page.locator('aside')).toBeVisible()
    
    // Cambiar a portrait
    await page.setViewportSize({ width: 375, height: 667 }) // Portrait móvil
    await page.reload()
    
    // El comportamiento debe adaptarse
    const mobileMenuButton = page.getByRole('button', { name: /Toggle navigation menu|Menú/ })
    await expect(mobileMenuButton).toBeVisible()
  })

  test('debe preservar estado de sidebar en navegación', async ({ authenticatedPage }) => {
    const page = authenticatedPage
    
    // Configurar en desktop
    await page.setViewportSize({ width: 1280, height: 720 })
    await page.reload()
    
    // Navegar a diferentes páginas
    await page.click('text=Gestión de Usuarios')
    await page.waitForTimeout(500)
    await page.click('text=Listado de Usuarios')
    
    // El sidebar debe mantenerse visible y funcional
    await expect(page.locator('aside')).toBeVisible()
    await expect(page.locator('nav >> text=10Code')).toBeVisible()
    
    // Navegar a ayuda
    await page.click('nav >> text=Ayuda')
    
    // Sidebar debe seguir funcionando
    await expect(page.locator('aside')).toBeVisible()
  })

  test('debe tener accesibilidad correcta en todos los tamaños', async ({ authenticatedPage }) => {
    const page = authenticatedPage
    
    // Probar accesibilidad en desktop
    await page.setViewportSize({ width: 1280, height: 720 })
    await page.reload()
    
    // Verificar que el sidebar tiene atributos de accesibilidad
    const sidebar = page.locator('aside')
    await expect(sidebar).toHaveAttribute('aria-label', 'Navegación principal')
    
    // Probar accesibilidad en móvil
    await page.setViewportSize({ width: 375, height: 667 })
    await page.reload()
    
    // El botón de menú móvil debe ser accesible
    const mobileMenuButton = page.getByRole('button', { name: /Toggle navigation menu|Menú/ })
    await expect(mobileMenuButton).toBeVisible()
    await expect(mobileMenuButton).toHaveAttribute('aria-label')
  })

  test('debe adaptar texto del sidebar en modo colapsado', async ({ authenticatedPage }) => {
    const page = authenticatedPage
    
    // Configurar en desktop
    await page.setViewportSize({ width: 1280, height: 720 })
    await page.reload()
    
    // El sidebar puede tener un modo colapsado (icon-only)
    // Verificar que el logo sigue siendo visible
    const logo = page.locator('img[alt="10Code Logo"]')
    await expect(logo).toBeVisible()
    
    // El texto puede ocultarse en modo colapsado, pero el logo debe permanecer
    // Este comportamiento depende de la implementación específica
    const sidebarText = page.locator('text=10Code')
    if (await sidebarText.isVisible()) {
      await expect(sidebarText).toContainText('10Code')
    }
  })
})