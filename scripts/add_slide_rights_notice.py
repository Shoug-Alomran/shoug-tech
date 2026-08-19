#!/usr/bin/env python3
"""Put the Prince Sultan University rights notice on every slide page.

The decks hosted on this site are PSU teaching material, so each slides page —
the section listing and every individual deck viewer — carries a notice saying
the University owns the content and it is shared for personal study only.

The accent colours come from the page's own CSS variables, so the notice picks
up each track's theme (purple for CS/SE, red for cybersecurity).

Usage:
    python3 scripts/add_slide_rights_notice.py           # add where missing
    python3 scripts/add_slide_rights_notice.py --check   # report only
"""

import argparse
import os
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ACADEMICS = os.path.join(REPO, 'docs', 'academics')
MARKER = 'PRINCE SULTAN UNIVERSITY'

EN = ('These slides are the intellectual property of Prince Sultan University. All academic '
      'content, materials, and resources are owned by the University and are shared here solely '
      'for personal study purposes. Redistribution or reproduction without explicit permission '
      'from Prince Sultan University is prohibited.')
AR = ('ملكية جامعة الأمير سلطان — هذه الشرائح ملك فكري لجامعة الأمير سلطان. جميع المحتويات '
      'والمواد والموارد الأكاديمية مملوكة للجامعة وتُعرض هنا لأغراض الدراسة الشخصية فقط. '
      'يُمنع إعادة النشر أو النسخ دون إذن صريح من جامعة الأمير سلطان.')

NOTICE = (
    '\n                <div class="psu-rights-note"'
    ' style="margin: 32px 40px 40px; padding: 20px 24px;'
    ' border: 1px solid rgba(184,41,234,0.25); background: rgba(184,41,234,0.04);'
    ' display: flex; align-items: flex-start; gap: 16px;">\n'
    '                    <div data-ar-text="الحقوق"'
    ' style="flex: 0 0 auto; font-family: \'JetBrains Mono\', monospace; font-size: 0.62rem;'
    ' font-weight: 700; letter-spacing: 0.18em; text-transform: uppercase;'
    ' color: var(--brand-purple, #b829ea); padding-top: 2px;">&#9632; RIGHTS</div>\n'
    '                    <div data-ar-text="%s"'
    ' style="font-family: \'JetBrains Mono\', monospace; font-size: 0.72rem; line-height: 1.6;'
    ' color: #a09fa6;">\n'
    '                        <span style="color: var(--text-purple-bright, #d978ff);'
    ' font-weight: 700;">PROPERTY OF PRINCE SULTAN UNIVERSITY</span> &mdash; %s\n'
    '                    </div>\n'
    '                </div>\n            ' % (AR, EN)
)


def slide_pages():
    for dirpath, _dirnames, filenames in os.walk(ACADEMICS):
        if 'index.html' in filenames and 'slides' in dirpath.split(os.sep):
            yield os.path.join(dirpath, 'index.html')


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--check', action='store_true', help='report without writing')
    args = ap.parse_args()

    added = skipped = noslot = 0
    for path in slide_pages():
        with open(path, encoding='utf-8') as fh:
            html = fh.read()
        if MARKER in html:
            skipped += 1
            continue
        close = html.rfind('</main>')
        if close < 0:
            noslot += 1
            continue
        html = html[:close] + NOTICE + html[close:]
        added += 1
        if not args.check:
            with open(path, 'w', encoding='utf-8') as fh:
                fh.write(html)
    print('%s notice on %d page(s); %d already had one%s'
          % ('would add' if args.check else 'added', added, skipped,
             '; %d had nowhere to put it' % noslot if noslot else ''))
    return 1 if (args.check and added) else 0


if __name__ == '__main__':
    sys.exit(main())
