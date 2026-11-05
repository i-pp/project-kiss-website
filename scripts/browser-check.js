// Playwright CLI run-code function. Run against the local static preview only.
// Selectors follow the inspected homepage and document accessibility snapshots.
async (page) => {
  const base = new URL(page.url()).origin;
  if (!['127.0.0.1', 'localhost'].includes(new URL(base).hostname)) {
    throw new Error('Browser checks require an explicitly local preview.');
  }
  const slugs = ['', 'philosophy/', 'products/', 'products/aceis/', 'roadmap/', 'docs/', 'contributing/'];
  const paths = ['', 'ja/'].flatMap(prefix => slugs.map(slug => `/${prefix}${slug}`)).concat('/404.html');
  const failures = [];
  const consoleErrors = [];
  const networkFailures = [];
  const navigationCancellations = [];
  const requests = new Set();
  page.on('pageerror', error => consoleErrors.push(error.message));
  page.on('requestfailed', request => {
    // A favicon fetch can be cancelled by the following navigation. Loaded
    // content images are independently checked with decode() on every route.
    if (request.failure()?.errorText === 'net::ERR_ABORTED') navigationCancellations.push(request.url());
    else networkFailures.push(request.url());
  });
  page.on('request', request => requests.add(request.url()));
  let layoutCases = 0;
  let accessibilityCases = 0;
  let languageCases = 0;
  let keyboardCases = 0;

  for (const path of paths) {
    const response = await page.goto(base + path);
    if (!response || response.status() !== 200) failures.push(`${path}: HTTP ${response?.status()}`);
    await page.evaluate(async () => {
      await document.fonts.ready;
      await Promise.all([...document.images].map(image => image.decode().catch(() => {})));
    });
    for (const width of [320, 390, 768, 1280, 1536]) {
      await page.setViewportSize({ width, height: 900 });
      for (const scale of [1, 2]) {
        await page.evaluate(scale => { document.documentElement.style.fontSize = `${scale * 100}%`; }, scale);
        const issues = await page.evaluate(() => {
          const errors = [];
          const visible = element => !!(element.getClientRects().length && getComputedStyle(element).visibility !== 'hidden');
          if (document.documentElement.scrollWidth > innerWidth + 1) errors.push('horizontal overflow');
          const header = document.querySelector('.site-header');
          const headerLinks = [...header.querySelectorAll('a')].filter(visible);
          for (let i = 0; i < headerLinks.length; i++) {
            const a = headerLinks[i].getBoundingClientRect();
            if (a.left < -1 || a.right > innerWidth + 1) errors.push('header link outside viewport');
            for (let j = i + 1; j < headerLinks.length; j++) {
              const b = headerLinks[j].getBoundingClientRect();
              if (Math.min(a.right, b.right) - Math.max(a.left, b.left) > 1 && Math.min(a.bottom, b.bottom) - Math.max(a.top, b.top) > 1) errors.push('overlapping header links');
            }
          }
          for (const image of document.images) {
            if (!image.complete || image.naturalWidth === 0) errors.push('image not loaded');
            if (getComputedStyle(image).objectFit !== 'contain' && Math.abs(image.width / image.height - image.naturalWidth / image.naturalHeight) > .02) errors.push('distorted logo');
          }
          if (getComputedStyle(document.body).backgroundColor !== 'rgba(0, 0, 0, 0)' && getComputedStyle(document.body).backgroundColor !== 'rgb(255, 255, 255)') errors.push('unexpected body background');
          return [...new Set(errors)];
        });
        layoutCases++;
        failures.push(...issues.map(issue => `${path} @ ${width}px / ${scale * 100}%: ${issue}`));
      }
      await page.evaluate(() => { document.documentElement.style.fontSize = ''; });
      if ([390, 1280].includes(width)) {
        await page.addScriptTag({ path: 'node_modules/axe-core/axe.min.js' });
        const violations = await page.evaluate(async () => {
          const result = await axe.run(document, { runOnly: { type: 'tag', values: ['wcag2a', 'wcag2aa', 'wcag21a', 'wcag21aa', 'wcag22aa'] } });
          return result.violations.map(violation => `${violation.id}: ${violation.nodes.map(node => node.target.join(' ')).join(', ')}`);
        });
        accessibilityCases++;
        failures.push(...violations.map(issue => `${path} @ ${width}px: axe ${issue}`));
      }
    }
    if (['/', '/ja/', '/products/aceis/', '/ja/products/aceis/'].includes(path)) {
      for (const width of [390, 1280]) {
        await page.setViewportSize({ width, height: 900 });
        await page.screenshot({ path: `output/playwright/${path.replaceAll('/', '-').replace(/^-|-$/g, '') || 'home-en'}-${width}.png`, fullPage: true });
      }
    }
    // Reload to reset focus; the first Tab must expose the skip link.
    await page.reload();
    await page.keyboard.press('Tab');
    const skip = await page.evaluate(() => {
      const link = document.activeElement;
      const rect = link.getBoundingClientRect();
      return link.classList.contains('skip-link') && rect.top >= 0 && rect.bottom > 0 && getComputedStyle(link).outlineStyle !== 'none';
    });
    if (!skip) failures.push(`${path}: skip-link keyboard focus failed`);
    await page.keyboard.press('Enter');
    if (await page.evaluate(() => document.activeElement.id) !== 'main') failures.push(`${path}: skip link did not focus main`);
    keyboardCases++;

    if (path !== '/404.html') {
      const target = path.startsWith('/ja/') ? path.slice(3) : '/ja' + path;
      const switchLink = page.getByRole('navigation', { name: path.startsWith('/ja/') ? '言語' : 'Language', exact: true }).getByRole('link', { name: path.startsWith('/ja/') ? 'EN' : '日本語', exact: true });
      await switchLink.click();
      if (new URL(page.url()).pathname !== target) failures.push(`${path}: language switch went to ${page.url()}`);
      languageCases++;
    }
  }
  // Exercise the explicit homepage PRODUCT link in each language.
  for (const prefix of ['', '/ja']) {
    await page.goto(`${base}${prefix}/`);
    await page.getByRole('link', { name: 'PRODUCT · Project-AceIS', exact: true }).click();
    if (new URL(page.url()).pathname !== `${prefix}/products/aceis/`) failures.push(`${prefix}/: product CTA failed`);
  }
  // The shipped site also works with JavaScript disabled.
  const noJsContext = await page.context().browser().newContext({ javaScriptEnabled: false, viewport: { width: 390, height: 900 } });
  const noJsPage = await noJsContext.newPage();
  for (const prefix of ['', '/ja']) {
    await noJsPage.goto(`${base}${prefix}/`);
    await noJsPage.getByRole('link', { name: 'PRODUCT · Project-AceIS', exact: true }).click();
    if (new URL(noJsPage.url()).pathname !== `${prefix}/products/aceis/`) failures.push(`${prefix}/: no-JavaScript CTA failed`);
  }
  await noJsContext.close();
  const externalRequests = [...requests].filter(url => new URL(url).origin !== base);
  failures.push(...consoleErrors.map(error => `console: ${error}`), ...networkFailures.map(url => `request failed: ${url}`), ...externalRequests.map(url => `unexpected external request: ${url}`));
  const report = { pages: paths.length, layoutCases, accessibilityCases, languageCases, keyboardCases, productCases: 2, noJavaScriptCases: 2, externalRequests, navigationCancellations: navigationCancellations.length, failures };
  if (failures.length) throw new Error(JSON.stringify(report));
  return report;
}
