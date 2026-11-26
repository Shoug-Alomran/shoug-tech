/* Mind map "Quick check": short MCQ sets added as a leaf under a branch.
 *
 * A page defines, before loading this script:
 *   window.MM_QUIZ = { "<branch node id>": [ ["Question", ["Right", "Wrong", ...], "Why"], ... ] };
 * The first option is the right one; options are shuffled (stably, per question) when shown.
 *
 * It relies on the mind map engine's globals: DATA, openPanel and render.
 */
(function () {
  "use strict";

  if (
    typeof DATA === "undefined" ||
    typeof openPanel !== "function" ||
    !window.MM_QUIZ
  )
    return;

  function find(node, id) {
    if (node.id === id) return node;
    for (var i = 0; node.children && i < node.children.length; i++) {
      var hit = find(node.children[i], id);
      if (hit) return hit;
    }
    return null;
  }

  Object.keys(window.MM_QUIZ).forEach(function (id) {
    var branch = find(DATA, id);
    var qs = window.MM_QUIZ[id];
    if (!branch || !qs || !qs.length) return;
    branch.children = branch.children || [];
    if (
      branch.children.some(function (c) {
        return c.quiz;
      })
    )
      return;
    branch.children.push({
      id: id + "-quick-check",
      label: "✎ Quick check",
      quiz: qs,
      desc:
        '<span class="panel-tag">Practice</span><p>' +
        qs.length +
        (qs.length === 1 ? " question" : " questions") +
        " on <strong>" +
        branch.label +
        "</strong>. Pick an answer to see if you're right and why.</p>",
    });
  });

  function esc(s) {
    return String(s).replace(/[&<>"]/g, function (c) {
      return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c];
    });
  }

  // Stable shuffle: same order every time for the same question.
  function order(n, seed) {
    var h = 2166136261;
    for (var i = 0; i < seed.length; i++)
      h = Math.imul(h ^ seed.charCodeAt(i), 16777619);
    var idx = [];
    for (var k = 0; k < n; k++) idx.push(k);
    for (var j = n - 1; j > 0; j--) {
      h = Math.imul(h ^ (h >>> 15), 2246822519) >>> 0;
      var r = h % (j + 1);
      var t = idx[j];
      idx[j] = idx[r];
      idx[r] = t;
    }
    return idx;
  }

  // On mind map pages site-palette.js repaints every green with saturation >= 0.35 to the theme colour, so
  // "correct" uses a slightly muted green (saturation 0.33) that it leaves alone. Red is never repainted.
  var MARKS = { ok: ["#55aa63", "✓"], bad: ["#f85149", "✗"] };
  function mark(button, kind) {
    var c = MARKS[kind][0];
    button.style.borderColor = c;
    button.style.background =
      "color-mix(in srgb, " + c + " 18%, var(--surface))";
    var m = document.createElement("span");
    m.className = "mmq-mark";
    m.style.color = c;
    m.textContent = MARKS[kind][1];
    button.appendChild(m);
  }

  function renderQuiz(node) {
    var body = document.getElementById("panel-body");
    if (!body) return;
    var wrap = document.createElement("div");
    wrap.className = "mmq";
    var score = document.createElement("div");
    score.className = "mmq-score";
    var answered = 0;
    var right = 0;
    function updateScore() {
      score.textContent =
        "Score: " +
        right +
        " / " +
        answered +
        " answered · " +
        node.quiz.length +
        " total";
    }
    updateScore();
    wrap.appendChild(score);

    node.quiz.forEach(function (item, qi) {
      var q = document.createElement("div");
      q.className = "mmq-q";
      q.innerHTML =
        '<p class="mmq-stem"><span class="mmq-n">Q' +
        (qi + 1) +
        "</span> " +
        esc(item[0]) +
        "</p>";
      var opts = document.createElement("div");
      opts.className = "mmq-opts";
      var why = document.createElement("p");
      why.className = "mmq-why";
      why.hidden = true;
      order(item[1].length, item[0]).forEach(function (oi) {
        var b = document.createElement("button");
        b.type = "button";
        b.className = "mmq-opt";
        b.textContent = item[1][oi];
        b.addEventListener("click", function () {
          if (q.classList.contains("done")) return;
          q.classList.add("done");
          answered++;
          if (oi === 0) right++;
          if (oi !== 0) mark(b, "bad");
          Array.prototype.forEach.call(opts.children, function (x) {
            x.disabled = true;
            if (x.dataset.right) mark(x, "ok");
          });
          why.innerHTML =
            (oi === 0
              ? "<strong>Correct.</strong> "
              : "<strong>Not quite.</strong> ") + esc(item[2] || "");
          why.hidden = false;
          updateScore();
        });
        if (oi === 0) b.dataset.right = "1";
        opts.appendChild(b);
      });
      q.appendChild(opts);
      q.appendChild(why);
      wrap.appendChild(q);
    });

    var reset = document.createElement("button");
    reset.type = "button";
    reset.className = "mmq-reset";
    reset.textContent = "Retry";
    reset.addEventListener("click", function () {
      wrap.remove();
      renderQuiz(node);
    });
    wrap.appendChild(reset);
    body.appendChild(wrap);
  }

  var baseOpen = openPanel;
  // eslint-disable-next-line no-global-assign
  openPanel = function (node) {
    baseOpen(node);
    if (node && node.quiz) renderQuiz(node);
  };

  var css = document.createElement("style");
  css.textContent = [
    ".mmq{margin-top:14px;display:flex;flex-direction:column;gap:14px}",
    ".mmq-score{font-size:12px;color:var(--text-muted);font-family:var(--font-mono,inherit)}",
    ".mmq-q{border:1px solid var(--border);border-radius:10px;padding:12px;background:var(--surface2)}",
    ".mmq-stem{margin:0 0 10px!important;color:var(--text);font-weight:500}",
    ".mmq-n{display:inline-block;margin-right:4px;color:var(--accent3);font-weight:700;font-size:12px}",
    ".mmq-opts{display:flex;flex-direction:column;gap:6px}",
    ".mmq-opt{text-align:left;font:inherit;font-size:13px;line-height:1.4;padding:8px 10px;border-radius:8px;cursor:pointer;",
    "border:1px solid var(--border);background:var(--surface);color:var(--text);transition:border-color .15s}",
    ".mmq-opt:hover:not(:disabled){border-color:var(--accent3)}",
    ".mmq-opt:disabled{cursor:default}",
    ".mmq-mark{font-weight:700;margin-left:6px}",
    ".mmq-why{margin:10px 0 0!important;font-size:13px;color:var(--text-muted)}",
    ".mmq-reset{align-self:flex-start;font:inherit;font-size:12px;padding:6px 12px;border-radius:999px;cursor:pointer;",
    "border:1px solid var(--border);background:transparent;color:var(--text)}",
    ".mmq-reset:hover{border-color:var(--accent3)}",
  ].join("");
  document.head.appendChild(css);

  if (typeof render === "function") render();
})();
