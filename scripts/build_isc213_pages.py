#!/usr/bin/env python3
"""Build the ISC213 course pages from the ISC113 page templates.

ISC213 (Islamic Financial Transactions) mirrors the ISC113 shell exactly: a
course overview, four section index pages, and one wrapper page per item that
either embeds a slide PDF or iframes a hand-written standalone study page.

Everything structural is lifted from the matching ISC113 file so the two
courses stay pixel-identical; only the course strings and the row/section
content are swapped. The hand-written standalone pages (cheat sheets, mindmap,
exams) are authored separately and are never touched by this script.

Usage:
    python3 scripts/build_isc213_pages.py
"""

import os
import re

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(REPO, 'docs', 'academics', 'other-courses', 'isc113')
DST = os.path.join(REPO, 'docs', 'academics', 'other-courses', 'isc213')

COURSE_NAME = 'Islamic Financial Transactions'
COURSE_NAME_AR = 'المعاملات المالية في الإسلام'
DESC = (
    'ISC213 studies contemporary financial transactions through Islamic '
    'jurisprudence: how new transactions emerged, how a qualified scholar '
    'derives a ruling for them, and how Sharia treats incorporeal rights, '
    'insurance, shares, bonds, murabaha, credit cards, gambling, and '
    'multi-level marketing.'
)
DESC_AR = (
    'يدرس مقرر ISC213 المعاملات المالية المعاصرة من منظور الفقه الإسلامي: كيف '
    'نشأت المعاملات الجديدة، وكيف يستنبط المجتهد حكمها، وكيف تتعامل الشريعة مع '
    'الحقوق المعنوية، والتأمين، والأسهم، والسندات، والمرابحة، وبطاقات الائتمان، '
    'والميسر، والتسويق الشبكي.'
)

# (section, [(slug, title, arabic title or '')]) — order defines SEQ numbering.
SECTIONS = {
    'slide-breakdowns': [
        ('01-lecture-1', 'Lecture 1', ''),
        ('02-lecture-2', 'Lecture 2', ''),
        ('03-lecture-3', 'Lecture 3', ''),
        ('04-lecture-4', 'Lecture 4', ''),
    ],
    'slides': [
        ('lecture-1', 'Lecture 1', ''),
        ('lecture-2', 'Lecture 2', ''),
        ('lecture-3', 'Lecture 3', ''),
        ('lecture-4', 'Lecture 4', ''),
    ],
    'extra-resources': [
        ('01-cheat-sheet-1', 'Cheat Sheet 1', 'ورقة المراجعة ١'),
        ('02-cheat-sheet-2', 'Cheat Sheet 2', 'ورقة المراجعة ٢'),
        ('03-mindmap', 'Mindmap', 'الخريطة الذهنية'),
    ],
    'exams': [
        ('01-exam-1', 'Exam 1', 'الاختبار الأول'),
        ('02-exam-2', 'Exam 2', 'الاختبار الثاني'),
        ('03-final-exam', 'Final Exam', 'الاختبار النهائي'),
    ],
}

# Which standalone file each wrapper iframes. Every document sits inside its own
# wrapper folder, so the reference is always a sibling.
EMBED = {
    'slide-breakdowns': {f'0{n}-lecture-{n}': f'./lecture-{n}.html' for n in range(1, 5)},
    'extra-resources': {
        '01-cheat-sheet-1': './cheat-sheet-1.html',
        '02-cheat-sheet-2': './cheat-sheet-2.html',
        '03-mindmap': './mindmap.html',
    },
    'exams': {
        '01-exam-1': './exam-1.html',
        '02-exam-2': './exam-2.html',
        '03-final-exam': './final-exam.html',
    },
}

# The order sections appear in the tab strips, the course sub-nav and the
# sidebar: overview first, then the raw material, then what is built from it.
SECTION_ORDER = ['', 'slides/', 'slide-breakdowns/', 'extra-resources/', 'exams/']

