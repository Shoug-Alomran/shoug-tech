#!/usr/bin/env python3
"""Render the ISC213 standalone study pages.

Emits two cheat sheets, one mindmap, and three practice exams into
docs/academics/other-courses/isc213/. Each page is a single self-contained file
in the same visual language as the lecture slide-breakdowns, sharing
docs/styles/isc213.css so the course reads as one design.

The wrapper index.html pages that iframe these files are built separately by
scripts/build_isc213_pages.py.

Usage:
    python3 scripts/build_isc213_study_tools.py
"""

import html
import json
import os

import isc213_content as C

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
COURSE = os.path.join(REPO, 'docs', 'academics', 'other-courses', 'isc213')

SITE = 'https://shoug-tech.com'
OG_IMAGE = f'{SITE}/assets/og-banner.png'

# These documents only ever load inside their wrapper page's iframe, so the
# canonical points at the wrapper — a self-canonical would compete with the page
# readers are meant to land on. Same rule scripts/backfill_seo_metadata.py uses.
WRAPPER = {
    'extra-resources/01-cheat-sheet-1/cheat-sheet-1.html': 'extra-resources/01-cheat-sheet-1/',
    'extra-resources/02-cheat-sheet-2/cheat-sheet-2.html': 'extra-resources/02-cheat-sheet-2/',
    'extra-resources/03-mindmap/mindmap.html': 'extra-resources/03-mindmap/',
    'exams/01-exam-1/exam-1.html': 'exams/01-exam-1/',
    'exams/02-exam-2/exam-2.html': 'exams/02-exam-2/',
    'exams/03-final-exam/final-exam.html': 'exams/03-final-exam/',
}

# Deliberately no html-theme-sync.js: it would overwrite #themeIcon with emoji
# and these pages already resolve and persist the site theme themselves.
CLARITY = '''<script type="text/javascript">
(function(c,l,a,r,i,t,y){
    c[a]=c[a]||function(){(c[a].q=c[a].q||[]).push(arguments)};
    t=l.createElement(r);t.async=1;t.src="https://www.clarity.ms/tag/"+i;
    y=l.getElementsByTagName(r)[0];y.parentNode.insertBefore(t,y);
})(window, document, "clarity", "script", "xub0eqmvs9");
</script>'''

FONTS = ('https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,400;9..144,500;'
         '9..144,600;9..144,700&family=Inter:wght@400;500;600;700&family=Amiri:wght@400;700&display=swap')

# Resolve stored site theme first, then the parent frame (the wrapper page only
# marks itself in light mode), then the OS. Persist whatever we inherit so the
# first toggle click is never a no-op.
THEME_JS = '''
  var root = document.documentElement;
  var themeToggle = document.getElementById('themeToggle');
  var themeIcon = document.getElementById('themeIcon');
  var themeLabel = document.getElementById('themeLabel');

  function applyTheme(theme) {
    root.setAttribute('data-theme', theme);
    themeIcon.textContent = theme === 'dark' ? '\\u263E' : '\\u2600\\uFE0E';
    themeLabel.textContent = theme === 'dark' ? 'Dark' : 'Light';
  }

  function storedTheme() {
    try {
      var v = localStorage.getItem('shoug-theme');
      if (v) return v === 'light' ? 'light' : 'dark';
    } catch (e) {}
    try {
      if (window.parent !== window && window.parent.document) {
        return window.parent.document.body.classList.contains('shoug-light-mode') ? 'light' : 'dark';
      }
    } catch (e) {}
    return (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches) ? 'dark' : 'light';
  }

  var initial = storedTheme();
  applyTheme(initial);
  try { localStorage.setItem('shoug-theme', initial); } catch (e) {}

  themeToggle.addEventListener('click', function () {
    var next = root.getAttribute('data-theme') === 'light' ? 'dark' : 'light';
    applyTheme(next);
    try { localStorage.setItem('shoug-theme', next); } catch (e) {}
  });
'''

FLASH_JS = '''
  var flashData = %s;
  var flashGrid = document.getElementById('flashGrid');
  if (flashGrid) {
    flashData.forEach(function (pair) {
      var card = document.createElement('div');
      card.className = 'flash';
      card.setAttribute('tabindex', '0');
      card.setAttribute('role', 'button');
      card.innerHTML = '<div class="flash-inner">' +
        '<div class="flash-face flash-front">' + pair[0] + '</div>' +
        '<div class="flash-face flash-back">' + pair[1] + '</div></div>';
      function flip() { card.classList.toggle('flipped'); }
      card.addEventListener('click', flip);
      card.addEventListener('keydown', function (e) {
        if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); flip(); }
      });
      flashGrid.appendChild(card);
    });
  }
'''

