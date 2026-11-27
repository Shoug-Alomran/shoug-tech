/* Track the active section in a breakdown TOC and show remaining sections. */
(function () {
  "use strict";
  function init() {
    if (document.querySelector(".breakdown-reading-progress")) return;
    var idMap = new Map();
    document.querySelectorAll("[id]").forEach(function (el) { idMap.set(el.id, el); });
    var selector = [
      ".toc a[href^='#']", ".table-of-contents a[href^='#']",
      ".chapter-toc a[href^='#']", ".toc-rail a[href^='#']",
      ".toc-bar a[href^='#']", ".toc-strip a[href^='#']",
      ".toc-pills a[href^='#']", ".toc-grid a[href^='#']",
      ".bdx-toc a[href^='#']", "nav a[href^='#']"
    ].join(",");
    var groups = [];
    document.querySelectorAll(selector).forEach(function (link) {
      var group = link.closest("nav, .toc, .table-of-contents, .chapter-toc, .toc-rail, .toc-bar, .toc-strip, .toc-pills, .toc-grid, .bdx-toc");
      if (!group) return;
      var entry = groups.find(function (item) { return item.el === group; });
      if (!entry) { entry = { el: group, links: [] }; groups.push(entry); }
      var id = link.getAttribute("href").slice(1);
      var target;
      try { target = idMap.get(decodeURIComponent(id)); } catch (_) { target = idMap.get(id); }
      if (target && !entry.links.some(function (item) { return item.target === target; })) entry.links.push({ link: link, target: target });
    });
    groups.sort(function (a, b) { return b.links.length - a.links.length; });
    var group = groups.find(function (item) { return item.links.length >= 2; });
    var items = group ? group.links : [];
    if (!items.length) {
      var sections = Array.from(document.querySelectorAll("main section[id], main article[id], .content section[id], .container section[id]"));
      if (!sections.length) sections = Array.from(document.querySelectorAll("main h2, article h2, .content h2, .container h2"));
      items = sections.map(function (target) {
        if (!target.id) target.setAttribute("data-breakdown-reading-section", "");
        return { target: target };
      });
    }
    var indicator = document.createElement("div");
    indicator.className = "breakdown-reading-progress";
    indicator.setAttribute("role", "status");
    indicator.setAttribute("aria-live", "polite");
    var label = document.createElement("span");
    var track = document.createElement("span");
    track.className = "breakdown-reading-progress-track";
    track.setAttribute("aria-hidden", "true");
    var fill = document.createElement("span");
    fill.className = "breakdown-reading-progress-fill";
    track.appendChild(fill);
    indicator.append(label, track);
    if (group) {
      items.forEach(function (item) { item.link.classList.add("breakdown-reading-progress-link"); });
      group.el.insertAdjacentElement("afterend", indicator);
    } else {
      indicator.classList.add("is-floating");
      document.body.appendChild(indicator);
    }

    if (!items.length) {
      function updatePageProgress() {
        var max = Math.max(1, document.documentElement.scrollHeight - window.innerHeight);
        var progress = Math.max(0, Math.min(1, window.scrollY / max));
        var percent = Math.round(progress * 100);
        label.textContent = "PAGE " + percent + "% · " + (100 - percent) + "% LEFT";
        fill.style.width = percent + "%";
      }
      window.addEventListener("scroll", updatePageProgress, { passive: true });
      window.addEventListener("resize", updatePageProgress);
      updatePageProgress();
      return;
    }

    var active = -1;
    function update(index) {
      index = Math.max(0, Math.min(index, items.length - 1));
      if (index === active) return;
      active = index;
      items.forEach(function (item, i) {
        if (item.link) {
          if (i === active) item.link.setAttribute("aria-current", "location");
          else item.link.removeAttribute("aria-current");
        }
        if (!group) item.target.classList.toggle("breakdown-reading-current", i === active);
      });
      var left = items.length - active - 1;
      label.textContent = "SECTION " + (active + 1) + " / " + items.length + " · " + left + " LEFT";
      fill.style.width = ((active + 1) / items.length * 100) + "%";
    }
    var observer = new IntersectionObserver(function (entries) {
      var visible = entries.filter(function (entry) { return entry.isIntersecting; });
      if (!visible.length) return;
      visible.sort(function (a, b) { return a.boundingClientRect.top - b.boundingClientRect.top; });
      var index = items.findIndex(function (item) { return item.target === visible[0].target; });
      if (index >= 0) update(index);
    }, { rootMargin: "-18% 0px -68% 0px", threshold: 0 });
    items.forEach(function (item) { observer.observe(item.target); });
    items.forEach(function (item, index) {
      if (item.link) item.link.addEventListener("click", function () { update(index); });
    });
    update(0);
  }
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", init);
  else init();
})();