SECTION_LABEL = {
    'slide-breakdowns': ('Slide Breakdowns', 'تفكيك الشرائح'),
    'slides': ('Slides', 'الشرائح'),
    'extra-resources': ('Study Material', 'المواد الدراسية'),
    'exams': ('Exams', 'الاختبارات'),
}

ARROW_SVG = ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" '
             'stroke-linecap="square"><path d="M5 12h14M12 5l7 7-7 7"/></svg>')

SYLLABUS = [
    ('Introduction to the Course', 'مقدمة المقرر', ''),
    ('The Concept of Contemporary Financial Transactions &amp; Its Characteristics',
     'مفهوم المعاملات المالية المعاصرة وخصائصها', '6 SLIDES'),
    ('Methodology of Ijtihad &amp; Introduction to Incorporeal Rights',
     'منهجية الاجتهاد ومدخل إلى الحقوق المعنوية', '4 SLIDES'),
    ('Incorporeal Rights: Copyright, Trade Name, Invention Certificate',
     'الحقوق المعنوية: حق التأليف والاسم التجاري وبراءة الاختراع', '8 SLIDES'),
    ('Insurance', 'التأمين', '9 SLIDES'),
    ('Financial Securities (Shares)', 'الأوراق المالية (الأسهم)', 'PENDING'),
    ('Bonds', 'السندات', 'PENDING'),
    ('Murabaha', 'المرابحة', 'PENDING'),
    ('Sale Deed Based on Leasing', 'البيع القائم على الإجارة', 'PENDING'),
    ('Credit Cards', 'بطاقات الائتمان', 'PENDING'),
    ('Gambling', 'الميسر', 'PENDING'),
    ('Multi-Level Marketing and Pyramid Schemes', 'التسويق الشبكي والهرمي', 'PENDING'),
]

OUTCOMES = [
    ('Define contemporary financial transactions and their characteristics in Islam.',
     'تعريف المعاملات المالية المعاصرة وخصائصها في الإسلام.'),
    ('Compare new contracts such as shares, bonds, and the kinds of credit cards.',
     'المقارنة بين العقود الحديثة كالأسهم والسندات وأنواع بطاقات الائتمان.'),
    ('Derive the rulings of new Islamic transactions from legitimate sources.',
     'استنباط أحكام المعاملات الإسلامية الجديدة من المصادر الشرعية.'),
    ('Give the legitimate alternatives for forbidden business transactions, such as '
     'cooperative insurance and alternatives to bonds.',
     'تقديم البدائل الشرعية للمعاملات المحرمة، كالتأمين التعاوني وبدائل السندات.'),
]

ASSESSMENTS = [
    ('First Major Exam', 'الاختبار الفصلي الأول', '25%'),
    ('Second Major Exam', 'الاختبار الفصلي الثاني', '25%'),
    ('Participation &amp; Assignment', 'المشاركة والواجبات', '10%'),
    ('Written Final Exam', 'الاختبار النهائي التحريري', '40%'),
]

IN_PROGRESS_CSS = '''        .tag-in-progress {
            font-family: var(--font-mono);
            font-size: 10px;
            font-weight: 700;
            color: #f5a623;
            background-color: transparent;
            padding: 4px 12px;
            letter-spacing: 0.1em;
            text-transform: uppercase;
            border: 1px solid #f5a623;
            box-shadow: 0 0 10px rgba(245, 166, 35, 0.2);
        }
'''

TOTAL_SLIDES = 27
TOTAL_DECKS = 4


def read(*parts):
    with open(os.path.join(SRC, *parts), encoding='utf-8') as fh:
        return fh.read()


def write(rel, html):
    path = os.path.join(DST, rel)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as fh:
        fh.write(html)
    print('wrote', os.path.relpath(path, REPO))