QUIZ_JS = '''
  var quizData = %s;
  var quizContainer = document.getElementById('quizContainer');
  var score = 0;

  quizData.forEach(function (item, qi) {
    var q = document.createElement('div');
    q.className = 'quiz-q';
    q.id = 'q' + (qi + 1);
    var opts = item.opts.map(function (opt, oi) {
      return '<button class="quiz-opt" data-qi="' + qi + '" data-oi="' + oi + '">' + opt + '</button>';
    }).join('');
    q.innerHTML = '<div class="q-src">' + item.src + '</div>' +
      '<p class="q-text">' + (qi + 1) + '. ' + item.q + '</p>' +
      '<div class="quiz-opts">' + opts + '</div>' +
      '<div class="quiz-feedback" id="fb-' + qi + '"></div>';
    quizContainer.appendChild(q);
  });

  var scoreBar = document.createElement('div');
  scoreBar.id = 'scoreBar';
  scoreBar.textContent = 'Score: 0 / ' + quizData.length;
  quizContainer.after(scoreBar);

  quizContainer.addEventListener('click', function (e) {
    if (!e.target.classList.contains('quiz-opt')) return;
    var btn = e.target;
    var qi = parseInt(btn.dataset.qi, 10);
    var oi = parseInt(btn.dataset.oi, 10);
    var group = btn.parentElement;
    if (group.dataset.locked === 'true') return;

    var fb = document.getElementById('fb-' + qi);
    if (oi === quizData[qi].correct) {
      btn.classList.add('correct');
      Array.prototype.forEach.call(group.children, function (b) { b.setAttribute('disabled', 'true'); });
      group.dataset.locked = 'true';
      fb.innerHTML = '<strong>Correct.</strong> ' + quizData[qi].why;
      fb.style.display = 'block';
      score++;
      scoreBar.textContent = 'Score: ' + score + ' / ' + quizData.length;
    } else {
      btn.classList.add('wrong');
      btn.setAttribute('disabled', 'true');
      fb.textContent = 'Not quite \\u2014 try another option.';
      fb.style.display = 'block';
    }
  });
'''

MAP_JS = '''
  var branches = Array.prototype.slice.call(document.querySelectorAll('.map-branch'));
  var expandAll = document.getElementById('expandAll');
  var collapseAll = document.getElementById('collapseAll');
  if (expandAll) {
    expandAll.addEventListener('click', function () {
      branches.forEach(function (b) { b.open = true; });
    });
  }
  if (collapseAll) {
    collapseAll.addEventListener('click', function () {
      branches.forEach(function (b) { b.open = false; });
    });
  }
'''


def head_meta(out_rel, page_title, description):
    """Favicons, canonical, social cards, hreflang and analytics for one page."""
    url = SITE + '/academics/other-courses/isc213/' + WRAPPER[out_rel]
    name = plain(page_title)
    jsonld = json.dumps({
        '@context': 'https://schema.org', '@type': 'WebPage', 'url': url,
        'name': html.unescape(page_title), 'description': html.unescape(description),
        'isPartOf': {'@type': 'WebSite', 'name': "Shoug's Digital Garden", 'url': SITE + '/'},
    }, ensure_ascii=False)
    return f'''<link rel="icon" type="image/png" sizes="256x256" href="/assets/shoug-favicon-v4.png">
<link rel="shortcut icon" type="image/png" href="/assets/shoug-favicon-v4.png">
<link rel="apple-touch-icon" sizes="180x180" href="/assets/shoug-apple-touch-icon-v4.png">
<link rel="canonical" href="{url}">
<meta property="og:title" content="{name}">
<meta property="og:description" content="{description}">
<meta property="og:url" content="{url}">
<meta property="og:type" content="article">
<meta property="og:image" content="{OG_IMAGE}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{name}">
<meta name="twitter:description" content="{description}">
<meta name="twitter:image" content="{OG_IMAGE}">
<script type="application/ld+json">{jsonld}</script>
<link rel="alternate" hreflang="en" href="{url}">
<link rel="alternate" hreflang="ar" href="{url}?lang=ar">
<link rel="alternate" hreflang="x-default" href="{url}">
{CLARITY}'''


