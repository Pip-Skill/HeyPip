# Web and product

> **Building a page?** This file covers stack choice and how a site plugs into the brand. The
> build itself follows the web engine: read `taste/ENGINE.md` in full and hand it the brand with
> `scripts/brand_to_taste.py` (see SKILL.md, "The web engine").

## Contents
1. Choosing the stack
2. Page architecture and flows
3. Building with the tokens
4. Section craft
5. Motion and micro-interactions
6. Performance and accessibility
7. Deliverable checklist

---

## 1. Choosing the stack

Use what the user names. Otherwise:

| Situation | Stack |
|---|---|
| Landing page, portfolio, quick launch, user isn't a developer | Single `index.html` + Tailwind (v4 via CDN `@tailwindcss/browser` for prototypes, or compiled) + `tokens.css` |
| Marketing site with several pages, content-heavy, SEO | Astro + Tailwind |
| App-like product, existing React codebase | React or Next.js + Tailwind, `tokens.ts` for JS access |
| Existing project | Its stack. Read its config first and wire tokens into it. |

Wire tokens once: import `tokens/tokens.css` (plain CSS / Astro) or `tokens/tokens.tailwind.css`
(Tailwind v4) or the v3 preset. After that, write classes that use token names
(`bg-bg text-text`, `text-2xl`, `rounded-md`, `p-6`) — never raw hexes or arbitrary values.

## 2. Page architecture and flows

Before code, write the page as a list in `site/PLAN.md`:
- the **one primary action** (Buy, Join waitlist, Book a call) and where it appears;
- sections in order, each with: its job, its headline, its visual (what is actually shown);
- for products: the core user flow (entry → value → action → confirmation) and each state
  (empty, loading, error, success).

Typical landing order (adapt, don't copy): hero (what + for whom + proof + action) →
problem/tension → how it works / product → proof (real, or placeholders marked) → offer /
pricing → FAQ → final action → footer. Each section does one job.

## 3. Building with the tokens

- Headings use the display family and the type scale (`text-5xl` etc.), body uses text family.
- Layout uses `layout.maxWidth`, `columns`, `gutter`, `margin` — one container component.
- One button component with variants from `brand.json`; reuse it everywhere.
- Dark mode, if defined, via `data-theme` toggle + system preference.
- Fonts: load only declared weights; `font-display: swap`; preconnect to the font host.

## 4. Section craft (what makes it look premium)

- **Hero:** say plainly what it is and for whom in ≤ 10 words; one supporting line with a
  concrete fact; primary + at most one secondary action; a real visual (product UI, product
  photo, or the brand's strongest image) — not an abstract blob.
- **Hierarchy:** one focal point per screen. Contrast in size (display vs body ≥ 3×) does more
  than colour.
- **Rhythm:** alternate density — a dense section, then air. Vary composition between
  sections (split, full-bleed image, grid, statement type) so the page doesn't feel templated.
- **Copy:** in the brand voice, specific, short. Buttons = verb + object ("Book a fitting").
- **Imagery:** use the photo direction from `brand.json → imagery`. If there are no assets,
  insert well-labelled placeholders sized correctly and generate prompts for them
  (see `photo.md`), rather than generic stock.
- **Details:** consistent icon set (one style, one stroke width), aligned baselines, real
  empty and error states, favicon and social share image.

## 5. Motion and micro-interactions

From `brand.json → motion`. Defaults:
- Hero enters once on load (staggered ≤ 3 elements, ≤ 600ms total).
- Hover: buttons shift 1px or change surface; cards lift ≤ 2px; links underline-draw.
- Press: scale .98 or translate 1–2px.
- Scroll reveals only for large section transitions, never on every element.
- Use CSS transitions first; reach for a library (Motion/GSAP) only for sequences.
- Wrap all non-essential motion in `@media (prefers-reduced-motion: no-preference)`.

## 6. Performance and accessibility

- Images: correct dimensions, `width`/`height` set, `loading="lazy"` below the fold, modern
  formats; hero image `fetchpriority="high"`.
- No layout shift from fonts (size-adjusted fallbacks or `font-display: swap` with similar
  metrics).
- Semantic HTML: landmarks, one `h1`, ordered headings, labels on inputs, `alt` text,
  buttons are `<button>`, links are `<a>`.
- Keyboard: everything reachable, visible focus, skip link, menu closes with Esc.
- Meta: title, description, Open Graph image, favicon, `lang`.
- Legal (EU/DE sites): Impressum and privacy links in footer when the site is public.

## 7. Deliverable checklist

- `site/` runs as delivered (open `index.html`, or `npm install && npm run dev`).
- Tokens imported, no stray hex values (`grep -R "#[0-9a-fA-F]\{6\}" site/` should only hit
  token files and images).
- Works at 390, 768, 1024, 1440 widths.
- Contrast check passes; reduced motion respected.
- A short `site/README.md`: how to run, where to edit copy, how to change tokens.
