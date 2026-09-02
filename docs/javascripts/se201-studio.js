(function () {
  "use strict";
  var root = document.documentElement, path = location.pathname.toLowerCase(), body;
  var storageKey = "shoug-theme";
  var topics = [
    { match: /practices-and-ethics|chapter-1-quiz/, key: "ethics", label: "Practices & Ethics", icon: "§" },
    { match: /software-processes|chapter-2-quiz/, key: "process", label: "Software Processes", icon: "↻" },
    { match: /agile-software|chapter-3-quiz/, key: "agile", label: "Agile Engineering", icon: "⚡" },
    { match: /project-management|chapter-4-quiz/, key: "management", label: "Project Management", icon: "◆" },
    { match: /uml|diagram-symbol|system-model|chapter-5-quiz/, key: "modeling", label: "Requirements & Modeling", icon: "◇" },
    { match: /requirements-engineering/, key: "requirements", label: "Requirements Engineering", icon: "◎" },
    { match: /software-design|chapter-6-quiz/, key: "design", label: "Software Design", icon: "⌘" },
    { match: /software-construction|chapter-7-quiz/, key: "construction", label: "Software Construction", icon: "</>" },
    { match: /software-testing|chapter-8-quiz/, key: "testing", label: "Software Testing", icon: "✓" }
  ];
  function pageType() {
    if (path.indexOf("/exams/") !== -1) return "exam";
    if (path.indexOf("/mindmaps/") !== -1) return "mindmap";
    if (/cheat-sheet|compiled-mcqs|complete-uml/.test(path)) return "reference";
    return "breakdown";
  }
  function topic() {
    for (var i = 0; i < topics.length; i += 1) if (topics[i].match.test(path)) return topics[i];
    return { key: "core", label: "Software Engineering", icon: "SE" };
  }
  function readTheme() {
    try { var saved = localStorage.getItem(storageKey) || localStorage.getItem("theme"); if (/^(light|dark)$/.test(saved)) return saved; } catch (e) {}
    return window.matchMedia && window.matchMedia("(prefers-color-scheme: dark)").matches ? "dark" : "light";
  }
  function themeIcon(theme) {
    return theme === "dark" ? '<svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="12" r="4"/><path d="M12 2v2m0 16v2M4.9 4.9l1.5 1.5m11.2 11.2 1.5 1.5M2 12h2m16 0h2M4.9 19.1l1.5-1.5M17.6 6.4l1.5-1.5"/></svg>' : '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M20.3 15.2A8.5 8.5 0 1 1 8.8 3.7a7 7 0 0 0 11.5 11.5Z"/></svg>';
  }
  function applyTheme(theme, persist) {
    root.setAttribute("data-theme", theme); root.style.colorScheme = theme;
    if (body) { body.setAttribute("data-theme", theme); body.classList.toggle("shoug-light-mode", theme === "light"); body.classList.toggle("shoug-dark-mode", theme === "dark"); }
    var toggle = document.getElementById("se201-theme-toggle");
    if (toggle) { toggle.innerHTML = themeIcon(theme); toggle.setAttribute("aria-label", "Switch to " + (theme === "dark" ? "light" : "dark") + " mode"); }
    if (persist) try { localStorage.setItem(storageKey, theme); localStorage.setItem("theme", theme); } catch (e) {}
  }
  applyTheme(readTheme(), false);
  function addBar(type, subject) {
    var bar = document.createElement("header"); bar.className = "se201-studio-bar";
    bar.innerHTML = '<a class="se201-studio-brand" href="/academics/software-engineering/se201/"><span class="se201-studio-mark" aria-hidden="true">' + subject.icon + '</span><span><small>SE201 · ' + type + '</small>' + subject.label + '</span></a><nav class="se201-studio-nav" aria-label="Study material"><a href="/academics/software-engineering/se201/slide-breakdowns/">Breakdowns</a><a href="/academics/software-engineering/se201/extra-resources/mindmaps/">Mind maps</a><a href="/academics/software-engineering/se201/exams/">Exams</a></nav><button class="se201-theme-toggle" id="se201-theme-toggle" type="button"></button>';
    body.insertBefore(bar, body.firstChild);
    bar.querySelector("button").addEventListener("click", function () { applyTheme(root.getAttribute("data-theme") === "dark" ? "light" : "dark", true); });
    applyTheme(readTheme(), false);
  }
  function setup() {
    body = document.body; if (!body) return;
    var type = pageType(), subject = topic();
    body.classList.add("se201-content", "se201-" + type, "se201-topic-" + subject.key);
    body.setAttribute("data-content-type", type); body.setAttribute("data-topic", subject.key);
    addBar(type, subject); applyTheme(readTheme(), false);
    requestAnimationFrame(function () { body.classList.add("se201-ready"); });
  }
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", setup, { once: true }); else setup();
  window.addEventListener("storage", function (event) { if (event.key === storageKey || event.key === "theme") applyTheme(readTheme(), false); });
})();