def recourse(html):
    """Swap every ISC113 identifier for its ISC213 counterpart."""
    html = html.replace('isc113', 'isc213').replace('ISC113', 'ISC213')
    html = html.replace('Islamic Economy', COURSE_NAME)
    html = html.replace('الاقتصاد الإسلامي', COURSE_NAME_AR)
    # ISC113's exams pages carry a duplicated tail in their SEO description;
    # don't inherit the typo.
    html = html.replace("Digital Garden.'s Digital Garden.", 'Digital Garden.')
    return html


def replace_between(html, start, end, new):
    i = html.index(start)
    j = html.index(end, i) + len(end)
    return html[:i] + new + html[j:]


def reorder_nav(html, nav_class, item_class):
    """Re-emit one nav's links in SECTION_ORDER, keeping each link untouched."""
    open_tag = f'<nav class="{nav_class}">'
    start = html.index(open_tag) + len(open_tag)
    end = html.index('</nav>', start)
    block = html[start:end]

    links = re.findall(rf'<a [^>]*class="{item_class}[^"]*"[^>]*>.*?</a>', block, re.S)
    base = '/academics/other-courses/isc213/'

    def rank(link):
        href = re.search(r'href="([^"]*)"', link).group(1)
        return SECTION_ORDER.index(href[len(base):]) if href.startswith(base) else len(SECTION_ORDER)

    indent = re.match(r'\s*', block).group(0)
    return html[:start] + indent + indent.join(sorted(links, key=rank)) + '\n            ' + html[end:]


def dir_rows(section):
    rows = []
    for n, (slug, title, title_ar) in enumerate(SECTIONS[section], start=1):
        attrs = f' data-en-text="{title}" data-ar-text="{title_ar}"' if title_ar else ''
        rows.append(
            f'                <a href="/academics/other-courses/isc213/{section}/{slug}/" class="dir-row">\n'
            f'                    <div class="dir-num">{n:02d}</div>\n'
            f'                    <div class="dir-title"{attrs}>{title}</div>\n'
            f'                    <div class="dir-status"><span class="status-tag available">AVAILABLE</span></div>\n'
            f'                    <div class="dir-arrow">{ARROW_SVG}</div>\n'
            f'                </a>'
        )
    return '\n'.join(rows)


# --------------------------------------------------------------------------- #
# section index pages
# --------------------------------------------------------------------------- #

def build_section_index(section):
    html = recourse(read(section, 'index.html'))
    rows = re.compile(
        r'(<div class="dir-header">.*?</div>\s*)'      # header row
        r'(?:<a href="[^"]*" class="dir-row">.*?</a>\s*)+',
        re.S)
    # ISC113's slide-breakdowns index describes itself as "Slides"; name the
    # real section instead.
    label = SECTION_LABEL[section][0]
    html = re.sub(r'(content="SHOUG\.TECH \| ISC213 )[^"]*?( study material)',
                  lambda m: m.group(1) + label + m.group(2), html)

    html = reorder_nav(html, 'content-tabs', 'tab')

    match = rows.search(html)
    html = html[:match.start()] + match.group(1).rstrip() + '\n' + dir_rows(section) + '\n' + html[match.end():]
    write(os.path.join(section, 'index.html'), html)


# --------------------------------------------------------------------------- #
# item wrapper pages
# --------------------------------------------------------------------------- #

