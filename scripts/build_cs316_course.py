#!/usr/bin/env python3
"""Build CS316 (Introduction to AI and Data Science) from CS340's page shells.

Moves each uploaded deck to slides/<slug>/<slug>.pdf, then writes the overview,
the slides listing and one viewer per deck. Safe to re-run. Edit DECKS or the
course facts here, not the generated HTML.

    python3 scripts/build_cs316_course.py

The other sections are built by build_cs316_annotated_slides.py and
build_cs316_study_tools.py.
"""
import html
import json
import os
import re
import shutil
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build_academic_sidebar import DATA_FILE, NAV_RE, render_nav  # noqa: E402

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOCS = os.path.join(REPO, "docs")
SLIDE_INDEX = os.path.join(REPO, "scripts", "course-slide-index.json")

COURSE_URL = "/academics/computer-science/cs316/"
COURSE_DIR = os.path.join(DOCS, COURSE_URL.strip("/"))
TEMPLATE_DIR = os.path.join(DOCS, "academics/computer-science/cs340")
TEMPLATE_DECK = "chapter-1-introduction-to-databases"
TEMPLATE_DECK_TITLE = "Chapter 1 Introduction To Databases"
TEMPLATE_NAME = "Introduction to Database Systems"

NAME = "Introduction to AI and Data Science"
NAME_AR = "مقدمة في الذكاء الاصطناعي وعلم البيانات"
PREREQS = "CS210, STAT101"
PREREQS_AR = "CS210، STAT101"
DESCRIPTION = (
    "CS316 builds a foundation in AI and data science that combines theory with "
    "practice: data wrangling, cleaning and interactive exploration in Python, "
    "feature engineering and dimensionality reduction, statistical learning, "
    "linear regression and binary classification, hypothesis testing, and the "
    "ethical and societal impact of data science and AI."
)
DESCRIPTION_AR = (
    "يقدم مقرر CS316 أساسا في الذكاء الاصطناعي وعلم البيانات يجمع بين النظرية والتطبيق: "
    "تجهيز البيانات وتنظيفها واستكشافها تفاعليا باستخدام Python، وهندسة الخصائص وتقليل الأبعاد، "
    "والتعلم الإحصائي، والانحدار الخطي والتصنيف الثنائي، واختبار الفرضيات، "
    "والأثر الأخلاقي والمجتمعي لعلم البيانات والذكاء الاصطناعي."
)

