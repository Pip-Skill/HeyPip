# Print and graphics: posters, flyers, cards, social

## Contents
1. What to make and in which format
2. The spec and the renderer
3. Composition that works
4. Type on posters
5. Print production
6. Social and digital
7. Checklist

## 1. What to make and in which format

| Job | Format name | Size | Notes |
|---|---|---|---|
| Street / event poster | `A2`, `poster-50x70`, `B2` | 420×594, 500×700, 500×707 mm | read at 3–5 m: headline ≥ 8% of height |
| Indoor poster | `A3` | 297×420 mm | read at 1–2 m |
| Flyer | `A5`, `A6`, `flyer-DL` | 148×210, 105×148, 99×210 mm | one message, one action |
| Business card | `card-eu`, `card-us`, `card-eu-v` | 85×55, 89×51 mm | name, role, one contact line, mark |
| Instagram post | `ig-post` / `ig-square` | 1080×1350 / 1080×1080 px | 4:5 wins the feed |
| Stories / Reels cover | `ig-story` | 1080×1920 px | keep top 14% and bottom 20% clear |
| Link preview | `og` | 1200×630 px | headline ≤ 6 words, readable at 300 px wide |
| X / LinkedIn | `x-post`, `linkedin` | 1600×900, 1200×627 px | |
| YouTube thumbnail | `yt-thumb` | 1280×720 px | 3–4 words, a face or object, huge type |
| Any other | `{"w":…, "h":…, "unit":"mm"\|"px"}` | | |

For a set (campaign), make one spec list with all formats so they render from the same brand
and copy, and check them side by side.

## 2. The spec and the renderer

```bash
python3 scripts/render_print.py brand.json print/specs.json print/ --export pdf,png --fonts site/fonts
```

`templates/print.example.json` shows every layout. Fields: `format`, `layout`, `mode`
(`light` | `dark` | `accent` ground), `kicker`, `headline`, `sub`, `body`, `number`, `meta`
(list), `cta`, `mark`, `image` (path) or `image_note` (labels the placeholder), `items` (grid).

Layouts:
- **type-led** — the headline is the image. Default for posters with no strong photo.
- **image-led** — full-bleed photo, headline over a ground-coloured fade at the bottom.
- **split** — text column + image column. Flyers, landscape formats.
- **big-number** — one figure (price, date, count) at 50–60% of the short side.
- **grid** — headline + 2-column list of short items. Schedules, steps, menus, stories.
- **card** — business cards.

The renderer sizes everything in container units, so a layout scales from a business card to a
50×70 poster. If a piece needs something the layouts can't do (a custom illustration, a
die-cut, a typographic experiment), write the HTML by hand using the same `:root` variables
from `render_print.py`, and still export through Chrome.

Fonts: pass `--fonts <dir>` with a `fonts.css` from `fetch_fonts.py` so PDFs embed the real
faces. Without it the Google Fonts link is used (fine online, risky for print shops).

## 3. Composition that works

- **One idea per piece.** If you need two headlines, you need two pieces.
- **Three levels max:** headline → one supporting line → small meta (date, place, URL).
- **Scale contrast is the design.** Headline 8–15× the meta size. Timid ratios look amateur.
- **Asymmetry over centring** unless the brand is classical. Anchor text to a corner or edge.
- **Empty space is a shape**, not leftovers: give it 30–50% of the area on posters.
- **One accent use** — the action or the number, never both plus a rule plus a badge.
- **Repeat the brand's signature** (a rule, a numbering system, a texture) across a set so
  pieces read as a family from across the street.

## 4. Type on posters

- Display face for the headline at weight 400–500 for serifs, 600–800 for grotesks;
  tighten tracking (-0.02 to -0.04em) above 60 pt.
- Break lines by sense, not by width ("Сорок вещей / в неделю."). Use `text-wrap: balance`.
- Figures: use lining numerals for big numbers (oldstyle 3/4/5/7/9 drop below the line).
- Body copy on print: 9–11 pt for flyers, never under 7 pt; meta in mono or small caps.
- Check the face covers the language (Cyrillic, diacritics) — `fetch_fonts.py` warns.

## 5. Print production

- PDFs include **3 mm bleed** on every side; backgrounds and images run into it.
- Keep text in the **safe area** (the renderer insets 5% of the short side + bleed).
- Colour: the renderer outputs RGB. For offset print, ask the printer for their profile and
  convert in Acrobat/Illustrator (or let a digital printer handle RGB — most do).
- Images: 300 dpi at final size for print (a 50×70 poster full-bleed photo ≈ 5900×8270 px);
  150 dpi is acceptable for large posters viewed from distance.
- Rich black for big dark areas is the printer's job; tell them "large dark background".
- Send: PDF + fonts licences note (Google fonts are OFL) + a PNG proof.

## 6. Social and digital

- Design at the exact px size; export PNG at 2× (the renderer does).
- Text must survive the feed thumbnail (~300 px wide): squint test.
- Stories: no text in the top 14% / bottom 20%; keep the CTA above the reply bar.
- Carousels: same layout, one idea per slide, a number or progress mark on each.
- Link previews (og): brand mark + 3–6 word headline, nothing small.

## 7. Checklist

- [ ] One message, readable from the right distance (3 m poster, 30 cm flyer, thumbnail post)
- [ ] Headline / support / meta — three levels, strong size contrast
- [ ] Real copy, real dates, real contacts (`.example` placeholders marked if unknown)
- [ ] Brand fonts embedded (`--fonts`), Cyrillic/diacritics present
- [ ] Contrast of text on ground ≥ 4.5:1 (≥ 3:1 for headlines over 40 px)
- [ ] Print: bleed present, nothing important in the outer 5%, images ≥ 150–300 dpi
- [ ] Set: all pieces share kicker style, mark position and accent use
