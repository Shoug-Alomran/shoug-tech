#!/usr/bin/env python3
"""Organize and build ECON102 (Principles of Macroeconomics) in the Business section.

Step 1 moves each uploaded file to an SEO-friendly path
(slides/<slug>/<slug>.pdf, extra-resources/<group>/<slug>/<slug>.<ext>,
syllabus.pdf) and converts PowerPoint and Word files to PDF with Office, keeping
the original next to the PDF. Safe to re-run: files already in place are skipped.

    python scripts/build_econ102_course.py
"""
import glob
import json
import os
import re
import shutil
import subprocess
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
COURSE_DIR = os.path.join(REPO, "docs", "academics", "business", "econ102")

CHAPTERS = {
    1: ("what-is-economics", "What Is Economics?", "ما هو علم الاقتصاد؟"),
    4: ("measuring-the-value-of-production-gdp", "Measuring the Value of Production: GDP",
        "قياس قيمة الإنتاج: الناتج المحلي الإجمالي"),
    5: ("monitoring-jobs-and-inflation", "Monitoring Jobs and Inflation", "رصد الوظائف والتضخم"),
    6: ("economic-growth", "Economic Growth", "النمو الاقتصادي"),
    7: ("finance-saving-and-investment", "Finance, Saving, and Investment", "التمويل والادخار والاستثمار"),
    8: ("money-the-price-level-and-inflation", "Money, the Price Level, and Inflation",
        "النقود ومستوى الأسعار والتضخم"),
    9: ("the-exchange-rate-and-the-balance-of-payments", "The Exchange Rate and the Balance of Payments",
        "سعر الصرف وميزان المدفوعات"),
    10: ("aggregate-supply-and-aggregate-demand", "Aggregate Supply and Aggregate Demand",
         "العرض الكلي والطلب الكلي"),
    11: ("expenditure-multipliers", "Expenditure Multipliers", "مضاعفات الإنفاق"),
    12: ("the-business-cycle-inflation-and-deflation", "The Business Cycle, Inflation, and Deflation",
         "الدورة الاقتصادية والتضخم والانكماش"),
    13: ("fiscal-policy", "Fiscal Policy", "السياسة المالية"),
    14: ("monetary-policy", "Monetary Policy", "السياسة النقدية"),
}


def ch(n, suffix=""):
    """chapter-<n>-<topic>[-suffix]"""
    return "chapter-%d-%s%s" % (n, CHAPTERS[n][0], "-" + suffix if suffix else "")


def slide(n, suffix=""):
    slug = ch(n, suffix)
    return "slides/%s/%s" % (slug, slug)


def extra(group, slug):
    return "extra-resources/%s/%s/%s" % (group, slug, slug)


