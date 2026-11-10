#!/usr/bin/env python3
"""Merge a course's slide sections into one "Slides" page, grouped by type.

    .venv/bin/python scripts/build_slide_hub.py computer-science/cs331 [--keep-previews]

slides/index.html becomes four cards: slides from the university, slides with
notes, annotated slides and slide breakdowns, each with a short explanation.
Opening a card shows a gallery of deck previews with their titles, and a preview
links to the deck's normal embedded page. The separate listing pages turn into
redirects, the extra tabs and sidebar sections go away, and deck URLs don't
change, so progress, ratings and bookmarks carry over.

Every other listing in the course (Study Material and its folders) becomes the
same preview grid, without the cards.

Previews are one image per list (a vertical strip of 480x360 cells, in
docs/assets/previews/<course>/, because embed_resources.py treats anything inside
a solved/unsolved folder as course content) as the site is close to the
20,000-file limit on Cloudflare Pages. Pages that follow the
site theme get a second "-dark" strip. --keep-previews reuses existing strips.

Safe to re-run: once a course has been merged, rows are read back from the hub.
Only the named course's pages are stamped. See the sidebar's `match` key in
build_academic_sidebar.py for how deck pages stay under SLIDES.
"""
import functools
import glob
import hashlib
import html
import http.server
import io
import json
import os
import re
import subprocess
import sys
import tempfile
import threading
import urllib.parse

sys.path.insert(0, os.path.dirname(__file__))
import build_academic_sidebar as sidebar  # noqa: E402

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ARROW_MARK = 'data-slide-hub'

# Order is the order on the page. `folder` is None for the hub's own listing.
TYPES = [
    {'id': 'university', 'folder': 'slides',
     'en': 'Slides from the University', 'ar': 'شرائح الجامعة', 'side_en': 'UNIVERSITY SLIDES', 'side_ar': 'شرائح الجامعة',
     'about_en': 'The original lecture decks from the instructor, with nothing added.',
     'about_ar': 'شرائح المحاضرات الأصلية من الأستاذ، دون أي إضافات.'},
    {'id': 'notes', 'folder': 'slides-with-notes',
     'en': 'Slides with Notes', 'ar': 'شرائح مع ملاحظات', 'side_en': 'SLIDES WITH NOTES', 'side_ar': 'شرائح مع ملاحظات',
     'about_en': 'The same decks marked up by hand, with handwritten notes and highlights.',
     'about_ar': 'الشرائح نفسها بعد تدوين ملاحظات وتظليلات عليها بخط اليد.'},
    {'id': 'annotated', 'folder': 'annotated-slides',
     'en': 'Annotated Slides', 'ar': 'الشرائح المشروحة', 'side_en': 'ANNOTATED SLIDES', 'side_ar': 'الشرائح المشروحة',
     'about_en': 'Made by Shoug: every slide with highlights linked to numbered study notes, memory tricks and likely exam questions.',
     'about_ar': 'من إعداد شوق: كل شريحة مع تظليلات مرتبطة بملاحظات دراسية مرقمة وحيل للحفظ وأسئلة متوقعة في الاختبار.'},
    {'id': 'breakdowns', 'folder': 'slide-breakdowns',
     'en': 'Slide Breakdowns', 'ar': 'تفكيك الشرائح', 'side_en': 'SLIDE BREAKDOWNS', 'side_ar': 'تفكيك الشرائح',
     'about_en': 'Each chapter rewritten as a study guide in plain language.',
     'about_ar': 'كل فصل مكتوب كدليل دراسي بلغة بسيطة.'},
]

# ETHCS303 is paid and gated: public thumbnails would expose its content.
EXCLUDED = {'ethcs303'}
# A course whose slides/ section isn't the plain university decks.
OVERRIDES = {'phy105': {'university': {
    'en': 'Slides with Notes', 'ar': 'شرائح مع ملاحظات', 'side_en': 'SLIDES WITH NOTES', 'side_ar': 'شرائح مع ملاحظات',
    'about_en': 'The lecture decks with notes added.', 'about_ar': 'شرائح المحاضرات مع ملاحظات مضافة.'}}}
CONTAINER = re.compile(r'<div\s+class="directory-container')
CELL = (480, 360)
PREVIEWS = os.path.join(REPO, 'docs', 'assets', 'previews')
HUB_URL = ['/']  # Base for resolving relative links while the hub is built.

