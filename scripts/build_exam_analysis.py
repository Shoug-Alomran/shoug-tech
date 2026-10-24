#!/usr/bin/env python3
"""Build the exam analysis files the calendar's Study Plan tab reads.

    python3 scripts/build_exam_analysis.py scripts/exam_analysis/cs331-final.json
    python3 scripts/build_exam_analysis.py --all

Input is a hand-checked inventory (scripts/exam_analysis/<course>-<season>.json):
chapters with their slide decks, and items (concepts, formulas, numbers, lists,
processes, comparisons and calculation types) with regexes that find them on a
slide. The script reads every deck page by page with pdftotext, counts how many
slides and decks mention each item and how often the practice sources do, then
ranks the items and estimates study time.

An inventory with no items is a baseline: it still gets slide counts, study
time and syllabus weights, and the tab says the concept breakdown is pending.

Output: docs/account/calendar/exam-analysis/<course>-<season>.json plus
index.json listing every built file.
"""
import json
import math
import re
import subprocess
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "scripts" / "exam_analysis"
OUT = ROOT / "docs" / "account" / "calendar" / "exam-analysis"

# Minutes to learn one item well enough for an exam, by kind. Calculation
# types include working practice problems.
KIND_MINUTES = {
    "calc": 30,
    "process": 12,
    "list": 10,
    "compare": 10,
    "formula": 8,
    "concept": 8,
    "number": 6,
}
KIND_LABELS = {
    "concept": "Concepts",
    "compare": "Comparisons",
    "list": "Lists to memorize",
    "process": "Processes and steps",
    "formula": "Formulas",
    "number": "Key numbers",
    "calc": "Problem types",
}
# Reading a slide closely enough to answer questions on it.
MINUTES_PER_SLIDE = 1.2


def pdf_pages(path, strip=()):
    out = subprocess.run(
        ["pdftotext", "-q", str(ROOT / path), "-"],
        capture_output=True,
        text=True,
        check=False,
    ).stdout
    pages = out.split("\f")
    if pages and not pages[-1].strip():
        pages.pop()
    pages = [re.sub(r"\s+", " ", p) for p in pages]
    # Title-slide and footer boilerplate repeats on every deck and would count
    # as a mention of whatever it names.
    for pat in strip:
        pages = [re.sub(pat, " ", p, flags=re.I) for p in pages]
    return pages


def compile_patterns(item):
    return [re.compile(p, re.I) for p in item.get("match", [])]


def count_hits(patterns, pages):
    return sum(1 for p in pages if any(r.search(p) for r in patterns))


def slug(course):
    return re.sub(r"[^a-z0-9]", "", course.lower())