# (glob of the uploaded file, target path without extension)
FILES = [
    ("ECON102_Course Syllabus_261_*.pdf", "syllabus"),
    # Textbook lecture decks (Parkin, Macroeconomics 14e)
    ("Macro_Ch01_Lecture_Presentation*.pptx", slide(1)),
    ("Macro_Ch04_Lecture_Presentation*.pptx", slide(4)),
    ("Macro_Ch05_Lecture_Presentation*.pptx", slide(5)),
    ("Macro_Ch06_Lecture_Presentation*.pptx", slide(6)),
    ("Macro_Ch07_Lecture_Presentation*.pptx", slide(7)),
    ("Macro_Ch08_Lecture_Presentation*.pptx", slide(8)),
    ("Macro_Ch09_Lecture_Presentation*.pptx", slide(9)),
    ("Macro_Ch10_Lecture_Presentation*.pptx", slide(10)),
    ("Macro_Ch12_Lecture_Presentation*.pptx", slide(12)),
    ("Macro_Ch13_Lecture_Presentation*.pptx", slide(13)),
    # Instructor short slides
    ("Chapter12_ShortSlide*.pptx", slide(12, "short-slides")),
    ("ECON102_Chapter13_ShortSlide*.pptx", slide(13, "short-slides")),
    ("Chapter14_ShortSlide*.pptx", slide(14, "short-slides")),
    # Student sheets
    ("ECON102_Chapter4_Student_Sheets_*.pdf", extra("student-sheets", ch(4, "student-sheet"))),
    ("ECON102_ Chapter4_Circular_Flow_Student_Practice_*.docx",
     extra("student-sheets", "chapter-4-circular-flow-practice")),
    ("ECON102_Chapter6_Student_Sheets *.docx", extra("student-sheets", ch(6, "student-sheet"))),
    ("ECON102_Chapter7_Student_Sheets_*.pdf", extra("student-sheets", ch(7, "student-sheet"))),
    ("ECON102_Chapter8_Student_Sheets_*.pdf", extra("student-sheets", ch(8, "student-sheet"))),
    ("2-ECON102_Chapter9_Student_Sheets_*.pdf", extra("student-sheets", ch(9, "student-sheet"))),
    ("2-Chapter10_Student_Sheet_*.pdf", extra("student-sheets", ch(10, "student-sheet"))),
    ("2-Chapter11_Student_Sheet_*.pdf", extra("student-sheets", ch(11, "student-sheet"))),
    ("2-Chapter13_Student_Sheet_*.pdf", extra("student-sheets", ch(13, "student-sheet"))),
    ("2-Chapter14_Student_Sheet_*.pdf", extra("student-sheets", ch(14, "student-sheet"))),
    # Group work
    ("ECON101_CH1_Groupwork_*.pdf", extra("group-work", ch(1, "group-work"))),
    ("ECON102_CH4_Groupwork_*.docx", extra("group-work", ch(4, "group-work"))),
    ("ECON102_Chapter5_Group_Work_*.pdf", extra("group-work", ch(5, "group-work"))),
    ("ECON102_Chapter6_Group_Work_*.docx", extra("group-work", ch(6, "group-work"))),
    ("ECON102_Chapter7_Group_Work *.pdf", extra("group-work", ch(7, "group-work"))),
    ("ECON102_Chapter8_Group_Work_*.pdf", extra("group-work", ch(8, "group-work"))),
    ("4-ECON102_Chapter9_Group_Work_*.pdf", extra("group-work", ch(9, "group-work"))),
    ("4-Chapter11_Group_Work_*.pdf", extra("group-work", ch(11, "group-work"))),
    ("4-Chapter13_Group_Work_*.pdf", extra("group-work", ch(13, "group-work"))),
    ("4-Chapter14_Group_Work_*.pdf", extra("group-work", ch(14, "group-work"))),
    # Chapter maps
    ("ECON102_Chapter7_Map *.pdf", extra("chapter-maps", ch(7, "map"))),
    ("1-ECON102_Chapter9_Map_*.pdf", extra("chapter-maps", ch(9, "map"))),
    ("1-Chapter13_Map_*.pdf", extra("chapter-maps", ch(13, "map"))),
    ("1-Chapter14_Map_*.pdf", extra("chapter-maps", ch(14, "map"))),
    # Assignments and study guides
    ("ECON102_Assignemnt1_*.pdf", extra("assignments", "assignment-1-chapters-1-and-4")),
    ("ECON102_Assignemnt2_*.pdf", extra("assignments", "assignment-2-chapters-7-and-8")),
    ("AD and AS Shifters Study Guide_*.png", extra("study-guides", "ad-and-as-shifters-study-guide")),
]

OFFICE_TO_PDF = r"""
$ErrorActionPreference = 'Stop'
$src = $args[0]; $dst = $args[1]
if ($src.ToLower().EndsWith('.pptx')) {
  $app = New-Object -ComObject PowerPoint.Application
  try {
    $doc = $app.Presentations.Open($src, $true, $false, $false)
    $doc.SaveAs($dst, 32)
    $doc.Close()
  } finally { $app.Quit() }
} else {
  $app = New-Object -ComObject Word.Application
  $app.Visible = $false
  try {
    $doc = $app.Documents.Open($src, $false, $true)
    $doc.SaveAs2($dst, 17)
    $doc.Close($false)
  } finally { $app.Quit() }
}
"""


def to_pdf(src, dst):
    subprocess.run(
        ["powershell", "-NoProfile", "-NonInteractive", "-Command",
         "& {" + OFFICE_TO_PDF + "}", src, dst],
        check=True,
    )
    if not os.path.exists(dst):
        raise SystemExit("conversion produced no PDF: " + src)


def organize_files():
    for pattern, target in FILES:
        matches = glob.glob(os.path.join(glob.escape(COURSE_DIR), pattern))
        if len(matches) > 1:
            raise SystemExit("more than one upload matches %r: %s" % (pattern, matches))
        placed = glob.glob(os.path.join(glob.escape(COURSE_DIR), target) + ".*")
        if matches:
            ext = os.path.splitext(matches[0])[1].lower()
            dest = os.path.join(COURSE_DIR, target + ext)
            os.makedirs(os.path.dirname(dest), exist_ok=True)
            shutil.move(matches[0], dest)
            print("moved", os.path.basename(matches[0]), "->", target + ext)
        elif not placed:
            raise SystemExit("missing upload: " + pattern)
        for office in (".pptx", ".docx"):
            src = os.path.join(COURSE_DIR, target + office)
            pdf = os.path.join(COURSE_DIR, target + ".pdf")
            if os.path.exists(src) and not os.path.exists(pdf):
                to_pdf(os.path.abspath(src), os.path.abspath(pdf))
                print("converted", target + office)
    leftovers = [n for n in os.listdir(COURSE_DIR)
                 if os.path.isfile(os.path.join(COURSE_DIR, n)) and n not in ("syllabus.pdf", "index.html")]
    if leftovers:
        print("files not in FILES, left in place:", leftovers)


# --------------------------------------------------------------------------- #
# Pages: overview, slides listing and one viewer per deck, from the same CS340
# shells build_new_courses.py uses for ECON101.
# --------------------------------------------------------------------------- #

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build_new_courses as bnc  # noqa: E402
from build_academic_sidebar import DATA_FILE  # noqa: E402

