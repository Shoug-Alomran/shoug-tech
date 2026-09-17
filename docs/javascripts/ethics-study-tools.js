/* Shared listening controls, transcript and transcript-derived chapter links. */
(() => {
  "use strict";
  // The surrounding slide page owns playback when a lesson is embedded.
  try {
    if (
      window.parent !== window &&
      window.parent.document.querySelector(
        'script[src="/javascripts/ethics-study-tools.js"]',
      )
    )
      return;
  } catch (_) {}
  const base = "/academics/other-courses/ethcs303/video-explanations/";
  const path = location.pathname.replace(/index\.html$/, "");
  const ar =
    document.documentElement.lang.startsWith("ar") ||
    new URLSearchParams(location.search).get("lang") === "ar";
  const text = (en, arabic) => (ar ? arabic : en);
  const node = (tag, cls, content) => {
    const el = document.createElement(tag);
    if (cls) el.className = cls;
    if (content != null) el.textContent = content;
    return el;
  };
  const time = (s) =>
    `${Math.floor(s / 60)}:${String(Math.floor(s % 60)).padStart(2, "0")}`;
  const getJSON = async (url) => {
    const response = await fetch(url);
    if (!response.ok) throw new Error("Unable to load lesson data");
    return response.json();
  };
  const pendingSeeks = new WeakMap();
  const cancelSeek = (media) => {
    const pending = pendingSeeks.get(media);
    if (pending) media.removeEventListener("loadedmetadata", pending);
    pendingSeeks.delete(media);
  };
  const seek = (media, t) => {
    cancelSeek(media);
    const go = () => {
      pendingSeeks.delete(media);
      media.currentTime = t;
      media.play().catch(() => {});
    };
    if (media.readyState >= 1) go();
    else {
      pendingSeeks.set(media, go);
      media.addEventListener("loadedmetadata", go, { once: true });
      media.load();
      media.play().catch(() => {});
    }
  };
  async function tools(host, media, lesson) {
    const wrap = node("section", "ethics-study-tools");
    wrap.setAttribute("aria-label", text("Lesson tools", "أدوات الدرس"));
    host.append(wrap);
    const status = node(
      "p",
      "",
      text("Loading lesson tools…", "جارٍ تحميل أدوات الدرس…"),
    );
    wrap.append(status);
    try {
      const data = await getJSON(`${base}lesson-data/${lesson.id}.json`);
      if (!wrap.isConnected) return;
      status.remove();
      const heading = node("h3", "", text("Lesson sections", "أقسام الدرس"));
      const chapters = node("nav", "ethics-chapters");
      chapters.setAttribute(
        "aria-label",
        text("Skip to a lesson section", "الانتقال إلى قسم الدرس"),
      );
      const chapterButtons = data.chapters.map((chapter) => {
        const button = node(
          "button",
          "",
          `${time(chapter.time)} · ${chapter.title}`,
        );
        button.type = "button";
        button.addEventListener("click", () => seek(media, chapter.time));
        chapters.append(button);
        return button;
      });
      const toggle = node(
        "button",
        "ethics-transcript-toggle",
        text("Lesson Transcript", "نص الدرس"),
      );
      toggle.type = "button";
      toggle.setAttribute("aria-expanded", "false");
      const transcript = node("div", "ethics-transcript");
      transcript.id = `transcript-${lesson.id}-${Math.random().toString(36).slice(2, 7)}`;
      transcript.hidden = true;
      toggle.setAttribute("aria-controls", transcript.id);
      transcript.append(
        node(
          "p",
          "ethics-caption-note",
          text(
            "Automatic Arabic transcript; may contain errors. Select a line to jump to that moment.",
            "نص عربي مُفرّغ آليًا وقد يحتوي أخطاء. اختر سطرًا للانتقال إليه.",
          ),
        ),
      );
      const search = node("input");
      search.type = "search";
      search.placeholder = text("Search transcript", "البحث في النص");
      search.setAttribute("aria-label", search.placeholder);
      transcript.append(search);
      const list = node("div", "ethics-transcript-lines");
      transcript.append(list);
      const buttons = data.transcript.map((cue) => {
        const button = node("button", "ethics-transcript-cue");
        button.type = "button";
        button.append(node("span", "ethics-cue-time", time(cue.start)));
        const words = node("span", "", cue.text);
        words.dir = "auto";
        button.append(words);
        button.addEventListener("click", () => seek(media, cue.start));
        list.append(button);
        return button;
      });
      search.addEventListener("input", () => {
        const q = search.value.toLocaleLowerCase();
        buttons.forEach((button, i) => {
          button.hidden = !data.transcript[i].text
            .toLocaleLowerCase()
            .includes(q);
        });
      });
      toggle.addEventListener("click", () => {
        transcript.hidden = !transcript.hidden;
        toggle.setAttribute("aria-expanded", String(!transcript.hidden));
      });
      let priorCue = -1,
        priorChapter = -1;
      const update = () => {
        if (!wrap.isConnected) {
          media.removeEventListener("timeupdate", update);
          return;
        }
        let lo = 0,
          hi = data.transcript.length;
        while (lo < hi) {
          const mid = (lo + hi) >> 1;
          if (data.transcript[mid].start <= media.currentTime) lo = mid + 1;
          else hi = mid;
        }
        const cue =
          lo > 0 && media.currentTime < data.transcript[lo - 1].end
            ? lo - 1
            : -1;
        if (cue !== priorCue) {
          if (buttons[priorCue])
            buttons[priorCue].removeAttribute("aria-current");
          if (buttons[cue]) buttons[cue].setAttribute("aria-current", "true");
          priorCue = cue;
        }
        let chapter = 0;
        data.chapters.forEach((c, i) => {
          if (c.time <= media.currentTime) chapter = i;
        });
        if (chapter !== priorChapter) {
          if (chapterButtons[priorChapter])
            chapterButtons[priorChapter].removeAttribute("aria-current");
          if (chapterButtons[chapter])
            chapterButtons[chapter].setAttribute("aria-current", "true");
          priorChapter = chapter;
        }
      };
      media.addEventListener("timeupdate", update);
      update();
      wrap.append(heading, chapters, toggle, transcript);
    } catch (error) {
      status.textContent = text(
        "Lesson tools could not load. Please reload to try again.",
        "تعذر تحميل أدوات الدرس. أعد تحميل الصفحة للمحاولة.",
      );
    }
  }
  getJSON(base + "study-tools.json")
    .then((index) => {
      const detail = index.lessons.find((v) => v.page === path);
      if (detail) {
        const media = document.querySelector("[data-video-lesson] video");
        if (media) {
          const host = node("div");
          media.closest(".video-player").after(host);
          tools(host, media, detail);
        }
        return;
      }
      const route = Object.keys(index.routes).find((r) => path.startsWith(r));
      if (!route) return;
      const lessons = index.routes[route]
        .map((id) => index.lessons.find((v) => v.id === id))
        .filter(Boolean);
      const panel = node("details", "ethics-listen-panel");
      panel.append(
        node("summary", "", text("Listen to my explanation", "استمع إلى شرحي")),
      );
      const body = node("div", "ethics-listen-body");
      panel.append(body);
      const select = node("select");
      select.setAttribute(
        "aria-label",
        text("Choose a recording", "اختر تسجيلًا"),
      );
      lessons.forEach((v) => {
        const option = node("option", "", v.title);
        option.value = v.id;
        select.append(option);
      });
      body.append(select);
      const audio = node("audio");
      audio.controls = true;
      audio.preload = "none";
      body.append(audio);
      const full = node(
        "a",
        "ethics-full-lesson",
        text("Open full video lesson", "فتح درس الفيديو"),
      );
      body.append(full);
      let activeHost;
      const choose = () => {
        const lesson = lessons.find((v) => v.id === select.value);
        cancelSeek(audio);
        audio.pause();
        audio.src = lesson.url;
        full.href = lesson.page;
        if (activeHost) activeHost.remove();
        activeHost = node("div");
        body.append(activeHost);
        tools(activeHost, audio, lesson);
      };
      select.addEventListener("change", choose);
      let initialized = false;
      panel.addEventListener("toggle", () => {
        if (panel.open && !initialized) {
          initialized = true;
          choose();
        }
        if (!panel.open) {
          cancelSeek(audio);
          audio.pause();
        }
      });
      document.body.append(panel);
    })
    .catch((error) => console.warn("Ethics lesson tools:", error.message));
})();
