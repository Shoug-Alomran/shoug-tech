#!/usr/bin/env python3
"""Move ECON101 from Other Courses to a new Business section (2026-11-27).

The folder itself was moved by hand (docs/academics/other-courses/econ101 ->
docs/academics/business/econ101). This does everything else, and is safe to
re-run:

  - rewrites every link to the old address in the site, its data files and the
    builders that generate pages, so future rebuilds keep the new address
  - points ECON101's breadcrumbs at Business
  - builds the Business section page from the Information Systems one
  - removes ECON101 from the Other Courses page and adds a Business card to
    /academics/, with the course counts updated
  - adds the BUSINESS/ group to the sidebar data and the Arabic labels
  - adds "business" wherever scripts keep a list of sections
  - adds 301 redirects from every old ECON101 address (legacy-redirects.json)
  - carries old "mark complete" records over to the new address, the same way
    STAT101's move to Math was handled

Then run the usual builders (see the end of main()).

    python3 scripts/move_econ101_to_business.py
"""
from __future__ import annotations

import json
import os
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"
OLD = "/academics/other-courses/econ101"
NEW = "/academics/business/econ101"
HUB = "/academics/business/"
TEXT = {".html", ".js", ".json", ".py", ".xml", ".txt", ".md", ".css", ".vtt", ".csv", ".mjs", ".cjs", ".jsonc"}
SKIP_DIRS = {".git", "node_modules", ".venv", "venv", ".wrangler", ".pages-build", ".r2-upload", ".pdf-cache"}
# Redirect tables keep old addresses as keys on purpose.
SKIP_FILES = {
    ROOT / "workers/indexing/src/legacy-redirects.json",
    ROOT / "workers/indexing/src/manifest.json",
    Path(__file__).resolve(),
}


def read(p: Path) -> str:
    return p.read_text(encoding="utf-8")


def write(p: Path, text: str) -> None:
    p.write_text(text, encoding="utf-8", newline="")


def text_files(*roots: Path):
    for root in roots:
        for dirpath, dirnames, filenames in os.walk(root):
            dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
            for name in filenames:
                p = Path(dirpath) / name
                if p.suffix.lower() in TEXT and p.resolve() not in SKIP_FILES:
                    yield p


def rewrite_paths() -> int:
    changed = 0
    for p in text_files(DOCS, ROOT / "scripts", ROOT / "templates", ROOT / "functions"):
        try:
            t = read(p)
        except UnicodeDecodeError:
            continue
        if "other-courses/econ101" not in t and "other-courses|econ101" not in t:
            continue
        n = t.replace("other-courses/econ101", "business/econ101").replace("other-courses|econ101", "business|econ101")
        if n != t:
            write(p, n)
            changed += 1
    return changed


def fix_breadcrumbs() -> int:
    """ECON101 pages linked "Other Courses" in their breadcrumb."""
    changed = 0
    for p in (DOCS / "academics/business/econ101").rglob("*.html"):
        t = read(p)
        n = re.sub(
            r'(<a\s+class="breadcrumb-link"\s+href=")/academics/other-courses/("[^>]*?)(?:\s+data-ar-text="[^"]*")?(\s*>\s*)Other Courses(\s*</a)',
            lambda m: m.group(1) + HUB + m.group(2) + ' data-ar-text="إدارة الأعمال"' + m.group(3) + "Business" + m.group(4),
            t,
        )
        if n != t:
            write(p, n)
            changed += 1
    return changed


def course_row(t: str) -> str:
    m = re.search(r'<a class="course-row" href="%s/"\s*>.*?</a\s*>' % re.escape(NEW), t, re.S)
    if not m:
        raise SystemExit("ECON101 row not found on the Other Courses page")
    return m.group(0)


