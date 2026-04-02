import { defineConfig } from 'vite'
import { svelte } from '@sveltejs/vite-plugin-svelte'

export default defineConfig({
  base: '/portfolio-website/',
  plugins: [svelte()],
  build: {
    target: 'esnext',
    minify: 'terser',
  },
  server: {
    port: 5173,
  }
})
