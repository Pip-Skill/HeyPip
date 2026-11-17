#!/usr/bin/env python3
"""Check WCAG 2.2 contrast for colour role pairs in brand.json.

Usage: python3 check_contrast.py <brand.json> [--json]
Exit code 1 if any required pair fails.

Default pairs (when the roles exist): text/bg, text/surface, muted/bg, muted/surface,
on-accent/accent (text on buttons), accent/bg (UI, 3:1), focus/bg (UI, 3:1),
border/bg (UI, informational 1.5:1 — hairline borders are decorative, reported not failed).
Extra pairs can be listed in color.pairs as ["fg-role", "bg-role"] or
["fg-role", "bg-role", "large"|"ui"].
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import brandlib as B  # noqa: E402

DEFAULT = [
    ("text", "bg", "body"), ("text", "surface", "body"),
    ("muted", "bg", "body"), ("muted", "surface", "body"),
    ("on-accent", "accent", "body"),
    ("accent", "bg", "ui"), ("focus", "bg", "ui"),
    ("border", "bg", "info"),
]
NEED = {"body": 4.5, "large": 3.0, "ui": 3.0, "info": 1.5}


def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    brand = B.load(sys.argv[1])
    as_json = "--json" in sys.argv
    try:
        modes = B.modes(brand)
    except ValueError as e:
        sys.exit(f"colour error: {e}")
    extra = [tuple(p) + (("body",) if len(p) == 2 else ()) for p in brand.get("color", {}).get("pairs", [])]
    pairs = []
    for p in DEFAULT + extra:
        if p not in pairs:
            pairs.append(p)

    results, failed = [], 0
    for mode, roles in modes.items():
        for fg, bg, kind in pairs:
            if fg not in roles or bg not in roles:
                continue
            ratio = B.contrast(roles[fg], roles[bg])
            need = NEED.get(kind, 4.5)
            ok = ratio >= need
            required = kind != "info"
            if not ok and required:
                failed += 1
            results.append({"mode": mode, "fg": fg, "bg": bg, "kind": kind, "fg_hex": roles[fg], "bg_hex": roles[bg],
                            "ratio": round(ratio, 2), "need": need, "pass": ok, "required": required})

    if as_json:
        print(json.dumps({"failed": failed, "results": results}, indent=2))
    else:
        for r in results:
            mark = "PASS" if r["pass"] else ("FAIL" if r["required"] else "note")
            print(f"{mark:4}  {r['mode']:5}  {r['fg']:>10} on {r['bg']:<8} {r['fg_hex']} / {r['bg_hex']}  "
                  f"{r['ratio']:>5}:1  (needs {r['need']}:1, {r['kind']})")
        print(f"\n{failed} required pair(s) failing." if failed else "\nAll required pairs pass.")
        if failed:
            print("Fix by changing lightness of the failing role in brand.json (keep the hue), then rerun.")
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
