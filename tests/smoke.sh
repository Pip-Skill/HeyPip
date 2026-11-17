#!/usr/bin/env bash
# Pip smoke test: runs every Python script on the example brand. No network needed.
set -euo pipefail
S="$(cd "$(dirname "$0")/.." && pwd)/skills/heypip"
T="$(mktemp -d)"; trap 'rm -rf "$T"' EXIT
cd "$S"
python3 scripts/check_contrast.py templates/brand.example.json
python3 scripts/build_tokens.py templates/brand.example.json "$T/tokens"
python3 scripts/render_brandbook.py templates/brand.example.json "$T/brandbook.html"
python3 scripts/render_moodboard.py templates/direction.example.json "$T/moodboard.html"
python3 scripts/prompt_pack.py templates/brand.example.json templates/shots.example.json "$T/prompts.md"
python3 scripts/render_print.py templates/brand.example.json templates/print.example.json "$T/print"
python3 scripts/lookup.py product "coffee roastery" --n 1 | grep -q '###'
python3 scripts/suggest_brand.py "invoicing app for freelancers" --name Test --lang ru --out "$T/brand.json"
python3 scripts/check_contrast.py "$T/brand.json"
for f in tokens.css tokens.tailwind.css tailwind.preset.js tokens.dtcg.json tokens.ts; do test -s "$T/tokens/$f"; done
test -s "$T/print/poster-type.html"
echo "smoke: all scripts OK"
