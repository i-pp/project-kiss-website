<!--
KISS Open License Version 1.0 (KOL-v1)

SPDX-FileCopyrightText: 2026 I-plusplus Inc.
SPDX-License-Identifier: LicenseRef-KOL-v1

Copyright remains with its respective holders; original copyright and attribution notices must be preserved.
Contributors may add copyright notices for their own original modifications.
Distributed modifications must be identified as required by Section 4(c) of KOL-v1.

Use, modification, distribution, and incorporation into commercial or proprietary software are permitted
without license fees or source disclosure, subject to all terms of the complete KOL-v1 license.

Contributors grant the patent permissions stated in KOL-v1. Outputs are not covered merely because a
KOL-licensed tool produced them; embedded licensed material remains subject to applicable license terms.

THIS SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OR LIABILITY TO THE EXTENT PERMITTED BY APPLICABLE LAW.

This header is a summary, not a separate license or an amendment to KOL-v1.
All terms and conditions of KOL-v1 apply. See the accompanying LICENSE file for the complete license text.
-->

# License evidence and minimum CI

The README is first-party repository bootstrap documentation. The .gitignore is the GitHub Node template, matching the reviewed upstream except for the newer Nitro entries. Its CC0-1.0 terms and the copied upstream license are retained, not replaced by KOL.

## Declared scope

New first-party CI and maintenance files use LicenseRef-KOL-v1, with I-plusplus Inc. attribution. Preserve the complete applicable license and NOTICE with distributions. No new rights are claimed in external tools, GitHub Actions, quoted material, SDKs, models, or dependencies. A root license does not override a file's separate terms.

## Evidence

The upstream gitignore template and its CC0 license are at https://github.com/github/gitignore.

Minimum CI checks tracked UTF-8 files, JSON syntax, local Markdown links and declared license evidence using a commit-pinned bootstrap action that resolves and verifies the latest stable license-check-ci release. Both jobs must succeed. It runs on pull requests, main pushes, merge groups and manual dispatch. It neither tests product functionality nor proves legal ownership, compatibility, certification or editorial readiness. Existing source bytes are preserved.
