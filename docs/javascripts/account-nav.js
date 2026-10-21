/**
 * Adds the "My Transcript" tab after "My Progress" in the account header.
 *
 * firebase-auth.js builds that header, but the live site gets firebase-auth.js
 * from the course-access Worker's bundled copy, which only updates on a Worker
 * deploy. Once that copy has the tab, this script finds it and does nothing.
 */
(function () {
  "use strict";

  var HREF = "/account/transcript/";

  function label() {
    return (document.documentElement.lang || "").indexOf("ar") === 0
      ? "سجلي الأكاديمي"
      : "My Transcript";
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
    // The older header relabels tabs by position on a language switch, so
    // restore this tab's text and the Community tab's afterwards.
    if (tab.hasAttribute("data-account-nav")) {
      tab.textContent = label();
      var community = nav.querySelector('.shoug-app-tab[href="/community/"]');
      if (community)
        community.textContent =
          (document.documentElement.lang || "").indexOf("ar") === 0
            ? "المجتمع"
            : "Community";
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
