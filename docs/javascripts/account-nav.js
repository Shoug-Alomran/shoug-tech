/**
 * Adds the "My Transcript" tab after "My Progress", and "My Plan" (the
 * student's academic plan grid) after it, in the account header.
 *
 * firebase-auth.js builds that header, but the live site gets firebase-auth.js
 * from the course-access Worker's bundled copy, which only updates on a Worker
 * deploy. Once that copy has the tabs, this script finds them and does nothing.
 */
(function () {
  "use strict";

  var HREF = "/account/transcript/";

  function isArabic() {
    return (document.documentElement.lang || "").indexOf("ar") === 0;
  }

  function label() {
    return isArabic() ? "سجلي الأكاديمي" : "My Transcript";
  }

  // Same choice as planGridHref() in firebase-auth.js: the plan picked on the
  // transcript page, else the grid the student has filled in, else the picker.
  var PLAN_GRID_KEYS = {
    "cs-ai": "shoug_academic_plan_grid_cs_ai_v1",
    "cs-cys": "shoug_academic_plan_grid_cs_cys_v1",
    "cs-dx": "shoug_academic_plan_grid_cs_dx_v1",
    "is-ai": "shoug_academic_plan_grid_is_ai_v1",
    "se-ai": "shoug_academic_plan_grid_se_ai_v1",
    "se-cys": "shoug_academic_plan_grid_v4",
    se: "shoug_academic_plan_grid_se_v1",
  };
  function planGridHref() {
    try {
      var picked = /^(cs-ai|cs-cys|cs-dx|se-ai|se-cys|se|is-ai)(?:\/classic)?$/.exec(
        localStorage.getItem("shoug-transcript-plan") || "",
      );
      if (picked) return "/academic-plan-themes/" + picked[1] + "/grid.html";
      var best = null,
        bestCount = 0;
      Object.keys(PLAN_GRID_KEYS).forEach(function (plan) {
        var saved = JSON.parse(localStorage.getItem(PLAN_GRID_KEYS[plan]) || "null");
        var count = saved && saved.statusMap ? Object.keys(saved.statusMap).length : 0;
        if (count > bestCount) {
          best = plan;
          bestCount = count;
        }
      });
      if (best) return "/academic-plan-themes/" + best + "/grid.html";
    } catch (e) {}
    return "/academic-plan-themes/academic-plan/";
  }

  function addPlanTab(nav, transcriptTab) {
    var tab = nav.querySelector('.shoug-app-tab[href^="/academic-plan-themes/"]');
    if (!tab) {
      tab = document.createElement("a");
      tab.className = "shoug-app-tab";
      tab.href = planGridHref();
      tab.setAttribute("data-plan-nav", "");
      transcriptTab.parentNode.insertBefore(tab, transcriptTab.nextSibling);
    }
    if (!tab.hasAttribute("data-plan-nav")) return;
    tab.textContent = isArabic() ? "خطتي الدراسية" : "My Plan";
    // An older header relabels by position, which shifts Community's label onto this tab.
    var community = nav.querySelector('.shoug-app-tab[href="/community/"]');
    if (community) community.textContent = isArabic() ? "المجتمع" : "Community";
  }

  function addTab() {
    var nav = document.getElementById("shoug-app-nav");
    if (!nav) return false;
    var tab = nav.querySelector('.shoug-app-tab[href="' + HREF + '"]');
    if (!tab) {
      var progress = nav.querySelector('.shoug-app-tab[href="/account/"]');
      if (!progress) return true;
      tab = document.createElement("a");
      tab.className = "shoug-app-tab";
      tab.href = HREF;
      tab.setAttribute("data-account-nav", "");
      if (location.pathname.indexOf(HREF) === 0) {
        tab.classList.add("active");
        nav.querySelectorAll(".shoug-app-tab.active").forEach(function (t) {
          t.classList.remove("active");
        });
      }
      progress.parentNode.insertBefore(tab, progress.nextSibling);
    }
    addPlanTab(nav, tab);
    // The older header relabels tabs by position on a language switch, so
    // restore this tab's text and the Community tab's afterwards.
    if (tab.hasAttribute("data-account-nav")) {
      tab.textContent = label();
      var community = nav.querySelector('.shoug-app-tab[href="/community/"]');
      if (community)
        community.textContent = isArabic() ? "المجتمع" : "Community";
    }
    return true;
  }

  if (!addTab()) {
    var watch = new MutationObserver(function () {
      if (addTab()) watch.disconnect();
    });
    watch.observe(document.documentElement, { childList: true, subtree: true });
  }
  new MutationObserver(function () {
    setTimeout(addTab, 0);
  }).observe(document.documentElement, {
    attributes: true,
    attributeFilter: ["lang"],
  });
})();
