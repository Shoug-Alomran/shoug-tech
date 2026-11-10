#!/usr/bin/env python3
"""Publish CS316 notes, lab notebooks and past quizzes; called by build_cs316_study_tools.py.

Notes are PDFs in extra-resources/notes/<slug>/ with a viewer page. Notebooks are .ipynb files in
extra-resources/notebooks/<slug>/ with a read-only HTML rendering next to them. Past quizzes are
rendered from originals kept off the site in ~/Desktop/CS316 exam originals/.
"""
import html
import json
import os
import re

import markdown

import build_cs316_course as course

URL = course.COURSE_URL
OUT = course.COURSE_DIR
SITE = "https://shoug-tech.com"
ORIGINALS = os.path.expanduser("~/Desktop/CS316 exam originals")

NOTES = [
    ("pandas-code-sheet", "Pandas Code Sheet"),
    ("pandas-data-analytics-cheat-sheet", "Pandas Data Analytics Cheat Sheet"),
    ("handling-missing-data-notes", "Chapter 2.3: Handling Missing Data Notes"),
    ("first-vs-second-order-derivatives", "Chapter 4: First vs Second Order Derivatives"),
    ("classification-compressed-notes", "Classification: Compressed Notes"),
    ("quiz-3-interpretation-guide", "Quiz 3: Interpretation Guide"),
]
NOTEBOOKS = [
    ("pandas-bookstore-scenario", "Chapter 2.1 Lab: Pandas Bookstore Scenario"),
    ("importing-summarizing-visualizing-data-lab", "Chapter 2.2 Lab: Importing, Summarizing and Visualizing Data"),
    ("missing-data-gradebook-rescue", "Chapter 2.3 Lab: Gradebook Rescue"),
    ("empirical-losses-and-risks-demo", "Chapter 3 Demo: Empirical Losses and Risks"),
    ("interactive-gradient-descent-visualization", "Chapter 4 Demo: Gradient Descent Visualization"),
    ("linear-regression-gradient-descent-lab", "Chapter 4 Lab: Linear Regression with Gradient Descent"),
    ("heart-disease-classification-lab", "Classification Lab: Heart Disease"),
    ("normalization-model-performance-lab", "Normalization Lab: Logistic and Linear Regression"),
    ("heart-disease-pca-lab", "Chapter 7.2 Lab: PCA on Heart Disease Data"),
    ("t-sne-tutorial", "Chapter 7.3 Tutorial: t-SNE"),
    ("cross-validation-tutorial", "Chapter 8 Tutorial: Cross-Validation"),
    ("hypothesis-testing-t-test-lab", "Chapter 10 Lab: Hands-on t-Tests"),
]
QUIZZES = [
    ("15-quiz-1-python-programming", "quiz-1-python-programming", "Quiz 1 (Term 261): Python Programming", "quiz1.ipynb"),
    ("16-quiz-2-importing-summarizing-visualizing", "quiz-2-importing-summarizing-visualizing", "Quiz 2 (Term 261): Importing, Summarizing and Visualizing Data", "quiz2.ipynb"),
    ("17-quiz-3-practical", "quiz-3-practical", "Quiz 3 (Term 261): Practical Quiz", "quiz3.ipynb"),
]

STYLE = """
:root{--bg:#f6f5fb;--panel:#fff;--code:#f0eef8;--text:#1c2435;--muted:#5b6478;--line:#d8d5e6;--accent:#7a3fd0}
html[data-theme="dark"]{--bg:#0b0912;--panel:#14111e;--code:#1b1727;--text:#ece9f5;--muted:#a59fb8;--line:#2e2840;--accent:#c084fc}
*{box-sizing:border-box}html,body{margin:0;background:var(--bg);color:var(--text)}
body{font:16px/1.65 Inter,system-ui,sans-serif;overflow-wrap:anywhere}
main{max-width:1000px;margin:0 auto;padding:28px clamp(14px,4vw,40px) 60px}
h1,h2,h3,h4{line-height:1.25;margin:1.4em 0 .5em}h1{font-size:1.8rem}h2{font-size:1.4rem}h3{font-size:1.15rem}
a{color:var(--accent)}img{max-width:100%;height:auto;background:#fff;border-radius:6px}
.note{color:var(--muted);font-size:.9rem;border-bottom:1px solid var(--line);padding-bottom:12px}
.cell{margin:14px 0}pre{margin:0;padding:12px 14px;background:var(--code);border:1px solid var(--line);border-radius:8px;overflow-x:auto;font:13px/1.5 "JetBrains Mono",ui-monospace,monospace;white-space:pre}
.out{margin-top:6px}.out pre{background:transparent;border-style:dashed;color:var(--muted)}
.tw{overflow-x:auto;margin:8px 0}table{border-collapse:collapse;font-size:.88rem}th,td{border:1px solid var(--line);padding:4px 9px;text-align:left}
"""
THEME = ("<script>(function(){var d='dark';try{if(window.parent!==window){var b=parent.document.body;"
         "if(!b.classList.contains('shoug-light-mode'))d='dark';else d='light';}else if(localStorage.getItem('theme')==='light'){d='light';}"
         "}catch(e){}document.documentElement.setAttribute('data-theme',d);})();</script>")
