// Site analytics: the collector behind docs/javascripts/site-analytics.js and
// the read API behind docs/admin/analytics/.
//
// Privacy model
// - No cookies and no visitor or session IDs. The browser keeps a few local
//   flags (first visit date, last visit date, page count in the current
//   session) and sends only the derived yes/no and counts.
// - The IP address is used once, as the rate-limit key, and never written.
//   Country and city come from Cloudflare's own request metadata.
// - Search queries are recorded because they show what students look for;
//   nothing typed into any other field is ever read.
//
// Storage: Workers Analytics Engine dataset `site_events` (binding
// SITE_EVENTS), kept for three months. Column layout, shared by every event:
//
//   index1  event name
//   blob1   event name          blob11  browser language
//   blob2   path                blob12  site language (en / ar)
//   blob3   section             blob13  theme (dark|light / palette)
//   blob4   course code         blob14  signed in (1 / 0)
//   blob5   content kind        blob15  utm_source
//   blob6   referrer host       blob16  utm_medium / utm_campaign
//   blob7   country             blob17  label (event-specific)
//   blob8   device              blob18  detail (event-specific)
//   blob9   browser             blob19  page title
//   blob10  operating system    blob20  city
//
//   double1  value (event-specific)      double9   quiz questions answered
//   double2  engaged seconds             double10  quiz questions correct
//   double3  max scroll %                double11  Riyadh date as yyyymmdd
//   double4  viewport width              double12  Riyadh hour 0-23
//   double5  first visit ever (1/0)      double13  Riyadh weekday 0=Sun
//   double6  first visit today (1/0)     double14  days since previous visit
//   double7  page number in session      double15  scroll was measured (1/0)
//   double8  page load ms
//
// Every count in a query must be SUM(_sample_interval): Analytics Engine
// samples at high volume and records how many events each row stands for.

export const DATASET = "site_events";
const MAX_EVENTS = 40;
const MAX_BODY = 32 * 1024;
const RIYADH_OFFSET_MS = 3 * 60 * 60 * 1000;

export const EVENTS = new Set([
  "pageview",
  "engage",
  "click",
  "rage",
  "search",
  "quiz",
  "vital",
  "error",
  "pref",
  "copy",
  "print",
]);

const SITE_HOSTS = new Set(["shoug-tech.com", "www.shoug-tech.com"]);
const BOT =
  /bot|crawl|spider|slurp|archiver|headless|lighthouse|pagespeed|gtmetrix|pingdom|uptime|monitor|preview|python|curl|wget|axios|node-fetch|go-http|java\/|okhttp|phantom|selenium|puppeteer|playwright|facebookexternalhit|embedly|quora link|whatsapp|telegrambot|discordbot|slackbot/i;

// Path segments that name a kind of study material, most specific first.
const KINDS = [
  "annotated-slides",
  "slide-breakdowns",
  "chapter-summaries",
  "past-papers",
  "mock-exam",
  "exams",
  "mindmaps",
  "cheat-sheets",
  "notebooks",
  "study-pack",
  "study-guide",
  "flashcards",
  "labs",
  "assignments",
  "extra-resources",
];

function text(value, max) {
  if (value === undefined || value === null) return "";
  return String(value)
    .replace(/[\u0000-\u001f\u007f]+/g, " ")
    .replace(/\s+/g, " ")
    .trim()
    .slice(0, max);
}

function num(value, min, max) {
  const n = Number(value);
  if (!Number.isFinite(n)) return 0;
  return Math.min(max, Math.max(min, n));
}