def shell(meta, sections_html, scripts, page_title, description, out_rel):
    """Wrap page content in the shared ISC213 document shell."""
    toc = '\n'.join(
        f'      <li><a href="#{s["id"]}">{s["toc"]}</a></li>' for s in sections_html['toc'])
    meta_blocks = '\n'.join(
        f'    <div><strong>{value}</strong>{label}</div>' for value, label in meta['meta'])
    return f'''<!DOCTYPE html>
<html lang="en" data-theme="light" data-sg-styled>
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{page_title}</title>
<meta name="description" content="{description}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="{FONTS}" rel="stylesheet">
<link rel="stylesheet" href="/styles/isc213.css">
<link rel="stylesheet" href="/styles/a11y.css">
{head_meta(out_rel, page_title, description)}
</head>
<body>
<a class="shoug-skip-link" href="#main-content">Skip to content</a>
<div class="motif-bg"></div>

<header class="topbar">
  <div class="brand">
    <span class="mark">&#1758;</span>
    <div>
      <div class="brand-text">ISC213 \u00b7 {meta['title']}</div>
      <div class="brand-sub">{meta['brand_sub']}</div>
    </div>
  </div>
  <div class="bar-actions">
    <button id="themeToggle" type="button" aria-label="Toggle dark and light mode">
      <span id="themeIcon">&#9728;&#65038;</span> <span id="themeLabel">Light</span>
    </button>
  </div>
</header>

<div class="hero">
  <div class="bismillah arabic">&#1576;&#1616;&#1587;&#1618;&#1605;&#1616; &#1575;&#1604;&#1604;&#1617;&#1614;&#1607;&#1616; &#1575;&#1604;&#1585;&#1617;&#1614;&#1581;&#1618;&#1605;&#1614;&#1648;&#1606;&#1616; &#1575;&#1604;&#1585;&#1617;&#1614;&#1581;&#1616;&#1610;&#1605;&#1616;</div>
  <h1>{meta['h1']}</h1>
  <p class="lede">{meta['lede']}</p>
  <div class="hero-meta">
{meta_blocks}
  </div>
</div>

<nav class="toc">
  <div class="toc-inner">
    <div class="toc-label">JUMP TO A SECTION</div>
    <ol>
{toc}
    </ol>
  </div>
</nav>

<main id="main-content" tabindex="-1">
{sections_html['body']}
</main>

<footer>
  Built for offline, single-file studying \u00b7 ISC213 {meta['title']} \u00b7 Islamic Financial Transactions
</footer>

<script>
{scripts}
</script>
</body>
</html>
'''


def plain(text):
    """Entity-decoded text, re-escaped for an attribute value."""
    return html.escape(html.unescape(text), quote=True)


def section(sec_id, tag, num, h2, body):
    return f'''<section class="slide" id="{sec_id}">
  <div class="slide-tag">{tag}</div>
  <h2><span class="num">{num}</span> {h2}</h2>
{body.strip()}
</section>'''


# --------------------------------------------------------------------------- #
# cheat sheets
# --------------------------------------------------------------------------- #

def build_cheat_sheet(meta, sections, flashcards, out_rel):
    body = []
    toc = []
    for s in sections:
        toc.append({'id': s['id'], 'toc': s['h2']})
        body.append(section(s['id'], s['tag'], s['num'], s['h2'], s['body']))

    flash_id = f's{len(sections) + 1}'
    toc.append({'id': flash_id, 'toc': 'Flashcard glossary'})
    body.append(section(
        flash_id, 'Final check', f'{len(sections) + 1:02d}', 'Flashcard glossary',
        '<p>Click or press Enter on a card to flip it. If you hesitate on one, go back to the block above it.</p>'
        '<div class="flash-grid" id="flashGrid"></div>'))

    scripts = THEME_JS + (FLASH_JS % json.dumps([list(f) for f in flashcards], ensure_ascii=False))
    page = shell(
        meta,
        {'toc': toc, 'body': '\n'.join(body)},
        scripts,
        f"ISC213 \u00b7 {meta['title']}",
        plain(f"ISC213 Islamic Financial Transactions — {meta['title']}."),
        out_rel)
    write(out_rel, page)


# --------------------------------------------------------------------------- #
# mindmap
# --------------------------------------------------------------------------- #

def count_nodes(children):
    return sum(1 + count_nodes(kids) for _, _, kids in children)


def render_nodes(children, depth=0):
    if not children:
        return ''
    items = []
    for label, note, kids in children:
        note_html = f'<span class="node-note">{note}</span>' if note else ''
        items.append(f'<li class="node"><span class="node-label">{label}</span>{note_html}'
                     f'{render_nodes(kids, depth + 1)}</li>')
    return '<ul class="node-list">' + ''.join(items) + '</ul>'


