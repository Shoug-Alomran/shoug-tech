(function () {
  "use strict";

  document.querySelectorAll(".notes .q").forEach(function (card) {
    var options = card.querySelector("ol.opts");
    var answer = card.querySelector("details p");
    if (!options || !answer) return;

    var strong = answer.querySelector("strong");
    var answerText = (strong ? strong.textContent : answer.textContent).trim();
    var match = answerText.match(/^([A-Z])(?:[.)])?\s*/);
    if (!match) return;

    var correctLetter = match[1];
    var rationale = answer.cloneNode(true);
    var lead = rationale.querySelector("strong");
    if (lead) lead.remove();
    var explanation = rationale.textContent.trim().replace(/^[\s—–:-]+/, "");

    if (!explanation) {
      var notes = card.closest(".notes");
      var context = notes
        ? Array.prototype.map
            .call(notes.querySelectorAll(":scope > ol .body"), function (note) {
              return note.textContent.trim();
            })
            .filter(Boolean)
            .join(" ")
        : "";
      explanation = context
        ? "Why it fits: " + context.slice(0, 520)
        : "Why it fits: this option matches the concept being tested in the slide.";
    }

    options.classList.add("mcq-interactive");
    var prompt = document.createElement("p");
    prompt.className = "mcq-prompt";
    prompt.textContent = "Select an option to check your answer.";
    options.parentNode.insertBefore(prompt, options);
    var feedback = document.createElement("div");
    feedback.className = "mcq-feedback";
    feedback.setAttribute("role", "status");
    feedback.setAttribute("aria-live", "polite");
    options.parentNode.insertBefore(feedback, options.nextSibling);

    Array.prototype.forEach.call(options.querySelectorAll("li"), function (item, index) {
      var letter = String.fromCharCode(65 + index);
      var content = item.innerHTML;
      var accessibleContent = item.textContent.trim();
      var button = document.createElement("button");
      button.type = "button";
      button.className = "mcq-choice";
      button.setAttribute("aria-pressed", "false");
      button.setAttribute(
        "aria-label",
        "Choose answer " + letter + ": " + accessibleContent,
      );
      button.innerHTML =
        '<span class="mcq-letter">' +
        letter +
        '.</span><span class="mcq-option">' +
        content +
        "</span>";
      item.textContent = "";
      item.appendChild(button);

      button.addEventListener("click", function () {
        options.querySelectorAll(".mcq-choice").forEach(function (choice) {
          choice.classList.remove("is-correct", "is-wrong");
          choice.setAttribute("aria-pressed", "false");
        });
        button.setAttribute("aria-pressed", "true");

        var isCorrect = letter === correctLetter;
        button.classList.add(isCorrect ? "is-correct" : "is-wrong");
        feedback.className = "mcq-feedback " + (isCorrect ? "is-correct" : "is-wrong");
        feedback.textContent = isCorrect
          ? "Correct. " + explanation
          : "Not quite. The correct answer is " +
            correctLetter +
            ": " +
            (options.children[correctLetter.charCodeAt(0) - 65].textContent.replace(/^\s*[A-Z]\.\s*/, "")) +
            " Why: " +
            explanation;
      });
    });
  });
})();
