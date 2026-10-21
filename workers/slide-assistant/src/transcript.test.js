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

import { modelJson, normalizeTranscript, termCode } from "./transcript.js";

test("transcript terms map to the site's PSU term codes", () => {
  assert.equal(termCode("20241"), "241");
  assert.equal(termCode("241"), "241");
  assert.equal(termCode("Term 20253 - Summer"), "253");
  assert.equal(termCode("First Semester 2024/2025"), "241");
  assert.equal(termCode("Second Semester 2025/2026"), "252");
  assert.equal(termCode("Summer Semester 2024/2025"), "243");
  assert.equal(termCode("Summer 2026"), "253");
  assert.equal(termCode("الفصل الثاني 2025/2026"), "252");
  assert.equal(termCode("Spring"), "");
});

test("each row is checked on its own; pending grades become in-progress courses", () => {
  const result = normalizeTranscript({
    courses: [
      { code: "cs331", title: "Algorithms", hours: 3, grade: "+A", term: "20251" },
      { code: "PHY 105", hours: 4, grade: "F", term: "20242" },
      { code: "PHY 105", hours: 4, grade: "C", term: "20243" },
      { code: "SE 322", hours: 3, grade: "ت", term: "20261" },
      { code: "Total hours", hours: 41, grade: "", term: "" },
      { code: "ENG 101", hours: 3, grade: "Excellent", term: "20241" },
    ],
    summary: { cumulativeGpa: 2.82, earnedHours: 41, gpaHours: 0 },
  });
  assert.deepEqual(result.courses, [
    { code: "CS 331", title: "Algorithms", hours: 3, grade: "A+", term: "251" },
    { code: "PHY 105", title: "", hours: 4, grade: "F", term: "242" },
    { code: "PHY 105", title: "", hours: 4, grade: "C", term: "243" },
  ]);
  assert.deepEqual(result.inProgress, [{ code: "SE 322", title: "", hours: 3, grade: "", term: "261" }]);
  assert.equal(result.skipped, 2);
  assert.deepEqual(result.summary, { cumulativeGpa: 2.82, earnedHours: 41, gpaHours: null });
});

test("model answers are read as text, fenced text, parsed objects or chat choices", () => {
  const body = { courses: [] };
  assert.deepEqual(modelJson({ response: body }), body);
  assert.deepEqual(modelJson({ response: "```json\n{\"courses\":[]}\n```" }), body);
  assert.deepEqual(modelJson({ choices: [{ message: { content: "Here: {\"courses\":[]}" } }] }), body);
  assert.equal(modelJson({ response: "no json here" }), null);
});
