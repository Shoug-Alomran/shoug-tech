#!/usr/bin/env python3
"""Build the CYS401 past-paper replicas (exams 12-16).

Each paper is transcribed from photos of the printed exam (or, for Sem 181,
the instructor's answer PDF) and laid out like the original sheet: the PSU
header, the bordered question frames, the mark brackets, the page numbers.
The pages are interactive through docs/javascripts/cys401-past-paper.js and
styled by docs/styles/cys401-past-paper.css.

Answers to every cipher question are computed here, not typed, so a typo in
the key or text can't produce a wrong model answer.

    python3 scripts/build_cys401_past_papers.py
"""
from __future__ import annotations

import html
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
EXAMS = ROOT / "docs/academics/cybersecurity/cys401/exams"
SITE = "https://shoug-tech.com"
A = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

esc = html.escape


# ---------------------------------------------------------------- ciphers
def pf_matrix(key: str) -> list[list[str]]:
    seen: list[str] = []
    for c in (key.upper() + A):
        c = "I" if c == "J" else c
        if c.isalpha() and c not in seen:
            seen.append(c)
    return [seen[i * 5 : i * 5 + 5] for i in range(5)]


def pf_pairs(text: str) -> list[str]:
    t = ["I" if c == "J" else c for c in text.upper() if c.isalpha()]
    out, i = [], 0
    while i < len(t):
        a = t[i]
        b = t[i + 1] if i + 1 < len(t) else "X"
        if a == b:
            out.append(a + "X")
            i += 1
        else:
            out.append(a + b)
            i += 2
    return out


def pf_apply(m, pairs, decrypt=False):
    def pos(c):
        for r in range(5):
            if c in m[r]:
                return r, m[r].index(c)
        raise ValueError(c)

    s = -1 if decrypt else 1
    res = []
    for p in pairs:
        (r1, c1), (r2, c2) = pos(p[0]), pos(p[1])
        if r1 == r2:
            res.append(m[r1][(c1 + s) % 5] + m[r2][(c2 + s) % 5])
        elif c1 == c2:
            res.append(m[(r1 + s) % 5][c1] + m[(r2 + s) % 5][c2])
        else:
            res.append(m[r1][c2] + m[r2][c1])
    return res


def vigenere(text, key, decrypt=False):
    s = -1 if decrypt else 1
    return "".join(
        A[(A.index(c) + s * A.index(key[i % len(key)])) % 26] for i, c in enumerate(text)
    )


def hill_rows(text, k):
    v = [A.index(c) for c in text]
    out = []
    for i in range(0, len(v), 2):
        a, b = v[i], v[i + 1]
        x = a * k[0][0] + b * k[1][0]
        y = a * k[0][1] + b * k[1][1]
        out.append(((a, b), (x, y), (x % 26, y % 26)))
    return out


def caesar(text, k):
    return "".join(A[(A.index(c) + k) % 26] for c in text)


def columnar(text, key):
    width = len(key)
    rows = [text[i : i + width] for i in range(0, len(text), width)]
    return "".join(
        "".join(r[key.index(n)] for r in rows if key.index(n) < len(r))
        for n in range(1, width + 1)
    )


# ---------------------------------------------------------------- page shell
THEME_BOOT = """    <script>
      /* html-theme-sync.js resolves stored preference, then the OS. Inside the
         wrapper iframe, with nothing stored, follow the embedding page instead:
         it only marks itself when light, so an unmarked parent means dark.
         Persist it so the shared script picks it up and its toggle works. */
      (function () {
        try {
          var saved = localStorage.getItem("shoug-theme") || localStorage.getItem("theme");
          if (saved === "dark" || saved === "light") return;
          if (!window.parent || window.parent === window) return;
          var body = window.parent.document.body;
          if (!body) return;
          var mode = body.classList.contains("shoug-light-mode") ? "light" : "dark";
          localStorage.setItem("shoug-theme", mode);
          localStorage.setItem("theme", mode);
        } catch (e) {}
      })();
    </script>
"""


def shell(slug, title, desc, term_chip, intro_html, sheets_html):
    url = f"{SITE}/academics/cybersecurity/cys401/exams/{slug}/"
    t, d = esc(title), esc(desc)
    return f"""<!doctype html>
<html lang="en" data-sg-styled>
  <head>
    <link rel="icon" type="image/png" sizes="256x256" href="/assets/shoug-favicon-v4.png" />
    <link rel="shortcut icon" type="image/png" href="/assets/shoug-favicon-v4.png" />
    <link rel="apple-touch-icon" sizes="180x180" href="/assets/shoug-apple-touch-icon-v4.png" />
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>{t}</title>
    <meta name="description" content="{d}" />
    <link rel="canonical" href="{url}" />
    <meta property="og:title" content="{t}" />
    <meta property="og:description" content="{d}" />
    <meta property="og:url" content="{url}" />
    <meta property="og:type" content="article" />
    <meta property="og:image" content="{SITE}/assets/og-banner.png" />
    <meta name="twitter:card" content="summary_large_image" />
    <link rel="preconnect" href="https://fonts.googleapis.com" />
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
    <link
      href="https://fonts.googleapis.com/css2?family=Tinos:ital,wght@0,400;0,700;1,400&family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;600&display=swap"
      rel="stylesheet"
    />
{THEME_BOOT}    <script src="/javascripts/html-theme-sync.js"></script>
    <link rel="stylesheet" href="/styles/cys401-past-paper.css" />
    <script src="/javascripts/cys401-past-paper.js" defer></script>
  </head>
  <body>
    <header class="pp-bar">
      <div class="pp-bar-row">
        <a class="pp-brand" href="#top">CYS401 past paper</a>
        <span class="pp-chip term">{esc(term_chip)}</span>
        <span class="pp-score" id="pp-score" aria-live="polite"></span>
        <div class="pp-actions">
          <div data-page-search-host></div>
          <button class="pp-btn primary" type="button" id="pp-check">Check<span class="long"> paper</span></button>
          <button class="pp-btn" type="button" id="pp-reveal" aria-pressed="false" data-short="Answers">Show model answers</button>
          <button class="pp-btn" type="button" id="pp-reset">Reset</button>
          <button class="pp-btn" type="button" onclick="toggleTheme()"><span data-theme-label>Dark</span></button>
        </div>
      </div>
    </header>
    <main class="desk" id="top">
      <section class="pp-intro">
{intro_html}
      </section>
{sheets_html}
    </main>
  </body>
</html>
"""


def intro(title, lines):
    items = "".join(f"<li>{x}</li>" for x in lines)
    return (
        f"        <h1>{esc(title)}</h1>\n"
        f"        <ul>{items}</ul>"
    )


PSU_HEAD = """<div class="psu-head">
  <div class="psu-en"><div class="uni">Prince Sultan University</div><div class="col">College of Computer and Information Sciences</div></div>
  <div class="psu-logo" aria-hidden="true">جامعة الأمير سلطان<span class="big">PRINCE SULTAN</span>UNIVERSITY</div>
  <div class="psu-ar" lang="ar">جامعة الأمير سلطان<br />كلية علوم الحاسب ونظم المعلومات</div>
</div>"""


def psu_page(n, total, body, foot_extra=""):
    return (
        f'<article class="sheet" aria-label="Page {n} of {total}">{PSU_HEAD}'
        f'<div class="frame">{body}</div>{foot_extra}'
        f'<div class="page-foot">Page {n} of {total}</div></article>'
    )


def missing(n, total, what):
    return (
        f'<article class="sheet missing" aria-label="Page {n} of {total}">'
        f"<b>Page {n} of {total} was not photographed</b>{what}</article>"
    )


def qhead(no, total, first=False):
    style = "" if first else ' style="border-top:1.5px solid var(--rule);padding-top:8px;margin-top:10px"'
    return (
        f'<div class="qhead"{style}><span>Question No.{no}:</span>'
        f'<span class="marks">[ <span class="got" data-q="{no}"></span> /{total} Marks]</span></div>'
    )


# ---------------------------------------------------------------- question helpers
_n = {"i": 0}


def uid(prefix="f"):
    _n["i"] += 1
    return f"{prefix}{_n['i']}"


def opts_html(options, answer, marks, style="paren", two_col=False):
    name = uid("r")
    labs = []
    for i, text in enumerate(options):
        letter = "abcd"[i]
        tag = f"{letter})" if style == "paren" else f"{letter}."
        labs.append(
            f'<label class="opt"><input type="radio" name="{name}" value="{letter}" />'
            f'<span class="ol">{tag}</span><span>{text}</span></label>'
        )
    cls = "opts two-col" if two_col else "opts"
    return (
        f'<div class="{cls}" data-unit="radio" data-marks="{marks}" data-answer="{answer}">'
        + "".join(labs)
        + "</div>",
        name,
    )


def mcq(num, text, options, answer, why, marks=0.5, qno="1", style="paren", two_col=False):
    o, name = opts_html(options, answer, marks, style, two_col)
    return (
        f'<div class="q" data-qno="{qno}"><div class="q-row"><span class="n">{num}.</span>'
        f'<div><p class="q-text">{text}</p>{o}</div></div><div class="why">{why}</div></div>'
    ), name


def sel(options, answer, marks, label="Answer", cls="blank"):
    opts = '<option value="">choose…</option>' + "".join(
        f'<option value="{esc(o)}">{esc(o)}</option>' for o in options
    )
    return (
        f'<select class="{cls}" data-unit="select" data-marks="{marks}" '
        f'data-answer="{esc(answer)}" aria-label="{esc(label)}">{opts}</select>'
    )


def txt(accept, marks, label="Answer", show=None, pattern=None, wide=False, ph=""):
    attrs = f'data-accept="{esc(accept)}"' if pattern is None else f'data-pattern="{esc(pattern)}"'
    s = f' data-show="{esc(show)}"' if show else ""
    w = " wide" if wide else ""
    return (
        f'<input class="line-in{w}" type="text" autocomplete="off" spellcheck="false" '
        f'data-unit="text" data-marks="{marks}" {attrs}{s} aria-label="{esc(label)}" placeholder="{esc(ph)}" />'
    )


def num(answer, marks, label="Answer", show=None):
    s = f' data-show="{esc(show)}"' if show else ""
    return (
        f'<input class="line-in" type="text" inputmode="decimal" autocomplete="off" '
        f'data-unit="num" data-marks="{marks}" data-answer="{answer}"{s} aria-label="{esc(label)}" />'
    )


def written(marks, model, lines=3, label="Your answer", inner=None, cls="ruled"):
    area = inner if inner is not None else (
        f'<textarea class="{cls}" rows="{lines}" aria-label="{esc(label)}" '
        f'style="min-height:{max(lines, 2) * 30}px"></textarea>'
    )
    return (
        f'<div class="written" data-unit="written" data-marks="{marks}">{area}'
        f'<div class="model"><span class="tag">Model answer · {marks} marks</span>{model}</div></div>'
    )


def q(inner, qno, why=None):
    w = f'<div class="why">{why}</div>' if why else ""
    return f'<div class="q" data-qno="{qno}">{inner}{w}</div>'