URL = "/academics/business/econ102/"
DOCS = os.path.join(REPO, "docs")


def deck(n, suffix="", counted=True):
    slug = ch(n, suffix)
    title = "Chapter %d - %s%s" % (n, CHAPTERS[n][1], " (Short Slides)" if suffix else "")
    title_ar = "الفصل %d - %s%s" % (n, CHAPTERS[n][2], " (شرائح مختصرة)" if suffix else "")
    return (slug, slug, title, title_ar, "CH %d" % n if counted else "")


COURSE = {
    "code": "ECON102",
    "url": URL,
    "section": "business",
    "name": "Principles of Macroeconomics",
    "name_ar": "مبادئ الاقتصاد الكلي",
    "prereqs": "None",
    "prereqs_ar": "لا يوجد",
    "file_id": "261-MACRO",
    "syllabus": True,
    "description": (
        "ECON102 introduces how the whole economy works in the short and long run: measuring "
        "GDP, unemployment and inflation, economic growth, finance, saving and investment, money "
        "and the banking system, exchange rates and the balance of payments, aggregate supply and "
        "aggregate demand, expenditure multipliers, the business cycle, and fiscal and monetary "
        "policy. Textbook: Macroeconomics by Michael Parkin, 14th Edition."
    ),
    "description_ar": (
        "يقدم مقرر ECON102 كيفية عمل الاقتصاد ككل في المدى القصير والطويل: قياس الناتج المحلي "
        "الإجمالي والبطالة والتضخم، والنمو الاقتصادي، والتمويل والادخار والاستثمار، والنقود والنظام "
        "المصرفي، وسعر الصرف وميزان المدفوعات، والعرض الكلي والطلب الكلي، ومضاعفات الإنفاق، والدورة "
        "الاقتصادية، والسياستين المالية والنقدية. الكتاب المقرر: Macroeconomics لمايكل باركن، الطبعة "
        "الرابعة عشرة."
    ),
    "outcomes": [
        ("Describe how the aggregate economy works both in the short and long run.",
         "وصف كيفية عمل الاقتصاد الكلي في المدى القصير والطويل."),
        ("Recognize the nature of the economic problem, economic growth, unemployment, and inflation.",
         "التعرف على طبيعة المشكلة الاقتصادية والنمو الاقتصادي والبطالة والتضخم."),
        ("Analyze real-world events by applying the economic way of thinking.",
         "تحليل الأحداث الواقعية بتطبيق طريقة التفكير الاقتصادي."),
        ("Explain real-world situations in economic terms.",
         "شرح المواقف الواقعية بمصطلحات اقتصادية."),
        ("Use data sources and spreadsheets to analyze economic information.",
         "استخدام مصادر البيانات وجداول البيانات لتحليل المعلومات الاقتصادية."),
    ],
    "weights": [
        ("Quiz I", "الاختبار القصير الأول", "5%"),
        ("Major I", "الاختبار الفصلي الأول", "20%"),
        ("Quiz II", "الاختبار القصير الثاني", "5%"),
        ("Major II", "الاختبار الفصلي الثاني", "20%"),
        ("Assignments", "الواجبات", "5%"),
        ("Class Attendance and Participation", "الحضور والمشاركة الصفية", "5%"),
        ("Final Examination", "الاختبار النهائي", "40%"),
    ],
    # Chapter 11 has no deck yet; the short slides for 12 and 13 are extra copies.
    "decks": [
        deck(1), deck(4), deck(5), deck(6), deck(7), deck(8), deck(9), deck(10),
        deck(12), deck(12, "short-slides", counted=False),
        deck(13), deck(13, "short-slides", counted=False),
        deck(14, "short-slides"),
    ],
}

# Real page counts of the PDFs (PowerPoint leaves hidden slides out).
PAGES = {1: 74, 4: 67, 5: 53, 6: 49, 7: 36, 8: 70, 9: 62, 10: 39, 12: 53, 13: 53, 14: 10}


def exam_group(heading, heading_ar, chapters):
    rows = []
    for n in chapters:
        if n not in PAGES:
            continue
        slug = ch(n, "short-slides") if n == 14 else ch(n)
        rows.append(("CH %d" % n, CHAPTERS[n][1], slug, PAGES[n]))
    return (heading, heading_ar, rows, sum(r[3] for r in rows))


EXAMS = [
    exam_group("Quiz I — Chapters 1 and 4", "الاختبار القصير الأول — الفصلان 1 و4", [1, 4]),
    exam_group("Major I — Chapters 4–6", "الاختبار الفصلي الأول — الفصول 4–6", [4, 5, 6]),
    exam_group("Quiz II — Chapters 7–8", "الاختبار القصير الثاني — الفصلان 7–8", [7, 8]),
    exam_group("Major II — Chapters 8–10", "الاختبار الفصلي الثاني — الفصول 8–10", [8, 9, 10]),
    exam_group("Final Exam — Comprehensive", "الاختبار النهائي — شامل", sorted(CHAPTERS)),
]

