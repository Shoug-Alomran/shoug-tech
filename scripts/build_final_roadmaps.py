#!/usr/bin/env python3
"""Build the final exam roadmaps from scripts/final_roadmaps/<course>.json.

    python3 scripts/build_final_roadmaps.py [se322 ...]

Writes docs/academics/<path>/extra-resources/final-roadmap/final-roadmap.html:
  01 Route: zoom levels from "why" down to the code. Each level holds topic groups;
     each group lists its chapter material (quiz, mind map, listing vault, cheat-sheet
     section) and its topics, and each topic links the exact lectures (breakdown,
     slides, annotated slides) and labs/diagram examples to study, plus a four-step
     status (not started, reviewed, can explain, tested myself).
  02 Look-alikes: confusable concepts side by side, the question that separates
     them, what to study, and a quick test.
  03 Past papers: full papers to finish with.
Statuses are saved in this browser (localStorage). The page has its own design in
the site's terminal style (docs/styles/final-roadmap.css, docs/javascripts/final-roadmap.js),
deliberately separate from the cheat sheets. The wrapper index.html is copied once
from the course's final-exam-cheat-sheet wrapper; the course overview links to it
from TARGET_METADATA. Every linked page is checked on disk and missing ones are reported.
"""
import html
import json
import os
import re
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(REPO, "scripts", "final_roadmaps")
SITE = "https://shoug-tech.com"
FOLDER = "final-roadmap"
SEG = ["—", "Read", "Explain", "Tested"]
SEG_TITLE = ["Not started", "Reviewed", "Can explain it", "Tested myself"]


def esc(s):
    return html.escape(s, quote=True)