def nav_strip(section, idx, style):
    """Previous/next strip; `style` picks the ISC113 markup variant used."""
    items = SECTIONS[section]
    base = f'/academics/other-courses/isc213/{section}/'
    prev_html = '<span class="nav-link prev disabled">&lt;- PREVIOUS</span>'
    next_html = '<span class="nav-link next disabled">NEXT -&gt;</span>'
    if style == 'embed':
        prev_html = ''
        next_html = ''
        if idx > 0:
            prev_html = f'<a href="{base}{items[idx - 1][0]}/" class="nav-link prev">&#8592; {items[idx - 1][1]}</a>'
        if idx < len(items) - 1:
            next_html = f'<a href="{base}{items[idx + 1][0]}/" class="nav-link next">{items[idx + 1][1]} &#8594;</a>'
        return (f'            <div class="nav-strip">\n'
                f'                <div>{prev_html}</div>\n'
                f'                <div>{next_html}</div>\n'
                f'            </div>')
    if idx > 0:
        prev_html = f'<a href="{base}{items[idx - 1][0]}/" class="nav-link prev">&lt;- PREVIOUS</a>'
    if idx < len(items) - 1:
        next_html = f'<a href="{base}{items[idx + 1][0]}/" class="nav-link next">NEXT -&gt;</a>'
    return (f'            <div class="nav-strip">\n'
            f'                {prev_html}\n'
            f'                {next_html}\n'
            f'            </div>')


def build_slide_wrapper(idx, slug, title):
    html = recourse(read('slides', 'lecture-1', 'index.html'))
    html = html.replace('Lecture 1', title).replace('lecture-1', slug)
    html = html.replace('ITEM_01 //', f'ITEM_{idx + 1:02d} //')
    html = replace_between(html, '            <div class="nav-strip">', '</div>\n            <div class="embed-area-wrapper">',
                           nav_strip('slides', idx, 'slides') + '\n            <div class="embed-area-wrapper">')
    write(os.path.join('slides', slug, 'index.html'), html)


def build_embed_wrapper(section, idx, slug, title, title_ar):
    template_dir = {'slide-breakdowns': '01-midterm-1',
                    'extra-resources': '04-mindmap',
                    'exams': '01-exam-1'}[section]
    html = recourse(read(section, template_dir, 'index.html'))
    old_slug = template_dir
    old_title = {'01-midterm-1': 'Midterm 1', '04-mindmap': 'Mindmap', '01-exam-1': 'Exam 1'}[old_slug]
    old_ar = {'01-midterm-1': '', '04-mindmap': 'الخريطة الذهنية', '01-exam-1': 'الاختبار الأول'}[old_slug]

    html = html.replace(f'/{old_slug}/', f'/{slug}/')
    if old_ar:
        html = html.replace(old_ar, title_ar or title)
    html = html.replace(old_title, title)

    # Point the iframe (and its "open in new tab" link) at the right standalone file.
    src = EMBED[section][slug]
    html = re.sub(r'(<iframe class="embed-frame" src=")[^"]*(")', lambda m: m.group(1) + src + m.group(2), html)
    html = re.sub(r'(<a href=")(?:\./|\.\./)[A-Za-z0-9._-]+\.html(" target="_blank")',
                  lambda m: m.group(1) + src + m.group(2), html)
    html = re.sub(r'title="[^"]*"( loading="lazy")', f'title="{title}"\\1', html)

    # Rebuild the prev/next strip for this section's own ordering.
    start = '            <div class="nav-strip">'
    end = '<div class="embed-area-wrapper">'
    html = replace_between(html, start, end, nav_strip(section, idx, 'embed') + '\n            <div class="embed-area-wrapper">')
    write(os.path.join(section, slug, 'index.html'), html)


# --------------------------------------------------------------------------- #
# course overview
# --------------------------------------------------------------------------- #

