#!/usr/bin/env python3
"""Build every SE365 study artifact from the single slide-audited course model.

Content lives in scripts/se365_content.py; this script only renders it, so the
breakdown page, the mindmap and the exam for a lecture can never drift apart:

    sections            -> the animated slide-breakdown page
    quiz                -> the pop quiz embedded in that page
    branches            -> the interactive mindmap (Ethics node-canvas model)
    exam_mcq/exam_short -> the standalone self-graded lecture exam

It also renames nothing: the PDFs under slides/ are already SEO-slugged, and the
viewers, listings and hub rows are generated from LECTURES so a new lecture only
has to be written once.

Usage:
    python3 scripts/build_se365_study_tools.py
"""

from __future__ import annotations

import html
import json
import re
import subprocess
import sys
import zlib
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

from se365_content import LECTURES, COURSE_CODE, COURSE_NAME, TEXTBOOK  # noqa: E402

ROOT = HERE.parent
SITE = "https://shoug-tech.com"
COURSE_ROUTE = "/academics/software-engineering/se365"
BASE = ROOT / "docs/academics/software-engineering/se365"
SLIDES = BASE / "slides"
BREAKDOWNS = BASE / "slide-breakdowns"
MAPS = BASE / "extra-resources/mindmaps"
EXAMS = BASE / "exams"

# Chrome donors. The breakdown shell borrows an ETHCS303 page (same layout family
# as every other course's breakdown wrapper); the mindmap borrows the Ethics
# node-canvas map, which is the interaction model Shoug settled on.
SHELL_SRC = (ROOT / "docs/academics/other-courses/ethcs303/slide-breakdowns"
             / "02-kantianism/index.html")
ETHICS_MAP_TEMPLATE = (ROOT / "docs/academics/other-courses/ethcs303/extra-resources/mindmap"
                       / "01-moral-systems-ethical-concepts-and-theories"
                       / "moral-systems-ethical-concepts-and-theories.html")

UNIVERSITY_CREDIT = (
    '<div class="university-credit"><strong>PROPERTY OF PRINCE SULTAN UNIVERSITY</strong> &mdash; '
    'These slides are the intellectual property of Prince Sultan University. All academic content, materials, '
    'and resources are owned by the University and are shared here solely for personal study purposes. '
    'Redistribution or reproduction without explicit permission from Prince Sultan University is prohibited.</div>'
)

SLIDE_VIEWER_STYLES = '''<style id="se365-slide-viewer-styles">
.slide-viewer-shell{margin:0 40px 48px}.university-credit{border:1px solid var(--border-purple);background:rgba(184,41,234,.07);padding:16px 18px;margin-bottom:18px;color:var(--text-secondary);line-height:1.65}.university-credit strong{color:var(--text-purple-bright);font-family:var(--font-mono);letter-spacing:.04em}.slide-actions{display:flex;justify-content:flex-end;margin-bottom:12px}.slide-open-link{border:1px solid var(--border-purple);color:var(--text-purple-bright);padding:8px 14px;font-family:var(--font-mono);font-size:.75rem}.slide-open-link:hover{background:rgba(184,41,234,.12)}.pdf-frame{display:block;width:100%;height:78vh;min-height:640px;border:1px solid var(--border-med);background:#fff}@media(max-width:760px){.slide-viewer-shell{margin:0 16px 32px}.pdf-frame{height:70vh;min-height:480px}.university-credit{font-size:.82rem}}
</style>'''

# Every lecture deck, in slide order, with the SEO-slugged PDF it renders from.
SLIDE_DECKS = [
    ("01", 1, "lecture-01-introduction-to-human-computer-interaction.pdf"),
    ("02", 2, "lecture-02-cognitive-aspects.pdf"),
    ("03", 3, "lecture-03-emotional-interaction.pdf"),
    ("04", 4, "lecture-04-interaction-and-interfaces.pdf"),
    ("05", 5, "lecture-05-the-process-of-interaction-design.pdf"),
    ("06-07", 6, "lecture-06-07-establishing-requirements.pdf"),
    ("08", 8, "lecture-08-design-principles-and-guidelines.pdf"),
    ("09-10", 9, "lecture-09-10-design-prototyping-and-construction.pdf"),
    ("11", 11, "lecture-11-evaluation-foundations.pdf"),
    ("12", 12, "lecture-12-evaluation-decide-usability-testing-and-experiments.pdf"),
    ("13", 13, "lecture-13-evaluation-inspections-heuristics-and-walkthroughs.pdf"),
]

ARROW = ('<div class="dir-arrow"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" '
         'stroke-width="2" stroke-linecap="square"><path d="M5 12h14M12 5l7 7-7 7"/></svg></div>')

COMING_SOON_RE = re.compile(r'\s*<div class="coming-soon-container".*?</div>\s*</div>', re.S)
DIRECTORY_RE = re.compile(r'\s*<div class="directory-container"[^>]*>.*?</div>\s*(?=\s*<footer)', re.S)


def by_num(num: int) -> dict:
    for lec in LECTURES:
        if lec["num"] == num:
            return lec
    raise KeyError(num)


def esc(value: str) -> str:
    return html.escape(value, quote=True)


# --------------------------------------------------------------------------- #
# 1. the animated slide-breakdown page
# --------------------------------------------------------------------------- #

