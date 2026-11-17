---
description: Audit an existing site, design or brand and fix it
argument-hint: <path or URL to the site/files, what worries you>
---

Use the **heypip** skill, phase 5 (`references/review.md`). Request: $ARGUMENTS

1. Read what exists; reconstruct a `brand.json` from it and run `check_contrast.py`.
2. Check against `references/review.md` and the library: `lookup.py ux "<issue>"`, `lookup.py stack:<stack> "<topic>"`, `lookup.py landing "<product>"`.
3. Write `review.md` with findings by severity and concrete fixes, then apply the fixes the user agrees to (or all of them if they said so).

_Paths like `scripts/…`, `references/…`, `taste/…` are inside the heypip skill folder (in this plugin: `skills/heypip/`)._