def build_overview():
    html = recourse(read('index.html'))
    # The header blurb and 01_DESCRIPTION both carry the old course description.
    html = re.sub(r'ISC213 introduces the Islamic economic system[^<]*', DESC, html)
    html = re.sub(r'يقدم مقرر ISC213 النظام الاقتصادي الإسلامي[^"]*', DESC_AR, html)

    # 02_SYLLABUS_INDEX
    topics = []
    for n, (name, name_ar, meta) in enumerate(SYLLABUS, start=1):
        topics.append(
            f'                                <div class="topic-item"><span class="topic-num">0x{n:02X}</span>'
            f'<span class="topic-name" data-ar-text="{name_ar}">{name}</span>'
            f'<span class="topic-meta">{meta}</span></div>')
    topics.append(
        f'                                <div class="topic-item exam-total"><span class="topic-num">&Sigma;</span>'
        f'<span class="topic-name" data-ar-text="مجموع الشرائح">Total Slides</span>'
        f'<span class="topic-meta">{TOTAL_SLIDES} SLIDES</span></div>')
    html = replace_between(
        html,
        '<div class="topics-list" style="margin-bottom: 48px;">',
        'Total Slides</span><span class="topic-meta">46 SLIDES</span></div>\n                            </div>',
        '<div class="topics-list" style="margin-bottom: 48px;">\n' + '\n'.join(topics) +
        '\n                            </div>')
    html = html.replace('02_SYLLABUS_INDEX // 12_DECKS // 46_SLIDES',
                        f'02_SYLLABUS_INDEX // {TOTAL_DECKS:02d}_DECKS // {TOTAL_SLIDES}_SLIDES')

    # 03_LEARNING_OUTCOMES
    lis = '\n'.join(
        f'                                    <li data-ar-text="{ar}">{en}</li>' for en, ar in OUTCOMES)
    html = replace_between(html, '<ul class="learning-outcomes">', '</ul>',
                           '<ul class="learning-outcomes">\n' + lis + '\n                                </ul>')

    # 04_WEIGHT_OF_ASSESSMENTS
    rows = '\n'.join(
        f'                                <div class="topic-item"><span class="topic-num">0x{n:02X}</span>'
        f'<span class="topic-name" data-ar-text="{ar}">{en}</span>'
        f'<span class="topic-meta">{pct}</span></div>'
        for n, (en, ar, pct) in enumerate(ASSESSMENTS, start=1))
    i = html.index('04_WEIGHT_OF_ASSESSMENTS')
    start = html.index('<div class="topics-list" style="margin-bottom: 48px;">', i)
    end = html.index('</div>', html.index('40%', start)) + len('</div>')
    end = html.index('</div>', end) + len('</div>')
    html = html[:start] + '<div class="topics-list" style="margin-bottom: 48px;">\n' + rows + \
        '\n                            </div>' + html[end:]

    # ISC213 is still running, so the badge and STATUS row read IN PROGRESS.
    # ISC113's stylesheet only defines .tag-complete, so bring the rule along.
    anchor = '        .tag-complete {'
    html = html.replace(anchor, IN_PROGRESS_CSS + anchor, 1)
    html = html.replace(
        '<span class="tag-complete" data-ar-text="مكتمل" vid="76">COMPLETE</span>',
        '<span class="tag-in-progress" data-ar-text="قيد التطوير" vid="76">IN PROGRESS</span>')
    html = html.replace(
        '<span class="meta-val highlight" style="color: var(--brand-purple);" data-ar-text="مكتمل"\n'
        '                                        vid="148">COMPLETE</span>',
        '<span class="meta-val highlight" style="color: #f5a623;" data-ar-text="قيد التطوير"\n'
        '                                        vid="148">IN PROGRESS</span>')
    html = html.replace(".status-tag, .tag-complete, .tag-available'",
                        ".status-tag, .tag-complete, .tag-in-progress, .tag-available'")

    html = reorder_nav(html, 'sub-nav', 'sub-nav-item')

    html = html.replace('04012023-DB', '10092025-DB')
    write('index.html', html)


def main():
    build_overview()
    for section in ('slide-breakdowns', 'slides', 'extra-resources', 'exams'):
        build_section_index(section)
    for idx, (slug, title, _) in enumerate(SECTIONS['slides']):
        build_slide_wrapper(idx, slug, title)
    for section in ('slide-breakdowns', 'extra-resources', 'exams'):
        for idx, (slug, title, title_ar) in enumerate(SECTIONS[section]):
            build_embed_wrapper(section, idx, slug, title, title_ar)


if __name__ == '__main__':
    main()
