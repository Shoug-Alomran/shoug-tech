#!/usr/bin/env python3
"""Build an exam study plan page from scripts/study_plans/<course>-<exam>.json.

    python3 scripts/build_study_plan.py scripts/study_plans/se423-midterm.json

Writes <out_dir>/<slug>.html only: the content page that the wrapper
index.html iframes. The wrapper, its Study Material row and its sidebar entry
are created once by hand (clone a sibling wrapper, then add the entry to
scripts/academic-sidebar.json and run build_academic_sidebar.py).

The JSON holds the judgment calls: each item's tier (core / high / optional),
minutes, focus and reason, plus a skip list with a reason and an alternative
for every entry. Links are relative to "base" and open in the top window,
because the page is shown inside the wrapper's iframe.
"""

import html
import json
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TIER_ORDER = ["core", "high", "optional"]


def esc(text):
    return html.escape(str(text), quote=True)


def fmt_minutes(total):
    hours, mins = divmod(int(total), 60)
    if hours and mins:
        return f"{hours}h {mins:02d}m"
    return f"{hours}h" if hours else f"{mins}m"


def link(plan, rel):
    return esc(plan["base"] + rel)


def chapter_chips(plan, chapters):
    out = []
    for ch in chapters:
        info = plan["chapters"][ch]
        out.append(
            f'<span class="chip" style="--hue: {info["hue"]}" title="{esc(info["name"])}">'
            f"Ch {esc(ch)}</span>"
        )
    return "".join(out)


def item_html(plan, item, number):
    key = item["title"]
    focus = f'<p class="focus"><b>Focus:</b> {esc(item["focus"])}</p>' if item.get("focus") else ""
    return f"""
          <li class="item" data-key="{esc(key)}" data-min="{item['minutes']}">
            <span class="num" aria-hidden="true">{number}</span>
            <h3><a href="{link(plan, item['url'])}" target="_top">{esc(item['title'])}</a></h3>
            <div class="body">
              <div class="meta">{chapter_chips(plan, item['chapters'])}<span class="mins">{item['minutes']} min</span></div>
              {focus}
              <p class="why">{esc(item['why'])}</p>
              <label class="done"><input type="checkbox" aria-label="Mark {esc(item['title'])} done" /> Done</label>
            </div>
          </li>"""


def plan_html(plan):
    parts = []
    number = 0
    for tier in TIER_ORDER:
        items = [i for i in plan["items"] if i["tier"] == tier]
        if not items:
            continue
        meta = plan["tiers"][tier]
        rows = []
        for item in items:
            number += 1
            rows.append(item_html(plan, item, number))
        minutes = sum(i["minutes"] for i in items)
        parts.append(f"""
        <section class="tier" data-tier="{tier}" aria-labelledby="tier-{tier}">
          <div class="tier-head">
            <span class="tier-tag">{esc(meta['label'])}</span>
            <h2 id="tier-{tier}">{esc(meta['label'])}</h2>
            <span class="tier-time">{fmt_minutes(minutes)}</span>
            <p>{esc(meta['blurb'])}</p>
          </div>
          <ol class="items" start="{number - len(items) + 1}">{''.join(rows)}
          </ol>
        </section>""")
    return "".join(parts)


def budget_html(plan):
    options = []
    for budget in plan["budgets"]:
        minutes = sum(i["minutes"] for i in plan["items"] if i["tier"] in budget["tiers"])
        checked = " checked" if budget["id"] == plan["default_budget"] else ""
        options.append(f"""
              <label>
                <input type="radio" name="budget" value="{esc(budget['id'])}" data-tiers="{esc(' '.join(budget['tiers']))}"{checked} />
                <span><b>{esc(budget['label'])}</b><small>{fmt_minutes(minutes)} of study</small></span>
              </label>""")
    return "".join(options)


def skip_html(plan):
    cards = []
    for entry in plan["skip"]:
        instead = ""
        if entry.get("instead"):
            instead = (
                f'<a class="instead" href="{link(plan, entry["instead"]["url"])}" target="_top">'
                f'Use instead: {esc(entry["instead"]["label"])} &rarr;</a>'
            )
        cards.append(f"""
          <article class="skip">
            <span class="skip-tag">Skip</span>
            <h3><a href="{link(plan, entry['url'])}" target="_top">{esc(entry['title'])}</a></h3>
            <p>{esc(entry['why'])}</p>
            {instead}
          </article>""")
    return "".join(cards)


