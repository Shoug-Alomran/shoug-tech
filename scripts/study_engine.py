#!/usr/bin/env python3
"""Turn one teaching file (scripts/study_content/<course>/NN-name.md) into study pages.

A file holds everything for one deck: a plain-language lesson per concept, the slide
map, a cheat sheet and the question bank. From it this module renders the slide
breakdown, the mind map data, the cheat sheet and the quiz bank.

File layout:
    @head Lecture 3            @title Recurrences
    @sources slide-folder-1, slide-folder-2
    @count 35                  (slides in the deck)
    @tldr one sentence         @why why anyone should care
    @connect how it links to what came before and after
    @vocab ... @map ... (rows until the next directive)
    ## Lesson title | Slides 3-7 | must      (must, know or skim)
    prose in Markdown, plus blocks written ::name argument ... ::
    @cheat ### Column / - item
    @mcq 7 / question / + right / - wrong x3 / > why
    @short 7 / question / ~ key, words / > model answer

Blocks: analogy, example, steps, mnemonic, trap, tip, why, says, class, formula,
check, key, code, plot, graph.
"""
import html
import json
import math
import os
import re

import markdown

import build_se371_breakdowns as breakdown

EMOJI = re.compile("[\U0001F300-\U0001FAFF☀-⛿✀-➿️]")
KEEP_SYMBOLS = set("✓✗")
ALLOWED_TAGS = r"/?(?:sub|sup|br|strong|em|mark|kbd)\b"


# ---------------------------------------------------------------- markdown ---

def guard(text):
    """Escape a stray < (as in f(n) < g(n)) everywhere except inside backticks."""
    parts = re.split(r"(`[^`\n]*`)", text)
    for i in range(0, len(parts), 2):
        parts[i] = re.sub(r"<(?!%s)" % ALLOWED_TAGS, "&lt;", parts[i])
    return "".join(parts)


def spaced(text):
    """Python-Markdown needs a blank line before a list or a table; authors do not."""
    out, previous = [], ""
    for line in text.split("\n"):
        starts = re.match(r"\s*(?:[-*]|\d+\.)\s", line) is not None
        table = line.lstrip().startswith("|")
        was_list = re.match(r"\s*(?:[-*]|\d+\.)\s", previous) is not None
        was_table = previous.lstrip().startswith("|")
        if previous.strip() and ((starts and not was_list) or (table and not was_table)):
            out.append("")
        out.append(line)
        previous = line
    return "\n".join(out)


def md(text):
    rendered = markdown.markdown(spaced(guard(text)), extensions=["tables", "sane_lists"], output_format="html")
    return rendered.replace("<table>", '<div class="table-wrap"><table>').replace("</table>", "</table></div>")


def inline(text):
    rendered = md(text).strip()
    return rendered[3:-4] if rendered.startswith("<p>") and rendered.endswith("</p>") and rendered.count("<p>") == 1 else rendered


def plain(text):
    text = re.sub(r"<[^>]+>", "", md(text))
    return html.unescape(" ".join(text.split()))


# ---------------------------------------------------------------- diagrams ---

def catmull(points):
    path = "M%.1f %.1f" % points[0]
    for i in range(len(points) - 1):
        p0 = points[i - 1] if i else points[0]
        p1, p2 = points[i], points[i + 1]
        p3 = points[i + 2] if i + 2 < len(points) else p2
        c1 = (p1[0] + (p2[0] - p0[0]) / 6, p1[1] + (p2[1] - p0[1]) / 6)
        c2 = (p2[0] - (p3[0] - p1[0]) / 6, p2[1] - (p3[1] - p1[1]) / 6)
        path += " C%.1f %.1f %.1f %.1f %.1f %.1f" % (*c1, *c2, *p2)
    return path


def pairs(text):
    return [tuple(float(v) for v in chunk.split(",")) for chunk in text.split()]


