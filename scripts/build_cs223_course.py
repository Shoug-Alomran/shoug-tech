#!/usr/bin/env python3
"""Build the CS223 (Computational Linear Algebra) course pages.

The course chrome is cloned from MATH221, the other Math-track course with the
same layout, so header, footer, theme and sidebar behave identically:

    overview            <- math221/index.html
    slides/, exams/,
    extra-resources/    <- math221/slides/index.html (directory listing)
    one PDF / one exam  <- math221/slides/1-1/index.html (viewer wrapper)
    slide-breakdowns/   <- math221/exams/index.html (COMING SOON page)

Interactive exams are rendered from scripts/cs223_exam_content.py into
standalone pages (exams/NN-<slug>/<slug>.html) styled by docs/styles/cs223-exam.css
and driven by docs/javascripts/cs223-exam.js; each one gets a viewer wrapper
that iframes it. Only re-typeset questions are published, never the original
papers.

Worksheets live in extra-resources/worksheets/{unsolved,solved}/ and are owned by
scripts/embed_resources.py (solved/unsolved listings, PDF viewers, Study
Material row). This script only creates the Study Material page they hang off.

After running:
    python3 scripts/embed_resources.py           # worksheets section
    python3 scripts/build_academic_sidebar.py    # stamp the sidebar
"""

import html
import json
import os
import re
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from cs223_exam_content import EXAMS  # noqa: E402

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOCS = os.path.join(REPO, "docs")
MATH = os.path.join(DOCS, "academics", "math")
SRC = os.path.join(MATH, "math221")
OUT = os.path.join(MATH, "cs223")
SIDEBAR_FILE = os.path.join(REPO, "scripts", "academic-sidebar.json")
SITE = "https://shoug-tech.com"
BASE = "/academics/math/cs223/"
CODE = "CS223"
NAME = "Computational Linear Algebra"

# --------------------------------------------------------------------------- #
# course content
# --------------------------------------------------------------------------- #

CHAPTERS = [
    (1, "Linear Equations in Linear Algebra"),
    (2, "Matrix Algebra"),
    (3, "Determinants"),
    (4, "Vector Spaces"),
    (5, "Eigenvalues and Eigenvectors"),
    (6, "Orthogonality and Least Squares"),
]

# (folder, sidebar label, full title, chapter); the PDF is <folder>/<folder>.pdf
DECKS = [
    ("ch1-lecture-1", "1.1 Systems of Linear Equations", "Chapter 1, Lecture 1: Systems of Linear Equations", 1),
    ("ch1-lecture-2", "1.2 Row Reduction and Echelon Forms", "Chapter 1, Lecture 2: Row Reduction and Echelon Forms", 1),
    ("ch1-lecture-3", "1.3 Vector Equations", "Chapter 1, Lecture 3: Vector Equations", 1),
    ("ch1-lecture-4", "1.4 The Matrix Equation Ax = b", "Chapter 1, Lecture 4: The Matrix Equation Ax = b", 1),
    ("ch1-lecture-5", "1.5 Linear Independence", "Chapter 1, Lecture 5: Linear Independence", 1),
    ("ch1-lecture-6", "1.6 Linear Transformations", "Chapter 1, Lecture 6: Introduction to Linear Transformations", 1),
    ("ch2-lecture-1", "2.1 Matrix Operations", "Chapter 2, Lecture 1: Matrix Operations", 2),
    ("ch2-lecture-2", "2.2 The Inverse of a Matrix", "Chapter 2, Lecture 2: The Inverse of a Matrix", 2),
    ("ch2-lecture-3", "2.3 LU Factorization", "Chapter 2, Lecture 3: Matrix Factorization (LU)", 2),
    ("ch2-lecture-4", "2.4 Subspaces of Rn", "Chapter 2, Lecture 4: Subspaces of Rn, Dimension and Rank", 2),
    ("ch3-lecture-1", "3.1 Introduction to Determinants", "Chapter 3, Lecture 1: Introduction to Determinants", 3),
    ("ch3-lecture-2", "3.2 Properties of Determinants", "Chapter 3, Lecture 2: Properties of Determinants", 3),
    ("ch3-lecture-3", "3.3 Cramer's Rule and Volume", "Chapter 3, Lecture 3: Cramer's Rule, the Adjugate and Volume", 3),
    ("ch4-lecture-1", "4.1 Vector Spaces and Subspaces", "Chapter 4, Lecture 1: Vector Spaces, Null and Column Spaces, Bases", 4),
    ("ch4-lecture-2", "4.2 Dimension and Rank", "Chapter 4, Lecture 2: Dimension and Rank", 4),
    ("ch4-lecture-3", "4.3 Difference Equations", "Chapter 4, Lecture 3: Discrete Signals and Difference Equations", 4),
    ("ch5-lecture-1", "5.1 Eigenvectors and Eigenvalues", "Chapter 5, Lecture 1: Eigenvectors and Eigenvalues", 5),
    ("ch5-lecture-2", "5.2 The Characteristic Equation", "Chapter 5, Lecture 2: The Characteristic Equation", 5),
    ("ch5-lecture-3", "5.3 Diagonalization", "Chapter 5, Lecture 3: Diagonalization", 5),
    ("ch5-lecture-4", "5.4 Eigenvectors and Transformations", "Chapter 5, Lecture 4: Eigenvectors and Linear Transformations", 5),
    ("ch5-lecture-5", "5.5 Complex Eigenvalues", "Chapter 5, Lecture 5: Complex Eigenvalues and Applications", 5),
    ("ch6-lecture-1", "6.1 Inner Product and Orthogonality", "Chapter 6, Lecture 1: Inner Product, Length and Orthogonality", 6),
    ("ch6-lecture-2", "6.2 Orthogonal Sets", "Chapter 6, Lecture 2: Orthogonal Sets", 6),
    ("ch6-lecture-3", "6.3 Projections, Gram-Schmidt, QR", "Chapter 6, Lecture 3: Orthogonal Projections, Gram-Schmidt and QR", 6),
    ("ch6-lecture-4", "6.4 Least-Squares Problems", "Chapter 6, Lecture 4: Least-Squares Problems", 6),
    ("ch6-lecture-5", "6.5 Linear Models", "Chapter 6, Lecture 5: Applications to Linear Models", 6),
    ("iterative-methods", "Iterative Methods", "Iterative Methods for Solving Linear Systems", 0),
]

