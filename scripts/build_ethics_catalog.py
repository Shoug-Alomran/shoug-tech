#!/usr/bin/env python3
"""Publish titles only; never publish lesson bodies or private asset URLs."""
from pathlib import Path
import html
import re
from ethics_course_structure import CHAPTERS, chapter, clean_title, sort_key

ROOT = Path(__file__).resolve().parent.parent
SOURCE = ROOT / '.private-courses/ethics/academics/other-courses/ethcs303'
GATE = ROOT / 'workers/course-access/src/gate.html'
GROUPS = {'video-explanations': 'Video explanations', 'slide-breakdowns': 'Slide breakdowns',
          'slides': 'Lecture slides', 'extra-resources': 'Mindmaps & study resources', 'exams': 'Exams & practice'}
START, END = '<!-- COURSE CATALOG START -->', '<!-- COURSE CATALOG END -->'

def build():
    if not SOURCE.exists():
        raise SystemExit('Private course source is required to refresh the catalog.')
    sections = []
    for folder, label in GROUPS.items():
        entries = []
        grouped = {}
        for path in sorted((SOURCE / folder).rglob('*.html')):
            # Folder indexes are navigation, not individual resources.
            if path.name == 'index.html' and any(p.is_dir() for p in path.parent.iterdir()):
                continue
            text = path.read_text()
            if 'data-course-locked="true"' in text:
                continue
            match = re.search(r'<title[^>]*>(.*?)</title>', text, re.S | re.I)
            if not match:
                continue
            title = html.unescape(re.sub('<[^>]+>', '', match[1])).strip()
            title = clean_title(title)
            relative = path.relative_to(SOURCE).as_posix()
            index = chapter(relative, title)
            resource_type = {
                'video-explanations': 'Breakdown walkthrough' if '/slide-breakdowns/' in relative else 'Slide explanation', 'slide-breakdowns': 'Slide breakdown',
                'slides': 'Annotated slides' if 'annotated-slides/' in relative else 'Lecture slides',
                'extra-resources': 'Mindmap' if '/mindmap/' in relative else 'Study resource',
                'exams': 'Exam practice',
            }[folder]
            # The topic stays prominent; format is a consistent secondary label.
            title = re.sub(r'\s*[—–|]\s*(?:Mind\s*Map|Slide Breakdown|Study Guide)$', '', title, flags=re.I)
            grouped.setdefault(index, []).append((title, resource_type))
            entries.append(title)
        body = []
        for index in sorted(grouped):
            body.append('<section class="catalog-chapter"><h3>' + html.escape(CHAPTERS[index][0]) + '</h3><ul>')
            for title, resource_type in sorted(grouped[index], key=lambda row: sort_key(row[0])):
                body.append('<li><span>' + html.escape(title) + '<small class="catalog-format">' + resource_type + '</small></span><span class="catalog-lock">Locked · Full course</span></li>')
            body.append('</ul></section>')
        sections.append(f'<details class="catalog-group"><summary>{label}<span>{len(entries)} resources <b aria-hidden="true">+</b></span></summary>{"".join(body)}</details>')
    fragment = START + '''
<section id="course-catalog" aria-labelledby="catalog-title">
<div class="sample-heading"><div><p class="eyebrow">Explore before you enroll</p><h2 id="catalog-title">Everything in your course.</h2></div><p>Browse the complete resource list. Only the three selected samples below open for free.</p></div>
<div class="catalog-samples"><strong>Available to preview</strong><a href="#free-samples">Video lesson ↗</a><a href="/course-access/samples/mindmap.html">Mindmap ↗</a><a href="/course-access/samples/breakdown.html">Slide breakdown ↗</a></div>
''' + ''.join(sections) + '</section>\n' + END
    source = GATE.read_text()
    if START in source:
        source = re.sub(re.escape(START) + '.*?' + re.escape(END), lambda _: fragment, source, flags=re.S)
    else:
        source = source.replace('<section id="free-samples"', fragment + '\n<section id="free-samples"', 1)
    GATE.write_text(source)
    print('Updated public catalog with titles only across', len(sections), 'categories.')

if __name__ == '__main__':
    build()