def later_html(plan):
    later = plan["out_of_scope"]
    links = "".join(
        f'<li><a href="{link(plan, l["url"])}" target="_top">{esc(l["label"])}</a></li>'
        for l in later["links"]
    )
    return f"""
        <div class="later">
          <p>{esc(later['blurb'])}</p>
          <ul>{links}</ul>
        </div>"""


SCRIPT = """
    <script>
      (function () {
        var KEY = "study-plan:%(key)s:";
        var EXAM = "%(exam_date)s";
        function load(name, fallback) {
          try {
            var v = localStorage.getItem(KEY + name);
            return v === null ? fallback : JSON.parse(v);
          } catch (e) {
            return fallback;
          }
        }
        function save(name, value) {
          try {
            localStorage.setItem(KEY + name, JSON.stringify(value));
          } catch (e) {}
        }
        function fmt(m) {
          var h = Math.floor(m / 60), r = m %% 60;
          if (h && r) return h + "h " + (r < 10 ? "0" : "") + r + "m";
          return h ? h + "h" : r + "m";
        }

        var done = load("done", {});
        var radios = document.querySelectorAll('input[name="budget"]');
        var tiers = document.querySelectorAll(".tier");
        var items = document.querySelectorAll(".item");
        var fill = document.querySelector(".progress .fill");
        var text = document.querySelector("[data-progress]");

        function activeTiers() {
          var r = document.querySelector('input[name="budget"]:checked');
          return r ? r.getAttribute("data-tiers").split(" ") : [];
        }
        function refresh() {
          var on = activeTiers();
          tiers.forEach(function (t) {
            t.hidden = on.indexOf(t.getAttribute("data-tier")) === -1;
          });
          var total = 0, left = 0, count = 0, finished = 0;
          items.forEach(function (it) {
            var isDone = !!done[it.getAttribute("data-key")];
            it.classList.toggle("is-done", isDone);
            it.querySelector(".done input").checked = isDone;
            if (it.closest(".tier").hidden) return;
            var m = parseInt(it.getAttribute("data-min"), 10);
            total += m;
            count += 1;
            if (isDone) finished += 1;
            else left += m;
          });
          fill.style.width = total ? Math.round(((total - left) / total) * 100) + "%%" : "0";
          text.innerHTML =
            "<b>" + finished + " of " + count + "</b> done · " +
            (left ? "<b>" + fmt(left) + "</b> left" : "<b>all done</b>");
        }

        var saved = load("budget", null);
        radios.forEach(function (r) {
          if (saved && r.value === saved) r.checked = true;
          r.addEventListener("change", function () {
            save("budget", r.value);
            refresh();
          });
        });
        items.forEach(function (it) {
          it.querySelector(".done input").addEventListener("change", function (e) {
            var k = it.getAttribute("data-key");
            if (e.target.checked) done[k] = true;
            else delete done[k];
            save("done", done);
            refresh();
          });
        });

        var countdown = document.querySelector("[data-countdown]");
        if (countdown) {
          var parts = EXAM.split("-");
          var exam = new Date(+parts[0], +parts[1] - 1, +parts[2]);
          var now = new Date();
          var today = new Date(now.getFullYear(), now.getMonth(), now.getDate());
          var days = Math.round((exam - today) / 86400000);
          if (days > 1) countdown.innerHTML = "<b>" + days + " days</b> to go";
          else if (days === 1) countdown.innerHTML = "<b>Tomorrow</b>";
          else if (days === 0) countdown.innerHTML = "<b>Today</b>, good luck";
          else countdown.parentNode.removeChild(countdown);
        }
        refresh();
      })();
    </script>"""


