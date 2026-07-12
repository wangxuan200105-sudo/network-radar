#!/usr/bin/env python3
"""Merge a fresh Network Radar CSV into an earlier CSV and emit a change log."""

from __future__ import annotations

import argparse
import csv
import re
from pathlib import Path
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit


COLUMNS = [
    "姓名/昵称",
    "平台",
    "主页链接",
    "公司",
    "岗位/简介",
    "城市/地区",
    "方向标签",
    "角色类型",
    "关系钩子",
    "核验状态",
    "优先级",
    "优先级理由",
    "建联状态",
    "推荐开场白",
    "备注/证据",
]

PRESERVE_OLD = {"建联状态", "推荐开场白"}
ID_QUERY_KEYS = ("dstu", "uid", "user_id", "id")
DROP_QUERY_KEYS = {
    "trackable_token",
    "from",
    "outofrel",
    "is_node",
    "utm_source",
    "utm_medium",
    "utm_campaign",
}


def norm(value: str) -> str:
    return re.sub(r"\s+", "", (value or "").strip().lower())


def canonical_url(raw_url: str) -> tuple[str, str]:
    raw_url = (raw_url or "").strip()
    if not raw_url:
        return "", ""
    try:
        parts = urlsplit(raw_url)
    except ValueError:
        return "", raw_url
    query = dict(parse_qsl(parts.query, keep_blank_values=True))
    for key in ID_QUERY_KEYS:
        if query.get(key):
            return f"{parts.netloc.lower()}:{key}:{query[key]}", raw_url
    kept = sorted((k, v) for k, v in query.items() if k not in DROP_QUERY_KEYS)
    canonical = urlunsplit(
        (parts.scheme.lower(), parts.netloc.lower(), parts.path.rstrip("/"), urlencode(kept), "")
    )
    return canonical, raw_url


def stable_key(row: dict[str, str]) -> str:
    url_key, _ = canonical_url(row.get("主页链接", ""))
    if url_key:
        return f"url:{url_key}"
    fallback = "|".join(
        norm(row.get(field, ""))
        for field in ("平台", "姓名/昵称", "公司", "岗位/简介")
    )
    return f"fallback:{fallback}"


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        headers = reader.fieldnames or []
        missing = [column for column in COLUMNS if column not in headers]
        if missing:
            raise ValueError(f"{path} 缺少字段：{', '.join(missing)}")
        return [{column: (row.get(column) or "").strip() for column in COLUMNS} for row in reader]


def write_rows(path: Path, headers: list[str], rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=headers, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def combine_notes(old: str, fresh: str) -> str:
    old = (old or "").strip()
    fresh = (fresh or "").strip()
    if not old:
        return fresh
    if not fresh or fresh in old:
        return old
    if old in fresh:
        return fresh
    return f"{old} | {fresh}"


def change_type(field: str) -> str:
    if field == "关系钩子":
        return "关系标签补充"
    if field in {"优先级", "优先级理由"}:
        return "优先级调整"
    return "字段修正"


def merge(old_rows: list[dict[str, str]], fresh_rows: list[dict[str, str]]):
    old_by_key: dict[str, dict[str, str]] = {}
    for row in old_rows:
        old_by_key.setdefault(stable_key(row), row)

    merged_rows: list[dict[str, str]] = []
    changes: list[dict[str, str]] = []
    matched_old: set[str] = set()

    for fresh in fresh_rows:
        key = stable_key(fresh)
        old = old_by_key.get(key)
        if old is None:
            merged_rows.append(fresh)
            changes.append(
                {
                    "稳定标识": key,
                    "姓名/昵称": fresh["姓名/昵称"],
                    "变更类型": "新增",
                    "字段": "",
                    "旧值": "",
                    "新值": fresh["岗位/简介"],
                }
            )
            continue

        matched_old.add(key)
        merged = dict(old)
        for field in COLUMNS:
            old_value = old.get(field, "")
            fresh_value = fresh.get(field, "")
            if field in PRESERVE_OLD and old_value:
                new_value = old_value
            elif field == "备注/证据":
                new_value = combine_notes(old_value, fresh_value)
            elif fresh_value:
                new_value = fresh_value
            else:
                new_value = old_value
            merged[field] = new_value

            same_profile_link = (
                field == "主页链接"
                and canonical_url(old_value)[0]
                and canonical_url(old_value)[0] == canonical_url(new_value)[0]
            )
            if new_value != old_value and field != "备注/证据" and not same_profile_link:
                changes.append(
                    {
                        "稳定标识": key,
                        "姓名/昵称": merged["姓名/昵称"],
                        "变更类型": change_type(field),
                        "字段": field,
                        "旧值": old_value,
                        "新值": new_value,
                    }
                )
        merged_rows.append(merged)

    for old in old_rows:
        key = stable_key(old)
        if key in matched_old:
            continue
        merged_rows.append(old)
        changes.append(
            {
                "稳定标识": key,
                "姓名/昵称": old["姓名/昵称"],
                "变更类型": "本次未发现",
                "字段": "",
                "旧值": old["岗位/简介"],
                "新值": "",
            }
        )

    return merged_rows, changes


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("old_csv", type=Path)
    parser.add_argument("fresh_csv", type=Path)
    parser.add_argument("output_csv", type=Path)
    parser.add_argument("--changes", type=Path, required=True, help="Change-log CSV path")
    args = parser.parse_args()

    old_rows = read_rows(args.old_csv)
    fresh_rows = read_rows(args.fresh_csv)
    merged_rows, changes = merge(old_rows, fresh_rows)
    write_rows(args.output_csv, COLUMNS, merged_rows)
    write_rows(
        args.changes,
        ["稳定标识", "姓名/昵称", "变更类型", "字段", "旧值", "新值"],
        changes,
    )
    print(
        f"merged={len(merged_rows)} changes={len(changes)} "
        f"output={args.output_csv} change_log={args.changes}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
