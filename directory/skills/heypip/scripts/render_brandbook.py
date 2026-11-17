#!/usr/bin/env python3
"""Render a one-page brand book (HTML) from brand.json.

Usage: python3 render_brandbook.py <brand.json> <out.html> [--fonts <dir with fonts.css>]

--fonts links self-hosted fonts (from fetch_fonts.py) instead of Google Fonts, relative to the page.
"""
import html
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import brandlib as B  # noqa: E402

e = html.escape


def badge(ratio):
    if ratio >= 7:
        return "AAA"
    if ratio >= 4.5:
        return "AA"
    if ratio >= 3:
        return "AA large"
    return "fail"


def main():
    a = sys.argv[1:]
    fonts_dir = None
    if "--fonts" in a:
        i = a.index("--fonts"); fonts_dir = a[i + 1]; del a[i:i + 2]
    if len(a) != 2:
        sys.exit(__doc__)
    brand = B.load(a[0])
    out = Path(a[1])
    modes = B.modes(brand)
    light = modes["light"]
    pal = B.palette_hex(brand)
    t = brand.get("type", {})
    fams = t.get("families", {})
    scale = B.type_scale(brand)
    space = B.space_scale(brand)
    radius = brand.get("radius", {})
    elev = brand.get("elevation", {})
    motion = brand.get("motion", {})
    pos = brand.get("positioning", {})
    voice = brand.get("voice", {})
    img = brand.get("imagery", {})
    film = brand.get("film", {})
    comps = brand.get("components", {})
    name = brand.get("name", "Brand")
    url = B.google_fonts_url(brand)
    if fonts_dir:
        import os
        url = os.path.relpath(Path(fonts_dir, "fonts.css").resolve(), Path(out).resolve().parent)
    disp = B.font_stack(fams.get("display", fams.get("text", {})))
    text = B.font_stack(fams.get("text", {}))
    mono = B.font_stack(fams.get("mono", {"fallback": "ui-monospace, monospace"}))
    # inline style="" attributes need single quotes inside
    disp, text, mono = (x.replace('"', "'") for x in (disp, text, mono))
    r_btn = radius.get(comps.get("button", {}).get("radius", "md"), 6)
    r_card = radius.get(comps.get("card", {}).get("radius", "lg"), 12)
    dur = motion.get("duration", {}).get("base", 240)
    ease = motion.get("easing", {}).get("standard", "ease")

    def swatches():
        rows = []
        for k, v in pal.items():
            on = "#FFFFFF" if B.contrast(v, "#FFFFFF") >= B.contrast(v, "#000000") else "#000000"
            rt = B.contrast(light["text"], v) if "text" in light else 0
            rows.append(f'<div class="sw"><div class="chip" style="background:{v};color:{on}">{e(k)}</div>'
                        f'<div class="meta"><b>{v}</b><span>text on it: {rt:.1f}:1 · {badge(rt)}</span></div></div>')
        return "".join(rows)

    def roles(mode):
        rr = modes[mode]
        bg = rr.get("bg", "#FFFFFF")
        cells = "".join(f'<div class="role"><i style="background:{v}"></i><span>{e(r)}</span><code>{v}</code></div>' for r, v in rr.items())
        demo = (f'<div class="demo" style="background:{bg};color:{rr.get("text", "#000")};border-color:{rr.get("border", "#ccc")}">'
                f'<div style="font-family:{disp};font-size:28px;line-height:1.1">{e(brand.get("tagline", name))}</div>'
                f'<p style="color:{rr.get("muted", rr.get("text"))}">Body text in the muted role, for supporting copy.</p>'
                f'<span class="btn" style="background:{rr.get("accent", "#000")};color:{rr.get("on-accent", "#fff")};border-radius:{r_btn}px">Primary action</span></div>')
        return f'<h3>{mode.title()}</h3><div class="roles">{cells}</div>{demo}'

    def contrast_rows():
        out_rows = []
        for mode, rr in modes.items():
            for fg, bg in (("text", "bg"), ("muted", "bg"), ("on-accent", "accent"), ("accent", "bg")):
                if fg in rr and bg in rr:
                    c = B.contrast(rr[fg], rr[bg])
                    need = 3 if fg == "accent" else 4.5
                    ok = "pass" if c >= need else "fail"
                    out_rows.append(f'<tr><td>{mode}</td><td>{fg} / {bg}</td><td>{c:.2f}:1</td><td class="{ok}">{ok}</td></tr>')
        return "".join(out_rows)

    type_rows = "".join(
        f'<div class="ts"><code>{k} · {px:g}px</code><div style="font-family:{disp if px >= t.get("base", 16) * 1.5 else text};'
        f'font-size:{px}px;line-height:{1.1 if px >= 30 else 1.4}">{e(voice.get("examples", [name])[0] if voice.get("examples") else name)}</div></div>'
        for k, px in sorted(scale.items(), key=lambda x: -x[1]))
    space_rows = "".join(f'<div class="sp"><code>{k}</code><i style="width:{px}px"></i><span>{px}px</span></div>' for k, px in space.items() if px)
    radius_rows = "".join(f'<div class="rd"><i style="border-radius:{min(v, 60)}px"></i><code>{k} · {v}px</code></div>' for k, v in radius.items())
    elev_rows = "".join(f'<div class="el"><i style="box-shadow:{v}"></i><code>{k}</code></div>' for k, v in elev.items())

    def lst(items):
        return "".join(f"<li>{e(str(x))}</li>" for x in items or [])

    page = f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{e(name)} — Brand book</title>{f'<link rel="stylesheet" href="{url}">' if url else ''}
