#!/usr/bin/env python3
"""Apply configurable hard admission gates to a contact CSV."""

from __future__ import annotations

import argparse
import csv
import json
import re
from pathlib import Path


def read_csv(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        return list(reader.fieldnames or []), [dict(row) for row in reader]


def compile_many(patterns: list[str]) -> list[re.Pattern[str]]:
    return [re.compile(pattern, re.IGNORECASE) for pattern in patterns if pattern]


def matches_any(value: str, patterns: list[re.Pattern[str]]) -> bool:
    return any(pattern.search(value) for pattern in patterns)


def normalize(value: str) -> str:
    return re.sub(r"\s+", "", value or "").casefold()


def classify(row: dict[str, str], config: dict) -> tuple[str, str]:
    company_field = config.get("company_field", "公司")
    role_field = config.get("role_field", "岗位/简介")
    evidence_field = config.get("evidence_field", "备注/证据")
    company = (row.get(company_field) or "").strip()
    role = (row.get(role_field) or "").strip()
    evidence = (row.get(evidence_field) or "").strip()

    company_exact = {normalize(value) for value in config.get("company_allow_exact", [])}
    company_patterns = compile_many(config.get("company_allow_regex", []))
    role_allow = compile_many(config.get("role_allow_regex", []))
    role_exclude = compile_many(config.get("role_exclude_regex", []))
    role_ambiguous = compile_many(config.get("role_ambiguous_regex", []))
    evidence_allow = compile_many(config.get("evidence_allow_regex", []))
    evidence_exclude = compile_many(config.get("evidence_exclude_regex", []))

    if not company:
        return "待核验", "当前公司缺失"
    if company_exact or company_patterns:
        company_ok = normalize(company) in company_exact or matches_any(company, company_patterns)
        if not company_ok:
            return "排除", f"当前公司不符合目标：{company}"

    if not role:
        return "待核验", "当前岗位缺失"
    if matches_any(role, role_exclude):
        return "排除", f"当前岗位属于排除职能：{role}"

    decisive_role = matches_any(role, role_allow)
    conflicting_evidence = matches_any(evidence, evidence_exclude)
    supporting_evidence = matches_any(evidence, evidence_allow)

    if decisive_role:
        if conflicting_evidence:
            return "待核验", "当前岗位与职业线证据冲突"
        return "合格", "当前公司与目标岗位均通过硬门槛"

    if matches_any(role, role_ambiguous):
        if supporting_evidence and not conflicting_evidence:
            return "合格", "当前岗位表述较泛，但职业线支持目标职能"
        return "待核验", f"当前岗位表述需要详情核验：{role}"

    if supporting_evidence and not conflicting_evidence:
        return "待核验", "职业线可能匹配，但当前岗位缺少明确目标职能"
    return "待核验", f"未取得明确的目标岗位证据：{role}"


def write_csv(path: Path, headers: list[str], rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=headers)
        writer.writeheader()
        writer.writerows(rows)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("csv_path", type=Path)
    parser.add_argument("--config", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--eligible", type=Path)
    parser.add_argument("--pending", type=Path)
    parser.add_argument("--excluded", type=Path)
    args = parser.parse_args()

    headers, rows = read_csv(args.csv_path)
    config = json.loads(args.config.read_text(encoding="utf-8"))
    out_headers = headers + [name for name in ("入池状态", "清洗原因") if name not in headers]
    buckets = {"合格": [], "待核验": [], "排除": []}
    audited = []
    for row in rows:
        state, reason = classify(row, config)
        result = dict(row)
        result["入池状态"] = state
        result["清洗原因"] = reason
        audited.append(result)
        buckets[state].append(result)

    write_csv(args.output, out_headers, audited)
    for path, state in ((args.eligible, "合格"), (args.pending, "待核验"), (args.excluded, "排除")):
        if path:
            write_csv(path, out_headers, buckets[state])

    summary = {
        "rows": len(audited),
        "eligible": len(buckets["合格"]),
        "pending": len(buckets["待核验"]),
        "excluded": len(buckets["排除"]),
    }
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
