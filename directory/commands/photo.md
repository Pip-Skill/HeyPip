---
description: "Photo art direction: style guide, shot list and Midjourney/Flux/SDXL prompts"
argument-hint: "<what to shoot, where it will be used, models>"
---

Use the **heypip** skill (read its SKILL.md first). This is a quick mode: skip Step 0 scoping and go straight to the phase below. Ask at most one question, only if the answer changes the work; otherwise decide, write assumptions at the top of `brief.md`, and proceed.

Request: $ARGUMENTS

Phase 4b (`references/photo.md`). Needs `brand.json` (make a compact one if missing: palette, imagery, mood). Write the style guide and `photo/shots.json`, run `scripts/prompt_pack.py brand.json photo/shots.json photo/prompts.md --models <models>`, then hand-tune the prompts.

_Paths like `scripts/…`, `references/…`, `taste/…` are inside the heypip skill folder (in this plugin: `skills/heypip/`)._
