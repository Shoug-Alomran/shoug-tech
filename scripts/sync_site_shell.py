#!/usr/bin/env python3
"""Apply shared shell markup and saved color-theme support before publishing."""
from pathlib import Path
import re
import sys
ROOT=Path(__file__).resolve().parent.parent
header=(ROOT/'templates/site-header.html').read_text()
footer=(ROOT/'templates/site-footer.html').read_text()
count=0

def add_head_asset(document, markup):
    if re.search(r'</head\s*>', document, flags=re.I):
        return re.sub(r'</head\s*>', markup + '\n</head>', document, count=1, flags=re.I)
    return re.sub(r'<body\b', markup + '\n<body', document, count=1, flags=re.I)

for page in (ROOT/'docs').rglob('*.html'):
    s=page.read_text()
    original=s
    if '/styles/site-shell.css' not in s:
        s=add_head_asset(s, '<link rel="stylesheet" href="/styles/site-shell.css">')
    if '--assets-only' not in sys.argv and '<header class="shoug-site-header">' in s:
        s=re.sub(r'<header class="shoug-site-header">.*?</header>',lambda _:header,s,count=1,flags=re.S)
        s=re.sub(r'<footer class="shoug-site-footer">.*?</footer>',lambda _:footer,s,count=1,flags=re.S)
    elif '/javascripts/site-palette.js' not in s:
        s=add_head_asset(s, '<script defer src="/javascripts/site-palette.js"></script>')
    if s!=original: page.write_text(s);count+=1
print(f'Synchronized palette support and shared site shells on {count} pages.')
