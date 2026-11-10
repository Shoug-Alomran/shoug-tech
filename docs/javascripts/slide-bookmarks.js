/* Bookmarks for single slides, on Annotated Slides decks and regular slide (PDF) pages.
   A bookmark is a document in userProgress/{uid}/pages, the same place page bookmarks live,
   so it also appears on /bookmarks/. Its url carries the slide: #slide-12, #s-12 or #page-12. */
(function () {
  "use strict";
  if (window.__slideBookmarks) return;
  window.__slideBookmarks = true;

  var cards = Array.prototype.slice.call(
    document.querySelectorAll(
      "section.card[data-slide], article.sheet[data-n]",
    ),
  );
  var pdfHost = /\/slides\//.test(location.pathname)
    ? document.querySelector(".pdf-embed")
    : null;
  if (!cards.length && !pdfHost) return;

  var rootWindow = window;
  try {
    if (window.top !== window.self && window.top.location.href)
      rootWindow = window.top;
  } catch (e) {}

  var pagePath = rootWindow.location.pathname.replace(/[^/]+\.html$/, "");
  var docPrefix = pagePath.replace(/\//g, "|").replace(/^\||\|$/g, "");
  var saved = {};
  var user = null;
  var db = null;
  var fb = null;
  var authKnown = false; // false until Firebase has reported the real sign-in state
  var pending = null; // a click made before that, finished once it is known
  var connecting = false;
  var listLoaded = false;
  var connectFailed = false;
  var giveUpTimer = null;

  var CSS =
    "html{--sb-bg:#fff;--sb-ink:#1d1d1f;--sb-muted:#5b5b63;--sb-line:#cfcdc7;--sb-accent:#2f5bb7;--sb-accent-ink:#fff}" +
    'html[data-theme="dark"]{--sb-bg:#1b1c20;--sb-ink:#ecebe8;--sb-muted:#a9a8b0;--sb-line:#3a3c44;--sb-accent:#8fb0ff;--sb-accent-ink:#0d1220}' +
    ".sb-btn{appearance:none;display:inline-flex;align-items:center;gap:6px;min-height:32px;padding:4px 10px;border:1px solid var(--sb-line);border-radius:8px;background:var(--sb-bg);color:var(--sb-ink);font:inherit;font-size:13px;font-weight:600;line-height:1.2;cursor:pointer;white-space:nowrap}" +
    ".sb-btn svg{width:13px;height:13px;flex:none;fill:none;stroke:currentColor;stroke-width:2}" +
    '.sb-btn[aria-pressed="true"]{background:var(--sb-accent);border-color:var(--sb-accent);color:var(--sb-accent-ink)}' +
    '.sb-btn[aria-pressed="true"] svg{fill:currentColor}' +
    ".sb-btn:hover{border-color:var(--sb-accent)}" +
    ".sb-btn:focus-visible,.sb-input:focus-visible{outline:2px solid var(--sb-accent);outline-offset:2px}" +
    ".card-head .sb-btn{margin-left:auto}.card-head .sb-btn+.note-toggle{margin-left:0}" +
    ".margin>.sb-btn{margin-bottom:10px}" +
    ".sb-saved{position:relative;display:inline-flex}" +
    ".sb-list{position:absolute;z-index:50;top:calc(100% + 6px);right:0;width:min(340px,calc(100vw - 24px));max-height:60vh;overflow:auto;background:var(--sb-bg);color:var(--sb-ink);border:1px solid var(--sb-line);border-radius:10px;box-shadow:0 12px 32px rgba(0,0,0,.22);font-size:14px;text-align:left}" +
    ".sb-list[hidden]{display:none}" +
    ".sb-list button{display:block;width:100%;padding:10px 14px;border:0;border-bottom:1px solid var(--sb-line);border-radius:0;background:none;color:inherit;font:inherit;text-align:left;white-space:normal;cursor:pointer}" +
    ".sb-list button:hover{background:var(--sb-line)}" +
    ".sb-list p{margin:0;padding:12px 14px;color:var(--sb-muted)}" +
    ".sb-toast{position:fixed;z-index:80;left:50%;bottom:20px;transform:translateX(-50%);max-width:calc(100vw - 24px);padding:10px 14px;border-radius:8px;background:#16111f;color:#fff;font-size:14px;box-shadow:0 8px 24px rgba(0,0,0,.3)}" +
    ".sb-bar{display:flex;flex-wrap:wrap;align-items:center;gap:8px;padding:10px 12px;margin:0 0 8px;border:1px solid var(--sb-line);border-radius:8px;background:var(--sb-bg);color:var(--sb-ink);font-size:13px}" +
    ".sb-bar label{font-weight:600}" +
    ".sb-input{box-sizing:border-box;width:76px;min-height:32px;padding:4px 8px;border:1px solid var(--sb-line);border-radius:8px;background:var(--sb-bg);color:var(--sb-ink);font:inherit;font-size:16px}" +
    ".sb-chips{display:flex;flex-wrap:wrap;gap:6px}" +
    ".sb-chip{display:inline-flex;border:1px solid var(--sb-line);border-radius:8px;overflow:hidden}" +
    ".sb-chip button{appearance:none;min-height:32px;padding:4px 8px;border:0;background:none;color:inherit;font:inherit;font-size:13px;cursor:pointer}" +
    ".sb-chip button:hover{background:var(--sb-line)}" +
    "@media print{.sb-btn,.sb-saved,.sb-bar,.sb-toast{display:none}}";

  function addStyles() {
    var style = document.createElement("style");
    style.textContent = pdfHost
      ? CSS +
        "body{--sb-bg:#110822;--sb-ink:#f8f7fb;--sb-muted:#a09fa6;--sb-line:rgba(255,255,255,.18);--sb-accent:#d978ff;--sb-accent-ink:#110822}" +
        "body.shoug-light-mode{--sb-bg:#fff;--sb-ink:#16111f;--sb-muted:#534a61;--sb-line:rgba(22,17,31,.2);--sb-accent:#8a1fb5;--sb-accent-ink:#fff}"
      : CSS;
    document.head.appendChild(style);
  }

  var ICON =
    '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M6 3h12v18l-6-4.5L6 21z"/></svg>';
  var toastTimer = null;

  function toast(text) {
    var el = document.querySelector(".sb-toast");
    if (!el) {
      el = document.createElement("div");
      el.className = "sb-toast";
      el.setAttribute("role", "status");
      document.body.appendChild(el);
    }
    el.textContent = text;
    clearTimeout(toastTimer);
    toastTimer = setTimeout(function () {
      el.remove();
    }, 3200);
  }

  // Firebase lives in the course page, and rejects objects created in this frame.
  function plain(values) {
    var out = new rootWindow.Object();
    Object.keys(values).forEach(function (k) {
      out[k] = values[k];
    });
    return out;
  }

  function pagesRef() {
    return db.collection("userProgress").doc(user.uid).collection("pages");
  }

  function deckTitle() {
    return document.title
      .replace(/^SHOUG\.TECH\s*(\||\/\/|-)\s*/, "")
      .replace(/\s*·\s*Annotated Slides/, "");
  }

  function save(n, label, anchor, on) {
    if (!canLoadAccount()) {
      // This deck was opened on its own, without the course page that holds the login.
      rootWindow.location.href = pagePath + "#" + anchor + n;
      return false;
    }
    if (connectFailed) {
      toast("Couldn’t reach your account. Reload the page and try again.");
      return false;
    }
    if (!authKnown || (user && !listLoaded)) {
      pending = function () {
        save(n, label, anchor, on);
      };
      toast("Connecting to your account…");
      loadAccount();
      return false;
    }
    if (!user) {
      toast("Sign in to bookmark slides.");
      return false;
    }
    function undo() {
      toast("That bookmark didn’t save. Try again.");
      if (on) delete saved[n];
      else saved[n] = label || true;
      refresh();
    }
    try {
      var ref = pagesRef().doc(docPrefix + "|slide-" + n);
      var data = on
        ? plain({
            url: pagePath + "#" + anchor + n,
            title: deckTitle() + " · Slide " + n + (label ? ": " + label : ""),
            bookmarked: true,
            bookmarkFolder: null,
            bookmarkSavedAt: fb.firestore.FieldValue.serverTimestamp(),
          })
        : plain({ bookmarked: false });
      ref.set(data, plain({ merge: true })).catch(undo);
    } catch (e) {
      undo();
      return false;
    }
    if (on) saved[n] = label || true;
    else delete saved[n];
    refresh();
    return true;
  }

  /* ------------------------------------------------------- annotated decks */
  var savedBtn = null;
  var savedList = null;

  function cardNumber(card) {
    return +(card.getAttribute("data-slide") || card.getAttribute("data-n"));
  }

  function cardLabel(card) {
    var h = card.querySelector("h3,h2");
    return h ? h.textContent.trim() : "";
  }

  function anchorPrefix(card) {
    return card.id.replace(/\d+$/, "");
  }

  function setButton(btn, on) {
    btn.setAttribute("aria-pressed", on ? "true" : "false");
    btn.innerHTML = ICON + (on ? "Bookmarked" : "Bookmark");
  }

  function goToCard(card) {
    if (savedList) savedList.hidden = true;
    if (card.hidden) {
      var all = document.querySelector(
        '[data-group="filter"][data-value="all"]',
      );
      if (all) all.click();
    }
    var flip =
      document.body.classList.contains("flip") ||
      document.body.classList.contains("mode-flip");
    if (flip) {
      var jump = document.getElementById("as-jump");
      if (jump) {
        jump.value = card.id;
        jump.dispatchEvent(new Event("change", { bubbles: true }));
      } else {
        var a = document.createElement("a");
        a.href = "#" + card.id;
        document.body.appendChild(a);
        a.click();
        a.remove();
      }
      return;
    }
    var bar = document.querySelector(".top,.as-top");
    var offset =
      bar && getComputedStyle(bar).position === "sticky"
        ? bar.offsetHeight + 12
        : 10;
    window.scrollTo(
      0,
      Math.max(
        0,
        card.getBoundingClientRect().top + window.pageYOffset - offset,
      ),
    );
  }

  function buildDeck() {
    cards.forEach(function (card) {
      var btn = document.createElement("button");
      btn.type = "button";
      btn.className = "sb-btn";
      btn.setAttribute("data-sb-n", cardNumber(card));
      setButton(btn, false);
      btn.addEventListener("click", function () {
        var n = cardNumber(card);
        save(n, cardLabel(card), anchorPrefix(card), !saved[n]);
      });
      var head = card.querySelector(".card-head");
      var margin = card.querySelector(".margin");
      if (head) head.insertBefore(btn, head.querySelector(".note-toggle"));
      else if (margin) margin.insertBefore(btn, margin.firstChild);
      else card.insertBefore(btn, card.firstChild);
    });
    var controls = document.querySelector(".controls,.as-controls");
    if (!controls) return;
    var wrap = document.createElement("div");
    wrap.className = "sb-saved";
    savedBtn = document.createElement("button");
    savedBtn.type = "button";
    savedBtn.className = "sb-btn";
    savedBtn.setAttribute("aria-expanded", "false");
    savedList = document.createElement("div");
    savedList.className = "sb-list";
    savedList.hidden = true;
    savedBtn.addEventListener("click", function () {
      savedList.hidden = !savedList.hidden;
      savedBtn.setAttribute(
        "aria-expanded",
        savedList.hidden ? "false" : "true",
      );
      if (!savedList.hidden) loadAccount();
    });
    document.addEventListener("click", function (ev) {
      if (!wrap.contains(ev.target)) savedList.hidden = true;
    });
    wrap.appendChild(savedBtn);
    wrap.appendChild(savedList);
    controls.appendChild(wrap);
  }

  function refreshDeck() {
    cards.forEach(function (card) {
      var n = cardNumber(card);
      var btn = card.querySelector(".sb-btn");
      if (btn) setButton(btn, !!saved[n]);
    });
    if (!savedBtn) return;
    var saved_ns = Object.keys(saved)
      .map(Number)
      .sort(function (a, b) {
        return a - b;
      });
    savedBtn.innerHTML = ICON + "Saved (" + saved_ns.length + ")";
    savedList.textContent = "";
    if (!saved_ns.length) {
      var empty = document.createElement("p");
      empty.textContent = !canLoadAccount()
        ? "Open this deck from its course page to use bookmarks."
        : connectFailed
          ? "Couldn’t reach your account. Reload the page and try again."
          : !authKnown || (user && !listLoaded)
            ? "Connecting to your account…"
            : user
              ? "No bookmarked slides in this deck yet."
              : "Sign in to bookmark slides.";
      savedList.appendChild(empty);
      return;
    }
    saved_ns.forEach(function (n) {
      var card = cards.filter(function (c) {
        return cardNumber(c) === n;
      })[0];
      if (!card) return;
      var item = document.createElement("button");
      item.type = "button";
      item.textContent =
        "Slide " + n + (cardLabel(card) ? " · " + cardLabel(card) : "");
      item.addEventListener("click", function () {
        goToCard(card);
      });
      savedList.appendChild(item);
    });
  }

  /* ---------------------------------------------------- regular PDF slides */
  var chips = null;

  function openPdfAt(n) {
    var src = pdfHost.getAttribute("data-pdf-src");
    var frame = pdfHost.querySelector("iframe");
    if (!frame) {
      var open = pdfHost.querySelector(".pdf-embed__btn");
      if (open) open.click();
      frame = pdfHost.querySelector("iframe");
    }
    if (frame && src) frame.src = src.split("#")[0] + "#page=" + n;
    pdfHost.scrollIntoView({ block: "nearest" });
  }

  function buildPdf() {
    var bar = document.createElement("div");
    bar.className = "sb-bar";
    var id = "sb-page-input";
    var label = document.createElement("label");
    label.setAttribute("for", id);
    label.textContent = "Bookmark slide";
    var input = document.createElement("input");
    input.id = id;
    input.className = "sb-input";
    input.type = "number";
    input.min = "1";
    input.inputMode = "numeric";
    input.placeholder = "No.";
    var btn = document.createElement("button");
    btn.type = "button";
    btn.className = "sb-btn";
    btn.innerHTML = ICON + "Save";
    btn.addEventListener("click", function () {
      var n = parseInt(input.value, 10);
      if (!(n >= 1)) {
        toast("Type the slide number first.");
        input.focus();
        return;
      }
      if (save(n, "", "page-", true)) input.value = "";
    });
    input.addEventListener("keydown", function (ev) {
      if (ev.key === "Enter") btn.click();
    });
    chips = document.createElement("div");
    chips.className = "sb-chips";
    bar.appendChild(label);
    bar.appendChild(input);
    bar.appendChild(btn);
    bar.appendChild(chips);
    // The viewer's parent can be a flex row, which would put the bar beside the PDF.
    var anchor = pdfHost;
    while (
      anchor.parentElement &&
      anchor.parentElement !== document.body &&
      getComputedStyle(anchor.parentElement).display.indexOf("flex") >= 0 &&
      getComputedStyle(anchor.parentElement).flexDirection.indexOf("row") === 0
    )
      anchor = anchor.parentElement;
    anchor.parentNode.insertBefore(bar, anchor);
  }

  function refreshPdf() {
    chips.textContent = "";
    Object.keys(saved)
      .map(Number)
      .sort(function (a, b) {
        return a - b;
      })
      .forEach(function (n) {
        var chip = document.createElement("span");
        chip.className = "sb-chip";
        var go = document.createElement("button");
        go.type = "button";
        go.textContent = "Slide " + n;
        go.addEventListener("click", function () {
          openPdfAt(n);
        });
        var remove = document.createElement("button");
        remove.type = "button";
        remove.textContent = "×";
        remove.setAttribute("aria-label", "Remove bookmark for slide " + n);
        remove.addEventListener("click", function () {
          save(n, "", "page-", false);
        });
        chip.appendChild(go);
        chip.appendChild(remove);
        chips.appendChild(chip);
      });
  }

  function refresh() {
    if (pdfHost) refreshPdf();
    else refreshDeck();
  }

  /* ---------------------------------------------------------------- sign-in */
  // Calls done once the list is in, so a bookmark made meanwhile can't be overwritten by it.
  function loadSaved(done) {
    pagesRef()
      .where("bookmarked", "==", true)
      .get()
      .then(function (snap) {
        saved = {};
        snap.forEach(function (doc) {
          if (doc.id.indexOf(docPrefix + "|slide-") !== 0) return;
          var n = parseInt(doc.id.slice(docPrefix.length + 7), 10);
          if (n) saved[n] = true;
        });
        refresh();
      })
      .catch(function () {})
      .then(function () {
        listLoaded = true;
        refresh();
        done();
      });
  }

  function firebaseReady() {
    try {
      var candidate = rootWindow.__shoug_fb || rootWindow.firebase;
      if (
        candidate &&
        candidate.apps &&
        candidate.apps.length &&
        candidate.auth &&
        candidate.firestore
      )
        return candidate;
    } catch (e) {}
    return null;
  }

  function canLoadAccount() {
    try {
      return !!(
        firebaseReady() ||
        typeof rootWindow.__shougLoadFirebaseAuth === "function"
      );
    } catch (e) {
      return false;
    }
  }

  // The site loads its account code late, on purpose, so slide pages stay fast. Ask for it.
  function loadAccount() {
    if (!authKnown && !giveUpTimer) {
      giveUpTimer = setTimeout(function () {
        if (authKnown) return;
        connectFailed = true;
        pending = null;
        refresh();
      }, 20000);
    }
    try {
      if (typeof rootWindow.__shougLoadFirebaseAuth === "function")
        rootWindow.__shougLoadFirebaseAuth(false);
    } catch (e) {}
  }

  function attach() {
    if (fb) return true;
    var candidate = firebaseReady();
    if (!candidate) return false;
    fb = candidate;
    db = fb.firestore();
    fb.auth().onAuthStateChanged(function (u) {
      authKnown = true;
      connectFailed = false;
      user = u;
      listLoaded = false;
      saved = {};
      refresh();
      function finishClick() {
        if (!pending) return;
        var run = pending;
        pending = null;
        run();
      }
      if (u) loadSaved(finishClick);
      else finishClick();
    });
    return true;
  }

  function connect() {
    if (connecting) return;
    connecting = true;
    if (attach()) return;
    try {
      rootWindow.addEventListener("shoug:fb", attach);
    } catch (e) {}
    var timer = setInterval(function () {
      if (attach()) clearInterval(timer);
    }, 500);
    // Someone who has signed in here before gets their bookmarks without having to click first.
    var activated = false;
    try {
      activated = localStorage.getItem("shoug-account-activated") === "true";
    } catch (e) {}
    if (activated) loadAccount();
  }

  function start() {
    addStyles();
    if (pdfHost) {
      buildPdf();
      var match = /^#page-(\d+)$/.exec(location.hash);
      if (match)
        setTimeout(function () {
          openPdfAt(+match[1]);
        }, 300);
    } else {
      buildDeck();
    }
    refresh();
    connect();
  }

  if (document.readyState === "loading")
    document.addEventListener("DOMContentLoaded", start);
  else start();
})();
