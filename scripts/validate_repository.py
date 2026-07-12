#!/usr/bin/env python3
"""Validate the public Network Radar plugin repository without external packages."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PLUGIN = ROOT / "plugins/network-radar"
MANIFEST = PLUGIN / ".codex-plugin/plugin.json"
MARKETPLACE = ROOT / ".agents/plugins/marketplace.json"
SKILL = PLUGIN / "skills/network-radar/SKILL.md"
PLACEHOLDER = "OWNER_" + "PLACEHOLDER"
SEMVER = re.compile(r"^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)(?:-[0-9A-Za-z.-]+)?(?:\+[0-9A-Za-z.-]+)?$")


def load_json(path: Path, errors: list[str]):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        errors.append(f"Missing {path.relative_to(ROOT)}")
    except json.JSONDecodeError as exc:
        errors.append(f"Invalid JSON in {path.relative_to(ROOT)}: {exc}")
    return {}


def validate_manifest(errors: list[str]) -> None:
    data = load_json(MANIFEST, errors)
    for field in ("name", "version", "description", "author", "skills", "interface"):
        if not data.get(field):
            errors.append(f"plugin.json missing {field}")
    if data.get("name") != "network-radar":
        errors.append("plugin.json name must be network-radar")
    if not SEMVER.fullmatch(str(data.get("version", ""))):
        errors.append("plugin.json version must be strict semver")
    if not isinstance(data.get("author"), dict) or not data.get("author", {}).get("name"):
        errors.append("plugin.json author.name is required")
    interface = data.get("interface")
    if not isinstance(interface, dict):
        errors.append("plugin.json interface must be an object")
        return
    for field in ("displayName", "shortDescription", "longDescription", "developerName", "category", "capabilities", "defaultPrompt"):
        if not interface.get(field):
            errors.append(f"plugin.json interface.{field} is required")
    prompts = interface.get("defaultPrompt", [])
    if not isinstance(prompts, list) or len(prompts) > 3 or any(len(str(x)) > 128 for x in prompts):
        errors.append("interface.defaultPrompt must contain at most 3 strings of at most 128 characters")


def validate_marketplace(errors: list[str]) -> None:
    data = load_json(MARKETPLACE, errors)
    entries = data.get("plugins", []) if isinstance(data, dict) else []
    matching = [entry for entry in entries if isinstance(entry, dict) and entry.get("name") == "network-radar"]
    if len(matching) != 1:
        errors.append("marketplace must contain exactly one network-radar entry")
        return
    entry = matching[0]
    if entry.get("source") != {"source": "local", "path": "./plugins/network-radar"}:
        errors.append("marketplace network-radar source path is invalid")
    policy = entry.get("policy", {})
    if policy.get("installation") != "AVAILABLE" or policy.get("authentication") not in {"ON_INSTALL", "ON_USE"}:
        errors.append("marketplace policy is invalid")


def validate_skill(errors: list[str]) -> None:
    try:
        text = SKILL.read_text(encoding="utf-8")
    except FileNotFoundError:
        errors.append("Missing network-radar SKILL.md")
        return
    match = re.match(r"^---\n(.*?)\n---\n", text, re.DOTALL)
    if not match:
        errors.append("SKILL.md frontmatter is invalid")
    else:
        frontmatter = match.group(1)
        name = re.search(r"^name:\s*(.+)$", frontmatter, re.MULTILINE)
        description = re.search(r"^description:\s*(.+)$", frontmatter, re.MULTILINE)
        if not name or name.group(1).strip() != "network-radar":
            errors.append("SKILL.md name must be network-radar")
        if not description or not description.group(1).strip():
            errors.append("SKILL.md description is required")

    for relative in re.findall(r"\]\((references/[^)]+)\)", text):
        if not (SKILL.parent / relative).is_file():
            errors.append(f"Broken SKILL.md reference: {relative}")

    for script in (SKILL.parent / "scripts").glob("*.py"):
        try:
            compile(script.read_text(encoding="utf-8"), str(script), "exec")
        except SyntaxError as exc:
            errors.append(f"Python syntax error in {script.name}: {exc}")


def validate_hygiene(errors: list[str], release: bool) -> None:
    forbidden_parts = {"__pycache__", ".DS_Store", "outputs", "private-data"}
    forbidden_suffixes = {".xlsx", ".xls", ".csv", ".tsv"}
    for path in ROOT.rglob("*"):
        relative = path.relative_to(ROOT)
        if any(part in forbidden_parts for part in relative.parts):
            errors.append(f"Forbidden generated/private path: {relative}")
        if path.is_file() and path.suffix.lower() in forbidden_suffixes:
            errors.append(f"Forbidden contact-data file: {relative}")
        if path.is_file() and path.suffix.lower() in {".md", ".json", ".yaml", ".yml", ".py", ".sh"}:
            text = path.read_text(encoding="utf-8")
            if "[TO" + "DO:" in text:
                errors.append(f"TODO placeholder in {relative}")
            if release and PLACEHOLDER in text:
                errors.append(f"Unresolved GitHub owner placeholder in {relative}")

    for required in (ROOT / "README.md", ROOT / "LICENSE", ROOT / "PRIVACY.md"):
        if not required.is_file():
            errors.append(f"Missing {required.name}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--release", action="store_true")
    args = parser.parse_args()
    errors: list[str] = []
    validate_manifest(errors)
    validate_marketplace(errors)
    validate_skill(errors)
    validate_hygiene(errors, args.release)
    if errors:
        print("Repository validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1
    print("Repository validation passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