class Page:
    def __init__(self, d):
        self.d = d
        self.course = "/academics/%s/" % d["path"]
        self.missing = []

    def url(self, rel):
        u = self.course + rel
        disk = os.path.join(REPO, "docs", u.lstrip("/").split("#")[0])
        if not (os.path.isfile(os.path.join(disk, "index.html")) or os.path.isfile(disk)):
            self.missing.append(u)
        return u

    def chip(self, kind, label, url, hot=False):
        return '<a class="rm-chip%s" href="%s" target="_top"><span>%s</span>%s</a>' % (
            " hot" if hot else "", esc(url), esc(kind), esc(label))

    def study(self, keys):
        out = []
        for k in keys:
            if k in self.d["lectures"]:
                # [name, breakdown, slides, annotated, slides-with-notes]; any but the name may be null
                lec = list(self.d["lectures"][k]) + [None] * 5
                name, bd, sl, an, nt = lec[:5]
                if bd:
                    out.append(self.chip("Breakdown", name, self.url(self.rel("slide-breakdowns", bd)), hot=True))
                if sl:
                    out.append(self.chip("Slides", name, self.url(self.rel("slides", sl))))
                if an:
                    out.append(self.chip("Annotated", name, self.url(self.rel("annotated-slides", an))))
                if nt:
                    out.append(self.chip("Notes", name, self.url(self.rel("slides-with-notes", nt))))
            elif k in self.d["extras"]:
                label, rel = self.d["extras"][k]
                kind, _, rest = label.partition(": ")
                out.append(self.chip(kind if rest else "Extra", rest or label, self.url(rel)))
            else:
                raise KeyError("unknown study key %r" % k)
        return "".join(out)

    def chapter_chips(self, ch):
        c = self.d["chapters"][ch]
        out = []
        for q in ([c["quiz"]] if isinstance(c.get("quiz"), str) else c.get("quiz") or []):
            out.append(self.chip("Quiz", c["name"], self.url(q), hot=True))
        if c.get("mindmap"):
            out.append(self.chip("Mind map", c["name"], self.url(self.rel("extra-resources/mindmaps", c["mindmap"]))))
        if c.get("vault"):
            out.append(self.chip("Listing vault", c["name"], self.url(self.rel("extra-resources/listing-vault", c["vault"]))))
        if c.get("cheat"):
            cheat = self.url("extra-resources/final-exam-cheat-sheet/") + "final-exam-cheat-sheet.html#" + c["cheat"]
            out.append(self.chip("Cheat sheet", c["name"], cheat))
        return "".join(out)

    @staticmethod
    def rel(folder, value):
        """A bare slug lives in `folder`; anything with a slash is already a course-relative path."""
        return value if "/" in value else "%s/%s/" % (folder, value)

    def render(self):
        d = self.d
        levels, total = [], 0
        for i, lv in enumerate(d["levels"], 1):
            groups = []
            for g in lv["groups"]:
                rows = []
                for t in g["topics"]:
                    total += 1
                    seg = "".join(
                        '<label title="%s"><input type="radio" name="st-%s" value="%d"%s /><span>%s</span></label>'
                        % (SEG_TITLE[v], esc(t["id"]), v, " checked" if v == 0 else "", SEG[v]) for v in range(4))
                    rows.append(
                        '<li class="rm-topic" data-id="%s"><div class="rm-topic-main"><div class="rm-topic-text">'
                        '<b>%s</b><span>%s</span></div><div class="rm-seg" role="radiogroup" aria-label="Status: %s">%s</div></div>'
                        '<div class="rm-study"><span class="rm-k">Study</span>%s</div></li>'
                        % (esc(t["id"]), esc(t["name"]), esc(t.get("hint", "")), esc(t["name"]), seg, self.study(t["study"])))
                groups.append(
                    '<details class="rm-group"><summary><span class="rm-gname">%s</span><span class="rm-gch">%s</span>'
                    '<span class="rm-gbar"><i></i></span><span class="rm-gn">0 / %d</span></summary>'
                    '<div class="rm-gbody"><div class="rm-chapter"><span class="rm-k">Chapter material</span>%s</div>'
                    '<ul class="rm-topics">%s</ul></div></details>'
                    % (esc(g["name"]), esc(d["chapters"][g["chapter"]]["name"]), len(g["topics"]),
                       self.chapter_chips(g["chapter"]), "".join(rows)))
            levels.append(
                '<div class="rm-level"><div class="rm-rail"><span class="rm-dot">%02d</span></div><div class="rm-level-body">'
                '<div class="rm-level-head"><span class="rm-zoom">LVL_%02d // %s</span><h3>%s</h3></div>'
                '<div class="rm-groups">%s</div>%s</div></div>'
                % (i, i, esc(lv["zoom"].upper()), esc(lv["question"]), "".join(groups),
                   '<p class="rm-down">%s</p>' % esc(lv["down"]) if lv.get("down") else ""))
        confs = []
        for c in d["confusables"]:
            rows = "".join("<tr><td>%s</td><td>%s</td><td>%s</td></tr>" % tuple(esc(x) for x in r) for r in c["rows"])
            q, a = c["test"]
            confs.append(
                '<article class="rm-panel rm-conf"><h3>%s</h3><p class="rm-ask"><span class="rm-k">Ask yourself</span>%s</p>'
                '<div class="rm-table"><table><thead><tr><th>Concept</th><th>Tell-tale sign</th><th>Example</th></tr></thead>'
                '<tbody>%s</tbody></table></div><div class="rm-study"><span class="rm-k">Study</span>%s</div>'
                '<details class="rm-test"><summary><span class="rm-k">Quick test</span>%s</summary><p>%s</p></details></article>'
                % (esc(c["title"]), esc(c["ask"]), rows, self.study(c["study"]), esc(q), esc(a)))
        papers = "".join(self.chip("Past paper", n, self.url(u), hot=(k == 0)) for k, (n, u) in enumerate(d["papers"]))
        cheat_url = self.url("extra-resources/final-exam-cheat-sheet/")
        if d["papers"]:
            papers_intro = ("When most topics show Explain or Tested, do a full paper under time, then mark anything "
                            "you missed back down to Read and revisit its material.")
        else:
            papers_intro = ("There are no past papers on the site for this course yet. When most topics show Explain or "
                            "Tested, do the self-test at the end of the final exam cheat sheet as your practice paper.")
            papers = self.chip("Practice", "Cheat sheet self-test", cheat_url + "final-exam-cheat-sheet.html#test", hot=True)
        url = "%s%sextra-resources/%s/" % (SITE, self.course, FOLDER)
        return TEMPLATE.format(
            title=esc("%s | Final Roadmap" % d["code"]), desc=esc(d["description"]), url=url, code=esc(d["code"]),
            course=esc(d["course"]), lede=esc(d["lede"]), total=total, nlev=len(d["levels"]), nconf=len(d["confusables"]),
            levels="".join(levels), confs="".join(confs), papers=papers,
            cheat=cheat_url, papers_intro=papers_intro, key="final-roadmap-" + d["code"].lower())


