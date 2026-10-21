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
    summary: { cumulativeGpa: 2.82, earnedHours: 41, totalPoints: 0 },
  });
  assert.deepEqual(result.courses, [
    { code: "CS 331", title: "Algorithms", hours: 3, grade: "A+", term: "251" },
    { code: "PHY 105", title: "", hours: 4, grade: "F", term: "242" },
    { code: "PHY 105", title: "", hours: 4, grade: "C", term: "243" },
  ]);
  assert.deepEqual(result.inProgress, [{ code: "SE 322", title: "", hours: 3, grade: "", term: "261" }]);
  assert.equal(result.skipped, 2);
  assert.deepEqual(result.summary, { cumulativeGpa: 2.82, earnedHours: 41, totalPoints: null });
});

test("model answers are read as text, fenced text, parsed objects or chat choices", () => {
  const body = { courses: [] };
  assert.deepEqual(modelJson({ response: body }), body);
  assert.deepEqual(modelJson({ response: "```json\n{\"courses\":[]}\n```" }), body);
  assert.deepEqual(modelJson({ choices: [{ message: { content: "Here: {\"courses\":[]}" } }] }), body);
  assert.equal(modelJson({ response: "no json here" }), null);
});

test("EduGate rows: reversed codes, * pending, preparatory flag, swapped hours/points", () => {
  const result = normalizeTranscript({
    courses: [
      { code: "101ARAB", hours: 2, points: 4, grade: "C", term: "20231" },
      { code: "MATH001", hours: 4, points: 6, grade: "+D", term: "20231" },
      { code: "PHY105", hours: 6, points: 4, grade: "D+", term: "20241" },
      { code: "ETHCS303", hours: 3, points: 12, grade: "A+", term: "20253" },
      { code: "CS 175", hours: 3, points: 9, grade: "A", term: "20241" },
      { code: "331CS", hours: 3, points: null, grade: "*", term: "20261" },
    ],
    summary: { cumulativeGpa: 3, earnedHours: 76, totalPoints: 227.75 },
  });
  assert.deepEqual(
    result.courses.map((c) => [c.code, c.hours, c.grade, c.term, c.prep || false, c.flag || ""]),
    [
      ["ARAB 101", 2, "C", "231", false, ""],
      ["MATH 001", 4, "D+", "231", true, ""],
      ["PHY 105", 4, "D+", "241", false, ""],
      ["ETHC 303", 3, "A+", "253", false, ""],
      ["CS 175", 3, "A", "241", false, "check"],
    ],
  );
  assert.deepEqual(result.inProgress.map((c) => c.code), ["CS 331"]);
  assert.deepEqual(result.summary, { cumulativeGpa: 3, earnedHours: 76, totalPoints: 227.75 });
});
