#!/usr/bin/env python3
"""Build SE322's Diagram Examples: one viewer per example with a PDF/Word switch.

Each example lives in extra-resources/diagram-examples/<slug>/<slug>.{pdf,docx}.
embed_resources.py only generates solved/unsolved sections, so this section has
its own builder; it reuses that module's page templates and sidebar handling.

Titles live in scripts/resource-titles.json under the example's folder key.

    python3 scripts/build_se322_diagram_examples.py
"""

import html
import os
import re
import sys
from urllib.parse import quote

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build_activity_and_project_pages as tpl  # noqa: E402
import embed_resources as er  # noqa: E402

SECTION = os.path.join(er.ACADEMICS, 'software-engineering', 'se322', 'extra-resources',
                       'diagram-examples')
TITLE = 'Diagram Examples'
SIDEBAR_LABEL = TITLE.upper()   # matches the neighbouring DIAGRAM VIDEO EXPLANATION entry
# Where these Word files were published before moving here. The Office viewer
# can only read live files, so the switch falls back to this until the new
# location is deployed.
OLD_URL = ('https://shoug-tech.com/academics/software-engineering/se322/extra-resources/'
           'activity/solved/%s/%s.docx')

STYLE = """
<style id="doc-format-switch-style">
.doc-format-switch{display:flex;align-items:center;flex-wrap:wrap;gap:8px;margin-bottom:12px}
.doc-format-switch__label{font-family:var(--font-mono);font-size:.68rem;font-weight:700;letter-spacing:.14em;text-transform:uppercase;color:var(--text-secondary);margin-inline-end:4px}
.doc-format-switch .btn{cursor:pointer}
.embed-container[hidden]{display:none}
</style>
"""


def viewer(url, ctx, title, trail, slug, back_url, doc_path):
    pdf, docx = quote(slug + '.pdf'), './' + quote(slug + '.docx')
    page = er.viewer_html(url, ctx, TITLE.upper(), title, trail, pdf, back_url)
    frame = er.OFFICE_EMBED_URL + quote(er.SITE_ORIGIN + er.url_of(doc_path), safe='')
    live = er.SITE_ORIGIN + er.url_of(doc_path)
    fallback = er.OFFICE_EMBED_URL + quote(OLD_URL % (slug, slug), safe='')
    label = html.escape('%s %s' % (ctx['code'], title), quote=True)
    body = """<div class="embed-area-wrapper">
          <div class="doc-format-switch" data-format-switch role="group" aria-label="Document format">
            <span class="doc-format-switch__label">View as</span>
            <button type="button" class="btn btn-primary" data-format="pdf" aria-pressed="true">PDF</button>
            <button type="button" class="btn btn-secondary" data-format="word" aria-pressed="false">Word</button>
          </div>
          <div class="embed-container" data-format-pane="pdf">
            <div class="pdf-embed" data-pdf-src="%(pdf)s" data-pdf-title="%(label)s"></div>
            <noscript><iframe src="%(pdf)s" width="100%%" height="100%%" title="%(label)s"></iframe></noscript>
          </div>
          <div class="embed-container" data-format-pane="word" data-doc-src="%(docx)s" hidden>
            <iframe data-frame-src="%(frame)s" data-file-url="%(live)s" data-frame-fallback="%(fallback)s" width="100%%" height="100%%" title="%(label)s (Word)" allowfullscreen></iframe>
          </div>
        </div>
      </main>""" % {'pdf': pdf, 'docx': docx, 'frame': frame, 'live': live, 'fallback': fallback, 'label': label}
    page, found = re.subn(r'<div class="embed-area-wrapper">.*?</div>\s*</main>',
                          lambda _m: body, page, count=1, flags=re.S)
    assert found == 1, 'viewer template has no embed area'
    page, found = re.subn(r'<a\s+class="btn btn-primary"[^>]*>.*?</a\s*>',
                          lambda _m: ('<a class="btn btn-primary" href="%s" target="_blank" '
                                      'rel="noopener noreferrer" data-format-action '
                                      'data-pdf-href="%s" data-word-href="%s">'
                                      '[ OPEN IN NEW TAB -&gt; ]</a>') % (pdf, pdf, docx),
                          page, count=1, flags=re.S)
    assert found == 1, 'viewer template has no header button'
    page = page.replace('</head>', STYLE + '</head>', 1)
    return page.replace('</body>', '<script src="/javascripts/doc-format-switch.js" defer></script>\n</body>', 1)


def main():
    build = er.Build(False, None)
    ctx = er.course_context(SECTION)
    sec_url = er.url_of(SECTION)
    rows, sidebar_rows = [], []
    for slug in sorted(os.listdir(SECTION), key=er.natural_key):
        folder = os.path.join(SECTION, slug)
        pdf, docx = (os.path.join(folder, slug + ext) for ext in ('.pdf', '.docx'))
        if not os.path.isdir(folder):
            continue
        if not (os.path.isfile(pdf) and os.path.isfile(docx)):
            sys.exit('%s needs both %s.pdf and %s.docx' % (folder, slug, slug))
        title = build.titles[er.rel(folder)]
        url = er.url_of(folder)
        build.put(os.path.join(folder, 'index.html'), viewer(
            url, ctx, title, ctx['trail'] + [(TITLE, sec_url), (title, None)], slug, sec_url, docx))
        rows.append((title, './%s/' % quote(slug), 'PDF / DOCX', 'pdf', False, False))
        sidebar_rows.append((url, title))

    build.put(os.path.join(SECTION, 'index.html'), er.listing_html(
        sec_url, ctx, TITLE, ctx['trail'] + [(TITLE, None)], tpl.rows(rows),
        '%s | %s' % (ctx['code'], TITLE)))
    build.set_children(sec_url, sidebar_rows)
    build.ensure_study_row(ctx, SECTION, TITLE)
    build.set_children(ctx['trail'][-1][1], [(sec_url, SIDEBAR_LABEL)], keep_labels=True, merge=True)

    if build.sidebar is not None and er.dump_json(er.SIDEBAR_FILE, build.sidebar):
        build.changed.append(er.SIDEBAR_FILE)
    if build.changed:
        build.stamp_sidebars()
    print('diagram examples: %d path(s) updated' % len(build.changed))


if __name__ == '__main__':
    main()
