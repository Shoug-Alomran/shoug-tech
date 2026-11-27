#!/usr/bin/env python3
"""Install the study tools (docs/javascripts/annotated-study.js) on every course's Annotated Slides.

For every deck page it:
  - tags each pick-an-answer question with a stable id (data-qid, a hash of its text) so saved
    answers survive rebuilds and reordering;
  - marks the body with the course, deck and chapter (and, where the course has study extras,
    whether the final exam covers the deck);
  - adds calculation drills (data-drill) and "Explain it to me" boxes from the course's
    study extras, when it has them (scripts/<code>_annotated/study_extras.py, today SE423 only);
  - adds the script tag.
A course with pick-an-answer questions also gets annotated-slides/review/ (a review page, its
site wrapper, questions.json and summary.json) and the script on its Slides page for tile scores.

Safe to run again, and run it again after rebuilding a deck: it replaces what it added before.
    PYTHONUTF8=1 python3 scripts/install_annotated_study.py            # every course
    PYTHONUTF8=1 python3 scripts/install_annotated_study.py se423     # one course
"""
import html
import importlib
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
SCRIPTS = ROOT / "scripts"
sys.path.insert(0, str(SCRIPTS))

VERSION = "2"
TAG = f'<script src="/javascripts/annotated-study.js?v={VERSION}"></script>'
TAG_RE = re.compile(r'\s*<script src="/javascripts/annotated-study\.js(?:\?v=[^"]*)?"(?: [^>]*)?></script>')
DEPT_NAMES = {
    "computer-science": "Computer Science",
    "cybersecurity": "Cybersecurity",
    "math": "Math",
    "software-engineering": "Software Engineering",
    "information-system": "Information Systems",
    "business": "Business",
    "other-courses": "Other Courses",
}
WRAPPER_TEMPLATE = SCRIPTS / "annotated_review_wrapper.html"
PAGE_TEMPLATE = SCRIPTS / "annotated_review_page.html"


def text(fragment):
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", fragment))).strip()


def qid(prompt, options):
    """FNV-1a over the question and its options: the same text always gets the same id."""
    h = 0x811C9DC5
    for byte in (prompt + "|" + "|".join(options)).lower().encode("utf-8"):
        h = ((h ^ byte) * 0x01000193) & 0xFFFFFFFF
    return format(h, "08x")


ARTICLE = re.compile(r'<article class="q pick[^"]*"(?: data-qid="[0-9a-f]+")?>.*?</article>', re.S)
OPTION = re.compile(r'<li( data-c="1")?>\s*<button[^>]*class="choice"[^>]*>(.*?)</button>(.*?)</li>', re.S)


def parse_question(block):
    after_header = block.split("</header>", 1)[-1]
    found = re.search(r"<p>(.*?)</p>", after_header, re.S)
    prompt = text(found.group(1)) if found else ""
    options = []
    for right, button, rest in OPTION.findall(block):
        spans = re.findall(r"<span[^>]*>(.*?)</span", button, re.S)
        why = re.search(r'<div class="opt-why"[^>]*>(.*?)</div>', rest, re.S)
        options.append([text(spans[-1] if spans else button), 1 if right else 0, text(why.group(1)) if why else ""])
    return prompt, options


def explain_html(entry):
    idea, example, trap = (html.escape(s, quote=False) for s in entry)
    return (
        '<!-- ss-explain --><details class="ss-explain"><summary>Explain it to me</summary>'
        f"<p><b>The idea</b>{idea}</p><p><b>Example</b>{example}</p>"
        f'<p class="trap"><b>Exam trap</b>{trap}</p></details><!-- /ss-explain -->'
    )


def extras_for(code):
    try:
        return importlib.import_module(f"{code}_annotated.study_extras")
    except ModuleNotFoundError:
        return None


def deck_name(folder):
    """(chapter label, title) from the wrapper's <title>, e.g. 'CS331 | Chapter 01 — Intro (Annotated Slides)'."""
    wrapper = folder / "index.html"
    raw = ""
    if wrapper.exists():
        m = re.search(r"<title>(.*?)</title>", wrapper.read_text(encoding="utf-8"), re.S)
        raw = text(m.group(1)) if m else ""
    raw = re.sub(r"^[A-Z]+\d+\s*\|\s*", "", raw)
    raw = re.sub(r"\s*\(Annotated Slides\)\s*$", "", raw)
    number = re.match(r"(\d+)", folder.name)
    chapter = "#" + str(int(number.group(1))) if number else folder.name
    m = re.search(r"\bChapter\s*0*(\d+(?:\.\d+)?)\b", raw, re.I)
    if m:
        chapter = "Ch " + m.group(1)
        raw = (raw[: m.start()] + raw[m.end():]).strip()
    else:
        m = re.match(r"(\d+\.\d+)\s+", raw)
        if m:
            chapter = m.group(1)
            raw = raw[m.end():]
    title = re.sub(r"^[\s:—–-]+|[\s:—–-]+$", "", raw).strip()
    return chapter, title or folder.name