TEMPLATE = """<!doctype html>
<html lang="en" data-sg-styled data-roadmap-key="{key}">
<head>
<link rel="icon" type="image/png" sizes="256x256" href="/assets/shoug-favicon-v4.png" />
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
<link rel="preconnect" href="https://fonts.googleapis.com" />
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=JetBrains+Mono:wght@400;500;700&family=Rajdhani:wght@500;600;700&display=swap" rel="stylesheet" />
<script src="/javascripts/html-theme-sync.js"></script>
<link rel="stylesheet" href="/styles/final-roadmap.css?v=4" />
</head>
<body>
<header class="rm-top">
<div class="rm-wrap rm-top-row">
<a class="rm-brand" href="#top">{code} <span>// FINAL_ROADMAP</span></a>
<div class="rm-meter" aria-label="Coverage"><span class="rm-meter-bar"><i class="m1"></i><i class="m2"></i><i class="m3"></i></span><span class="rm-meter-n">0%</span></div>
<div class="rm-actions"><div data-page-search-host></div><button class="rm-btn" type="button" onclick="toggleTheme()"><span data-theme-label>Dark</span></button></div>
</div>
<nav class="rm-wrap rm-nav" aria-label="Sections"><a href="#route">[ 01 ROUTE ]</a><a href="#lookalikes">[ 02 LOOK-ALIKES ]</a><a href="#papers">[ 03 PRACTICE ]</a></nav>
</header>
<main class="rm-wrap" id="top">
<section class="rm-hero">
<div class="rm-panel rm-intro">
<span class="rm-k">ROUTE_PLAN // {course}</span>
<h1>Final roadmap</h1>
<p>{lede}</p>
<ul class="rm-stats"><li><b>{nlev}</b>zoom levels</li><li><b>{total}</b>topics</li><li><b>{nconf}</b>look-alike groups</li></ul>
</div>
<aside class="rm-panel rm-cover">
<div class="rm-cover-head"><span class="rm-k">COVERAGE</span><div class="rm-barcode" aria-hidden="true"></div></div>
<div class="rm-big"><b class="rm-pct">0%</b><span>of the course tested</span></div>
<div class="rm-stack" aria-hidden="true"><i class="s1"></i><i class="s2"></i><i class="s3"></i></div>
<ul class="rm-legend">
<li><i class="s0"></i>Not started<b data-count="0">{total}</b></li>
<li><i class="s1"></i>Reviewed<b data-count="1">0</b></li>
<li><i class="s2"></i>Can explain<b data-count="2">0</b></li>
<li><i class="s3"></i>Tested myself<b data-count="3">0</b></li>
</ul>
<div class="rm-next"><span class="rm-k">NEXT_UP</span><a href="#route" data-next>Start at level 01</a></div>
<p class="rm-foot">Saved in this browser. <button type="button" class="rm-reset">Reset</button></p>
</aside>
</section>

<section id="route" class="rm-section">
<div class="rm-section-head"><span class="rm-k">01</span><h2>The route</h2><button type="button" class="rm-btn rm-expand">Expand all</button></div>
<p class="rm-section-intro">Each level answers a narrower question than the one above. Open a box to see its topics and exactly what to study. Mark each topic as you go: <b>Read</b> once you have been through the material, <b>Explain</b> when you can teach it without notes, <b>Tested</b> after answering quiz or past-paper questions on it.</p>
<div class="rm-route">{levels}</div>
</section>

<section id="lookalikes" class="rm-section">
<div class="rm-section-head"><span class="rm-k">02</span><h2>Look-alikes</h2></div>
<p class="rm-section-intro">These are the pairs and trios that get mixed up. The question under each title is the one that tells them apart.</p>
<div class="rm-confs">{confs}</div>
</section>

<section id="papers" class="rm-section">
<div class="rm-section-head"><span class="rm-k">03</span><h2>Finish with practice</h2></div>
<p class="rm-section-intro">{papers_intro}</p>
<div class="rm-study rm-papers">{papers}<a class="rm-chip" href="{cheat}" target="_top"><span>Review</span>Final exam cheat sheet</a></div>
</section>
<footer class="rm-footer">DATA_VERIFIED // Built from the course slides, breakdowns, labs and past papers. Shoug Alomran.</footer>
</main>
<script src="/javascripts/final-roadmap.js?v=2"></script>
</body>
</html>
"""


def make_wrapper(d, folder_dir):
    src = os.path.join(os.path.dirname(folder_dir), "final-exam-cheat-sheet", "index.html")
    out = open(src, encoding="utf-8").read()
    out = out.replace("final-exam-cheat-sheet.html", FOLDER + ".html")
    out = out.replace("extra-resources/final-exam-cheat-sheet/", "extra-resources/%s/" % FOLDER)
    out = out.replace("Final Exam Cheat Sheet", "Final Roadmap")
    old = re.search(r'<meta\s+name="description"\s+content="([^"]*)"', out).group(1)
    out = out.replace(old, esc(d["description"]))
    out = re.sub(r'ITEM_\d+ //', 'ROADMAP //', out, count=1)
    return out


def build(name):
    d = json.load(open(os.path.join(DATA, name + ".json"), encoding="utf-8"))
    page = Page(d)
    folder_dir = os.path.join(REPO, "docs", "academics", d["path"], "extra-resources", FOLDER)
    os.makedirs(folder_dir, exist_ok=True)
    with open(os.path.join(folder_dir, FOLDER + ".html"), "w", encoding="utf-8") as f:
        f.write(page.render())
    wrapper = os.path.join(folder_dir, "index.html")
    made = ""
    if not os.path.exists(wrapper):
        with open(wrapper, "w", encoding="utf-8") as f:
            f.write(make_wrapper(d, folder_dir))
        made = " (+ wrapper)"
    print("[ok] %s roadmap%s" % (name, made))
    for u in sorted(set(page.missing)):
        print("  [missing] %s" % u)


if __name__ == "__main__":
    for n in sys.argv[1:] or sorted(f[:-5] for f in os.listdir(DATA) if f.endswith(".json")):
        build(n)
