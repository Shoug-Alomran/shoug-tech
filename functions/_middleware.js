// Runs in front of the static files on Cloudflare Pages.
//
// 1. Pages redirects /page.html to /page and /dir/index.html to /dir/. The site's
//    canonical URLs and sitemap use .html for inner pages, so .html requests are
//    served directly instead of redirecting.
// 2. Old URLs from git history (workers/indexing/src/manifest.json) and meta-refresh
//    pages (generated at deploy by scripts/build_meta_redirects.py) get real 301s,
//    which search engines and AI fetchers follow.
// 3. PDFs that have a viewer page get a Link canonical header pointing at it.
// 4. Every HTML page gets the site analytics script (docs/javascripts/
//    site-analytics.js) and the admin header tab (admin-nav.js), so the
//    ~3,900 static pages need no edits. Admin pages get no analytics.
import manifest from "../workers/indexing/src/manifest.json";
import moved from "../.pages-build/meta-redirects.json";

// The CSP is deliberately narrow: pages rely on inline scripts and several
// CDNs, so it doesn't restrict script sources. It does block plugins, <base>
// hijacking, mixed content and framing by other sites (clickjacking).
// Other shoug-tech.com subdomains may still embed pages.
const HEADERS = {
  "X-Content-Type-Options": "nosniff",
  "Referrer-Policy": "strict-origin-when-cross-origin",
  "X-Frame-Options": "SAMEORIGIN",
  "Content-Security-Policy":
    "object-src 'none'; base-uri 'self'; frame-ancestors 'self' https://*.shoug-tech.com; upgrade-insecure-requests",
  // geolocation and fullscreen stay available to the site itself: an SE371
  // JavaScript example uses geolocation and the PDF viewers go fullscreen.
  "Permissions-Policy":
    "camera=(), microphone=(), payment=(), usb=(), serial=(), bluetooth=(), magnetometer=(), gyroscope=(), accelerometer=(), browsing-topics=(), geolocation=(self), fullscreen=(self)",
};

const ANALYTICS_TAG =
  '<script defer src="/javascripts/site-analytics.js?v=1"></script>';
// Theme: follow the device until the visitor picks one (docs/javascripts/
// site-theme.js explains the two storage keys). THEME_BOOT runs first in
// <head>, before any page script reads "shoug-theme". The first visit after
// this shipped ("shoug-theme-v2") resets saved themes once, because older
// scripts saved the theme on page load even when nobody had chosen one.
const THEME_BOOT = `<script>(function(){try{var s=localStorage,k="shoug-theme",a="shoug-theme-auto",v="shoug-theme-v2",m=window.matchMedia&&matchMedia("(prefers-color-scheme: light)").matches?"light":"dark",saved=s.getItem(k),auto=s.getItem(a);if(!s.getItem(v)){s.setItem(v,"1");saved=null;}if(!saved||saved===auto){s.setItem(k,m);s.setItem(a,m);}else if(auto!==null){s.removeItem(a);}}catch(e){}})();</script>`;
const THEME_TAG =
  '<script defer src="/javascripts/site-theme.js?v=1"></script>';
// The administrator's "Admin" header tab (docs/javascripts/admin-nav.js).
const ADMIN_NAV_TAG =
  '<script defer src="/javascripts/admin-nav.js?v=1"></script>';

// Microsoft Clarity (heatmaps and session replay). About 2,900 pages carry the
// snippet in their own <head>; the generated study pages (annotated slides,
// exams, breakdowns...) never did. Pages without it get it here, except where
// replay is deliberately off: admin, account, payment and paid-course pages.
// Masking for account and community pages is configured in Clarity itself.
const CLARITY_TAG = `<script type="text/javascript">(function(c,l,a,r,i,t,y){c[a]=c[a]||function(){(c[a].q=c[a].q||[]).push(arguments)};t=l.createElement(r);t.async=1;t.src="https://www.clarity.ms/tag/"+i;y=l.getElementsByTagName(r)[0];y.parentNode.insertBefore(t,y);})(window,document,"clarity","script","xub0eqmvs9");</script>`;
const NO_CLARITY =
  /^\/(?:admin|account|checkout|course-access|course-media)(?:\/|$)|^\/academics\/other-courses\/ethcs303(?:\/|$)/;

function withSiteScripts(response, path) {
  const type = response.headers.get("content-type") || "";
  if (!response.ok || !type.includes("text/html")) return response;
  const tags =
    THEME_TAG +
    (path.startsWith("/admin") ? ADMIN_NAV_TAG : ANALYTICS_TAG + ADMIN_NAV_TAG);
  const wantClarity = !NO_CLARITY.test(path);
  let hasClarity = false;
  return new HTMLRewriter()
    .on("head script", {
      text(chunk) {
        if (chunk.text.includes("clarity.ms/tag")) hasClarity = true;
      },
    })
    .on("head", {
      element(head) {
        head.prepend(THEME_BOOT, { html: true });
        head.append(tags, { html: true });
        // Decided at </head>, once every script in the head has been seen.
        if (wantClarity)
          head.onEndTag((end) => {
            if (!hasClarity) end.before(CLARITY_TAG, { html: true });
          });
      },
    })
    .transform(response);
}

// Old links may omit the trailing slash or name index.html directly.
function lookup(table, path) {
  return (
    table[path] ?? table[path + "/"] ?? table[path.replace(/index\.html$/, "")]
  );
}

export async function onRequest({ request, next, env }) {
  if (!["GET", "HEAD"].includes(request.method)) return next();
  const url = new URL(request.url);
  let path;
  try {
    path = decodeURIComponent(url.pathname);
  } catch {
    return next();
  }

  const target = lookup(manifest.redirects, path) ?? lookup(moved, path);
  if (target) {
    const destination = new URL(target, url.origin);
    if (!destination.search) destination.search = url.search;
    return Response.redirect(destination.href, 301);
  }

  let response;
  if (path.endsWith(".html") && !path.endsWith("/index.html")) {
    const clean = new URL(url);
    clean.pathname = url.pathname.slice(0, -".html".length);
    const asset = await env.ASSETS.fetch(new Request(clean, request));
    if (asset.status === 200) response = asset;
  }
  if (!response) response = await next();
  response = new Response(response.body, response);
  if (response.ok && manifest.canonicals[path]) {
    response.headers.set(
      "Link",
      `<${manifest.canonicals[path]}>; rel="canonical"`,
    );
  }
  for (const [name, value] of Object.entries(HEADERS)) {
    if (!response.headers.has(name)) response.headers.set(name, value);
  }
  return request.method === "GET" ? withSiteScripts(response, path) : response;
}
