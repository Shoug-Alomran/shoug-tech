/* CS223 interactive exams: answer checking, solutions, scoring, timer.
   Markup comes from scripts/build_cs223_course.py; styles from /styles/cs223-exam.css.

   Each .ex-part carries data-pts and data-kind:
     mcq     one radio group; data-answer is the 0-based index of the right option
     fields  inputs with data-answer ("3/8", "1,-2,2"); optional data-mode:
               "parallel"  a vector that may be any nonzero multiple of the answer
               "set"       a list whose order does not matter
     written no auto-check: reveal the worked solution, then mark yourself
   Answers accept fractions, decimals, sqrt(..)/√, pi, and ^ for powers. */
(function () {
  "use strict";

  var root = document.querySelector("[data-cs223-exam]");
  if (!root) return;
  var examId = root.getAttribute("data-cs223-exam");
  var STORE = "cs223-exam:" + examId;
  var parts = Array.prototype.slice.call(root.querySelectorAll(".ex-part"));

  /* ---------------- math rendering ---------------- */
  function renderMath(el) {
    if (typeof window.renderMathInElement !== "function") return;
    window.renderMathInElement(el, {
      delimiters: [
        { left: "$$", right: "$$", display: true },
        { left: "\\[", right: "\\]", display: true },
        { left: "$", right: "$", display: false },
      ],
      throwOnError: false,
    });
  }
  if (typeof window.renderMathInElement === "function") renderMath(root);
  else
    window.addEventListener("load", function () {
      renderMath(root);
    });

  /* ---------------- expression parser ---------------- */
  function evaluate(src) {
    var s = String(src)
      .toLowerCase()
      .replace(/[−–]/g, "-")
      .replace(/×|·/g, "*")
      .replace(/÷/g, "/")
      .replace(/√/g, "sqrt")
      .replace(/π/g, "pi")
      .replace(/\s+/g, "");
    var i = 0;
    function peek() {
      return s[i];
    }
    function eat(c) {
      if (s[i] === c) {
        i++;
        return true;
      }
      return false;
    }
    function expr() {
      var v = term();
      for (;;) {
        if (eat("+")) v += term();
        else if (eat("-")) v -= term();
        else return v;
      }
    }
    function term() {
      var v = factor();
      for (;;) {
        if (eat("*")) v *= factor();
        else if (eat("/")) v /= factor();
        else if (peek() === "(" || peek() === "s" || peek() === "p")
          v *= factor();
        else return v;
      }
    }
    function factor() {
      if (eat("-")) return -factor();
      if (eat("+")) return factor();
      var v = power();
      return v;
    }
    function power() {
      var b = atom();
      if (eat("^")) return Math.pow(b, factor());
      return b;
    }
    function atom() {
      if (eat("(")) {
        var v = expr();
        if (!eat(")")) throw new Error("bracket");
        return v;
      }
      if (s.substr(i, 4) === "sqrt") {
        i += 4;
        if (peek() === "(") return Math.sqrt(atom());
        return Math.sqrt(power());
      }
      if (s.substr(i, 2) === "pi") {
        i += 2;
        return Math.PI;
      }
      var m = /^(\d+\.?\d*|\.\d+)(e[+-]?\d+)?/.exec(s.slice(i));
      if (!m) throw new Error("number");
      i += m[0].length;
      return parseFloat(m[0]);
    }
    if (!s) throw new Error("empty");
    var out = expr();
    if (i !== s.length || !isFinite(out)) throw new Error("trailing");
    return out;
  }

  /* "1, -2, 2", "[1 -2 2]" and "(1;-2;2)" all read as a list. Spaces only
     separate items when there are no commas, so "- 7/16" stays one value. */
  function splitList(src, expected) {
    var s = String(src)
      .replace(/[\[\]{}<>]/g, " ")
      .trim();
    if (/^\(.*\)$/.test(s) && /[,;]/.test(s)) s = s.slice(1, -1);
    if (expected === 1) return s ? [s] : [];
    var items = /[,;]/.test(s) ? s.split(/[,;]/) : s.split(/\s+/);
    return items.filter(function (t) {
      return t.trim() !== "";
    });
  }

  function close(a, b) {
    return Math.abs(a - b) <= 2e-3 * Math.max(1, Math.abs(b));
  }

  function matches(input, answer, mode) {
    var want = splitList(answer).map(evaluate);
    var got = splitList(input, want.length).map(evaluate);
    if (got.length !== want.length) return false;
    if (mode === "set") {
      want.sort(function (x, y) {
        return x - y;
      });
      got.sort(function (x, y) {
        return x - y;
      });
    }
    if (mode === "parallel") {
      var k = null;
      for (var j = 0; j < want.length; j++) {
        if (Math.abs(want[j]) < 1e-12) {
          if (Math.abs(got[j]) > 1e-6) return false;
          continue;
        }
        var r = got[j] / want[j];
        if (k === null) k = r;
        else if (!close(r, k)) return false;
      }
      return k !== null && Math.abs(k) > 1e-9;
    }
    for (var n = 0; n < want.length; n++)
      if (!close(got[n], want[n])) return false;
    return true;
  }

  /* ---------------- per-part state ---------------- */
  var state = {}; // id -> { earned, done }
  function partId(p) {
    return p.getAttribute("data-part");
  }
  function pts(p) {
    return parseFloat(p.getAttribute("data-pts")) || 0;
  }

  function setFeedback(p, cls, text) {
    var fb = p.querySelector(".ex-feedback");
    if (!fb) return;
    fb.className = "ex-feedback" + (cls ? " " + cls : "");
    fb.textContent = text;
  }

  function settle(p, earned) {
    var full = pts(p);
    state[partId(p)] = { earned: earned, done: true };
    var ratio = full ? earned / full : 0;
    p.setAttribute(
      "data-state",
      ratio >= 0.999 ? "correct" : ratio > 0 ? "partial" : "wrong",
    );
    update();
  }

  function checkPart(p) {
    var kind = p.getAttribute("data-kind");
    if (kind === "mcq") {
      var right = parseInt(p.getAttribute("data-answer"), 10);
      var picked = p.querySelector("input[type=radio]:checked");
      if (!picked) {
        setFeedback(p, "is-partial", "Pick an option first.");
        return;
      }
      var opts = p.querySelectorAll(".ex-option");
      Array.prototype.forEach.call(opts, function (o, idx) {
        o.classList.toggle("is-right", idx === right);
        o.classList.toggle("is-wrong", o.contains(picked) && idx !== right);
      });
      var ok = parseInt(picked.value, 10) === right;
      setFeedback(
        p,
        ok ? "is-right" : "is-wrong",
        ok ? "✓ Correct" : "✗ Not quite. The right option is highlighted.",
      );
      settle(p, ok ? pts(p) : 0);
      return;
    }
    if (kind === "fields") {
      var inputs = Array.prototype.slice.call(p.querySelectorAll(".ex-input"));
      var blank = inputs.filter(function (el) {
        return !el.value.trim();
      });
      if (blank.length === inputs.length) {
        setFeedback(p, "is-partial", "Enter an answer first.");
        return;
      }
      var good = 0;
      inputs.forEach(function (el) {
        var ok = false;
        try {
          ok =
            el.value.trim() !== "" &&
            el
              .getAttribute("data-answer")
              .split("|")
              .some(function (alt) {
                return matches(el.value, alt, el.getAttribute("data-mode"));
              });
        } catch (e) {
          ok = false;
        }
        el.classList.toggle("is-right", ok);
        el.classList.toggle("is-wrong", !ok);
        if (ok) good++;
      });
      var earned = (pts(p) * good) / inputs.length;
      if (good === inputs.length)
        setFeedback(p, "is-right", "✓ All " + good + " correct");
      else if (good)
        setFeedback(
          p,
          "is-partial",
          "~ " + good + " of " + inputs.length + " correct",
        );
      else
        setFeedback(
          p,
          "is-wrong",
          "✗ Not quite. Open the solution to see where it goes.",
        );
      settle(p, Math.round(earned * 100) / 100);
    }
  }

  function reveal(p, open) {
    var sol = p.querySelector(".ex-solution");
    var btn = p.querySelector("[data-act=reveal]");
    if (!sol) return;
    var show = open === undefined ? sol.hidden : open;
    sol.hidden = !show;
    if (btn) btn.textContent = show ? "Hide solution" : "Show solution";
    if (show && !sol.getAttribute("data-rendered")) {
      renderMath(sol);
      sol.setAttribute("data-rendered", "1");
    }
  }

  function selfMark(p, value, btn) {
    Array.prototype.forEach.call(
      p.querySelectorAll("[data-mark]"),
      function (b) {
        b.classList.toggle("is-on", b === btn);
      },
    );
    settle(p, Math.round(pts(p) * value * 100) / 100);
    save();
  }

  /* ---------------- totals ---------------- */
  var total = parts.reduce(function (sum, p) {
    return sum + pts(p);
  }, 0);
  function fmt(n) {
    return (Math.round(n * 100) / 100).toString();
  }

  function update() {
    var done = 0,
      earned = 0;
    parts.forEach(function (p) {
      var st = state[partId(p)];
      if (st && st.done) {
        done++;
        earned += st.earned;
      }
    });
    var bar = root.querySelector(".ex-progress-fill");
    if (bar)
      bar.style.width = (parts.length ? (done / parts.length) * 100 : 0) + "%";
    var label = root.querySelector(".ex-progress-label");
    if (label)
      label.textContent = done + " / " + parts.length + " parts marked";
    var score = root.querySelector("[data-score]");
    if (score) score.textContent = fmt(earned) + " / " + fmt(total);
    var res = root.querySelector(".ex-result");
    if (res) {
      res.hidden = done !== parts.length;
      var pct = total ? Math.round((earned / total) * 100) : 0;
      var big = res.querySelector("[data-result-score]");
      if (big)
        big.textContent = fmt(earned) + " / " + fmt(total) + " (" + pct + "%)";
    }
  }

  /* ---------------- saved answers (per viewer, best effort) ---------------- */
  function save() {
    try {
      var data = { inputs: {}, picks: {}, marks: {} };
      parts.forEach(function (p) {
        var id = partId(p);
        Array.prototype.forEach.call(
          p.querySelectorAll(".ex-input"),
          function (el, k) {
            if (el.value) data.inputs[id + ":" + k] = el.value;
          },
        );
        var picked = p.querySelector("input[type=radio]:checked");
        if (picked) data.picks[id] = picked.value;
        var mark = p.querySelector("[data-mark].is-on");
        if (mark) data.marks[id] = mark.getAttribute("data-mark");
      });
      localStorage.setItem(STORE, JSON.stringify(data));
    } catch (e) {}
  }

  function restore() {
    var data;
    try {
      data = JSON.parse(localStorage.getItem(STORE) || "null");
    } catch (e) {
      data = null;
    }
    if (!data) return;
    parts.forEach(function (p) {
      var id = partId(p);
      Array.prototype.forEach.call(
        p.querySelectorAll(".ex-input"),
        function (el, k) {
          var v = data.inputs && data.inputs[id + ":" + k];
          if (v) el.value = v;
        },
      );
      if (data.picks && data.picks[id] !== undefined) {
        var r = p.querySelector(
          'input[type=radio][value="' + data.picks[id] + '"]',
        );
        if (r) {
          r.checked = true;
          markPicked(p);
        }
      }
      if (data.marks && data.marks[id] !== undefined) {
        var b = p.querySelector('[data-mark="' + data.marks[id] + '"]');
        if (b) {
          reveal(p, true);
          selfMark(p, parseFloat(data.marks[id]), b);
        }
      }
    });
  }

  function markPicked(p) {
    Array.prototype.forEach.call(
      p.querySelectorAll(".ex-option"),
      function (o) {
        o.classList.toggle("is-picked", !!o.querySelector("input:checked"));
      },
    );
  }

  /* ---------------- timer ---------------- */
  var minutes = parseFloat(root.getAttribute("data-duration")) || 0;
  var elapsed = 0,
    ticking = null;
  var timerOut = root.querySelector("[data-timer]");
  var timerBtn = root.querySelector("[data-act=timer]");
  function two(n) {
    return (n < 10 ? "0" : "") + n;
  }
  function paintTimer() {
    if (!timerOut) return;
    var left = minutes ? minutes * 60 - elapsed : elapsed;
    var neg = left < 0;
    left = Math.abs(left);
    timerOut.textContent =
      (neg ? "+" : "") + two(Math.floor(left / 60)) + ":" + two(left % 60);
    timerOut.parentNode.classList.toggle("is-over", neg);
  }
  function toggleTimer() {
    if (ticking) {
      clearInterval(ticking);
      ticking = null;
      timerBtn.textContent = "Resume timer";
    } else {
      ticking = setInterval(function () {
        elapsed++;
        paintTimer();
      }, 1000);
      timerBtn.textContent = "Pause timer";
    }
  }
  paintTimer();

  /* ---------------- wiring ---------------- */
  root.addEventListener("click", function (e) {
    var t = e.target.closest("[data-act], [data-mark]");
    if (!t) return;
    var p = t.closest(".ex-part");
    var act = t.getAttribute("data-act");
    if (t.hasAttribute("data-mark") && p)
      return selfMark(p, parseFloat(t.getAttribute("data-mark")), t);
    if (act === "check" && p) {
      checkPart(p);
      save();
    } else if (act === "reveal" && p) reveal(p);
    else if (act === "timer") toggleTimer();
    else if (act === "reveal-all") {
      var anyHidden = parts.some(function (q) {
        var s = q.querySelector(".ex-solution");
        return s && s.hidden;
      });
      parts.forEach(function (q) {
        reveal(q, anyHidden);
      });
      t.textContent = anyHidden ? "Hide all solutions" : "Show all solutions";
    } else if (act === "check-all") {
      parts.forEach(function (q) {
        if (q.getAttribute("data-kind") !== "written") checkPart(q);
      });
      save();
    } else if (act === "reset") {
      if (!window.confirm("Clear every answer and mark on this exam?")) return;
      try {
        localStorage.removeItem(STORE);
      } catch (err) {}
      window.location.reload();
    }
  });

  root.addEventListener("change", function (e) {
    var p = e.target.closest(".ex-part");
    if (p && e.target.type === "radio") markPicked(p);
    save();
  });
  root.addEventListener("keydown", function (e) {
    if (e.key === "Enter" && e.target.classList.contains("ex-input")) {
      e.preventDefault();
      checkPart(e.target.closest(".ex-part"));
      save();
    }
  });

  restore();
  update();
})();
