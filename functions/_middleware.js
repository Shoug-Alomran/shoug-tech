// Runs in front of the static files on Cloudflare Pages.
//
// 1. Pages redirects /page.html to /page and /dir/index.html to /dir/. The site's
//    canonical URLs and sitemap use .html for inner pages, so .html requests are
//    served directly instead of redirecting.
// 2. Old URLs from git history (workers/indexing/src/manifest.json) and meta-refresh
//    pages (generated at deploy by scripts/build_meta_redirects.py) get real 301s,
//    which search engines and AI fetchers follow.
// 3. PDFs that have a viewer page get a Link canonical header pointing at it.
import manifest from "../workers/indexing/src/manifest.json";
import moved from "../.pages-build/meta-redirects.json";

const HEADERS = {
  "X-Content-Type-Options": "nosniff",
  "Referrer-Policy": "strict-origin-when-cross-origin",
};

// Old links may omit the trailing slash or name index.html directly.
function lookup(table, path) {
  return table[path] ?? table[path + "/"] ?? table[path.replace(/index\.html$/, "")];
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
    response.headers.set("Link", `<${manifest.canonicals[path]}>; rel="canonical"`);
  }
  for (const [name, value] of Object.entries(HEADERS)) {
    if (!response.headers.has(name)) response.headers.set(name, value);
  }
  return response;
}
