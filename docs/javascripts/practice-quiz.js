/* Practice quiz engine (SE423 chapter quizzes, built by scripts/build_se423_quizzes.py).

   Reads the quiz from <script type="application/json" id="quiz-data"> and renders every
   question type: multiple choice, true/false, matching, ordering, calculation, scenario
   (a case with its own sub-questions) and short answer.

   Fairness rules the page enforces:
   - correct answers are spread evenly over A–D across the whole quiz (the extra slot, when
     the count isn't a multiple of 4, varies by quiz), and wrong options are ordered by the
     question text, so the letter and position never give the answer away;
   - a short answer is graded only on the points its question asks for, and any point the
     keyword check missed can be claimed with "I covered this" after reading the model answer. */
(function () {
  "use strict";
  var dataEl = document.getElementById("quiz-data");
  if (!dataEl) return;
  var QUIZ = JSON.parse(dataEl.textContent);
  var root = document.getElementById("pq-root");
  var LET = "ABCDEFGH";

  /* ---------------------------------------------------------- helpers */
  function hashStr(s) {
    var h = 0;
    for (var i = 0; i < s.length; i++) h = (h * 31 + s.charCodeAt(i)) >>> 0;
    return h;
  }
  function rng(seed) {
    return function () {
      seed = (seed + 0x6d2b79f5) >>> 0;
      var r = Math.imul(seed ^ (seed >>> 15), 1 | seed);
      r = (r + Math.imul(r ^ (r >>> 7), 61 | r)) ^ r;
      return ((r ^ (r >>> 14)) >>> 0) / 4294967296;
    };
  }
  function shuffle(a, rand) {
    a = a.slice();
    for (var j = a.length - 1; j > 0; j--) {
      var k = Math.floor(rand() * (j + 1)),
        t = a[j];
      a[j] = a[k];
      a[k] = t;
    }
    return a;
  }
  function esc(s) {
    return String(s).replace(/[&<>"]/g, function (c) {
      return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c];
    });
  }
  function el(tag, cls, html) {
    var n = document.createElement(tag);
    if (cls) n.className = cls;
    if (html != null) n.innerHTML = html;
    return n;
  }
  function norm(s) {
    return (" " + String(s).toLowerCase() + " ")
      .replace(/[’‘`]/g, "'")
      .replace(/[–—−]/g, "-")
      .replace(/×/g, "x")
      .replace(/÷/g, "/")
      .replace(/\s+/g, " ");
  }
  function evalNumber(text) {
    var t = String(text || "")
      .replace(/,/g, "")
      .replace(/[×xX]/g, "*")
      .replace(/÷/g, "/")
      .replace(/−/g, "-")
      .replace(/\^/g, "**")
      .replace(/%\s*$/, "")
      .replace(/[a-zA-Z\s-]+$/g, "")
      .replace(/^[a-zA-Z\s]+=\s*/, "")
      .trim();
    if (!t || !/^[0-9.+\-*/() ]+$/.test(t)) return NaN;
    try {
      var v = Function('"use strict";return (' + t + ")")();
      return typeof v === "number" && isFinite(v) ? v : NaN;
    } catch (e) {
      return NaN;
    }
  }
  function fmt(x) {
    return Math.round(x * 100) / 100;
  }

  /* --------------------------------------------- theme, timer, numbering */
  var body = document.body;
  var themeBtn = document.getElementById("themeToggle");
  var THEME_KEY = "shoug-quiz-theme";
  function applyTheme(t) {
    body.setAttribute("data-theme", t);
    if (themeBtn) themeBtn.textContent = t === "dark" ? "☀️" : "🌙";
    try {
      localStorage.setItem(THEME_KEY, t);
    } catch (e) {}
  }
  var saved = "dark";
  try {
    saved = localStorage.getItem(THEME_KEY) || "dark";
  } catch (e) {}
  applyTheme(saved);
  if (themeBtn)
    themeBtn.addEventListener("click", function () {
      applyTheme(body.getAttribute("data-theme") === "dark" ? "light" : "dark");
    });

  var timerEl = document.getElementById("timer");
  var remaining = (QUIZ.minutes || 25) * 60;
  var submitted = false;
  function fmtTime(s) {
    return String(Math.floor(s / 60)).padStart(2, "0") + ":" + String(s % 60).padStart(2, "0");
  }
  if (timerEl) {
    timerEl.textContent = fmtTime(remaining);
    var timer = setInterval(function () {
      if (submitted) return clearInterval(timer);
      remaining--;
      timerEl.textContent = fmtTime(Math.max(0, remaining));
      if (remaining <= 180) timerEl.classList.add("warn");
      if (remaining <= 0) {
        clearInterval(timer);
        grade(true);
      }
    }, 1000);
  }

  /* ---------------------------------------------- balanced MCQ letters */
  // Every multiple-choice question in render order, including scenario parts.
  var mcqList = [];
  QUIZ.sections.forEach(function (s) {
    s.items.forEach(function (it) {
      if (it.type === "mcq") mcqList.push(it);
      if (it.type === "scenario")
        it.parts.forEach(function (p) {
          if (p.type === "mcq") mcqList.push(p);
        });
    });
  });
  var off = hashStr(QUIZ.id) % 4;
  var slots = shuffle(
    mcqList.map(function (_, i) {
      return (i + off) % 4;
    }),
    rng(hashStr(QUIZ.id + "|slots")),
  );
  mcqList.forEach(function (it, i) {
    // source convention: options[0] is the correct answer
    var n = it.options.length,
      target = slots[i] % n;
    var wrong = shuffle(
      it.options.slice(1).map(function (o, k) {
        return { t: o, w: (it.wrong || [])[k] || "" };
      }),
      rng(hashStr(it.q)),
    );
    wrong.splice(target, 0, { t: it.options[0], w: "", right: true });
    it._opts = wrong;
    it._correct = target;
  });

  /* ------------------------------------------------------------ render */
  var graders = [];
  var qn = 0;
  var maxTotal = 0;
  var bySection = [];

  function header(card, label, pts, tag) {
    var h = el("div", "mcq-prompt");
    h.innerHTML =
      '<span class="num">' + label + "</span>" + "<span class=\"pq-pts\">" + pts + (pts === 1 ? " pt" : " pts") + "</span>" + (tag ? '<span class="tag">' + esc(tag) + "</span>" : "");
    card.appendChild(h);
  }
  function feedback(card) {
    var f = el("div", "feedback-line");
    card.appendChild(f);
    return f;
  }
  function showFeedback(f, ok, html) {
    f.className = "feedback-line show " + (ok === true ? "correct" : ok === false ? "incorrect" : "partial");
    f.innerHTML = html;
  }
  function mark(card, ok) {
    card.classList.remove("pq-right", "pq-wrong", "pq-part");
    card.classList.add(ok === true ? "pq-right" : ok === false ? "pq-wrong" : "pq-part");
  }

  function renderMcq(it, label, host) {
    var card = el("div", "mcq pq-item");
    header(card, label, 1, it.tag);
    card.appendChild(el("div", "pq-q", esc(it.q)));
    var name = "q" + qn + "-" + label.replace(/\W/g, "");
    var opts = el("div", "options");
    it._opts.forEach(function (o, k) {
      var lab = el("label", "option");
      lab.innerHTML = '<input type="radio" name="' + name + '" value="' + k + '"><span class="pq-letter">' + LET[k] + ")</span> <span>" + esc(o.t) + "</span>";
      opts.appendChild(lab);
    });
    card.appendChild(opts);
    var fb = feedback(card);
    host.appendChild(card);
    return {
      max: 1,
      grade: function () {
        var picked = card.querySelector("input:checked");
        var p = picked ? +picked.value : -1;
        var labs = opts.querySelectorAll(".option");
        labs.forEach(function (l, k) {
          l.querySelector("input").disabled = true;
          if (k === it._correct) l.classList.add("correct-mark");
          else if (k === p) l.classList.add("wrong-mark", "wrong");
        });
        var ok = p === it._correct;
        mark(card, ok);
        var why = esc(it.why || "");
        if (!ok && p >= 0 && it._opts[p].w) why = "<b>Why not " + LET[p] + ":</b> " + esc(it._opts[p].w) + "<br>" + why;
        showFeedback(fb, ok, (ok ? "<b>Correct.</b> " : "<b>Answer: " + LET[it._correct] + ") " + esc(it._opts[it._correct].t) + ".</b> ") + why);
        return ok ? 1 : 0;
      },
    };
  }

  function renderTf(it, label, host) {
    var card = el("div", "mcq pq-item pq-tf");
    header(card, label, 1, it.tag);
    card.appendChild(el("div", "pq-q", esc(it.q)));
    var name = "q" + qn + "-" + label.replace(/\W/g, "");
    var opts = el("div", "options pq-tf-opts");
    ["True", "False"].forEach(function (t) {
      var lab = el("label", "option");
      lab.innerHTML = '<input type="radio" name="' + name + '" value="' + t + '"><span>' + t + "</span>";
      opts.appendChild(lab);
    });
    card.appendChild(opts);
    var fb = feedback(card);
    host.appendChild(card);
    return {
      max: 1,
      grade: function () {
        var picked = card.querySelector("input:checked");
        var want = it.a ? "True" : "False";
        opts.querySelectorAll(".option").forEach(function (l) {
          var v = l.querySelector("input").value;
          l.querySelector("input").disabled = true;
          if (v === want) l.classList.add("correct-mark");
          else if (picked && picked.value === v) l.classList.add("wrong-mark", "wrong");
        });
        var ok = !!picked && picked.value === want;
        mark(card, ok);
        showFeedback(fb, ok, (ok ? "<b>Correct.</b> " : "<b>It's " + want.toLowerCase() + ".</b> ") + esc(it.why || ""));
        return ok ? 1 : 0;
      },
    };
  }

  function renderMatch(it, label, host) {
    var pairs = it.pairs;
    var each = it.each || 0.5;
    var max = pairs.length * each;
    var card = el("div", "mcq pq-item pq-match");
    header(card, label, max, it.tag);
    card.appendChild(el("div", "pq-q", esc(it.q)));
    var choices = shuffle(
      pairs.map(function (p) {
        return p[1];
      }).concat(it.extra || []),
      rng(hashStr(it.q + "|m")),
    );
    var grid = el("div", "pq-match-grid");
    var rows = pairs.map(function (p, i) {
      var row = el("div", "pq-match-row");
      row.appendChild(el("div", "pq-match-left", esc(p[0])));
      var sel = el("select", "pq-select");
      sel.setAttribute("aria-label", "Match for " + p[0]);
      sel.innerHTML = '<option value="">Choose…</option>' + choices.map(function (c) {
        return "<option>" + esc(c) + "</option>";
      }).join("");
      row.appendChild(sel);
      var note = el("div", "pq-match-note");
      row.appendChild(note);
      grid.appendChild(row);
      return { sel: sel, row: row, note: note, want: p[1] };
    });
    card.appendChild(grid);
    if (it.extra && it.extra.length) card.appendChild(el("div", "pq-hint", "One option on the right is not used."));
    var fb = feedback(card);
    host.appendChild(card);
    return {
      max: max,
      grade: function () {
        var right = 0;
        rows.forEach(function (r) {
          r.sel.disabled = true;
          var ok = r.sel.value === r.want;
          if (ok) right++;
          r.row.classList.add(ok ? "correct-mark" : "wrong-mark");
          r.note.textContent = ok ? "✓" : "✗ " + r.want;
        });
        var got = right * each;
        mark(card, right === rows.length ? true : right === 0 ? false : null);
        showFeedback(fb, right === rows.length ? true : right === 0 ? false : null, "<b>" + right + " of " + rows.length + " matched.</b> " + esc(it.why || ""));
        return got;
      },
    };
  }

  function renderOrder(it, label, host) {
    var items = it.items;
    var max = it.pts || 2;
    var card = el("div", "mcq pq-item pq-order");
    header(card, label, max, it.tag);
    card.appendChild(el("div", "pq-q", esc(it.q)));
    var shown = shuffle(items, rng(hashStr(it.q + "|o")));
    if (shown.join("|") === items.join("|")) shown.push(shown.shift());
    var list = el("div", "pq-order-list");
    var rows = shown.map(function (text) {
      var row = el("div", "pq-order-row");
      var sel = el("select", "pq-select pq-pos");
      sel.setAttribute("aria-label", "Position of " + text);
      sel.innerHTML = '<option value="">#</option>' + items.map(function (_, i) {
        return "<option>" + (i + 1) + "</option>";
      }).join("");
      row.appendChild(sel);
      row.appendChild(el("div", "pq-order-text", esc(text)));
      var note = el("div", "pq-match-note");
      row.appendChild(note);
      list.appendChild(row);
      return { sel: sel, row: row, note: note, want: items.indexOf(text) + 1 };
    });
    card.appendChild(list);
    card.appendChild(el("div", "pq-hint", "Number the steps 1 to " + items.length + "."));
    var fb = feedback(card);
    host.appendChild(card);
    return {
      max: max,
      grade: function () {
        var right = 0;
        rows.forEach(function (r) {
          r.sel.disabled = true;
          var ok = +r.sel.value === r.want;
          if (ok) right++;
          r.row.classList.add(ok ? "correct-mark" : "wrong-mark");
          r.note.textContent = ok ? "✓" : "✗ " + r.want;
        });
        var got = Math.round((max * right) / rows.length * 2) / 2;
        mark(card, right === rows.length ? true : right === 0 ? false : null);
        showFeedback(fb, right === rows.length ? true : right === 0 ? false : null, "<b>Correct order:</b> " + items.map(esc).join(" → ") + (it.why ? "<br>" + esc(it.why) : ""));
        return got;
      },
    };
  }

  function renderNum(it, label, host) {
    var max = it.pts || 1;
    var card = el("div", "mcq pq-item pq-num");
    header(card, label, max, it.tag);
    card.appendChild(el("div", "pq-q", esc(it.q)));
    var row = el("div", "pq-num-row");
    var input = el("input", "pq-input");
    input.type = "text";
    input.setAttribute("inputmode", "decimal");
    input.setAttribute("autocomplete", "off");
    input.setAttribute("aria-label", "Your answer");
    row.appendChild(input);
    if (it.unit) row.appendChild(el("span", "pq-unit", esc(it.unit)));
    card.appendChild(row);
    card.appendChild(el("div", "pq-hint", "A number or the calculation itself (like 100/10). Small rounding differences are accepted."));
    var fb = feedback(card);
    host.appendChild(card);
    return {
      max: max,
      grade: function () {
        input.disabled = true;
        var v = evalNumber(input.value);
        var tol = it.tol != null ? it.tol : Math.abs(it.answer) * 0.03;
        var ok = !isNaN(v) && Math.abs(v - it.answer) <= tol + 1e-9;
        input.classList.add(ok ? "correct-mark" : "wrong-mark");
        mark(card, ok);
        showFeedback(fb, ok, (ok ? "<b>Correct.</b> " : "<b>Answer: " + fmt(it.answer) + (it.unit ? " " + esc(it.unit) : "") + ".</b> ") + (it.work ? esc(it.work) : ""));
        return ok ? max : 0;
      },
    };
  }

  function renderShort(it, label, host) {
    var rubric = it.rubric;
    // need: how many of the rubric points earn full marks ("name any three of ...")
    var need = Math.min(it.need || rubric.length, rubric.length);
    var max = it.pts || need;
    var card = el("div", "written pq-item");
    card.appendChild(el("div", "written-topic", esc(label) + (it.tag ? " · " + esc(it.tag) : "") + " · " + max + (max === 1 ? " pt" : " pts")));
    card.appendChild(el("div", "written-label", esc(it.q)));
    var ta = el("textarea");
    ta.placeholder = "Your answer…";
    ta.rows = it.rows || 3;
    card.appendChild(ta);
    var status = el("div", "keyword-status");
    card.appendChild(status);
    var key = el("div", "answer-key", '<div class="key-label">Model answer</div>' + esc(it.model));
    card.appendChild(key);
    host.appendChild(card);
    var state = { hits: [], claimed: [] };
    var api = {
      max: max,
      grade: function () {
        ta.disabled = true;
        var text = norm(ta.value);
        state.hits = rubric.map(function (r) {
          return r[1].some(function (k) {
            return text.indexOf(norm(k).trim()) >= 0;
          });
        });
        state.claimed = rubric.map(function () {
          return false;
        });
        paint();
        key.classList.add("show");
        return api.score();
      },
      score: function () {
        var n = 0;
        rubric.forEach(function (_, i) {
          if (state.hits[i] || state.claimed[i]) n++;
        });
        return Math.round((max * Math.min(n, need)) / need * 2) / 2;
      },
    };
    function paint() {
      var got = api.score();
      var n = state.hits.filter(Boolean).length + state.claimed.filter(Boolean).length;
      status.innerHTML = "";
      status.appendChild(el("div", "pq-sa-sum", (need < rubric.length ? "Gave " + Math.min(n, need) + " of the " + need + " needed" : "Covered " + n + " of " + rubric.length + " points") + " → " + got + " / " + max + " pts."));
      var chips = el("div", "pq-chips");
      var enough = n >= need;
      rubric.forEach(function (r, i) {
        if (!state.hits[i] && !state.claimed[i] && enough) {
          chips.appendChild(el("span", "kw-chip pq-other", esc(r[0])));
          return;
        }
        if (state.hits[i]) chips.appendChild(el("span", "kw-chip hit", "✓ " + esc(r[0])));
        else if (state.claimed[i]) {
          var c = el("button", "kw-chip hit pq-claimed", "✓ " + esc(r[0]) + " (you marked)");
          c.type = "button";
          c.title = "Undo";
          c.addEventListener("click", function () {
            state.claimed[i] = false;
            paint();
            total();
          });
          chips.appendChild(c);
        } else {
          var b = el("button", "kw-chip miss pq-claim", esc(r[0]) + " · I covered this");
          b.type = "button";
          b.title = "The check looks for key words. If your answer made this point in other words, claim it.";
          b.addEventListener("click", function () {
            state.claimed[i] = true;
            paint();
            total();
          });
          chips.appendChild(b);
        }
      });
      status.appendChild(chips);
      status.classList.add("show");
      mark(card, n >= need ? true : n === 0 ? false : null);
    }
    return api;
  }

  function renderScenario(it, label, host) {
    var card = el("div", "pq-scenario");
    card.appendChild(el("div", "pq-case-label", esc(label) + " · Scenario" + (it.tag ? " · " + esc(it.tag) : "")));
    if (it.title) card.appendChild(el("div", "pq-case-title", esc(it.title)));
    card.appendChild(el("div", "pq-case-text", esc(it.text).replace(/\n/g, "<br>")));
    host.appendChild(card);
    var parts = el("div", "pq-case-parts");
    card.appendChild(parts);
    var gs = it.parts.map(function (p, i) {
      return renderAny(p, label + LET[i].toLowerCase(), parts);
    });
    var max = gs.reduce(function (s, g) {
      return s + g.max;
    }, 0);
    return {
      max: max,
      parts: gs,
      grade: function () {
        return gs.reduce(function (s, g) {
          return s + g.grade();
        }, 0);
      },
      score: function () {
        return gs.reduce(function (s, g) {
          return s + (g._last || 0);
        }, 0);
      },
    };
  }

  function renderAny(it, label, host) {
    var g =
      it.type === "mcq"
        ? renderMcq(it, label, host)
        : it.type === "tf"
          ? renderTf(it, label, host)
          : it.type === "match"
            ? renderMatch(it, label, host)
            : it.type === "order"
              ? renderOrder(it, label, host)
              : it.type === "num"
                ? renderNum(it, label, host)
                : it.type === "short"
                  ? renderShort(it, label, host)
                  : renderScenario(it, label, host);
    var inner = g.grade;
    g.grade = function () {
      g._last = inner();
      return g._last;
    };
    return g;
  }

  QUIZ.sections.forEach(function (s) {
    var block = el("div", "question-block");
    var head = el("div", "q-head");
    var h = el("h2", null, esc(s.title));
    var pts = el("span", "q-points");
    head.appendChild(h);
    head.appendChild(pts);
    block.appendChild(head);
    if (s.note) block.appendChild(el("p", "pq-section-note", esc(s.note)));
    var gs = [];
    s.items.forEach(function (it) {
      qn++;
      var g = renderAny(it, "Q" + qn, block);
      gs.push(g);
      graders.push(g);
    });
    var smax = gs.reduce(function (a, g) {
      return a + g.max;
    }, 0);
    maxTotal += smax;
    pts.textContent = smax + " points";
    bySection.push({ title: s.short || s.title, gs: gs, max: smax });
    root.appendChild(block);
  });

  /* ------------------------------------------------------------- grade */
  var submitBtn = document.getElementById("submitBtn");
  var resetBtn = document.getElementById("resetBtn");
  var panel = document.getElementById("scorePanel");
  var big = document.getElementById("bigScore");
  var sub = document.getElementById("scoreSub");
  var breakdown = document.getElementById("scoreBreakdown");
  document.querySelectorAll("[data-total]").forEach(function (n) {
    n.textContent = maxTotal;
  });

  function current(g) {
    if (g.parts)
      return g.parts.reduce(function (s, p) {
        return s + current(p);
      }, 0);
    return g.score ? g.score() : g._last || 0;
  }
  function total() {
    if (!submitted) return;
    var sum = 0;
    breakdown.innerHTML = "";
    bySection.forEach(function (s) {
      var got = s.gs.reduce(function (a, g) {
        return a + current(g);
      }, 0);
      sum += got;
      breakdown.appendChild(el("span", null, "<b>" + fmt(got) + "/" + s.max + "</b>" + esc(s.title)));
    });
    big.textContent = fmt(sum) + " / " + maxTotal;
    var pct = sum / maxTotal;
    sub.textContent =
      (pct >= 0.85 ? "Excellent. " : pct >= 0.65 ? "Good, review the misses. " : "Worth another pass through the slides. ") +
      "Every question now shows the answer and why. For short answers, read the model answer and use “I covered this” for any point you made in other words.";
  }
  function grade(auto) {
    if (submitted) return;
    submitted = true;
    graders.forEach(function (g) {
      g.grade();
    });
    total();
    if (auto) sub.textContent = "Time is up, so the quiz was submitted. " + sub.textContent;
    panel.classList.add("show");
    submitBtn.disabled = true;
    resetBtn.style.display = "inline-block";
    panel.scrollIntoView({ behavior: "smooth", block: "center" });
  }
  submitBtn.addEventListener("click", function () {
    grade(false);
  });
  resetBtn.addEventListener("click", function () {
    location.reload();
  });
})();
