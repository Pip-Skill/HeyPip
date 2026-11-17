# Review and polish

Run this before handing anything over. Write findings and fixes to `review.md` (what you
checked, what failed, what you changed). Fix, don't just list.

## Direction
- [ ] Positioning names category, difference, three character words, is/is-not.
- [ ] The direction would *not* fit a competitor in the same category unchanged.
- [ ] There is a "refuse" list and the outputs obey it.

## System
- [ ] `check_contrast.py` passes for light (and dark, if defined).
- [ ] One type scale, one spacing scale, one radius philosophy, ≤ 3 elevation levels.
- [ ] Fonts support every language/script the brand needs; only used weights load.
- [ ] Tokens regenerated after the last `brand.json` change (timestamps match).

## Web
- [ ] Hero says what it is and for whom; one primary action visible without scrolling.
- [ ] No raw hex or arbitrary values outside token files.
- [ ] Real copy in brand voice; no lorem ipsum; unknown facts marked `[LIKE THIS]`.
- [ ] Works at 390 / 768 / 1024 / 1440; no horizontal scroll; tap targets ≥ 44px.
- [ ] Visible focus, keyboard reachable, labels, alt text, one `h1`, reduced motion.
- [ ] Images sized, lazy below the fold; no layout shift from fonts.
- [ ] Title, description, OG image, favicon, `lang`.
- [ ] If you can render, screenshot each breakpoint and look at it. Fix what looks off:
      crowded sections, orphans in headings, misaligned edges, inconsistent gaps.

## Photo
- [ ] Every prompt/shot carries the same brand suffix (light, grade, palette).
- [ ] Type space planned on hero and social formats.
- [ ] No living-artist names, no real identifiable people in prompts.

## Video
- [ ] Hook in first 1.5s for social; captions for all speech; safe areas respected.
- [ ] Shot IDs match across script, storyboard and prompts.
- [ ] Motion durations/easings match the web tokens.

## Common AI tells to remove
Purple-blue gradients, glassmorphism by default, emoji in headings, "Unlock / Elevate /
Seamless / Revolutionize", three identical feature cards with icons, centred everything,
fake testimonials, stock-photo smiles, random 3D blobs, every element fading in on scroll.
