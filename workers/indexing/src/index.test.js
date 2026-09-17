import test from "node:test";
import assert from "node:assert/strict";
import worker, { handle } from "./index.js";

const request = (path, host = "shoug-tech.com") =>
  new Request(`https://${host}${path}`);
const unexpected = () => {
  throw new Error("Origin must not be called");
};

test("old mixed-case Software Processes URL goes directly to existing wrapper", async () => {
  const res = await handle(
    request(
      "/Academics/software-engineering/SE201/Chapter-2/Software-Processes.html",
    ),
    unexpected,
  );
  assert.equal(res.status, 301);
  assert.equal(
    res.headers.get("location"),
    "https://shoug-tech.com/academics/software-engineering/se201/slide-breakdowns/02-chapter-2-software-processes/",
  );
});

test("renamed physics PDF encodes # and spaces without losing query", async () => {
  const res = await handle(
    request(
      "/academics/math/phy105/slides/Chapter%20%23%202%20(Last%20updated).pdf?download=1",
    ),
    unexpected,
  );
  assert.equal(res.status, 301);
  assert.equal(
    res.headers.get("location"),
    "https://shoug-tech.com/academics/math/phy105/slides/chapter-2-vectors/Chapter%20%23%202%20%28Last%20updated%29.pdf?download=1",
  );
});

test("PDF bytes/range status survive canonical header injection", async () => {
  const res = await handle(
    request(
      "/academics/software-engineering/se423/slides/change-management/change-management.pdf",
    ),
    async () =>
      new Response("pdf bytes", {
        status: 206,
        headers: { "Content-Range": "bytes 0-8/100" },
      }),
  );
  assert.equal(res.status, 206);
  assert.equal(res.headers.get("content-range"), "bytes 0-8/100");
  assert.equal(
    res.headers.get("link"),
    '<https://shoug-tech.com/academics/software-engineering/se423/slides/change-management/>; rel="canonical"',
  );
  assert.equal(await res.text(), "pdf bytes");
});

test("never attach PDF canonicals to missing files or server errors", async () => {
  for (const status of [404, 500]) {
    const res = await handle(
      request(
        "/academics/software-engineering/se423/slides/change-management/change-management.pdf",
      ),
      async () => new Response("error", { status }),
    );
    assert.equal(res.status, status);
    assert.equal(res.headers.get("link"), null);
  }
});

test("OS source URLs redirect only when a replacement was verified", async () => {
  const res = await handle(
    request("/phase-2/plan.md", "operating-systems.shoug-tech.com"),
    unexpected,
  );
  assert.equal(
    res.headers.get("location"),
    "https://operating-systems.shoug-tech.com/phase-2/plan/",
  );
  const missing = await handle(
    request("/unknown.md", "operating-systems.shoug-tech.com"),
    async () => new Response(null, { status: 404 }),
  );
  assert.equal(missing.status, 404);
});

test("robots exceptions retain source/search exclusions", async () => {
  const res = await handle(
    request("/robots.txt", "operating-systems.shoug-tech.com"),
    async () =>
      new Response("User-agent: *\nDisallow: /*.md$\nDisallow: /*?q=*\n"),
  );
  const text = await res.text();
  assert.ok(text.includes("Allow: /phase-2/plan.md$"));
  assert.ok(text.includes("Disallow: /*.md$"));
  assert.ok(text.includes("Disallow: /*?q=*"));
});

test("database obsolete PDF redirects to published report", async () => {
  const res = await handle(
    request("/Phase%203/report.pdf", "database.shoug-tech.com"),
    unexpected,
  );
  assert.equal(
    res.headers.get("location"),
    "https://database.shoug-tech.com/phase-3/report/",
  );
});

test("unsafe methods and unrelated paths pass through unchanged", async () => {
  const original = new Response("unchanged");
  assert.equal(
    await handle(
      new Request("https://shoug-tech.com/api/test", { method: "POST" }),
      async () => original,
    ),
    original,
  );
  assert.equal(
    await handle(request("/unknown"), async () => original),
    original,
  );
});

test("www and HTTP normalization preserves path and query", async () => {
  const res = await handle(
    new Request("http://www.shoug-tech.com/academics/?lang=ar"),
    unexpected,
  );
  assert.equal(
    res.headers.get("location"),
    "https://shoug-tech.com/academics/?lang=ar",
  );
});

test("Cloudflare entrypoint accepts env and execution context arguments", async () => {
  const previous = globalThis.fetch;
  try {
    globalThis.fetch = async () => new Response("ok");
    const res = await worker.fetch(request("/"), {}, {});
    assert.equal(await res.text(), "ok");
  } finally {
    globalThis.fetch = previous;
  }
});
