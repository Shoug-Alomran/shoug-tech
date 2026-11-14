#!/usr/bin/env python3
"""Build the final exam cheat sheets from plain-text content files.

    python3 scripts/build_final_cheat_sheets.py [cys401 cs331 se423 se322]

Each course has one content file, scripts/final_cheat_sheets/<course>.txt, and
gets docs/academics/<path>/extra-resources/final-exam-cheat-sheet/
final-exam-cheat-sheet.html. The wrapper index.html beside it is created once
from WRAPPER_FROM (another page in the same folder) and then left alone, so
sidebar stamping and hand edits survive rebuilds. Styling lives in
docs/styles/final-cheat-sheet.css, behaviour in docs/javascripts/final-cheat-sheet.js.

Content file format
-------------------
Header lines (before the first "=="):
    @code CYS401            @course Fundamentals of Cybersecurity
    @path cybersecurity/cys401
    @brand Final            (pill after the course code in the top bar)
    @description ...        (meta description)
    @h1 Final exam | cheat sheet   (text after | gets the gradient)
    @lede ...               (hero paragraph; may repeat, one <p> each)
    @stat 10 | chapters | 190      (number | label | hue)
    @legend 300 | Title | text     (hue | title | text)
    @footer ...

Body:
    == id | hue | tab label | badge | Heading     starts a section
    > text                  section intro paragraph
    ### Heading             sub heading
    [grid] / [grid wide] ... [/grid]
    [card Title] / [card full Title] ... [/card]  (Title may contain inline marks)
    [table] rows "a | b | c", first row is the header [/table]
    [calc] preformatted text, kept exactly [/calc]
    [qs] question cards [/qs]:
        ? SOURCE :: question stem     (SOURCE "practice" gets the dashed chip)
        - option                       (options, lettered a, b, c ...)
        = the right answer
        + explanation line (as many as needed)
    [check] "count | text" lines [/check]       recite list
    [ready key] one statement per line [/ready] ticks saved in localStorage
    [chips] "label | url" or "label" lines, "*label" = highlighted [/chips]
    !trap text   !tip text   !hook text         callouts
    - bullet     1. numbered                    lists
    anything else is a paragraph.

Inline: **bold**, __gradient keyword__, `code`, {{mono source}}, [[label|url]].
Text is HTML-escaped first, so write <, > and & literally.
"""
import html
import os
import re
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONTENT = os.path.join(REPO, "scripts", "final_cheat_sheets")
SITE = "https://shoug-tech.com"
FOLDER = "final-exam-cheat-sheet"

# An existing single-page wrapper in each course's extra-resources folder,
# copied once to make the new wrapper.
WRAPPER_FROM = {
    "cys401": "chapters-1-5-cheat-sheet",
    "cs331": "major-1-cheat-sheet",
    "se423": "midterm-cheat-sheet",
    "se322": "diagram-guide",
}


def esc(s):
    return html.escape(s, quote=True)


def inline(s):
    s = esc(s)
    s = re.sub(r"\[\[(.+?)\|(.+?)\]\]", r'<a href="\2">\1</a>', s)
    s = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", s)
    s = re.sub(r"__(.+?)__", r'<span class="kw">\1</span>', s)
    s = re.sub(r"`(.+?)`", r"<code>\1</code>", s)
    s = re.sub(r"\{\{(.+?)\}\}", r'<span class="mono">\1</span>', s)
    return s


def cells(line):
    line = line.strip()
    if line.endswith("|"):
        line = line[:-1]
    return [c.strip() for c in line.split("|")]