# ---------------------------------------------------------------- figures
def cbc_svg():
    parts = ['<svg viewBox="0 0 760 140" role="img" aria-label="CBC mode: encryption and decryption chains of four blocks" style="max-width:760px">']
    parts.append('<g fill="none" stroke="currentColor" stroke-width="1.4">')
    t = []
    for g, x0, dec in ((0, 60, False), (1, 440, True)):
        t.append(f'<text class="lbl" x="{x0 + 110}" y="12" text-anchor="middle">{"Decryption:" if dec else "Encryption"}</text>')
        t.append(f'<text class="lbl" x="{x0 - 34}" y="54">V</text>')
        parts.append(f'<path d="M{x0 - 24} 50 H{x0 - 7}"/>')
        for i in range(4):
            cx = x0 + i * 80
            parts.append(f'<circle cx="{cx}" cy="50" r="7"/><path d="M{cx - 7} 50 H{cx + 7} M{cx} 43 V57"/>')
            parts.append(f'<rect x="{cx - 15}" y="66" width="30" height="22" fill="currentColor" fill-opacity="0.85"/>')
            t.append(f'<text x="{cx}" y="81" text-anchor="middle" style="font:11px var(--serif);fill:var(--paper)">{"D" if dec else "E"}ₖ</text>')
            if not dec:
                t.append(f'<text class="lbl" x="{cx}" y="27" text-anchor="middle">P[{i}]</text>')
                parts.append(f'<path d="M{cx} 31 V43 M{cx} 57 V66 M{cx} 88 V110"/>')
                t.append(f'<text class="lbl" x="{cx}" y="124" text-anchor="middle">C[{i}]</text>')
                if i < 3:
                    parts.append(f'<path d="M{cx} 100 H{cx + 40} V50 H{cx + 73}"/>')
            else:
                t.append(f'<text class="lbl" x="{cx}" y="27" text-anchor="middle">P[{i}]</text>')
                parts.append(f'<path d="M{cx} 43 V31 M{cx} 66 V57 M{cx} 110 V88"/>')
                t.append(f'<text class="lbl" x="{cx}" y="124" text-anchor="middle">C[{i}]</text>')
                if i < 3:
                    parts.append(f'<path d="M{cx} 100 H{cx + 40} V50 H{cx + 73}"/>')
    parts.append("</g>")
    parts.extend(t)
    parts.append("</svg>")
    return '<div class="fig">' + "".join(parts) + "</div>"


def mode_svg(kind):
    """Three-block sketch of a block-cipher mode, in the style of the paper."""
    g = ['<svg viewBox="0 0 345 118" aria-hidden="true"><g fill="none" stroke="currentColor" stroke-width="1.1">']
    tx = []

    def box(x, y, label="block cipher"):
        g.append(f'<rect x="{x}" y="{y}" width="62" height="20"/>')
        tx.append(f'<text x="{x + 31}" y="{y + 13.5}" text-anchor="middle" style="font:8.5px var(--serif);fill:currentColor">{label}</text>')
        tx.append(f'<text x="{x - 21}" y="{y + 13.5}" style="font:8px var(--serif);fill:currentColor">key</text>')
        g.append(f'<path d="M{x - 7} {y + 10} H{x}"/>')

    def xor(cx, cy):
        g.append(f'<circle cx="{cx}" cy="{cy}" r="5"/><path d="M{cx - 5} {cy} H{cx + 5} M{cx} {cy - 5} V{cy + 5}"/>')

    def lab(x, y, s, anchor="middle"):
        tx.append(f'<text x="{x}" y="{y}" text-anchor="{anchor}" style="font:8px var(--serif);fill:currentColor">{s}</text>')

    for i in range(3):
        x = 8 + i * 113
        bx, cx = x + 30, x + 61
        if kind == "ecb":
            lab(cx, 10, "plaintext")
            g.append(f'<path d="M{cx} 14 V30"/>')
            box(bx, 30)
            g.append(f'<path d="M{cx} 50 V86"/>')
            lab(cx, 98, "ciphertext")
        elif kind == "cbc":
            lab(cx, 10, "plaintext")
            g.append(f'<path d="M{cx} 14 V25"/>')
            xor(cx, 30)
            g.append(f'<path d="M{cx} 35 V44"/>')
            box(bx, 44)
            g.append(f'<path d="M{cx} 64 V90"/>')
            lab(cx, 102, "ciphertext")
            if i < 2:
                g.append(f'<path d="M{cx} 80 H{cx + 50} V30 H{cx + 108}"/>')
            else:
                pass
            if i == 0:
                lab(x + 6, 33, "IV", "start")
                g.append(f'<path d="M{x + 18} 30 H{cx - 5}"/>')
        elif kind == "cfb":
            box(bx, 18)
            g.append(f'<path d="M{cx} 38 V55"/>')
            xor(cx, 60)
            lab(x + 2, 63, "plaintext", "start")
            g.append(f'<path d="M{x + 36} 60 H{cx - 5}"/>')
            g.append(f'<path d="M{cx} 65 V90"/>')
            lab(cx, 102, "ciphertext")
            if i == 0:
                lab(cx, 9, "IV")
                g.append(f'<path d="M{cx} 11 V18"/>')
            if i < 2:
                g.append(f'<path d="M{cx} 80 H{cx + 48} V8 H{cx + 113} V18"/>')
        elif kind == "ctr":
            lab(cx, 9, f"Nonce, c{'+' + str(i) if i else ''}")
            g.append(f'<path d="M{cx} 12 V18"/>')
            box(bx, 18)
            g.append(f'<path d="M{cx} 38 V55"/>')
            xor(cx, 60)
            lab(x + 2, 63, "plaintext", "start")
            g.append(f'<path d="M{x + 36} 60 H{cx - 5}"/>')
            g.append(f'<path d="M{cx} 65 V90"/>')
            lab(cx, 102, "ciphertext")
    g.append("</g>")
    return "".join(g) + "".join(tx) + "</svg>"


def tableau(header_note=False):
    head = "".join(f"<th>{c}</th>" for c in A)
    rows = []
    for r in range(26):
        cells = "".join(f"<td>{A[(r + c) % 26]}</td>" for c in range(26))
        rows.append(f"<tr><th>{A[r]}</th>{cells}</tr>")
    cap = (
        '<caption style="font:12px var(--serif);caption-side:top">Plaintext across, key down</caption>'
        if header_note
        else ""
    )
    return f'<table class="tableau" aria-label="Vigenère table">{cap}<tr><th></th>{head}</tr>{"".join(rows)}</table>'


def matrix_static(m):
    rows = "".join("<tr>" + "".join(f"<td>{'I/J' if c == 'I' else c}</td>" for c in r) + "</tr>" for r in m)
    return f'<table class="matrix5" aria-label="Key matrix">{rows}</table>'


def matrix_input(answer_rows, marks, label):
    ans = "".join("".join(r) for r in answer_rows)
    cells = "".join(
        "<tr>" + "".join(f'<td><input maxlength="3" aria-label="{label} row {r + 1} column {c + 1}" /></td>' for c in range(5)) + "</tr>"
        for r in range(5)
    )
    return f'<table class="matrix5" data-unit="matrix" data-marks="{marks}" data-answer="{ans}">{cells}</table>'


def alpha_strip(upper=True, labels=("", "")):
    letters = A if upper else A.lower()
    th = f"<th>{labels[0]}</th>" if labels[0] else ""
    td = f"<th>{labels[1]}</th>" if labels[1] else ""
    return (
        '<table class="alpha" aria-label="Letter values"><tr>' + th
        + "".join(f"<td>{c}</td>" for c in letters)
        + "</tr><tr>" + td
        + "".join(f"<td>{i}</td>" for i in range(26))
        + "</tr></table>"
    )


def mat(rows):
    cols = list(zip(*rows))
    inner = "".join("<span style='display:grid;gap:2px'>" + "".join(f"<span>{v}</span>" for v in col) + "</span>" for col in cols)
    return f'<span class="mat">{inner}</span>'


def mccumber(marks_each):
    terms = sorted(["Confidentiality", "Integrity", "Availability", "Processing", "Transmission", "Storage", "Technology", "Education", "Policy"])
    titles = ["Security goals", "Information states", "Security measures"]
    sets = {
        "Security goals": ["Confidentiality", "Integrity", "Availability"],
        "Information states": ["Processing", "Storage", "Transmission"],
        "Security measures": ["Technology", "Policy", "Education"],
    }

    def s(cls, options, label):
        o = '<option value="">…</option>' + "".join(f'<option value="{x}">{x}</option>' for x in options)
        return f'<select class="blank {cls}" aria-label="{label}">{o}</select>'

    def slot(x, y, w, inner):
        return f'<div class="mc-slot" style="--x:{x}%;--y:{y}%;--w:{w}%">{inner}</div>'

    axes = [
        ("1 · vertical axis", (1, 2, 27), [(1, 33, 27), (1, 45, 27), (1, 57, 27)]),
        ("2 · diagonal axis", (66, 3, 31), [(34, 20, 20), (34, 32, 20), (34, 44, 20)]),
        ("3 · horizontal axis", (71, 68, 28), [(31, 88, 21), (54, 88, 21), (77, 88, 21)]),
    ]
    blocks = []
    for name, tpos, ipos in axes:
        inner = f'<span class="mc-list-label">Axis {name}</span>'
        inner += slot(*tpos, s("title", titles, f"Axis {name}: dimension"))
        for k, p in enumerate(ipos):
            inner += slot(*p, s("item", terms, f"Axis {name}: label {k + 1}"))
        blocks.append(f'<div data-unit="axis" data-marks="{marks_each}" style="display:contents">{inner}</div>')
    svg = (
        '<svg viewBox="0 0 560 400" aria-hidden="true"><g fill="none" stroke="currentColor" stroke-width="2.2">'
        '<path d="M175 330 V40 M175 330 H540 M175 330 L450 70"/>'
        '<path d="M168 52 L175 38 L182 52 M528 323 L542 330 L528 337 M436 74 L452 68 L446 84"/></g>'
        '<g style="font:600 15px var(--sans);fill:currentColor"><text x="183" y="56">1</text><text x="520" y="318">3</text><text x="430" y="100">2</text></g></svg>'
    )
    return (
        f'<div class="mc" data-sets=\'{json.dumps(sets)}\'><div class="mc-stage">{svg}'
        f'<div class="mc-slots">{"".join(blocks)}</div></div></div>'
    )


def sdlc_svg():
    boxes = [
        ("Requirements", "Analysis", 70, 52, False),
        ("System Design", "", 135, 96, True),
        ("Implementation", "", 200, 140, False),
        ("Integration and", "Deployment", 265, 184, False),
        ("Operation and", "Maintenance", 400, 246, True),
    ]
    g = ['<svg viewBox="0 0 560 300" role="img" aria-label="SDLC waterfall: requirements analysis, system design, implementation, integration and deployment, operation and maintenance; system design and operation and maintenance are highlighted" style="max-width:600px">']
    g.append('<g fill="none" stroke="currentColor" stroke-width="1.3">')
    g.append('<circle cx="34" cy="22" r="9"/><path d="M34 31 V52 M22 40 H46 M34 52 L24 66 M34 52 L44 66"/>')
    t = ['<text class="lbl" x="52" y="20">User</text>']
    for i, (a, b, x, y, hl) in enumerate(boxes):
        w = 120
        sw = ' stroke-width="2.6" style="stroke:var(--accent)"' if hl else ""
        g.append(f'<rect x="{x}" y="{y}" width="{w}" height="30" fill="currentColor" fill-opacity="0.08"{sw}/>')
        if b:
            t.append(f'<text class="lbl" x="{x + w / 2}" y="{y + 13}" text-anchor="middle">{a}</text><text class="lbl" x="{x + w / 2}" y="{y + 25}" text-anchor="middle">{b}</text>')
        else:
            t.append(f'<text class="lbl" x="{x + w / 2}" y="{y + 19}" text-anchor="middle">{a}</text>')
        if i < 3:
            nx, ny = boxes[i + 1][2], boxes[i + 1][3]
            g.append(f'<path d="M{x + w} {y + 15} H{nx + 40} V{ny}"/><path d="M{nx + 36} {ny - 7} L{nx + 40} {ny} L{nx + 44} {ny - 7}"/>')
    # Integration and Deployment -> Product -> Operation and Maintenance
    g.append('<path d="M46 34 Q60 40 70 60"/>')
    g.append('<path d="M385 199 H412"/><path d="M405 194 L412 199 L405 204"/>')
    g.append('<path d="M412 188 L424 180 H450 V206 L438 214 H412 Z M412 188 H438 V214 M438 188 L450 180" fill="currentColor" fill-opacity="0.12"/>')
    t.append('<text class="lbl" x="431" y="174" text-anchor="middle">Product</text>')
    g.append('<path d="M450 197 H476 V246"/><path d="M471 239 L476 246 L481 239"/>')
    g.append('<path d="M400 266 C240 280 80 220 40 70"/><path d="M34 80 L40 68 L46 80"/>')
    g.append("</g>")
    return '<div class="fig">' + "".join(g) + "".join(t) + "</svg></div>"


