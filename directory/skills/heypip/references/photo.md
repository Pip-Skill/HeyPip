# Photo and visuals

## Contents
1. Photo style guide
2. Shot list and shoot brief (real photographers)
3. Image-generation prompts
4. Post-production direction
5. Rights and ethics

---

All photo work reads `brand.json → imagery` and `color.palette`. If those are thin, fill them
in first: light, grade, lens, framing, subjects, palette words, avoid-list.

## 1. Photo style guide — `photo/style-guide.md`

```markdown
# Photo style — <Brand>
**In one line:** e.g. "Quiet daylight portraits of making — matte, warm, unhurried."
## Light       — source, direction, hardness, time of day
## Colour      — palette words, white balance, saturation, how the accent appears in frame
## Lens & depth — focal lengths, apertures, distance to subject
## Framing     — composition habits, negative space, crop rules (where type will sit)
## Subjects    — who/what, casting notes, wardrobe, props, locations
## Retouching  — what is allowed, what is not
## Do / Don't  — 5 each, concrete
## Formats     — aspect ratios needed (16:9 hero, 4:5 social, 9:16 stories, 1:1 product)
```

Always plan **where text will sit** on hero images (leave clean space top-left or a side
third) — it saves re-shoots.

## 2. Shot list and shoot brief — `photo/shot-list.md`

For each shot: ID, use (hero / section / social / product), aspect ratio, subject and action,
setting, light, lens, framing and type-space, props/wardrobe, priority (must / nice).
Group shots by location and light to make the day efficient. Add a one-page brief:
objective, references (described), schedule, crew, deliverables (count, formats, deadline).

## 3. Image-generation prompts — `photo/prompts.md`

Write shot ideas as `shots.json`, then expand them so every prompt carries the brand:

```json
[
  {"id": "hero", "kind": "photo", "use": "website hero", "aspect": "16:9",
   "subject": "a tailor's hands pinning raw linen on a wooden table",
   "setting": "small Lisbon atelier, morning", "framing": "subject in right third, clean space left for headline"}
]
```

```bash
python3 scripts/prompt_pack.py <brand>/brand.json <brand>/photo/shots.json <brand>/photo/prompts.md \
  --models midjourney,flux,sdxl
```

The script composes: **subject + action → setting → light → lens/depth → framing → colour
grade + palette words → mood words from `positioning.character`**, and adds each model's
format (Midjourney parameters, Flux natural-language paragraph, SDXL positive/negative).
Review and hand-tune the output — the script gives consistency, you add taste.

Prompt craft that matters for every model:
- Concrete nouns and physical light beat adjectives ("north window light from left" >
  "beautiful lighting").
- Name the camera language (focal length, aperture, angle) for photographic realism.
- Say what is *in* frame and what is *empty* (type space).
- Keep a fixed "brand suffix" (light + grade + palette) across all prompts so a series matches.
- Model syntax and versions change often — keep parameters minimal and tell the user to
  check the current docs of their tool for flags like aspect ratio and style strength.

## 4. Post-production direction

Write grade notes the retoucher or a LUT can follow: white balance target, contrast curve
(lifted blacks? crushed?), saturation per hue (e.g. "pull blues −20, keep rust"), grain
(amount/size), sharpening, skin policy (texture kept, no smoothing), and export specs per
format (sRGB, long edge px, quality, WebP/AVIF for web).

## 5. Rights and ethics

- Don't prompt for living artists' names or trademarked characters; describe the qualities
  instead ("high-contrast black-and-white street photography, 1960s grain").
- Don't generate images of real, identifiable people; for people, describe casting
  (age range, style) and use real models with releases for production.
- Label AI-generated images where the platform or law requires it.