def page(plan):
    exam_day = date.fromisoformat(plan["exam_date"])
    exam_label = exam_day.strftime("%a %d %b %Y").replace(" 0", " ")
    title = f"{plan['course']} | {plan['title']}"
    canonical = f"https://shoug-tech.com{plan['base']}extra-resources/{plan['slug']}/"
    script = SCRIPT % {
        "key": esc(f"{plan['course'].lower()}-{plan['slug']}"),
        "exam_date": plan["exam_date"],
    }
    return f"""<!doctype html>
<html lang="en" data-sg-styled style="--hue: {plan['hue']}">
  <head>
    <link rel="icon" type="image/png" sizes="256x256" href="/assets/shoug-favicon-v4.png" />
    <link rel="shortcut icon" type="image/png" href="/assets/shoug-favicon-v4.png" />
    <link rel="apple-touch-icon" sizes="180x180" href="/assets/shoug-apple-touch-icon-v4.png" />
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>{esc(title)}</title>
    <meta name="description" content="{esc(plan['description'])}" />
    <link rel="canonical" href="{esc(canonical)}" />
    <meta property="og:title" content="{esc(title)}" />
    <meta property="og:description" content="{esc(plan['description'])}" />
    <meta property="og:url" content="{esc(canonical)}" />
    <meta property="og:type" content="website" />
    <meta property="og:image" content="https://shoug-tech.com/assets/og-banner.png" />
    <meta name="twitter:card" content="summary_large_image" />
    <link rel="preconnect" href="https://fonts.googleapis.com" />
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
    <link
      href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,500;9..144,650&family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500;600;700&display=swap"
      rel="stylesheet"
    />
    <script src="/javascripts/html-theme-sync.js"></script>
    <link rel="stylesheet" href="/styles/study-plan.css" />
  </head>
  <body>
    <header class="topbar">
      <div class="wrap">
        <span class="brand"><b>{esc(plan['course'])}</b> // {esc(plan['exam'].upper())} PLAN</span>
        <nav class="topnav" aria-label="Page sections">
          <a href="#plan">Plan</a>
          <a href="#skip">Skip</a>
          <a href="#later">Later</a>
        </nav>
        <div class="topbar-end">
          <div data-page-search-host></div>
          <button class="btn" type="button" onclick="toggleTheme()">
            <span data-theme-label>Dark</span>
          </button>
        </div>
      </div>
    </header>

    <main class="wrap">
      <section class="hero">
        <div class="eyebrow">{esc(plan['course'])} · {esc(plan['course_name'])} · {esc(plan['exam'])}</div>
        <h1>What to study, and what to skip</h1>
        <p class="lede">{esc(plan['lede'])}</p>
        <ul class="facts">
          <li><b>{esc(plan['exam'])}</b> · {esc(exam_label)}</li>
          <li data-countdown></li>
          <li>Covers <b>{esc(plan['scope'])}</b></li>
        </ul>

        <div class="budget-panel">
          <fieldset class="budget">
            <legend>How much time do you have?</legend>
            <div class="budget-options">{budget_html(plan)}
            </div>
          </fieldset>
          <div class="progress">
            <span class="track"><span class="fill"></span></span>
            <span data-progress></span>
          </div>
        </div>
      </section>

      <section class="part" id="plan" aria-label="Study plan">{plan_html(plan)}
      </section>

      <section class="part" id="skip">
        <h2>Skip these for the {esc(plan['exam'].lower())}</h2>
        <p>Each one either repeats a page above or teaches material that doesn't match the slides.</p>
        <div class="skips">{skip_html(plan)}
        </div>
      </section>

      <section class="part" id="later">
        <h2>Not on this exam</h2>{later_html(plan)}
      </section>

      <p class="foot">{esc(plan['course'])} · {esc(plan['title'])} · checked against the course slides</p>
    </main>
{script}
  </body>
</html>
"""


def main():
    if len(sys.argv) != 2:
        sys.exit("usage: build_study_plan.py scripts/study_plans/<plan>.json")
    plan = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    for item in plan["items"]:
        if item["tier"] not in TIER_ORDER:
            sys.exit(f"unknown tier {item['tier']!r} for {item['title']}")
        for ch in item["chapters"]:
            if ch not in plan["chapters"]:
                sys.exit(f"unknown chapter {ch!r} for {item['title']}")
    for entry in plan["skip"]:
        if not entry.get("why"):
            sys.exit(f"skip entry {entry['title']!r} needs a reason")
    out = ROOT / plan["out_dir"] / f"{plan['slug']}.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(page(plan), encoding="utf-8")
    print(f"[ok] {out.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