GENERIC_SCOPE = "SCOPE — Taken from the course syllabus. Slide counts are the real page counts of the lecture PDFs."
GENERIC_SCOPE_AR = "النطاق مأخوذ من الخطة الدراسية. أعداد الشرائح هي أعداد صفحات ملفات PDF الفعلية."
SCOPE = (
    "SCOPE — Taken from the course syllabus: Quiz I covers Chapters 1 and 4, Major I covers Chapters "
    "4–6, Quiz II covers Chapters 7–8, Major II covers Chapters 8–10, and the Final is comprehensive. "
    "Counts use the textbook deck for each chapter (the short slides for Chapter 14); Chapter 11 has "
    "no slides yet."
)
SCOPE_AR = (
    "النطاق مأخوذ من الخطة الدراسية: الاختبار القصير الأول يغطي الفصلين 1 و4، والاختبار الفصلي الأول "
    "الفصول 4–6، والاختبار القصير الثاني الفصلين 7–8، والاختبار الفصلي الثاني الفصول 8–10، والاختبار "
    "النهائي شامل. تستخدم الأعداد شرائح الكتاب لكل فصل (والشرائح المختصرة للفصل 14)، ولا توجد شرائح "
    "للفصل 11 بعد."
)


def fill_overview():
    """Fix the parts of the shared overview that assume a .docx syllabus and every chapter having a deck."""
    path = os.path.join(COURSE_DIR, "index.html")
    t = bnc.read(path)
    t = t.replace(URL + "syllabus.docx", URL + "syllabus.pdf")
    t = t.replace(bnc.esc(GENERIC_SCOPE_AR), bnc.esc(SCOPE_AR)).replace(GENERIC_SCOPE, SCOPE)
    ch11 = (
        '<div class="topic-item"><span class="topic-num">CH 11</span>'
        '<span class="topic-name" data-ar-text="%s">%s</span>'
        '<span class="topic-meta" data-ar-text="لا توجد شرائح بعد">NO SLIDES YET</span></div>'
        % (CHAPTERS[11][2], CHAPTERS[11][1])
    )
    if ">CH 11<" not in t:
        anchor = '<div class="topic-item"><span class="topic-num">CH 12</span>'
        if anchor not in t:
            raise SystemExit("overview lost its Chapter 12 row")
        t = t.replace(anchor, ch11 + anchor, 1)
    bnc.write(path, t)


SLIDE_EXPORT = r"""
$ErrorActionPreference = 'Stop'
$app = New-Object -ComObject PowerPoint.Application
try {
  for ($i = 0; $i -lt $args.Count; $i += 3) {
    $p = $app.Presentations.Open($args[$i], $true, $false, $false)
    $p.Slides.Item([int]$args[$i + 2]).Export($args[$i + 1], 'PNG', 960, 720)
    $p.Close()
  }
} finally { $app.Quit() }
"""


def build_preview_strip():
    """slides-university.jpg: each deck's title slide (slide 2 of the textbook decks, whose slide 1 is the book cover), 480x360, stacked in listing order."""
    from PIL import Image, ImageOps

    out = os.path.join(DOCS, "assets", "previews", "econ102", "slides-university.jpg")
    tmp = os.path.join(os.environ.get("TEMP", "/tmp"), "econ102-previews")
    os.makedirs(tmp, exist_ok=True)
    args = []
    for slug, *_ in COURSE["decks"]:
        args += [os.path.abspath(os.path.join(COURSE_DIR, "slides", slug, slug + ".pptx")),
                 os.path.join(tmp, slug + ".png"), "1" if slug.endswith("short-slides") else "2"]
    subprocess.run(["powershell", "-NoProfile", "-NonInteractive", "-Command",
                    "& {" + SLIDE_EXPORT + "}"] + args, check=True)
    strip = Image.new("RGB", (480, 360 * len(COURSE["decks"])), "white")
    for i, (slug, *_) in enumerate(COURSE["decks"]):
        tile = ImageOps.fit(Image.open(os.path.join(tmp, slug + ".png")).convert("RGB"), (480, 360))
        strip.paste(tile, (0, 360 * i))
    os.makedirs(os.path.dirname(out), exist_ok=True)
    strip.save(out, quality=82, optimize=True, progressive=True)


# --------------------------------------------------------------------------- #
# Registration in the shared files (Business section made by
# move_econ101_to_business.py).
# --------------------------------------------------------------------------- #

def update_sidebar_data():
    with open(DATA_FILE, encoding="utf-8") as f:
        data = json.load(f)
    group = bnc.group_of(data, "tree-business")
    if not any(k.get("url") == URL for k in group["children"]):
        group["children"].append({"type": "course", "url": URL, "label": "ECON102"})
    bnc.add_course_entries(data, COURSE)
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        f.write("\n")
    return data