def plot(arg, body):
    """Axes with lines, curves, areas, guides and labelled points; colours are --c1..--c8."""
    title, xlabel, ylabel, xmax, ymax = [p.strip() for p in arg.split("|")]
    xmax, ymax = float(xmax), float(ymax)
    W, H, L, R, T, B = 540, 340, 58, 74, 18, 50
    sx = lambda x: L + (W - L - R) * x / xmax
    sy = lambda y: H - B - (H - T - B) * y / ymax
    out, top = [], []
    def text(x, y, s, cls="pl", anchor="start"):
        top.append('<text x="%.1f" y="%.1f" class="%s" text-anchor="%s">%s</text>' % (x, y, cls, anchor, html.escape(s)))
    for raw in body:
        line = raw.strip()
        if not line:
            continue
        m = re.match(r"(line|curve|dash)\s+(.*?)\s+(\d)\s*:\s*(.+)$", line)
        if m:
            kind, name, colour, pts = m.groups()
            points = [(sx(x), sy(y)) for x, y in pairs(pts)]
            d = catmull(points) if kind == "curve" else "M" + " L".join("%.1f %.1f" % p for p in points)
            dash = ' stroke-dasharray="6 5"' if kind == "dash" else ""
            out.append('<path d="%s" fill="none" stroke="var(--c%s)" stroke-width="2.6"%s/>' % (d, colour, dash))
            if name != "-":
                ex, ey = points[-1]
                anchor = "end" if ex > W - R + 40 else "start"
                top.append('<text x="%.1f" y="%.1f" class="pn" fill="var(--c%s)" text-anchor="%s">%s</text>'
                           % (ex + 6, ey + 4, colour, anchor, html.escape(name)))
            continue
        m = re.match(r"fn\s+(.*?)\s+(\d)\s*:\s*(.+)$", line)
        if m:
            name, colour, expr = m.groups()
            scope = {k: getattr(math, k) for k in ("log", "log2", "sqrt", "exp", "pi", "sin", "cos")}
            pts = []
            for k in range(1, 161):
                x = xmax * k / 160
                y = eval(expr, {"__builtins__": {}}, {**scope, "x": x})  # noqa: S307 - author-written formula
                if y > ymax:
                    break
                pts.append((sx(x), sy(y)))
            out.append('<path d="M%s" fill="none" stroke="var(--c%s)" stroke-width="2.6"/>'
                       % (" L".join("%.1f %.1f" % p for p in pts), colour))
            ex, ey = pts[-1]
            top.append('<text x="%.1f" y="%.1f" class="pn" fill="var(--c%s)">%s</text>' % (ex + 5, ey + 4, colour, html.escape(name)))
            continue
        m = re.match(r"area\s+(.*?)\s+(\d)\s*:\s*(.+)$", line)
        if m:
            name, colour, pts = m.groups()
            points = [(sx(x), sy(y)) for x, y in pairs(pts)]
            out.insert(0, '<polygon points="%s" fill="var(--c%s)" opacity="0.28"/>'
                       % (" ".join("%.1f,%.1f" % p for p in points), colour))
            if name != "-":
                cx = sum(p[0] for p in points) / len(points)
                cy = sum(p[1] for p in points) / len(points)
                text(cx, cy + 4, name, "pa", "middle")
            continue
        m = re.match(r"guide\s+([\d.]+),([\d.]+)$", line)
        if m:
            x, y = float(m.group(1)), float(m.group(2))
            out.append('<path d="M%.1f %.1f L%.1f %.1f L%.1f %.1f" fill="none" stroke="var(--text3)" stroke-dasharray="4 4"/>'
                       % (sx(x), sy(0), sx(x), sy(y), sx(0), sy(y)))
            continue
        m = re.match(r"dot\s*(.*?):\s*([\d.]+),([\d.]+)$", line)
        if m:
            label, x, y = m.group(1).strip(), float(m.group(2)), float(m.group(3))
            top.append('<circle cx="%.1f" cy="%.1f" r="5" fill="var(--accent)"/>' % (sx(x), sy(y)))
            if label:
                text(sx(x) + 8, sy(y) - 8, label, "pn")
            continue
        m = re.match(r"text\s+(.*?):\s*([\d.]+),([\d.]+)$", line)
        if m:
            text(sx(float(m.group(2))), sy(float(m.group(3))), m.group(1), "pa", "middle")
            continue
        m = re.match(r"ticks\s+([xy]):\s*(.+)$", line)
        if m:
            axis = m.group(1)
            for pair in m.group(2).split():
                value, label = pair.split("=", 1)
                value = float(value)
                label = label.replace("_", " ")
                if axis == "x":
                    text(sx(value), H - B + 18, label, "pt", "middle")
                else:
                    text(L - 7, sy(value) + 4, label, "pt", "end")
            continue
        raise SystemExit("plot: cannot read line: " + line)
    axes = ('<path d="M%d %d V%d H%d" fill="none" stroke="var(--text3)" stroke-width="1.6"/>' % (L, T, H - B, W - R))
    text((L + W - R) / 2, H - 10, xlabel, "pl", "middle")
    top.append('<text transform="translate(16 %.1f) rotate(-90)" class="pl" text-anchor="middle">%s</text>'
               % ((T + H - B) / 2, html.escape(ylabel)))
    return ('<figure class="diagram"><svg viewBox="0 0 %d %d" role="img" aria-label="%s">%s%s%s</svg>'
            '<figcaption>%s</figcaption></figure>' % (W, H, html.escape(title, quote=True), axes, "".join(out), "".join(top), inline(title)))


