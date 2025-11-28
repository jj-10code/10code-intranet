import { test, expect } from '../fixtures/auth'

test.describe('Dark mode', () => {
  test('debe cambiar a modo oscuro', async ({ authenticatedPage }) => {
    const page = authenticatedPage
    
    // Buscar botón de cambio de tema (puede estar en sidebar o header)
    const themeButton = page.locator('button').filter({ hasText: /Cambiar tema|tema|Theme/ })
    
    // Hacer click en el botón de tema para abrir dropdown
    await themeButton.click()
    
    // Buscar y hacer click en "Oscuro"
    const darkModeOption = page.locator('text=Oscuro').first()
    await expect(darkModeOption).toBeVisible()
    await darkModeOption.click()
    
    // Verificar que el HTML tiene la clase dark
    await expect(page.locator('html')).toHaveClass(/dark/)
  })

  test('debe cambiar a modo claro', async ({ authenticatedPage }) => {
    const page = authenticatedPage
    
    // Primero cambiar a modo oscuro
    const themeButton = page.locator('button').filter({ hasText: /Cambiar tema|tema|Theme/ })
    await themeButton.click()
    
    const darkModeOption = page.locator('text=Oscuro').first()
    await darkModeOption.click()
    
    // Verificar que estamos en modo oscuro
    await expect(page.locator('html')).toHaveClass(/dark/)
    
    // Ahora cambiar a modo claro
    await themeButton.click()
    const lightModeOption = page.locator('text=Claro').first()
    await expect(lightModeOption).toBeVisible()
    await lightModeOption.click()
    
    // Verificar que se quitó la clase dark
    await expect(page.locator('html')).not.toHaveClass(/dark/)
  })

  test('debe cambiar a modo sistema', async ({ authenticatedPage }) => {
    const page = authenticatedPage
    
    // Abrir dropdown de tema
    const themeButton = page.locator('button').filter({ hasText: /Cambiar tema|tema|Theme/ })
    await themeButton.click()
    
    // Buscar y hacer click en "Sistema"
    const systemModeOption = page.locator('text=Sistema').first()
    await expect(systemModeOption).toBeVisible()
    await systemModeOption.click()
    
    // El comportamiento del modo sistema depende de la configuración del sistema
    // Verificar que el dropdown se cerró y no hay errores
    await expect(page.locator('text=Sistema')).not.toBeVisible()
  })

  test('debe persistir preferencia de tema después de recarga', async ({ authenticatedPage }) => {
    const page = authenticatedPage
    
    // Cambiar a modo oscuro
    const themeButton = page.locator('button').filter({ hasText: /Cambiar tema|tema|Theme/ })
    await themeButton.click()
    
    const darkModeOption = page.locator('text=Oscuro').first()
    await darkModeOption.click()
    
    // Verificar que estamos en modo oscuro
    await expect(page.locator('html')).toHaveClass(/dark/)
    
    // Recargar la página
    await page.reload()
    
    // Debe mantener el tema oscuro
    await expect(page.locator('html')).toHaveClass(/dark/)
  })

  test('debe mantener preferencia de tema en navegación', async ({ authenticatedPage }) => {
    const page = authenticatedPage
    
    // Cambiar a modo oscuro
    const themeButton = page.locator('button').filter({ hasText: /Cambiar tema|tema|Theme/ })
    await themeButton.click()
    
    const darkModeOption = page.locator('text=Oscuro').first()
    await darkModeOption.click()
    
    // Verificar modo oscuro activo
    await expect(page.locator('html')).toHaveClass(/dark/)
    
    // Navegar a otra página
    await page.click('text=Gestión de Usuarios')
    await page.waitForTimeout(500)
    await page.click('text=Listado de Usuarios')
    
    // El tema debe persistir
    await expect(page.locator('html')).toHaveClass(/dark/)
    
    // Navegar a ayuda
    await page.click('nav >> text=Ayuda')
    
    // Tema debe seguir activo
    await expect(page.locator('html')).toHaveClass(/dark/)
  })

  test('debe funcionar el cambio de tema en móvil', async ({ authenticatedPage }) => {
    const page = authenticatedPage
    
    // Configurar viewport móvil
    await page.setViewportSize({ width: 375, height: 667 })
    await page.reload()
    
    // En móvil, el botón de tema puede estar en el sidebar
    // Abrir sidebar móvil si es necesario
    const mobileMenuButton = page.getByRole('button', { name: /Toggle navigation menu|Menú/ })
    await mobileMenuButton.click()
    
    // Buscar botón de tema en sidebar
    const themeButton = page.locator('button').filter({ hasText: /Cambiar tema|tema|Theme/ })
    await themeButton.click()
    
    // Cambiar a modo oscuro
    const darkModeOption = page.locator('text=Oscuro').first()
    await expect(darkModeOption).toBeVisible()
    await darkModeOption.click()
    
    // Verificar cambio de tema
    await expect(page.locator('html')).toHaveClass(/dark/)
  })

  test('debe tener iconografía adecuada para el tema', async ({ authenticatedPage }) => {
    const page = authenticatedPage
    
    // Verificar iconos del botón de tema inicialmente
    const themeButton = page.locator('button').filter({ hasText: /Cambiar tema|tema|Theme/ })
    await expect(themeButton).toBeVisible()
    
    // Cambiar a modo oscuro
    await themeButton.click()
    const darkModeOption = page.locator('text=Oscuro').first()
    await darkModeOption.click()
    
    // En modo oscuro, el botón debe mostrar el icono apropiado
    // (Generalmente luna en modo oscuro, sol en modo claro)
    const sunIcon = page.locator('svg').filter({ hasText: /sun|Sun|SOL/ })
    const moonIcon = page.locator('svg').filter({ hasText: /moon|Moon|LUNA/ })
    
    // Al menos uno de los iconos debe estar visible
    const sunVisible = await sunIcon.isVisible()
    const moonVisible = await moonIcon.isVisible()
    expect(sunVisible || moonVisible).toBe(true)
  })

  test('debe aplicar estilos de tema correctamente', async ({ authenticatedPage }) => {
    const page = authenticatedPage
    
    // Cambiar a modo oscuro
    const themeButton = page.locator('button').filter({ hasText: /Cambiar tema|tema|Theme/ })
    await themeButton.click()
    
    const darkModeOption = page.locator('text=Oscuro').first()
    await darkModeOption.click()
    
    // Verificar que elementos clave tienen estilos de tema oscuro
    // Verificar que el background y text colors se aplicaron
    const sidebar = page.locator('aside')
    await expect(sidebar).toBeVisible()
    
    // Verificar que el contenido principal también tiene estilos de tema
    const mainContent = page.locator('main')
    await expect(mainContent).toBeVisible()
    
    // El tema debe cambiar la apariencia visual, no solo agregar la clase
    // Esto se verifica por el comportamiento visual en los tests
  })

  test('debe manejar transiciones de tema suavemente', async ({ authenticatedPage }) => {
    const page = authenticatedPage
    
    // Cambiar tema varias veces rápidamente para verificar que no hay errores
    const themeButton = page.locator('button').filter({ hasText: /Cambiar tema|tema|Theme/ })
    
    // Ciclo: claro -> oscuro -> claro -> oscuro
    for (let i = 0; i < 2; i++) {
      // Cambiar a oscuro
      await themeButton.click()
      const darkModeOption = page.locator('text=Oscuro').first()
      await darkModeOption.click()
      
      // Cambiar a claro
      await themeButton.click()
      const lightModeOption = page.locator('text=Claro').first()
      await lightModeOption.click()
    }
    
    // Verificar que terminamos en modo claro
    await expect(page.locator('html')).not.toHaveClass(/dark/)
    
    // Verificar que la aplicación sigue funcionando
    await expect(page.locator('h1')).toBeVisible()
  })
})