def did_svg():
    g = ['<svg viewBox="0 0 540 270" role="img" aria-label="Defense in depth: a user outside nested layers perimeter, network, client and server, each with application and data" style="max-width:600px">']
    g.append('<g fill="none" stroke="currentColor" stroke-width="1.4">')
    g.append('<circle cx="34" cy="96" r="10"/><path d="M34 106 V140 M18 118 H50 M34 140 L22 162 M34 140 L46 162"/>')
    g.append('<rect x="92" y="8" width="430" height="252" fill="currentColor" fill-opacity="0.04"/><rect x="112" y="40" width="390" height="208"/>')
    g.append('<rect x="128" y="66" width="164" height="150" fill="currentColor" fill-opacity="0.05"/><rect x="320" y="66" width="164" height="150" fill="currentColor" fill-opacity="0.05"/>')
    g.append('<ellipse cx="210" cy="150" rx="62" ry="50"/><ellipse cx="402" cy="150" rx="62" ry="50"/>')
    g.append('<rect x="188" y="160" width="44" height="24"/><rect x="380" y="160" width="44" height="24"/>')
    g.append('<rect x="128" y="224" width="164" height="14" fill="currentColor" fill-opacity="0.15"/>')
    g.append('<path stroke-dasharray="5 4" d="M52 102 H92 M52 114 H112 M52 126 H128 M52 138 H150 M52 150 H190"/>')
    g.append('<path d="M228 196 V210 H372 V196" stroke-width="1"/>')
    g.append("</g>")
    t = [
        '<text class="lbl" x="307" y="28" text-anchor="middle">Perimeter</text>',
        '<text class="lbl" x="307" y="58" text-anchor="middle">Network</text>',
        '<text class="lbl" x="210" y="84" text-anchor="middle">Client</text>',
        '<text class="lbl" x="402" y="84" text-anchor="middle">Server</text>',
        '<text class="lbl" x="210" y="136" text-anchor="middle">Application</text>',
        '<text class="lbl" x="402" y="136" text-anchor="middle">Application</text>',
        '<text class="lbl" x="210" y="176" text-anchor="middle">Data</text>',
        '<text class="lbl" x="402" y="176" text-anchor="middle">Data</text>',
    ]
    return '<div class="fig">' + "".join(g) + "".join(t) + "</svg></div>"


# ---------------------------------------------------------------- shared answers
STRIDE_ROWS = [
    ("Spoofing", "Authentication", "Fabrication"),
    ("Tampering", "Integrity", "Modification"),
    ("Repudiation", "Non-repudiation", "Fabrication (Modification also accepted)"),
    ("Information disclosure", "Confidentiality", "Interception"),
    ("Denial of service", "Availability", "Interruption"),
    ("Elevation of privilege", "Authorization", "Modification"),
]
CATS = ["Interruption", "Interception", "Modification", "Fabrication"]

CAT_NOTE = (
    "The four threat categories each attack one property: interruption → availability, "
    "interception → confidentiality, modification → integrity, fabrication → authenticity. "
    "Map each STRIDE threat through the property it violates. Repudiation (forging or denying "
    "a record) is marked as fabrication or modification; elevation of privilege as "
    "modification, as on the marked paper."
)


def cat_table():
    return (
        '<table class="ptable center" style="width:auto;margin:8px auto">'
        + "".join(f"<tr><td>{c}</td></tr>" for c in CATS)
        + "</table>"
    )


# ================================================================= PAPER: Quiz 1, 232
def paper_232():
    _n["i"] = 0
    qn = "all"
    p1 = []
    p1.append(
        '<div class="quiz-top"><span>Instructor: Dr. Rabia Latif</span><span>Date: 1 February 2024</span></div>'
        '<div class="quiz-meta"><div class="quiz-title">CYS401- Fundamentals of Cybersecurity<br />'
        "Semester 232- Sec: 1242/1249<br /><u>Quiz 1</u></div>"
        '<div class="marks-box"><div>Marks</div><div><span class="got" data-q="all"></span>/5</div></div></div>'
        '<p>Student ID: ______________________ &nbsp;&nbsp; Name: ______________________</p>'
    )
    p1.append('<p class="part">Q1: Choose the best option: [0.5 Mark Each = 1 Marks]</p>')
    m, _ = mcq(
        1,
        "Which of the following is not a physical security measure to protect against physical hacking?",
        [
            "Create a phishing policy.",
            "Updating the patches in the software you're working on at your office laptop.",
            "Add front desk &amp; restrict unknown access to the back room.",
            "Analyze how employees maintain their physical data and data storage peripheral devices.",
        ],
        "b",
        "Patching software is a technical control; it does nothing against someone who walks up to the machine. "
        "A phishing policy (a) is also not physical (it is administrative), so the question has two defensible "
        "answers; (b) is keyed, matching the same question on the Semester 222 quiz.",
        qno=qn,
    )
    p1.append(m)
    m, _ = mcq(
        2,
        "What is a characteristic of a layered defense-in-depth security approach?",
        [
            "Three or more devices are used.",
            "Routers are replaced with firewalls.",
            "One safeguard failure does not affect the effectiveness of other safeguards.",
            "When one device fails, another one takes over.",
        ],
        "c",
        "Defense in depth stacks independent safeguards, so losing one leaves the others working. "
        "(d) describes fail-over redundancy, which protects availability, not layering.",
        qno=qn,
    )
    p1.append(m)
    p1.append('<p class="part">Q2: For each statement, choose the appropriate option from the given table. [1 Marks]</p>')
    p1.append('<table class="ptable terms" style="width:auto;margin:6px auto"><tr><td>Utility</td><td>Authentic</td></tr><tr><td>Integrity</td><td>Accuracy</td></tr></table>')
    terms = ["Utility", "Authentic", "Integrity", "Accuracy"]
    rows = [
        ("When the information is the same as it was originally created, placed, stored, or transferred, it is ", "Authentic", ".",
         "Authenticity is the quality of being genuine or original — unchanged since it was created, placed, stored or transferred."),
        ("If information contains a value different from the user's expectations due to intentional or unintentional modification of the content, it means no ", "Accuracy", ".",
         "Accuracy means free from errors and holding the value the user expects; modified content is no longer accurate."),
        ("If information is available, but not in the format meaningful to the end user, it means no ", "Utility", ".",
         "Utility is the quality of being useful for a purpose. Data that is present but unreadable to the user has no utility."),
        ("If an unauthorized user obtains an organization's procedure, this poses a threat to the ", "Integrity", " of the information.",
         "This is the answer the marked paper accepted for full marks."),
    ]
    for i, (a, ans, b, why) in enumerate(rows):
        p1.append(q(f'<div class="q-row"><span class="n">{"abcd"[i]})</span><p class="q-text">{a}{sel(terms, ans, 0.25, "Blank " + "abcd"[i])}{b}</p></div>', qn, why))
    p1.append('<p class="part">Q3: For the given McCumber Graph, label it with THREE different dimensions. [0.75 Marks]</p>')
    p1.append(q(mccumber(0.25), qn,
                "Each axis earns 0.25 when its dimension name and its three labels belong together. The cube's dimensions: "
                "<b>Security goals</b> (confidentiality, integrity, availability), <b>Information states</b> "
                "(processing, storage, transmission) and <b>Security measures</b> (technology, policy, education)."))

    p2 = []
    p2.append('<p class="part">Q4: For the given SDLC phases, write any TWO points for each phase to make it SecSDLC. [1 Marks]</p>')
    p2.append(sdlc_svg())
    p2.append(
        '<div class="dd-grid">'
        + '<div class="answer-box"><div class="lab">System Design</div>'
        + written(0.5, "<ul><li>Security planning and secure architecture design</li><li>Threat modelling and risk assessment of the design</li><li>Define security functional and assurance requirements</li><li>Design review against security requirements (attack-surface analysis)</li></ul>", 2, "System Design points")
        + "</div>"
        + '<div class="answer-box"><div class="lab">Operation and Maintenance</div>'
        + written(0.5, "<ul><li>Apply patches and security updates</li><li>Continuously monitor performance and logs with respect to security</li><li>Incident response and periodic vulnerability assessments / audits</li><li>Secure disposal of the system and its data at end of life</li></ul>", 2, "Operation and Maintenance points")
        + "</div></div>"
    )
    p2[-1] = q(p2[-1], qn)
    p2.append('<p class="part">Q5: You are working as a security analyst in Hitech security company. The company assigns you the task of implementing a defense-in-depth approach to protect it from various cyber-attacks. For the given scenario, suggest any <u>ONE</u> security control for the given layers (in figure) to protect the company from cyber-attacks. [0.25 marks each = 1.25 marks]</p>')
    p2.append(did_svg())
    layers = [
        ("Data", "Encryption at rest, or backup and restore"),
        ("Application", "Application hardening, input validation / secure coding"),
        ("Host (Client / Server)", "OS hardening, patching, or antivirus with updates"),
        ("Network", "Network segmentation, or IDS/IPS"),
        ("Perimeter", "Firewall, or VPN with quarantine for remote access"),
    ]
    rows_html = "".join(
        f'<tr><td><b>{name}</b></td><td>{written(0.25, model, 1, name + " control", cls="ruled short")}</td></tr>'
        for name, model in layers
    )
    p2.append(q(f'<table class="ptable stack table-stack-labels"><thead><tr><th>Layer</th><th>One security control</th></tr></thead><tbody>{rows_html}</tbody></table>', qn))
    p2.append('<div class="end-line">************************ END ************************</div>')

    sheets = (
        f'<article class="sheet" aria-label="Page 1 of 2">{"".join(p1)}</article>'
        f'<article class="sheet" aria-label="Page 2 of 2">{"".join(p2)}</article>'
    )
    return sheets


