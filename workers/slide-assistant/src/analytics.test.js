import { test } from "node:test";
import assert from "node:assert/strict";
import {
  classify,
  cleanPath,
  parseAgent,
  referrerHost,
  riyadhClock,
  toDataPoints,
  cleanFilters,
  buildQueries,
  handleCollect,
  handleAnalyticsQuery,
  isAdmin,
} from "./analytics.js";

const CHROME_WIN =
  "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0 Safari/537.36";
const IPHONE =
  "Mozilla/5.0 (iPhone; CPU iPhone OS 18_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.0 Mobile/15E148 Safari/604.1";

test("classify derives section, course and kind from the path", () => {
  assert.deepEqual(classify("/"), {
    section: "home",
    course: "",
    kind: "home",
  });
  assert.deepEqual(
    classify(
      "/academics/software-engineering/se322/exams/12-midterm-261/midterm-261.html",
    ),
    { section: "academics", course: "se322", kind: "exams" },
  );
  assert.deepEqual(classify("/academics/software-engineering/se322/"), {
    section: "academics",
    course: "se322",
    kind: "course-home",
  });
  assert.equal(
    classify("/academics/cybersecurity/cys403/annotated-slides/03-x/x.html")
      .kind,
    "annotated-slides",
  );
  assert.deepEqual(classify("/work/"), {
    section: "work",
    course: "",
    kind: "section-home",
  });
});

test("cleanPath strips queries, decodes and normalizes index.html", () => {
  assert.equal(cleanPath("/a/index.html?x=1#y"), "/a/");
  assert.equal(cleanPath("a//b"), "/a/b");
  assert.equal(cleanPath("/%D8%B4"), "/ش");
  assert.equal(cleanPath(undefined), "/");
});

test("parseAgent identifies device, browser, OS and bots", () => {
  assert.deepEqual(parseAgent(CHROME_WIN), {
    os: "Windows",
    device: "desktop",
    browser: "Chrome",
    bot: false,
  });
  const phone = parseAgent(IPHONE);
  assert.equal(phone.device, "mobile");
  assert.equal(phone.os, "iOS");
  assert.equal(phone.browser, "Safari");
  const ipad = parseAgent(
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 Version/18.0 Safari/605.1.15",
    5,
  );
  assert.equal(ipad.device, "tablet");
  assert.equal(ipad.os, "iPadOS");
  assert.equal(
    parseAgent("Googlebot/2.1 (+http://www.google.com/bot.html)").bot,
    true,
  );
  assert.equal(
    parseAgent(CHROME_WIN.replace("Chrome", "HeadlessChrome")).bot,
    true,
  );
});

test("referrerHost hides this site and strips www", () => {
  assert.equal(referrerHost("https://www.google.com/search?q=x"), "google.com");
  assert.equal(referrerHost("https://shoug-tech.com/academics/"), "");
  assert.equal(referrerHost("https://www.shoug-tech.com/"), "");
  assert.equal(referrerHost("not a url"), "");
  assert.equal(referrerHost(""), "");
});

test("riyadhClock is UTC+3", () => {
  // 2026-11-26 22:30 UTC is 01:30 on Friday 27 November in Riyadh.
  assert.deepEqual(riyadhClock(Date.UTC(2026, 10, 26, 22, 30)), {
    day: 20261127,
    hour: 1,
    weekday: 5,
  });
});

const meta = { userAgent: CHROME_WIN, country: "SA", city: "Riyadh" };
const context = {
  p: "/academics/software-engineering/se322/exams/q/q.html?utm=1",
  t: "SE322 quiz",
  r: "https://www.google.com/",
  bl: "ar-SA",
  sl: "en",
  th: "dark/original",
  si: 1,
  us: "Twitter",
  um: "social",
  uc: "launch",
  vw: 1280,
  nv: 1,
  nd: 1,
  ix: 1,
  ds: -1,
};

test("toDataPoints lays out a pageview in the documented columns", () => {
  const now = Date.UTC(2026, 10, 26, 9, 0);
  const [point] = toDataPoints(
    { c: context, e: [{ n: "pageview", ms: 812 }] },
    meta,
    now,
  );
  assert.deepEqual(point.indexes, ["pageview"]);
  assert.deepEqual(point.blobs, [
    "pageview",
    "/academics/software-engineering/se322/exams/q/q.html",
    "academics",
    "se322",
    "exams",
    "google.com",
    "SA",
    "desktop",
    "Chrome",
    "Windows",
    "ar-sa",
    "en",
    "dark/original",
    "1",
    "twitter",
    "social / launch",
    "",
    "",
    "SE322 quiz",
    "Riyadh",
  ]);
  assert.deepEqual(
    point.doubles,
    [0, 0, 0, 1280, 1, 1, 1, 812, 0, 0, 20261126, 12, 4, -1, 0],
  );
});

