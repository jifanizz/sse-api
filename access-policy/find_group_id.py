"""Find the identity ID for a given label in secure-access-group.json.

Looks for entries in `data[]` whose `label` matches the target string and
prints the associated `id`.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

DATA_FILE = Path(__file__).resolve().parent / "secure-access-group.json"

TARGET_LABEL = "Protected Users (example.com\\\\Protected Users)"


def load_identities(path: Path) -> dict:
    raw = path.read_text(encoding="utf-8").strip()
    
    # Remove trailing quote if present (happens if the `b'` prefix was partially removed)
    if raw.endswith("'"):
        raw = raw[:-1]
    
    # Fix Python byte string escapes that might be in the JSON
    # e.g., \xe2\x80\x99 -> ’
    def replace_hex(match):
        hex_str = match.group(0).replace('\\x', '')
        try:
            return bytes.fromhex(hex_str).decode('utf-8', errors='replace')
        except ValueError:
            return match.group(0)

    raw_fixed = re.sub(r'(?:\\x[0-9a-fA-F]{2})+', replace_hex, raw)
    
    return json.loads(raw_fixed)


def main() -> int:
    try:
        payload = load_identities(DATA_FILE)
    except Exception as e:
        print(f"Error loading file: {e}", file=sys.stderr)
        return 1

    matches = [item for item in payload.get("data", []) if item.get("label") == TARGET_LABEL]

    if not matches:
        print(f"No entry found with label == {TARGET_LABEL!r}")
        return 1

    for item in matches:
        print(item["id"])
    return 0


if __name__ == "__main__":
    sys.exit(main())
