import { defineConfig } from 'vite';
import preact from '@preact/preset-vite';

export default defineConfig({
  root: '/app/web',
  plugins: [preact()],
  base: '/',
  build: {
    outDir: 'dist',
    emptyOutDir: true,
    sourcemap: false,
    assetsInlineLimit: 0,
  },
  server: { port: 5173, proxy: { '/api': 'http://localhost:4173' } },
});
