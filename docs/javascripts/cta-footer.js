(function () {
  const EMAIL = "inquiry@shoug-tech.com";
  const LINKEDIN = "https://www.linkedin.com/in/shoug-alomran";

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

  function addHeaderCTA() {
    const headerInner = document.querySelector(".md-header__inner");
    if (!headerInner) return;

    // Avoid duplicating on instant navigation
    if (headerInner.querySelector(".header-actions")) return;

    const wrap = document.createElement("div");
    wrap.className = "header-actions";

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

    // Contact button
    const cta = document.createElement("a");
    cta.className = "header-cta";
    cta.href = `mailto:${EMAIL}`;
    cta.textContent = isArabic() ? "تواصل" : "Contact";
    cta.setAttribute("aria-label", cta.textContent);

    wrap.appendChild(li);
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
        };

    // Navigation links
    const homeHref = isArabic() ? url("ar/") : url("");
    const academicsHref = isArabic() ? url("ar/Academics/intro/") : url("Academics/intro/");
    const careerHref = isArabic()
      ? url("ar/career-development/me/")
      : url("career-development/me/");
    const linksHref = isArabic() ? url("ar/links/") : url("links/");

    // Policies
    const privacyHref = isArabic() ? url("ar/privacy-notice/") : url("privacy-notice/");
    const disclaimerHref = isArabic() ? url("ar/academic-disclaimer/") : url("academic-disclaimer/");
    const copyrightHref = isArabic() ? url("ar/copyright/") : url("copyright/");

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
    addFooterBlock();
  }

  // Material instant navigation support
  if (typeof document$ !== "undefined" && document$.subscribe) {
    document$.subscribe(run);
  } else {
    document.addEventListener("DOMContentLoaded", run);
  }
})();