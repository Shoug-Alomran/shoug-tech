(function () {
  const EMAIL = "inquiry@shoug-tech.com";

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
    if (headerInner.querySelector("a.header-cta")) return;

    const cta = document.createElement("a");
    cta.className = "header-cta";
    cta.href = `mailto:${EMAIL}`;
    cta.textContent = isArabic() ? "تواصل" : "Contact";
    cta.setAttribute("aria-label", cta.textContent);

    headerInner.appendChild(cta);
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
        };

    // ✅ FIXED: Academics points to Academics/Intro.md => usually /Academics/intro/
    const homeHref = isArabic() ? url("ar/") : url("");
    const academicsHref = isArabic() ? url("ar/Academics/intro/") : url("Academics/intro/");
    const careerHref = isArabic()
      ? url("ar/Career%20Development/me/")
      : url("Career%20Development/me/");
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
