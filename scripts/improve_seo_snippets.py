#!/usr/bin/env python3
"""Lengthen short <title>s and meta descriptions so search engines accept them.

Bing Webmaster Tools flags titles under ~30 characters and descriptions that are
short or boilerplate ("PHY105 // Physics I study material from Shoug's Digital
Garden."). Hundreds of builders emit those, and re-running a builder would undo
a one-off edit, so this runs at deploy on the final HTML instead:

  * a title shorter than 30 characters is rebuilt from the course code, course
    name and page type ("Chapter 7 Quiz | CYS401 Fundamentals of Cybersecurity");
  * a description that is missing, templated or shorter than 120 characters is
    rewritten for the page type and fitted to 120-160 characters;
  * og:/twitter: title and description follow when they mirrored the old value.

Hand-written titles of 30+ characters and descriptions of 120+ are left alone.
Redirect stubs and the sealed ETHCS303 pages are skipped.

    python3 scripts/improve_seo_snippets.py            # dry run, prints samples
    python3 scripts/improve_seo_snippets.py --apply    # write changes
"""
from __future__ import annotations

import html
import os
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DOCS = Path(os.environ.get("SEO_DOCS", ROOT / "docs")).resolve()

MIN_TITLE, MAX_TITLE = 30, 65
MIN_DESC, MAX_DESC = 120, 160
BRAND = "SHOUG.TECH"
GARDEN = "Shoug's Digital Garden"
SKIP = ("/ethcs303/",)

TITLE_RE = re.compile(r"(<title\b[^>]*>)(.*?)(</title>)", re.S | re.I)
DESC_RE = re.compile(r'(<meta\s+name=["\']description["\']\s+content=")([^"]*)(")', re.S | re.I)
META_RE = r'(<meta\s+(?:property|name)=["\']{key}["\']\s+content=")([^"]*)(")'
HEAD_END = re.compile(r"</head>|<body\b", re.I)  # some pages omit </head>
REFRESH = re.compile(r'http-equiv=["\']refresh["\']', re.I)
NOINDEX = re.compile(r'<meta\s+name=["\']robots["\'][^>]*noindex', re.I)
CODE_RE = re.compile(r"\b([A-Z]{2,5}\d{3})\b")
BOILERPLATE = ("study material from Shoug", "[ SYS_NAV ]", "ID_PROFILE", "SYSTEM_DIRECTORY",
               "WORKSHOP_DIRECTORY", "///")
# Descriptions scraped from the page's nav bar ("Contact [ WORK ] Builder. ...").
SCRAPED = re.compile(r"^Contact\b|\[ [A-Z0-9_/ .-]+ \]")


def is_boilerplate(desc: str) -> bool:
    return any(b in desc for b in BOILERPLATE) or bool(SCRAPED.search(desc))

# Course names the home page title doesn't carry cleanly.
COURSE_NAMES = {
    "sci101": "Introduction to Physical Science",
    "stat101": "Introduction to Probability Theory and Statistics",
    "english": "English Language Skills",
}

