(function () {
  "use strict";
  if (window.__shougCalendarAssistantLoaded) return;
  window.__shougCalendarAssistantLoaded = true;

  var endpoint = window.SHOUG_CALENDAR_AI_ENDPOINT || "https://shoug-tech.shoug-alomran.workers.dev/v1/calendar-assistant";
  var history = [];
  var MODES = {
    chat: { tab: "Ask", intent: "chat", placeholder: "What do I have this week?", hint: "Answers come from the classes, exams and events on your calendar." },
    add: { tab: "Add", intent: "parse", placeholder: "SE322 final on 2026-05-12 from 14:00 to 16:00 in building 5", hint: "Describe it in a sentence. Nothing is saved until you press Add." },
    plan: { tab: "Plan", intent: "plan", placeholder: "Plan revision for my SE322 final", hint: "Proposes study sessions around your existing classes. Nothing is saved until you press Add." },
    brief: { tab: "Brief", intent: "brief", placeholder: "Pick an exam below, then ask for what to focus on.", hint: "Builds a revision brief from that course's material on this site." }
  };
  var mode = "chat";
  var lastPlanProposals = [];

  function timeMinutes(value) {
    var parts = String(value || "").split(":").map(Number);
    return parts.length === 2 && isFinite(parts[0]) && isFinite(parts[1]) ? parts[0] * 60 + parts[1] : null;
  }

  function clock(minutes) {
    minutes = Math.max(0, Math.min(1439, Math.round(minutes)));
    return String(Math.floor(minutes / 60)).padStart(2, "0") + ":" + String(minutes % 60).padStart(2, "0");
  }

  function localPlanRevision(question) {
    if (!lastPlanProposals.length) return null;
    var lower = question.toLowerCase();
    if (!/(from scratch|haven.?t (started|touched)|beginner|no prior|shorter|fewer|evening|after class)/i.test(lower)) return null;
    var revised = lastPlanProposals.slice();
    var bridge = api(), course = revised[0].course || revised[0].title.split(/\s+(?:study|review|chapter|quiz)/i)[0];
    var exam = bridge && bridge.upcomingExams().find(function (entry) { return String(entry.course || "").replace(/[^a-z0-9]/gi, "").toLowerCase() === String(course || "").replace(/[^a-z0-9]/gi, "").toLowerCase(); });
    if (exam) revised = revised.filter(function (proposal) { return proposal.date < exam.date; });
    if (/fewer/i.test(lower)) revised = revised.slice(0, 3);
    if (/from scratch|haven.?t (started|touched)|beginner|no prior/i.test(lower)) {
      var source = lastPlanProposals.map(function (proposal) { return [proposal.title, proposal.note].join(" "); }).join(" ");
      var range = source.match(/chapters?\s*(\d+)\s*(?:-|–|to)\s*(\d+)/i), chapters = [];
      if (range) for (var number = Number(range[1]); number <= Number(range[2]) && chapters.length < 8; number++) chapters.push(number);
      if (!chapters.length) chapters = [1, 2, 3];
      revised = revised.map(function (proposal, index) {
        var chapter = chapters[Math.min(chapters.length - 1, Math.floor(index * chapters.length / Math.max(1, revised.length)))];
        var finalStep = index === revised.length - 1;
        return Object.assign({}, proposal, {
          course: course,
          title: finalStep ? course + " Mixed Practice & Recall" : course + " Learn Chapter " + chapter,
          note: finalStep ? "Test yourself across all chapters, then revisit mistakes" : "Start from the basics: learn Chapter " + chapter + ", make notes, then use active recall"
        });
      });
    }
    revised = revised.map(function (proposal) {
      var start = timeMinutes(proposal.start), duration = Math.max(45, (timeMinutes(proposal.end) || (start === null ? 0 : start + 90)) - (start === null ? 0 : start));
      if (/shorter/i.test(lower)) duration = Math.min(duration, 60);
      if (/evening|after class/i.test(lower)) start = 18 * 60;
      if (start === null) start = 18 * 60;
      return Object.assign({}, proposal, { start: clock(start), end: clock(start + duration) });
    });
    return revised;
  }


  var style = document.createElement("style");
  style.textContent = [
    ".cal-ai-launch{position:fixed;right:24px;bottom:24px;z-index:9100;height:38px;padding:0 16px;border:1px solid rgba(184,41,234,.55);background:#0a0514;color:#b829ea;font:800 .64rem 'JetBrains Mono',monospace;letter-spacing:.12em;text-transform:uppercase;cursor:pointer;box-shadow:0 4px 24px rgba(0,0,0,.4);transition:background .15s,color .15s,opacity .15s}",
    ".cal-ai-launch:hover{background:rgba(184,41,234,.12)}.cal-ai-launch[aria-expanded='true']{opacity:0;pointer-events:none}",
    ".cal-ai-panel{position:fixed;z-index:9110;right:0;top:0;bottom:0;width:min(420px,100vw);display:flex;flex-direction:column;background:#0a0514;color:#f8f7fb;border-left:1px solid rgba(184,41,234,.35);box-shadow:-20px 0 60px rgba(0,0,0,.5);transform:translateX(105%);transition:transform .2s ease;font-family:'JetBrains Mono',monospace}",
    ".cal-ai-panel.is-open{transform:none}",
    ".cal-ai-head{padding:16px 18px;border-bottom:1px solid rgba(255,255,255,.08);display:flex;justify-content:space-between;align-items:flex-start;gap:14px}.cal-ai-kicker{color:#b829ea;font-size:.55rem;letter-spacing:.18em;text-transform:uppercase;font-weight:800}.cal-ai-title{margin-top:5px;font-size:.86rem;font-weight:800}",
    ".cal-ai-close{color:inherit;border:1px solid rgba(255,255,255,.14);width:30px;height:30px;background:transparent;font-size:1rem;cursor:pointer;flex-shrink:0}",
    ".cal-ai-tabs{display:flex;border-bottom:1px solid rgba(255,255,255,.08)}.cal-ai-tab{flex:1;padding:10px 4px;background:transparent;border:0;border-bottom:2px solid transparent;color:#8f8b9a;font:800 .58rem 'JetBrains Mono',monospace;letter-spacing:.12em;text-transform:uppercase;cursor:pointer}.cal-ai-tab.active{color:#b829ea;border-bottom-color:#b829ea}",
    ".cal-ai-hint{padding:10px 18px;color:#8f8b9a;font-size:.62rem;line-height:1.6;border-bottom:1px solid rgba(255,255,255,.06)}",
    ".cal-ai-exam{padding:10px 18px;border-bottom:1px solid rgba(255,255,255,.06);display:none}.cal-ai-exam.show{display:block}.cal-ai-exam select{width:100%;background:rgba(255,255,255,.04);border:1px solid rgba(255,255,255,.12);color:#f8f7fb;font:inherit;font-size:.68rem;padding:8px}",
    ".cal-ai-log{flex:1;overflow:auto;padding:16px 18px;display:flex;flex-direction:column;gap:10px}",
    ".cal-ai-msg{padding:10px 12px;border:1px solid rgba(255,255,255,.09);font-family:'Inter',sans-serif;font-size:.82rem;line-height:1.65;white-space:pre-wrap;word-break:break-word}",
    ".cal-ai-msg.user{margin-left:28px;background:rgba(184,41,234,.09);border-color:rgba(184,41,234,.28)}.cal-ai-msg.bot{background:rgba(255,255,255,.025)}.cal-ai-msg.err{border-color:rgba(255,42,75,.4);color:#ff9db0}",
    ".cal-ai-sources{display:block;margin-top:8px;color:#8f8b9a;font:600 .56rem 'JetBrains Mono',monospace}",
    ".cal-ai-card{border:1px solid rgba(184,41,234,.3);background:rgba(184,41,234,.05);padding:11px 12px;display:flex;flex-direction:column;gap:8px}",
    ".cal-ai-card-title{font-size:.74rem;font-weight:800}.cal-ai-card-meta{color:#8f8b9a;font-size:.6rem;line-height:1.6;font-family:'Inter',sans-serif}",
    ".cal-ai-card-actions{display:flex;gap:8px}.cal-ai-btn{height:28px;padding:0 12px;border:0;background:#b829ea;color:#0a0514;font:800 .56rem 'JetBrains Mono',monospace;letter-spacing:.1em;text-transform:uppercase;cursor:pointer}.cal-ai-btn.ghost{background:transparent;border:1px solid rgba(255,255,255,.16);color:#8f8b9a}.cal-ai-btn:disabled{opacity:.45;cursor:default}",
    ".cal-ai-form{padding:12px 14px;border-top:1px solid rgba(255,255,255,.08);display:grid;grid-template-columns:1fr auto;gap:8px}.cal-ai-input{min-width:0;resize:none;height:62px;background:rgba(255,255,255,.04);color:#f8f7fb;border:1px solid rgba(255,255,255,.14);padding:9px;font-family:'Inter',sans-serif;font-size:.8rem}",
    ".cal-ai-send{width:64px;background:#b829ea;color:#0a0514;border:0;font:800 .6rem 'JetBrains Mono',monospace;text-transform:uppercase;cursor:pointer}.cal-ai-send:disabled{opacity:.45}",
    "body.shoug-light-mode .cal-ai-panel,body.shoug-light-mode .cal-ai-launch{background:#fff;color:#16111f}body.shoug-light-mode .cal-ai-msg.bot{background:rgba(22,17,31,.03)}body.shoug-light-mode .cal-ai-input,body.shoug-light-mode .cal-ai-exam select{background:rgba(22,17,31,.03);color:#16111f}",
    "@media(max-width:600px){.cal-ai-launch{right:16px;bottom:16px}}"
  ].join("");
  document.head.appendChild(style);

  var launch = document.createElement("button");
  launch.className = "cal-ai-launch";
  launch.type = "button";
  launch.textContent = "Ask AI";
  launch.setAttribute("aria-expanded", "false");

  var panel = document.createElement("aside");
  panel.className = "cal-ai-panel";
  panel.setAttribute("aria-label", "Calendar assistant");
  panel.innerHTML = [
    '<div class="cal-ai-head"><div><div class="cal-ai-kicker">// Calendar assistant</div><div class="cal-ai-title">Ask, add, plan, revise</div></div><button class="cal-ai-close" type="button" aria-label="Close">&times;</button></div>',
    '<div class="cal-ai-tabs"></div>',
    '<div class="cal-ai-hint"></div>',
    '<div class="cal-ai-exam"><select aria-label="Exam to revise for"></select></div>',
    '<div class="cal-ai-log" aria-live="polite"></div>',
    '<form class="cal-ai-form"><textarea class="cal-ai-input" maxlength="800" required aria-label="Your request"></textarea><button class="cal-ai-send" type="submit">Send</button></form>'
  ].join("");
  document.body.appendChild(launch);
  document.body.appendChild(panel);

  var tabs = panel.querySelector(".cal-ai-tabs");
  var hint = panel.querySelector(".cal-ai-hint");
  var examWrap = panel.querySelector(".cal-ai-exam");
  var examSelect = examWrap.querySelector("select");
  var log = panel.querySelector(".cal-ai-log");
  var input = panel.querySelector(".cal-ai-input");
  var send = panel.querySelector(".cal-ai-send");

  Object.keys(MODES).forEach(function (name) {
    var tab = document.createElement("button");
    tab.type = "button";
    tab.className = "cal-ai-tab" + (name === mode ? " active" : "");
    tab.textContent = MODES[name].tab;
    tab.addEventListener("click", function () { setMode(name); });
    tabs.appendChild(tab);
  });

  function api() { return window.__shougCalendarAI || null; }

  function setMode(name) {
    mode = name;
    Array.prototype.forEach.call(tabs.children, function (tab, index) {
      tab.classList.toggle("active", Object.keys(MODES)[index] === name);
    });
    hint.textContent = MODES[name].hint;
    input.placeholder = MODES[name].placeholder;
    input.required = name !== "plan" && name !== "brief";
    examWrap.classList.toggle("show", name === "brief");
    if (name === "brief") fillExams();
    input.focus();
  }

  function fillExams() {
    var bridge = api();
    var exams = bridge ? bridge.upcomingExams() : [];
    examSelect.innerHTML = "";
    if (!exams.length) {
      examSelect.innerHTML = '<option value="">No upcoming exams on your calendar</option>';
      return;
    }
    exams.forEach(function (exam) {
      var option = document.createElement("option");
      option.value = exam.course + "|" + exam.type + "|" + exam.date;
      option.textContent = exam.date + " · " + exam.course + " " + exam.type;
      examSelect.appendChild(option);
    });
  }

  function say(role, text) {
    var node = document.createElement("div");
    node.className = "cal-ai-msg " + role;
    node.textContent = text;
    log.appendChild(node);
    log.scrollTop = log.scrollHeight;
    return node;
  }

  function describe(proposal) {
    var when = proposal.start ? proposal.start + (proposal.end ? "–" + proposal.end : "") : "all day";
    var span = proposal.endDate && proposal.endDate !== proposal.date ? proposal.date + " → " + proposal.endDate : proposal.date;
    var parts = [span + " · " + when, proposal.kind];
    if (proposal.location) parts.push(proposal.location);
    if (proposal.note) parts.push(proposal.note);
    return parts.join(" · ");
  }

  function card(proposal) {
    var bridge = api();
    var node = document.createElement("div");
    node.className = "cal-ai-card";
    var title = document.createElement("div");
    title.className = "cal-ai-card-title";
    title.textContent = proposal.kind === "exam" && proposal.course ? proposal.course + " " + (proposal.examType || "exam") : proposal.title;
    var meta = document.createElement("div");
    meta.className = "cal-ai-card-meta";
    meta.textContent = describe(proposal);
    var actions = document.createElement("div");
    actions.className = "cal-ai-card-actions";
    var add = document.createElement("button");
    add.type = "button";
    add.className = "cal-ai-btn";
    add.textContent = "Add";
    var skip = document.createElement("button");
    skip.type = "button";
    skip.className = "cal-ai-btn ghost";
    skip.textContent = "Discard";
    add.addEventListener("click", function () {
      if (!bridge) return;
      add.disabled = skip.disabled = true;
      var save = proposal.kind === "exam" ? bridge.addExam(proposal) : bridge.addEvent(proposal);
      Promise.resolve(save).then(function (saved) {
        if (saved === false) { add.disabled = skip.disabled = false; return; }
        actions.remove();
        meta.textContent = "Added to your calendar · " + describe(proposal);
      });
    });
    skip.addEventListener("click", function () { node.remove(); });
    actions.appendChild(add);
    actions.appendChild(skip);
    node.appendChild(title);
    node.appendChild(meta);
    node.appendChild(actions);
    log.appendChild(node);
    log.scrollTop = log.scrollHeight;
  }

  function setOpen(open) {
    panel.classList.toggle("is-open", open);
    launch.setAttribute("aria-expanded", open ? "true" : "false");
    if (open) { if (mode === "brief") fillExams(); input.focus(); }
  }
  launch.addEventListener("click", function () { setOpen(!panel.classList.contains("is-open")); });
  panel.querySelector(".cal-ai-close").addEventListener("click", function () { setOpen(false); });
  document.addEventListener("keydown", function (event) { if (event.key === "Escape") setOpen(false); });

  panel.querySelector("form").addEventListener("submit", function (event) {
    event.preventDefault();
    var bridge = api();
    if (!bridge || !bridge.signedIn()) { say("bot err", "Sign in to use the calendar assistant — it works from your saved classes and exams."); return; }
    var question = input.value.trim();
    if (send.disabled) return;
    if (!question && mode !== "plan") return;

    if (mode === "plan") {
      var localRevision = localPlanRevision(question);
      if (localRevision) {
        say("user", question);
        say("bot", "I revised the previous plan for " + (localRevision[0].course || "that exam") + " — nothing is saved yet:");
        localRevision.forEach(card);
        lastPlanProposals = localRevision;
        input.value = "";
        return;
      }
    }

    var config = MODES[mode];
    var payload = { intent: config.intent, question: question, today: bridge.today(), snapshot: bridge.snapshot() };
    if (mode === "chat") payload.history = history.slice(-6);
    if (mode === "brief") {
      var selection = examSelect.value;
      if (!selection) { say("bot err", "Add an upcoming exam to your calendar first, then I can build a brief for it."); return; }
      var parts = selection.split("|");
      payload.course = courseRoute(parts[0]);
      payload.question = (question || "What should I focus on") + " for the " + parts[0] + " " + parts[1] + " on " + parts[2] + "?";
      if (!payload.course) { say("bot err", "I could not match " + parts[0] + " to a course page on this site."); return; }
    }

    if (question) say("user", question);
    input.value = "";
    send.disabled = true;
    var pending = say("bot", mode === "plan" ? "Looking for free slots…" : "Working…");

    fetch(endpoint, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload)
    }).then(function (response) {
      return response.json().catch(function () { return {}; }).then(function (data) {
        if (!response.ok) throw new Error(data.error || "The assistant is unavailable.");
        return data;
      });
    }).then(function (data) {
      pending.remove();
      if (data.proposals && data.proposals.length) {
        say("bot", data.proposals.length === 1 ? "Here is what I understood — nothing is saved yet:" : "Here is what I propose — nothing is saved yet:");
        data.proposals.forEach(card);
        if (mode === "plan") lastPlanProposals = data.proposals.slice();
        return;
      }
      var node = say("bot", data.answer || "I could not work that out from your calendar.");
      if (data.sources && data.sources.length) {
        var cite = document.createElement("span");
        cite.className = "cal-ai-sources";
        cite.textContent = "Sources: " + data.sources.join(", ");
        node.appendChild(cite);
      }
      if (mode === "chat") history.push({ role: "user", content: question }, { role: "assistant", content: data.answer || "" });
    }).catch(function (error) {
      var reason = error && error.message ? error.message : "";
      if (!reason || /failed to fetch|networkerror|load failed/i.test(reason)) {
        reason = "Could not reach the assistant. Check your connection and try again.";
      }
      pending.textContent = reason;
      pending.className = "cal-ai-msg bot err";
    }).finally(function () { send.disabled = false; input.focus(); });
  });

  // Course codes map onto the academics tree by slug; the assistant needs the
  // course page route so the worker can pull that course's material.
  function courseRoute(course) {
    var code = String(course || "").trim().toLowerCase().replace(/[^a-z0-9]/g, "");
    if (!code) return "";
    var map = window.SHOUG_COURSE_ROUTES || {};
    return map[code] || "";
  }

  setMode("chat");
  say("bot", "Ask about your schedule, add something in plain words, plan revision around your classes, or build a brief for an upcoming exam.");
})();
