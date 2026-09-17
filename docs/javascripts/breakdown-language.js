(function () {
  'use strict';
  // Cached wrapper pages may still load this script. Only lesson files own it.
  if (/\/(?:index\.html)?$/.test(location.pathname)) return;
  if (window.__shougBreakdownLanguageLoaded) return;
  window.__shougBreakdownLanguageLoaded = true;
  var desired = new URLSearchParams(location.search).get('lang');
  try { desired = desired || localStorage.getItem('shoug-breakdown-lang'); } catch (_) {}
  desired = desired === 'ar' ? 'ar' : 'en';

  function start() {
    var root = document.documentElement;
    root.setAttribute('data-breakdown-language', '');
    var endpoint = window.SHOUG_TRANSLATION_ENDPOINT || 'https://shoug-tech.shoug-alomran.workers.dev/v1/breakdown-translation';
    var records = new Map();
    var translations = new Map();
    var controller;
    var revision = 0;
    var active = 'en';
    var busy = false;
    var toolbar = document.createElement('div');
    toolbar.className = 'bd-language';
    toolbar.setAttribute('role', 'group');
    toolbar.setAttribute('aria-label', 'Breakdown language / لغة الشرح');
    toolbar.innerHTML = '<div><button type="button" data-bd-lang="en" lang="en" aria-label="English">EN</button><button type="button" data-bd-lang="ar" lang="ar" aria-label="العربية">AR</button></div><span class="bd-language-status" role="status" aria-live="polite"></span>';
    var host = document.querySelector('.bdx-bar-inner, .topbar-actions, .header-actions, .topbar-inner');
    if (host) {
      var themeButton = host.querySelector('.theme-toggle, #themeToggle');
      host.insertBefore(toolbar, themeButton);
    } else {
      toolbar.classList.add('bd-language--inline');
      (document.querySelector('#main-content, main, .header, .topbar, header') || document.body).prepend(toolbar);
    }
    var status = toolbar.querySelector('[role="status"]');
    function report(message, error) {
      status.textContent = message;
      toolbar.classList.toggle('bd-language--error', Boolean(error));
      toolbar.title = message;
    }
    var skip = 'script,style,noscript,code,pre,kbd,samp,svg,math,textarea,input,[contenteditable],.bd-language,.sg-ai-panel,.sg-ai-launch,.sys-time,[translate="no"],#arabicContent,#shoug-fb-user,#shoug-auth-modal,#shoug-ue-modal,#shoug-page-comments,#shoug-notes-panel,#shoug-ob-card,.shoug-user-dropdown';

    // One controller owns the controls; legacy toggles only changed headings or
    // exposed incomplete translations. Translate the complete English lesson.
    document.querySelectorAll('#langToggle,[data-lang-toggle],.shoug-lang-btn').forEach(function (button) { button.hidden = true; });
    document.querySelectorAll('[data-lang-panel="ar"]').forEach(function (panel) {
      var other = panel.parentElement.querySelector('[data-lang-panel="en"] iframe');
      var frame = panel.querySelector('iframe');
      if (other && frame && other.src === frame.src) panel.remove();
    });
    var english = document.getElementById('englishContent');
    var arabic = document.getElementById('arabicContent');
    if (english && arabic) { english.style.display = 'block'; arabic.style.display = 'none'; }

    function remember(node, attribute) {
      if (!records.has(node)) records.set(node, new Map());
      var slots = records.get(node);
      var current = attribute ? node.getAttribute(attribute) : node.nodeValue;
      var old = slots.get(attribute);
      // Dynamic quizzes and tabs may replace the text on an existing node.
      if (old && (current === old.en || current === old.ar)) return;
      if (!current || !/[A-Za-z]{3}/.test(current)) return;
      slots.set(attribute, { en: current, ar: null });
    }

    function collect() {
      document.querySelectorAll('option:not([value])').forEach(function (option) { option.setAttribute('value', option.textContent); });
      var title = document.querySelector('title');
      if (title && title.firstChild) remember(title.firstChild, '');
      var walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
      var node;
      while ((node = walker.nextNode())) {
        if (node.parentElement && !node.parentElement.closest(skip)) remember(node, '');
      }
      document.body.querySelectorAll('[placeholder],[title],[aria-label],[alt]').forEach(function (element) {
        if (element.closest(skip.replace('textarea,input,', ''))) return;
        ['placeholder', 'title', 'aria-label', 'alt'].forEach(function (attribute) {
          if (element.hasAttribute(attribute)) remember(element, attribute);
        });
      });
    }

    function render(lang) {
      records.forEach(function (slots, node) {
        if (!node.isConnected) { records.delete(node); return; }
        slots.forEach(function (record, attribute) {
          var value = lang === 'ar' ? record.ar || record.en : record.en;
          if (attribute) {
            if (node.getAttribute(attribute) !== value) node.setAttribute(attribute, value);
          } else if (node.nodeValue !== value) node.nodeValue = value;
        });
      });
      root.lang = lang === 'ar' ? 'ar' : 'en';
      root.dir = lang === 'ar' ? 'rtl' : 'ltr';
      document.body.classList.toggle('shoug-arabic-mode', lang === 'ar');
      active = lang;
      toolbar.querySelectorAll('button').forEach(function (button) {
        button.setAttribute('aria-pressed', String(button.dataset.bdLang === lang));
      });
    }

    function notifyFrames(lang) {
      document.querySelectorAll('iframe').forEach(function (frame) {
        try {
          if (!frame.closest('[hidden]') && new URL(frame.src, location.href).origin === location.origin)
            frame.contentWindow.postMessage({ type: 'shoug-breakdown-language', lang: lang }, location.origin);
        } catch (_) {}
      });
    }

    function isReference(text) {
      return /^(?:(?:https?:\/\/|mailto:|www\.)\S+|[^\s@]+@[^\s@]+\.[^\s@]+|[A-Za-z0-9_-]+(?:\.[A-Za-z0-9_-]+)+(?:\/\S*)?)$/.test(text.trim());
    }

    function validTranslation(value, original) {
      return typeof value === 'string' && value.trim() && (/[\u0600-\u06ff]/.test(value) || isReference(original) || /^[A-Z0-9][A-Z0-9\s/_.:+-]*$/.test(original.trim()));
    }

    // Translations persist per lesson so a revisit (or a new tab) is instant.
    var storeKey = 'bd-ar-v6:' + location.pathname;
    var stored = {};
    try { stored = JSON.parse(localStorage.getItem(storeKey)) || {}; } catch (_) { stored = {}; }
    function persistStore() {
      try { localStorage.setItem(storeKey, JSON.stringify(stored)); }
      catch (_) {
        // Quota: drop other lessons' caches, then try once more.
        try {
          Object.keys(localStorage).forEach(function (key) { if (key.indexOf('bd-ar-') === 0 && key !== storeKey) localStorage.removeItem(key); });
          localStorage.setItem(storeKey, JSON.stringify(stored));
        } catch (_) {}
      }
    }

    async function fetchBatch(texts, signal) {
      var requestController = new AbortController();
      var cancel = function () { requestController.abort(); };
      signal.addEventListener('abort', cancel, { once: true });
      var timeout = setTimeout(cancel, 60000);
      var response;
      try {
        response = await fetch(endpoint, {
          method: 'POST', headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ texts: texts }), signal: requestController.signal
        });
      } finally {
        clearTimeout(timeout);
        signal.removeEventListener('abort', cancel);
      }
      if (!response.ok) {
        var error = new Error('Translation unavailable');
        error.status = response.status;
        throw error;
      }
      var data = await response.json();
      if (!Array.isArray(data.translations) || data.translations.length !== texts.length) throw new Error('Incomplete translation');
      // One unusable item (a term the model left in English) keeps its English
      // text instead of discarding the whole batch.
      return data.translations.map(function (text, i) {
        if (validTranslation(text, texts[i])) { stored[texts[i]] = text; return text; }
        return texts[i];
      });
    }

    function pieces(text) {
      // Keep requests bounded even for a long paragraph in a single text node.
      return text.match(/[\s\S]{1,3000}(?:\s|$)|[\s\S]{1,3000}/g) || [text];
    }

    async function setLanguage(lang, persist) {
      desired = lang === 'ar' ? 'ar' : 'en';
      var version = ++revision;
      if (controller) controller.abort();
      controller = new AbortController();
      var signal = controller.signal;
      if (persist) {
        try { localStorage.setItem('shoug-breakdown-lang', desired); } catch (_) {}
        var url = new URL(location.href);
        url.searchParams.set('lang', desired);
        history.replaceState(null, '', url);
      }
      notifyFrames(desired);
      collect();
      busy = desired === 'ar';
      toolbar.setAttribute('aria-busy', String(busy));
      if (desired === 'en') { render('en'); report(''); return; }
      report('جارٍ ترجمة الشرح إلى العربية…');
      try {
        var missing = new Set();
        records.forEach(function (slots) {
          slots.forEach(function (record) {
            pieces(record.en).forEach(function (part) { if (!/[A-Za-z]{3}/.test(part) || isReference(part)) translations.set(part, part);
              else if (!translations.has(part)) missing.add(part); });
          });
        });
        missing.forEach(function (text) {
          if (typeof stored[text] === 'string') { translations.set(text, stored[text]); missing.delete(text); }
        });
        var batches = [], batch = [], size = 0;
        missing.forEach(function (text) {
          if (batch.length && (batch.length >= 16 || size + text.length > 2500)) { batches.push(batch); batch = []; size = 0; }
          batch.push(text); size += text.length;
        });
        if (batch.length) batches.push(batch);
        function apply() {
          records.forEach(function (slots) {
            slots.forEach(function (record) {
              var parts = pieces(record.en);
              if (!parts.every(function (part) { return translations.has(part); })) return;
              var translated = parts.map(function (part) { return translations.get(part); }).join(' ').trim();
              // Isolate arithmetic from surrounding RTL text without adding DOM nodes.
              translated = translated.replace(/\d+(?:\s*[+*/]\s*\d+)+/g, '\u2066$&\u2069');
              record.ar = record.en.match(/^\s*/)[0] + translated + record.en.match(/\s*$/)[0];
            });
          });
          render('ar');
        }
        // Show cached text and switch direction at once, then fill in top-down as
        // batches arrive. A few requests run together; the worker allows 60/min.
        if (batches.length) apply();
        var done = 0, next = 0, failure = null;
        async function worker() {
          while (next < batches.length && !failure) {
            var texts = batches[next++];
            try {
              var values;
              try { values = await fetchBatch(texts, signal); }
              catch (first) {
                // A slow or rate-limited model call gets one more try before it counts.
                if (version !== revision) return;
                await new Promise(function (resolve) { setTimeout(resolve, first.status === 429 ? 20000 : 1500); });
                if (version !== revision) return;
                values = await fetchBatch(texts, signal);
              }
              if (version !== revision) return;
              texts.forEach(function (text, i) { translations.set(text, values[i]); });
              done++;
              apply();
              report('جارٍ ترجمة الشرح… ' + done + '/' + batches.length);
            } catch (error) { failure = failure || error; }
          }
        }
        var workers = [];
        for (var w = 0; w < Math.min(4, batches.length); w++) workers.push(worker());
        await Promise.all(workers);
        if (version !== revision) return;
        persistStore();
        if (failure && !done && batches.length) throw failure;
        apply();
        if (failure) report('Part of this lesson is still in English. Select AR to finish. / جزء من الشرح لم يُترجم بعد، اضغط AR لإكماله.', true);
        else report('ترجمة آلية · الصور الأصلية بلغتها الأصلية');
      } catch (error) {
        if (version !== revision) return;
        render('en');
        var message = error.status === 404
          ? 'Arabic translation service is not available yet. / خدمة الترجمة غير متاحة بعد.'
          : error.status === 429
            ? 'Please wait a minute, then select AR. / انتظر دقيقة ثم اضغط AR.'
            : 'Translation failed. Select AR to retry. / تعذّرت الترجمة. اضغط AR لإعادة المحاولة.';
        report(message, true);
      } finally {
        if (version === revision) { busy = false; toolbar.setAttribute('aria-busy', 'false'); }
      }
    }

    toolbar.addEventListener('click', function (event) {
      var button = event.target.closest('[data-bd-lang]');
      if (button) setLanguage(button.dataset.bdLang, true);
    });
    window.addEventListener('message', function (event) {
      if (event.origin !== location.origin || !event.data || event.data.type !== 'shoug-breakdown-language') return;
      var trusted = event.source === window.parent || Array.from(document.querySelectorAll('iframe')).some(function (frame) { return frame.contentWindow === event.source; });
      if (!trusted || (event.data.lang === desired && (busy || active === desired))) return;
      if (event.data.lang === 'ar' || event.data.lang === 'en') setLanguage(event.data.lang, false);
    });
    window.addEventListener('storage', function (event) {
      if (event.key === 'shoug-breakdown-lang' && (event.newValue === 'ar' || event.newValue === 'en')) setLanguage(event.newValue, false);
    });
    document.querySelectorAll('iframe').forEach(function (frame) { frame.addEventListener('load', function () { notifyFrames(desired); }); });
    var timer;
    new MutationObserver(function (mutations) {
      var changed = mutations.some(function (mutation) {
        var element = mutation.target.nodeType === 1 ? mutation.target : mutation.target.parentElement;
        return element && !element.closest(skip);
      });
      if (!changed || busy || active !== 'ar') return;
      clearTimeout(timer);
      timer = setTimeout(function () {
        collect();
        var pending = false;
        records.forEach(function (slots) { slots.forEach(function (record) { if (!record.ar) pending = true; }); });
        if (pending) setLanguage('ar', false);
      }, 150);
    }).observe(document.body, { childList: true, characterData: true, subtree: true });
    window.__shougSetLanguage = function (lang) { return setLanguage(lang, true); };
    setLanguage(desired, false);
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', start);
  else start();
})();
