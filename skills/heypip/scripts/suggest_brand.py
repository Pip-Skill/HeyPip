#!/usr/bin/env python3
"""Draft a complete brand.json from a one-line product description, grounded in the design
library (product -> style -> palette -> font pairing), with contrast fixed automatically.

Usage:
  python3 suggest_brand.py "<what it is and for whom>" [--name "Brand"] [--lang ru|en|de|de,ru ...]
                           [--style "<style name>"] [--out brand.json] [--alternatives 3]

Examples:
  python3 suggest_brand.py "invoicing SaaS for freelancers" --name Ledgerly --lang ru --out brand.json
  python3 suggest_brand.py "specialty coffee roastery with a cafe" --alternatives 3

This is a starting point for phase 3, not a replacement for Direction: read the printed
rationale, then edit positioning, voice and imagery by hand. Then run check_contrast.py and
build_tokens.py as usual. Write the description in English (the library is English); the
brand's languages go in --lang, comma-separated for several ("de,ru"). --lang makes the font pairing cover that language's script
(ru/uk/bg/sr -> cyrillic, el -> greek, vi -> vietnamese).
"""
import csv
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import _brand as B  # noqa: E402
from lookup import LIB, search  # noqa: E402

SCRIPT_FOR_LANG = {"ru": "cyrillic", "uk": "cyrillic", "be": "cyrillic", "bg": "cyrillic", "sr": "cyrillic",
                   "kk": "cyrillic", "el": "greek", "vi": "vietnamese"}
SERIF_CATS = ("serif", "slab")


# ---------- colour helpers ----------
def hex2rgb(h):
    h = B.norm_hex(h).lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def rgb2hex(c):
    return "#" + "".join(f"{max(0, min(255, round(v))):02X}" for v in c)


def mix(a, b, t):
    ca, cb = hex2rgb(a), hex2rgb(b)
    return rgb2hex([x + (y - x) * t for x, y in zip(ca, cb)])


def fix_contrast(fg, bg, need):
    """Move fg toward black or white (whichever helps) until it meets `need` against bg."""
    if B.contrast(fg, bg) >= need:
        return fg
    target = "#000000" if B.luminance(bg) > 0.4 else "#FFFFFF"
    for i in range(1, 41):
        c = mix(fg, target, i / 40)
        if B.contrast(c, bg) >= need:
            return c
    return target


def best_on(bg):
    return "#FFFFFF" if B.contrast("#FFFFFF", bg) >= B.contrast("#111111", bg) else "#111111"


def accent_pair(acc, bg, need_bg=3.0):
    """Return (accent, on_accent): label on the button passes 4.5:1 and the button stands out from bg."""
    on = best_on(acc)
    toward = "#000000" if on == "#FFFFFF" else "#FFFFFF"
    for i in range(0, 41):
        c = mix(acc, toward, i / 40)
        if B.contrast(on, c) >= 4.5 and B.contrast(c, bg) >= need_bg:
            return c, on
    other = "#111111" if on == "#FFFFFF" else "#FFFFFF"
    toward = "#FFFFFF" if other == "#111111" else "#000000"
    for i in range(0, 41):
        c = mix(acc, toward, i / 40)
        if B.contrast(other, c) >= 4.5 and B.contrast(c, bg) >= need_bg:
            return c, other
    return acc, on


# ---------- font helpers ----------
_fonts = None


def font_info(name):
    global _fonts
    if _fonts is None:
        with open(LIB / "google-fonts.csv", newline="", encoding="utf-8") as f:
            _fonts = {r["Family"].lower(): r for r in csv.DictReader(f)}
    return _fonts.get(name.lower())


def covers(name, script):
    if not script:
        return True
    info = font_info(name)
    return bool(info) and script in [s.strip() for s in info["Subsets"].split("|")]


def weights_of(name, want):
    info = font_info(name)
    if not info:
        return want
    have = {int(x) for x in re.findall(r"\d+", info["Styles"])}
    return [w for w in want if w in have] or sorted(have)[:2]


def fallback_for(name):
    info = font_info(name) or {}
    cat = info.get("Category", "").lower()
    if cat in ("serif",):
        return "Georgia, 'Times New Roman', serif"
    if "mono" in cat or "monospace" in cat:
        return "ui-monospace, Menlo, monospace"
    return "system-ui, -apple-system, 'Segoe UI', sans-serif"


