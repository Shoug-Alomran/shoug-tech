#!/usr/bin/env python3
"""Archive paid source outside the public site, build Worker assets, seal Pages.

Run --archive --build-worker --seal once before deploying the course Worker.
The GitHub Pages pipeline runs --seal after all content generators. Original
source is retained under ignored .private-courses/ and in the Worker deployment.
"""
import argparse
import json
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / 'docs'
PRIVATE = ROOT / '.private-courses/ethics'
WORKER = ROOT / 'workers/course-access'
COURSE = 'academics/other-courses/ethcs303'
PROTECTED = [COURSE, 'ai-context/' + COURSE, 'javascripts/past-exam-practice.js']
PUBLIC_VIDEO = 'https://pub-1ae2691df7364eea93afb4e67996d97c.r2.dev/ethics/'

def protected_files():
    for rel in PROTECTED:
        path = DOCS / rel
        if path.is_file(): yield path
        elif path.is_dir(): yield from (p for p in path.rglob('*') if p.is_file())

def is_locked(path):
    return path.suffix == '.html' and 'data-course-locked="true"' in path.read_text()

def archive():
    copied = 0
    for source in protected_files():
        if is_locked(source) or source.name == '.DS_Store': continue
        destination = PRIVATE / source.relative_to(DOCS)
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, destination)
        copied += 1
    print(f'Preserved {copied} paid source files in .private-courses/ethics (not published or committed).')

def build_worker():
    if not (PRIVATE / COURSE / 'index.html').exists():
        raise SystemExit('Archive paid source before building private assets.')
    assets = WORKER / 'assets'
    shutil.copytree(PRIVATE, assets, dirs_exist_ok=True)
    for path in assets.rglob('*'):
        if path.suffix in {'.html', '.json', '.js', '.vtt'}:
            text = path.read_text().replace(PUBLIC_VIDEO, '/course-media/ethics/')
            if path.suffix == '.html':
                # No replay of private lessons; no offline copies after sign-out.
                import re
                text = re.sub(r'<script\b[^>]*>[^<]*www\.clarity\.ms/tag/[\s\S]*?</script>', '', text, flags=re.I)
                text = text.replace('</head>', '<script defer src="/course-access/session-sync.js"></script></head>')
            path.write_text(text)
    access = assets / 'course-access'
    access.mkdir(exist_ok=True)
    for source, dest in [('gate.html', 'index.html'), ('gate.js', 'gate.js'), ('session-sync.js', 'session-sync.js')]:
        shutil.copy2(WORKER / 'src' / source, access / dest)
    for relative in ['checkout/ethics/index.html', 'admin/transfers/index.html',
                     'styles/course-transfers.css', 'javascripts/course-transfers.js',
                     'styles/site-shell.css', 'javascripts/site-shell.js', 'javascripts/mobile-navigation.js', 'styles/ethics-study-tools.css', 'javascripts/ethics-study-tools.js', 'javascripts/email-verification.js', 'javascripts/firebase-auth.js', 'sw.js']:
        target = assets / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(DOCS / relative, target)
    shutil.copytree(DOCS / 'course-access/samples', access / 'samples', dirs_exist_ok=True)
    print('Built private Worker assets; all lesson video URLs now use authenticated routes.')

def seal():
    gate = (WORKER / 'src/gate.html').read_text()
    count = 0
    for path in list(protected_files()):
        if path.suffix == '.html':
            route = '/' + path.relative_to(DOCS).as_posix()
            if route.endswith('/index.html'): route = route[:-len('index.html')]
            path.write_text(gate.replace('</head>', f'<link rel="canonical" href="https://shoug-tech.com{route}"><meta property="og:title" content="Ethics course · Access required"><meta property="og:url" content="https://shoug-tech.com{route}"></head>'))
        else: path.unlink()
        count += 1
    # Public mirrors display only the gate, even when JavaScript is disabled.
    access = DOCS / 'course-access'
    access.mkdir(exist_ok=True)
    (access / 'index.html').write_text(gate)
    shutil.copy2(WORKER / 'src/gate.js', access / 'gate.js')
    for name in ['search-index.json', 'search-pdf-index.json']:
        path = DOCS / name
        if not path.exists(): continue
        rows = json.loads(path.read_text())
        if not isinstance(rows, list): raise SystemExit(f'Unexpected {name} shape; refusing to publish.')
        rows = [row for row in rows if not any(COURSE in str(row.get(key, '')) for key in ['url', 'u', 'f', 'path'])]
        path.write_text(json.dumps(rows, ensure_ascii=False, separators=(',', ':')))
    print(f'Sealed {count} public files and removed paid content from search indexes.')

def check():
    leaks = [str(p.relative_to(DOCS)) for p in protected_files() if not is_locked(p)]
    if leaks: raise SystemExit('Unprotected paid files in public output: ' + ', '.join(leaks[:10]))
    print('Public output contains access gates only; no paid files.')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    for flag in ['archive', 'build-worker', 'seal', 'check']: parser.add_argument('--' + flag, action='store_true')
    args = parser.parse_args()
    if args.archive: archive()
    if args.build_worker: build_worker()
    if args.seal: seal()
    if args.check: check()
