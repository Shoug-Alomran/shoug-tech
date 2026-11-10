#!/usr/bin/env python3
"""Choose the best page to study from for each chapter of each final.

Writes docs/account/calendar/exam-analysis/study-sources.json, which the study
plan reads when a session is opened. It looks at what the site really has for
a chapter and measures how repetitive the slides are:

  New material  Annotated slides, unless many slides repeat earlier ones and a
                slide breakdown exists. Then the breakdown is the faster read.
  Review        Mind map, then breakdown, notes, annotated slides.
  Practice      The chapter's quiz or practice sheet, then past exams.

Chapters are matched by the numbers in page titles, never file names: several
CYS 401 deck slugs name the wrong chapter.

Run after adding slides, annotated slides, breakdowns, mind maps or quizzes:
    python3 scripts/build_study_sources.py
Needs pdftotext and pdftoppm (poppler) and Pillow.
"""
import glob
import html
import json
import os
import re
import subprocess
import tempfile

from PIL import Image, ImageChops, ImageStat

ROOT = os.path.join(os.path.dirname(__file__), "..", "docs")
ANALYSIS = os.path.join(ROOT, "account", "calendar", "exam-analysis")
# At or above this share of repeated slides, the breakdown is the better read.
REPEAT_LIMIT = 0.2
STOP = set("the a an and of for to in on with is are this that quiz".split())
# CS 331's mind maps have no chapter numbers in their titles.
CS331_MAPS = {
    "ch1": ["02-data-communications-and-networking-mind-map", "10-protocol-layering-and-network-models-mind-map"],
    "ch3a": ["03-data-link-layer-control-mind-map"],
    "ch3b": ["04-data-link-layer-mac-protocols-mind-map"],
    "ch4": ["06-ethernet-and-lans-mind-map"],
    "ch6": ["07-interconnecting-devices-and-vlans-mind-map"],
    "ch7": ["08-network-layer-data-transfer-mind-map"],
    "ch8": ["09-network-layer-routing-mind-map"],
    "ch9": ["11-transport-layer-mind-map"],
    "ch10": ["05-dns-and-application-layer-mind-map"],
}


def tokens(text):
    return {w for w in re.findall(r"[a-z؀-ۿ0-9]{3,}", text.lower()) if w not in STOP}


def page_title(path):
    with open(path, encoding="utf-8", errors="ignore") as f:
        text = f.read(250000)
    m = re.search(r"<h1[^>]*>(.*?)</h1>", text, re.S) or re.search(r"<title>(.*?)</title>", text, re.S)
    return html.unescape(re.sub(r"<[^>]+>|\s+", " ", m.group(1))).strip() if m else ""


def url_of(path):
    rel = os.path.relpath(os.path.dirname(path), ROOT).replace(os.sep, "/")
    return "/" + rel + "/"


def exists(url):
    target = os.path.join(ROOT, url.strip("/"))
    return os.path.isfile(target if url.endswith(".pdf") else os.path.join(target, "index.html"))


def text_repeats(pdf):
    """(pages, repeated pages, pages with almost no text)."""
    out = subprocess.run(["pdftotext", "-layout", pdf, "-"], capture_output=True, text=True).stdout
    pages = out.split("\f")
    if pages and not pages[-1].strip():
        pages = pages[:-1]
    seen, dup, sparse = [], 0, 0
    for page in pages:
        words = tokens(page)
        if len(words) < 8:
            sparse += 1
        if len(words) >= 4 and any(len(words & s) / len(words) >= 0.8 for s in seen):
            dup += 1
        if words:
            seen.append(words)
    return len(pages), dup, sparse


def image_repeats(pdf):
    """For decks that are pictures of slides: near-identical nearby pages."""
    with tempfile.TemporaryDirectory() as tmp:
        subprocess.run(["pdftoppm", "-r", "12", "-gray", pdf, os.path.join(tmp, "p")], capture_output=True)
        images = [Image.open(p).convert("L") for p in sorted(glob.glob(os.path.join(tmp, "p*")))]
        dup = 0
        for n, img in enumerate(images):
            for old in images[max(0, n - 6):n]:
                if old.size == img.size and ImageStat.Stat(ImageChops.difference(old, img)).mean[0] <= 3:
                    dup += 1
                    break
        return len(images), dup


def deck_repeats(url):
    folder = os.path.join(ROOT, url.strip("/"))
    pdfs = [folder] if url.endswith(".pdf") else sorted(glob.glob(os.path.join(folder, "*.pdf")))
    if not pdfs:
        return None
    pages, dup, sparse = text_repeats(pdfs[0])
    if pages and sparse / pages >= 0.5:
        pages, dup = image_repeats(pdfs[0])
    return pages, dup


def chapter_number(ch):
    m = re.match(r"(?:Ch|Lecture)\s+(\d+(?:\.\d+)?)", ch["title"])
    return str(float(m.group(1))) if m else ""


