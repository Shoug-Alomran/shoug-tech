#!/usr/bin/env python3
"""Build the SE201 chapter mindmaps.

Content lives in se201_mindmap_content.py; the interactive page itself is
rendered by build_se401_study_tools.mindmap_html, which stamps the shared
mindmap template (the ETHCS303 chapter-1 page). SE322 is used as the layout
reference for the wrapper pages and the mindmaps hub, so SE201 comes out
identical to the SE322 mindmaps the rest of the site already uses.

Unlike the SE322 builder this one does not touch exams — SE201 already has
its own exam section.

    python3 scripts/build_se201_mindmaps.py
"""
from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import build_se401_study_tools as core
from se201_mindmap_content import CHAPTERS

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "docs/academics/software-engineering/se201"
MAPS = BASE / "extra-resources/mindmaps"
REF = ROOT / "docs/academics/software-engineering/se322"
REF_MAPS = REF / "extra-resources/mindmaps"
SIDEBAR_JSON = ROOT / "scripts/academic-sidebar.json"
COURSE_URL = "/academics/software-engineering/se201/extra-resources/mindmaps/"

FOLDER_ICON = ('<svg class="dir-folder-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
               'stroke-width="2" stroke-linecap="square" stroke-linejoin="square" aria-hidden="true">'
               '<path d="M3 7a1 1 0 0 1 1-1h5l2 2h9a1 1 0 0 1 1 1v9a1 1 0 0 1-1 1H4a1 1 0 0 1-1-1V7z"/></svg>')


def ref_chapters() -> list[tuple[str, str]]:
    """(slug, title) of the SE322 mindmaps, in chapter order, as the layout source."""
    out = []
    for d in sorted(p for p in REF_MAPS.iterdir() if p.is_dir()):
        page = next(p for p in d.glob("*.html") if p.name != "index.html")
        title = re.search(r"<title>(.*?)\s+—", page.read_text()).group(1)
        out.append((page.stem, title))
    return out


def retarget(text: str, pairs: list[tuple[str, str, str, str]]) -> str:
    """Swap SE322 slugs/titles for the SE201 ones, then the course code.

    Two-phase with placeholders so a replacement can never be re-matched by a
    later pair (SE322 titles share words with each other).
    """
    for i, (old_slug, old_title, _new_slug, _new_title) in enumerate(pairs):
        text = text.replace(old_slug, f"@@SLUG{i}@@").replace(old_title, f"@@TITLE{i}@@")
    for i, (_o_slug, _o_title, new_slug, new_title) in enumerate(pairs):
        text = text.replace(f"@@SLUG{i}@@", new_slug).replace(f"@@TITLE{i}@@", new_title)
    return text.replace("se322", "se201").replace("SE322", "SE201")


def build_pages(pairs) -> None:
    MAPS.mkdir(parents=True, exist_ok=True)
    for i, (slug, title, branches) in enumerate(CHAPTERS, 1):
        folder = MAPS / f"{i:02d}-{slug}"
        folder.mkdir(parents=True, exist_ok=True)

        page = core.mindmap_html(i, title, branches)
        page = page.replace("se401", "se201").replace("SE401", "SE201")
        folder.joinpath(f"{slug}.html").write_text(page)

        ref_dir = REF_MAPS / sorted(p.name for p in REF_MAPS.iterdir() if p.is_dir())[i - 1]
        wrapper = retarget((ref_dir / "index.html").read_text(), pairs)
        folder.joinpath("index.html").write_text(re.sub(r"[ \t]+\n", "\n", wrapper))


def build_hub(pairs) -> None:
    hub = retarget((REF_MAPS / "index.html").read_text(), pairs)
    MAPS.joinpath("index.html").write_text(re.sub(r"[ \t]+\n", "\n", hub))


def add_extra_resources_row() -> None:
    """Add one Mindmaps row to the SE201 study-material hub (idempotent)."""
    path = BASE / "extra-resources/index.html"
    text = path.read_text()
    row_marker = f'href="{COURSE_URL}" class="dir-row"'
    if row_marker in text:      # the sidebar also links here, so match the row itself
        return

    # Scope the search to the container: a greedy match over the whole page
    # ends at the footer's last link instead of at the last directory row.
    start = text.index('<div class="directory-container">')
    stop = text.index("<footer", start)
    insert_at = start + text[start:stop].rindex("</a>") + len("</a>")
    row = (f'\n                            <a {row_marker} data-ar-title="الخرائط الذهنية">\n'
           '                                <div class="dir-num">05</div>\n'
           f'                                <div class="dir-title"><span class="dir-title-text">Mindmaps</span>{FOLDER_ICON}</div>\n'
           '                                <div class="dir-status"><span class="status-tag available">AVAILABLE</span></div>\n'
           '                                <div class="dir-arrow">\n'
           '                                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="square"><path d="M5 12h14M12 5l7 7-7 7"/></svg>\n'
           '                                </div>\n'
           '                            </a>')
    text = text[:insert_at] + row + text[insert_at:]
    if ".dir-folder-icon {" not in text and ".dir-folder-icon{" not in text:
        text = text.replace("</style>", ".dir-title:has(.dir-folder-icon){display:flex;align-items:center;gap:10px}"
                                        ".dir-folder-icon{width:20px;height:20px;flex:0 0 auto;color:var(--text-tertiary);transition:.2s}"
                                        ".dir-row:hover .dir-folder-icon{color:var(--brand-purple);transform:translateY(-1px)}</style>", 1)
    path.write_text(text)


def update_sidebar_data() -> None:
    """Register the mindmaps in academic-sidebar.json — the nav's only source."""
    data = json.loads(SIDEBAR_JSON.read_text())
    key = "/academics/software-engineering/se201/extra-resources/"
    rows = [r for r in data["children"][key] if "/mindmaps/" not in r["url"]]
    rows.append({"url": COURSE_URL, "attrs": "", "label": "MINDMAPS"})
    for i, (slug, title, _b) in enumerate(CHAPTERS, 1):
        rows.append({"url": f"{COURSE_URL}{i:02d}-{slug}/", "attrs": "", "label": f"Chapter {i}: {title}"})
    data["children"][key] = rows
    SIDEBAR_JSON.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n")


def main() -> None:
    pairs = [(ref_slug, ref_title, slug, title)
             for (ref_slug, ref_title), (slug, title, _b) in zip(ref_chapters(), CHAPTERS)]
    build_pages(pairs)
    build_hub(pairs)
    add_extra_resources_row()
    update_sidebar_data()

    subprocess.run([sys.executable, str(ROOT / "scripts/build_academic_sidebar.py")], check=True)

    from fix_mindmap_sidebar_state import apply_course
    chapter_labels = {f"{i:02d}-{slug}": f"Chapter {i}: {title}"
                      for i, (slug, title, _b) in enumerate(CHAPTERS, 1)}
    apply_course("se201", BASE, chapter_labels)

    from fix_academic_sidebar_links import fix_page
    for page in [MAPS / "index.html", *MAPS.glob("*/index.html")]:
        fix_page(page)

    print(f"Built {len(CHAPTERS)} SE201 mindmaps")


if __name__ == "__main__":
    main()
