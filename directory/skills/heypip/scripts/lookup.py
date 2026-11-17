#!/usr/bin/env python3
"""Search Pip's design library (library/uiux, data from UI/UX Pro Max, MIT).

Usage:
  python3 lookup.py <domain> "<query>" [--n 3] [--full]
  python3 lookup.py domains

Domains:
  product   product type -> recommended style, landing pattern, colour focus      (192)
  reason    product type -> style priority, colour/type mood, anti-patterns         (192)
  style     UI styles: keywords, colours, effects, best for / avoid, checklist      (89)
  color     ready palettes per product type (primary/secondary/accent/bg/fg/...)  (192)
  type      font pairings with mood and best-for                                   (74)
  font      Google Fonts catalogue                                                 (~1900)
  landing   landing-page patterns: section order, CTA placement, conversion tips   (34)
  ux        UX guidelines with do / don't and severity                             (120)
  app       app-interface rules (mobile and desktop)
  chart     which chart for which data, with accessibility notes                   (25)
  icon      icons by meaning, library and import                                   (105)
  motion    motion presets: duration, easing, do / don't
  stack:<name>  rules for a stack, e.g. stack:react, stack:nextjs, stack:swiftui, stack:flutter

Ranking is BM25 over each row's text, with extra weight on the row's name/keywords columns.
Use it to ground a decision in data, then write the decision into brand.json or the plan —
don't paste raw rows into deliverables.
"""
import csv
import json
import math
import re
import sys
from collections import Counter
from pathlib import Path

LIB = Path(__file__).resolve().parent.parent / "library" / "uiux"

# domain -> (file, title column, boosted columns, columns to show in short mode)
DOMAINS = {
    "product": ("products.csv", "Product Type", ["Product Type", "Keywords"],
                ["Primary Style Recommendation", "Secondary Styles", "Landing Page Pattern", "Color Palette Focus", "Key Considerations"]),
    "reason": ("ui-reasoning.csv", "UI_Category", ["UI_Category"],
               ["Recommended_Pattern", "Style_Priority", "Color_Mood", "Typography_Mood", "Key_Effects", "Anti_Patterns"]),
    "style": ("styles.csv", "Style Category", ["Style Category", "Keywords", "Aliases"],
              ["Keywords", "Primary Colors", "Effects & Animation", "Best For", "Do Not Use For", "Accessibility", "Implementation Checklist"]),
    "color": ("colors.csv", "Product Type", ["Product Type", "Notes"],
              ["Primary", "On Primary", "Secondary", "Accent", "On Accent", "Background", "Foreground", "Muted", "Muted Foreground", "Border", "Notes"]),
    "type": ("typography.csv", "Font Pairing Name", ["Font Pairing Name", "Mood/Style Keywords", "Best For"],
             ["Heading Font", "Body Font", "Mood/Style Keywords", "Best For", "Notes"]),
    "font": ("google-fonts.csv", None, [], None),
    "landing": ("landing.csv", "Pattern Name", ["Pattern Name", "Keywords", "Aliases"],
                ["Section Order", "Primary CTA Placement", "Color Strategy", "Recommended Effects", "Conversion Optimization"]),
    "ux": ("ux-guidelines.csv", "Issue", ["Issue", "Category"],
           ["Category", "Platform", "Description", "Do", "Don't", "Severity"]),
    "app": ("app-interface.csv", "Issue", ["Issue", "Keywords", "Category"],
            ["Category", "Platform", "Description", "Do", "Don't", "Severity"]),
    "chart": ("charts.csv", "Data Type", ["Data Type", "Keywords"],
              ["Best Chart Type", "Secondary Options", "When to Use", "When NOT to Use", "Accessibility Notes", "Library Recommendation"]),
    "icon": ("icons.csv", "Icon Name", ["Icon Name", "Keywords", "Category"],
             ["Category", "Library", "Import Code", "Usage", "Best For"]),
    "motion": ("motion.csv", "Category", ["Category", "Keywords"],
               ["Intensity Tier", "Trigger", "Duration", "Easing", "Do", "Don't", "Performance Notes"]),
}

TOKEN = re.compile(r"[a-z0-9]+")


STOP = {"a", "an", "the", "and", "or", "for", "of", "to", "in", "on", "with", "app", "apps", "website", "site", "platform"}


def stem(w):
    """Tiny English stemmer: invoicing/invoices/invoice -> invoic, freelancers -> freelanc."""
    for suf in ("ations", "ation", "ists", "ist", "ism", "ings", "ing", "ers", "er", "ies", "es", "ed", "ly", "s", "e"):
        if len(w) > len(suf) + 3 and w.endswith(suf):
            return w[: -len(suf)]
    return w


def tokens(text):
    return [stem(w) for w in TOKEN.findall(str(text).lower()) if w not in STOP]


