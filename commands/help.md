---
description: Cheat sheet — every Pip command with an example
---

Show this cheat sheet to the user, translated into the language they use with you. Don't run
anything else. Keep the formatting.

**Pip — what to type**

Start: `/heypip:start` — guided first project.

Design
- `/heypip:brand <what it is, for whom>` — brand: direction, moodboard, colours, fonts, brand book
- `/heypip:moodboard <brand and the feeling>` — 2–3 visual directions to pick from
- `/heypip:system <description or your colours>` — design system and code tokens
- `/heypip:logo <name, what it is>` — wordmark and simple mark as SVG, several options
- `/heypip:site <what the site is for>` — website or landing page
- `/heypip:poster <what to announce, formats>` — posters, flyers, business cards, Instagram, stories
- `/heypip:photo <what to shoot>` — photo style + prompts for Midjourney / Flux
- `/heypip:video <length, platform, idea>` — script, storyboard + prompts for Kling / Runway / Veo
- `/heypip:campaign <the launch>` — everything above in one style
- `/heypip:review <path or link>` — audit and fix existing work
- `/heypip:find <topic> <words>` — search the design library (e.g. `type luxury`, `color fintech`)

Code
- `/heypip:plan`, `/heypip:tdd`, `/heypip:code-review`, `/heypip:e2e`, `/heypip:verify`,
  `/heypip:build-fix`, `/heypip:test-coverage`, `/heypip:refactor-clean`, `/heypip:checkpoint`,
  `/heypip:eval`, `/heypip:learn`, `/heypip:orchestrate`, `/heypip:update-docs`,
  `/heypip:update-codemaps`, `/heypip:setup-pm`

You can also just write normally: "make me a poster for Saturday's market in our brand" works.
Everything for one brand lives in one folder; change a colour in `brand.json` and ask Pip to
"regenerate" — the site, posters and prompts update together.
