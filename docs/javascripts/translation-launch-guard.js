(function () {
  "use strict";

  // Temporary launch guard. Remove this script include to re-enable Arabic.
  try {
    localStorage.setItem("shoug-lang", "en");
  } catch (_) {}

  document.documentElement.lang = "en";

  var style = document.createElement("style");
  style.id = "translation-launch-guard-style";
  style.textContent = "[data-lang-toggle],.shoug-lang-btn{display:none!important}";
  document.head.appendChild(style);

  function removeToggle() {
    document.querySelectorAll("[data-lang-toggle],.shoug-lang-btn").forEach(function (node) {
      node.remove();
    });
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", removeToggle);
  } else {
    removeToggle();
  }
})();