def build_mindmap(out_rel):
    branches = []
    toc = []
    for n, (label, note, children) in enumerate(C.MINDMAP, start=1):
        branch_id = f'b{n}'
        toc.append({'id': branch_id, 'toc': label})
        branches.append(f'''<details class="map-branch" id="{branch_id}" open>
  <summary><span class="branch-num">{n:02d}</span> {label}
    <span class="branch-count">{count_nodes(children)} nodes</span></summary>
  <div class="map-body">
    <p>{note}</p>
    {render_nodes(children)}
  </div>
</details>''')

    body = ('<div class="map-controls">'
            '<button class="pill-btn" type="button" id="expandAll">Expand all</button>'
            '<button class="pill-btn" type="button" id="collapseAll">Collapse all</button>'
            '</div>\n' + '\n'.join(branches))

    page = shell(
        C.MINDMAP_META,
        {'toc': toc, 'body': body},
        THEME_JS + MAP_JS,
        'ISC213 \u00b7 Course Mindmap',
        'ISC213 Islamic Financial Transactions — a collapsible mindmap of Lectures 1 to 4.',
        out_rel)
    write(out_rel, page)


# --------------------------------------------------------------------------- #
# exams
# --------------------------------------------------------------------------- #

def build_exam(meta, mcq, written, out_rel):
    quiz_json = json.dumps(
        [{'q': q, 'src': src, 'opts': opts, 'correct': correct, 'why': why}
         for q, src, opts, correct, why in mcq], ensure_ascii=False)

    written_html = []
    for n, (q, src, answer) in enumerate(written, start=1):
        written_html.append(f'''<div class="written-q">
  <div class="q-src">{src}</div>
  <p class="q-text">{n}. {q}</p>
  <details class="model-answer"><summary>Show model answer</summary>
{answer.strip()}
  </details>
</div>''')

    body = [
        section('s1', f'Part one &middot; {meta["scope"]}', '01',
                f'Multiple choice &mdash; {len(mcq)} questions',
                '<p>One attempt per option. A correct answer locks the question and explains itself; a '
                'wrong one only disables that option, so you can keep trying. The running score sits at '
                'the bottom of the page.</p>'
                '<div id="quizContainer"></div>'),
        section('s2', f'Part two &middot; {meta["scope"]}', '02',
                f'Written questions &mdash; {len(written)} questions',
                '<p>Answer each in full before opening its model answer. The model answers are written at '
                'the length a full-mark response needs.</p>'
                + '\n'.join(written_html)),
    ]
    toc = [{'id': 's1', 'toc': f'Multiple choice ({len(mcq)})'},
           {'id': 's2', 'toc': f'Written questions ({len(written)})'}]

    page = shell(
        meta,
        {'toc': toc, 'body': '\n'.join(body)},
        THEME_JS + (QUIZ_JS % quiz_json),
        f"ISC213 \u00b7 {meta['title']}",
        plain(f"ISC213 Islamic Financial Transactions — practice {meta['title'].lower()} "
              f"covering {meta['scope']}."),
        out_rel)
    write(out_rel, page)


def write(rel, page):
    path = os.path.join(COURSE, rel)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as fh:
        fh.write(page)
    print('wrote', os.path.relpath(path, REPO))


def main():
    build_cheat_sheet(C.CHEAT_1_META, C.CHEAT_1_SECTIONS, C.CHEAT_1_FLASH,
                      'extra-resources/01-cheat-sheet-1/cheat-sheet-1.html')
    build_cheat_sheet(C.CHEAT_2_META, C.CHEAT_2_SECTIONS, C.CHEAT_2_FLASH,
                      'extra-resources/02-cheat-sheet-2/cheat-sheet-2.html')
    build_mindmap('extra-resources/03-mindmap/mindmap.html')
    build_exam(C.EXAM_1_META, C.EXAM_1_MCQ, C.EXAM_1_WRITTEN, 'exams/01-exam-1/exam-1.html')
    build_exam(C.EXAM_2_META, C.EXAM_2_MCQ, C.EXAM_2_WRITTEN, 'exams/02-exam-2/exam-2.html')

    # The final samples both halves evenly, then adds its own synthesis items.
    final_mcq = (C.EXAM_1_MCQ[::2] + C.EXAM_2_MCQ[::2] + C.FINAL_EXTRA_MCQ)
    final_written = (C.EXAM_1_WRITTEN[::3] + C.EXAM_2_WRITTEN[::3] + C.FINAL_EXTRA_WRITTEN)
    build_exam(C.FINAL_META, final_mcq, final_written, 'exams/03-final-exam/final-exam.html')


if __name__ == '__main__':
    main()
