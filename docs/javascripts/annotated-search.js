/* Search bar for Annotated Slides decks. Added to both deck formats. It searches the
   course's annotated-slides/search-index.json (titles, slide text, notes, tips, question
   stems; never answers), which scripts/annotated_search.py builds. */
(function () {
  "use strict";
  if (document.getElementById("ans-search")) return;
  var head =
    document.querySelector(".top .wrap") || document.querySelector(".as-top .as-wrap");
  if (!head) return;

  var CSS =
    "html{--ans-bg:#fff;--ans-ink:#1d1d1f;--ans-muted:#5b5b63;--ans-line:#dedcd6;--ans-accent:#2f5bb7;--ans-hover:#eef1f8;--ans-mark:#ffe58a;--ans-mark-ink:#1d1d1f}" +
    'html[data-theme="dark"]{--ans-bg:#1b1c20;--ans-ink:#ecebe8;--ans-muted:#a9a8b0;--ans-line:#3a3c44;--ans-accent:#8fb0ff;--ans-hover:#282a31;--ans-mark:#f5cf57;--ans-mark-ink:#1d1d1f}' +
    "#ans-search{position:relative;flex:1 1 240px;min-width:0;max-width:440px}" +
    "#ans-input{box-sizing:border-box;width:100%;height:36px;padding:0 12px;border:1px solid var(--ans-line);border-radius:8px;background:var(--ans-bg);color:var(--ans-ink);font:inherit;font-size:16px}" +
    "#ans-input::placeholder{color:var(--ans-muted)}" +
    "#ans-input:focus{outline:2px solid var(--ans-accent);outline-offset:1px}" +
    "#ans-panel{position:absolute;z-index:50;top:calc(100% + 6px);left:0;width:min(620px,calc(100vw - 24px));max-height:min(70vh,560px);overflow:auto;background:var(--ans-bg);color:var(--ans-ink);border:1px solid var(--ans-line);border-radius:10px;box-shadow:0 12px 32px rgba(0,0,0,.22);font-size:14px;line-height:1.45;text-align:left}" +
    "#ans-panel[hidden]{display:none}" +
    ".ans-msg{padding:12px 14px;color:var(--ans-muted)}" +
    ".ans-group{position:sticky;top:0;padding:8px 14px;background:var(--ans-bg);border-bottom:1px solid var(--ans-line);color:var(--ans-muted);font-size:12px;font-weight:700}" +
    ".ans-item{display:block;width:100%;box-sizing:border-box;padding:10px 14px;border:0;border-bottom:1px solid var(--ans-line);border-radius:0;background:none;color:inherit;font:inherit;text-align:left;text-decoration:none;cursor:pointer;white-space:normal}" +
    ".ans-item:hover,.ans-item.sel{background:var(--ans-hover)}" +
    ".ans-title{display:block;font-weight:700}" +
    ".ans-where{display:block;color:var(--ans-accent);font-size:12px;font-weight:700}" +
    ".ans-snip{display:block;color:var(--ans-muted);overflow-wrap:anywhere}" +
    "#ans-panel mark,mark.ans-hit{background:var(--ans-mark);color:var(--ans-mark-ink);border-radius:2px;padding:0 1px}" +
    ".ans-flash{outline:3px solid var(--ans-accent);outline-offset:2px;transition:outline-color 1.2s}" +
    "@media (max-width:640px){#ans-search{flex-basis:100%;max-width:none;order:5}#ans-panel{width:100%}}" +
    "@media print{#ans-search{display:none}mark.ans-hit{background:none;color:inherit}}";
  var style = document.createElement("style");
  style.textContent = CSS;
  document.head.appendChild(style);

  var box = document.createElement("div");
  box.id = "ans-search";
  box.setAttribute("role", "search");
  var input = document.createElement("input");
  input.id = "ans-input";
  input.type = "search";
  input.placeholder = "Search slides, notes, tips…";
  input.setAttribute("aria-label", "Search the annotated slides for this course");
  input.setAttribute("autocomplete", "off");
  input.setAttribute("spellcheck", "false");
  var panel = document.createElement("div");
  panel.id = "ans-panel";
  panel.hidden = true;
  box.appendChild(input);
  box.appendChild(panel);
  var brand = head.querySelector(".brand,.as-brand");
  if (brand && brand.nextSibling) head.insertBefore(box, brand.nextSibling);
  else head.appendChild(box);

  var parts = location.pathname.split("/");
  var thisDeck = parts[parts.length - 2];
  var indexData = null;
  var loading = null;
  var selected = -1;
  var timer = null;

  function loadIndex() {
    if (!loading) {
      loading = fetch(new URL("../search-index.json", location.href).href)
        .then(function (r) {
          if (!r.ok) throw new Error("HTTP " + r.status);
          return r.json();
        })
        .then(function (d) {
          d.decks.forEach(function (deck) {
            deck.n.forEach(function (s) {
              s.push(s[1].toLowerCase(), s[2].toLowerCase());
            });
          });
          indexData = d;
        });
    }
    return loading;
  }

  function tokens(q) {
    return q.toLowerCase().split(/\s+/).filter(Boolean);
  }

  function score(slide, words, phrase) {
    var title = slide[3];
    var text = slide[4];
    var total = 0;
    for (var i = 0; i < words.length; i++) {
      var inTitle = title.indexOf(words[i]) >= 0;
      var at = text.indexOf(words[i]);
      if (!inTitle && at < 0) return 0;
      if (inTitle) total += 20;
      if (at >= 0) total += 2;
    }
    if (title.indexOf(phrase) >= 0) total += 100;
    if (text.indexOf(phrase) >= 0) total += 40;
    return total;
  }

  function appendMarked(parent, text, words) {
    var escaped = words.map(function (w) {
      return w.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
    });
    var re = new RegExp("(" + escaped.join("|") + ")", "ig");
    text.split(re).forEach(function (part, i) {
      if (!part) return;
      if (i % 2) {
        var m = document.createElement("mark");
        m.textContent = part;
        parent.appendChild(m);
      } else parent.appendChild(document.createTextNode(part));
    });
  }

  function snippet(slide, words) {
    var text = slide[2];
    var lower = slide[4];
    var at = -1;
    for (var i = 0; i < words.length && at < 0; i++) at = lower.indexOf(words[i]);
    if (at < 0) return text.slice(0, 130);
    var from = Math.max(0, at - 55);
    if (from > 0) {
      var space = text.indexOf(" ", from);
      if (space >= 0 && space < at) from = space + 1;
    }
    return (from > 0 ? "…" : "") + text.slice(from, from + 150) + (from + 150 < text.length ? "…" : "");
  }

  function items() {
    return Array.prototype.slice.call(panel.querySelectorAll(".ans-item"));
  }

  function select(i) {
    var list = items();
    if (!list.length) return;
    selected = (i + list.length) % list.length;
    list.forEach(function (el, k) {
      el.classList.toggle("sel", k === selected);
    });
    var el = list[selected];
    if (el.offsetTop < panel.scrollTop + 34) panel.scrollTop = el.offsetTop - 34;
    else if (el.offsetTop + el.offsetHeight > panel.scrollTop + panel.clientHeight)
      panel.scrollTop = el.offsetTop + el.offsetHeight - panel.clientHeight;
  }

  // The bar can sit near the right edge of the header, so keep the panel on screen.
  function keepOnScreen() {
    panel.style.left = "0";
    var over = panel.getBoundingClientRect().right - (window.innerWidth - 12);
    if (over > 0) panel.style.left = -over + "px";
  }

  function message(text) {
    panel.textContent = "";
    var m = document.createElement("div");
    m.className = "ans-msg";
    m.textContent = text;
    panel.appendChild(m);
    panel.hidden = false;
    keepOnScreen();
  }

  function addGroup(label) {
    var g = document.createElement("div");
    g.className = "ans-group";
    g.textContent = label;
    panel.appendChild(g);
  }

  function addItem(deck, slide, words, here) {
    var el = document.createElement(here ? "button" : "a");
    el.className = "ans-item";
    if (here) {
      el.type = "button";
      el.addEventListener("click", function () {
        openSlide(slide[0], words);
      });
    } else {
      el.href = new URL(
        "../" + deck.s + "/#" + deck.a + slide[0],
        location.href,
      ).href;
      el.target = "_top";
    }
    if (!here) {
      var where = document.createElement("span");
      where.className = "ans-where";
      where.textContent = deck.c;
      el.appendChild(where);
    }
    var title = document.createElement("span");
    title.className = "ans-title";
    appendMarked(title, "Slide " + slide[0] + " · " + (slide[1] || "Untitled"), words);
    el.appendChild(title);
    var snip = document.createElement("span");
    snip.className = "ans-snip";
    appendMarked(snip, snippet(slide, words), words);
    el.appendChild(snip);
    panel.appendChild(el);
  }

  function collect(deck, words, phrase) {
    var out = [];
    deck.n.forEach(function (s) {
      var v = score(s, words, phrase);
      if (v) out.push({ deck: deck, slide: s, v: v });
    });
    out.sort(function (a, b) {
      return b.v - a.v || a.slide[0] - b.slide[0];
    });
    return out;
  }

  function run() {
    clearMarks();
    selected = -1;
    var q = input.value.trim();
    if (q.length < 2) {
      panel.hidden = true;
      panel.textContent = "";
      return;
    }
    if (!indexData) {
      message("Loading search…");
      loadIndex().then(run, function () {
        loading = null;
        message("Search couldn’t load. Check your connection and try again.");
      });
      return;
    }
    var words = tokens(q);
    var phrase = q.toLowerCase();
    var here = [];
    var other = [];
    indexData.decks.forEach(function (deck) {
      var hits = collect(deck, words, phrase);
      if (deck.s === thisDeck) here = hits;
      else other = other.concat(hits);
    });
    other.sort(function (a, b) {
      return b.v - a.v;
    });
    panel.textContent = "";
    panel.hidden = false;
    keepOnScreen();
    panel.scrollTop = 0;
    if (!here.length && !other.length) {
      message("No results for “" + q + "”.");
      return;
    }
    addGroup("This chapter: " + here.length + (here.length === 1 ? " slide" : " slides"));
    here.slice(0, 40).forEach(function (h) {
      addItem(h.deck, h.slide, words, true);
    });
    if (other.length) {
      addGroup("Other chapters: " + other.length + (other.length === 1 ? " slide" : " slides"));
      other.slice(0, 40).forEach(function (h) {
        addItem(h.deck, h.slide, words, false);
      });
    }
    select(0);
  }

  function clearMarks() {
    document.querySelectorAll("mark.ans-hit").forEach(function (m) {
      var p = m.parentNode;
      p.replaceChild(document.createTextNode(m.textContent), m);
      p.normalize();
    });
  }

  function markWords(card, words) {
    if (!words || !words.length) return null;
    var escaped = words.map(function (w) {
      return w.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
    });
    var re = new RegExp(escaped.join("|"), "ig");
    var walker = document.createTreeWalker(card, NodeFilter.SHOW_TEXT, {
      acceptNode: function (node) {
        var el = node.parentElement;
        if (!el || el.closest("svg,button,details,.picks,.opt-why,.verdict,textarea")) return NodeFilter.FILTER_REJECT;
        return node.nodeValue.trim() ? NodeFilter.FILTER_ACCEPT : NodeFilter.FILTER_REJECT;
      },
    });
    var nodes = [];
    while (walker.nextNode()) nodes.push(walker.currentNode);
    var first = null;
    nodes.forEach(function (node) {
      var text = node.nodeValue;
      re.lastIndex = 0;
      if (!re.test(text)) return;
      re.lastIndex = 0;
      var frag = document.createDocumentFragment();
      var last = 0;
      var m;
      while ((m = re.exec(text))) {
        if (!m[0]) break;
        frag.appendChild(document.createTextNode(text.slice(last, m.index)));
        var mark = document.createElement("mark");
        mark.className = "ans-hit";
        mark.textContent = m[0];
        frag.appendChild(mark);
        if (!first) first = mark;
        last = m.index + m[0].length;
      }
      frag.appendChild(document.createTextNode(text.slice(last)));
      node.parentNode.replaceChild(frag, node);
    });
    return first;
  }

  function isFlip() {
    return document.body.classList.contains("flip") || document.body.classList.contains("mode-flip");
  }

  function openSlide(n, words) {
    var card = document.getElementById("slide-" + n) || document.getElementById("s-" + n);
    if (!card) return;
    panel.hidden = true;
    clearMarks();
    if (card.hidden) {
      var all = document.querySelector('[data-group="filter"][data-value="all"]');
      if (all) all.click();
    }
    if (card.classList.contains("notes-hidden")) {
      var toggle = card.querySelector(".note-toggle");
      if (toggle) toggle.click();
    }
    if (isFlip()) {
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
    }
    var first = markWords(card, words);
    requestAnimationFrame(function () {
      var bar = head.parentElement;
      var offset = bar && getComputedStyle(bar).position === "sticky" ? bar.offsetHeight + 12 : 10;
      var top = card.getBoundingClientRect().top + window.pageYOffset - offset;
      if (first) {
        var markTop = first.getBoundingClientRect().top + window.pageYOffset;
        if (markTop - top > window.innerHeight - offset - 80) top = markTop - offset - 80;
      }
      window.scrollTo(0, Math.max(0, top));
      card.classList.add("ans-flash");
      setTimeout(function () {
        card.classList.remove("ans-flash");
      }, 1400);
    });
  }

  input.addEventListener("input", function () {
    clearTimeout(timer);
    timer = setTimeout(run, 120);
  });
  input.addEventListener("focus", function () {
    loadIndex().catch(function () {
      loading = null;
    });
    if (input.value.trim().length >= 2 && panel.hidden) run();
  });
  input.addEventListener("keydown", function (ev) {
    ev.stopPropagation();
    if (ev.key === "ArrowDown") {
      ev.preventDefault();
      select(selected + 1);
    } else if (ev.key === "ArrowUp") {
      ev.preventDefault();
      select(selected - 1);
    } else if (ev.key === "Enter") {
      ev.preventDefault();
      var el = items()[selected];
      if (el) el.click();
    } else if (ev.key === "Escape") {
      panel.hidden = true;
    }
  });
  document.addEventListener("click", function (ev) {
    if (!box.contains(ev.target)) panel.hidden = true;
  });
  document.addEventListener("keydown", function (ev) {
    if (ev.key !== "/" || ev.ctrlKey || ev.metaKey || ev.altKey) return;
    var t = ev.target.tagName;
    if (t === "INPUT" || t === "TEXTAREA" || t === "SELECT") return;
    ev.preventDefault();
    input.focus();
  });

  // A result from another chapter opens that chapter's wrapper page with the slide in its hash.
  if (window.top !== window.self) {
    try {
      var match = /^#(?:slide-|s-)(\d+)$/.exec(window.top.location.hash);
      if (match) setTimeout(function () { openSlide(+match[1]); }, 60);
    } catch (e) {}
  }
})();
