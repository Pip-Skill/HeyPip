#!/usr/bin/env python3
"""Expand shot ideas into model-specific image/video prompts that all carry the brand look.

Usage:
  python3 prompt_pack.py <brand.json> <shots.json> <out.md> [--models midjourney,flux,sdxl,runway,kling,luma,veo]

shots.json is a list of shots:
  {"id": "hero", "kind": "photo"|"video", "use": "website hero", "aspect": "16:9",
   "subject": "...", "setting": "...", "framing": "...",
   // video only:
   "duration": 4, "camera_move": "slow push-in", "motion": "what moves in frame"}

Model syntax changes often; the script keeps parameters minimal. Check your tool's docs for
current flags (aspect ratio, style strength, negative prompts, durations).
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import _brand as B  # noqa: E402

PHOTO_MODELS = {"midjourney", "flux", "sdxl"}
VIDEO_MODELS = {"runway", "kling", "luma", "veo"}


def brand_suffix(brand):
    img = brand.get("imagery", {})
    parts = [img.get("light"), img.get("lens"), img.get("grade")]
    pw = img.get("palette_words")
    if pw:
        parts.append("palette of " + ", ".join(pw))
    char = brand.get("positioning", {}).get("character")
    if char:
        parts.append("mood: " + ", ".join(char))
    return ", ".join(p for p in parts if p)


def avoid(brand):
    return brand.get("imagery", {}).get("avoid", [])


def core(shot):
    bits = [shot.get("subject"), shot.get("setting"), shot.get("framing")]
    return ", ".join(b for b in bits if b)


def photo_prompt(model, shot, brand):
    suf = brand_suffix(brand)
    ar = shot.get("aspect", "4:5")
    base = core(shot)
    av = avoid(brand)
    if model == "midjourney":
        no = f" --no {', '.join(av)}" if av else ""
        return f"editorial photograph, {base}, {suf} --ar {ar} --style raw{no}"
    if model == "flux":
        txt = (f"An editorial photograph of {shot.get('subject', '')}"
               + (f" in {shot.get('setting')}" if shot.get("setting") else "") + ". "
               + (f"Composition: {shot.get('framing')}. " if shot.get("framing") else "")
               + (f"Light and look: {suf}. " if suf else "")
               + (f"Avoid {', '.join(av)}. " if av else "")
               + f"Aspect ratio {ar}.")
        return txt
    if model == "sdxl":
        pos = f"photograph, {base}, {suf}, high detail, natural texture"
        neg = ", ".join(av + ["text", "watermark", "logo", "extra fingers", "deformed hands", "oversaturated"])
        return f"POSITIVE: {pos}\nNEGATIVE: {neg}\nASPECT: {ar}"
    return base


def video_prompt(model, shot, brand):
    film = brand.get("film", {})
    suf = brand_suffix(brand)
    cam = shot.get("camera_move") or film.get("camera", "static camera")
    motion = shot.get("motion", "")
    dur = shot.get("duration", 4)
    ar = shot.get("aspect", "16:9")
    av = avoid(brand) + ["on-screen text", "logos", "warping faces", "flicker"]
    scene = f"{shot.get('subject', '')}" + (f", {shot.get('setting')}" if shot.get("setting") else "")
    if model == "runway":
        return f"{cam}: {scene}. {motion}. {suf}. Cinematic, {film.get('pace', 'calm pace')}. Duration {dur}s, {ar}."
    if model == "kling":
        return (f"Scene: {scene}\nCamera: {cam}\nAction: {motion}\nLook: {suf}\nDuration: {dur}s · Aspect: {ar}\n"
                f"Negative: {', '.join(av)}")
    if model == "luma":
        return f"{scene}. {motion}. Camera {cam}. {suf}. {ar}, about {dur} seconds."
    if model == "veo":
        sound = film.get("sound")
        return (f"A {dur}-second {ar} shot. {cam.capitalize()} on {scene}. {motion}. "
                f"Visual style: {suf}." + (f" Audio: {sound}." if sound else "") + " No text on screen.")
    return scene


def main():
    if len(sys.argv) < 4:
        sys.exit(__doc__)
    brand = B.load(sys.argv[1])
    shots = json.loads(Path(sys.argv[2]).read_text(encoding="utf-8"))
    out = Path(sys.argv[3])
    models = None
    if "--models" in sys.argv:
        models = [m.strip().lower() for m in sys.argv[sys.argv.index("--models") + 1].split(",") if m.strip()]
    L = [f"# Prompt pack — {brand.get('name', '')}", "",
         f"**Brand suffix (keep identical across the series):** {brand_suffix(brand)}", "",
         f"**Avoid:** {', '.join(avoid(brand)) or '—'}", "",
         "_Model syntax changes often — check your tool's current docs for flags._", ""]
    for s in shots:
        kind = s.get("kind", "photo")
        pool = PHOTO_MODELS if kind == "photo" else VIDEO_MODELS
        use = [m for m in (models or sorted(pool)) if m in pool] or sorted(pool)
        L.append(f"## {s.get('id', '?')} — {s.get('use', kind)} ({s.get('aspect', '')}{', ' + str(s.get('duration')) + 's' if kind == 'video' else ''})")
        L.append("")
        for m in use:
            p = photo_prompt(m, s, brand) if kind == "photo" else video_prompt(m, s, brand)
            L.append(f"**{m.title()}**")
            L.append("```")
            L.append(p)
            L.append("```")
        L.append("")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text("\n".join(L), encoding="utf-8")
    print(f"wrote {out} ({len(shots)} shots)")


if __name__ == "__main__":
    main()
