#!/usr/bin/env python3
"""Render a moodboard page from a small direction JSON (see references/direction.md §4).

Usage: python3 render_moodboard.py <direction.json> <out.html>
"""
import html
import json
import sys
from pathlib import Path

e = html.escape

PATTERNS = {
    "linen": "repeating-linear-gradient(0deg,{a} 0 2px,{b} 2px 4px),repeating-linear-gradient(90deg,transparent 0 3px,rgba(0,0,0,.05) 3px 4px)",
    "grain": "radial-gradient(rgba(0,0,0,.12) 1px,transparent 1px) 0 0/5px 5px,radial-gradient(rgba(255,255,255,.18) 1px,{a} 1px) 2px 3px/7px 7px",
    "grid": "linear-gradient({b} 1px,transparent 1px) 0 0/24px 24px,linear-gradient(90deg,{b} 1px,{a} 1px) 0 0/24px 24px",
    "dots": "radial-gradient({b} 2px,{a} 2.5px) 0 0/18px 18px",
    "stripes": "repeating-linear-gradient(45deg,{a} 0 12px,{b} 12px 24px)",
    "paper": "linear-gradient(180deg,rgba(255,255,255,.25),rgba(0,0,0,.04)),radial-gradient(rgba(0,0,0,.06) 1px,{a} 1px) 0 0/3px 3px",
    "noise": "repeating-radial-gradient(circle at 30% 40%,{a} 0 1px,{b} 1px 2px)",
}

COMPOSITIONS = {
    "asym-left": '<i style="left:8%;top:14%;width:44%;height:12%"></i><i style="left:8%;top:30%;width:30%;height:5%;opacity:.5"></i><b style="left:60%;top:10%;width:32%;height:80%"></b>',
    "asym-right": '<b style="left:8%;top:10%;width:32%;height:80%"></b><i style="left:48%;top:14%;width:44%;height:12%"></i><i style="left:48%;top:30%;width:30%;height:5%;opacity:.5"></i>',
    "centered": '<i style="left:25%;top:30%;width:50%;height:14%"></i><i style="left:35%;top:50%;width:30%;height:5%;opacity:.5"></i>',
    "split": '<b style="left:0;top:0;width:50%;height:100%"></b><i style="left:58%;top:30%;width:34%;height:12%"></i><i style="left:58%;top:48%;width:26%;height:5%;opacity:.5"></i>',
    "grid-3": '<b style="left:6%;top:20%;width:27%;height:60%"></b><b style="left:37%;top:20%;width:27%;height:60%"></b><b style="left:68%;top:20%;width:27%;height:60%"></b>',
    "full-bleed": '<b style="left:0;top:0;width:100%;height:100%;opacity:.6"></b><i style="left:8%;top:62%;width:50%;height:12%"></i>',
    "stacked": '<i style="left:8%;top:10%;width:70%;height:12%"></i><b style="left:8%;top:30%;width:84%;height:40%"></b><i style="left:8%;top:78%;width:40%;height:5%;opacity:.5"></i>',
}


def tile(t, pal, fonts):
    kind = t.get("type")
    label = e(t.get("label", ""))
    cap = f'<figcaption>{label}</figcaption>' if label else ""
    if kind == "color":
        return f'<figure class="t tall"><div class="fill" style="background:{e(t["hex"])}"></div>{cap or f"<figcaption>{e(t["hex"])}</figcaption>"}</figure>'
    if kind == "type":
        font = t.get("font") or fonts.get("display", "serif")
        return f'<figure class="t wide"><div class="fill type" style="font-family:\'{e(font)}\',serif">{e(t.get("sample", "Aa"))}</div><figcaption>{e(font)} · {label}</figcaption></figure>'
    if kind == "texture":
        cols = t.get("colors") or [pal[0]["hex"] if pal else "#eee", pal[1]["hex"] if len(pal) > 1 else "#ccc"]
        bg = PATTERNS.get(t.get("pattern", "grain"), PATTERNS["grain"]).format(a=cols[0], b=cols[-1])
        return f'<figure class="t"><div class="fill" style="background:{bg}"></div>{cap}</figure>'
    if kind == "composition":
        shapes = COMPOSITIONS.get(t.get("layout", "asym-left"), COMPOSITIONS["asym-left"])
        return f'<figure class="t wide"><div class="fill comp">{shapes}</div>{cap}</figure>'
    if kind == "reference":
        return f'<figure class="t note"><div class="fill"><b class="h">{e(t.get("title", "Reference"))}</b><p>{e(t.get("text", ""))}</p></div>{cap}</figure>'
    if kind == "prompt":
        return (f'<figure class="t note prompt"><div class="fill"><b class="h">Image prompt · {e(t.get("title", ""))}</b>'
                f'<p>{e(t.get("text", ""))}</p></div>{cap}</figure>')
    if kind == "words":
        words = "".join(f"<span>{e(w)}</span>" for w in t.get("items", []))
        return f'<figure class="t wide"><div class="fill words">{words}</div>{cap}</figure>'
    if kind == "image":
        return f'<figure class="t tall"><img src="{e(t["src"])}" alt="{e(t.get("alt", label))}" loading="lazy">{cap}</figure>'
    return ""