BREAKDOWN_CSS = r"""
/* Tokens are declared light-first on :root, then overridden for the explicit
   dark choice and for the system default. The page is iframed inside a dark
   shell, so it also inherits the parent's theme when nothing is stored. */
:root{
  --accent:__ACCENT__; --accent2:__ACCENT2__;
  --bg:#f6f4fb; --bg2:#ffffff; --panel:#ffffff; --panel2:#f3f1fa;
  --ink:#16111f; --ink-dim:#4d465c; --ink-faint:#6f6880;
  --line:#e0dcec; --line-strong:#c9c2dd;
  --shadow:0 18px 44px rgba(30,20,60,.10);
  --code-bg:#f0edf8;
  --ok:#177a4a; --bad:#b3283f; --warn:#8a5a06;
}
html[data-theme="dark"]{
  --bg:#07050e; --bg2:#0b0716; --panel:#100b1e; --panel2:#160f2a;
  --ink:#ece6fa; --ink-dim:#a79cc2; --ink-faint:#7b7194;
  --line:#241a3c; --line-strong:#3a2c5c;
  --shadow:0 18px 50px rgba(0,0,0,.55);
  --code-bg:#180f2c;
  --ok:#63d99a; --bad:#ff7d90; --warn:#f0b95c;
}
*{box-sizing:border-box}
html{scroll-behavior:smooth}
body{
  margin:0; background:var(--bg); color:var(--ink);
  font:16px/1.68 ui-sans-serif,-apple-system,"Segoe UI",Inter,system-ui,sans-serif;
  -webkit-font-smoothing:antialiased;
  transition:background .3s ease,color .3s ease;
}
body::before{
  content:""; position:fixed; inset:0; z-index:-1; pointer-events:none;
  background:
    radial-gradient(60rem 40rem at 12% -8%, color-mix(in srgb,var(--accent) 22%,transparent), transparent 70%),
    radial-gradient(52rem 38rem at 105% 12%, color-mix(in srgb,var(--accent2) 18%,transparent), transparent 70%);
  opacity:.55;
}
a{color:var(--accent)}
code{background:var(--code-bg);padding:.1em .38em;border-radius:5px;font-family:ui-monospace,"JetBrains Mono",monospace;font-size:.9em}

/* ── top bar ─────────────────────────────────────────────────────────────── */
.topbar{
  position:sticky; top:0; z-index:40;
  background:color-mix(in srgb,var(--bg) 86%,transparent);
  backdrop-filter:blur(16px);
  border-bottom:1px solid var(--line);
}
.topbar-in{max-width:1180px;margin:0 auto;padding:11px clamp(16px,4vw,44px);display:flex;align-items:center;gap:14px}
.brandmark{font:700 11px/1 ui-monospace,monospace;letter-spacing:.18em;color:var(--accent);white-space:nowrap}
.brandmark b{display:block;font:600 13px/1.4 inherit;letter-spacing:.02em;color:var(--ink);font-family:inherit;margin-top:4px}
.topbar-spacer{flex:1}
.tbtn{
  border:1px solid var(--line-strong); background:var(--panel); color:var(--ink);
  border-radius:9px; padding:8px 12px; font:600 12px/1 ui-monospace,monospace;
  cursor:pointer; letter-spacing:.06em; transition:.18s;
}
.tbtn:hover{border-color:var(--accent);color:var(--accent);transform:translateY(-1px)}
.readbar{height:3px;background:transparent}
.readbar i{display:block;height:100%;width:0;background:linear-gradient(90deg,var(--accent),var(--accent2));transition:width .12s linear}

/* ── layout ──────────────────────────────────────────────────────────────── */
main{max-width:1180px;margin:0 auto;padding:0 clamp(16px,4vw,44px) 90px}
.hero{padding:clamp(38px,7vw,84px) 0 26px}
.eyebrow{font:700 11px/1 ui-monospace,monospace;letter-spacing:.2em;color:var(--accent)}
h1{
  font-size:clamp(30px,5.4vw,58px); line-height:1.08; margin:16px 0 18px; font-weight:800;
  letter-spacing:-.02em;
  background:linear-gradient(104deg,var(--ink) 12%,var(--accent) 58%,var(--accent2) 96%);
  -webkit-background-clip:text; background-clip:text; color:transparent;
}
h1 em{font-style:normal;opacity:.92}
.lede{max-width:74ch;color:var(--ink-dim);font-size:clamp(15px,1.5vw,18px)}
.badges{display:flex;flex-wrap:wrap;gap:8px;margin:24px 0 0}
.badge{
  border:1px solid var(--line-strong); border-radius:999px; padding:6px 13px;
  font:600 12px/1 ui-monospace,monospace; color:var(--ink-dim);
  background:color-mix(in srgb,var(--panel) 70%,transparent);
}
.badge:hover{border-color:var(--accent);color:var(--accent)}

.outcomes{
  margin:30px 0 0; border:1px solid var(--line); border-left:3px solid var(--accent);
  border-radius:14px; background:var(--panel); padding:20px 24px; box-shadow:var(--shadow);
}
.outcomes h2{margin:0 0 10px;font:700 12px/1 ui-monospace,monospace;letter-spacing:.16em;color:var(--accent)}
.outcomes ol{margin:0;padding-left:20px;color:var(--ink-dim)}
.outcomes li{margin:6px 0}

/* ── table of contents ───────────────────────────────────────────────────── */
.toc{display:grid;grid-template-columns:repeat(auto-fill,minmax(min(100%,250px),1fr));gap:10px;margin:30px 0 10px}
.toc a{
  display:block; text-decoration:none; color:var(--ink); border:1px solid var(--line);
  border-radius:12px; padding:12px 14px; background:var(--panel); transition:.2s;
  font-size:14px;
}
.toc a span{display:block;font:700 11px/1 ui-monospace,monospace;letter-spacing:.12em;color:var(--ink-faint);margin-bottom:6px}
.toc a:hover{border-color:var(--accent);transform:translateY(-2px);box-shadow:var(--shadow)}

/* ── sections ────────────────────────────────────────────────────────────── */
section.lec{
  margin:26px 0; padding:clamp(20px,3.2vw,34px);
  border:1px solid var(--line); border-radius:20px;
  background:linear-gradient(150deg,var(--panel),var(--panel2));
  box-shadow:var(--shadow);
  opacity:0; transform:translateY(22px);
}
section.lec.in{animation:rise .58s cubic-bezier(.2,.7,.3,1) forwards}
@keyframes rise{to{opacity:1;transform:none}}
.kicker{font:700 11px/1 ui-monospace,monospace;letter-spacing:.18em;color:var(--accent)}
section.lec h2{font-size:clamp(21px,2.9vw,30px);margin:12px 0 12px;line-height:1.2;letter-spacing:-.01em}
.lead{color:var(--ink-dim);max-width:82ch;margin:0 0 18px}
section.lec p{max-width:82ch}
section.lec ul{padding-left:20px;color:var(--ink-dim)}
section.lec ul li{margin:9px 0}
section.lec ul li::marker{color:var(--accent2)}
section.lec b,section.lec strong{color:var(--ink)}

.cards{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,270px),1fr));gap:14px;margin:16px 0}
.card{
  border:1px solid var(--line); border-top:3px solid var(--accent2); border-radius:14px;
  padding:16px 17px; background:var(--bg2); transition:.22s;
}
html[data-theme="dark"] .card{background:color-mix(in srgb,var(--panel) 80%,#000)}
.card:hover{transform:translateY(-3px);border-color:var(--accent);box-shadow:var(--shadow)}
.card h3{margin:0 0 8px;font-size:15px;color:var(--accent)}
.card p{margin:0;color:var(--ink-dim);font-size:14.5px}

.tablewrap{overflow-x:auto;margin:16px 0;border:1px solid var(--line);border-radius:14px}
table{border-collapse:collapse;width:100%;min-width:520px;font-size:14.5px;background:var(--bg2)}
html[data-theme="dark"] table{background:color-mix(in srgb,var(--panel) 80%,#000)}
th{
  text-align:left;padding:12px 14px;background:color-mix(in srgb,var(--accent) 14%,var(--panel));
  color:var(--ink);font:700 12px/1.4 ui-monospace,monospace;letter-spacing:.06em;
  border-bottom:1px solid var(--line-strong);
}
td{padding:12px 14px;border-bottom:1px solid var(--line);color:var(--ink-dim);vertical-align:top}
tr:last-child td{border-bottom:0}
tbody tr:hover td{background:color-mix(in srgb,var(--accent) 6%,transparent)}

.callout{margin:16px 0;padding:15px 17px;border-radius:13px;border:1px solid var(--line);border-left:4px solid var(--accent)}
.callout .lbl{display:block;font:700 11px/1 ui-monospace,monospace;letter-spacing:.14em;margin-bottom:8px;color:var(--accent)}
.callout p{margin:0;color:var(--ink-dim)}
.callout.warn{border-left-color:var(--bad);background:color-mix(in srgb,var(--bad) 8%,transparent)}
.callout.warn .lbl{color:var(--bad)}
.callout.hook{border-left-color:var(--accent2);background:color-mix(in srgb,var(--accent2) 10%,transparent)}
.callout.hook .lbl{color:var(--accent2)}
.callout.note{background:color-mix(in srgb,var(--accent) 7%,transparent)}

.steps{list-style:none;margin:16px 0;padding:0;counter-reset:s}
.steps li{
  counter-increment:s; position:relative; padding:12px 0 12px 54px;
  border-bottom:1px solid var(--line); color:var(--ink-dim);
}
.steps li:last-child{border-bottom:0}
.steps li::before{
  content:counter(s,decimal-leading-zero); position:absolute; left:0; top:12px;
  width:36px;height:36px;border-radius:10px;display:grid;place-items:center;
  background:color-mix(in srgb,var(--accent) 16%,var(--panel));
  border:1px solid var(--line-strong);
  font:700 12px/1 ui-monospace,monospace;color:var(--accent);
}
.steps li b{display:block;color:var(--ink);margin-bottom:2px}

/* ── mistakes / cheat / lab ──────────────────────────────────────────────── */
.mistake{border:1px solid var(--line);border-radius:13px;margin:12px 0;overflow:hidden;background:var(--bg2)}
html[data-theme="dark"] .mistake{background:color-mix(in srgb,var(--panel) 80%,#000)}
.mistake .m-claim{padding:13px 16px;font-weight:650;color:var(--bad);border-left:4px solid var(--bad)}
.mistake .m-fix{padding:0 16px 14px 20px;color:var(--ink-dim);font-size:14.5px}

.lab details{border:1px solid var(--line);border-radius:13px;margin:12px 0;background:var(--bg2)}
html[data-theme="dark"] .lab details{background:color-mix(in srgb,var(--panel) 80%,#000)}
.lab summary{padding:14px 17px;cursor:pointer;font-weight:650;list-style:none}
.lab summary::-webkit-details-marker{display:none}
.lab summary::before{content:"+ ";color:var(--accent);font-family:ui-monospace,monospace;font-weight:800}
.lab details[open] summary::before{content:"- "}
.lab details[open] summary{border-bottom:1px solid var(--line);color:var(--accent)}
.lab .ans{padding:14px 17px;color:var(--ink-dim);font-size:14.5px}

/* ── quiz ────────────────────────────────────────────────────────────────── */
.quiz .q{border-top:1px solid var(--line);padding:20px 0}
.quiz .q:first-of-type{border-top:0}
.qnum{font:700 12px/1 ui-monospace,monospace;letter-spacing:.1em;color:var(--accent2)}
.prompt{font-weight:650;margin:8px 0 12px}
.quiz label{
  display:block;border:1px solid var(--line);background:var(--bg2);border-radius:11px;
  padding:11px 14px;margin:8px 0;cursor:pointer;transition:.16s;font-size:15px;
}
html[data-theme="dark"] .quiz label{background:color-mix(in srgb,var(--panel) 80%,#000)}
.quiz label:hover{border-color:var(--accent);transform:translateX(4px)}
.quiz label.correct{border-color:var(--ok);background:color-mix(in srgb,var(--ok) 18%,transparent);box-shadow:inset 4px 0 0 var(--ok)}
.quiz label.wrong{border-color:var(--bad);background:color-mix(in srgb,var(--bad) 18%,transparent);box-shadow:inset 4px 0 0 var(--bad)}
.quiz label.correct::after{content:"CORRECT";float:right;color:var(--ok);font:800 11px/1.6 ui-monospace,monospace}
.quiz label.wrong::after{content:"YOUR ANSWER";float:right;color:var(--bad);font:800 11px/1.6 ui-monospace,monospace}
.fb{display:none;margin-top:11px;padding:13px 15px;border-radius:11px;font-size:14.5px;color:var(--ink-dim)}
.fb.show{display:block}
.fb.ok{border:1px solid var(--ok);background:color-mix(in srgb,var(--ok) 10%,transparent)}
.fb.no{border:1px solid var(--bad);background:color-mix(in srgb,var(--bad) 10%,transparent)}
.quizbar{display:flex;flex-wrap:wrap;gap:12px;align-items:center;margin-top:20px}
.qsubmit{
  border:0;border-radius:12px;padding:13px 26px;cursor:pointer;
  background:linear-gradient(100deg,var(--accent),var(--accent2));color:#fff;
  font:800 15px/1 inherit;letter-spacing:.01em;
  box-shadow:0 12px 30px color-mix(in srgb,var(--accent) 34%,transparent);
}
.qsubmit:hover{transform:translateY(-2px)}
.score{display:none;font:800 17px/1.5 ui-monospace,monospace}
.score.show{display:block}
.score.pass{color:var(--ok)}
.score.fail{color:var(--bad)}

footer.foot{margin-top:44px;padding-top:22px;border-top:1px solid var(--line);color:var(--ink-faint);font-size:13.5px}

@media(max-width:700px){
  .topbar-in{flex-wrap:wrap}
  section.lec{border-radius:16px}
}
@media(prefers-reduced-motion:reduce){
  *{animation:none!important;transition:none!important}
  section.lec{opacity:1;transform:none}
}
"""