def graph(arg, body):
    """Boxes or circles joined by lines. Node: n id x y label [*|~]. Edge: e a b label [*|~]."""
    parts = [p.strip() for p in arg.split("|")]
    caption, directed = parts[0], len(parts) > 1 and parts[1] == "directed"
    nodes, edges = {}, []
    for raw in body:
        line = raw.strip()
        if not line:
            continue
        mark = ""
        if line.endswith((" *", " ~")):
            line, mark = line[:-2].rstrip(), line[-1]
        bits = line.split(None, 4 if line.startswith("n ") else 3)
        if bits[0] == "n":
            label = bits[4] if len(bits) > 4 else bits[1]
            rows = label.split("\\n")
            wide = max(len(r) for r in rows)
            box = wide > 3 or len(rows) > 1
            nodes[bits[1]] = dict(x=float(bits[2]), y=float(bits[3]), rows=rows, mark=mark, box=box,
                                  w=wide * 8.0 + 26 if box else 42, h=len(rows) * 18 + 16 if box else 42)
        elif bits[0] == "e":
            edges.append((bits[1], bits[2], bits[3] if len(bits) > 3 else "", mark))
        else:
            raise SystemExit("graph: cannot read line: " + line)
    x0 = min(n["x"] - n["w"] / 2 for n in nodes.values()) - 14
    x1 = max(n["x"] + n["w"] / 2 for n in nodes.values()) + 14
    y0 = min(n["y"] - n["h"] / 2 for n in nodes.values()) - 14
    y1 = max(n["y"] + n["h"] / 2 for n in nodes.values()) + 14

    def rim(a, b):
        dx, dy = b["x"] - a["x"], b["y"] - a["y"]
        length = math.hypot(dx, dy) or 1
        if a["box"]:
            scale = min(a["w"] / 2 / (abs(dx) or 1e-6), a["h"] / 2 / (abs(dy) or 1e-6))
        else:
            scale = a["w"] / 2 / length
        return a["x"] + dx * scale, a["y"] + dy * scale

    uid = abs(hash(caption + str(sorted(nodes)))) % 10 ** 8
    out = ('<defs><marker id="a%d" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">'
           '<path d="M0 0L10 5L0 10z" fill="var(--text3)"/></marker><marker id="b%d" viewBox="0 0 10 10" refX="9" refY="5" '
           'markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0 0L10 5L0 10z" fill="var(--accent)"/></marker></defs>'
           % (uid, uid))
    for a, b, label, mark in edges:
        p, q = nodes[a], nodes[b]
        x1e, y1e = rim(p, q)
        x2e, y2e = rim(q, p)
        hot = mark == "*"
        stroke = "var(--accent)" if hot else "var(--text3)"
        width = 3 if hot else 1.6
        dash = ' stroke-dasharray="5 5"' if mark == "~" else ""
        arrow = ' marker-end="url(#%s%d)"' % ("b" if hot else "a", uid) if directed else ""
        out += '<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="%s" stroke-width="%s"%s%s/>' % (x1e, y1e, x2e, y2e, stroke, width, dash, arrow)
        if label:
            mx, my = (x1e + x2e) / 2, (y1e + y2e) / 2
            w = len(label) * 7.6 + 8
            out += ('<rect x="%.1f" y="%.1f" width="%.1f" height="18" rx="3" fill="var(--bg2)"/>'
                    '<text x="%.1f" y="%.1f" class="gl" text-anchor="middle">%s</text>'
                    % (mx - w / 2, my - 9, w, mx, my + 4, html.escape(label)))
    for node in nodes.values():
        hot, muted = node["mark"] == "*", node["mark"] == "~"
        fill = "color-mix(in srgb, var(--accent) 24%, var(--bg3))" if hot else "var(--bg3)"
        stroke = "var(--accent)" if hot else "var(--border2)"
        opacity = ' opacity="0.55"' if muted else ""
        if node["box"]:
            out += '<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" rx="7" fill="%s" stroke="%s" stroke-width="1.6"%s/>' % (
                node["x"] - node["w"] / 2, node["y"] - node["h"] / 2, node["w"], node["h"], fill, stroke, opacity)
        else:
            out += '<circle cx="%.1f" cy="%.1f" r="21" fill="%s" stroke="%s" stroke-width="1.6"%s/>' % (node["x"], node["y"], fill, stroke, opacity)
        first = node["y"] - (len(node["rows"]) - 1) * 9 + 5
        for i, row in enumerate(node["rows"]):
            out += '<text x="%.1f" y="%.1f" class="gn" text-anchor="middle">%s</text>' % (node["x"], first + i * 18, html.escape(row))
    w, h = x1 - x0, y1 - y0
    return ('<figure class="diagram"><svg viewBox="%.1f %.1f %.1f %.1f" style="max-width:min(100%%,%dpx)" role="img" aria-label="%s">%s</svg>'
            '<figcaption>%s</figcaption></figure>' % (x0, y0, w, h, int(w * 1.25), html.escape(caption, quote=True), out, inline(caption)))


# ------------------------------------------------------------------ blocks ---

NOTE_LABEL = {
    "analogy": "Think of it like this", "mnemonic": "Memory trick", "tip": "Exam tip", "why": "Why it matters",
    "class": "Noted in class", "trap": "Exam trap", "says": "What the slide really means",
}
GRID_KINDS = {"analogy", "mnemonic", "tip", "why", "class"}


def note(kind, title, body):
    head = "<h4>%s</h4>" % inline(title) if title else ""
    return '<div class="note n-%s"><div class="note-tag">%s</div>%s%s</div>' % (kind, NOTE_LABEL[kind], head, md("\n".join(body)))


