#!/usr/bin/env python3
"""Keep collection folders above individual resources in academic listings."""

from __future__ import annotations

import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ACADEMICS = ROOT / "docs" / "academics"

ROW_RE = re.compile(
    r'(?P<indent>[ \t]*)<a\b(?=[^>]*\bclass="[^"]*\bdir-row\b[^"]*")[^>]*>.*?</a>',
    re.DOTALL,
)
NUMBER_RE = re.compile(r'(<div class="dir-num">)\d+(</div>)')


def sort_folder_rows(text: str) -> tuple[str, bool]:
    """Move rows carrying ``dir-folder-icon`` before all file rows."""
    matches = list(ROW_RE.finditer(text))
    if not matches or not any("dir-folder-icon" in match.group(0) for match in matches):
        return text, False

    # Listings on these pages contain one contiguous group of dir-row anchors.
    groups: list[list[re.Match[str]]] = []
    current: list[re.Match[str]] = []
    for match in matches:
        if current and text[current[-1].end() : match.start()].strip():
            groups.append(current)
            current = []
        current.append(match)
    if current:
        groups.append(current)

    changed = False
    for group in reversed(groups):
        rows = [match.group(0) for match in group]
        ordered = [row for row in rows if "dir-folder-icon" in row]
        ordered.extend(row for row in rows if "dir-folder-icon" not in row)
        ordered = [
            NUMBER_RE.sub(rf"\g<1>{index:02d}\g<2>", row, count=1)
            for index, row in enumerate(ordered, start=1)
        ]
        if ordered == rows:
            continue

        separator = text[group[0].end() : group[1].start()] if len(group) > 1 else "\n"
        replacement = separator.join(ordered)
        text = text[: group[0].start()] + replacement + text[group[-1].end() :]
        changed = True

    return text, changed


def main() -> None:
    changed_files = 0
    for path in sorted(ACADEMICS.rglob("index.html")):
        original = path.read_text()
        updated, changed = sort_folder_rows(original)
        if changed:
            path.write_text(updated)
            changed_files += 1
            print(path.relative_to(ROOT))
    print(f"[ok] folder-first ordering applied to {changed_files} academic pages")


if __name__ == "__main__":
    main()