BREAKDOWN_JS = r"""
(function(){
  var root=document.documentElement;
  // Resolve stored -> parent shell -> OS. The wrapper marks itself only in light
  // mode, so an unmarked same-origin parent means dark.
  function initial(){
    try{var s=localStorage.getItem('shoug-theme'); if(s==='light'||s==='dark')return s;}catch(e){}
    try{
      if(window.parent&&window.parent!==window&&window.parent.document){
        var b=window.parent.document.body;
        if(b) return b.classList.contains('shoug-light-mode')?'light':'dark';
      }
    }catch(e){}
    return window.matchMedia&&window.matchMedia('(prefers-color-scheme: light)').matches?'light':'dark';
  }
  var theme=initial();
  root.setAttribute('data-theme',theme);
  try{localStorage.setItem('shoug-theme',theme);}catch(e){}
  var tb=document.getElementById('themeBtn');
  function label(){tb.textContent=root.getAttribute('data-theme')==='dark'?'LIGHT':'DARK';}
  label();
  tb.addEventListener('click',function(){
    var next=root.getAttribute('data-theme')==='dark'?'light':'dark';
    root.setAttribute('data-theme',next);
    try{localStorage.setItem('shoug-theme',next);}catch(e){}
    label();
  });

  // reveal-on-scroll for the section cards
  var secs=[].slice.call(document.querySelectorAll('section.lec'));
  if('IntersectionObserver' in window){
    var io=new IntersectionObserver(function(es){
      es.forEach(function(e){ if(e.isIntersecting){e.target.classList.add('in');io.unobserve(e.target);} });
    },{rootMargin:'0px 0px -12% 0px'});
    secs.forEach(function(s){io.observe(s);});
  } else { secs.forEach(function(s){s.classList.add('in');}); }

  // reading progress
  var bar=document.getElementById('readbar');
  function prog(){
    var h=document.documentElement.scrollHeight-window.innerHeight;
    bar.style.width=(h>0?Math.min(100,(window.scrollY/h)*100):0)+'%';
  }
  window.addEventListener('scroll',prog,{passive:true});
  window.addEventListener('resize',prog);
  prog();

  document.getElementById('topBtn').addEventListener('click',function(){
    window.scrollTo({top:0,behavior:'smooth'});
  });

  // pop quiz
  var mount=document.getElementById('quizBody');
  QUIZ.forEach(function(q,i){
    var opts=q.options.map(function(o,j){
      return '<label><input type="radio" name="q'+i+'" value="'+j+'"> '+
             String.fromCharCode(65+j)+'. '+o+'</label>';
    }).join('');
    mount.insertAdjacentHTML('beforeend',
      '<article class="q"><span class="qnum">Q'+(i+1)+'</span><div class="prompt">'+q.q+'</div>'+
      opts+'<div class="fb" id="fb'+i+'"></div></article>');
  });
  var submitted=false;
  document.getElementById('quizSubmit').addEventListener('click',function(){
    if(submitted){location.reload();return;}
    var got=0;
    QUIZ.forEach(function(q,i){
      var inputs=[].slice.call(document.querySelectorAll('input[name=q'+i+']'));
      var chosen=inputs.filter(function(n){return n.checked;})[0];
      var fb=document.getElementById('fb'+i);
      inputs.forEach(function(n){
        n.disabled=true;
        if(+n.value===q.correct) n.parentNode.classList.add('correct');
      });
      if(chosen&&+chosen.value===q.correct){
        got++; fb.className='fb show ok'; fb.innerHTML='<b>Correct.</b> '+q.why;
      }else{
        if(chosen) chosen.parentNode.classList.add('wrong');
        fb.className='fb show no';
        fb.innerHTML='<b>Incorrect. Answer: '+String.fromCharCode(65+q.correct)+'.</b> '+q.why;
      }
    });
    var sc=document.getElementById('quizScore');
    sc.className='score show '+(got/QUIZ.length>=0.6?'pass':'fail');
    sc.textContent=got+' / '+QUIZ.length+'  -  '+
      (got/QUIZ.length>=0.6?'Pass. Read the explanations for anything you missed.'
                           :'Below pass. Re-read the flagged sections, then retry.');
    submitted=true;
    this.textContent='Reset quiz';
  });
})();
"""




def shuffled_mcqs(items: list, seed: str) -> list:
    """Rotate each question's options so the key is not always option A.

    Authored questions all put the correct answer first, which is easy to
    pattern-match. The rotation is deterministic (seeded by lecture and question
    index) so a rebuild never reshuffles a page someone has already studied, and
    every explanation is written to name the wrong answers by content rather than
    by position.
    """
    out = []
    for index, item in enumerate(items):
        options = list(item["options"])
        shift = (zlib.crc32(("%s:%d" % (seed, index)).encode()) % len(options))
        rotated = options[shift:] + options[:shift]
        new = dict(item)
        new["options"] = rotated
        new["correct"] = rotated.index(options[item["correct"]])
        out.append(new)
    return out


def theme_css(css: str, lec: dict) -> str:
    """Inject the lecture's accents. The stylesheets contain literal % signs, so
    this deliberately avoids %-formatting."""
    return css.replace("__ACCENT2__", lec["accent2"]).replace("__ACCENT__", lec["accent"])


def render_blocks(blocks: list) -> str:
    out = []
    for kind, payload in blocks:
        if kind == "p":
            out.append("<p>%s</p>" % payload)
        elif kind == "list":
            out.append("<ul>%s</ul>" % "".join("<li>%s</li>" % item for item in payload))
        elif kind == "cards":
            out.append('<div class="cards">%s</div>' % "".join(
                '<div class="card"><h3>%s</h3><p>%s</p></div>' % (title, body)
                for title, body in payload))
        elif kind == "table":
            headers, rows = payload
            head = "".join("<th>%s</th>" % h for h in headers)
            body = "".join("<tr>%s</tr>" % "".join("<td>%s</td>" % c for c in row) for row in rows)
            out.append('<div class="tablewrap"><table><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>'
                       % (head, body))
        elif kind in ("note", "warn", "hook"):
            label, body = payload
            css = {"note": "note", "warn": "warn", "hook": "hook"}[kind]
            out.append('<div class="callout %s"><span class="lbl">%s</span><p>%s</p></div>' % (css, label, body))
        elif kind == "steps":
            out.append('<ol class="steps">%s</ol>' % "".join(
                "<li><b>%s</b>%s</li>" % (name, body) for name, body in payload))
        else:
            raise ValueError("unknown block kind: %r" % kind)
    return "\n            ".join(out)


def breakdown_html(lec: dict) -> str:
    canonical = "%s%s/slide-breakdowns/%s/%s.html" % (SITE, COURSE_ROUTE, lec["slug"], lec["slug"])
    title = "%s - %s %s Slide Breakdown" % (lec["title"], COURSE_CODE, lec["lecture_label"])
    desc = "%s %s: %s" % (COURSE_CODE, lec["lecture_label"], lec["tagline"])

    toc = "".join(
        '<a href="#%s"><span>%02d</span>%s</a>' % (s["id"], i + 1, html.escape(s["title"]))
        for i, s in enumerate(lec["sections"]))
    toc += ('<a href="#mistakes"><span>%02d</span>Common mistakes</a>'
            '<a href="#cheat"><span>%02d</span>Cheat sheet</a>'
            '<a href="#lab"><span>%02d</span>Apply it</a>'
            '<a href="#quiz"><span>%02d</span>Pop quiz</a>'
            % (len(lec["sections"]) + 1, len(lec["sections"]) + 2,
               len(lec["sections"]) + 3, len(lec["sections"]) + 4))

    sections = "\n        ".join(
        '<section class="lec" id="%s">\n            <div class="kicker">%s</div>\n'
        '            <h2>%s</h2>\n            <p class="lead">%s</p>\n            %s\n        </section>'
        % (s["id"], s["kicker"], html.escape(s["title"]), s["lead"], render_blocks(s["blocks"]))
        for s in lec["sections"])

    mistakes = "".join(
        '<div class="mistake"><div class="m-claim">%s</div><div class="m-fix">%s</div></div>' % (claim, fix)
        for claim, fix in lec["mistakes"])

    cheat_headers, cheat_rows = lec["cheat"]
    cheat = ('<div class="tablewrap"><table><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>'
             % ("".join("<th>%s</th>" % h for h in cheat_headers),
                "".join("<tr>%s</tr>" % "".join("<td>%s</td>" % c for c in row) for row in cheat_rows)))

    lab = "".join(
        '<details><summary>%s</summary><div class="ans">%s</div></details>' % (question, answer)
        for question, answer in lec["lab"])

    schema = json.dumps({
        "@context": "https://schema.org", "@type": "LearningResource",
        "url": canonical, "name": title, "description": desc,
        "educationalLevel": "University", "learningResourceType": "Lecture breakdown",
        "about": {"@type": "Thing", "name": "%s %s" % (COURSE_CODE, COURSE_NAME)},
        "isPartOf": {"@type": "WebSite", "name": "Shoug's Digital Garden", "url": SITE + "/"},
    }, ensure_ascii=False)

    return """<!DOCTYPE html>
<html lang="en" data-theme="dark" data-sg-styled>
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>%(title)s</title>
<meta name="description" content="%(desc)s">
<link rel="canonical" href="%(canonical)s">
<link rel="icon" type="image/png" href="/assets/shoug-favicon-v4.png">
<meta property="og:type" content="article">
<meta property="og:title" content="%(title)s">
<meta property="og:description" content="%(desc)s">
<meta property="og:url" content="%(canonical)s">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="%(title)s">
<meta name="twitter:description" content="%(desc)s">
<script type="application/ld+json">%(schema)s</script>
<style>%(css)s</style>
</head>
<body>

<div class="topbar">
  <div class="topbar-in">
    <div class="brandmark">%(code)s &middot; %(label)s<b>%(short)s</b></div>
    <div class="topbar-spacer"></div>
    <button class="tbtn" id="topBtn" type="button">TOP</button>
    <button class="tbtn" id="themeBtn" type="button" aria-label="Toggle light and dark theme">LIGHT</button>
  </div>
  <div class="readbar"><i id="readbar"></i></div>
</div>

<main>
  <header class="hero">
    <div class="eyebrow">%(code)s &middot; %(label)s &middot; SLIDE BREAKDOWN</div>
    <h1>%(hero_title)s</h1>
    <p class="lede">%(hero_sub)s</p>
    <div class="badges">%(badges)s</div>
    <div class="outcomes">
      <h2>LEARNING OUTCOMES</h2>
      <ol>%(outcomes)s</ol>
    </div>
    <nav class="toc" aria-label="Contents">%(toc)s</nav>
  </header>

        %(sections)s

        <section class="lec" id="mistakes">
            <div class="kicker">COMMON MISTAKES</div>
            <h2>What students get wrong on this lecture</h2>
            <p class="lead">Each claim below is the wrong answer; the line beneath it is the correction, in the wording this course marks against.</p>
            %(mistakes)s
        </section>

        <section class="lec" id="cheat">
            <div class="kicker">CHEAT SHEET</div>
            <h2>Shortest correct answers</h2>
            <p class="lead">The night-before table: every term in this lecture with the smallest answer that still earns the mark.</p>
            %(cheat)s
        </section>

        <section class="lec lab" id="lab">
            <div class="kicker">APPLY IT</div>
            <h2>Exam-style application</h2>
            <p class="lead">Write your own answer first, then open the model answer. These are the longer-form questions this material generates.</p>
            %(lab)s
        </section>

        <section class="lec quiz" id="quiz">
            <div class="kicker">POP QUIZ</div>
            <h2>Check yourself</h2>
            <p class="lead">%(nquiz)d questions. Every option is explained after submitting, including why the wrong ones are wrong.</p>
            <div id="quizBody"></div>
            <div class="quizbar">
              <button class="qsubmit" id="quizSubmit" type="button">Submit answers</button>
              <span class="score" id="quizScore"></span>
            </div>
        </section>

  <footer class="foot">
    <p><b>%(code)s &mdash; %(course)s.</b> Breakdown of %(label)s: %(plaintitle)s. Based on material from %(textbook)s Slides are the intellectual property of Prince Sultan University and are summarised here for personal study.</p>
  </footer>
</main>

<script>const QUIZ=%(quiz)s;</script>
<script>%(js)s</script>
</body>
</html>
""" % {
        "title": esc(title), "desc": esc(desc), "canonical": canonical, "schema": schema,
        "css": theme_css(BREAKDOWN_CSS, lec),
        "code": COURSE_CODE, "course": COURSE_NAME, "label": lec["lecture_label"].upper(),
        "short": html.escape(lec["short"]),
        "hero_title": lec["hero_title"], "hero_sub": lec["hero_sub"],
        "badges": "".join('<span class="badge">%s</span>' % html.escape(b) for b in lec["badges"]),
        "outcomes": "".join("<li>%s</li>" % html.escape(o) for o in lec["outcomes"]),
        "toc": toc, "sections": sections, "mistakes": mistakes, "cheat": cheat, "lab": lab,
        "nquiz": len(lec["quiz"]),
        "quiz": json.dumps(shuffled_mcqs(lec["quiz"], "%s-quiz" % lec["slug"]),
                           ensure_ascii=False).replace("</", "<\\/"),
        "js": BREAKDOWN_JS,
        "plaintitle": html.escape(lec["title"]), "textbook": html.escape(TEXTBOOK),
    }