# Top-level pages: hand-written, since no pattern describes them.
PAGES = {
    "": ("Shoug Alomran | Software Engineering and Cybersecurity",
         "Shoug Alomran's digital garden: course notes, lecture slides, practice exams and projects "
         "from a Software Engineering degree at Prince Sultan University."),
    "about/": ("About Shoug Alomran | Software Engineer and Cybersecurity",
               "About Shoug Alomran, a Software Engineering student with a minor in Cybersecurity at "
               "Prince Sultan University: experience, projects and skills."),
    "work/": ("Work and Projects | Shoug Alomran, Software Engineer",
              "Shoug Alomran's work: software engineering and cybersecurity projects, research and "
              "studio work, with a summary for recruiters and links to each project."),
    "work/projects/": ("Project Archive | Software Projects by Shoug Alomran",
                       "Archive of software engineering and cybersecurity projects built by Shoug Alomran, "
                       "each documented with its goals, stack, screenshots and outcome."),
    "academics/": ("Academics | Course Notes, Slides and Exams | SHOUG.TECH",
                   "Every course in one place: lecture slides, annotated notes, practice quizzes, past "
                   "exams and cheat sheets for computing courses at Prince Sultan University."),
    "workshops/": ("Workshops and Events | SHOUG.TECH by Shoug Alomran",
                   "Workshops, bootcamps and competitions Shoug Alomran has attended or run, from CTFs to "
                   "career events, with notes, slides and takeaways from each one."),
    "resources/": ("Study Resources and Tools | SHOUG.TECH by Shoug Alomran",
                   "Curated study resources and tools for computer science, software engineering and "
                   "cybersecurity students: guides, references and links worth keeping."),
    "community/": ("Community | Study Together on SHOUG.TECH",
                   "The SHOUG.TECH community: connect with other students using the course notes, share "
                   "resources and study together for quizzes and exams."),
    "account/": ("My Progress | Study Tracker on SHOUG.TECH",
                 "Your SHOUG.TECH account: track courses, quiz results, bookmarks and study progress "
                 "across every course in Shoug's Digital Garden."),
    "career-development/cv.html": ("Shoug Alomran CV | Software Engineering and Cybersecurity",
                                   "Curriculum vitae of Shoug Alomran: Software Engineering student with a minor "
                                   "in Cybersecurity at Prince Sultan University, with experience, projects and skills."),
    "academic-plan-themes/academic-plan/": ("Academic Plan | PSU Degree Planner on SHOUG.TECH",
                                            "Plan your Prince Sultan University degree semester by semester: "
                                            "required courses, prerequisites and electives for each computing major."),
}

DEPTS = {"information-system": "Information Systems", "business": "Business", "other-courses": "General Education",
         "math": "Math and Science"}
SECTION_WORDS = {
    "slides": "lecture slides",
    "annotated-slides": "chapter notes",
    "slide-breakdowns": "chapter notes",
    "exams": "practice exams",
    "extra-resources": "cheat sheets",
}
EXAM_FOLDERS = {"chapter-quizzes": "Chapter Quizzes", "midterm-1": "Midterm 1",
                "midterm-2": "Midterm 2", "final": "Final Exam"}
GENERIC_LABELS = {"", "overview", "study material", "slides", "quizzes", "exams", "extra resources",
                  "slide breakdowns", "annotated slides", "index", "home"}


def clean(s: str) -> str:
    return html.unescape(re.sub(r"\s+", " ", s)).strip()


def humanize(slug: str) -> str:
    slug = re.sub(r"\.html?$", "", slug)
    slug = re.sub(r"^\d+[-_]", "", slug)
    words = re.split(r"[-_\s]+", slug)
    small = {"and", "or", "of", "the", "in", "to", "for", "a", "an", "on", "with", "vs"}
    out = []
    for i, w in enumerate(words):
        if not w:
            continue
        if re.fullmatch(r"[a-z]{2,5}\d{3}", w) or w in {"ai", "os", "ui", "ux", "dns", "sql", "mcq", "cia"}:
            out.append(w.upper())
        elif i and w in small:
            out.append(w)
        else:
            out.append(w[0].upper() + w[1:])
    return " ".join(out)


def strip_brand(title: str, code: str | None = None) -> str:
    t = re.sub(r"(?i)\bshoug\.tech\b", "", title)
    if code:
        t = re.sub(rf"(?i)\b{code}\b", "", t)
    t = re.sub(r"\s*(//|\||—|–|·|::)\s*", " | ", t)
    parts = [p.strip(" -|:") for p in t.split(" | ")]
    parts = [p for p in parts if p]
    return " | ".join(parts)


def fit_desc(text: str, extra: str = f" Part of {GARDEN}.") -> str:
    text = re.sub(r"\s+", " ", text).strip()
    if len(text) < MIN_DESC and len(text + extra) <= MAX_DESC:
        text += extra
    if len(text) > MAX_DESC:
        cut = text[: MAX_DESC - 1].rsplit(" ", 1)[0].rstrip(",;:—- ")
        text = cut + "…"
    return text


def join_words(items: list[str]) -> str:
    if len(items) <= 1:
        return "".join(items)
    return ", ".join(items[:-1]) + " and " + items[-1]


