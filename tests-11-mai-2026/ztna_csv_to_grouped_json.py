#!/usr/bin/env python3
"""Convert a ZTNA rules CSV to JSON grouped by Rule.

Rows sharing the same Rule are merged: AD Group and Description come from the
first row for that Rule; Private Resource, Destination, Protocole, and Port are
collected as a list under ``targets``.
"""

from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    p = argparse.ArgumentParser(
        description="Convert CSV (grouped by Rule column) to JSON.",
    )
    p.add_argument(
        "csv_file",
        type=Path,
        help="Path to the source CSV file",
    )
    p.add_argument(
        "-o",
        "--output",
        type=Path,
        default=None,
        metavar="PATH",
        help="Output JSON path (default: <csv-stem>-grouped.json next to the CSV)",
    )
    return p.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    csv_path: Path = args.csv_file

    if not csv_path.is_file():
        print(f"error: CSV file not found: {csv_path}", file=sys.stderr)
        return 1

    out_path: Path = args.output if args.output is not None else csv_path.with_name(
        f"{csv_path.stem}-grouped.json"
    )

    rule_order: list[str] = []
    grouped: dict[str, dict] = {}

    with csv_path.open(encoding="utf-8-sig", newline="") as f:
        for row in csv.DictReader(f):
            rule = (row.get("Rule") or "").strip()
            if not rule:
                continue

            target = {
                "Private Resource": (row.get("Private Resource") or "").strip(),
                "Destination": (row.get("Destination") or "").strip(),
                "Protocole": (row.get("Protocole") or "").strip(),
                "Port": (row.get("Port") or "").strip(),
            }

            if rule not in grouped:
                rule_order.append(rule)
                grouped[rule] = {
                    "Rule": rule,
                    "AD Group": (row.get("AD Group") or "").strip(),
                    "Description": (row.get("Description") or "").strip(),
                    "targets": [target],
                }
            else:
                grouped[rule]["targets"].append(target)

    out = [grouped[r] for r in rule_order]

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(
        json.dumps(out, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    n_rows = sum(len(grouped[r]["targets"]) for r in rule_order)
    print(f"Wrote {len(out)} rule objects ({n_rows} CSV rows) -> {out_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
