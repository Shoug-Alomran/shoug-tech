/**
 * Service worker for shoug-tech.com.
 *
 * The site is read in classrooms and on patchy phone data, so the goal is that
 * a page you have already opened keeps working offline, and that repeat visits
 * do not re-download the shell.
 *
 * Strategy per resource type:
 *   HTML          network-first, falling back to cache, then /offline.html
 *   CSS/JS/icons  stale-while-revalidate -- instant, refreshed in background
 *   search index  stale-while-revalidate, so search works offline
 *   PDFs          never cached; they are large and the browser handles them
 *
 * Bump CACHE_VERSION to invalidate everything after a deploy.
 */
const CACHE_VERSION = 'v1';
const SHELL_CACHE = `shoug-shell-${CACHE_VERSION}`;
const PAGE_CACHE = `shoug-pages-${CACHE_VERSION}`;
const ASSET_CACHE = `shoug-assets-${CACHE_VERSION}`;

const OFFLINE_URL = '/offline.html';

/* Kept small on purpose: precaching the whole site would mean thousands of
   requests on first visit. Everything else is cached as it is visited. */
const PRECACHE = [
    OFFLINE_URL,
    '/styles/a11y.css',
    '/assets/icon-192.png',
];

const MAX_PAGES = 60;

self.addEventListener('install', (event) => {
    event.waitUntil(
        caches.open(SHELL_CACHE)
            .then((cache) => cache.addAll(PRECACHE))
            .then(() => self.skipWaiting())
            // A failed precache must not block activation; the fetch handler
            // degrades to plain network without it.
            .catch(() => self.skipWaiting())
    );
});

self.addEventListener('activate', (event) => {
    const keep = new Set([SHELL_CACHE, PAGE_CACHE, ASSET_CACHE]);
    event.waitUntil(
        caches.keys()
            .then((names) => Promise.all(
                names.map((n) => (keep.has(n) ? null : caches.delete(n)))
            ))
            .then(() => self.clients.claim())
    );
});

/* The page cache is unbounded otherwise; a term of browsing a course tree can
   run to hundreds of entries. Oldest-first is a good enough proxy for LRU. */
async function trimCache(name, max) {
    const cache = await caches.open(name);
    const keys = await cache.keys();
    if (keys.length <= max) return;
    await Promise.all(keys.slice(0, keys.length - max).map((k) => cache.delete(k)));
}

function isHTML(request) {
    return request.mode === 'navigate'
        || (request.headers.get('accept') || '').includes('text/html');
}

function isCacheableAsset(url) {
    return /\.(css|js|png|jpg|jpeg|svg|gif|webp|woff2?|ico|json)$/i.test(url.pathname);
}

async function networkFirst(request) {
    try {
        const response = await fetch(request);
        if (response && response.ok) {
            const cache = await caches.open(PAGE_CACHE);
            cache.put(request, response.clone());
            trimCache(PAGE_CACHE, MAX_PAGES);
        }
        return response;
    } catch (error) {
        const cached = await caches.match(request);
        if (cached) return cached;
        const offline = await caches.match(OFFLINE_URL);
        if (offline) return offline;
        throw error;
    }
}

async function staleWhileRevalidate(request) {
    const cache = await caches.open(ASSET_CACHE);
    const cached = await cache.match(request);
    const network = fetch(request)
        .then((response) => {
            if (response && response.ok) cache.put(request, response.clone());
            return response;
        })
        .catch(() => cached);
    return cached || network;
}

self.addEventListener('fetch', (event) => {
    const { request } = event;
    if (request.method !== 'GET') return;

    const url = new URL(request.url);
    if (url.origin !== self.location.origin) return;

    // PDFs are the bulk of the site by bytes and would evict everything else.
    if (url.pathname.toLowerCase().endsWith('.pdf')) return;

    if (isHTML(request)) {
        event.respondWith(networkFirst(request));
        return;
    }

    if (isCacheableAsset(url)) {
        event.respondWith(staleWhileRevalidate(request));
    }
});

/* Lets a page trigger an immediate update instead of waiting for all tabs to
   close (see javascripts/register-sw.js). */
self.addEventListener('message', (event) => {
    if (event.data === 'skip-waiting') self.skipWaiting();
});