# ================================================================= PAPER: Major, Sem 181
def paper_181():
    _n["i"] = 0
    mc = [
        ("What is layer 4 of the <b>OSI model</b>?", ["Presentation", "Network", "Data Link", "Transport"], "d",
         "Counting up from the bottom: 1 Physical, 2 Data Link, 3 Network, 4 Transport, 5 Session, 6 Presentation, 7 Application."),
        ("What is a <b>TCP wrapper</b>?", ["An encapsulation protocol used by switches", "An application that can serve as a basic firewall by restricting access based on user IDs or system IDs", "A security protocol used to protect TCP/IP traffic over WAN links", "A mechanism to tunnel TCP/IP through non-IP networks"], "b",
         "A TCP wrapper sits in front of network services and allows or denies connections by user or system ID, which makes it a basic host firewall."),
        ("Which of the following is <b>NOT</b> true regarding firewalls?", ["They are able to log traffic information.", "They are able to block viruses.", "They are able to issue alarms based on suspected attacks.", "They are unable to prevent internal attacks."], "b",
         "Firewalls filter traffic by rules; they log, raise alarms and cannot stop insiders. Spotting viruses inside the content is antivirus work."),
        ("What is <b>encapsulation</b>?", ["Changing the source and destination addresses of a packet", "Adding a header and footer to data as it moves down the OSI stack", "Verifying a person’s identity", "Protecting evidence until it has been properly collected"], "b",
         "Each layer wraps the data from the layer above with its own header (and the data link layer a footer) on the way down."),
        ("Which one of the following devices is most susceptible to <b>TEMPEST</b> monitoring of its emanations?", ["Switch", "Monitor", "CD-ROM", "Router"], "b",
         "TEMPEST is about reading electromagnetic emanations. Monitors give off the strongest readable signal of these devices."),
        ("Which one of the following security modes does not require that all users have a <b>security clearance</b> for the highest level of information processed by the system?", ["Dedicated", "System high", "Compartmented", "Multilevel"], "d",
         "Dedicated, system-high and compartmented modes all require clearance for the highest level. Multilevel mode lets users with lower clearances work while the system enforces separation."),
        ("Which of the following is a problem with <b>symmetric key encryption</b>?", ["Is slower than asymmetric key encryption", "Most algorithms are kept proprietary", "Work factor is not a function of the key size", "Secure distribution of the secret key"], "d",
         "Both sides need the same secret, so getting it to them securely is the classic problem. Symmetric encryption is faster than asymmetric, not slower."),
        ("In <b>public key cryptography</b>", ["Only the private key can encrypt and only the public key can decrypt", "Only the public key can encrypt and only the private key can decrypt", "The public key used to encrypt and decrypt", "If the public key encrypts, then only the private key can decrypt"], "d",
         "The two keys are a pair: whatever one encrypts only the other decrypts. Both directions are used (encryption with the public key, signatures with the private key), so the 'only' in (a) and (b) is wrong."),
        ("In a block cipher, <b>diffusion</b>", ["Conceals the connection between the ciphertext and plaintext", "Spreads the influence of a plaintext character over many ciphertext characters", "Is usually implemented by nonlinear S-boxes", "Cannot be accomplished"], "b",
         "Diffusion spreads each plaintext bit over many ciphertext bits. Concealing the relationship (a) is confusion, which S-boxes (c) provide."),
        ("What is used to create a <b>digital signature</b>?", ["The receiver’s private key", "The sender’s public key", "The sender’s private key", "The receiver’s public key"], "c",
         "The sender encrypts the message digest with their own private key; anyone verifies it with the sender's public key."),
        ("Why would a certificate authority <b>revoke a certificate</b>?", ["If the user’s public key has become compromised", "If the user changed over to using the Project Execution Model (PEM) model that uses a web of trust", "If the user’s private key has become compromised", "If the user moved to a new location"], "c",
         "A compromised private key means someone else can sign as the user, so the CA puts the certificate on its revocation list. A public key is public by design."),
        ("Which of the following best describes a <b>certificate authority</b>?", ["An organization that issues private keys and the corresponding algorithms", "An organization that validates encryption processes", "An organization that verifies encryption keys", "An organization that issues certificates"], "d",
         "A CA is the trusted third party that issues certificates binding an identity to a public key."),
    ]
    tf = [
        ("<b>CROSS-SITE SCRIPTING (XSS)</b> is a form of malicious code-injection attack in which an attacker is able to compromise a web server.", "a",
         "Keyed TRUE on the instructor's answer sheet: XSS injects malicious script through a vulnerable web application."),
        ("<b>Defense in depth</b> is used to provide a protective multilayer barrier against various forms of attack.", "a", "Layered, independent controls are the definition of defense in depth."),
        ("<b>Wired Equivalent Privacy</b> (WEP) uses a predefined shared secret key.", "a", "WEP uses a static pre-shared key configured on the access point and every client."),
        ("In <b>Symmetric multiprocessing</b> (SMP) the processors are often operating independently of each other.", "b",
         "FALSE. In SMP the processors share the OS and memory and work together. The instructor cites the CISSP book (p. 495): it is <i>asymmetric</i> multiprocessing (AMP) where processors often operate independently."),
    ]
    names = {}
    pages = {1: [], 2: [], 3: [], 4: [], 5: []}
    pages[1].append(
        '<div class="doc-pageno">1</div><div class="doc-head"><div class="doc-logo">جامعة الأمير سلطان<br />PRINCE SULTAN<br />UNIVERSITY</div>'
        '<div class="doc-title">Major Sem 181</div></div>'
        '<div class="doc-info"><div>Course instructor: <u>Dr. Gabriela Mogos</u></div><div></div>'
        "<div>Course title: <u>Fundamentals of Cybersecurity</u></div><div>Course code: <u>CYS401</u></div>"
        "<div>Duration: &nbsp;70 minutes</div><div>Exam date: 18.11.2018</div>"
        "<div>Student Name:</div><div>ID:</div></div>"
        '<p style="text-align:right;font-weight:700;margin-top:22px">TOTAL MARKS: ( <span class="got" data-q="all"></span> /20)</p>'
        '<div class="doc-h">SECTION A. Multiple Choice Questions</div>'
        "<p><b><u>Note</u>: Answer all the questions and fill the TABLE at the end with appropriate answers.</b></p>"
        '<div class="doc-sub"><span>I. Choose the best answer/choice for the below statements:</span><span>( &nbsp; /1 marks)</span></div>'
    )
    for i, (text, opts, ans, why) in enumerate(mc, 1):
        m, name = mcq(i, text, opts, ans, why, marks=1, qno="A", style="dot")
        names[f"mc{i}"] = name
        pages[1 if i <= 3 else 2 if i <= 9 else 3].append(m)
    pages[2].insert(0, '<div class="doc-pageno">2</div>')
    pages[3].insert(0, '<div class="doc-pageno">3</div>')
    pages[3].append('<div class="doc-sub"><span>II. State whether these statements are True or False:</span><span>( &nbsp; /0,5 marks)</span></div>')
    for i, (text, ans, why) in enumerate(tf, 1):
        m, name = mcq(i, text, ["TRUE", "FALSE"], ans, why, marks=0.5, qno="A", style="dot")
        names[f"tf{i}"] = name
        pages[3].append(m)

    def cell(key):
        return f'<td class="mirror" data-mirror="{names[key]}"></td>' if key in names else "<td></td>"

    rows = ""
    for r in range(6):
        tfk = f"tf{r + 1}" if r < 4 else None
        rows += (
            f"<tr><td><b>{r + 1}</b></td>{cell(f'mc{r + 1}')}<td><b>{r + 7}</b></td>{cell(f'mc{r + 7}')}"
            + (f"<td><b>{r + 1}</b></td>{cell(tfk)}" if tfk else "<td></td><td></td>")
            + "</tr>"
        )
    pages[4].append(
        '<div class="doc-pageno">4</div>'
        '<table class="ptable answer-grid"><tr><th colspan="4">Multiple Choice Questions<br />( &nbsp; /1 marks)</th>'
        '<th colspan="2">TRUE/FALSE<br />( &nbsp; /0,5 marks)</th></tr>' + rows + "</table>"
        '<p style="font:13px var(--sans);color:var(--ink-2)">This table fills itself in from the options you pick above.</p>'
        '<div class="doc-h">SECTION B. ESSAY Questions</div>'
        "<p><b><u>Note</u>: Section B contains Three (3) questions. Answer all THREE (3) questions.</b></p>"
    )
    essays = [
        ("1. Shortly describe the Authoritative Name Server", " (definition and types).",
         "<p>An Authoritative Name Server holds the actual DNS records for a particular domain / address.</p>"
         "<p>There are two types of Authoritative Name Servers:</p><ul><li><b>Primary</b> authoritative name server hosts the original zone file for the domain.</li>"
         "<li><b>Secondary</b> authoritative name servers can be used to host read-only copies of the zone file.</li></ul>", 4),
        ("2. Shortly describe the Grid Computing.", "",
         "<ul><li>Grid computing is a form of <u>parallel distributed processing</u> that loosely groups <u>a significant number of processing nodes to work toward</u> a specific processing goal.</li>"
         "<li>The biggest security concern with grid computing is that the content of each work packet is potentially exposed to the world.</li>"
         "<li>Grid computing often uses a central primary core of servers to manage the project, track work packets, and integrate returned work segments.</li>"
         "<li>If the central servers are overloaded or go offline, complete failure or crashing of the grid can occur.</li></ul>", 5),
        ("3. Shortly describe the configuration modes of a Wireless access points WAP.", "",
         "<ul><li><u>Infrastructure mode</u> — wireless NICs on systems can’t interact directly, and the restrictions of the wireless access point for wireless network access are enforced.</li>"
         "<li><u>Ad hoc mode</u> — two wireless network interface cards (NICs) can communicate without a centralized control authority.</li></ul>", 4),
    ]
    for k, (head, tail, model, lines) in enumerate(essays):
        block = (
            f'<div class="doc-sub"><span>{head}<span style="font-weight:400">{tail}</span></span><span>( &nbsp; /2 marks)</span></div>'
            + written(2, model, lines, head)
        )
        pages[4 if k < 2 else 5].append(q(block, "B"))
    pages[5].insert(0, '<div class="doc-pageno">5</div>')
    return "".join(f'<article class="sheet doc" aria-label="Page {n}">{"".join(pages[n])}</article>' for n in range(1, 6))


