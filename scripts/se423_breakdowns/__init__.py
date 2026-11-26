"""HTML building blocks for SE423 slide breakdowns rebuilt on the Estimation page's template
(scripts/build_se423_breakdowns.py). Content strings may contain inline HTML (<b>, <i>, <br>)."""


def sec(id_, num, title, desc, *blocks):
    d = f'\n            <p class="sec-desc">{desc}</p>' if desc else ""
    body = "\n".join(blocks)
    return f'''      <section id="{id_}">
        <div class="wrap">
          <div class="sec-head">
            <div class="sec-num">{num}</div>
            <h2 class="sec-title">{title}</h2>{d}
          </div>
{body}
        </div>
      </section>
'''


def hook(icon, phrase, decode, label="Memory hook"):
    return f'''          <div class="mnemonic">
            <div class="icon">{icon}</div>
            <div>
              <div class="label">{label}</div>
              <div class="phrase">{phrase}</div>
              <div class="decode">{decode}</div>
            </div>
          </div>'''


def box(html, style=""):
    s = f' style="{style}"' if style else ""
    return f'<div class="rule-box"{s}>{html}</div>'


def strip(html):
    return f'<div class="example-strip">{html}</div>'


def sub(text):
    return f'<span class="subhead">{text}</span>'


def col(*parts):
    return "<div>" + "".join(parts) + "</div>"


def two(left, right):
    return f'          <div class="two-col">{left}{right}</div>'


def table(headers, rows, num_cols=()):
    head = "".join(f'<th{" class=\"num\"" if i in num_cols else ""}>{h}</th>' for i, h in enumerate(headers))
    body = "".join("<tr>" + "".join(f'<td{" class=\"num\"" if i in num_cols else ""}>{c}</td>' for i, c in enumerate(r)) + "</tr>" for r in rows)
    return f'<div class="table-scroll"><table class="cheat-table"><tr>{head}</tr>{body}</table></div>'


def qa(title, tag, definition, *blocks, accent=None):
    style = f' style="margin-top: 26px; border-left-color: var(--{accent})"' if accent else ' style="margin-top: 26px"'
    d = f'<p class="qa-def">{definition}</p>' if definition else ""
    return f'''          <div class="qa-deep"{style}>
            <div class="qa-deep-head"><h3>{title}</h3><span class="qa-tag">{tag}</span></div>
            {d}{"".join(blocks)}
          </div>'''


def bullets(items):
    return box("<br />".join(f"• {i}" for i in items))


def cheat(rows):
    return sec("cheat", "§ CHEAT SHEET", "Everything in one table", None, "          " + table(["Concept", "What to remember"], rows))


def mistakes(items):
    out = []
    for i, (title, wrong, right) in enumerate(items, 1):
        out.append(f'''          <div class="mistake-box">
            <div class="m-title">{i}. {title}</div>
            <div class="mistake-row wrong"><span class="mk">✗ WRONG</span><span>{wrong}</span></div>
            <div class="mistake-row right"><span class="mk">✓ RIGHT</span><span>{right}</span></div>
          </div>''')
    return sec("mistakes", "§ COMMON MISTAKES", "Where exam answers usually go wrong",
               f"{len(items)} places this chapter's terms get mixed up.", *out)


def quiz(items):
    out = ['          <div class="quiz-list">']
    for i, (q, a) in enumerate(items, 1):
        out.append(f'''            <div class="quiz-item">
              <div class="quiz-q" onclick="this.nextElementSibling.classList.toggle('show')">
                <span class="qtext">{i}. {q}</span>
                <button class="quiz-reveal" type="button" onclick="event.stopPropagation(); this.closest('.quiz-item').querySelector('.quiz-answer').classList.toggle('show');">Reveal</button>
              </div>
              <div class="quiz-answer">{a}</div>
            </div>''')
    out.append("          </div>")
    return sec("quiz", "§ POP QUIZ", "Click a question to reveal the answer",
               "No tracking: click a question (or Reveal) to check yourself.", *out)
