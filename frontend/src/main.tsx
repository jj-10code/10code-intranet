import { createInertiaApp } from '@inertiajs/react'
import { createRoot } from 'react-dom/client'
import './styles/globals.css'

// Axios (usado por Inertia) detecta automáticamente la cookie XSRF-TOKEN
// y la envía en el header X-XSRF-Token. Django está configurado para aceptarlo.

createInertiaApp({
  resolve: name => {
    const pages = import.meta.glob('./Pages/**/*.tsx', { eager: true })
    return pages[`./Pages/${name}.tsx`]
  },
  setup({ el, App, props }) {
    createRoot(el).render(<App {...props} />)
  },
})
