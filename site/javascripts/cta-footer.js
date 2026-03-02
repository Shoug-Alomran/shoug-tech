(function () {
  const EMAIL = "inquiry@shoug-tech.com";
  const LINKEDIN = "https://www.linkedin.com/in/shoug-alomran";
  const GITHUB = "https://github.com/Shoug-Alomran";
  const REPO = `${GITHUB}/My-Garden`;
  const LS_LEFT_KEY = "sg_hide_left_sidebar";
  const LS_RIGHT_KEY = "sg_hide_right_sidebar";

  function isArabic() {
    return location.pathname.includes("/ar/");
  }

  function getBase() {
    // MkDocs Material base path (GitHub Pages subpath safe)
    try {
      if (typeof __md_get === "function") return __md_get("__base") || "";
    } catch (e) {}
    return "";
  }

  function url(path) {
    const base = getBase().replace(/\/$/, ""); // remove trailing slash
    const clean = String(path || "").replace(/^\//, ""); // remove leading slash
    return `${base}/${clean}`.replace(/\/+$/, "/"); // ensure ends with /
  }

  function repoPolicyFile(path) {
    const clean = String(path || "").replace(/^\//, "");
    return `${REPO}/blob/main/policy/${clean}`;
  }

  function addHeaderCTA() {
    const headerInner = document.querySelector(".md-header__inner");
    if (!headerInner) return;

    // Avoid duplicating on instant navigation
    if (headerInner.querySelector(".header-actions")) return;

    const wrap = document.createElement("div");
    wrap.className = "header-actions";

    // Sidebar toggles
    const leftToggle = document.createElement("button");
    leftToggle.type = "button";
    leftToggle.className = "header-icon-btn header-toggle-btn header-toggle-left";
    leftToggle.setAttribute("aria-label", isArabic() ? "إخفاء/إظهار القائمة الجانبية اليسرى" : "Toggle left sidebar");
    leftToggle.setAttribute("title", isArabic() ? "القائمة اليسرى" : "Left sidebar");
    leftToggle.innerHTML = `
      <svg viewBox="0 0 24 24" aria-hidden="true" focusable="false">
        <path d="M3 4h18v16H3V4zm2 2v12h4V6H5zm6 0v2h8V6h-8zm0 4v2h8v-2h-8zm0 4v2h8v-2h-8z"/>
      </svg>
    `;

    const rightToggle = document.createElement("button");
    rightToggle.type = "button";
    rightToggle.className = "header-icon-btn header-toggle-btn header-toggle-right";
    rightToggle.setAttribute("aria-label", isArabic() ? "إخفاء/إظهار جدول المحتويات" : "Toggle table of contents");
    rightToggle.setAttribute("title", isArabic() ? "جدول المحتويات" : "Table of contents");
    rightToggle.innerHTML = `
      <svg viewBox="0 0 24 24" aria-hidden="true" focusable="false">
        <path d="M3 4h18v16H3V4zm2 2v12h8V6H5zm10 0v2h4V6h-4zm0 4v2h4v-2h-4zm0 4v2h4v-2h-4z"/>
      </svg>
    `;

    // LinkedIn button
    const li = document.createElement("a");
    li.className = "header-icon-btn header-linkedin";
    li.href = LINKEDIN;
    li.target = "_blank";
    li.rel = "noopener noreferrer";
    li.setAttribute("aria-label", "LinkedIn");
    li.innerHTML = `
      <svg viewBox="0 0 24 24" aria-hidden="true" focusable="false">
        <path d="M4.98 3.5C4.98 4.88 3.87 6 2.5 6S0 4.88 0 3.5 1.11 1 2.5 1 4.98 2.12 4.98 3.5zM0.5 8H4.5V23H0.5V8zM8 8H12V10.05H12.06C12.62 9.02 14 7.93 16.08 7.93 20.36 7.93 21 10.44 21 14.02V23H17V15.02C17 13.1 16.96 10.64 14.33 10.64 11.66 10.64 11.25 12.72 11.25 14.88V23H7.25V8H8z"/>
      </svg>
    `;

    // GitHub button
    const gh = document.createElement("a");
    gh.className = "header-icon-btn header-github";
    gh.href = GITHUB;
    gh.target = "_blank";
    gh.rel = "noopener noreferrer";
    gh.setAttribute("aria-label", "GitHub");
    gh.innerHTML = `
      <svg viewBox="0 0 24 24" aria-hidden="true" focusable="false">
        <path d="M12 0.5C5.73 0.5.75 5.63.75 12c0 5.11 3.29 9.44 7.86 10.97.58.11.79-.26.79-.58v-2.1c-3.2.71-3.88-1.56-3.88-1.56-.53-1.36-1.29-1.72-1.29-1.72-1.05-.73.08-.72.08-.72 1.16.08 1.77 1.21 1.77 1.21 1.03 1.8 2.7 1.28 3.36.98.1-.76.4-1.28.73-1.57-2.55-.3-5.23-1.3-5.23-5.78 0-1.28.45-2.33 1.2-3.15-.12-.3-.52-1.52.12-3.17 0 0 .98-.32 3.2 1.2.93-.26 1.92-.39 2.9-.39.99 0 1.98.13 2.9.39 2.22-1.52 3.2-1.2 3.2-1.2.64 1.65.24 2.87.12 3.17.75.82 1.2 1.87 1.2 3.15 0 4.49-2.69 5.48-5.25 5.77.41.36.78 1.08.78 2.18v3.23c0 .32.21.69.8.58 4.56-1.53 7.84-5.86 7.84-10.97C23.25 5.63 18.27.5 12 .5z"/>
      </svg>
    `;

    // Contact button
    const cta = document.createElement("a");
    cta.className = "header-cta";
    cta.href = `mailto:${EMAIL}`;
    cta.textContent = isArabic() ? "تواصل" : "Contact";
    cta.setAttribute("aria-label", cta.textContent);

    wrap.appendChild(leftToggle);
    wrap.appendChild(rightToggle);
    wrap.appendChild(li);
    wrap.appendChild(gh);
    wrap.appendChild(cta);

    headerInner.appendChild(wrap);
  }

  function addFooterBlock() {
    const footer = document.querySelector(".md-footer");
    if (!footer) return;
    if (footer.querySelector(".custom-footer")) return;

    const meta = footer.querySelector(".md-footer-meta");
    const block = document.createElement("section");
    block.className = "custom-footer";

    const t = isArabic()
      ? {
          brand: "حديقة شوق الرقمية",
          title: "ملاحظات جديدة وتحديثات",
          subtitle: "مساحة شخصية أجمع فيها ملاحظات المواد والملخصات والروابط والمشاريع.",
          placeholder: "البريد الإلكتروني",
          subscribe: "اشتراك",
          note: "بإدخال بريدك، أنتِ توافقين على التواصل معك عند نشر ملاحظات أو تحديثات جديدة.",
          explore: "استكشف",
          policies: "السياسات",
          contact: "التواصل",
          home: "الرئيسية",
          academics: "المسار الأكاديمي",
          career: "التطوير المهني",
          links: "الروابط",
          privacy: "إشعار الخصوصية",
          disclaimer: "إخلاء مسؤولية أكاديمي",
          copyright: "حقوق النشر",
          linkedin: "LinkedIn",
          github: "GitHub",
        }
      : {
          brand: "Shoug’s Digital Garden",
          title: "New notes & updates",
          subtitle: "A personal knowledge base for course notes, summaries, links, and projects.",
          placeholder: "Email address",
          subscribe: "Subscribe",
          note: "By entering your email, you agree to be contacted when new notes or updates are published.",
          explore: "Explore",
          policies: "Policies",
          contact: "Contact",
          home: "Home",
          academics: "Academics",
          career: "Career Development",
          links: "Links",
          privacy: "Privacy Notice",
          disclaimer: "Academic Disclaimer",
          copyright: "Copyright",
          linkedin: "LinkedIn",
          github: "GitHub",
        };

    // Navigation links
    const homeHref = isArabic() ? url("ar/") : url("");
    const academicsHref = isArabic() ? url("ar/Academics/Intro/") : url("Academics/Intro/");
    const careerHref = isArabic()
      ? url("ar/career-development/me/")
      : url("career-development/me/");
    const linksHref = isArabic() ? url("ar/links/") : url("links/");

    // Policies (moved to repository-level policy folder)
    const privacyHref = isArabic()
      ? repoPolicyFile("privacy-notice.ar.md")
      : repoPolicyFile("privacy-notice.md");
    const disclaimerHref = isArabic()
      ? repoPolicyFile("academic-disclaimer.ar.md")
      : repoPolicyFile("academic-disclaimer.md");
    const copyrightHref = isArabic()
      ? repoPolicyFile("copyright.ar.md")
      : repoPolicyFile("copyright.md");

    const dirAttr = isArabic() ? 'dir="rtl"' : 'dir="ltr"';

    block.innerHTML = `
      <div class="custom-footer__inner" ${dirAttr}>
        <div class="custom-footer__left">
          <div class="custom-footer__brand">${t.brand}</div>
          <div class="custom-footer__title">${t.title}</div>
          <div class="custom-footer__subtitle">${t.subtitle}</div>

          <form class="custom-footer__form" novalidate>
            <input
              class="custom-footer__input"
              type="email"
              name="email"
              placeholder="${t.placeholder}"
              autocomplete="email"
              inputmode="email"
              required
            >
            <button class="custom-footer__button" type="submit">${t.subscribe}</button>
          </form>

          <div class="custom-footer__note">${t.note}</div>
        </div>

        <div class="custom-footer__right">
          <div class="footer-col">
            <div class="footer-col__title">${t.explore}</div>
            <a class="footer-link" href="${homeHref}">${t.home}</a>
            <a class="footer-link" href="${academicsHref}">${t.academics}</a>
            <a class="footer-link" href="${careerHref}">${t.career}</a>
            <a class="footer-link" href="${linksHref}">${t.links}</a>
          </div>

          <div class="footer-col">
            <div class="footer-col__title">${t.policies}</div>
            <a class="footer-link" href="${privacyHref}">${t.privacy}</a>
            <a class="footer-link" href="${disclaimerHref}">${t.disclaimer}</a>
            <a class="footer-link" href="${copyrightHref}">${t.copyright}</a>
          </div>

          <div class="footer-col">
            <div class="footer-col__title">${t.contact}</div>
            <a class="footer-link" href="mailto:${EMAIL}">${EMAIL}</a>
            <a class="footer-link" href="${LINKEDIN}" target="_blank" rel="noopener noreferrer">${t.linkedin}</a>
            <a class="footer-link" href="${GITHUB}" target="_blank" rel="noopener noreferrer">${t.github}</a>
          </div>
        </div>
      </div>
    `;

    // Better “subscribe” behavior: open mail with subject/body (mailto cannot actually subscribe)
    const form = block.querySelector(".custom-footer__form");
    const input = block.querySelector(".custom-footer__input");

    form.addEventListener("submit", (e) => {
      e.preventDefault();
      const value = (input.value || "").trim();

      // basic validity
      if (!value || !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value)) {
        input.focus();
        input.classList.add("is-invalid");
        return;
      }
      input.classList.remove("is-invalid");

      const subject = encodeURIComponent(isArabic() ? "اشتراك بالتحديثات" : "Subscribe to updates");
      const body = encodeURIComponent(
        isArabic()
          ? `مرحبًا،\n\nأرغب بالاشتراك بالتحديثات.\n\nالبريد: ${value}\n`
          : `Hi,\n\nI’d like to subscribe to updates.\n\nEmail: ${value}\n`
      );

      window.location.href = `mailto:${EMAIL}?subject=${subject}&body=${body}`;
      input.value = "";
    });

    if (meta) footer.insertBefore(block, meta);
    else footer.prepend(block);
  }

  function run() {
    addHeaderCTA();
    addQuickLinksWidget();
    initSidebarToggles();
    addFooterBlock();
    replaceFooterCredit();
    initRevealMotion();
    syncEmbeddedIframesTheme();
    translateTabs();
  }

  function replaceFooterCredit() {
    const footerMeta = document.querySelector(".md-footer-meta");
    if (!footerMeta) return;

    const creditLink = footerMeta.querySelector(
      'a[href*="squidfunk.github.io/mkdocs-material"], a[href*="mkdocs-material"]'
    );
    if (!creditLink) return;

    creditLink.textContent = "Made by Blueprint";
    creditLink.href = "https://blueprint.shoug-tech.com/";
    creditLink.target = "_blank";
    creditLink.rel = "noopener noreferrer";
  }

  function addQuickLinksWidget() {
    const content = document.querySelector(".md-content__inner.md-typeset");
    if (!content) return;
    if (content.querySelector(".quick-links-widget")) return;
    if (location.pathname.endsWith("/")) {
      const p = location.pathname.replace(/\/+$/, "/");
      if (p === "/" || p === "/ar/" || p === "/start-here/" || p === "/ar/start-here/") return;
    }

    const links = isArabic()
      ? [
          ["الرئيسية", url("ar/")],
          ["ابدأ من هنا", url("ar/start-here/")],
          ["نظرة عامة أكاديمية", url("ar/Academics/Intro/")],
          ["الخطة الأكاديمية", url("ar/academic-plan/")],
          ["SE201", url("ar/Academics/software-engineering/SE201/Intro/")],
          ["CS340", url("ar/Academics/computer-science/CS340/Intro/")],
          ["CYS401", url("ar/Academics/cyber-security/CYS401/Intro/")],
          ["التطوير المهني", url("ar/career-development/Intro/")],
          ["المشاريع", url("ar/career-development/projects/")],
          ["الروابط", url("ar/links/")]
        ]
      : [
          ["Home", url("")],
          ["Start Here", url("start-here/")],
          ["Academics Overview", url("Academics/Intro/")],
          ["Academic Plan", url("academic-plan/")],
          ["SE201", url("Academics/software-engineering/SE201/Intro/")],
          ["CS340", url("Academics/computer-science/CS340/Intro/")],
          ["CYS401", url("Academics/cyber-security/CYS401/Intro/")],
          ["Career Development", url("career-development/Intro/")],
          ["Projects", url("career-development/projects/")],
          ["Links", url("links/")]
        ];

    const block = document.createElement("details");
    block.className = "quick-links-widget";

    const summary = document.createElement("summary");
    summary.textContent = isArabic() ? "وصول سريع (أكثر 10 صفحات)" : "Quick Access (Top 10 pages)";
    block.appendChild(summary);

    const list = document.createElement("div");
    list.className = "quick-links-widget__list";
    links.forEach(([label, href]) => {
      const a = document.createElement("a");
      a.className = "quick-links-widget__link";
      a.href = href;
      a.textContent = label;
      list.appendChild(a);
    });
    block.appendChild(list);

    const firstHeading = content.querySelector("h1, h2");
    if (firstHeading && firstHeading.parentElement) {
      firstHeading.parentElement.insertBefore(block, firstHeading.nextSibling);
    } else {
      content.prepend(block);
    }
  }

  function setToggleVisualState() {
    const leftBtn = document.querySelector(".header-toggle-left");
    const rightBtn = document.querySelector(".header-toggle-right");
    if (leftBtn) {
      leftBtn.classList.toggle("is-active", document.body.classList.contains("sg-hide-left-sidebar"));
    }
    if (rightBtn) {
      rightBtn.classList.toggle("is-active", document.body.classList.contains("sg-hide-right-sidebar"));
    }
  }

  function initSidebarToggles() {
    const leftBtn = document.querySelector(".header-toggle-left");
    const rightBtn = document.querySelector(".header-toggle-right");
    if (!leftBtn || !rightBtn) return;

    if (!leftBtn.dataset.bound) {
      leftBtn.dataset.bound = "1";
      leftBtn.addEventListener("click", () => {
        const hide = !document.body.classList.contains("sg-hide-left-sidebar");
        document.body.classList.toggle("sg-hide-left-sidebar", hide);
        try {
          localStorage.setItem(LS_LEFT_KEY, hide ? "1" : "0");
        } catch (e) {}
        setToggleVisualState();
      });
    }

    if (!rightBtn.dataset.bound) {
      rightBtn.dataset.bound = "1";
      rightBtn.addEventListener("click", () => {
        const hide = !document.body.classList.contains("sg-hide-right-sidebar");
        document.body.classList.toggle("sg-hide-right-sidebar", hide);
        try {
          localStorage.setItem(LS_RIGHT_KEY, hide ? "1" : "0");
        } catch (e) {}
        setToggleVisualState();
      });
    }

    try {
      const hideLeft = localStorage.getItem(LS_LEFT_KEY) === "1";
      const hideRight = localStorage.getItem(LS_RIGHT_KEY) === "1";
      document.body.classList.toggle("sg-hide-left-sidebar", hideLeft);
      document.body.classList.toggle("sg-hide-right-sidebar", hideRight);
    } catch (e) {}

    setToggleVisualState();
  }

  function isSiteDark() {
    return document.body?.getAttribute("data-md-color-scheme") === "slate";
  }

  function getIframeThemeStyle() {
    return `
      html[data-parent-theme="dark"] { color-scheme: dark; }
      html[data-parent-theme="dark"] body {
        background: #0b1020 !important;
        color: #e5e7eb !important;
      }
      html[data-parent-theme="dark"] .container,
      html[data-parent-theme="dark"] main,
      html[data-parent-theme="dark"] section,
      html[data-parent-theme="dark"] article,
      html[data-parent-theme="dark"] aside,
      html[data-parent-theme="dark"] nav,
      html[data-parent-theme="dark"] header,
      html[data-parent-theme="dark"] footer,
      html[data-parent-theme="dark"] .content,
      html[data-parent-theme="dark"] .card,
      html[data-parent-theme="dark"] .panel,
      html[data-parent-theme="dark"] .box,
      html[data-parent-theme="dark"] .wrapper {
        background: #111827 !important;
        color: #e5e7eb !important;
      }
      html[data-parent-theme="dark"] h1,
      html[data-parent-theme="dark"] h2,
      html[data-parent-theme="dark"] h3,
      html[data-parent-theme="dark"] h4,
      html[data-parent-theme="dark"] h5,
      html[data-parent-theme="dark"] h6,
      html[data-parent-theme="dark"] p,
      html[data-parent-theme="dark"] li,
      html[data-parent-theme="dark"] dt,
      html[data-parent-theme="dark"] dd,
      html[data-parent-theme="dark"] span,
      html[data-parent-theme="dark"] div,
      html[data-parent-theme="dark"] label {
        color: #e5e7eb !important;
      }
      html[data-parent-theme="dark"] a { color: #c4b5fd !important; }
      html[data-parent-theme="dark"] table {
        background: #0f172a !important;
        color: #e5e7eb !important;
      }
      html[data-parent-theme="dark"] th {
        background: #1f2937 !important;
        color: #f8fafc !important;
      }
      html[data-parent-theme="dark"] td {
        background: #111827 !important;
        color: #e5e7eb !important;
        border-color: #374151 !important;
      }
      html[data-parent-theme="dark"] pre,
      html[data-parent-theme="dark"] code,
      html[data-parent-theme="dark"] .formula {
        background: #111827 !important;
        color: #e5e7eb !important;
        border-color: #374151 !important;
      }
      html[data-parent-theme="dark"] input,
      html[data-parent-theme="dark"] textarea,
      html[data-parent-theme="dark"] select,
      html[data-parent-theme="dark"] button {
        background: #1f2937 !important;
        color: #f8fafc !important;
        border-color: #4b5563 !important;
      }
    `;
  }

  function applyThemeToIframe(iframe) {
    const dark = isSiteDark();
    try {
      const doc = iframe.contentDocument;
      if (!doc || !doc.documentElement) return;

      doc.documentElement.setAttribute("data-parent-theme", dark ? "dark" : "light");

      if (doc.body) {
        doc.body.classList.toggle("parent-dark", dark);
        doc.body.classList.toggle("parent-light", !dark);
      }

      let styleTag = doc.getElementById("parent-iframe-dark-theme");
      if (!styleTag) {
        styleTag = doc.createElement("style");
        styleTag.id = "parent-iframe-dark-theme";
        styleTag.textContent = getIframeThemeStyle();
        (doc.head || doc.documentElement).appendChild(styleTag);
      }
    } catch (e) {
      // ignore cross-origin or transient iframe loading errors
    }
  }

  function syncEmbeddedIframesTheme() {
    const iframes = document.querySelectorAll(".md-content iframe");
    if (!iframes.length) return;

    iframes.forEach((iframe) => {
      if (!iframe.dataset.themeBound) {
        iframe.dataset.themeBound = "1";
        iframe.addEventListener("load", () => applyThemeToIframe(iframe));
      }
      applyThemeToIframe(iframe);
    });

    if (syncEmbeddedIframesTheme.boundObserver) return;
    syncEmbeddedIframesTheme.boundObserver = true;

    const target = document.body;
    if (!target || typeof MutationObserver === "undefined") return;

    new MutationObserver(() => {
      document.querySelectorAll(".md-content iframe").forEach((iframe) => applyThemeToIframe(iframe));
    }).observe(target, {
      attributes: true,
      attributeFilter: ["data-md-color-scheme"]
    });
  }

  function initRevealMotion() {
    const selectors = [
      ".md-typeset .grid.cards > ul > li",
      ".home-hero__text",
      ".value-strip",
      ".md-typeset > h1"
    ];

    const nodes = document.querySelectorAll(selectors.join(","));
    if (!nodes.length) return;

    nodes.forEach((el) => el.classList.add("reveal"));

    const reduced = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
    if (reduced || typeof IntersectionObserver === "undefined") {
      nodes.forEach((el) => el.classList.add("is-visible"));
      return;
    }

    const io = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            entry.target.classList.add("is-visible");
            io.unobserve(entry.target);
          }
        });
      },
      { threshold: 0.16 }
    );

    nodes.forEach((el) => io.observe(el));
  }

  // Material instant navigation support
  if (typeof document$ !== "undefined" && document$.subscribe) {
    document$.subscribe(run);
  } else {
    document.addEventListener("DOMContentLoaded", run);
  }

  function translateTabs() {
    if (!isArabic()) return;

    const map = {
      "Home": "الرئيسية",
      "Start Here": "ابدأ من هنا",
      "Learn": "تعلّم",
      "Career": "المسار المهني",
      "Career Development": "المسار المهني",
      "Resources": "الموارد",
      "About": "حول"
    };

    document.querySelectorAll(".md-tabs__link").forEach((a) => {
      const t = a.textContent.trim();
      if (map[t]) a.textContent = map[t];
    });
  }

})();