export function cleanPath(value) {
  let path = text(value, 400).split(/[?#]/)[0] || "/";
  try {
    path = decodeURIComponent(path);
  } catch {}
  if (!path.startsWith("/")) path = "/" + path;
  path = path.replace(/\/index\.html$/i, "/").replace(/\/{2,}/g, "/");
  return path.slice(0, 300);
}

/** Section, course code and content kind, derived from the path alone. */
export function classify(path) {
  const parts = path.split("/").filter(Boolean);
  const section = parts.length ? parts[0].toLowerCase().slice(0, 40) : "home";
  const course =
    parts.map((p) => p.toLowerCase()).find((p) => /^[a-z]{2,4}\d{3}$/.test(p)) ||
    "";
  let kind = "";
  for (const k of KINDS) {
    if (parts.includes(k)) {
      kind = k;
      break;
    }
  }
  if (!kind) {
    if (!parts.length) kind = "home";
    else if (course && parts[parts.length - 1] === course) kind = "course-home";
    else if (course) kind = "course-page";
    else kind = parts.length === 1 ? "section-home" : "page";
  }
  return { section, course, kind };
}

export function parseAgent(ua, touchPoints = 0) {
  const s = String(ua || "");
  let os = "Other";
  if (/Windows/i.test(s)) os = "Windows";
  else if (/iPhone|iPod/i.test(s)) os = "iOS";
  else if (/iPad/i.test(s)) os = "iPadOS";
  else if (/Android/i.test(s)) os = "Android";
  else if (/CrOS/i.test(s)) os = "ChromeOS";
  else if (/Mac OS X|Macintosh/i.test(s)) os = touchPoints > 1 ? "iPadOS" : "macOS";
  else if (/Linux/i.test(s)) os = "Linux";

  let device = "desktop";
  if (os === "iPadOS" || /Tablet|PlayBook|Silk/i.test(s) || (os === "Android" && !/Mobile/i.test(s)))
    device = "tablet";
  else if (/Mobi|iPhone|iPod|Android/i.test(s)) device = "mobile";

  let browser = "Other";
  if (/Edg(e|A|iOS)?\//.test(s)) browser = "Edge";
  else if (/OPR\/|Opera/.test(s)) browser = "Opera";
  else if (/SamsungBrowser/.test(s)) browser = "Samsung Internet";
  else if (/Firefox|FxiOS/.test(s)) browser = "Firefox";
  else if (/CriOS|Chrome\//.test(s)) browser = "Chrome";
  else if (/Safari\//.test(s)) browser = "Safari";

  return { os, device, browser, bot: BOT.test(s) };
}

export function referrerHost(value) {
  const raw = text(value, 500);
  if (!raw) return "";
  try {
    const url = new URL(raw);
    if (url.protocol === "android-app:") return url.hostname.slice(0, 80);
    const host = url.hostname.replace(/^www\./, "").toLowerCase();
    if (SITE_HOSTS.has(url.hostname) || SITE_HOSTS.has(host)) return "";
    return host.slice(0, 80);
  } catch {
    return "";
  }
}

export function riyadhClock(nowMs) {
  const d = new Date(nowMs + RIYADH_OFFSET_MS);
  return {
    day: d.getUTCFullYear() * 10000 + (d.getUTCMonth() + 1) * 100 + d.getUTCDate(),
    hour: d.getUTCHours(),
    weekday: d.getUTCDay(),
  };
}

/**
 * Turns one collector request body into Analytics Engine data points.
 * Returns [] for bots, foreign pages and malformed input.
 */
export function toDataPoints(body, meta, nowMs = Date.now()) {
  if (!body || typeof body !== "object" || !Array.isArray(body.e)) return [];
  const c = body.c && typeof body.c === "object" ? body.c : {};
  const agent = parseAgent(meta.userAgent, num(c.tp, 0, 20));
  if (agent.bot || c.wd) return [];

  const path = cleanPath(c.p);
  const { section, course, kind } = classify(path);
  const clock = riyadhClock(nowMs);
  const shared = {
    path,
    section,
    course,
    kind,
    ref: referrerHost(c.r),
    country: text(meta.country, 4),
    city: text(meta.city, 60),
    lang: text(c.bl, 12).toLowerCase(),
    siteLang: text(c.sl, 6).toLowerCase(),
    theme: text(c.th, 40),
    signed: c.si ? "1" : "0",
    utmSource: text(c.us, 60).toLowerCase(),
    utmRest: text([c.um, c.uc].filter(Boolean).join(" / "), 120).toLowerCase(),
    title: text(c.t, 160),
    vw: num(c.vw, 0, 10000),
    newEver: c.nv ? 1 : 0,
    newToday: c.nd ? 1 : 0,
    pageIndex: num(c.ix, 0, 10000),
    since: num(c.ds, -1, 10000),
  };

  const points = [];
  for (const raw of body.e.slice(0, MAX_EVENTS)) {
    if (!raw || typeof raw !== "object") continue;
    const name = text(raw.n, 20);
    if (!EVENTS.has(name)) continue;
    const isView = name === "pageview";
    const hasScroll = raw.sc !== undefined && raw.sc !== null && raw.sc >= 0;
    points.push({
      indexes: [name],
      blobs: [
        name,
        shared.path,
        shared.section,
        shared.course,
        shared.kind,
        isView ? shared.ref : "",
        shared.country,
        agent.device,
        agent.browser,
        agent.os,
        shared.lang,
        shared.siteLang,
        shared.theme,
        shared.signed,
        isView ? shared.utmSource : "",
        isView ? shared.utmRest : "",
        text(raw.l, name === "error" ? 240 : 200),
        text(raw.d, 120),
        isView ? shared.title : "",
        shared.city,
      ],
      doubles: [
        num(raw.v, -1e9, 1e9),
        num(raw.s, 0, 3600),
        hasScroll ? num(raw.sc, 0, 100) : 0,
        shared.vw,
        isView ? shared.newEver : 0,
        isView ? shared.newToday : 0,
        isView ? shared.pageIndex : 0,
        isView ? num(raw.ms, 0, 120000) : 0,
        num(raw.qa, 0, 1000),
        num(raw.qc, 0, 1000),
        clock.day,
        clock.hour,
        clock.weekday,
        isView ? shared.since : 0,
        hasScroll ? 1 : 0,
      ],
    });
  }
  return points;
}

export async function handleCollect(request, env, origin) {
  const headers = {
    "access-control-allow-origin": origin,
    vary: "Origin",
    "cache-control": "no-store",
  };
  const done = (status) => new Response(null, { status, headers });
  if (!env.SITE_EVENTS) return done(204);
  const ip = request.headers.get("cf-connecting-ip") || "";
  if (env.ANALYTICS_RATE_LIMIT && ip) {
    const { success } = await env.ANALYTICS_RATE_LIMIT.limit({ key: ip });
    if (!success) return done(429);
  }
  const raw = await request.text();
  if (raw.length > MAX_BODY) return done(413);
  let body;
  try {
    body = JSON.parse(raw);
  } catch {
    return done(400);
  }
  const cf = request.cf || {};
  const points = toDataPoints(body, {
    userAgent: request.headers.get("user-agent"),
    country: cf.country || request.headers.get("cf-ipcountry") || "",
    city: cf.city || "",
  });
  for (const point of points) {
    try {
      env.SITE_EVENTS.writeDataPoint(point);
    } catch (error) {
      console.error("analytics write failed", error);
      break;
    }
  }
  return done(204);
}

// ---------------------------------------------------------------- reports --

const RANGES = { "1": 1, "7": 7, "30": 30, "90": 90 };
const C = "SUM(_sample_interval)";

// Analytics Engine documents no escape for quotes inside string literals, so
// cleanFilters admits no quote or backslash at all and this only wraps.
function quote(value) {
  const s = String(value);
  if (/['\\]/.test(s)) throw new Error("unsafe filter value");
  return "'" + s + "'";
}

/** Validates dashboard filters; anything unexpected is dropped, never passed to SQL. */
export function cleanFilters(input) {
  const f = input && typeof input === "object" ? input : {};
  const out = {};
  if (typeof f.course === "string" && /^[a-z]{2,4}\d{3}$/.test(f.course)) out.course = f.course;
  if (typeof f.section === "string" && /^[a-z0-9-]{1,40}$/.test(f.section)) out.section = f.section;
  if (typeof f.kind === "string" && /^[a-z0-9-]{1,40}$/.test(f.kind)) out.kind = f.kind;
  if (typeof f.country === "string" && /^[A-Z0-9]{2}$/.test(f.country)) out.country = f.country;
  if (typeof f.device === "string" && /^(desktop|mobile|tablet)$/.test(f.device)) out.device = f.device;
  if (typeof f.path === "string" && /^\/[^'\\\u0000-\u001f]{0,299}$/.test(f.path)) out.path = f.path;
  return out;
}

function windowClause(days, previous) {
  if (previous)
    return `timestamp <= NOW() - INTERVAL '${days}' DAY AND timestamp > NOW() - INTERVAL '${days * 2}' DAY`;
  return `timestamp > NOW() - INTERVAL '${days}' DAY`;
}

function filterClause(f) {
  const parts = [];
  if (f.course) parts.push(`blob4 = ${quote(f.course)}`);
  if (f.section) parts.push(`blob3 = ${quote(f.section)}`);
  if (f.kind) parts.push(`blob5 = ${quote(f.kind)}`);
  if (f.country) parts.push(`blob7 = ${quote(f.country)}`);
  if (f.device) parts.push(`blob8 = ${quote(f.device)}`);
  if (f.path) parts.push(`blob2 = ${quote(f.path)}`);
  return parts.length ? " AND " + parts.join(" AND ") : "";
}

/**
 * Every report the dashboard shows, as named SQL statements. Only the range
 * and the validated filters vary; there is no way to send SQL from outside.
 */
export function buildQueries(rangeKey, filters) {
  const days = RANGES[rangeKey] || 7;
  const f = cleanFilters(filters);
  const scope = filterClause(f);
  const where = (event, extra = "") =>
    `WHERE ${windowClause(days)} AND blob1 = '${event}'${scope}${extra}`;
  const from = `FROM ${DATASET}`;
  const top = (dim, event, extra = "", limit = 25) =>
    `SELECT ${dim} AS k, ${C} AS n ${from} ${where(event, extra)} GROUP BY k ORDER BY n DESC LIMIT ${limit}`;

  const totals = (previous) =>
    `SELECT
      SUM(if(blob1 = 'pageview', _sample_interval, 0)) AS pageviews,
      SUM(if(blob1 = 'pageview', _sample_interval * double6, 0.0)) AS visitors,
      SUM(if(blob1 = 'pageview', _sample_interval * double5, 0.0)) AS new_visitors,
      SUM(if(blob1 = 'pageview' AND double7 = 1, _sample_interval, 0)) AS sessions,
      SUM(if(blob1 = 'pageview' AND double7 = 2, _sample_interval, 0)) AS sessions_2plus,
      SUM(if(blob1 = 'engage', _sample_interval * double2, 0.0)) AS engaged_seconds,
      SUM(if(blob1 = 'engage', _sample_interval * double3, 0.0)) AS scroll_sum,
      SUM(if(blob1 = 'engage', _sample_interval * double15, 0.0)) AS scroll_n,
      SUM(if(blob1 = 'search', _sample_interval, 0)) AS searches,
      SUM(if(blob1 = 'quiz', _sample_interval, 0)) AS quiz_submits,
      SUM(if(blob1 = 'engage', _sample_interval * double9, 0.0)) AS quiz_answered,
      SUM(if(blob1 = 'engage', _sample_interval * double10, 0.0)) AS quiz_correct,
      SUM(if(blob1 = 'error', _sample_interval, 0)) AS errors,
      SUM(if(blob1 = 'pageview' AND blob18 = '404', _sample_interval, 0)) AS not_found
    ${from} WHERE ${windowClause(days, previous)}${scope}`;

  const queries = {
    totals: totals(false),
    series: `SELECT double11 AS day,
        SUM(if(blob1 = 'pageview', _sample_interval, 0)) AS pageviews,
        SUM(if(blob1 = 'pageview', _sample_interval * double6, 0.0)) AS visitors,
        SUM(if(blob1 = 'pageview' AND double7 = 1, _sample_interval, 0)) AS sessions
      ${from} WHERE ${windowClause(days)}${scope}
      GROUP BY day ORDER BY day`,
    heat: `SELECT double13 AS weekday, double12 AS hour, ${C} AS n ${from} ${where("pageview")}
      GROUP BY weekday, hour`,
    pages: `SELECT blob2 AS k, ${C} AS n, SUM(_sample_interval * double6) AS visitors
      ${from} ${where("pageview")} GROUP BY k ORDER BY n DESC LIMIT 50`,
    titles: `SELECT blob2 AS k, blob19 AS title, ${C} AS n ${from} ${where("pageview", " AND blob19 != ''")}
      GROUP BY k, title ORDER BY n DESC LIMIT 200`,
    pageEngage: `SELECT blob2 AS k,
        SUM(_sample_interval * double2) AS seconds,
        SUM(_sample_interval * double3) AS scroll_sum,
        SUM(_sample_interval * double15) AS scroll_n
      ${from} ${where("engage")} GROUP BY k ORDER BY seconds DESC LIMIT 200`,
    entries: top("blob2", "pageview", " AND double7 = 1"),
    flows: `SELECT blob17 AS source, blob2 AS target, ${C} AS n ${from}
      ${where("pageview", " AND blob17 != '' AND blob18 != '404'")}
      GROUP BY source, target ORDER BY n DESC LIMIT 30`,
    referrers: top("blob6", "pageview", " AND blob6 != ''"),
    utm: `SELECT blob15 AS k, blob16 AS rest, ${C} AS n ${from} ${where("pageview", " AND blob15 != ''")}
      GROUP BY k, rest ORDER BY n DESC LIMIT 25`,
    countries: top("blob7", "pageview", " AND blob7 != ''", 40),
    cities: `SELECT blob20 AS k, blob7 AS country, ${C} AS n ${from} ${where("pageview", " AND blob20 != ''")}
      GROUP BY k, country ORDER BY n DESC LIMIT 25`,
    devices: top("blob8", "pageview"),
    browsers: top("blob9", "pageview"),
    os: top("blob10", "pageview"),
    languages: top("blob11", "pageview", " AND blob11 != ''", 15),
    siteLanguage: top("blob12", "pageview"),
    themes: top("blob13", "pageview", "", 15),
    signedIn: top("blob14", "pageview"),
    viewports: `SELECT if(double4 < 600, 'under 600px', if(double4 < 1024, '600-1023px', if(double4 < 1440, '1024-1439px', '1440px+'))) AS k,
        ${C} AS n ${from} ${where("pageview")} GROUP BY k ORDER BY n DESC`,
    returning: `SELECT if(double14 < 0, 'first visit', if(double14 < 1, 'same day', if(double14 < 2, '1 day', if(double14 < 8, '2-7 days', if(double14 < 31, '8-30 days', '31+ days'))))) AS k,
        ${C} AS n ${from} ${where("pageview", " AND double6 = 1")} GROUP BY k ORDER BY n DESC`,
    sections: top("blob3", "pageview"),
    courses: `SELECT blob4 AS k, ${C} AS n, SUM(_sample_interval * double6) AS visitors ${from}
      ${where("pageview", " AND blob4 != ''")} GROUP BY k ORDER BY n DESC LIMIT 60`,
    kinds: top("blob5", "pageview"),
    searches: `SELECT blob17 AS k, ${C} AS n, AVG(double1) AS results ${from}
      ${where("search", " AND blob17 != ''")} GROUP BY k ORDER BY n DESC LIMIT 40`,
    zeroSearches: top("blob17", "search", " AND double1 = 0", 30),
    outbound: top("blob17", "click", " AND blob18 = 'outbound'", 30),
    downloads: top("blob17", "click", " AND blob18 = 'download'", 30),
    contact: top("blob17", "click", " AND blob18 = 'contact'", 15),
    buttons: `SELECT blob17 AS k, blob5 AS kind, ${C} AS n ${from}
      ${where("click", " AND blob18 = 'button'")} GROUP BY k, kind ORDER BY n DESC LIMIT 40`,
    rage: `SELECT blob17 AS k, blob2 AS path, ${C} AS n ${from} ${where("rage")}
      GROUP BY k, path ORDER BY n DESC LIMIT 20`,
    quizzes: `SELECT blob2 AS k,
        SUM(_sample_interval * double9) AS answered,
        SUM(_sample_interval * double10) AS correct
      ${from} ${where("engage", " AND double9 > 0")} GROUP BY k ORDER BY answered DESC LIMIT 40`,
    quizSubmits: `SELECT blob2 AS k, ${C} AS n, AVG(double1) AS avg_score ${from} ${where("quiz")}
      GROUP BY k ORDER BY n DESC LIMIT 40`,
    vitals: `SELECT blob17 AS k,
        quantileExactWeighted(0.75)(double1, _sample_interval) AS p75,
        SUM(if(blob18 = 'good', _sample_interval, 0)) AS good,
        SUM(if(blob18 = 'needs-improvement', _sample_interval, 0)) AS ni,
        SUM(if(blob18 = 'poor', _sample_interval, 0)) AS poor
      ${from} ${where("vital")} GROUP BY k`,
    vitalsByDevice: `SELECT blob17 AS k, blob8 AS device,
        quantileExactWeighted(0.75)(double1, _sample_interval) AS p75, ${C} AS n
      ${from} ${where("vital")} GROUP BY k, device`,
    slowPages: `SELECT blob2 AS k, quantileExactWeighted(0.75)(double1, _sample_interval) AS p75, ${C} AS n
      ${from} ${where("vital", " AND blob17 = 'LCP'")} GROUP BY k HAVING n >= 3 ORDER BY p75 DESC LIMIT 20`,
    loadTime: `SELECT quantileExactWeighted(0.5)(double8, _sample_interval) AS p50,
        quantileExactWeighted(0.75)(double8, _sample_interval) AS p75,
        quantileExactWeighted(0.95)(double8, _sample_interval) AS p95
      ${from} ${where("pageview", " AND double8 > 0")}`,
    errors: `SELECT blob17 AS k, blob18 AS source, ${C} AS n ${from} ${where("error")}
      GROUP BY k, source ORDER BY n DESC LIMIT 30`,
    errorPages: top("blob2", "error", "", 20),
    notFound: `SELECT blob2 AS k, blob17 AS source, ${C} AS n ${from} ${where("pageview", " AND blob18 = '404'")}
      GROUP BY k, source ORDER BY n DESC LIMIT 30`,
    prefs: `SELECT blob17 AS k, blob18 AS value, ${C} AS n ${from} ${where("pref")}
      GROUP BY k, value ORDER BY n DESC LIMIT 30`,
    copies: top("blob2", "copy", "", 20),
    prints: top("blob2", "print", "", 20),
    pwa: top("blob18", "pageview", " AND blob18 IN ('standalone', 'offline')", 5),
    live: `SELECT blob2 AS k, ${C} AS n ${from}
      WHERE timestamp > NOW() - INTERVAL '30' MINUTE AND blob1 = 'pageview'${scope}
      GROUP BY k ORDER BY n DESC LIMIT 10`,
  };
  if (days < 90) queries.previous = totals(true);
  return { days, filters: f, queries };
}

async function runSql(env, sql, fetcher) {
  const response = await fetcher(
    `https://api.cloudflare.com/client/v4/accounts/${env.CF_ACCOUNT_ID}/analytics_engine/sql`,
    {
      method: "POST",
      headers: { authorization: `Bearer ${env.CF_ANALYTICS_TOKEN}` },
      body: sql.replace(/\s+/g, " ").trim() + " FORMAT JSON",
    },
  );
  const body = await response.text();
  if (!response.ok) throw new Error(body.slice(0, 300) || `HTTP ${response.status}`);
  const parsed = JSON.parse(body);
  return parsed.data || [];
}

/** True when the token belongs to the account named in courseCommerce/ethics.adminUid. */
export async function isAdmin(token, identity, fetcher = fetch, project = "shoug-tech") {
  if (!identity?.uid || !identity.emailVerified) return false;
  const response = await fetcher(
    `https://firestore.googleapis.com/v1/projects/${project}/databases/(default)/documents/courseCommerce/ethics?mask.fieldPaths=adminUid`,
    { headers: { authorization: `Bearer ${token}` } },
  );
  if (!response.ok) return false;
  const doc = await response.json();
  return doc?.fields?.adminUid?.stringValue === identity.uid;
}

export async function handleAnalyticsQuery(request, env, origin, json, verify, fetcher = fetch) {
  const match = (request.headers.get("authorization") || "").match(/^Bearer\s+(.+)$/i);
  if (!match) return json({ error: "Sign in as the site administrator." }, 401, origin);
  const identity = await verify(match[1]);
  if (!identity) return json({ error: "Your sign-in has expired. Reload the page." }, 401, origin);
  if (!(await isAdmin(match[1], identity, fetcher)))
    return json({ error: "This account is not the site administrator." }, 403, origin);
  if (!env.CF_ACCOUNT_ID || !env.CF_ANALYTICS_TOKEN)
    return json(
      {
        error:
          "Analytics reading is not configured: set the CF_ACCOUNT_ID and CF_ANALYTICS_TOKEN worker secrets.",
      },
      503,
      origin,
    );
  let input = {};
  try {
    input = await request.json();
  } catch {}
  const { days, filters, queries } = buildQueries(String(input.range || "7"), input.filters);
  const names = Object.keys(queries);
  const settled = await Promise.allSettled(names.map((n) => runSql(env, queries[n], fetcher)));
  const data = {};
  const errors = {};
  settled.forEach((result, i) => {
    if (result.status === "fulfilled") data[names[i]] = result.value;
    else errors[names[i]] = String(result.reason?.message || result.reason).slice(0, 300);
  });
  return json({ days, filters, generatedAt: new Date().toISOString(), data, errors }, 200, origin);
}
