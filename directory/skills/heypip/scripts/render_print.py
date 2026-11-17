#!/usr/bin/env python3
"""Render on-brand posters, flyers, business cards and social graphics from brand.json + a
small spec, then export print-ready PDF (with bleed) and PNG via headless Chrome.

Usage:
  python3 render_print.py <brand.json> <spec.json> <out_dir> [--export pdf,png] [--fonts <dir with fonts.css>]

spec.json — one piece or a list:
  {
    "id": "launch-poster",
    "format": "A2",              # see FORMATS below, or {"w": 500, "h": 700, "unit": "mm"|"px"}
    "layout": "type-led",        # type-led | image-led | split | big-number | grid | card
    "mode": "light",             # light | dark | accent (ground colour)
    "kicker": "Lisboa · Partida 48",
    "headline": "Made slowly.",
    "sub": "Forty pieces a week. Each one numbered.",
    "body": "",                  # optional paragraph
    "number": "40",              # for big-number
    "meta": ["Graça, Lisboa", "Tue–Sat 10–19"],
    "cta": "lumenloom.example",
    "image": "photo/hero.jpg",   # optional; a labelled placeholder is drawn when missing
    "items": [{"title": "...", "text": "..."}]   # for grid
  }

Print formats get 3 mm bleed in the PDF (tell the printer "3 mm bleed, no crop marks"); keep text inside the safe area
(the script insets content by 5% of the short side + bleed). Digital formats export PNG at 2x.
"""
import html
import json
import shutil
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import brandlib as B  # noqa: E402

e = html.escape

FORMATS = {  # name: (w, h, unit)
    "A6": (105, 148, "mm"), "A5": (148, 210, "mm"), "A4": (210, 297, "mm"), "A3": (297, 420, "mm"),
    "A2": (420, 594, "mm"), "A1": (594, 841, "mm"), "B2": (500, 707, "mm"),
    "poster-50x70": (500, 700, "mm"), "poster-18x24in": (457, 610, "mm"),
    "flyer-DL": (99, 210, "mm"), "letter": (216, 279, "mm"),
    "card-eu": (85, 55, "mm"), "card-us": (89, 51, "mm"), "card-eu-v": (55, 85, "mm"),
    "ig-post": (1080, 1350, "px"), "ig-square": (1080, 1080, "px"), "ig-story": (1080, 1920, "px"),
    "og": (1200, 630, "px"), "x-post": (1600, 900, "px"), "yt-thumb": (1280, 720, "px"),
    "linkedin": (1200, 627, "px"), "banner-wide": (1920, 600, "px"),
}
BLEED_MM = 3
MM_PX = 96 / 25.4


def chrome():
    for c in ("google-chrome", "chromium", "chromium-browser", "chrome",
              "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"):
        p = shutil.which(c) or (c if Path(c).exists() else None)
        if p:
            return p
    return None


def css_for(brand, mode, fonts_css):
    m = B.modes(brand)
    light, dark = m["light"], m.get("dark", m["light"])
    if mode == "dark":
        bg, fg, mu, ac, on = dark["bg"], dark["text"], dark.get("muted", dark["text"]), dark["accent"], dark.get("on-accent", "#fff")
    elif mode == "accent":
        bg, fg = light["accent"], light.get("on-accent", "#fff")
        mu, ac, on = fg, light["text"], light["bg"]
    else:
        bg, fg, mu, ac, on = light["bg"], light["text"], light.get("muted", light["text"]), light["accent"], light.get("on-accent", "#fff")
    fams = brand.get("type", {}).get("families", {})
    disp = B.font_stack(fams.get("display", fams.get("text", {})))
    text = B.font_stack(fams.get("text", {}))
    mono = B.font_stack(fams["mono"]) if fams.get("mono") else text  # no brand mono: labels use the text face
    track = brand.get("type", {}).get("tracking", {})
    r = brand.get("radius", {}).get("md", 6)
    imp = ""
    if fonts_css:
        imp = f'<link rel="stylesheet" href="{fonts_css}">'
    else:
        url = B.google_fonts_url(brand)
        imp = f'<link rel="stylesheet" href="{url}">' if url else ""
    return imp, f"""
:root{{--bg:{bg};--fg:{fg};--mu:{mu};--ac:{ac};--on:{on};--disp:{disp};--text:{text};--mono:{mono};
--td:{track.get('display', '-0.02em')};--tl:{track.get('label', '0.1em')};--r:{r}px}}"""