# ================================================================= PAPER A (term unknown, 7 pages)
def paper_a():
    _n["i"] = 0
    T = 7
    # ---- page 2
    p = [qhead(1, 5, first=True), '<p class="part">A) Choose the Correct Option. [2.5 Marks]</p>']
    p.append(mcq(1, "To <u>Decrypt</u> the ciphertext (C) using Triple DES, where K1≠K2≠K3, which of the following could be used:",
                 ["Dec<sub>K3</sub>(Enc<sub>K2</sub>(Dec<sub>K1</sub>(C)))", "Enc<sub>K3</sub>(Dec<sub>K2</sub>(Enc<sub>K1</sub>(C)))",
                  "Dec<sub>K1</sub>(Enc<sub>K2</sub>(Dec<sub>K3</sub>(C)))", "Enc<sub>K1</sub>(Dec<sub>K2</sub>(Enc<sub>K3</sub>(C)))"],
                 "c", "Triple DES encrypts as C = E<sub>K3</sub>(D<sub>K2</sub>(E<sub>K1</sub>(P))). Decryption undoes the steps in reverse order with the inverse operation: decrypt with K3, encrypt with K2, decrypt with K1.")[0])
    pt = "GLOBALCYBERSECURITYFORUM"
    p.append(mcq(2, f'The following message is encrypted using Caesar Cipher, find its associated key assuming the space is replaced by the letter “X”.<br /><span style="display:inline-block;margin-left:5em">Plaintext &nbsp;= {pt}<br />Ciphertext = {caesar(pt, 10)}</span>',
                 ["K = 3", "K = 5", "K = 7", "K = 10"], "d",
                 f"G (6) → Q (16): shift 10. Check another pair: L (11) → V (21). Every letter moves 10 places, so K = 10.")[0])
    figs = "".join(
        f'<label class="fig-opt"><input type="radio" name="cfbmode" value="{k}" class="sr" style="position:absolute;opacity:0" />'
        f'<span class="ol" style="font-weight:700">{k.upper()}.</span>{mode_svg(kind)}</label>'
        for k, kind in (("a", "ecb"), ("b", "cbc"), ("c", "cfb"), ("d", "ctr"))
    )
    p.append(q(f'<div class="q-row"><span class="n">3.</span><div><p class="q-text">Which of the following is better representing the Cipher Feedback (CFB) Mode:</p>'
               f'<div class="fig-opts" data-unit="radio" data-marks="0.5" data-answer="c">{figs}</div></div></div>', "1",
               "C is CFB: the previous ciphertext block goes into the block cipher, and the cipher's output is XORed with the plaintext to give the ciphertext. "
               "A is ECB (each block alone), B is CBC (plaintext XORed with the previous ciphertext <i>before</i> the cipher), D is CTR (a nonce and counter are encrypted)."))
    p.append(mcq(4, "Which role is directly responsible for deciding who has access to information systems and with what privileges, according to NIST SP 800-18?",
                 ["Information Steward", "Asset Owner", "Information Custodian", "Data Owner"], "d",
                 "Under NIST SP 800-18 the data owner establishes the rules for use and protection and decides who has access and with what privileges. The custodian only implements those decisions.")[0])
    p.append(mcq(5, "Identify the term which denotes the protection of data from modification by unknown users.",
                 ["Confidentiality", "Integrity", "Authentication", "Non-repudiation"], "b",
                 "Integrity is protection against unauthorized modification. Confidentiality protects against disclosure.",
                 two_col=True)[0])
    pages = [missing(1, T, "The cover page (student details and instructions)."), psu_page(2, T, "".join(p))]

    # ---- page 3
    p = ['<p class="part boxed">B) Read carefully the following <u>wrong statements</u> and correct them. [2.5 Marks]</p>']
    wrong = [
        ("Secure SDLC means applying security to only requirement and implementation phases.",
         "Secure SDLC applies security in <b>all</b> phases: requirements, design, implementation, testing/integration, deployment and maintenance."),
        ("Security attackers are always external.", "Attackers can be <b>internal or external</b> (insiders such as employees and contractors are a major threat)."),
        ("Regarding the McCumber Cube, data needs to be protected only during transmission.",
         "Data must be protected in <b>all three states</b>: transmission, storage and processing."),
        ("Strategic plan is usually a short-term plan with too many details.", "A strategic plan is a <b>long-term</b>, high-level plan with <b>general direction, little detail</b> (tactical and operational plans hold the detail)."),
        ("The information assets within the same organization have the same risk value.",
         "Assets have <b>different</b> risk values, depending on their value, criticality and exposure."),
    ]
    for i, (stmt, model) in enumerate(wrong):
        p.append(q(f'<div class="q-row"><span class="n">{"abcde"[i]})</span><div><p class="q-text">{stmt}</p>{written(0.5, model, 1, "Correction " + "abcde"[i], cls="ruled short")}</div></div>', "1"))
    p.append(qhead(2, 9))
    p.append(q(
        '<p class="part" style="font-weight:400"><b>A)</b> A hospital IT administrator simply deletes patient records from its system but does not follow NIST SP 800-88r1 guidelines for sanitization. Later, attackers recover fragments of those records using a simple recovery tool. <u>Explain how data remanence occurred in this case.</u> <u>Suggest two methods of destroying data to prevent data remanence.</u> [1.5 marks]</p>'
        + written(1.5,
                  "<p><b>How:</b> deleting a file only removes its directory entry and marks the space as free. The bits stay on the media until they are overwritten, so this residual data (data remanence) can be read back with simple recovery tools.</p>"
                  "<p><b>Two methods</b> (any two): purging, e.g. degaussing or cryptographic erase; physical destruction (shredding, disintegration, incineration, pulverizing); clearing by overwriting the media before reuse.</p>", 4), "2"))
    p.append(
        '<p class="part" style="font-weight:400"><b>B)</b> <u>SmartHealth Cloud</u>, a cloud-based healthcare platform, stores sensitive patient medical records, including lab results, prescriptions, and diagnostic imaging. The platform also manages user authentication for doctors, nurses, and administrative staff through a centralized Identity and Access Management (IAM) system. During a routine security assessment, the cybersecurity team discovered that: Some patient data storage buckets were misconfigured and publicly accessible. The platform’s API endpoints for uploading and retrieving medical records were not rate-limited, allowing brute-force attacks. Certain staff members used weak passwords for accessing the IAM system. A malicious hacker or a ransomware attacker may exploit these weaknesses, they could access confidential patient records, alter medical data, or impersonate medical staff, potentially leading to data breaches, compromised patient care, and regulatory violations. <u>Based on this scenario, identify two Assets, two Threats, two Vulnerabilities.</u> [1.5 Marks] (0.25 for each point)</p>'
    )
    pages.append(psu_page(3, T, "".join(p)))

    # ---- page 4
    cell = lambda lab: f'<textarea class="ruled cell" rows="2" aria-label="{lab}"></textarea>'
    table = (
        '<table class="ptable stack table-stack-labels"><thead><tr><th>Asset</th><th>Threat</th><th>Vulnerability</th></tr></thead><tbody>'
        + "".join(f"<tr><td>{cell('Asset ' + str(r))}</td><td>{cell('Threat ' + str(r))}</td><td>{cell('Vulnerability ' + str(r))}</td></tr>" for r in (1, 2))
        + "</tbody></table>"
    )
    model = (
        '<table class="ptable"><tr><th>Assets</th><th>Threats</th><th>Vulnerabilities</th></tr>'
        "<tr><td>Patient medical records (lab results, prescriptions, imaging)</td><td>Malicious hacker / ransomware attacker; data breach</td><td>Misconfigured, publicly accessible storage buckets</td></tr>"
        "<tr><td>IAM system (or the API endpoints)</td><td>Brute-force attack; impersonation of medical staff; alteration of medical data</td><td>API endpoints not rate-limited; weak staff passwords</td></tr></table>"
        "<p>A vulnerability is the weakness; the threat is who or what exploits it. \"Data breach\" is a threat or impact, never a vulnerability.</p>"
    )
    p = [q(written(1.5, model, inner=table), "2")]
    p.append(
        '<p class="part" style="font-weight:400"><b>C)</b> A fintech company located in Riyadh has developed a mobile banking app that allows customers to:</p>'
        '<ul style="margin:0 0 6px"><li>Log in using their username and password.</li><li>View account balances, monthly statements, and transaction history.</li><li>Transfer money to other accounts and Pay bills and receive real-time payment notifications.</li></ul>'
        "<p style=\"margin:0\">Before launching the app nationwide, the company wants to perform a <b>STRIDE threat modeling analysis</b> to identify potential security risks.</p>"
        '<ol type="I" style="margin:4px 0"><li>List down the STRIDE threats. (Column 1)</li><li>For each threat, write an example presenting an associated threat (Column 2).</li><li>For each STRIDE threat, write an appropriate Cyber security threat category <b>(given below)</b> (Column 3).</li></ol>'
        + cat_table()
    )
    rows = ""
    for r in range(6):
        rows += (
            f'<tr><td><input class="line-in" data-unit="stride-threat" data-marks="0.25" aria-label="STRIDE threat {r + 1}" /></td>'
            f'<td><textarea class="ruled cell" rows="2" aria-label="Threat example {r + 1}"></textarea></td>'
            f'<td>{sel(CATS, "", 0.25, "Category " + str(r + 1)).replace("data-unit=\"select\"", "data-unit=\"stride-cat\"").replace(" data-answer=\"\"", "")}</td></tr>'
        )
    stride = (
        '<table class="ptable stack table-stack-labels"><thead><tr><th>STRIDE THREAT [1.5 Marks]</th><th>Threat Example [1.5 Marks]</th><th>CYBER SECURITY THREAT CATEGORY [1.5 Marks]</th></tr></thead>'
        f"<tbody>{rows}</tbody></table>"
    )
    ex_model = (
        "<ul><li><b>Spoofing:</b> logging in with a stolen customer username and password, pretending to be that customer.</li>"
        "<li><b>Tampering:</b> altering the amount or recipient of a transfer, or editing the transaction history.</li>"
        "<li><b>Repudiation:</b> a customer denies making a transfer that they did make, and there are no logs to prove it.</li>"
        "<li><b>Information disclosure:</b> leaking customers' balances, statements or credentials.</li>"
        "<li><b>Denial of service:</b> flooding the app's servers so customers can't log in or pay bills.</li>"
        "<li><b>Elevation of privilege:</b> a regular customer gains admin rights or reaches other customers' accounts.</li></ul>"
    )
    p.append(q(stride + "<p style='font:13px var(--sans);color:var(--ink-2);margin:4px 0'>Columns 1 and 3 are checked automatically; mark column 2 yourself below.</p>"
               + written(1.5, ex_model, inner="<span></span>"), "2", CAT_NOTE))
    pages.append(psu_page(4, T, "".join(p)))

    # ---- page 5
    p = ['<p class="part" style="font-weight:400"><b>D) You are presented with the following scenarios related to a company’s cybersecurity practices. For each scenario, classify it as either an example of due care or due diligence, and briefly explain your reasoning. [1.5 marks] (0.5 for each point)</b></p>']
    dd = [
        ("Scenario A:", "A fintech company in Riyadh implements a robust employee training program that includes regular workshops on some security practices to comply with NCA standards.", "Due care",
         "Due care: the company is doing what a responsible organization should do — training staff to meet the NCA standards it must comply with."),
        ("Scenario B:", "A company is implementing a new incident response plan. The security team investigates each single potential threats, reviews best practices, and assesses all risks.", "Due diligence",
         "Due diligence: investigating threats, reviewing best practices and assessing risks is the research and analysis done before acting."),
        ("Scenario C:", "<b>Medwin Hospital</b> implements a comprehensive cybersecurity awareness program for all staff, including regular workshops on data privacy, secure handling of patient health records, and AI system ethics, to comply with national healthcare and data protection regulations.", "Due care",
         "Due care: implementing an awareness program to comply with regulations is the protective action itself."),
    ]
    rows = ""
    for lab, sc, ans, why in dd:
        rows += (
            f'<tr><td><b>{lab}</b> {sc}</td></tr><tr><td>'
            + q(sel(["Due care", "Due diligence"], ans, 0.25, lab + " classification")
                + written(0.25, why, 1, lab + " reasoning", cls="ruled short"), "2")
            + "</td></tr>"
        )
    p.append(f'<table class="ptable">{rows}</table>')
    p.append(qhead(3, 6))
    pt3 = "Incomprehensibilities"
    p.append(q(
        f'<p class="part" style="font-weight:400"><b>A)</b> Assuming the block size b=128 bits. The plaintext is “{pt3}”. How many total blocks needed to send the complete plaintext. Calculate the number of padded bits needed to complete the last block. [1 mark] (0.5 mark for each point)</p>'
        f'<div class="q-row"><span class="n">I.</span><p class="q-text">How many blocks will be used? {num(2, 0.5, "Blocks")}</p></div>'
        f'<div class="q-row"><span class="n">II.</span><p class="q-text">How many Padded bits are needed to send the complete data? {num(88, 0.5, "Padded bits")} bits</p></div>',
        "3",
        f"“{pt3}” has 21 characters = 21 bytes = 168 bits. A block is 128 bits = 16 bytes, so 2 blocks (32 bytes) are needed. "
        "Padding = 32 − 21 = 11 bytes = <b>88 bits</b>. The marker took a quarter mark off for writing 16 × 2 = 32 without stating “2 blocks” — say the number of blocks explicitly."))
    pages.append(psu_page(5, T, "".join(p)))

    # ---- page 6
    m = pf_matrix("NO")
    dear = "".join(pf_apply(m, pf_pairs("DEAR")))
    trans = columnar("HelloThere", [4, 2, 1, 5, 3])
    easy = vigenere("QEEC", "ME", decrypt=True)
    hill = hill_rows("HELP", [[3, 3], [2, 5]])
    help_ct = "".join(A[x] + A[y] for _, _, (x, y) in hill)
    scratch = "".join(
        "<tr>" + "".join('<td><input class="line-in" maxlength="2" aria-label="Transposition grid cell" style="min-width:0;text-align:center" /></td>' for _ in range(5)) + "</tr>"
        for _ in range(2)
    )
    p = ['<p class="part">B) Apply Whether Encryption or Decryption to each of the following [3 marks]:</p>']
    p.append(
        '<table class="ptable"><thead><tr><th>Plaintext</th><th>Cipher Algorithm</th><th>Ciphertext</th></tr></thead><tbody>'
        f'<tr><td><b>DEAR</b></td><td><b>Playfair cipher</b><br />Key: “NO”<br /><span style="font-size:.85em">Key matrix</span>{matrix_static(m)}</td>'
        f'<td>{q(txt(dear, 1, "Playfair ciphertext", ph="ciphertext"), "3", "Pairs: DE AR. DE share a row (D E F G H), so each letter takes the one to its right: EF. A and R form a rectangle: each takes the letter in its own row and the other letter’s column: A→O, R→S. Ciphertext <b>" + dear + "</b>.")}</td></tr>'
        f'<tr><td><b>HelloThere</b></td><td><b>Transposition cipher</b><br />Key: 4, 2, 1, 5, 3'
        f'<table class="ptable center" style="width:auto"><tr><th>4</th><th>2</th><th>1</th><th>5</th><th>3</th></tr>{scratch}</table></td>'
        f'<td>{q(txt(trans, 1, "Transposition ciphertext", ph="ciphertext"), "3", "Write HelloThere in rows under the key (H e l l o / T h e r e), then read the columns in key order 1, 2, 3, 4, 5: le · eh · oe · HT · lr → <b>" + trans + "</b>.")}</td></tr>'
        f'<tr><td>{q(txt(easy, 1, "Vigenère plaintext", ph="plaintext"), "3", "Decryption: subtract the key letter (M = 12, E = 4, repeating) from each ciphertext letter: Q−M = E, E−E = A, E−M = S, C−E = Y → <b>" + easy + "</b>. The ciphertext was given, so this row is a decryption.")}</td>'
        f'<td><b>Vigenère cipher</b><br />Key: “ME”{tableau(True)}</td><td><b>QEEC</b></td></tr>'
        "</tbody></table>"
    )
    work = "".join(
        f"<li>{A[a]}{A[b]} = ({a}, {b}) × K = ({a}·3 + {b}·2, {a}·3 + {b}·5) = ({x}, {y}) mod 26 = ({mx}, {my}) → <b>{A[mx]}{A[my]}</b></li>"
        for (a, b), (x, y), (mx, my) in hill
    )
    p.append(q(
        '<p class="part">C) Encrypt the word (HELP) using the hill cipher (Using row approach) where the key and key inverse are: [1 mark]</p>'
        + alpha_strip(True)
        + f'<table class="ptable center" style="width:auto"><tr><th>K</th><td>{mat([[3, 3], [2, 5]])}</td><th>K<sup>−1</sup></th><td>{mat([[15, 17], [20, 9]])}</td></tr></table>'
        + f'<p class="q-text">Ciphertext: {txt(help_ct, 1, "Hill ciphertext")}</p>',
        "3", f"Row approach: each pair is a row vector multiplied by K.<ol>{work}</ol>Ciphertext <b>{help_ct}</b>. The inverse key is only for decryption."))
    pages.append(psu_page(6, T, "".join(p)))

    # ---- page 7
    p = ['<p class="part">D) Given the following figure, answer the following questions. [1 Marks]</p>', cbc_svg()]
    p.append(q(f'<div class="q-row"><span class="n">i.</span><p class="q-text">What is the encryption mode? [0.5 Mark] {txt("CBC|CIPHERBLOCKCHAINING", 0.5, "Mode", show="CBC (Cipher Block Chaining)")}</p></div>', "3",
               "Each plaintext block is XORed with the previous ciphertext block (the IV for the first) before encryption: Cipher Block Chaining."))
    p.append(q('<div class="q-row"><span class="n">ii.</span><div><p class="q-text">Write the decryption function for P[2]. [0.5 Mark]</p>'
               + written(0.5, "<p><b>P[2] = D<sub>K</sub>(C[2]) ⊕ C[1]</b></p><p>General form: P[i] = D<sub>K</sub>(C[i]) ⊕ C[i−1], with C[−1] = IV. "
                         "Writing the encryption formula C[i] = E<sub>K</sub>(P[i] ⊕ C[i−1]) or an unfinished expression lost marks on the marked paper.</p>", 2) + "</div></div>", "3"))
    pages.append(psu_page(7, T, "".join(p), '<div class="goodluck">GOODLUCK ☺</div>'))
    return "".join(pages)