# (original upload, slug, title, Arabic title, overview row number label)
DECKS = [
    ("Topic 1_ Introduction to Data Science and AI_261_Student.pdf",
     "chapter-1-introduction-to-ai-and-data-science",
     "Chapter 1 - Introduction to AI and Data Science",
     "الفصل 1 - مقدمة في الذكاء الاصطناعي وعلم البيانات", "CH 1"),
    ("Topic 2 -Part 1- Pandas for Data Analytics_242_261.pdf",
     "chapter-2-1-pandas-for-data-analytics",
     "Chapter 2.1 - Pandas for Data Analytics",
     "الفصل 2.1 - مكتبة Pandas لتحليل البيانات", "CH 2.1"),
    ("2.2 - Importing_Summarizing_Visualizing_Data_ab0203194068a21ab791b242dfd0810d.pdf",
     "chapter-2-2-importing-summarizing-and-visualizing-data",
     "Chapter 2.2 - Importing, Summarizing and Visualizing Data",
     "الفصل 2.2 - استيراد البيانات وتلخيصها وتصويرها", "CH 2.2"),
    ("Topic 2.3 - Handling Missing Data_0b2b45dfbf4967e93d003590a95b99d8.pdf",
     "chapter-2-3-handling-missing-data",
     "Chapter 2.3 - Handling Missing Data",
     "الفصل 2.3 - التعامل مع البيانات المفقودة", "CH 2.3"),
    ("Chapter 3_Statistical Learning_v2.pdf",
     "chapter-3-statistical-learning",
     "Chapter 3 - Statistical Learning",
     "الفصل 3 - التعلم الإحصائي", "CH 3"),
    ("Chpater4_foundations of predictive modeling_3fe60e14941158bebc252a2e9af02886.pdf",
     "chapter-4-foundations-of-predictive-modeling",
     "Chapter 4 - Foundations of Predictive Modeling",
     "الفصل 4 - أساسيات النمذجة التنبؤية", "CH 4"),
    ("Classification_V0.pdf",
     "classification-part-1-bayes-error-and-metrics",
     "Classification Part 1 - Bayes Error and Metrics",
     "التصنيف، الجزء 1 - خطأ بايز والمقاييس", "CLS 1"),
    ("Classification_part2_00b2991b73973c1fa502f084513884af.pdf",
     "classification-part-2-binary-classification",
     "Classification Part 2 - Binary Classification",
     "التصنيف، الجزء 2 - التصنيف الثنائي", "CLS 2"),
    ("Normalization_70fa254878f96c1f3728662cb6f78254.pdf",
     "normalization-why-feature-scaling-matters",
     "Normalization - Why Feature Scaling Matters",
     "التسوية - أهمية توحيد مقاييس الخصائص", "NORM"),
    ("Chapter7.1 - Similarity Measure_7c27c64ae2d6d0e998bbc472d4fc44a4.pdf",
     "chapter-7-1-numpy-and-similarity-measures",
     "Chapter 7.1 - NumPy and Similarity Measures",
     "الفصل 7.1 - مكتبة NumPy ومقاييس التشابه", "CH 7.1"),
    ("Part 7.2 - Dimensionality reduction - PCA_98d2b2979427c083cb4ddf67c244644c.pdf",
     "chapter-7-2-dimensionality-reduction-with-pca",
     "Chapter 7.2 - Dimensionality Reduction with PCA",
     "الفصل 7.2 - تقليل الأبعاد باستخدام PCA", "CH 7.2"),
    ("Part 7.3 - Dimensionality Reduction using t-SNE_56f87b09dab3487aa662426a98721acf.pdf",
     "chapter-7-3-dimensionality-reduction-with-t-sne",
     "Chapter 7.3 - Dimensionality Reduction with t-SNE",
     "الفصل 7.3 - تقليل الأبعاد باستخدام t-SNE", "CH 7.3"),
    ("chapter-8-cross-validation-and-grid-search.pdf",
     "chapter-8-cross-validation-and-grid-search",
     "Chapter 8 - Cross-Validation and Grid Search",
     "الفصل 8 - التحقق المتقاطع والبحث الشبكي", "CH 8"),
    ("Chapter 9 - statistical theorems_1d37e0d15b78755668d55f3a4caf05f5.pdf",
     "chapter-9-fundamental-statistical-theorems",
     "Chapter 9 - Fundamental Statistical Theorems",
     "الفصل 9 - النظريات الإحصائية الأساسية", "CH 9"),
    ("hypothesis_testing_h (1)_52a97c9b4726e88a48734ab6514253c5.pdf",
     "chapter-10-hypothesis-testing",
     "Chapter 10 - Hypothesis Testing",
     "الفصل 10 - اختبار الفرضيات", "CH 10"),
]

OUTCOMES = [
    ("Demonstrate a thorough knowledge of AI, data science and hypothesis testing.",
     "إظهار معرفة شاملة بالذكاء الاصطناعي وعلم البيانات واختبار الفرضيات."),
    ("Develop and evaluate machine learning models to gain insights and assess their performance.",
     "تطوير نماذج تعلم الآلة وتقييمها لاستخلاص الرؤى وقياس أدائها."),
    ("Employ current and emerging tools and programming languages for data processing, visualization and interpretation.",
     "توظيف الأدوات ولغات البرمجة الحالية والناشئة في معالجة البيانات وتصويرها وتفسيرها."),
    ("Execute a team capstone project that applies theory to a significant AI and data science problem.",
     "تنفيذ مشروع جماعي ختامي يطبق المعرفة النظرية على مشكلة مهمة في الذكاء الاصطناعي وعلم البيانات."),
    ("Analyze the ethical implications, societal impact and professional responsibilities involved in AI and data science.",
     "تحليل الآثار الأخلاقية والأثر المجتمعي والمسؤوليات المهنية في الذكاء الاصطناعي وعلم البيانات."),
]

WEIGHTS = [
    ("Python Programming Quiz", "اختبار برمجة Python", "5%"),
    ("Quizzes (3)", "اختبارات قصيرة (3)", "15%"),
    ("Major Exam", "الاختبار الفصلي", "20%"),
    ("Project", "المشروع", "15%"),
    ("Attendance", "الحضور", "5%"),
    ("Final Exam", "الاختبار النهائي", "40%"),
]

