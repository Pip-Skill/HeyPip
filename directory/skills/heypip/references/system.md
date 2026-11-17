# Design system

## Contents
1. `brand.json` — the source of truth (schema)
2. Deriving tokens from the direction
3. Components
4. Accessibility and responsive rules
5. Generating outputs
6. Working from an existing system

---

## 1. `brand.json` schema

Copy `templates/brand.example.json` and edit. Every key below is read by the scripts.
Colour roles may reference a palette name (`"ink"`) or a hex (`"#111111"`).

```jsonc
{
  "name": "Lumen & Loom",
  "version": "1.0.0",
  "tagline": "Made slowly, in Lisbon.",
  "positioning": {
    "category": "...", "difference": "...",
    "character": ["quiet", "tactile", "defiant"],
    "is": ["..."], "is_not": ["..."]
  },
  "voice": { "tone": ["..."], "do": ["..."], "dont": ["..."], "examples": ["headline 1", "..."] },

  "color": {
    "palette": { "bone": "#EFE9DF", "ink": "#1E1B17", "rust": "#B5532D", "...": "..." },
    "light": {                              // semantic roles, used everywhere
      "bg": "bone", "surface": "#F7F3EC", "text": "ink", "muted": "#5E574D",
      "accent": "rust", "on-accent": "#FFFFFF", "border": "#D9CFBF", "focus": "rust"
    },
    "dark": { "bg": "#151310", "surface": "#1F1C18", "text": "#EFE9DF", "...": "..." },   // optional
    "pairs": [["text","bg"], ["muted","bg"], ["text","surface"], ["on-accent","accent"]],   // optional extra checks
    "usage": "70% bone, 20% ink, 10% rust (rust only for actions)"
  },

  "type": {
    "families": {
      "display": { "name": "Fraunces", "fallback": "Georgia, serif", "source": "google", "weights": [400, 600] },
      "text":    { "name": "Inter", "fallback": "system-ui, sans-serif", "source": "google", "weights": [400, 500, 600] },
      "mono":    { "name": "JetBrains Mono", "fallback": "ui-monospace, monospace", "source": "google", "weights": [400] }
    },
    "base": 17,              // px, body size
    "ratio": 1.25,           // modular scale
    "steps": { "xs": -2, "sm": -1, "base": 0, "lg": 1, "xl": 2, "2xl": 3, "3xl": 4, "4xl": 5, "5xl": 6, "6xl": 7 },
    "leading": { "tight": 1.05, "snug": 1.25, "body": 1.6 },
    "tracking": { "display": "-0.02em", "body": "0", "label": "0.1em" }
  },

  "space":  { "base": 4, "scale": [0, 1, 2, 3, 4, 6, 8, 12, 16, 24, 32] },   // multiples of base
  "radius": { "none": 0, "sm": 2, "md": 4, "lg": 8, "pill": 999 },
  "border": { "width": 1 },
  "elevation": { "0": "none", "1": "0 1px 2px rgba(30,27,23,.06)", "2": "0 8px 24px -12px rgba(30,27,23,.18)" },
  "motion": {
    "character": "calm",
    "duration": { "fast": 140, "base": 260, "slow": 520 },
    "easing": { "standard": "cubic-bezier(.2,0,0,1)", "enter": "cubic-bezier(0,0,0,1)", "exit": "cubic-bezier(.3,0,1,1)" },
    "rules": ["Only opacity and translate under 16px", "No looping animation outside loaders"]
  },
  "layout": { "maxWidth": 1240, "columns": 12, "gutter": 24, "margin": 32,
              "breakpoints": { "sm": 640, "md": 768, "lg": 1024, "xl": 1280 } },

  "components": {             // short rules, rendered in the brand book
    "button": { "radius": "md", "height": 48, "weight": 600, "variants": ["primary", "secondary", "ghost"] },
    "card":   { "radius": "lg", "elevation": "1", "padding": 6 },
    "input":  { "radius": "md", "height": 48 }
  },

  "imagery": {
    "light": "soft north-window daylight, low contrast",
    "grade": "matte, warm highlights, lifted blacks, no teal-orange",
    "lens": "50mm and 85mm, f/2–f/2.8, shallow depth of field",
    "framing": "asymmetric, generous negative space, hands and textures over faces",
    "subjects": "makers at work, raw linen, finished garments on real people",
    "palette_words": ["bone", "oat", "rust", "ink"],
    "avoid": ["studio seamless white", "heavy retouching", "stock smiles", "neon"]
  },
  "film": {
    "pace": "slow, 3–5s shots", "camera": "locked-off or slow dolly, no whip pans",
    "cuts": "straight cuts on action, occasional match cut", "sound": "room tone, scissors, loom, sparse piano",
    "type_in_motion": "display serif, fades only, 500ms"
  },
  "logo": { "wordmark": "Lumen & Loom", "file": null }
}
```