# Single-file Study Material items: (folder, title, keep the PSU rights notice?)
STUDY = [
    ("final-review-notes", "Final Review Notes (Handwritten, All Chapters)", False),
    ("practice-ref-and-rref", "Practice: REF and RREF", True),
    ("ch4-lecture-3-solved", "Chapter 4, Lecture 3: Solved Examples", True),
    ("python-project", "Project: Solving Linear Systems in Python", True),
    ("textbook", "Textbook: Lay, Linear Algebra and Its Applications (5th ed.)", False),
]

ARROW = ('<div class="dir-arrow"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" '
         'stroke-linecap="square"><path d="M5 12h14M12 5l7 7-7 7"/></svg></div>')
# Same folder markup embed_resources.py writes, so sort_folder_rows sees a folder.
from build_activity_and_project_pages import EXTRA_CSS, FOLDER as FOLDER_ICON  # noqa: E402

TABS = [("", "Overview"), ("slide-breakdowns/", "Slide Breakdowns"), ("slides/", "Slides"),
        ("extra-resources/", "Study Material"), ("exams/", "Exams")]


def esc(text):
    return html.escape(text, quote=True)


def read(path):
    with open(path, encoding="utf-8") as fh:
        return fh.read()


PENDING = {}


def write(path, text):
    """Queue a page; flush() stamps the sidebar and writes only what changed."""
    PENDING[path] = text


def save(path, text):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    old = read(path) if os.path.exists(path) else None
    if old != text:
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(text)
        print("wrote", os.path.relpath(path, REPO))


def pages(pdf):
    try:
        out = subprocess.run(["pdfinfo", pdf], capture_output=True, text=True, check=True).stdout
        return int(re.search(r"Pages:\s+(\d+)", out).group(1))
    except (OSError, subprocess.CalledProcessError, AttributeError):
        return 0


# --------------------------------------------------------------------------- #
# template retargeting
# --------------------------------------------------------------------------- #

def course_swap(text):
    return text.replace("/academics/math/math221/", BASE).replace("MATH221", CODE).replace("math221", "cs223")


def retarget_head(text, old_path, new_path, title, desc):
    """Point a cloned page's <title>, description, canonical, OG/Twitter, JSON-LD and hreflang at new_path."""
    text = text.replace(SITE + old_path + '"', SITE + new_path + '"').replace(SITE + old_path + "?lang=ar", SITE + new_path + "?lang=ar")
    text = re.sub(r"<title>.*?</title>", "<title>%s</title>" % esc(title), text, count=1, flags=re.S)
    social = "SHOUG.TECH | " + title
    for attr in ('property="og:title"', 'name="twitter:title"'):
        text = re.sub(r'(%s\s+content=")[^"]*(")' % re.escape(attr), lambda m: m.group(1) + esc(social) + m.group(2), text)
    for attr in ('name="description"', 'property="og:description"', 'name="twitter:description"'):
        text = re.sub(r'(%s\s+content=")[^"]*(")' % re.escape(attr), lambda m: m.group(1) + esc(desc) + m.group(2), text)
    text = re.sub(r'("name":\s*")SHOUG\.TECH[^"]*(")', lambda m: m.group(1) + social.replace('"', "'") + m.group(2), text, count=1)
    text = re.sub(r'(<script type="application/ld\+json">.*?"description":\s*")[^"]*(")',
                  lambda m: m.group(1) + desc.replace('"', "'") + m.group(2), text, count=1, flags=re.S)
    return text


def set_tab(text, active):
    """Mark the content tab for `active` (a TABS suffix) as the current one."""
    text = re.sub(r'class="tab active"', 'class="tab"', text)
    return text.replace('href="%s%s" class="tab"' % (BASE, active), 'href="%s%s" class="tab active"' % (BASE, active), 1)


