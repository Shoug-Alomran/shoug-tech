#!/usr/bin/env python3
"""Write docs/llms.txt, a short map of the site for AI assistants.

AI tools look for /llms.txt when asked about a site; the sitemap is too long for
them to read in one go. Built from the course manifest at deploy:

    python3 scripts/build_llms_txt.py
"""
from __future__ import annotations

import html
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"
OUT = DOCS / "llms.txt"
ORIGIN = "https://shoug-tech.com"
ACADEMICS = DOCS / "academics"
# Only the paid course's public landing page is listed.
PAID = "ethcs303"
SUMMARY = (
    "Portfolio and study site of Shoug Fawaz Alomran, a Software Engineering and Cybersecurity "
    "student at Prince Sultan University (PSU) in Riyadh. It holds projects, workshops and "
    "organized study material for PSU courses: slides, slide breakdowns, mind maps, cheat sheets "
    "and practice exams."
)
PAGES = [
    ("/", "Home", "overview, featured projects and links to every section"),
    ("/about/", "About", "profile, roles and experience"),
    ("/work/projects/", "Projects", "archive of course and personal projects with descriptions and links"),
    ("/workshops/", "Workshops", "workshops delivered, with agendas and materials"),
    ("/resources/", "Resources", "curated tools, references and links"),
    ("/academics/", "Academics", "all courses by track"),
    ("/academics/study-pack/", "Study Pack", "printable revision checklist for any course"),
]
ORDER = ["slides", "annotated-slides", "slide-breakdowns", "slides-with-notes", "extra-resources", "exams", "quizzes"]


def title(page: Path) -> str:
    text = page.read_text(encoding="utf-8", errors="ignore")
    match = re.search(r"<title[^>]*>(.*?)</title>", text, re.S | re.I)
    return re.sub(r"\s+", " ", html.unescape(match.group(1))).strip() if match else page.parent.name.upper()


def is_redirect(page: Path) -> bool:
    return bool(re.search(r'http-equiv=["\']refresh', page.read_text(encoding="utf-8", errors="ignore")[:20000], re.I))


def label(slug: str) -> str:
    return slug.replace("-", " ").title()


def main() -> int:
    lines = [
        "# SHOUG.TECH", "", f"> {SUMMARY}", "",
        "Every page is static HTML; no sign-in or JavaScript is needed to read it (except the paid "
        "ETHCS303 course). Slide pages include a \"Text version\" section with the text of each slide. "
        f"Extracted text for academic pages is also available as JSON at {ORIGIN}/ai-context/<page path>/context.json, "
        f"for example {ORIGIN}/ai-context/academics/computer-science/cs101/slides/chapter-1/context.json.",
        "", "## Main pages", "",
    ]
    lines += [f"- [{name}]({ORIGIN}{route}): {desc}" for route, name, desc in PAGES if (DOCS / route.strip("/") / "index.html").is_file()]
    total = 0
    for track in sorted(p for p in ACADEMICS.iterdir() if (p / "index.html").is_file()):
        rows = []
        for course in sorted(p for p in track.iterdir() if (p / "index.html").is_file() and not is_redirect(p / "index.html")):
            url = f"{ORIGIN}/academics/{track.name}/{course.name}/"
            line = f"- [{title(course / 'index.html')}]({url})"
            if PAID not in course.name:
                sections = [
                    s for s in sorted(course.iterdir(), key=lambda p: (ORDER.index(p.name) if p.name in ORDER else 99, p.name))
                    if (s / "index.html").is_file() and not is_redirect(s / "index.html")
                ]
                parts = []
                for s in sections:
                    count = sum(1 for c in s.iterdir() if (c / "index.html").is_file())
                    parts.append(f"[{label(s.name)}]({url}{s.name}/)" + (f" ({count})" if count else ""))
                if parts:
                    line += ": " + ", ".join(parts)
            rows.append(line)
        if rows:
            total += len(rows)
            heading = label(track.name)
            lines += ["", f"## {heading if heading.endswith('Courses') else heading + ' courses'}", "", *rows]
    lines += ["", "## Optional", "", f"- [Full sitemap]({ORIGIN}/sitemap.xml): every page URL (large)."]
    OUT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Wrote {OUT.relative_to(ROOT)}: {total} courses, {OUT.stat().st_size // 1024} KB")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