def split_blocks(lines):
    blocks, buffer, i = [], [], 0
    while i < len(lines):
        m = re.match(r"::(\w+)\s*(.*)$", lines[i])
        if not m:
            buffer.append(lines[i])
            i += 1
            continue
        if buffer:
            blocks.append(("text", "", buffer))
            buffer = []
        name, arg = m.group(1), m.group(2).strip()
        i += 1
        body = []
        while i < len(lines) and lines[i].strip() != "::":
            body.append(lines[i])
            i += 1
        if i >= len(lines):
            raise SystemExit("block never closed: ::" + name)
        i += 1
        blocks.append((name, arg, body))
    if buffer:
        blocks.append(("text", "", buffer))
    return [b for b in blocks if b[0] != "text" or "".join(b[2]).strip()]


def render_block(name, arg, body):
    text = "\n".join(body)
    if name == "text":
        return '<div class="prose">%s</div>' % md(text)
    if name in NOTE_LABEL:
        return note(name, arg, body)
    if name == "example":
        return '<div class="worked"><div class="note-tag">Worked example</div><h4>%s</h4>%s</div>' % (inline(arg), md(text))
    if name == "steps":
        items = [re.sub(r"^\s*\d+\.\s*", "", b) for b in body if b.strip()]
        return ('<div class="worked"><div class="note-tag">Step by step</div><h4>%s</h4><ol class="stepper">%s</ol></div>'
                % (inline(arg), "".join("<li>%s</li>" % inline(i) for i in items)))
    if name == "formula":
        rows = "".join('<div class="f-line">%s</div>' % inline(b) for b in body if b.strip())
        cap = '<div class="f-cap">%s</div>' % inline(arg) if arg else ""
        return '<div class="formula">%s%s</div>' % (cap, rows)
    if name == "check":
        return '<details class="try"><summary><span>Try it</span>%s</summary><div>%s</div></details>' % (inline(arg), md(text))
    if name == "key":
        items = [re.sub(r"^\s*-\s*", "", b) for b in body if b.strip()]
        return '<div class="remember"><div class="note-tag">Remember</div><ul>%s</ul></div>' % "".join("<li>%s</li>" % inline(i) for i in items)
    if name == "code":
        return ('<div class="code-block"><div class="code-head"><span class="code-file">%s</span></div><pre>%s</pre></div>'
                % (html.escape(arg or "code"), html.escape(text.strip("\n"))))
    if name == "plot":
        return plot(arg, body)
    if name == "graph":
        return graph(arg, body)
    raise SystemExit("unknown block ::" + name)


def render_blocks(blocks):
    out, run = [], []
    def flush():
        if len(run) > 1:
            out.append('<div class="note-grid">%s</div>' % "".join(run))
        elif run:
            out.append(run[0])
        run.clear()
    for name, arg, body in blocks:
        html_part = render_block(name, arg, body)
        if name in GRID_KINDS:
            run.append(html_part)
        else:
            flush()
            out.append(html_part)
    flush()
    return "\n".join(out)


# ------------------------------------------------------------------ parser ---

SINGLE = {"head", "title", "sources", "count", "tldr", "why", "connect"}
BLOCKS = {"vocab", "map", "goals", "cheat", "mcq", "short"}


def parse(path):
    with open(path, encoding="utf-8") as f:
        lines = f.read().split("\n")
    deck = {"lessons": [], "vocab": [], "map": [], "goals": [], "cheat": [], "mcq": [], "short": [],
            "path": path, "slug": os.path.basename(path)[:-3]}
    i = 0
    while i < len(lines):
        line = lines[i]
        m = re.match(r"@(\w+)\s*(.*)$", line)
        lesson = re.match(r"## (.+)$", line)
        if lesson or (m and m.group(1) in BLOCKS):
            j = i + 1
            while j < len(lines) and not re.match(r"## |@(?:%s)\b" % "|".join(SINGLE | BLOCKS), lines[j]):
                j += 1
            chunk = lines[i + 1:j]
            if lesson:
                bits = [p.strip() for p in lesson.group(1).split("|")]
                bits += [""] * (3 - len(bits))
                deck["lessons"].append({"title": bits[0], "slides": bits[1], "level": bits[2] or "know", "blocks": split_blocks(chunk)})
            else:
                read_block(deck, m.group(1), m.group(2).strip(), chunk)
            i = j
            continue
        if m and m.group(1) in SINGLE:
            deck[m.group(1)] = m.group(2).strip()
        elif line.strip() and not line.startswith("#!"):
            raise SystemExit("%s:%d: stray line: %s" % (path, i + 1, line))
        i += 1
    validate(deck)
    return deck


