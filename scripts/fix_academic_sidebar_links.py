#!/usr/bin/env python3
"""Normalize internal links inside academic sidebars to real docs routes."""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"


def course_base(code: str) -> str:
    code = code.lower()
    if code.startswith("cs") and not code.startswith("cys"):
        track = "computer-science"
    elif code.startswith("se"):
        track = "software-engineering"
    elif code.startswith("cys"):
        track = "cybersecurity"
    elif code.startswith(("phy", "sci", "stat", "math")):
        track = "math"
    else:
        track = "other-courses"
    return f"/academics/{track}/{code}/"


def normalize(href: str) -> str:
    if href == "/Academics/":
        return "/academics/"
    match = re.fullmatch(r"/course-([a-z0-9]+)\.html", href, re.I)
    if match:
        return course_base(match.group(1))
    match = re.match(r"/Academics/courses/([a-z0-9]+)/?(.*)", href, re.I)
    if match:
        href = course_base(match.group(1)) + match.group(2)
    href = re.sub(r"^/Academics/", "/academics/", href)
    href = re.sub(r"^/academics/cyber-security/", "/academics/cybersecurity/", href, flags=re.I)
    href = re.sub(r"^/academics/other/", "/academics/other-courses/", href, flags=re.I)
    href = re.sub(r"^/academics/other-courses/((?:phy|sci|stat|math)[a-z0-9]*)/", r"/academics/math/\1/", href, flags=re.I)
    href = re.sub(r"^/academics/(computer-science|software-engineering|cybersecurity|math|other-courses)/([A-Z0-9]+)", lambda m: f"/academics/{m.group(1).lower()}/{m.group(2).lower()}", href)
    href = href.replace("/study-material/", "/extra-resources/")
    href = href.replace("/quizzes/", "/exams/").replace("/quizez/", "/exams/")
    path_only = href.split("?", 1)[0].split("#", 1)[0]
    target = DOCS / path_only.lstrip("/")
    exists = target.is_file() if target.suffix else (target / "index.html").is_file()
    if not exists and "/slides/" in path_only:
        return path_only.split("/slides/", 1)[0] + "/slides/"
    return href


def fix_page(path: Path) -> int:
    text = path.read_text(errors="ignore")
    if "academic-sidebar" not in text:
        return 0
    changed = 0
    def sidebar_repl(match: re.Match[str]) -> str:
        nonlocal changed
        block = match.group(0)
        if '/academics/cybersecurity/cys405/' not in block and '/academics/cybersecurity/cys406/' in block:
            cys405 = '<li class="tree-item"><a class="tree-file" href="/academics/cybersecurity/cys405/">CYS405</a></li>'
            block, inserted = re.subn(r'(?=<li[^>]*>\s*<a[^>]*href="/academics/cybersecurity/cys406/"[^>]*>.*?CYS406</a>\s*</li>)', cys405, block, count=1, flags=re.S)
            changed += inserted
        def href_repl(link: re.Match[str]) -> str:
            nonlocal changed
            old = link.group(1); new = normalize(old)
            changed += old != new
            return f'href="{new}"'
        return re.sub(r'href="([^"]+)"', href_repl, block)
    text = re.sub(r'<nav\b[^>]*class="[^"]*\bacademic-sidebar\b[^"]*"[^>]*>.*?</nav>', sidebar_repl, text, flags=re.S)
    if changed:
        path.write_text(text)
    return changed


def main() -> None:
    pages = 0; links = 0
    for path in DOCS.rglob("*.html"):
        count = fix_page(path)
        pages += count > 0; links += count
    print(f"Normalized {links} sidebar links across {pages} pages")


if __name__ == "__main__":
    main()
