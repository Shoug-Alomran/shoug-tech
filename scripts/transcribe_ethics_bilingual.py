#!/usr/bin/env python3
"""Draft original-language Arabic/English captions locally with MLX Whisper.

Requires mlx-whisper, numpy and ffmpeg. Review drafts before copying to the
private course source. Short pause-aligned windows retain the bilingual prompt.
"""
import argparse,json,subprocess,sys,re
from pathlib import Path
import numpy as np
import mlx_whisper
from validate_video_captions import audit
import build_ethics_video_pages as pages
parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('--source',type=Path,default=Path.home()/'Library/Mobile Documents/com~apple~CloudDocs/Ethics')
parser.add_argument('--output-dir',type=Path,required=True)
parser.add_argument('--only',action='append',required=True,help='Lesson slug; repeat for more recordings')
parser.add_argument('--model',default='mlx-community/whisper-large-v3-turbo')
args=parser.parse_args()
out=args.output_dir;out.mkdir(parents=True,exist_ok=True)
rows=[v for v in pages.VIDEOS if v['slug'] in args.only]
if set(args.only)!={v['slug'] for v in rows}:parser.error('Unknown lesson slug')
def stamp(t):
 n=round(t*1000);return f'{n//3600000:02}:{n//60000%60:02}:{n//1000%60:02}.{n%1000:03}'
for v in rows:
 if (out/(v['slug']+'.vtt')).exists():continue
 f=args.source/v['source']
 raw=subprocess.check_output(['ffmpeg','-v','error','-i',str(f),'-vn','-ac','1','-ar','16000','-f','f32le','pipe:1']);audio=np.frombuffer(raw,dtype=np.float32);duration=len(audio)/16000
 silence=subprocess.run(['ffmpeg','-hide_banner','-i',str(f),'-vn','-af','silencedetect=noise=-32dB:d=0.12','-f','null','-'],capture_output=True,text=True).stderr
 ends=[float(x) for x in re.findall(r'silence_end: ([\d.]+)',silence)]
 cuts=[0.0]
 while cuts[-1]+28<duration:
  start=cuts[-1];near=[x-.04 for x in ends if start+20<x<start+28];cuts.append(min(near,key=lambda x:abs(x-start-25)) if near else start+28)
 cuts.append(duration);segments=[]
 for i,(a,b) in enumerate(zip(cuts,cuts[1:])):
  result=mlx_whisper.transcribe(audio[round(a*16000):round(b*16000)],path_or_hf_repo=args.model,language='ar',task='transcribe',condition_on_previous_text=False,temperature=(0.0,0.2,0.4),initial_prompt='شرح بالعربية والإنجليزية. Systems analysis, software engineering, ethical policies, informed consent, safety-critical systems, business ethics, stakeholders. هذا الشرح عربي مع مصطلحات وجمل English.',verbose=None)
  for s in result['segments']:
   end=min(b,a+s['end']);start=max(a,a+s['start'])
   if end>start and s['text'].strip():segments.append([stamp(start),stamp(end),s['text'].strip()])
  if i%10==0:print(v['slug'],i+1,'/',len(cuts)-1,flush=True)
 (out/(v['slug']+'.vtt')).write_text('WEBVTT\n\nNOTE Automatic original-language Arabic and English captions. Whisper large-v3-turbo with short speech windows; may contain recognition errors.\n\n'+'\n\n'.join(f'{a} --> {b}\n{t}' for a,b,t in segments)+'\n')
 print('DONE',v['slug'],'audit',audit(segments),flush=True)
