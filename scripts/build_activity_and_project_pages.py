#!/usr/bin/env python3
"""Render the SE322/SE423 Activity folders and the SE423 Project folder.

Both courses ship raw course files (docx/pdf/png) that need the standard
directory pages around them: an "Activity" folder that opens into "Solved" and
"Unsolved", and for SE423 a "Project" folder holding the project description and
a "Scenario" sub-folder.

The pages are stamped from the ENG103 study-material templates, which are the
smallest self-contained listing/viewer pages on the site. The sidebar stamped in
here is a placeholder: run scripts/build_academic_sidebar.py afterwards to fill
it in from scripts/academic-sidebar.json.

Usage:
    python3 scripts/build_activity_and_project_pages.py
"""

import os
import re

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOCS = os.path.join(REPO, 'docs')

ENG103 = os.path.join(DOCS, 'academics/other-courses/english/eng103/extra-resources',
                      'assignment-1-annotated-bibliography')
LIST_TEMPLATE = os.path.join(ENG103, 'index.html')
VIEW_TEMPLATE = os.path.join(ENG103, 'group-work-log', 'index.html')

TPL_TITLE = 'ENG103 | Assignment 1: Annotated Bibliography'
TPL_URL = ('https://shoug-tech.com/academics/other-courses/english/eng103/extra-resources/'
           'assignment-1-annotated-bibliography/')
TPL_VIEW_TITLE = 'ENG103 // Group Work Log & Deadlines'
TPL_VIEW_URL = TPL_URL + 'group-work-log/'
TPL_VIEW_PDF = '../assignment-1-group-work-log-and-deadlines.pdf'

SITE = 'https://shoug-tech.com'
ARROW = ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" '
         'stroke-linecap="square"><path d="M5 12h14M12 5l7 7-7 7"/></svg>')
FOLDER = ('<svg class="dir-folder-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
          'stroke-width="2" stroke-linecap="square" stroke-linejoin="square">'
          '<path d="M3 7a1 1 0 0 1 1-1h5l2 2h9a1 1 0 0 1 1 1v9a1 1 0 0 1-1 1H4a1 1 0 0 1-1-1V7z"/></svg>')

# Folder rows need the icon styles the ENG103 pages never carried.
EXTRA_CSS = """
        .dir-title:has(.dir-folder-icon) { display: flex; align-items: center; gap: 10px; }
        .dir-folder-icon { width: 20px; height: 20px; flex-shrink: 0; color: var(--text-tertiary); transition: color 0.15s ease; }
        .dir-row:hover .dir-folder-icon { color: var(--brand-purple); }
        .status-tag.png { color: #14b8a6; border-color: rgba(20,184,166,0.4); background: rgba(20,184,166,0.08); }
        .status-tag.available { color: #22c55e; border-color: rgba(34,197,94,0.4); background: rgba(34,197,94,0.08); }
        .status-tag.coming-soon { color: #eab308; border-color: rgba(234,179,8,0.4); background: rgba(234,179,8,0.08); }
        .empty-state { flex-grow: 1; display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 18px; padding: 96px 40px; }
        .empty-state-title { font-family: var(--font-display); font-size: 2rem; font-weight: 700; letter-spacing: 0.1em; text-transform: uppercase; color: var(--text-secondary); }
        .empty-state-text { font-family: var(--font-mono); font-size: 0.8rem; line-height: 1.8; letter-spacing: 0.05em; color: var(--text-tertiary); text-align: center; max-width: 44ch; }
"""

TABS = {
    'se322': [
        ('Overview', 'نظرة عامة', '/academics/software-engineering/se322/'),
        ('Slide Breakdowns', 'تفكيك الشرائح', '/academics/software-engineering/se322/slide-breakdowns/'),
        ('Slides', 'الشرائح', '/academics/software-engineering/se322/slides/'),
        ('Study Material', 'المواد الدراسية', '/academics/software-engineering/se322/extra-resources/'),
        ('Exams', 'الاختبارات', '/academics/software-engineering/se322/exams/'),
    ],
    'se423': [
        ('Overview', 'نظرة عامة', '/academics/software-engineering/se423/'),
        ('Slide Breakdowns', 'تفكيك الشرائح', '/academics/software-engineering/se423/slide-breakdowns/'),
        ('Slides', 'الشرائح', '/academics/software-engineering/se423/slides/'),
        ('Study Material', 'المواد الدراسية', '/academics/software-engineering/se423/extra-resources/'),
        ('Exams', 'الاختبارات', '/academics/software-engineering/se423/exams/'),
    ],
}


