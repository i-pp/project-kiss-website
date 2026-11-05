# Verification record

2026-11-05, Asia/Tokyo. Local checkout on branch `feat/project-kiss-official-site`, based on `80f14dd`. Local tools: Node.js 26.13.0, npm 11.20.0, Python 3, existing Google Chrome. CI targets Node.js 24 and sandboxed Chrome on an Ubuntu runner.

## Local results

| Check | Result |
| --- | --- |
| `ASTRO_TELEMETRY_DISABLED=1 npm run verify` | PASS: Astro check has 0 errors/warnings/hints; 15 HTML pages build; 10 checker regression tests pass; 484 local references, 7 language pairs, metadata, sitemap, CNAME, `.nojekyll`, and 2 original logo hashes pass. |
| `npm run test:external` | PASS: all 3 distinct external URLs return HTTP 200 (repository, website issue tracker, corporate homepage). The future custom domain is not fetched. |
| `npx playwright-cli -s=kiss-review run-code --filename scripts/browser-check.js` | PASS: 150 layout cases, 30 axe checks, 14 same-page language switches, 15 keyboard skip-link cases, 2 homepage PRODUCT cases, and 2 no-JavaScript PRODUCT cases. No uncancelled failed requests, page errors, or external page requests observed. |
| Original logo comparison | PASS: both PNGs are byte-identical to the existing corporate website assets; Pillow confirms full RGBA equality with the documented rectangles of the combined source. Combined source SHA-256 remains unchanged. |
| `npm audit --omit=dev --audit-level=high` | PASS: 0 reported production dependency vulnerabilities at the time of the check. This is an advisory database check, not a full security assessment. |
| `git diff --check` | PASS. |

The first browser checks found enlarged-text overflow and an accessible-name mismatch. These were corrected through wrapping grid/flex sizing, scrollable code blocks within their columns, and removing the overriding logo-link name. The final local run passes the same checks.

The initial GitHub run passed `npm run verify` but remained in the preview-start command, before browser execution. Source inspection of the pinned Astro CLI confirmed that local agent detection can infer background mode, while an ordinary CI shell defaults to a foreground server. CI now uses explicit `--background`, separate startup/browser/check steps, and per-step timeouts. The superseded run is not counted as a browser pass.

Browser screenshots and machine results are generated under ignored `output/playwright/`. Representative English/Japanese home and AceIS pages are captured at desktop and mobile widths. CI uploads its own browser evidence and static output as artifacts; a local result is not evidence that CI passed.

## Browser scope

- All 14 localized content routes plus `/404.html`.
- 320, 390, 768, 1280, and 1536 CSS pixels; normal and 200% root font sizing.
- Loaded images, preserved display proportions, document overflow, and header link overlap.
- axe-core 4.14.0 rules tagged WCAG 2 A/AA, 2.1 A/AA, and 2.2 AA at 390 and 1280 pixels.
- Keyboard focus visibility, skip navigation, localized routes, and explicit product links.
- JavaScript disabled in a separate browser context for both homepage-to-product flows.
- Cancelled favicon requests during navigation are recorded separately, rather than treated as successful requests or content-image failures.

## Content and technical review

- Homepage leads with the philosophy. PRODUCT links lead directly to the separate AceIS page.
- English and Japanese pages describe the same scope. AceIS retains the source material's vision/goals qualification.
- No invented product release dates, benchmark values, supported-platform claims, download links, customer claims, or implementation-completion claims were added.
- Roadmap entries are explicitly proposed documentation priorities.
- Public output contains no combined original source, internal infrastructure records, local paths, raw logs, credentials, analytics, external fonts, or client runtime scripts.
- CI and deployment are separate. No push/PR/merge event triggers publication; the manual deployment workflow requires `main` and an affirmative input.
- New layout and copy are reviewable proposals. Final PM acceptance and authorization to publish remain outstanding.

## Limits and follow-up

GitHub CI results are available on the PR and must be assessed separately from the local checks. Production Pages deployment, custom-domain configuration, DNS, HTTPS, real-device behavior, Firefox/Safari, screen-reader use, browser zoom, and a comprehensive accessibility audit have not been verified. Automated axe checks do not constitute WCAG certification.

No deployment workflow was dispatched. Pages, DNS, secrets, organization permissions, existing services, authentication, and other workspaces were not changed. The source/design gaps and their effect are listed in [content-and-design.md](content-and-design.md). The publication prerequisites and recovery procedure are in [deployment.md](deployment.md).