class Page:
    def __init__(self, name, text):
        self.name = name
        self.meta = {"lede": [], "stat": [], "legend": []}
        self.sections = []  # (id, hue, tab, badge, heading, html)
        self.parse(text)

    # ---------- parsing ----------
    def parse(self, text):
        lines = text.split("\n")
        i = 0
        while i < len(lines) and not lines[i].startswith("=="):
            ln = lines[i].strip()
            if ln.startswith("@"):
                key, _, val = ln[1:].partition(" ")
                if key in self.meta and isinstance(self.meta[key], list):
                    self.meta[key].append(val.strip())
                else:
                    self.meta[key] = val.strip()
            i += 1
        cur = None
        buf = []
        for ln in lines[i:]:
            if ln.startswith("=="):
                if cur:
                    self.sections.append(cur + (self.body(buf),))
                parts = cells(ln[2:])
                while len(parts) < 5:
                    parts.append("")
                cur = tuple(parts[:5])
                buf = []
            else:
                buf.append(ln)
        if cur:
            self.sections.append(cur + (self.body(buf),))

    def body(self, lines):
        out = []
        para = []  # pending list items
        list_kind = None

        def flush():
            nonlocal para, list_kind
            if para:
                tag = "ol" if list_kind == "ol" else "ul"
                out.append("<%s>%s</%s>" % (tag, "".join("<li>%s</li>" % inline(p) for p in para), tag))
            para, list_kind = [], None

        i = 0
        n = len(lines)
        while i < n:
            raw = lines[i]
            ln = raw.strip()
            i += 1
            if not ln:
                flush()
                continue
            m = re.match(r"\[(calc|table|qs|check|ready|chips)\b ?(.*)\]$", ln)
            if m:
                flush()
                kind, arg = m.group(1), m.group(2).strip()
                block = []
                while i < n and lines[i].strip() != "[/%s]" % kind:
                    block.append(lines[i])
                    i += 1
                i += 1
                out.append(getattr(self, "blk_" + kind)(block, arg))
                continue
            m = re.match(r"\[(grid|card)\b ?(.*)\]$", ln)
            if m:
                flush()
                kind, arg = m.group(1), m.group(2).strip()
                if kind == "grid":
                    out.append('<div class="grid%s">' % (" wide" if arg == "wide" else ""))
                else:
                    full = arg.startswith("full")
                    title = arg[4:].strip() if full else arg
                    out.append('<div class="card%s">' % (" full" if full else ""))
                    if title:
                        out.append("<h4>%s</h4>" % inline(title))
                continue
            if ln in ("[/grid]", "[/card]"):
                flush()
                out.append("</div>")
                continue
            if ln.startswith("== "):
                continue
            if ln.startswith(">"):
                flush()
                out.append('<p class="ch-intro">%s</p>' % inline(ln[1:].strip()))
            elif ln.startswith("### "):
                flush()
                out.append("<h3>%s</h3>" % inline(ln[4:]))
            elif re.match(r"!(trap|tip|hook) ", ln):
                flush()
                kind, _, txt = ln[1:].partition(" ")
                out.append('<div class="%s">%s</div>' % (kind, inline(txt)))
            elif ln.startswith("- "):
                if list_kind == "ol":
                    flush()
                list_kind = "ul"
                para.append(ln[2:])
            elif re.match(r"\d+\. ", ln):
                if list_kind == "ul":
                    flush()
                list_kind = "ol"
                para.append(re.sub(r"^\d+\. ", "", ln))
            else:
                flush()
                out.append("<p>%s</p>" % inline(ln))
        flush()
        return "\n".join(out)

    def blk_calc(self, block, arg):
        while block and not block[0].strip():
            block.pop(0)
        while block and not block[-1].strip():
            block.pop()
        indent = min((len(b) - len(b.lstrip()) for b in block if b.strip()), default=0)
        text = "\n".join(b[indent:] for b in block)
        return '<pre class="calc">%s</pre>' % esc(text)

    def blk_table(self, block, arg):
        rows = [cells(b) for b in block if b.strip()]
        if not rows:
            return ""
        head = "".join("<th>%s</th>" % inline(c) for c in rows[0])
        body = "".join("<tr>%s</tr>" % "".join("<td>%s</td>" % inline(c) for c in r) for r in rows[1:])
        return '<div class="tbl"><table><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>' % (head, body)

    def blk_qs(self, block, arg):
        qs = []
        for b in block:
            ln = b.strip()
            if not ln:
                continue
            if ln.startswith("? "):
                src, _, stem = ln[2:].partition("::")
                qs.append({"src": src.strip(), "stem": stem.strip(), "opts": [], "ans": [], "why": []})
            elif not qs:
                continue
            elif ln.startswith("- "):
                qs[-1]["opts"].append(ln[2:])
            elif ln.startswith("= "):
                qs[-1]["ans"].append(ln[2:])
            elif ln.startswith("+ "):
                qs[-1]["why"].append(ln[2:])
            else:
                qs[-1]["stem"] += " " + ln
        out = ['<div class="qs">']
        for q in qs:
            practice = q["src"].lower().startswith("practice")
            out.append('<div class="q"><span class="src%s">%s</span>' % (" practice" if practice else "", esc(q["src"])))
            out.append('<p class="stem">%s</p>' % inline(q["stem"]))
            if q["opts"]:
                out.append('<ol class="opts">%s</ol>' % "".join("<li>%s</li>" % inline(o) for o in q["opts"]))
            ans = "".join('<span class="right">%s</span>' % inline(a) for a in q["ans"])
            why = "".join("<p>%s</p>" % inline(w) for w in q["why"])
            out.append('<details><summary>Answer</summary><div class="ans">%s%s</div></details></div>' % (ans, why))
        out.append("</div>")
        return "\n".join(out)

    def blk_check(self, block, arg):
        items = []
        for b in block:
            if not b.strip():
                continue
            cnt, _, txt = b.strip().partition("|")
            items.append("<li><b>%s</b><span>%s</span></li>" % (esc(cnt.strip()), inline(txt.strip())))
        return '<ul class="checklist">%s</ul>' % "".join(items)

    def blk_ready(self, block, arg):
        items = [b.strip() for b in block if b.strip()]
        key = arg or "ready"
        meter = ('<div class="ready-meter"><span class="n">0 / %d</span><span class="bar"><i></i></span>'
                 '<button type="button">Reset</button></div>' % len(items))
        lis = "".join('<li><label><input type="checkbox" /><span>%s</span></label></li>' % inline(t) for t in items)
        return '%s<ul class="ready" data-key="%s">%s</ul>' % (meter, esc(key), lis)

    def blk_chips(self, block, arg):
        out = []
        for b in block:
            ln = b.strip()
            if not ln:
                continue
            hot = ln.startswith("*")
            ln = ln.lstrip("*").strip()
            label, _, url = ln.partition("|")
            cls = "chip hot" if hot else "chip"
            if url.strip():
                out.append('<a class="%s" href="%s">%s</a>' % (cls, esc(url.strip()), inline(label.strip())))
            else:
                out.append('<span class="%s">%s</span>' % (cls, inline(label.strip())))
        return '<div class="chips">%s</div>' % "".join(out)

    # ---------- rendering ----------
    def url(self):
        return "%s/academics/%s/extra-resources/%s/" % (SITE, self.meta["path"], FOLDER)

    def render(self):
        m = self.meta
        code = m["code"]
        title = "%s | Final Exam Cheat Sheet" % code
        desc = m.get("description", "")
        h1a, _, h1b = m.get("h1", "Final exam | cheat sheet").partition("|")
        tabs = "\n".join(
            '<a href="#%s" style="--hue: %s"><span class="n">%02d</span>%s</a>' % (sid, hue, k, esc(tab))
            for k, (sid, hue, tab, badge, head, body) in enumerate(self.sections)
        )
        stats = "".join(
            '<div class="stat" style="--hue: %s"><b>%s</b>%s</div>' % (esc(c[2] if len(c) > 2 else "262"), esc(c[0]), esc(c[1]))
            for c in map(cells, m["stat"])
        )
        legend = "".join(
            '<div style="--hue: %s"><b>%s</b>%s</div>' % (esc(c[0]), inline(c[1]), inline(c[2]))
            for c in map(cells, m["legend"])
        )
        lede = "".join("<p>%s</p>" % inline(p) for p in m["lede"])
        secs = []
        for k, (sid, hue, tab, badge, head, body) in enumerate(self.sections):
            secs.append(
                '<section class="chapter" id="%s" style="--hue: %s">\n<div class="ch-head"><span class="ch-num">%s</span>'
                "<h2>%s</h2></div>\n%s\n</section>" % (sid, hue, esc(badge or "%02d" % k), inline(head), body)
            )
        return TEMPLATE.format(
            title=esc(title), desc=esc(desc), url=self.url(), code=esc(code), brand=esc(m.get("brand", "Final")),
            tabs=tabs, course=esc(m.get("course", "")), h1a=inline(h1a.strip()), h1b=inline(h1b.strip()),
            lede=lede, stats=stats, legend=legend, sections="\n".join(secs), footer=inline(m.get("footer", "")),
            key="final-cheat-" + self.name,
        )


