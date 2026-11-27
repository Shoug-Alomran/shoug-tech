/* Highlights the current chapter and estimates how many chapters remain. */
(function () {
  "use strict";
  function init() {
    var nav = document.querySelector("header.top nav.pillnav");
    if (!nav) return;
    var links = Array.from(nav.querySelectorAll('a[href^="#"]'));
    var sections = links
      .map(function (link) {
        return document.getElementById(decodeURIComponent(link.hash.slice(1)));
      })
      .filter(Boolean);
    if (!sections.length) return;

    var indicator = document.createElement("div");
    indicator.className = "se423-reading-progress";
    indicator.setAttribute("role", "status");
    indicator.setAttribute("aria-live", "polite");
    var label = document.createElement("span");
    var track = document.createElement("span");
    track.className = "se423-reading-progress-track";
    track.setAttribute("aria-hidden", "true");
    var fill = document.createElement("span");
    fill.className = "se423-reading-progress-fill";
    track.appendChild(fill);
    indicator.append(label, track);
    nav.insertAdjacentElement("afterend", indicator);

    var active = 0;
    function update(index) {
      active = Math.max(0, Math.min(index, sections.length - 1));
      links.forEach(function (link, i) {
        if (sections[i]) {
          if (i === active) link.setAttribute("aria-current", "location");
          else link.removeAttribute("aria-current");
        }
      });
      var remaining = sections.length - active - 1;
      label.textContent =
        "SECTION " +
        (active + 1) +
        " / " +
        sections.length +
        " · " +
        remaining +
        " LEFT";
      fill.style.width = ((active + 1) / sections.length) * 100 + "%";
    }
    var observer = new IntersectionObserver(
      function (entries) {
        var visible = entries.filter(function (entry) {
          return entry.isIntersecting;
        });
        if (!visible.length) return;
        visible.sort(function (a, b) {
          return a.boundingClientRect.top - b.boundingClientRect.top;
        });
        var index = sections.indexOf(visible[0].target);
        if (index >= 0) update(index);
      },
      { rootMargin: "-18% 0px -68% 0px", threshold: 0 },
    );
    sections.forEach(function (section) {
      observer.observe(section);
    });
    links.forEach(function (link) {
      link.addEventListener("click", function () {
        var index = sections.findIndex(function (section) {
          return "#" + section.id === link.hash;
        });
        if (index >= 0) update(index);
      });
    });
    update(0);
  }
  if (document.readyState === "loading")
    document.addEventListener("DOMContentLoaded", init);
  else init();
})();