def dir_row(num, href, title, status, folder=False):
    cls = "dir-row directory-folder" if folder else "dir-row"
    title_html = ('<div class="dir-title">%s<span class="dir-title-text">%s</span></div>' % (FOLDER_ICON, esc(title))
                  if folder else '<div class="dir-title">%s</div>' % esc(title))
    tag = '<span class="status-tag">%s</span>' % status if folder else '<span class="status-tag available">%s</span>' % status
    return ('\n                <a href="%s" class="%s" data-ar-title="">\n                    <div class="dir-num">%02d</div>\n'
            '                    %s\n                    <div class="dir-status">%s</div>\n                    %s\n                </a>'
            % (href, cls, num, title_html, tag, ARROW))


def listing_page(path_suffix, label, rows, desc, title):
    text = course_swap(read(os.path.join(SRC, "slides", "index.html")))
    text = retarget_head(text, BASE + "slides/", BASE + path_suffix, title, desc)
    text = text.replace('<span class="current">Slides</span>', '<span class="current">%s</span>' % esc(label))
    text = text.replace('<div class="type-label">SLIDES</div>', '<div class="type-label">%s</div>' % esc(label.upper()))
    text = set_tab(text, path_suffix)
    body = "".join(rows)
    # The MATH221 listing has no folder-icon rules; without them the SVG fills the row.
    icon_css = "\n".join(line for line in EXTRA_CSS.splitlines() if "dir-folder-icon" in line)
    if 'id="cs223-folder-icon"' not in text:
        text = text.replace("</head>", '<style id="cs223-folder-icon">\n%s\n</style>\n</head>' % icon_css, 1)
    text = re.sub(r'(<div class="dir-header">.*?</div>).*?(\s*</div>\s*</div>\s*</main>)',
                  lambda m: m.group(1) + body + m.group(2), text, count=1, flags=re.S)
    return text


VIEWER = None


def viewer_page(url, section_url, section_label, label, title, desc, embed, open_href, prev_href, next_href, rights=True):
    global VIEWER
    if VIEWER is None:
        VIEWER = course_swap(read(os.path.join(SRC, "slides", "1-1", "index.html")))
    text = retarget_head(VIEWER, BASE + "slides/1-1/", url, title, desc)
    text = re.sub(r'<a class="breadcrumb-link" href="%sslides/"\s*>Slides</a\s*>' % re.escape(BASE),
                  '<a class="breadcrumb-link" href="%s">%s</a>' % (section_url, esc(section_label)), text, count=1)
    text = text.replace('<span class="current">1.1</span>', '<span class="current">%s</span>' % esc(label))
    text = text.replace('<div class="ch-label">SLIDES</div>', '<div class="ch-label">%s</div>' % esc(section_label.upper()))
    text = text.replace('<h1 class="ch-title">1.1</h1>', '<h1 class="ch-title">%s</h1>' % esc(label))
    text = re.sub(r'(<a\s+class="btn btn-primary"\s+href=")[^"]*(")', lambda m: m.group(1) + open_href + m.group(2), text, count=1)
    text = re.sub(r'(<a class="btn btn-secondary" href=")[^"]*(")', lambda m: m.group(1) + section_url + m.group(2), text, count=1)
    nav = ('<div class="nav-strip">\n          <a href="%s" class="nav-link prev">&lt;- PREVIOUS</a>\n'
           '          <a href="%s" class="nav-link next">NEXT -&gt;</a>\n        </div>' % (prev_href, next_href))
    text = re.sub(r'<div class="nav-strip">.*?</div>', nav, text, count=1, flags=re.S)
    text = re.sub(r'(<div class="embed-container" id="embedded-content">).*?</noscript>\s*',
                  lambda m: m.group(1) + "\n" + embed + "\n          ", text, count=1, flags=re.S)
    if not rights:
        text = re.sub(r'\s*<div\s+style="\s*margin: 24px 40px 0;.*?is prohibited\.\s*</div>\s*</div>', "", text, count=1, flags=re.S)
    return text


def pdf_embed(src, title):
    return ('            <div class="pdf-embed" data-pdf-src="%s" data-pdf-title="%s"></div>\n'
            '            <noscript><iframe src="%s" width="100%%" height="100%%" title="%s"></iframe></noscript>'
            % (src, esc(title), src, esc(title)))


def chain(urls, index_url):
    """(prev, next) for each url in order; the ends point back at the index."""
    out = []
    for i, _ in enumerate(urls):
        out.append((urls[i - 1] if i else index_url, urls[i + 1] if i + 1 < len(urls) else index_url))
    return out


# --------------------------------------------------------------------------- #
# exam pages
# --------------------------------------------------------------------------- #

