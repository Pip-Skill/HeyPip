---
description: "Creative direction and moodboard only (2–3 directions to choose from)"
argument-hint: "<brand / product and the feeling you want>"
---

Use the **heypip** skill (read its SKILL.md first). This is a quick mode: skip Step 0 scoping and go straight to the phase below. Ask at most one question, only if the answer changes the work; otherwise decide, write assumptions at the top of `brief.md`, and proceed.

Request: $ARGUMENTS

Phases 1–2 only. Read `references/direction.md` and `references/styles.md`. Use `python3 scripts/lookup.py style "<words>"` and `lookup.py type` to ground choices. Produce 2–3 distinct directions, each with a moodboard via `scripts/render_moodboard.py`. Stop and let the user pick.

_Paths like `scripts/…`, `references/…`, `taste/…` are inside the heypip skill folder (in this plugin: `skills/heypip/`)._