def main():
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    d = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    pal = d.get("palette", [])
    fonts = d.get("fonts", {})
    ground = pal[0]["hex"] if pal else "#F4F1EC"
    ink = next((p["hex"] for p in pal if p.get("role") in ("text", "ink")), "#1A1A1A")
    fam = [f for f in {fonts.get("display"), fonts.get("text")} if f]
    gf = ""
    if fam:
        gf = '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?' + "&".join(
            "family=" + f.replace(" ", "+") + ":wght@400;600" for f in fam) + '&display=swap">'
    strip = "".join(f'<div style="background:{e(p["hex"])}" title="{e(p.get("name", ""))}"><span>{e(p.get("name", ""))}<br>{e(p["hex"])}{(" · " + e(p["role"])) if p.get("role") else ""}</span></div>' for p in pal)
    tiles = "".join(tile(t, pal, fonts) for t in d.get("tiles", []))
    page = f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{e(d.get('brand', ''))} — {e(d.get('direction', 'Moodboard'))}</title>{gf}
<style>
*{{box-sizing:border-box}}body{{margin:0;background:{ground};color:{ink};font-family:'{e(fonts.get('text', 'Inter'))}',system-ui,sans-serif}}
.wrap{{max-width:1320px;margin:0 auto;padding:48px 28px 80px}}
.k{{font-size:12px;letter-spacing:.14em;text-transform:uppercase;opacity:.7}}
h1{{font-family:'{e(fonts.get('display', 'serif'))}',serif;font-size:clamp(40px,6vw,84px);line-height:1;margin:12px 0 14px;letter-spacing:-.02em}}
.sum{{font-size:20px;max-width:720px;opacity:.85;margin:0 0 28px;line-height:1.5}}
.strip{{display:flex;height:96px;border-radius:14px;overflow:hidden;margin-bottom:28px}}.strip div{{flex:1;display:flex;align-items:flex-end;padding:10px}}
.strip span{{font-size:11px;background:rgba(255,255,255,.85);color:#111;padding:4px 6px;border-radius:6px}}
.board{{columns:4 260px;column-gap:16px}}
.t{{break-inside:avoid;margin:0 0 16px;border-radius:14px;overflow:hidden;background:rgba(255,255,255,.35);border:1px solid rgba(0,0,0,.08)}}
.t .fill{{height:200px;position:relative}}.t.tall .fill,.t.tall img{{height:300px}}.t img{{width:100%;object-fit:cover;display:block}}
.t figcaption{{font-size:12px;padding:8px 12px;opacity:.75}}
.type{{display:flex;align-items:center;justify-content:center;font-size:52px;line-height:1;text-align:center;padding:16px}}
.comp{{background:rgba(0,0,0,.04)}}.comp i,.comp b{{position:absolute;border-radius:3px}}.comp i{{background:{ink}}}.comp b{{background:{pal[-1]['hex'] if pal else '#999'};opacity:.85}}
.note .fill{{height:auto;min-height:150px;padding:18px}}.note .h{{display:block;font-size:13px;letter-spacing:.06em;text-transform:uppercase;margin-bottom:8px}}.note p{{margin:0;font-size:15px;line-height:1.5}}
.prompt .fill{{font-family:ui-monospace,Menlo,monospace}}.prompt p{{font-size:13px}}
.words{{display:flex;flex-wrap:wrap;align-content:center;gap:10px;padding:18px}}.words span{{border:1.5px solid currentColor;border-radius:999px;padding:8px 16px;font-size:20px}}
</style></head><body><div class="wrap">
<div class="k">{e(d.get('brand', ''))} · Moodboard</div><h1>{e(d.get('direction', ''))}</h1><p class="sum">{e(d.get('summary', ''))}</p>
<div class="strip">{strip}</div><div class="board">{tiles}</div></div></body></html>"""
    out = Path(sys.argv[2])
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(page, encoding="utf-8")
    print(f"wrote {out} ({len(d.get('tiles', []))} tiles)")


if __name__ == "__main__":
    main()
