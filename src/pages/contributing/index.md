---
layout: "../../layouts/DocumentLayout.astro"
title: "Contributing"
description: "Help improve Project-KISS with focused changes, reproducible reports, and evidence-led review."
locale: "en"
eyebrow: "CONTRIBUTING"
lead: "Bring a small, clear improvement — and enough evidence to review it."
---

## Choose a focused change

Corrections, translation improvements, accessibility fixes, and clearer engineering explanations are useful contributions. For a change to project scope or product claims, explain the source and reasoning in an issue before expanding the site.

Use the [website issue tracker](https://github.com/i-pp/project-kiss-website/issues) for website questions and proposals. Do not include credentials, private logs, or confidential source material in an issue or pull request.

## Propose it through a pull request

1. Work on a branch and keep the change limited to its purpose.
2. Update the corresponding English and Japanese pages together.
3. Run `npm ci` and `npm run verify` from a checkout with Node.js 24, npm, and Python 3. See [the website development guide](/docs/#working-on-this-website) for the full starting point.
4. Check the result on narrow and wide screens, with keyboard navigation and enlarged text.
5. Describe what changed, why it helps, the checks performed, and any remaining limits.

Product descriptions must distinguish goals from verified implementation. Do not invent release dates, performance claims, or supported platforms.

## Preserve the brand assets

Use the supplied Project-KISS and Project-AceIS PNGs without changing their source bytes. Preserve their aspect ratios and transparency. Do not redraw, recolor, or replace the logos as part of an unrelated change.

## Rights and review

This website does not currently assign a repository-wide open-source license. The project names and logos retain their existing rights. Submit only material you are authorized to contribute; no license for the logos is implied by their inclusion here.

Changes require technical and editorial review before publication. A pull request or a successful build does not itself authorize a production deployment, DNS change, or credentials change.

[Read the philosophy](/philosophy/) · [Browse the repository](https://github.com/i-pp/project-kiss-website)
