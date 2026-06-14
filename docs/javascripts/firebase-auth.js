(function () {
  "use strict";

  var FB_VERSION = "10.12.0";
  var FB_BASE = "https://www.gstatic.com/firebasejs/" + FB_VERSION + "/firebase-";
  var FB_CONFIG = {
    apiKey: "AIzaSyDUklr3u8laDZH2jhHVAO3BPE12GaPpOmI",
    authDomain: "shoug-tech.firebaseapp.com",
    projectId: "shoug-tech",
    storageBucket: "shoug-tech.firebasestorage.app",
    messagingSenderId: "621041999813",
    appId: "1:621041999813:web:8982befd8b0ccc1d9475ac"
  };

  // ── Helpers ──────────────────────────────────────────────────────────────

  function pageSlug() {
    return window.location.pathname.replace(/\//g, "|").replace(/^\||\ |$/g, "") || "home";
  }

  function pageTitle() {
    return document.title
      .replace("SHOUG.TECH | ", "")
      .replace("SHOUG.TECH // ", "")
      .replace("SHOUG.TECH - ", "");
  }

  function isLegalPage() {
    var path = window.location.pathname;
    if (document.body && document.body.getAttribute("data-legal-document") === "true") return true;
    return path.indexOf("/policy") === 0 ||
           path.indexOf("/privacy") === 0 ||
           path.indexOf("/copyright") === 0 ||
           path.indexOf("/terms") === 0 ||
           path.indexOf("/legal") === 0;
  }

  function isContentPage() {
    var path = window.location.pathname;
    if (isLegalPage()) return false;
    if (path === "/" || path.indexOf("/account") === 0 || path.indexOf("/community") === 0 || path.indexOf("/bookmarks") === 0) return false;
    // Listing/overview pages (directory indexes) are never content pages, regardless of depth.
    if (document.querySelector(".directory-container")) return false;
    // For academics pages only show on actual leaf content pages, not listing/overview pages.
    // Content pages have 5+ segments: /academics/track/course/section/page/
    if (path.indexOf("/academics/") === 0) {
      return path.split("/").filter(Boolean).length >= 5;
    }
    return true;
  }

  function escHtml(s) {
    return String(s)
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;");
  }

  // ── Avatar presets (shared with /community/profile/) ──────────────────────
  var AVATAR_PRESETS = [
    'av-f1.png','av-f2.png','av-f3.png','av-f4.png','av-f5.png','av-f6.png','av-f7.png',
    'av-m1.png','av-m2.png','av-m3.png','av-m4.png','av-m5.png','av-m6.png','av-m7.png'
  ];
  function avatarUrl(preset) {
    var i = parseInt(preset, 10);
    return (!isNaN(i) && AVATAR_PRESETS[i]) ? '/assets/avatars/' + AVATAR_PRESETS[i] : null;
  }
  function avatarBlock(className, preset, color, initial) {
    var url = avatarUrl(preset);
    if (url) return '<div class="' + className + '" style="padding:0;background:#0d0720;border:1px solid ' + color + '55;"><img src="' + url + '" alt=""></div>';
    return '<div class="' + className + '" style="background:' + color + '1a;border:1px solid ' + color + '55;color:' + color + '">' + initial + '</div>';
  }

  function loadScript(src, cb) {
    var s = document.createElement("script");
    s.src = src;
    s.onload = cb;
    document.head.appendChild(s);
  }

  // ── Styles ───────────────────────────────────────────────────────────────

  function injectStyles() {
    if (document.getElementById("shoug-fb-styles")) return;
    var el = document.createElement("style");
    el.id = "shoug-fb-styles";
    el.textContent = [
      /* sign-in button */
      ".shoug-auth-btn{height:34px;display:inline-flex;align-items:center;padding:0 14px;border:1px solid rgba(184,41,234,.5);background:transparent;color:#b829ea;font-family:'JetBrains Mono',monospace;font-size:.65rem;font-weight:800;letter-spacing:.14em;text-transform:uppercase;cursor:pointer;transition:background 160ms}",
      ".shoug-auth-btn:hover{background:rgba(184,41,234,.12)}",
      /* user avatar */
      ".shoug-user-btn{width:34px;height:34px;display:inline-flex;align-items:center;justify-content:center;border:1px solid rgba(184,41,234,.5);background:rgba(184,41,234,.1);color:#b829ea;font-family:'JetBrains Mono',monospace;font-size:.72rem;font-weight:800;cursor:pointer;position:relative;user-select:none}",
      ".shoug-user-btn:hover{background:rgba(184,41,234,.2)}",
      ".shoug-user-avatar-img{width:32px;height:32px;object-fit:cover;display:block;}",
      /* dropdown */
      ".shoug-user-dropdown{position:absolute;top:calc(100% + 8px);right:0;background:#0a0514;border:1px solid rgba(184,41,234,.3);min-width:220px;z-index:99998;display:none;flex-direction:column;box-shadow:0 8px 32px rgba(0,0,0,.5)}",
      ".shoug-user-btn.open .shoug-user-dropdown{display:flex}",
      ".shoug-drop-email{padding:10px 14px;font-family:'JetBrains Mono',monospace;font-size:.6rem;color:#4a4258;border-bottom:1px solid rgba(255,255,255,.06);overflow:hidden;text-overflow:ellipsis;white-space:nowrap}",
      ".shoug-drop-link{display:block;padding:10px 14px;font-family:'JetBrains Mono',monospace;font-size:.68rem;color:#f8f7fb;text-decoration:none;letter-spacing:.06em;cursor:pointer;border:none;background:transparent;text-align:left;width:100%;transition:background 120ms,color 120ms;box-sizing:border-box}",
      ".shoug-drop-link:hover{background:rgba(184,41,234,.1);color:#b829ea}",
      ".shoug-drop-link.red:hover{background:rgba(255,42,75,.1);color:#ff2a4b}",
      /* notification badge */
      ".shoug-notif-badge{position:absolute;top:-5px;right:-5px;min-width:16px;height:16px;background:#ff2a4b;border-radius:8px;font-size:.52rem;font-weight:800;color:#fff;display:flex;align-items:center;justify-content:center;padding:0 4px;pointer-events:none;font-family:'JetBrains Mono',monospace;line-height:1;box-shadow:0 0 0 2px #0a0514;}",
      /* notification section inside dropdown */
      ".shoug-notif-section{border-bottom:1px solid rgba(255,255,255,.06);max-height:220px;overflow-y:auto;}",
      ".shoug-notif-hdr{padding:7px 14px 4px;font-size:.5rem;color:#b829ea;letter-spacing:.18em;text-transform:uppercase;font-family:'JetBrains Mono',monospace;}",
      ".shoug-notif-item{display:flex;flex-direction:column;gap:2px;padding:8px 14px;cursor:pointer;text-decoration:none;color:inherit;transition:background 100ms;border-left:2px solid transparent;}",
      ".shoug-notif-item:hover{background:rgba(184,41,234,.08);}",
      ".shoug-notif-item.unread{border-left-color:#b829ea;background:rgba(184,41,234,.04);}",
      ".shoug-notif-text{font-size:.66rem;color:#d1c5e5;line-height:1.45;font-family:'Inter',sans-serif;}",
      ".shoug-notif-text strong{color:#f8f7fb;font-family:'JetBrains Mono',monospace;font-size:.64rem;}",
      ".shoug-notif-preview{font-size:.6rem;color:#4a4258;font-family:'Inter',sans-serif;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;max-width:200px;}",
      ".shoug-notif-time{font-size:.52rem;color:#4a4258;font-family:'JetBrains Mono',monospace;letter-spacing:.04em;margin-top:1px;}",
      ".shoug-notif-empty{padding:10px 14px;font-size:.6rem;color:#4a4258;font-family:'JetBrains Mono',monospace;letter-spacing:.04em;}",
      /* modal backdrop */
      "#shoug-auth-modal{position:fixed;inset:0;z-index:99999;background:rgba(0,0,0,.75);backdrop-filter:blur(6px);display:none;align-items:center;justify-content:center;opacity:0;transition:opacity 150ms}",
      "#shoug-auth-modal.open{opacity:1;display:flex}",
      /* modal box */
      "#shoug-auth-box{width:min(420px,calc(100vw - 32px));background:#0a0514;border:1px solid rgba(184,41,234,.4);font-family:'JetBrains Mono',monospace;box-shadow:0 0 60px rgba(184,41,234,.15)}",
      ".auth-head{padding:18px 24px 14px;border-bottom:1px solid rgba(255,255,255,.06);display:flex;justify-content:space-between;align-items:center}",
      ".auth-tag{font-size:.58rem;color:#b829ea;letter-spacing:.12em;margin-bottom:4px}",
      ".auth-title{font-size:.78rem;font-weight:800;letter-spacing:.14em;text-transform:uppercase;color:#f8f7fb}",
      ".auth-close{background:transparent;border:none;color:#4a4258;font-size:1rem;cursor:pointer;line-height:1;padding:0;transition:color 120ms}",
      ".auth-close:hover{color:#f8f7fb}",
      ".auth-tabs{display:flex;border-bottom:1px solid rgba(255,255,255,.06)}",
      ".auth-tab{flex:1;padding:11px;text-align:center;font-family:'JetBrains Mono',monospace;font-size:.63rem;font-weight:700;letter-spacing:.1em;text-transform:uppercase;cursor:pointer;color:#4a4258;border:none;background:transparent;border-bottom:2px solid transparent;transition:color 120ms,border-color 120ms}",
      ".auth-tab.active{color:#b829ea;border-bottom-color:#b829ea}",
      ".auth-body{padding:22px 24px;display:flex;flex-direction:column;gap:14px}",
      ".auth-field{display:flex;flex-direction:column;gap:6px}",
      ".auth-label{font-size:.58rem;letter-spacing:.14em;text-transform:uppercase;color:#4a4258}",
      ".auth-input{background:rgba(255,255,255,.03);border:1px solid rgba(255,255,255,.08);color:#f8f7fb;font-family:'JetBrains Mono',monospace;font-size:.82rem;padding:10px 12px;outline:none;transition:border-color 150ms;width:100%;box-sizing:border-box}",
      ".auth-input:focus{border-color:rgba(184,41,234,.5)}",
      ".auth-error{font-size:.63rem;color:#ff2a4b;min-height:14px;letter-spacing:.04em}",
      ".auth-submit{background:#b829ea;color:#0a0514;border:none;font-family:'JetBrains Mono',monospace;font-size:.7rem;font-weight:800;letter-spacing:.14em;text-transform:uppercase;padding:12px;cursor:pointer;transition:background 150ms;width:100%}",
      ".auth-submit:hover{background:#c940f5}",
      ".auth-submit:disabled{opacity:.5;cursor:not-allowed}",
      ".auth-github{display:flex;align-items:center;justify-content:center;gap:10px;width:100%;padding:11px;background:rgba(255,255,255,.05);border:1px solid rgba(255,255,255,.12);color:#f8f7fb;font-family:'JetBrains Mono',monospace;font-size:.68rem;font-weight:700;letter-spacing:.08em;cursor:pointer;transition:background 150ms,border-color 150ms}",
      ".auth-github:hover{background:rgba(255,255,255,.1);border-color:rgba(255,255,255,.25)}",
      ".auth-github:disabled{opacity:.5;cursor:not-allowed}",
      ".auth-divider{display:flex;align-items:center;gap:12px;color:#4a4258;font-family:'JetBrains Mono',monospace;font-size:.58rem;letter-spacing:.1em}",
      ".auth-divider::before,.auth-divider::after{content:'';flex:1;height:1px;background:rgba(255,255,255,.06)}",
      /* mark complete pill */
      "#shoug-complete-btn{position:fixed;bottom:24px;right:24px;z-index:9000;display:flex;align-items:center;gap:10px;background:#0a0514;border:1px solid rgba(184,41,234,.35);padding:10px 16px 10px 12px;box-shadow:0 4px 24px rgba(0,0,0,.4);font-family:'JetBrains Mono',monospace;cursor:pointer;transition:border-color 150ms,background 150ms}",
      "#shoug-complete-btn:hover{border-color:rgba(184,41,234,.7);background:rgba(184,41,234,.08)}",
      "#shoug-complete-btn.done{border-color:rgba(34,197,94,.45)}",
      "#shoug-complete-btn.done:hover{border-color:rgba(34,197,94,.8);background:rgba(34,197,94,.06)}",
      ".complete-check{width:18px;height:18px;border:1px solid rgba(184,41,234,.5);display:flex;align-items:center;justify-content:center;flex-shrink:0;transition:background 150ms,border-color 150ms}",
      "#shoug-complete-btn.done .complete-check{border-color:rgba(34,197,94,.6);background:rgba(34,197,94,.12)}",
      ".complete-label{font-size:.6rem;letter-spacing:.1em;text-transform:uppercase;color:#8f8b9a}",
      "#shoug-complete-btn.done .complete-label{color:rgba(34,197,94,.85)}",
      /* light mode */
      "body.shoug-light-mode #shoug-auth-box,body.shoug-light-mode .shoug-user-dropdown,body.shoug-light-mode #shoug-complete-btn{background:#fff}",
      "body.shoug-light-mode .auth-input{color:#16111f;background:rgba(0,0,0,.03)}",
      "body.shoug-light-mode .auth-title{color:#16111f}",
      "body.shoug-light-mode .shoug-drop-link{color:#16111f}",
      "body.shoug-light-mode .shoug-drop-email,body.shoug-light-mode .shoug-notif-section{border-bottom-color:rgba(0,0,0,.08)}",
      "body.shoug-light-mode .shoug-notif-text{color:#3a3448}",
      "body.shoug-light-mode .shoug-notif-text strong{color:#16111f}",
      /* page comment section */
      "#shoug-page-comments{width:100%;max-width:var(--container-w,1400px);margin:56px auto 0;padding:0 max(4vw,20px) 48px;font-family:'JetBrains Mono',monospace;border-top:1px solid rgba(184,41,234,.14);box-sizing:border-box;}",
      /* header strip with brand accent */
      ".scmt-inner{position:relative;padding-top:32px;}",
      ".scmt-inner::before{content:'';position:absolute;top:0;left:0;right:0;height:2px;background:linear-gradient(90deg,#b829ea 0%,rgba(184,41,234,.2) 60%,transparent 100%);}",
      ".scmt-inner::after{content:'';position:absolute;top:0;left:0;width:64px;height:3px;background:#b829ea;}",
      ".scmt-head{display:flex;align-items:center;justify-content:space-between;margin-bottom:18px;}",
      ".scmt-tag{font-size:1.05rem;color:#b829ea;letter-spacing:.08em;text-transform:uppercase;font-weight:800;}",
      ".scmt-count{font-size:.6rem;color:#b829ea;letter-spacing:.1em;background:rgba(184,41,234,.1);border:1px solid rgba(184,41,234,.3);padding:5px 14px;}",
      /* comment list */
      ".scmt-list{display:flex;flex-direction:column;gap:10px;margin-bottom:28px;}",
      ".scmt-empty{font-size:.72rem;color:#4a4258;padding:28px 32px;text-align:center;border:1px dashed rgba(184,41,234,.12);letter-spacing:.06em;}",
      ".scmt-item{display:flex;gap:14px;align-items:flex-start;padding:18px 20px;background:rgba(255,255,255,.02);border:1px solid rgba(255,255,255,.06);transition:border-color 150ms;}",
      ".scmt-item:hover{border-color:rgba(184,41,234,.18);}",
      ".scmt-av{width:34px;height:34px;display:inline-flex;align-items:center;justify-content:center;font-size:.8rem;font-weight:800;flex-shrink:0;overflow:hidden;}",
      ".scmt-av img{width:100%;height:100%;object-fit:cover;display:block;}",
      ".scmt-body{flex:1;min-width:0;}",
      ".scmt-meta{display:flex;align-items:center;gap:8px;margin-bottom:8px;flex-wrap:wrap;}",
      ".scmt-author{font-size:.72rem;font-weight:800;}",
      ".scmt-uname{font-size:.62rem;color:#4a4258;}",
      ".scmt-time{font-size:.58rem;color:#4a4258;margin-left:auto;}",
      ".scmt-del{background:transparent;border:none;color:#4a4258;font-size:.6rem;cursor:pointer;padding:0 4px;margin-left:4px;transition:color 120ms;line-height:1;}",
      ".scmt-del:hover{color:#ff2a4b;}",
      ".scmt-text{font-size:.84rem;color:#8f8b9a;line-height:1.7;white-space:pre-wrap;word-break:break-word;font-family:'Inter',sans-serif;}",
      /* post form */
      ".scmt-form{background:rgba(184,41,234,.06);border:1px solid rgba(184,41,234,.22);padding:16px 20px;}",
      ".scmt-form-label{font-size:.58rem;color:#b829ea;letter-spacing:.16em;text-transform:uppercase;margin-bottom:14px;display:block;font-weight:800;}",
      ".scmt-form-row{display:flex;gap:12px;align-items:flex-start;margin-bottom:14px;}",
      ".scmt-input{flex:1;background:rgba(255,255,255,.03);border:1px solid rgba(255,255,255,.08);color:#f8f7fb;font-family:'Inter',sans-serif;font-size:.85rem;padding:10px 12px;outline:none;resize:vertical;transition:border-color 150ms;min-height:80px;line-height:1.6;}",
      ".scmt-input:focus{border-color:rgba(184,41,234,.45);background:rgba(184,41,234,.03);}",
      ".scmt-form-foot{display:flex;align-items:center;justify-content:space-between;gap:12px;}",
      ".scmt-as{font-size:.58rem;color:#4a4258;}",
      ".scmt-as strong{font-weight:700;}",
      ".scmt-post{height:36px;padding:0 20px;background:#b829ea;color:#0a0514;border:none;font-family:'JetBrains Mono',monospace;font-size:.65rem;font-weight:800;letter-spacing:.14em;text-transform:uppercase;cursor:pointer;transition:background 150ms,box-shadow 150ms;flex-shrink:0;}",
      ".scmt-post:hover{background:#c940f5;box-shadow:0 0 16px rgba(184,41,234,.3);}",
      ".scmt-post:disabled{opacity:.45;cursor:not-allowed;}",
      /* no-profile state */
      ".scmt-noprofile{font-size:.68rem;color:#4a4258;padding:22px;border:1px dashed rgba(255,255,255,.07);text-align:center;letter-spacing:.04em;}",
      ".scmt-noprofile a{color:#b829ea;text-decoration:none;font-weight:700;}",
      ".scmt-noprofile a:hover{text-decoration:underline;}",
      /* light mode */
      "body.shoug-light-mode .scmt-item{background:#fff;border-color:rgba(22,17,31,.08);}",
      "body.shoug-light-mode .scmt-item:hover{border-color:rgba(184,41,234,.25);}",
      "body.shoug-light-mode .scmt-form{background:rgba(184,41,234,.03);border-color:rgba(184,41,234,.18);}",
      "body.shoug-light-mode .scmt-input{color:#16111f;background:rgba(0,0,0,.02);border-color:rgba(0,0,0,.1);}",
      "body.shoug-light-mode .scmt-text{color:#534a61;}",
      "body.shoug-light-mode .scmt-empty,body.shoug-light-mode .scmt-noprofile{border-color:rgba(22,17,31,.1);}",
      /* reply threads */
      ".scmt-reply-wrap{display:flex;flex-direction:column;}",
      ".scmt-replies{margin-left:48px;border-left:2px solid rgba(255,255,255,.06);padding-left:14px;display:flex;flex-direction:column;gap:6px;margin-top:6px;}",
      "body.shoug-light-mode .scmt-replies{border-left-color:rgba(22,17,31,.08);}",
      ".scmt-item--reply{background:rgba(255,255,255,.015);}",
      "body.shoug-light-mode .scmt-item--reply{background:rgba(22,17,31,.015);}",
      ".scmt-reply-to{font-size:.56rem;color:#4a4258;font-style:italic;}",
      /* reply button */
      ".scmt-actions{display:flex;align-items:center;margin-top:5px;}",
      ".scmt-reply-btn{background:transparent;border:none;font-family:'JetBrains Mono',monospace;font-size:.56rem;color:#4a4258;cursor:pointer;padding:0;letter-spacing:.08em;text-transform:uppercase;transition:color 120ms;}",
      ".scmt-reply-btn:hover{color:#b829ea;}",
      /* inline reply form */
      ".scmt-inline-form{margin-top:8px;margin-left:48px;display:none;flex-direction:row;gap:8px;align-items:flex-start;}",
      ".scmt-inline-form.open{display:flex;}",
      ".scmt-inline-input{flex:1;background:rgba(255,255,255,.03);border:1px solid rgba(255,255,255,.08);color:#f8f7fb;font-family:'Inter',sans-serif;font-size:.82rem;padding:8px 11px;outline:none;resize:vertical;transition:border-color 150ms;min-height:58px;line-height:1.5;box-sizing:border-box;}",
      ".scmt-inline-input:focus{border-color:rgba(184,41,234,.45);background:rgba(184,41,234,.02);}",
      ".scmt-inline-input::placeholder{color:#2e2840;}",
      ".scmt-inline-actions{display:flex;flex-direction:column;gap:6px;flex-shrink:0;}",
      ".scmt-inline-post{height:32px;padding:0 14px;background:#b829ea;color:#0a0514;border:none;font-family:'JetBrains Mono',monospace;font-size:.58rem;font-weight:800;letter-spacing:.1em;text-transform:uppercase;cursor:pointer;transition:background 150ms;white-space:nowrap;}",
      ".scmt-inline-post:hover{background:#c940f5;}",
      ".scmt-inline-post:disabled{opacity:.45;cursor:not-allowed;}",
      ".scmt-inline-cancel{height:32px;padding:0 10px;background:transparent;border:1px solid rgba(255,255,255,.1);color:#4a4258;font-family:'JetBrains Mono',monospace;font-size:.58rem;cursor:pointer;text-transform:uppercase;letter-spacing:.06em;transition:border-color 150ms,color 150ms;}",
      ".scmt-inline-cancel:hover{border-color:rgba(255,255,255,.2);color:#8f8b9a;}",
      "body.shoug-light-mode .scmt-inline-input{color:#16111f;background:rgba(0,0,0,.02);border-color:rgba(0,0,0,.1);}",
      "body.shoug-light-mode .scmt-inline-input::placeholder{color:#b0a8c0;}",
      "body.shoug-light-mode .scmt-inline-cancel{border-color:rgba(0,0,0,.12);color:#8f8b9a;}",
      /* page icon buttons (bookmark + notes) */
      "#shoug-page-icons{position:fixed;bottom:74px;right:24px;z-index:9000;display:flex;gap:8px;}",
      ".shoug-icon-btn{width:36px;height:36px;display:flex;align-items:center;justify-content:center;background:#0a0514;border:1px solid rgba(255,255,255,.12);box-shadow:0 4px 20px rgba(0,0,0,.4);cursor:pointer;transition:border-color 150ms,background 150ms,color 150ms;color:#8f8b9a;flex-shrink:0;}",
      ".shoug-icon-btn:hover{border-color:rgba(184,41,234,.5);background:rgba(184,41,234,.06);color:#b829ea;}",
      ".shoug-icon-btn.active{border-color:rgba(184,41,234,.6);background:rgba(184,41,234,.1);color:#b829ea;}",
      /* notes panel */
      "#shoug-notes-panel{position:fixed;bottom:122px;right:24px;z-index:9000;width:300px;background:#0a0514;border:1px solid rgba(184,41,234,.35);box-shadow:0 8px 32px rgba(0,0,0,.5);display:none;flex-direction:column;}",
      "#shoug-notes-panel.open{display:flex;}",
      "#shoug-notes-panel::before{content:'';position:absolute;top:0;left:0;width:32px;height:2px;background:#b829ea;}",
      ".np-hdr{padding:10px 14px;border-bottom:1px solid rgba(255,255,255,.06);display:flex;align-items:center;justify-content:space-between;font-family:'JetBrains Mono',monospace;font-size:.52rem;color:#b829ea;letter-spacing:.18em;text-transform:uppercase;}",
      ".np-status{font-size:.48rem;color:#4a4258;letter-spacing:.04em;font-family:'JetBrains Mono',monospace;}",
      "#shoug-notes-ta{background:transparent;border:none;color:#f8f7fb;font-family:'Inter',sans-serif;font-size:.82rem;padding:12px 14px;resize:none;outline:none;min-height:130px;line-height:1.65;width:100%;box-sizing:border-box;}",
      "#shoug-notes-ta::placeholder{color:#2e2840;}",
      "body.shoug-light-mode #shoug-notes-panel{background:#fff;border-color:rgba(184,41,234,.3);}",
      "body.shoug-light-mode #shoug-notes-ta{color:#16111f;}",
      "body.shoug-light-mode .shoug-icon-btn{background:#fff;border-color:rgba(0,0,0,.12);}",
      /* theme toggle button */
      "#shoug-theme-toggle{width:34px;height:34px;display:inline-flex;align-items:center;justify-content:center;border:1px solid rgba(255,255,255,.12);background:rgba(255,255,255,.02);color:#f8f7fb;cursor:pointer;transition:border-color 160ms,color 160ms,background 160ms;flex-shrink:0;}",
      "#shoug-theme-toggle:hover{color:#b829ea;border-color:rgba(184,41,234,.55);background:rgba(184,41,234,.08);}",
      "#shoug-theme-toggle svg{width:15px;height:15px;display:block;}",
      "body.shoug-light-mode #shoug-theme-toggle{border-color:rgba(0,0,0,.12);background:transparent;color:#16111f;}",
      /* app-section tab bar */
      "#shoug-app-nav{position:relative;width:100%;max-width:100vw;height:40px;z-index:1;background:rgba(5,5,8,.96);border-bottom:1px solid rgba(255,255,255,.06);display:flex;align-items:stretch;overflow-x:auto;-webkit-overflow-scrolling:touch;scrollbar-width:none;}",
      "#shoug-app-nav::-webkit-scrollbar{display:none;}",
      ".shoug-app-tab{display:flex;align-items:center;flex-shrink:0;padding:0 20px;font-family:'JetBrains Mono',monospace;font-size:.58rem;font-weight:700;letter-spacing:.12em;text-transform:uppercase;color:#4a4258;text-decoration:none;border-bottom:2px solid transparent;transition:color 150ms,border-color 150ms;white-space:nowrap;}",
      ".shoug-app-tab:hover{color:#b829ea;}",
      ".shoug-app-tab.active{color:#b829ea;border-bottom-color:#b829ea;}",
      "body.shoug-light-mode #shoug-app-nav{background:rgba(255,255,255,.96);border-bottom-color:rgba(0,0,0,.08);}",
      "body.shoug-light-mode .shoug-app-tab.active{color:#b829ea;}",
      "@media(max-width:480px){#shoug-app-nav{height:38px;}.shoug-app-tab{padding:0 14px;font-size:.54rem;}#shoug-theme-toggle{margin-right:14px;}}",
      /* forgot password / reset link */
      ".auth-forgot{background:transparent;border:none;color:#4a4258;font-family:'JetBrains Mono',monospace;font-size:.58rem;cursor:pointer;padding:0;text-align:left;letter-spacing:.04em;transition:color 120ms;}",
      ".auth-forgot:hover{color:#b829ea;}",
      /* update-email mini modal */
      "#shoug-ue-modal{position:fixed;inset:0;z-index:99999;background:rgba(0,0,0,.75);backdrop-filter:blur(6px);display:none;align-items:center;justify-content:center;opacity:0;transition:opacity 150ms;}",
      "#shoug-ue-modal.open{opacity:1;display:flex;}",
      "#shoug-ue-box{width:min(380px,calc(100vw - 32px));background:#0a0514;border:1px solid rgba(184,41,234,.4);font-family:'JetBrains Mono',monospace;box-shadow:0 0 60px rgba(184,41,234,.15);}",
      "body.shoug-light-mode #shoug-ue-box{background:#fff;}",
      /* Blueprint credit bar */
      ".shoug-site-footer:has(#shoug-blueprint-bar){padding-bottom:18px;}",
      "#shoug-blueprint-bar{width:min(1440px,100%);margin:16px auto 0;padding:0;display:flex;align-items:center;justify-content:flex-end;border-top:0;font-family:'JetBrains Mono',monospace;font-size:.68rem;color:#5a5266;letter-spacing:.12em;box-sizing:border-box;}",
      "#shoug-blueprint-bar a{color:#b829ea;text-decoration:none;font-weight:700;transition:color 120ms;}",
      "#shoug-blueprint-bar a:hover{color:#c940f5;}",
      "body.shoug-light-mode #shoug-blueprint-bar{color:#8f8b9a;}",
      "@media(max-width:760px){.shoug-site-footer:has(#shoug-blueprint-bar){padding-bottom:22px;}#shoug-blueprint-bar{justify-content:flex-start;margin-top:20px;font-size:.66rem;}}",
    ].join("");
    document.head.appendChild(el);
  }

  function injectBlueprintCredit() {
    if (document.getElementById("shoug-blueprint-bar")) return;
    var footer = document.querySelector(".shoug-site-footer");
    if (!footer) return;
    var bar = document.createElement("div");
    bar.id = "shoug-blueprint-bar";
    bar.innerHTML = 'Made by&nbsp;<a href="https://blueprint.shoug-tech.com/" target="_blank" rel="noopener">Blueprint</a>';
    footer.appendChild(bar);
  }

  // ── Auth Modal ────────────────────────────────────────────────────────────

  var modal, emailInput, passInput, errorEl, submitEl, currentTab;

  function buildModal() {
    if (document.getElementById("shoug-auth-modal")) return;
    modal = document.createElement("div");
    modal.id = "shoug-auth-modal";
    modal.innerHTML = [
      '<div id="shoug-auth-box">',
      '  <div class="auth-head">',
      '    <div><div class="auth-tag">// IDENTITY PROTOCOL</div><div class="auth-title" id="auth-modal-title">Sign In</div></div>',
      '    <button class="auth-close" id="auth-close-btn">✕</button>',
      '  </div>',
      '  <div class="auth-tabs">',
      '    <button class="auth-tab active" data-tab="signin">Sign In</button>',
      '    <button class="auth-tab" data-tab="signup">Create Account</button>',
      '  </div>',
      '  <div class="auth-body">',
      '    <button class="auth-github" id="auth-github"><svg width="16" height="16" viewBox="0 0 16 16" fill="currentColor"><path d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27.68 0 1.36.09 2 .27 1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.013 8.013 0 0016 8c0-4.42-3.58-8-8-8z"/></svg> Continue with GitHub</button>',
      '    <div class="auth-divider"><span>or</span></div>',
      '    <div class="auth-field"><label class="auth-label">Email</label><input class="auth-input" id="auth-email" type="email" placeholder="your@email.com" autocomplete="email"></div>',
      '    <div class="auth-field"><label class="auth-label">Password</label><input class="auth-input" id="auth-pass" type="password" placeholder="••••••••" autocomplete="current-password"></div>',
      '    <button class="auth-forgot" id="auth-forgot">Forgot password?</button>',
      '    <div class="auth-error" id="auth-error"></div>',
      '    <button class="auth-submit" id="auth-submit">Sign In</button>',
      '  </div>',
      '  <div class="auth-body" id="auth-reset-body" style="display:none">',
      '    <div class="auth-field"><label class="auth-label">Your Email</label><input class="auth-input" id="auth-reset-email" type="email" placeholder="your@email.com" autocomplete="email"></div>',
      '    <div class="auth-error" id="auth-reset-error"></div>',
      '    <button class="auth-submit" id="auth-reset-submit">Send Reset Link</button>',
      '    <button class="auth-forgot" id="auth-reset-back" style="margin-top:4px">← Back to Sign In</button>',
      '  </div>',
      '</div>',
    ].join("");
    document.body.appendChild(modal);

    emailInput = document.getElementById("auth-email");
    passInput = document.getElementById("auth-pass");
    errorEl = document.getElementById("auth-error");
    submitEl = document.getElementById("auth-submit");
    currentTab = "signin";

    document.getElementById("auth-close-btn").addEventListener("click", closeModal);
    modal.addEventListener("click", function (e) { if (e.target === modal) closeModal(); });
    passInput.addEventListener("keydown", function (e) { if (e.key === "Enter") doSubmit(); });
    submitEl.addEventListener("click", doSubmit);
    document.getElementById("auth-github").addEventListener("click", doGithub);
    document.getElementById("auth-forgot").addEventListener("click", showResetView);
    document.getElementById("auth-reset-back").addEventListener("click", hideResetView);
    document.getElementById("auth-reset-submit").addEventListener("click", doResetPassword);
    document.getElementById("auth-reset-email").addEventListener("keydown", function(e) { if (e.key === "Enter") doResetPassword(); });

    modal.querySelectorAll(".auth-tab").forEach(function (tab) {
      tab.addEventListener("click", function () {
        currentTab = tab.dataset.tab;
        modal.querySelectorAll(".auth-tab").forEach(function (t) { t.classList.remove("active"); });
        tab.classList.add("active");
        submitEl.textContent = currentTab === "signin" ? "Sign In" : "Create Account";
        errorEl.textContent = "";
        var forgotBtn = document.getElementById("auth-forgot");
        if (forgotBtn) forgotBtn.style.display = currentTab === "signin" ? "" : "none";
        hideResetView();
      });
    });
  }

  function showResetView() {
    var main = document.querySelector("#shoug-auth-box .auth-body:not(#auth-reset-body)");
    var reset = document.getElementById("auth-reset-body");
    var tabs = document.querySelector(".auth-tabs");
    if (main) main.style.display = "none";
    if (tabs) tabs.style.display = "none";
    if (reset) { reset.style.display = "flex"; document.getElementById("auth-reset-email").focus(); }
    document.getElementById("auth-modal-title").textContent = "Reset Password";
  }

  function hideResetView() {
    var main = document.querySelector("#shoug-auth-box .auth-body:not(#auth-reset-body)");
    var reset = document.getElementById("auth-reset-body");
    var tabs = document.querySelector(".auth-tabs");
    if (main) main.style.display = "";
    if (tabs) tabs.style.display = "";
    if (reset) { reset.style.display = "none"; document.getElementById("auth-reset-error").textContent = ""; }
    document.getElementById("auth-modal-title").textContent = "Sign In";
  }

  function doResetPassword() {
    var emailEl = document.getElementById("auth-reset-email");
    var errEl = document.getElementById("auth-reset-error");
    var btn = document.getElementById("auth-reset-submit");
    var email = emailEl ? emailEl.value.trim() : "";
    if (!email) { errEl.textContent = "Enter your email address."; return; }
    btn.disabled = true;
    btn.textContent = "Sending…";
    firebase.auth().sendPasswordResetEmail(email)
      .then(function() {
        errEl.style.color = "#22c55e";
        errEl.textContent = "Reset link sent — check your inbox.";
        btn.textContent = "Sent ✓";
      })
      .catch(function(err) {
        errEl.style.color = "";
        errEl.textContent = authError(err.code) || "Could not send reset email.";
        btn.disabled = false;
        btn.textContent = "Send Reset Link";
      });
  }

  function openModal() {
    buildModal();
    modal.style.display = "flex";
    requestAnimationFrame(function () { modal.classList.add("open"); });
    document.body.style.overflow = "hidden";
    setTimeout(function () { emailInput && emailInput.focus(); }, 60);
  }

  function closeModal() {
    if (!modal) return;
    modal.classList.remove("open");
    document.body.style.overflow = "";
    setTimeout(function () { modal.style.display = "none"; }, 150);
  }

  function doSubmit() {
    var email = emailInput.value.trim();
    var pass = passInput.value;
    errorEl.textContent = "";
    if (!email || !pass) { errorEl.textContent = "Email and password required."; return; }
    submitEl.disabled = true;
    submitEl.textContent = "Loading…";
    var fn = currentTab === "signin"
      ? firebase.auth().signInWithEmailAndPassword(email, pass)
      : firebase.auth().createUserWithEmailAndPassword(email, pass);
    fn.then(closeModal).catch(function (err) {
      errorEl.textContent = authError(err.code);
      submitEl.disabled = false;
      submitEl.textContent = currentTab === "signin" ? "Sign In" : "Create Account";
    });
  }

  var GITHUB_BTN_HTML = '<svg width="16" height="16" viewBox="0 0 16 16" fill="currentColor"><path d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27.68 0 1.36.09 2 .27 1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.013 8.013 0 0016 8c0-4.42-3.58-8-8-8z"/></svg> Continue with GitHub';

  function doGithub() {
    var btn = document.getElementById("auth-github");
    if (btn) { btn.disabled = true; btn.textContent = "Redirecting…"; }
    var provider = new firebase.auth.GithubAuthProvider();
    firebase.auth().signInWithPopup(provider)
      .then(closeModal)
      .catch(function (err) {
        // Popups are unreliable on iOS/iPad Safari and in-app browsers — fall back to a full redirect.
        if (err.code === "auth/popup-blocked" || err.code === "auth/operation-not-supported-in-this-environment" || err.code === "auth/cancelled-popup-request") {
          firebase.auth().signInWithRedirect(provider);
          return;
        }
        if (errorEl) errorEl.textContent = err.code === "auth/popup-closed-by-user" ? "" : (err.message || "GitHub sign-in failed.");
        if (btn) { btn.disabled = false; btn.innerHTML = GITHUB_BTN_HTML; }
      });
  }

  function authError(code) {
    return ({
      "auth/user-not-found": "No account with that email.",
      "auth/wrong-password": "Incorrect password.",
      "auth/invalid-credential": "Invalid email or password.",
      "auth/email-already-in-use": "Email already in use.",
      "auth/weak-password": "Password must be 6+ characters.",
      "auth/invalid-email": "Invalid email address.",
      "auth/too-many-requests": "Too many attempts — try again later.",
      "auth/requires-recent-login": "Re-enter your password to confirm.",
    })[code] || "Something went wrong. Try again.";
  }

  // ── Update Email Modal ────────────────────────────────────────────────────

  function openUpdateEmailModal(user) {
    var existing = document.getElementById("shoug-ue-modal");
    if (existing) existing.remove();

    var m = document.createElement("div");
    m.id = "shoug-ue-modal";
    m.innerHTML = [
      '<div id="shoug-ue-box">',
      '  <div class="auth-head">',
      '    <div><div class="auth-tag">// ACCOUNT SETTINGS</div><div class="auth-title">Update Email</div></div>',
      '    <button class="auth-close" id="ue-close">✕</button>',
      '  </div>',
      '  <div class="auth-body">',
      '    <div class="auth-field"><label class="auth-label">New Email Address</label><input class="auth-input" id="ue-new-email" type="email" placeholder="new@email.com" autocomplete="email"></div>',
      '    <div class="auth-field"><label class="auth-label">Current Password</label><input class="auth-input" id="ue-pass" type="password" placeholder="••••••••" autocomplete="current-password"></div>',
      '    <div class="auth-error" id="ue-error"></div>',
      '    <button class="auth-submit" id="ue-submit">Update Email</button>',
      '  </div>',
      '</div>',
    ].join("");
    document.body.appendChild(m);

    var closeUe = function() {
      m.classList.remove("open");
      document.body.style.overflow = "";
      setTimeout(function() { m.remove(); }, 150);
    };
    document.getElementById("ue-close").addEventListener("click", closeUe);
    m.addEventListener("click", function(e) { if (e.target === m) closeUe(); });

    var newEmailEl = document.getElementById("ue-new-email");
    var passEl = document.getElementById("ue-pass");
    var errEl = document.getElementById("ue-error");
    var btn = document.getElementById("ue-submit");

    function doUpdateEmail() {
      var newEmail = newEmailEl.value.trim();
      var pass = passEl.value;
      errEl.style.color = "";
      errEl.textContent = "";
      if (!newEmail || !pass) { errEl.textContent = "Fill in both fields."; return; }
      btn.disabled = true;
      btn.textContent = "Updating…";
      var cred = firebase.auth.EmailAuthProvider.credential(user.email, pass);
      user.reauthenticateWithCredential(cred)
        .then(function() { return user.updateEmail(newEmail); })
        .then(function() {
          errEl.style.color = "#22c55e";
          errEl.textContent = "Email updated successfully.";
          btn.textContent = "Done ✓";
          var emailEl = document.getElementById("shoug-drop-email");
          if (emailEl) emailEl.textContent = newEmail;
        })
        .catch(function(err) {
          errEl.textContent = authError(err.code);
          btn.disabled = false;
          btn.textContent = "Update Email";
        });
    }

    btn.addEventListener("click", doUpdateEmail);
    passEl.addEventListener("keydown", function(e) { if (e.key === "Enter") doUpdateEmail(); });

    m.style.display = "flex";
    requestAnimationFrame(function() { m.classList.add("open"); });
    document.body.style.overflow = "hidden";
    setTimeout(function() { newEmailEl && newEmailEl.focus(); }, 60);
  }

  // ── Notifications ─────────────────────────────────────────────────────────

  var _notifUnsub = null;

  function timeAgo(date) {
    var s = Math.floor((Date.now() - date.getTime()) / 1000);
    if (s < 60) return "just now";
    var m = Math.floor(s / 60);
    if (m < 60) return m + "m ago";
    var h = Math.floor(m / 60);
    if (h < 24) return h + "h ago";
    var d = Math.floor(h / 24);
    return d + "d ago";
  }

  function writeNotif(toUid, data) {
    if (!toUid || !data) return;
    firebase.firestore()
      .collection("notifications").doc(toUid).collection("items")
      .add(Object.assign({ read: false, createdAt: firebase.firestore.FieldValue.serverTimestamp() }, data))
      .catch(function() {});
  }

  function renderNotifDropdown(docs) {
    var list = document.getElementById("shoug-notif-list");
    if (!list) return;
    if (!docs || !docs.length) {
      list.innerHTML = '<div class="shoug-notif-empty">No new notifications</div>';
      return;
    }
    list.innerHTML = docs.map(function(d) {
      var n = d.data();
      var when = n.createdAt ? timeAgo(n.createdAt.toDate()) : "";
      var pageLabel = n.pageUrl ? n.pageUrl.replace(/^\/|\/$/g, "").split("/").pop() || "page" : "page";
      return '<a class="shoug-notif-item unread" href="' + escHtml(n.pageUrl || "/") + '">'
        + '<span class="shoug-notif-text"><strong>' + escHtml(n.fromDisplayName || n.fromUsername || "Someone") + '</strong>'
        + ' replied to your comment' + (pageLabel ? ' on <strong>' + escHtml(pageLabel) + '</strong>' : '') + '</span>'
        + (n.commentPreview ? '<span class="shoug-notif-preview">"' + escHtml(n.commentPreview) + '"</span>' : "")
        + '<span class="shoug-notif-time">' + when + '</span>'
        + '</a>';
    }).join("");
  }

  function startNotifListener(user) {
    if (_notifUnsub) { _notifUnsub(); _notifUnsub = null; }
    _notifUnsub = firebase.firestore()
      .collection("notifications").doc(user.uid).collection("items")
      .where("read", "==", false)
      .orderBy("createdAt", "desc")
      .limit(20)
      .onSnapshot(function(snap) {
        var count = snap.size;
        var badge = document.getElementById("shoug-notif-badge");
        if (badge) {
          badge.textContent = count > 9 ? "9+" : String(count);
          badge.style.display = count > 0 ? "flex" : "none";
        }
        // Don't wipe the visible list while the dropdown is open (happens right after
        // markNotifsRead fires). The list will clear naturally the next time it opens.
        var btn = document.getElementById("shoug-fb-user");
        var dropdownOpen = btn && btn.classList.contains("open");
        if (!dropdownOpen || count > 0) {
          renderNotifDropdown(snap.docs);
        }
      }, function() {});
  }

  function markNotifsRead(user) {
    firebase.firestore()
      .collection("notifications").doc(user.uid).collection("items")
      .where("read", "==", false).limit(20).get()
      .then(function(snap) {
        if (snap.empty) return;
        var batch = firebase.firestore().batch();
        snap.forEach(function(d) { batch.update(d.ref, { read: true }); });
        return batch.commit();
      }).catch(function() {});
  }

  // ── Header button ─────────────────────────────────────────────────────────

  function setHeaderButton(user) {
    var old = document.getElementById("shoug-fb-user");
    var actions = document.querySelector(".shoug-header-actions");
    if (!actions) return;
    if (old) old.remove();

    var el = document.createElement(user ? "div" : "button");
    el.id = "shoug-fb-user";

    if (!user) {
      el.className = "shoug-auth-btn";
      el.textContent = "Sign In";
      el.addEventListener("click", openModal);
    } else {
      el.className = "shoug-user-btn";
      el.style.position = "relative";
      el.innerHTML = [
        '<span id="shoug-user-avatar">' + escHtml((user.email || "U")[0].toUpperCase()) + '</span>',
        '<span class="shoug-notif-badge" id="shoug-notif-badge" style="display:none"></span>',
        '<div class="shoug-user-dropdown">',
        '  <div class="shoug-notif-section" id="shoug-notif-section">',
        '    <div class="shoug-notif-hdr">// Notifications</div>',
        '    <div id="shoug-notif-list"><div class="shoug-notif-empty">No new notifications</div></div>',
        '  </div>',
        '  <div class="shoug-drop-email" id="shoug-drop-email">' + escHtml(user.email || "") + "</div>",
        '  <a class="shoug-drop-link" href="/community/profile/?u=' + encodeURIComponent(user.uid) + '">My Profile</a>',
        '  <a class="shoug-drop-link" href="/bookmarks/">Bookmarks</a>',
        '  <a class="shoug-drop-link" href="/account/">My Progress</a>',
        '  <a class="shoug-drop-link" href="/community/">Community</a>',
        '  <button class="shoug-drop-link red" id="shoug-signout">Sign Out</button>',
        "</div>",
      ].join("");
      actions.insertBefore(el, actions.firstChild);

      el.addEventListener("click", function (e) {
        var wasOpen = el.classList.contains("open");
        el.classList.toggle("open");
        e.stopPropagation();
        // Mark read when closing (so user can see notifications while dropdown is open)
        if (wasOpen) markNotifsRead(user);
      });
      document.addEventListener("click", function () {
        if (el.classList.contains("open")) markNotifsRead(user);
        el.classList.remove("open");
      });
      el.querySelector("#shoug-signout").addEventListener("click", function (e) {
        e.stopPropagation();
        firebase.auth().signOut();
      });
      startNotifListener(user);

      firebase.firestore().collection("users").doc(user.uid).get().then(function (doc) {
        if (!doc.exists) return;
        var url = avatarUrl(doc.data().avatarPreset);
        if (!url) return;
        var av = el.querySelector("#shoug-user-avatar");
        if (av) av.outerHTML = '<img id="shoug-user-avatar" class="shoug-user-avatar-img" src="' + url + '" alt="">';
      }).catch(function () {});

      return;
    }

    actions.insertBefore(el, actions.firstChild);
  }

  // ── Progress bar ──────────────────────────────────────────────────────────

  var completeBtn = null;

  function pageDoc(user) {
    var slug = pageSlug();
    return firebase.firestore()
      .collection("userProgress").doc(user.uid)
      .collection("pages").doc(slug);
  }

  function injectCompleteBtn(user) {
    if (!isContentPage()) return;
    if (window.location.pathname.indexOf("/academics/") !== 0) return;
    if (document.getElementById("shoug-complete-btn")) return;

    completeBtn = document.createElement("div");
    completeBtn.id = "shoug-complete-btn";
    completeBtn.innerHTML = [
      '<div class="complete-check" id="complete-icon"></div>',
      '<span class="complete-label" id="complete-label">Mark as complete</span>',
    ].join("");
    document.body.appendChild(completeBtn);

    pageDoc(user).get().then(function (doc) {
      if (doc.exists && doc.data().completed) setDone(true);
    });

    completeBtn.addEventListener("click", function () {
      var isDone = completeBtn.classList.contains("done");
      var next = !isDone;
      setDone(next);
      var path = window.location.pathname;
      var data = {
        url: path,
        title: pageTitle(),
        section: path.split("/")[1] || "home",
        completed: next,
        updatedAt: firebase.firestore.FieldValue.serverTimestamp(),
      };
      if (next) data.completedAt = firebase.firestore.FieldValue.serverTimestamp();
      pageDoc(user).set(data, { merge: true });

      // Sync totalCompleted on the user doc
      firebase.firestore().collection("users").doc(user.uid).set(
        { totalCompleted: firebase.firestore.FieldValue.increment(next ? 1 : -1) },
        { merge: true }
      );

      // Sync coursesActive: recount distinct completed courses from userProgress
      firebase.firestore().collection("userProgress").doc(user.uid)
        .collection("pages").where("completed", "==", true).get()
        .then(function(snap) {
          var seen = {};
          snap.forEach(function(doc) {
            var url = (doc.data().url || "").replace(/^\/+/, "");
            var parts = url.split("/").filter(Boolean);
            if (parts.length >= 3) seen[parts[0] + "/" + parts[1] + "/" + parts[2]] = true;
          });
          firebase.firestore().collection("users").doc(user.uid)
            .update({ coursesActive: Object.keys(seen).length })
            .catch(function() {});
        });
    });
  }

  function setDone(done) {
    if (!completeBtn) return;
    completeBtn.classList.toggle("done", done);
    document.getElementById("complete-icon").innerHTML = done
      ? '<svg width="11" height="11" viewBox="0 0 11 11" fill="none"><path d="M1.5 5.5l3 3 5-5" stroke="#22c55e" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/></svg>'
      : "";
    document.getElementById("complete-label").textContent = done ? "Completed" : "Mark as complete";
  }

  function removeCompleteBtn() {
    if (completeBtn) { completeBtn.remove(); completeBtn = null; }
    var el = document.getElementById("shoug-complete-btn");
    if (el) el.remove();
  }

  // ── Page Comment Section ──────────────────────────────────────────────────

  var _cmtUnsub = null;
  var _cmtProfile = null;

  function removeCommentSection() {
    if (_cmtUnsub) { _cmtUnsub(); _cmtUnsub = null; }
    var el = document.getElementById("shoug-page-comments");
    if (el) el.remove();
    _cmtProfile = null;
  }

  function injectCommentSection(user) {
    if (!isContentPage()) return;
    if (document.getElementById("shoug-page-comments")) return;
    firebase.firestore().collection("users").doc(user.uid).get()
      .catch(function() { return { exists: false, data: function() { return null; } }; })
      .then(function(doc) {
        _cmtProfile = doc.exists ? doc.data() : null;
        buildCommentSection(user);
      });
  }

  function buildCommentSection(user) {
    if (document.getElementById("shoug-page-comments")) return;
    var slug = pageSlug();
    var p = _cmtProfile;
    var hasProfile = p && p.username;
    var c = hasProfile ? (p.avatarColor || "#b829ea") : "#b829ea";
    var init = hasProfile ? escHtml((p.displayName || p.username || "?")[0].toUpperCase()) : "?";

    var formHtml = hasProfile
      ? '<div class="scmt-form">'
          + '<span class="scmt-form-label">Leave a comment</span>'
          + '<div class="scmt-form-row">'
          + avatarBlock("scmt-av", p.avatarPreset, c, init)
          + '<textarea class="scmt-input" id="scmt-input" placeholder="Share your thoughts, ask a question, or help a classmate…" rows="3" maxlength="1000"></textarea>'
          + '</div>'
          + '<div class="scmt-form-foot">'
          + '<span class="scmt-as">Posting as <strong style="color:'+c+'">@'+escHtml(p.username)+'</strong> &nbsp;·&nbsp; Ctrl+Enter to post</span>'
          + '<button class="scmt-post" id="scmt-post">Post Comment</button>'
          + '</div>'
          + '</div>'
      : '<div class="scmt-noprofile">Set up a <a href="/account/">community profile</a> on your dashboard to join the discussion.</div>';

    var wrap = document.createElement("section");
    wrap.id = "shoug-page-comments";
    wrap.innerHTML = '<div class="scmt-inner">'
      + '<div class="scmt-head"><span class="scmt-tag">// Discussion</span><span class="scmt-count" id="scmt-count"></span></div>'
      + '<div class="scmt-list" id="scmt-list"><div class="scmt-empty">Loading comments…</div></div>'
      + formHtml
      + '</div>';

    var embedWrapper = document.querySelector(".embed-area-wrapper");
    var contentArea  = document.querySelector(".content-area");
    if (embedWrapper && contentArea) {
      contentArea.style.overflow = "visible";
      contentArea.style.display = "block";
      embedWrapper.style.flex = "none";
      embedWrapper.after(wrap);
    } else {
      // Always append as the very last child of <main> so the discussion
      // appears after ALL page content. The wrap's own CSS handles width/centering.
      var mainEl = document.querySelector("main");
      if (mainEl) {
        mainEl.appendChild(wrap);
      } else {
        var footer = document.querySelector("footer");
        if (footer) { footer.before(wrap); } else { document.body.appendChild(wrap); }
      }
    }

    if (hasProfile) {
      var input = document.getElementById("scmt-input");
      var btn = document.getElementById("scmt-post");
      btn.addEventListener("click", function() { postPageComment(user, slug, input, btn); });
      input.addEventListener("keydown", function(e) {
        if ((e.ctrlKey || e.metaKey) && e.key === "Enter") postPageComment(user, slug, input, btn);
      });
    }

    _cmtUnsub = firebase.firestore()
      .collection("pageComments").doc(slug).collection("comments")
      .orderBy("createdAt", "asc").limit(100)
      .onSnapshot(function(snap) { renderCommentList(snap, user); },
        function() {
          var list = document.getElementById("scmt-list");
          if (list) list.innerHTML = '<div class="scmt-empty">Comments unavailable — update your Firestore rules to enable this.</div>';
        });
  }

  function renderCommentList(snap, user) {
    var list = document.getElementById("scmt-list");
    var countEl = document.getElementById("scmt-count");
    if (!list) return;
    var all = [];
    snap.forEach(function(doc) { all.push(Object.assign({ id: doc.id }, doc.data())); });

    // Separate top-level comments from replies
    var topLevel = all.filter(function(c) { return !c.replyTo; });
    var replyMap = {};
    all.forEach(function(c) {
      if (c.replyTo) {
        if (!replyMap[c.replyTo]) replyMap[c.replyTo] = [];
        replyMap[c.replyTo].push(c);
      }
    });
    Object.keys(replyMap).forEach(function(k) {
      replyMap[k].sort(function(a, b) {
        var ta = a.createdAt && a.createdAt.toDate ? a.createdAt.toDate().getTime() : 0;
        var tb = b.createdAt && b.createdAt.toDate ? b.createdAt.toDate().getTime() : 0;
        return ta - tb;
      });
    });

    if (countEl) countEl.textContent = all.length ? all.length + " comment" + (all.length !== 1 ? "s" : "") : "";
    if (!topLevel.length) { list.innerHTML = '<div class="scmt-empty">No comments yet — be the first!</div>'; return; }

    var slug = pageSlug();
    var hasProfile = _cmtProfile && _cmtProfile.username;

    function commentHtml(cm, isReply) {
      var ts = cm.createdAt && cm.createdAt.toDate ? cm.createdAt.toDate() : new Date();
      var timeStr = ts.toLocaleDateString("en-US", { month: "short", day: "numeric", year: "numeric" });
      var isMe = cm.uid === user.uid;
      var cc = cm.avatarColor || "#b829ea";
      var ci = escHtml((cm.displayName || cm.username || "?")[0].toUpperCase());
      return '<div class="scmt-item' + (isReply ? " scmt-item--reply" : "") + '" data-id="' + escHtml(cm.id) + '">'
        + avatarBlock("scmt-av", cm.avatarPreset, cc, ci)
        + '<div class="scmt-body">'
        + '<div class="scmt-meta">'
        + (isReply && cm.replyToUsername ? '<span class="scmt-reply-to">↳ @'+escHtml(cm.replyToUsername)+'&nbsp;&nbsp;</span>' : "")
        + '<span class="scmt-author" style="color:'+cc+'">'+escHtml(cm.displayName || cm.username || "Unknown")+'</span>'
        + '<span class="scmt-uname">@'+escHtml(cm.username || "")+'</span>'
        + '<span class="scmt-time">'+escHtml(timeStr)+'</span>'
        + (isMe ? '<button class="scmt-del" data-id="'+escHtml(cm.id)+'" data-slug="'+escHtml(slug)+'">✕</button>' : "")
        + '</div>'
        + '<div class="scmt-text">'+escHtml(cm.text)+'</div>'
        + (hasProfile && !isReply ? '<div class="scmt-actions"><button class="scmt-reply-btn" data-id="'+escHtml(cm.id)+'">↳ Reply</button></div>' : "")
        + '</div></div>';
    }

    list.innerHTML = topLevel.map(function(cm) {
      var replies = replyMap[cm.id] || [];
      var html = '<div class="scmt-reply-wrap">' + commentHtml(cm, false);
      if (hasProfile) {
        html += '<div class="scmt-inline-form" id="rform-'+escHtml(cm.id)+'">'
          + '<textarea class="scmt-inline-input" placeholder="Write a reply…" rows="2" maxlength="500"></textarea>'
          + '<div class="scmt-inline-actions">'
          + '<button class="scmt-inline-post">Reply</button>'
          + '<button class="scmt-inline-cancel">Cancel</button>'
          + '</div></div>';
      }
      if (replies.length) {
        html += '<div class="scmt-replies">' + replies.map(function(r) { return commentHtml(r, true); }).join("") + '</div>';
      }
      return html + '</div>';
    }).join("");

    // Delete buttons
    list.querySelectorAll(".scmt-del").forEach(function(btn) {
      btn.addEventListener("click", function(e) {
        e.stopPropagation();
        if (!confirm("Delete this comment?")) return;
        firebase.firestore().collection("pageComments").doc(btn.dataset.slug)
          .collection("comments").doc(btn.dataset.id).delete();
      });
    });

    // Reply buttons → open inline form
    if (hasProfile) {
      list.querySelectorAll(".scmt-reply-btn").forEach(function(btn) {
        btn.addEventListener("click", function() {
          var parentId = btn.dataset.id;
          list.querySelectorAll(".scmt-inline-form.open").forEach(function(f) { f.classList.remove("open"); });
          var form = document.getElementById("rform-" + parentId);
          if (!form) return;
          form.classList.add("open");
          var ta = form.querySelector(".scmt-inline-input");
          if (ta) { ta.value = ""; ta.focus(); }
        });
      });

      list.querySelectorAll(".scmt-inline-form").forEach(function(form) {
        var parentId = form.id.replace("rform-", "");
        var parentCm = topLevel.filter(function(c) { return c.id === parentId; })[0];
        var parentUsername = parentCm ? (parentCm.username || "") : "";
        var ta = form.querySelector(".scmt-inline-input");
        var postBtn = form.querySelector(".scmt-inline-post");
        var cancelBtn = form.querySelector(".scmt-inline-cancel");

        if (cancelBtn) cancelBtn.addEventListener("click", function() { form.classList.remove("open"); });

        function doReply() {
          var text = ta ? ta.value.trim() : "";
          if (!text) return;
          postBtn.disabled = true;
          firebase.firestore().collection("pageComments").doc(slug).collection("comments").add({
            uid: user.uid,
            username: _cmtProfile.username || "",
            displayName: _cmtProfile.displayName || "",
            avatarColor: _cmtProfile.avatarColor || "#b829ea",
            avatarPreset: _cmtProfile.avatarPreset != null ? _cmtProfile.avatarPreset : null,
            text: text,
            replyTo: parentId,
            replyToUsername: parentUsername,
            createdAt: firebase.firestore.FieldValue.serverTimestamp(),
          }).then(function() {
            if (ta) ta.value = "";
            form.classList.remove("open");
            postBtn.disabled = false;
            // Notify the parent comment's author
            if (parentCm && parentCm.uid && parentCm.uid !== user.uid) {
              writeNotif(parentCm.uid, {
                type: "reply",
                fromUid: user.uid,
                fromUsername: _cmtProfile.username || "",
                fromDisplayName: _cmtProfile.displayName || "",
                fromAvatarColor: _cmtProfile.avatarColor || "#b829ea",
                pageUrl: window.location.pathname,
                commentPreview: text.slice(0, 120),
              });
            }
          }).catch(function() { postBtn.disabled = false; });
        }

        if (postBtn) postBtn.addEventListener("click", doReply);
        if (ta) {
          ta.addEventListener("keydown", function(e) {
            if ((e.ctrlKey || e.metaKey) && e.key === "Enter") doReply();
            if (e.key === "Escape") form.classList.remove("open");
          });
        }
      });
    }
  }

  function postPageComment(user, slug, input, btn) {
    var text = input ? input.value.trim() : "";
    if (!text || !_cmtProfile) return;
    btn.disabled = true;
    firebase.firestore().collection("pageComments").doc(slug).collection("comments").add({
      uid: user.uid,
      username: _cmtProfile.username || "",
      displayName: _cmtProfile.displayName || "",
      avatarColor: _cmtProfile.avatarColor || "#b829ea",
      avatarPreset: _cmtProfile.avatarPreset != null ? _cmtProfile.avatarPreset : null,
      text: text,
      createdAt: firebase.firestore.FieldValue.serverTimestamp(),
    }).then(function() {
      input.value = "";
      btn.disabled = false;
    }).catch(function() {
      btn.disabled = false;
    });
  }

  // ── Onboarding ────────────────────────────────────────────────────────────

  function showOnboarding() {
    // Detect page context so each section type gets its own contextual walkthrough
    var path = window.location.pathname;
    var parts = path.replace(/\/$/, "").split("/").filter(Boolean);
    // parts: [] = home, ["academics"] = hub, ["academics","computer-science"] = subject,
    //        ["academics","computer-science","cs285"] = course overview, 4+ = content leaf

    var context, storageKey;
    if (parts.length === 0) {
      context = "home";
      storageKey = "shoug-onboarded";
    } else if (parts[0] === "academics") {
      if (parts.length === 1) { context = "academics-index"; storageKey = "shoug-ob-academics"; }
      else if (parts.length === 2) { context = "academics-subject"; storageKey = "shoug-ob-subject"; }
      else { context = "academics-course"; storageKey = "shoug-ob-course"; }
    } else if (parts[0] === "resources") {
      context = "resources"; storageKey = "shoug-ob-resources";
    } else if (parts[0] === "workshops") {
      if (parts.length === 1) { context = "workshops"; storageKey = "shoug-ob-workshops"; }
      else { context = "workshop-detail"; storageKey = "shoug-ob-workshop-detail"; }
    } else if (parts[0] === "about") {
      context = "about"; storageKey = "shoug-ob-about";
    } else if (parts[0] === "work") {
      if (parts.length === 1) { context = "work"; storageKey = "shoug-ob-work"; }
      else { context = "work-detail"; storageKey = "shoug-ob-work-detail"; }
    } else if (parts[0] === "community") {
      if (parts.length === 1) { context = "community"; storageKey = "shoug-ob-community"; }
      else { context = "community-profile"; storageKey = "shoug-ob-profile"; }
    } else if (parts[0] === "account") {
      context = "account"; storageKey = "shoug-ob-account";
    } else if (parts[0] === "bookmarks") {
      context = "bookmarks"; storageKey = "shoug-ob-bookmarks";
    } else if (parts[0] === "academic-plan-themes") {
      context = "academic-plan-themes"; storageKey = "shoug-ob-apt";
    } else {
      return; // No walkthrough for unrecognised pages (policy, career-development, etc.)
    }

    if (localStorage.getItem(storageKey)) return;

    // Header is z-index:10000 (fixed). Overlay below header = 9999 lets header show through.
    // Overlay above header = 10001 covers everything (used for center/no-target steps).
    var HDR_Z = 10000;
    // Mobile nav drawer is z-index:10020 (see mobile-fixes.css) — card/arrow must sit above it
    // so the walkthrough is still visible when it opens the drawer to highlight a nav link.
    var CARD_Z = 10030;
    var navMenuOpenedByOnboarding = false;

    // ── Step sets per context ─────────────────────────────────────────────────

    var steps;

    if (context === "academics-index") {
      // The 4 subject-track cards on /academics/
      steps = [
        {
          target: null,
          position: "center",
          tag: "Academics Hub",
          title: "Browse by Subject Track",
          body: "This is the <strong>Academics hub</strong> — the starting point for all course content on SHOUG.TECH. Four subject tracks are organised below, each covering a set of PSU courses. Click any card to open that track and pick a course.",
        },
        {
          target: function(){ return document.querySelector(".hub-grid") || document.querySelector(".track-card"); },
          position: "bottom",
          tag: "Step 1 of 5 · Track Cards",
          title: "Four Subject Tracks",
          body: "Each card represents a <strong>subject track</strong>. The number badge in the top-right corner shows how many courses are inside. The tags below the title give you a quick preview of what topics you'll find.",
        },
        {
          target: function(){ return document.querySelector('a.track-card[href="/academics/computer-science/"]'); },
          position: "bottom",
          tag: "Step 2 of 5 · Computer Science",
          title: "Computer Science Track",
          body: "<strong>CS</strong> covers data structures, operating systems, databases, discrete math, computer networks, and more. The largest track on the site — most CS and SE students spend the majority of their study time here.",
        },
        {
          target: function(){ return document.querySelector('a.track-card[href="/academics/software-engineering/"]'); },
          position: "bottom",
          tag: "Step 3 of 5 · Software Engineering",
          title: "Software Engineering Track",
          body: "<strong>SE</strong> covers requirements engineering, software architecture, system design, software testing, and professional practice. All notes and slide breakdowns are included for each SE course.",
        },
        {
          target: function(){ return document.querySelector('a.track-card[href="/academics/cybersecurity/"]') || document.querySelector('a.track-card.cyber'); },
          position: "top",
          tag: "Step 4 of 5 · Cybersecurity",
          title: "Cybersecurity Track",
          body: "<strong>CYS</strong> focuses on penetration testing, security labs, and CTF-style content. More practical and tool-focused than the CS/SE tracks — great for hands-on security work.",
        },
        {
          target: function(){ return document.querySelector('a.track-card[href="/academics/other-courses/"]'); },
          position: "top",
          tag: "Step 5 of 5 · Other Courses",
          title: "Other Courses",
          body: "<strong>Other Courses</strong> covers ethics, physics, English writing, and general PSU requirements that don't belong to a specific major track. Required across most programs. <em>Click any card to dive in.</em>",
        },
      ];

    } else if (context === "academics-subject") {
      // Subject listing page like /academics/computer-science/
      steps = [
        {
          target: null,
          position: "center",
          tag: "Subject Track",
          title: "Pick a Course",
          body: "You're on a subject track page. Each card below is a <strong>course</strong> within this track. Click any course to open its full page — overview, slide breakdowns, study material, and quizzes all included.",
        },
      ];

    } else if (context === "academics-course") {
      // Any course or content page under /academics/{subject}/{course}/...
      steps = [
        {
          target: null,
          position: "center",
          tag: "Course Page",
          title: "What's on This Page",
          body: "You've opened a <strong>course page</strong>. Every course on SHOUG.TECH has multiple sections — slide breakdowns by chapter, raw lecture slides, extra study material, and quizzes. Use the sidebar and the tab bar to navigate between them.",
        },
        {
          target: function(){ return document.querySelector(".academic-sidebar"); },
          position: "right",
          tag: "Step 1 of 6 · Sidebar",
          title: "Course Directory Sidebar",
          body: "This sidebar is your full site-wide directory. Subjects are shown as collapsible trees — the <strong>[+]</strong> and <strong>[-]</strong> labels expand and collapse each subject. The <strong>highlighted entry</strong> (with the dot) is the page you're currently on. Click any course or section to jump there directly.",
        },
        {
          target: function(){
            return document.querySelector(".academic-sidebar .tree-toggle-button")
              || document.querySelector(".tree-toggle-button");
          },
          position: "right",
          tag: "Step 2 of 6 · Expand / Collapse",
          title: "Collapsible Subject Groups",
          body: "Click a subject label like <strong>[+] COMPUTER SCIENCE/</strong> to expand it and reveal every course inside. Click <strong>[-]</strong> to collapse it. The active course's subject is always auto-expanded when the page loads.",
        },
        {
          target: function(){
            return document.querySelector("nav.sub-nav") || document.querySelector(".sub-nav");
          },
          position: "bottom",
          tag: "Step 3 of 6 · Section Tabs",
          title: "Course Sections",
          body: "The tab bar above the content switches between sections of this course:<br><br><strong>Overview</strong> — course summary, syllabus, and grade breakdown.<br><strong>Slide Breakdowns</strong> — chapter-by-chapter detailed notes.<br><strong>Slides</strong> — the raw lecture slide decks.<br><strong>Study Material</strong> — extra resources and references.<br><strong>Exams</strong> — practice questions with answers.",
        },
        {
          target: function(){
            return document.querySelector(".meta-panel-container") || document.querySelector(".meta-panel");
          },
          position: "left",
          tag: "Step 4 of 6 · Metadata Panel",
          title: "Course Info Panel",
          body: "The panel on the right shows all course metadata at a glance: <strong>status</strong> (complete or in-progress), <strong>credit hours</strong>, <strong>prerequisites</strong>, and quick-jump links to each section. The barcode at the top is a unique file ID for this course.",
        },
        {
          target: function(){
            return document.querySelector(".tag-complete")
              || document.getElementById("shoug-complete-btn")
              || document.querySelector(".shoug-complete-btn");
          },
          position: "bottom",
          tag: "Step 5 of 6 · Completion",
          title: "Track What You've Studied",
          body: "The <strong>COMPLETE</strong> tag marks a course as fully studied. On each individual section page (slide breakdowns, quizzes, etc.), a <strong>Mark as Complete</strong> button appears in the bottom-right — clicking it records that page in your progress dashboard.",
        },
        {
          target: null,
          position: "center",
          tag: "Step 6 of 6 · Page Tools",
          title: "Three Tools on Every Study Page",
          body: "On any page inside a course, three buttons appear fixed in the bottom-right corner:<br><br><strong>✓ Complete</strong> — marks that specific page as studied.<br><strong>🔖 Bookmark</strong> — saves the page to your personal Bookmarks database.<br><strong>📝 Notes</strong> — a private notepad that auto-saves as you type, tied to this exact page.",
        },
      ];

    } else if (context === "resources") {
      steps = [
        {
          target: null,
          position: "center",
          tag: "Resources",
          title: "A Curated Shelf of Tools & Links",
          body: "The Resources page is a hand-picked collection of tools, documentation sites, platforms, and references that are genuinely useful for PSU students. Everything here is something used regularly — not just a link dump.",
        },
        {
          target: function(){ return document.querySelector(".jump-nav") || document.querySelector(".jump-nav-inner"); },
          position: "bottom",
          tag: "Step 1 of 4 · Section Nav",
          title: "Jump to Any Category",
          body: "The <strong>sticky nav bar</strong> lets you jump directly to any category. Sections include Learning, Dev Tools, Containers, Visualization, Cybersecurity, and more. Items highlighted in <span style='color:#ff2a4b;'>red</span> flag sections with security-focused tools.",
        },
        {
          target: function(){ return document.querySelector(".section-title-wrap") || document.querySelector(".section-num"); },
          position: "bottom",
          tag: "Step 2 of 4 · Sections",
          title: "Organised by Category",
          body: "Each numbered section groups related tools and links. The category label tells you what domain the tools cover — scroll through or use the jump nav to navigate quickly.",
        },
        {
          target: function(){ return document.querySelector("a.card") || document.querySelector(".card"); },
          position: "bottom",
          tag: "Step 3 of 4 · Resource Cards",
          title: "Resource Cards",
          body: "Each card links to a specific tool or reference. The small ID in the top-left is a unique entry code. Tags below the title show the topics or languages it covers. Click any card to open it directly.",
        },
        {
          target: function(){ return document.querySelector(".nav-alert"); },
          position: "bottom",
          tag: "Step 4 of 4 · Security Sections",
          title: "Security-Flagged Content",
          body: "Sections marked in <span style='color:#ff2a4b;'>red</span> contain cybersecurity and offensive security tools for the CYS track — penetration testing labs, CTF tools, and frameworks. Use only in authorised environments.",
        },
      ];

    } else if (context === "workshops") {
      steps = [
        {
          target: null,
          position: "center",
          tag: "Workshops",
          title: "Hands-On Sessions",
          body: "Workshops are structured, practical sessions — more guided than a project, more applied than a lecture. Each one is fully documented with all the materials, tools, and steps you need to follow along.",
        },
        {
          target: function(){ return document.querySelector(".hero") || document.querySelector(".hero-title"); },
          position: "bottom",
          tag: "Step 1 of 3 · Overview",
          title: "What's Here",
          body: "The hero section gives you a quick summary of the workshops available — how many there are, what domains they cover, and who they were delivered for.",
        },
        {
          target: function(){ return document.querySelector(".workshops-hub") || document.querySelector(".dossier-card"); },
          position: "bottom",
          tag: "Step 2 of 3 · Workshop Cards",
          title: "Workshop Dossiers",
          body: "Each card is a <strong>workshop dossier</strong>. Click any card to open the full documentation for that workshop — context, tools, session structure, and all lab files or exercises included.",
        },
        {
          target: function(){
            return document.querySelector('.dossier-card[data-accent="red"]') || document.querySelector(".dossier-card");
          },
          position: "bottom",
          tag: "Step 3 of 3 · Cybersecurity Workshop",
          title: "Cybersecurity Crash Course",
          body: "The <strong>Cybersecurity Crash Course</strong> is a practical offensive-security workshop covering CTF labs, common attack techniques, and hands-on tools. Delivered at PSU — all materials are inside the card.",
        },
      ];

    } else if (context === "about") {
      steps = [
        {
          target: null,
          position: "center",
          tag: "About",
          title: "The Person Behind SHOUG.TECH",
          body: "This page is the profile of the site's author. It covers academic background, roles, skills, and contact details — styled as a terminal-style CV.",
        },
        {
          target: function(){ return document.querySelector(".identity-col") || document.querySelector(".display-name"); },
          position: "right",
          tag: "Step 1 of 3 · Identity",
          title: "Who Built This",
          body: "This column shows the <strong>name, roles, and personal statement</strong> of the site's author — a PSU Software Engineering student, course instructor, and peer tutor at PSU WTC.",
        },
        {
          target: function(){ return document.querySelector(".terminal-col") || document.querySelector(".terminal-block"); },
          position: "left",
          tag: "Step 2 of 3 · Terminal Block",
          title: "Skills & Stats",
          body: "The terminal block on the right is a styled readout of technical skills, tools, and stats written to look like a system log. Scroll down for more — projects, experience, and contact details are all further down the page.",
        },
        {
          target: function(){ return document.querySelector(".shoug-contact-btn") || document.querySelector('a[href^="mailto"]'); },
          position: "bottom",
          tag: "Step 3 of 3 · Contact",
          title: "Get in Touch",
          body: "The <strong>Contact</strong> button in the header opens a direct email. If you spot an error in the course notes, want to suggest a resource, or just want to reach out — that's the fastest way.",
        },
      ];

    } else if (context === "work") {
      steps = [
        {
          target: null,
          position: "center",
          tag: "Work",
          title: "Projects & Portfolio",
          body: "This is the <strong>Work</strong> section — a portfolio of real projects, case studies, and applied work. Browse to see how concepts from courses translate into actual software and research.",
        },
        {
          target: function(){ return document.querySelector(".hero") || document.querySelector(".hero-title"); },
          position: "bottom",
          tag: "Step 1 of 3 · Hero",
          title: "Work Overview",
          body: "The hero section summarises what kind of work is featured here — software engineering, cybersecurity research, and studio projects. Scroll down to browse the full collection.",
        },
        {
          target: function(){ return document.querySelector(".panels-grid") || document.querySelector(".panel"); },
          position: "bottom",
          tag: "Step 2 of 3 · Panels",
          title: "Work Categories",
          body: "The panels break the work into categories — by role, context, or type of output. Each panel describes a domain of work and links to the relevant projects inside it.",
        },
        {
          target: function(){ return document.querySelector(".work-grid") || document.querySelector(".work-card"); },
          position: "top",
          tag: "Step 3 of 3 · Project Cards",
          title: "Project Cards",
          body: "Each card is a <strong>specific project</strong>. Click any card to open the full case study — what the project was, what technologies were used, and what was built or shipped.",
        },
      ];

    } else if (context === "workshop-detail") {
      // Inside a specific workshop like /workshops/cybersecurity-crash-course/
      steps = [
        {
          target: null,
          position: "center",
          tag: "Workshop Dossier",
          title: "Inside the Workshop",
          body: "You're inside a <strong>workshop dossier</strong> — the full documentation for a single workshop. Everything delivered in the session is archived here: context, objectives, schedule, labs, handouts, and reflections.",
        },
        {
          target: function(){ return document.querySelector(".hero") || document.querySelector(".hero-content"); },
          position: "bottom",
          tag: "Step 1 of 2 · Overview",
          title: "Workshop Brief",
          body: "The hero section gives you the workshop's mission at a glance — what it covered, who it was delivered to, and where. Scroll down for the full breakdown.",
        },
        {
          target: function(){ return document.querySelector(".cards-grid") || document.querySelector(".workshop-card"); },
          position: "bottom",
          tag: "Step 2 of 2 · Sections",
          title: "Navigate the Dossier",
          body: "Each card links to a specific section of this workshop: <strong>Schedule</strong>, <strong>Topics & Learning Outcomes</strong>, <strong>Handouts</strong>, <strong>Labs</strong>, and <strong>Reflection</strong>. Click any card to open that section.",
        },
      ];

    } else if (context === "work-detail") {
      // Inside /work/projects/ or other work sub-pages
      steps = [
        {
          target: null,
          position: "center",
          tag: "Project Archive",
          title: "Full Case Studies",
          body: "This is the <strong>project archive</strong> — detailed records of every project built as part of coursework or independent work. Each record covers the scope, tech stack, role, and outputs.",
        },
        {
          target: function(){ return document.querySelector(".filters") || document.querySelector(".filter-btn"); },
          position: "bottom",
          tag: "Step 1 of 2 · Filters",
          title: "Filter by Category",
          body: "Use the filter buttons to narrow projects by domain — <strong>Software Engineering</strong>, <strong>Computer Science</strong>, <strong>Mathematics</strong>, or view all at once. Active filter is highlighted.",
        },
        {
          target: function(){ return document.querySelector(".project-record") || document.querySelector(".project-list"); },
          position: "top",
          tag: "Step 2 of 2 · Project Records",
          title: "Project Records",
          body: "Each record shows the project title, category, summary, tech stack, role, and direct links to the <strong>documentation site</strong> and <strong>GitHub repository</strong>. Click any link to open it.",
        },
      ];

    } else if (context === "community") {
      steps = [
        {
          target: null,
          position: "center",
          tag: "Community",
          title: "Student Community Hub",
          body: "The Community section connects PSU students — follow classmates, track study progress together, discuss course material, and see who's at the top of the leaderboard. You need a community profile to participate.",
        },
        {
          target: function(){ return document.querySelector(".comm-tabs") || document.querySelector(".comm-tab"); },
          position: "bottom",
          tag: "Step 1 of 3 · Tabs",
          title: "Four Sections",
          body: "The tab bar switches between four views:<br><br><strong>Browse</strong> — find and follow other students.<br><strong>Activity</strong> — a feed of your followed students' recent completions.<br><strong>Leaderboards</strong> — ranked list by pages completed, with a visual podium for the top 3.<br><strong>Discussions</strong> — threaded course discussions.",
        },
        {
          target: function(){ return document.querySelector('button.comm-tab[data-tab="discuss"]') || document.querySelector('button.comm-tab'); },
          position: "bottom",
          tag: "Step 2 of 3 · Discussions",
          title: "Course Discussions",
          body: "Pick a course from the dropdown and join the conversation — ask questions, share notes, reply to classmates. Replies send a notification to the original poster so no message goes unanswered.",
        },
        {
          target: function(){ return document.querySelector('button.comm-tab[data-tab="leaderboard"]'); },
          position: "bottom",
          tag: "Step 3 of 3 · Leaderboards",
          title: "Leaderboard & Podium",
          body: "The <strong>Leaderboard</strong> tab ranks all users by total pages completed. The top 3 get a visual podium — 2nd, 1st (tallest), 3rd. Below that, every student gets a progress bar showing their percentage of the leader's score.",
        },
      ];

    } else if (context === "community-profile") {
      steps = [
        {
          target: null,
          position: "center",
          tag: "Student Profile",
          title: "Public Profile Card",
          body: "Every community member has a public profile — showing their study stats, course progress, subject breakdown, and upcoming exam countdowns. You're looking at someone's profile right now.",
        },
        {
          target: function(){ return document.querySelector(".profile-stats"); },
          position: "bottom",
          tag: "Step 1 of 3 · Stats",
          title: "Study Stats",
          body: "These four numbers show <strong>pages completed</strong>, active courses, followers, and who they're following. If the profile is private, page and course counts are hidden — only follow counts show.",
        },
        {
          target: function(){ return document.getElementById("exam-section"); },
          position: "top",
          tag: "Step 2 of 3 · Exams",
          title: "Exam Countdowns",
          body: "Students can add upcoming exams here — midterms, finals, quizzes. The countdown turns <span style='color:#ff2a4b'>red</span> as the date gets close. If you're the profile owner, click <strong>+ Add Exam</strong> and enable notifications to get reminders 7, 3, and 1 day before.",
        },
        {
          target: function(){ return document.getElementById("follow-btn") || document.getElementById("edit-btn"); },
          position: "bottom",
          tag: "Step 3 of 3 · Follow",
          title: "Follow or Edit",
          body: "If this is someone else's profile, click <strong>Follow</strong> to add them to your activity feed — their completed pages show up in the <strong>Activity</strong> tab on the Community page. If it's your own profile, the button becomes <strong>Edit Profile</strong> to update your name, bio, major, and account settings.",
        },
      ];

    } else if (context === "account") {
      steps = [
        {
          target: null,
          position: "center",
          tag: "My Progress",
          title: "Your Personal Dashboard",
          body: "This dashboard shows your full study history on SHOUG.TECH. Every time you click <strong>Mark as Complete</strong> on a page, it's recorded here — broken down by course, track, and time. Sign in to see your data.",
        },
        {
          target: function(){ return document.getElementById("stats-row") || document.querySelector(".stats-row"); },
          position: "bottom",
          tag: "Step 1 of 3 · Stats Strip",
          title: "Key Numbers at a Glance",
          body: "The stats strip shows your high-level numbers: total pages completed, active study streak, courses with full completion, and total study days. These update automatically as you mark pages complete.",
        },
        {
          target: function(){ return document.getElementById("overview-row") || document.querySelector(".overview-row"); },
          position: "bottom",
          tag: "Step 2 of 3 · Progress Overview",
          title: "Progress Ring & Charts",
          body: "The overview section shows your overall completion percentage as a <strong>ring chart</strong>, plus a track balance radar and an activity heatmap. Hover any cell in the heatmap to see how many pages you completed on that day.",
        },
        {
          target: function(){ return document.getElementById("track-grid") || document.querySelector(".track-grid"); },
          position: "top",
          tag: "Step 3 of 3 · Track Breakdown",
          title: "Progress by Track",
          body: "The bottom section breaks your progress down <strong>by academic track</strong> (CS, SE, CYS, Other). Each card shows how many pages you've completed in that track and which specific courses you've touched.",
        },
      ];

    } else if (context === "bookmarks") {
      steps = [
        {
          target: null,
          position: "center",
          tag: "Bookmarks",
          title: "Your Personal Database",
          body: "The Bookmarks page is a <strong>terminal-style database view</strong> of every page you've saved while studying. Organised into folders, filterable, with an inspector panel and a real command-line interface at the bottom.",
        },
        {
          target: function(){ return document.querySelector(".folder-col") || document.querySelector(".folder-list"); },
          position: "right",
          tag: "Step 1 of 3 · Directories",
          title: "Folder Sidebar",
          body: "The left panel is your <strong>directory tree</strong>. Click any folder to filter the table to that folder's bookmarks. Use <strong>+ INITIALIZE_NEW_DIR</strong> to create a new folder. You can also move bookmarks between folders.",
        },
        {
          target: function(){ return document.querySelector(".table-col") || document.querySelector(".table-body"); },
          position: "left",
          tag: "Step 2 of 3 · Records Table",
          title: "Bookmark Records",
          body: "The center panel lists all your bookmarks as database records — each row shows the page title, URL, and save date. Click any row to open the <strong>Inspector</strong> on the right with full details and a direct link.",
        },
        {
          target: function(){ return document.querySelector(".term-input-row") || document.querySelector(".term-input"); },
          position: "top",
          tag: "Step 3 of 3 · Terminal",
          title: "Command Interface",
          body: "The terminal at the bottom accepts commands to query and manage your bookmarks. Type <strong>help</strong> and press Enter to see all available commands — including search, move, delete, and export.",
        },
      ];

    } else if (context === "academic-plan-themes") {
      steps = [
        {
          target: null,
          position: "center",
          tag: "Academic Plan",
          title: "Visualised Degree Plans",
          body: "These pages display your full PSU degree plan in different visual styles — roadmap, stacked blocks, classic table, and more. Each theme shows the same curriculum data in a different format so you can find the layout that clicks for you.",
        },
        {
          target: function(){ return document.querySelector(".hero") || document.querySelector("h1"); },
          position: "bottom",
          tag: "Step 1 of 2 · Your Plan",
          title: "Degree Plan Overview",
          body: "The plan shows all courses organised by semester, grouped by track. Completed courses are typically highlighted differently from upcoming ones. Scroll to see the full timeline from Year 1 through graduation.",
        },
        {
          target: function(){ return document.querySelector("nav") || document.querySelector(".shoug-header-nav"); },
          position: "bottom",
          tag: "Step 2 of 2 · Switch Themes",
          title: "Try Other Layouts",
          body: "There are multiple plan themes available — <strong>Stacks</strong>, <strong>Roadmap</strong>, <strong>Classic</strong>, and more, including Arabic versions. Use the <strong>Academic Plan</strong> section in the site to find and switch between them.",
        },
      ];

    } else {
      // Home page / general — full site tour
      steps = [
        {
          target: null,
          position: "center",
          tag: "Welcome",
          title: "Welcome to SHOUG.TECH",
          body: "A personal digital garden built by a PSU Software Engineering student — a living study space for CS, SE, CYS, AI&DS, and DX courses. Here's a quick tour so you know where everything lives.",
        },
        {
          target: function(){ return document.querySelector('.shoug-header-nav a[href="/academics/"]'); },
          position: "bottom",
          tag: "Step 1 of 7 · Academics",
          title: "Course Content",
          body: "<strong>Academics</strong> is the main section. Find slide breakdowns, chapter summaries, and quizzes for every PSU course — organised by subject track and then by course. Start here when studying.",
        },
        {
          target: function(){ return document.querySelector('.shoug-header-nav a[href="/work/"]'); },
          position: "bottom",
          tag: "Step 2 of 7 · Work",
          title: "Projects & Portfolio",
          body: "<strong>Work</strong> is a portfolio of real projects and case studies — useful for seeing how course concepts translate into actual software.",
        },
        {
          target: function(){ return document.querySelector('.shoug-header-nav a[href="/workshops/"]'); },
          position: "bottom",
          tag: "Step 3 of 7 · Workshops",
          title: "Workshops",
          body: "<strong>Workshops</strong> are guided, hands-on sessions. Deeper than a lecture, more structured than a project — think step-by-step walkthroughs where you build or solve something.",
        },
        {
          target: function(){ return document.querySelector('.shoug-header-nav a[href="/resources/"]'); },
          position: "bottom",
          tag: "Step 4 of 7 · Resources",
          title: "Study Resources",
          body: "<strong>Resources</strong> is a curated list of tools, references, and links — from cheat sheets and study guides to software and documentation useful for PSU students.",
        },
        {
          target: function(){ return document.querySelector('.shoug-header-nav a[href="/about/"]'); },
          position: "bottom",
          tag: "Step 5 of 7 · About",
          title: "About This Site",
          body: "<strong>About</strong> explains who built SHOUG.TECH and why. If you spot an error in the notes or want to suggest a resource, that's the place to go.",
        },
        {
          target: function(){ return document.getElementById("shoug-fb-user") || document.querySelector(".shoug-auth-btn") || document.querySelector(".shoug-header-actions"); },
          position: "bottom",
          tag: "Step 6 of 7 · Account",
          title: "Sign In to Track Progress",
          body: "Create a free account here. Once signed in, every page you study is automatically tracked. Your completion stats, bookmarks, and notes are all saved to your account and accessible from any device.",
        },
        {
          target: null,
          position: "center",
          tag: "Step 7 of 7 · Dashboard",
          title: "Your Dashboard",
          body: "Once signed in, clicking your avatar opens a personal dashboard. From there you can reach <strong>My Profile</strong>, <strong>Bookmarks</strong>, <strong>My Progress</strong>, and the <strong>Community</strong> hub — each section has its own walkthrough when you visit it for the first time.",
        },
      ];
    }

    var current = 0;

    // Dim backdrop — z-index swaps per step (below header for targeted, above for center)
    var dimEl = document.createElement("div");
    dimEl.style.cssText = "position:fixed;inset:0;background:rgba(5,2,10,.84);pointer-events:all;";

    // Arrow (CSS triangle) — always above header
    var arrowEl = document.createElement("div");
    arrowEl.style.cssText = "position:fixed;width:0;height:0;z-index:"+(CARD_Z)+";pointer-events:none;display:none;";

    // Tooltip card — always above header
    var card = document.createElement("div");
    card.id = "shoug-ob-card";
    card.style.cssText = "position:fixed;z-index:"+(CARD_Z)+";width:min(400px,calc(100vw - 40px));max-width:calc(100vw - 16px);box-sizing:border-box;margin:0;background:#0a0514;border:1px solid rgba(184,41,234,.45);font-family:'JetBrains Mono',monospace;pointer-events:all;";

    document.body.appendChild(dimEl);
    document.body.appendChild(arrowEl);
    document.body.appendChild(card);

    function clearHighlight() {
      document.querySelectorAll(".ob-hl").forEach(function(el){
        el.classList.remove("ob-hl");
        el.style.removeProperty("box-shadow");
        el.style.removeProperty("outline");
        el.style.removeProperty("border-radius");
      });
    }

    function highlight(el) {
      clearHighlight();
      if (!el) return;
      el.classList.add("ob-hl");
      el.style.boxShadow = "0 0 0 2px #b829ea, 0 0 0 5px rgba(184,41,234,.22), 0 0 28px rgba(184,41,234,.4)";
      el.style.outline = "none";
      el.style.borderRadius = "3px";
    }

    function positionCard(rect, position) {
      var cw = card.offsetWidth || 400;
      var ch = card.offsetHeight || 180;
      var vw = window.innerWidth;
      var vh = window.innerHeight;
      var GAP = 14;
      var top, left;

      arrowEl.style.display = "none";

      if (!rect || position === "center") {
        top  = (vh - ch) / 2;
        left = (vw - cw) / 2;
      } else {
        var midX = rect.left + rect.width / 2;
        var midY = rect.top + rect.height / 2;
        if (position === "bottom") {
          top  = rect.bottom + GAP;
          left = Math.min(Math.max(midX - cw / 2, 12), vw - cw - 12);
          arrowEl.style.cssText = [
            "position:fixed",
            "left:" + (midX - 7) + "px",
            "top:" + rect.bottom + "px",
            "border-left:7px solid transparent",
            "border-right:7px solid transparent",
            "border-bottom:12px solid #b829ea",
            "z-index:" + (CARD_Z),
            "pointer-events:none",
            "display:block"
          ].join(";");
        } else if (position === "right") {
          top  = Math.min(Math.max(midY - ch / 2, 12), vh - ch - 12);
          left = rect.right + GAP;
          var flippedLeft = left + cw > vw - 12;
          if (flippedLeft) left = rect.left - cw - GAP;
          var arrowTop = Math.min(Math.max(midY - 7, top + 16), top + ch - 30);
          arrowEl.style.cssText = [
            "position:fixed",
            "top:" + arrowTop + "px",
            "left:" + (flippedLeft ? (left + cw) : (left - 12)) + "px",
            "border-top:7px solid transparent",
            "border-bottom:7px solid transparent",
            flippedLeft ? "border-right:12px solid #b829ea" : "border-left:12px solid #b829ea",
            "z-index:" + (CARD_Z),
            "pointer-events:none",
            "display:block"
          ].join(";");
        } else if (position === "left") {
          top  = Math.min(Math.max(midY - ch / 2, 12), vh - ch - 12);
          left = rect.left - cw - GAP;
          var flippedRight = left < 12;
          if (flippedRight) left = rect.right + GAP;
          var arrowTop2 = Math.min(Math.max(midY - 7, top + 16), top + ch - 30);
          arrowEl.style.cssText = [
            "position:fixed",
            "top:" + arrowTop2 + "px",
            "left:" + (flippedRight ? (left - 12) : (left + cw)) + "px",
            "border-top:7px solid transparent",
            "border-bottom:7px solid transparent",
            flippedRight ? "border-left:12px solid #b829ea" : "border-right:12px solid #b829ea",
            "z-index:" + (CARD_Z),
            "pointer-events:none",
            "display:block"
          ].join(";");
        } else {
          top  = rect.top - GAP - ch;
          left = Math.min(Math.max(midX - cw / 2, 12), vw - cw - 12);
          arrowEl.style.cssText = [
            "position:fixed",
            "left:" + (midX - 7) + "px",
            "top:" + (rect.top - GAP) + "px",
            "border-left:7px solid transparent",
            "border-right:7px solid transparent",
            "border-top:12px solid #b829ea",
            "z-index:" + (CARD_Z),
            "pointer-events:none",
            "display:block"
          ].join(";");
        }
        if (position !== "right" && position !== "left") {
          if (top + ch > vh - 12) top = rect.top - GAP - ch;
          if (top < 8) top = rect.bottom + GAP;
          // Hard clamp — always keep card inside the viewport
          top = Math.max(8, Math.min(top, vh - ch - 12));
        }
        // Hard clamp for right/left too
        top = Math.max(8, Math.min(top, vh - ch - 12));
        left = Math.max(8, Math.min(left, vw - cw - 8));
      }

      card.style.top  = top + "px";
      card.style.left = left + "px";

      // Final safety pass — re-measure after layout (fonts/images can change
      // the card's real size) and re-clamp so it can never spill off-screen.
      requestAnimationFrame(function(){
        var vw2 = window.innerWidth;
        var vh2 = window.innerHeight;
        var r = card.getBoundingClientRect();
        var newLeft = Math.min(Math.max(r.left, 8), vw2 - r.width - 8);
        var newTop  = Math.min(Math.max(r.top, 8), vh2 - r.height - 8);
        if (Math.abs(newLeft - r.left) > .5) card.style.left = newLeft + "px";
        if (Math.abs(newTop - r.top) > .5) card.style.top = newTop + "px";
      });
    }

    function render() {
      var s = steps[current];
      var targetEl = s.target ? s.target() : null;

      // If this step targets a link inside the mobile nav drawer, open the drawer on
      // small screens so the link is actually visible — otherwise close it again.
      var inMobileNav = targetEl && targetEl.closest && targetEl.closest(".shoug-header-nav");
      if (inMobileNav && window.innerWidth <= 760) {
        document.body.classList.add("mobile-nav-open");
        navMenuOpenedByOnboarding = true;
      } else if (navMenuOpenedByOnboarding) {
        document.body.classList.remove("mobile-nav-open");
        navMenuOpenedByOnboarding = false;
      }

      var rect = targetEl ? targetEl.getBoundingClientRect() : null;
      // Treat as no target if: zero-sized, fully outside viewport (e.g. mobile nav drawer), or display:none
      if (rect && (
        (rect.width === 0 && rect.height === 0) ||
        rect.right <= 0 || rect.bottom <= 0 ||
        rect.left >= window.innerWidth || rect.top >= window.innerHeight
      )) { rect = null; targetEl = null; }

      // Below header (9999) → header stays visible so target element is lit up naturally.
      // Above header (10001) → center steps cover everything including header.
      dimEl.style.zIndex = rect ? (HDR_Z - 1) + "" : (HDR_Z + 1) + "";

      highlight(targetEl);

      var dots = steps.map(function(_, i){
        return '<div style="flex-shrink:0;width:'+(i===current?'20px':'6px')+';height:6px;border-radius:3px;background:'+(i===current?'#b829ea':'rgba(255,255,255,.15)')+';transition:width 200ms;"></div>';
      }).join("");

      card.innerHTML = [
        '<div style="position:absolute;top:0;left:0;right:0;height:2px;background:linear-gradient(90deg,#b829ea,rgba(184,41,234,.08));"></div>',
        '<div style="padding:28px 28px 18px;">',
        '  <div style="font-size:.5rem;color:#b829ea;letter-spacing:.22em;text-transform:uppercase;margin-bottom:8px;">'+s.tag+'</div>',
        '  <div style="font-size:.94rem;font-weight:800;color:#f8f7fb;margin-bottom:10px;line-height:1.3;">'+s.title+'</div>',
        '  <div style="font-size:.76rem;color:#8f8b9a;line-height:1.75;font-family:\'Inter\',sans-serif;">'+s.body+'</div>',
        '</div>',
        '<div style="padding:12px 28px 20px;display:flex;align-items:center;justify-content:space-between;border-top:1px solid rgba(255,255,255,.05);">',
        '  <div style="display:flex;gap:6px;align-items:center;">'+dots+'</div>',
        '  <div style="display:flex;gap:8px;align-items:center;">',
        (current === 0
          ? '<button id="ob-skip" style="height:32px;padding:0 14px;background:transparent;border:none;color:#4a4258;font-family:\'JetBrains Mono\',monospace;font-size:.6rem;cursor:pointer;">Skip</button>'
          : '<button id="ob-prev" style="height:32px;padding:0 14px;background:transparent;border:1px solid rgba(255,255,255,.1);color:#8f8b9a;font-family:\'JetBrains Mono\',monospace;font-size:.6rem;font-weight:700;letter-spacing:.1em;text-transform:uppercase;cursor:pointer;">Back</button>'),
        '  <button id="ob-next" style="height:32px;padding:0 18px;background:#b829ea;border:none;color:#0a0514;font-family:\'JetBrains Mono\',monospace;font-size:.62rem;font-weight:800;letter-spacing:.14em;text-transform:uppercase;cursor:pointer;">'+(current===steps.length-1?(context==='home'?'Get Started ✓':'Done ✓'):'Next →')+'</button>',
        '  </div>',
        '</div>',
      ].join("");

      requestAnimationFrame(function(){ positionCard(rect, s.position); });

      document.getElementById("ob-next").addEventListener("click", function(){
        if (current < steps.length - 1) { current++; render(); } else { finish(); }
      });
      var prev = document.getElementById("ob-prev");
      var skip = document.getElementById("ob-skip");
      if (prev) prev.addEventListener("click", function(){ current--; render(); });
      if (skip) skip.addEventListener("click", finish);
    }

    function finish() {
      localStorage.setItem(storageKey, "1");
      clearHighlight();
      if (navMenuOpenedByOnboarding) {
        document.body.classList.remove("mobile-nav-open");
        navMenuOpenedByOnboarding = false;
      }
      [dimEl, arrowEl, card].forEach(function(el){
        el.style.opacity = "0";
        el.style.transition = "opacity 300ms";
        setTimeout(function(){ el.remove(); }, 320);
      });
    }

    dimEl.style.opacity = "0";
    card.style.opacity  = "0";
    dimEl.style.transition = card.style.transition = "opacity 300ms";
    render();
    requestAnimationFrame(function(){ requestAnimationFrame(function(){
      dimEl.style.opacity = "1";
      card.style.opacity  = "1";
    }); });

    // Escape hatches — the walkthrough must never be able to fully block the
    // site. Clicking the dim backdrop or pressing Escape always closes it.
    dimEl.addEventListener("click", finish);
    var escHandler = function(e){
      if (e.key === "Escape") { finish(); document.removeEventListener("keydown", escHandler); }
    };
    document.addEventListener("keydown", escHandler);

    // Watchdog — if the card never ends up visible on-screen (positioning
    // bug, slow layout, etc.), auto-dismiss instead of leaving a stuck overlay.
    setTimeout(function(){
      if (!document.body.contains(card)) return;
      var r = card.getBoundingClientRect();
      var onScreen = r.width > 0 && r.height > 0 &&
        r.right > 0 && r.bottom > 0 &&
        r.left < window.innerWidth && r.top < window.innerHeight;
      console.log("[onboarding debug]", JSON.stringify(r), "vw="+window.innerWidth, "vh="+window.innerHeight, "onScreen="+onScreen, "opacity="+card.style.opacity);
      if (!onScreen) finish();
    }, 1500);

    // Re-position on viewport changes (orientation flip, mobile browser
    // address-bar collapse/expand, on-screen keyboard) so the card never
    // ends up stuck off-screen from a stale top/left.
    window.addEventListener("resize", function(){
      var s = steps[current];
      var targetEl = s.target ? s.target() : null;
      var rect = targetEl ? targetEl.getBoundingClientRect() : null;
      if (rect && (
        (rect.width === 0 && rect.height === 0) ||
        rect.right <= 0 || rect.bottom <= 0 ||
        rect.left >= window.innerWidth || rect.top >= window.innerHeight
      )) { rect = null; }
      positionCard(rect, s.position);
    });
  }

  // ── Page Icons (Bookmark + Notes) ────────────────────────────────────────

  var _notesDebounce = null;

  function injectPageIcons(user) {
    if (!isContentPage()) return;
    if (document.getElementById("shoug-page-icons")) return;
    var slug = pageSlug();
    var db = firebase.firestore();

    // Icon bar
    var bar = document.createElement("div");
    bar.id = "shoug-page-icons";
    bar.innerHTML = [
      '<div class="shoug-icon-btn" id="shoug-notes-icon" title="My Notes">',
      '<svg width="13" height="13" viewBox="0 0 13 13" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">',
      '<rect x="1" y="1" width="11" height="11" rx="1"/><line x1="3.5" y1="4.5" x2="9.5" y2="4.5"/><line x1="3.5" y1="7" x2="9.5" y2="7"/><line x1="3.5" y1="9.5" x2="6.5" y2="9.5"/>',
      '</svg></div>',
      '<div class="shoug-icon-btn" id="shoug-bookmark-icon" title="Bookmark">',
      '<svg width="11" height="13" viewBox="0 0 11 13" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">',
      '<path d="M1 1h9v11L5.5 8.5 1 12z"/>',
      '</svg></div>',
    ].join("");
    document.body.appendChild(bar);

    // Notes panel
    var panel = document.createElement("div");
    panel.id = "shoug-notes-panel";
    panel.innerHTML = [
      '<div class="np-hdr"><span>// Notes</span><span class="np-status" id="np-status"></span></div>',
      '<textarea id="shoug-notes-ta" placeholder="Private notes for this page…" maxlength="2000"></textarea>',
    ].join("");
    document.body.appendChild(panel);

    // Load note + bookmark state from the existing pages doc (single read)
    db.collection("userProgress").doc(user.uid).collection("pages").doc(slug).get().then(function(doc) {
      if (!doc.exists) return;
      var d = doc.data();
      if (d.note) { var ta = document.getElementById("shoug-notes-ta"); if (ta) ta.value = d.note; }
      if (d.bookmarked) { var btn = document.getElementById("shoug-bookmark-icon"); if (btn) btn.classList.add("active"); }
    });

    // Notes toggle
    document.getElementById("shoug-notes-icon").addEventListener("click", function() {
      var p = document.getElementById("shoug-notes-panel");
      var ic = document.getElementById("shoug-notes-icon");
      var open = p.classList.toggle("open");
      ic.classList.toggle("active", open);
      if (open) { var ta = document.getElementById("shoug-notes-ta"); if (ta) ta.focus(); }
    });

    // Notes auto-save
    document.getElementById("shoug-notes-ta").addEventListener("input", function() {
      clearTimeout(_notesDebounce);
      var st = document.getElementById("np-status");
      if (st) st.textContent = "unsaved…";
      _notesDebounce = setTimeout(function() { saveNote(user, slug); }, 1500);
    });

    // Bookmark toggle — stored on the existing pages doc via merge
    document.getElementById("shoug-bookmark-icon").addEventListener("click", function() {
      var btn = document.getElementById("shoug-bookmark-icon");
      var active = btn.classList.toggle("active");
      var ref = db.collection("userProgress").doc(user.uid).collection("pages").doc(slug);
      if (active) {
        ref.set({ url: window.location.pathname, title: pageTitle(), bookmarked: true, bookmarkFolder: null, bookmarkSavedAt: firebase.firestore.FieldValue.serverTimestamp() }, { merge: true });
      } else {
        ref.set({ bookmarked: false }, { merge: true });
      }
    });
  }

  function saveNote(user, slug) {
    var ta = document.getElementById("shoug-notes-ta");
    var st = document.getElementById("np-status");
    if (!ta) return;
    var note = ta.value;
    // Merge note onto the existing pages doc so we don't overwrite progress data
    var ref = firebase.firestore().collection("userProgress").doc(user.uid).collection("pages").doc(slug);
    ref.set({ note: note, url: window.location.pathname, title: pageTitle(), noteUpdatedAt: firebase.firestore.FieldValue.serverTimestamp() }, { merge: true })
      .then(function() {
        if (st) { st.textContent = "saved"; setTimeout(function() { var s = document.getElementById("np-status"); if (s) s.textContent = ""; }, 2000); }
      }).catch(function() { if (st) st.textContent = "error"; });
  }

  // ── App section tab bar ───────────────────────────────────────────────────

  function isAppPage() {
    var p = window.location.pathname;
    return p.indexOf("/bookmarks") === 0 ||
           p.indexOf("/account") === 0 ||
           p.indexOf("/community") === 0;
  }

  function injectAppNav(user) {
    if (!isAppPage()) return;
    if (document.getElementById("shoug-app-nav")) return;
    var path = window.location.pathname;
    var tabs = [
      { label: "Home",        href: "/",
        active: false },
      { label: "My Profile",  href: "/community/profile/?u=" + encodeURIComponent(user.uid),
        active: path.indexOf("/community/profile") === 0 },
      { label: "Bookmarks",   href: "/bookmarks/",
        active: path.indexOf("/bookmarks") === 0 },
      { label: "My Progress", href: "/account/",
        active: path.indexOf("/account") === 0 },
      { label: "Community",   href: "/community/",
        active: path.indexOf("/community") === 0 && path.indexOf("/community/profile") !== 0 },
    ];
    var isLight = document.body.classList.contains("shoug-light-mode");
    var nav = document.createElement("nav");
    nav.id = "shoug-app-nav";
    nav.innerHTML = tabs.map(function(t) {
      return '<a class="shoug-app-tab' + (t.active ? " active" : "") + '" href="' + t.href + '">' + t.label + "</a>";
    }).join("")
      + '<div style="flex:1"></div>'
      + '<button id="shoug-theme-toggle" type="button" aria-label="Toggle dark and light mode" style="margin-right:20px">'
      + (isLight ? MOON_SVG : SUN_SVG)
      + '</button>';
    // Insert as first child so it sits in document flow at the top of the page
    document.body.insertBefore(nav, document.body.firstChild);
    // App pages have no fixed site header, so clear any pre-set padding-top
    document.body.style.paddingTop = "0";

    document.getElementById("shoug-theme-toggle").addEventListener("click", function() {
      var nowLight = document.body.classList.toggle("shoug-light-mode");
      localStorage.setItem("shoug-theme", nowLight ? "light" : "dark");
      if (nowLight) {
        document.documentElement.style.background = "#f8f6ff";
        document.documentElement.style.color = "#21152f";
      } else {
        document.documentElement.style.background = "";
        document.documentElement.style.color = "";
      }
      this.innerHTML = nowLight ? MOON_SVG : SUN_SVG;
    });
  }

  function removeAppNav() {
    var el = document.getElementById("shoug-app-nav");
    if (el) el.remove();
  }

  function removePageIcons() {
    clearTimeout(_notesDebounce);
    ["shoug-page-icons", "shoug-notes-panel"].forEach(function(id) {
      var el = document.getElementById(id); if (el) el.remove();
    });
  }

  // ── Boot ──────────────────────────────────────────────────────────────────

  // ── Theme toggle ──────────────────────────────────────────────────────────

  var MOON_SVG = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 12.79A9 9 0 1111.21 3 7 7 0 0021 12.79z"/></svg>';
  var SUN_SVG  = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="5"/><line x1="12" y1="1" x2="12" y2="3"/><line x1="12" y1="21" x2="12" y2="23"/><line x1="4.22" y1="4.22" x2="5.64" y2="5.64"/><line x1="18.36" y1="18.36" x2="19.78" y2="19.78"/><line x1="1" y1="12" x2="3" y2="12"/><line x1="21" y1="12" x2="23" y2="12"/><line x1="4.22" y1="19.78" x2="5.64" y2="18.36"/><line x1="18.36" y1="5.64" x2="19.78" y2="4.22"/></svg>';

  function injectThemeToggle() {
    if (!isAppPage()) return;
    if (document.getElementById("shoug-theme-toggle")) return;
    var actions = document.querySelector(".shoug-header-actions");
    if (!actions) return;

    var isLight = document.body.classList.contains("shoug-light-mode");
    var btn = document.createElement("button");
    btn.id = "shoug-theme-toggle";
    btn.type = "button";
    btn.setAttribute("aria-label", "Toggle dark and light mode");
    btn.innerHTML = isLight ? SUN_SVG : MOON_SVG;

    btn.addEventListener("click", function () {
      var nowLight = document.body.classList.toggle("shoug-light-mode");
      localStorage.setItem("shoug-theme", nowLight ? "light" : "dark");
      if (nowLight) {
        document.documentElement.style.background = "#f8f6ff";
        document.documentElement.style.color = "#21152f";
      } else {
        document.documentElement.style.background = "";
        document.documentElement.style.color = "";
      }
      btn.innerHTML = nowLight ? SUN_SVG : MOON_SVG;
    });

    actions.insertBefore(btn, actions.firstChild);
  }

  function boot() {
    injectStyles();

    if (!firebase.apps.length) firebase.initializeApp(FB_CONFIG);

    // Signal to other page scripts that Firebase is ready
    window.__shoug_fb = firebase;
    window.dispatchEvent(new CustomEvent("shoug:fb"));

    // Show sign-in button immediately (before auth resolves)
    setHeaderButton(null);
    injectThemeToggle();
    injectBlueprintCredit();

    // First-time visitor onboarding
    setTimeout(showOnboarding, 800);

    // Pick up the result of a signInWithRedirect (GitHub fallback on iOS/Safari)
    firebase.auth().getRedirectResult().catch(function (err) {
      if (err && err.code && err.code !== "auth/no-auth-event") {
        console.error("GitHub sign-in failed:", err.message || err.code);
      }
    });

    firebase.auth().onAuthStateChanged(function (user) {
      if (!user && _notifUnsub) { _notifUnsub(); _notifUnsub = null; }
      setHeaderButton(user);
      removeCompleteBtn();
      removePageIcons();
      removeAppNav();
      removeCommentSection();
      if (user) {
        injectCompleteBtn(user);
        injectPageIcons(user);
        injectAppNav(user);
        injectCommentSection(user);
      }
      injectThemeToggle();
      // Let page-level scripts hook into auth state (used by account dashboard)
      if (typeof window.__shoug_onAuth === "function") {
        window.__shoug_onAuth(user);
      }
    });
  }

  function loadAndBoot() {
    loadScript(FB_BASE + "app-compat.js", function () {
      loadScript(FB_BASE + "auth-compat.js", function () {
        loadScript(FB_BASE + "firestore-compat.js", boot);
      });
    });
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", loadAndBoot);
  } else {
    loadAndBoot();
  }
})();
