#!/usr/bin/env python3
"""Render the ISC213 standalone study pages.

Emits the midterm cheat sheet, four lesson mindmaps, and six practice exams into
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
import re

import isc213_content as C

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
COURSE = os.path.join(REPO, 'docs', 'academics', 'other-courses', 'isc213')

SITE = 'https://shoug-tech.com'
OG_IMAGE = f'{SITE}/assets/og-banner.png'

# These documents only ever load inside their wrapper page's iframe, so the
# canonical points at the wrapper — a self-canonical would compete with the page
# readers are meant to land on. Same rule scripts/backfill_seo_metadata.py uses.
WRAPPER = {
    'extra-resources/01-cheat-sheet/cheat-sheet.html': 'extra-resources/01-cheat-sheet/',
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
    url = SITE + '/academics/other-courses/isc213/' + WRAPPER.get(out_rel, out_rel.rsplit('/', 1)[0] + '/')
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


def build_mindmap(n, out_rel):
    """Reuse ETHCS303's interactive canvas, details panel and print layout."""
    template = os.path.join(REPO, 'docs/academics/other-courses/ethcs303/extra-resources/mindmap/03-utilitarianism/utilitarianism.html')
    with open(template, encoding='utf-8') as fh:
        page = fh.read()
    def node(item, key):
        label, note, children = item
        result = {'id': key, 'label': html.unescape(label),
                  'desc': '<p>' + note + '</p>'}
        if children:
            result['children'] = [node(child, f'{key}-{i}') for i, child in enumerate(children)]
        return result
    data = node(C.MINDMAP[n - 1], 'root')
    title = f'ISC213 — Lecture {n} Mindmap'
    description = f'Interactive mindmap for ISC213 Lecture {n}: ' + html.unescape(C.MINDMAP[n - 1][1])
    start = page.index('        const DATA = {')
    end = page.index('\n        // ', start)
    page = page[:start] + '        const DATA = ' + json.dumps(data, ensure_ascii=False) + ';\n' + page[end:]
    start = page.index('    <meta name="description"')
    end = page.index('</head>', start)
    page = page[:start] + head_meta(out_rel, title, plain(description)) + '\n<meta name="description" content="' + plain(description) + '">\n' + page[end:]
    page = page.replace('Utilitarianism — Mindmap', title)
    page = page.replace('Moral Systems, Ethical Concepts & Theories — Utilitarianism', f'ISC213 — Lecture {n}')
    write(out_rel, page)


def exam_meta(title, scope, mcq, written):
    return {'title': title, 'h1': title, 'brand_sub': scope + ' · Practice exam',
            'scope': scope,
            'lede': f'{len(mcq)} multiple-choice questions and {len(written)} written questions covering {scope}. Try each question before revealing its explanation or model answer. Based on the course materials.',
            'meta': [(str(len(mcq)), 'multiple choice'), (str(len(written)), 'written questions'), (scope, 'coverage')]}


def lesson_questions(n):
    # Every existing single-lesson question is retained, including final-bank items.
    mcq = [q for q in C.EXAM_1_MCQ + C.EXAM_2_MCQ + C.FINAL_EXTRA_MCQ if re.match(rf'^L{n} ·', q[1])]
    written = [q for q in C.EXAM_1_WRITTEN + C.EXAM_2_WRITTEN + C.FINAL_EXTRA_WRITTEN if re.match(rf'^L{n} ·', q[1])]
    # A structured written question for every teaching block closes coverage gaps.
    prompts = {
        1: ['Define transactions, finance and contemporary, then classify sale, waqf, debt forgiveness and mortgage.',
            'Explain all four cases included in contemporary financial transactions, with an example distinguishing a changed procedure from a changed name.',
            'Name the four relevant terms used for newly emerged issues requiring a ruling.',
            'Explain the four characteristics of financial transactions, their evidence, and the contrast with acts of worship.'],
        2: ['Define ijtihad and explain all nine qualifications of a researcher, including character and practical knowledge.',
            'List the eight steps to reaching a ruling in order. Explain when personal opinion is considered and what to do if no legitimate ruling is reached.',
            'Define a right and reconstruct its classification from political and civil rights down to family and financial rights, giving examples.',
            'Compare personal, material and incorporeal financial rights. Classify a debt owed, land ownership and an innovation, explaining each choice.'],
        3: ['Define incorporeal rights and explain why they qualify as property in fiqh. Name the three forms and the dates given in the lecture.',
            'Explain who counts as an author, the role of a publisher for anonymous work, and what counts as a creative contribution. Compare literary and financial rights and explain the four reasons for recognition.',
            'Explain patent rights, disclosure, duration and registration. Distinguish all four certificate types and explain the three reasons for recognition.',
            'Explain the components of a trade name, the functions of a trademark, the two owner rights and the reasons and condition for recognition.'],
        4: ['Define insurance linguistically and technically and explain its original purpose and later development.',
            'Explain collaborative insurance, its evidence, three historical forms and three modern systems, with the ruling for each.',
            'Describe the emergence of commercial insurance, its five elements, all five risk conditions and its three types.',
            'Explain gharar, gambling and both forms of riba in commercial insurance, then discuss each of the three exceptions with its limits.',
            'Compare commercial and collaborative insurance in contract, purpose, risk, ownership of surplus and Shariah ruling.']}
    sections = [s for s in C.CHEAT_1_SECTIONS + C.CHEAT_2_SECTIONS if s['tag'].startswith(f'Lecture {n} ·')]
    assert len(sections) == len(prompts[n])
    written += [(q, s['tag'].replace(f'Lecture {n}', f'L{n}'), s['body']) for q, s in zip(prompts[n], sections)]
    return mcq, written


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
    build_cheat_sheet(C.CHEAT_META, C.CHEAT_SECTIONS, C.CHEAT_FLASH,
                      'extra-resources/01-cheat-sheet/cheat-sheet.html')
    for n in range(1, 5):
        build_mindmap(n, f'extra-resources/03-mindmap/0{n}-lecture-{n}/lecture-{n}.html')
        mcq, written = lesson_questions(n)
        build_exam(exam_meta(f'Lecture {n} Comprehensive Exam', f'Lecture {n}', mcq, written),
                   mcq, written, f'exams/lesson-{n}/lesson-{n}.html')
    mcq = C.EXAM_1_MCQ + C.EXAM_2_MCQ
    written = C.EXAM_1_WRITTEN + C.EXAM_2_WRITTEN
    build_exam(exam_meta('Midterm 1', 'Lectures 1–4', mcq, written), mcq, written,
               'exams/01-midterm-1/midterm-1.html')

    # The final samples both halves evenly, then adds its own synthesis items.
    final_mcq = (C.EXAM_1_MCQ[::2] + C.EXAM_2_MCQ[::2] + C.FINAL_EXTRA_MCQ)
    final_written = (C.EXAM_1_WRITTEN[::3] + C.EXAM_2_WRITTEN[::3] + C.FINAL_EXTRA_WRITTEN)
    build_exam(C.FINAL_META, final_mcq, final_written, 'exams/03-final-exam/final-exam.html')


if __name__ == '__main__':
    main()
