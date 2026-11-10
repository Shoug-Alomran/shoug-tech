#!/usr/bin/env python3
"""Basic study plans for courses without a full exam analysis.

The study planner needs each course's chapters and how long they take. Courses
with a hand-written analysis get that from scripts/build_exam_analysis.py; this
gives every other course with slides a plan from what's on the site: chapters,
slide counts and study pages. It has no topic-level detail.

ETHCS 303 is left out on purpose: it's a paid course, and these files are public.

    python3 scripts/build_baseline_analyses.py
Then run scripts/build_study_sources.py. Needs pdfinfo (poppler).
"""
import datetime
import glob
import html
import json
import os
import re
import subprocess
import sys

sys.path.insert(0, os.path.dirname(__file__))
from build_exam_analysis import KIND_LABELS, MINUTES_PER_SLIDE, OUT, SRC, write_index

DOCS = os.path.join(os.path.dirname(__file__), "..", "docs")
SKIP = {"ethcs303"}
NOISE = {"chapter", "ch", "lecture", "halliday", "handout", "slides", "part", "the", "and", "of", "to", "in", "a", "an"}


def rel(path):
    return "/" + os.path.relpath(path, DOCS).replace(os.sep, "/")


def natural(text):
    return [int(p) if p.isdigit() else p for p in re.split(r"(\d+)", text)]


def h1(path):
    with open(path, encoding="utf-8", errors="ignore") as f:
        text = f.read(250000)
    m = re.search(r"<h1[^>]*>(.*?)</h1>", text, re.S) or re.search(r"<title>(.*?)</title>", text, re.S)
    return html.unescape(re.sub(r"<[^>]+>|\s+", " ", m.group(1))).strip() if m else ""


def deck_number(name):
    m = re.search(r"(?:^|-)(chapter|ch|lecture)-?(\d+)", name)
    if m:
        return ("Lecture" if m.group(1) == "lecture" else "Ch"), int(m.group(2))
    m = re.match(r"(\d+)(?:-|$)", name)
    return ("Ch", int(m.group(1))) if m else ("", None)


def words(name, code):
    parts = [w for w in name.lower().split("-") if not w.isdigit() and w not in NOISE and w != code and not re.fullmatch(r"ch\d+", w)]
    return set(parts)


def deck_title(name, code):
    cleaned = re.sub(r"^%s-" % code, "", name)
    cleaned = re.sub(r"^(\d+-)?(chapter|ch|lecture)-?\d+-?", "", cleaned)
    cleaned = re.sub(r"^\d+-(?=[a-z])", "", cleaned)  # chapter-2-1-pandas: drop the part number
    cleaned = re.sub(r"-(halliday|handout)$", "", cleaned)
    cleaned = re.sub(r"^[\d-]+$", "", cleaned)
    cleaned = re.sub(r"^lecture-\d+$", "", cleaned)
    return cleaned.replace("-", " ").strip().capitalize()


def pages_of(pdf):
    out = subprocess.run(["pdfinfo", pdf], capture_output=True, text=True).stdout
    m = re.search(r"Pages:\s+(\d+)", out)
    return int(m.group(1)) if m else 0


def pages_in(folder, code):
    found = []
    for path in sorted(glob.glob(os.path.join(folder, "*", "index.html"))):
        name = path.split(os.sep)[-2]
        title = h1(path)
        m = re.search(r"(?:Chapter|Lecture)\s+(\d+)", title, re.I)
        found.append({"name": name, "words": words(re.sub(r"^\d+-", "", name), code), "number": int(m.group(1)) if m else None, "title": title, "url": rel(os.path.dirname(path)) + "/"})
    return found


def match(deck, pages, position, total):
    """A deck's page: same topic words, then same number, then same position."""
    best, score = None, 0
    for p in pages:
        union = deck["words"] | p["words"]
        s = len(deck["words"] & p["words"]) / len(union) if union else 0
        if s > score:
            best, score = p, s
    if best and score >= 0.5:
        return best
    if deck["number"] is not None:
        for p in pages:
            if p["number"] == deck["number"]:
                return p
    return pages[position] if len(pages) == total else None


