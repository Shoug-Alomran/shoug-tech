import { test } from "node:test";
import assert from "node:assert/strict";
import { handle, authorize, parseRange, protectedPath } from "./index.js";
const response = (body, status = 200) =>
  new Response(JSON.stringify(body), { status });
function fixture({ state = "approved", identity = true, admin = false } = {}) {
  let privateReads = 0,
    videoReads = 0;
  const env = {
    FIREBASE_PROJECT: "demo-project",
    FIREBASE_API_KEY: "test-key",
    ASSETS: {
      async fetch(request) {
        const path = new URL(request.url).pathname;
        if (path === "/course-access/index.html")
          return new Response("COURSE LOCKED", {
            headers: { "Content-Type": "text/html" },
          });
        privateReads++;
        return new Response("PRIVATE LESSON", {
          headers: {
            "Content-Type": "text/html",
            "Cache-Control": "public, max-age=3600",
          },
        });
      },
    },
    VIDEOS: {
      async head() {
        videoReads++;
        return { size: 100, httpMetadata: { contentType: "video/mp4" } };
      },
      async get(_, options) {
        videoReads++;
        return { body: new Uint8Array(options.range?.length || 100) };
      },
    },
  };
  const fetcher = async (url) => {
    if (url.includes("accounts:lookup"))
      return identity
        ? response({ users: [{ localId: "buyer", emailVerified: true }] })
        : response({}, 400);
    if (url.includes("courseCommerce"))
      return response({
        fields: { adminUid: { stringValue: admin ? "buyer" : "owner" } },
      });
    return response({
      fields: {
        status: { stringValue: state },
        course: { stringValue: "ethics" },
        amount: { integerValue: "32500" },
        currency: { stringValue: "SAR" },
      },
    });
  };
  return {
    env,
    fetcher,
    privateReads: () => privateReads,
    videoReads: () => videoReads,
  };
}
const root = "https://shoug-tech.com";
const course = "/academics/other-courses/ethcs303/";
const withToken = { headers: { Cookie: "__Host-ethics_session=valid-token" } };
test("signed-out direct lesson, PDF, quiz data and video requests never read paid assets", async () => {
  const f = fixture();
  for (const path of [
    course,
    course + "slides/test.pdf",
    "/javascripts/past-exam-practice.js",
    "/course-media/ethics/test.mp4",
    "/ai-context" + course + "index.json",
  ]) {
    const result = await handle(new Request(root + path), f.env, f.fetcher);
    assert.doesNotMatch(await result.text(), /PRIVATE LESSON/);
    assert.match(result.headers.get("Cache-Control"), /no-store/);
  }
  assert.equal(f.privateReads(), 0);
  assert.equal(f.videoReads(), 0);
});
test("signed-in pending and rejected buyers remain locked", async () => {
  for (const state of ["pending", "rejected", "", "paid"]) {
    const f = fixture({ state });
    assert.equal(
      await (
        await handle(new Request(root + course, withToken), f.env, f.fetcher)
      ).text(),
      "COURSE LOCKED",
    );
    assert.equal(f.privateReads(), 0);
  }
});
test("forged or expired authentication never grants access", async () => {
  const f = fixture({ identity: false });
  assert.equal((await authorize("forged", f.env, f.fetcher)).allowed, false);
});
test("approved buyer receives private, non-cacheable lessons", async () => {
  const f = fixture(),
    result = await handle(
      new Request(root + course, withToken),
      f.env,
      f.fetcher,
    );
  assert.equal(await result.text(), "PRIVATE LESSON");
  assert.match(result.headers.get("Cache-Control"), /no-store/);
  assert.equal(result.headers.get("Vary"), "Cookie, Authorization");
});
test("configured owner can preview without creating a fake payment", async () => {
  const f = fixture({ state: "pending", admin: true });
  assert.equal((await authorize("valid", f.env, f.fetcher)).allowed, true);
});
test("session creation requires same-origin POST and approved status", async () => {
  const f = fixture();
  const request = (origin) =>
    new Request(root + "/course-access/session", {
      method: "POST",
      headers: { Origin: origin },
      body: JSON.stringify({ idToken: "valid" }),
    });
  assert.equal(
    (await handle(request("https://other.test"), f.env, f.fetcher)).status,
    403,
  );
  const result = await handle(request(root), f.env, f.fetcher);
  assert.equal(result.status, 200);
  assert.match(
    result.headers.get("Set-Cookie"),
    /Secure; HttpOnly; SameSite=Strict/,
  );
  const pending = fixture({ state: "pending" });
  assert.equal(
    (await handle(request(root), pending.env, pending.fetcher)).headers.get(
      "Set-Cookie",
    ),
    null,
  );
});
test("sign-out clears secure session cookie", async () => {
  const f = fixture();
  const result = await handle(
    new Request(root + "/course-access/session", {
      method: "DELETE",
      headers: { Origin: root },
    }),
    f.env,
    f.fetcher,
  );
  assert.match(result.headers.get("Set-Cookie"), /Max-Age=0/);
});
test("approved video playback supports seeking with bounded byte ranges", async () => {
  const f = fixture();
  const result = await handle(
    new Request(root + "/course-media/ethics/test.mp4", {
      headers: { ...withToken.headers, Range: "bytes=10-19" },
    }),
    f.env,
    f.fetcher,
  );
  assert.equal(result.status, 206);
  assert.equal(result.headers.get("Content-Range"), "bytes 10-19/100");
  assert.equal((await result.arrayBuffer()).byteLength, 10);
});
test("invalid byte ranges cannot read video data", async () => {
  for (const range of [
    "bytes=100-101",
    "bytes=9-2",
    "bytes=0-1,8-9",
    "bytes=-0",
    "bytes=-",
  ])
    assert.equal(parseRange(range, 100), null);
  assert.deepEqual(parseRange("bytes=-10", 100), { offset: 90, length: 10 });
  assert.deepEqual(parseRange("bytes=90-999", 100), { offset: 90, length: 10 });
});
test("upstream failures fail closed, without any asset fallback", async () => {
  const f = fixture();
  const result = await handle(
    new Request(root + course, withToken),
    f.env,
    async () => {
      throw new Error("offline");
    },
  );
  assert.equal(result.status, 503);
  assert.equal(f.privateReads(), 0);
});
test("unknown routes cannot be used to reach asset binding", async () => {
  const f = fixture();
  assert.equal(
    (
      await handle(
        new Request(root + "/other.html", withToken),
        f.env,
        f.fetcher,
      )
    ).status,
    404,
  );
  assert.equal(f.privateReads(), 0);
  assert.equal(protectedPath("/academics/math/stat101/"), false);
});

test("only the selected sample video is available without payment", async () => {
  const f = fixture();
  const sample = await handle(
    new Request(
      "https://shoug-tech.com/course-access/samples/intro-video.mp4",
      { headers: { Range: "bytes=0-9" } },
    ),
    f.env,
    f.fetcher,
  );
  assert.equal(sample.status, 206);
  const privateVideo = await handle(
    new Request("https://shoug-tech.com/course-media/ethics/other.mp4"),
    f.env,
    f.fetcher,
  );
  assert.equal(privateVideo.status, 401);
});
