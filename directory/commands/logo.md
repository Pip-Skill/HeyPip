---
description: "Logo — wordmark and simple mark as SVG, in several directions, on the brand's colours and fonts"
argument-hint: "<name, what it is, the feeling; optional path to brand.json>"
---

Use the **heypip** skill. Quick mode: logo. Request: $ARGUMENTS

1. If there is a `brand.json`, use its fonts and colours; otherwise make a quick one
   (`suggest_brand.py` → `check_contrast.py`) and say so.
2. Make **4 directions** as hand-written SVG in `logo/`:
   (a) pure wordmark in the display face, with one deliberate detail (a ligature, a cut, a custom letter);
   (b) monogram (1–2 letters) built from simple geometry;
   (c) symbol + wordmark lockup — the symbol comes from the brand's story, not a generic icon;
   (d) a stamp / badge variant for packaging, stickers, social avatars.
   Make the SVG independent of installed fonts: run `fetch_fonts.py` for the display face, then
   convert the letters to paths with fontTools (`pip install fonttools brotli`; read the woff2,
   draw each glyph with a pen into `<path>`). If fontTools can't be installed, keep `<text>` and
   embed the woff2 as an `@font-face` data URL inside the SVG's `<style>`.
3. For each: light and dark versions, a 1-colour version, and a 32 px favicon test. At 32 px
   drop secondary text (taglines, ring text) and keep only the symbol or initials.
   Render a sheet `logo/logos.html` showing all of them at large and small sizes, on light,
   dark and accent grounds; screenshot it with headless Chrome
   (`google-chrome --headless=new --screenshot=logo/logos.png --window-size=1400,1800 file://…/logos.html`)
   and look at the PNG before showing the user.
4. Never copy or imitate an existing brand's logo; avoid clichés (lightbulbs, globes, swooshes,
   generic AI sparkles). Explain each direction in one line.
5. Update `brand.json` → `logo.file` with the chosen one when the user picks.

_This edition has no `scripts/` folder: where a step names a script, do that step yourself as the heypip skill's "Directory edition" note says._
