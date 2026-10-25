import { defineConfig } from 'astro/config';
import cloudflare from '@astrojs/cloudflare';
import tailwindcss from '@tailwindcss/vite';
import r2Preview from './scripts/r2-preview.mjs';

export default defineConfig({
  integrations: [r2Preview()],
  vite: {
    plugins: [tailwindcss()],
  },
  adapter: cloudflare(),
  output: 'static',
});