def build_hub(row: str) -> None:
    path = DOCS / "academics/business/index.html"
    t = read(DOCS / "academics/information-system/index.html")
    t = t.replace("/academics/information-system/", HUB)
    t = t.replace("SHOUG.TECH // INFORMATION SYSTEMS", "SHOUG.TECH // BUSINESS")
    t = t.replace('<div class="hero-label">[ INFORMATION SYSTEMS ]</div>', '<div class="hero-label">[ BUSINESS ]</div>')
    t = t.replace("TRACK.ID: 0xIS_01", "TRACK.ID: 0xBU_01")
    t = t.replace('<span vid="73">Information Systems</span>', '<span vid="73" data-ar-text="إدارة الأعمال">Business</span>')
    t, n = re.subn(r'<h1 class="hero-title">.*?</h1>',
                   '<h1 class="hero-title">\n              Business.<br />Economics, markets,<br />and decisions.\n            </h1>', t, count=1, flags=re.S)
    assert n == 1, "hero title"
    t, n = re.subn(r'<div class="hero-metadata-strip">.*?</div>',
                   '<div class="hero-metadata-strip">\n              <span>Business Track</span><span class="meta-sep">//</span\n              ><span>Economics</span><span class="meta-sep">·</span\n              ><span>Markets</span><span class="meta-sep">·</span\n              ><span>Decisions</span>\n            </div>', t, count=1, flags=re.S)
    assert n == 1, "metadata strip"
    t, n = re.subn(r'(<div class="course-list">).*?(\n\s*</div>\n\s*</div>\n\s*</main>)', lambda m: m.group(1) + "\n            " + row + m.group(2), t, count=1, flags=re.S)
    assert n == 1, "course list"
    # The hero is re-written on load from these tables (English, then Arabic).
    tables = [
        ("BUSINESS", "Business.<br>Economics, markets,<br>and decisions.", ["Business Track", "Economics", "Markets", "Decisions"]),
        ("إدارة الأعمال", "إدارة الأعمال.<br>الاقتصاد، والأسواق،<br>واتخاذ القرار.", ["مسار إدارة الأعمال", "الاقتصاد", "الأسواق", "القرارات"]),
    ]
    for label, title, meta in tables:
        t, a = re.subn(r'"information systems":\s*"[^"]*",', '"business": %s,' % json.dumps(label, ensure_ascii=False), t, count=1)
        t, b = re.subn(r'"information systems":\s*"[^"]*",', '"business": %s,' % json.dumps(title, ensure_ascii=False), t, count=1)
        t, c = re.subn(r'"information systems":\s*\[[^\]]*\],', '"business": %s,' % json.dumps(meta, ensure_ascii=False), t, count=1)
        # Some tables put the value on the next line.
        if not b:
            t, b = re.subn(r'"information systems":\s*\n\s*"[^"]*",', '"business": %s,' % json.dumps(title, ensure_ascii=False), t, count=1)
        if not (a and b and c):
            raise SystemExit("hub translation tables not found (%s %s %s)" % (a, b, c))
    left = re.findall(r"information.?system", t, re.I)
    if left:
        print("note: Business page still mentions Information Systems %d times (sidebar is restamped later)" % len(left))
    write(path, t)


def update_other_hub() -> str:
    path = DOCS / "academics/other-courses/index.html"
    t = read(path)
    row = course_row(t)
    t = t.replace(row, "", 1)
    t = re.sub(r'("other courses":\s*")\d+ courses\.', r"\g<1>7 courses.", t)
    t = re.sub(r'("other courses":\s*\[\s*"General Track",\s*")\d+ Courses"', r'\g<1>7 Courses"', t)
    write(path, t)
    return row


def update_academics_hub() -> None:
    path = DOCS / "academics/index.html"
    t = read(path)
    if 'href="%s" class="track-card"' % HUB not in t:
        m = re.search(r'<a href="/academics/information-system/" class="track-card"[^>]*>.*?</a>', t, re.S)
        if not m:
            raise SystemExit("academics hub has no Information Systems card")
        card = m.group(0).replace("/academics/information-system/", HUB)
        card = re.sub(r'(<h2 class="card-title display")[^>]*>.*?</h2>',
                      lambda x: x.group(1) + ' data-ar-text="إدارة الأعمال">BUSINESS</h2>', card, count=1, flags=re.S)
        card = re.sub(r'(<div class="card-count mono"[^>]*>)\s*\d+\s*', r"\g<1>01", card, count=1)
        tags = "".join('<span class="tag-item" data-ar-text="%s">%s</span>' % (ar, en) for en, ar in (
            ("Economics", "الاقتصاد"), ("Markets", "الأسواق"), ("Decisions", "القرارات")))
        card, n = re.subn(r'(<div class="card-tags mono"[^>]*>).*?(</div>)', lambda x: x.group(1) + tags + x.group(2), card, count=1, flags=re.S)
        if n != 1:
            raise SystemExit("IS card has no tags")
        other = re.search(r'<a href="/academics/other-courses/" class="track-card"', t)
        if not other:
            raise SystemExit("academics hub has no Other Courses card")
        t = t[: other.start()] + card + "\n\n          " + t[other.start():]
    # Other Courses: one course fewer, and Economics now has its own section.
    t = re.sub(r'(href="/academics/other-courses/" class="track-card".*?<div class="card-count mono"[^>]*>)\s*\d+', r"\g<1>07", t, count=1, flags=re.S)
    t = re.sub(r'(href="/academics/other-courses/" class="track-card".*?<div class="card-tags mono"[^>]*>.*?)<span class="tag-item"[^>]*>Economics</span>',
               lambda m: m.group(1) + '<span class="tag-item" data-ar-text="الدراسات الإسلامية">Islamic Studies</span>', t, count=1, flags=re.S)
    t = re.sub(r'("other courses":\s*")\d+ courses\.', r"\g<1>7 courses.", t)
    t = re.sub(r'("other courses":\s*\[\s*"General Track",\s*")\d+ Courses"', r'\g<1>7 Courses"', t)
    write(path, t)


