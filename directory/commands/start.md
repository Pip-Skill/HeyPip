---
description: "Start here — a guided first project with Pip, step by step, no experience needed"
argument-hint: "(optional) what you want to make"
---

The user is new to Pip and maybe to Claude Code. Be a friendly guide. Speak the user's
language (match the language they write in). Keep every message short.

Request (may be empty): $ARGUMENTS

1. If the request is empty, greet in one line and ask **one** question with simple options:
   "What do you want to make today?" —
   (a) a brand from scratch, (b) a website or landing page, (c) a poster / flyer / Instagram post,
   (d) photo or video prompts for AI generators, (e) a full launch campaign, (f) improve something I already have.
   Use the AskUserQuestion tool if available.
2. Then ask at most two more short questions: what the business/product is and who it's for;
   and the language of the texts. Don't ask about colours, fonts or styles — Pip proposes them.
3. Say in one sentence what you'll make and where the files will be (one project folder).
4. Do it with the **heypip** skill, using the matching quick mode
   (brand / site / poster / photo / video / campaign / review — see the skill's "Quick modes").
   For a brand, show 3 directions from `suggest_brand.py --alternatives 3` and let them pick.
5. When done, show what was made in plain words (no jargon: say "colours and fonts file" before
   "tokens"), how to open it (e.g. "open site/index.html in your browser"), and suggest exactly
   one next command, e.g. `/heypip:poster` to make a poster in the same style.
6. End with: "Tip: `/heypip:help` lists everything Pip can do."

_This edition has no `scripts/` folder: where a step names a script, do that step yourself as the heypip skill's "Directory edition" note says._