def title_number(title):
    if re.search(r"\bold chapter\b", title, re.I):
        return ""
    m = re.search(r"Chapter\s+(\d+(?:\.\d+)?)", title, re.I)
    return str(float(m.group(1))) if m else ""


def chapters_for(number, title, by_number):
    """A page's chapters: exact number, else the whole number (6.1 is Ch 6)."""
    if not number:
        return []
    found = by_number.get(number) or by_number.get(str(float(int(float(number))))) or []
    if len(found) > 1:
        part = re.search(r"Part\s+(\d+)", title)
        if part and int(part.group(1)) <= len(found):
            return [found[int(part.group(1)) - 1]]
    return found


def part_of(title):
    m = re.search(r"(Part \d+|Lecture \d+|Structural|Behavioral)", title)
    return m.group(1) if m else ""


def link(label, url):
    if not exists(url):
        raise SystemExit("Missing page: " + url)
    return {"label": label, "url": url}


def build_course(slug, base):
    a = json.load(open(os.path.join(ANALYSIS, slug + "-final.json"), encoding="utf-8"))
    home = os.path.join(ROOT, "academics", base)
    by_number = {}
    for ch in a["chapters"]:
        n = chapter_number(ch)
        if n:
            by_number.setdefault(n, []).append(ch)
    found = {ch["id"]: {"annotated": [], "breakdown": [], "notes": [], "slides": [], "map": [], "quiz": [], "sheet": []} for ch in a["chapters"]}
    repeats = {ch["id"]: [0, 0, True] for ch in a["chapters"]}

    for ch in a["chapters"]:
        got = found[ch["id"]]
        for l in ch.get("links", []):
            label, url = l["label"], l["url"]
            if not exists(url):
                continue
            low = label.lower()
            if low.startswith("breakdown"):
                tail = re.split(r"[:·]", label, maxsplit=1)
                extra = tail[1].strip() if len(tail) > 1 else ""
                generic = not extra or re.match(r"(slides|ch\b)", extra, re.I)
                if not any(x["url"] == url for x in got["breakdown"]):
                    got["breakdown"].append(link("Slide breakdown" + ("" if generic else " · " + extra), url))
            elif low.startswith("annotated"):
                got["annotated"].append(link("Annotated slides", url))
            elif low.startswith("lesson notes"):
                got["notes"].append(link("Lesson notes", url))
            elif "practice" in low:
                got["sheet"].append(link(label, url))
            elif low.startswith(("slides", "lecture pdf")):
                got["slides"].append(link("Slides" if low.startswith("slides") else "Lecture PDF", url))
                r = deck_repeats(url)
                if r:
                    repeats[ch["id"]][0] += r[0]
                    repeats[ch["id"]][1] += r[1]

    baseline = a.get("baseline")
    for path in [] if baseline else sorted(glob.glob(os.path.join(home, "annotated-slides", "*", "index.html"))):
        title = page_title(path)
        for ch in chapters_for(title_number(title), title, by_number):
            part = part_of(title)
            found[ch["id"]]["annotated"].append(link("Annotated slides" + (" · " + part if part else ""), url_of(path)))

    # Breakdowns the chapter's own links miss, by the chapter in the folder name.
    for path in [] if baseline else sorted(glob.glob(os.path.join(home, "slide-breakdowns", "*", "index.html"))):
        m = re.match(r"\d+-chapter-(\d+)-", path.split(os.sep)[-2])
        if m:
            for ch in by_number.get(str(float(m.group(1))), []):
                if not found[ch["id"]]["breakdown"]:
                    found[ch["id"]]["breakdown"].append(link("Slide breakdown", url_of(path)))

    if slug == "cs331":
        maps = os.path.join(home, "extra-resources", "mindmap")
        for cid, names in CS331_MAPS.items():
            for name in names:
                found[cid]["map"].append(link("Mind map", url_of(os.path.join(maps, name, "index.html"))))
    else:
        for path in sorted(glob.glob(os.path.join(home, "extra-resources", "mindmaps", "*", "index.html"))):
            folder, title = path.split(os.sep)[-2], page_title(path)
            number = title_number(title)
            if not number and slug in ("cys401", "se322"):
                number = str(float(int(folder.split("-")[0])))
            targets = chapters_for(number, title, by_number)
            if slug == "se423" and "Tailoring" in title and "Performance" in title:
                targets = by_number.get("1.0", []) + by_number.get("1.2", []) + by_number.get("1.3", [])
            for ch in targets:
                part = part_of(title)
                found[ch["id"]]["map"].append(link("Mind map" + (" · " + part if part else ""), url_of(path)))

    finals = []
    for path in sorted(glob.glob(os.path.join(home, "exams", "*", "index.html"))):
        folder = path.split(os.sep)[-2]
        low = folder.lower()
        if "quiz" in low and not re.search(r"final|midterm|major", low):
            m = re.search(r"chapter-(\d+)-quiz", low)
            if m:
                targets = by_number.get(str(float(m.group(1))), [])
            else:
                words = tokens(re.sub(r"^\d+-", "", folder).replace("-", " "))
                best = max(a["chapters"], key=lambda c: len(words & tokens(c["title"])))
                targets = [best] if words & tokens(best["title"]) else []
            for ch in targets:
                found[ch["id"]]["quiz"].append(link("Chapter quiz", url_of(path)))
        elif re.search(r"final|midterm|major|paper", low):
            finals.append(link(page_title(path) or folder, url_of(path)))

    past, sheets = [], []
    for r in a.get("resources", []):
        if not exists(r["url"]):
            continue
        low = r["label"].lower()
        if re.search(r"past|final|midterm|paper|quiz|exam|tutorial|worksheet|lab", low):
            past.append(link(r["label"], r["url"]))
        else:
            sheets.append(link(r["label"], r["url"]))
    seen = {x["url"] for x in past}
    past += [x for x in finals if x["url"] not in seen and len(past) < 5]

    # Pages made for learning things by heart.
    memorize = []
    for path in sorted(glob.glob(os.path.join(home, "extra-resources", "*", "index.html"))):
        if re.search(r"cheat|formula|listing|vault|summary|table", path.split(os.sep)[-2], re.I):
            memorize.append(link(page_title(path) or path.split(os.sep)[-2].replace("-", " "), url_of(path)))
    memorize = memorize[:4]

    out = {"chapters": {}, "final": past[:5], "sheets": sheets, "page": a.get("course_page", "")}
    for ch in a["chapters"]:
        got, (pages, dup, _) = found[ch["id"]], repeats[ch["id"]]
        share = dup / pages if pages else None
        if got["notes"] and not got["annotated"]:
            learn, why = got["notes"], "These lesson notes cover the whole lecture in one place."
        elif share is not None and share >= REPEAT_LIMIT and got["breakdown"]:
            learn, why = got["breakdown"], "%d of %d slides repeat earlier ones, so the breakdown is the faster read." % (dup, pages)
        elif got["annotated"] and share is not None and share >= REPEAT_LIMIT:
            learn, why = got["annotated"], "%d of %d slides repeat earlier ones. There's no breakdown for this chapter, so skim the repeats." % (dup, pages)
        elif got["annotated"] and share is not None:
            learn, why = got["annotated"], "Only %d of %d slides repeat, so the annotated slides explain each one without wasting your time." % (dup, pages)
        elif got["annotated"]:
            learn, why = got["annotated"], "The annotated slides explain every slide."
        elif got["breakdown"]:
            learn, why = got["breakdown"], "The breakdown is the clearest page the site has for this chapter."
        else:
            learn, why = got["slides"], "The slides are the only page for this chapter so far."
        if got["map"]:
            review, rwhy = got["map"], "A mind map shows how the ideas connect, so gaps stand out quickly."
        elif got["breakdown"]:
            review, rwhy = got["breakdown"], "The breakdown is the quickest way back over the key points."
        elif got["notes"]:
            review, rwhy = got["notes"], "Go back over the lesson notes from memory first."
        else:
            review, rwhy = got["annotated"] or got["slides"], "Go back over the slides from memory first."
        practice = got["quiz"] + got["sheet"]
        everything = []
        for key in ("annotated", "breakdown", "notes", "map", "quiz", "sheet", "slides"):
            everything += got[key]
        out["chapters"][ch["id"]] = {
            "repeat": [dup, pages] if pages else None,
            "learn": {"why": why if learn else "", "links": learn},
            "review": {"why": rwhy if review else "", "links": review},
            "practice": {"why": "Test yourself with this first, then check what you missed." if practice else "", "links": practice},
            "memorize": {"why": "Cover the answers and recite them from memory, then check. Repeat only what you missed." if (memorize or review) else "", "links": memorize or review},
            "all": everything,
        }
    return a["course"], out


def main():
    data = {}
    for path in sorted(glob.glob(os.path.join(ANALYSIS, "*-final.json"))):
        slug = os.path.basename(path)[: -len("-final.json")]
        page = json.load(open(path, encoding="utf-8")).get("course_page", "")
        base = page.replace("/academics/", "", 1).strip("/")
        course, out = build_course(slug, base)
        data[course] = out
        print("==", course, "| past", len(out["final"]), "| sheets", len(out["sheets"]))
        for cid, c in out["chapters"].items():
            r = c["repeat"]
            print("  %-22s rep %-8s learn: %-34s review: %-22s practice: %s" % (
                cid[:22], "%d/%d" % tuple(r) if r else "-", (c["learn"]["links"][0]["label"] if c["learn"]["links"] else "NONE")[:34],
                (c["review"]["links"][0]["label"] if c["review"]["links"] else "NONE")[:22], len(c["practice"]["links"])))
    path = os.path.join(ANALYSIS, "study-sources.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=1)
        f.write("\n")
    print("wrote", os.path.relpath(path))


if __name__ == "__main__":
    main()
