#!/usr/bin/env python3
"""Transcribe the ETHCS303 recordings into WebVTT caption tracks.

Captions are written to docs/.../video-explanations/captions/<slug>.vtt, which
is where build_ethics_video_pages.py looks when it decides whether a player
gets a <track> element. Rebuild the pages afterwards.

Needs faster-whisper (pip install faster-whisper) and the local recordings.

Usage:
    python3 scripts/transcribe_ethics_videos.py --only vishing
    python3 scripts/transcribe_ethics_videos.py --model medium
"""

import argparse
import importlib.util
import subprocess
import tempfile
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
spec = importlib.util.spec_from_file_location('pages', REPO / 'scripts' / 'build_ethics_video_pages.py')
pages = importlib.util.module_from_spec(spec)
spec.loader.exec_module(pages)

CAPTIONS = pages.SECTION / 'captions'


def stamp(seconds):
    ms = int(round(seconds * 1000))
    hours, ms = divmod(ms, 3600000)
    minutes, ms = divmod(ms, 60000)
    secs, ms = divmod(ms, 1000)
    return '%02d:%02d:%02d.%03d' % (hours, minutes, secs, ms)


def extract_audio(source, target):
    """16 kHz mono wav — what the model wants, and small enough to stream."""
    subprocess.run(['ffmpeg', '-y', '-v', 'error', '-nostdin', '-i', str(source),
                    '-vn', '-ac', '1', '-ar', '16000', str(target)], check=True)


def write_vtt(segments, target, language):
    lines = ['WEBVTT', '', 'NOTE Auto-transcribed with Whisper (%s); may contain errors.' % language, '']
    for index, segment in enumerate(segments, 1):
        text = segment.text.strip()
        if not text:
            continue
        lines.append(str(index))
        lines.append('%s --> %s' % (stamp(segment.start), stamp(segment.end)))
        lines.append(text)
        lines.append('')
    target.write_text('\n'.join(lines), encoding='utf-8')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source', type=Path,
                        default=Path.home() / 'Library/Mobile Documents/com~apple~CloudDocs/Ethics')
    parser.add_argument('--model', default='medium', help='whisper model size (default: medium)')
    parser.add_argument('--only', action='append', default=[], help='slug to transcribe; repeatable')
    parser.add_argument('--force', action='store_true', help='re-transcribe even if a .vtt exists')
    args = parser.parse_args()

    from faster_whisper import WhisperModel

    todo = [v for v in pages.VIDEOS if not args.only or v['slug'] in args.only]
    if not todo:
        parser.error('No recordings matched --only %s' % args.only)

    CAPTIONS.mkdir(parents=True, exist_ok=True)
    model = WhisperModel(args.model, device='cpu', compute_type='int8')

    for video in todo:
        target = CAPTIONS / (video['slug'] + '.vtt')
        if target.exists() and not args.force:
            print('exists, skipping: ' + target.name, flush=True)
            continue
        source = args.source / video['source']
        if not source.exists():
            raise SystemExit('Missing recording: ' + str(source))
        print('transcribing %s (%s)' % (video['slug'], pages.runtime(video['seconds'])), flush=True)
        with tempfile.TemporaryDirectory(prefix='ethics-audio-') as temp:
            audio = Path(temp) / 'audio.wav'
            extract_audio(source, audio)
            segments, info = model.transcribe(str(audio), vad_filter=True, beam_size=5)
            write_vtt(list(segments), target, info.language)
        print('wrote %s (language: %s)' % (target.name, info.language), flush=True)


if __name__ == '__main__':
    main()
