---
description: Design system and tokens (CSS, Tailwind v4/v3, DTCG, TS) from a description or existing colours
argument-hint: <product description, or your colours/fonts, or a path to an existing site>
---

Use the **heypip** skill (read its SKILL.md first). This is a quick mode: skip Step 0 scoping and go straight to the phase below. Ask at most one question, only if the answer changes the work; otherwise decide, write assumptions at the top of `brief.md`, and proceed.

Request: $ARGUMENTS

Phase 3 only (`references/system.md`).
- From scratch: `python3 scripts/suggest_brand.py "<short English description: what it is, for whom>" --name <Name> --lang <languages, e.g. de,ru> --out brand.json`.
- From existing colours/fonts/site: read them and write `brand.json` by hand.
Then `check_contrast.py` (fix until it passes), `build_tokens.py brand.json tokens/`, `render_brandbook.py`, and `fetch_fonts.py brand.json fonts/` if they want self-hosted fonts.

_Paths like `scripts/…`, `references/…`, `taste/…` are inside the heypip skill folder (in this plugin: `skills/heypip/`)._