BASE_CSS = """
*{box-sizing:border-box;margin:0;padding:0}
html,body{background:#888}
.sheet{position:relative;overflow:hidden;background:var(--bg);color:var(--fg);font-family:var(--text);
  container-type:size;-webkit-print-color-adjust:exact;print-color-adjust:exact}
.safe{position:absolute;inset:var(--inset);display:grid}
.k{font:500 2.1cqmin/1.2 var(--mono);letter-spacing:var(--tl);text-transform:uppercase;color:var(--mu)}
.h{font-family:var(--disp);font-weight:500;letter-spacing:var(--td);line-height:.95;text-wrap:balance}
.s{font-size:3.4cqmin;line-height:1.3;color:var(--fg);max-width:34ch;text-wrap:pretty}
.b{font-size:2.3cqmin;line-height:1.5;color:var(--mu);max-width:48ch}
.meta{display:flex;flex-wrap:wrap;gap:.6em 2.4em;font:500 2.1cqmin/1.3 var(--mono);letter-spacing:.04em;color:var(--fg)}
.cta{display:inline-block;background:var(--ac);color:var(--on);font-weight:600;font-size:2.4cqmin;padding:.7em 1.2em;border-radius:var(--r)}
.rule{height:max(1px,.25cqmin);background:currentColor;opacity:.9}
.img{position:relative;background:color-mix(in srgb,var(--fg) 8%,var(--bg));overflow:hidden}
.img img{width:100%;height:100%;object-fit:cover;display:block}
.img .ph{position:absolute;inset:0;display:grid;place-items:center;font:500 1.8cqmin var(--mono);color:var(--mu);
  background:repeating-linear-gradient(135deg,transparent 0 2.2cqmin,color-mix(in srgb,var(--fg) 7%,transparent) 2.2cqmin 2.4cqmin)}
.mark{font-family:var(--disp);font-size:3cqmin;letter-spacing:var(--td)}
/* layouts */
.type-led .safe{grid-template-rows:auto 1fr auto auto;gap:3cqmin}
.type-led .h{font-size:var(--hsize,17cqw);align-self:end}
.image-led .safe{grid-template-rows:1fr auto auto;gap:3cqmin}
.image-led .img{position:absolute;inset:0}
.image-led .shade{position:absolute;inset:0;background:linear-gradient(to top,color-mix(in srgb,var(--bg) 92%,transparent) 0,transparent 55%)}
.image-led .h{font-size:13cqw}
.split .safe{grid-template-columns:1fr 1fr;gap:4cqmin}
.split .col{display:grid;grid-template-rows:auto 1fr auto;gap:3cqmin}
.split .h{font-size:9cqw;align-self:center}
.big-number .safe{grid-template-rows:auto 1fr auto;gap:2cqmin}
.big-number .n{font-family:var(--disp);font-size:var(--nsize,58cqmin);white-space:nowrap;line-height:.9;font-variant-numeric:lining-nums;font-feature-settings:"lnum" 1;margin-bottom:.04em;letter-spacing:-.04em;color:var(--ac)}
.big-number .h{font-size:7cqw}
.grid .safe{grid-template-rows:auto auto 1fr auto;gap:3cqmin}
.grid .h{font-size:13cqw}
.grid .items{display:grid;grid-template-columns:repeat(2,1fr);gap:4cqmin 3cqmin;align-content:end}
.grid .it{border-top:max(1px,.25cqmin) solid currentColor;padding-top:1.5cqmin}
.grid .it b{display:block;font-family:var(--disp);font-weight:500;font-size:6cqmin;margin-bottom:.35em}
.grid .it span{font-size:3.6cqmin;line-height:1.4;color:var(--mu)}
.card .safe{grid-template-rows:1fr auto;gap:2cqmin}
.card .mark{font-size:9cqmin}
.card .meta{font-size:4.2cqmin;flex-direction:column;gap:.3em}
.card .h{font-size:6cqmin;font-family:var(--text);font-weight:600;letter-spacing:0}
@media screen{body{display:grid;place-items:center;min-height:100vh;padding:24px}}
"""


NBSP_LANGS = {"ru", "uk", "be", "bg", "sr", "kk"}