# --------------------------------------------------------------------------- #
# shared rendering helpers
# --------------------------------------------------------------------------- #

def read(path):
    with open(path, encoding='utf-8') as fh:
        return fh.read()


def write(url, html):
    path = os.path.join(DOCS, url.strip('/'), 'index.html')
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as fh:
        fh.write(html)
    print('wrote %s' % os.path.relpath(path, REPO))


def breadcrumb(trail):
    """trail: [(label, url or None), ...]; the last entry is the current page."""
    parts = []
    for label, url in trail[:-1]:
        parts.append('<a class="breadcrumb-link" href="%s">%s</a>' % (url, label))
    parts.append('<span class="current">%s</span>' % trail[-1][0])
    return '<div class="breadcrumb">%s</div>' % ' / '.join(parts)


def tabs(course, active):
    out = ['<nav class="content-tabs">']
    for label, ar, url in TABS[course]:
        cls = 'tab active' if url == active else 'tab'
        out.append('                <a href="%s" class="%s" data-en-text="%s" data-ar-text="%s">%s</a>'
                   % (url, cls, label, ar, label))
    out.append('            </nav>')
    return '\n'.join(out)


def add_extra_css(html):
    anchor = '        .dir-arrow { justify-self: end;'
    return html.replace(anchor, EXTRA_CSS.rstrip('\n') + '\n' + anchor, 1)


def head(html, title, url, template_title, template_url):
    html = html.replace(template_title, title)
    return html.replace(template_url, SITE + url)


def rows(entries):
    """entries: (label, href, tag, tag_class, is_folder, external).

    Folders sort above single files, matching scripts/sort_academic_folder_rows.py.
    """
    entries = [e for e in entries if e[4]] + [e for e in entries if not e[4]]
    out = ['<div class="directory-container">',
           '                <div class="dir-header"><span>SEQ</span><span>DESCRIPTOR</span>'
           '<span>TYPE</span><span></span></div>']
    for i, (label, href, tag, tag_cls, folder, external) in enumerate(entries, 1):
        title = (FOLDER + '<span class="dir-title-text">%s</span>' % label) if folder else label
        attrs = ' target="_blank" rel="noopener noreferrer"' if external else ''
        cls = 'dir-row directory-folder' if folder else 'dir-row'
        out.append(
            '                <a href="%s"%s class="%s">\n'
            '                    <div class="dir-num">%02d</div>\n'
            '                    <div class="dir-title">%s</div>\n'
            '                    <div class="dir-status"><span class="status-tag %s">%s</span></div>\n'
            '                    <div class="dir-arrow">%s</div>\n'
            '                </a>' % (href, attrs, cls, i, title, tag_cls, tag, ARROW))
    out.append('            </div>')
    return '\n'.join(out)


def listing_page(url, course, code, type_label, trail, body, meta_title):
    html = add_extra_css(read(LIST_TEMPLATE))
    html = head(html, meta_title, url, TPL_TITLE, TPL_URL)
    html = re.sub(r'<div class="breadcrumb">.*?</div>', breadcrumb(trail), html, count=1, flags=re.S)
    html = html.replace('<h1 class="course-code">ENG103</h1>',
                        '<h1 class="course-code">%s</h1>' % code, 1)
    html = re.sub(r'<div class="type-label">.*?</div>',
                  '<div class="type-label">%s</div>' % type_label, html, count=1, flags=re.S)
    html = re.sub(r'<nav class="content-tabs">.*?</nav>',
                  tabs(course, TABS[course][3][2]), html, count=1, flags=re.S)
    html = re.sub(r'<div class="directory-container">.*?\n            </div>\n        </main>',
                  body + '\n        </main>', html, count=1, flags=re.S)
    write(url, html)