TABS = [
    ("", "Overview", "نظرة عامة"),
    ("slide-breakdowns/", "Slide Breakdowns", "تفكيك الشرائح"),
    ("slides/", "Slides", "الشرائح"),
    ("annotated-slides/", "Annotated Slides", "الشرائح المشروحة"),
    ("extra-resources/", "Study Material", "المواد الدراسية"),
    ("exams/", "Exams", "الاختبارات"),
]

ARROW = (
    '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" '
    'stroke-linecap="square"><path d="M5 12h14M12 5l7 7-7 7" /></svg>'
)


def read(path):
    with open(path, encoding="utf-8", newline="") as f:
        return f.read()


def write(path, text):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(text)


def esc(text):
    return html.escape(text, quote=True)


def replace_block(pattern, new, text, flags=re.S):
    """Swap the one match of pattern for new; a template change must fail loudly."""
    result, count = re.subn(pattern, lambda _m: new, text, count=1, flags=flags)
    if count != 1:
        raise SystemExit("template no longer matches: " + pattern)
    return result


def rebrand(text):
    return text.replace(TEMPLATE_NAME, NAME).replace("CS340", "CS316").replace("cs340", "cs316")


def stamp_sidebar(text, data, url):
    return NAV_RE.sub(lambda _m: render_nav(data, url), text, count=1)


def move_decks():
    slides = os.path.join(COURSE_DIR, "slides")
    for source, slug, *_ in DECKS:
        target = os.path.join(slides, slug, slug + ".pdf")
        origin = os.path.join(slides, source)
        if os.path.exists(origin):
            os.makedirs(os.path.dirname(target), exist_ok=True)
            shutil.move(origin, target)
        elif not os.path.exists(target):
            raise SystemExit("missing deck: " + source)


def update_sidebar_data():
    with open(DATA_FILE, encoding="utf-8") as f:
        data = json.load(f)
    entry = {"type": "course", "url": COURSE_URL, "label": "CS316"}
    group = next(n for n in data["tree"] if n.get("id") == "tree-computer-science")
    if not any(c.get("url") == COURSE_URL for c in group["children"]):
        at = next(i for i, c in enumerate(group["children"]) if c.get("label") == "CS330")
        group["children"].insert(at, entry)
    data["sections"][COURSE_URL] = [
        {
            "url": COURSE_URL + path,
            "attrs": 'data-en-text="%s" data-ar-text="%s"' % (en.upper(), ar),
            "label": en.upper(),
        }
        for path, en, ar in TABS
    ]
    data["children"][COURSE_URL + "slides/"] = [
        {"url": "%sslides/%s/" % (COURSE_URL, slug), "attrs": "", "label": title}
        for _src, slug, title, *_ in DECKS
    ]
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        f.write("\n")
    return data


def update_slide_index():
    raw = read(SLIDE_INDEX)
    key = '"%s"' % COURSE_URL
    start = raw.find('  ' + key)
    if start >= 0:  # replace the existing entry so the rows follow DECKS
        depth, i = 0, raw.index('{', start)
        for j in range(i, len(raw)):
            depth += {'{': 1, '}': -1}.get(raw[j], 0)
            if depth == 0:
                end = raw.index('\n', j) + 1
                break
        raw = raw[:start] + raw[end:]
    counted = [d for d in DECKS if d[4]]
    spec = {
        "rows": {str(i): ["%s/%s.pdf" % (d[1], d[1])] for i, d in enumerate(counted, 1)},
        "ignore_decks": ["%s/%s.pdf" % (d[1], d[1]) for d in DECKS if not d[4]],
        "labels": {str(len(counted) + 2): ["PROJECT", "مشروع"]},
    }
    spec["rows"][str(len(counted) + 1)] = []
    block = json.dumps({COURSE_URL: spec}, indent=2, ensure_ascii=False)[2:-2]
    anchor = '  "/academics/computer-science/cs330/": {'
    if anchor not in raw:
        raise SystemExit("course-slide-index.json has no CS330 entry to insert before")
    write(SLIDE_INDEX, raw.replace(anchor, block + ",\n" + anchor, 1))


def topic_row(num, name, name_ar, url=None):
    if url:
        title = '<a class="topic-name topic-name-link" href="%s" data-ar-text="%s">%s</a>' % (
            url, esc(name_ar), esc(name))
    else:
        title = '<span class="topic-name" data-ar-text="%s">%s</span>' % (esc(name_ar), esc(name))
    return '<div class="topic-item"><span class="topic-num">%s</span>%s</div>' % (esc(num), title)


