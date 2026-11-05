---
layout: "../../layouts/DocumentLayout.astro"
title: "Documentation"
description: "Start with the Project-KISS philosophy, engineering evidence principles, product vision, and website development guide."
locale: "en"
eyebrow: "DOCUMENTATION"
lead: "Start with the principles. Keep the conditions and limits alongside the results."
---

## Start here

- [Philosophy](/philosophy/): KISS, observability, verification, and governance.
- [Project-AceIS](/products/aceis/): the product vision and development goals.
- [Roadmap](/roadmap/): the scope of this website and proposed documentation work.
- [Contributing](/contributing/): proposing changes and reporting issues.

## What a useful verification report includes

A report should explain the question being tested, the relevant version and environment, the procedure, the observed result, and any limitations. Someone reading it should be able to distinguish measured behavior from a proposal or assumption.

State whether a check used a fixture, mock, or live integration. Keep unexecuted checks separate from passing and failing results. Remove secrets and unrelated private information before sharing a report.

## Working on this website

These commands apply to a checkout of the **website repository**. They do not install or run Project-AceIS.

Prerequisites: Git, Node.js 24 (at least 22.23.4 is required by the pinned Astro version), npm, and Python 3. The website uses Astro for static output and Markdown for its text pages.

```sh
git clone https://github.com/i-pp/project-kiss-website.git
cd project-kiss-website
npm ci
npm run dev
```

The development server prints its local address and binds to `127.0.0.1`. From the same checkout, run the checks and static preview:

```sh
npm run verify
npm run preview
```

`verify` checks Astro types, builds the static site, tests the checker, and validates local links, fragments, metadata, language pairs, and logo hashes. The preview command serves the built output locally.

For the repository structure and publication procedure, see the [repository README](https://github.com/i-pp/project-kiss-website#readme). Product implementation documentation will be added when reviewed material is ready.
