#!/usr/bin/env python3
"""Fill GitHub owner and repository metadata before the first public release."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "plugins/network-radar/.codex-plugin/plugin.json"
PUBLIC_TEXT_FILES = [ROOT / "README.md", ROOT / "LAUNCH_POST.md"]
PLACEHOLDER = "OWNER_" + "PLACEHOLDER"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--owner", required=True, help="GitHub account or organization")
    parser.add_argument("--repo", default="network-radar")
    args = parser.parse_args()

    repository_url = f"https://github.com/{args.owner}/{args.repo}"
    payload = json.loads(MANIFEST.read_text(encoding="utf-8"))
    payload["repository"] = repository_url
    payload["homepage"] = repository_url
    payload.setdefault("author", {})["url"] = f"https://github.com/{args.owner}"
    payload.setdefault("interface", {})["websiteURL"] = repository_url
    MANIFEST.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    for path in PUBLIC_TEXT_FILES:
        text = path.read_text(encoding="utf-8").replace(PLACEHOLDER, args.owner)
        path.write_text(text, encoding="utf-8")
    print(f"Prepared release metadata for {repository_url}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
