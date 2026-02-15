#!/usr/bin/env bash
set -euo pipefail

# Deploy dist/ contents to the gh-pages branch.
# The built files land at the repo root so GitHub Pages serves index.html directly.

BRANCH="gh-pages"
DIST="dist"

# Derive the base URL from the GitHub repo name (e.g. "/website-sita")
REMOTE_URL=$(git remote get-url origin)
REPO_NAME=$(basename -s .git "$REMOTE_URL")
BASE_URL="/${REPO_NAME}"

# 1. Build with the correct base URL for GitHub Pages
echo "Building site with base_url=${BASE_URL}..."
source .venv/bin/activate
python3 build.py --base-url "$BASE_URL"

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
git push --force "$REMOTE_URL" "$BRANCH"

echo ""
echo "Deployed to branch '$BRANCH'."
echo "Site will be at: https://$(echo "$REMOTE_URL" | sed -E 's|.*[:/]([^/]+)/.*|\L\1|').github.io${BASE_URL}/"
