import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import { VitePWA } from 'vite-plugin-pwa'

export default defineConfig({
  base: './',
  plugins: [
    react(),
    VitePWA({
      registerType: 'autoUpdate',
      includeAssets: ['icons/icon-192.png', 'icons/icon-512.png'],
      manifest: {
        name: 'Fomi Stock',
        short_name: 'FomiStock',
        description: 'Gestion des stocks d’engrais FOMI',
        theme_color: '#15803d',
        background_color: '#f4f7f5',
        display: 'standalone',
        start_url: './',
        lang: 'fr',
        icons: [
          { src: 'icons/icon-192.png', sizes: '192x192', type: 'image/png' },
          { src: 'icons/icon-512.png', sizes: '512x512', type: 'image/png' }
        ]
      },
      workbox: {
        globPatterns: ['**/*.{js,css,html,svg,png,ico,webmanifest}'],
        navigateFallbackDenylist: [/^\/api/]
      }
    })
  ],
  server: {
    proxy: {
      '/api': 'https://fomi-stock-api-production.up.railway.app'
    }
  }
})
