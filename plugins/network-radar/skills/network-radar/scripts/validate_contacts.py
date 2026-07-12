#!/usr/bin/env python3
"""Validate a Network Radar contact CSV and report actionable quality issues."""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path

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

    return {
        "path": str(path),
        "rows": len(rows),
        "unique_contacts": len(seen),
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

