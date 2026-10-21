import test from "node:test";
import assert from "node:assert/strict";
import worker from "./index.js";

const origin = "http://localhost:8000";
function request(path, body, headers = {}) {
  return new Request(`https://worker.test${path}`, {
    method: "POST",
    headers: { origin, "content-type": "application/json", ...headers },
    body: JSON.stringify(body),
  });
}

test("transcript endpoint is mounted and requires authentication", async () => {
  const response = await worker.fetch(request("/v1/transcript-import", {}), {});
  assert.equal(response.status, 401);
});

test("transcript upload rejects oversized bodies before parsing", async () => {
  const response = await worker.fetch(
    new Request("https://worker.test/v1/transcript-import", {
      method: "POST",
      headers: { origin, "content-type": "multipart/form-data; boundary=x", "content-length": "6000000" },
      body: "",
    }),
    {},
  );
  assert.equal(response.status, 413);
});

test("transcript endpoint rejects non-site origins", async () => {
  const response = await worker.fetch(
    new Request("https://worker.test/v1/transcript-import", {
      method: "POST",
      headers: { origin: "https://attacker.example", "content-type": "application/json" },
      body: "{}",
    }),
    {},
  );
  assert.equal(response.status, 403);
});
