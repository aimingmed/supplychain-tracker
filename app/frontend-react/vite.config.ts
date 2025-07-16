import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import path from 'path'

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, 'src'),
    },
  },
  server: {
    host: true,
    strictPort: true,
    port: 80,
    allowedHosts: ["frontend-sctracker", "staging-sctracker.aimingmed.local", "localhost"],
    hmr: {
      clientPort: 443
    }
  },
})