def read_block(deck, name, arg, chunk):
    rows = [l for l in chunk if l.strip()]
    if name in ("vocab", "map"):
        deck[name] = [[p.strip() for p in r.split("|")] for r in rows]
    elif name == "goals":
        deck["goals"] = [re.sub(r"^\s*-\s*", "", r) for r in rows]
    elif name == "cheat":
        for row in rows:
            if row.startswith("### "):
                deck["cheat"].append((row[4:].strip(), []))
            else:
                deck["cheat"][-1][1].append(re.sub(r"^\s*-\s*", "", row))
    elif name == "mcq":
        item = {"slide": arg, "q": rows[0], "correct": None, "wrong": [], "why": ""}
        for row in rows[1:]:
            if row.startswith("+ "):
                item["correct"] = row[2:].strip()
            elif row.startswith("- "):
                item["wrong"].append(row[2:].strip())
            elif row.startswith("> "):
                item["why"] = row[2:].strip()
            else:
                item["q"] += "\n" + row
        deck["mcq"].append(item)
    elif name == "short":
        item = {"slide": arg, "q": rows[0], "keywords": [], "answer": ""}
        for row in rows[1:]:
            if row.startswith("~ "):
                item["keywords"] = [k.strip() for k in row[2:].split(",")]
            elif row.startswith("> "):
                item["answer"] = row[2:].strip()
            else:
                item["q"] += "\n" + row
        deck["short"].append(item)


def validate(deck):
    where = deck["path"]
    for key in ("head", "title", "sources", "count", "tldr", "why"):
        if key not in deck:
            raise SystemExit("%s: missing @%s" % (where, key))
    if not deck["lessons"]:
        raise SystemExit(where + ": no lessons")
    raw = open(where, encoding="utf-8").read()
    bad = sorted({c for c in EMOJI.findall(raw) if c not in KEEP_SYMBOLS})
    if bad:
        raise SystemExit("%s: emoji found: %s" % (where, bad))
    for lesson in deck["lessons"]:
        keys = [b for b in lesson["blocks"] if b[0] == "key"]
        if not keys or len([x for x in keys[0][2] if x.strip()]) < 2:
            raise SystemExit("%s: lesson needs a ::key block: %s" % (where, lesson["title"]))
        if lesson["level"] not in ("must", "know", "skim"):
            raise SystemExit("%s: bad level on %s" % (where, lesson["title"]))
    for item in deck["mcq"]:
        if item["correct"] is None or len(item["wrong"]) != 3 or not item["why"]:
            raise SystemExit("%s: incomplete question: %s" % (where, item["q"]))
    for item in deck["short"]:
        if not item["keywords"] or not item["answer"]:
            raise SystemExit("%s: incomplete written question: %s" % (where, item["q"]))


# --------------------------------------------------------------- breakdown ---