def install_deck(course, folder, extras):
    page = next(p for p in folder.glob("*.html") if p.name != "index.html")
    deck = folder.name
    src = page.read_text(encoding="utf-8")
    out = src
    chapter, title = deck_name(folder)
    final = extras.FINAL.get(deck) if extras and hasattr(extras, "FINAL") else None
    if final:
        chapter = final[1]

    def body(m):
        attrs = re.sub(r'\s+data-(course|deck|final|chapter)="[^"]*"', "", m.group(1))
        extra = f' data-final="{1 if final[0] else 0}"' if final else ""
        return f'<body{attrs} data-course="{course["code"]}" data-deck="{deck}"{extra} data-chapter="{html.escape(chapter)}">'
    out = re.sub(r"<body([^>]*)>", body, out, count=1)

    # explain boxes and drill markers (cleared first so a rerun replaces them)
    out = re.sub(r"<!-- ss-explain -->.*?<!-- /ss-explain -->", "", out, flags=re.S)
    out = re.sub(r'(<section class="card[^"]*" id="slide-\d+" data-slide="\d+")(?: data-drill="[^"]*")', r"\1", out)
    drills = getattr(extras, "DRILLS", {}).get(deck, {}) if extras else {}
    for n, kind in drills.items():
        out, k = re.subn(rf'(<section class="card[^"]*" id="slide-{n}" data-slide="{n}")', rf'\1 data-drill="{kind}"', out, count=1)
        if not k:
            print(f"  ! {deck}: no slide {n} for the {kind} drill")
    explains = getattr(extras, "EXPLAIN", {}).get(deck, {}) if extras else {}
    for n, entry in explains.items():
        start = re.search(rf'<section class="card[^"]*" id="slide-{n}" data-slide="{n}"', out)
        if not start:
            print(f"  ! {deck}: no slide {n} to explain")
            continue
        end = out.find('<section class="card', start.end())
        end = len(out) if end < 0 else end
        notes = out.find('<div class="notes"', start.end(), end)
        close = out.find("</ol>", notes, end) if notes >= 0 else -1
        if close < 0:
            print(f"  ! {deck}: slide {n} has no notes list")
            continue
        at = close + len("</ol>")
        out = out[:at] + explain_html(entry) + out[at:]

    # question ids
    questions = []
    slide_starts = [(m.start(), int(m.group(1))) for m in re.finditer(r'id="slide-(\d+)" data-slide=', out)]

    def tag(m):
        block = re.sub(r' data-qid="[0-9a-f]+"', "", m.group(0), count=1)
        prompt, options = parse_question(block)
        ident = qid(prompt, [o[0] for o in options])
        slide = max((n for pos, n in slide_starts if pos < m.start()), default=0)
        if prompt and len(options) > 1 and sum(o[1] for o in options) == 1:
            questions.append({"d": deck, "id": ident, "s": slide, "p": prompt, "o": options})
        return re.sub(r'^(<article class="q pick[^"]*")', rf'\1 data-qid="{ident}"', block)
    out = ARTICLE.sub(tag, out)

    # script tag after the bookmarks script
    out = TAG_RE.sub("", out)
    marker = re.search(r'<script src="/javascripts/slide-bookmarks\.js[^"]*"[^>]*></script>', out)
    if marker:
        out = out[:marker.end()] + "\n    " + TAG + out[marker.end():]
    else:
        out = out.replace("</body>", TAG + "\n</body>", 1)

    if out != src:
        page.write_text(out, encoding="utf-8", newline="")
    url = course["url"] + "annotated-slides/" + deck + "/"
    return {
        "key": deck,
        "title": title,
        "chapter": chapter,
        "final": final[0] if final else None,
        "href": url + page.name,
        "wrapper": url,
        "count": len(questions),
        "ids": [q["id"] for q in questions],
        "drills": len(drills),
        "explained": len(explains),
    }, questions, out != src


