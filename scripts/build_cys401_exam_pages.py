#!/usr/bin/env python3
"""Render the CYS401 past papers as interactive exam pages.

For each exam in scripts/quiz_banks/cys401_exams.py this writes:
  * <slug>/<file>        the standalone interactive exam (opens in a new tab)
  * <slug>/index.html    the site wrapper that embeds it, cloned from a sibling
                         exam page so the chrome always matches the course

Answers are checked in the browser. Every question explains itself once
checked: why the keyed answer is right, and for multiple choice, why the option
you picked is wrong.
"""

from __future__ import annotations

import html
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from normalize_page_urls import normalize  # noqa: E402
from quiz_banks.cys401_exams import EXAMS  # noqa: E402

EXAMS_DIR = ROOT / "docs/academics/cybersecurity/cys401/exams"
CHROME = EXAMS_DIR / "01-chapter-1-quiz/index.html"
BASE = "/academics/cybersecurity/cys401/exams/"

PAGE_CSS = """
:root{color-scheme:dark;--bg:#07050a;--panel:#100a12;--panel-2:#160e1a;--line:rgba(255,255,255,.12);
--line-dim:rgba(255,255,255,.07);--text:#f4f1f6;--muted:#a49daa;--accent:#ff2e63;--accent-soft:rgba(255,46,99,.12);
--ok:#22c55e;--ok-soft:rgba(34,197,94,.12);--bad:#ef4444;--bad-soft:rgba(239,68,68,.1);--warn:#eab308;
--mono:"JetBrains Mono",ui-monospace,SFMono-Regular,Menlo,monospace;
--sans:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--text);font-family:var(--sans);font-size:16px;line-height:1.65}
.wrap{max-width:900px;margin:0 auto;padding:clamp(20px,4vw,48px) clamp(16px,4vw,32px) 96px}
header.exam-head{border:1px solid var(--line);background:linear-gradient(160deg,var(--panel-2),var(--panel));padding:clamp(20px,3vw,32px);margin-bottom:22px}
.kicker{font-family:var(--mono);font-size:.7rem;letter-spacing:.18em;text-transform:uppercase;color:var(--accent);margin-bottom:10px}
h1{font-size:clamp(1.5rem,4vw,2.2rem);line-height:1.2;margin:0 0 10px}
.meta{font-family:var(--mono);font-size:.72rem;color:var(--muted);letter-spacing:.04em}
.intro{margin:14px 0 0;color:var(--muted);font-size:.95rem}
.scorebar{position:sticky;top:0;z-index:5;display:flex;align-items:center;gap:14px;flex-wrap:wrap;
padding:12px 16px;margin-bottom:24px;border:1px solid var(--line);background:rgba(16,10,18,.96);backdrop-filter:blur(6px)}
.score{font-family:var(--mono);font-size:.8rem;letter-spacing:.06em}
.score strong{color:var(--accent);font-size:1rem}
.btn{font-family:var(--mono);font-size:.72rem;letter-spacing:.08em;text-transform:uppercase;padding:10px 15px;
border:1px solid var(--line);background:transparent;color:var(--text);cursor:pointer}
.btn:hover{border-color:var(--accent);color:var(--accent)}
.btn-primary{border-color:var(--accent);color:var(--accent);background:var(--accent-soft)}
section.part{margin:0 0 28px}
.part-head{display:flex;align-items:baseline;gap:12px;flex-wrap:wrap;border-bottom:1px solid var(--line);padding-bottom:8px;margin-bottom:18px}
.part-head h2{font-family:var(--mono);font-size:.82rem;letter-spacing:.12em;text-transform:uppercase;color:var(--accent);margin:0}
.part-note{font-family:var(--mono);font-size:.68rem;color:var(--muted)}
.q{border:1px solid var(--line);background:var(--panel);padding:clamp(16px,2.5vw,24px);margin-bottom:16px}
.q.correct{border-color:rgba(34,197,94,.5)}
.q.wrong{border-color:rgba(239,68,68,.5)}
.q-num{font-family:var(--mono);font-size:.68rem;letter-spacing:.1em;color:var(--accent);margin-bottom:8px}
.q-text{margin:0 0 14px;font-weight:500}
.opts{display:flex;flex-direction:column;gap:8px}
.opt{display:flex;gap:10px;align-items:flex-start;padding:10px 12px;border:1px solid var(--line-dim);cursor:pointer}
.opt:hover{border-color:var(--line)}
.opt input{margin:4px 0 0}
.opt.is-correct{border-color:var(--ok);background:var(--ok-soft)}
.opt.is-wrong{border-color:var(--bad);background:var(--bad-soft)}
.opt-tag{font-family:var(--mono);font-size:.7rem;color:var(--muted);flex:0 0 auto}
.match-item{display:grid;grid-template-columns:1fr 240px;gap:12px;align-items:start;padding:12px 0;border-top:1px solid var(--line-dim)}
.match-item:first-child{border-top:0}
select,input[type=text],textarea{width:100%;font:inherit;font-size:.92rem;color:var(--text);background:var(--panel-2);
border:1px solid var(--line);padding:9px 11px}
textarea{min-height:110px;resize:vertical;line-height:1.6}
input[type=text]{max-width:260px}
select:focus,input:focus,textarea:focus{outline:2px solid var(--accent);outline-offset:1px}
.unit{font-family:var(--mono);color:var(--muted);margin-left:8px}
.feedback{display:none;margin-top:14px;padding:13px 15px;border-inline-start:3px solid var(--accent);background:var(--panel-2);font-size:.92rem}
.feedback.show{display:block}
.verdict{font-family:var(--mono);font-size:.72rem;letter-spacing:.08em;text-transform:uppercase;margin-bottom:8px}
.verdict.ok{color:var(--ok)}
.verdict.no{color:var(--bad)}
.feedback p{margin:0 0 8px}
.feedback p:last-child{margin-bottom:0}
.model{margin-top:10px;padding-top:10px;border-top:1px solid var(--line-dim);color:var(--muted)}
.model b{color:var(--text)}
.note{margin-top:10px;padding:10px 12px;border:1px dashed rgba(234,179,8,.5);color:#f5e6a8;font-size:.87rem}
.note b{color:var(--warn)}
.missed{color:var(--bad)}
.q-actions{margin-top:14px}
footer.exam-foot{margin-top:32px;padding-top:18px;border-top:1px solid var(--line);font-family:var(--mono);
font-size:.68rem;color:var(--muted);letter-spacing:.05em}
@media(max-width:700px){.match-item{grid-template-columns:1fr}.wrap{padding-bottom:72px}
.scorebar{position:static}input[type=text]{max-width:none}}
@media print{.scorebar,.q-actions,.btn{display:none}.feedback{display:block}}
"""