def typeset(sp):
    """Language-aware fixes: no line may start with a dash; short words stick to the next one."""
    if sp.get("lang") not in NBSP_LANGS:
        return sp
    import re as _re
    fix = lambda t: _re.sub(r"(?<=\s)(в|и|с|к|о|у|а|на|по|за|до|от|из|не|для)\s", lambda m: m.group(1) + "\u00a0", t.replace(" —", "\u00a0—").replace(" –", "\u00a0–"))  # noqa: E731
    out = dict(sp)
    for k in ("kicker", "headline", "sub", "body", "cta"):
        if isinstance(out.get(k), str):
            out[k] = fix(out[k])
    if isinstance(out.get("meta"), list):
        out["meta"] = [fix(m) for m in out["meta"]]
    if isinstance(out.get("items"), list):
        out["items"] = [{**i, "title": fix(i.get("title", "")), "text": fix(i.get("text", ""))} for i in out["items"]]
    return out


def layout_html(sp):
    k = f'<div class="k">{e(sp.get("kicker", ""))}</div>' if sp.get("kicker") else "<div></div>"
    h = f'<h1 class="h">{e(sp.get("headline", ""))}</h1>'
    s = f'<p class="s">{e(sp["sub"])}</p>' if sp.get("sub") else ""
    b = f'<p class="b">{e(sp["body"])}</p>' if sp.get("body") else ""
    meta = "".join(f"<span>{e(m)}</span>" for m in sp.get("meta", []))
    meta = f'<div class="meta">{meta}</div>' if meta else ""
    cta = f'<span class="cta">{e(sp["cta"])}</span>' if sp.get("cta") else ""
    mark = f'<div class="mark">{e(sp.get("mark", ""))}</div>' if sp.get("mark") else ""
    src = sp.get("image")
    img = (f'<div class="img"><img src="{e(src)}" alt=""></div>' if src else
           f'<div class="img"><div class="ph">image · {e(sp.get("image_note", sp.get("id", "")))}</div></div>')
    lay = sp.get("layout", "type-led")
    foot = f'<div style="display:flex;justify-content:space-between;align-items:end;gap:3cqmin">{meta}{cta}</div>'
    if lay == "image-led":
        return f'{img}<div class="shade"></div><div class="safe"><div style="display:flex;justify-content:space-between">{k}{mark}</div><div style="align-self:end;display:grid;gap:2.4cqmin">{h}{s}</div>{foot}</div>'
    if lay == "split":
        return f'<div class="safe"><div class="col">{k}<div style="display:grid;gap:2.4cqmin;align-self:center">{h}{s}{b}</div>{foot}</div>{img.replace(chr(34) + "img" + chr(34), chr(34) + "img" + chr(34) + " style=" + chr(34) + "height:100%" + chr(34), 1)}</div>'
    if lay == "big-number":
        return f'<div class="safe"><div style="display:flex;justify-content:space-between">{k}{mark}</div><div style="align-self:center"><div class="n">{e(sp.get("number", ""))}</div><div style="display:grid;gap:2cqmin;margin-top:3cqmin">{h}{s}</div></div>{foot}</div>'
    if lay == "grid":
        items = "".join(f'<div class="it"><b>{e(i.get("title", ""))}</b><span>{e(i.get("text", ""))}</span></div>' for i in sp.get("items", []))
        return f'<div class="safe">{k}<div style="display:grid;gap:2cqmin">{h}{s}</div><div class="items">{items}</div>{foot}</div>'
    if lay == "card":
        return f'<div class="safe">{mark or h}<div style="display:grid;gap:1cqmin">{h if mark else ""}{meta}</div></div>'
    return f'<div class="safe">{k}{h}<div style="display:grid;gap:2cqmin">{s}{b}</div><div class="rule"></div>{foot}</div>'


