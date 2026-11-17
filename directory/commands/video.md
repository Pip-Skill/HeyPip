---
description: "Video: script, storyboard, motion brief and Runway/Kling/Luma/Veo prompts"
argument-hint: "<length, platform, what happens; models>"
---

Use the **heypip** skill (read its SKILL.md first). This is a quick mode: skip Step 0 scoping and go straight to the phase below. Ask at most one question, only if the answer changes the work; otherwise decide, write assumptions at the top of `brief.md`, and proceed.

Request: $ARGUMENTS

Phase 4c (`references/video.md`). Needs `brand.json` (compact one if missing: palette, film, motion). Script with timings that add up, `video/storyboard.html`, motion brief, `video/shots.json` → `prompt_pack.py` for the chosen models.

_Paths like `scripts/…`, `references/…`, `taste/…` are inside the heypip skill folder (in this plugin: `skills/heypip/`)._