# --------------------------------------------------------------------------- #
# 2. the wrapper shell that embeds a breakdown in the site chrome
# --------------------------------------------------------------------------- #

# The donor page carries the accessibility baseline (id/tabindex on <main>),
# so match the opening tag loosely rather than byte-for-byte.
MAIN_RE = re.compile(r'        <main class="content-area"[^>]*>.*?    </main>', re.S)


def shell_main(lec: dict, prev_lec: dict | None, next_lec: dict | None) -> str:
    base = "%s/slide-breakdowns/" % COURSE_ROUTE
    crumb = (
        '<div class="breadcrumb"><a class="breadcrumb-link" href="/academics/">Academics</a> '
        '<span class="separator">/</span> <a class="breadcrumb-link" href="/academics/software-engineering/">'
        'Software Engineering</a> <span class="separator">/</span> '
        '<a class="breadcrumb-link" href="%s/">SE365</a> <span class="separator">/</span> '
        '<a class="breadcrumb-link" href="%s">Slide Breakdowns</a> '
        '<span class="separator">/</span> <span class="current">%s</span></div>'
        % (COURSE_ROUTE, base, html.escape(lec["title"])))

    parts = []
    if prev_lec:
        parts.append('<a href="%s%s/" class="nav-link prev">&lt;- PREVIOUS</a>' % (base, prev_lec["slug"]))
    if next_lec:
        parts.append('<a href="%s%s/" class="nav-link next">NEXT -&gt;</a>' % (base, next_lec["slug"]))
    navstrip = '<div class="nav-strip uppercase">%s</div>' % "".join(parts) if parts else ""

    title = html.escape(lec["title"])
    return """        <main class="content-area" vid="58" id="main-content" tabindex="-1">

            <div class="top-bar uppercase" vid="59">
                {crumb}
                <div class="sys-time" id="clock" vid="70">SYS_TIME [ 00 00 00 ]</div>
            </div>

            <div class="page-header" vid="73">
                <div class="ch-label uppercase">{label} // SLIDE BREAKDOWNS</div>
                <h1 class="ch-title uppercase">{title}</h1>
                <div class="action-buttons"><a class="btn btn-primary" href="./{file}" target="_blank" rel="noopener noreferrer">[ OPEN IN NEW TAB -&gt; ]</a><a class="btn btn-secondary" href="{base}">[ &lt;- BACK TO INDEX ]</a></div>
            </div>

            {navstrip}

            <div class="embed-area-wrapper" vid="82">
                <div class="embed-container" id="embedded-content">
                    <div class="rendered-content" data-lang-panel="en"><iframe class="embed-frame legacy-html-frame" src="./{file}" loading="lazy" title="{title}"></iframe></div>
                    <div class="rendered-content" data-lang-panel="ar" hidden><iframe class="embed-frame legacy-html-frame" src="./{file}" loading="lazy" title="{title}"></iframe></div>
                </div>
            </div>
    </div>
    </div>

    </main>""".format(crumb=crumb, label=lec["lecture_label"].upper().replace(" ", "_"),
                      title=title, file=lec["slug"] + ".html", base=base, navstrip=navstrip)


def build_shell(lec: dict, prev_lec: dict | None, next_lec: dict | None, template: str) -> str:
    out = MAIN_RE.sub(lambda _m: shell_main(lec, prev_lec, next_lec), template, count=1)
    out = re.sub(r"<title>.*?</title>",
                 "<title>SHOUG.TECH | SE365 %s</title>" % html.escape(lec["title"]),
                 out, count=1, flags=re.S)
    # Drop the borrowed ETHCS303 SEO block, then restate it for this page.
    out = re.sub(r'<meta\s+(?:property="og:[a-z:]+"|name="twitter:[a-z:]+"|name="description")'
                 r'\s+content="[^"]*"\s*>', '', out, flags=re.S)
    out = re.sub(r'<script\s+type="application/ld\+json"\s*>.*?</script>', '', out, flags=re.S)
    out = re.sub(r'<link\s+rel="alternate"\s+hreflang="[^"]*"\s+href="[^"]*"\s*>', '', out, flags=re.S)
    out = re.sub(r'<link rel="canonical"[^>]*>', '', out, flags=re.S)
    out = out.replace("ethcs303", "se365").replace("ETHCS303", "SE365")
    # standalone pages inside the frame read the shell for their theme, so the
    # shell has to declare its own default rather than leaving it implicit.
    out = re.sub(r'<html(?![^>]*\bdata-theme=)([^>]*)>', r'<html\1 data-theme="dark">', out, count=1)

    url = "%s%s/slide-breakdowns/%s/" % (SITE, COURSE_ROUTE, lec["slug"])
    page_title = "SE365 %s &mdash; Slide Breakdown" % html.escape(lec["title"])
    desc = html.escape("%s %s: %s" % (COURSE_CODE, lec["lecture_label"], lec["tagline"]), quote=True)
    seo = (
        '<link rel="canonical" href="{url}">'
        '<meta name="description" content="{desc}">'
        '<meta property="og:title" content="{title}">'
        '<meta property="og:description" content="{desc}">'
        '<meta property="og:url" content="{url}">'
        '<meta property="og:type" content="article">'
        '<meta property="og:image" content="{site}/assets/og-banner.png">'
        '<meta name="twitter:card" content="summary_large_image">'
        '<meta name="twitter:title" content="{title}">'
        '<meta name="twitter:description" content="{desc}">'
        '<meta name="twitter:image" content="{site}/assets/og-banner.png">'
        '<script type="application/ld+json">{ld}</script>'
        '<link rel="alternate" hreflang="en" href="{url}">'
        '<link rel="alternate" hreflang="ar" href="{arurl}">'
        '<link rel="alternate" hreflang="x-default" href="{url}">'
    ).format(url=url, arurl=url.replace(SITE + "/", SITE + "/ar/"), desc=desc, title=page_title, site=SITE,
             ld=json.dumps({
                 "@context": "https://schema.org", "@type": "WebPage", "url": url,
                 "name": "SE365 %s - Slide Breakdown" % lec["title"],
                 "description": "%s %s: %s" % (COURSE_CODE, lec["lecture_label"], lec["tagline"]),
                 "isPartOf": {"@type": "WebSite", "name": "Shoug's Digital Garden", "url": SITE + "/"},
             }, ensure_ascii=False))
    out = out.replace("</head>", seo + "</head>", 1)
    return re.sub(r"[ \t]+\n", "\n", out)


# --------------------------------------------------------------------------- #
# 3. mindmaps (Ethics node-canvas model, fed from `branches`)
# --------------------------------------------------------------------------- #

