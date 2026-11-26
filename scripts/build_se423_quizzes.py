#!/usr/bin/env python3
"""Build the SE423 chapter quizzes from scripts/se423_quizzes/ (content) and
docs/javascripts/practice-quiz.js (engine).

Each quiz page keeps its URL and its <head> (styles, metadata); the body is rebuilt with every
question type: multiple choice, true/false, matching, ordering, calculation, scenario and short answer.

Fairness checks run on every build (warnings, not errors):
  - a multiple-choice correct option must not be clearly longer than every wrong option;
  - no bracket that only the correct option has;
  - true/false answers should be roughly balanced.
    PYTHONUTF8=1 python3 scripts/build_se423_quizzes.py
"""
import html
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from se423_quizzes import bank_a, bank_b  # noqa: E402

EXAMS = ROOT / "docs/academics/software-engineering/se423/exams"
ENGINE = '<script src="/javascripts/practice-quiz.js?v=1"></script>'
CSS = '<link rel="stylesheet" href="/styles/practice-quiz.css?v=1" />'
SECTIONS = [
    ("mcq", "Multiple choice", "MCQ", "Pick the best answer."),
    ("tf", "True or false", "True/false", "Decide whether each statement is true or false."),
    ("match", "Matching", "Matching", "Choose the matching item for each row."),
    ("order", "Ordering", "Ordering", None),
    ("num", "Calculations", "Calculations", "Type the number, or the calculation itself."),
    ("scenario", "Scenarios", "Scenarios", "Read each case, then answer its parts."),
    ("short", "Short answer", "Short answer", "Answer only what the question asks. Each point it asks for is worth marks."),
]
LABELS = {"mcq": "multiple choice", "tf": "true/false", "match": "matching", "order": "ordering", "num": "calculation",
          "scenario": "scenario", "short": "short answer"}


def walk(items):
    for it in items:
        yield it
        if it["type"] == "scenario":
            yield from it["parts"]


def check(slug, quiz):
    warnings = []
    tf = [it["a"] for it in walk(quiz["items"]) if it["type"] == "tf"]
    for it in walk(quiz["items"]):
        if it["type"] == "mcq":
            opts = it["options"]
            c, wrong = len(opts[0]), [len(o) for o in opts[1:]]
            if c > max(wrong) * 1.15 and c - max(wrong) > 6:
                warnings.append(f"correct option much longer: {it['q'][:60]}")
            if "(" in opts[0] and not any("(" in o for o in opts[1:]):
                warnings.append(f"bracket only in the correct option: {it['q'][:60]}")
            if len(set(opts)) != len(opts):
                warnings.append(f"duplicate options: {it['q'][:60]}")
        if it["type"] == "match" and len({p[1] for p in it["pairs"]}) != len(it["pairs"]):
            pass  # repeated right-hand values are allowed (factor/effect style)
    if tf and abs(sum(tf) - (len(tf) - sum(tf))) > 2:
        warnings.append(f"true/false unbalanced: {sum(tf)} true vs {len(tf) - sum(tf)} false")
    for w in warnings:
        print(f"  ! {slug}: {w}")


def body(slug, quiz, page_title):
    counts = {}
    for it in quiz["items"]:
        counts[it["type"]] = counts.get(it["type"], 0) + 1
    fmt = " · ".join(f"{counts[k]} {LABELS[k]}" for k, *_ in SECTIONS if k in counts)
    sections = []
    for kind, title, short, note in SECTIONS:
        items = [it for it in quiz["items"] if it["type"] == kind]
        if items:
            sections.append({"title": title, "short": short, "note": note, "items": items})
    data = {"id": "se423-" + slug, "minutes": quiz["minutes"], "sections": sections}
    data_json = json.dumps(data, ensure_ascii=False).replace("</", "<\\/")
    chap, title = quiz["chapter"], quiz["title"]
    e = html.escape
    return f"""  <body data-theme="dark">
    <div class="topbar">
      <div class="topbar-inner">
        <div class="brand">
          <span class="course">SE423 · {e(chap)}</span>
          <span class="title">{e(title)} — Chapter Quiz</span>
        </div>
        <div class="controls">
          <div class="timer" id="timer">{quiz['minutes']:02d}:00</div>
          <button class="toggle-btn" id="themeToggle" aria-label="Toggle dark and light mode" title="Toggle dark/light">☀️</button>
        </div>
      </div>
    </div>

    <div class="exam-header">
      <div class="stamp-row"><span class="dot"></span> Self-Graded Chapter Practice Quiz</div>
      <h1>{e(title)}</h1>
      <p>{e(quiz['blurb'])} Submit for instant grading: every question shows the answer and why.</p>
      <div class="meta-strip">
        <span>Total: <b><span data-total>…</span> points</b></span>
        <span>Time limit: <b>{quiz['minutes']} minutes</b></span>
        <span>Questions: <b>{len(quiz['items'])}</b></span>
        <span>Format: <b>{e(fmt)}</b></span>
      </div>
      <div class="coverage-strip">
        <b>How it's graded:</b> short answers are checked only against the points each question asks for. The check looks
        for key words, so after submitting you can claim any point you made in other words with “I covered this”.
      </div>
    </div>

    <main>
      <hr class="rule-line" />
      <div id="pq-root"></div>

      <div class="submit-zone">
        <button class="submit-btn" id="submitBtn">Submit Quiz</button>
        <button class="reset-link" id="resetBtn" style="display: none">Reset and try again</button>
      </div>

      <div class="score-panel" id="scorePanel">
        <div class="big-score" id="bigScore">0</div>
        <div class="score-sub" id="scoreSub"></div>
        <div class="score-breakdown" id="scoreBreakdown"></div>
      </div>
    </main>

    <footer>{e(chap)} self-graded practice quiz · <b>Shoug Alomran</b></footer>

    <script type="application/json" id="quiz-data">{data_json}</script>
    {ENGINE}
    <script src="/javascripts/quiz-mistakes.js" defer></script>
  </body>
</html>
"""


def build(slug, quiz):
    page = EXAMS / slug / f"{slug}.html"
    src = page.read_text(encoding="utf-8")
    head_end = src.index("</head>")
    head = src[:head_end]
    if "practice-quiz.css" not in head:
        head = head.rstrip() + "\n    " + CSS + "\n  "
    desc = (f"SE423 {quiz['chapter']}: {quiz['title']} practice quiz with multiple choice, true/false, matching, "
            f"ordering, scenarios and short answers, graded instantly.")
    head = re.sub(r'(<meta\s+name="description"\s+content=")[^"]*(")', lambda m: m.group(1) + html.escape(desc) + m.group(2), head, count=1)
    head = re.sub(r'(<meta\s+(?:property="og:description"|name="twitter:description")\s+content=")[^"]*(")',
                  lambda m: m.group(1) + html.escape(desc) + m.group(2), head)
    title_m = re.search(r"<title>(.*?)</title>", head, re.S)
    out = head + "</head>\n\n" + body(slug, quiz, title_m.group(1) if title_m else "")
    check(slug, quiz)
    if out != src:
        page.write_text(out, encoding="utf-8", newline="")
        return True
    return False


def main():
    quizzes = {**bank_a.QUIZZES, **bank_b.QUIZZES}
    changed = 0
    for slug, quiz in quizzes.items():
        did = build(slug, quiz)
        changed += did
        n = sum(1 for _ in walk(quiz["items"]))
        print(f"{slug:34} {len(quiz['items']):3} questions ({n} with scenario parts){'  updated' if did else ''}")
    print(f"{changed} quiz page(s) updated")


if __name__ == "__main__":
    main()
