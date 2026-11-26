/* Read aloud for Annotated Slides decks and slide breakdowns.
   Uses the browser's own speech (Web Speech API): no server, no key, nothing leaves the device.

   Annotated decks: each slide card gets a Listen button. It reads the slide itself (the text of
   its PDF page, embedded by scripts/build_slide_speech.py), not the notes, then goes on to the next slide.
   Breakdowns: the lesson is split at its h2 headings. Each heading gets a Listen button, and only
   what is on screen is read: translated text when Arabic is showing, closed panels are skipped.
   The floating Listen button starts from wherever the reader is on the page. */
(function () {
  "use strict";
  if (window.__slideReader) return;
  window.__slideReader = true;

  var synth = window.speechSynthesis;
  if (!synth || typeof window.SpeechSynthesisUtterance === "undefined") return;
  // Breakdown wrapper pages only hold the lesson in an iframe; the lesson file runs its own copy.
  if (
    /\/(?:index\.html)?$/.test(location.pathname) &&
    !document.querySelector("section.card[data-slide]")
  )
    return;

  var deckCards = [].slice.call(
    document.querySelectorAll("section.card[data-slide]"),
  );
  var mode = deckCards.length
    ? "deck"
    : /\/slide-breakdowns\//.test(location.pathname)
      ? "breakdown"
      : "";
  if (!mode) return;

  /* ------------------------------------------------------------------ text */
  var UI =
    ".sr-ui,.sb-btn,.sb-saved,.sb-toast,.bd-language,.bd-contents,.sg-ai-panel,.sg-ai-launch,.sg-page-search,.sys-time,.sfx-lightbox";
  var BREAK = "\u2028"; // a <br>: a pause inside one block
  var SKIP_COMMON =
    "script,style,noscript,template,svg,canvas,iframe,video,audio,img,button,select,textarea,input,nav,annotation," +
    '[hidden],[aria-hidden="true"],' +
    UI;
  // In a slide card: no header (read separately), no slide image, no answers or feedback.
  var SKIP_BREAKDOWN = SKIP_COMMON + ",footer";

  var BLOCK = {
    P: 1,
    DIV: 1,
    LI: 1,
    UL: 1,
    OL: 1,
    H1: 1,
    H2: 1,
    H3: 1,
    H4: 1,
    H5: 1,
    H6: 1,
    TD: 1,
    TH: 1,
    TR: 1,
    TABLE: 1,
    CAPTION: 1,
    FIGCAPTION: 1,
    FIGURE: 1,
    DT: 1,
    DD: 1,
    DL: 1,
    BLOCKQUOTE: 1,
    SECTION: 1,
    ARTICLE: 1,
    HEADER: 1,
    MAIN: 1,
    ASIDE: 1,
    PRE: 1,
    SUMMARY: 1,
    DETAILS: 1,
    LABEL: 1,
    BUTTON: 1,
  };

  function isVisible(el) {
    if (el.checkVisibility) {
      if (el.checkVisibility({ visibilityProperty: true })) return true;
      return getComputedStyle(el).display === "contents";
    }
    return (
      el.getClientRects().length > 0 ||
      getComputedStyle(el).display === "contents"
    );
  }

  function blockOf(el, scope) {
    while (el && el !== scope && !BLOCK[el.tagName]) el = el.parentElement;
    return el || scope;
  }

  /* Text from `start` up to (not including) `end`, in reading order, as blocks [{el, text}]. */
  function collect(scope, start, end, skipSel, visibleOnly) {
    var items = [];
    var started = false;
    var done = false;
    var lastParent = null;
    function add(el, text, parent) {
      var last = items[items.length - 1];
      if (last && last.el === el) {
        // <span>Prediction</span><span>Q1</span> must not run together as one word.
        if (
          parent !== lastParent &&
          !/\s$/.test(last.text) &&
          !/^\s/.test(text)
        )
          text = " " + text;
        last.text += text;
      } else items.push({ el: el, text: text });
      lastParent = parent;
    }
    function skip(el) {
      return el.matches(skipSel) || (visibleOnly && !isVisible(el));
    }
    function walk(node) {
      if (done) return;
      if (node === end) {
        done = true;
        return;
      }
      if (node.nodeType === 3) {
        if (!started) return;
        var p = node.parentElement;
        // Source line wraps are not pauses: only blocks and <br> are.
        var text = node.nodeValue.replace(/\s+/g, " ");
        // "Tip" / "A" labels run into the text after them; give them a pause.
        if (p.matches(".kind,.ltr") && text.trim()) text = text.trim() + ": ";
        add(blockOf(p, scope), text, p);
        return;
      }
      if (node.nodeType !== 1) return;
      if (node === start) started = true;
      else if (!started && !node.contains(start)) return;
      else if (started && skip(node)) return;
      if (started && node.tagName === "BR") {
        add(blockOf(node.parentElement, scope), BREAK, node);
        return;
      }
      if (started && node.matches("pre,.code-block")) {
        // Code read symbol by symbol is noise; say it is there instead.
        items.push({
          el: node,
          text: isArabic()
            ? "مثال برمجي معروض على الشاشة."
            : "Code example on screen.",
        });
        return;
      }
      for (var c = node.firstChild; c && !done; c = c.nextSibling) walk(c);
    }
    walk(scope);
    return items;
  }

  function speakable(text) {
    return text
      .replace(/[\p{Extended_Pictographic}️‍]/gu, " ")
      .replace(/§\s*(?=\d)/g, "section ")
      .replace(/§/g, " ")
      .replace(/\s*[·•▸▪]\s*/g, ", ")
      .replace(/\s*(?:→|->|⇒|=>)\s*/g, " to ")
      .replace(/\s*(?:←|<-)\s*/g, " from ")
      .replace(/[✓✔]/g, " yes ")
      .replace(/[✗✘]/g, " no ")
      .replace(/\s+/g, " ")
      .replace(/\s+([,.;:!?،؟])/g, "$1")
      .trim();
  }

  // One utterance per block, long blocks split at sentences: Chrome cuts off long utterances.
  function toChunks(items) {
    var out = [];
    var lastShort = false;
    items.forEach(function (item) {
      item.text.split(BREAK).forEach(function (line) {
        var text = speakable(line);
        if (!text || !/[\p{L}\p{N}]/u.test(text)) return;
        // Runs of tiny cells (diagram labels, table numbers) read as one list, not a sentence each.
        var short = text.length <= 4;
        var prev = out[out.length - 1];
        if (short && lastShort && prev && prev.text.length < 180) {
          prev.text =
            prev.text.replace(/[.]$/, "") +
            ", " +
            text.replace(/[.]$/, "") +
            ".";
          return;
        }
        lastShort = short;
        if (!/[.!?:;,؟،…]$/.test(text)) text += ".";
        text
          .replace(/([.!?؟])\s+/g, "$1\u0000")
          .split("\u0000")
          .forEach(function (sentence) {
            while (sentence.length > 220) {
              var cut = sentence.lastIndexOf(", ", 220);
              if (cut < 60) cut = sentence.lastIndexOf(" ", 220);
              if (cut < 60) cut = 220;
              out.push({ el: item.el, text: sentence.slice(0, cut + 1) });
              sentence = sentence.slice(cut + 1).trim();
            }
            var last = out[out.length - 1];
            if (
              last &&
              last.el === item.el &&
              last.text.length + sentence.length < 200
            )
              last.text += " " + sentence;
            else if (sentence) out.push({ el: item.el, text: sentence });
          });
      });
    });
    return out;
  }

  /* -------------------------------------------------------------- segments */
  var segments = [];

  function cardTitle(card) {
    var h = card.querySelector(".card-head h3, h3");
    return h
      ? h.textContent
          .replace(/§(?!\s*\d)/g, " ")
          .replace(/\s+/g, " ")
          .replace(/\s+([,.;:!?])/g, "$1")
          .replace(/[\s.]+$/, "")
          .trim()
      : "";
  }

  // Each slide is a picture of a PDF page; scripts/build_slide_speech.py embeds the page text.
  var speech = null;
  function slideSpeech() {
    if (speech === null) {
      speech = {};
      var data = document.getElementById("slide-speech");
      try {
        if (data) speech = JSON.parse(data.textContent).slides || {};
      } catch (e) {}
    }
    return speech;
  }

  if (mode === "deck") {
    deckCards.forEach(function (card) {
      var n = card.getAttribute("data-slide");
      var head = card.querySelector(".card-head") || card;
      segments.push({
        anchor: card,
        mark: card,
        label: "Slide " + n + (cardTitle(card) ? ": " + cardTitle(card) : ""),
        host: head,
        // The slide itself, not the study notes beside it.
        chunks: function () {
          var lines = slideSpeech()[n] || [];
          var figure = card.querySelector("figure.slide") || card;
          var items = [{ el: head, text: "Slide " + n + "." }];
          if (lines.length) items.push({ el: figure, text: lines.join(BREAK) });
          else {
            var title = /^slide\s*\d+$/i.test(cardTitle(card))
              ? ""
              : cardTitle(card);
            items.push({
              el: figure,
              text: (title ? title + "." + BREAK : "") + t("picture"),
            });
          }
          return toChunks(items);
        },
      });
    });
  } else {
    var root = document.querySelector("main") || document.body;
    var heads = [].slice.call(root.querySelectorAll("h2")).filter(function (h) {
      return !h.closest("nav,footer," + UI);
    });
    var h1 = root.querySelector("h1") || document.querySelector("h1");
    var addSeg = function (start, end, label, host) {
      segments.push({
        anchor: start,
        mark: start,
        label: label,
        host: host,
        chunks: function () {
          var scope = root.contains(start) ? root : document.body;
          return toChunks(collect(scope, start, end, SKIP_BREAKDOWN, true));
        },
      });
    };
    var cleanLabel = function (el) {
      return el ? el.textContent.replace(/\s+/g, " ").trim() : "";
    };
    if (
      h1 &&
      (!heads.length ||
        h1.compareDocumentPosition(heads[0]) & Node.DOCUMENT_POSITION_FOLLOWING)
    )
      addSeg(h1, heads[0] || null, cleanLabel(h1), null);
    else if (!heads.length) addSeg(root, null, document.title, null);
    heads.forEach(function (h, i) {
      addSeg(h, heads[i + 1] || null, cleanLabel(h), h);
    });
  }
  if (!segments.length) return;

  /* ---------------------------------------------------------------- voices */
  var LS = {
    get: function (k) {
      try {
        return localStorage.getItem(k);
      } catch (e) {
        return null;
      }
    },
    set: function (k, v) {
      try {
        localStorage.setItem(k, v);
      } catch (e) {}
    },
  };
  var rate = parseFloat(LS.get("shoug-reader-rate")) || 1;

  function isArabic() {
    return /^ar/i.test(document.documentElement.lang || "");
  }

  function langOf(text) {
    return /[؀-ۿ]/.test(text) ? "ar" : "en";
  }

  function voicesFor(lang) {
    return synth.getVoices().filter(function (v) {
      return (v.lang || "").toLowerCase().replace("_", "-").indexOf(lang) === 0;
    });
  }

  function bestVoice(lang) {
    var list = voicesFor(lang);
    if (!list.length) return null;
    var want = LS.get("shoug-reader-voice-" + lang);
    for (var i = 0; i < list.length; i++)
      if (list[i].name === want) return list[i];
    function score(v) {
      var s = 0;
      if (/natural|neural|online|premium|enhanced/i.test(v.name)) s += 4;
      if (/google/i.test(v.name)) s += 2;
      if (lang === "en" && /en-(us|gb)/i.test(v.lang)) s += 1;
      if (v.default) s += 1;
      return s;
    }
    return list.slice().sort(function (a, b) {
      return score(b) - score(a);
    })[0];
  }

  /* -------------------------------------------------------------------- UI */
  var TEXT = {
    en: {
      listen: "Listen",
      listening: "Listening",
      pause: "Pause",
      resume: "Resume",
      stop: "Stop",
      prev: "Previous section",
      next: "Next section",
      speed: "Speed",
      voice: "Voice",
      reading: "Reading",
      paused: "Paused",
      auto: "Default",
      noVoice:
        "This device has no voice for this language. Install one in your system speech settings.",
      start: "Listen to this page",
      here: "Listen from here",
      move: "Move the player (drag, or use the arrow keys)",
      collapse: "Collapse",
      expand: "Expand",
      hide: "Hide the player (keeps reading)",
      show: "Show the player",
      picture: "This slide is a picture with no text to read.",
    },
    ar: {
      listen: "استمع",
      listening: "يقرأ",
      pause: "إيقاف مؤقت",
      resume: "متابعة",
      stop: "إيقاف",
      prev: "القسم السابق",
      next: "القسم التالي",
      speed: "السرعة",
      voice: "الصوت",
      reading: "يقرأ الآن",
      paused: "متوقف مؤقتًا",
      auto: "تلقائي",
      noVoice:
        "لا يوجد صوت لهذه اللغة على جهازك. يمكنك تثبيته من إعدادات النطق في النظام.",
      start: "استمع إلى الصفحة",
      here: "استمع من هنا",
      move: "حرّك المشغل (اسحبه أو استخدم الأسهم)",
      collapse: "تصغير",
      expand: "توسيع",
      hide: "إخفاء المشغل (تستمر القراءة)",
      show: "إظهار المشغل",
      picture: "هذه الشريحة صورة بلا نص للقراءة.",
    },
  };
  function t(key) {
    return (isArabic() ? TEXT.ar : TEXT.en)[key];
  }

  var ICON_SPEAK =
    '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M4 9h4l5-4v14l-5-4H4z"/><path d="M16.5 8.5a5 5 0 0 1 0 7M19 6a8.5 8.5 0 0 1 0 12"/></svg>';
  var ICON_PAUSE =
    '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M8 5v14M16 5v14"/></svg>';
  var ICON_PLAY =
    '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M7 5l12 7-12 7z"/></svg>';
  var ICON_PREV =
    '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M18 6l-8 6 8 6zM6 6v12"/></svg>';
  var ICON_NEXT =
    '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M6 6l8 6-8 6zM18 6v12"/></svg>';
  var ICON_STOP =
    '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M7 7h10v10H7z"/></svg>';
  var ICON_GRIP =
    '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M9 6h.01M15 6h.01M9 12h.01M15 12h.01M9 18h.01M15 18h.01" stroke-width="3.2"/></svg>';
  var ICON_DOWN =
    '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M6 9l6 6 6-6"/></svg>';
  var ICON_UP =
    '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M6 15l6-6 6 6"/></svg>';
  var ICON_HIDE =
    '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M3 3l18 18M10.6 5.1A10 10 0 0 1 12 5c5 0 9 4.5 10 7a13 13 0 0 1-3 4.2M6.6 6.6C4.4 8 2.8 10.2 2 12c1 2.5 5 7 10 7a9.8 9.8 0 0 0 5.4-1.6M9.9 9.9a3 3 0 0 0 4.2 4.2"/></svg>';

  var CSS =
    ".sr-btn{appearance:none;display:inline-flex;align-items:center;gap:6px;min-height:32px;padding:4px 10px;border:1px solid currentColor;border-color:color-mix(in srgb,currentColor 35%,transparent);border-radius:8px;background:transparent;color:inherit;font:inherit;font-size:13px;font-weight:600;line-height:1.2;cursor:pointer;white-space:nowrap;letter-spacing:normal;text-transform:none}" +
    ".sr-btn svg,#sr-player svg,#sr-launch svg{width:14px;height:14px;flex:none;fill:none;stroke:currentColor;stroke-width:2;stroke-linejoin:round;stroke-linecap:round}" +
    ".sr-btn:hover{border-color:currentColor}" +
    '.sr-btn[aria-pressed="true"]{background:#2f5bb7;border-color:#2f5bb7;color:#fff}' +
    ".sr-btn:focus-visible,#sr-player button:focus-visible,#sr-player select:focus-visible,#sr-launch:focus-visible{outline:2px solid #8fb0ff;outline-offset:2px}" +
    ".card-head .sr-btn{margin-left:auto}.card-head .sr-btn+.sb-btn,.card-head .sr-btn+.note-toggle{margin-left:0}" +
    "h2+.sr-btn.sr-head{display:flex;width:max-content;margin:-4px 0 12px;font-size:12px;min-height:28px;padding:3px 9px;opacity:.85}" +
    ".sr-reading{outline:2px solid #6f95ff;outline-offset:6px;border-radius:4px}" +
    ".sr-now{background:rgba(111,149,255,.16);box-shadow:0 0 0 4px rgba(111,149,255,.16);border-radius:3px}" +
    "html body #sr-launch,html body #sr-player{position:fixed!important;z-index:99990!important;left:16px!important;bottom:16px!important;font:600 13px/1.3 system-ui,-apple-system,'Segoe UI',sans-serif!important;color:#fff!important;background:#16111f!important;border:1px solid rgba(255,255,255,.18)!important;border-radius:12px!important;box-shadow:0 12px 32px rgba(0,0,0,.35)!important}" +
    "html body #sr-launch{appearance:none!important;display:inline-flex!important;align-items:center!important;gap:7px!important;min-height:40px!important;padding:8px 14px!important;cursor:pointer!important}" +
    "html body #sr-launch:hover{background:#2a2140!important}" +
    "html body #sr-player{display:flex!important;flex-direction:column!important;gap:8px!important;width:min(400px,calc(100vw - 32px))!important;padding:10px 12px!important}" +
    "html body #sr-player[hidden],html body #sr-launch[hidden]{display:none!important}" +
    "html body .sr-status{display:flex!important;gap:6px!important;min-width:0!important;font-weight:500!important;color:#cfd2dc!important}" +
    "html body .sr-status b{flex:none!important;color:#fff!important}" +
    "html body .sr-status span{overflow:hidden!important;text-overflow:ellipsis!important;white-space:nowrap!important}" +
    "html body .sr-row{display:flex!important;flex-wrap:wrap!important;align-items:center!important;gap:6px!important}" +
    "html body #sr-player button{appearance:none!important;display:inline-flex!important;align-items:center!important;justify-content:center!important;min-width:36px!important;min-height:36px!important;padding:0 8px!important;border:1px solid rgba(255,255,255,.2)!important;border-radius:8px!important;background:transparent!important;color:#fff!important;font:inherit!important;cursor:pointer!important}" +
    "html body #sr-player button:hover{background:rgba(255,255,255,.1)!important}" +
    "html body #sr-player button.sr-main{background:#2f5bb7!important;border-color:#2f5bb7!important}" +
    "html body #sr-player label{display:inline-flex!important;align-items:center!important;gap:4px!important;font-weight:500!important;color:#cfd2dc!important}" +
    "html body #sr-player select{max-width:min(300px,100%)!important;min-height:32px!important;padding:2px 4px!important;border:1px solid rgba(255,255,255,.2)!important;border-radius:6px!important;background:#221b30!important;color:#fff!important;font:inherit!important;font-size:13px!important}" +
    "html body .sr-spacer{flex:1!important}" +
    "html body .sr-note{margin:0!important;font-weight:500!important;font-size:12px!important;color:#ffd38a!important}" +
    "html body .sr-top{display:flex!important;align-items:center!important;gap:6px!important;min-width:0!important}" +
    "html body .sr-top .sr-status{flex:1!important}" +
    "html body #sr-player .sr-top button{min-width:30px!important;min-height:30px!important;padding:0 6px!important;border-color:transparent!important}" +
    "html body #sr-player .sr-top button:hover{border-color:rgba(255,255,255,.2)!important}" +
    "html body #sr-player button.sr-grip{cursor:grab!important;touch-action:none!important;margin-inline-start:-4px!important;color:#9a9fb0!important}" +
    "html body #sr-player button.sr-grip:active{cursor:grabbing!important}" +
    "html body #sr-player button.sr-mini{background:#2f5bb7!important;border-color:#2f5bb7!important}" +
    "html body #sr-player .sr-mini[hidden]{display:none!important}" +
    "html body #sr-player.sr-collapsed{width:auto!important;max-width:min(340px,calc(100vw - 16px))!important;padding:6px 8px!important}" +
    "html body #sr-player.sr-collapsed .sr-row,html body #sr-player.sr-collapsed .sr-note{display:none!important}" +
    "html body #sr-launch.sr-bubble{width:46px!important;height:46px!important;min-height:0!important;padding:0!important;justify-content:center!important;border-radius:50%!important;background:#2f5bb7!important;touch-action:none!important}" +
    "html body #sr-launch.sr-bubble svg{width:20px!important;height:20px!important}" +
    "html body #sr-launch{touch-action:none!important}" +
    "html body .sr-dragging{transition:none!important;opacity:.92!important;user-select:none!important}" +
    "@media (max-width:520px){html body #sr-launch,html body #sr-player{left:8px!important;bottom:8px!important}html body #sr-player{width:calc(100vw - 16px)!important}}" +
    "@media print{.sr-btn,#sr-launch,#sr-player{display:none!important}.sr-reading{outline:0}.sr-now{background:none;box-shadow:none}}";

  var style = document.createElement("style");
  style.textContent = CSS;
  document.head.appendChild(style);

  function el(tag, cls, html) {
    var e = document.createElement(tag);
    if (cls) e.className = cls;
    if (html) e.innerHTML = html;
    e.setAttribute("translate", "no");
    return e;
  }

  // Per-section buttons.
  segments.forEach(function (seg, i) {
    var btn = el("button", "sr-btn sr-ui");
    btn.type = "button";
    seg.btn = btn;
    btn.addEventListener("click", function () {
      if (state.seg === i && state.active) togglePause();
      else play(i);
    });
    if (mode === "deck") {
      var before = seg.host.querySelector(".sb-btn, .note-toggle");
      if (before && before.parentNode === seg.host)
        seg.host.insertBefore(btn, before);
      else seg.host.appendChild(btn);
    } else if (seg.host) {
      btn.classList.add("sr-head");
      seg.host.insertAdjacentElement("afterend", btn);
    }
  });

  var launch = el("button", "sr-launch sr-ui");
  launch.id = "sr-launch";
  launch.type = "button";
  launch.addEventListener("click", function () {
    if (dragMoved) return; // that press was a drag, not a click
    if (state.active) {
      playerHidden = false; // the round button stands in for a hidden player
      paint();
      bPlay.focus();
    } else play(startIndex());
  });

  var panel = el("div", "sr-player sr-ui");
  panel.id = "sr-player";
  panel.hidden = true;
  panel.setAttribute("role", "region");
  var status = el("div", "sr-status");
  status.setAttribute("aria-live", "polite");
  var statusState = el("b");
  var statusLabel = el("span");
  status.appendChild(statusState);
  status.appendChild(statusLabel);
  var note = el("p", "sr-note");
  note.hidden = true;
  var row = el("div", "sr-row");
  var bPrev = el("button", "", ICON_PREV);
  var bPlay = el("button", "sr-main");
  var bNext = el("button", "", ICON_NEXT);
  var bStop = el("button", "", ICON_STOP);
  [bPrev, bPlay, bNext, bStop].forEach(function (b) {
    b.type = "button";
    row.appendChild(b);
  });
  row.appendChild(el("span", "sr-spacer"));
  var speedLabel = el("label");
  var speedText = el("span");
  var speed = el("select");
  [0.75, 1, 1.25, 1.5, 1.75, 2].forEach(function (r) {
    var o = document.createElement("option");
    o.value = r;
    o.textContent = r + "×";
    speed.appendChild(o);
  });
  speed.value = String(rate);
  if (speed.value !== String(rate)) speed.value = "1";
  speedLabel.appendChild(speedText);
  speedLabel.appendChild(speed);
  row.appendChild(speedLabel);
  var voiceRow = el("div", "sr-row");
  var voiceLabel = el("label");
  var voiceText = el("span");
  var voiceSel = el("select");
  voiceLabel.appendChild(voiceText);
  voiceLabel.appendChild(voiceSel);
  voiceRow.appendChild(voiceLabel);
  // Top row: drag handle, status, and (collapsed) play/pause, then collapse and hide.
  var top = el("div", "sr-top");
  var bGrip = el("button", "sr-grip", ICON_GRIP);
  var bMini = el("button", "sr-mini");
  var bFold = el("button", "sr-fold");
  var bHide = el("button", "sr-hide", ICON_HIDE);
  [bGrip, bMini, bFold, bHide].forEach(function (b) {
    b.type = "button";
  });
  top.appendChild(bGrip);
  top.appendChild(bMini);
  top.appendChild(status);
  top.appendChild(bFold);
  top.appendChild(bHide);
  panel.appendChild(top);
  panel.appendChild(row);
  panel.appendChild(voiceRow);
  panel.appendChild(note);
  document.body.appendChild(launch);
  document.body.appendChild(panel);

  bPrev.addEventListener("click", function () {
    move(-1);
  });
  bNext.addEventListener("click", function () {
    move(1);
  });
  bPlay.addEventListener("click", togglePause);
  bMini.addEventListener("click", togglePause);
  bStop.addEventListener("click", stop);
  bFold.addEventListener("click", function () {
    collapsed = !collapsed;
    LS.set("shoug-reader-collapsed", collapsed ? "1" : "0");
    paint();
    bFold.focus();
  });
  bHide.addEventListener("click", function () {
    playerHidden = true;
    paint();
    launch.focus();
  });

  /* ------------------------------------------------------------ position */
  // One spot shared by the player and the Listen button, kept between visits.
  var collapsed = LS.get("shoug-reader-collapsed") === "1";
  var playerHidden = false;
  var pos = null;
  var dragMoved = false;
  try {
    pos = JSON.parse(LS.get("shoug-reader-pos") || "null");
  } catch (e) {}

  function visibleBox() {
    return panel.hidden ? launch : panel;
  }

  function place() {
    [launch, panel].forEach(function (node) {
      if (!pos) {
        ["left", "top", "bottom", "right"].forEach(function (p) {
          node.style.removeProperty(p);
        });
        return;
      }
      node.style.setProperty("left", pos.x + "px", "important");
      node.style.setProperty("top", pos.y + "px", "important");
      node.style.setProperty("bottom", "auto", "important");
      node.style.setProperty("right", "auto", "important");
    });
    if (pos) clampInto(visibleBox());
  }

  // Keep the box fully on screen (the window shrank, or the player is bigger than the button).
  function clampInto(node) {
    if (!pos) return;
    var w = node.offsetWidth;
    var h = node.offsetHeight;
    var x = Math.max(4, Math.min(pos.x, window.innerWidth - w - 4));
    var y = Math.max(4, Math.min(pos.y, window.innerHeight - h - 4));
    if (x !== pos.x || y !== pos.y) {
      node.style.setProperty("left", x + "px", "important");
      node.style.setProperty("top", y + "px", "important");
    }
  }

  function savePos() {
    LS.set("shoug-reader-pos", JSON.stringify(pos));
  }

  function draggable(handle, box) {
    var start = null;
    handle.addEventListener("pointerdown", function (ev) {
      if (ev.button !== 0) return;
      var r = box.getBoundingClientRect();
      start = { px: ev.clientX, py: ev.clientY, x: r.left, y: r.top };
      dragMoved = false;
      try {
        handle.setPointerCapture(ev.pointerId);
      } catch (e) {}
    });
    handle.addEventListener("pointermove", function (ev) {
      if (!start) return;
      var dx = ev.clientX - start.px;
      var dy = ev.clientY - start.py;
      if (!dragMoved && Math.abs(dx) + Math.abs(dy) < 5) return;
      dragMoved = true;
      box.classList.add("sr-dragging");
      pos = {
        x: Math.round(
          Math.max(
            4,
            Math.min(start.x + dx, window.innerWidth - box.offsetWidth - 4),
          ),
        ),
        y: Math.round(
          Math.max(
            4,
            Math.min(start.y + dy, window.innerHeight - box.offsetHeight - 4),
          ),
        ),
      };
      place();
      ev.preventDefault();
    });
    function end() {
      if (!start) return;
      start = null;
      box.classList.remove("sr-dragging");
      if (dragMoved) savePos();
      // The click that follows a drag must not count as a press.
      setTimeout(function () {
        dragMoved = false;
      }, 0);
    }
    handle.addEventListener("pointerup", end);
    handle.addEventListener("pointercancel", end);
  }
  draggable(bGrip, panel);
  draggable(launch, launch);

  // Arrow keys on the handle move the player too (Shift for bigger steps).
  bGrip.addEventListener("keydown", function (ev) {
    var step = ev.shiftKey ? 40 : 10;
    var d = {
      ArrowLeft: [-step, 0],
      ArrowRight: [step, 0],
      ArrowUp: [0, -step],
      ArrowDown: [0, step],
    }[ev.key];
    if (!d) return;
    var r = panel.getBoundingClientRect();
    pos = { x: Math.round(r.left + d[0]), y: Math.round(r.top + d[1]) };
    place();
    var now = panel.getBoundingClientRect();
    pos = { x: Math.round(now.left), y: Math.round(now.top) };
    savePos();
    ev.preventDefault();
  });
  window.addEventListener("resize", function () {
    if (pos) clampInto(visibleBox());
  });
  speed.addEventListener("change", function () {
    rate = parseFloat(speed.value) || 1;
    LS.set("shoug-reader-rate", String(rate));
    restartChunk();
  });
  voiceSel.addEventListener("change", function () {
    LS.set("shoug-reader-voice-" + pageLang(), voiceSel.value);
    restartChunk();
  });

  function pageLang() {
    return isArabic() ? "ar" : "en";
  }

  function fillVoices() {
    var lang = pageLang();
    var list = voicesFor(lang);
    var chosen = bestVoice(lang);
    voiceSel.textContent = "";
    if (!list.length) {
      var o = document.createElement("option");
      o.value = "";
      o.textContent = t("auto");
      voiceSel.appendChild(o);
      return;
    }
    list.forEach(function (v) {
      var o = document.createElement("option");
      o.value = v.name;
      o.textContent =
        v.name.replace(/^(Microsoft|Google)\s+/, "") + " (" + v.lang + ")";
      if (chosen && v.name === chosen.name) o.selected = true;
      voiceSel.appendChild(o);
    });
  }
  if (typeof synth.addEventListener === "function")
    synth.addEventListener("voiceschanged", fillVoices);
  else synth.onvoiceschanged = fillVoices;

  function paint() {
    var dir = isArabic() ? "rtl" : "ltr";
    panel.dir = dir;
    launch.dir = dir;
    var bubble = state.active && playerHidden;
    launch.classList.toggle("sr-bubble", bubble);
    launch.innerHTML = bubble
      ? ICON_SPEAK
      : ICON_SPEAK + "<span>" + t("start") + "</span>";
    launch.setAttribute("aria-label", bubble ? t("show") : t("start"));
    launch.title = bubble ? t("show") : "";
    panel.classList.toggle("sr-collapsed", collapsed);
    bGrip.setAttribute("aria-label", t("move"));
    bGrip.title = t("move");
    bFold.innerHTML = collapsed ? ICON_UP : ICON_DOWN;
    bFold.setAttribute("aria-label", collapsed ? t("expand") : t("collapse"));
    bFold.setAttribute("aria-expanded", collapsed ? "false" : "true");
    bFold.title = collapsed ? t("expand") : t("collapse");
    bHide.setAttribute("aria-label", t("hide"));
    bHide.title = t("hide");
    bMini.hidden = !collapsed;
    panel.setAttribute("aria-label", t("listen"));
    bPrev.setAttribute("aria-label", t("prev"));
    bPrev.title = t("prev");
    bNext.setAttribute("aria-label", t("next"));
    bNext.title = t("next");
    bStop.setAttribute("aria-label", t("stop"));
    bStop.title = t("stop");
    var playing = state.active && !state.paused;
    bPlay.innerHTML = playing ? ICON_PAUSE : ICON_PLAY;
    bPlay.setAttribute("aria-label", playing ? t("pause") : t("resume"));
    bPlay.title = playing ? t("pause") : t("resume");
    bMini.innerHTML = bPlay.innerHTML;
    bMini.setAttribute("aria-label", bPlay.getAttribute("aria-label"));
    bMini.title = bPlay.title;
    speedText.textContent = t("speed");
    voiceText.textContent = t("voice");
    segments.forEach(function (seg, i) {
      var on = state.active && state.seg === i;
      var label = on ? (state.paused ? t("resume") : t("pause")) : t("listen");
      seg.btn.innerHTML =
        (on && !state.paused ? ICON_PAUSE : ICON_SPEAK) +
        "<span>" +
        label +
        "</span>";
      seg.btn.setAttribute("aria-pressed", on ? "true" : "false");
      seg.btn.title = on ? label : t("here");
    });
    if (state.active) {
      statusState.textContent =
        (state.paused ? t("paused") : t("reading")) + " ·";
      statusLabel.textContent = segments[state.seg]
        ? segments[state.seg].label
        : "";
    }
    launch.hidden = state.active && !playerHidden;
    panel.hidden = !state.active || playerHidden;
    place();
  }

  /* ---------------------------------------------------------------- engine */
  var state = {
    active: false,
    paused: false,
    seg: -1,
    chunks: [],
    ci: 0,
    token: 0,
    utter: null,
  };
  var marked = null;
  var nowEl = null;
  var warned = {};

  function clearMarks() {
    if (marked) marked.classList.remove("sr-reading");
    if (nowEl) nowEl.classList.remove("sr-now");
    marked = nowEl = null;
  }

  function startIndex() {
    if (mode === "deck" && document.body.classList.contains("flip")) {
      for (var k = 0; k < segments.length; k++)
        if (segments[k].anchor.classList.contains("current")) return k;
    }
    var best = 0;
    for (var i = 0; i < segments.length; i++) {
      var r = segments[i].anchor.getBoundingClientRect();
      if (r.top <= 140) best = i;
      else break;
    }
    return best;
  }

  function inView(node) {
    var r = node.getBoundingClientRect();
    var h = window.innerHeight || document.documentElement.clientHeight;
    return r.bottom > 60 && r.top < h - 120;
  }

  function showCard(card) {
    if (
      !document.body.classList.contains("flip") ||
      card.classList.contains("current")
    )
      return;
    var jump = document.getElementById("f-jump");
    var all = [].slice.call(document.querySelectorAll("main>.card"));
    if (jump && all.indexOf(card) >= 0) {
      jump.value = String(all.indexOf(card));
      jump.dispatchEvent(new Event("change", { bubbles: true }));
    }
  }

  function bringIntoView(node) {
    if (!node || inView(node)) return;
    try {
      node.scrollIntoView({ behavior: "smooth", block: "center" });
    } catch (e) {
      node.scrollIntoView();
    }
  }

  function cancelSpeech() {
    state.token++;
    synth.cancel();
  }

  function play(i) {
    cancelSpeech();
    for (; i < segments.length; i++) {
      var seg = segments[i];
      if (mode === "breakdown" && !isVisible(seg.anchor)) continue;
      var chunks = seg.chunks();
      if (!chunks.length) continue;
      state.active = true;
      state.paused = false;
      state.seg = i;
      state.chunks = chunks;
      state.ci = 0;
      clearMarks();
      if (mode === "deck") showCard(seg.anchor);
      marked = seg.mark;
      marked.classList.add("sr-reading");
      bringIntoView(seg.anchor);
      fillVoices();
      paint();
      speakChunk();
      return;
    }
    stop(); // reached the end of the page
  }

  function speakChunk() {
    var token = ++state.token;
    if (state.ci >= state.chunks.length) {
      play(state.seg + 1);
      return;
    }
    var chunk = state.chunks[state.ci];
    if (nowEl !== chunk.el) {
      if (nowEl) nowEl.classList.remove("sr-now");
      nowEl = chunk.el && chunk.el !== marked ? chunk.el : null;
      if (nowEl) {
        nowEl.classList.add("sr-now");
        bringIntoView(nowEl);
      }
    }
    var lang = langOf(chunk.text);
    var voice = null;
    if (lang === pageLang() && voiceSel.value) {
      voice = synth.getVoices().filter(function (v) {
        return v.name === voiceSel.value;
      })[0];
    }
    voice = voice || bestVoice(lang);
    if (
      !voice &&
      voicesFor(lang).length === 0 &&
      synth.getVoices().length &&
      !warned[lang]
    ) {
      warned[lang] = true;
      note.textContent = t("noVoice");
      note.hidden = false;
    }
    var u = new SpeechSynthesisUtterance(chunk.text);
    u.rate = rate;
    u.lang = voice ? voice.lang : lang === "ar" ? "ar-SA" : "en-US";
    if (voice) u.voice = voice;
    u.onend = function () {
      if (token !== state.token) return;
      state.ci++;
      speakChunk();
    };
    u.onerror = function (ev) {
      if (token !== state.token) return;
      if (ev.error === "interrupted" || ev.error === "canceled") return;
      state.ci++;
      speakChunk();
    };
    state.utter = u; // a reference keeps Chrome from dropping the end event
    synth.speak(u);
  }

  // Pausing cancels and remembers the sentence: speechSynthesis.pause() is unreliable on Android.
  function togglePause() {
    if (!state.active) return;
    if (state.paused) {
      state.paused = false;
      paint();
      speakChunk();
    } else {
      cancelSpeech();
      state.paused = true;
      paint();
    }
  }

  function restartChunk() {
    if (!state.active || state.paused) return;
    cancelSpeech();
    speakChunk();
  }

  function move(step) {
    if (!state.active) return;
    var i = state.seg + step;
    if (step < 0) {
      while (i > 0 && mode === "breakdown" && !isVisible(segments[i].anchor))
        i--;
      i = Math.max(0, i);
    }
    play(i);
  }

  function stop() {
    cancelSpeech();
    state.active = false;
    state.paused = false;
    state.seg = -1;
    playerHidden = false;
    clearMarks();
    note.hidden = true;
    paint();
  }

  window.addEventListener("pagehide", function () {
    synth.cancel();
  });
  document.addEventListener("keydown", function (ev) {
    if (ev.key === "Escape" && state.active) stop();
  });
  // Breakdowns switch language in place: relabel the controls and offer that language's voices.
  new MutationObserver(function () {
    fillVoices();
    paint();
  }).observe(document.documentElement, {
    attributes: true,
    attributeFilter: ["lang"],
  });

  synth.cancel(); // speech left over from a page that was just closed or reloaded
  fillVoices();
  paint();
})();