PAGE_JS = """
(function(){
  var DATA = __DATA__;
  var total = 0, checked = {}, correct = {};

  function esc(s){var d=document.createElement('div');d.textContent=s;return d.innerHTML;}

  function feedback(el, ok, bodyHtml){
    el.innerHTML = '<div class="verdict ' + (ok ? 'ok">Correct' : 'no">Not quite') + '</div>' + bodyHtml;
    el.classList.add('show');
  }

  function markCard(card, ok){
    card.classList.remove('correct','wrong');
    card.classList.add(ok ? 'correct' : 'wrong');
  }

  function scoreLine(){
    var done = Object.keys(checked).length;
    var right = Object.keys(correct).filter(function(k){return correct[k];}).length;
    var pct = done ? Math.round(right / done * 100) : 0;
    document.getElementById('score').innerHTML =
      'Answered <strong>' + done + '</strong> of ' + total +
      ' &nbsp;·&nbsp; Correct <strong>' + right + '</strong>' +
      (done ? ' &nbsp;·&nbsp; <strong>' + pct + '%</strong>' : '');
  }

  function check(card, force){
    var q = DATA[card.dataset.qid];
    var fb = card.querySelector('.feedback');
    var ok = false, body = '';

    if (q.type === 'mcq'){
      var picked = card.querySelector('input[type=radio]:checked');
      if (!picked && !force) return false;
      var idx = picked ? parseInt(picked.value, 10) : -1;
      ok = idx === q.correct;
      card.querySelectorAll('.opt').forEach(function(o, i){
        o.classList.remove('is-correct','is-wrong');
        if (i === q.correct) o.classList.add('is-correct');
        else if (i === idx) o.classList.add('is-wrong');
      });
      if (idx === -1) body += '<p><b>Not answered.</b></p>';
      else if (!ok && q.wrong && q.wrong[idx]) body += '<p><b>Why your answer is wrong:</b> ' + q.wrong[idx] + '</p>';
      body += '<p><b>Why ' + String.fromCharCode(97 + q.correct) + ' is right:</b> ' + q.why + '</p>';

    } else if (q.type === 'fill'){
      var v = (card.querySelector('input[type=text]').value || '').trim().toLowerCase();
      if (!v && !force) return false;
      if (!v) body += '<p><b>Not answered.</b></p>';
      ok = q.accept.some(function(a){ return v.indexOf(a) !== -1 || a.indexOf(v) !== -1 && v.length > 3; });
      body = '<p><b>Answer:</b> ' + q.answer + '</p><p>' + q.why + '</p>';

    } else if (q.type === 'numeric'){
      var raw = (card.querySelector('input[type=text]').value || '').replace(/[%\\s,]/g,'');
      if (!raw && !force) return false;
      if (!raw) body += '<p><b>Not answered.</b></p>';
      var n = parseFloat(raw);
      ok = !isNaN(n) && Math.abs(n - q.answer) <= q.tol;
      body = '<p><b>Answer:</b> ' + q.answer + (q.unit || '') + '</p><p>' + q.why + '</p>';

    } else if (q.type === 'match'){
      var rows = card.querySelectorAll('select');
      var any = false, allRight = true, lines = [];
      rows.forEach(function(sel, i){
        if (sel.value) any = true;
        var right = sel.value === q.items[i][1];
        if (!right) allRight = false;
        if (sel.value && !right){
          lines.push('<p><b>' + esc(q.items[i][0].slice(0, 60)) + '…</b><br />' +
            'You chose <span class="missed">' + esc(sel.value) + '</span>. The answer is <b>' +
            esc(q.items[i][1]) + '</b> — ' + q.items[i][2] + '</p>');
        } else if (!sel.value){
          allRight = false;
          lines.push('<p><b>' + esc(q.items[i][0].slice(0, 60)) + '…</b><br />Left blank. The answer is <b>' +
            esc(q.items[i][1]) + '</b> — ' + q.items[i][2] + '</p>');
        }
      });
      if (!any && !force) return false;
      ok = allRight;
      body = ok
        ? '<p>Every item matched. ' + q.items.map(function(it){ return '<br /><b>' + esc(it[1]) + '</b> — ' + it[2]; }).join('') + '</p>'
        : lines.join('');

    } else if (q.type === 'short'){
      var text = (card.querySelector('textarea').value || '').toLowerCase();
      if (!text.trim() && !force) return false;
      var hit = [], miss = [];
      q.concepts.forEach(function(group){
        (group.some(function(w){ return text.indexOf(w) !== -1; }) ? hit : miss).push(group[0]);
      });
      ok = miss.length === 0;
      body = ok
        ? '<p>Your answer covers every point the marker looks for: ' + hit.map(esc).join(', ') + '.</p>'
        : '<p><b>Missing from your answer:</b> <span class="missed">' + miss.map(esc).join(', ') +
          '</span>' + (hit.length ? ' &nbsp;(you did cover: ' + hit.map(esc).join(', ') + ')' : '') + '</p>';
      body += '<p>' + q.why + '</p>';
      body += '<div class="model"><b>Model answer.</b> ' + q.answer + '</div>';
    }

    if (q.note) body += '<div class="note"><b>Note.</b> ' + q.note + '</div>';
    feedback(fb, ok, body);
    markCard(card, ok);
    checked[card.dataset.qid] = true;
    correct[card.dataset.qid] = ok;
    scoreLine();
    return true;
  }

  document.addEventListener('DOMContentLoaded', function(){
    var cards = document.querySelectorAll('.q');
    total = cards.length;
    cards.forEach(function(card){
      card.querySelector('.check-one').addEventListener('click', function(){
        if (!check(card)){
          var fb = card.querySelector('.feedback');
          feedback(fb, false, '<p>Answer the question first, then check it.</p>');
        }
      });
    });
    document.getElementById('check-all').addEventListener('click', function(){
      cards.forEach(function(card){ check(card, true); });
      scoreLine();
    });
    document.getElementById('reset').addEventListener('click', function(){
      checked = {}; correct = {};
      cards.forEach(function(card){
        card.classList.remove('correct','wrong');
        card.querySelector('.feedback').classList.remove('show');
        card.querySelectorAll('.opt').forEach(function(o){ o.classList.remove('is-correct','is-wrong'); });
        card.querySelectorAll('input[type=radio]').forEach(function(i){ i.checked = false; });
        card.querySelectorAll('input[type=text], textarea').forEach(function(i){ i.value = ''; });
        card.querySelectorAll('select').forEach(function(s){ s.selectedIndex = 0; });
      });
      scoreLine();
      window.scrollTo({top:0, behavior:'smooth'});
    });
    scoreLine();
  });
})();
"""


