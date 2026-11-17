---
description: Brand identity: direction, moodboard, brand.json, tokens and brand book
argument-hint: <what it is, for whom, any must-keep colours/fonts>
---

Use the **heypip** skill (read its SKILL.md first). This is a quick mode: skip Step 0 scoping and go straight to the phase below. Ask at most one question, only if the answer changes the work; otherwise decide, write assumptions at the top of `brief.md`, and proceed.

Request: $ARGUMENTS

Run phases 1 → 2 → 3:
1. Short brief (`references/direction.md` §1).
2. Draft from data: `python3 scripts/suggest_brand.py "<short English description: what it is, for whom>" --name <Name> --lang <languages, e.g. de,ru> --alternatives 3`. Its picks are a starting point, not the answer: if a palette, font or match is off (a script font for headings, a grey accent, a wrong product type), fix it by hand or choose from `lookup.py type|color|style`. Pick one, then write the direction (`references/direction.md`, `references/styles.md`) and `moodboard.html`.
3. Finish `brand.json` by hand (positioning, voice, imagery, film), then `check_contrast.py`, `build_tokens.py`, `render_brandbook.py`.

Deliver: direction.md, moodboard.html, brand.json, tokens/, brandbook.html. Offer next: /heypip:site, /heypip:poster, /heypip:photo.

_Paths like `scripts/…`, `references/…`, `taste/…` are inside the heypip skill folder (in this plugin: `skills/heypip/`)._
