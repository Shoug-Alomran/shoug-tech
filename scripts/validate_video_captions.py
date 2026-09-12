#!/usr/bin/env python3
"""Validate WebVTT timing and flag likely transcription repetition.

Use --repair-timing to join zero-duration text to the next timed cue, preserving
its words. This does not certify transcription accuracy or remove repetitions.
"""
import argparse
import itertools
import re
import textwrap
from pathlib import Path

TIMING = re.compile(r'^(\d{2}:\d{2}:\d{2}\.\d{3}) --> (\d{2}:\d{2}:\d{2}\.\d{3})$')


def seconds(value):
    h, m, s = value.split(':')
    return int(h) * 3600 + int(m) * 60 + float(s)


def read_cues(path):
    text = path.read_text(encoding='utf-8-sig')
    if not text.startswith('WEBVTT\n'):
        raise ValueError(f'{path}: missing WEBVTT header')
    notes, cues = [], []
    for block in re.split(r'\n\s*\n', text.strip())[1:]:
        if block.startswith('NOTE'):
            notes.append(block)
            continue
        lines = block.splitlines()
        timing = TIMING.fullmatch(lines[0])
        if not timing or len(lines) < 2:
            raise ValueError(f'{path}: malformed cue: {block[:100]}')
        cues.append([timing[1], timing[2], '\n'.join(lines[1:]).strip()])
    if not cues:
        raise ValueError(f'{path}: no caption cues')
    return notes, cues


def audit(cues):
    errors = []
    for i, (start, end, text) in enumerate(cues):
        if seconds(end) <= seconds(start):
            errors.append(f'cue {i + 1}: nonpositive duration')
        if not text:
            errors.append(f'cue {i + 1}: empty text')
        if i and seconds(start) < seconds(cues[i - 1][0]):
            errors.append(f'cue {i + 1}: out of order')
    longest = max(len(list(g)) for _, g in itertools.groupby(cues, key=lambda c: c[2]))
    if longest >= 4:
        errors.append(f'{longest} consecutive identical cues; review transcription')
    return errors


def repair_timing(cues):
    result, pending = [], []
    for start, end, text in cues:
        if seconds(end) <= seconds(start):
            pending.append(text)
            continue
        if pending:
            text = ' '.join(pending + [text])
            pending = []
        result.append([start, end, text])
    if pending:
        if not result:
            raise ValueError('No positive-duration cue to hold caption text')
        result[-1][2] += ' ' + ' '.join(pending)
    return result


def timestamp(milliseconds):
    hours, rest = divmod(milliseconds, 3600000)
    minutes, rest = divmod(rest, 60000)
    secs, millis = divmod(rest, 1000)
    return f'{hours:02}:{minutes:02}:{secs:02}.{millis:03}'


def format_cues(cues):
    """Wrap at word boundaries; divide long cues within their existing span.

    Subcue timing is proportional to text length, not word-level alignment.
    All words and the original cue's overall time interval are retained.
    """
    result = []
    for start, end, text in cues:
        lines = textwrap.wrap(' '.join(text.split()), width=42,
                              break_long_words=False, break_on_hyphens=False)
        groups = ['\n'.join(lines[i:i + 2]) for i in range(0, len(lines), 2)]
        begin, finish = round(seconds(start) * 1000), round(seconds(end) * 1000)
        if finish - begin < len(groups):
            result.append([start, end, text])
            continue
        total = sum(len(g) for g in groups)
        used, previous = 0, begin
        for i, group in enumerate(groups):
            used += len(group)
            boundary = finish if i == len(groups) - 1 else begin + round((finish - begin) * used / total)
            result.append([timestamp(previous), timestamp(boundary), group])
            previous = boundary
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('directory', type=Path)
    parser.add_argument('--repair-timing', action='store_true')
    parser.add_argument('--format', action='store_true', help='limit captions to two lines')
    args = parser.parse_args()
    files = sorted(args.directory.glob('*.vtt'))
    if not files:
        parser.error('No VTT files found')
    failures = 0
    for path in files:
        notes, cues = read_cues(path)
        if args.repair_timing or args.format:
            fixed = repair_timing(cues) if args.repair_timing else cues
            if args.format:
                fixed = format_cues(fixed)
            if fixed != cues:
                blocks = ['WEBVTT'] + notes + [f'{a} --> {b}\n{t}' for a, b, t in fixed]
                path.write_text('\n\n'.join(blocks) + '\n', encoding='utf-8')
                cues = fixed
        errors = audit(cues)
        failures += bool(errors)
        print(f'{path.name}: ' + ('; '.join(errors) if errors else f'OK ({len(cues)} cues)'))
    return 1 if failures else 0


if __name__ == '__main__':
    raise SystemExit(main())
