// ── Free-time interpreter (schedule planner) ───────────────────────────────
// /academics/schedule-planner/ lets students write when they want to be free
// ("I have the gym Monday and Wednesday evenings, and I'd like Thursdays
// off"). The page reads common phrasing itself (docs/javascripts/
// free-time-parser.js) and only sends text it couldn't read here. The model
// turns it into blocks of time with no classes; everything it returns is
// re-checked by cleanResult() before it reaches the page.
//
// Only the student's sentence is sent: no name, grades or account details.

export const MAX_TEXT = 500;
const DAY_START = 7 * 60;
const DAY_END = 22 * 60;
const DAY_NAMES = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday"];

const SYSTEM = `You turn a university student's description of when they want to be FREE (no classes) into JSON.
The week is Sunday (0) to Thursday (4). Classes run 08:00 to 21:00. 12:00-13:00 is already a break for everyone.
Return ONLY a JSON object, no prose, in this shape:
{"rules":[{"days":[0,1,2,3,4],"from":"HH:MM","to":"HH:MM","label":"short English description"}],"maxDays":null,"preferFewerGaps":false,"notUnderstood":""}
- "rules" are times with NO classes. A whole day off is from "07:00" to "22:00".
- "only between 9 and 2" means two rules: 07:00-09:00 and 14:00-22:00.
- Bare hours 1-6 mean PM. "Evening" is 17:00-22:00, "afternoon" 13:00-17:00, "morning" 07:00-12:00.
- "maxDays" is a number only if they ask for at most N days on campus.
- "preferFewerGaps" is true if they want classes back to back.
- Put anything that is not about time in "notUnderstood".
Examples:
"gym on monday and wednesday evenings" -> {"rules":[{"days":[1,3],"from":"17:00","to":"22:00","label":"Gym Mon and Wed evenings"}],"maxDays":null,"preferFewerGaps":false,"notUnderstood":""}
"I pick up my sister at 1:30 every day except thursday" -> {"rules":[{"days":[0,1,2,3],"from":"13:30","to":"22:00","label":"Free from 1:30 PM except Thursday"}],"maxDays":null,"preferFewerGaps":false,"notUnderstood":""}`;

function minutes(value) {
  const m = String(value || "").match(/^(\d{1,2}):(\d{2})$/);
  if (!m) return null;
  const h = Number(m[1]);
  const min = Number(m[2]);
  if (h > 24 || min > 59) return null;
  return Math.min(DAY_END, Math.max(DAY_START, h * 60 + min));
}

/** Pulls the first JSON object out of the model's answer. */
export function extractJson(text) {
  const s = String(text || "");
  const start = s.indexOf("{");
  if (start < 0) return null;
  let depth = 0;
  for (let i = start; i < s.length; i++) {
    if (s[i] === "{") depth++;
    else if (s[i] === "}" && --depth === 0) {
      try {
        return JSON.parse(s.slice(start, i + 1));
      } catch {
        return null;
      }
    }
  }
  return null;
}

/** Keeps only well-formed rules: days 0–4, times inside the day, short labels. */
export function cleanResult(raw) {
  const out = { rules: [], maxDays: null, preferGaps: false, unknown: [] };
  if (!raw || typeof raw !== "object") return out;
  for (const r of Array.isArray(raw.rules) ? raw.rules.slice(0, 12) : []) {
    if (!r || typeof r !== "object") continue;
    const days = [...new Set((Array.isArray(r.days) ? r.days : []).map(Number))]
      .filter((d) => Number.isInteger(d) && d >= 0 && d <= 4)
      .sort();
    const from = minutes(r.from);
    const to = minutes(r.to);
    if (!days.length || from == null || to == null || to <= from) continue;
    const label =
      typeof r.label === "string" && r.label.trim()
        ? r.label.replace(/[<>]/g, "").replace(/\s+/g, " ").trim().slice(0, 80)
        : `Free ${r.from}–${r.to} on ${days.map((d) => DAY_NAMES[d]).join(", ")}`;
    out.rules.push({ days, from, to, label });
  }
  const n = Number(raw.maxDays);
  if (Number.isInteger(n) && n >= 1 && n <= 5) out.maxDays = n;
  out.preferGaps = raw.preferFewerGaps === true;
  if (typeof raw.notUnderstood === "string" && raw.notUnderstood.trim())
    out.unknown.push(
      raw.notUnderstood.replace(/[<>]/g, "").trim().slice(0, 120),
    );
  return out;
}

export async function handleFreeTime(request, env, origin, json, generate) {
  if (env.AI_RATE_LIMIT) {
    const key = request.headers.get("cf-connecting-ip") || "unknown";
    const result = await env.AI_RATE_LIMIT.limit({ key });
    if (!result.success)
      return json(
        { error: "Too many requests. Please wait a minute and try again." },
        429,
        origin,
      );
  }
  let body;
  try {
    body = await request.json();
  } catch {
    return json({ error: "Invalid JSON." }, 400, origin);
  }
  const text =
    typeof body.text === "string"
      ? body.text.replace(/\s+/g, " ").trim().slice(0, MAX_TEXT)
      : "";
  if (!text)
    return json({ error: "Describe when you want to be free." }, 400, origin);
  const answer = await generate(env, {
    messages: [
      { role: "system", content: SYSTEM },
      { role: "user", content: text },
    ],
    temperature: 0,
    max_tokens: 500,
  });
  const parsed = extractJson(answer);
  if (!parsed)
    return json(
      { error: "Couldn't read that. Try simpler phrases." },
      502,
      origin,
    );
  return json(cleanResult(parsed), 200, origin);
}