def update_business_hub():
    path = os.path.join(DOCS, "academics/business/index.html")
    t = bnc.read(path)
    row_re = re.compile(r'<a class="course-row" href="%s">.*?</a\s*>' % re.escape(URL), re.S)
    if row_re.search(t):
        t = row_re.sub(lambda _m: bnc.course_row(COURSE), t, count=1)
    else:
        econ101 = re.search(r'<a class="course-row" href="/academics/business/econ101/"\s*>.*?</a\s*>', t, re.S)
        if not econ101:
            raise SystemExit("Business page has no ECON101 row")
        t = t[: econ101.end()] + "\n            " + bnc.course_row(COURSE) + t[econ101.end():]
    bnc.write(path, t)


def update_academics_hub():
    path = os.path.join(DOCS, "academics/index.html")
    t = bnc.read(path)
    t, n = re.subn(r'(href="/academics/business/" class="track-card".*?<div class="card-count mono"[^>]*>)\d+',
                   r"\g<1>02", t, count=1, flags=re.S)
    if n != 1:
        raise SystemExit("academics page has no Business card")
    bnc.write(path, t)


def update_routes():
    path = os.path.join(DOCS, "javascripts/course-routes.js")
    t = bnc.read(path)
    if "econ102:" not in t:
        anchor = '  econ101: "/academics/business/econ101/",\n'
        if anchor not in t:
            raise SystemExit("course-routes.js has no ECON101 route")
        t = t.replace(anchor, anchor + '  econ102: "%s",\n' % URL, 1)
        bnc.write(path, t)


def update_slide_index():
    with open(bnc.SLIDE_INDEX, encoding="utf-8") as f:
        raw = f.read()
    old = '  "/academics/business/econ101/": {'
    if old not in raw:
        raise SystemExit("course-slide-index.json has no ECON101 entry")
    bnc.SLIDE_ANCHORS["ECON102"] = old
    bnc.update_slide_index(COURSE)


def build_pages(data):
    bnc.SECTIONS["business"] = ("Business", "إدارة الأعمال")
    bnc.EXAM_PAGE_COUNTS["ECON102"] = EXAMS
    bnc.build_overview(data, COURSE)
    fill_overview()
    bnc.build_listing(data, COURSE)
    bnc.build_viewers(data, COURSE)


# --------------------------------------------------------------------------- #
# Study pages: slide breakdowns, mind maps, quizzes, practice exams and cheat
# sheets, all from the teaching files in scripts/study_content/econ102/.
# --------------------------------------------------------------------------- #

# (folder, name, chapters or None for all, practice questions per chapter), from the syllabus.
STUDY_EXAMS = [
    ("quiz-1", "Quiz 1", (1, 4), 8),
    ("major-1", "Major 1", (4, 5, 6), 8),
    ("quiz-2", "Quiz 2", (7, 8), 8),
    ("major-2", "Major 2", (8, 9, 10), 8),
    ("final", "Final Exam", None, 3),
]


REVIEW = ("course-review", "Complete Course Review")


def install_page_addons():
    """Read-aloud on breakdowns, and the quiz colour/motion layer and mistakes tracker on quiz pages.

    The same tags the site-wide installers add, applied to ECON102's pages only."""
    import install_quiz_motion as motion
    import install_quiz_review as review
    import install_slide_reader as reader

    changed = 0
    for page in glob.glob(os.path.join(COURSE_DIR, "slide-breakdowns", "*", "*.html")):
        if page.endswith("index.html"):
            continue
        t = bnc.read(page)
        new = reader.EXISTING.sub(reader.TAG, t, count=1) if reader.EXISTING.search(t) else t.replace("</body>", reader.TAG + "\n</body>", 1)
        if new != t:
            bnc.write(page, new)
            changed += 1
    for page in glob.glob(os.path.join(COURSE_DIR, "exams", "*", "*.html")):
        if page.endswith("index.html"):
            continue
        t = new = bnc.read(page)
        if "quiz-motion.js" not in new:
            new = re.sub(r"</head\s*>", motion.TAGS + "</head>", new, count=1)
        if page.endswith("-quiz.html") and review.TAG not in new and "</body>" in new:
            i = new.rindex("</body>")
            new = new[:i] + "    " + review.TAG + "\n  " + new[i:]
        if new != t:
            bnc.write(page, new)
            changed += 1
    print("page add-ons installed on", changed, "pages")


