"""CS316 annotated slides: one namespace per deck, built from the shared study content.

Every slide is shown as the original image (whole=True) because most decks keep their
content in pictures. Notes come from each deck's `ann`; a deck's quiz questions also
appear on the slide they test.
"""
import hashlib
import random

from .common import DECKS, mcq, short, tip, trap, trick
from . import content1, content2, content3
from .titles import TITLES

CONTENT = {
    'd01': content1.D01, 'd02': content1.D02, 'd03': content1.D03, 'd04': content1.D04,
    'd05': content2.D05, 'd06': content2.D06, 'd07': content2.D07, 'd08': content2.D08, 'd09': content2.D09,
    'd10': content3.D10, 'd11': content3.D11, 'd12': content3.D12, 'd13': content3.D13, 'd14': content3.D14, 'd15': content3.D15,
}


def options(item):
    opts = [item['correct'], *item['wrong']]
    random.Random(hashlib.sha1(item['q'].encode()).hexdigest()).shuffle(opts)
    return opts, opts.index(item['correct'])


def annotations(key, data):
    out = {}
    for n in range(1, data['count'] + 1):
        ann = {'whole': True}
        if n in TITLES.get(key, {}):
            ann['title'] = TITLES[key][n]
        note = data['ann'].get(n)
        if note:
            ann['notes'] = [note['note']]
            tips = []
            if note['tip']:
                tips.append(tip(note['tip']))
            if note['trap']:
                tips.append(trap(note['trap']))
            if note['trick']:
                tips.append(trick(note['trick']))
            ann['tips'] = tips
            if note['weight']:
                ann['weight'] = note['weight']
        exam = []
        for item in data['mcq']:
            if item['slide'] == n:
                opts, a = options(item)
                exam.append(mcq(item['q'], opts, a, item['why']))
        for item in data['short']:
            if item['slide'] == n:
                exam.append(short(item['q'], item['answer']))
        if exam:
            ann['exam'] = exam
        out[n] = ann
    return out


def chapter(key):
    slug, file, folder, label = DECKS[key]
    head, title = label.split(': ', 1)
    data = CONTENT[key]
    return type(key, (), {
        'AUTO_SLIDES': True,
        'DECK': {'key': key, 'slug': slug, 'file': file, 'title': title, 'chapter': head,
                 'pdf': '/academics/computer-science/cs316/slides/%s/' % folder, 'lede': data['lede']},
        'ANN': annotations(key, data),
    })


d01, d02, d03, d04, d05, d06, d07, d08, d09, d10, d11, d12, d15, d13, d14 = (chapter(k) for k in DECKS)