# ================================================================= PAPER B (term unknown, 7 pages, page 4 missing)
CAESAR_PT = "THEXIDESXOFXMARCHXAREXCOME"
CAESAR_Q = (
    'The following message is encrypted using Caesar Cipher, find its associated key assuming the space is replaced by the letter “X”.<br />'
    '<span style="display:inline-block;margin-left:5em">Message = THE IDES OF MARCH ARE COME<br />'
    f"Plaintext = {CAESAR_PT}<br />Ciphertext = {caesar(CAESAR_PT, 7)}</span>"
)
CAESAR_WHY = "T (19) → A (0): 19 + 7 = 26 ≡ 0. Check: H (7) → O (14). Every letter shifts 7, so K = 7."
SARAH = (
    "Sarah, a financial analyst at a multinational company located in London, needs to share a confidential financial report with her manager, "
    "before a very important meeting in Riyadh as part of LEAP conference. She is considering different ways to send the file and wants to ensure "
    "that the data remains secure. Which of the following security controls should Sarah follow when storing, accessing, and transferring confidential data?"
)
SARAH_OPTS = ["Do not transfer confidential data by email .", "Do not transfer confidential data by email unless encrypted .",
              "Transfer confidential data by email without restrictions .", "None of the above."]
SARAH_WHY = "Email itself is fine; unencrypted email is the problem. Encrypting the file protects its confidentiality in storage and in transit."
HOSP = 'A hospital categorizes its data as <b><u>Confidential</u></b>, <b><u>Internal Use</u></b>, or <b><u>Public</u></b>. Which data classification is correct?'
HOSP_OPTS = [
    "<b>Confidential</b>→Staff payroll, <b>Internal Use</b>→Patient records , <b>Public</b>→Internal emails",
    "<b>Confidential</b>→Public health announcements, <b>Internal Use</b>→Patient records, <b>Public</b>→ Financial reports",
    "<b>Confidential</b>→Employee schedules, <b>Internal Use</b>→Press releases, <b>Public</b>→Patient medical history",
    "<b>Confidential</b>→Patient records, <b>Internal Use</b>→Staff payroll, <b>Public</b>→Health awareness brochures",
]
HOSP_WHY = "Patient records are the most sensitive (confidential), payroll is for internal staff only, and awareness brochures are meant for the public."