def overview_body():
    rows = [
        topic_row(num, title, title_ar, "%sslides/%s/" % (COURSE_URL, slug))
        for _src, slug, title, title_ar, num in DECKS
        if num
    ]
    rows.append(topic_row("0x10", "Ethics and Bias in Data Science and AI",
                          "الأخلاقيات والتحيز في علم البيانات والذكاء الاصطناعي"))
    rows.append(topic_row("0x11", "Team Capstone Project", "المشروع الجماعي الختامي"))
    outcomes = "".join(
        '<li data-ar-text="%s">%s</li>' % (esc(ar), esc(en)) for en, ar in OUTCOMES
    )
    weights = "".join(
        '<div class="topic-item"><span class="topic-num">0x%02X</span>'
        '<span class="topic-name" data-ar-text="%s">%s</span>'
        '<span class="topic-meta">%s</span></div>' % (i, esc(ar), esc(en), pct)
        for i, (en, ar, pct) in enumerate(WEIGHTS, 1)
    )
    blocks = [
        ("Course Code", "<span class=\"data-block-val\">CS316</span>"),
        ("Credit Hours", "<span class=\"data-block-val\">3</span>"),
        ("Prerequisites",
         '<span class="data-block-val" data-ar-text="%s" style="font-family: var(--font-mono); '
         'font-size: 1.1rem; padding-top: 6px">%s</span>' % (PREREQS_AR, PREREQS)),
    ]
    grid = "".join(
        '<div class="data-block"><span class="data-block-label">%s</span>%s</div>' % b
        for b in blocks
    )
    return (
        '<div class="content-section"><div class="grid-data-blocks">' + grid + "</div>"
        '<div class="section-label" id="section-description">01_DESCRIPTION</div>'
        '<div class="text-block"><p data-ar-text="%s">%s</p></div>' % (esc(DESCRIPTION_AR), esc(DESCRIPTION))
        + '<div class="section-label" id="section-syllabus-index">02_SYLLABUS_INDEX</div>'
        '<div class="topics-list" style="margin-bottom: 48px">' + "".join(rows) + "</div>"
        '<div class="section-label" id="section-learning-outcomes">03_LEARNING_OUTCOMES</div>'
        '<div class="text-block"><ul class="learning-outcomes">' + outcomes + "</ul></div>"
        '<div class="section-label" id="section-weight-of-assessments">04_WEIGHT_OF_ASSESSMENTS</div>'
        '<div class="topics-list" style="margin-bottom: 48px">' + weights + "</div></div>"
    )


def build_overview(data):
    t = rebrand(read(os.path.join(TEMPLATE_DIR, "index.html")))
    t = replace_block(
        r'<span class="tag-complete"[^>]*>COMPLETE</span>',
        '<span class="tag-complete" data-en-text="IN PROGRESS" data-ar-text="قيد التنفيذ">IN PROGRESS</span>',
        t,
    )
    t = replace_block(
        r'<h2\s+class="course-name".*?</h2>',
        '<h2 class="course-name" data-ar-text="%s">%s</h2>' % (NAME_AR, NAME),
        t,
    )
    t = replace_block(
        r'<p\s+class="course-desc-brief".*?</p>',
        '<p class="course-desc-brief" data-ar-text="%s">%s</p>' % (esc(DESCRIPTION_AR), esc(DESCRIPTION)),
        t,
    )
    links = "".join(
        '<a href="%s%s" class="sub-nav-item%s" data-en-text="[ %s ]" data-ar-text="[ %s ]">[ %s ]</a>'
        % (COURSE_URL, path, " active" if not path else "", en.upper(), ar, en.upper())
        for path, en, ar in TABS
    )
    t = replace_block(r'<nav class="sub-nav">.*?</nav>', '<nav class="sub-nav">%s</nav>' % links, t)
    t = replace_block(r'<div class="content-section".*?(?=\s*</article>)', overview_body(), t)
    t = re.sub(r'(class="meta-val highlight"[^>]*>)\s*COMPLETE', r"\1IN PROGRESS", t, count=1, flags=re.S)
    t = re.sub(
        r'(<span class="meta-key"[^>]*>PREREQUISITES</span>\s*<span\s+class="meta-val"[^>]*?)'
        r'\s*data-ar-text="[^"]*"\s*>[^<]*',
        lambda m: '%s data-ar-text="%s">%s' % (m.group(1), PREREQS_AR, PREREQS),
        t, count=1, flags=re.S,
    )
    t = re.sub(r'(<span class="meta-key"[^>]*>FILE_ID</span>.*?>)\s*04012023-DB', r"\g<1>261-AIDS", t, count=1, flags=re.S)
    quick = (
        ('%ssyllabus.docx' % COURSE_URL, "Syllabus", "الخطة الدراسية", True),
        ("#section-description", "Description", "الوصف", False),
        ("#section-learning-outcomes", "Learning Outcomes", "نواتج التعلم", False),
        ("#section-weight-of-assessments", "Weight Of Assessments", "أوزان التقييمات", False),
    )
    quick_html = "".join(
        '<a href="%s" class="quick-link-btn"%s data-en-text="%s" data-ar-text="%s">%s</a>'
        % (href, ' target="_blank" rel="noopener noreferrer"' if new_tab else "", en, ar, en)
        for href, en, ar, new_tab in quick
    )
    t = replace_block(r'<div class="quick-links">.*?</div>', '<div class="quick-links">%s</div>' % quick_html, t)
    write(os.path.join(COURSE_DIR, "index.html"), stamp_sidebar(t, data, COURSE_URL))