def build(page):
    base = os.path.dirname(page)
    code = base.split(os.sep)[-1]
    if code in SKIP or os.path.exists(os.path.join(SRC, code + "-final.json")):
        return None
    m = re.fullmatch(r"([a-z]+)(\d+)", code)
    if not m:
        return None
    label = m.group(1).upper() + " " + m.group(2)
    slides = os.path.join(base, "slides")
    decks = []
    for path in glob.glob(os.path.join(slides, "*", "index.html")):
        folder = os.path.dirname(path)
        if folder.endswith("-partial-notes"):  # earlier copy of a deck already counted
            continue
        pdfs = sorted(glob.glob(os.path.join(folder, "*.pdf")))
        if pdfs:
            decks.append({"name": os.path.basename(folder), "pdf": pdfs[0], "url": rel(folder) + "/"})
    if not decks:
        for pdf in glob.glob(os.path.join(slides, "*.pdf")):
            decks.append({"name": os.path.basename(pdf)[:-4], "pdf": pdf, "url": rel(pdf)})
    if not decks:
        return None
    for d in decks:
        d["kind"], d["number"] = deck_number(d["name"])
        d["words"] = words(d["name"], code)
    decks.sort(key=lambda d: (d["number"] is None, d["number"] or 0, natural(d["name"])))
    annotated = pages_in(os.path.join(base, "annotated-slides"), code)
    breakdowns = pages_in(os.path.join(base, "slide-breakdowns"), code)
    if any(d["number"] is None for d in decks) and annotated:
        order = {}
        for n, p in enumerate(annotated):
            order[p["name"]] = n
        for n, d in enumerate(decks):
            a = match(d, annotated, n, len(decks))
            d["order"] = order[a["name"]] if a else 999
        decks.sort(key=lambda d: d["order"])
    chapters, by_key, topic = [], {}, 0
    for n, d in enumerate(decks):
        a = match(d, annotated, n, len(decks)) if annotated else None
        b = match(d, breakdowns, n, len(decks)) if breakdowns else None
        key = (d["kind"], d["number"]) if d["number"] is not None else ("", n)
        ch = by_key.get(key)
        if ch is None:
            title = deck_title(d["name"], code)
            if not title and a:
                title = re.sub(r"^(Chapter|Lecture)\s+\d+\s*[:—–.-]*\s*", "", a["title"]).strip()
            if d["number"] is not None:
                prefix = "%s %d" % (d["kind"], d["number"])
            else:
                topic += 1
                prefix = "Topic %d" % topic
            ch = {"id": re.sub(r"[^a-z0-9]+", "-", prefix.lower()) if d["number"] is not None else "t%d-%s" % (topic, d["name"]), "title": prefix + (" · " + title if title else ""), "slides": 0, "decks": 0, "items": 0, "kinds": {k: 0 for k in KIND_LABELS}, "links": []}
            by_key[key] = ch
            chapters.append(ch)
        ch["slides"] += pages_of(d["pdf"])
        ch["decks"] += 1
        ch["links"].append({"label": "Slides", "url": d["url"]})
        for extra, name in ((a, "Annotated slides"), (b, "Breakdown")):
            if extra and not any(l["url"] == extra["url"] for l in ch["links"]):
                ch["links"].append({"label": name, "url": extra["url"]})
    # One or two decks would look like a whole course and plan far too little.
    if len(chapters) < 3:
        return None
    total = sum(c["slides"] for c in chapters) or 1
    for c in chapters:
        c["minutes"] = max(20, round(c["slides"] * MINUTES_PER_SLIDE / 5) * 5)
        c["syllabus_share"] = round(c["slides"] / total, 3)
    resources = []
    if glob.glob(os.path.join(base, "exams", "*", "index.html")) and os.path.exists(os.path.join(base, "exams", "index.html")):
        resources.append({"label": "Past exams", "url": rel(os.path.join(base, "exams")) + "/"})
    for name, tag in (("worksheets", "Worksheets"), ("tutorials", "Tutorials"), ("labs", "Labs")):
        folder = os.path.join(base, "extra-resources", name)
        if os.path.exists(os.path.join(folder, "index.html")):
            resources.append({"label": tag, "url": rel(folder) + "/"})
    return code + "-final.json", {
        "course": label, "season": "final", "title": label, "course_page": rel(base) + "/",
        "generated": datetime.date.today().isoformat(), "curated": False, "baseline": True,
        "syllabus": {}, "style": {}, "resources": resources, "kind_labels": KIND_LABELS,
        "totals": {"chapters": len(chapters), "decks": len(decks), "slides": sum(c["slides"] for c in chapters), "minutes": sum(c["minutes"] for c in chapters), "items": 0, "to_memorize": 0, "kinds": {k: 0 for k in KIND_LABELS}, "practice_questions_sources": 0, "practice_questions": 0},
        "repeated": [], "exam_scopes": [], "chapters": chapters, "items": [],
    }


def main():
    for page in sorted(glob.glob(os.path.join(DOCS, "academics", "*", "*", "index.html"))):
        got = build(page)
        if not got:
            continue
        name, data = got
        with open(os.path.join(OUT, name), "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=1)
            f.write("\n")
        ann = sum(any(l["label"].startswith("Annotated") for l in c["links"]) for c in data["chapters"])
        brk = sum(any(l["label"] == "Breakdown" for l in c["links"]) for c in data["chapters"])
        print("%-9s %2d chapters %4d slides %4d min | annotated %2d breakdown %2d | %s" % (data["course"], len(data["chapters"]), data["totals"]["slides"], data["totals"]["minutes"], ann, brk, [c["title"][:26] for c in data["chapters"][:2]]))
    write_index()


if __name__ == "__main__":
    main()
