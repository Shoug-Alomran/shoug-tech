import test from "node:test";
import assert from "node:assert/strict";
import { cleanResult, extractJson, handleFreeTime } from "./free-time.js";

function json(body, status = 200) {
  return new Response(JSON.stringify(body), { status });
}

function request(body) {
  return new Request("https://worker.test/v1/free-time", {
    method: "POST",
    headers: { "content-type": "application/json" },
    body: JSON.stringify(body),
  });
}

test("extractJson finds the object inside chatter", () => {
  assert.deepEqual(extractJson('Sure! {"rules":[],"maxDays":3} done'), {
    rules: [],
    maxDays: 3,
  });
  assert.equal(extractJson("no json here"), null);
});

test("cleanResult keeps valid rules and drops bad ones", () => {
  const out = cleanResult({
    rules: [
      {
        days: [1, 3, 3],
        from: "17:00",
        to: "22:00",
        label: "Gym <b>evenings</b>",
      },
      { days: [6], from: "09:00", to: "10:00" },
      { days: [0], from: "10:00", to: "09:00" },
      { days: [2], from: "nine", to: "10:00" },
    ],
    maxDays: 9,
    preferFewerGaps: true,
    notUnderstood: "cheap parking",
  });
  assert.deepEqual(out.rules, [
    { days: [1, 3], from: 1020, to: 1320, label: "Gym bevenings/b" },
  ]);
  assert.equal(out.maxDays, null);
  assert.equal(out.preferGaps, true);
  assert.deepEqual(out.unknown, ["cheap parking"]);
});

test("handleFreeTime sends only the text and returns cleaned rules", async () => {
  let sent;
  const res = await handleFreeTime(
    request({ text: "  gym  monday evenings " }),
    {},
    "",
    json,
    async (env, input) => {
      sent = input;
      return '{"rules":[{"days":[1],"from":"17:00","to":"22:00","label":"Gym Monday evenings"}],"maxDays":null}';
    },
  );
  assert.equal(res.status, 200);
  assert.equal(sent.messages[1].content, "gym monday evenings");
  const body = await res.json();
  assert.equal(body.rules[0].from, 1020);
});

test("handleFreeTime rejects empty text and unreadable answers", async () => {
  assert.equal(
    (await handleFreeTime(request({ text: "" }), {}, "", json, async () => ""))
      .status,
    400,
  );
  assert.equal(
    (
      await handleFreeTime(
        request({ text: "hi" }),
        {},
        "",
        json,
        async () => "sorry",
      )
    ).status,
    502,
  );
});