def tabs_html(active):
    return "".join(
        '<a href="%s%s" class="tab%s" data-en-text="%s" data-ar-text="%s">%s</a>'
        % (COURSE_URL, path, " active" if path == active else "", en, ar, en)
        for path, en, ar in TABS
    )


def section_page(data, path, label, label_ar, rows_html):
    """A section listing cloned from this course's own exams page: path like "notes/"."""
    t = read(os.path.join(COURSE_DIR, "exams/index.html"))
    head_end = t.index("</head>")
    head = t[:head_end].replace("cs316/exams/", "cs316/" + path).replace("CS316 Exams", "CS316 " + label)
    t = head + t[head_end:]
    t = replace_block(r'<nav class="content-tabs">.*?</nav>',
                      '<nav class="content-tabs">%s</nav>' % tabs_html(path), t)
    t = replace_block(r'<span class="current"[^>]*>.*?</span\s*>',
                      '<span class="current" data-en-text="%s" data-ar-text="%s">%s</span>' % (label, label_ar, label), t)
    t = replace_block(r'<div class="type-label"[^>]*>.*?</div>',
                      '<div class="type-label" data-en-text="%s" data-ar-text="%s">%s</div>' % (label.upper(), label_ar, label.upper()), t)
    rows = list(re.finditer(r'<a\s+href="[^"]*"\s+class="dir-row"\s*>.*?</a\s*>', t, re.S))
    if not rows:
        return  # the Slides hub owns this listing now; build_slide_hub.py rebuilds it
    t = t[: rows[0].start()] + rows_html + t[rows[-1].end() :]
    url = COURSE_URL + path
    write(os.path.join(COURSE_DIR, path, "index.html"), stamp_sidebar(t, data, url))


def build_listing(data):
    t = rebrand(read(os.path.join(TEMPLATE_DIR, "slides/index.html")))
    t = replace_block(r'<nav class="content-tabs">.*?</nav>',
                      '<nav class="content-tabs">%s</nav>' % tabs_html("slides/"), t)
    rows = list(re.finditer(r'<a\s+href="[^"]*"\s+class="dir-row"\s*>.*?</a\s*>', t, re.S))
    if not rows:
        raise SystemExit("slides template has no dir-row")
    new = "".join(
        '<a href="%sslides/%s/" class="dir-row"><div class="dir-num">%02d</div>'
        '<div class="dir-title">%s</div><div class="dir-status">'
        '<span class="status-tag available">AVAILABLE</span></div>'
        '<div class="dir-arrow">%s</div></a>' % (COURSE_URL, slug, i, esc(title), ARROW)
        for i, (_src, slug, title, *_rest) in enumerate(DECKS, 1)
    )
    t = t[: rows[0].start()] + new + t[rows[-1].end() :]
    url = COURSE_URL + "slides/"
    write(os.path.join(COURSE_DIR, "slides/index.html"), stamp_sidebar(t, data, url))