## 2. Deriving tokens from the direction

Translate words into numbers deliberately, and write the reason in `direction.md`:

- **Colour.** Start from 2–3 neutrals (ground, text, a mid) + 1 accent; add a second accent
  only with a defined job. Assign roles before hexes. Check contrast with
  `scripts/check_contrast.py` and adjust lightness, not hue, to pass.
  Dark mode is not "invert": lift the ground to ~#121212–#1A1A1A territory, desaturate the
  accent slightly, and re-check every pair.
- **Type.** Pair by contrast of purpose (display with character + neutral text face).
  Ratio: 1.2 for dense UI, 1.25 general, 1.333–1.5 editorial/marketing. Body 16–18px on web.
  Only load the weights you use. Prefer fonts with the scripts the brand needs (Cyrillic,
  Greek, Vietnamese) — check this, it is the most common silent failure.
- **Space.** Base 4 for dense products, 8 for marketing. Sections breathe in big steps
  (64–128px); components in small ones.
- **Radius.** Sharp (0–2) = authority/editorial; soft (6–12) = friendly product; round
  (16+/pill) = playful. One philosophy, applied everywhere.
- **Elevation.** Flat brands use borders; soft brands use 1–2 shadow levels. Never more than 3.
- **Motion.** Calm = 240–520ms, opacity/short translate. Snappy = 120–200ms. Elastic =
  spring with overshoot, only for playful brands. Always honour reduced motion.

## 3. Components

Define the core set as rules (in `brand.json → components`) and, for web work, as code:
button (primary/secondary/ghost, sizes, states: hover, active, focus-visible, disabled,
loading), link, input/textarea/select (with label, help, error), checkbox/radio/switch,
card, badge/tag, nav (desktop + mobile), footer, modal/sheet, toast, tabs, table, empty
state. Each component uses only tokens. Document "use when / don't use when" for each in
the brand book.

## 4. Accessibility and responsive rules

- Text contrast ≥ 4.5:1 (≥ 3:1 for ≥ 24px or ≥ 18.66px bold), UI boundaries and focus ≥ 3:1.
- Focus ring visible on every interactive element (2px+ outline, offset 2px, `focus` colour).
- Touch targets ≥ 44×44px; spacing between targets ≥ 8px.
- Never encode meaning by colour alone (pair with icon/text).
- `prefers-reduced-motion`: disable transforms and long transitions, keep opacity ≤ 150ms.
- Type scales down at `sm`: display sizes use `clamp()` (the scripts emit fluid sizes for
  `3xl`+).
- Content max width ~65–75ch for reading text.

## 5. Generating outputs

```bash
python3 scripts/check_contrast.py <brand>/brand.json          # fix failures first
python3 scripts/build_tokens.py <brand>/brand.json <brand>/tokens
python3 scripts/render_brandbook.py <brand>/brand.json <brand>/brandbook.html
```

`tokens/` then contains:
- `tokens.css` — CSS custom properties (`--color-bg`, `--text-2xl`, `--space-6`, …), light by
  default, dark under `[data-theme="dark"]` and `prefers-color-scheme: dark`.
- `tokens.tailwind.css` — Tailwind v4 `@theme` block (import after `@import "tailwindcss"`).
- `tailwind.preset.js` — Tailwind v3 preset (`presets: [require('./tokens/tailwind.preset.js')]`).
- `tokens.dtcg.json` — W3C Design Tokens format (Figma via Tokens Studio, Style Dictionary).
- `tokens.ts` — typed object for React/Next/React Native.

## 6. Working from an existing system

Read their CSS/Tailwind config/Figma export, map what exists into `brand.json` (keep their
names in `palette`), note inconsistencies (e.g. 14 greys, 6 radii) in `review.md`, propose a
consolidated scale, and only then generate. Never silently change a brand colour the user
didn't ask to change.