STYLE = """<style id="slide-hub-style">
      .directory-container.slide-hub { display: block; padding: 28px 40px 64px; }
      .slide-hub-intro { margin: 0 0 22px; color: var(--text-secondary); font-size: 1rem; line-height: 1.6; }
      .slide-hub-grid { display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); gap: 16px; }
      .slide-type { display: flex; flex-direction: column; min-width: 0; padding: 18px; border: 1px solid var(--border-med); color: inherit; text-decoration: none; transition: border-color .15s ease, background .15s ease; }
      .slide-type:hover { border-color: var(--brand-purple); }
      .slide-type:focus-visible { outline: 2px solid var(--brand-purple); outline-offset: 2px; }
      .slide-type[aria-expanded="true"] { border-color: var(--brand-purple); background: rgba(184, 41, 234, .08); }
      .slide-type strong { font-family: var(--font-display); font-size: 1.25rem; font-weight: 700; line-height: 1.2; letter-spacing: .03em; text-transform: uppercase; color: var(--text-primary); }
      .slide-type-about { flex: 1; margin: 8px 0 14px; font-size: .9rem; line-height: 1.5; color: var(--text-secondary); }
      .slide-type-foot { display: flex; align-items: center; justify-content: space-between; font-family: var(--font-mono); font-size: .68rem; letter-spacing: .1em; text-transform: uppercase; color: var(--brand-purple); }
      .slide-type-foot svg { width: 14px; height: 14px; transition: transform .15s ease; }
      .slide-type[aria-expanded="true"] .slide-type-foot svg { transform: rotate(180deg); }
      .slide-gallery { margin-top: 28px; scroll-margin-top: 84px; }
      .slide-gallery h2 { margin: 0 0 16px; font-family: var(--font-display); font-size: 1.5rem; font-weight: 700; letter-spacing: .03em; text-transform: uppercase; color: var(--text-primary); }
      .slide-gallery-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(230px, 1fr)); gap: 18px; }
      .deck-preview { display: block; min-width: 0; color: inherit; text-decoration: none; }
      .slide-gallery { --strip: var(--strip-dark); }
      body.shoug-light-mode .slide-gallery { --strip: var(--strip-light); }
      .deck-thumb { display: block; aspect-ratio: 4 / 3; border: 1px solid var(--border-med); background-color: var(--bg-surface); background-image: var(--strip); background-size: 100% auto; background-repeat: no-repeat; transition: border-color .15s ease, transform .15s ease; }
      a.deck-preview:hover .deck-thumb { border-color: var(--brand-purple); transform: translateY(-2px); }
      a.deck-preview:focus-visible { outline: 2px solid var(--brand-purple); outline-offset: 3px; }
      .deck-name { margin-top: 10px; font-family: var(--font-display); font-size: 1rem; font-weight: 600; line-height: 1.3; color: var(--text-primary); }
      a.deck-preview:hover .deck-name { color: var(--brand-purple); }
      .deck-preview .rrt-chip { margin-top: 6px; }
      .deck-kind { display: block; margin-top: 10px; font-family: var(--font-mono); font-size: .62rem; letter-spacing: .12em; text-transform: uppercase; color: var(--brand-purple); }
      .deck-kind + .deck-name { margin-top: 3px; }
      .deck-preview.is-file .deck-thumb { background-image: none; }
      .deck-preview.is-soon .deck-thumb, .deck-preview.is-file .deck-thumb { display: flex; align-items: center; justify-content: center; font-family: var(--font-mono); font-size: .68rem; letter-spacing: .1em; text-transform: uppercase; color: var(--text-tertiary); }
      .deck-preview.is-soon .deck-name { color: var(--text-tertiary); }
      .deck-preview .dir-sets { display: inline-block; margin-inline-start: 8px; padding: 2px 6px; vertical-align: middle; font-family: var(--font-mono); font-size: .58rem; font-weight: 700; letter-spacing: .12em; color: var(--brand-purple); border: 1px solid rgba(184, 41, 234, .4); }
      body.shoug-light-mode .slide-type { background: #fff; border-color: rgba(22, 17, 31, .2); }
      body.shoug-light-mode .slide-type:hover, body.shoug-light-mode .slide-type[aria-expanded="true"] { border-color: #b829ea; }
      body.shoug-light-mode .slide-type[aria-expanded="true"] { background: #f7effd; }
      body.shoug-light-mode .slide-type strong, body.shoug-light-mode .slide-gallery h2, body.shoug-light-mode .deck-name { color: #16111f; }
      body.shoug-light-mode .slide-type-about, body.shoug-light-mode .slide-hub-intro { color: #534a61; }
      body.shoug-light-mode .deck-thumb { background-color: #fff; border-color: rgba(22, 17, 31, .2); }
      body.shoug-light-mode a.deck-preview:hover .deck-name { color: #b829ea; }
      body.shoug-light-mode a.deck-preview:hover .deck-thumb { border-color: #b829ea; }
      body.shoug-light-mode .deck-preview.is-soon .deck-name, body.shoug-light-mode .deck-preview.is-soon .deck-thumb, body.shoug-light-mode .deck-preview.is-file .deck-thumb { color: #6b6378; }
      .slide-hub-grid[data-count="1"] { grid-template-columns: minmax(0, 1fr); max-width: 520px; }
      .slide-hub-grid[data-count="2"] { grid-template-columns: repeat(2, minmax(0, 1fr)); }
      .slide-hub-grid[data-count="3"] { grid-template-columns: repeat(3, minmax(0, 1fr)); }
      @media (max-width: 1280px) { .slide-hub-grid:not([data-count="1"]) { grid-template-columns: repeat(2, minmax(0, 1fr)); } }
      @media (max-width: 1024px) { .directory-container.slide-hub { padding: 24px 24px 48px; } }
      @media (max-width: 768px) { .directory-container.slide-hub { padding: 18px 16px 40px; } }
      @media (max-width: 640px) { .slide-gallery-grid { grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 14px; } }
      @media (max-width: 480px) { .slide-hub-grid:not([data-count="1"]) { grid-template-columns: minmax(0, 1fr); } }
    </style>
"""