<style>
:root{{--bg:{light.get('bg')};--text:{light.get('text')};--muted:{light.get('muted', light.get('text'))};--line:{light.get('border', '#ddd')};--accent:{light.get('accent')};--surface:{light.get('surface', light.get('bg'))}}}
*{{box-sizing:border-box}}body{{margin:0;background:var(--bg);color:var(--text);font-family:{text};line-height:1.55}}
.wrap{{max-width:1180px;margin:0 auto;padding:56px 32px 96px}}
header{{padding:48px 0 56px;border-bottom:1px solid var(--line)}}
header .k{{font:600 12px/1 {mono};letter-spacing:.12em;text-transform:uppercase;color:var(--muted)}}
h1{{font-family:{disp};font-size:clamp(44px,7vw,96px);line-height:1;margin:16px 0 12px;letter-spacing:-.02em}}
header p{{font-size:20px;color:var(--muted);max-width:640px;margin:0}}
section{{padding:56px 0;border-bottom:1px solid var(--line)}}
h2{{font-family:{disp};font-size:32px;margin:0 0 6px}}h2+p{{color:var(--muted);margin:0 0 28px;max-width:640px}}
h3{{font-size:14px;letter-spacing:.08em;text-transform:uppercase;color:var(--muted);margin:28px 0 12px}}
.grid2{{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:32px}}
.card{{background:var(--surface);border:1px solid var(--line);border-radius:{r_card}px;padding:24px}}
ul{{margin:0;padding-left:18px}}li{{margin:4px 0}}
.isnot{{display:grid;grid-template-columns:1fr 1fr;gap:16px}}
.chars{{display:flex;gap:10px;flex-wrap:wrap;margin-top:12px}}.chars span{{border:1px solid var(--text);border-radius:999px;padding:6px 14px;font-weight:600}}
.pal{{display:grid;grid-template-columns:repeat(auto-fill,minmax(170px,1fr));gap:14px}}
.chip{{height:110px;border-radius:{r_card}px;display:flex;align-items:flex-end;padding:12px;font-weight:600;border:1px solid var(--line)}}
.meta{{padding:8px 2px;font-size:13px;display:flex;flex-direction:column}}.meta span{{color:var(--muted)}}
.roles{{display:flex;flex-wrap:wrap;gap:10px}}.role{{display:flex;align-items:center;gap:8px;border:1px solid var(--line);border-radius:999px;padding:4px 12px 4px 4px;font-size:13px}}
.role i{{width:22px;height:22px;border-radius:50%;border:1px solid var(--line)}}.role code{{color:var(--muted)}}
.demo{{margin-top:14px;border:1px solid;border-radius:{r_card}px;padding:28px}}.btn{{display:inline-block;padding:12px 20px;font-weight:600}}
table{{border-collapse:collapse;width:100%;font-size:14px}}td{{border-bottom:1px solid var(--line);padding:8px 6px}}.pass{{color:#1d7a3a;font-weight:700}}.fail{{color:#b3261e;font-weight:700}}
.ts{{display:grid;grid-template-columns:140px 1fr;gap:16px;align-items:baseline;padding:10px 0;border-bottom:1px dashed var(--line)}}.ts code{{color:var(--muted);font-size:12px}}
.ts div{{white-space:nowrap;overflow:hidden;text-overflow:ellipsis}}
.sp{{display:grid;grid-template-columns:50px 1fr 60px;gap:12px;align-items:center;margin:6px 0}}.sp i{{display:block;height:14px;background:var(--accent);border-radius:2px}}.sp span,.sp code{{font-size:12px;color:var(--muted)}}
.row{{display:flex;flex-wrap:wrap;gap:20px}}.rd i,.el i{{display:block;width:96px;height:96px;border:2px solid var(--text);background:var(--surface)}}.el i{{border:1px solid var(--line);border-radius:{r_card}px}}
.rd code,.el code{{display:block;font-size:12px;color:var(--muted);margin-top:8px}}
.motion-demo{{width:56px;height:56px;border-radius:{r_btn}px;background:var(--accent);animation:mv {dur * 4}ms {ease} infinite alternate}}
@keyframes mv{{to{{transform:translateX(220px)}}}}@media (prefers-reduced-motion:reduce){{.motion-demo{{animation:none}}}}
code{{font-family:{mono}}}
@media (max-width:760px){{.grid2,.isnot{{grid-template-columns:1fr}}.ts{{grid-template-columns:1fr}}}}
</style></head><body><div class="wrap">
<header><div class="k">Brand book · v{e(str(brand.get('version', '1.0')))}</div><h1>{e(name)}</h1><p>{e(brand.get('tagline', ''))}</p></header>

<section><h2>Positioning</h2><p>{e(pos.get('category', ''))}</p>
<div class="grid2"><div class="card"><h3>What makes it different</h3><p style="margin:0">{e(pos.get('difference', ''))}</p>
<div class="chars">{''.join(f'<span>{e(c)}</span>' for c in pos.get('character', []))}</div></div>
<div class="card isnot"><div><h3>Is</h3><ul>{lst(pos.get('is'))}</ul></div><div><h3>Is not</h3><ul>{lst(pos.get('is_not'))}</ul></div></div></div></section>

<section><h2>Colour</h2><p>{e(brand.get('color', {}).get('usage', ''))}</p><div class="pal">{swatches()}</div>
{''.join(roles(m) for m in modes)}
<h3>Contrast (WCAG 2.2)</h3><table>{contrast_rows()}</table></section>

<section><h2>Typography</h2><p>{' · '.join(f"{k}: {e(f.get('name', ''))}" for k, f in fams.items())} — base {t.get('base', 16)}px, ratio {t.get('ratio', 1.25)}</p>{type_rows}</section>

<section><h2>Space, radius, elevation</h2><p>Base unit {brand.get('space', {}).get('base', 4)}px.</p>
<div class="grid2"><div>{space_rows}</div><div><h3>Radius</h3><div class="row">{radius_rows}</div><h3>Elevation</h3><div class="row">{elev_rows}</div></div></div></section>

<section><h2>Motion</h2><p>Character: {e(motion.get('character', ''))} · base {dur}ms · {e(ease)}</p><div class="motion-demo" role="img" aria-label="Motion sample"></div>
<h3>Rules</h3><ul>{lst(motion.get('rules'))}</ul></section>

<section><h2>Components</h2><p>Rules from brand.json → components.</p><div class="grid2">{''.join(f'<div class="card"><h3>{e(k)}</h3><ul>{lst(f"{a}: {b}" for a, b in v.items())}</ul></div>' for k, v in comps.items())}</div></section>

<section><h2>Voice</h2><p>{', '.join(e(x) for x in voice.get('tone', []))}</p><div class="grid2"><div class="card"><h3>Do</h3><ul>{lst(voice.get('do'))}</ul><h3>Don't</h3><ul>{lst(voice.get('dont'))}</ul></div>
<div class="card"><h3>Examples</h3>{''.join(f'<p style="font-family:{disp};font-size:24px;line-height:1.2;margin:0 0 12px">{e(x)}</p>' for x in voice.get('examples', []))}</div></div></section>

<section><h2>Imagery</h2><p>Every photo and generated image follows these.</p><div class="grid2"><div class="card"><ul>{''.join(f'<li><b>{e(k)}:</b> {e(v if isinstance(v, str) else ", ".join(v))}</li>' for k, v in img.items() if k != 'avoid')}</ul></div>
<div class="card"><h3>Avoid</h3><ul>{lst(img.get('avoid'))}</ul></div></div></section>

<section style="border:0"><h2>Film and motion pictures</h2><p>Pace, camera and sound for video.</p><div class="card"><ul>{''.join(f'<li><b>{e(k)}:</b> {e(str(v))}</li>' for k, v in film.items())}</ul></div></section>
</div></body></html>"""
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(page, encoding="utf-8")
    print(f"wrote {out}")


if __name__ == "__main__":
    main()
