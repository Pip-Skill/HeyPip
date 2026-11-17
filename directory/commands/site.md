---
description: "Website / landing page built by the web engine on the brand"
argument-hint: "<what the site is for; path to brand.json if you have one>"
---

Use the **heypip** skill (read its SKILL.md first). This is a quick mode: skip Step 0 scoping and go straight to the phase below. Ask at most one question, only if the answer changes the work; otherwise decide, write assumptions at the top of `brief.md`, and proceed.

Request: $ARGUMENTS

Phase 4a. If there is no `brand.json`, make one first in 2 minutes: `suggest_brand.py` → `check_contrast.py` → `build_tokens.py` (say you did).
Then read `references/web.md`. If the skill has a `taste/` folder (full install from GitHub), also read **`taste/ENGINE.md` in full** and follow the engine's run; otherwise build by `references/web.md` alone. At the deal step use `python3 scripts/brand_to_taste.py brand.json --page <kind>` instead of dealing a palette/type. Before delivery: `fetch_fonts.py brand.json site/fonts`, no CDN dependencies (and the engine gate passes, when the engine is present).

_Paths like `references/…` are inside the heypip skill folder (`skills/heypip/`). This edition has no `scripts/` folder: where a step names a script, do that step yourself as the heypip skill's "Directory edition" note says._
