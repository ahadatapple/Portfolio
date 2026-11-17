import { defineConfig } from 'astro/config';
import mdx from '@astrojs/mdx';
import sitemap from '@astrojs/sitemap';

// The public URL of the site. Social previews need it for absolute image URLs,
// and it drives canonical links and the sitemap. Override with SITE_URL only
// if the site moves.
const site = process.env.SITE_URL || 'https://ahadatapple.dev';

export default defineConfig({
  site,
  output: 'static',
  trailingSlash: 'never',
  build: { format: 'file', inlineStylesheets: 'always' },
  integrations: [mdx(), ...(site ? [sitemap()] : [])],
  markdown: {
    shikiConfig: { themes: { light: 'github-light', dark: 'github-dark' } },
  },
  prefetch: false,
});