# ---------- style -> numbers ----------
def style_numbers(style_row):
    v = (style_row or {}).get("Design System Variables", "") + " " + (style_row or {}).get("Keywords", "")
    m = re.search(r"--border-radius:\s*(\d+)px", v)
    r = int(m.group(1)) if m else None
    low = v.lower()
    if r is None:
        r = 0 if any(k in low for k in ("brutal", "swiss", "sharp")) else 16 if any(k in low for k in ("playful", "bubbly", "rounded", "soft")) else 8
    flat = "shadow: none" in low or "flat" in low or "brutal" in low
    calm = any(k in low for k in ("calm", "minimal", "luxury", "elegant", "editorial"))
    lively = any(k in low for k in ("playful", "bouncy", "energetic", "motion-driven", "kinetic"))
    return r, flat, ("calm" if calm else "lively" if lively else "neutral")


def build(desc, name, lang, style_hint, product, reason, style_row, colors, pair, alt_note):
    script = next((SCRIPT_FOR_LANG[l.strip()] for l in (lang or "").split(",") if l.strip() in SCRIPT_FOR_LANG), None)
    # palette
    P = {
        "primary": colors["Primary"], "secondary": colors["Secondary"], "accent": colors["Accent"],
        "background": colors["Background"], "foreground": colors["Foreground"], "card": colors["Card"],
        "muted": colors["Muted"], "muted-fg": colors["Muted Foreground"], "border": colors["Border"],
        "danger": colors["Destructive"],
    }
    P = {k: B.norm_hex(v) for k, v in P.items() if re.match(r"#[0-9A-Fa-f]{6}", v or "")}
    bg, fg = P["background"], P["foreground"]
    import colorsys
    def sat(c):  # chroma: how much colour there is, regardless of lightness
        v = hex2rgb(c)
        return (max(v) - min(v)) / 255
    candidates = [c for c in (P["primary"], P.get("accent"), P.get("secondary")) if c]
    vivid = [c for c in candidates if sat(c) >= 0.3]
    base_action = (vivid or candidates)[0]  # first brand colour that is actually a colour, not grey
    action, on_action = accent_pair(base_action, bg)
    darker_ground = lambda a, b: a if B.luminance(a) < B.luminance(b) else b  # noqa: E731
    lighter_ground = lambda a, b: b if B.luminance(a) < B.luminance(b) else a  # noqa: E731
    muted = fix_contrast(P["muted-fg"], darker_ground(bg, P.get("card", bg)) if B.luminance(bg) > 0.4 else lighter_ground(bg, P.get("card", bg)), 4.5)
    # dark mode, derived
    night = mix("#121316", fg, 0.35) if B.luminance(fg) < 0.2 else "#121316"
    night2 = mix(night, "#FFFFFF", 0.06)
    d_text = bg if B.contrast(bg, night) >= 7 else "#F2F2F2"
    d_accent, d_on = accent_pair(mix(base_action, "#FFFFFF", 0.3), night)
    d_muted = fix_contrast(mix(P["muted-fg"], "#FFFFFF", 0.35), night2, 4.5)
    P["night"], P["night-2"] = night, night2
    dark_first = B.luminance(bg) < 0.2
    if dark_first:
        paper = mix("#FAFAF9", fg, 0.04)
        P["night"], P["night-2"] = bg, P.get("card", night2)
        P["paper"], P["paper-2"] = paper, mix(paper, "#000000", 0.03)
        l_text = mix(bg, "#000000", 0.2)
        l_action, l_on = accent_pair(base_action, paper)
        light_mode = {"bg": "paper", "surface": "paper-2", "text": l_text,
                      "muted": fix_contrast(mix(P["muted-fg"], "#000000", 0.3), P["paper-2"], 4.5),
                      "accent": l_action, "on-accent": l_on, "border": mix(paper, "#000000", 0.12), "focus": l_action}
        dark_mode = {"bg": "night", "surface": "night-2", "text": fg,
                     "muted": fix_contrast(P["muted-fg"], P["night-2"], 4.5),
                     "accent": action, "on-accent": on_action, "border": "border", "focus": action}
    radius, flat, motion = style_numbers(style_row)
    head, body = pair["Heading Font"].strip(), pair["Body Font"].strip()
    head_serif = (font_info(head) or {}).get("Category", "").lower() in SERIF_CATS
    brand = {
        "name": name or "Untitled",
        "lang": (lang or "en").split(",")[0].strip(),
        "version": "0.1.0",
        "tagline": "",
        "_generated": {
            "by": "heypip/suggest_brand.py — a draft; edit positioning, voice and imagery by hand",
            "from": desc,
            "product_match": product["Product Type"],
            "style": style_row["Style Category"] if style_row else product["Primary Style Recommendation"],
            "font_pairing": pair["Font Pairing Name"],
            "landing_pattern": product.get("Landing Page Pattern"),
            "anti_patterns": (reason or {}).get("Anti_Patterns"),
            "notes": alt_note,
        },
        "positioning": {
            "category": product["Product Type"],
            "difference": "TODO: one sentence on what only this brand can say",
            "character": [w.strip() for w in re.split(r"[,+]", (reason or {}).get("Typography_Mood", "clear, confident")) if w.strip()][:3],
            "is": [], "is_not": [w.strip() for w in re.split(r"[+,]", (reason or {}).get("Anti_Patterns", "")) if w.strip()][:3],
        },
        "voice": {"tone": [], "do": [], "dont": [], "examples": []},
        "color": {
            "palette": P,
            "light": light_mode if dark_first else {"bg": "background", "surface": "card", "text": "foreground", "muted": muted,
                      "accent": action, "on-accent": on_action, "border": "border", "focus": action,
                      "danger": "danger"},
            "dark": dark_mode if dark_first else {"bg": "night", "surface": "night-2", "text": d_text, "muted": d_muted,
                     "accent": d_accent, "on-accent": d_on, "border": mix(night, "#FFFFFF", 0.16),
                     "focus": d_accent},
            "default_mode": "dark" if dark_first else "light",
            "usage": f"{(colors.get('Notes') or product.get('Color Palette Focus', '')).strip()}. Accent only for the main action and active states.",
        },
        "type": {
            "families": {
                "display": {"name": head, "fallback": fallback_for(head), "source": "google",
                            "weights": weights_of(head, [500, 600] if head_serif else [600, 700])},
                "text": {"name": body, "fallback": fallback_for(body), "source": "google",
                         "weights": weights_of(body, [400, 500, 600])},
            },
            "base": 17 if head_serif else 16,
            "ratio": 1.333 if head_serif else 1.25,
            "steps": {"xs": -1.25, "sm": -0.5, "base": 0, "lg": 1, "xl": 2, "2xl": 3, "3xl": 4, "4xl": 5, "5xl": 6},
            "leading": {"tight": 1.08 if head_serif else 1.1, "snug": 1.3, "body": 1.6},
            "tracking": {"display": "-0.02em", "body": "0", "label": "0.08em"},
        },
        "space": {"base": 4, "scale": [0, 1, 2, 3, 4, 6, 8, 12, 16, 24, 32]},
        "radius": {"none": 0, "sm": max(0, radius // 2), "md": radius, "lg": radius * 2 if radius else 0, "pill": 999},
        "border": {"width": 2 if "brutal" in (style_row or {}).get("Style Category", "").lower() else 1},
        "elevation": {"0": "none", "1": "none" if flat else "0 1px 2px rgba(0,0,0,.06)",
                      "2": "none" if flat else "0 12px 32px -16px rgba(0,0,0,.22)"},
        "motion": {
            "character": motion,
            "duration": {"fast": 120, "base": 280 if motion == "calm" else 200, "slow": 520 if motion == "calm" else 360},
            "easing": {"standard": "cubic-bezier(.2,0,0,1)", "enter": "cubic-bezier(0,0,0,1)", "exit": "cubic-bezier(.3,0,1,1)"},
            "rules": [(reason or {}).get("Key_Effects", ""), "Honour prefers-reduced-motion"],
        },
        "layout": {"maxWidth": 1240, "columns": 12, "gutter": 24, "margin": 24,
                   "breakpoints": {"sm": 640, "md": 768, "lg": 1024, "xl": 1280}},
        "components": {
            "button": {"radius": "md", "height": 48, "weight": 600, "variants": ["primary", "secondary", "ghost"]},
            "card": {"radius": "lg", "elevation": "0" if flat else "1", "padding": 6},
            "input": {"radius": "md", "height": 48},
        },
        "imagery": {"light": "", "grade": "", "lens": "", "framing": "", "subjects": "",
                    "palette_words": [], "avoid": ["stock smiles", "generic office stock", "AI-gloss skin"]},
        "film": {"pace": "", "camera": "", "cuts": "", "sound": "", "type_in_motion": ""},
        "logo": {"wordmark": name or "", "file": None},
    }
    if script and not (covers(head, script) and covers(body, script)):
        brand["_generated"]["warning"] = f"pairing may lack {script}; run fetch_fonts.py to confirm"
    return brand


def is_script_face(name):
    return (font_info(name) or {}).get("Category", "").lower() in ("handwriting", "script")


def pick_pair(query, script, n=12):
    hits = search("type", query, n)
    if "script" not in query.lower() and "handwrit" not in query.lower():
        hits = [h for h in hits if not is_script_face(h[1]["Heading Font"].strip())] or hits
    if hits:
        top = hits[0][0]
        close = [h for h in hits if h[0] >= 0.75 * top]
        distinct = [h for h in close if h[1]["Heading Font"].strip() != h[1]["Body Font"].strip()]
        hits = distinct + [h for h in hits if h not in distinct]
    for _, row in hits:
        if covers(row["Heading Font"].strip(), script) and covers(row["Body Font"].strip(), script):
            return row, None
    if hits:
        return hits[0][1], f"no top pairing covers {script}; kept the best match — swap fonts by hand"
    with open(LIB / "typography.csv", newline="", encoding="utf-8") as f:
        return next(csv.DictReader(f)), "no font match; default pairing"


def main():
    a = sys.argv[1:]
    if a and a[0] in ("-h", "--help"):
        print(__doc__)
        return
    if not a or a[0].startswith("-"):
        sys.exit(__doc__)
    desc = a[0]
    opt = lambda k, d=None: a[a.index(k) + 1] if k in a else d  # noqa: E731
    name, lang, style_hint, out = opt("--name"), opt("--lang"), opt("--style"), opt("--out")
    alts = int(opt("--alternatives", 1))
    langs = [l.strip() for l in (lang or "").split(",") if l.strip()]
    scripts_needed = sorted({SCRIPT_FOR_LANG[l] for l in langs if l in SCRIPT_FOR_LANG})
    script = scripts_needed[0] if scripts_needed else None
    if sum(1 for ch in desc if ord(ch) > 127) > len(desc) * 0.3:
        print("note: the description is not in English; the library is English — pass a short English "
              "description (the brand's language goes in --lang)", file=sys.stderr)
    products = search("product", desc, max(alts, 1))
    if not products:
        # nothing matched: fall back to the broadest local-business type and say so
        products = search("product", "hyperlocal services", 1)
        print("note: no product type matched this description; started from 'Hyperlocal Services' — "
              "rerun with plainer words (what it is, for whom) or --style", file=sys.stderr)
    results = []
    if alts > 1 and len(products) < alts:
        print(f"note: only {len(products)} product type(s) matched; add plainer English words for more options",
              file=sys.stderr)
    for _, product in products[:alts]:
        reason = next((r for _, r in search("reason", product["Product Type"], 3) if r["UI_Category"] == product["Product Type"]), None)
        colors = next((r for _, r in search("color", product["Product Type"], 5) if r["Product Type"] == product["Product Type"]), None)
        if colors is None:
            colors = search("color", desc, 1)[0][1]
        style_q = style_hint or product["Primary Style Recommendation"].split("+")[0]
        if not style_hint:
            from lookup import tokens as _tok
            dt = set(_tok(desc))
            for _, srow in search("style", desc, 3):
                if any(w in dt and len(w) > 4 for w in _tok(srow["Style Category"] + " " + srow.get("Aliases", ""))):
                    style_q = srow["Style Category"]
                    break
        st = search("style", style_q, 1)
        style_row = st[0][1] if st else None
        tq = " ".join([desc, (reason or {}).get("Typography_Mood", ""), style_q])
        pair, note = pick_pair(tq, script)
        results.append(build(desc, name, lang, style_hint, product, reason, style_row, colors, pair, note))
    for i, br in enumerate(results, 1):
        g = br["_generated"]
        L = br["color"]["light"]
        print(f"[{i}] {g['product_match']} → style: {g['style']} · fonts: {br['type']['families']['display']['name']} + "
              f"{br['type']['families']['text']['name']} · accent {L['accent']} · landing: {g['landing_pattern']}",
              file=sys.stderr)
        if g.get("anti_patterns"):
            print(f"    avoid: {g['anti_patterns']}", file=sys.stderr)
        if g.get("notes") or g.get("warning"):
            print(f"    note: {g.get('notes') or g.get('warning')}", file=sys.stderr)
    data = results[0] if alts == 1 else results
    text = json.dumps(data, ensure_ascii=False, indent=2)
    if out:
        Path(out).write_text(text + "\n", encoding="utf-8")
        print(f"wrote {out}", file=sys.stderr)
    else:
        print(text)


if __name__ == "__main__":
    main()