EXTRA_CSS = r"""
.prose p, .prose ul, .prose ol { font-size: 1rem; line-height: 1.72; }
.prose ul, .prose ol { margin: 0 0 1rem 1.2rem; }
.prose li { margin-bottom: .4rem; }
.prose strong { color: var(--text); }
.lesson-meta { display: flex; flex-wrap: wrap; gap: .45rem; margin: -.3rem 0 1.1rem; }
.pill { font-family: 'JetBrains Mono', monospace; font-size: .68rem; letter-spacing: .06em; text-transform: uppercase; padding: .22rem .6rem; border-radius: 99px; border: 1px solid var(--border2); color: var(--text2); }
.pill.must { color: var(--c5); border-color: color-mix(in srgb, var(--c5) 55%, transparent); background: color-mix(in srgb, var(--c5) 12%, transparent); }
.pill.know { color: var(--c2); border-color: color-mix(in srgb, var(--c2) 55%, transparent); background: color-mix(in srgb, var(--c2) 12%, transparent); }
.pill.skim { color: var(--text3); }
.tldr { font-size: 1.16rem; line-height: 1.6; color: var(--text); padding: 1.15rem 1.3rem; border-radius: 12px; background: color-mix(in srgb, var(--sec) 13%, var(--bg2)); border: 1px solid color-mix(in srgb, var(--sec) 40%, transparent); margin-bottom: 1.2rem; }
.tldr b { display: block; font-family: 'JetBrains Mono', monospace; font-size: .7rem; letter-spacing: .1em; text-transform: uppercase; color: var(--sec); margin-bottom: .4rem; font-weight: 700; }
.start-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(min(100%, 20rem), 1fr)); gap: .9rem; margin-bottom: 1.1rem; }
.start-item { padding: 1rem 1.15rem; border: 1px solid var(--border); border-radius: 12px; background: var(--bg2); }
.start-item h4 { margin: 0 0 .4rem; color: var(--sec); font-size: .92rem; }
.start-item p, .start-item ul { margin-bottom: 0; font-size: .95rem; }
.start-item ul { margin-left: 1.1rem; }
.slide-links { display: flex; flex-wrap: wrap; gap: .5rem; margin: .4rem 0 1.2rem; }
.slide-links a { font-family: 'JetBrains Mono', monospace; font-size: .74rem; padding: .45rem .8rem; border: 1px solid var(--accent); color: var(--accent); border-radius: 7px; text-decoration: none; }
.slide-links a:hover { background: var(--accent); color: var(--bg); }
.note, .worked, .remember, .formula { margin: 1rem 0; border-radius: 12px; }
.note { padding: 1rem 1.15rem; border: 1px solid var(--tone-line); background: var(--tone-bg); --tone: var(--c2); --tone-line: color-mix(in srgb, var(--tone) 42%, transparent); --tone-bg: color-mix(in srgb, var(--tone) 10%, var(--bg2)); }
.note h4 { margin: 0 0 .4rem; font-size: 1.02rem; color: var(--text); }
.note p:last-child, .note ul:last-child, .note ol:last-child { margin-bottom: 0; }
.note p, .note li { font-size: .96rem; line-height: 1.66; }
.note ul, .note ol { margin-left: 1.15rem; }
.note-tag { font-family: 'JetBrains Mono', monospace; font-size: .67rem; letter-spacing: .1em; text-transform: uppercase; font-weight: 700; color: var(--tone, var(--sec)); margin-bottom: .45rem; }
.n-analogy { --tone: var(--c2); } .n-mnemonic { --tone: var(--c7); } .n-tip { --tone: var(--c3); } .n-why { --tone: var(--c6); } .n-class { --tone: var(--c8); } .n-says { --tone: var(--c1); } .n-trap { --tone: var(--c5); }
.n-mnemonic h4 { font-family: 'JetBrains Mono', monospace; letter-spacing: .08em; color: var(--c7); font-size: 1.12rem; }
.note-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(min(100%, 19rem), 1fr)); gap: .9rem; margin: 1rem 0; }
.note-grid > .note { margin: 0; }
.worked { padding: 1.1rem 1.25rem; border: 1px solid var(--border2); background: var(--bg2); border-left: 3px solid var(--c4); --tone: var(--c4); }
.worked h4 { margin: 0 0 .65rem; font-size: 1.06rem; color: var(--text); }
.worked p:last-child, .worked ol:last-child, .worked ul:last-child { margin-bottom: 0; }
.worked p, .worked li { font-size: .97rem; line-height: 1.66; }
.worked ol:not(.stepper), .worked ul { margin-left: 1.2rem; }
.stepper { list-style: none; counter-reset: st; margin: 0; }
.stepper li { counter-increment: st; position: relative; padding: 0 0 .75rem 2.5rem; margin: 0; }
.stepper li:last-child { padding-bottom: 0; }
.stepper li::before { content: counter(st); position: absolute; left: 0; top: 0; width: 1.65rem; height: 1.65rem; border-radius: 50%; display: grid; place-items: center; font-family: 'JetBrains Mono', monospace; font-size: .76rem; font-weight: 700; color: var(--bg); background: var(--c4); }
.stepper li::after { content: ''; position: absolute; left: .79rem; top: 1.75rem; bottom: .1rem; width: 2px; background: var(--border2); }
.stepper li:last-child::after { display: none; }
.formula { padding: .95rem 1.15rem; background: var(--code-bg); border: 1px solid var(--border2); text-align: center; }
.f-cap { font-family: 'JetBrains Mono', monospace; font-size: .68rem; letter-spacing: .1em; text-transform: uppercase; color: var(--text3); margin-bottom: .5rem; }
.f-line { font-family: 'JetBrains Mono', monospace; font-size: 1.04rem; color: var(--text); line-height: 1.75; overflow-wrap: anywhere; }
.remember { padding: 1rem 1.2rem; border: 1px dashed color-mix(in srgb, var(--sec) 55%, transparent); --tone: var(--sec); }
.remember ul { margin: 0 0 0 1.1rem; }
.remember li { margin-bottom: .32rem; font-size: .95rem; }
.remember li:last-child { margin-bottom: 0; }
details.try { margin: .8rem 0; border: 1px solid var(--border2); border-radius: 10px; background: var(--bg2); }
details.try summary { cursor: pointer; padding: .8rem 1rem; font-weight: 600; color: var(--text); font-size: .97rem; list-style: none; }
details.try summary::-webkit-details-marker { display: none; }
details.try summary span { font-family: 'JetBrains Mono', monospace; font-size: .66rem; letter-spacing: .08em; text-transform: uppercase; color: var(--bg); background: var(--c3); padding: .14rem .45rem; border-radius: 4px; margin-right: .6rem; vertical-align: 1px; }
details.try summary:hover { color: var(--accent); }
details.try > div { padding: 0 1rem .9rem; border-top: 1px solid var(--border); padding-top: .75rem; }
details.try p:last-child, details.try ul:last-child { margin-bottom: 0; }
.diagram { margin: 1.1rem 0; text-align: center; }
.diagram svg { width: 100%; max-width: 40rem; height: auto; }
.diagram figcaption { font-size: .82rem; color: var(--text3); margin-top: .35rem; }
.diagram text { font-family: 'JetBrains Mono', monospace; }
.pl { fill: var(--text2); font-size: 13px; } .pt { fill: var(--text3); font-size: 12px; } .pn { fill: var(--text); font-size: 13.5px; font-weight: 700; } .pa { fill: var(--text); font-size: 13px; }
.gn { fill: var(--text); font-size: 13.5px; font-weight: 600; } .gl { fill: var(--text2); font-size: 12px; }
.table-wrap td, .table-wrap th { white-space: normal; }
.roundup .note { margin: .8rem 0; }
@media print { .topbar, .toc-rail, #progress { display: none !important; } .layout { display: block; } details.try > div { display: block; } }
"""


