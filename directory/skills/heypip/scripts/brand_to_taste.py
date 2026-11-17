#!/usr/bin/env python3
"""Bridge brand.json -> the web engine (taste/). Prints the engine's :root block in the brand's
own colours and type, so a page built by taste/ENGINE.md is on-brand.

Usage:
  python3 brand_to_taste.py <brand.json> --page software|gaming|tech|product|service|place [--out root.css]

What it does:
  1. takes bg / text / accent / surface / muted from brand.json (light mode),
  2. picks the engine pairing (library/type.json) that matches the brand's display font,
     else the closest one of the same class (serif / sans) that suits the page kind,
  3. maps the brand radius to sharp / soft / round,
  4. runs `node taste/scripts/start.mjs brand ...` and prints its block,
  5. if the brand's fonts are not that pairing's, appends overrides for --font-display/--font-text/--font-mono
     and prints the Google Fonts link for the brand's own fonts.
Use the printed block in place of `start.mjs css` (ENGINE.md section 4, the deal step), as the engine
says for a client's own colours.
"""
import json
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import brandlib as B  # noqa: E402

ENGINE_SRC = HERE.parent / "taste"
WORK = Path("/tmp/taste-skill")


def ensure_engine():
    """The engine ships its assets packed; work from an unpacked copy (ENGINE.md, 'First, every session')."""
    if (ENGINE_SRC / "assets" / "effects").is_dir():
        return ENGINE_SRC
    if not (WORK / "assets" / "effects").is_dir():
        import shutil
        if WORK.exists():
            shutil.rmtree(WORK)
        shutil.copytree(ENGINE_SRC, WORK)
        if (WORK / "assets.tar.gz").exists() and not (WORK / "assets").exists():
            subprocess.run(["tar", "-xzf", "assets.tar.gz"], cwd=WORK, check=True)
    return WORK


ENGINE = ENGINE_SRC
PAGES = ["software", "gaming", "tech", "product", "service", "place"]
SERIF_HINTS = ("serif", "garamond", "fraunces", "literata", "lora", "newsreader", "vollkorn", "besley",
               "cormorant", "playfair", "libre baskerville", "dm serif", "instrument serif", "zilla", "slab")


def is_serif(fam):
    name = (fam.get("name", "") + " " + fam.get("fallback", "")).lower()
    return any(h in name for h in SERIF_HINTS) and "sans-serif" not in fam.get("fallback", "").lower().split(",")[0]


def pick_type(types, disp, text, page):
    def suits(t):
        return page == "place" or page in t.get("kinds", {})
    dn, tn = disp.get("name", "").lower(), text.get("name", "").lower()
    exact = [t for t in types if t["display"]["family"].lower() == dn and t["text"]["family"].lower() == tn]
    if exact:
        return exact[0], True
    same_disp = [t for t in types if t["display"]["family"].lower() == dn]
    if same_disp:
        return sorted(same_disp, key=lambda t: not suits(t))[0], False
    want_serif = is_serif(disp)
    pool = [t for t in types if (t["class"] in ("serif", "slab")) == want_serif and suits(t)]
    pool = pool or [t for t in types if suits(t)] or types
    pool.sort(key=lambda t: -t.get("kinds", {}).get(page, 0))
    return pool[0], False


def radius_word(brand):
    r = brand.get("radius", {})
    comp = brand.get("components", {}).get("button", {}).get("radius", "md")
    px = r.get(comp, r.get("md", 6)) if isinstance(r, dict) else 6
    return "sharp" if px <= 2 else ("round" if px >= 16 else "soft")


def main():
    a = sys.argv[1:]
    if not a or "--page" not in a:
        sys.exit(__doc__)
    brand = B.load(a[0])
    page = a[a.index("--page") + 1]
    if page not in PAGES:
        sys.exit(f"--page must be one of {', '.join(PAGES)}")
    out = a[a.index("--out") + 1] if "--out" in a else None
    light = B.modes(brand)["light"]
    fams = brand.get("type", {}).get("families", {})
    disp = fams.get("display", fams.get("text", {}))
    text = fams.get("text", disp)
    mono = fams.get("mono")
    global ENGINE
    ENGINE = ensure_engine()
    types = json.loads((ENGINE / "library" / "type.json").read_text())
    t, exact = pick_type(types, disp, text, page)
    cmd = ["node", str(ENGINE / "scripts" / "start.mjs"), "brand",  # runs from the engine copy "--page", page,
           "--bg", light["bg"], "--ink", light["text"], "--accent", light["accent"],
           "--type", t["id"], "--radius", radius_word(brand), "--force"]
    for role, flag in (("surface", "--surface"), ("muted", "--muted")):
        if role in light:
            cmd += [flag, light[role]]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode:
        sys.exit(r.stderr or r.stdout)
    block = r.stdout.rstrip()
    lang = brand.get("lang") or ""
    # drop the engine pairing's own Google Fonts lines: the brand's fonts replace them
    if not exact:
        block = "\n".join(l for l in block.splitlines()
                          if "fonts.googleapis.com" not in l and "fonts.gstatic.com" not in l)
    if lang:
        block = block.replace('<html lang="en"', f'<html lang="{lang}"')
    extra = []
    if not exact:
        extra.append(f"<style>/* brand fonts from brand.json (engine pairing '{t['id']}' kept for weights and tracking) */")
        extra.append(":root {")
        extra.append(f"  --font-display: {B.font_stack(disp)};")
        extra.append(f"  --font-text: {B.font_stack(text)};")
        if mono:
            extra.append(f"  --font-mono: {B.font_stack(mono)};")
        dw = sorted(disp.get("weights") or [400])
        extra.append(f"  --display-weight: {dw[0] if len(dw) == 1 else dw[len(dw) // 2]};  /* a weight the brand actually loads */")
        extra.append("}</style>")
        url = B.google_fonts_url(brand)
        if url:
            extra.append(f'<link rel="stylesheet" href="{url}">  <!-- before delivery self-host instead: '
                         'python3 scripts/fetch_fonts.py brand.json site/fonts, then link fonts/fonts.css -->')
    result = block + "\n" + "\n".join(extra)
    print(f"# engine pairing: {t['id']} ({'exact match' if exact else 'closest; brand fonts override below'})", file=sys.stderr)
    print("# command: " + " ".join(cmd), file=sys.stderr)
    if out:
        Path(out).write_text(result + "\n", encoding="utf-8")
        print(f"wrote {out}", file=sys.stderr)
    else:
        print(result)


if __name__ == "__main__":
    main()
