#!/usr/bin/env python3
"""Transcribe the ETHCS303 recordings into WebVTT caption tracks.

The narration is Arabic (Saudi dialect) with English technical terms, so the
captions are Arabic and the pages mark the track srclang="ar".

Captions land in docs/.../video-explanations/captions/<slug>.vtt, which is where
build_ethics_video_pages.py looks when deciding whether a player gets a <track>.

Transcription runs locally through whisper.cpp with Metal on Apple Silicon.
Text context resets between audio windows to avoid propagating a mistaken
phrase through the recording. Review drafts with validate_video_captions.py
before copying them into the site's caption directory.

Build whisper.cpp once (no system install needed):

    git clone --depth 1 https://github.com/ggml-org/whisper.cpp
    cd whisper.cpp && cmake -B build -DCMAKE_BUILD_TYPE=Release && cmake --build build -j8
    bash models/download-ggml-model.sh large-v3-turbo

Usage:
    python3 scripts/transcribe_ethics_videos.py --whisper ~/whisper.cpp --only vishing
    python3 scripts/transcribe_ethics_videos.py --whisper ~/whisper.cpp     # all 19

Rebuild the pages afterwards so the <track> elements appear.
"""

import argparse
import importlib.util
import subprocess
import tempfile
import time
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
spec = importlib.util.spec_from_file_location('pages', REPO / 'scripts' / 'build_ethics_video_pages.py')
pages = importlib.util.module_from_spec(spec)
spec.loader.exec_module(pages)

CAPTIONS = pages.SECTION / 'captions'
MODEL = 'ggml-large-v3-turbo.bin'
NOTE = 'NOTE Auto-transcribed with Whisper (large-v3-turbo). Arabic narration; may contain errors.'


def extract_audio(source, target):
    """16 kHz mono wav — the only input format whisper.cpp accepts."""
    subprocess.run(['ffmpeg', '-y', '-v', 'error', '-nostdin', '-i', str(source),
                    '-vn', '-ac', '1', '-ar', '16000', str(target)], check=True)


def annotate(target):
    """Add a provenance note under the WEBVTT header."""
    text = target.read_text(encoding='utf-8')
    if NOTE in text:
        return
    head, _, rest = text.partition('\n')
    # The blank line after NOTE matters: a comment block runs to the next blank
    # line, so without it the first cue is swallowed into the comment.
    target.write_text('%s\n\n%s\n\n%s' % (head, NOTE, rest.lstrip('\n')), encoding='utf-8')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source', type=Path,
                        default=Path.home() / 'Library/Mobile Documents/com~apple~CloudDocs/Ethics')
    parser.add_argument('--whisper', type=Path, required=True,
                        help='whisper.cpp checkout holding build/bin/whisper-cli and models/')
    parser.add_argument('--language', default='ar', help='spoken language (default: ar)')
    parser.add_argument('--threads', type=int, default=8)
    parser.add_argument('--only', action='append', default=[], help='slug to transcribe; repeatable')
    parser.add_argument('--force', action='store_true', help='re-transcribe even if a .vtt exists')
    parser.add_argument('--output-dir', type=Path, default=CAPTIONS,
                        help='write drafts here before reviewing and publishing')
    args = parser.parse_args()

    cli = args.whisper / 'build/bin/whisper-cli'
    model = args.whisper / 'models' / MODEL
    for path in (cli, model):
        if not path.exists():
            raise SystemExit('Missing %s — see the build steps in this script\'s docstring.' % path)

    todo = [v for v in pages.VIDEOS if not args.only or v['slug'] in args.only]
    if not todo:
        parser.error('No recordings matched --only %s' % args.only)

    args.output_dir.mkdir(parents=True, exist_ok=True)
    total = sum(v['seconds'] for v in todo)
    print('%d recording(s), %s of audio'
          % (len(todo), pages.runtime(total)), flush=True)

    for video in todo:
        target = args.output_dir / (video['slug'] + '.vtt')
        if target.exists() and not args.force:
            print('exists, skipping: ' + target.name, flush=True)
            continue
        source = args.source / video['source']
        if not source.exists():
            raise SystemExit('Missing recording: ' + str(source))
        print('transcribing %s (%s)' % (video['slug'], pages.runtime(video['seconds'])), flush=True)
        started = time.time()
        with tempfile.TemporaryDirectory(prefix='ethics-audio-') as temp:
            audio = Path(temp) / 'audio.wav'
            extract_audio(source, audio)
            subprocess.run([
                str(cli), '-m', str(model), '-f', str(audio),
                '-l', args.language, '-t', str(args.threads),
                # Reset text context between audio windows so a mistaken phrase
                # cannot seed repetition across the rest of a recording.
                '-mc', '0',
                '-ovtt', '-of', str(target.with_suffix('')),
            ], check=True, stdout=subprocess.DEVNULL)
        annotate(target)
        print('wrote %s in %s' % (target.name, pages.runtime(int(time.time() - started))), flush=True)


if __name__ == '__main__':
    main()
