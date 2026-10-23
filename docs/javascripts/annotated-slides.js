/* Annotated slides: view modes, annotation toggle, past-exam filter and the
   exam-radar questions. Markup is rendered by scripts/build_se423_annotated_slides.py. */
(function () {
  "use strict";

  var root = document.documentElement;
  var body = document.body;
  var sheets = Array.prototype.slice.call(document.querySelectorAll(".sheet"));
  var jump = document.getElementById("as-jump");
  var prevBtn = document.getElementById("flip-prev");
  var nextBtn = document.getElementById("flip-next");
  var posText = document.getElementById("flip-text");
  var posFill = document.getElementById("flip-fill");
  var emptyMsg = document.getElementById("as-empty");
  var current = 0;

  function load(key, fallback) {
    try {
      var v = localStorage.getItem(key);
      return v === null ? fallback : v;
    } catch (e) {
      return fallback;
    }
  }

  function save(key, value) {
    try {
      localStorage.setItem(key, value);
    } catch (e) {}
  }

  /* ---------------------------------------------------------------- theme */
  var themeBtn = document.getElementById("as-theme");

  function applyTheme(t) {
    root.setAttribute("data-theme", t);
    if (themeBtn) {
      themeBtn.textContent = t === "light" ? "☾ Dark" : "☀︎ Light";
      themeBtn.setAttribute("aria-label", "Switch to " + (t === "light" ? "dark" : "light") + " theme");
    }
  }

  var storedTheme = load("shoug-theme", null);
  var prefersLight = window.matchMedia && window.matchMedia("(prefers-color-scheme: light)").matches;
  applyTheme(storedTheme === "light" || storedTheme === "dark" ? storedTheme : prefersLight ? "light" : "dark");
  if (themeBtn) {
    themeBtn.addEventListener("click", function () {
      var t = root.getAttribute("data-theme") === "light" ? "dark" : "light";
      applyTheme(t);
      save("shoug-theme", t);
    });
  }

  /* -------------------------------------------------------------- helpers */
  function visible() {
    return sheets.filter(function (s) {
      return !s.hidden;
    });
  }

  function setPressed(group, value) {
    document.querySelectorAll('[data-group="' + group + '"]').forEach(function (b) {
      b.setAttribute("aria-pressed", String(b.getAttribute("data-value") === value));
    });
  }

  function updateFlipBar() {
    var list = visible();
    var i = list.indexOf(sheets[current]);
    if (posText) posText.textContent = list.length ? "Slide " + sheets[current].getAttribute("data-n") + " · " + (i + 1) + " / " + list.length : "No slides";
    if (posFill) posFill.style.width = list.length ? ((i + 1) / list.length) * 100 + "%" : "0";
    if (prevBtn) prevBtn.disabled = i <= 0;
    if (nextBtn) nextBtn.disabled = i < 0 || i >= list.length - 1;
    if (jump) jump.value = sheets[current] ? sheets[current].id : "";
  }

  // window.scrollTo stays inside this document; scrollIntoView would also scroll the
  // site wrapper that embeds the deck in an iframe.
  function scrollToSheet(sheet, behavior) {
    var bar = document.querySelector(".as-top");
    var offset = bar && getComputedStyle(bar).position === "sticky" ? bar.offsetHeight + 12 : 10;
    window.scrollTo({ top: Math.max(0, sheet.getBoundingClientRect().top + window.pageYOffset - offset), behavior: behavior });
  }

  function show(index, direction, scroll) {
    if (index < 0 || index >= sheets.length) return;
    var prev = sheets[current];
    current = index;
    var sheet = sheets[current];
    if (body.classList.contains("mode-flip")) {
      if (prev) prev.classList.remove("is-current", "turn-next", "turn-prev");
      sheet.classList.add("is-current");
      sheet.classList.remove("turn-next", "turn-prev");
      if (direction) {
        void sheet.offsetWidth;
        sheet.classList.add(direction > 0 ? "turn-next" : "turn-prev");
      }
      if (scroll !== false) scrollToSheet(sheet, "auto");
    } else if (scroll !== false) {
      scrollToSheet(sheet, "smooth");
    }
    // Inside the site wrapper's iframe a hash change scrolls the parent page, so only
    // keep the URL in sync when the deck is opened on its own.
    if (scroll !== false && window.top === window && history.replaceState) history.replaceState(null, "", "#" + sheet.id);
    updateFlipBar();
  }

  function step(delta) {
    var list = visible();
    var i = list.indexOf(sheets[current]);
    var target = list[i + delta];
    if (target) show(sheets.indexOf(target), delta);
  }

  /* ----------------------------------------------------------- view mode */
  function setMode(mode, scroll) {
    body.classList.toggle("mode-flip", mode === "flip");
    body.classList.toggle("mode-scroll", mode !== "flip");
    setPressed("mode", mode);
    save("as-mode", mode);
    sheets.forEach(function (s) {
      s.classList.remove("is-current", "turn-next", "turn-prev");
    });
    if (sheets[current] && sheets[current].hidden) current = sheets.indexOf(visible()[0] || sheets[0]);
    if (mode === "flip" && sheets[current]) sheets[current].classList.add("is-current");
    show(current, 0, scroll !== false);
  }

  document.querySelectorAll('[data-group="mode"]').forEach(function (b) {
    b.addEventListener("click", function () {
      setMode(b.getAttribute("data-value"));
    });
  });

  /* --------------------------------------------------------- annotations */
  var annBtn = document.getElementById("as-ann");

  function setAnn(on) {
    body.classList.toggle("no-ann", !on);
    if (annBtn) {
      annBtn.setAttribute("aria-pressed", String(on));
      annBtn.textContent = on ? "✎ Notes on" : "✎ Notes off";
    }
    save("as-ann", on ? "on" : "off");
  }

  if (annBtn) {
    annBtn.addEventListener("click", function () {
      setAnn(body.classList.contains("no-ann"));
    });
  }

  /* -------------------------------------------------------------- filter */
  function setFilter(f) {
    sheets.forEach(function (s) {
      s.hidden = f === "past" && s.getAttribute("data-past") !== "1";
    });
    setPressed("filter", f);
    if (jump) {
      Array.prototype.forEach.call(jump.options, function (o) {
        var s = document.getElementById(o.value);
        o.hidden = o.disabled = !!(s && s.hidden);
      });
    }
    if (emptyMsg) emptyMsg.hidden = visible().length > 0;
    var list = visible();
    if (list.length && sheets[current].hidden) {
      show(sheets.indexOf(list[0]), 0, body.classList.contains("mode-flip"));
    } else {
      setMode(body.classList.contains("mode-flip") ? "flip" : "scroll");
    }
  }

  document.querySelectorAll('[data-group="filter"]').forEach(function (b) {
    b.addEventListener("click", function () {
      setFilter(b.getAttribute("data-value"));
    });
  });

  /* ---------------------------------------------------------- navigation */
  if (jump) {
    jump.addEventListener("change", function () {
      var s = document.getElementById(jump.value);
      if (s) show(sheets.indexOf(s), 0);
    });
  }
  if (prevBtn) prevBtn.addEventListener("click", function () { step(-1); });
  if (nextBtn) nextBtn.addEventListener("click", function () { step(1); });

  document.addEventListener("keydown", function (e) {
    if (!body.classList.contains("mode-flip")) return;
    var tag = (e.target && e.target.tagName) || "";
    if (/INPUT|SELECT|TEXTAREA/.test(tag) || e.altKey || e.ctrlKey || e.metaKey) return;
    if (e.key === "ArrowRight" || e.key === "PageDown") {
      e.preventDefault();
      step(1);
    } else if (e.key === "ArrowLeft" || e.key === "PageUp") {
      e.preventDefault();
      step(-1);
    }
  });

  var touchX = null;
  var touchY = null;
  document.addEventListener("touchstart", function (e) {
    if (!body.classList.contains("mode-flip") || e.touches.length !== 1) return;
    touchX = e.touches[0].clientX;
    touchY = e.touches[0].clientY;
  }, { passive: true });
  document.addEventListener("touchend", function (e) {
    if (touchX === null) return;
    var dx = e.changedTouches[0].clientX - touchX;
    var dy = e.changedTouches[0].clientY - touchY;
    touchX = null;
    if (Math.abs(dx) > 60 && Math.abs(dx) > Math.abs(dy) * 1.5) step(dx < 0 ? 1 : -1);
  }, { passive: true });

  // In-deck links (#s-N) work in both modes.
  document.addEventListener("click", function (e) {
    var a = e.target.closest && e.target.closest('a[href^="#s-"]');
    if (!a) return;
    var s = document.getElementById(a.getAttribute("href").slice(1));
    if (!s) return;
    e.preventDefault();
    if (s.hidden) setFilter("all");
    show(sheets.indexOf(s), 0);
  });

  // Track the slide in view while scrolling so the jump menu and position stay in sync.
  if ("IntersectionObserver" in window) {
    var io = new IntersectionObserver(function (entries) {
      if (body.classList.contains("mode-flip")) return;
      entries.forEach(function (en) {
        if (en.isIntersecting) {
          current = sheets.indexOf(en.target);
          if (jump) jump.value = en.target.id;
        }
      });
    }, { rootMargin: "-30% 0px -60% 0px" });
    sheets.forEach(function (s) { io.observe(s); });
  }

  /* --------------------------------------------------------- exam radar */
  document.querySelectorAll(".q").forEach(function (q) {
    var why = q.querySelector(".why");
    q.querySelectorAll(".opt").forEach(function (btn) {
      btn.addEventListener("click", function () {
        var right = btn.getAttribute("data-right") === "1";
        btn.classList.add(right ? "right" : "wrong");
        btn.disabled = true;
        if (right) {
          q.querySelectorAll(".opt").forEach(function (o) { o.disabled = true; });
          if (why) why.hidden = false;
        }
      });
    });
    var reveal = q.querySelector(".reveal");
    if (reveal) {
      reveal.addEventListener("click", function () {
        var open = why.hidden;
        why.hidden = !open;
        reveal.textContent = open ? "Hide model answer" : "Show model answer";
        reveal.setAttribute("aria-expanded", String(open));
      });
    }
  });

  /* ---------------------------------------------------------------- start */
  setAnn(load("as-ann", "on") !== "off");
  var start = location.hash ? document.getElementById(location.hash.slice(1)) : null;
  current = start && sheets.indexOf(start) >= 0 ? sheets.indexOf(start) : 0;
  setMode(load("as-mode", "scroll") === "flip" ? "flip" : "scroll", !!start);
})();
