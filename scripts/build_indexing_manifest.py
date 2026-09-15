#!/usr/bin/env python3
"""Build the edge SEO manifest from real files; never infer PDF wrapper equivalence."""
import json
import re
from pathlib import Path
from urllib.parse import quote, unquote, urljoin, urlsplit

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / 'docs'
OUTPUT = ROOT / 'workers/indexing/src/manifest.json'
ORIGIN = 'https://shoug-tech.com'


def build():
    redirects = {
        '/Academics/software-engineering/SE201/Chapter-2/Software-Processes.html':
        '/academics/software-engineering/se201/slide-breakdowns/02-chapter-2-software-processes/',
    }
    canonicals = {}
    candidates = {}
    for pdf in sorted(DOCS.rglob('*.pdf')):
        relative = pdf.relative_to(DOCS).as_posix()
        path = '/' + relative
        canonical = ORIGIN + quote(path, safe='/')
        wrapper = pdf.parent / 'index.html'
        if wrapper.is_file():
            html = wrapper.read_text()
            refs = re.findall(r'(?:src|data-pdf-src)=["\']([^"\']+)["\']', html)
            wrapper_url = ORIGIN + quote('/' + pdf.parent.relative_to(DOCS).as_posix() + '/', safe='/')
            if any(unquote(urlsplit(urljoin(wrapper_url, ref)).path) == path for ref in refs):
                canonical = wrapper_url
        canonicals[path] = canonical
        # PDF nesting moved flat course /slides/name.pdf into /slides/topic/name.pdf.
        # Accept only unambiguous names, and never shadow an existing file.
        parts = relative.split('/')
        if 'slides' in parts:
            i = parts.index('slides')
            old = '/' + '/'.join(parts[:i + 1] + [pdf.name])
            candidates.setdefault(old, []).append(path)
    for old, targets in candidates.items():
        if len(targets) == 1 and not (DOCS / old.lstrip('/')).exists():
            redirects[old] = quote(targets[0], safe='/')
    for destination in redirects.values():
        target = DOCS / unquote(destination).lstrip('/')
        if destination.endswith('/'):
            target /= 'index.html'
        assert target.is_file(), destination
    return {'redirects': redirects, 'canonicals': canonicals}


if __name__ == '__main__':
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    manifest = build()
    OUTPUT.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + '\n')
    print(f"Indexing manifest: {len(manifest['redirects'])} redirects, {len(manifest['canonicals'])} PDF canonicals")