class Courses:
    def __init__(self) -> None:
        self.names: dict[str, str] = {}
        for home in (DOCS / "academics").glob("*/*/index.html"):
            slug = home.parent.name
            text = home.read_text(encoding="utf-8", errors="ignore")[:200000]
            name = COURSE_NAMES.get(slug, "")
            if not name:
                m = TITLE_RE.search(text)
                if m and "//" in m.group(2):
                    name = clean(m.group(2)).split("//", 1)[1]
                    name = re.sub(r"\s*[—|-]\s*SHOUG\.TECH\s*$", "", name, flags=re.I).strip()
            self.names[slug] = name

    def label(self, slug: str, full: bool = True) -> str:
        code = slug.upper() if re.fullmatch(r"[a-z]{2,5}\d{3}", slug) else humanize(slug)
        name = self.names.get(slug, "")
        return f"{code} {name}".strip() if full and name else code


def course_snippets(parts: list[str], title: str, courses: Courses, course_dir: Path):
    """parts = path segments after academics/<dept>/, starting with the course slug."""
    slug, rest = parts[0], parts[1:]
    if rest and rest[-1] == "index.html":
        rest = rest[:-1]
    code = slug.upper() if re.fullmatch(r"[a-z]{2,5}\d{3}", slug) else None
    full, short = courses.label(slug), courses.label(slug, full=False)

    own = strip_brand(title, code)
    if own.lower() == courses.names.get(slug, "").lower():
        own = ""
    own = own.split(" | ")[0] if own else ""
    own = re.sub(r"^(Breakdown|Slides?|Annotated Slides?|Quiz)\s*:\s*", "", own, flags=re.I)
    if own.lower() in GENERIC_LABELS or own.lower().startswith(("overview", "study material")):
        own = ""
    item = own or (humanize(rest[-1]) if rest else "")

    section = rest[0] if rest else ""
    if section == "slides" and len(rest) > 1 and rest[1] == "annotated-slides":
        section, rest = "annotated-slides", ["annotated-slides"] + rest[2:]
    depth = len(rest)

    def both(make, fallback=None):
        """First wording that fits: full course name, code only, then the shorter wording."""
        tries = [make(full), make(short)]
        if fallback:
            tries += [fallback(full), fallback(short)]
        for d in tries:
            if len(d) <= MAX_DESC:
                return d
        return tries[-1]

    if not rest:
        present = list(dict.fromkeys(w for k, w in SECTION_WORDS.items() if (course_dir / k).is_dir()))
        what = join_words(present) or "lecture notes and study material"
        t = f"{full}: Slides, Exams and Study Notes"
        d = both(lambda c: f"{c} at Prince Sultan University: {what} in one study hub, "
                           f"organised by chapter for exam revision.",
                 lambda c: f"{c} at Prince Sultan University: {what}, organised by chapter.")
    elif section == "slides":
        if depth == 1:
            t = f"{full} Lecture Slides"
            d = both(lambda c: f"Every {c} lecture slide deck in chapter order. Open a deck in the "
                               f"in-browser viewer or download the PDF to study offline.")
        else:
            t = f"{item} | {full} Slides"
            d = both(lambda c: f"{item} lecture slides for {c}. Read the deck in the in-browser viewer "
                               f"or download the PDF to revise the chapter before exams.",
                     lambda c: f"{item}: {c} lecture slides to read in the browser or download as a PDF.")
    elif section == "annotated-slides":
        if depth == 1:
            t = f"{full} Annotated Slides"
            d = both(lambda c: f"Annotated slides for {c}: every lecture slide explained in plain language "
                               f"with notes on what to remember for the exam.")
        else:
            t = f"{item} | {full} Annotated Slides"
            d = both(lambda c: f"{item} annotated slides for {c}, with each slide explained in plain "
                               f"language and notes on what to remember for the exam.",
                     lambda c: f"{item}: {c} annotated slides, each one explained in plain language.")
    elif section == "slide-breakdowns":
        if depth == 1:
            t = f"{full} Chapter Breakdowns"
            d = both(lambda c: f"Chapter-by-chapter breakdowns of the {c} lecture slides, with the key "
                               f"ideas of each lecture summarised for quick revision.")
        else:
            t = f"{item} | {full} Breakdown"
            d = both(lambda c: f"{item} broken down for {c}: the key ideas of the lecture summarised "
                               f"slide by slide for quick revision before quizzes and exams.",
                     lambda c: f"{item}: the key ideas of this {c} lecture, summarised for quick revision.")
    elif section == "exams":
        if depth == 1:
            t = f"{full} Practice Quizzes and Exams"
            d = both(lambda c: f"Practice quizzes and exams for {c}, sorted by chapter and exam so you "
                               f"can test yourself before every quiz, midterm and final.")
        elif depth == 2 and rest[1] in EXAM_FOLDERS:
            folder = EXAM_FOLDERS[rest[1]]
            t = f"{full} {folder} Practice"
            d = both(lambda c: f"{folder} practice for {c}: every quiz and exam covering this part of "
                               f"the course, ready to take in the browser.")
        else:
            if not own and depth > 2 and rest[1] in EXAM_FOLDERS:
                item = humanize(rest[2])
            t = f"{item} | {full}"
            d = both(lambda c: f"{item} for {c}: practice questions you can answer in the browser to "
                               f"check your understanding before the real exam.",
                     lambda c: f"{item}: {c} practice questions to answer in the browser before the exam.")
    elif section == "extra-resources":
        if depth == 1:
            t = f"{full} Extra Study Resources"
            d = both(lambda c: f"Extra study material for {c} beyond the lecture slides: cheat sheets, "
                               f"summaries and other resources for exam revision.")
        else:
            t = f"{item} | {full}"
            d = both(lambda c: f"{item} for {c}, a study resource for revising the course quickly "
                               f"alongside the lecture slides and practice exams.",
                     lambda c: f"{item}: a {c} study resource for quick revision before exams.")
    else:
        t = f"{item or humanize(section)} | {full}"
        d = both(lambda c: f"{item or humanize(section)} for {c}, part of the course study hub with "
                           f"lecture slides, practice exams and revision notes.",
                 lambda c: f"{item or humanize(section)}: part of the {c} study hub.")

    if len(t) > MAX_TITLE:
        t = t.replace(full, short)
    if len(t) < MIN_TITLE:
        t = f"{t} | {BRAND}"
    return t, fit_desc(d)