KATEX = ('<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/KaTeX/0.16.11/katex.min.css">'
         '<script defer src="https://cdnjs.cloudflare.com/ajax/libs/KaTeX/0.16.11/katex.min.js"></script>'
         '<script defer src="https://cdnjs.cloudflare.com/ajax/libs/KaTeX/0.16.11/contrib/auto-render.min.js" '
         "onload=\"renderMathInElement(document.body,{delimiters:[{left:'$$',right:'$$',display:true},{left:'$',right:'$',display:false}],throwOnError:false})\"></script>")
EMOJI = re.compile("[\U0001F300-\U0001FAFF\u2600-\u27BF\u23E9-\u23FA\u2B05-\u2B55\uFE0F\u200D]+ ?")
ANSI = re.compile(r"\x1b\[[0-9;]*m")
MATH = re.compile(r"\$\$.+?\$\$|(?<![\\$])\$[^$\n]+?\$", re.S)


def text_of(value):
    return "".join(value) if isinstance(value, list) else (value or "")


def render_markdown(source):
    stash = []
    def hold(match):
        stash.append(match.group(0))
        return "MATHSTASH%dX" % (len(stash) - 1)
    body = MATH.sub(hold, EMOJI.sub("", source))
    out = markdown.markdown(body, extensions=["tables", "fenced_code", "sane_lists"])
    return re.sub(r"MATHSTASH(\d+)X", lambda m: html.escape(stash[int(m.group(1))], quote=False), out)


def render_output(out):
    kind = out.get("output_type")
    if kind == "stream":
        return "<pre>%s</pre>" % html.escape(ANSI.sub("", text_of(out.get("text")))[:6000])
    if kind == "error":
        return "<pre>%s</pre>" % html.escape(ANSI.sub("", "\n".join(out.get("traceback", [])))[:3000])
    data = out.get("data", {})
    if "image/png" in data:
        return '<img alt="Notebook output" loading="lazy" src="data:image/png;base64,%s">' % text_of(data["image/png"]).strip()
    rich = text_of(data.get("text/html"))
    if "<table" in rich:
        rich = re.sub(r"<style.*?</style>|<script.*?</script>", "", rich, flags=re.S)
        return '<div class="tw">%s</div>' % rich
    if data.get("text/plain"):
        return "<pre>%s</pre>" % html.escape(text_of(data["text/plain"])[:6000])
    return ""


def render_notebook(path, title, page_url, note):
    with open(path, encoding="utf-8") as f:
        book = json.load(f)
    cells = []
    for cell in book["cells"]:
        source = text_of(cell["source"])
        if not source.strip():
            continue
        if cell["cell_type"] == "markdown":
            cells.append('<div class="cell">%s</div>' % render_markdown(source))
        elif cell["cell_type"] == "code":
            outs = "".join(render_output(o) for o in cell.get("outputs", []))
            cells.append('<div class="cell"><pre>%s</pre>%s</div>' % (
                html.escape(source), '<div class="out">%s</div>' % outs if outs else ""))
    body = "".join(cells)
    desc = html.escape("CS316 %s, Introduction to AI and Data Science." % title, quote=True)
    safe = html.escape(title, quote=True)
    ld = json.dumps({"@context": "https://schema.org", "@type": "WebPage", "url": page_url, "name": title}, ensure_ascii=False)
    return ('<!doctype html><html lang="en" data-sg-styled data-theme="dark"><head><meta charset="utf-8">'
            '<meta name="viewport" content="width=device-width,initial-scale=1"><title>CS316 %s</title>'
            '<meta name="description" content="%s"><link rel="canonical" href="%s">'
            '<meta property="og:title" content="CS316 %s"><meta property="og:description" content="%s">'
            '<meta property="og:url" content="%s"><meta property="og:type" content="article">'
            '<meta property="og:image" content="%s/assets/og-banner.png">'
            '<meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="CS316 %s">'
            '<meta name="twitter:description" content="%s"><meta name="twitter:image" content="%s/assets/og-banner.png">'
            '<script type="application/ld+json">%s</script>%s<style>%s</style>%s</head><body><main>'
            '<h1>%s</h1><p class="note">%s</p>%s</main></body></html>'
            % (safe, desc, page_url, safe, desc, page_url, SITE, safe, desc, SITE, ld, THEME, STYLE,
               KATEX if "$" in body else "", safe, note, body))


