#!/usr/bin/env python3
"""Build the study sections of CS311, IS321 and ECON101 from scripts/study_content/.

Writes slide breakdowns, mind maps, cheat sheets, practice quizzes, mock exams, the
section listings and the Annotated Slides "coming soon" page. Run
build_new_courses.py first. Edit the teaching files, not the HTML.

    .venv/bin/python scripts/build_course_study.py            # every course
    .venv/bin/python scripts/build_course_study.py cs311      # one course
"""
import glob
import hashlib
import html
import json
import os
import random
import re
import shutil
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import build_new_courses as nc  # noqa: E402
import build_se401_study_tools as tools  # noqa: E402
import build_slide_hub as hub  # noqa: E402
import study_engine as engine  # noqa: E402
from build_academic_sidebar import DATA_FILE  # noqa: E402

SITE = "https://shoug-tech.com"
CONTENT = os.path.join(nc.REPO, "scripts", "study_content")
LISTING_TEMPLATE = os.path.join(nc.DOCS, "academics/computer-science/cs316/exams/index.html")
FRAME_TEMPLATE = os.path.join(nc.TEMPLATE_DIR, "exams/02-chapter-2-quiz/index.html")
MAP_TEMPLATE = os.path.join(nc.DOCS, "academics/software-engineering/se322/extra-resources/mindmaps/"
                            "01-introduction-to-software-design-and-architecture/introduction-to-software-design-and-architecture.html")
FOLDER_ICON = (
    '<svg class="dir-folder-icon" style="width:18px;height:18px;vertical-align:-3px;margin-right:10px" viewBox="0 0 24 24" fill="none" '
    'stroke="currentColor" stroke-width="2" stroke-linecap="square" stroke-linejoin="square" aria-hidden="true">'
    '<path d="M3 7a1 1 0 0 1 1-1h5l2 2h9a1 1 0 0 1 1 1v9a1 1 0 0 1-1 1H4a1 1 0 0 1-1-1V7z"/></svg>'
)
KINDS = {
    "breakdown": ("slide-breakdowns/", "Slide Breakdowns", "", "SLIDE BREAKDOWNS", "", ".html"),
    "mindmap": ("extra-resources/mindmaps/", "Mind Maps", " Mind Map", "MIND MAPS", "", ".html"),
    "quiz": ("exams/", "Exams", " Quiz", "EXAMS", "-quiz", "-quiz.html"),
}
# One cheat sheet and one practice exam per real exam: (folder, name, deck numbers from the file
# names or None for all, practice questions per deck). Coverage comes from each syllabus; where a
# syllabus gives only a date (CS311, IS321, CS316), it is read off the weekly schedule.
EXAMS = {
    "CS311": [("major-1", "Major 1", (1, 2, 3, 4), 5),
              ("major-2", "Major 2", (5, 6, 7, 8), 5),
              ("final", "Final Exam", None, 3)],
    "IS321": [("major", "Major Exam", range(1, 10), 4),
              ("final", "Final Exam", None, 3)],
    # Chapters 1 and 2 were marked EXCLUDED in the course folder, so the final sheet leaves them out.
    "ECON101": [("major-1", "Major 1", (2, 3, 4), 8),
                ("major-2", "Major 2", (6, 8, 9), 8),
                ("final", "Final Exam", (3, 4, 5, 6, 8, 9, 11, 12, 13, 14), 3)],
    # No SE411 syllabus yet, so one sheet covers every chapter until exam coverage is known.
    "SE411": [("final", "Final Exam", None, 3)],
    "CS316": [("major", "Major Exam", (1, 2, 3, 4, 5, 10, 11, 12), 4),
              ("final", "Final Exam", None, 3)],
}
CHEAT_PATH = "extra-resources/cheat-sheets/"
# Single resources kept in Study Material next to the generated folders: (folder, title).
EXTRA_RESOURCES = {
    "ECON101": [("chapter-11-qamar-bakery-step-by-step", "Chapter 11 Worked Example: Qamar Bakery, Step by Step")],
}


