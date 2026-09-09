#!/usr/bin/env python3
"""Prepare downloaded Ethics recordings and upload new objects to R2.

Defaults to an inventory only. Pass --upload to remux and upload.
Uses the locally configured AWS credentials; never stores credentials.
"""
import argparse
import json
import re
import subprocess
import tempfile
from pathlib import Path

ENDPOINT = 'https://8baba61b0b1e25d88220970b015bab81.r2.cloudflarestorage.com'
PUBLIC = 'https://pub-1ae2691df7364eea93afb4e67996d97c.r2.dev'


def run(args):
    return subprocess.check_output(args, text=True)


def slug(value):
    return re.sub(r'[^a-z0-9]+', '-', value.lower()).strip('-')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source', type=Path, default=Path.home() / 'Library/Mobile Documents/com~apple~CloudDocs/Ethics')
    parser.add_argument('--upload', action='store_true')
    args = parser.parse_args()
    files = sorted(p for p in args.source.rglob('*') if p.suffix.lower() in {'.mov', '.mp4'})
    if not files:
        parser.error('No video files found.')
    pending = [p for p in files if getattr(p.stat(), 'st_flags', 0) & 0x40000000]
    print(f'{len(files)} videos; {len(pending)} still cloud-only.', flush=True)
    for p in files:
        print(('CLOUD ONLY ' if p in pending else 'LOCAL      ') + str(p.relative_to(args.source)), flush=True)
    if not args.upload:
        return
    if pending:
        print('Skipping cloud-only files; uploading available recordings.', flush=True)
    aws = ['aws', '--endpoint-url', ENDPOINT]
    listing = json.loads(run(aws + ['s3api', 'list-objects-v2', '--bucket', 'videos', '--prefix', 'ethics/', '--output', 'json']))
    existing = {x['Key'] for x in listing.get('Contents', [])}
    for source in files:
        if source in pending:
            continue
        relative = source.relative_to(args.source)
        # Retain the source extension in the key to distinguish the two
        # Professional Ethics recordings without assuming they are duplicates.
        key = '/'.join(['ethics', *(slug(x) for x in relative.parts[:-1]), slug(source.stem) + '-' + source.suffix[1:].lower() + '.mp4'])
        if key in existing:
            print('Already exists; leaving unchanged: ' + key, flush=True)
            continue
        info = json.loads(run(['ffprobe', '-v', 'error', '-show_streams', '-of', 'json', str(source)]))
        codecs = {s['codec_name'] for s in info['streams'] if s['codec_type'] in {'audio', 'video'}}
        if not codecs <= {'h264', 'aac'}:
            raise SystemExit(f'{source.name}: codecs {codecs} need inspection before conversion.')
        with tempfile.TemporaryDirectory(prefix='ethics-video-') as temp:
            output = Path(temp) / 'video.mp4'
            subprocess.run(['ffmpeg', '-v', 'error', '-nostdin', '-i', str(source), '-map', '0:v:0', '-map', '0:a:0?', '-c', 'copy', '-movflags', '+faststart', str(output)], check=True)
            subprocess.run(aws + ['s3', 'cp', str(output), 's3://videos/' + key, '--content-type', 'video/mp4', '--no-progress'], check=True)
            remote = json.loads(run(aws + ['s3api', 'head-object', '--bucket', 'videos', '--key', key, '--output', 'json']))
            if remote['ContentLength'] != output.stat().st_size:
                raise SystemExit('Uploaded size mismatch: ' + key)
            print('Uploaded: ' + PUBLIC + '/' + key, flush=True)


if __name__ == '__main__':
    main()
