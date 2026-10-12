(function () {
  "use strict";
  if (window.__shougAboutAssistantLoaded) return;
  window.__shougAboutAssistantLoaded = true;

  // The Worker holds the only copy of what the assistant knows (a public
  // profile). Nothing about Shoug is sent from the page.
  var endpoint =
    window.SHOUG_ABOUT_AI_ENDPOINT ||
    "https://shoug-tech.shoug-alomran.workers.dev/v1/about-assistant";
  var root = document.getElementById("about-assistant");
  if (!root) return;
  var log = root.querySelector(".aa-log"),
    form = root.querySelector(".aa-form"),
    input = root.querySelector(".aa-input"),
    send = root.querySelector(".aa-send"),
    history = [],
    busy = false;

  function isArabic() {
    return document.documentElement.lang === "ar";
  }

  // Turn site links, URLs and the contact email into anchors without ever
  // inserting model output as HTML.
  var LINK =
    /(https?:\/\/[^\s)]+|(?:www\.)?(?:shoug-tech\.com|blueprint\.shoug-tech\.com|linkedin\.com|github\.com)\/?[^\s),]*|[\w.+-]+@shoug-tech\.com)/gi;
  function appendRich(el, text) {
    var last = 0;
    text.replace(LINK, function (match, _g, offset) {
      var clean = match.replace(/[.,;:]+$/, "");
      el.appendChild(document.createTextNode(text.slice(last, offset)));
      var a = document.createElement("a");
      a.textContent = clean;
      a.href = /@/.test(clean)
        ? "mailto:" + clean
        : /^https?:/.test(clean)
          ? clean
          : "https://" + clean;
      if (!/^(https:\/\/)?(www\.)?shoug-tech\.com/.test(a.href) && !/^mailto:/.test(a.href)) {
        a.target = "_blank";
        a.rel = "noopener noreferrer";
      }
      el.appendChild(a);
      last = offset + clean.length;
      return match;
    });
    el.appendChild(document.createTextNode(text.slice(last)));
  }

  // **bold** inside a line, links handled by appendRich.
  function appendInline(el, text) {
    String(text)
      .split(/\*\*(.+?)\*\*/g)
      .forEach(function (part, i) {
        if (!part) return;
        if (i % 2) {
          var b = document.createElement("strong");
          appendRich(b, part);
          el.appendChild(b);
        } else appendRich(el, part);
      });
  }

  // Plain-text answers: blank lines split paragraphs, lines starting with
  // "- ", "* " or "1." become list items.
  function renderAnswer(body, text) {
    var list = null,
      para = null;
    String(text)
      .replace(/\r/g, "")
      .split("\n")
      .forEach(function (raw) {
        var line = raw.trim(),
          bullet = line.match(/^(?:[-*\u2022]|(\d+)[.)])\s+(.*)$/);
        if (!line) {
          list = para = null;
          return;
        }
        if (bullet) {
          var tag = bullet[1] ? "OL" : "UL";
          if (!list || list.tagName !== tag) {
            list = document.createElement(tag);
            body.appendChild(list);
          }
          para = null;
          var li = document.createElement("li");
          appendInline(li, bullet[2]);
          list.appendChild(li);
          return;
        }
        list = null;
        line = line.replace(/^#+\s*/, "");
        if (para) para.appendChild(document.createElement("br"));
        else {
          para = document.createElement("p");
          body.appendChild(para);
        }
        appendInline(para, line);
      });
  }

  function say(role, text, extra) {
    var row = document.createElement("div");
    row.className = "aa-msg aa-" + role + (extra ? " " + extra : "");
    var who = document.createElement("span");
    who.className = "aa-who";
    who.textContent =
      role === "user"
        ? isArabic()
          ? "أنت"
          : "YOU"
        : isArabic()
          ? "المساعد"
          : "ASSISTANT";
    var body = document.createElement("div");
    body.className = "aa-text";
    renderAnswer(body, text);
    row.appendChild(who);
    row.appendChild(body);
    log.appendChild(row);
    log.hidden = false;
    log.scrollTop = log.scrollHeight;
    return row;
  }

  function ask(question) {
    question = String(question || "").trim();
    if (!question || busy) return;
    busy = true;
    send.disabled = true;
    input.value = "";
    say("user", question);
    var pending = say("bot", isArabic() ? "جارٍ التفكير..." : "Thinking...", "aa-pending");
    fetch(endpoint, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ question: question, history: history }),
    })
      .then(function (response) {
        return response
          .json()
          .catch(function () {
            return {};
          })
          .then(function (data) {
            if (!response.ok || !data.answer)
              throw new Error(data.error || "The assistant is unavailable.");
            return data;
          });
      })
      .then(function (data) {
        pending.remove();
        say("bot", data.answer);
        history.push(
          { role: "user", content: question },
          { role: "assistant", content: data.answer },
        );
        history = history.slice(-6);
      })
      .catch(function (error) {
        pending.remove();
        say(
          "bot",
          (error && error.message) ||
            "The assistant is unavailable right now. Please try again later.",
          "aa-err",
        );
      })
      .then(function () {
        busy = false;
        send.disabled = false;
        input.focus();
      });
  }

  form.addEventListener("submit", function (e) {
    e.preventDefault();
    ask(input.value);
  });
  root.querySelectorAll("[data-aa-q]").forEach(function (chip) {
    chip.addEventListener("click", function () {
      ask(isArabic() && chip.dataset.aaQAr ? chip.dataset.aaQAr : chip.dataset.aaQ);
    });
  });
})();
