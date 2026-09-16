#!/usr/bin/env python3
"""Install translation only in lesson documents, never their site wrappers."""
from pathlib import Path
import os
import re

DOCS = Path(__file__).resolve().parents[1] / 'docs'


def main():
    count = 0
    removed = 0
    for path in DOCS.glob('**/slide-breakdowns/**/*.html'):
        text = path.read_text()
        if path.name == 'index.html':
            # Retain the stylesheet to suppress legacy site-level language
            # buttons here, but never run lesson translation in the wrapper.
            cleaned = re.sub(r'<script\b[^>]*src=[\"\'][^\"\']*breakdown-language\.js(?:\?[^\"\']*)?[\"\'][^>]*>\s*</script>\s*', '', text, flags=re.I)
            if 'breakdown-language.css' not in cleaned:
                css = os.path.relpath(DOCS / 'styles/breakdown-language.css', path.parent)
                cleaned = cleaned.replace('</head>', f'<link rel="stylesheet" href="{css}">\n</head>', 1)
            if cleaned != text:
                path.write_text(cleaned)
                removed += 1
            continue
        if 'breakdown-language.js' in text:
            continue
        js = os.path.relpath(DOCS / 'javascripts/breakdown-language.js', path.parent)
        css = os.path.relpath(DOCS / 'styles/breakdown-language.css', path.parent)
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
