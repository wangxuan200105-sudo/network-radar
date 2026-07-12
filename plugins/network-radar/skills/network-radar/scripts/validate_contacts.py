#!/usr/bin/env python3
"""Validate a Network Radar contact CSV and report actionable quality issues."""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
from urllib.parse import parse_qs, urlsplit

from merge_contacts import COLUMNS, stable_key


VALID_PRIORITIES = {"高", "中", "低"}
VALID_VERIFICATION = {"已核验", "部分核验", "待核验", "冲突"}


def read_csv(path: Path):
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        headers = reader.fieldnames or []
        rows = [dict(row) for row in reader]
    return headers, rows


def validate(path: Path) -> dict:
    headers, rows = read_csv(path)
    errors: list[dict] = []
    warnings: list[dict] = []
    missing = [column for column in COLUMNS if column not in headers]
    if missing:
        errors.append({"type": "missing_columns", "columns": missing})
        return {"path": str(path), "rows": len(rows), "errors": errors, "warnings": warnings}

    seen: dict[str, int] = {}
    token_owners: dict[str, list[tuple[int, str]]] = {}
    maimai_links = {
        "total": 0,
        "full_detail": 0,
        "full_token": 0,
        "search_fallback_primary": 0,
        "missing_link": 0,
        "missing_token": 0,
        "missing_search_fallback_note": 0,
    }
    for number, row in enumerate(rows, start=2):
        key = stable_key(row)
        if key in seen:
            errors.append(
                {"type": "duplicate", "row": number, "first_row": seen[key], "stable_key": key}
            )
        else:
            seen[key] = number

        priority = (row.get("优先级") or "").strip()
        verification = (row.get("核验状态") or "").strip()
        if priority not in VALID_PRIORITIES:
            errors.append({"type": "invalid_priority", "row": number, "value": priority})
        if verification not in VALID_VERIFICATION:
            errors.append({"type": "invalid_verification", "row": number, "value": verification})
        if priority == "高" and not (row.get("优先级理由") or "").strip():
            errors.append({"type": "high_without_reason", "row": number})
        if verification == "已核验" and not (row.get("备注/证据") or "").strip():
            warnings.append({"type": "verified_without_evidence_note", "row": number})
        if priority == "高" and verification == "待核验":
            warnings.append({"type": "high_but_unverified", "row": number})
        if not (row.get("姓名/昵称") or "").strip():
            errors.append({"type": "missing_name", "row": number})
        if not (row.get("平台") or "").strip():
            errors.append({"type": "missing_platform", "row": number})

        platform = (row.get("平台") or "").strip().lower()
        if platform in {"脉脉", "maimai"}:
            maimai_links["total"] += 1
            raw_url = (row.get("主页链接") or "").strip()
            notes = row.get("备注/证据") or ""
            if not raw_url:
                maimai_links["missing_link"] += 1
                errors.append({"type": "missing_maimai_link", "row": number})
                continue
            try:
                parts = urlsplit(raw_url)
            except ValueError:
                errors.append({"type": "invalid_maimai_url", "row": number})
                continue
            query = parse_qs(parts.query)
            host = parts.netloc.lower()
            if not (host == "maimai.cn" or host.endswith(".maimai.cn")):
                warnings.append({"type": "unexpected_maimai_link_host", "row": number, "host": host})

            if parts.path.rstrip("/") == "/profile/detail":
                maimai_links["full_detail"] += 1
                dstu = (query.get("dstu") or [""])[0]
                token = (query.get("trackable_token") or [""])[0]
                source = (query.get("from") or [""])[0]
                if not dstu:
                    errors.append({"type": "maimai_detail_link_missing_dstu", "row": number})
                if not token:
                    maimai_links["missing_token"] += 1
                    warnings.append({"type": "maimai_detail_link_missing_token", "row": number, "dstu": dstu})
                else:
                    maimai_links["full_token"] += 1
                    token_owners.setdefault(token, []).append((number, dstu))
                if source != "pc_web_search":
                    warnings.append(
                        {"type": "maimai_detail_link_missing_search_context", "row": number, "dstu": dstu}
                    )
                if "search_center" not in notes:
                    maimai_links["missing_search_fallback_note"] += 1
                    warnings.append({"type": "missing_maimai_search_fallback_note", "row": number})
            elif parts.path.rstrip("/") == "/web/search_center":
                maimai_links["search_fallback_primary"] += 1
                if not (query.get("query") or [""])[0]:
                    warnings.append({"type": "empty_maimai_search_fallback", "row": number})
            else:
                warnings.append(
                    {"type": "unsupported_maimai_link_shape", "row": number, "path": parts.path}
                )

    for owners in token_owners.values():
        distinct_ids = {dstu for _, dstu in owners if dstu}
        if len(distinct_ids) > 1:
            errors.append(
                {
                    "type": "reused_maimai_trackable_token",
                    "rows": [row_number for row_number, _ in owners],
                    "dstu_ids": sorted(distinct_ids),
                }
            )

    maimai_total = maimai_links["total"]
    maimai_links["full_token_coverage"] = (
        round(maimai_links["full_token"] / maimai_total, 4) if maimai_total else None
    )
    maimai_links["fallback_primary_coverage"] = (
        round(maimai_links["search_fallback_primary"] / maimai_total, 4) if maimai_total else None
    )

    return {
        "path": str(path),
        "rows": len(rows),
        "unique_contacts": len(seen),
        "maimai_links": maimai_links,
        "errors": errors,
        "warnings": warnings,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("csv_path", type=Path)
    parser.add_argument("--strict", action="store_true", help="Treat warnings as failure")
    args = parser.parse_args()

    result = validate(args.csv_path)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    failed = bool(result["errors"]) or (args.strict and bool(result["warnings"]))
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
