---
description: Posters, flyers, business cards and social graphics (PDF with bleed + PNG)
argument-hint: <what to announce, formats e.g. A2 poster + IG post + story>
---

Use the **heypip** skill (read its SKILL.md first). This is a quick mode: skip Step 0 scoping and go straight to the phase below. Ask at most one question, only if the answer changes the work; otherwise decide, write assumptions at the top of `brief.md`, and proceed.

Request: $ARGUMENTS

Read `references/print.md`. If there is no `brand.json`, make a quick one with `suggest_brand.py`.
Write `print/specs.json` (one entry per format, see `templates/print.example.json`), self-host fonts with `fetch_fonts.py brand.json print/fonts`, then:
`python3 scripts/render_print.py brand.json print/specs.json print/ --export pdf,png --fonts print/fonts`
Look at every PNG, fix composition and copy, re-render. Deliver the PDFs and PNGs.

_Paths like `scripts/…`, `references/…`, `taste/…` are inside the heypip skill folder (in this plugin: `skills/heypip/`)._