def esc(text: str) -> str:
    return html.escape(text, quote=False)


def render_question(q: dict, qid: str, number: int) -> str:
    out = [f'<div class="q" data-qid="{qid}">',
           f'  <div class="q-num">Q{number}</div>',
           f'  <p class="q-text">{esc(q["q"])}</p>']

    if q["type"] == "mcq":
        out.append('  <div class="opts">')
        for i, opt in enumerate(q["options"]):
            letter = chr(97 + i)
            out += [f'    <label class="opt"><input type="radio" name="{qid}" value="{i}" />',
                    f'      <span class="opt-tag">{letter})</span><span>{esc(opt)}</span></label>']
        out.append('  </div>')

    elif q["type"] in ("fill", "numeric"):
        unit = f'<span class="unit">{esc(q["unit"])}</span>' if q.get("unit") else ""
        out.append(f'  <div><input type="text" name="{qid}" autocomplete="off" '
                   f'placeholder="Your answer" />{unit}</div>')

    elif q["type"] == "match":
        for i, item in enumerate(q["items"]):
            options = "".join(f'<option value="{html.escape(o, quote=True)}">{esc(o)}</option>'
                              for o in q["options"])
            out += ['  <div class="match-item">',
                    f'    <div>{esc(item[0])}</div>',
                    f'    <select name="{qid}-{i}" aria-label="Answer {i + 1}">'
                    f'<option value="">Choose…</option>{options}</select>',
                    '  </div>']

    elif q["type"] == "short":
        out.append(f'  <textarea name="{qid}" placeholder="Write your answer"></textarea>')

    out += ['  <div class="q-actions"><button type="button" class="btn check-one">Check this answer</button></div>',
            '  <div class="feedback"></div>',
            '</div>']
    return "\n".join(out)


