import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import tailwindcss from "@tailwindcss/vite"
import path from 'path'

// https://vite.dev/config/
export default defineConfig({
  plugins: [react(), tailwindcss()],

  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
    },
  },

  // Configuración para django-vite
  base: '/static/',

  build: {
    // Output a la carpeta que Django espera
    outDir: 'dist',
    emptyOutDir: true,

    // Generar manifest para django-vite
    manifest: true,

    rollupOptions: {
      input: {
        main: path.resolve(__dirname, 'src/main.tsx'),
      },
    },
  },

  server: {
    host: '0.0.0.0',
    port: 5173,
    strictPort: true,

    // CORS configuration for Django integration
    cors: { origin: '*' },

    // HMR configuration para Docker
    hmr: {
      clientPort: 5173,
    },
    origin: 'http://localhost:5173',

    // Watch configuration
    watch: {
      usePolling: true,
    },
  },
})
