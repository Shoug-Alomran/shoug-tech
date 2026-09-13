#!/usr/bin/env python3
"""Upload registered recordings and automatically prepare captioned lessons.

Run with --whisper /path/to/whisper.cpp. This is the site's local ingestion
workflow; manual uploads to the R2 dashboard do not execute local software.
Caption review failures leave the recording unpublished, ready for correction.
"""
import argparse
import json
import subprocess
import tempfile
from pathlib import Path
from urllib.parse import quote
from upload_ethics_videos import ENDPOINT, PUBLIC
from validate_video_captions import read_cues, repair_timing, format_cues, audit

ROOT = Path(__file__).resolve().parent.parent
REGISTRY = ROOT / 'scripts/ethics-new-recordings.json'
SECTION = ROOT / 'docs/academics/other-courses/ethcs303/video-explanations'


def run(args):
    return subprocess.check_output([str(x) for x in args], text=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--whisper', type=Path, required=True)
    parser.add_argument('--source', type=Path, default=Path.home() / 'Library/Mobile Documents/com~apple~CloudDocs/Ethics')
    args = parser.parse_args()
    cli = args.whisper / 'build/bin/whisper-cli'
    model = args.whisper / 'models/ggml-large-v3-turbo.bin'
    if not cli.exists() or not model.exists():
        parser.error('The local Whisper executable and model are required.')
    rows = json.loads(REGISTRY.read_text())
    aws = ['aws', '--endpoint-url', ENDPOINT]
    objects = json.loads(run(aws + ['s3api', 'list-objects-v2', '--bucket', 'videos', '--output', 'json']))
    existing = {x['Key'] for x in objects.get('Contents', [])}
    for video in rows:
        if video.get('ready'):
            continue
        # Recheck before each lesson: the owner may upload files while this
        # long-running caption batch is processing an earlier recording.
        objects = json.loads(run(aws + ['s3api', 'list-objects-v2', '--bucket', 'videos', '--prefix', video['video'], '--output', 'json']))
        existing.update(x['Key'] for x in objects.get('Contents', []))
        path = args.source / video['source']
        local = path.exists() and not (getattr(path.stat(), 'st_flags', 0) & 0x40000000)
        if not local and video['video'] not in existing:
            print('WAITING FOR ICLOUD: ' + video['source'], flush=True)
            continue
        source = str(path) if local else PUBLIC + '/' + quote(video['video'], safe='/')
        print('PROCESSING: ' + video['title'], flush=True)
        info = json.loads(run(['ffprobe', '-v', 'error', '-show_format', '-show_streams', '-of', 'json', source]))
        video['seconds'] = round(float(info['format']['duration']))
        codecs = {s.get('codec_name') for s in info['streams'] if s['codec_type'] in ['audio', 'video']}
        if not codecs <= {'h264', 'aac'}:
            print('REVIEW CODECS: ' + str(codecs), flush=True)
            continue
        with tempfile.TemporaryDirectory(prefix='ethics-ingest-') as temp:
            temp = Path(temp)
            if video['video'] not in existing:
                output = temp / 'video.mp4'
                subprocess.run(['ffmpeg', '-v', 'error', '-nostdin', '-i', source, '-map', '0:v:0', '-map', '0:a:0?', '-c', 'copy', '-movflags', '+faststart', str(output)], check=True)
                subprocess.run(aws + ['s3', 'cp', str(output), 's3://videos/' + video['video'], '--content-type', 'video/mp4', '--no-progress'], check=True)
                head = json.loads(run(aws + ['s3api', 'head-object', '--bucket', 'videos', '--key', video['video']]))
                if head['ContentLength'] != output.stat().st_size:
                    raise RuntimeError('Upload size mismatch')
            audio = temp / 'audio.wav'
            subprocess.run(['ffmpeg', '-v', 'error', '-nostdin', '-i', source, '-vn', '-ac', '1', '-ar', '16000', str(audio)], check=True)
            draft = temp / 'caption'
            prompt = 'شرح الأخلاقيات والأمن السيبراني. ' + video['title'] + '. Morality, ethics, deontology, consequentialism, virtue ethics, moral systems, professional ethics.'
            subprocess.run([str(cli), '-m', str(model), '-f', str(audio), '-l', 'ar', '-mc', '0', '--prompt', prompt, '-t', '8', '-ovtt', '-of', str(draft)], check=True, stdout=subprocess.DEVNULL)
            notes, cues = read_cues(draft.with_suffix('.vtt'))
            cues = format_cues(repair_timing(cues))
            caption = SECTION / 'captions' / (video['slug'] + '.vtt')
            caption.parent.mkdir(parents=True, exist_ok=True)
            caption.write_text('\n\n'.join(['WEBVTT', 'NOTE Automatic Arabic captions generated locally with Whisper; may contain errors.'] + [f'{a} --> {b}\n{t}' for a,b,t in cues]) + '\n')
            errors = audit(cues)
            if errors:
                print('CAPTION REVIEW: ' + video['slug'] + ': ' + '; '.join(errors), flush=True)
                continue
            poster = SECTION / 'thumbnails' / (video['slug'] + '.jpg')
            poster.parent.mkdir(parents=True, exist_ok=True)
            subprocess.run(['ffmpeg', '-y', '-v', 'error', '-nostdin', '-ss', str(video['seconds'] * .06), '-i', source, '-frames:v', '1', '-vf', 'scale=960:-1', str(poster)], check=True)
            video['ready'] = True
            REGISTRY.write_text(json.dumps(rows, ensure_ascii=False, indent=2) + '\n')
            print('READY: ' + video['slug'], flush=True)
    print('Ready recordings: ' + str(sum(bool(v.get('ready')) for v in rows)), flush=True)
    subprocess.run(['python3', str(ROOT / 'scripts/build_ethics_video_pages.py')], check=True)
    subprocess.run(['python3', str(ROOT / 'scripts/build_ethics_study_tools.py')], check=True)


if __name__ == '__main__':
    main()