SCRIPT = """<script id="slide-hub-script">
(function () {
  var cards = Array.prototype.slice.call(document.querySelectorAll(".slide-type"));
  function panel(card) { return document.getElementById(card.getAttribute("aria-controls")); }
  function show(id, scroll) {
    cards.forEach(function (card) {
      var on = card.getAttribute("aria-controls") === id;
      card.setAttribute("aria-expanded", String(on));
      panel(card).hidden = !on;
      if (on && scroll && panel(card).getBoundingClientRect().top > window.innerHeight * 0.55)
        panel(card).scrollIntoView({ behavior: "smooth", block: "start" });
    });
  }
  function fromHash() {
    var id = location.hash.slice(1);
    if (cards.some(function (c) { return c.getAttribute("aria-controls") === id; })) show(id, true);
  }
  cards.forEach(function (card) {
    card.addEventListener("click", function (e) {
      e.preventDefault();
      var id = card.getAttribute("aria-controls");
      var open = card.getAttribute("aria-expanded") === "true";
      show(open ? "" : id, !open);
      // Kept in the URL so Back from a deck reopens the same gallery.
      history.replaceState(null, "", open ? location.pathname : "#" + id);
    });
  });
  window.addEventListener("hashchange", fromHash);
  fromHash();
})();
</script>
"""


def read(path):
    with open(path, encoding='utf-8') as fh:
        return fh.read()


def write(path, text):
    with open(path, 'w', encoding='utf-8') as fh:
        fh.write(text)


def balanced_end(text, start, tag):
    """Index just past the element opening at `start`."""
    depth = 0
    for m in re.finditer(r'<%s\b|</%s\s*>' % (tag, tag), text[start:]):
        depth += -1 if m.group(0).startswith('</') else 1
        if depth == 0:
            return start + m.end()
    raise ValueError('unbalanced <%s>' % tag)


