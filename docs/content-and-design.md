# Content and design basis

Inspected on 2026-11-05. This records the sources and implementation decisions for this website; it is not a product specification.

## Verified source material

- The target repository initially contained only its README and Node-oriented `.gitignore` at `80f14dd`. There was no site or stack to migrate.
- The existing I-plusplus corporate website has English and Japanese Project-KISS / Project-AceIS descriptions. It identifies Project-KISS as an open-source and technical development initiative, broader than the local LLM environment. AceIS is described as a next-generation system-software research and development vision, spanning OS foundations and compiler technology, emphasizing real-time behavior, predictability, portability, and verifiability.
- The corporate site's existing approved PNG logo assets and their combined source were inspected. Hashes, dimensions, and the original crop rectangles are in [the asset manifest](brand-assets.json). The source workspace remains unchanged.
- The current website brief explicitly requires KISS, observable/verifiable engineering, governance, a separate PRODUCT route to AceIS, white and blue styling, English as primary language, Japanese content, and the seven navigation destinations.
- The official [Astro Markdown guide](https://docs.astro.build/en/guides/markdown-content/) and [GitHub Pages deployment guide](https://docs.astro.build/en/guides/deploy/github/) informed the static implementation and deployment preparation.

The corporate source repository is private. Its internal files, logs, infrastructure details, and combined original image are not included in this public repository. Only the two existing public-facing logo PNGs are reused as authorized by the website brief.

## Website decisions

- Use Astro static output, plain CSS, two small Astro layouts, and Markdown text pages. No UI framework, CMS, client runtime, analytics, external fonts, or account system is needed.
- Serve English at `/` and Japanese at `/ja/`. Language switches preserve the corresponding page. Do not infer language or redirect based on browser settings.
- Place the philosophy first on the homepage. Label the AceIS link PRODUCT and give the product its own description and explicit R&D status.
- Use white backgrounds, blue links and accents, readable typography, restrained borders, and the unmodified logos. The layout and precise color values are website implementation choices, not a claimed pre-existing brand specification.
- Use visible wrapping navigation, semantic headings and landmarks, skip navigation, focus indicators, responsive layouts, and reduced-motion compatibility. The site remains usable without JavaScript.
- Present roadmap entries as proposed documentation priorities. Do not assign unverified product milestones, dates, release status, capabilities, performance, supported platforms, or downloads.

## Source gaps

No dedicated Project-KISS website design specification, exact brand-color standard, typeface standard, public AceIS implementation specification, supported-platform matrix, benchmark, release download, or dated product roadmap was found in the inspected material. The GitHub repository search for AceIS returned no matching accessible repository; that does not prove that no repository exists elsewhere.

Both requested logos and the combined source were available, so logo placeholders are unnecessary. New layout and prose are proposals in this PR and require PM review. Technical/editorial checks are recorded in [verification.md](verification.md); production publication remains a separate decision.