def breakdown_sections(deck, ctx):
    links = "".join('<a href="%s" target="_top">Open the slides: %s &rarr;</a>' % (url, html.escape(name))
                    for name, url in ctx["slide_links"])
    tiles = []
    if deck.get("connect"):
        tiles.append('<div class="start-item"><h4>Where this fits</h4><p>%s</p></div>' % inline(deck["connect"]))
    if deck["goals"]:
        tiles.append('<div class="start-item"><h4>By the end you can</h4><ul>%s</ul></div>'
                     % "".join("<li>%s</li>" % inline(g) for g in deck["goals"]))
    intro = ('<div class="tldr"><b>In one sentence</b>%s</div><div class="prose">%s</div>' % (inline(deck["tldr"]), md(deck["why"])))
    if tiles:
        intro += '<div class="start-grid">%s</div>' % "".join(tiles)
    intro += '<div class="slide-links">%s</div>' % links
    if deck["vocab"]:
        rows = "".join("<tr><td><strong>%s</strong></td><td>%s</td></tr>" % (inline(a), inline(b)) for a, b in deck["vocab"])
        intro += ('<h3>Words you need first</h3><div class="table-wrap"><table><thead><tr><th>Term</th>'
                  '<th>In plain English</th></tr></thead><tbody>%s</tbody></table></div>' % rows)
    sections = [{"id": "start", "nav": "Start Here", "label": "Read this first", "title": "The big picture", "html": intro}]
    slide_rows = ctx.get("slide_map") or deck["map"]
    if slide_rows:
        sections.append({"id": "map", "nav": "Slide Map", "label": "Navigation", "title": "Where to spend your time",
                         "html": breakdown_slidemap(slide_rows)})
    traps, tricks = [], []
    level_name = {"must": "Must know", "know": "Good to know", "skim": "Just skim"}
    for n, lesson in enumerate(deck["lessons"], 1):
        pills = '<span class="pill %s">%s</span>' % (lesson["level"], level_name[lesson["level"]])
        if lesson["slides"]:
            pills += '<span class="pill">%s</span>' % html.escape(lesson["slides"])
        sections.append({"id": "lesson-%d" % n, "nav": html.escape(lesson["title"]), "label": "Lesson %d" % n,
                         "title": inline(lesson["title"]),
                         "html": '<div class="lesson-meta">%s</div>%s' % (pills, render_blocks(lesson["blocks"]))})
        for name, arg, body in lesson["blocks"]:
            if name == "trap":
                traps.append(note("trap", arg, body))
            elif name == "mnemonic":
                tricks.append(note("mnemonic", arg, body))
    if traps:
        sections.append({"id": "traps", "nav": "Exam Traps", "label": "Marks lost here", "title": "Every trap in one place",
                         "html": '<div class="note-grid roundup">%s</div>' % "".join(traps)})
    if tricks:
        sections.append({"id": "tricks", "nav": "Memory Tricks", "label": "Make it stick", "title": "Every memory trick in one place",
                         "html": '<div class="note-grid roundup">%s</div>' % "".join(tricks)})
    columns = cheat_columns(deck, ctx)
    if columns:
        sections.append({"id": "cheat", "nav": "Quick Reference", "label": "One screen", "title": "Quick reference",
                         "html": cheat_html(columns)})
    return sections


def breakdown_slidemap(rows):
    from se371_breakdown_content import slidemap
    return slidemap([(html.escape(a), inline(b), w, inline(c)) for a, b, w, c in rows])


def cheat_columns(deck, ctx):
    return deck["cheat"] or ctx.get("cheat") or []


def cheat_html(columns):
    return '<div class="cheat">%s</div>' % "".join(
        '<div class="cheat-col"><h4>%s</h4><ul>%s</ul></div>' % (inline(t), "".join("<li>%s</li>" % inline(i) for i in items))
        for t, items in columns)


def render_breakdown(deck, ctx):
    """ctx: code, name, base (breakdowns URL), num, slug, file, slide_links, quiz, section path, optional cheat."""
    words = sum(len(" ".join(b[2]).split()) for lesson in deck["lessons"] for b in lesson["blocks"])
    minutes = max(5, round(words / 190))
    chapter = {
        "num": ctx["num"], "slug": ctx["slug"], "file": ctx["file"], "title": deck["title"],
        "desc": "%s %s explained in plain language with examples and memory tricks: %s" % (ctx["code"], deck["head"], plain(deck["tldr"])),
        "sub": "The slides explained in plain language, with examples, memory tricks and practice questions.",
        "stats": ["%s slides" % deck["count"], deck["head"], "%d lessons" % len(deck["lessons"]), "%d min read" % minutes],
        "sections": breakdown_sections(deck, ctx), "quiz": ctx["quiz"],
    }
    breakdown.BASE = ctx["base"]
    text = breakdown.render_content(chapter)
    label = "%s %s" % (ctx["code"], ctx["name"])
    text = text.replace("SE371 // CH%02d" % ctx["num"], "%s // %s" % (ctx["code"], deck["head"].upper()))
    text = text.replace("Chapter %02d &middot; Slide Breakdown" % ctx["num"], "%s &middot; Slide Breakdown" % deck["head"])
    text = text.replace("SE371 Web Engineering &mdash; Chapter %02d" % ctx["num"], "%s &mdash; %s" % (label, deck["head"]))
    text = text.replace("SE371 Web Engineering", label).replace("SE371", ctx["code"]).replace("se371", ctx["code"].lower())
    return text.replace("</style>", EXTRA_CSS + "</style>", 1)


