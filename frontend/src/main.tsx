import { createInertiaApp } from '@inertiajs/react'
import { createRoot } from 'react-dom/client'
import '@fontsource/geist-sans/index.css'
import '@fontsource/geist-mono/index.css'
import '@fontsource/space-grotesk/index.css'
import './styles/globals.css'

// Axios (usado por Inertia) detecta automáticamente la cookie XSRF-TOKEN
// y la envía en el header X-XSRF-Token. Django está configurado para aceptarlo.

createInertiaApp({
  id: 'app',
  progress: {
    color: '#4B5563',
  },
  resolve: name => {
    console.log('Resolving component:', name)
    const pages = import.meta.glob('./pages/**/*.tsx', { eager: true })
    const parts = name.split('/')
    const path = parts.map((part, index) =>
      index === parts.length - 1 ? part : part.toLowerCase()
    ).join('/')
    const fullPath = `./pages/${path}.tsx`
    console.log('Looking for:', fullPath)
    const module = pages[fullPath]
    console.log('Found module:', !!module)
    return module
  },
  setup({ el, App, props }) {
    createRoot(el).render(<App {...props} />)
  },
})
