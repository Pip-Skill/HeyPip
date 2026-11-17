# Video and motion

## Contents
1. Formats and structure
2. Script
3. Storyboard
4. Motion brief (UI and brand motion)
5. Video-generation prompts
6. Timing, pacing and sound

---

All video work reads `brand.json → film`, `motion`, `imagery`, `color` and `voice`.

## 1. Formats and structure

| Format | Length | Structure |
|---|---|---|
| Short-form social (Reels/TikTok/Shorts), 9:16 | 6–30s | Hook in first 1.5s → 2–4 beats → payoff + logo/CTA |
| Brand film, 16:9 | 45–90s | Tension → world → product in use → promise → end card |
| Product demo, 16:9 | 30–60s | Problem → 3 key moments in UI → result → CTA |
| Website hero loop | 6–12s, silent, seamless | One continuous mood shot, no text burned in |
| Bumper / ad | 6s | One idea, one visual, logo |

Always state: aspect ratio, length, platform, sound on/off assumption, captions needed.

## 2. Script — `video/script.md`

Two-column script: **Picture** | **Sound/Voice/Text**, with timecodes. Voice-over in the
brand voice, short sentences; on-screen text ≤ 6 words per card and readable for 1.5s+.
Write captions for every spoken line (most social video is watched muted).

## 3. Storyboard — `video/storyboard.html`

One frame per shot: number, timecode, duration, shot size (ECU/CU/MS/WS), camera
(static/dolly/pan/handheld, lens), action, on-screen text, sound, transition out. Build it as
an HTML grid using the brand tokens (simple frame boxes with a composition sketch made of
CSS shapes or a generated still if an image tool is available). Number shots `S01`, `S02`…
so they map 1:1 to prompts and edit decisions.

## 4. Motion brief — `video/motion-brief.md`

For UI and brand motion (logo reveal, transitions, kinetic type):
- character (from `motion.character`) and three motion words;
- durations and easings (from tokens) — the same curves as the website;
- what moves (type, masks, product) and what never moves (logo shape, brand colour fields);
- logo animation: build, hold, exit, total length (≤ 2s for bumpers);
- type in motion rules (`film.type_in_motion`);
- deliverables: aspect ratios, frame rate (24/25 for film feel, 30/60 for UI), codecs.

## 5. Video-generation prompts — `video/prompts.md`

Use the same `shots.json` with `"kind": "video"` and add `duration`, `camera_move`,
`motion` (what moves in frame):

```json
{"id": "S01", "kind": "video", "aspect": "9:16", "duration": 4,
 "subject": "raw linen fabric falling onto a wooden table", "setting": "atelier, morning",
 "camera_move": "slow push-in", "motion": "fabric settles, dust in light beam"}
```

```bash
python3 scripts/prompt_pack.py <brand>/brand.json <brand>/video/shots.json <brand>/video/prompts.md \
  --models runway,kling,luma,veo
```

Video prompt craft:
- One shot = one prompt = one camera move. Describe the move explicitly (static, slow
  push-in, lateral dolly, orbit) and the subject motion separately.
- Start with the strongest visual noun; then camera; then light and grade (brand suffix).
- Keep shots 3–6s; generate several takes; edit them, don't expect one long perfect clip.
- For consistency across shots, reuse the same brand suffix, the same subject description
  wording, and (if the tool supports it) a reference/first frame from the photo set.
- Avoid on-screen text in generated video — add type in the edit with the brand fonts.
- Tools change fast; tell the user to check their tool's current options (duration,
  resolution, reference images, negative prompts).

## 6. Timing, pacing and sound

- Pace from `film.pace`: calm brands hold shots 3–5s; energetic 0.5–1.5s cuts on beat.
- Cut on action or on music downbeats; one transition style for the whole piece.
- Sound design list per shot (room tone, foley, accents) + music direction: tempo (BPM),
  instrumentation, mood, where it peaks; suggest royalty-free sources or a composer brief.
- End card: logo + one line + CTA, held ≥ 2s, safe margins for platform UI (9:16: keep
  text out of top 14% and bottom 20%).
