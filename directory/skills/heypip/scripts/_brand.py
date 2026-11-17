#!/usr/bin/env python3
"""Shared helpers for Pip scripts: load brand.json, resolve colours, build scales, contrast."""
import json
import re
import sys
from pathlib import Path

HEX = re.compile(r"^#([0-9a-fA-F]{3}|[0-9a-fA-F]{6}|[0-9a-fA-F]{8})$")


def load(path):
    p = Path(path)
    if not p.exists():
        sys.exit(f"brand file not found: {p}")
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        sys.exit(f"{p} is not valid JSON: {e}")


def norm_hex(h):
    h = h.strip()
    if not HEX.match(h):
        raise ValueError(f"not a hex colour: {h}")
    if len(h) == 4:
        h = "#" + "".join(c * 2 for c in h[1:])
    return h[:7].upper()


def resolve_color(value, palette, seen=None):
    """A role value is a hex or a palette name (which may itself point to a name)."""
    seen = seen or set()
    if isinstance(value, str) and value.startswith("#"):
        return norm_hex(value)
    if value in seen:
        raise ValueError(f"colour reference loop at '{value}'")
    if value not in palette:
        raise ValueError(f"unknown colour '{value}' (not a hex and not in palette)")
    seen.add(value)
    return resolve_color(palette[value], palette, seen)


def modes(brand):
    """Return {'light': {role: hex}, 'dark': {...}?}."""
    color = brand.get("color", {})
    palette = color.get("palette", {})
    out = {}
    for mode in ("light", "dark"):
        roles = color.get(mode)
        if roles:
            out[mode] = {role: resolve_color(v, palette) for role, v in roles.items()}
    if "light" not in out:
        raise ValueError("brand.json needs color.light roles (bg, text, ...)")
    return out


def palette_hex(brand):
    pal = brand.get("color", {}).get("palette", {})
    return {k: resolve_color(v, pal) for k, v in pal.items()}


# ---------- contrast (WCAG 2.x) ----------
def _lin(c):
    c = c / 255
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4


def luminance(hexc):
    h = norm_hex(hexc)
    r, g, b = (int(h[i:i + 2], 16) for i in (1, 3, 5))
    return 0.2126 * _lin(r) + 0.7152 * _lin(g) + 0.0722 * _lin(b)


def contrast(a, b):
    la, lb = luminance(a), luminance(b)
    hi, lo = max(la, lb), min(la, lb)
    return (hi + 0.05) / (lo + 0.05)


# ---------- scales ----------
def type_scale(brand):
    t = brand.get("type", {})
    base = float(t.get("base", 16))
    ratio = float(t.get("ratio", 1.25))
    steps = t.get("steps") or {"xs": -2, "sm": -1, "base": 0, "lg": 1, "xl": 2, "2xl": 3, "3xl": 4, "4xl": 5, "5xl": 6}
    out = {}
    for name, n in steps.items():
        px = base * (ratio ** n)
        out[name] = round(px, 2)
    return out


def fluid(px, base):
    """Fluid clamp for large sizes: shrink to ~62% at 375px, full at 1280px."""
    min_px = max(base * 1.25, px * 0.62)
    if min_px >= px:
        return f"{px / 16:.4g}rem"
    slope = (px - min_px) / (1280 - 375)
    inter = min_px - slope * 375
    return f"clamp({min_px / 16:.4g}rem, {inter / 16:.4g}rem + {slope * 100:.4g}vw, {px / 16:.4g}rem)"


def space_scale(brand):
    s = brand.get("space", {})
    base = s.get("base", 4)
    scale = s.get("scale", [0, 1, 2, 3, 4, 6, 8, 12, 16, 24, 32])
    return {str(n): n * base for n in scale}


def font_stack(fam):
    name = fam.get("name", "")
    fb = fam.get("fallback", "sans-serif")
    return f"\"{name}\", {fb}" if name else fb


def google_fonts_url(brand):
    fams = brand.get("type", {}).get("families", {})
    parts = []
    for fam in fams.values():
        if fam.get("source") == "google" and fam.get("name"):
            w = sorted(set(fam.get("weights", [400])))
            parts.append("family=" + fam["name"].replace(" ", "+") + ":wght@" + ";".join(map(str, w)))
    if not parts:
        return None
    return "https://fonts.googleapis.com/css2?" + "&".join(parts) + "&display=swap"


def kebab(s):
    return re.sub(r"[^a-z0-9]+", "-", str(s).lower()).strip("-")
