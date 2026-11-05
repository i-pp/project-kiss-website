# Project-KISS website

The official website implementation for Project-KISS. It leads with KISS, observable and verifiable engineering, and governance, with a separate **PRODUCT → Project-AceIS** route.

English is primary at `/`; Japanese is at `/ja/`. Each language has Home, Philosophy, Products, AceIS, Roadmap, Docs, and Contributing. A static 404 page provides both home links.

## Develop and verify

Prerequisites: Git, Node.js 24 (Astro requires at least 22.23.4), npm, Python 3. Browser QA additionally requires an installed Google Chrome capable of running with its sandbox enabled. No model, Docker service, database, or account connection is needed.

```sh
git clone https://github.com/i-pp/project-kiss-website.git
cd project-kiss-website
npm ci
npm run dev
```

The server binds to `127.0.0.1`; use the local URL it prints. To build and verify:

```sh
npm run verify
npm run test:external
npm run preview
```

`verify` runs Astro type checks, the static build, checker regression tests, and local link/fragment checks. It also checks required routes, language pairs, canonical metadata, the sitemap, and the original logo hashes. External checks are separate bounded HTTP requests and never fetch the unpublished custom domain. To disable Astro usage telemetry, set `ASTRO_TELEMETRY_DISABLED=1` for Astro commands.

For the repeatable browser suite, explicitly start the preview in the background, run the checks, and stop the owned processes:

```sh
mkdir -p output/playwright
npm run preview -- --background --port 4321
npx playwright-cli -s=kiss-review open http://127.0.0.1:4321 --config .playwright/cli.config.json
npx playwright-cli -s=kiss-review run-code --filename scripts/browser-check.js
npx playwright-cli -s=kiss-review close
npx astro preview stop
```

The suite checks all 15 HTML pages at 320, 390, 768, 1280, and 1536 pixels with normal and 200% root text sizing; it checks image loading, overflow, header overlap, keyboard skip navigation, same-page language switches, PRODUCT links, no-JavaScript navigation, and axe WCAG A/AA rules at 390 and 1280 pixels. It is not a screen-reader test or WCAG certification. Text sizing is an approximation of enlarged-text use, not a browser-zoom certification. Browser evidence stays in ignored `output/playwright/`.

The explicit `--background` matters in automation: Astro 7 may automatically background when it detects a local agent, while a normal CI shell runs a foreground server by default.

## Structure

```text
src/components/Home.astro       Bilingual homepage
src/layouts/                   Shared page shell and Markdown layout
src/pages/                     English Markdown and Astro routes
src/pages/ja/                  Corresponding Japanese routes
src/styles/global.css          White/blue responsive design
public/assets/                 Unmodified Project-KISS and AceIS PNGs
scripts/check_site.py           Static output and optional external link checks
scripts/browser-check.js        Playwright CLI browser QA
tests/                         Negative cases for the static checker
docs/                          Sources, brand provenance, deployment and checks
.github/workflows/ci.yml        Build, links and browser checks; no deployment
.github/workflows/pages.yml     Manual publication workflow only
```

Text pages use Markdown frontmatter and `DocumentLayout.astro`. Update English and Japanese counterparts together. The homepage uses one Astro component with both locales. There is no client-side framework, analytics, external font request, or runtime backend.

## Sources and status

- [Content and design basis, including gaps](docs/content-and-design.md)
- [Original logo hashes and provenance](docs/brand-assets.json)
- [Verification record and limits](docs/verification.md)
- [GitHub Pages preparation and publication procedure](docs/deployment.md)

The site is prepared for `https://kiss.i-pp.co.jp/`. Publication is **not automatic**: neither PR creation nor merge triggers the Pages workflow. GitHub Pages enablement, custom-domain settings, DNS, secrets, organization permissions, merging, and public deployment are outside this implementation task. They require separate authorization. The prepared manual workflow requires a confirmed publication input and the `main` branch.

The AceIS pages describe a research and development vision. They do not claim delivered features, benchmarks, supported platforms, or a release date. Roadmap entries are proposed documentation priorities.

## Rights

No repository-wide license has been selected. Existing rights to names and logos are preserved; their inclusion does not grant a new license. The combined original logo source remains unchanged in its original workspace and is not included in the public repository or build output.