THEME_SCRIPT = r"""    <script>
      /* Theme: stored site preference, then the embedding wrapper (it only marks
         itself in LIGHT mode, so an unmarked same-origin parent means dark),
         then the OS. Same resolver as the CS210 exam pages. */
      (function () {
        var root = document.documentElement;
        function parentTheme() {
          try {
            if (!window.parent || window.parent === window) return null;
            var body = window.parent.document.body;
            if (body && body.classList.contains("shoug-light-mode")) return "light";
            var attr = (body && body.getAttribute("data-theme")) || window.parent.document.documentElement.getAttribute("data-theme");
            if (attr === "dark" || attr === "light") return attr;
            return "dark";
          } catch (e) {
            return null;
          }
        }
        function stored() {
          try {
            var saved = localStorage.getItem("shoug-theme") || localStorage.getItem("theme");
            if (saved === "dark" || saved === "light") return saved;
          } catch (e) {}
          return null;
        }
        function resolve() {
          var saved = stored();
          if (saved) return saved;
          var inherited = parentTheme();
          if (inherited) {
            try {
              localStorage.setItem("shoug-theme", inherited);
              localStorage.setItem("theme", inherited);
            } catch (e) {}
            return inherited;
          }
          return window.matchMedia && window.matchMedia("(prefers-color-scheme: dark)").matches ? "dark" : "light";
        }
        function apply() {
          var theme = resolve();
          if (root.getAttribute("data-theme") !== theme) root.setAttribute("data-theme", theme);
          if (root.style.colorScheme !== theme) root.style.colorScheme = theme;
        }
        apply();
        if (window.parent !== window) root.classList.add("is-embedded");
        /* The wrapper's theme button writes localStorage; follow it live. */
        window.addEventListener("storage", function (e) {
          if (e.key === "shoug-theme" || e.key === "theme") apply();
        });
        if (window.MutationObserver) {
          new MutationObserver(apply).observe(root, { attributes: true, attributeFilter: ["data-theme"] });
        }
        document.addEventListener("DOMContentLoaded", apply);
        window.addEventListener("load", apply);
      })();
    </script>"""

THEME_TOGGLE = """<button class="sg-theme-toggle" type="button" onclick="toggleTheme()" aria-label="Toggle dark and light mode">
          <svg class="sg-icon-moon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M20.2 14.6A8.4 8.4 0 0 1 9.4 3.8a8.4 8.4 0 1 0 10.8 10.8Z" /></svg>
          <svg class="sg-icon-sun" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="12" cy="12" r="4.1" /><path d="M12 2.4v2.3M12 19.3v2.3M2.4 12h2.3M19.3 12h2.3M5.2 5.2l1.6 1.6M17.2 17.2l1.6 1.6M18.8 5.2l-1.6 1.6M6.8 17.2l-1.6 1.6" /></svg>
          <span data-theme-label>Dark</span>
        </button>"""

KATEX = "https://cdnjs.cloudflare.com/ajax/libs/KaTeX/0.16.9"


def fmt_pts(p):
    p = float(p)
    num = ("%g" % p)
    return "%s pt" % num if p == 1 else "%s pts" % num


def render_part(exam_slug, si, part):
    pid = "s%d-%s" % (si + 1, re.sub(r"[^a-z0-9]+", "-", part["label"].lower()).strip("-"))
    kind = part["kind"]
    attrs = 'data-part="%s" data-kind="%s" data-pts="%g"' % (pid, kind, part["pts"])
    if kind == "mcq":
        attrs += ' data-answer="%d"' % part["answer"]
    out = ['        <article class="ex-part" id="%s" %s>' % (pid, attrs),
           '          <div class="ex-part-head">',
           '            <span class="ex-part-label">%s</span>' % esc(part["label"]),
           '            <div class="ex-part-prompt">%s</div>' % part["prompt"],
           '            <span class="ex-part-pts">%s</span>' % fmt_pts(part["pts"]),
           "          </div>",
           '          <div class="ex-answer">']
    if kind == "mcq":
        out.append('            <div class="ex-options" role="radiogroup" aria-label="Options for %s">' % esc(part["label"]))
        for i, opt in enumerate(part["options"]):
            out.append('              <label class="ex-option"><input type="radio" name="%s" value="%d" /><span>%s</span></label>'
                       % (pid, i, opt))
        out.append("            </div>")
    elif kind == "fields":
        out.append('            <div class="ex-fields">')
        for k, field in enumerate(part["fields"]):
            label, answer = field[0], field[1]
            mode = field[2] if len(field) > 2 else ""
            fid = "%s-f%d" % (pid, k)
            out.append('              <div class="ex-field"><label for="%s">%s</label>'
                       '<input class="ex-input" id="%s" type="text" autocomplete="off" spellcheck="false" data-answer="%s"%s /></div>'
                       % (fid, esc(label), fid, esc(answer), ' data-mode="%s"' % mode if mode else ""))
        out.append("            </div>")
        hint = part.get("hint") or "Fractions, decimals, sqrt(…) and lists separated by commas all work."
        out.append('            <p class="ex-hint">%s</p>' % esc(hint))
    out.append('            <div class="ex-part-actions">')
    if kind != "written":
        out.append('              <button class="ex-btn ex-btn--primary" type="button" data-act="check">Check</button>')
    out.append('              <button class="ex-btn" type="button" data-act="reveal">Show solution</button>')
    out.append("            </div>")
    out.append('            <div class="ex-feedback" aria-live="polite"></div>')
    out.append("          </div>")
    out.append('          <div class="ex-solution" hidden>')
    out.append('            <div class="ex-solution-title">Worked solution</div>')
    out.append('            <ol class="ex-steps">')
    for step in part.get("steps", []):
        out.append("              <li>%s</li>" % step)
    out.append("            </ol>")
    if part.get("final"):
        out.append('            <p class="ex-final"><strong>Answer:</strong> %s</p>' % part["final"])
    if part.get("note"):
        out.append('            <p class="ex-note"><strong>Note on the original key:</strong> %s</p>' % part["note"])
    if kind == "written":
        out.append('            <div class="ex-selfmark" role="group" aria-label="Mark your answer">'
                   '<span>How did you do?</span>'
                   '<button class="ex-btn" type="button" data-mark="1">Full marks</button>'
                   '<button class="ex-btn" type="button" data-mark="0.5">Half</button>'
                   '<button class="ex-btn" type="button" data-mark="0">Missed it</button></div>')
    out.append("          </div>")
    out.append("        </article>")
    return "\n".join(out)


