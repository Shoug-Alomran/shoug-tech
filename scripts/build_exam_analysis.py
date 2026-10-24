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
import html
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
    # Image-only decks have (almost) no text layer; use their OCR cache from
    # scripts/exam_analysis/ocr_deck.sh instead.
    cache = SRC / "ocr" / (Path(path).stem + ".txt")
    if cache.exists() and sum(len(p.strip()) for p in pages) < 30 * max(1, len(pages)):
        pages = cache.read_text().split("\f")
        if pages and not pages[-1].strip():
            pages.pop()
    pages = [re.sub(r"\s+", " ", p) for p in pages]
    # Title-slide and footer boilerplate repeats on every deck and would count
    # as a mention of whatever it names.
    for pat in strip:
        pages = [re.sub(pat, " ", p, flags=re.I) for p in pages]
    return pages


STRING_RE = re.compile(r'"((?:[^"\\\n]|\\.){3,})"|\'((?:[^\'\\\n]|\\.){3,})\'|`([^`]{3,})`')
QUESTION_KEY_RE = re.compile(
    r"\{\s*(?=[\"']?(?:id|q|question|text|prompt|stem|title|topic|type)[\"']?\s*:)"
)


def html_segments(path):
    """One text segment per question of an HTML practice exam.

    Questions live either in JS data arrays (objects with q/question/prompt
    keys) or in the page as "Question N" blocks; whichever gives more
    segments wins."""
    s = (ROOT / path).read_text(encoding="utf-8", errors="ignore")
    # A question bank (.js) is all script.
    scripts = s if str(path).endswith(".js") else " ".join(re.findall(r"<script[^>]*>(.*?)</script>", s, re.S))
    if str(path).endswith(".js"):
        s = ""
    js = []
    for chunk in QUESTION_KEY_RE.split(scripts)[1:]:
        parts = [a or b or c for a, b, c in STRING_RE.findall(chunk)]
        text = " ".join(parts)
        text = re.sub(r"\\u([0-9a-fA-F]{4})", lambda m: chr(int(m.group(1), 16)), text)
        text = re.sub(r"<[^>]+>", " ", text)
        text = re.sub(r"\s+", " ", html.unescape(text)).strip()
        # Diagram-drawing data (node coordinates) isn't a question.
        if len(text) > 40 and not re.search(r"\bx: \d+, y: \d+", chunk):
            js.append(text)
    body = re.sub(r"<script.*?</script>|<style.*?</style>", " ", s, flags=re.S)
    text = re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", body)))
    page = [x for x in re.split(r"(?i)\bQUESTION\s+\d+\b", text)[1:] if len(x) > 40]
    # Question elements (class "q" or "question") in printed-paper replicas.
    blocks = []
    for b in re.split(r'<(?:div|section|article|li)\b[^>]*class="(?:q|question)(?:\s[^"]*)?"', body)[1:]:
        t = re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", b))).strip()
        if len(t) > 40:
            blocks.append(t[:4000])
    return max([js, page, blocks], key=len)


def practice_segments(path):
    return html_segments(path) if str(path).endswith((".html", ".js")) else pdf_pages(path)


def exam_type(label):
    l = label.lower()
    if "final" in l:
        return "final"
    if "quiz" in l:
        return "quiz"
    if "midterm" in l or "major" in l:
        return "midterm"
    return ""


def exam_scopes(cfg, chapters):
    """Which chapters each exam covers, read from the course overview page's
    "page count by exam" cards (each topic links to its slide folder).

    Returns [{label, type, chapters}] in page order; a "Comprehensive" final
    covers every chapter."""
    page = ROOT / "docs" / cfg.get("course_page", "").strip("/") / "index.html"
    if not cfg.get("course_page") or not page.exists():
        return []
    s = page.read_text(encoding="utf-8", errors="ignore")
    by_url = {}
    for c in chapters:
        for l in c.get("links", []):
            if "/slides/" in l["url"]:
                by_url[l["url"].rstrip("/")] = c["id"]
    all_ids = [c["id"] for c in chapters]
    out = []
    groups = re.split(r'<div class="exam-count-group"', s)[1:]
    for g in groups:
        g = g.split('<div class="exam-count-group"')[0]
        head = re.search(r'class="exam-count-heading">\s*<span[^>]*>(.*?)</span', g, re.S)
        if not head:
            continue
        label = re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", "", head.group(1)))).strip()
        kind = exam_type(label)
        if not kind:
            continue
        ids = []
        for href, text in re.findall(r'<a\s+class="topic-name[^"]*"\s+href="([^"]+)"[^>]*>(.*?)</a\s*>', g, re.S):
            text = re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", "", text)))
            if text.strip().endswith("otal"):
                continue
            # Some cards link the PDF itself rather than its folder.
            href = re.sub(r"/[^/]+\.pdf$", "", href)
            urls = [href.rstrip("/")]
            # "Parts 1 & 2" links only to part 1.
            if re.search(r"(?i)parts?\s*1\s*(?:&|and|,)\s*2", text):
                urls.append(urls[0].replace("part-1", "part-2"))
            for u in urls:
                cid = by_url.get(u)
                if cid and cid not in ids:
                    ids.append(cid)
        if "comprehensive" in label.lower() or (kind == "final" and not ids):
            ids = all_ids
        if ids:
            out.append({"label": label, "type": kind, "chapters": [i for i in all_ids if i in ids]})
    return out


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
        segs = practice_segments(p["path"])
        p["questions"] = len(segs)
        practice.extend(segs)

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
            "practice_questions": len(practice),
        },
        "repeated": [i["id"] for i in repeated],
        "exam_scopes": exam_scopes(cfg, chapters),
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