def study_course():
    import build_course_study as bcs

    class Econ102Course(bcs.Course):
        """Chapter 11 has no deck yet, so its breakdown links to the student sheet instead."""

        def slide_links(self, deck):
            sources = [s.strip() for s in deck["sources"].split(",")]
            if all(s.startswith("extra-resources/") for s in sources):
                return [("%s student sheet (no slides yet)" % deck["head"],
                         "%s%s/%s.pdf" % (URL, s, s.rstrip("/").split("/")[-1])) for s in sources]
            return super().slide_links(deck)

        # The cheat-sheet folder is rebuilt from STUDY_EXAMS each time; keep the course review in it.
        # build_econ102_cheat_sheets.py then writes every sheet's content (these are placeholders).
        def write_cheats(self, data):
            # OneDrive can lock an emptied folder; the files are rewritten next, so skip what can't be removed.
            real = bcs.shutil.rmtree
            bcs.shutil.rmtree = lambda p, *a, **k: real(p, ignore_errors=True)
            try:
                super().write_cheats(data)
            finally:
                bcs.shutil.rmtree = real
            path = bcs.CHEAT_PATH
            href = lambda slug: "%s%s%s/" % (self.url, path, slug)
            sheets = [(e[0], "%s Cheat Sheet" % e[1]) for e in STUDY_EXAMS] + [(REVIEW[0], REVIEW[1])]
            n = len(sheets)
            bnc.write(os.path.join(self.out, path, REVIEW[0], "index.html"), self.frame_page(
                href(REVIEW[0]), path, "Cheat Sheets", "CHEAT SHEETS", n, REVIEW[1], REVIEW[0] + ".html",
                href(sheets[-2][0]), None, data))
            rows = "".join(self.row(href(slug), i, title) for i, (slug, title) in enumerate(sheets, 1))
            self.listing(data, path, "Cheat Sheets", "أوراق المراجعة", rows, active="extra-resources/")

        def update_sidebar(self):
            data = super().update_sidebar()
            data["children"][self.url + bcs.CHEAT_PATH].append(
                {"url": "%s%s%s/" % (self.url, bcs.CHEAT_PATH, REVIEW[0]), "attrs": "", "label": REVIEW[1]})
            with open(DATA_FILE, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
                f.write("\n")
            return data

    bnc.SECTIONS["business"] = ("Business", "إدارة الأعمال")
    bcs.EXAMS["ECON102"] = STUDY_EXAMS
    return Econ102Course(COURSE)


def build_study():
    course = study_course()
    print("ECON102 study pages built for", course.build(), "chapters")
    return course


def breakdown_rows(course):
    return [(course.href("breakdown", d), "%s: %s" % (d["head"], d["title"]), d["slug"]) for d in course.decks]


def build_breakdown_strip(course):
    """slides-breakdowns.jpg: each chapter's title slide (exported by build_preview_strip), or a text tile."""
    from PIL import Image, ImageDraw, ImageFont, ImageOps

    tmp = os.path.join(os.environ.get("TEMP", "/tmp"), "econ102-previews")
    rows = breakdown_rows(course)
    strip = Image.new("RGB", (480, 360 * len(rows)), "white")
    for i, (_url, title, slug) in enumerate(rows):
        n = int(slug.split("-", 1)[0])
        png = None
        for candidate in (ch(n), ch(n, "short-slides")):
            path = os.path.join(tmp, candidate + ".png")
            if os.path.exists(path):
                png = path
                break
        if png:
            tile = ImageOps.fit(Image.open(png).convert("RGB"), (480, 360))
        else:
            tile = Image.new("RGB", (480, 360), (17, 8, 34))
            draw = ImageDraw.Draw(tile)
            try:
                big, small = ImageFont.truetype("arialbd.ttf", 40), ImageFont.truetype("arial.ttf", 24)
            except OSError:
                big = small = ImageFont.load_default()
            draw.text((240, 150), "Chapter %d" % n, font=big, fill=(217, 120, 255), anchor="mm")
            draw.text((240, 205), CHAPTERS[n][1], font=small, fill=(255, 255, 255), anchor="mm")
        strip.paste(tile, (0, 360 * i))
    out = os.path.join(DOCS, "assets", "previews", "econ102", "slides-breakdowns.jpg")
    strip.save(out, quality=82, optimize=True, progressive=True)


def breakdown_panel(rows):
    strip = "/assets/previews/econ102/slides-breakdowns.jpg"
    tiles = "".join(
        '<a href="%s" class="deck-preview"><span class="deck-thumb" style="background-position: 0 %.4f%%"></span>'
        '<div class="deck-name">%s</div></a>' % (url, i * 100 / max(1, len(rows) - 1), bnc.esc(title))
        for i, (url, title, _slug) in enumerate(rows))
    return ('<section class="slide-gallery" id="breakdowns" hidden style="--strip-dark: url(&quot;%s&quot;);'
            '--strip-light: url(&quot;%s&quot;)"><h2 data-en-text="Slide Breakdowns" data-ar-text="تفكيك الشرائح">'
            'Slide Breakdowns</h2><div class="slide-gallery-grid">%s</div></section>' % (strip, strip, tiles))


def build_slide_hub_sections(course=None):
    """Build the expandable three-folder Slides hub used by the other course hubs."""
    path = os.path.join(DOCS, "academics/business/econ102/slides/index.html")
    t = bnc.read(path)
    university = re.search(r'<section class="slide-gallery" id="university".*?</section>', t, re.S)
    if not university:
        raise SystemExit("ECON102 slide hub has no university gallery")
    university_panel = re.sub(r' id="university"(?: hidden)?', ' id="university" hidden', university.group(0), count=1)
    rows = breakdown_rows(course) if course else []
    folders = (
        ('university', 'Slides from the University', 'Lecture decks supplied for ECON102.', '13 decks'),
        ('breakdowns', 'Slide Breakdowns',
         'Every chapter explained in plain language, with memory tricks and pop quizzes.' if rows
         else 'No slide breakdown pages are published yet.', '%d chapters' % len(rows)),
        ('annotated', 'Annotated Slides', 'No annotated slide pages are published yet.', '0 decks'),
    )
    cards = []
    for panel_id, title, description, count in folders:
        cards.append(
            '<a class="slide-type" href="#%s" aria-controls="%s" aria-expanded="false">'
            '<strong>%s</strong><span class="slide-type-about">%s</span>'
            '<span class="slide-type-foot"><span>%s</span><svg viewBox="0 0 24 24" fill="none" '
            'stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M6 9l6 6 6-6"/></svg></span></a>'
            % (panel_id, panel_id, title, description, count)
        )
    empty_panel = lambda panel_id, title: (
        '<section class="slide-gallery" id="%s" hidden><h2>%s</h2>'
        '<p class="slide-hub-intro">There are no published previews in this folder yet.</p></section>'
        % (panel_id, title)
    )
    hub = (
        '<div class="directory-container slide-hub"><p class="slide-hub-intro">Open a folder to browse its previews.</p>'
        '<div class="slide-hub-grid" data-count="3">%s</div>' % ''.join(cards)
        + university_panel + (breakdown_panel(rows) if rows else empty_panel('breakdowns', 'Slide Breakdowns'))
        + empty_panel('annotated', 'Annotated Slides') + '</div>'
        + '<script id="slide-hub-script">(function(){var cards=[].slice.call(document.querySelectorAll(".slide-type"));'
        'function show(id,scroll){cards.forEach(function(c){var on=c.getAttribute("aria-controls")===id;'
        'c.setAttribute("aria-expanded",String(on));document.getElementById(c.getAttribute("aria-controls")).hidden=!on;'
        'if(on&&scroll)document.getElementById(id).scrollIntoView({behavior:"smooth",block:"start"});});}'
        'function fromHash(){var id=location.hash.slice(1);if(cards.some(function(c){return c.getAttribute("aria-controls")===id;}))show(id,false);}'
        'cards.forEach(function(c){c.addEventListener("click",function(e){e.preventDefault();var id=c.getAttribute("aria-controls");'
        'var open=c.getAttribute("aria-expanded")==="true";show(open?"":id,!open);history.replaceState(null,"",open?location.pathname:"#"+id);});});'
        'window.addEventListener("hashchange",fromHash);fromHash();})();</script>'
    )
    t = re.sub(r'<div class="directory-container slide-hub".*?(?=\s*</main>)', hub, t, count=1, flags=re.S)
    t = t.replace('href="%sslide-breakdowns/"' % URL, 'href="#breakdowns"')
    t = t.replace('href="%sannotated-slides/"' % URL, 'href="#annotated"')
    bnc.write(path, t)


RESOURCE_CATEGORIES = [
    ("assignments", "Assignments"),
    ("chapter-maps", "Chapter Maps"),
    ("group-work", "Group Work"),
    ("student-sheets", "Student Sheets"),
    ("study-guides", "Study Guides"),
    ("mindmaps", "Mind Maps"),
    ("cheat-sheets", "Cheat Sheets"),
    ("listing-vault", "Listing Vault"),
    ("glossary", "Glossary"),
]


def resource_rows(category_dir):
    """One link per resource, preferring a browser-friendly PDF when present."""
    rows = []
    for item_dir in sorted(p for p in glob.glob(os.path.join(category_dir, "*")) if os.path.isdir(p)):
        files = [p for p in glob.glob(os.path.join(item_dir, "*")) if os.path.isfile(p)]
        if not files:
            continue
        item_index = os.path.join(item_dir, "index.html")
        chosen = item_index if os.path.isfile(item_index) else next(
            (p for ext in (".pdf", ".png", ".jpg", ".jpeg", ".docx")
             for p in files if os.path.splitext(p)[1].lower() == ext), None)
        if not chosen:
            continue
        slug = os.path.basename(item_dir)
        title = re.sub(r"\bGdp\b", "GDP", slug.replace("-", " ").title())
        if slug.startswith("ad-and-as-"):
            title = title.replace("Ad And As", "AD and AS")
        ext = os.path.splitext(chosen)[1].lower()
        url = ("/" + os.path.relpath(item_dir, DOCS).replace(os.sep, "/") + "/"
               if chosen == item_index else "/" + os.path.relpath(chosen, DOCS).replace(os.sep, "/"))
        rows.append((url, title, ext.lstrip(".").upper()))
    return rows


def resource_row(url, number, title, kind):
    return (
        '<a href="%s" class="dir-row"><div class="dir-num">%02d</div>'
        '<div class="dir-title">%s</div><div class="dir-status"><span class="status-tag available">%s</span></div>'
        '<div class="dir-arrow"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" '
        'stroke-width="2" stroke-linecap="square"><path d="M5 12h14M12 5l7 7-7 7" /></svg></div></a>'
        % (url, number, bnc.esc(title), kind)
    )


def replace_directory(page, body):
    return re.sub(r'<div class="directory-container(?: slide-hub)?"[^>]*>.*?(?=\s*</main>)',
                  '<div class="directory-container">%s</div>' % body, page, count=1, flags=re.S)


def build_resource_indexes():
    """Expose every ECON102 study-resource folder and file in browsable preview grids."""
    root = os.path.join(COURSE_DIR, "extra-resources")
    root_index = os.path.join(root, "index.html")
    shell = bnc.read(root_index)
    with open(DATA_FILE, encoding="utf-8") as f:
        data = json.load(f)
    categories, child_links = [], {}
    for slug, label in RESOURCE_CATEGORIES:
        category_dir = os.path.join(root, slug)
        if not os.path.isdir(category_dir):
            continue
        rows = resource_rows(category_dir)
        category_url = URL + "extra-resources/" + slug + "/"
        if slug in {"listing-vault", "glossary"}:
            rows = [(category_url + ("listing-vault.html" if slug == "listing-vault" else "glossary.html"),
                     label, "HTML")]
        child_links[category_url] = [
            {"url": href, "attrs": "", "label": title} for href, title, _kind in rows
        ]
        categories.append((slug, label, len(rows)))
        index = os.path.join(category_dir, "index.html")
        if slug not in {"mindmaps", "cheat-sheets", "listing-vault", "glossary"}:
            page = shell
            page = re.sub(r"<title>.*?</title>", "<title>ECON102 | %s</title>" % label, page, count=1, flags=re.S)
            page = page.replace("https://shoug-tech.com" + URL + "extra-resources/",
                                "https://shoug-tech.com" + category_url)
            page = re.sub(r'(<div class="breadcrumb">).*?(</div>)',
                          r'\1<a class="breadcrumb-link" href="/academics/">Academics</a> / '
                          r'<a class="breadcrumb-link" href="/academics/business/">Business</a> / '
                          r'<a class="breadcrumb-link" href="%s">ECON102</a> / '
                          r'<a class="breadcrumb-link" href="%sextra-resources/">Study Material</a> / '
                          r'<span class="current">%s</span>\2' % (URL, URL, label), page, count=1, flags=re.S)
            page = re.sub(r'(<div class="type-label"[^>]*>).*?(</div>)', r'\1STUDY MATERIAL\2', page, count=1, flags=re.S)
            body = "".join(resource_row(href, i, title, kind) for i, (href, title, kind) in enumerate(rows, 1))
            page = replace_directory(page, body)
            page = bnc.stamp(page, data, category_url)
            bnc.write(index, page)
    body = "".join(
        resource_row(URL + "extra-resources/" + slug + "/", i, label,
                     "%d ITEM%s" % (count, "" if count == 1 else "S"))
        for i, (slug, label, count) in enumerate(categories, 1)
    )
    shell = replace_directory(shell, body)
    bnc.write(root_index, shell)
    data.setdefault("children", {})[URL + "extra-resources/"] = [
        {"url": URL + "extra-resources/" + slug + "/", "attrs": "", "label": label}
        for slug, label, _count in categories
    ]
    data["children"].update(child_links)
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        f.write("\n")


def run(cmd):
    print("$", " ".join(cmd))
    subprocess.run(cmd, cwd=REPO, check=True)


def main():
    organize_files()
    if "--files-only" in sys.argv:
        return
    if "--previews-only" in sys.argv:
        return build_preview_strip()
    data = update_sidebar_data()
    update_slide_index()
    build_pages(data)
    if "--no-previews" not in sys.argv:
        build_preview_strip()
    course = build_study()
    # Breakdown add-ons, limited to this course (contents, translation, reading progress).
    # Read-aloud and the quiz layers are site-wide only; run install_slide_reader.py,
    # install_quiz_motion.py and install_quiz_review.py by hand and revert other courses.
    for installer in ("install_breakdown_contents.py", "install_breakdown_language.py"):
        run([sys.executable, "scripts/" + installer, URL.strip("/")])
    install_page_addons()
    # The full cheat sheets replace the placeholders build_study just wrote.
    run([sys.executable, "scripts/build_econ102_cheat_sheets.py"])
    build_breakdown_strip(course)
    run([sys.executable, "scripts/build_econ102_study_tools.py"])
    build_resource_indexes()
    run([sys.executable, "scripts/build_slide_hub.py", "business/econ102", "--keep-previews"])
    update_business_hub()
    update_academics_hub()
    update_routes()
    if "--no-build" not in sys.argv:
        py = sys.executable
        run([py, "scripts/build_academic_sidebar.py"])
        run([py, "scripts/build_slide_counts.py", "--only", URL])
        os.environ.setdefault("PYTHONUTF8", "1")  # these scripts read files with the locale default
        run([py, "scripts/build_indexing_manifest.py"])
        run(["node", "scripts/build-course-manifest.js"])
        run(["node", "scripts/build-search-index.js"])
        run([py, "scripts/check_sitemap.py", "--write"])


if __name__ == "__main__":
    sys.exit(main())