def extract_rows(region, code):
    """Every item in `region` (old .dir-row or .deck-preview markup)."""
    rows = []
    for m in re.finditer(r'<(a|div)\b[^>]*class="(?:dir-row|deck-preview)[^"]*"[^>]*>', region):
        tag = m.group(1)
        end = region.index('</a', m.start()) if tag == 'a' else None
        row = (region[m.start():region.index('>', end) + 1] if tag == 'a'
               else region[m.start():balanced_end(region, m.start(), 'div')])
        opening = m.group(0)
        found = re.search(r'<div class="(?:dir-title|deck-name)"[^>]*>(.*?)</div>', row, re.S)
        if not found:
            continue
        title = found.group(1)
        title = re.sub(r'<svg\b.*?</svg\s*>', '', title, flags=re.S)
        title = re.sub(r'</?span class="dir-title-text"\s*>|</span\s*>(?=\s*$)', '', title) if 'dir-title-text' in title else title
        title = re.sub(r'\s+', ' ', title).strip()
        title = re.sub(r'^%s\s+' % re.escape(code), '', title)
        href = re.search(r'\bhref="([^"]+)"', opening)
        extra = ''.join(' ' + x for x in re.findall(r'\b(?:target|rel|download)(?:="[^"]*")?', opening))
        rows.append({'href': href.group(1) if href and tag == 'a' else None, 'title': title, 'extra': extra,
                     'folder': 'directory-folder' in opening})
    return rows


def committed(path):
    result = subprocess.run(['git', 'show', 'HEAD:' + os.path.relpath(path, REPO)], cwd=REPO, capture_output=True, text=True)
    return result.stdout if result.returncode == 0 else ''


def listing_rows(course, kind, code, hub, base):
    if hub and ARROW_MARK in hub:
        m = re.search(r'<section\b(?=[^>]*\bclass="slide-(?:type|gallery)")(?=[^>]*\bid="%s")' % kind['id'], hub)
        if m:
            return extract_rows(hub[m.start():balanced_end(hub, m.start(), 'section')], code)
    path = os.path.join(course, kind['folder'], 'index.html')
    if not os.path.isfile(path):
        return []
    page = read(path)
    found = CONTAINER.search(page)
    if not found or 'Slides moved</title>' in page or ARROW_MARK in page:
        # Already replaced by the hub or a redirect: fall back to the committed listing.
        page = committed(path)
        found = CONTAINER.search(page)
    if not found or ARROW_MARK in page:
        return []
    start = found.start()
    rows = extract_rows(page[start:balanced_end(page, start, 'div')], code)
    listing = base + kind['folder'] + '/'
    for r in rows:  # The rows move to the hub, so relative links need a new base.
        if r['href']:
            r['href'] = urllib.parse.urljoin(listing, r['href'])
    return rows


