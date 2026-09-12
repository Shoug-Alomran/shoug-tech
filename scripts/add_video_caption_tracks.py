#!/usr/bin/env python3
"""Put a <track> on every video lesson page that has a caption file.

build_ethics_video_pages.py emits the same markup, but a full rebuild rewrites
each page from the section index's chrome and undoes any formatting pass over
these files. This edits the <video> tag in place instead, so it is safe to run
against pages that have been hand-formatted or reformatted since.

Usage:
    python3 scripts/add_video_caption_tracks.py           # add what's missing
    python3 scripts/add_video_caption_tracks.py --check   # report, write nothing
"""

import argparse
import importlib.util
import re
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
spec = importlib.util.spec_from_file_location('pages', REPO / 'scripts' / 'build_ethics_video_pages.py')
pages = importlib.util.module_from_spec(spec)
spec.loader.exec_module(pages)

VIDEO_TAG_RE = re.compile(r'(<video\b[^>]*>)')
TRACK_RE = re.compile(r'<track\b[^>]*>')


def track_for(video):
    return ('<track kind="captions" srclang="ar" label="العربية (تلقائية)" default '
            'src="%scaptions/%s.vtt">' % (pages.SECTION_URL, video['slug']))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true', help='report drift, write nothing')
    args = parser.parse_args()

    added, already, missing = [], [], []
    for video in pages.VIDEOS:
        vtt = pages.SECTION / 'captions' / (video['slug'] + '.vtt')
        page = pages.SECTION / video['slug'] / 'index.html'
        if not vtt.exists():
            missing.append(video['slug'])
            continue
        if not page.exists():
            raise SystemExit('No page for ' + video['slug'])
        html = page.read_text(encoding='utf-8')
        track = track_for(video)
        if track in html:
            already.append(video['slug'])
            continue
        # Replace a stale track (different path or language) rather than stack them.
        html = TRACK_RE.sub('', html, count=1)
        html, count = VIDEO_TAG_RE.subn(lambda m: m.group(1) + track, html, count=1)
        if not count:
            raise SystemExit('No <video> tag in ' + str(page))
        added.append(video['slug'])
        if not args.check:
            page.write_text(html, encoding='utf-8')

    verb = 'would add' if args.check else 'added'
    print('%s %d track(s); %d already current; %d without captions'
          % (verb, len(added), len(already), len(missing)))
    for slug in added:
        print('  + ' + slug)
    if missing:
        print('  no caption file yet: ' + ', '.join(missing))
    return 1 if (args.check and added) else 0


if __name__ == '__main__':
    raise SystemExit(main())