def update_sidebar_data() -> None:
    path = ROOT / "scripts/academic-sidebar.json"
    data = json.loads(read(path))
    tree = data["tree"]
    other = next(g for g in tree if g.get("id") == "tree-other-courses")
    node = next((c for c in other["children"] if c.get("url") == NEW + "/"), None)
    business = next((g for g in tree if g.get("id") == "tree-business"), None)
    if business is None:
        business = {"type": "group", "id": "tree-business", "label": "BUSINESS/", "children": []}
        tree.insert(tree.index(other), business)
    if node is not None:
        other["children"].remove(node)
        business["children"].append(node)
    write(path, json.dumps(data, ensure_ascii=False, indent=2) + "\n")


def update_arabic() -> None:
    path = DOCS / "javascripts/arabic-localization.js"
    t = read(path)
    if '"BUSINESS/"' not in t:
        anchor = '    "OTHER COURSES/": "مواد أخرى/",\n'
        if anchor not in t:
            raise SystemExit("arabic-localization.js lost its sidebar table")
        t = t.replace(anchor, '    "BUSINESS/": "إدارة الأعمال/",\n    "Business": "إدارة الأعمال",\n' + anchor, 1)
        write(path, t)


def update_section_lists() -> None:
    edits = [
        (DOCS / "javascripts/course-ratings.js",
         '"computer-science|software-engineering|cybersecurity|math|information-system|other-courses"',
         '"computer-science|software-engineering|cybersecurity|math|information-system|business|other-courses"'),
        (ROOT / "scripts/improve_seo_snippets.py", '"information-system": "Information Systems",',
         '"information-system": "Information Systems", "business": "Business",'),
        (ROOT / "scripts/install_annotated_study.py", '"information-system": "Information Systems",',
         '"information-system": "Information Systems",\n    "business": "Business",'),
        (ROOT / "scripts/build_final_cheat_sheets.py", '"information-system": "Information Systems",',
         '"information-system": "Information Systems",\n    "business": "Business",'),
        (DOCS / "javascripts/firebase-auth.js", "Information Systems, Math, or Other Courses",
         "Information Systems, Math, Business, or Other Courses"),
    ]
    for path, old, new in edits:
        t = read(path)
        if new in t:
            continue
        if old not in t:
            print("note: %s has no %r, skipped" % (path.relative_to(ROOT), old[:40]))
            continue
        write(path, t.replace(old, new, 1))


def update_progress_remaps() -> None:
    """Old completions are stored under the old URL; count them for the new one."""
    stat = re.compile(r'\.replace\(\s*/other-courses\(\\/\|%2F\)stat101/gi,\s*"math\$1stat101",?\s*\)')
    econ = '.replace(/other-courses(\\/|%2F)econ101/gi, "business$1econ101")'
    for rel in ("javascripts/firebase-auth.js", "community/profile/index.html", "account/course/index.html", "account/index.html"):
        p = DOCS / rel
        t = read(p)
        if "business$1econ101" in t:
            continue
        n, count = stat.subn(lambda m: m.group(0) + econ, t)
        if not count:
            print("note: no STAT101 remap found in", rel)
            continue
        write(p, n)


def add_redirects() -> int:
    path = ROOT / "workers/indexing/src/legacy-redirects.json"
    redirects = json.loads(read(path))
    added = 0
    for p in (DOCS / "academics/business/econ101").rglob("*"):
        if not p.is_file():
            continue
        rel = "/" + p.relative_to(DOCS).as_posix()
        old = rel.replace(NEW, OLD, 1)
        if p.name == "index.html":
            pairs = [(old[: -len("index.html")], rel[: -len("index.html")])]
        else:
            pairs = [(old, rel)]
        for o, n in pairs:
            if redirects.get(o) != n:
                redirects[o] = n
                added += 1
    # Older redirects that pointed into the old folder now point to the new one.
    for k, v in list(redirects.items()):
        if v.startswith(OLD):
            redirects[k] = NEW + v[len(OLD):]
    write(path, json.dumps(dict(sorted(redirects.items())), ensure_ascii=False, indent=2) + "\n")
    return added


def run(cmd: list[str]) -> None:
    print("$", " ".join(cmd))
    subprocess.run(cmd, cwd=ROOT, check=True)


def main() -> None:
    if not (DOCS / "academics/business/econ101/index.html").exists():
        raise SystemExit("Move the folder to docs/academics/business/econ101 first.")
    print("files with the old address rewritten:", rewrite_paths())
    print("breadcrumbs fixed:", fix_breadcrumbs())
    row = update_other_hub() if NEW in read(DOCS / "academics/other-courses/index.html") else None
    if row:
        build_hub(row)
    elif not (DOCS / "academics/business/index.html").exists():
        raise SystemExit("ECON101 row missing from Other Courses and no Business page yet")
    update_academics_hub()
    update_sidebar_data()
    update_arabic()
    update_section_lists()
    update_progress_remaps()
    print("redirects added:", add_redirects())
    if "--no-build" not in sys.argv:
        py = sys.executable
        run([py, "scripts/build_academic_sidebar.py"])
        run([py, "scripts/build_indexing_manifest.py"])
        run(["node", "scripts/build-course-manifest.js"])
        run(["node", "scripts/build-search-index.js"])
        run([py, "scripts/check_sitemap.py", "--write"])


if __name__ == "__main__":
    main()