def load(file):
    """Library tables ship as JSON lists of records (converted from the original CSV)."""
    path = LIB / file
    if path.suffix == ".csv" and not path.exists():
        path = path.with_suffix(".json")
    if path.suffix == ".json":
        return json.loads(path.read_text(encoding="utf-8"))
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def rank(rows, query, boost_cols, n):
    """BM25 with boosted fields (boosted columns counted 2x)."""
    docs = []
    for r in rows:
        t = []
        for k, v in r.items():
            if k is None or v is None:
                continue
            w = tokens(v)
            t += w * (2 if k in boost_cols else 1)
        docs.append(Counter(t))
    N = len(docs) or 1
    avg = sum(sum(d.values()) for d in docs) / N
    q = tokens(query)
    df = Counter(w for d in docs for w in set(d) if w in q)
    k1, b = 0.9, 0.6
    scored = []
    for r, d in zip(rows, docs):
        dl = sum(d.values()) or 1
        s = 0.0
        for w in q:
            f = d.get(w, 0)
            if not f:
                continue
            idf = math.log(1 + (N - df[w] + 0.5) / (df[w] + 0.5))
            s += idf * f * (k1 + 1) / (f + k1 * (1 - b + b * dl / avg))
        if s > 0:
            scored.append((s, r))
    scored.sort(key=lambda x: -x[0])
    return scored[:n]


# everyday words -> words the library uses (product, reason and color domains)
SYNONYMS = {
    "coffee": "cafe bakery", "espresso": "cafe", "roastery": "cafe", "roaster": "cafe", "kaffee": "cafe",
    "bistro": "restaurant food", "bar": "restaurant food", "pub": "restaurant food", "wine": "restaurant food",
    "pizza": "restaurant food", "sushi": "restaurant food", "brewery": "restaurant food", "patisserie": "bakery",
    "yoga": "fitness wellness", "pilates": "fitness wellness", "stretching": "fitness wellness", "gym": "fitness",
    "meditation": "wellness mindfulness", "massage": "spa wellness", "barber": "beauty salon", "hair": "beauty salon",
    "nails": "beauty salon", "tattoo": "beauty salon", "boutique": "e-commerce retail", "store": "e-commerce retail",
    "shop": "e-commerce retail", "clothing": "fashion e-commerce", "apparel": "fashion e-commerce",
    "dentist": "healthcare clinic", "doctor": "healthcare clinic", "clinic": "healthcare", "therapist": "healthcare wellness",
    "lawyer": "legal", "attorney": "legal", "accountant": "finance accounting", "bookkeeping": "finance accounting invoice",
    "tutor": "education", "school": "education", "course": "education", "kids": "children education",
    "photographer": "photography portfolio", "architect": "architecture portfolio", "designer": "portfolio agency",
    "guesthouse": "hotel hospitality", "hostel": "hotel hospitality", "flowers": "florist", "plants": "florist plant",
    "coding": "developer tool ide", "developers": "developer tool", "devtool": "developer tool",
    "band": "music", "musician": "music", "podcast": "media", "newsletter": "media blog",
}


def expand(query):
    extra = [SYNONYMS[w] for w in TOKEN.findall(query.lower()) if w in SYNONYMS]
    return query + (" " + " ".join(extra) if extra else "")


def resolve(domain):
    if domain.startswith("stack:"):
        f = f"stacks/{domain.split(':', 1)[1]}.json"
        if not (LIB / f).exists():
            names = sorted(p.stem for p in (LIB / "stacks").glob("*.json"))
            sys.exit(f"unknown stack; one of: {', '.join(names)}")
        return f, "Guideline", ["Guideline", "Category"], ["Category", "Description", "Do", "Don't", "Severity"]
    if domain not in DOMAINS:
        sys.exit(f"unknown domain '{domain}'. Run: lookup.py domains")
    return DOMAINS[domain]


def search(domain, query, n=3):
    """Return [(score, row)] — used by other scripts."""
    file, title, boost, _ = resolve(domain)
    rows = load(file)
    if domain in ("product", "reason", "color"):
        query = expand(query)
    if not boost:
        boost = list(rows[0].keys())[:2] if rows else []
    return rank(rows, query, boost, n)


def main():
    a = sys.argv[1:]
    if not a or a[0] in ("-h", "--help"):
        sys.exit(__doc__)
    if a[0] == "domains":
        print(__doc__.split("Domains:")[1].split("Ranking")[0])
        return
    if len(a) < 2:
        sys.exit(__doc__)
    domain, query = a[0], a[1]
    n = int(a[a.index("--n") + 1]) if "--n" in a else 3
    full = "--full" in a
    file, title, boost, show = resolve(domain)
    hits = search(domain, query, n)
    if not hits:
        print(f"no match in {domain} for '{query}' — try broader words")
        return
    for s, r in hits:
        name = r.get(title) if title else next(iter(r.values()))
        print(f"### {name}  ({domain}, score {s:.1f})")
        cols = r.keys() if full or not show else show
        for c in cols:
            v = (r.get(c) or "").strip()
            if v and c not in ("No", title):
                print(f"- **{c}:** {v}")
        print()


if __name__ == "__main__":
    main()
