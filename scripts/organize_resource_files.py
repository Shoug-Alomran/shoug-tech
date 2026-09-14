#!/usr/bin/env python3
"""Keep local resource documents beside their existing dedicated viewer pages.
Run after page generators; updates local references without changing file bytes.
"""
from pathlib import Path
from urllib.parse import unquote, urlsplit, quote
import re
import hashlib
import os

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / 'docs'
EXTENSIONS = {'.pdf', '.docx', '.pptx', '.xlsx', '.zip'}
ATTR = re.compile(r'((?:href|src|data-pdf-src)\s*=\s*[\"\'])([^\"\']+)([\"\'])')

def resolve(value, page):
    parts = urlsplit(value)
    if parts.scheme or parts.netloc:
        if parts.netloc != 'shoug-tech.com':
            return None
    return (DOCS / unquote(parts.path).lstrip('/') if parts.path.startswith('/') else page.parent / unquote(parts.path)).resolve()

def main():
    candidates = {}
    for page in DOCS.rglob('index.html'):
        for match in ATTR.finditer(page.read_text()):
            if 'href' in match[1]:
                continue
            source = resolve(match[2], page)
            if source and source.exists() and source.suffix.lower() in EXTENSIONS and not source.parent.samefile(page.parent):
                candidates.setdefault(source, set()).add(page.parent / source.name)
    for source in DOCS.rglob('*'):
        if source.is_file() and source.suffix.lower() in EXTENSIONS and (source.parent / source.stem).is_dir():
            candidates.setdefault(source, set()).add(source.parent / source.stem / source.name)
    moves = {}
    for source, targets in candidates.items():
        matching = source.parent / source.stem / source.name
        if matching in targets:
            targets = {matching}
        if len(targets) != 1:
            print('Shared resource (kept):', source.relative_to(ROOT))
            continue
        target = next(iter(targets))
        if target.exists():
            print('Destination already exists (kept):', target.relative_to(ROOT))
            continue
        moves[source] = target
    for folder in (DOCS, ROOT / 'scripts'):
        for page in folder.rglob('*'):
            if not page.is_file() or page == Path(__file__).resolve() or page.suffix not in {'.html', '.json', '.xml', '.py', '.js', '.md', '.txt'}:
                continue
            try:
                original = page.read_text()
            except UnicodeDecodeError:
                continue
            def replace(match):
                source = resolve(match[2], page)
                if source not in moves:
                    return match[0]
                parts = urlsplit(match[2])
                target = moves[source]
                path = '/' + target.relative_to(DOCS).as_posix() if parts.path.startswith('/') else os.path.relpath(target, page.parent)
                path = quote(path, safe='/.-_')
                if parts.netloc:
                    path = parts.scheme + '://' + parts.netloc + path
                if parts.query: path += '?' + parts.query
                if parts.fragment: path += '#' + parts.fragment
                return match[1] + path + match[3]
            updated = ATTR.sub(replace, original)
            for source, target in moves.items():
                old = source.relative_to(DOCS).as_posix()
                new = target.relative_to(DOCS).as_posix()
                # Literal site paths in manifests, generators, and metadata.
                updated = updated.replace(old, new)
            if updated != original:
                page.write_text(updated)
    for source, target in moves.items():
        digest = hashlib.sha256(source.read_bytes()).digest()
        source.rename(target)
        assert hashlib.sha256(target.read_bytes()).digest() == digest
    print(f'Moved {len(moves)} resources; verified identical file contents.')

if __name__ == '__main__':
    main()