test("non-pageview events carry no visit flags, referrer or title", () => {
  const points = toDataPoints(
    {
      c: context,
      e: [
        { n: "engage", s: 42, sc: 80, qa: 5, qc: 4 },
        { n: "engage", s: 10 },
        { n: "search", l: "  uml   diagrams ", v: 3 },
      ],
    },
    meta,
  );
  assert.equal(points.length, 3);
  const [engage, later, search] = points;
  assert.equal(engage.blobs[5], "");
  assert.equal(engage.blobs[18], "");
  assert.deepEqual(
    engage.doubles.slice(0, 10),
    [0, 42, 80, 1280, 0, 0, 0, 0, 5, 4],
  );
  assert.equal(engage.doubles[14], 1);
  assert.equal(later.doubles[2], 0);
  assert.equal(later.doubles[14], 0);
  assert.equal(search.blobs[16], "uml diagrams");
  assert.equal(search.doubles[0], 3);
});

test("toDataPoints drops bots, automation, unknown events and junk", () => {
  assert.deepEqual(
    toDataPoints(
      { c: context, e: [{ n: "pageview" }] },
      { userAgent: "curl/8" },
    ),
    [],
  );
  assert.deepEqual(
    toDataPoints({ c: { ...context, wd: 1 }, e: [{ n: "pageview" }] }, meta),
    [],
  );
  assert.deepEqual(
    toDataPoints({ c: context, e: [{ n: "drop table" }, null, 5] }, meta),
    [],
  );
  assert.deepEqual(toDataPoints(null, meta), []);
  assert.deepEqual(toDataPoints({ e: "x" }, meta), []);
  const many = toDataPoints(
    { c: context, e: Array(100).fill({ n: "click" }) },
    meta,
  );
  assert.equal(many.length, 40);
});

test("long and control-character input is cut down", () => {
  const [p] = toDataPoints(
    { c: context, e: [{ n: "error", l: "a\u0000b".repeat(500), v: 1e20 }] },
    meta,
  );
  assert.ok(!p.blobs[16].includes("\u0000"));
  assert.ok(p.blobs[16].length <= 240);
  assert.equal(p.doubles[0], 1e9);
});

function collectRequest(body, headers = {}) {
  return new Request("https://w.example/v1/collect", {
    method: "POST",
    headers: {
      "user-agent": CHROME_WIN,
      "cf-connecting-ip": "1.2.3.4",
      ...headers,
    },
    body: typeof body === "string" ? body : JSON.stringify(body),
  });
}

test("handleCollect writes points and never stores the IP", async () => {
  const written = [];
  const keys = [];
  const env = {
    SITE_EVENTS: { writeDataPoint: (p) => written.push(p) },
    ANALYTICS_RATE_LIMIT: {
      limit: async ({ key }) => (keys.push(key), { success: true }),
    },
  };
  const res = await handleCollect(
    collectRequest({
      c: context,
      e: [{ n: "pageview" }, { n: "click", l: "Read aloud", d: "button" }],
    }),
    env,
    "https://shoug-tech.com",
  );
  assert.equal(res.status, 204);
  assert.equal(
    res.headers.get("access-control-allow-origin"),
    "https://shoug-tech.com",
  );
  assert.equal(written.length, 2);
  assert.deepEqual(keys, ["1.2.3.4"]);
  assert.ok(!JSON.stringify(written).includes("1.2.3.4"));
});

test("handleCollect rejects bad JSON, oversize bodies and rate-limited clients", async () => {
  const env = { SITE_EVENTS: { writeDataPoint() {} } };
  assert.equal(
    (await handleCollect(collectRequest("{"), env, "o")).status,
    400,
  );
  assert.equal(
    (await handleCollect(collectRequest("x".repeat(40000)), env, "o")).status,
    413,
  );
  const limited = {
    ...env,
    ANALYTICS_RATE_LIMIT: { limit: async () => ({ success: false }) },
  };
  assert.equal(
    (await handleCollect(collectRequest({ e: [] }), limited, "o")).status,
    429,
  );
  // A missing binding (e.g. local dev) is a silent no-op, not an error.
  assert.equal(
    (await handleCollect(collectRequest({ e: [] }), {}, "o")).status,
    204,
  );
});