def paper_b():
    _n["i"] = 0
    T = 7
    p = [qhead(1, 5, first=True), '<p class="part">A) Choose the Correct Option. [2.5 Marks]</p>']
    p.append(mcq(1, "Given the nested DES encryption operation C = EKC(DKB(EKA(P))); what is the correct sequence of decryption operations?",
                 ["The output from decrypting with KC is used as the input for encrypting with KB, then for decrypting with KA.",
                  "The output from encrypting with KC is used as the input for encrypting with KB, then for decrypting with KA.",
                  "The input from decrypting with KC is used as the output for encrypting with KB, then for decrypting with KA.",
                  "The output from encrypting with KC is used as the input for decrypting with KB, then for encrypting with KA."],
                 "a", "Undo the outermost step first, each with its inverse: P = D<sub>KA</sub>(E<sub>KB</sub>(D<sub>KC</sub>(C))). So decrypt with KC, feed that output into encryption with KB, then decrypt with KA.")[0])
    p.append(mcq(2, CAESAR_Q, ["K = 3", "K = 5", "K = 6", "K = 7"], "d", CAESAR_WHY)[0])
    p.append(mcq(3, SARAH, SARAH_OPTS, "b", SARAH_WHY)[0])
    p.append(mcq(4, HOSP, HOSP_OPTS, "d", HOSP_WHY)[0])
    p.append(mcq(5, "You have been tasked with crafting a fairly stable security plan. It also needs to define the security function and align it to the goals, mission, and objectives of the organization. What are you being asked to create?",
                 ["Operational Plan", "Strategic Plan", "Tactical Plan", "Rollback Plan"], "b",
                 "A strategic plan is the long-term, stable plan that defines the security function and aligns it with the organization's goals, mission and objectives. Tactical plans are mid-term; operational plans are day-to-day.",
                 two_col=True)[0])
    pages = [missing(1, T, "The cover page (student details and instructions)."), psu_page(2, T, "".join(p))]

    terms = ["Utility", "Authenticity", "Brute-Force Attack", "Cyber criminal", "Tailgating", "Confidentiality", "Two factor authentication", "Firewall", "Phishing"]
    p = ['<p class="part">B) For each statement, choose the appropriate Term from the given table to fill the blank. [2.5 Marks]</p>',
         '<table class="ptable terms"><tr><td>Utility</td><td>Authenticity</td><td>Brute-Force Attack</td></tr><tr><td>Cyber criminal</td><td>Tailgating</td><td>Confidentiality</td></tr><tr><td>Two factor authentication</td><td>Firewall</td><td>Phishing</td></tr></table>']
    fills = [
        ("", "Confidentiality", " refers to the quality or state of preventing disclosure or exposure to unauthorized individuals.", "Confidentiality is about preventing disclosure to unauthorized people."),
        ("", "Tailgating", " a physical security breach where an unauthorized person gains access to a restricted area by following an authorized individual without proper authentication.", "Following someone through a secured door is tailgating (piggybacking)."),
        ("The main motivation of ", "Cyber criminal", " is to gain financial benefits and make money.", "Cyber criminals are driven by money; hacktivists by causes, nation states by politics."),
        ("", "Utility", " if information is available, but not in a format meaningful to the end user. For example if a doctor tries to access a patient’s file but receives the data in raw hexadecimal code instead of a readable medical report",
         "Utility is the value of information for a purpose: raw hexadecimal is available but useless to the doctor, so it lacks utility."),
        ("", "Two factor authentication", " can prevent unauthorized access even if a user’s password is compromised.", "A second factor (a token, a code on the phone) is still needed after the password leaks."),
    ]
    for i, (a, ans, b, why) in enumerate(fills):
        p.append(q(f'<div class="q-row"><span class="n">{"abcde"[i]})</span><p class="q-text">{a}{sel(terms, ans, 0.5, "Blank " + "abcde"[i])}{b}</p></div>', "1", why))
    p.append(qhead(2, 9))
    p.append('<p class="part" style="font-weight:400"><b>A)</b></p><ol type="I" style="margin:0 0 4px"><li>List down the STRIDE threats. (Column 1)</li><li>For each threat, write the security property it violates (Column 2).</li><li>For each STRIDE threat, write an appropriate Cyber security threat category (given below) (Column 3).</li></ol>')
    p.append(cat_table())
    rows = ""
    for r in range(6):
        rows += (
            f'<tr><td><input class="line-in" data-unit="stride-threat" data-marks="0.25" aria-label="STRIDE threat {r + 1}" /></td>'
            f'<td><input class="line-in" data-unit="stride-prop" data-marks="0.25" aria-label="Property violated {r + 1}" /></td>'
            f'<td>{sel(CATS, "", 0.25, "Category " + str(r + 1)).replace("data-unit=\"select\"", "data-unit=\"stride-cat\"").replace(" data-answer=\"\"", "")}</td></tr>'
        )
    key = "".join(f"<tr><td>{a}</td><td>{b}</td><td>{c}</td></tr>" for a, b, c in STRIDE_ROWS)
    p.append(q('<table class="ptable stack table-stack-labels"><thead><tr><th>STRIDE THREAT [1.5 Marks]</th><th>PROPERTY VIOLATED [1.5 Marks]</th><th>CYBER SECURITY THREAT CATEGORY [1.5 Marks]</th></tr></thead>'
               f"<tbody>{rows}</tbody></table>", "2",
               f'<table class="ptable" style="margin-top:6px"><tr><th>Threat</th><th>Property</th><th>Category</th></tr>{key}</table>{CAT_NOTE}'))
    pages.append(psu_page(3, T, "".join(p)))
    pages.append(missing(4, T, "This page held Question 2 parts B, C and D (3.5 marks). They aren't included, so this paper is marked out of 16.5."))

    p = ['<p class="part" style="font-weight:400"><b>E) You are presented with the following scenarios related to a company’s cybersecurity practices. For each scenario, classify it as either an example of due care or due diligence, and briefly explain your reasoning. [1 marks]</b></p>']
    dd = [
        ("Scenario A:", "A company in Riyadh implements a robust employee training program that includes regular workshops on phishing awareness and secure password practices to meet NCA requirements.", "Due care",
         "Due care: running the training to meet NCA requirements is the reasonable protective action itself."),
        ("Scenario B:", "The company conducts risk assessments every two months to identify potential security threats and vulnerabilities in its systems.", "Due diligence",
         "Due diligence: regular risk assessments are the ongoing investigation that identifies what needs protecting."),
    ]
    rows = ""
    for lab, sc, ans, why in dd:
        rows += f'<tr><td><b>{lab}</b> {sc}</td></tr><tr><td>' + q(sel(["Due care", "Due diligence"], ans, 0.25, lab + " classification") + written(0.25, why, 1, lab + " reasoning", cls="ruled short"), "2") + "</td></tr>"
    p.append(f'<table class="ptable">{rows}</table>')
    p.append(qhead(3, 6))
    pt = "wewillattentandenjoyLEAPinKSA"
    n = len(pt)
    blocks = -(-n // 8)
    pad = (blocks * 8 - n) * 8
    p.append(q(
        f'<p class="part" style="font-weight:400"><b>A)</b> Assuming the block size b=64 bits. The plaintext is “{pt}”.[1 mark]</p>'
        f'<div class="q-row"><span class="n">I.</span><p class="q-text">How many Padded bits are needed to send the complete data? {num(pad, 0.5, "Padded bits")} bits</p></div>'
        f'<div class="q-row"><span class="n">II.</span><p class="q-text">How many blocks will be used? {num(blocks, 0.5, "Blocks")}</p></div>',
        "3", f"“{pt}” has {n} characters = {n} bytes. A 64-bit block holds 8 bytes, so {blocks} blocks ({blocks * 8} bytes) are needed. "
             f"Padding = {blocks * 8} − {n} = {blocks * 8 - n} bytes = <b>{pad} bits</b>."))
    m = pf_matrix("EFFECTIVENESS")
    pairs = pf_pairs("COMMITTEES")
    ct = pf_apply(m, pairs)
    p.append(q(
        '<p class="part" style="font-weight:400"><b>B)</b> Using the Playfair cipher, construct a Playfair matrix, and encrypt the message ” COMMITTEES ” with the keyword ” EFFECTIVENESS ” considering that (I/J) will be in the same cell. Show your answer. [1.5 mark]</p>'
        + matrix_input(m, 0.5, "Playfair matrix")
        + f'<p class="q-text">Ciphertext: {txt("".join(ct), 1, "Playfair ciphertext")}</p>',
        "3", f"Matrix: keyword letters without repeats (E F C T I V N S), then the rest of the alphabet: {matrix_static(m)}"
             f"Split into pairs, putting X between the double letters: {' '.join(pairs)}. Encrypt each pair: {' '.join(ct)} → <b>{''.join(ct)}</b>."))
    pages.append(psu_page(5, T, "".join(p)))

    vct = "CMRUVLERMYOLRX"
    vpt = vigenere(vct, "RIYADH", decrypt=True)
    p = [q(f'<p class="part">C) Using Vigenère cipher, decrypt the Ciphertext: “{vct}” with key “ RIYADH ”. [1 Marks]</p>{tableau()}'
           f'<p class="q-text">Plaintext: {txt(vpt, 1, "Vigenère plaintext")}</p>', "3",
           f"Repeat the key under the ciphertext (RIYADHRIYADHRI) and subtract each key letter: C−R = L, M−I = E, R−Y = T, U−A = U, V−D = S, L−H = E, … → <b>{vpt}</b> (“let us enjoy LEAP”).")]
    p.append('<p class="part">D) Given the following figure, answer the following questions. [2.5 Marks]</p>')
    p.append(cbc_svg())
    p.append(q(f'<div class="q-row"><span class="n">i.</span><p class="q-text">What is the encryption Mode? [1 Mark] {txt("CBC|CIPHERBLOCKCHAINING", 1, "Mode", show="CBC (Cipher Block Chaining)")}</p></div>', "3",
               "Plaintext is XORed with the previous ciphertext block (the IV first) before encryption: Cipher Block Chaining."))
    pages.append(psu_page(6, T, "".join(p)))
    p = [q('<div class="q-row"><span class="n">ii.</span><div><p class="q-text">Write the encryption function for C[2] / decryption function for P[2]. [1.5 Mark]</p>'
           + written(1.5, "<p><b>Encryption:</b> C[2] = E<sub>K</sub>(P[2] ⊕ C[1])</p><p><b>Decryption:</b> P[2] = D<sub>K</sub>(C[2]) ⊕ C[1]</p>"
                          "<p>General form: C[i] = E<sub>K</sub>(P[i] ⊕ C[i−1]) and P[i] = D<sub>K</sub>(C[i]) ⊕ C[i−1], with C[−1] = IV (the V in the figure).</p>", 6) + "</div></div>", "3")]
    pages.append(psu_page(7, T, "".join(p), '<div class="goodluck">GOODLUCK ☺</div>'))
    return "".join(pages)


# ================================================================= PAPER C (term unknown, 6 pages)
def paper_c():
    _n["i"] = 0
    T = 6
    p = [qhead(1, 5, first=True), '<p class="part">A) Choose the Correct Option. [2.5 Marks]</p>']
    p.append(mcq(1, CAESAR_Q, ["K = 3", "K = 5", "K = 6", "K = 7"], "d", CAESAR_WHY)[0])
    p.append(mcq(2, SARAH, SARAH_OPTS, "b", SARAH_WHY)[0])
    p.append(mcq(3, "You are a cybersecurity officer for the SAB bank in Riyadh. A customer reports seeing an unauthorized transaction in their account history, even though they claim they never made any transaction. Upon investigating the network traffic, you discover that an attacker (Man-in-the-Middle) intercepted the communication between the customer and your servers. The attacker altered the data in transit to divert the funds to their own account. This is considered as a violation to:",
                 ["Authorization", "Authentication", "Integrity", "Accounting"], "c",
                 "The attacker changed the data in transit (tampering), so integrity is violated.")[0])
    p.append(mcq(4, HOSP, HOSP_OPTS, "d", HOSP_WHY)[0])
    p.append(mcq(5, "Knowledge of letter frequencies, including pairs and triples can be used in cryptologic attacks against ______________ ciphers.",
                 ["Substitution ciphers", "Transposition ciphers", "Asymmetric ciphers", "Both (a) &amp; (b)"], "a",
                 "Substitution ciphers keep each letter's frequency pattern (just relabelled), so frequency analysis breaks them. Transposition keeps the letters themselves and is attacked by rearranging, not by letter frequencies.")[0])
    pages = [missing(1, T, "The cover page (student details and instructions)."), psu_page(2, T, "".join(p))]

    terms = ["Declassification", "Degaussing", "Destruction", "Purging", "Erasing", "Overwriting"]
    p = ['<p class="part">B) For each statement, choose the appropriate term from the given table. [2.5 Marks]</p>',
         '<table class="ptable terms"><tr><td>Declassification</td><td>Degaussing</td><td>Destruction</td></tr><tr><td>Purging</td><td>Erasing</td><td>Overwriting</td></tr></table>']
    fills = [
        ("Prepares media for reuse in less secure environments.", "Purging", "Purging is a more intense form of clearing that prepares media for reuse in a less secure environment."),
        ("Any process that purges media or a system in preparation for reuse in an unclassified environment.", "Declassification", "Declassification purges media or a system so it can be reused in an unclassified environment."),
        ("Process of preparing media for reuse and ensuring that the cleared data cannot be recovered using traditional recovery tools.", "Overwriting", "Clearing, or overwriting, prepares media for reuse so that traditional recovery tools can't recover the data. Degaussing is the distractor: it is a purging technique for magnetic media."),
        ("Simply performing a delete operation against a file, a selection of files, or the entire media.", "Erasing", "Erasing is just a delete, so the data remains recoverable."),
        ("The most secure method of sanitizing media.", "Destruction", "Destruction (shredding, incineration, disintegration) is the most secure method."),
    ]
    for i, (stmt, ans, why) in enumerate(fills):
        p.append(q(f'<div class="q-row"><span class="n">{"abcde"[i]})</span><p class="q-text">{stmt} {sel(terms, ans, 0.5, "Blank " + "abcde"[i])}</p></div>', "1", why))
    p.append(qhead(2, 8))
    p.append('<p class="part" style="font-weight:400"><b>A)</b> You are part of the security team for a fintech company developing a mobile banking app. The app allows users to: view account balances and recent transactions, transfer money between accounts, pay bills and receive notifications about suspicious activity. The backend system includes APIs for authentication, account management, and transaction processing, all hosted in the cloud behind a web application firewall (WAF). The app uses 2FA for user authentication.<br />Using the <b>STRIDE</b> threat modeling framework, complete the following table:</p>'
             '<ol type="a" style="margin:0 0 6px"><li>Identify <b>one potential threat on any given assets</b> for the given STRIDE threats (Column 2).</li><li>write the security property it violates (Column 3).</li><li>For each threat, one <b>possible mitigation</b>. (Column 4)</li></ol>')
    given = [
        ("S", "Spoofing", "An attacker logs in as a customer with stolen credentials (or a stolen 2FA code) and transfers money.", "Enforce 2FA/MFA, strong password policy, lock accounts after repeated failures."),
        ("T", "Tampering", "A man-in-the-middle alters the amount or recipient of a transfer request sent to the transaction API.", "TLS for all API traffic; sign/HMAC transaction requests; server-side validation."),
        ("D", "Denial of Service", "Flooding the authentication or transaction APIs so customers can't view balances or pay bills.", "Rate limiting and WAF rules, DDoS protection, load balancing / autoscaling."),
        ("E", "Elevation of Privileges", "A normal user exploits an account-management API flaw to reach admin functions or other users' accounts.", "Least privilege with role-based access control; server-side authorization checks on every request."),
    ]
    rows = ""
    for k, name, threat, mit in given:
        rows += (
            f'<tr data-given="{k}"><td><b>{name}</b></td>'
            f'<td>{written(0.25, threat, 2, name + " threat", cls="ruled cell")}</td>'
            f'<td><input class="line-in" data-unit="stride-prop" data-marks="0.25" aria-label="{name} property violated" /></td>'
            f'<td>{written(0.25, mit, 2, name + " mitigation", cls="ruled cell")}</td></tr>'
        )
    p.append(q('<table class="ptable stack table-stack-labels"><thead><tr><th>STRIDE THREAT</th><th>POTENTIAL THREAT ON ASSETS [1 Marks]</th><th>PROPERTY VIOLATED [1 Marks]</th><th>MITIGATION/ SECURITY CONTROL [1 Marks]</th></tr></thead>'
               f"<tbody>{rows}</tbody></table>", "2",
               "Properties: Spoofing → Authentication, Tampering → Integrity, Denial of Service → Availability, Elevation of Privileges → Authorization. "
               "On the marked copy the property names went into the threat column; the threat column needs an actual attack on one of the app's assets."))
    pages.append(psu_page(3, T, "".join(p)))

    p = [q('<p class="part" style="font-weight:400"><b>B) What is ASP? When using an ASP, what should be conducted to ensure the protection of the data. [1 Marks]</b></p>'
           + written(1, "<p><b>ASP = Application Service Provider:</b> a third party that hosts and maintains software on its own servers and delivers it to customers over the internet.</p>"
                        "<p>The organization stays accountable for its data, so it must perform <b>due diligence</b> on the provider before engaging it, and sign <b>contracts and SLAs</b> that define security requirements, responsibilities and breach notification (and audit the provider's controls).</p>", 3), "2")]
    p.append(q('<p class="part" style="font-weight:400"><b>C) For the commercial classification systems, write any THREE criteria’s used to classify information [1.5 Marks]</b></p>'
               + written(1.5, "<p>Any three of: <b>business value</b> of the information; <b>legal and regulatory</b> impact (e.g. PDPL, GDPR); <b>reputational damage</b> if it is disclosed; <b>operational impact</b> if it is altered or lost. (Also accepted in the textbooks: age / useful life and personal association.)</p>"
                               "<p>Tactical, operational and strategic are types of <i>plans</i>, not classification criteria — the answer on the marked copy scored 0 for that reason.</p>", 3), "2"))
    p.append(q('<p class="part" style="font-weight:400"><b>D) Analyze why symmetric encryption algorithms are preferred for encrypting large amounts of data compared to asymmetric algorithms. [1 Mark]</b></p>'
               + written(1, "<p>Symmetric algorithms use one shared key and simple, fast operations (substitution, permutation, XOR), so they are much faster and need far less computation than asymmetric algorithms, which do heavy maths on very large numbers. That speed makes symmetric encryption practical for bulk data; asymmetric encryption is used only to exchange the symmetric key or sign (hybrid encryption).</p>"
                           "<p>Symmetric uses <i>one</i> key, not two; \"more keys means more security\" scored 0 on the marked copy.</p>", 3), "2"))
    p.append('<p class="part" style="font-weight:400"><b>E) You are presented with the following scenarios related to a company\'s cybersecurity practices. For each scenario, classify it as either an example of <u>due care, due diligence or both</u>, and briefly explain your reasoning. [1.5 Marks]</b></p>')
    dd = [
        ("Scenario A:", "After detecting a data breach, a company immediately activates its incident response plan, notifies affected customers, and begins remediation efforts.", "Due care",
         "Due care: responding to the breach, notifying customers and fixing the damage is the reasonable action a responsible company takes. It is not research or assessment, so it is not due diligence (\"Both\" scored 0 on the marked copy)."),
        ("Scenario B:", "A company suffers a ransomware attack that encrypts all their files. An investigation reveals that the company hadn’t updated its antivirus software in over a year and ignored security examination advise from their software vendors.", "Both",
         "Both are missing: not updating the antivirus is a failure of due care, and ignoring the vendors' security examination advice is a failure of due diligence. Answering only \"due care\" earned half marks."),
        ("Scenario C:", "The company requires all third-party vendors to sign a data protection agreement and undergo security audits before accessing sensitive information.", "Due diligence",
         "Due diligence: vetting and auditing third parties before giving them access is investigating risk before acting."),
    ]
    rows = ""
    for lab, sc, ans, why in dd:
        rows += f'<tr><td><b>{lab}</b> {sc}</td></tr><tr><td>' + q(sel(["Due care", "Due diligence", "Both"], ans, 0.25, lab + " classification") + written(0.25, why, 2, lab + " reasoning", cls="ruled short"), "2") + "</td></tr>"
    p.append(f'<table class="ptable">{rows}</table>')
    pages.append(psu_page(4, T, "".join(p)))

    m = pf_matrix("EFFECTIVENESS")
    ct = "FPPUUEBFTSIEWG"
    pairs = [ct[i : i + 2] for i in range(0, len(ct), 2)]
    pl = pf_apply(m, pairs, decrypt=True)
    p = [qhead(3, 7, first=True)]
    p.append(q(f'<p class="part" style="font-weight:400"><b>A) (a) <u>Decrypt</u> the Ciphertext: “{ct}”, using Playfair Cipher with the keyword “EFFECTIVENESS”. Show the complete working. [1.5 Marks]</b></p>'
               + '<p style="font:13px var(--sans);color:var(--ink-2);margin:0">Build the matrix here (checked, not marked), then write the plaintext.</p>'
               + matrix_input(m, 0, "Playfair matrix")
               + f'<p class="q-text">Plaintext: {txt("COMMUNICATION|COMXMUNICATION|COMXMUNICATIONX", 1.5, "Playfair plaintext", show="COMMUNICATION")}</p>', "3",
               f"Matrix rows: {' / '.join(' '.join(r) for r in m)}. Decrypt each pair (same row → letter to the left, same column → letter above, rectangle → own row, other letter's column): "
               f"{' '.join(f'{a}→{b}' for a, b in zip(pairs, pl))}. That gives {''.join(pl)}; drop the filler X between the double M: <b>COMMUNICATION</b>. "
               "The marked copy lost a quarter for decrypting FP as OC: in a rectangle each letter takes the corner in <i>its own</i> row, so FP → CO."))
    p.append(q('<p class="part" style="font-weight:400"><b>(b) In Playfair Cipher, the cryptanalysis depends on which factor? [1 Marks]</b></p>'
               + f'<p class="q-text">{txt("", 1, "Factor", pattern="key", show="the keyword (the key matrix)")}</p>', "3",
               "The whole cipher is the 5×5 matrix built from the keyword, so breaking Playfair means recovering the keyword / key square (usually through digram frequency analysis)."))
    p.append('<p class="part">B) Using a Hill Cipher, answer the following questions.</p>')
    p.append(alpha_strip(False, ("Plaintext Alphabet", "Plaintext Value")))
    p.append(q('<div class="q-row"><span class="n">a)</span><div><p class="q-text">Is the key K = [2 &nbsp;6] suitable for use as a Hill Cipher encryption matrix? Give the reason. [0.5 Marks]</p>'
               + sel(["Yes", "No"], "No", 0.25, "Suitable?")
               + written(0.25, "<p><b>No.</b> A Hill key must be a <b>square</b> (n × n, here 2 × 2) matrix that is <b>invertible mod 26</b> (its determinant must have no common factor with 26), otherwise the ciphertext can't be decrypted. [2 6] is a 1 × 2 row, so it has no inverse.</p>", 1, "Reason", cls="ruled short")
               + "</div></div>", "3"))
    hill = hill_rows("FKMFIO", [[2, 25], [25, 18]])
    plain = "".join(A[x] + A[y] for _, _, (x, y) in hill)
    work = "".join(
        f"<li>{A[a]}{A[b]} = ({a}, {b}) × K<sup>−1</sup> = ({x}, {y}) mod 26 = ({mx}, {my}) → <b>{A[mx]}{A[my]}</b></li>"
        for (a, b), (x, y), (mx, my) in hill
    )
    p.append(q(f'<div class="q-row"><span class="n">b)</span><div><p class="q-text">Given the matrix k = {mat([[2, 3], [3, 6]])} and k<sup>−1</sup> = {mat([[2, 25], [25, 18]])}, choose a suitable key to decrypt the ciphertext “FKMFIO” [1.5 Marks]</p>'
               + f'<p class="q-text">Key used: {sel(["k", "k⁻¹"], "k⁻¹", 0.5, "Key to use")} &nbsp; Plaintext: {txt(plain, 1, "Hill plaintext")}</p></div></div>', "3",
               f"Decryption uses the inverse key. Row approach, plaintext pair = ciphertext pair × k<sup>−1</sup>:<ol>{work}</ol>Plaintext <b>{plain}</b>."))
    pages.append(psu_page(5, T, "".join(p)))

    p = ['<p class="part" style="font-weight:400"><b>C) Read the scenarios below carefully, and answer the questions based on the information provided with no further assumptions</b></p>']
    p.append(q('<p class="q-text"><b><u>Scenario 1:</u></b><br />A company has gone through a round of phishing attacks. More than 200 users have had their workstation infected because they clicked on a link in an email. An incident analysis has determined an executable ran and compromised the administrator account on each workstation. Management is demanding the information security team prevent this from happening again.<br /><b>Which action do you need to take to prevent this from happening again? [0.5 Marks]</b></p>'
               + written(0.5, "<p>Run <b>security awareness training</b> on phishing so users stop clicking malicious links (the action the marked copy got full marks for). Technical backups to mention: application whitelisting so unknown executables can't run, and removing administrator rights from everyday accounts (least privilege).</p>", 2), "3"))
    p.append(q('<p class="q-text"><b><u>Scenario 2:</u></b><br />You receive a message on Instagram from a friend, asking if you would like to invest in a new cryptocurrency that’s "guaranteed to make huge returns." They provide a link to an investment website that looks very professional, and they urge you to act quickly.<br /><b>What type of phishing attack is targeting you and What action should you take? [1 Marks]</b></p>'
               + f'<p class="q-text">Type: {txt("", 0.5, "Phishing type", pattern="angler", show="Angler phishing")}</p>'
               + written(0.5, "<p>Don't open the link or send money. Verify with the friend through another channel (their account may be compromised), check the URL with a link checker, and report the account.</p>", 2, "Action"), "3",
               "Phishing through social media is <b>angler phishing</b>."))
    p.append(q('<p class="q-text"><b><u>Scenario 3:</u></b><br />A company employee receives a call from someone claiming to be from the IT department, offering a free software upgrade in exchange for the employee’s login credentials. The caller insists that the credentials are necessary to complete the upgrade remotely. The employee, wanting to take advantage of the upgrade, provides their username and password.<br /><b>Identify the type of social engineering attack used in this scenario and write one way an organization can protect against such attacks. [1 Marks]</b></p>'
               + f'<p class="q-text">Type: {txt("", 0.5, "Attack type", pattern="quid", show="Quid pro quo")}</p>'
               + written(0.5, "<p>Security awareness training, plus a policy that IT never asks for passwords and that callers are verified by calling back the official help-desk number.</p>", 2, "Protection"), "3",
               "Something offered <i>in exchange</i> for information is <b>quid pro quo</b> (it arrives by phone, so vishing is also a fair description). Baiting — the answer on the marked copy, which got half marks — leaves a lure such as an infected USB drive for the victim to pick up; it doesn't trade a service for credentials."))
    pages.append(psu_page(6, T, "".join(p), '<div class="goodluck">GOODLUCK ☺</div>'))
    return "".join(pages)


# ================================================================= build
PAPERS = [
    dict(
        slug="12-major-exam-semester-181",
        title="CYS401 | Major Exam (Semester 181)",
        desc="The CYS401 major exam of semester 181 (Dr. Gabriela Mogos, 18 November 2018), laid out like the original paper and interactive: 12 MCQs, 4 true/false, the answer table and 3 essay questions with the instructor's answers.",
        chip="Semester 181",
        h1="Major Exam · Semester 181",
        notes=[
            "Source: the instructor's answer sheet (Dr. Gabriela Mogos, 18 November 2018, 70 minutes, 20 marks), laid out like the original paper.",
            "Pick an option and the answer table on page 4 fills itself in. <b>Check paper</b> marks Section A; the essays show the instructor's answers so you can mark yourself.",
        ],
        build=paper_181,
    ),
    dict(
        slug="13-quiz-1-semester-232",
        title="CYS401 | Quiz 1 (Semester 232)",
        desc="CYS401 Quiz 1 of semester 232 (Dr. Rabia Latif, 1 February 2024), laid out like the original paper and interactive: MCQs, CIA terms, the McCumber cube, SecSDLC and defense in depth.",
        chip="Semester 232",
        h1="Quiz 1 · Semester 232",
        notes=[
            "Source: a marked copy (Dr. Rabia Latif, 1 February 2024, sections 1242/1249, 5 marks). The answers here are corrected, not copied from the student.",
            "MCQs, the blanks and the McCumber labels are checked automatically; the SecSDLC and defense-in-depth answers show a model answer to mark yourself against.",
        ],
        build=paper_232,
    ),
    dict(
        slug="14-major-exam-a-term-unknown",
        title="CYS401 | Major Exam A (Term Unknown)",
        desc="A CYS401 major exam from an unknown term, laid out like the original paper and interactive: Triple DES, Caesar, CFB, NIST SP 800-18, data remanence, STRIDE, due care, padding, Playfair, transposition, Vigenère, Hill and CBC.",
        chip="Term unknown",
        h1="Major Exam A · Term unknown",
        notes=[
            "Source: photos of a marked copy (pages 2–7 of 7; the cover page wasn't photographed, so the term and instructor are unknown).",
            "Every cipher answer is computed and checked automatically. Written parts show a model answer and, where the marked copy lost marks, why.",
        ],
        build=paper_a,
    ),
    dict(
        slug="15-major-exam-b-term-unknown",
        title="CYS401 | Major Exam B (Term Unknown)",
        desc="A CYS401 major exam from an unknown term, laid out like the original paper and interactive: nested DES, Caesar, security plans, STRIDE with properties, padding, Playfair, Vigenère and CBC.",
        chip="Term unknown",
        h1="Major Exam B · Term unknown",
        notes=[
            "Source: photos of a blank copy (pages 2, 3, 5, 6 and 7 of 7). The cover and page 4 (Question 2 B–D, 3.5 marks) weren't photographed, so the paper is marked out of 16.5.",
            "It shares several questions with Major Exam C, so the two are probably versions of the same exam.",
        ],
        build=paper_b,
    ),
    dict(
        slug="16-major-exam-c-term-unknown",
        title="CYS401 | Major Exam C (Term Unknown)",
        desc="A CYS401 major exam from an unknown term, laid out like the original paper and interactive: Caesar, media sanitization, STRIDE with mitigations, ASP, classification, due care, Playfair, Hill and social engineering scenarios.",
        chip="Term unknown",
        h1="Major Exam C · Term unknown",
        notes=[
            "Source: photos of a marked copy (pages 2–6 of 6; the cover page wasn't photographed, so the term and instructor are unknown).",
            "The answers are corrected where the marked copy lost marks, and each one explains what the marker was looking for.",
        ],
        build=paper_c,
    ),
]


def main():
    for p in PAPERS:
        out = EXAMS / p["slug"] / (p["slug"].split("-", 1)[1] + ".html")
        out.parent.mkdir(parents=True, exist_ok=True)
        page = shell(p["slug"], p["title"], p["desc"], p["chip"], intro(p["h1"], p["notes"]), p["build"]())
        out.write_text(page, encoding="utf-8")
        print("wrote", out.relative_to(ROOT))


if __name__ == "__main__":
    main()
