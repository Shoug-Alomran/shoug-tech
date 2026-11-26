#!/usr/bin/env python3
"""Install the study tools (docs/javascripts/annotated-study.js) on the SE423 Annotated Slides.

For every deck page it:
  - tags each pick-an-answer question with a stable id (data-qid, a hash of its text) so saved
    answers survive rebuilds and reordering;
  - marks the body with the course, deck, chapter and whether the final exam covers it;
  - marks the slides that get a calculation drill (data-drill);
  - adds the "Explain it to me" boxes from se423_annotated/study_extras.py;
  - adds the script tag.
Then it writes annotated-slides/review/questions.json (every question, for the review page) and
summary.json (deck facts for the course Slides page), and puts the script on the Slides page.

Safe to run again, and run it again after rebuilding a deck: it replaces what it added before.
    PYTHONUTF8=1 python3 scripts/install_annotated_study.py
"""
import html
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from se423_annotated import study_extras as X  # noqa: E402

VERSION = "1"
COURSE_DIR = ROOT / "docs/academics/software-engineering/se423"
DECKS = COURSE_DIR / "annotated-slides"
REVIEW = DECKS / "review"
URL = "/academics/software-engineering/se423/annotated-slides/"
TAG = f'<script src="/javascripts/annotated-study.js?v={VERSION}"></script>'
TAG_RE = re.compile(r'\s*<script src="/javascripts/annotated-study\.js(?:\?v=[^"]*)?"(?: [^>]*)?></script>')
HUB_TAG = f'<script src="/javascripts/annotated-study.js?v={VERSION}" data-study-hub="{X.COURSE}" defer></script>'


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
    prompt = text(re.search(r"<p>(.*?)</p>", after_header, re.S).group(1))
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


def install_deck(folder):
    page = next(p for p in folder.glob("*.html") if p.name != "index.html")
    deck = folder.name
    src = page.read_text(encoding="utf-8")
    out = src
    on_final, chapter = X.FINAL[deck]

    # body attributes
    def body(m):
        attrs = re.sub(r'\s+data-(course|deck|final|chapter)="[^"]*"', "", m.group(1))
        return (f'<body{attrs} data-course="{X.COURSE}" data-deck="{deck}" '
                f'data-final="{1 if on_final else 0}" data-chapter="{chapter}">')
    out = re.sub(r"<body([^>]*)>", body, out, count=1)

    # explain boxes and drill markers (cleared first so a rerun replaces them)
    out = re.sub(r"<!-- ss-explain -->.*?<!-- /ss-explain -->", "", out, flags=re.S)
    out = re.sub(r'(<section class="card[^"]*" id="slide-\d+" data-slide="\d+")(?: data-drill="[^"]*")', r"\1", out)
    drills = X.DRILLS.get(deck, {})
    for n, kind in drills.items():
        out, k = re.subn(rf'(<section class="card[^"]*" id="slide-{n}" data-slide="{n}")', rf'\1 data-drill="{kind}"', out, count=1)
        if not k:
            print(f"  ! {deck}: no slide {n} for the {kind} drill")
    explains = X.EXPLAIN.get(deck, {})
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
        if prompt and any(o[1] for o in options):
            questions.append({"d": deck, "id": ident, "s": slide, "p": prompt, "o": options})
        return re.sub(r'^(<article class="q pick[^"]*")', rf'\1 data-qid="{ident}"', block)
    out = ARTICLE.sub(tag, out)
    dupes = len(questions) - len({q["id"] for q in questions})
    if dupes:
        print(f"  ! {deck}: {dupes} questions share an id (identical text)")

    # script tag after the bookmarks script
    out = TAG_RE.sub("", out)
    marker = re.search(r'<script src="/javascripts/slide-bookmarks\.js[^"]*"[^>]*></script>', out)
    if marker:
        out = out[:marker.end()] + "\n    " + TAG + out[marker.end():]
    else:
        out = out.replace("</body>", TAG + "\n</body>", 1)

    if out != src:
        page.write_text(out, encoding="utf-8", newline="")
    # The wrapper's heading is the clean deck name ("Estimation - Chapter 6"); the deck's own brand
    # line is sometimes a slide fragment.
    heading = re.search(r'<h1 class="ch-title">(.*?)</h1>', (folder / "index.html").read_text(encoding="utf-8"), re.S)
    title = re.sub(r"\s+-\s+Chapter\s+[\d.]+$", "", text(heading.group(1))) if heading else deck
    return {
        "key": deck,
        "title": title,
        "chapter": chapter,
        "final": on_final,
        "href": URL + deck + "/" + page.name,
        "wrapper": URL + deck + "/",
        "count": len(questions),
        "ids": [q["id"] for q in questions],
    }, questions, out != src


def install_hub():
    hub = COURSE_DIR / "slides/index.html"
    src = hub.read_text(encoding="utf-8")
    out = TAG_RE.sub("", src)
    out = out.replace("</body>", "    " + HUB_TAG + "\n  </body>", 1)
    if out != src:
        hub.write_text(out, encoding="utf-8", newline="")
    return out != src


def main():
    decks, bank, changed = [], [], 0
    for folder in sorted(p for p in DECKS.iterdir() if p.is_dir() and p.name in X.FINAL):
        meta, questions, did = install_deck(folder)
        decks.append(meta)
        bank.extend(questions)
        changed += did
        print(f"{folder.name:28} {meta['count']:4} questions  drills {len(X.DRILLS.get(folder.name, {}))}  explained {len(X.EXPLAIN.get(folder.name, {}))}")
    drills = []
    for deck, slides in X.DRILLS.items():
        on_final, chapter = X.FINAL[deck]
        for kind in slides.values():
            if kind not in {d["type"] for d in drills}:
                drills.append({"type": kind, "label": chapter, "final": on_final})
    REVIEW.mkdir(exist_ok=True)
    summary = {"course": X.COURSE, "decks": [{k: d[k] for k in ("key", "title", "chapter", "final", "count")} for d in decks]}
    full = {"course": X.COURSE, "decks": decks, "drills": drills, "questions": bank}
    for name, obj in (("questions.json", full), ("summary.json", summary)):
        (REVIEW / name).write_text(json.dumps(obj, ensure_ascii=False, separators=(",", ":")), encoding="utf-8", newline="")
    hub = install_hub()
    print(f"{len(bank)} questions in the bank; {changed} deck page(s) updated; slides page {'updated' if hub else 'unchanged'}")


if __name__ == "__main__":
    main()