test("cleanFilters keeps only well-formed values", () => {
  assert.deepEqual(
    cleanFilters({
      course: "se322",
      section: "academics",
      country: "SA",
      device: "mobile",
      path: "/academics/",
      kind: "exams",
    }),
    {
      course: "se322",
      section: "academics",
      country: "SA",
      device: "mobile",
      path: "/academics/",
      kind: "exams",
    },
  );
  assert.deepEqual(
    cleanFilters({
      course: "se322' OR 1=1 --",
      section: "a b",
      country: "sa",
      device: "fridge",
      path: "/x' OR '1'='1",
      extra: "y",
    }),
    {},
  );
  assert.deepEqual(cleanFilters(null), {});
  assert.deepEqual(cleanFilters({ path: "/a\\b" }), {});
});

test("buildQueries scopes every report by range and filters", () => {
  const { days, queries } = buildQueries("30", {
    course: "se322",
    device: "mobile",
  });
  assert.equal(days, 30);
  for (const [name, sql] of Object.entries(queries)) {
    if (name === "live") {
      assert.match(sql, /INTERVAL '30' MINUTE/);
    } else if (name === "previous") {
      assert.match(sql, /INTERVAL '60' DAY/);
    } else {
      assert.match(sql, /INTERVAL '30' DAY/, name);
    }
    assert.match(sql, /blob4 = 'se322'/, name);
    assert.match(sql, /blob8 = 'mobile'/, name);
    assert.match(sql, /FROM site_events/, name);
  }
  assert.equal(buildQueries("90").queries.previous, undefined);
  assert.equal(buildQueries("bogus").days, 7);
});

function json(body, status = 200, origin = "") {
  return new Response(JSON.stringify(body), {
    status,
    headers: {
      "content-type": "application/json",
      "access-control-allow-origin": origin,
    },
  });
}

function queryRequest(token, body = { range: "7" }) {
  return new Request("https://w.example/v1/analytics-query", {
    method: "POST",
    headers: token ? { authorization: `Bearer ${token}` } : {},
    body: JSON.stringify(body),
  });
}

function firestore(adminUid, status = 200) {
  return async (url, init) => {
    if (url.startsWith("https://firestore.googleapis.com/")) {
      assert.match(url, /courseCommerce\/ethics\?mask\.fieldPaths=adminUid$/);
      assert.equal(init.headers.authorization, "Bearer tok");
      return new Response(
        JSON.stringify({ fields: { adminUid: { stringValue: adminUid } } }),
        { status },
      );
    }
    if (url.includes("/analytics_engine/sql")) {
      assert.equal(init.headers.authorization, "Bearer cf-token");
      assert.match(init.body, / FORMAT JSON$/);
      if (
        init.body.includes(
          "quantileExactWeighted(0.75)(double1, _sample_interval) AS p75, SUM(IF",
        )
      )
        return new Response("bad", { status: 400 });
      return new Response(JSON.stringify({ data: [{ n: 3 }] }), {
        status: 200,
      });
    }
    throw new Error("unexpected fetch " + url);
  };
}

test("isAdmin needs a verified email and the configured admin UID", async () => {
  assert.equal(
    await isAdmin("tok", { uid: "u1", emailVerified: true }, firestore("u1")),
    true,
  );
  assert.equal(
    await isAdmin("tok", { uid: "u1", emailVerified: false }, firestore("u1")),
    false,
  );
  assert.equal(
    await isAdmin("tok", { uid: "u2", emailVerified: true }, firestore("u1")),
    false,
  );
  assert.equal(
    await isAdmin(
      "tok",
      { uid: "u1", emailVerified: true },
      firestore("u1", 403),
    ),
    false,
  );
});

test("handleAnalyticsQuery gates on sign-in, admin and configuration", async () => {
  const env = { CF_ACCOUNT_ID: "acct", CF_ANALYTICS_TOKEN: "cf-token" };
  const admin = async () => ({ uid: "u1", emailVerified: true });
  let res = await handleAnalyticsQuery(
    queryRequest(""),
    env,
    "o",
    json,
    admin,
    firestore("u1"),
  );
  assert.equal(res.status, 401);
  res = await handleAnalyticsQuery(
    queryRequest("tok"),
    env,
    "o",
    json,
    async () => null,
    firestore("u1"),
  );
  assert.equal(res.status, 401);
  res = await handleAnalyticsQuery(
    queryRequest("tok"),
    env,
    "o",
    json,
    admin,
    firestore("someone-else"),
  );
  assert.equal(res.status, 403);
  res = await handleAnalyticsQuery(
    queryRequest("tok"),
    {},
    "o",
    json,
    admin,
    firestore("u1"),
  );
  assert.equal(res.status, 503);
  res = await handleAnalyticsQuery(
    queryRequest("tok"),
    env,
    "o",
    json,
    admin,
    firestore("u1"),
  );
  assert.equal(res.status, 200);
  const body = await res.json();
  assert.equal(body.days, 7);
  assert.deepEqual(body.data.totals, [{ n: 3 }]);
  assert.ok(Object.keys(body.data).length > 30);
});