def viewer_page(url, course, item_label, title, trail, pdf_src, back_url, prev_url=None):
    html = read(VIEW_TEMPLATE)
    html = head(html, '%s // %s' % (course.upper(), title), url, TPL_VIEW_TITLE, TPL_VIEW_URL)
    html = re.sub(r'<div class="breadcrumb">.*?</div>', breadcrumb(trail), html, count=1, flags=re.S)
    html = html.replace('<div class="ch-label">ITEM_07 // STUDY MATERIAL</div>',
                        '<div class="ch-label">%s</div>' % item_label, 1)
    html = re.sub(r'<h1 class="ch-title">.*?</h1>',
                  '<h1 class="ch-title">%s</h1>' % title, html, count=1, flags=re.S)
    html = re.sub(r'<a class="btn btn-secondary" href="[^"]*"',
                  '<a class="btn btn-secondary" href="%s"' % back_url, html, count=1)
    prev = ('<a href="%s" class="nav-link prev">&lt;- PREVIOUS</a>' % prev_url) if prev_url else \
           ('<a href="%s" class="nav-link prev">&lt;- BACK TO INDEX</a>' % back_url)
    html = re.sub(r'<div class="nav-strip">.*?</div>',
                  '<div class="nav-strip">\n                %s\n'
                  '                <span class="nav-link next disabled">NEXT -&gt;</span>\n'
                  '            </div>' % prev, html, count=1, flags=re.S)
    html = html.replace(TPL_VIEW_PDF, pdf_src)
    html = html.replace('ENG103 Group Work Log and Deadlines', '%s %s' % (course.upper(), title))
    write(url, html)


# --------------------------------------------------------------------------- #
# page definitions
# --------------------------------------------------------------------------- #

SE322 = '/academics/software-engineering/se322/'
SE423 = '/academics/software-engineering/se423/'


def se322_trail(*tail):
    trail = [('Academics', '/academics/'), ('Software Engineering', '/academics/software-engineering/'),
             ('SE322', SE322), ('Study Material', SE322 + 'extra-resources/')]
    return trail + list(tail)


def se423_trail(*tail):
    trail = [('Academics', '/academics/'), ('Software Engineering', '/academics/software-engineering/'),
             ('SE423', SE423), ('Study Material', SE423 + 'extra-resources/')]
    return trail + list(tail)


def build_se322():
    base = SE322 + 'extra-resources/activity/'

    listing_page(
        base, 'se322', 'SE322', 'Activity',
        se322_trail(('Activity', None)),
        rows([('Solved', './solved/', '1 FOLDER', 'available', True, False),
              ('Unsolved', './unsolved/', '2 FILES', 'available', True, False)]),
        'SE322 | Activity')

    # Solved keeps one folder per activity, so later solutions just drop in beside it.
    listing_page(
        base + 'solved/', 'se322', 'SE322', 'Activity // Solved',
        se322_trail(('Activity', base), ('Solved', None)),
        rows([('Activity 3', './activity-3/', '3 FILES', 'available', True, False)]),
        'SE322 | Activity: Solved')

    listing_page(
        base + 'solved/activity-3/', 'se322', 'SE322', 'Activity // Solved // Activity 3',
        se322_trail(('Activity', base), ('Solved', base + 'solved/'), ('Activity 3', None)),
        rows([('UML and Tools Workshop', './uml-and-tools-workshop/', 'PDF', 'pdf', False, False),
              ('Use Case Diagram', './activity-3-use-case-diagram.png', 'PNG', 'png', False, True),
              ('Class Diagram', './activity-3-class-diagram.png', 'PNG', 'png', False, True)]),
        'SE322 | Activity 3: Solved')

    listing_page(
        base + 'unsolved/', 'se322', 'SE322', 'Activity // Unsolved',
        se322_trail(('Activity', base), ('Unsolved', None)),
        rows([('Activity 2: Modularization', './activity-2.docx', 'DOCX', 'docx', False, True),
              ('Activity 3: UML and Tools Workshop', './activity-3.docx', 'DOCX', 'docx', False, True)]),
        'SE322 | Activity: Unsolved')

    viewer_page(
        base + 'solved/activity-3/uml-and-tools-workshop/', 'se322',
        'SOLVED // ACTIVITY 3', 'UML and Tools Workshop',
        se322_trail(('Activity', base), ('Solved', base + 'solved/'),
                    ('Activity 3', base + 'solved/activity-3/'), ('UML and Tools Workshop', None)),
        '../activity-3-uml-and-tools-workshop.pdf', base + 'solved/activity-3/')