def build(src_path):
    cfg = json.loads(Path(src_path).read_text())
    chapters = cfg["chapters"]
    strip = cfg.get("strip", [])
    deck_pages = {}
    for ch in chapters:
        for d in ch["decks"]:
            deck_pages[d] = pdf_pages(d, strip)
    practice = []
    for p in cfg.get("practice_sources", []):
        practice.extend(pdf_pages(p["path"]))

    total_weeks = sum(c.get("syllabus_weeks", 1) for c in chapters) or 1
    items_out = []
    for it in cfg.get("items", []):
        pats = compile_patterns(it)
        slides = 0
        decks = 0
        for d, pages in deck_pages.items():
            n = count_hits(pats, pages)
            slides += n
            if n:
                decks += 1
        if not slides:
            raise SystemExit(f"{it['id']}: no slide matches; check its patterns")
        items_out.append(
            {
                "id": it["id"],
                "kind": it["kind"],
                "chapter": it["chapter"],
                "name": it["name"],
                "memorize": it.get("memorize", ""),
                "slides": slides,
                "decks": decks,
                "practice": count_hits(pats, practice) if practice else 0,
                "minutes": KIND_MINUTES[it["kind"]],
            }
        )

    # Priority: how often the slides return to it (log-scaled, so one huge
    # topic doesn't drown the rest), whether it spans decks, whether the
    # practice sheets ask about it, how much syllabus time its chapter gets,
    # and whether it is a calculation (those carry the most marks).
    ch_weight = {
        c["id"]: c.get("syllabus_weeks", 1) / total_weeks for c in chapters
    }
    for it in items_out:
        score = (
            math.log2(1 + it["slides"]) * 2
            + (it["decks"] - 1) * 1.5
            + min(it["practice"], 4) * 1.5
            + ch_weight[it["chapter"]] * 10
            + (3 if it["kind"] == "calc" else 1 if it["kind"] == "formula" else 0)
        )
        it["score"] = round(score, 2)
    ranked = sorted(items_out, key=lambda x: -x["score"])
    n = len(ranked)
    for i, it in enumerate(ranked):
        it["tier"] = "core" if i < n * 0.3 else "high" if i < n * 0.7 else "review"
    # The most repeated items, by slide count.
    repeated = sorted(items_out, key=lambda x: (-x["slides"], -x["decks"]))[:10]

    chapters_out = []
    for c in chapters:
        pages = [p for d in c["decks"] for p in deck_pages[d]]
        mine = [i for i in items_out if i["chapter"] == c["id"]]
        item_min = sum(i["minutes"] for i in mine)
        slide_min = len(pages) * MINUTES_PER_SLIDE
        chapters_out.append(
            {
                "id": c["id"],
                "title": c["title"],
                "slides": len(pages),
                "decks": len(c["decks"]),
                "syllabus_share": round(c.get("syllabus_weeks", 1) / total_weeks, 3),
                "minutes": int(round(max(item_min, slide_min) / 5.0) * 5),
                "items": len(mine),
                "kinds": {k: sum(1 for i in mine if i["kind"] == k) for k in KIND_LABELS},
                "links": c.get("links", []),
            }
        )

    kinds = {k: sum(1 for i in items_out if i["kind"] == k) for k in KIND_LABELS}
    out = {
        "course": cfg["course"],
        "season": cfg["season"],
        "title": cfg.get("title", ""),
        "course_page": cfg.get("course_page", ""),
        "generated": date.today().isoformat(),
        "curated": bool(items_out),
        "syllabus": {k: v for k, v in cfg.get("syllabus", {}).items() if k != "path"},
        "style": cfg.get("style", {}),
        "resources": cfg.get("resources", []),
        "kind_labels": KIND_LABELS,
        "totals": {
            "chapters": len(chapters_out),
            "decks": sum(c["decks"] for c in chapters_out),
            "slides": sum(c["slides"] for c in chapters_out),
            "minutes": sum(c["minutes"] for c in chapters_out),
            "items": len(items_out),
            "to_memorize": kinds["formula"] + kinds["number"] + kinds["list"],
            "kinds": kinds,
            "practice_questions_sources": len(cfg.get("practice_sources", [])),
        },
        "repeated": [i["id"] for i in repeated],
        "chapters": chapters_out,
        "items": ranked,
    }
    OUT.mkdir(parents=True, exist_ok=True)
    name = f"{slug(cfg['course'])}-{cfg['season']}.json"
    (OUT / name).write_text(json.dumps(out, indent=1, ensure_ascii=False) + "\n")
    return name, out


def write_index():
    entries = []
    for f in sorted(OUT.glob("*.json")):
        if f.name == "index.json":
            continue
        d = json.loads(f.read_text())
        entries.append(
            {
                "course": d["course"],
                "season": d["season"],
                "file": f.name,
                "curated": d["curated"],
                "generated": d["generated"],
            }
        )
    (OUT / "index.json").write_text(json.dumps(entries, indent=1) + "\n")
    return entries


def main(argv):
    paths = sorted(SRC.glob("*.json")) if argv == ["--all"] else [Path(a) for a in argv]
    if not paths:
        raise SystemExit(__doc__)
    for p in paths:
        name, out = build(p)
        t = out["totals"]
        print(
            f"{name}: {t['chapters']} chapters, {t['slides']} slides, "
            f"{t['items']} items, {t['minutes']} min"
        )
    write_index()


if __name__ == "__main__":
    main(sys.argv[1:])