def build_viewers(data):
    shell = rebrand(read(os.path.join(TEMPLATE_DIR, "slides", TEMPLATE_DECK, "index.html")))
    for i, (_src, slug, title, *_rest) in enumerate(DECKS):
        t = shell.replace(TEMPLATE_DECK, slug).replace(TEMPLATE_DECK_TITLE, esc(title))
        t = t.replace("ITEM_01", "ITEM_%02d" % (i + 1))
        prev_link = (
            '<a href="%sslides/%s/" class="nav-link prev">&lt;- PREVIOUS</a>' % (COURSE_URL, DECKS[i - 1][1])
            if i else '<span class="nav-link prev disabled">&lt;- PREVIOUS</span>'
        )
        next_link = (
            '<a href="%sslides/%s/" class="nav-link next">NEXT -&gt;</a>' % (COURSE_URL, DECKS[i + 1][1])
            if i + 1 < len(DECKS) else '<span class="nav-link next disabled">NEXT -&gt;</span>'
        )
        t = replace_block(r'<div class="nav-strip">.*?</div>',
                          '<div class="nav-strip">%s%s</div>' % (prev_link, next_link), t)
        url = "%sslides/%s/" % (COURSE_URL, slug)
        write(os.path.join(COURSE_DIR, "slides", slug, "index.html"), stamp_sidebar(t, data, url))


SIDEBAR_LI = '<li class="tree-item"><a class="tree-file" href="%s">CS316</a></li>' % COURSE_URL
SIDEBAR_RE = re.compile(
    r'<li class="tree-item[^"]*">\s*<a class="tree-file[^"]*"[^>]*href="/academics/computer-science/cs330/"'
)
COUNT_TITLE_RE = re.compile(r'("computer science":\s*")7 courses\.')
COUNT_META_RE = re.compile(r'("computer science":\s*\[\s*"CS Track",\s*")7 Courses"')
# The same table is pasted into most pages, but only these two hubs show it.
COUNT_PAGES = {
    os.path.join(DOCS, "academics/index.html"),
    os.path.join(DOCS, "academics/computer-science/index.html"),
}


def register_everywhere():
    """Add only the CS316 sidebar row, and the count on the hubs; never re-stamp other pages."""
    changed = 0
    for dirpath, _dirs, files in os.walk(DOCS):
        if dirpath.startswith(COURSE_DIR):
            continue
        for name in files:
            if not name.endswith(".html"):
                continue
            path = os.path.join(dirpath, name)
            text = read(path)
            new = text
            if SIDEBAR_LI not in new:
                new = SIDEBAR_RE.sub(lambda m: SIDEBAR_LI + m.group(0), new, count=1)
            if path in COUNT_PAGES:
                new = COUNT_TITLE_RE.sub(r"\g<1>8 courses.", new)
                new = COUNT_META_RE.sub(r'\g<1>8 Courses"', new)
            if new != text:
                write(path, new)
                changed += 1
    return changed


def update_hub():
    path = os.path.join(DOCS, "academics/computer-science/index.html")
    t = read(path)
    t = t.replace("7 courses.<br />Structured", "8 courses.<br />Structured")
    t = t.replace("<span>7 Courses</span>", "<span>8 Courses</span>")
    if 'class="course-row" href="%s"' % COURSE_URL not in t:
        row = (
            '<a class="course-row" href="%s"><div class="course-code">CS316</div>'
            '<div class="course-name"><span data-ar-text="%s">%s</span></div>'
            '<div class="course-status-area"><div class="status-tag status-pending">IN PROGRESS</div>'
            '<div class="row-arrow">-&gt;</div></div></a\n            >' % (COURSE_URL, NAME_AR, NAME)
        )
        anchor = '<a class="course-row" href="/academics/computer-science/cs330/">'
        if anchor not in t:
            raise SystemExit("CS hub has no CS330 row to insert before")
        t = t.replace(anchor, row + anchor, 1)
    write(path, t)


def update_routes():
    path = os.path.join(DOCS, "javascripts/course-routes.js")
    t = read(path)
    if "cs316:" not in t:
        anchor = '  cs330: "/academics/computer-science/cs330/",\n'
        if anchor not in t:
            raise SystemExit("course-routes.js has no CS330 route")
        t = t.replace(anchor, '  cs316: "%s",\n' % COURSE_URL + anchor, 1)
        write(path, t)


def main():
    move_decks()
    data = update_sidebar_data()
    update_slide_index()
    build_overview(data)
    build_listing(data)
    build_viewers(data)
    update_hub()
    update_routes()
    print("pages updated with the CS316 sidebar row or course count:", register_everywhere())
    subprocess.run(
        [sys.executable, os.path.join(REPO, "scripts/build_slide_counts.py"), "--only", COURSE_URL],
        check=True,
    )


if __name__ == "__main__":
    main()
