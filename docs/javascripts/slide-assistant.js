(function () {
  "use strict";
  if (window.__shougSlideAssistantLoaded) return;
  window.__shougSlideAssistantLoaded = true;

  var route = location.pathname.replace(/index\.html$/, "");
  if (!/\/(slides|slide-breakdowns)\/[^/]+\/$/.test(route)) return;
  var endpoint = window.SHOUG_AI_ENDPOINT || "https://shoug-tech.shoug-alomran.workers.dev/v1/slide-assistant";
  var history = [];

  var style = document.createElement("style");
  style.textContent = [
    ".sg-ai-launch{position:fixed;right:22px;bottom:22px;z-index:99970;height:36px;padding:0 14px;border:1px solid #ff2a4b;background:#0a0514;color:#ff2a4b;font:800 .68rem 'JetBrains Mono',monospace;letter-spacing:.12em;text-transform:uppercase;box-shadow:0 12px 36px rgba(0,0,0,.35);transition:opacity .16s ease,transform .16s ease}",
    ".sg-ai-launch:hover{background:#ff2a4b;color:#050508}.sg-ai-panel{position:fixed;z-index:99980;right:0;top:68px;bottom:0;width:min(410px,100vw);display:flex;flex-direction:column;background:#09050f;color:#f8f7fb;border-left:1px solid rgba(255,42,75,.35);box-shadow:-20px 0 60px rgba(0,0,0,.42);transform:translateX(105%);transition:transform .2s ease}",
    ".sg-ai-panel.is-open{transform:none}.sg-ai-launch[aria-expanded='true']{opacity:0;pointer-events:none;transform:translateY(8px)}.sg-ai-head{padding:18px;border-bottom:1px solid rgba(255,255,255,.1);display:flex;justify-content:space-between;gap:16px}.sg-ai-kicker{color:#ff2a4b;font:800 .58rem 'JetBrains Mono',monospace;letter-spacing:.16em;text-transform:uppercase}.sg-ai-title{margin-top:5px;font:800 .9rem 'JetBrains Mono',monospace}.sg-ai-close{color:#f8f7fb;border:1px solid rgba(255,255,255,.14);width:32px;height:32px;background:transparent;font-size:1.1rem}",
    ".sg-ai-note{padding:10px 18px;color:#9b96a4;border-bottom:1px solid rgba(255,255,255,.07);font-size:.72rem;line-height:1.5}.sg-ai-chat{flex:1;overflow:auto;padding:18px;display:flex;flex-direction:column;gap:12px}.sg-ai-msg{padding:11px 12px;border:1px solid rgba(255,255,255,.1);font-size:.82rem;line-height:1.6;white-space:pre-wrap}.sg-ai-msg.user{margin-left:30px;background:rgba(255,42,75,.08);border-color:rgba(255,42,75,.24)}.sg-ai-msg.bot{margin-right:20px;background:rgba(255,255,255,.025)}",
    ".sg-ai-sources{display:block;margin-top:8px;color:#9b96a4;font:600 .58rem 'JetBrains Mono',monospace}.sg-ai-form{padding:14px;border-top:1px solid rgba(255,255,255,.1);display:grid;grid-template-columns:1fr auto;gap:8px}.sg-ai-input{min-width:0;resize:none;height:66px;background:#110b18;color:#fff;border:1px solid rgba(255,255,255,.14);padding:10px;font:inherit}.sg-ai-send{width:70px;background:#ff2a4b;color:#050508;border:0;font:800 .62rem 'JetBrains Mono',monospace;text-transform:uppercase}.sg-ai-send:disabled{opacity:.45}.sg-ai-panel button,.sg-ai-launch{cursor:pointer}",
    "body.shoug-light-mode .sg-ai-panel{background:#fff;color:#16111f}.shoug-light-mode .sg-ai-msg.bot,.shoug-light-mode .sg-ai-input{background:#f5f1f8;color:#16111f}.shoug-light-mode .sg-ai-close{color:#16111f}@media(max-width:600px){.sg-ai-panel{top:0}}"
  ].join("");
  document.head.appendChild(style);

  var launch = document.createElement("button");
  launch.className = "sg-ai-launch";
  launch.type = "button";
  launch.textContent = "Ask AI";
  launch.setAttribute("aria-expanded", "false");
  var panel = document.createElement("aside");
  panel.className = "sg-ai-panel";
  panel.setAttribute("aria-label", "Slide assistant");
  panel.innerHTML = '<div class="sg-ai-head"><div><div class="sg-ai-kicker">// Grounded assistant</div><div class="sg-ai-title">Ask about this material</div></div><button class="sg-ai-close" type="button" aria-label="Close">&times;</button></div><div class="sg-ai-note">Answers use only the slides or breakdown on this page. AI can make mistakes—check the cited slide or section.</div><div class="sg-ai-chat" aria-live="polite"><div class="sg-ai-msg bot">Ask me to explain a concept, compare two ideas, make an example, or quiz you on this material.</div></div><form class="sg-ai-form"><textarea class="sg-ai-input" maxlength="800" required aria-label="Your question" placeholder="What does this concept mean?"></textarea><button class="sg-ai-send" type="submit">Ask</button></form>';
  document.body.appendChild(launch);
  document.body.appendChild(panel);

  var chat = panel.querySelector(".sg-ai-chat");
  var input = panel.querySelector(".sg-ai-input");
  var send = panel.querySelector(".sg-ai-send");
  function setOpen(open) { panel.classList.toggle("is-open", open); launch.setAttribute("aria-expanded", open ? "true" : "false"); if (open) input.focus(); }
  // Keep the launcher clear of the bookmark/notes rail and the "mark as
  // complete" pill, both injected asynchronously by firebase-auth.js.
  function placeLaunch() {
    var rail = document.getElementById("shoug-page-icons");
    var anchorEl = rail && rail.offsetParent !== null ? rail : document.getElementById("shoug-complete-btn");
    var gap = window.innerWidth <= 600 ? 8 : 10;
    if (!anchorEl || anchorEl.offsetParent === null) {
      launch.style.right = "";
      launch.style.bottom = "";
      return;
    }
    var box = anchorEl.getBoundingClientRect();
    if (!box.width) return;
    launch.style.bottom = Math.max(12, window.innerHeight - box.bottom) + "px";
    launch.style.right = Math.max(12, window.innerWidth - box.left + gap) + "px";
  }
  placeLaunch();
  window.addEventListener("resize", placeLaunch);
  new MutationObserver(function () {
    clearTimeout(placeLaunch.timer);
    placeLaunch.timer = setTimeout(placeLaunch, 60);
  }).observe(document.body, { childList: true });

  launch.addEventListener("click", function () { setOpen(!panel.classList.contains("is-open")); });
  panel.querySelector(".sg-ai-close").addEventListener("click", function () { setOpen(false); });
  document.addEventListener("keydown", function (event) { if (event.key === "Escape") setOpen(false); });

  function message(role, text, sources) {
    var node = document.createElement("div");
    node.className = "sg-ai-msg " + role;
    node.textContent = text;
    if (sources && sources.length) {
      var cite = document.createElement("span");
      cite.className = "sg-ai-sources";
      cite.textContent = "Sources: " + sources.join(", ");
      node.appendChild(cite);
    }
    chat.appendChild(node);
    chat.scrollTop = chat.scrollHeight;
    return node;
  }

  panel.querySelector("form").addEventListener("submit", function (event) {
    event.preventDefault();
    var question = input.value.trim();
    if (!question || send.disabled) return;
    message("user", question);
    input.value = "";
    send.disabled = true;
    var pending = message("bot", "Reading this material…");
    fetch(endpoint, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ route: route, question: question, history: history.slice(-6) })
    }).then(function (response) {
      return response.json().catch(function () { return {}; }).then(function (data) {
        if (!response.ok) throw new Error(data.error || "The assistant is unavailable.");
        return data;
      });
    }).then(function (data) {
      pending.remove();
      message("bot", data.answer || "I could not find that in this material.", data.sources || []);
      history.push({ role: "user", content: question }, { role: "assistant", content: data.answer || "" });
    }).catch(function (error) {
      var reason = error && error.message ? error.message : "";
      if (!reason || /failed to fetch|networkerror|load failed/i.test(reason)) {
        reason = "Could not reach the assistant from this page. Check your connection or try again shortly.";
      }
      pending.textContent = reason;
    }).finally(function () { send.disabled = false; input.focus(); });
  });
})();