SCENARIOS = [
    ('Scenario 1: CRM Rewrite', 'scenario-01-crm-rewrite', 'pdf'),
    ('Scenario 3: State Metro System', 'scenario-03-state-metro-system', 'pdf'),
    ('Scenario 4: Water Monitoring and Alert System',
     'scenario-04-water-monitoring-and-alert-system', 'pdf'),
    ('Scenario 5: Athletic Health Compliance and Monitoring System',
     'scenario-05-athletic-health-compliance-and-monitoring-system', 'pdf'),
    ('Scenario 6: Smart City Traffic Management System',
     'scenario-06-smart-city-traffic-management-system', 'docx'),
    ('Scenario 7: National E-Health Records System',
     'scenario-07-national-e-health-records-system', 'docx'),
    ('Scenario 8: National Digital Archiving System',
     'scenario-08-national-digital-archiving-system', 'docx'),
    ('Scenario 9: Smart Agriculture System for Arid Regions',
     'scenario-09-smart-agriculture-system-for-arid-regions', 'docx'),
    ('Scenario 10: National Cultural Heritage Digitization Portal',
     'scenario-10-national-cultural-heritage-digitization-portal', 'docx'),
    ('Scenario 11: National Employment and Skill Matching Platform',
     'scenario-11-national-employment-and-skill-matching-platform', 'docx'),
]


def build_se423_activity():
    base = SE423 + 'extra-resources/activity/'

    listing_page(
        base, 'se423', 'SE423', 'Activity',
        se423_trail(('Activity', None)),
        rows([('Solved', './solved/', '1 FILE', 'available', True, False),
              ('Unsolved', './unsolved/', '1 FILE, 1 FOLDER', 'available', True, False)]),
        'SE423 | Activity')

    listing_page(
        base + 'solved/', 'se423', 'SE423', 'Activity // Solved',
        se423_trail(('Activity', base), ('Solved', None)),
        rows([('Activity 2', './activity-2.pdf', 'PDF', 'pdf', False, True)]),
        'SE423 | Activity: Solved')

    listing_page(
        base + 'unsolved/', 'se423', 'SE423', 'Activity // Unsolved',
        se423_trail(('Activity', base), ('Unsolved', None)),
        rows([('Activity 2', './activity-2/', '3 FILES', 'available', True, False),
              ('Activity 1', './Activity%201.docx', 'DOCX', 'docx', False, True)]),
        'SE423 | Activity: Unsolved')

    listing_page(
        base + 'unsolved/activity-2/', 'se423', 'SE423',
        'Activity // Unsolved // Activity 2',
        se423_trail(('Activity', base), ('Unsolved', base + 'unsolved/'),
                    ('Activity 2', None)),
        rows([('Classic Mistakes', './activity-2-classic-mistakes.docx',
               'DOCX', 'docx', False, True),
              ('Case Study - Giga Safe', './activity-2-case-study-giga-safe.docx',
               'DOCX', 'docx', False, True),
              ('Examples of Classic Mistakes',
               './activity-2-examples-of-classic-mistakes.docx',
               'DOCX', 'docx', False, True)]),
        'SE423 | Activity 2: Unsolved')


def build_se423_project():
    base = SE423 + 'extra-resources/project/'

    listing_page(
        base, 'se423', 'SE423', 'Project',
        se423_trail(('Project', None)),
        rows([('Project Description', './description/', 'PDF', 'pdf', False, False),
              ('Scenario', './scenario/', '10 FILES', 'available', True, False)]),
        'SE423 | Project')

    viewer_page(
        base + 'description/', 'se423', 'PROJECT // STUDY MATERIAL', 'Project Description',
        se423_trail(('Project', base), ('Project Description', None)),
        '../project-description.pdf', base)

    entries, viewers = [], []
    for label, slug, kind in SCENARIOS:
        if kind == 'pdf':
            entries.append((label, './%s/' % slug, 'PDF', 'pdf', False, False))
            viewers.append((label, slug))
        else:
            entries.append((label, './%s.docx' % slug, 'DOCX', 'docx', False, True))

    listing_page(
        base + 'scenario/', 'se423', 'SE423', 'Project // Scenario',
        se423_trail(('Project', base), ('Scenario', None)),
        rows(entries), 'SE423 | Project: Scenario')

    for label, slug in viewers:
        viewer_page(
            base + 'scenario/' + slug + '/', 'se423', 'PROJECT // SCENARIO', label,
            se423_trail(('Project', base), ('Scenario', base + 'scenario/'), (label, None)),
            '../%s.pdf' % slug, base + 'scenario/')


def main():
    build_se322()
    build_se423_activity()
    build_se423_project()


if __name__ == '__main__':
    main()
