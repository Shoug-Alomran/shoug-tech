#!/usr/bin/env python3
"""Build the SE423 Listing Vault page from scripts/se423_annotated/listing_vault_data.py."""
import html
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from se423_annotated.listing_vault_data import CHAPTERS  # noqa: E402

OUT = os.path.join(os.path.dirname(HERE), 'docs/academics/software-engineering/se423/extra-resources/listing-vault/listing-vault.html')


def item(text):
    term, _, explain = text.partition(' | ')
    term = html.escape(term, quote=False)
    return '<b>%s</b> — %s' % (term, html.escape(explain, quote=False)) if explain else term


def main():
    chapters = []
    for ch in CHAPTERS:
        lists = [dict(l, t=html.escape(l['t'], quote=False), items=[item(i) for i in l['items']], note=html.escape(l['note'], quote=False))
                 for l in ch['lists']]
        chapters.append(dict(ch, title=html.escape(ch['title'], quote=False), sub=html.escape(ch['sub'], quote=False), lists=lists))
    with open(os.path.join(HERE, 'se423_annotated/listing_vault_template.html'), encoding='utf-8') as fh:
        page = fh.read()
    data = json.dumps(chapters, ensure_ascii=False).replace('</', '<\\/')
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, 'w', encoding='utf-8') as fh:
        fh.write(page.replace('__DATA__', data))
    print('%d decks, %d lists, %d items' % (len(chapters), sum(len(c['lists']) for c in chapters), sum(len(l['items']) for c in chapters for l in c['lists'])))


if __name__ == '__main__':
    main()
