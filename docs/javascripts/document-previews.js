(function () {
  "use strict";

  if (window.__shougDocumentPreviews) return;
  window.__shougDocumentPreviews = true;
  var isPreview = new URLSearchParams(window.location.search).get("preview") === "1";

  var css = document.createElement("style");
  css.id = "shoug-document-preview-styles";
  css.textContent =
    ".deck-preview .deck-thumb.document-preview{position:relative!important;display:block!important;overflow:hidden!important;background-image:none!important;padding:0!important}" +
    ".deck-preview .doc-preview-frame{position:absolute!important;inset:0!important;display:block!important;width:100%!important;height:100%!important;min-width:0!important;min-height:0!important;border:0!important;margin:0!important;transform:none!important;pointer-events:none!important;background:transparent}" +
    "html[data-document-preview='1'],html[data-document-preview='1'] body{height:100%!important;min-height:0!important;overflow:hidden!important}";
  (document.head || document.documentElement).appendChild(css);
  if (isPreview) {
    document.documentElement.setAttribute("data-document-preview", "1");
    document.addEventListener("DOMContentLoaded", function () {
      document.querySelectorAll("iframe").forEach(function (frame) {
        frame.loading = "eager";
        frame.setAttribute("scrolling", "no");
      });
    }, { once: true });
  }

  function previewUrl(anchor) {
    var url;
    try {
      url = new URL(anchor.getAttribute("href"), document.baseURI);
    } catch (error) {
      return null;
    }
    if (url.origin !== window.location.origin) return null;
    if (url.hash) return null;

    if (url.pathname.endsWith("/")) {
      url.pathname += "index.html";
    } else if (/\.(?:html?|pdf|png|jpe?g|gif|svg)$/i.test(url.pathname)) {
      // These formats render in the browser's document or image viewer.
    } else if (/\.[a-z\d]{1,8}$/i.test(url.pathname)) {
      // Office and other binary files need a dedicated viewer, not a broken iframe.
      return null;
    } else {
      url.pathname += "/index.html";
    }
    var pagePath = function (path) {
      return path.replace(/index\.html$/i, "");
    };
    if (pagePath(url.pathname) === pagePath(window.location.pathname)) return null;
    url.searchParams.set("preview", "1");
    return url.href;
  }

  function addPreviews() {
    document
      .querySelectorAll(".slide-gallery-grid .deck-preview[href]")
      .forEach(function (anchor) {
        if (anchor.classList.contains("is-soon")) return;
        var thumb = anchor.querySelector(".deck-thumb");
        if (!thumb) return;

        var existingFrame = thumb.querySelector("iframe");
        if (existingFrame) {
          try {
            var existingUrl = new URL(existingFrame.src, document.baseURI);
            existingUrl.searchParams.set("preview", "1");
            existingFrame.src = existingUrl.href;
            existingFrame.setAttribute("scrolling", "no");
            thumb.classList.add("document-preview");
          } catch (error) {}
          return;
        }

        var src = previewUrl(anchor);
        if (!src) return;

        var titleNode = anchor.querySelector(".deck-name");
        var title = titleNode ? titleNode.textContent.trim() : "course document";
        var frame = document.createElement("iframe");
        frame.className = "doc-preview-frame";
        frame.src = src;
        frame.title = "Preview of " + title;
        frame.setAttribute("aria-hidden", "true");
        frame.tabIndex = -1;
        frame.loading = "lazy";
        frame.setAttribute("scrolling", "no");
        frame.addEventListener("load", function () {
          try {
            var doc = frame.contentDocument;
            if (!doc) return;
            var embedded = doc.querySelector(
              ".embed-container iframe, iframe.legacy-html-frame, iframe.embed-frame",
            );
            if (embedded && embedded.src && !frame.dataset.documentResolved) {
              embedded.loading = "eager";
              var direct = new URL(embedded.src, frame.src);
              if (direct.origin === window.location.origin) {
                direct.searchParams.set("preview", "1");
                frame.dataset.documentResolved = "1";
                frame.src = direct.href;
                return;
              }
            }

            if (!doc.getElementById("document-preview-crop")) {
              var crop = doc.createElement("style");
              crop.id = "document-preview-crop";
              crop.textContent =
                "html,body{margin:0!important;padding:0!important;min-height:0!important;height:100%!important;overflow:hidden!important}" +
                ".shoug-site-header,.academic-sidebar,.content-topbar,.content-header,.content-tabs,.shoug-site-footer,.ask-ai-button{display:none!important}" +
                "body:has(.app-layout){padding-top:0!important;display:block!important;height:auto!important;overflow:hidden!important}" +
                ".app-layout{display:block!important;height:auto!important;min-height:0!important;padding:0!important;overflow:hidden!important}" +
                ".sys-main{display:block!important;min-height:0!important;height:auto!important;overflow:hidden!important}" +
                ".directory-container.slide-hub{padding:8px!important}.slide-gallery{margin:0!important}.slide-gallery-grid{grid-template-columns:repeat(2,minmax(0,1fr))!important;gap:8px!important}" +
                ".deck-name{margin-top:4px!important;font-size:12px!important;line-height:1.2!important}.deck-kind{margin-top:4px!important}";
              (doc.head || doc.documentElement).appendChild(crop);
            }
          } catch (error) {
            // Cross-origin viewers and native PDF frames remain on their wrapper.
          }
        });
        frame.addEventListener("error", function () {
          thumb.classList.remove("document-preview");
          frame.remove();
        }, { once: true });
        thumb.classList.add("document-preview");
        thumb.appendChild(frame);
      });
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", addPreviews, { once: true });
  } else {
    addPreviews();
  }
})();
