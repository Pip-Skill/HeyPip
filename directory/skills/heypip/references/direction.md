# Discovery and creative direction

## Contents
1. Discovery — the brief
2. Positioning
3. The direction document
4. The moodboard
5. Presenting directions

---

## 1. Discovery — the brief

Write `brief.md` before any visual decision. It is short (one screen) and it is the thing
every later choice is checked against.

```markdown
# Brief — <Brand>
**What it is:** one sentence, concrete (what is sold, to whom, at what price level).
**Audience:** who buys, what they already use instead, what they care about, what puts them off.
**The job of this work:** e.g. "launch site that converts waitlist sign-ups", "rebrand to look
premium enough for €300 price point".
**Must keep:** existing logo, colours, names, legal requirements, stack.
**Constraints:** budget, deadline, platforms, languages, accessibility needs.
**Success looks like:** the one measurable or observable outcome.
**Assumptions:** what you decided without asking (so the user can correct it).
**Changelog:** v1 — …
```

Questions worth asking (pick at most three, only if the answer changes the work):
- Who is it for, and what do they buy instead today?
- What price level or positioning (budget / mid / premium / luxury)?
- Anything we must keep (logo, colour, name)?
- For sites: what is the one action a visitor should take? What stack?

If the user gave a one-liner, infer the rest from the category and write it as assumptions.

## 2. Positioning

Before visuals, write three lines. They decide everything downstream.

- **Category:** what shelf it sits on ("independent slow-fashion label").
- **Difference:** the true, specific reason to choose it ("made-to-order in a Lisbon atelier,
  6 pieces a week").
- **Character:** three adjectives that pull against each other a little — tension makes a
  brand memorable ("quiet, tactile, defiant"; "precise, warm, slightly nerdy").

Then write **"is / is not"** pairs. This is the most useful tool against generic output:

| Is | Is not |
|---|---|
| quiet confidence | minimal-for-the-sake-of-it |
| tactile, material | glossy, plastic |
| editorial pacing | e-commerce grid noise |

## 3. The direction document

`direction.md` turns positioning into concrete visual language. Every line has a decision
and a reason.

```markdown
# Direction — <Brand>: "<direction name>"
One paragraph: the idea in plain words, as if pitching it to the client.

## Positioning
Category / Difference / Character (three adjectives) / Is–Is not table

## Visual language
- **Style family:** e.g. editorial minimalism with Swiss grid discipline (see styles.md)
- **Colour logic:** which colours, in what proportions (e.g. 70% bone, 20% ink, 10% rust),
  and what each colour *means* (rust = action only).
- **Typography:** display face + text face + (optional) mono; why these; how big the contrast
  between display and body sizes is.
- **Layout and rhythm:** grid, density, whitespace, alignment habits, how sections breathe.
- **Shape:** radius philosophy (sharp/soft/round), borders, elevation (flat/soft shadows).
- **Imagery:** photo style in one line (light, colour grade, framing, people or not).
- **Motion:** character (calm/snappy/elastic), durations, what moves and what never moves.
- **Voice:** how headlines sound; 3 example headlines.

## What we refuse
Five concrete "never" rules (e.g. "never a gradient", "never centred body text").

## Risks
What could go wrong with this direction and how we guard against it.
```

Name the direction ("Workshop Light", "Night Ledger"). Names make directions discussable.

### Offering alternatives
When the brief is open, offer **two or three directions** that differ in *stance*, not just
colour — e.g. "quiet editorial" vs "loud graphic" vs "warm crafted". Give each a one-paragraph
pitch and a moodboard strip; recommend one and say why. Then build only the chosen one.

## 4. The moodboard

A moodboard is evidence for the direction, not decoration. Build it as a page
(`moodboard.html`) with `scripts/render_moodboard.py`. Input JSON:

```json
{
  "brand": "Lumen & Loom",
  "direction": "Workshop Light",
  "summary": "Natural light, raw linen, slow hands. Editorial calm with one rust accent.",
  "palette": [{"name": "Bone", "hex": "#EFE9DF", "role": "ground"}, {"name": "Rust", "hex": "#B5532D", "role": "action"}],
  "fonts": {"display": "Fraunces", "text": "Inter"},
  "tiles": [
    {"type": "color", "hex": "#EFE9DF", "label": "Bone · 70%"},
    {"type": "type", "font": "Fraunces", "sample": "Made slowly.", "label": "Display"},
    {"type": "texture", "pattern": "linen", "colors": ["#EFE9DF", "#D9CFBF"], "label": "Raw linen"},
    {"type": "composition", "layout": "asym-left", "label": "Asymmetric, lots of air"},
    {"type": "reference", "title": "North light studio portrait", "text": "Soft window light from camera left, matte grade, no retouching gloss."},
    {"type": "prompt", "title": "Hero image", "text": "editorial photo of hands stitching raw linen, north window light, ..."},
    {"type": "words", "items": ["quiet", "tactile", "defiant"]}
  ]
}
```

Tile types: `color`, `type`, `texture` (patterns: `linen`, `grain`, `grid`, `dots`,
`stripes`, `paper`, `noise`), `composition` (layouts: `asym-left`, `asym-right`, `centered`,
`split`, `grid-3`, `full-bleed`, `stacked`), `reference` (a described visual reference —
photographer, era, film, product category; describe it, don't paste copyrighted images),
`prompt` (an image prompt the user can run), `words`, `image` (only if the user supplied
an image file or a licensed URL).

If an image-generation tool is connected in the session, generate 3–6 images from the
`prompt` tiles and add them as `image` tiles. If not, the prompt tiles are the deliverable —
say so plainly.

## 5. Presenting directions

Show the moodboard, then in chat: the direction name, the one-paragraph idea, the three
character words, the "refuse" list, and a clear question: "Go with this, or adjust (warmer /
bolder / more minimal …)?" Keep it short.