def render_exam(exam: dict) -> str:
    data: dict[str, dict] = {}
    body: list[str] = []
    number = 0

    for section in exam["sections"]:
        body += ['<section class="part">',
                 '  <div class="part-head">',
                 f'    <h2>{esc(section["name"])}</h2>',
                 f'    <span class="part-note">{esc(section.get("note", ""))}</span>',
                 '  </div>']
        for q in section["questions"]:
            number += 1
            qid = f"q{number}"
            payload = {k: v for k, v in q.items() if k != "q"}
            if q["type"] == "mcq" and "wrong" in q:
                payload["wrong"] = {str(k): v for k, v in q["wrong"].items()}
            data[qid] = payload
            body.append(render_question(q, qid, number))
        body.append('</section>')

    script = PAGE_JS.replace("__DATA__", json.dumps(data, ensure_ascii=False))
    # The standalone file is indexed under its folder route, matching the
    # sibling quizzes and what check_seo_metadata.py expects.
    canonical = f'https://shoug-tech.com{BASE}{exam["slug"]}/'
    desc = html.escape(exam["intro"], quote=True)
    og_title = html.escape(f'CYS401 {exam["title"]} - interactive, with answer checking', quote=True)
    return f"""<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>CYS401 | {esc(exam["title"])}</title>
    <meta name="description" content="{desc}" />
    <link rel="canonical" href="{canonical}" />
    <meta property="og:title" content="{og_title}" />
    <meta property="og:description" content="{desc}" />
    <meta property="og:url" content="{canonical}" />
    <meta property="og:type" content="article" />
    <meta property="og:image" content="https://shoug-tech.com/assets/og-banner.png" />
    <meta name="twitter:card" content="summary_large_image" />
    <meta name="twitter:title" content="{og_title}" />
    <meta name="twitter:description" content="{desc}" />
    <meta name="twitter:image" content="https://shoug-tech.com/assets/og-banner.png" />
    <link rel="stylesheet" href="/styles/a11y.css" />
    <style>{PAGE_CSS}</style>
  </head>
  <body>
    <div class="wrap">
      <header class="exam-head">
        <div class="kicker">CYS401 · Fundamentals of Cybersecurity</div>
        <h1>{esc(exam["title"])}</h1>
        <div class="meta">{esc(exam["meta"])}</div>
        <p class="intro">{esc(exam["intro"])}</p>
      </header>
      <div class="scorebar">
        <span class="score" id="score"></span>
        <button type="button" class="btn btn-primary" id="check-all">Check all answers</button>
        <button type="button" class="btn" id="reset">Reset</button>
      </div>
{chr(10).join(body)}
      <footer class="exam-foot">
        Transcribed from the original paper for revision. Answers follow the official key;
        where the key is wrong or ambiguous, the explanation says so.
      </footer>
    </div>
    <script>{script}</script>
  </body>
</html>
"""


def wrapper(exam: dict) -> str:
    page = CHROME.read_text(encoding="utf-8")
    page = page.replace("Chapter 1 Quiz", exam["title"])
    page = page.replace("ITEM_01 // EXAMS", f'{exam["item"]} // EXAMS')
    page = re.sub(r'(?<=")(?:\./)?chapter-1-quiz\.html(?=")', exam["file"], page)
    page = re.sub(r'<title>.*?</title>',
                  f'<title>CYS401 | {esc(exam["title"])}</title>', page, count=1, flags=re.S)
    return page


def main() -> None:
    for exam in EXAMS:
        folder = EXAMS_DIR / exam["slug"]
        folder.mkdir(parents=True, exist_ok=True)
        (folder / exam["file"]).write_text(render_exam(exam), encoding="utf-8")
        target = folder / "index.html"
        target.write_text(normalize(wrapper(exam), target.resolve()), encoding="utf-8")
        questions = sum(len(s["questions"]) for s in exam["sections"])
        print(f'built {exam["slug"]}/ ({questions} questions)')


if __name__ == "__main__":
    main()
