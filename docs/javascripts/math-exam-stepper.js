(function () {
  "use strict";
  var root = document.querySelector(".math-one-at-a-time");
  if (!root) return;
  var questions = Array.prototype.slice.call(
    root.querySelectorAll(".math-one-question"),
  );
  var position = root.parentNode.querySelector(".math-question-position");
  var prev = root.parentNode.querySelector('[data-question-step="prev"]');
  var next = root.parentNode.querySelector('[data-question-step="next"]');
  var current = Math.max(
    0,
    questions.findIndex(function (q) {
      return !q.hidden;
    }),
  );
  function show(index, shouldScroll) {
    current = Math.max(0, Math.min(index, questions.length - 1));
    questions.forEach(function (q, i) {
      q.hidden = i !== current;
      if (i === current) q.setAttribute("aria-current", "step");
      else q.removeAttribute("aria-current");
    });
    if (position)
      position.textContent =
        "Question " + (current + 1) + " of " + questions.length;
    if (prev) prev.disabled = current === 0;
    if (next) next.disabled = current === questions.length - 1;
    if (shouldScroll)
      questions[current].scrollIntoView({ behavior: "smooth", block: "start" });
  }
  root.parentNode.addEventListener("click", function (event) {
    var button = event.target.closest("[data-question-step]");
    if (!button) return;
    show(
      current + (button.getAttribute("data-question-step") === "next" ? 1 : -1),
      true,
    );
  });
  document.addEventListener("keydown", function (event) {
    if (
      event.altKey ||
      event.ctrlKey ||
      event.metaKey ||
      /INPUT|TEXTAREA|SELECT/.test(event.target.tagName)
    )
      return;
    if (event.key === "ArrowRight") show(current + 1, true);
    if (event.key === "ArrowLeft") show(current - 1, true);
  });
  show(current, false);
})();
