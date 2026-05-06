#!/usr/bin/env python3
"""Trim generated MkDocs search text to reduce first-load payload."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
INDEX = ROOT / "site" / "search" / "search_index.json"
MAX_TEXT_CHARS = 280


def compact_text(value: str) -> str:
    text = re.sub(r"\s+", " ", value).strip()
    if len(text) <= MAX_TEXT_CHARS:
        return text

    clipped = text[:MAX_TEXT_CHARS].rsplit(" ", 1)[0].rstrip()
    return f"{clipped}..."


def main() -> int:
    if not INDEX.is_file():
        print("[warn] search index not found; skipping trim")
        return 0

    before = INDEX.stat().st_size
    data = json.loads(INDEX.read_text(encoding="utf-8"))

    docs = data.get("docs", [])
    for doc in docs:
        text = doc.get("text")
        if isinstance(text, str):
            doc["text"] = compact_text(text)

    INDEX.write_text(
        json.dumps(data, ensure_ascii=False, separators=(",", ":")),
        encoding="utf-8",
    )

    after = INDEX.stat().st_size
    saved = before - after
    print(
        f"[ok] trimmed search index: {before // 1024} KiB -> "
        f"{after // 1024} KiB ({saved // 1024} KiB saved)"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