def esc(text):
    return html.escape(text, quote=False)


def base_name(slug):
    return slug.split("-", 1)[1]


def options(item):
    opts = [item["correct"], *item["wrong"]]
    random.Random(hashlib.sha1(item["q"].encode()).hexdigest()).shuffle(opts)
    return opts, opts.index(item["correct"])


def spread(items, count):
    """count items spaced evenly through a list, so a sample covers the whole deck."""
    if len(items) <= count:
        return list(items)
    return [items[i * len(items) // count] for i in range(count)]


class Course:
    def __init__(self, c):
        self.c = c
        self.url = c["url"]
        self.out = nc.course_dir(c)
        folder = os.path.join(CONTENT, c["code"].lower())
        self.decks = [engine.parse(p) for p in sorted(glob.glob(os.path.join(folder, "*.md")))]
        self.titles = {slug: title for _s, slug, title, *_ in c["decks"]}

    def folder(self, kind, deck):
        return deck["slug"] + KINDS[kind][4]

    def file_name(self, kind, deck):
        return base_name(deck["slug"]) + KINDS[kind][5]

    def item_title(self, kind, deck):
        return "%s%s: %s" % (deck["head"], KINDS[kind][2], deck["title"])

    def href(self, kind, deck):
        return "%s%s%s/" % (self.url, KINDS[kind][0], self.folder(kind, deck)) if deck else None

    def slide_links(self, deck):
        out = []
        sources = [s.strip() for s in deck["sources"].split(",")]
        extras = dict(EXTRA_RESOURCES.get(self.c["code"], []))
        for slug in sources:
            if slug in extras:
                out.append(("Worked example", "%sextra-resources/%s/" % (self.url, slug)))
                continue
            if slug not in self.titles:
                raise SystemExit("%s: unknown slide folder %s" % (deck["path"], slug))
            title = self.titles[slug]
            match = re.search(r"\(([^)]*)\)$", title)
            name = match.group(1) if match and len(sources) > 1 else ("Course Slides" if len(sources) > 1 else deck["head"])
            if slug == sources[0] and len(sources) == 1:
                name = deck["head"]
            out.append((name, "%sslides/%s/" % (self.url, slug)))
        return out

    # ---- identity -------------------------------------------------------
    def set_identity(self, text, url, title, desc):
        text = re.sub(r"<link rel=\"canonical\"[^>]*>\s*", "", text)
        text = re.sub(r"<link rel=\"alternate\" hreflang=[^>]*>\s*", "", text)
        text = re.sub(r"<meta (?:property=\"og:[^\"]*\"|name=\"twitter:[^\"]*\"|name=\"description\")\s+content=\"[^\"]*\"\s*/?>\s*", "", text)
        text = re.sub(r"<script\s+type=\"application/ld\+json\">.*?</script>\s*", "", text, flags=re.S)
        text = re.sub(r"<title>.*?</title>", lambda _m: "<title>%s</title>" % esc(title), text, count=1, flags=re.S)
        ld = json.dumps({"@context": "https://schema.org", "@type": "WebPage", "url": url, "name": title, "description": desc}, ensure_ascii=False)
        tags = (
            '<link rel="canonical" href="{u}"><meta name="description" content="{d}">'
            '<meta property="og:title" content="{t}"><meta property="og:description" content="{d}">'
            '<meta property="og:url" content="{u}"><meta property="og:type" content="article">'
            '<meta property="og:image" content="{s}/assets/og-banner.png">'
            '<meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="{t}">'
            '<meta name="twitter:description" content="{d}"><meta name="twitter:image" content="{s}/assets/og-banner.png">'
            '<script type="application/ld+json">{l}</script>'
        ).format(u=url, d=html.escape(desc, quote=True), t=html.escape(title, quote=True), s=SITE, l=ld)
        return text.replace("</head>", tags + "</head>", 1)

    def identity_for(self, text, kind, deck):
        url = "%s%s%s%s/%s" % (SITE, self.url, KINDS[kind][0], self.folder(kind, deck), self.file_name(kind, deck))
        title = "%s %s | Shoug's Digital Garden" % (self.c["code"], self.item_title(kind, deck))
        desc = "%s %s, built from the %s lecture slides." % (self.c["code"], self.item_title(kind, deck), self.c["name"])
        return self.set_identity(text, url, title, desc)

    # ---- pages ----------------------------------------------------------
    def breakdown_page(self, i, deck):
        ctx = {
            "code": self.c["code"], "name": self.c["name"], "base": self.url + "slide-breakdowns/", "num": i,
            "slug": deck["slug"], "file": self.file_name("breakdown", deck), "slide_links": self.slide_links(deck),
            "quiz": [engine.quiz_json(m, deck["head"], options) for m in spread(deck["mcq"], 8)],
        }
        return engine.render_breakdown(deck, ctx)

    def map_tree(self, deck):
        def node(node_id, label, tag, desc, children=None):
            out = {"id": node_id, "label": label, "desc": '<span class="panel-tag">%s</span><p>%s</p>' % (tag, desc)}
            if children is not None:
                out["children"] = children
            return out
        branches = []
        for b, (name, summary, facts, examples) in enumerate(engine.branches(deck), 1):
            children = []
            for f, fact in enumerate(facts, 1):
                words = fact.rstrip(".").split()
                children.append(node("b%d-f%d" % (b, f), " ".join(words[:7]) + ("…" if len(words) > 7 else ""), "Key Detail", esc(fact)))
            if examples:
                children.append(node("b%d-ex" % b, "Examples", "Examples", "Ways to picture <strong>%s</strong>." % esc(name), [
                    node("b%d-ex%d" % (b, e), label, "Example", esc(text)) for e, (label, text) in enumerate(examples, 1)]))
            branches.append(node("b%d" % b, name, "Core Concept", esc(summary), children))
        root = "<strong>%s</strong>. Expand branches, select a node for detail, search topics, zoom, pan, or export the map." % esc(deck["title"])
        return {"id": "root", "label": deck["title"], "desc": '<span class="panel-tag">%s · %s</span><p>%s</p>' % (self.c["code"], deck["head"], root), "children": branches}

    def mindmap_page(self, deck):
        text = nc.read(MAP_TEMPLATE)
        block = re.compile(r"const DATA = \{.*?\n\s*\};(?=\n\n\s*// ─+\n\s*// STATE)", re.S)
        if not block.search(text):
            raise SystemExit("mind map template no longer matches")
        data = json.dumps(self.map_tree(deck), ensure_ascii=False, indent=2).replace("</", "<\\/")
        text = block.sub(lambda _m: "const DATA = " + data + ";", text, count=1)
        text = re.sub(r"Moral\s+Systems,\s+Ethical\s+Concepts,\s+and\s+Theories", deck["title"], text)
        text = re.sub(r"Introduction\s+to\s+Software\s+Design\s+and\s+Architecture", deck["title"], text)
        return engine.with_theme_assets(self.identity_for(text.replace("SE322", self.c["code"]), "mindmap", deck))

    def cheat_columns(self, deck):
        columns = list(deck["cheat"])
        traps = engine.plain_trap_titles(deck)
        if traps:
            columns.append(("Do not fall for", traps))
        return columns

    def exam_cheat_page(self, folder, name, numbers):
        decks = self.mock_decks(numbers)
        url = "%s%s%s%s/%s-cheat-sheet.html" % (SITE, self.url, CHEAT_PATH, folder, folder)
        title = "%s %s Cheat Sheet" % (self.c["code"], name)
        body = "".join("<h2>%s: %s</h2>%s" % (esc(d["head"]), esc(d["title"]), engine.cheat_html(self.cheat_columns(d)))
                       for d in decks if d["cheat"])
        scope = ", ".join(d["head"] for d in decks)
        return engine.cheat_page(title, "%s Cheat Sheet" % name, "%s // %s" % (self.c["code"], scope),
                                 "%s, covering %s." % (title, scope), url, body)

    def write_cheats(self, data):
        """Every cheat sheet belongs to one exam, so this folder is rebuilt from EXAMS each time."""
        root = os.path.join(self.out, CHEAT_PATH)
        if os.path.isdir(root):
            shutil.rmtree(root)
        exams = EXAMS[self.c["code"]]
        href = lambda e: "%s%s%s/" % (self.url, CHEAT_PATH, e[0]) if e else None
        rows = ""
        for i, exam in enumerate(exams, 1):
            folder, name, numbers, _ = exam
            target = os.path.join(root, folder)
            nc.write(os.path.join(target, folder + "-cheat-sheet.html"), self.exam_cheat_page(folder, name, numbers))
            nc.write(os.path.join(target, "index.html"), self.frame_page(
                href(exam), CHEAT_PATH, "Cheat Sheets", "CHEAT SHEETS", i, "%s Cheat Sheet" % name, folder + "-cheat-sheet.html",
                href(exams[i - 2]) if i > 1 else None, href(exams[i]) if i < len(exams) else None, data))
            rows += self.row(href(exam), i, "%s Cheat Sheet" % name)
        self.listing(data, CHEAT_PATH, "Cheat Sheets", "أوراق المراجعة", rows, active="extra-resources/")

    def exam_text(self, i, title, head, bank, branches):
        tools.QUIZ_BANK = {i: bank}
        text = tools.exam_html(i, title, branches)
        text = re.sub(r"SE401 · CHAPTER %d\b" % i, "%s · %s" % (self.c["code"], head.upper()), text)
        text = re.sub(r"SE401 · Chapter %d\b" % i, "%s · %s" % (self.c["code"], head), text)
        text = re.sub(r"SE401 Chapter %d\b" % i, "%s %s" % (self.c["code"], head), text)
        path = self.url.strip("/").replace("academics/", "", 1)
        text = text.replace("software-engineering/se401", path)
        return engine.with_theme_assets(text.replace("SE401", self.c["code"]).replace("se401", self.c["code"].lower()))

    @staticmethod
    def bank(mcqs, shorts):
        return {"mcq": [(m["q"], m["correct"], m["wrong"], m["why"]) for m in mcqs],
                "short": [(s["q"], s["keywords"], s["answer"]) for s in shorts]}

    def quiz_page(self, i, deck):
        text = self.exam_text(i, deck["title"], deck["head"], self.bank(deck["mcq"], deck["short"]), engine.branches(deck))
        return self.identity_for(text, "quiz", deck)

    def mock_decks(self, numbers):
        if numbers is None:
            return self.decks
        wanted = set(numbers)
        return [d for d in self.decks if int(d["slug"].split("-", 1)[0]) in wanted]

    def mock_page(self, i, folder, title, numbers, per_deck):
        decks = self.mock_decks(numbers)
        mcqs = [m for d in decks for m in spread(d["mcq"], per_deck)]
        shorts = [s for d in decks for s in spread(d["short"], 1)]
        branches = [b for d in decks for b in engine.branches(d)]
        text = self.exam_text(i, title, title, self.bank(mcqs, shorts), branches)
        url = "%s%sexams/%s/%s.html" % (SITE, self.url, folder, folder)
        return self.set_identity(text, url, "%s %s | Shoug's Digital Garden" % (self.c["code"], title),
                                 "%s %s drawn from every covered lecture of %s." % (self.c["code"], title, self.c["name"]))

    # ---- wrappers and listings -----------------------------------------
    def frame_page(self, url, path, section, upper, i, title, raw, prev_url, next_url, data):
        t = nc.rebrand(nc.read(FRAME_TEMPLATE), self.c)
        t = t.replace(self.url + "exams/02-chapter-2-quiz/", url).replace("Chapter 2 Quiz", esc(title))
        t = nc.replace_block(r'<a\s+class="breadcrumb-link"\s+href="%sexams/"\s*>Exams</a\s*>' % re.escape(self.url),
                             '<a class="breadcrumb-link" href="%s%s">%s</a>' % (self.url, path, section), t)
        t = t.replace("ITEM_02 // EXAMS", "ITEM_%02d // %s" % (i, upper))
        t = nc.replace_block(r'class="btn btn-primary"\s+href="[^"]*"', 'class="btn btn-primary" href="./%s"' % raw, t)
        t = nc.replace_block(r'class="btn btn-secondary"\s+href="[^"]*"', 'class="btn btn-secondary" href="%s%s"' % (self.url, path), t)
        link = lambda u, cls, word: ('<a href="%s" class="nav-link %s">%s</a>' % (u, cls, word) if u
                                     else '<span class="nav-link %s disabled">%s</span>' % (cls, word))
        t = nc.replace_block(r'<div class="nav-strip[^"]*">.*?</div>',
                             '<div class="nav-strip uppercase">%s%s</div>' % (link(prev_url, "prev", "&lt;- PREVIOUS"), link(next_url, "next", "NEXT -&gt;")), t)
        t = nc.replace_block(r'<iframe.*?</iframe\s*>',
                             '<iframe class="embed-frame legacy-html-frame" src="./%s" loading="lazy" title="%s"></iframe>' % (raw, html.escape(title, quote=True)), t)
        return nc.stamp(t, data, url)

    def write_item(self, kind, i, deck, page, data):
        path, section, _suffix, upper, *_ = KINDS[kind]
        folder = os.path.join(self.out, path, self.folder(kind, deck))
        nc.write(os.path.join(folder, self.file_name(kind, deck)), page)
        prev_deck = self.decks[i - 2] if i > 1 else None
        next_deck = self.decks[i] if i < len(self.decks) else None
        nc.write(os.path.join(folder, "index.html"), self.frame_page(
            self.href(kind, deck), path, section, upper, i, self.item_title(kind, deck), self.file_name(kind, deck),
            self.href(kind, prev_deck), self.href(kind, next_deck), data))

    def row(self, url, i, title, tag="AVAILABLE"):
        return ('<a href="%s" class="dir-row"><div class="dir-num">%02d</div><div class="dir-title">%s</div>'
                '<div class="dir-status"><span class="status-tag available">%s</span></div><div class="dir-arrow">%s</div></a>'
                % (url, i, esc(title), tag, nc.ARROW))

    def rows(self, kind, start=1):
        return "".join(self.row(self.href(kind, d), i, self.item_title(kind, d)) for i, d in enumerate(self.decks, start))

    def listing(self, data, path, label, label_ar, body, active=None):
        """Write a plain .dir-row listing; build_slide_hub.py then turns it into a preview gallery."""
        target = os.path.join(self.out, path, "index.html")
        if os.path.isfile(target) and "Slides moved" in nc.read(target):
            return  # already merged into the Slides hub
        t = nc.rebrand(nc.read(LISTING_TEMPLATE).replace("academics/computer-science/cs316", self.url.strip("/"))
                       .replace("Introduction to AI and Data Science", self.c["name"]).replace("CS316", self.c["code"]).replace("cs316", self.c["code"].lower()), self.c)
        head_end = t.index("</head>")
        head = t[:head_end].replace(self.url + "exams/", self.url + path).replace("%s Exams" % self.c["code"], "%s %s" % (self.c["code"], label))
        t = head + t[head_end:]
        t = nc.replace_block(r'<nav class="content-tabs">.*?</nav>', '<nav class="content-tabs">%s</nav>' % nc.tabs_html(self.c, active or path), t)
        t = nc.replace_block(r'<span class="current"[^>]*>.*?</span\s*>',
                             '<span class="current" data-en-text="%s" data-ar-text="%s">%s</span>' % (label, label_ar, label), t)
        start = t.index('<div class="directory-container')
        t = t[:start] + '<div class="directory-container">%s</div>' % body + t[hub.balanced_end(t, start, "div"):]
        nc.write(target, nc.stamp(t, data, self.url + path))

    def coming_soon(self, data):
        """One unlinked row per deck: the hub shows those as Coming soon tiles."""
        body = "".join(
            '<div class="dir-row"><div class="dir-num">%02d</div><div class="dir-title">%s</div></div>'
            % (i, esc("%s: %s" % (d["head"], d["title"]))) for i, d in enumerate(self.decks, 1))
        self.listing(data, "annotated-slides/", "Annotated Slides", "الشرائح المشروحة", body)

    def update_sidebar(self):
        with open(DATA_FILE, encoding="utf-8") as f:
            data = json.load(f)
        for kind in KINDS:
            path = KINDS[kind][0]
            rows = [{"url": self.href(kind, d), "attrs": "", "label": self.item_title(kind, d)} for d in self.decks]
            if kind == "quiz":
                rows += [{"url": "%sexams/practice-%s/" % (self.url, e[0]), "attrs": "", "label": "Practice %s" % e[1]} for e in EXAMS[self.c["code"]]]
            data["children"][self.url + path] = rows
        data["children"][self.url + CHEAT_PATH] = [
            {"url": "%s%s%s/" % (self.url, CHEAT_PATH, e[0]), "attrs": "", "label": "%s Cheat Sheet" % e[1]} for e in EXAMS[self.c["code"]]]
        data["children"][self.url + "extra-resources/"] = [
            {"url": self.url + "extra-resources/mindmaps/", "attrs": "", "label": "Mind Maps"},
            {"url": self.url + "extra-resources/cheat-sheets/", "attrs": "", "label": "Cheat Sheets"},
        ] + [{"url": "%sextra-resources/%s/" % (self.url, slug), "attrs": "", "label": title}
             for slug, title in EXTRA_RESOURCES.get(self.c["code"], [])]
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
            f.write("\n")
        return data

    def restamp(self, data):
        for dirpath, _dirs, files in os.walk(self.out):
            if "index.html" not in files:
                continue
            path = os.path.join(dirpath, "index.html")
            text = nc.read(path)
            new = nc.stamp(text, data, "/" + os.path.relpath(dirpath, nc.DOCS) + "/")
            if new != text:
                nc.write(path, new)

    def build(self):
        data = self.update_sidebar()
        makers = {
            "breakdown": self.breakdown_page,
            "mindmap": lambda _i, d: self.mindmap_page(d),
            "quiz": self.quiz_page,
        }
        for kind, make in makers.items():
            for i, deck in enumerate(self.decks, 1):
                self.write_item(kind, i, deck, make(i, deck), data)
        total = len(self.decks)
        mock_rows = ""
        for n, (folder, name, numbers, per_deck) in enumerate(EXAMS[self.c["code"]], total + 1):
            folder, title = "practice-" + folder, "Practice " + name
            page = self.mock_page(n, folder, title, numbers, per_deck)
            target = os.path.join(self.out, "exams", folder)
            nc.write(os.path.join(target, folder + ".html"), page)
            nc.write(os.path.join(target, "index.html"), self.frame_page(
                "%sexams/%s/" % (self.url, folder), "exams/", "Exams", "EXAMS", n, title, folder + ".html", None, None, data))
            mock_rows += self.row("%sexams/%s/" % (self.url, folder), n, title)
        self.write_cheats(data)
        self.listing(data, "slide-breakdowns/", "Slide Breakdowns", "تفكيك الشرائح", self.rows("breakdown"))
        self.listing(data, "exams/", "Exams", "الاختبارات", self.rows("quiz") + mock_rows)
        self.listing(data, "extra-resources/mindmaps/", "Mind Maps", "الخرائط الذهنية", self.rows("mindmap"), active="extra-resources/")
        folder_row = lambda n, slug, label, count: (
            '<a href="%sextra-resources/%s/" class="dir-row"><div class="dir-num">%02d</div><div class="dir-title">%s %s</div>'
            '<div class="dir-status"><span class="status-tag available">%d FILES</span></div><div class="dir-arrow">%s</div></a>'
            % (self.url, slug, n, FOLDER_ICON, label, count, nc.ARROW))
        extra_rows = "".join(self.row("%sextra-resources/%s/" % (self.url, slug), n, title)
                             for n, (slug, title) in enumerate(EXTRA_RESOURCES.get(self.c["code"], []), 3))
        self.listing(data, "extra-resources/", "Study Material", "المواد الدراسية",
                     folder_row(1, "mindmaps", "Mind Maps", total) + folder_row(2, "cheat-sheets", "Cheat Sheets", len(EXAMS[self.c["code"]]))
                     + extra_rows)
        self.coming_soon(data)
        self.restamp(data)
        return total


def build_cs316():
    """CS316 keeps its pages and quizzes; only its breakdowns and new cheat sheets come from here."""
    from cs316_annotated.common import DECKS
    from cs316_annotated.decks import CONTENT as OLD
    c = {"code": "CS316", "url": "/academics/computer-science/cs316/", "section": "computer-science",
         "name": "Introduction to AI and Data Science", "decks": [(None, v[2], v[3]) for v in DECKS.values()]}
    course = Course(c)
    by_slug = {d["slug"]: d for d in course.decks}
    decks, data = [], None
    for key, (slug, _file, folder, _label) in DECKS.items():
        if slug in by_slug:
            deck = by_slug[slug]
            deck["sources"] = folder
            deck["mcq"], deck["short"] = OLD[key]["mcq"], OLD[key]["short"]
            deck["cheat"] = deck["cheat"] or [(t, list(items)) for t, items in OLD[key]["cheat"]]
            deck["map"] = deck["map"] or [list(r) for r in OLD[key]["slide_map"]]
            decks.append(deck)
    course.decks = decks
    with open(DATA_FILE, encoding="utf-8") as f:
        data = json.load(f)
    data["children"][course.url + CHEAT_PATH] = [
        {"url": "%s%s%s/" % (course.url, CHEAT_PATH, e[0]), "attrs": "", "label": "%s Cheat Sheet" % e[1]} for e in EXAMS["CS316"]]
    nest = data["children"][course.url + "extra-resources/"]
    if not any(n["url"].endswith("cheat-sheets/") for n in nest):
        nest.insert(1, {"url": course.url + "extra-resources/cheat-sheets/", "attrs": "", "label": "Cheat Sheets"})
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        f.write("\n")
    for i, deck in enumerate(decks, 1):
        folder = os.path.join(course.out, KINDS["breakdown"][0], deck["slug"])
        nc.write(os.path.join(folder, course.file_name("breakdown", deck)), course.breakdown_page(i, deck))
    course.write_cheats(data)
    path = os.path.join(course.out, "extra-resources/index.html")
    text = nc.read(path)
    if 'extra-resources/cheat-sheets/"' not in text:
        tile = ('<a href="%sextra-resources/cheat-sheets/" class="deck-preview" data-kind="folder"><span class="deck-thumb"></span>'
                '<div class="deck-name">Cheat Sheets</div></a>' % course.url)
        at = text.index("</div>", text.index('class="slide-gallery-grid"'))
        anchor = text.rindex("</a", 0, text.index("</section>", at))
        close = text.index(">", anchor) + 1
        text = text[:close] + tile + text[close:]
        nc.write(path, text)
    print("CS316 breakdowns rebuilt:", len(decks))


def main():
    wanted = {a.upper() for a in sys.argv[1:]}
    if not wanted or "CS316" in wanted:
        build_cs316()
    import build_se411_slides
    for c in nc.COURSES + [build_se411_slides.COURSE]:
        if wanted and c["code"] not in wanted:
            continue
        course = Course(c)
        if course.decks:
            print(c["code"], "decks built:", course.build())


if __name__ == "__main__":
    main()
