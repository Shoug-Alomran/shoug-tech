/* SE423 mock midterm engine: renders window.MOCK, grades strictly on submit. */
(function () {
  "use strict";
  function hash(s) {
    var h = 2166136261;
    for (var i = 0; i < s.length; i++) {
      h ^= s.charCodeAt(i);
      h = Math.imul(h, 16777619);
    }
    return h >>> 0;
  }
  function shuffled(arr, seed) {
    var a = arr.slice();
    var s = seed || 1;
    for (var i = a.length - 1; i > 0; i--) {
      s = (Math.imul(s ^ (s >>> 15), 2246822507) + 0x9e3779b9) >>> 0;
      var j = s % (i + 1);
      var t = a[i];
      a[i] = a[j];
      a[j] = t;
    }
    return a;
  }
  function norm(s) {
    return (" " + String(s).toLowerCase() + " ")
      .replace(/&/g, " and ")
      .replace(/[’']/g, "")
      .replace(/[^a-z0-9%$]+/g, " ")
      .replace(/\s+/g, " ")
      .trim();
  }
  function lev(a, b) {
    if (Math.abs(a.length - b.length) > 2) return 9;
    var pp = [],
      prev = [],
      cur = [],
      i,
      j;
    for (j = 0; j <= b.length; j++) prev[j] = j;
    for (i = 1; i <= a.length; i++) {
      cur = [i];
      for (j = 1; j <= b.length; j++) {
        cur[j] = Math.min(prev[j] + 1, cur[j - 1] + 1, prev[j - 1] + (a[i - 1] === b[j - 1] ? 0 : 1));
        // adjacent swap ("chnage") counts as one edit
        if (i > 1 && j > 1 && a[i - 1] === b[j - 2] && a[i - 2] === b[j - 1]) cur[j] = Math.min(cur[j], pp[j - 2] + 1);
      }
      pp = prev;
      prev = cur;
    }
    return prev[b.length];
  }
  function wordHit(tokens, w) {
    for (var i = 0; i < tokens.length; i++) {
      var t = tokens[i];
      if (t === w) return true;
      if (w.length >= 4 && t.indexOf(w) === 0) return true;
      if (w.length >= 5) {
        var d = lev(t.slice(0, w.length + 1), w);
        if (d <= 1 || (w.length >= 8 && d <= 2)) return true;
        if (lev(t, w) <= 1) return true;
      }
    }
    return false;
  }
  function keyHit(tokens, key) {
    var words = norm(key).split(" ").filter(Boolean);
    if (!words.length) return false;
    return words.every(function (w) {
      return wordHit(tokens, w);
    });
  }
  function anyHit(tokens, keys) {
    return keys.some(function (k) {
      return keyHit(tokens, k);
    });
  }
  function tokensOf(text) {
    var n = norm(text);
    return n ? n.split(" ") : [];
  }
  function esc(s) {
    return String(s).replace(/[&<>"]/g, function (c) {
      return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c];
    });
  }

  var M = window.MOCK;
  var STORE = "se423-mock-midterm-v1";
  var state = { v: {}, graded: false };
  try { state = JSON.parse(localStorage.getItem(STORE)) || state; } catch (e) {}
  function save() { try { localStorage.setItem(STORE, JSON.stringify(state)); } catch (e) {} }
  var LETTERS = ["A", "B", "C", "D"];
  var LIST_PTS = 2;
  var all = [];
  var n = 0;

  function card(id, html) {
    var el = document.createElement("article");
    el.className = "q"; el.id = id; el.innerHTML = html;
    return el;
  }
  function words(s) { return (s || "").trim().split(/\s+/).filter(Boolean).length; }

  M.mcq.forEach(function (q, i) {
    n++; var id = "a" + i;
    var order = shuffled([0, 1, 2, 3], hash(q.q) + 11);
    q.order = order;
    var html = '<div class="q-top"><span class="pts" data-pts>1 pt</span></div><p class="q-text"><span class="num">' + n + '.</span>' + esc(q.q) + '</p><div class="opts">' +
      order.map(function (o, k) {
        return '<label class="opt" data-o="' + o + '"><input type="radio" name="' + id + '" value="' + o + '"' + (state.v[id] === String(o) ? " checked" : "") + '><span class="letter">' + LETTERS[k] + '</span><span>' + esc(q.opts[o]) + "</span></label>";
      }).join("") + '</div><div class="feedback" hidden></div>';
    var el = card(id, html); document.getElementById("qa").appendChild(el);
    all.push({ type: "mcq", q: q, id: id, el: el, max: 1 });
  });
  M.tf.forEach(function (q, i) {
    n++; var id = "b" + i;
    var html = '<div class="q-top"><span class="pts" data-pts>1 pt</span></div><p class="q-text"><span class="num">' + n + '.</span>' + esc(q.q) + '</p><div class="opts tf">' +
      ["true", "false"].map(function (v) {
        return '<label class="opt" data-o="' + v + '"><input type="radio" name="' + id + '" value="' + v + '"' + (state.v[id] === v ? " checked" : "") + "><span>" + (v === "true" ? "True" : "False") + "</span></label>";
      }).join("") + '</div><div class="feedback" hidden></div>';
    var el = card(id, html); document.getElementById("qb").appendChild(el);
    all.push({ type: "tf", q: q, id: id, el: el, max: 1 });
  });
  M.list.forEach(function (q, i) {
    n++; var id = "c" + i;
    var html = '<div class="q-top"><span class="pts" data-pts>' + LIST_PTS + ' pts</span></div><p class="q-text"><span class="num">' + n + '.</span>' + esc(q.q) + '</p><textarea aria-label="Your list" placeholder="One item per line or separated by commas">' + esc(state.v[id] || "") + '</textarea><div class="feedback" hidden></div>';
    var el = card(id, html); document.getElementById("qc").appendChild(el);
    all.push({ type: "list", q: q, id: id, el: el, max: LIST_PTS });
  });
  var dTotal = 0;
  M.short.forEach(function (q, i) {
    n++; var id = "d" + i; dTotal += q.max;
    var html = '<div class="q-top"><span class="pts" data-pts>' + q.max + ' pts</span></div><p class="q-text"><span class="num">' + n + '.</span>' + esc(q.q) + '</p><textarea aria-label="Your answer" placeholder="Explain in 2–4 sentences: what, how, and why.">' + esc(state.v[id] || "") + '</textarea><div class="words" data-words></div><div class="feedback" hidden></div>';
    var el = card(id, html); document.getElementById("qd").appendChild(el);
    all.push({ type: "short", q: q, id: id, el: el, max: q.max });
  });
  document.getElementById("d-points").textContent = dTotal + " points";

  function updateWords(item) {
    var w = item.el.querySelector("[data-words]");
    if (w) w.textContent = words(item.el.querySelector("textarea").value) + " words";
  }
  all.forEach(function (item) {
    item.el.addEventListener("input", function () { capture(item); if (item.type === "short") updateWords(item); });
    item.el.addEventListener("change", function () { capture(item); });
    if (item.type === "short") updateWords(item);
  });
  function capture(item) {
    if (item.type === "mcq" || item.type === "tf") {
      var r = item.el.querySelector("input:checked"); state.v[item.id] = r ? r.value : null;
    } else state.v[item.id] = item.el.querySelector("textarea").value;
    save(); progress();
  }
  function progress() {
    var done = all.filter(function (it) { var v = state.v[it.id]; return v != null && String(v).trim() !== ""; }).length;
    if (!state.graded) document.getElementById("progress").textContent = done + " of " + all.length + " questions answered. Answers are saved in this browser.";
  }

  function pill(frac) {
    var cls = frac >= 0.999 ? "ok" : frac > 0 ? "part" : "no";
    var txt = frac >= 0.999 ? "Correct" : frac > 0 ? "Partially correct" : "Incorrect";
    return '<span class="verdict-pill ' + cls + '">' + txt + "</span>";
  }
  function grade(item) {
    var q = item.q, v = state.v[item.id], pts = 0, fb = "";
    if (item.type === "mcq") {
      var correct = String(q.a);
      item.el.querySelectorAll(".opt").forEach(function (o) {
        var val = o.getAttribute("data-o");
        o.classList.toggle("right", val === correct);
        o.classList.toggle("wrong", val === v && v !== correct);
      });
      pts = v === correct ? 1 : 0;
      var letter = LETTERS[q.order.indexOf(q.a)];
      fb = (v == null ? "<b>Not answered.</b> " : pts ? "" : "<b>Your answer is wrong.</b> ") + "Correct answer: <b>" + letter + ". " + esc(q.opts[q.a]) + "</b><div class='why'>" + esc(q.why) + "</div>" + (q.near ? "<div class='why'><b>Closest distractor:</b> " + esc(q.near) + "</div>" : "");
    } else if (item.type === "tf") {
      var c = String(q.a);
      item.el.querySelectorAll(".opt").forEach(function (o) {
        var val = o.getAttribute("data-o");
        o.classList.toggle("right", val === c);
        o.classList.toggle("wrong", val === v && v !== c);
      });
      pts = v === c ? 1 : 0;
      fb = (v == null ? "<b>Not answered.</b> " : "") + "Answer: <b>" + (q.a ? "True" : "False") + "</b><div class='why'>" + esc(q.why) + "</div>";
    } else if (item.type === "list") {
      var t = tokensOf(v || "");
      var hits = q.items.map(function (it) { return anyHit(t, it[1]); });
      var got = hits.filter(Boolean).length, need = Math.min(q.need, q.items.length);
      pts = Math.round((Math.min(got, need) / need) * item.max * 2) / 2;
      fb = got + " of " + need + " items found." + '<ul class="kwlist">' + q.items.map(function (it, k) {
        return '<li class="' + (hits[k] ? "hit" : "miss") + '">' + (hits[k] ? "✓ " : "✗ ") + esc(it[0]) + "</li>";
      }).join("") + "</ul>";
    } else {
      var tk = tokensOf(v || ""), wc = words(v);
      var gh = q.groups.map(function (g) { return anyHit(tk, g[1]); });
      var hit = gh.filter(Boolean).length;
      pts = Math.round((hit / q.groups.length) * item.max * 2) / 2;
      var brief = wc > 0 && wc < 15;
      if (brief) pts = Math.min(pts, 1);
      var miss = q.groups.filter(function (g, k) { return !gh[k]; }).map(function (g) { return g[0]; });
      fb = (wc === 0 ? "<b>Not answered.</b>" : brief ? "<b>Too brief (" + wc + " words).</b> Naming the concept is not enough: explain what to do, how, and why. Capped at 1 point." : "") +
        (miss.length ? "<div style='margin-top:6px'><b>Missing detail:</b></div><ul class='missing'>" + miss.map(function (m) { return "<li>" + esc(m) + "</li>"; }).join("") + "</ul>" : "<div>All expected points are covered.</div>") +
        "<div class='model'><b>Model answer:</b> " + esc(q.model) + "</div>";
    }
    item.pts = pts;
    item.el.classList.remove("ok", "part-ok", "no");
    item.el.classList.add(pts >= item.max ? "ok" : pts > 0 ? "part-ok" : "no");
    var top = item.el.querySelector(".q-top");
    top.querySelectorAll(".verdict-pill").forEach(function (p) { p.remove(); });
    top.insertAdjacentHTML("beforeend", pill(pts / item.max));
    item.el.querySelector("[data-pts]").textContent = pts + " / " + item.max;
    var f = item.el.querySelector(".feedback"); f.hidden = false; f.innerHTML = fb;
  }

  function results() {
    var secs = { mcq: ["Part A · MCQ", 0, 0], tf: ["Part B · True/False", 0, 0], list: ["Part C · Listing", 0, 0], short: ["Part D · Short answer", 0, 0] };
    var tot = 0, max = 0, review = {};
    all.forEach(function (it) {
      secs[it.type][1] += it.pts; secs[it.type][2] += it.max; tot += it.pts; max += it.max;
      if (it.pts < it.max) review[it.q.c] = (review[it.q.c] || 0) + (it.max - it.pts);
    });
    var r = Object.keys(review).sort(function (a, b) { return review[b] - review[a]; });
    var pct = Math.round((tot / max) * 100);
    document.getElementById("results").innerHTML =
      '<div class="score"><div><div class="big">' + tot + "<small> / " + max + '</small></div><div class="sub">' + pct + "% · " +
      (pct >= 90 ? "exam-ready" : pct >= 75 ? "close, fix the gaps below" : "review the topics below, then retake") + '</div></div><div class="bars">' +
      Object.keys(secs).map(function (k) {
        var s = secs[k], p = s[2] ? (s[1] / s[2]) * 100 : 0;
        return '<div class="bar"><div class="lbl"><span>' + s[0] + "</span><span>" + s[1] + "/" + s[2] + '</span></div><div class="track"><div class="fill" style="width:' + p.toFixed(1) + '%"></div></div></div>';
      }).join("") + "</div></div>" +
      (r.length ? '<div class="card" style="margin-bottom:14px"><h4>Concepts to review most</h4><ol class="review-list">' + r.map(function (c) { return "<li>" + esc(c) + " <span>−" + review[c] + " pts</span></li>"; }).join("") + "</ol></div>" : '<div class="card" style="margin-bottom:14px"><h4>Nothing to review: full marks.</h4></div>');
    document.getElementById("progress").textContent = "Graded: " + tot + " / " + max + " (" + pct + "%). Scroll through for explanations and model answers.";
  }

  function gradeAll() {
    all.forEach(capture); all.forEach(grade); results();
    document.getElementById("exam").classList.add("graded");
    state.graded = true; save();
  }
  document.getElementById("submit").addEventListener("click", function () {
    var blank = all.filter(function (it) { var v = state.v[it.id]; return v == null || String(v).trim() === ""; }).length;
    if (blank && !confirm(blank + " question(s) are unanswered. Submit anyway?")) return;
    gradeAll(); document.getElementById("results").scrollIntoView({ behavior: "smooth" });
  });
  document.getElementById("reset").addEventListener("click", function () {
    if (!confirm("Clear all your answers and start the exam again?")) return;
    try { localStorage.removeItem(STORE); } catch (e) {}
    location.reload();
  });
  if (state.graded) gradeAll(); else progress();
})();