# ----------------------------------------------------------------- derived ---

def branches(deck):
    """(name, summary, facts, examples) per lesson: the shape mind maps and quizzes use."""
    out = []
    for lesson in deck["lessons"]:
        summary, facts, examples = "", [], []
        for name, arg, body in lesson["blocks"]:
            text = "\n".join(body)
            if name == "text" and not summary:
                summary = plain(text.split("\n\n")[0])
            elif name == "key":
                facts = [plain(re.sub(r"^\s*-\s*", "", b)) for b in body if b.strip()]
            elif name in ("analogy", "mnemonic", "example") and len(examples) < 3:
                snippet = plain(text)
                examples.append((plain(arg) or NOTE_LABEL.get(name, "Example"), snippet[:320] + ("…" if len(snippet) > 320 else "")))
        out.append((plain(lesson["title"]), summary or facts[0], facts, examples))
    return out


def plain_trap_titles(deck):
    return [plain(arg) for lesson in deck["lessons"] for name, arg, _ in lesson["blocks"] if name == "trap" and arg]


CHEAT_PAGE = """<!DOCTYPE html>
<html lang="en" data-theme="dark" data-sg-styled="true">
<head>
<link rel="icon" type="image/png" sizes="256x256" href="/assets/shoug-favicon-v4.png">
<meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title><meta name="description" content="{desc}"><link rel="canonical" href="{canonical}">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;600;700&display=swap" rel="stylesheet">
<style>{style}{extra}
.sheet {{ padding: clamp(.8rem, 2.4vw, 2rem); }}
.sheet h2 {{ font-size: 1.15rem; margin: 1.6rem 0 .7rem; color: var(--accent); }}
.sheet h2:first-of-type {{ margin-top: 0; }}
.sheet-head {{ display: flex; flex-wrap: wrap; justify-content: space-between; gap: .6rem; align-items: center; padding: clamp(.8rem, 2.4vw, 2rem) clamp(.8rem, 2.4vw, 2rem) 0; }}
.sheet-head h1 {{ margin: 0; font-size: clamp(1.25rem, 3vw, 2rem); }}
.sheet-head small {{ display: block; color: var(--text3); font-family: 'JetBrains Mono', monospace; font-size: .72rem; letter-spacing: .08em; text-transform: uppercase; margin-bottom: .25rem; }}
.sheet-actions {{ display: flex; gap: .4rem; }}
@media (max-width: 640px) {{ :root {{ --gutter: .5rem; }} .sheet {{ padding: .4rem; }} }}
@media print {{ .sheet-actions {{ display: none; }} :root {{ --bg: #fff; }} .cheat-col {{ break-inside: avoid; }} }}
</style></head>
<body>
<header class="sheet-head"><div><small>{eyebrow}</small><h1>{heading}</h1></div>
<div class="sheet-actions"><button class="toggle-btn" type="button" onclick="window.print()">Print</button><button class="toggle-btn" id="theme-btn" type="button">Light</button></div></header>
<main class="sheet">{body}</main>
<script>
(function(){{var r=document.documentElement,b=document.getElementById('theme-btn');
function a(t){{r.setAttribute('data-theme',t);try{{localStorage.setItem('shoug-theme',t);localStorage.setItem('theme',t)}}catch(e){{}}b.textContent=t==='dark'?'Light':'Dark'}}
var s=null;try{{s=localStorage.getItem('shoug-theme')||localStorage.getItem('theme')}}catch(e){{}}a(s==='light'?'light':'dark');
b.addEventListener('click',function(){{a(r.getAttribute('data-theme')==='dark'?'light':'dark')}})}})();
</script>
<script src="/javascripts/standalone-theme.js"></script><script src="/javascripts/html-theme-sync.js"></script>
</body></html>
"""


def cheat_page(title, heading, eyebrow, desc, canonical, body):
    return CHEAT_PAGE.format(title=html.escape(title), desc=html.escape(desc, quote=True), canonical=canonical,
                             style=breakdown.STYLE, extra=EXTRA_CSS, eyebrow=html.escape(eyebrow),
                             heading=html.escape(heading), body=body)


def quiz_json(item, tag, options):
    opts, answer = options(item)
    esc = lambda s: html.escape(s, quote=False)
    return {"tag": tag, "q": esc(item["q"]), "opts": [esc(o) for o in opts], "a": answer, "why": esc(item["why"])}


def json_dump(value):
    return json.dumps(value, ensure_ascii=False, indent=2)