def mindmap_html(lec: dict) -> str:
    title = lec["title"]
    tree = {
        "id": "root", "label": title,
        "desc": ('<span class="panel-tag">%s &middot; %s</span><p>A detailed concept map for '
                 '<strong>%s</strong>. Expand branches, select a node for detail, search topics, '
                 'zoom, pan, or export the full map.</p>'
                 % (COURSE_CODE, html.escape(lec["lecture_label"]), html.escape(title))),
        "children": [],
    }
    for bi, (name, desc, facts, *rest) in enumerate(lec["branches"], 1):
        examples = list(rest[0]) if rest else []
        branch = {
            "id": "branch-%d" % bi, "label": name,
            "desc": '<span class="panel-tag">Core Concept</span><p>%s</p>' % html.escape(desc),
            "children": [],
        }
        for fi, fact in enumerate(facts, 1):
            words = fact.rstrip(".").split()
            label = " ".join(words[:7]) + ("…" if len(words) > 7 else "")
            branch["children"].append({
                "id": "branch-%d-detail-%d" % (bi, fi), "label": label,
                "desc": '<span class="panel-tag">Key Detail</span><p>%s</p>' % html.escape(fact),
            })
        if examples:
            node = {
                "id": "branch-%d-examples" % bi, "label": "Examples",
                "desc": ('<span class="panel-tag">Examples</span><p>Worked illustrations of '
                         '<strong>%s</strong> from the lecture and from practice.</p>' % html.escape(name)),
                "children": [],
            }
            for ei, (elabel, etext) in enumerate(examples, 1):
                node["children"].append({
                    "id": "branch-%d-example-%d" % (bi, ei), "label": elabel,
                    "desc": '<span class="panel-tag">Example</span><p>%s</p>' % html.escape(etext),
                })
            branch["children"].append(node)
        tree["children"].append(branch)

    text = ETHICS_MAP_TEMPLATE.read_text(encoding="utf-8")
    page_title = "%s - %s Mindmap" % (title, COURSE_CODE)
    description = ("Interactive %s %s %s mindmap with expandable concepts, examples, search, zoom, pan, "
                   "details, and PNG export." % (COURSE_CODE, lec["lecture_label"], title))
    canonical = "%s%s/extra-resources/mindmaps/%02d-%s/%s.html" % (
        SITE, COURSE_ROUTE, lec["num"], lec["slug"], lec["slug"])

    text = re.sub(r"<title>.*?</title>", "<title>%s</title>" % esc(page_title), text, count=1, flags=re.S)
    text = re.sub(r'<meta name="description" content="[^"]*">',
                  '<meta name="description" content="%s">' % esc(description), text, count=1)
    for prop in ("og:title", "twitter:title"):
        text = re.sub(r'(<meta (?:property|name)="%s" content=")[^"]*(">)' % re.escape(prop),
                      lambda m: m.group(1) + esc(page_title) + m.group(2), text)
    for prop in ("og:description", "twitter:description"):
        text = re.sub(r'(<meta (?:property|name)="%s" content=")[^"]*(">)' % re.escape(prop),
                      lambda m: m.group(1) + esc(description) + m.group(2), text)
    text = re.sub(r'(<link rel="canonical" href=")[^"]*(">)',
                  lambda m: m.group(1) + canonical + m.group(2), text, count=1)
    text = re.sub(r'(<meta property="og:url" content=")[^"]*(">)',
                  lambda m: m.group(1) + canonical + m.group(2), text, count=1)
    text = re.sub(r'(<link rel="alternate" hreflang="(?:en|x-default)" href=")[^"]*(">)',
                  lambda m: m.group(1) + canonical + m.group(2), text)
    text = re.sub(r'(<link rel="alternate" hreflang="ar" href=")[^"]*(">)',
                  lambda m: m.group(1) + canonical.replace("shoug-tech.com/", "shoug-tech.com/ar/") + m.group(2),
                  text, count=1)
    schema = '<script type="application/ld+json">' + json.dumps({
        "@context": "https://schema.org", "@type": "WebPage", "url": canonical,
        "name": page_title, "description": description,
        "isPartOf": {"@type": "WebSite", "name": "Shoug's Digital Garden", "url": SITE + "/"},
    }, ensure_ascii=False) + "</script>"
    text = re.sub(r'<script\s+type="application/ld\+json">.*?</script>',
                  lambda _m: schema, text, count=1, flags=re.S)
    # The donor template labels its theme toggle with sun/moon pictographs; this
    # site's pages use text labels instead, so swap them for the SE365 maps.
    text = text.replace('id="theme-toggle" title="Toggle theme">\U0001f319<',
                        'id="theme-toggle" title="Toggle theme">LIGHT<')
    text = text.replace("themeBtn.textContent = dark ? '\U0001f319' : '\u2600\ufe0f';",
                        "themeBtn.textContent = dark ? 'LIGHT' : 'DARK';")
    text = text.replace("Moral Systems, Ethical Concepts, and Theories Mindmap",
                        "%s Mindmap" % html.escape(title))
    text = re.sub(r"const DATA = \{.*?\n\};\n\n        // ─+\n        // STATE",
                  lambda _m: "const DATA = " + json.dumps(tree, ensure_ascii=False, indent=4)
                  + ";\n\n        // ─────────────"
                    "───────────────"
                    "───────────────"
                    "──\n        // STATE",
                  text, count=1, flags=re.S)
    return text


# --------------------------------------------------------------------------- #
# 4. self-graded lecture exams
# --------------------------------------------------------------------------- #

EXAM_CSS = r"""
:root{--accent:__ACCENT__;--accent2:__ACCENT2__;
 --bg:#f5f4fb;--panel:#fff;--card:#faf9ff;--text:#1c2435;--muted:#5e687b;--line:#d8d5e6;
 --ok:#14753b;--bad:#ba2c41;--gold:#8a5a06;--shadow:0 16px 40px rgba(30,20,60,.10)}
html[data-theme="dark"]{--bg:#08050f;--panel:#120c22;--card:#180f2c;--text:#f0ebff;--muted:#a99ec6;
 --line:#2d2148;--ok:#5ad894;--bad:#ff6f86;--gold:#f0b95c;--shadow:0 18px 50px rgba(0,0,0,.55)}
*{box-sizing:border-box}
body{margin:0;color:var(--text);background:var(--bg);
 font:16px/1.6 ui-sans-serif,-apple-system,"Segoe UI",Inter,system-ui,sans-serif;min-height:100vh}
body::before{content:"";position:fixed;inset:0;z-index:-1;pointer-events:none;opacity:.5;
 background:radial-gradient(58rem 40rem at 10% -6%,color-mix(in srgb,var(--accent) 24%,transparent),transparent 70%),
 radial-gradient(48rem 36rem at 104% 16%,color-mix(in srgb,var(--accent2) 20%,transparent),transparent 70%)}
.top{position:sticky;top:0;z-index:20;background:color-mix(in srgb,var(--bg) 88%,transparent);
 backdrop-filter:blur(16px);border-bottom:1px solid var(--line)}
.topin,main{max-width:1180px;margin:0 auto;padding:13px clamp(16px,4vw,44px)}
.topin{display:flex;align-items:center;gap:13px}
.brand{margin-right:auto}
.eyebrow{font:700 11px/1 ui-monospace,monospace;letter-spacing:.18em;color:var(--accent)}
button{cursor:pointer;font-family:inherit}
.timer,.tbtn{border:1px solid var(--line);border-radius:10px;background:var(--panel);color:var(--text);
 padding:9px 12px;font:700 13px/1 ui-monospace,monospace;letter-spacing:.05em}
.tbtn:hover,.timer:hover{border-color:var(--accent);color:var(--accent)}
.hero{padding:clamp(30px,6vw,68px) 0 24px}
h1{font-size:clamp(28px,5.4vw,56px);line-height:1.06;margin:10px 0 14px;font-weight:800;letter-spacing:-.02em;
 background:linear-gradient(102deg,var(--text) 10%,var(--accent) 60%,var(--accent2) 98%);
 -webkit-background-clip:text;background-clip:text;color:transparent}
.hero p{max-width:80ch;color:var(--muted)}
.meta{display:flex;gap:15px;flex-wrap:wrap;font:13px/1.6 ui-monospace,monospace;color:var(--muted);margin-top:14px}
.meta b{color:var(--accent)}
.progress{height:7px;background:var(--line);border-radius:9px;overflow:hidden;margin:22px 0}
.progress i{display:block;width:0;height:100%;background:linear-gradient(90deg,var(--accent),var(--accent2));transition:.25s}
section{background:var(--panel);border:1px solid var(--line);border-radius:18px;
 padding:clamp(16px,3vw,30px);margin:20px 0;box-shadow:var(--shadow)}
section h2{margin-top:0;font-size:clamp(18px,2.4vw,24px)}
.q{border-top:1px solid var(--line);padding:22px 0}
.q:first-of-type{border-top:0}
.qnum{color:var(--gold);font:700 13px/1 ui-monospace,monospace;letter-spacing:.1em}
.prompt{font-weight:650;margin:8px 0 13px}
label{display:block;border:1px solid var(--line);background:var(--card);border-radius:11px;
 padding:11px 14px;margin:8px 0;transition:.18s;cursor:pointer}
label:hover{border-color:var(--accent);transform:translateX(4px)}
textarea{width:100%;min-height:104px;border:1px solid var(--line);background:var(--card);color:var(--text);
 border-radius:11px;padding:12px;font:inherit}
.feedback{display:none;margin-top:12px;padding:14px;border:1px solid transparent;border-radius:11px;
 color:var(--muted);font-size:15px}
.feedback.show{display:block}
.correct{border-color:var(--ok)!important;background:color-mix(in srgb,var(--ok) 16%,var(--card))!important;
 box-shadow:inset 4px 0 0 var(--ok)}
.wrong{border-color:var(--bad)!important;background:color-mix(in srgb,var(--bad) 16%,var(--card))!important;
 box-shadow:inset 4px 0 0 var(--bad)}
label.correct::after{content:"CORRECT";float:right;color:var(--ok);font:800 11px/1.6 ui-monospace,monospace}
label.wrong::after{content:"YOUR ANSWER";float:right;color:var(--bad);font:800 11px/1.6 ui-monospace,monospace}
textarea.correct,textarea.wrong{border-width:2px}
.actions{text-align:center;padding:18px}
.submit{border:0;border-radius:12px;background:linear-gradient(102deg,var(--accent),var(--accent2));color:#fff;
 padding:14px 30px;font-weight:800;font-size:16px;box-shadow:0 12px 32px color-mix(in srgb,var(--accent) 32%,transparent)}
.submit:hover{transform:translateY(-2px)}
.score{display:none;text-align:center;font-size:clamp(22px,4.4vw,42px);font-weight:800;padding:22px;
 border:2px solid transparent;border-radius:16px}
.score.show{display:block}
.score.pass{border-color:var(--ok);background:color-mix(in srgb,var(--ok) 14%,var(--panel))}
.score.fail{border-color:var(--bad);background:color-mix(in srgb,var(--bad) 14%,var(--panel))}
.score small{display:block;font-size:15px;font-weight:500;color:var(--muted);margin-top:8px}
@media(prefers-reduced-motion:reduce){*{transition:none!important}}
"""