def generic_snippets(rel: str, title: str, desc: str):
    route = rel[: -len("index.html")] if rel.endswith("index.html") else rel
    if route in PAGES:
        t, d = PAGES[route]
        return t, fit_desc(d)
    parts = route.strip("/").split("/")
    # Department hubs: /academics/computer-science/ and friends.
    if len(parts) == 2 and parts[0] == "academics" and any((DOCS / "academics" / parts[1]).glob("*/index.html")):
        dept = DEPTS.get(parts[1], humanize(parts[1]))
        return (f"{dept} Courses | Slides, Exams and Notes | {BRAND}",
                fit_desc(f"{dept} courses at Prince Sultan University: lecture slides, chapter notes, "
                         f"practice exams and cheat sheets for each course on {BRAND}."))

    segs = [s for s in strip_brand(title).split(" | ") if "_" not in s]
    label = " · ".join(
        " ".join(w.capitalize() if w.isupper() and len(w) > 4 and "-" not in w else w for w in s.split())
        for s in segs) or humanize(Path(route).name or "Home")
    t = f"{label} | {BRAND}, Shoug's Digital Garden"
    if len(t) > MAX_TITLE:
        t = f"{label} | {BRAND}"
    if desc and not is_boilerplate(desc):
        base = desc if desc.endswith((".", "!", "?")) else desc + "."
        d = fit_desc(base, " From SHOUG.TECH, Shoug Alomran's digital garden of course notes, "
                           "slides and projects.")
        if len(d) >= MIN_DESC:
            return t, d
    tries = [f"{label}, on SHOUG.TECH: Shoug Alomran's digital garden of course notes, lecture slides, "
             f"practice exams and projects from Prince Sultan University.",
             f"{label}, on SHOUG.TECH: Shoug Alomran's digital garden of course notes, slides, exams "
             f"and projects."]
    return t, fit_desc(next((d for d in tries if len(d) <= MAX_DESC), tries[-1]))


def set_meta(text: str, key: str, old: str, new: str, head_end: int) -> str:
    rx = re.compile(META_RE.format(key=re.escape(key)), re.S | re.I)
    m = rx.search(text, 0, head_end)
    if not m:
        return text
    cur = clean(m.group(2))
    if cur == old or is_boilerplate(cur) or len(cur) < len(new) // 2:
        return text[: m.start(2)] + html.escape(new, quote=True) + text[m.end(2):]
    return text