def exam_html(exam, url):
    title = "%s | %s" % (CODE, exam["title"])
    desc = "Interactive %s %s: check your answers and open a worked solution for every part." % (CODE, exam["title"])
    total = sum(p["pts"] for s in exam["sections"] for p in s["parts"])
    sections = []
    for si, sec in enumerate(exam["sections"]):
        declared = sum(p["pts"] for p in sec["parts"])
        assert abs(declared - sec["pts"]) < 1e-9, "%s / %s: parts sum to %s, section says %s" % (exam["slug"], sec["title"], declared, sec["pts"])
        block = ['      <section class="ex-section" aria-labelledby="sec-%d">' % (si + 1),
                 '        <div class="ex-section-head"><h2 id="sec-%d">%s</h2><span class="ex-section-pts">%s</span></div>'
                 % (si + 1, esc(sec["title"]), fmt_pts(sec["pts"]).upper())]
        if sec.get("intro"):
            block.append('        <div class="ex-section-intro">%s</div>' % sec["intro"])
        block += [render_part(exam["slug"], si, p) for p in sec["parts"]]
        block.append("      </section>")
        sections.append("\n".join(block))
    meta = "".join("<li>%s</li>" % esc(m) for m in exam["meta"])
    notice = '\n        <p class="ex-note">%s</p>' % esc(exam["notice"]) if exam.get("notice") else ""
    canonical = SITE + url
    return """<!doctype html>
<html lang="en" data-sg-styled>
  <head>
    <link rel="icon" type="image/png" sizes="256x256" href="/assets/shoug-favicon-v4.png" />
    <link rel="shortcut icon" type="image/png" href="/assets/shoug-favicon-v4.png" />
    <link rel="apple-touch-icon" sizes="180x180" href="/assets/shoug-apple-touch-icon-v4.png" />
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>{title}</title>
    <link rel="preconnect" href="https://fonts.googleapis.com" />
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;700;800&family=Rajdhani:wght@600;700&display=swap" rel="stylesheet" />
    <link rel="stylesheet" href="{katex}/katex.min.css" />
    <link rel="stylesheet" href="/styles/cs223-exam.css" />
{theme}
    <script src="/javascripts/standalone-theme.js"></script>
    <script src="/javascripts/html-theme-sync.js"></script>

    <meta name="description" content="{desc}" />
    <link rel="canonical" href="{canonical}" />
    <meta property="og:title" content="SHOUG.TECH | {title}" />
    <meta property="og:description" content="{desc}" />
    <meta property="og:url" content="{canonical}" />
    <meta property="og:type" content="article" />
    <meta property="og:image" content="https://shoug-tech.com/assets/og-banner.png" />
    <meta name="twitter:card" content="summary_large_image" />
    <meta name="twitter:title" content="SHOUG.TECH | {title}" />
    <meta name="twitter:description" content="{desc}" />
    <meta name="twitter:image" content="https://shoug-tech.com/assets/og-banner.png" />
    <script type="application/ld+json">
      {{
        "@context": "https://schema.org",
        "@type": "WebPage",
        "url": "{canonical}",
        "name": "SHOUG.TECH | {title}",
        "description": "{desc}",
        "isPartOf": {{ "@type": "WebSite", "name": "Shoug's Digital Garden", "url": "https://shoug-tech.com/" }}
      }}
    </script>
    <link rel="alternate" hreflang="en" href="{canonical}" />
    <link rel="alternate" hreflang="ar" href="{canonical}?lang=ar" />
    <link rel="alternate" hreflang="x-default" href="{canonical}" />
    <link rel="stylesheet" href="/styles/a11y.css" />
    <link rel="manifest" href="/site.webmanifest" />
    <meta name="theme-color" content="#050508" />
  </head>
  <body>
    <main class="ex-shell" id="main-content" data-cs223-exam="{slug}" data-duration="{duration}">
      <header class="ex-head">
        <div class="ex-head-top">
          <div class="ex-kicker">{kicker}</div>
          {toggle}
        </div>
        <h1>{h1}</h1>
        <p class="ex-lede">{lede}</p>
        <ul class="ex-meta">{meta}<li>{total} points total</li></ul>{notice}
        <div class="ex-search" data-page-search-host></div>
      </header>

      <div class="ex-bar">
        <div class="ex-progress">
          <div class="ex-progress-track"><div class="ex-progress-fill"></div></div>
          <span class="ex-progress-label">0 parts marked</span>
        </div>
        <span class="ex-score">Score <strong data-score>0 / {total}</strong></span>
        <span class="ex-timer">{timer_label} <strong data-timer>00:00</strong></span>
        <div class="ex-actions">
          <button class="ex-btn" type="button" data-act="timer">Start timer</button>
          <button class="ex-btn" type="button" data-act="check-all">Check all</button>
          <button class="ex-btn" type="button" data-act="reveal-all">Show all solutions</button>
          <button class="ex-btn" type="button" data-act="reset">Reset</button>
        </div>
      </div>

{sections}

      <section class="ex-result" hidden aria-live="polite">
        <h2>Result: <span data-result-score></span></h2>
        <p>Every part is marked. Auto-checked parts count what you typed; written parts count your own marks. Use Reset to try again.</p>
      </section>
    </main>

    <script defer src="{katex}/katex.min.js"></script>
    <script defer src="{katex}/contrib/auto-render.min.js"></script>
    <script defer src="/javascripts/cs223-exam.js"></script>
    <script src="/javascripts/register-sw.js" defer></script>
  </body>
</html>
""".format(title=esc(title), katex=KATEX, theme=THEME_SCRIPT, desc=esc(desc), canonical=canonical, slug=exam["slug"],
           duration=exam["duration"], kicker=esc(exam["kicker"]), toggle=THEME_TOGGLE, h1=esc(exam["title"]),
           lede=esc(exam["lede"]), meta=meta, total="%g" % total, notice=notice,
           timer_label="Time left" if exam["duration"] else "Elapsed", sections="\n\n".join(sections))


