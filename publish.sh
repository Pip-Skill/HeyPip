#!/usr/bin/env bash
# Pip — one-time publishing helper (macOS / Linux).
# Fills in your name and GitHub username, builds the skill files, creates the GitHub repo
# and a release. Run from this folder:  bash publish.sh
set -euo pipefail
cd "$(dirname "$0")"
VERSION=$(python3 -c "import json;print(json.load(open('.claude-plugin/plugin.json'))['version'])")

read -rp "Your GitHub username: " GH
read -rp "Your name as author (e.g. Alex K.): " AUTHOR
[ -n "$GH" ] && [ -n "$AUTHOR" ] || { echo "Both are needed."; exit 1; }

echo "→ Filling in placeholders"
grep -rlI --exclude-dir=.git --exclude=publish.sh -e YOUR_GITHUB -e YOUR_NAME . | while read -r f; do
  GH="$GH" AUTHOR="$AUTHOR" perl -pi -e 's/YOUR_GITHUB/$ENV{GH}/g; s/YOUR_NAME/$ENV{AUTHOR}/g' "$f"
done

echo "→ Checking the plugin"
if command -v claude >/dev/null; then claude plugin validate . || exit 1; else echo "  (Claude Code not found — skipped validation)"; fi

echo "→ Building skill files into dist/"
rm -rf dist && mkdir -p dist/tmp
cp -R skills/heypip dist/tmp/heypip
# claude.ai takes at most 200 files per skill, so the uploadable skill leaves out the web engine
# (sites then follow references/web.md); the full engine ships in the Claude Code plugin.
( cd dist/tmp && zip -qr ../heypip.skill heypip -x 'heypip/taste/*' )
rm -rf dist/tmp
ls -lh dist

echo "→ Git"
[ -d .git ] || git init -q -b main
git add -A
git commit -qm "Pip $VERSION" || echo "  (nothing new to commit)"

if command -v gh >/dev/null && gh auth status >/dev/null 2>&1; then
  if ! gh repo view "$GH/heypip" >/dev/null 2>&1; then
    echo "→ Creating github.com/$GH/heypip (public)"
    gh repo create "$GH/heypip" --public --source . --remote origin --push \
      --description "Pip — a creative studio in Claude: brand, logo, website, posters, photo & video prompts from one brand.json"
  else
    git remote get-url origin >/dev/null 2>&1 || git remote add origin "https://github.com/$GH/heypip.git"
    git push -u origin main
  fi
  gh release view "v$VERSION" >/dev/null 2>&1 || gh release create "v$VERSION" dist/heypip.skill \
    --title "Pip $VERSION" --notes-file CHANGELOG.md
  echo
  echo "Done: https://github.com/$GH/heypip"
  echo "Install in Claude Code:  /plugin marketplace add $GH/heypip   then   /plugin install heypip@heypip"
else
  echo
  echo "GitHub CLI (gh) is not installed or not logged in. Either:"
  echo "  • install it (brew install gh), run: gh auth login, then run this script again; or"
  echo "  • create an empty public repo named 'heypip' on github.com and run:"
  echo "      git remote add origin https://github.com/$GH/heypip.git && git push -u origin main"
  echo "    then attach dist/heypip.skill to a new Release."
fi
