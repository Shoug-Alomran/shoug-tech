#!/usr/bin/env python3
"""Install the shared, full-content language controller on every slide breakdown."""
from pathlib import Path
import os
import re

DOCS = Path(__file__).resolve().parents[1] / 'docs'


def main():
    count = 0
    for path in DOCS.glob('**/slide-breakdowns/**/*.html'):
        text = path.read_text()
        if 'breakdown-language.js' in text:
            continue
        js = os.path.relpath(DOCS / 'javascripts/breakdown-language.js', path.parent)
        css = os.path.relpath(DOCS / 'styles/breakdown-language.css', path.parent)
        # Load early to retain the saved choice before legacy startup writes EN.
        includes = f'\n<link rel="stylesheet" href="{css}">\n<script src="{js}"></script>\n'
        text, inserted = re.subn(r'<head\b[^>]*>', lambda match: match.group(0) + includes, text, count=1, flags=re.I)
        if not inserted:
            raise ValueError(f'Missing head: {path}')
        # Existing wrapper startup must leave the English source intact for an
        # exact restoration. The shared controller applies the saved language.
        text = text.replace('var l = initialLang();', "var l = 'en';")
        text = text.replace("try { localStorage.setItem('shoug-lang', l); } catch (e) { }", '')
        path.write_text(text)
        count += 1
    print(f'Installed language controller on {count} breakdown pages')


if __name__ == '__main__':
    main()