def fill(template, course, n_decks, desc, drills):
    word = "Drills" if drills else "Practice"
    return (
        template.replace("{{DESC}}", html.escape(desc))
        .replace("{{LABEL}}", "Review &amp; " + word)
        .replace("{{LABEL_LC}}", "Review &amp; " + word.lower())
        .replace("{{LABEL_PLAIN}}", "Review and " + word.lower())
        .replace("{{PATH}}", course["path"])
        .replace("{{DEPT_NAME}}", DEPT_NAMES.get(course["dept"], course["dept"].replace("-", " ").title()))
        .replace("{{DEPT}}", course["dept"])
        .replace("{{CODE}}", course["code"].upper())
        .replace("{{code}}", course["code"])
        .replace("{{N}}", str(n_decks))
    )


def write_if_changed(path, content):
    if path.exists() and path.read_text(encoding="utf-8") == content:
        return False
    path.write_text(content, encoding="utf-8", newline="")
    return True


def install_review(course, decks, bank, drills):
    review = course["dir"] / "annotated-slides" / "review"
    review.mkdir(exist_ok=True)
    code = course["code"].upper()
    desc = (f"{code} practice from the Annotated Slides: your saved mistakes, unanswered questions and a "
            f"random mix from every deck" + (", plus calculation drills with new numbers each time." if drills else "."))
    write_if_changed(review / "review.html", fill(PAGE_TEMPLATE.read_text(encoding="utf-8"), course, len(decks), desc, drills))
    wrapper = review / "index.html"
    if not wrapper.exists():  # its sidebar is stamped afterwards; later runs leave the page alone
        wrapper.write_text(fill(WRAPPER_TEMPLATE.read_text(encoding="utf-8"), course, len(decks), desc, drills), encoding="utf-8", newline="")
    summary = {"course": course["code"], "decks": [{k: d[k] for k in ("key", "title", "chapter", "final", "count")} for d in decks]}
    full = {"course": course["code"], "decks": [{k: v for k, v in d.items() if k not in ("drills", "explained")} for d in decks],
            "drills": drills, "questions": bank}
    for name, obj in (("questions.json", full), ("summary.json", summary)):
        write_if_changed(review / name, json.dumps(obj, ensure_ascii=False, separators=(",", ":")))


def install_hub(course):
    hub = course["dir"] / "slides" / "index.html"
    if not hub.exists() or 'id="annotated"' not in hub.read_text(encoding="utf-8"):
        return False
    src = hub.read_text(encoding="utf-8")
    tag = f'<script src="/javascripts/annotated-study.js?v={VERSION}" data-study-hub="{course["code"]}" defer></script>'
    out = TAG_RE.sub("", src).replace("</body>", "    " + tag + "\n  </body>", 1)
    if out != src:
        hub.write_text(out, encoding="utf-8", newline="")
    return out != src


def courses(only):
    for decks_dir in sorted(DOCS.glob("academics/*/*/annotated-slides")):
        course_dir = decks_dir.parent
        code = course_dir.name
        if only and code not in only:
            continue
        folders = sorted(p for p in decks_dir.iterdir() if p.is_dir() and p.name != "review"
                         and any(f.name != "index.html" and 'data-slide="' in f.read_text(encoding="utf-8") for f in p.glob("*.html")))
        if not folders:
            continue
        rel = course_dir.relative_to(DOCS / "academics").as_posix()
        yield {"code": code, "dir": course_dir, "path": rel, "dept": rel.split("/")[0],
               "url": f"/academics/{rel}/"}, folders


def main():
    only = set(a.lower() for a in sys.argv[1:])
    report = []
    for course, folders in courses(only):
        extras = extras_for(course["code"])
        decks, bank, changed = [], [], 0
        for folder in folders:
            meta, questions, did = install_deck(course, folder, extras)
            decks.append(meta)
            bank.extend(questions)
            changed += did
        drills = []
        if extras:
            for deck, slides in getattr(extras, "DRILLS", {}).items():
                final = getattr(extras, "FINAL", {}).get(deck)
                for kind in slides.values():
                    if kind not in {d["type"] for d in drills}:
                        drills.append({"type": kind, "label": final[1] if final else "", "final": final[0] if final else None})
        review = bool(bank)
        if review:
            install_review(course, decks, bank, drills)
        hub = install_hub(course) if review else False
        report.append((course["code"], len(decks), len(bank), changed, review,
                       sum(d["drills"] for d in decks), sum(d["explained"] for d in decks)))
    print(f"{'course':8} decks questions updated review drills explained")
    for code, n, q, ch, rv, dr, ex in report:
        print(f"{code:8} {n:5} {q:9} {ch:7} {'yes' if rv else 'no ':6} {dr:6} {ex:9}")


if __name__ == "__main__":
    main()