# --------------------------------------------------------------------------- #
# build
# --------------------------------------------------------------------------- #

def build_exams():
    folders = ["%02d-%s" % (i + 1, e["slug"]) for i, e in enumerate(EXAMS)]
    urls = [BASE + "exams/%s/" % f for f in folders]
    rows = []
    for i, (exam, folder, url) in enumerate(zip(EXAMS, folders, urls)):
        content_url = url + exam["slug"] + ".html"
        write(os.path.join(OUT, "exams", folder, exam["slug"] + ".html"), exam_html(exam, content_url))
        prev_href, next_href = chain(urls, BASE + "exams/")[i]
        embed = ('            <iframe class="embed-frame cs223-exam-frame" src="%s" title="%s" loading="lazy" '
                 'style="min-height: calc(100vh - 140px);"></iframe>' % (content_url, esc(exam["title"])))
        desc = "Interactive %s %s with answer checking and worked solutions." % (CODE, exam["title"])
        write(os.path.join(OUT, "exams", folder, "index.html"),
              viewer_page(url, BASE + "exams/", "Exams", exam["title"], "%s | %s" % (CODE, exam["title"]), desc,
                          embed, content_url, prev_href, next_href, rights=False))
        rows.append(dir_row(i + 1, url, exam["title"], "INTERACTIVE"))
    write(os.path.join(OUT, "exams", "index.html"),
          listing_page("exams/", "Exams", rows, "Interactive %s past exams with answer checking and worked solutions." % CODE,
                       "%s | Exams" % CODE))
    return list(zip(urls, [e["title"] for e in EXAMS]))


def build_slides():
    urls = [BASE + "slides/%s/" % d[0] for d in DECKS]
    rows = []
    for i, (folder, label, title, _ch) in enumerate(DECKS):
        base = os.path.join(OUT, "slides", folder)
        pdf = os.path.join(base, folder + ".pdf")
        pptx = os.path.join(base, folder + ".pptx")
        prev_href, next_href = chain(urls, BASE + "slides/")[i]
        desc = "%s %s slides: %s." % (CODE, NAME, title)
        if os.path.exists(pdf):
            src = BASE + "slides/%s/%s.pdf" % (folder, folder)
            embed = pdf_embed(src, title)
            open_href = src
        else:
            # Only the PowerPoint exists: offer it as a download instead of an embed.
            src = BASE + "slides/%s/%s.pptx" % (folder, folder)
            embed = ('            <div class="cs223-download" style="margin: auto; padding: 48px 24px; text-align: center; '
                     'font-family: var(--font-mono); line-height: 1.8;">This lecture is only available as a PowerPoint file.<br />'
                     '<a class="btn btn-primary" style="display: inline-block; margin-top: 16px;" href="%s" download>'
                     '[ DOWNLOAD .PPTX ]</a></div>' % src)
            open_href = src
        write(os.path.join(base, "index.html"),
              viewer_page(urls[i], BASE + "slides/", "Slides", label, "%s | %s" % (CODE, title), desc, embed, open_href,
                          prev_href, next_href, rights=True))
        rows.append(dir_row(i + 1, urls[i], title, "AVAILABLE" if os.path.exists(pdf) else "PPTX"))
    write(os.path.join(OUT, "slides", "index.html"),
          listing_page("slides/", "Slides", rows, "%s %s lecture slides for all six chapters." % (CODE, NAME), "%s | Slides" % CODE))
    return list(zip(urls, [d[1] for d in DECKS]))


