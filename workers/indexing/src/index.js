import manifest from './manifest.json' with { type: 'json' };

const ORIGIN = 'https://shoug-tech.com';
const osRoutes = new Set([
  '/project-overview/repo-structure', '/project-overview/team',
  '/phase-2/plan', '/phase-2/report', '/phase-2/results', '/phase-1/report',
]);
const dbLegacy = ['/Phase 3/report.pdf', '/Phase-0/Project plan.html'];

export async function handle(request, fetchOrigin = fetch) {
  const url = new URL(request.url);
  if (!['GET', 'HEAD'].includes(request.method)) return fetchOrigin(request);
  let path;
  try { path = decodeURIComponent(url.pathname); }
  catch { return fetchOrigin(request); }
  const main = ['shoug-tech.com', 'www.shoug-tech.com'].includes(url.hostname);
  let target;
  if (main) target = manifest.redirects[path];
  if (url.hostname === 'operating-systems.shoug-tech.com' && path.endsWith('.md') && osRoutes.has(path.slice(0, -3))) {
    target = path.slice(0, -3) + '/';
  }
  if (url.hostname === 'database.shoug-tech.com' && path === '/Phase 3/report.pdf') target = '/phase-3/report/';
  if (target || (main && (url.protocol !== 'https:' || url.hostname.startsWith('www.')))) {
    const destination = new URL(target || url.pathname, main ? ORIGIN : url.origin);
    destination.protocol = 'https:';
    destination.search = url.search;
    return Response.redirect(destination.href, 301);
  }

  let response = await fetchOrigin(request);
  if (!response.ok) return response;
  if (main && manifest.canonicals[path]) {
    response = new Response(response.body, response);
    response.headers.set('Link', `<${manifest.canonicals[path]}>; rel="canonical"`);
  }
  if (path === '/robots.txt' && ['operating-systems.shoug-tech.com', 'database.shoug-tech.com'].includes(url.hostname)) {
    // Narrow Allow exceptions let Google discover redirects/404s while preserving
    // search and other source-file exclusions. These origins use a single * group.
    const allows = url.hostname.startsWith('operating-systems.')
      ? [...osRoutes].map(route => route + '.md') : dbLegacy;
    const text = await response.text();
    const additions = allows.flatMap(route => [...new Set([route, encodeURI(route)])])
      .map(route => `Allow: ${route}$`).join('\n');
    response = new Response(text.replace(/(User-agent:\s*\*[^\r\n]*\r?\n)/i, `$1${additions}\n`), response);
    response.headers.delete('content-length');
    response.headers.delete('etag');
  }
  if (url.hostname === 'lilly-kitchen.shoug-tech.com' && /^\/(en|ar)\/?$/.test(path) && response.headers.get('content-type')?.includes('text/html')) {
    const lang = path.split('/')[1];
    const base = 'https://lilly-kitchen.shoug-tech.com';
    response = new HTMLRewriter()
      .on('link[rel="canonical"], link[rel="alternate"][hreflang]', { element(el) { el.remove(); } })
      .on('head', { element(el) {
        el.append(`<link rel="canonical" href="${base}/${lang}"><link rel="alternate" hreflang="en" href="${base}/en"><link rel="alternate" hreflang="ar" href="${base}/ar">`, { html: true });
      } }).transform(response);
  }
  return response;
}

export default { fetch(request) { return handle(request); } };