TEMPLATE = """<!doctype html>
<html lang="en" data-sg-styled data-ready-key="{key}">
<head>
<link rel="icon" type="image/png" sizes="256x256" href="/assets/shoug-favicon-v4.png" />
<link rel="shortcut icon" type="image/png" href="/assets/shoug-favicon-v4.png" />
<link rel="apple-touch-icon" sizes="180x180" href="/assets/shoug-apple-touch-icon-v4.png" />
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
<title>{title}</title>
<meta name="description" content="{desc}" />
<link rel="canonical" href="{url}" />
<meta property="og:title" content="{title}" />
<meta property="og:description" content="{desc}" />
<meta property="og:url" content="{url}" />
<meta property="og:type" content="website" />
<meta property="og:image" content="https://shoug-tech.com/assets/og-banner.png" />
<meta name="twitter:card" content="summary_large_image" />
<link rel="preconnect" href="https://fonts.googleapis.com" />
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
<link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,500;9..144,650&family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500;600&display=swap" rel="stylesheet" />
<script src="/javascripts/html-theme-sync.js"></script>
<link rel="stylesheet" href="/styles/final-cheat-sheet.css?v=2" />
<link rel="stylesheet" href="/styles/site-shell.css" />
<script defer src="/javascripts/site-palette.js"></script>
</head>
<body>
<header class="topbar">
<div class="progress" aria-hidden="true"></div>
<div class="wrap topbar-row">
<a class="brand" href="#top">{code} <span>{brand}</span></a>
<div class="actions">
<div data-page-search-host></div>
<button class="btn primary" type="button" id="toggle-answers">Show all <span class="long">answers</span></button>
<button class="btn" type="button" onclick="toggleTheme()"><span data-theme-label>Dark</span></button>
</div>
</div>
<nav class="wrap tabs" aria-label="Sections">
{tabs}
</nav>
</header>
<main class="wrap" id="top">
<div class="hero">
<div class="hero-bg" aria-hidden="true"><span class="blob b1"></span><span class="blob b2"></span><span class="blob b3"></span></div>
<div>
<div class="eyebrow">{code} · {course}</div>
<h1>{h1a} <span class="grad-text">{h1b}</span></h1>
{lede}
<div class="stats">{stats}</div>
</div>
<div class="legend">{legend}</div>
</div>
{sections}
<footer>{footer}</footer>
</main>
<script src="/javascripts/final-cheat-sheet.js?v=1"></script>
</body>
</html>
"""


