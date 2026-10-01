#!/usr/bin/env python3
"""Keep standard site pages on the shared header/footer source during publishing.
Standalone embedded study tools retain their own compact controls.
"""
from pathlib import Path
import re
ROOT=Path(__file__).resolve().parent.parent
header=(ROOT/'templates/site-header.html').read_text()
footer=(ROOT/'templates/site-footer.html').read_text()
count=0
for page in (ROOT/'docs').rglob('*.html'):
    s=page.read_text()
    if '<header class="shoug-site-header">' not in s: continue
    original=s
    s=re.sub(r'<header class="shoug-site-header">.*?</header>',lambda _:header,s,count=1,flags=re.S)
    s=re.sub(r'<footer class="shoug-site-footer">.*?</footer>',lambda _:footer,s,count=1,flags=re.S)
    if '/styles/site-shell.css' not in s:
        s=s.replace('</head>','<link rel="stylesheet" href="/styles/site-shell.css"></head>')
    if s!=original: page.write_text(s);count+=1
print(f'Synchronized {count} site shells.')