def build_study():
    urls = [BASE + "extra-resources/%s/" % s[0] for s in STUDY]
    for i, (folder, title, rights) in enumerate(STUDY):
        src = BASE + "extra-resources/%s/%s.pdf" % (folder, folder)
        prev_href, next_href = chain(urls, BASE + "extra-resources/")[i]
        write(os.path.join(OUT, "extra-resources", folder, "index.html"),
              viewer_page(urls[i], BASE + "extra-resources/", "Study Material", title, "%s | %s" % (CODE, title),
                          "%s %s study material: %s." % (CODE, NAME, title), pdf_embed(src, title), src, prev_href, next_href,
                          rights=rights))
    # Folders first, then files (site-wide rule). The worksheets row is kept up to
    # date by embed_resources.py; this is its initial state.
    ws = os.path.join(OUT, "extra-resources", "worksheets")
    count = sum(len([f for f in os.listdir(os.path.join(ws, s)) if f.endswith(".pdf")])
                for s in ("unsolved", "solved") if os.path.isdir(os.path.join(ws, s)))
    rows = [dir_row(1, BASE + "extra-resources/worksheets/", "Worksheets", "%d FILES" % count, folder=True)]
    rows += [dir_row(i + 2, u, s[1], "AVAILABLE") for i, (u, s) in enumerate(zip(urls, STUDY))]
    path = os.path.join(OUT, "extra-resources", "index.html")
    if not os.path.exists(path):
        write(path, listing_page("extra-resources/", "Study Material", rows,
                                 "%s %s study material: worksheets with solutions, review notes, practice and the textbook." % (CODE, NAME),
                                 "%s | Study Material" % CODE))
    else:
        # embed_resources.py owns the worksheets row once the page exists; only
        # refresh the single-file rows after it.
        text = read(path)
        listing = text.index('<div class="directory-container">')
        start = text.index('href="%sextra-resources/worksheets/"' % BASE, listing)
        end = text.index("</a>", start) + 4
        tail = re.search(r"\s*</div>\s*</div>\s*</main>", text[end:])
        text = text[:end] + "".join(rows[1:]) + text[end + tail.start():]
        write(path, text)
    return list(zip(urls, [s[1] for s in STUDY]))


def build_breakdowns():
    text = course_swap(read(os.path.join(SRC, "exams", "index.html")))
    text = retarget_head(text, BASE + "exams/", BASE + "slide-breakdowns/", "%s | Slide Breakdowns" % CODE,
                         "%s %s slide breakdowns are being prepared." % (CODE, NAME))
    text = text.replace('<span class="current">Quizzes</span>', '<span class="current">Slide Breakdowns</span>')
    text = text.replace('<div class="type-label">QUIZZES</div>', '<div class="type-label">SLIDE BREAKDOWNS</div>')
    write(os.path.join(OUT, "slide-breakdowns", "index.html"), set_tab(text, "slide-breakdowns/"))