TRACKS = {
    "computer-science": "Computer Science",
    "cybersecurity": "Cybersecurity",
    "software-engineering": "Software Engineering",
    "other-courses": "Other Courses",
    "information-system": "Information Systems",
}
# Template wrapper per track: the cybersecurity pages use the red cyber palette
# (cyber-track.css + red --brand-purple), every other track uses the purple one.
GENERIC_FROM = {"cybersecurity": ("cybersecurity/cys401", "CYS401")}
GENERIC_DEFAULT = ("software-engineering/se423", "SE423")


def make_generic_wrapper(page):
    """Courses without a single-page wrapper of their own reuse another course's final wrapper.

    Header `@prev <url>` sets the PREVIOUS link (the item listed before this sheet);
    without it the link is disabled. The sidebar is restamped afterwards by
    build_academic_sidebar.py, so the copied sidebar never survives."""
    path, code = page.meta["path"], page.meta["code"]
    track = path.split("/")[0]
    src_path, src_code = GENERIC_FROM.get(track, GENERIC_DEFAULT)
    src = open(os.path.join(REPO, "docs", "academics", src_path, "extra-resources", FOLDER, "index.html"),
               encoding="utf-8").read()
    src_track = src_path.split("/")[0]
    out = re.sub(r'(href="/academics/)%s(/"\s*>)%s(</a)' % (src_track, re.escape(TRACKS[src_track])),
                 lambda m: m.group(1) + track + m.group(2) + TRACKS.get(track, track) + m.group(3), src)
    out = out.replace("/academics/" + src_path + "/", "/academics/%s/" % path)
    out = out.replace(src_code, code)
    desc = esc(page.meta.get("description", ""))
    old_desc = re.search(r'<meta\s+name="description"\s+content="([^"]*)"', src).group(1)
    out = out.replace(old_desc, desc)
    prev = page.meta.get("prev")
    m = re.search(r'<a\s+href="[^"]*"\s+class="nav-link prev"\s*>&lt;- PREVIOUS</a\s*>', out)
    if m:
        link = ('<a href="%s" class="nav-link prev">&lt;- PREVIOUS</a>' % prev if prev
                else '<span class="nav-link prev disabled">&lt;- PREVIOUS</span>')
        out = out[:m.start()] + link + out[m.end():]
    m = re.search(r'<a\s+href="[^"]*"\s+class="nav-link next"\s*>NEXT -&gt;</a\s*>', out)
    if m:
        out = out[:m.start()] + '<span class="nav-link next disabled">NEXT -&gt;</span>' + out[m.end():]
    return out


