import { defineConfig } from 'astro/config';

export default defineConfig({
  site: 'https://kiss.i-pp.co.jp',
  output: 'static',
  trailingSlash: 'always',
  devToolbar: { enabled: false },
});
