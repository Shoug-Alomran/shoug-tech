#!/usr/bin/env python3
"""Keep course sidebars aligned with the active Mindmaps folder/page."""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COURSES = {
    "se401": ROOT / "docs/academics/software-engineering/se401",
    "se322": ROOT / "docs/academics/software-engineering/se322",
    "cys405": ROOT / "docs/academics/cybersecurity/cys405",
    "cys406": ROOT / "docs/academics/cybersecurity/cys406",
}


def chapter_entries(maps: Path):
    entries = []
    for folder in sorted(p for p in maps.iterdir() if p.is_dir()):
        match = re.match(r"(\d+)-(.+)", folder.name)
        if match:
            entries.append((int(match.group(1)), folder.name))
    return entries


def apply_course(code: str, base: Path) -> None:
    maps = base / "extra-resources/mindmaps"
    if not maps.exists():
        return
    entries = chapter_entries(maps)
    route = f"/academics/{'cybersecurity' if code.startswith('cys') else 'software-engineering'}/{code}"
    for page in [base / "extra-resources/index.html", maps / "index.html", *[maps / folder / "index.html" for _n, folder in entries]]:
        if not page.exists():
            continue
        inside_maps = maps == page.parent or maps in page.parents
        active_folder = page.parent.name if inside_maps and page.parent != maps else None
        children = []
        if (base / "extra-resources/summary/index.html").exists():
            children.append(f'<li class="tree-item tree-viewer"><a class="tree-file" href="{route}/extra-resources/summary/">SUMMARY</a></li>')
        map_active = " file-active" if inside_maps else ""
        map_dot = '<span class="status-dot"></span>' if inside_maps else ""
        children.append(f'<li class="tree-item tree-viewer{map_active}"><a class="tree-file" href="{route}/extra-resources/mindmaps/">{map_dot}MINDMAPS</a></li>')
        if active_folder:
            for number, folder in entries:
                active = " file-active" if folder == active_folder else ""
                dot = '<span class="status-dot"></span>' if active else ""
                children.append(f'<li class="tree-item tree-viewer{active}"><a class="tree-file" href="{route}/extra-resources/mindmaps/{folder}/">{dot}Chapter {number} Mindmap</a></li>')
        replacement = (
            f'<li class="tree-item tree-section file-active"><a class="tree-file" href="{route}/extra-resources/" '
            'data-en-text="STUDY MATERIAL" data-ar-text="المواد الدراسية"><span class="status-dot"></span>STUDY MATERIAL</a></li>'
            '<ul class="tree-children item-children is-open">' + ''.join(children) + '</ul>'
        )
        text = page.read_text()
        pattern = re.compile(
            r'<li class="tree-item tree-section(?: file-active)?"><a class="tree-file" href="[^"]*(?:study-material|extra-resources)/"[^>]*>.*?STUDY MATERIAL</a></li>'
            r'(?:<ul class="tree-children item-children is-open">.*?</ul>)?', re.S | re.I)
        text, count = pattern.subn(replacement, text, count=1)
        if count != 1:
            raise RuntimeError(f"Could not locate Study Material sidebar entry in {page}")
        # Remove the accidentally repurposed EXAMS/MINDMAPS entry from older generated hubs.
        text = re.sub(r'<li class="tree-item tree-section file-active"><a class="tree-file" href="[^"]*/exams/"[^>]*>.*?MINDMAPS</a></li>', '', text, count=1, flags=re.S)
        page.write_text(text)


def main() -> None:
    for code, base in COURSES.items():
        apply_course(code, base)


if __name__ == "__main__":
    main()