def pdf_viewer(slug, title, i, prev_url, next_url, data):
    shell = course.rebrand(course.read(os.path.join(course.TEMPLATE_DIR, "slides", course.TEMPLATE_DECK, "index.html")))
    path = "extra-resources/notes/"
    t = shell.replace(course.TEMPLATE_DECK, slug).replace(course.TEMPLATE_DECK_TITLE, course.esc(title))
    t = t.replace("/cs316/slides/", "/cs316/" + path).replace(">Slides</a", ">Notes</a").replace("ITEM_01 // SLIDES", "ITEM_%02d // NOTES" % i)
    link = lambda u, cls, word: ('<a href="%s" class="nav-link %s">%s</a>' % (u, cls, word) if u
                                 else '<span class="nav-link %s disabled">%s</span>' % (cls, word))
    t = course.replace_block(r'<div class="nav-strip">.*?</div>',
                             '<div class="nav-strip">%s%s</div>' % (link(prev_url, "prev", "&lt;- PREVIOUS"), link(next_url, "next", "NEXT -&gt;")), t)
    url = URL + path + slug + "/"
    course.write(os.path.join(OUT, path, slug, "index.html"), course.stamp_sidebar(t, data, url))


def row(url, n, title, state="AVAILABLE"):
    return ('<a href="%s" class="dir-row"><div class="dir-num">%02d</div><div class="dir-title">%s</div><div class="dir-status">'
            '<span class="status-tag available">%s</span></div><div class="dir-arrow">%s</div></a>'
            % (url, n, html.escape(title, quote=False), state, course.ARROW))


def add_sidebar(data):
    data["children"][URL + "extra-resources/notes/"] = [
        {"url": "%sextra-resources/notes/%s/" % (URL, s), "attrs": "", "label": t} for s, t in NOTES]
    data["children"][URL + "extra-resources/notebooks/"] = [
        {"url": "%sextra-resources/notebooks/%s/" % (URL, s), "attrs": "", "label": t} for s, t in NOTEBOOKS]
    data["children"][URL + "exams/"] += [
        {"url": "%sexams/%s/" % (URL, q[0]), "attrs": "", "label": q[2]} for q in QUIZZES]


def build(data, frame_page):
    for i, (slug, title) in enumerate(NOTES, 1):
        prev_url = "%sextra-resources/notes/%s/" % (URL, NOTES[i - 2][0]) if i > 1 else None
        next_url = "%sextra-resources/notes/%s/" % (URL, NOTES[i][0]) if i < len(NOTES) else None
        pdf_viewer(slug, title, i, prev_url, next_url, data)
    base = "extra-resources/notebooks/"
    for i, (slug, title) in enumerate(NOTEBOOKS, 1):
        folder = os.path.join(OUT, base, slug)
        page_url = "%s%s%s%s/%s.html" % (SITE, URL, base, slug, slug)
        note = 'Read-only copy of the course notebook. <a href="./%s.ipynb" download>Download the .ipynb</a> to run it in Jupyter or Colab.' % slug
        course.write(os.path.join(folder, slug + ".html"), render_notebook(os.path.join(folder, slug + ".ipynb"), title, page_url, note))
        href = lambda k: "%s%s%s/" % (URL, base, NOTEBOOKS[k][0])
        page = frame_page("%s%s%s/" % (URL, base, slug), base, "Notebooks", "NOTEBOOKS", i, title, slug + ".html",
                          href(i - 2) if i > 1 else None, href(i) if i < len(NOTEBOOKS) else None, data)
        course.write(os.path.join(folder, "index.html"), page)
    for i, (folder, file, title, source) in enumerate(QUIZZES):
        src = os.path.join(ORIGINALS, source)
        target = os.path.join(OUT, "exams", folder)
        page_url = "%s%sexams/%s/%s.html" % (SITE, URL, folder, file)
        note = "The quiz as it was given in Term 261, as a read-only page. Work through it in your own notebook."
        if os.path.exists(src):
            course.write(os.path.join(target, file + ".html"), render_notebook(src, title, page_url, note))
        href = lambda k: "%sexams/%s/" % (URL, QUIZZES[k][0])
        page = frame_page("%sexams/%s/" % (URL, folder), "exams/", "Exams", "EXAMS", 15 + i + 1, title, file + ".html",
                          href(i - 1) if i else None, href(i + 1) if i + 1 < len(QUIZZES) else None, data)
        course.write(os.path.join(target, "index.html"), page)
    return {
        "exam_rows": "".join(row("%sexams/%s/" % (URL, q[0]), 16 + n, q[2]) for n, q in enumerate(QUIZZES)),
        "note_rows": "".join(row("%sextra-resources/notes/%s/" % (URL, s), n, t) for n, (s, t) in enumerate(NOTES, 1)),
        "notebook_rows": "".join(row("%s%s%s/" % (URL, base, s), n, t) for n, (s, t) in enumerate(NOTEBOOKS, 1)),
        "note_count": len(NOTES), "notebook_count": len(NOTEBOOKS),
    }