EXAM_JS = r"""
(function(){
  var root=document.documentElement;
  function initial(){
    try{var s=localStorage.getItem('shoug-theme');if(s==='light'||s==='dark')return s;}catch(e){}
    try{if(window.parent&&window.parent!==window&&window.parent.document){
      var b=window.parent.document.body;
      if(b)return b.classList.contains('shoug-light-mode')?'light':'dark';}}catch(e){}
    return window.matchMedia&&window.matchMedia('(prefers-color-scheme: light)').matches?'light':'dark';
  }
  var t0=initial();root.setAttribute('data-theme',t0);
  try{localStorage.setItem('shoug-theme',t0);}catch(e){}
  var tb=document.getElementById('theme');
  function label(){tb.textContent=root.getAttribute('data-theme')==='dark'?'LIGHT':'DARK';}
  label();
  tb.onclick=function(){var n=root.getAttribute('data-theme')==='dark'?'light':'dark';
    root.setAttribute('data-theme',n);try{localStorage.setItem('shoug-theme',n);}catch(e){}label();};

  var mc=document.getElementById('mcq'),sa=document.getElementById('short');
  MCQ.forEach(function(x,i){
    mc.insertAdjacentHTML('beforeend','<article class="q"><span class="qnum">Q'+(i+1)+'</span>'+
      '<div class="prompt">'+x.q+'</div>'+
      x.options.map(function(o,j){return '<label><input type="radio" name="m'+i+'" value="'+j+'"> '+
        String.fromCharCode(65+j)+'. '+o+'</label>';}).join('')+
      '<div class="feedback" id="fm'+i+'"></div></article>');
  });
  SHORT.forEach(function(x,i){
    sa.insertAdjacentHTML('beforeend','<article class="q"><span class="qnum">Q'+(MCQ.length+i+1)+'</span>'+
      '<div class="prompt">'+x.q+'</div><textarea id="s'+i+'" placeholder="Write your answer..."></textarea>'+
      '<div class="feedback" id="fs'+i+'"></div></article>');
  });

  function update(){
    var done=document.querySelectorAll('input:checked').length+
      [].slice.call(document.querySelectorAll('textarea')).filter(function(x){return x.value.trim();}).length;
    document.getElementById('bar').style.width=(done/(MCQ.length+SHORT.length)*100)+'%';
  }
  document.addEventListener('input',update);

  var left=MINUTES*60,tick=setInterval(function(){
    left--;
    document.getElementById('timer').textContent=
      String(Math.floor(left/60)).padStart(2,'0')+':'+String(left%60).padStart(2,'0');
    if(left<=0){clearInterval(tick);grade();}
  },1000);

  function grade(){
    clearInterval(tick);
    var points=0;
    MCQ.forEach(function(x,i){
      var inputs=[].slice.call(document.querySelectorAll('input[name=m'+i+']'));
      var chosen=inputs.filter(function(n){return n.checked;})[0];
      var f=document.getElementById('fm'+i);
      inputs.forEach(function(n){n.disabled=true;if(+n.value===x.correct)n.parentNode.classList.add('correct');});
      if(chosen&&+chosen.value===x.correct){points++;f.className='feedback show correct';
        f.innerHTML='<b>Correct.</b> '+x.why;}
      else{if(chosen)chosen.parentNode.classList.add('wrong');f.className='feedback show wrong';
        f.innerHTML='<b>Incorrect. Correct answer: '+String.fromCharCode(65+x.correct)+'. '+
          x.options[x.correct]+'.</b> '+x.why;}
    });
    SHORT.forEach(function(x,i){
      var area=document.getElementById('s'+i),v=area.value.toLowerCase();
      var hits=x.keywords.filter(function(k){return v.indexOf(k)>-1;}).length;
      var earned=Math.min(2,hits);points+=earned;
      var state=earned>=1?'correct':'wrong';
      area.classList.add(state);area.disabled=true;
      var f=document.getElementById('fs'+i);f.className='feedback show '+state;
      f.innerHTML='<b>'+(earned>=1?'Credit earned':'Needs review')+' ('+earned+'/2 by keyword check).</b> '+
        'Model answer: '+x.answer;
    });
    var max=MCQ.length+SHORT.length*2,passed=points/max>=0.6,sc=document.getElementById('score');
    sc.className='score show '+(passed?'pass':'fail');
    sc.innerHTML=points+' / '+max+
      '<small>'+(passed?'Pass. ':'Below pass. ')+
      'Review the colour-coded answers above, then retry to strengthen weak areas.</small>';
    document.getElementById('submit').hidden=true;
    document.getElementById('reset').hidden=false;
  }
  document.getElementById('submit').onclick=grade;
  document.getElementById('reset').onclick=function(){location.reload();};
})();
"""


