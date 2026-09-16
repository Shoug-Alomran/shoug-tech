#!/usr/bin/env python3
"""Install translation only in lesson documents, never their site wrappers."""
from pathlib import Path
import hashlib
import os
import re

DOCS = Path(__file__).resolve().parents[1] / 'docs'


def main():
    js_version = hashlib.sha256((DOCS / 'javascripts/breakdown-language.js').read_bytes()).hexdigest()[:12]
    css_version = hashlib.sha256((DOCS / 'styles/breakdown-language.css').read_bytes()).hexdigest()[:12]
    count = 0
    removed = 0
    for path in DOCS.glob('**/slide-breakdowns/**/*.html'):
        text = path.read_text()
        if path.name == 'index.html':
            # Site wrappers keep their original global language controls.
            cleaned = re.sub(r'<script\b[^>]*src=[\"\'][^\"\']*breakdown-language\.js(?:\?[^\"\']*)?[\"\'][^>]*>\s*</script>\s*', '', text, flags=re.I)
            cleaned = re.sub(r'<link\b[^>]*href=[\"\'][^\"\']*breakdown-language\.css(?:\?[^\"\']*)?[\"\'][^>]*>\s*', '', cleaned, flags=re.I)
            if cleaned != text:
                path.write_text(cleaned)
                removed += 1
            continue
        js = os.path.relpath(DOCS / 'javascripts/breakdown-language.js', path.parent)
        css = os.path.relpath(DOCS / 'styles/breakdown-language.css', path.parent)
        js += '?v=' + js_version
        css += '?v=' + css_version
        if f'src="{js}"' in text and f'href="{css}"' in text:
            continue
        text = re.sub(r'<script\b[^>]*src=[\"\'][^\"\']*breakdown-language\.js(?:\?[^\"\']*)?[\"\'][^>]*>\s*</script>\s*', '', text, flags=re.I)
        text = re.sub(r'<link\b[^>]*href=[\"\'][^\"\']*breakdown-language\.css(?:\?[^\"\']*)?[\"\'][^>]*>\s*', '', text, flags=re.I)
        # Load early to retain the saved choice before legacy startup writes EN.
        includes = f'\n<link rel="stylesheet" href="{css}">\n<script src="{js}"></script>\n'
        text, inserted = re.subn(r'<head\b[^>]*>', lambda match: match.group(0) + includes, text, count=1, flags=re.I)
        if not inserted:
            raise ValueError(f'Missing head: {path}')
        # Legacy startup must leave the English source intact for an
        # exact restoration. The shared controller applies the saved language.
        text = text.replace('var l = initialLang();', "var l = 'en';")
        text = text.replace("try { localStorage.setItem('shoug-lang', l); } catch (e) { }", '')
        path.write_text(text)
        count += 1
    print(f'Installed on {count} lesson documents; removed from {removed} site wrappers')


if __name__ == '__main__':
    main()