def build_overview(exams):
    text = course_swap(read(os.path.join(SRC, "index.html")))
    desc = "%s // %s: lecture slides, worksheets with solutions and interactive past exams with worked answers." % (CODE, NAME)
    text = retarget_head(text, BASE, BASE, "%s // %s" % (CODE, NAME), desc)
    text = text.replace("SHOUG.TECH | SHOUG.TECH", "SHOUG.TECH")
    # MATH221's overview clock has id="clock" but its ticker updates #live-clock.
    text = text.replace('<span id="clock">', '<span id="live-clock">')
    decks = {}
    total = 0
    for folder, _label, _title, ch in DECKS:
        n = pages(os.path.join(OUT, "slides", folder, folder + ".pdf"))
        if n == 0 and os.path.exists(os.path.join(OUT, "slides", folder, folder + ".pptx")):
            n = 15  # the PowerPoint-only deck has 15 slides
        decks.setdefault(ch, []).append(n)
        total += n
    topics = []
    for ch, name in CHAPTERS + [(0, "Iterative Methods for Linear Systems")]:
        counts = decks.get(ch, [])
        topics.append('                  <div class="topic-item">\n                    <span class="topic-num">0x%02d</span\n'
                      '                    ><span class="topic-name">%s</span\n                    ><span class="topic-meta">%d SLIDES</span>\n'
                      '                  </div>' % (ch if ch else 7, esc(name), sum(counts)))
    topics.append('                  <div class="topic-item exam-total">\n                    <span class="topic-num">&Sigma;</span\n'
                  '                    ><span class="topic-name" data-ar-text="مجموع الشرائح">Total Slides</span\n'
                  '                    ><span class="topic-meta">%d SLIDES</span>\n                  </div>' % total)
    content = """<header class="course-header">
                <div class="course-code-wrapper-big">
                  <h1 class="course-code-big">{code}</h1>
                  <span class="tag-available">AVAILABLE</span>
                </div>
                <h2 class="course-name">{name}</h2>
                <p class="course-desc-brief">
                  Linear systems and matrices from a computational point of view: elimination, factorizations,
                  determinants, vector spaces, eigenvalues and orthogonality, with interactive past exams.
                </p>
              </header>
              {subnav}
              <div class="content-section">
                <div class="grid-data-blocks">
                  <div class="data-block">
                    <span class="data-block-label">Course Code</span>
                    <span class="data-block-val">{code}</span>
                  </div>
                  <div class="data-block">
                    <span class="data-block-label">Interactive Exams</span>
                    <span class="data-block-val">{nexams}</span>
                  </div>
                  <div class="data-block">
                    <span class="data-block-label">Prerequisite</span>
                    <span class="data-block-val" style="font-family: var(--font-mono); font-size: 1.1rem; padding-top: 6px">MATH113</span>
                  </div>
                </div>
                <div class="section-label" id="section-description">01_DESCRIPTION</div>
                <div class="text-block">
                  <p>
                    {code} covers linear equations in linear algebra, matrix algebra and LU factorization, determinants,
                    vector spaces, eigenvalues and eigenvectors, and orthogonality with least squares, plus iterative methods
                    for solving linear systems. The course follows Lay's <em>Linear Algebra and Its Applications</em>.
                  </p>
                  <p>
                    The Exams tab holds re-typeset past quizzes, majors and finals. Every part can be checked as you go
                    and opens a step-by-step worked solution.
                  </p>
                </div>
                <div class="section-label" id="section-syllabus-index">02_COURSE_CONTENT // {ndecks}_DECKS // {total}_SLIDES</div>
                <div class="topics-list" style="margin-bottom: 48px">
{topics}
                </div>
              </div>
            </article>""".format(code=CODE, name=NAME, nexams=len(exams), ndecks=len(DECKS), total=total, topics="\n".join(topics),
                                 subnav=re.search(r'<nav class="sub-nav">.*?</nav>', text, re.S).group(0))
    text = re.sub(r'<header class="course-header">.*?</article>', lambda m: content, text, count=1, flags=re.S)
    # Credit hours and prerequisite as listed in the SE academic plan (academic-plan-themes).
    text = re.sub(r'(<span class="meta-key">PREREQUISITE</span>\s*<span class="meta-val">)NOT LISTED(</span>)', r"\g<1>MATH113\g<2>", text)
    links = "".join('<a href="%s%s" class="quick-link-btn">%s</a>' % (BASE, suffix, label) for suffix, label in TABS)
    text = re.sub(r'<div class="quick-links">.*?</div>', '<div class="quick-links">%s</div>' % links, text, count=1, flags=re.S)
    write(os.path.join(OUT, "index.html"), text)


def update_sidebar(slides, exams, study):
    with open(SIDEBAR_FILE, encoding="utf-8") as fh:
        data = json.load(fh)

    def visit(nodes):
        for node in nodes:
            if node.get("id") == "tree-math":
                kids = node["children"]
                if not any(c.get("url") == BASE for c in kids):
                    at = next(i for i, c in enumerate(kids) if c.get("url") == "/academics/math/math221/") + 1
                    kids.insert(at, {"type": "course", "url": BASE, "label": CODE})
            if isinstance(node.get("children"), list):
                visit(node["children"])
    visit(data["tree"])

    sections = json.loads(course_swap(json.dumps(data["sections"]["/academics/math/math221/"], ensure_ascii=False)))
    for s in sections:
        if s["url"].endswith("/exams/"):
            s["label"] = "EXAMS"
    data["sections"][BASE] = sections
    data["children"][BASE + "slides/"] = [{"url": u, "attrs": "", "label": l} for u, l in slides]
    data["children"][BASE + "exams/"] = [{"url": u, "attrs": "", "label": l} for u, l in exams]
    study_items = data["children"].get(BASE + "extra-resources/", [])
    worksheets = [i for i in study_items if i["url"].startswith(BASE + "extra-resources/worksheets/")]
    data["children"][BASE + "extra-resources/"] = worksheets + [{"url": u, "attrs": "", "label": l} for u, l in study]
    text = json.dumps(data, ensure_ascii=False, indent=2) + "\n"
    if read(SIDEBAR_FILE) != text:
        with open(SIDEBAR_FILE, "w", encoding="utf-8") as fh:
            fh.write(text)
        print("wrote scripts/academic-sidebar.json")


def flush():
    """Stamp the sidebar into every queued page (the clones carry MATH221's) and write it.

    Only this course's pages are touched; other pages get the CS223 entry from
    build_academic_sidebar.py.
    """
    import build_academic_sidebar as sidebar
    data = sidebar.load_data()
    for path, text in PENDING.items():
        match = sidebar.NAV_RE.search(text)
        if match and path.endswith("index.html"):
            url = "/" + os.path.relpath(os.path.dirname(path), DOCS).replace(os.sep, "/") + "/"
            text = text[:match.start()] + sidebar.render_nav(data, url) + text[match.end():]
        save(path, text)
    PENDING.clear()


def main():
    exams = build_exams()
    slides = build_slides()
    study = build_study()
    build_breakdowns()
    build_overview(exams)
    update_sidebar(slides, exams, study)
    flush()


if __name__ == "__main__":
    main()