def exam_html(lec: dict) -> str:
    mcqs, shorts = lec["exam_mcq"], lec["exam_short"]
    count = len(mcqs) + len(shorts)
    max_points = len(mcqs) + len(shorts) * 2
    minutes = max(30, ((count * 3 + 1) // 2 // 5) * 5)
    title = "%s %s Exam - %s" % (COURSE_CODE, lec["lecture_label"], lec["title"])
    desc = "Self-graded %s %s exam on %s with explanations and model answers." % (
        COURSE_CODE, lec["lecture_label"], lec["title"])
    canonical = "%s%s/exams/%02d-%s-exam/%s-exam.html" % (
        SITE, COURSE_ROUTE, lec["num"], lec["slug"], lec["slug"])
    schema = json.dumps({
        "@context": "https://schema.org", "@type": "Quiz", "url": canonical,
        "name": title, "description": desc, "educationalLevel": "University",
        "about": {"@type": "Thing", "name": "%s %s" % (COURSE_CODE, COURSE_NAME)},
        "isPartOf": {"@type": "WebSite", "name": "Shoug's Digital Garden", "url": SITE + "/"},
    }, ensure_ascii=False)

    return """<!DOCTYPE html>
<html lang="en" data-theme="dark" data-sg-styled>
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>%(title)s</title>
<meta name="description" content="%(desc)s">
<link rel="canonical" href="%(canonical)s">
<link rel="icon" type="image/png" href="/assets/shoug-favicon-v4.png">
<meta property="og:type" content="article">
<meta property="og:title" content="%(title)s">
<meta property="og:description" content="%(desc)s">
<meta property="og:url" content="%(canonical)s">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="%(title)s">
<meta name="twitter:description" content="%(desc)s">
<script type="application/ld+json">%(schema)s</script>
<style>%(css)s</style>
</head>
<body>
<div class="top"><div class="topin">
  <div class="brand"><div class="eyebrow">%(code)s &middot; %(label)s</div>
    <strong>%(shortname)s &mdash; Lecture Exam</strong></div>
  <div class="timer" id="timer">%(minutes)d:00</div>
  <button class="tbtn" id="theme" type="button" aria-label="Toggle light and dark theme">LIGHT</button>
</div></div>

<main>
  <header class="hero">
    <div class="eyebrow">SELF-GRADED &middot; COMPREHENSIVE PRACTICE</div>
    <h1>%(plaintitle)s</h1>
    <p>Apply this lecture's definitions, distinctions and design implications. Submit for instant grading; every
       item carries an explanation of why the right answer is right and the others are wrong, or a model answer.</p>
    <div class="meta"><b>%(count)d questions</b><span>%(nmcq)d MCQ + %(nshort)d short answer</span>
      <span>%(max)d points</span><span>%(minutes)d minutes</span><span>Pass mark 60%%</span></div>
    <div class="progress"><i id="bar"></i></div>
  </header>

  <section><h2>Part A &mdash; Multiple choice</h2><div id="mcq"></div></section>
  <section><h2>Part B &mdash; Short answer</h2><div id="short"></div></section>

  <div class="actions">
    <button class="submit" id="submit" type="button">Submit exam</button>
    <button class="tbtn" id="reset" type="button" hidden>Reset</button>
  </div>
  <div class="score" id="score"></div>
</main>

<script>const MCQ=%(mcq)s,SHORT=%(short)s,MINUTES=%(minutes)d;</script>
<script>%(js)s</script>
</body>
</html>
""" % {
        "title": esc(title), "desc": esc(desc), "canonical": canonical, "schema": schema,
        "css": theme_css(EXAM_CSS, lec),
        "code": COURSE_CODE, "label": lec["lecture_label"].upper(),
        "shortname": html.escape(lec["short"]), "plaintitle": html.escape(lec["title"]),
        "count": count, "nmcq": len(mcqs), "nshort": len(shorts),
        "max": max_points, "minutes": minutes,
        "mcq": json.dumps(shuffled_mcqs(mcqs, "%s-exam" % lec["slug"]),
                          ensure_ascii=False).replace("</", "<\\/"),
        "short": json.dumps(shorts, ensure_ascii=False).replace("</", "<\\/"),
        "js": EXAM_JS,
    }


# --------------------------------------------------------------------------- #
# 5. wrappers for mindmaps and exams, and the listing pages
# --------------------------------------------------------------------------- #

def wrapper(lec: dict, kind: str, prev_lec: dict | None, next_lec: dict | None, template: str) -> str:
    """Reuse the breakdown shell for the mindmap and exam pages."""
    if kind == "map":
        folder_base = "%s/extra-resources/mindmaps/" % COURSE_ROUTE
        folder = "%02d-%s" % (lec["num"], lec["slug"])
        file = "%s.html" % lec["slug"]
        crumb_label, section, suffix = "Mindmaps", "Study Material", "Mindmap"
    else:
        folder_base = "%s/exams/" % COURSE_ROUTE
        folder = "%02d-%s-exam" % (lec["num"], lec["slug"])
        file = "%s-exam.html" % lec["slug"]
        crumb_label, section, suffix = "Exams", "Exams", "Exam"

    crumb = (
        '<div class="breadcrumb"><a class="breadcrumb-link" href="/academics/">Academics</a> '
        '<span class="separator">/</span> <a class="breadcrumb-link" href="/academics/software-engineering/">'
        'Software Engineering</a> <span class="separator">/</span> '
        '<a class="breadcrumb-link" href="%s/">SE365</a> <span class="separator">/</span> '
        '<a class="breadcrumb-link" href="%s">%s</a> '
        '<span class="separator">/</span> <span class="current">%s</span></div>'
        % (COURSE_ROUTE, folder_base, crumb_label, html.escape(lec["title"])))

    parts = []
    if prev_lec:
        prev_folder = ("%02d-%s" % (prev_lec["num"], prev_lec["slug"])) + ("-exam" if kind == "exam" else "")
        parts.append('<a href="%s%s/" class="nav-link prev">&lt;- PREVIOUS</a>' % (folder_base, prev_folder))
    if next_lec:
        next_folder = ("%02d-%s" % (next_lec["num"], next_lec["slug"])) + ("-exam" if kind == "exam" else "")
        parts.append('<a href="%s%s/" class="nav-link next">NEXT -&gt;</a>' % (folder_base, next_folder))
    navstrip = '<div class="nav-strip uppercase">%s</div>' % "".join(parts) if parts else ""

    title = html.escape(lec["title"])
    main = """        <main class="content-area" vid="58" id="main-content" tabindex="-1">

            <div class="top-bar uppercase" vid="59">
                {crumb}
                <div class="sys-time" id="clock" vid="70">SYS_TIME [ 00 00 00 ]</div>
            </div>

            <div class="page-header" vid="73">
                <div class="ch-label uppercase">{label} // {suffixup}</div>
                <h1 class="ch-title uppercase">{title}</h1>
                <div class="action-buttons"><a class="btn btn-primary" href="./{file}" target="_blank" rel="noopener noreferrer">[ OPEN IN NEW TAB -&gt; ]</a><a class="btn btn-secondary" href="{base}">[ &lt;- BACK TO INDEX ]</a></div>
            </div>

            {navstrip}

            <div class="embed-area-wrapper" vid="82">
                <div class="embed-container" id="embedded-content">
                    <div class="rendered-content" data-lang-panel="en"><iframe class="embed-frame legacy-html-frame" src="./{file}" loading="lazy" title="{title}"></iframe></div>
                    <div class="rendered-content" data-lang-panel="ar" hidden><iframe class="embed-frame legacy-html-frame" src="./{file}" loading="lazy" title="{title}"></iframe></div>
                </div>
            </div>
    </div>
    </div>

    </main>""".format(crumb=crumb, label=lec["lecture_label"].upper().replace(" ", "_"),
                      suffixup=suffix.upper() + "S", title=title, file=file,
                      base=folder_base, navstrip=navstrip)

    out = MAIN_RE.sub(lambda _m: main, template, count=1)
    out = re.sub(r"<title>.*?</title>",
                 "<title>SHOUG.TECH | SE365 %s %s</title>" % (html.escape(lec["title"]), suffix),
                 out, count=1, flags=re.S)
    out = re.sub(r'<meta\s+(?:property="og:[a-z:]+"|name="twitter:[a-z:]+"|name="description")'
                 r'\s+content="[^"]*"\s*>', '', out, flags=re.S)
    out = re.sub(r'<script\s+type="application/ld\+json"\s*>.*?</script>', '', out, flags=re.S)
    out = re.sub(r'<link\s+rel="alternate"\s+hreflang="[^"]*"\s+href="[^"]*"\s*>', '', out, flags=re.S)
    out = re.sub(r'<link rel="canonical"[^>]*>', '', out, flags=re.S)
    out = out.replace("ethcs303", "se365").replace("ETHCS303", "SE365")
    out = re.sub(r'<html(?![^>]*\bdata-theme=)([^>]*)>', r'<html\1 data-theme="dark">', out, count=1)

    url = "%s%s%s/" % (SITE, folder_base, folder)
    page_title = "SE365 %s &mdash; %s" % (html.escape(lec["title"]), suffix)
    desc_plain = "%s %s %s: %s" % (COURSE_CODE, lec["lecture_label"], suffix.lower(), lec["tagline"])
    desc = html.escape(desc_plain, quote=True)
    seo = (
        '<link rel="canonical" href="{url}">'
        '<meta name="description" content="{desc}">'
        '<meta property="og:title" content="{title}">'
        '<meta property="og:description" content="{desc}">'
        '<meta property="og:url" content="{url}">'
        '<meta property="og:type" content="article">'
        '<meta property="og:image" content="{site}/assets/og-banner.png">'
        '<meta name="twitter:card" content="summary_large_image">'
        '<meta name="twitter:title" content="{title}">'
        '<meta name="twitter:description" content="{desc}">'
        '<meta name="twitter:image" content="{site}/assets/og-banner.png">'
        '<script type="application/ld+json">{ld}</script>'
        '<link rel="alternate" hreflang="en" href="{url}">'
        '<link rel="alternate" hreflang="ar" href="{arurl}">'
        '<link rel="alternate" hreflang="x-default" href="{url}">'
    ).format(url=url, arurl=url.replace(SITE + "/", SITE + "/ar/"), desc=desc, title=page_title, site=SITE,
             ld=json.dumps({
                 "@context": "https://schema.org", "@type": "WebPage", "url": url,
                 "name": "SE365 %s - %s" % (lec["title"], suffix), "description": desc_plain,
                 "isPartOf": {"@type": "WebSite", "name": "Shoug's Digital Garden", "url": SITE + "/"},
             }, ensure_ascii=False))
    out = out.replace("</head>", seo + "</head>", 1)
    return re.sub(r"[ \t]+\n", "\n", out)


def listing_rows(kind: str) -> str:
    rows = []
    for lec in LECTURES:
        if kind == "breakdown":
            href = "%s/slide-breakdowns/%s/" % (COURSE_ROUTE, lec["slug"])
        elif kind == "map":
            href = "%s/extra-resources/mindmaps/%02d-%s/" % (COURSE_ROUTE, lec["num"], lec["slug"])
        else:
            href = "%s/exams/%02d-%s-exam/" % (COURSE_ROUTE, lec["num"], lec["slug"])
        seq = lec["lecture_label"].replace("Lectures ", "L").replace("Lecture ", "L").replace(" & ", "/")
        rows.append(
            '                            <a href="%s" class="dir-row">\n'
            '                                <div class="dir-num">%s</div>\n'
            '                                <div class="dir-title">%s</div>\n'
            '                                <div class="dir-status">'
            '<span class="status-tag available">AVAILABLE</span></div>\n'
            '                                %s\n'
            '                            </a>' % (href, seq, html.escape(lec["title"]), ARROW))
    return (
        '\n                <div class="directory-container">\n'
        '                <div class="dir-header">\n'
        '                    <span>SEQ</span>\n'
        '                    <span>DESCRIPTOR</span>\n'
        '                    <span>SYS_STATE</span>\n'
        '                    <span></span>\n'
        '                </div>\n\n'
        + "\n".join(rows) + "\n                </div>\n\n    ")


def write_listing(path: Path, block: str, section: str) -> None:
    page = path.read_text(encoding="utf-8")
    if COMING_SOON_RE.search(page):
        page = COMING_SOON_RE.sub(lambda _m: block, page, count=1)
    elif DIRECTORY_RE.search(page):
        page = DIRECTORY_RE.sub(lambda _m: block, page, count=1)
    else:
        raise SystemExit("%s: neither a coming-soon block nor a directory to replace" % path)
    path.write_text(re.sub(r"[ \t]+\n", "\n", page), encoding="utf-8")


# --------------------------------------------------------------------------- #
# 6. slide viewers
# --------------------------------------------------------------------------- #

def slides_replace_content(page: str, content: str) -> str:
    if COMING_SOON_RE.search(page):
        return COMING_SOON_RE.sub(lambda _m: "\n            " + content + "\n\n    ", page, count=1)
    if DIRECTORY_RE.search(page):
        return DIRECTORY_RE.sub(lambda _m: "\n            " + content + "\n\n    ", page, count=1)
    start = page.index('<section class="slide-viewer-shell"')
    end = page.index("\n\n\n            <footer", start)
    return page[:start] + content + page[end:]


def build_slides(template: str) -> None:
    rows = []
    for seq, num, pdf in SLIDE_DECKS:
        lec = by_num(num)
        rows.append(
            '<a class="dir-row" href="%s/slides/%s/">'
            '<div class="dir-num">%s</div>'
            '<div class="dir-title"><span class="dir-title-text">%s</span></div>'
            '<div class="dir-status"><span class="status-tag available">AVAILABLE</span></div>'
            '<div class="dir-arrow">-&gt;</div></a>'
            % (COURSE_ROUTE, pdf[:-4], seq, html.escape(lec["title"])))
    directory = ('<section class="slide-viewer-shell" aria-label="SE365 slide attribution">'
                 + UNIVERSITY_CREDIT + '</section>'
                 '<div class="directory-container" aria-label="SE365 lecture slides">'
                 '<div class="dir-header"><span>LEC</span><span>LECTURE</span>'
                 '<span>SYS_STATE</span><span></span></div>' + "".join(rows) + "</div>")
    index = slides_replace_content(template, directory)
    (SLIDES / "index.html").write_text(re.sub(r"[ \t]+\n", "\n", index), encoding="utf-8")

    for seq, num, pdf in SLIDE_DECKS:
        lec = by_num(num)
        if not (SLIDES / pdf).is_file():
            raise FileNotFoundError(SLIDES / pdf)
        slug = pdf[:-4]
        route = "%s%s/slides/%s/" % (SITE, COURSE_ROUTE, slug)
        page = re.sub(r"<title>.*?</title>",
                      "<title>%s: %s | SE365 Slides</title>" % (lec["lecture_label"], html.escape(lec["title"])),
                      template, count=1, flags=re.S)
        page = re.sub(r'<meta name="description"[^>]*>',
                      '<meta name="description" content="%s">'
                      % esc("View the embedded SE365 %s lecture slides on %s, credited to Prince Sultan University."
                            % (lec["lecture_label"], lec["title"])),
                      page, count=1)
        page = re.sub(r'<link rel="canonical"[^>]*>', '<link rel="canonical" href="%s">' % route, page, count=1)
        page = re.sub(r'<meta property="og:url"[^>]*>', '<meta property="og:url" content="%s">' % route,
                      page, count=1)
        page = page.replace(
            '<span class="current" data-en-text="Slides" data-ar-text="الشرائح">Slides</span>',
            '<a class="breadcrumb-link" href="%s/slides/">Slides</a> <span class="separator">/</span> '
            '<span class="current">%s</span>' % (COURSE_ROUTE, html.escape(lec["lecture_label"])), 1)
        page = page.replace(
            '<div class="type-label" data-en-text="SLIDES" data-ar-text="الشرائح">SLIDES</div>',
            '<div class="type-label">%s // %s</div>'
            % (lec["lecture_label"].upper(), html.escape(lec["title"]).upper()), 1)
        viewer = (
            '<section class="slide-viewer-shell" aria-label="%s slide viewer">%s'
            '<div class="slide-actions"><a class="slide-open-link" href="../%s" target="_blank" rel="noopener">'
            'OPEN PDF -&gt;</a></div>'
            '<iframe class="pdf-frame" src="../%s#view=FitH" title="%s slides"></iframe></section>'
            % (esc(lec["title"]), UNIVERSITY_CREDIT, pdf, pdf, esc(lec["title"])))
        page = slides_replace_content(page, viewer)
        folder = SLIDES / slug
        folder.mkdir(exist_ok=True)
        (folder / "index.html").write_text(re.sub(r"[ \t]+\n", "\n", page), encoding="utf-8")


# --------------------------------------------------------------------------- #
# 7. the study-material hub
# --------------------------------------------------------------------------- #

FOLDER_ICON = ('<svg class="dir-folder-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
               'stroke-width="2" stroke-linecap="square" stroke-linejoin="square" aria-hidden="true">'
               '<path d="M3 7a1 1 0 0 1 1-1h5l2 2h9a1 1 0 0 1 1 1v9a1 1 0 0 1-1 1H4a1 1 0 0 1-1-1V7z"/></svg>')


def build_extra_hub() -> None:
    path = BASE / "extra-resources/index.html"
    page = path.read_text(encoding="utf-8")
    block = ('\n                <div class="directory-container">'
             '<div class="dir-header"><span>SEQ</span><span>DESCRIPTOR</span>'
             '<span>SYS_STATE</span><span></span></div>'
             '<a class="dir-row" href="%s/extra-resources/mindmaps/">'
             '<div class="dir-num">1</div>'
             '<div class="dir-title"><span class="dir-title-text">Mindmaps</span>%s</div>'
             '<div class="dir-status"><span class="status-tag available">AVAILABLE</span></div>'
             '<div class="dir-arrow">-&gt;</div></a>'
             '</div>\n\n    ' % (COURSE_ROUTE, FOLDER_ICON))
    if COMING_SOON_RE.search(page):
        page = COMING_SOON_RE.sub(lambda _m: block, page, count=1)
    elif DIRECTORY_RE.search(page):
        page = DIRECTORY_RE.sub(lambda _m: block, page, count=1)
    else:
        raise SystemExit("extra-resources hub: nothing to replace")
    if ".dir-folder-icon {" not in page:
        page = page.replace("</style>", """
        .dir-title:has(.dir-folder-icon) { display: flex; align-items: center; gap: 10px; }
        .dir-folder-icon { width: 20px; height: 20px; flex: 0 0 auto; color: var(--text-tertiary); transition: color .2s ease, transform .2s ease; }
        .dir-row:hover .dir-folder-icon { color: var(--brand-purple); transform: translateY(-1px); }
        </style>""", 1)
    path.write_text(re.sub(r"[ \t]+\n", "\n", page), encoding="utf-8")


def clone_hub(source: Path, dest: Path, type_label: str, ar_label: str, crumb: str, ar_crumb: str) -> None:
    """Create a listing hub for a folder that has none, from a sibling hub."""
    page = source.read_text(encoding="utf-8")
    page = re.sub(r'<div class="type-label"[^>]*>[^<]*',
                  '<div class="type-label" data-en-text="%s" data-ar-text="%s">%s' % (type_label, ar_label, type_label),
                  page, count=1)
    page = page.replace('data-en-text="Study Material" data-ar-text="المواد الدراسية">Study Material</span>',
                        'data-en-text="%s" data-ar-text="%s">%s</span>' % (crumb, ar_crumb, crumb))
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(page, encoding="utf-8")


def main() -> None:
    template = SHELL_SRC.read_text(encoding="utf-8")

    # -- slide breakdowns --------------------------------------------------- #
    BREAKDOWNS.mkdir(parents=True, exist_ok=True)
    for i, lec in enumerate(LECTURES):
        folder = BREAKDOWNS / lec["slug"]
        folder.mkdir(exist_ok=True)
        (folder / ("%s.html" % lec["slug"])).write_text(breakdown_html(lec), encoding="utf-8")
        (folder / "index.html").write_text(
            build_shell(lec, LECTURES[i - 1] if i else None,
                        LECTURES[i + 1] if i + 1 < len(LECTURES) else None, template),
            encoding="utf-8")
    write_listing(BREAKDOWNS / "index.html", listing_rows("breakdown"), "Slide Breakdowns")

    # -- mindmaps ----------------------------------------------------------- #
    MAPS.mkdir(parents=True, exist_ok=True)
    if not (MAPS / "index.html").is_file():
        clone_hub(BASE / "slide-breakdowns/index.html", MAPS / "index.html",
                  "MINDMAPS", "الخرائط الذهنية", "Mindmaps", "الخرائط الذهنية")
    for i, lec in enumerate(LECTURES):
        folder = MAPS / ("%02d-%s" % (lec["num"], lec["slug"]))
        folder.mkdir(parents=True, exist_ok=True)
        (folder / ("%s.html" % lec["slug"])).write_text(mindmap_html(lec), encoding="utf-8")
        (folder / "index.html").write_text(
            wrapper(lec, "map", LECTURES[i - 1] if i else None,
                    LECTURES[i + 1] if i + 1 < len(LECTURES) else None, template),
            encoding="utf-8")
    write_listing(MAPS / "index.html", listing_rows("map"), "Study Material")

    # -- exams -------------------------------------------------------------- #
    EXAMS.mkdir(parents=True, exist_ok=True)
    for i, lec in enumerate(LECTURES):
        folder = EXAMS / ("%02d-%s-exam" % (lec["num"], lec["slug"]))
        folder.mkdir(parents=True, exist_ok=True)
        (folder / ("%s-exam.html" % lec["slug"])).write_text(exam_html(lec), encoding="utf-8")
        (folder / "index.html").write_text(
            wrapper(lec, "exam", LECTURES[i - 1] if i else None,
                    LECTURES[i + 1] if i + 1 < len(LECTURES) else None, template),
            encoding="utf-8")
    write_listing(EXAMS / "index.html", listing_rows("exam"), "Exams")

    # -- slides and the study-material hub ---------------------------------- #
    slides_template = (SLIDES / "index.html").read_text(encoding="utf-8")
    # Strip the previously generated attribution block together with the blank
    # lines around it, or each rebuild would leave one more of them behind.
    slides_template = re.sub(r'\n*\s*<section class="slide-viewer-shell".*?</section>', '',
                             slides_template, count=1, flags=re.S)
    if 'id="se365-slide-viewer-styles"' in slides_template:
        slides_template = re.sub(r'<style id="se365-slide-viewer-styles">.*?</style>',
                                 SLIDE_VIEWER_STYLES, slides_template, count=1, flags=re.S)
    else:
        slides_template = slides_template.replace("</head>", SLIDE_VIEWER_STYLES + "</head>", 1)
    build_slides(slides_template)
    build_extra_hub()

    print("SE365: %d breakdowns, %d mindmaps, %d exams, %d slide viewers."
          % (len(LECTURES), len(LECTURES), len(LECTURES), len(SLIDE_DECKS)))

    # The shells arrive with the donor course's sidebar; restamp from the single
    # source of truth rather than letting the two drift.
    subprocess.check_call([sys.executable, str(HERE / "build_academic_sidebar.py")])
    from fix_academic_sidebar_links import fix_page
    pages = [BREAKDOWNS / "index.html", MAPS / "index.html", EXAMS / "index.html",
             SLIDES / "index.html",
             *BREAKDOWNS.glob("*/index.html"), *MAPS.glob("*/index.html"),
             *EXAMS.glob("*/index.html"), *SLIDES.glob("*/index.html")]
    for page in pages:
        fix_page(page)


if __name__ == "__main__":
    main()
