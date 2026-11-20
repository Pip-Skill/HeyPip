# Pip (heypip) — directory edition

Pip is a creative studio in one Claude plugin: brand identity, design system, websites, posters and social graphics, photo art direction and image prompts, and video storyboards — all from one `brand.json`, so every piece looks like the same brand. It also ships engineering agents and commands (code review, TDD, build fixes, docs).

This folder is the edition submitted to the Claude plugin directory. It has no hooks, no scripts and no bundled web engine: Claude does every step itself by the rules in `skills/heypip/references/`. The full edition with the engine and hooks lives at the repository root: https://github.com/Pip-Skill/HeyPip

## Install

```
/plugin install heypip --marketplace Pip-Skill/HeyPip
```

## Use

- `/heypip:start` — guided start: describe your product, get a brand.
- `/heypip:brand`, `/heypip:system`, `/heypip:logo`, `/heypip:moodboard` — identity and tokens.
- `/heypip:site`, `/heypip:poster`, `/heypip:photo`, `/heypip:video`, `/heypip:campaign` — outputs.
- `/heypip:review`, `/heypip:find`, `/heypip:help`.

Or just say "hey pip, make a brand for my bakery".

## Credits

Includes material from UI/UX Pro Max (Next Level Builder, MIT), everything-claude-code (Affaan Mustafa, MIT) and Taste Skill (Leonxlnx, MIT). Licenses are in this folder.
