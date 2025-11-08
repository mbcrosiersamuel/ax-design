import { defineConfig } from 'astro/config';
import netlify from '@astrojs/netlify';
import sitemap from '@astrojs/sitemap';

export default defineConfig({
  site: 'https://agentexperience.design',
  output: 'hybrid',
  adapter: netlify({
    imageCDN: false,
    edgeMiddleware: false,
  }),
  integrations: [sitemap()],
  markdown: {
    shikiConfig: {
      theme: 'github-light',
    },
  },
  vite: {
    build: {
      assetsInlineLimit: 0,
    },
  },
});