def process(p: Path, courses: Courses):
    rel = p.relative_to(DOCS).as_posix()
    if any(s in "/" + rel for s in SKIP) or p.name == "404.html":
        return None
    text = p.read_text(encoding="utf-8", errors="ignore")
    he = HEAD_END.search(text)
    if not he or REFRESH.search(text, 0, he.start()) or NOINDEX.search(text, 0, he.start()):
        return None

    tm = TITLE_RE.search(text, 0, he.start())
    dm = DESC_RE.search(text, 0, he.start())
    title = clean(tm.group(2)) if tm else ""
    desc = clean(dm.group(2)) if dm else ""

    bad_title = len(title) < MIN_TITLE
    bad_desc = len(desc) < MIN_DESC or is_boilerplate(desc)
    route = rel[: -len("index.html")] if rel.endswith("index.html") else rel
    if route in PAGES:
        bad_title = bad_title or title != PAGES[route][0]
        bad_desc = True
    if not (bad_title or bad_desc) or not title:
        return None

    parts = rel.split("/")
    if parts[0] == "academics" and len(parts) >= 3 and parts[2] != "index.html":
        course_dir = DOCS / "academics" / parts[1] / parts[2]
        new_t, new_d = course_snippets(parts[2:], title, courses, course_dir)
        # Keep a good hand-written description, just extend it with context.
        if bad_desc and desc and not is_boilerplate(desc) and len(desc) >= 50:
            base = desc.rstrip(".") + "."
            for suffix in (f" From the {courses.label(parts[2])} study hub on {GARDEN}.",
                           f" From the {courses.label(parts[2], full=False)} study hub on {GARDEN}.",
                           f" Part of the {courses.label(parts[2], full=False)} study hub on {BRAND}.",
                           f" {courses.label(parts[2], full=False)} on {BRAND}."):
                ext = fit_desc(base, suffix)
                if MIN_DESC <= len(ext) and not ext.endswith("…"):
                    new_d = ext
                    break
    else:
        new_t, new_d = generic_snippets(rel, title, desc)

    if not bad_title:
        new_t = title
    if not bad_desc:
        new_d = desc

    out = text
    # Replace from the end of the head backwards so offsets stay valid.
    edits = []
    if new_d != desc:
        if dm:
            edits.append((dm.start(2), dm.end(2), html.escape(new_d, quote=True)))
        else:
            edits.append((he.start(), he.start(),
                          f'    <meta name="description" content="{html.escape(new_d, quote=True)}" />\n'))
    if new_t != title and tm:
        edits.append((tm.start(2), tm.end(2), html.escape(new_t, quote=False)))
    for s, e, v in sorted(edits, reverse=True):
        out = out[:s] + v + out[e:]

    he2 = HEAD_END.search(out).start()
    if new_t != title:
        for k in ("og:title", "twitter:title"):
            out = set_meta(out, k, title, new_t, he2)
            he2 = HEAD_END.search(out).start()
    if new_d != desc:
        for k in ("og:description", "twitter:description"):
            out = set_meta(out, k, desc, new_d, he2)
            he2 = HEAD_END.search(out).start()

    if out == text:
        return None
    return out, (rel, title, new_t, desc, new_d)


def main() -> int:
    apply = "--apply" in sys.argv
    courses = Courses()
    changes = []
    for p in sorted(DOCS.rglob("*.html")):
        r = process(p, courses)
        if not r:
            continue
        out, info = r
        changes.append(info)
        if apply:
            p.write_text(out, encoding="utf-8")

    titles = sum(1 for c in changes if c[1] != c[2])
    descs = sum(1 for c in changes if c[3] != c[4])
    print(f"{'updated' if apply else 'would update'} {len(changes)} pages: "
          f"{titles} titles, {descs} descriptions")
    if "--verbose" in sys.argv or not apply:
        for rel, ot, nt, od, nd in changes[: (None if "--verbose" in sys.argv else 15)]:
            print(f"\n{rel}")
            if ot != nt:
                print(f"  title: {ot!r}\n      -> {nt!r} ({len(nt)})")
            if od != nd:
                print(f"  desc:  {od!r}\n      -> {nd!r} ({len(nd)})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
