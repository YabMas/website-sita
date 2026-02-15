#!/usr/bin/env bash
set -euo pipefail

# Deploy dist/ contents to the gh-pages branch.
# The built files land at the repo root so GitHub Pages serves index.html directly.

BRANCH="gh-pages"
DIST="dist"

# 1. Build
echo "Building site..."
source .venv/bin/activate
python3 build.py

# 2. Sanity check
if [ ! -f "$DIST/index.html" ]; then
    echo "ERROR: $DIST/index.html not found. Build may have failed."
    exit 1
fi

# 3. Create a temporary work area (avoids touching the working tree)
TMPDIR=$(mktemp -d)
trap 'rm -rf "$TMPDIR"' EXIT

# 4. Copy dist contents into the temp dir
cp -a "$DIST"/. "$TMPDIR"/

# 5. Build a git commit from the temp dir
cd "$TMPDIR"
git init --quiet
git checkout --quiet -b "$BRANCH"
git add -A
git commit --quiet -m "Deploy $(date -u '+%Y-%m-%d %H:%M:%S UTC')"

# 6. Force-push to the remote gh-pages branch
REMOTE=$(cd "$OLDPWD" && git remote get-url origin)
git push --force "$REMOTE" "$BRANCH"

echo ""
echo "Deployed to branch '$BRANCH'."
echo "Configure GitHub Pages to serve from branch '$BRANCH' (root)."
