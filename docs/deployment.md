# GitHub Pages preparation

Target: `https://kiss.i-pp.co.jp/`.

Prepared files:

- `astro.config.mjs`: canonical origin, static output, trailing slashes, no repository-name base path for the custom domain.
- `public/CNAME`: intended hostname only. A file in this branch does not configure DNS or GitHub Pages settings.
- `public/.nojekyll`: includes Astro's underscore-prefixed assets in a static artifact.
- `.github/workflows/ci.yml`: build, type checks, regression checks, local link validation, sandboxed Chrome checks, and downloadable static and browser-evidence artifacts. It has no deployment job.
- `.github/workflows/pages.yml`: publication only through `workflow_dispatch`, on `main`, with explicit confirmation. It rebuilds and verifies before uploading and deploying the Pages artifact.

## Before publication

The implementation task does not authorize enabling Pages, changing its custom-domain settings, editing DNS, granting permissions, creating secrets, merging the PR, or dispatching the publication workflow.

After the PM separately approves publication of a specific reviewed revision:

1. Complete technical and editorial review and merge the reviewed PR through the repository's usual approval process.
2. Have an authorized administrator configure GitHub Pages to use GitHub Actions, set the approved custom domain, and complete domain/DNS/HTTPS requirements. Those are external prerequisites, not performed by this repository's build.
3. Confirm the workflow is using the reviewed `main` revision. Manually run **Publish Pages (manual approval required)** with `confirm_publication: true` only when separately authorized. Respect any existing environment protection.
4. Inspect the deployment result and verify the live hostname, HTTPS, language switches, assets, deep routes, 404 behavior, and canonical URLs.

The repository's existing GitHub-provided workflow identity is used at runtime; no manually created secret or credential is required by these files. The deployment job requests only the Pages and OIDC permissions needed by the official action. Whether the organization's current policy permits those permissions remains unverified until an authorized deployment.

## Recovery

Do not change DNS as an automatic recovery step. For a content rollback, review a revert PR, rebuild it, and publish the approved revision through the same manual workflow. If publication itself must be disabled, that requires a separately authorized administrator action.

No public deployment or DNS test has been performed as part of this implementation.