def make_wrapper(page, folder_dir):
    if page.name not in WRAPPER_FROM:
        return make_generic_wrapper(page)
    course_dir = os.path.dirname(folder_dir)
    src_name = WRAPPER_FROM[page.name]
    src = open(os.path.join(course_dir, src_name, "index.html"), encoding="utf-8").read()
    # find the old page title as shown in the wrapper's <title>
    old_title = re.search(r"<title>\s*(.*?)\s*</title>", src, re.S).group(1)
    old_label = old_title.split("|", 1)[1].strip() if "|" in old_title else old_title
    new_label = "Final Exam Cheat Sheet"
    out = src.replace("extra-resources/%s/" % src_name, "extra-resources/%s/" % FOLDER)
    # the iframe / open-in-new-tab target
    out = re.sub(r'(src|href)="\./[^"]+\.(html|pdf)"', r'\1="./%s.html"' % FOLDER, out)
    out = re.sub(r'(src|href)="(/academics/[^"]*/%s/)[^"/]+\.(html|pdf)"' % FOLDER, r'\1="\2%s.html"' % FOLDER, out)
    out = out.replace(old_title, "%s | %s" % (page.meta["code"], new_label))
    out = re.sub(r'(<h1 class="ch-title"[^>]*>)\s*.*?\s*(</h1>)', r"\g<1>%s\g<2>" % new_label, out, count=1, flags=re.S)
    desc = esc(page.meta.get("description", ""))
    out = re.sub(r'(<meta\s+name="description"\s+content=")[^"]*(")', r"\g<1>%s\g<2>" % desc, out)
    out = re.sub(r'(<meta\s+property="og:description"\s+content=")[^"]*(")', r"\g<1>%s\g<2>" % desc, out)
    out = re.sub(r'(<meta\s+name="twitter:description"\s+content=")[^"]*(")', r"\g<1>%s\g<2>" % desc, out)
    out = re.sub(r'("description":\s*")[^"]*(")', r"\g<1>%s\g<2>" % desc.replace("\\", ""), out)
    out = out.replace(old_label, new_label)
    return out


def build(name):
    text = open(os.path.join(CONTENT, name + ".txt"), encoding="utf-8").read()
    page = Page(name, text)
    folder_dir = os.path.join(REPO, "docs", "academics", page.meta["path"], "extra-resources", FOLDER)
    os.makedirs(folder_dir, exist_ok=True)
    target = os.path.join(folder_dir, FOLDER + ".html")
    with open(target, "w", encoding="utf-8") as f:
        f.write(page.render())
    wrapper = os.path.join(folder_dir, "index.html")
    made = ""
    if not os.path.exists(wrapper):
        with open(wrapper, "w", encoding="utf-8") as f:
            f.write(make_wrapper(page, folder_dir))
        made = " (+ wrapper)"
    print("[ok] %s -> %s%s" % (name, os.path.relpath(target, REPO), made))


def main():
    names = sys.argv[1:] or sorted(f[:-4] for f in os.listdir(CONTENT) if f.endswith(".txt"))
    for n in names:
        build(n)


if __name__ == "__main__":
    main()