def render(brand, sp, out_dir, fonts_css):
    fmt = sp.get("format", "A3")
    w, h, unit = (fmt["w"], fmt["h"], fmt.get("unit", "mm")) if isinstance(fmt, dict) else FORMATS[fmt]
    printed = unit == "mm"
    bleed = BLEED_MM if printed else 0
    W, H = w + 2 * bleed, h + 2 * bleed
    if printed:
        inset = f"calc({bleed}{unit} + {round(min(w, h) * 0.05, 2)}{unit})"
    elif fmt == "ig-story":  # Instagram covers the top ~14% and bottom ~20% with its own UI
        side = round(w * 0.07)
        inset = f"{round(h * 0.14)}px {side}px {round(h * 0.20)}px {side}px"
    else:
        inset = f"{round(min(w, h) * 0.06)}px"
    sp = typeset(sp)
    imp, root = css_for(brand, sp.get("mode", "light"), fonts_css)
    # size type to its length: short headlines get big, long ones shrink; big numbers always fit the width
    head = sp.get("headline", "")
    longest = max((len(w) for w in head.split()), default=1)
    hsize = max(9.0, min(24.0, 17.0 * (14 / max(len(head), 1)) ** 0.5, 92.0 / (longest * 0.55)))
    num = str(sp.get("number", ""))
    nsize = f"min(58cqmin, {round(88 / max(len(num) * 0.6, 1), 2)}cqw)"
    extra_vars = f"--hsize:{hsize:.1f}cqw;--nsize:{nsize};"
    page = f"@page{{size:{W}{unit} {H}{unit};margin:0}}@media print{{body{{padding:0;display:block;background:none}}}}"
    doc = f"""<!doctype html><html lang="{e(sp.get('lang', 'en'))}"><head><meta charset="utf-8">
<title>{e(brand.get('name', ''))} — {e(sp.get('id', 'print'))}</title>{imp}
<style>{root}{BASE_CSS}{page}.sheet{{width:{W}{unit};height:{H}{unit};--inset:{inset};{extra_vars}}}</style></head>
<body><div class="sheet {e(sp.get('layout', 'type-led'))}">{layout_html(sp)}</div></body></html>"""
    out = out_dir / f"{sp.get('id', 'piece')}.html"
    out.write_text(doc, encoding="utf-8")
    px_w = int(W * MM_PX) if printed else W
    px_h = int(H * MM_PX) if printed else H
    return out, px_w, px_h, printed


def export(path, px_w, px_h, printed, kinds):
    c = chrome()
    if not c:
        print("  (no Chrome found: open the HTML and print to PDF / screenshot by hand)")
        return
    url = path.resolve().as_uri()
    common = [c, "--headless=new", "--no-sandbox", "--disable-gpu", "--hide-scrollbars", "--virtual-time-budget=3000"]
    if "pdf" in kinds:
        pdf = path.with_suffix(".pdf")
        subprocess.run(common + ["--no-pdf-header-footer", f"--print-to-pdf={pdf}", url], capture_output=True, timeout=120)
        print(f"  pdf  {pdf}" + ("  (includes 3 mm bleed)" if printed else ""))
    if "png" in kinds:
        png = path.with_suffix(".png")
        scale = 2 if not printed else max(1, min(4, round(3600 / max(px_w, px_h), 2)))
        tmp = path.with_name(path.stem + ".shot.html")
        tmp.write_text(path.read_text().replace("@media screen{body{display:grid;place-items:center;min-height:100vh;padding:24px}}", "html,body{background:var(--bg)!important;overflow:hidden}"), encoding="utf-8")
        px_w, px_h = int(px_w), int(px_h)  # floor: a rounded-up size shows a 1px strip of page background
        subprocess.run(common + [f"--window-size={px_w},{px_h}", f"--force-device-scale-factor={scale}",
                                 f"--screenshot={png}", tmp.resolve().as_uri()], capture_output=True, timeout=120)
        tmp.unlink(missing_ok=True)
        print(f"  png  {png}")


def main():
    a = sys.argv[1:]
    if a and a[0] in ("-h", "--help"):
        print(__doc__)
        return
    if len(a) < 3:
        sys.exit(__doc__)
    brand = B.load(a[0])
    specs = json.loads(Path(a[1]).read_text(encoding="utf-8"))
    specs = specs if isinstance(specs, list) else [specs]
    out_dir = Path(a[2])
    out_dir.mkdir(parents=True, exist_ok=True)
    kinds = a[a.index("--export") + 1].split(",") if "--export" in a else []
    fonts = a[a.index("--fonts") + 1] if "--fonts" in a else None
    fonts_css = None
    if fonts:
        fonts_css = Path(fonts, "fonts.css").resolve().as_uri()
    for sp in specs:
        p, w, h, printed = render(brand, sp, out_dir, fonts_css)
        print(f"wrote {p}  ({sp.get('format')}, {sp.get('layout', 'type-led')})")
        if kinds:
            export(p, w, h, printed, kinds)


if __name__ == "__main__":
    main()