def plain_title(row):
    no_badge = re.sub(r'<span class="dir-sets".*?</span\s*>', '', row['title'], flags=re.S)
    return html.unescape(re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', '', no_badge)).strip())


def attr(s):
    return html.escape(s, quote=True)


def local_path(url):
    return os.path.join(REPO, 'docs', urllib.parse.unquote(url.split('#')[0].split('?')[0]).lstrip('/'))


def source_of(href, page_url, depth=0):
    """(kind, path) to preview an item, or (None, extension) if it can't be shown."""
    url = urllib.parse.urljoin(page_url, html.unescape(href))
    src = urllib.parse.parse_qs(urllib.parse.urlparse(url).query).get('src')
    if src:  # STAT101's shared viewer: the deck is in the query string.
        return source_of(src[0], url, depth + 1)
    path = local_path(url)
    ext = os.path.splitext(path)[1].lower()
    if ext == '.pdf' or ext == '.html' or ext in ('.png', '.jpg', '.jpeg', '.webp'):
        if not os.path.isfile(path):
            return None, ext
        return ('pdf' if ext == '.pdf' else 'html' if ext == '.html' else 'image'), path
    if ext:
        return None, ext
    pdfs = sorted(glob.glob(os.path.join(path, '*.pdf')))
    if pdfs:  # The handwritten set, when a chapter also has a highlighted copy.
        return 'pdf', next((p for p in pdfs if p.endswith('-notes.pdf')), pdfs[0])
    pages = [p for p in sorted(glob.glob(os.path.join(path, '*.html'))) if not p.endswith('/index.html')]
    if pages:
        return 'html', pages[0]
    index = os.path.join(path, 'index.html')
    if not os.path.isfile(index) or depth > 4:
        return None, ''
    text = read(index)
    frame = re.search(r'<iframe\b[^>]*?\b(?:data-src|src)="([^"#]+)"', text[text.find('<main'):], re.S)
    if frame and not frame.group(1).startswith(('http', 'about:', 'data:')):
        found = source_of(frame.group(1), url, depth + 1)
        if found[0]:
            return found
    first = extract_rows(text[text.find('<main'):], '') if CONTAINER.search(text) else []
    for row in first:
        if row['href']:
            found = source_of(row['href'], url, depth + 1)
            if found[0]:
                return found
    return 'html', index


def is_folder(row, page_url):
    if row['folder']:
        return True
    if not row['href']:
        return False
    index = os.path.join(local_path(urllib.parse.urljoin(page_url, row['href'])), 'index.html')
    return os.path.isfile(index) and bool(CONTAINER.search(read(index)))


def render_pdf(path):
    from PIL import Image
    with tempfile.TemporaryDirectory() as tmp:
        out = os.path.join(tmp, 'page')
        subprocess.run(['pdftoppm', '-f', '1', '-l', '1', '-r', '80', '-jpeg', '-singlefile', path, out], check=True)
        return Image.open(out + '.jpg').convert('RGB')


def fit_cell(image):
    from PIL import Image
    copy = image.copy()
    copy.thumbnail(CELL, Image.LANCZOS)
    cell = Image.new('RGB', CELL, (255, 255, 255))
    cell.paste(copy, ((CELL[0] - copy.width) // 2, (CELL[1] - copy.height) // 2))
    return cell


class Quiet(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *args):
        pass


class Renderer:
    """Serves docs/ so pages get the site's absolute CSS and scripts; one tab per theme."""

    def __enter__(self):
        from playwright.sync_api import sync_playwright
        handler = functools.partial(Quiet, directory=os.path.join(REPO, 'docs'))
        self.server = http.server.ThreadingHTTPServer(('127.0.0.1', 0), handler)
        threading.Thread(target=self.server.serve_forever, daemon=True).start()
        self.origin = 'http://127.0.0.1:%d' % self.server.server_address[1]
        self.driver = sync_playwright().start()
        self.browser = self.driver.chromium.launch(channel='chrome')
        self.tabs = {}
        for mode in ('light', 'dark'):
            ctx = self.browser.new_context(viewport={'width': 1280, 'height': 960}, color_scheme=mode)
            ctx.add_init_script('try{localStorage.setItem("shoug-theme","%s")}catch(e){}' % mode)
            self.tabs[mode] = ctx.new_page()
        return self

    def __exit__(self, *exc):
        self.browser.close()
        self.driver.stop()
        self.server.shutdown()

    def shot(self, mode, url):
        from PIL import Image
        page = self.tabs[mode]
        page.goto(url, wait_until='load')
        page.wait_for_timeout(600)
        page.evaluate("""() => document.querySelectorAll('a').forEach(a => {
          if (/^skip to/i.test(a.textContent.trim())) a.remove();
        })""")
        slide = page.locator('.slide:has(.hl)').first  # Annotated decks: a slide with its highlights.
        if slide.count():
            slide.scroll_into_view_if_needed()
            page.wait_for_timeout(400)
            data = slide.screenshot(type='jpeg', quality=90)
        else:
            data = page.screenshot(type='jpeg', quality=90)
        return Image.open(io.BytesIO(data)).convert('RGB')

    def cells(self, kind, path):
        """(light, dark) cells for one item."""
        from PIL import Image
        if kind == 'pdf':
            cell = fit_cell(render_pdf(path))
            return cell, cell
        if kind == 'image':
            cell = fit_cell(Image.open(path).convert('RGB'))
            return cell, cell
        rel = os.path.relpath(path, os.path.join(REPO, 'docs')).replace(os.sep, '/')
        url = self.origin + '/' + urllib.parse.quote(rel)
        return fit_cell(self.shot('light', url)), fit_cell(self.shot('dark', url))


def asset_url(path):
    with open(path, 'rb') as fh:
        digest = hashlib.sha1(fh.read()).hexdigest()[:8]
    return '/%s?v=%s' % (os.path.relpath(path, os.path.join(REPO, 'docs')).replace(os.sep, '/'), digest)


def build_strip(renderer, rows, page_url, folder, stem, keep):
    """Write the strip(s) for a list and return (dark url, light url)."""
    from PIL import Image, ImageChops
    os.makedirs(folder, exist_ok=True)
    light_path = os.path.join(folder, stem + '.jpg')
    dark_path = os.path.join(folder, stem + '-dark.jpg')
    if not (keep and os.path.isfile(light_path)):
        items = [r for r in rows if r['href']]
        size = (CELL[0], CELL[1] * max(1, len(items)))
        light, dark = Image.new('RGB', size, (255, 255, 255)), Image.new('RGB', size, (255, 255, 255))
        for i, r in enumerate(items):
            kind, path = source_of(r['href'], page_url)
            if not kind:
                continue
            try:
                one, two = renderer.cells(kind, path)
            except Exception as err:
                print('  no preview for %s: %s' % (r['href'], err))
                r['kind'] = None
                continue
            light.paste(one, (0, CELL[1] * i))
            dark.paste(two, (0, CELL[1] * i))
        light.save(light_path, quality=72, optimize=True, progressive=True)
        if ImageChops.difference(light, dark).getbbox():
            dark.save(dark_path, quality=72, optimize=True, progressive=True)
        elif os.path.isfile(dark_path):
            os.remove(dark_path)
    light_url = asset_url(light_path)
    return (asset_url(dark_path) if os.path.isfile(dark_path) else light_url), light_url


CHEVRON = ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="square" '
           'aria-hidden="true"><path d="M6 9l6 6 6-6" /></svg>')


def tile(row, position, page_url):
    title = '<div class="deck-name">%s</div>' % row['title']
    if not row['href']:
        return ('<div class="deck-preview is-soon"><span class="deck-thumb" data-en-text="Coming soon" '
                'data-ar-text="قريبًا">Coming soon</span>%s</div>' % title)
    kind, detail = source_of(row['href'], page_url)
    folder = is_folder(row, page_url)
    label = ('<span class="deck-kind" data-en-text="Folder" data-ar-text="مجلد">Folder</span>' if folder else '')
    if not kind:
        text = (detail or 'file').lstrip('.').upper()
        return ('<a href="%s"%s class="deck-preview is-file"><span class="deck-thumb">%s</span>%s</a>'
                % (row['href'], row.get('extra', ''), text, title))
    return ('<a href="%s"%s class="deck-preview"%s><span class="deck-thumb" style="background-position:0 %s%%"></span>%s%s</a>'
            % (row['href'], row.get('extra', ''), ' data-kind="folder"' if folder else '', position, label, title))


def tiles_html(rows, page_url):
    n = sum(1 for r in rows if r['href'])
    out, i = [], 0
    for r in rows:
        out.append(tile(r, ('%.4f' % (i * 100.0 / (n - 1))) if n > 1 else '0', page_url))
        i += 1 if r['href'] else 0
    return '\n              '.join(out)


def strip_style(urls):
    return '--strip-dark:url(&quot;%s&quot;);--strip-light:url(&quot;%s&quot;)' % urls


def build_grid(groups, strips):
    cards, galleries = [], []
    for kind, rows in groups:
        n = sum(1 for r in rows if r['href'])
        en = 'Coming soon' if not n else ('1 deck' if n == 1 else '%d decks' % n)
        ar = 'قريبًا' if not n else ('مجموعة واحدة' if n == 1 else '%d مجموعات' % n)
        cards.append(
            '<a class="slide-type" href="#%s" aria-controls="%s" aria-expanded="false">\n'
            '            <strong data-en-text="%s" data-ar-text="%s">%s</strong>\n'
            '            <span class="slide-type-about" data-en-text="%s" data-ar-text="%s">%s</span>\n'
            '            <span class="slide-type-foot"><span data-en-text="%s" data-ar-text="%s">%s</span>%s</span>\n          </a>'
            % (kind['id'], kind['id'], attr(kind['en']), attr(kind['ar']), html.escape(kind['en']),
               attr(kind['about_en']), attr(kind['about_ar']), html.escape(kind['about_en']), en, ar, en, CHEVRON))
        galleries.append(
            '<section class="slide-gallery" id="%s" hidden style="%s">\n'
            '            <h2 data-en-text="%s" data-ar-text="%s">%s</h2>\n'
            '            <div class="slide-gallery-grid">\n              %s\n            </div>\n          </section>'
            % (kind['id'], strip_style(strips[kind['id']]), attr(kind['en']), attr(kind['ar']), html.escape(kind['en']),
               tiles_html(rows, HUB_URL[0])))
    return ('<div class="directory-container slide-hub" %s>\n'
            '          <noscript><style>.slide-gallery[hidden]{display:block}</style></noscript>\n'
            '          <p class="slide-hub-intro" data-en-text="Every version of the lecture slides. Open one to preview its decks." '
            'data-ar-text="كل نسخ شرائح المحاضرات. افتح أي نسخة لمعاينة شرائحها.">'
            'Every version of the lecture slides. Open one to preview its decks.</p>\n'
            '          <div class="slide-hub-grid" data-count="%d">\n          %s\n          </div>\n          %s\n        </div>\n        %s'
            % (ARROW_MARK, len(cards), '\n          '.join(cards), '\n          '.join(galleries), SCRIPT))


def convert_listings(renderer, course, code, keep):
    """Turn every other listing in the course into a preview grid."""
    done = 0
    docs = os.path.join(REPO, 'docs')
    for path in sorted(glob.glob(os.path.join(course, '**', 'index.html'), recursive=True)):
        text = read(path)
        found = CONTAINER.search(text)
        if not found or ARROW_MARK in text:
            continue
        start = found.start()
        rows = extract_rows(text[start:balanced_end(text, start, 'div')], code)
        if not rows:
            continue
        folder = os.path.dirname(path)
        url = '/' + os.path.relpath(folder, docs).replace(os.sep, '/') + '/'
        stem = os.path.relpath(folder, course).replace(os.sep, '-')
        if len(stem) > 80:
            stem = stem[:60] + '-' + hashlib.sha1(stem.encode()).hexdigest()[:10]
        urls = build_strip(renderer, rows, url, os.path.join(PREVIEWS, code.lower()), stem, keep)
        grid = ('<div class="directory-container slide-hub" data-preview-grid>\n'
                '          <section class="slide-gallery" style="%s">\n            <div class="slide-gallery-grid">\n'
                '              %s\n            </div>\n          </section>\n        </div>'
                % (strip_style(urls), tiles_html(rows, url)))
        text = text[:start] + grid + text[balanced_end(text, start, 'div'):]
        text = re.sub(r'<style id="slide-hub-style">.*?</style>\s*', '', text, flags=re.S)
        text = text.replace('</head>', STYLE + '  </head>', 1)
        write(path, text)
        done += 1
    print('%d other listing(s) turned into preview grids' % done)


def drop_from_sitemap(urls):
    """A redirect must not stay listed: scripts/check_sitemap.py rejects it."""
    path = os.path.join(REPO, 'docs', 'sitemap.xml')
    text = read(path)
    new = text
    for url in urls:
        new = re.sub(r'[ \t]*<url>\s*<loc>https://shoug-tech\.com%s</loc>.*?</url>\s*?\n' % re.escape(url), '', new, flags=re.S)
    if new != text:
        write(path, new)


def stub(code, target):
    return ('<!doctype html>\n<html lang="en">\n  <head>\n    <meta charset="utf-8" />\n    <title>%s — Slides moved</title>\n'
            '    <meta http-equiv="refresh" content="0;url=%s" />\n    <link rel="canonical" href="https://shoug-tech.com%s" />\n'
            '    <script>location.replace("%s");</script>\n  </head>\n  <body>\n    <p>This section is now part of '
            '<a href="%s">Slides</a>.</p>\n  </body>\n</html>\n' % (code, target, target.split('#')[0], target, target))


def update_sidebar_data(base, groups):
    data = sidebar.load_data()
    moved = {base + k['folder'] + '/' for k, _ in groups if k['folder'] != 'slides'} | {
        base + k['folder'] + '/' for k in TYPES if k['folder'] != 'slides'}
    sections = data['sections'].setdefault(base, [])
    sections[:] = [s for s in sections if s['url'] not in moved]
    hub_url = base + 'slides/'
    for s in sections:
        if s['url'] == hub_url:
            s['match'] = sorted(base + k['folder'] + '/' for k, _ in groups if k['folder'] != 'slides')
    for url in moved:
        data['children'].pop(url, None)
    for k in TYPES:
        data['children'].pop('%s#%s' % (hub_url, k['id']), None)
    data['children'][hub_url] = [
        {'url': '%s#%s' % (hub_url, k['id']), 'match': [base + k['folder'] + '/'],
         'attrs': 'data-en-text="%s" data-ar-text="%s"' % (attr(k['side_en']), attr(k['side_ar'])), 'label': k['side_en']}
        for k, _ in groups]
    for k, rows in groups:
        data['children']['%s#%s' % (hub_url, k['id'])] = [
            {'url': r['href'], 'attrs': '', 'label': plain_title(r)} for r in rows if r['href']]
    with open(sidebar.DATA_FILE, 'w', encoding='utf-8') as fh:
        json.dump(data, fh, ensure_ascii=False, indent=2)
        fh.write('\n')
    return data


def fix_page_links(page, base, groups):
    """Drop the old tabs, and point links at the matching column of the hub."""
    for k in TYPES:
        if k['folder'] == 'slides':
            continue
        url = re.escape(base + k['folder'] + '/')
        page = re.sub(r'[ \t]*<a\b(?=[^>]*href="%s")(?=[^>]*class="(?:tab|sub-nav-item)\b)[^>]*>.*?</a\s*>\s*?\n?' % url, '', page, flags=re.S)
    for k, _ in groups:
        if k['folder'] != 'slides':
            page = page.replace('href="%s%s/"' % (base, k['folder']), 'href="%sslides/#%s"' % (base, k['id']))
    return page


def main():
    args = [a for a in sys.argv[1:] if not a.startswith('--')]
    if len(args) != 1:
        sys.exit(__doc__)
    rel = args[0].strip('/')
    if os.path.basename(rel) in EXCLUDED:
        sys.exit('%s is excluded: see EXCLUDED' % rel)
    course = os.path.join(REPO, 'docs', 'academics', rel)
    base = '/academics/%s/' % rel
    code = os.path.basename(rel).upper()
    hub_path = os.path.join(course, 'slides', 'index.html')
    keep = '--keep-previews' in sys.argv
    renderer = Renderer().__enter__()
    data = sidebar.load_data()
    groups = []
    if os.path.isfile(hub_path):
        hub = read(hub_path)
        groups = [(dict(k, **OVERRIDES.get(code.lower(), {}).get(k['id'], {})), rows) for k in TYPES for rows in [listing_rows(course, k, code, hub, base)] if any(r['href'] for r in rows)]  # A type with nothing to open gets no card.
    if groups:
        HUB_URL[0] = base + 'slides/'
        strips = {k['id']: build_strip(renderer, rows, HUB_URL[0], os.path.join(PREVIEWS, code.lower()), 'slides-' + k['id'], keep)
                  for k, rows in groups}
        found = CONTAINER.search(hub)  # Otherwise university slides are "coming soon" but another type exists.
        start = found.start() if found else re.search(r'<div\s+class="coming-soon-container"', hub).start()
        intro = hub.find('<section class="slide-options-intro"')
        begin = intro if 0 <= intro < start else start
        tail = hub[balanced_end(hub, start, 'div'):]
        tail = re.sub(r'^\s*<script id="slide-hub-script">.*?</script>\n?', '', tail, count=1, flags=re.S)
        hub = hub[:begin] + build_grid(groups, strips) + tail
        hub = re.sub(r'[ \t]*\.slide-options?[^\n]*\n|[ \t]*@media\(max-width:760px\)\{\.slide-options-grid[^\n]*\n', '', hub)
        hub = re.sub(r'<style id="slide-hub-style">.*?</style>\s*', '', hub, flags=re.S)
        hub = hub.replace('</head>', STYLE + '  </head>', 1)
        write(hub_path, hub)
        have = {k['id'] for k, _ in groups}
        for k in TYPES:  # Includes "coming soon" sections, whose tabs go away too.
            old = os.path.join(course, k['folder'], 'index.html')
            # Only a section that truly has nothing, or whose rows moved here, becomes a redirect.
            if k['folder'] != 'slides' and os.path.isfile(old) and (k['id'] in have or not re.search(r'class="dir-row', read(old))):
                write(old, stub(code, base + 'slides/' + ('#' + k['id'] if k['id'] in have else '')))
        drop_from_sitemap([base + k['folder'] + '/' for k in TYPES if k['folder'] != 'slides'])
        data = update_sidebar_data(base, groups)
    changed = 0
    for path, url in sidebar.page_urls():
        if not path.startswith(course + os.sep):
            continue
        page = read(path)
        m = sidebar.NAV_RE.search(page)
        before, nav, after = (page[:m.start()], sidebar.render_nav(data, url), page[m.end():]) if m else (page, '', '')
        fix = (lambda part: fix_page_links(part, base, groups)) if groups else (lambda part: part)
        new = fix(before) + nav + fix(after)
        if new != page:
            write(path, new)
            changed += 1
    convert_listings(renderer, course, code, keep)
    renderer.__exit__()
    for k, rows in groups:
        print('%-11s %d rows' % (k['id'], len(rows)))
    print('updated %d %s page(s)' % (changed, code))


if __name__ == '__main__':
    main()
