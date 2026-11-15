/**
 * Colour and motion for the exam pages of every course (see styles/quiz-motion.css,
 * linked by scripts/install_quiz_motion.py).
 *
 * The quizzes come from several templates, and most build their questions in
 * JavaScript after load, so this script watches the page instead of expecting
 * fixed markup: it tags question cards, options, feedback, progress bars and
 * score readouts as they appear, and turns each template's own answer classes
 * (correct / is-correct / c-correct ...) into a pulse or a shake.
 */
(function () {
  "use strict";
  if (window.__quizMotion) return;
  window.__quizMotion = true;

  var root = document.documentElement;
  var reduce = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  var CARD = ".q, .question, .q-card, .question-card, .question-block, .quiz-q, .ex-part";
  var OPTION = "label, .opt, .opt-label, .option, .option-btn, .choice, .quiz-opt";
  var FEEDBACK = ".feedback, .fb, .explanation";
  var SCORE = ".score, .scorebar, .scorebox, .score-box, .progress-pill, #scoreBar, #score";
  var BAR = ".progress-fill, .progress > i, .progress > span, .progress-bar > *, .bar-fill";
  var HEAD = ".hero, .exam-head, .exam-header, .topbar, header.top, .top";
  var BUTTON = "button, .btn";
  // Each question card takes the next accent; --cqm-c2 is the one after it.
  var PALETTE = ["#ff3d8b", "#8b5cf6", "#22d3ee", "#f59e0b", "#10b981", "#3b82f6"];
  var CTA = /check|submit|grade|finish|reveal|show (all|model)|answers/i;
  var OK = ["correct", "is-correct", "c-correct", "selected-correct", "correct-ans", "is-right", "correct-answer", "answered-correct"];
  var BAD = ["wrong", "is-wrong", "c-wrong", "selected-wrong", "wrong-ans", "picked-wrong", "incorrect", "incorrect-answer", "answered-wrong"];

  root.classList.add("cqm");
  if (!reduce && "IntersectionObserver" in window) root.classList.add("cqm-motion");

  function isLight() {
    var t = root.getAttribute("data-theme");
    if (t) return t === "light";
    var b = document.body;
    if (b && (b.classList.contains("light") || b.classList.contains("shoug-light-mode"))) return true;
    var m = getComputedStyle(b || root).backgroundColor.match(/[\d.]+/g);
    return !!m && (+m[3] !== 0) && 0.299 * m[0] + 0.587 * m[1] + 0.114 * m[2] > 150;
  }

  function syncLight() {
    root.classList.toggle("cqm-light", isLight());
  }

  function addAmbient() {
    if (reduce || document.querySelector(".cqm-ambient")) return;
    var layer = document.createElement("div");
    layer.className = "cqm-ambient";
    layer.setAttribute("aria-hidden", "true");
    layer.innerHTML = "<i></i><i></i><i></i><i></i>";
    document.body.insertBefore(layer, document.body.firstChild);
  }


  var order = 0;
  var revealer =
    root.classList.contains("cqm-motion") &&
    new IntersectionObserver(
      function (entries) {
        entries.forEach(function (entry) {
          if (!entry.isIntersecting) return;
          entry.target.classList.add("cqm-in");
          revealer.unobserve(entry.target);
        });
      },
      { rootMargin: "0px 0px -5% 0px", threshold: 0.05 },
    );

  function each(node, selector, fn) {
    if (!node || node.nodeType !== 1) return;
    if (node.matches(selector)) fn(node);
    node.querySelectorAll(selector).forEach(fn);
  }

  function prepCard(card) {
    if (card.__cqm || card.parentElement.closest(CARD)) return;
    card.__cqm = true;
    card.classList.add("cqm-card");
    var hue = order % PALETTE.length;
    card.style.setProperty("--cqm-c", PALETTE[hue]);
    card.style.setProperty("--cqm-c2", PALETTE[(hue + 1) % PALETTE.length]);
    if (!revealer) order++;
    // Cards without side padding would put the accent bar over the text.
    if (parseFloat(getComputedStyle(card).paddingLeft) < 10) card.classList.add("cqm-flush");
    if (revealer) {
      card.style.setProperty("--cqm-delay", (order++ % 5) * 70 + "ms");
      revealer.observe(card);
    } else {
      card.classList.add("cqm-in");
    }
  }

  function prepOption(option) {
    if (option.__cqm || !option.closest(".cqm-card")) return;
    option.__cqm = true;
    option.classList.add("cqm-opt");
  }

  function prepButton(button) {
    if (button.__cqm || button.closest(".cqm-opt") || button.closest(OPTION)) return;
    if (button.closest(".cqm-card") && !/check|submit|reveal|show|next|finish|grade/i.test(button.textContent)) return;
    button.__cqm = true;
    button.classList.add("cqm-btn");
    if (CTA.test(button.textContent) && button.offsetWidth < 360) button.classList.add("cqm-cta");
  }

  function scan(node) {
    each(node, CARD, prepCard);
    each(node, OPTION, prepOption);
    each(node, BUTTON, prepButton);
    each(node, SCORE, function (el) { el.classList.add("cqm-score"); });
    each(node, BAR, function (el) { el.classList.add("cqm-bar"); });
  }

  function replay(el, cls, ms) {
    el.classList.remove(cls);
    void el.offsetWidth;
    el.classList.add(cls);
    setTimeout(function () { el.classList.remove(cls); }, ms);
  }

  function gained(el, oldValue, list) {
    var before = " " + (oldValue || "") + " ";
    return list.some(function (c) {
      return el.classList.contains(c) && before.indexOf(" " + c + " ") === -1;
    });
  }

  // One pulse per question per check, even when a template marks several elements at once.
  var flashed = new WeakMap();
  function answered(el, ok) {
    var card = el.closest(".cqm-card");
    var target = el.closest(".cqm-opt") || card || el;
    var key = card || target;
    var now = Date.now();
    if (flashed.get(key) > now - 400) return;
    flashed.set(key, now);
    if (card) card.classList.add("cqm-answered");
    replay(target, ok ? "cqm-ok" : "cqm-bad", 950);
  }

  function showFeedback(el) {
    if (!el.textContent.trim() && !el.children.length) return;
    var style = getComputedStyle(el);
    if (style.display === "none" || style.visibility === "hidden") return;
    replay(el, "cqm-feedback-in", 500);
  }

  var bumpTimer = new WeakMap();
  function bump(el) {
    clearTimeout(bumpTimer.get(el));
    bumpTimer.set(el, setTimeout(function () { replay(el, "cqm-bump", 550); }, 30));
  }

  function onMutations(mutations) {
    mutations.forEach(function (m) {
      if (m.type === "childList") {
        m.addedNodes.forEach(scan);
        var holder = m.target.nodeType === 1 ? m.target : m.target.parentElement;
        if (!holder) return;
        var fb = holder.closest(FEEDBACK);
        if (fb && m.addedNodes.length) showFeedback(fb);
        var score = holder.closest(".cqm-score");
        if (score) bump(score);
        return;
      }
      if (m.type === "characterData") {
        var parent = m.target.parentElement;
        var s = parent && parent.closest(".cqm-score");
        if (s) bump(s);
        return;
      }
      var el = m.target;
      if (m.attributeName !== "class" || el.classList.contains("cqm-ok") || el.classList.contains("cqm-bad")) return;
      if (gained(el, m.oldValue, OK)) answered(el, true);
      else if (gained(el, m.oldValue, BAD)) answered(el, false);
      if (el.matches(FEEDBACK) && el.classList.contains("show") && (" " + (m.oldValue || "") + " ").indexOf(" show ") === -1) {
        showFeedback(el);
      }
    });
  }

  // Page zoom from styles/site-shell.css (large screens). getBoundingClientRect and
  // pointer coordinates are zoomed; CSS px set on elements are not.
  function pageZoom() {
    return parseFloat(getComputedStyle(document.documentElement).zoom) || 1;
  }

  function ripple(event) {
    var option = event.target.closest && event.target.closest(".cqm-opt");
    if (!option || reduce) return;
    var rect = option.getBoundingClientRect();
    var dot = document.createElement("span");
    dot.className = "cqm-ripple";
    var z = pageZoom();
    dot.style.left = (event.clientX - rect.left) / z + "px";
    dot.style.top = (event.clientY - rect.top) / z + "px";
    option.appendChild(dot);
    setTimeout(function () { dot.remove(); }, 650);
  }

  function start() {
    syncLight();
    addAmbient();
    var head = document.querySelector(HEAD);
    if (head && !reduce) head.classList.add("cqm-head");
    scan(document.body);
    new MutationObserver(onMutations).observe(document.body, {
      childList: true,
      subtree: true,
      characterData: true,
      attributes: true,
      attributeFilter: ["class"],
      attributeOldValue: true,
    });
    new MutationObserver(syncLight).observe(root, { attributes: true, attributeFilter: ["data-theme", "class"] });
    new MutationObserver(syncLight).observe(document.body, { attributes: true, attributeFilter: ["class"] });
    document.addEventListener("pointerdown", ripple, true);
  }

  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", start);
  else start();
})();
