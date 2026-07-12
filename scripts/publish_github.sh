#!/usr/bin/env bash
set -euo pipefail

visibility="${1:-public}"
if [[ "$visibility" != "public" && "$visibility" != "private" ]]; then
  echo "Usage: $0 [public|private]" >&2
  exit 2
fi

if ! command -v gh >/dev/null 2>&1; then
  echo "GitHub CLI (gh) is required: https://cli.github.com/" >&2
  exit 1
fi

if ! gh auth status >/dev/null 2>&1; then
  gh auth login
fi

root="$(cd "$(dirname "$0")/.." && pwd)"
cd "$root"

owner="$(gh api user --jq .login)"
user_id="$(gh api user --jq .id)"
author_name="$(gh api user --jq '.name // .login')"
repo="network-radar"
version="$(python3 -c 'import json; print(json.load(open("plugins/network-radar/.codex-plugin/plugin.json", encoding="utf-8"))["version"])')"

python3 scripts/prepare_release.py --owner "$owner" --repo "$repo"
python3 scripts/validate_repository.py --release

if [[ ! -d .git ]]; then
  git init -b main
fi
git config user.name "$author_name"
git config user.email "${user_id}+${owner}@users.noreply.github.com"
git add .
if ! git diff --cached --quiet; then
  git commit -m "release: network-radar v${version}"
fi

if ! gh repo view "${owner}/${repo}" >/dev/null 2>&1; then
  gh repo create "${owner}/${repo}" "--${visibility}" --source=. --remote=origin --push \
    --description "Discover, verify, and organize professional contacts with Codex."
else
  if ! git remote get-url origin >/dev/null 2>&1; then
    git remote add origin "https://github.com/${owner}/${repo}.git"
  fi
  git push -u origin main
fi

gh repo edit "${owner}/${repo}" \
  --description "Discover, verify, and organize professional contacts with Codex." \
  --add-topic codex \
  --add-topic agent-skills \
  --add-topic networking \
  --add-topic outreach \
  --add-topic maimai \
  --add-topic feishu \
  --add-topic spreadsheet

tag="v${version}"
if ! git rev-parse "$tag" >/dev/null 2>&1; then
  git tag "$tag"
  git push origin "$tag"
fi

if ! gh release view "$tag" >/dev/null 2>&1; then
  gh release create "$tag" \
    --title "Network Radar ${tag}" \
    --notes-file CHANGELOG.md
fi

echo "Published: https://github.com/${owner}/${repo}"
