/**
 * Review mistakes: records questions answered wrong on quiz pages so
 * /academics/review/ can bring them back later (spaced repetition).
 *
 * Quizzes come from several builders with different markup, so this does not
 * hook into any one of them. It watches for the classes they all add when an
 * answer is marked wrong, then reads the question, the chosen answer and the
 * correct answer from the surrounding question card. localStorage only, so it
 * works signed out; nothing leaves the browser.
 */
(function () {
  "use strict";
  if (window.__shougQuizMistakes) return;
  window.__shougQuizMistakes = true;

  var KEY = "shoug-quiz-mistakes";
  var MAX = 400;
  var DAY = 86400000;
  var WRONG =
    /(^|\s)(wrong|incorrect|c-wrong|selected-wrong|answered-wrong|wrong-ans|wrong-input|wrong-mark)(\s|$)/;
  // Some quizzes only highlight the right answer; a different checked choice
  // in the same question is then the mistake.
  var REVEAL = /(^|\s)(correct|c-correct|correct-mark|show-correct|correct-ans)(\s|$)/;
  var CONTAINER =
    ".q-card, .question-card, .question-block, .question-container, .quiz-question, .question, .mcq, .written, .q-item, .q, fieldset, [data-q], [data-question]";
  var QTEXT =
    ".q-text, .question-text, .q-title, .q-stem, .stem, .prompt, .q-prompt, .mcq-prompt, [class*='q-text'], [class*='question-text'], [class*='prompt'], legend, h3, h4, p";
  var CORRECT =
    ".c-correct, .show-correct, .correct-ans, .correct-mark, .selected-correct, label.correct, button.correct, li.correct, .option.correct, .opt.correct, .choice.correct";
  var FEEDBACK =
    ".feedback, .explanation, .explain, .result, .result-box, [class*='feedback'], [class*='explanation']";

  function read() {
    try {
      var v = JSON.parse(localStorage.getItem(KEY));
      return Array.isArray(v) ? v : [];
    } catch (e) {
      return [];
    }
  }
  function write(list) {
    try {
      localStorage.setItem(KEY, JSON.stringify(list.slice(-MAX)));
    } catch (e) {}
  }
  function clean(t) {
    return String(t || "")
      .replace(/\s+/g, " ")
      .trim();
  }
  function hash(s) {
    var h = 2166136261;
    for (var i = 0; i < s.length; i++) {
      h ^= s.charCodeAt(i);
      h = Math.imul(h, 16777619);
    }
    return (h >>> 0).toString(36);
  }

  // The quiz's own page (the folder the wrapper serves), not the iframed file.
  function quizPage() {
    var path = location.pathname.replace(/[^/]*\.html$/, "");
    return path;
  }
  function courseOf(path) {
    var m = path.match(/^\/academics\/[^/]+\/([^/]+)\//);
    return m ? m[1].toUpperCase() : "";
  }
  function quizTitle() {
    var h1 = document.querySelector("h1");
    return clean(
      (h1 && h1.textContent) ||
        String(document.title || "").split(/\s[|/]{1,2}\s/).pop(),
    ).slice(0, 120);
  }

  function questionText(box) {
    var nodes = box.querySelectorAll(QTEXT);
    for (var i = 0; i < nodes.length; i++) {
      var n = nodes[i];
      if (n.closest(FEEDBACK) || n.closest("label, button")) continue;
      // Drop number badges and topic tags that sit inside the prompt.
      var copy = n.cloneNode(true);
      copy
        .querySelectorAll(
          ".num, .number, .q-num, .question-number, .tag, .badge, .chip, .points, .marks, .q-meta",
        )
        .forEach(function (x) {
          x.remove();
        });
      var t = clean(copy.textContent)
        .replace(/^(?:q(?:uestion)?\s*\d{1,3}\s*[.):]?|\d{1,3}\s*[.):])\s*/i, "")
        .replace(/^\(\s*\d+\s*(?:points?|marks?|pts)\s*\)\s*/i, "");
      if (t.length >= 8) return t;
    }
    return "";
  }

  var seen = {},
    noticeShown = false;

  function capture(el) {
    var box = el.matches(CONTAINER) ? el : el.closest(CONTAINER);
    if (!box || box === document.body) return;
    var q = questionText(box);
    if (!q) return;
    var page = quizPage(),
      id = hash(page + "|" + q);
    if (seen[id]) return;
    seen[id] = true;

    var chosenEl = el.matches("label, button, li, .opt, .option, .choice")
        ? el
        : box.querySelector(
            ".selected, .selected-wrong, .c-wrong, .wrong-ans, input:checked",
          ),
      chosen = chosenEl
        ? clean(
            (chosenEl.matches("input") && chosenEl.closest("label")
              ? chosenEl.closest("label")
              : chosenEl
            ).textContent,
          )
        : el.matches("input, textarea")
          ? clean(el.value)
          : "",
      correctEl = box.querySelector(CORRECT),
      feedbackEl = box.querySelector(FEEDBACK);

    var list = read().filter(function (m) {
      return m.id !== id;
    });
    list.push({
      id: id,
      q: q.slice(0, 600),
      chosen: chosen.slice(0, 300),
      correct: correctEl ? clean(correctEl.textContent).slice(0, 300) : "",
      explain: feedbackEl ? clean(feedbackEl.textContent).slice(0, 600) : "",
      page: page,
      course: courseOf(page),
      quiz: quizTitle(),
      at: Date.now(),
      due: Date.now() + DAY,
      box: 0,
    });
    write(list);
    notice();
  }

  function notice() {
    if (noticeShown) return;
    noticeShown = true;
    var a = document.createElement("a");
    a.href = "/academics/review/";
    a.target = "_top";
    a.textContent = "Missed questions are saved to Review mistakes";
    a.setAttribute("role", "status");
    a.style.cssText =
      "position:fixed;right:16px;bottom:16px;z-index:9999;max-width:calc(100% - 32px);" +
      "padding:10px 14px;border-radius:10px;border:1px solid rgba(184,41,234,.45);" +
      "background:#120b1b;color:#f8f7fb;font:600 13px/1.3 Inter,system-ui,sans-serif;" +
      "text-decoration:none;box-shadow:0 8px 24px rgba(0,0,0,.35)";
    document.body.appendChild(a);
    setTimeout(function () {
      a.remove();
    }, 6000);
  }

  function check(el) {
    if (el.nodeType !== 1 || typeof el.className !== "string") return;
    if (WRONG.test(el.className)) return capture(el);
    if (REVEAL.test(el.className) && !el.matches(FEEDBACK)) {
      var box = el.closest(CONTAINER),
        picked = box && box.querySelector("input:checked");
      if (picked && !el.contains(picked)) capture(picked);
    }
  }

  new MutationObserver(function (records) {
    records.forEach(function (r) {
      if (r.type === "attributes") check(r.target);
      else
        r.addedNodes.forEach(function (n) {
          if (n.nodeType !== 1) return;
          check(n);
          n.querySelectorAll && n.querySelectorAll("[class]").forEach(check);
        });
    });
  }).observe(document.documentElement, {
    subtree: true,
    childList: true,
    attributes: true,
    attributeFilter: ["class"],
  });
})();
