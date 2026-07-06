(function () {
  var mobileMenuButton = document.querySelector(".shoug-header-menu-btn");
  var directoryButton = document.querySelector(".shoug-directory-btn");
  var mobileOverlay = document.querySelector("[data-mobile-overlay]");
  var primaryNav = document.querySelector(".shoug-header-nav");

  if (primaryNav && !primaryNav.id) {
    primaryNav.id = "shoug-mobile-nav";
  }

  function setMobileMenu(open) {
    document.body.classList.toggle("mobile-nav-open", open);
    if (mobileMenuButton) {
      mobileMenuButton.setAttribute("aria-expanded", open ? "true" : "false");
      mobileMenuButton.setAttribute("aria-label", open ? "Close site menu" : "Open site menu");
    }
  }

  function setDirectory(open) {
    document.body.classList.toggle("sidebar-open", open);
    if (directoryButton) {
      directoryButton.setAttribute("aria-expanded", open ? "true" : "false");
      directoryButton.setAttribute("aria-label", open ? "Close academic directory" : "Open academic directory");
    }
  }

  if (mobileMenuButton) {
    mobileMenuButton.addEventListener("click", function () {
      var next = !document.body.classList.contains("mobile-nav-open");
      setDirectory(false);
      setMobileMenu(next);
    });
  }

  if (directoryButton) {
    if (!document.querySelector(".academic-sidebar")) {
      directoryButton.hidden = true;
    }

    directoryButton.addEventListener("click", function () {
      var next = !document.body.classList.contains("sidebar-open");
      setMobileMenu(false);
      setDirectory(next);
    });
  }

  if (mobileOverlay) {
    mobileOverlay.addEventListener("click", function () {
      setMobileMenu(false);
      setDirectory(false);
    });
  }

  document.addEventListener("keydown", function (event) {
    if (event.key === "Escape") {
      setMobileMenu(false);
      setDirectory(false);
    }
  });

  document.querySelectorAll(".shoug-header-nav a, .academic-sidebar a").forEach(function (link) {
    link.addEventListener("click", function () {
      setMobileMenu(false);
      setDirectory(false);
    });
  });

  var sidebarCollapseBtn = document.querySelector("[data-sidebar-collapse]");
  if (sidebarCollapseBtn) {
    sidebarCollapseBtn.addEventListener("click", function () {
      if (document.body.classList.contains("sidebar-open")) {
        setDirectory(false);
      }
    });
  }
})();

// Load search on every page
(function () {
  var s = document.createElement("script");
  s.src = "/javascripts/search.js";
  s.async = true;
  document.head.appendChild(s);
})();

// Load Firebase auth + progress tracking on every page
(function () {
  var s = document.createElement("script");
  s.src = "/javascripts/firebase-auth.js?v=55";
  s.async = true;
  document.head.appendChild(s);
})();
