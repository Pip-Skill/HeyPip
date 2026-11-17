# Style library

Use this as a vocabulary, not a menu to copy. Each style lists what defines it, token
starting points, where it fits, and the traps that make it look cheap. Mix two at most
(e.g. "Swiss grid + warm editorial type"), and say which one leads.

## Contents
Swiss / International · Editorial · Quiet luxury · Warm minimal · Neo-brutalism (soft and
loud) · Maximalism · Retro-futurism / tech · Organic / crafted · Playful / toy · Dark
precision (dev tools, fintech) · Y2K / chrome · Brutalist web (raw) · Choosing quickly

---

### Swiss / International
**Defined by:** strict grid, flush-left ragged-right text, grotesk type, big type-size
contrast, asymmetry, generous margins, colour used sparingly and flat.
**Tokens:** radius 0–2px; one grotesk (Inter Tight, Neue Haas-like: "Inter", "Helvetica
Now" alternatives such as "Schibsted Grotesk", "Geist"); scale ratio 1.333–1.5; spacing
base 8; 12-col grid; motion snappy 120–200ms, no bounce.
**Fits:** architecture, culture, agencies, B2B that wants authority.
**Traps:** centred layouts, too many weights, decorative shadows.

### Editorial
**Defined by:** a serif display (high contrast), long-form rhythm, pull quotes, captions,
column layouts, photography as the hero, restrained UI chrome.
**Tokens:** display serif (Fraunces, Newsreader, Instrument Serif, Playfair alt: "DM Serif
Display"), text sans or serif at 17–19px; line-height 1.5–1.65; radius 0–4px; motion calm
300–500ms fades/slides.
**Fits:** fashion, publishing, hospitality, premium D2C.
**Traps:** using the display serif for body/UI; too-small body text.

### Quiet luxury
**Defined by:** almost nothing on screen, exceptional photography, tiny uppercase labels with
wide tracking, neutral palette (bone, stone, ink), one subtle metal or deep accent.
**Tokens:** palette 3–4 neutrals + 1 accent at ≤5% usage; text 15–16px; tracking on labels
+0.08–0.14em; radius 0; motion slow 500–800ms, opacity only.
**Fits:** luxury, jewellery, high-end real estate, hotels.
**Traps:** low contrast grey-on-grey text (fails WCAG); empty without great photos.

### Warm minimal
**Defined by:** soft neutrals with warmth (cream, sand, clay), rounded friendly type,
generous spacing, soft radius, illustration or warm photography.
**Tokens:** radius 12–20px; sans with humanist warmth (Manrope, Figtree, General Sans alt:
"Outfit"); soft shadows; motion 200–320ms ease-out.
**Fits:** wellness, consumer apps, education, food.
**Traps:** turning beige-boring; pick one confident accent.

### Neo-brutalism
**Loud:** saturated flat colours, thick black borders, hard offset shadows, chunky type,
stickers. **Soft:** same structure, muted palette, 2px borders, 3–4px offsets.
**Tokens:** border 2–3px ink; shadow `4px 4px 0 ink`; radius 0–12px; grotesk or rounded
display; motion snappy with press-down states (translate 2px).
**Fits:** creator tools, indie products, Gen-Z brands, playful SaaS.
**Traps:** every element shouting; unreadable colour combos; using it for luxury.

### Maximalism
**Defined by:** layered imagery, pattern, multiple typefaces in a controlled system, big
colour, collage, overlapping elements, kinetic type.
**Tokens:** a strict underlying grid so chaos reads as intentional; 2–3 type families with
clear roles; motion expressive but short.
**Fits:** music, fashion drops, festivals, culture.
**Traps:** illegible text over images; performance (huge images, too many fonts).

### Retro-futurism / tech
**Defined by:** mono or technical type, grids and coordinates, scanlines/dither, terminal
details, accent neon on dark or ink on paper.
**Fits:** dev tools, hardware, AI labs, crypto-adjacent (careful).
**Traps:** cliché purple-cyan glow; low contrast neon text.

### Organic / crafted
**Defined by:** hand-drawn marks, paper and grain textures, irregular shapes, earthy palette,
imperfect type (soft serifs, handwritten accents used sparingly).
**Fits:** food, craft, sustainability, local businesses.
**Traps:** looking amateur — keep the grid and type system strict underneath.

### Playful / toy
**Defined by:** rounded everything, bouncy motion, mascots, bright but harmonised palette,
big friendly type.
**Tokens:** radius 16–999px; motion spring/overshoot 300–450ms; scale 1.25.
**Fits:** kids, games, consumer apps, community.
**Traps:** childish for adult B2B; motion overload.

### Dark precision
**Defined by:** near-black grounds, thin hairlines, small precise type, data-dense
components, one sharp accent, subtle glows only where state changes.
**Fits:** developer tools, fintech, analytics, security.
**Traps:** grey-on-black contrast failures; everything glowing.

### Y2K / chrome
**Defined by:** chrome gradients, bubbly type, stars, translucency, saturated pastels.
**Fits:** fashion drops, music, nostalgia campaigns. Short-lived on purpose.
**Traps:** it ages fast; keep it for campaigns, not core systems.

### Brutalist web (raw)
**Defined by:** default-looking HTML, system fonts, visible structure, underlined links,
deliberate "unstyled" honesty.
**Fits:** artists, manifestos, experimental portfolios.
**Traps:** looks broken to mainstream audiences.

---

## Choosing quickly

| Audience / category | Strong starting points |
|---|---|
| Premium fashion, beauty | Editorial, Quiet luxury |
| Slow / sustainable goods | Warm minimal + Organic, Editorial |
| B2B SaaS (general) | Swiss + Warm minimal; Dark precision for dev audiences |
| Fintech | Dark precision or Swiss; avoid playful unless consumer |
| Consumer apps | Warm minimal, Playful, Soft neo-brutal |
| Creator / indie tools | Neo-brutalism, Retro-tech |
| Culture, music, events | Maximalism, Swiss, Y2K for drops |
| Local business | Organic / crafted, Warm minimal |
| Luxury, hospitality | Quiet luxury, Editorial |

Whatever you pick, write why it fits *this* audience in `direction.md`.
