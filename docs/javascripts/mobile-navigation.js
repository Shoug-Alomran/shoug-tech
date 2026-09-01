(function () {
  var mobileMenuButton = document.querySelector(".shoug-header-menu-btn");
  var directoryButton = document.querySelector(".shoug-directory-btn");
  var mobileOverlay = document.querySelector("[data-mobile-overlay]");
  var primaryNav = document.querySelector(".shoug-header-nav");

  if (primaryNav && !primaryNav.id) {
    primaryNav.id = "shoug-mobile-nav";
  }

  // The profile avatar button is injected later by firebase-auth.js (async,
  // after auth state resolves), so it's driven the same way the menu/
  // directory toggles are — a body class flipped from here — rather than a
  // class on the button itself. That keeps all three overlays on one shared,
  // mutually-exclusive open/close mechanism instead of each having its own.
  function setProfile(open) {
    document.body.classList.toggle("profile-open", open);
    document.dispatchEvent(new CustomEvent("shoug:profile-toggle", { detail: { open: open } }));
  }

  function setMobileMenu(open) {
    document.body.classList.toggle("mobile-nav-open", open);
    if (open) setProfile(false);
    if (mobileMenuButton) {
      mobileMenuButton.setAttribute("aria-expanded", open ? "true" : "false");
      mobileMenuButton.setAttribute("aria-label", open ? "Close site menu" : "Open site menu");
    }
  }

  function setDirectory(open) {
    document.body.classList.toggle("sidebar-open", open);
    if (open) setProfile(false);
    if (directoryButton) {
      directoryButton.setAttribute("aria-expanded", open ? "true" : "false");
      directoryButton.setAttribute("aria-label", open ? "Close academic directory" : "Open academic directory");
    }
  }

  document.addEventListener("click", function (event) {
    var target = event.target;
    var profileBtn = target.closest && target.closest("#shoug-fb-user");
    var insideDropdown = target.closest && target.closest(".shoug-user-dropdown");
    if (profileBtn && !insideDropdown) {
      var next = !document.body.classList.contains("profile-open");
      setMobileMenu(false);
      setDirectory(false);
      setProfile(next);
      return;
    }
    if (!insideDropdown && document.body.classList.contains("profile-open")) {
      setProfile(false);
    }
  });

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
      setProfile(false);
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

// Slide and breakdown pages share one grounded AI assistant client.
(function () {
  if (!/\/(slides|slide-breakdowns)\/[^/]+\/?(?:index\.html)?$/.test(location.pathname)) return;
  if (document.getElementById("shoug-slide-assistant-script")) return;
  var script = document.createElement("script");
  script.id = "shoug-slide-assistant-script";
  script.src = "/javascripts/slide-assistant.js?v=20260902-1";
  script.defer = true;
  document.head.appendChild(script);
})();

// Keep the copyright notice present on every page that uses the shared footer.
(function () {
  var footer = document.querySelector(".shoug-site-footer");
  var noticeText = "© 2026 Shoug Alomran. All rights reserved.";
  if (!footer || footer.querySelector(".shoug-footer-copyright")) return;

  var brandText = footer.querySelector(".shoug-footer-text");
  if (!brandText || !brandText.parentElement) return;

  var notice = document.createElement("span");
  notice.className = "shoug-footer-text shoug-footer-copyright";
  notice.setAttribute("data-ar-text", "© 2026 شوق العمران. جميع الحقوق محفوظة.");
  notice.textContent = noticeText;

  brandText.insertAdjacentElement("afterend", notice);
})();

// Load search on every page
(function () {
  var s = document.createElement("script");
  s.src = "/javascripts/search.js?v=20260729-resources-1";
  s.async = true;
  document.head.appendChild(s);
})();

// Load Arabic localization on every page that uses the shared shell.
(function () {
  if (window.__shougArabicLocalizationLoaded || document.getElementById("shoug-arabic-localization-script")) return;
  var loading = false;
  function loadArabicLocalization(callback) {
    if (window.__shougArabicLocalizationLoaded) {
      if (callback) callback();
      return;
    }
    if (loading) return;
    loading = true;
    var s = document.createElement("script");
    s.id = "shoug-arabic-localization-script";
    s.src = "/javascripts/arabic-localization.js?v=61";
    s.defer = true;
    if (callback) s.addEventListener("load", callback, { once: true });
    document.head.appendChild(s);
  }

  var storedArabic = false;
  try { storedArabic = localStorage.getItem("shoug-lang") === "ar"; } catch (error) { }
  if (storedArabic || document.documentElement.lang.indexOf("ar") === 0) {
    loadArabicLocalization();
    return;
  }

  var toggle = document.querySelector("[data-lang-toggle]");
  if (toggle) {
    toggle.addEventListener("click", function (event) {
      if (window.__shougArabicLocalizationLoaded) return;
      event.preventDefault();
      event.stopImmediatePropagation();
      loadArabicLocalization(function () {
        if (typeof window.__shougSetLanguage === "function") window.__shougSetLanguage("ar");
      });
    }, true);
  }
})();

// Keep a lightweight account control visible on every shared-shell page, then
// load Firebase on account intent (or shortly after the initial render).
(function () {
  var loaded = false;

  function loadFirebase(openWhenReady) {
    if (loaded) {
      if (openWhenReady) {
        if (typeof window.__shougOpenAuthModal === "function") {
          window.__shougOpenAuthModal();
        } else {
          window.addEventListener("shoug:fb", function () {
            if (typeof window.__shougOpenAuthModal === "function") window.__shougOpenAuthModal();
          }, { once: true });
        }
      }
      return;
    }
    loaded = true;
    try { localStorage.setItem("shoug-account-activated", "true"); } catch (error) { }
    if (openWhenReady) {
      window.addEventListener("shoug:fb", function () {
        setTimeout(function () {
          if (typeof window.__shougOpenAuthModal === "function") {
            window.__shougOpenAuthModal();
            return;
          }
          var readyButton = document.getElementById("shoug-fb-user");
          if (readyButton && !readyButton.hasAttribute("data-account-loader")) readyButton.click();
        }, 0);
      }, { once: true });
    }
    var s = document.createElement("script");
    s.src = "/javascripts/firebase-auth.js?v=61";
    s.async = true;
    document.head.appendChild(s);
  }
  window.__shougLoadFirebaseAuth = loadFirebase;
  window.addEventListener("shoug:load-account", function (event) {
    loadFirebase(!!(event.detail && event.detail.open));
  });

  var actions = document.querySelector(".shoug-header-actions");
  if (!actions) {
    if (/^\/(?:account|community|bookmarks)(?:\/|$)/.test(window.location.pathname)) loadFirebase(false);
    return;
  }
  var accountActivated = false;
  try { accountActivated = localStorage.getItem("shoug-account-activated") === "true"; } catch (error) { }

  var style = document.getElementById("shoug-auth-placeholder-style");
  if (!style) {
    style = document.createElement("style");
    style.id = "shoug-auth-placeholder-style";
    style.textContent = ".shoug-auth-btn{height:34px;display:inline-flex;align-items:center;padding:0 14px;border:1px solid rgba(184,41,234,.5);background:transparent;color:#c940f5;font-family:'SFMono-Regular',Consolas,monospace;font-size:.65rem;font-weight:800;letter-spacing:.14em;text-transform:uppercase;cursor:pointer}";
    document.head.appendChild(style);
  }

  var accountButton = document.getElementById("shoug-fb-user");
  if (!accountButton) {
    accountButton = document.createElement("button");
    accountButton.id = "shoug-fb-user";
    accountButton.className = "shoug-auth-btn";
    accountButton.type = "button";
    accountButton.textContent = "Sign In";
    actions.insertBefore(accountButton, actions.firstChild);
  }
  accountButton.setAttribute("data-account-loader", "");

  accountButton.addEventListener("click", function () { loadFirebase(true); }, { once: true });
  actions.addEventListener("pointerover", function () { loadFirebase(false); }, { once: true, passive: true });
  actions.addEventListener("focusin", function () { loadFirebase(false); }, { once: true });
  if (accountActivated) {
    loadFirebase(false);
  } else {
    setTimeout(function () { loadFirebase(false); }, 15000);
  }
})();
