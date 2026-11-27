#!/usr/bin/env node
"use strict";

/**
 * Downloads PSU's public class timetable from Edugate and writes one JSON file
 * per term and campus for the schedule planner (docs/academics/schedule-planner/).
 *
 *   docs/data/psu-timetable/index.json        terms, campuses, departments, updatedAt
 *   docs/data/psu-timetable/<term>-<m|f>.json courses + sections for one campus
 *
 * Edugate's guest timetable is a JSF form: pick campus + degree + term, then a
 * department in the tree (setIndex(n)). Each department page lists every
 * section of every course in that department's plan, with the instructor,
 * meeting times, room and final exam date in hidden inputs. One session walks
 * every department of one campus/term by re-posting the tree page's ViewState.
 *
 * Usage: node scripts/sync-psu-timetable.js [--term 20262] [--campus f|m]
 */

const fs = require("fs");
const path = require("path");

const URL_ =
  "https://edugate.psu.edu.sa/psu/ui/guest/timetable/index/scheduleTreeCoursesIndex.faces";
const OUT_DIR = path.join(__dirname, "..", "docs", "data", "psu-timetable");
const UA = "shoug-tech-timetable-sync/1.0 (+https://shoug-tech.com/)";
const DELAY_MS = 400;
const CAMPUSES = { m: "1", f: "2" };
const DEGREE_BACHELOR = "1";

// Edugate day codes → 0 = Sunday … 4 = Thursday (PSU teaches Sun–Thu).
const DAYS = { ح: 0, ثن: 1, ثل: 2, ر: 3, خ: 4, ج: 5, س: 6 };
// L lecture, B lab, T tutorial, S design studio, C co-op training.
const ACTIVITY = {
  محاضرات: "L",
  معامل: "B",
  تمارين: "T",
  مرسم: "S",
  "تدريب تعاوني": "C",
};

const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

function arg(name) {
  const i = process.argv.indexOf(`--${name}`);
  return i > -1 ? process.argv[i + 1] : null;
}

function decode(value) {
  return String(value || "")
    .replace(/&nbsp;/gi, " ")
    .replace(/&quot;/gi, '"')
    .replace(/&#39;|&apos;/gi, "'")
    .replace(/&lt;/gi, "<")
    .replace(/&gt;/gi, ">")
    .replace(/&#(\d+);/g, (_, n) => String.fromCharCode(+n))
    .replace(/&amp;/gi, "&")
    .replace(/[‎‏‪-‮]/g, "")
    .replace(/\s+/g, " ")
    .trim();
}

const text = (html) => decode(String(html).replace(/<[^>]+>/g, " "));

class Session {
  constructor() {
    this.cookies = new Map();
  }
  cookieHeader() {
    return [...this.cookies].map(([k, v]) => `${k}=${v}`).join("; ");
  }
  keep(res) {
    const list =
      typeof res.headers.getSetCookie === "function"
        ? res.headers.getSetCookie()
        : [res.headers.get("set-cookie")].filter(Boolean);
    for (const c of list) {
      const [pair] = c.split(";");
      const eq = pair.indexOf("=");
      if (eq > 0)
        this.cookies.set(pair.slice(0, eq).trim(), pair.slice(eq + 1));
    }
  }
  async request(form, attempt = 1) {
    const opts = {
      headers: { "user-agent": UA, cookie: this.cookieHeader() },
      redirect: "follow",
    };
    if (form) {
      opts.method = "POST";
      opts.body = new URLSearchParams(form).toString();
      opts.headers["content-type"] = "application/x-www-form-urlencoded";
    }
    try {
      const res = await fetch(URL_, opts);
      this.keep(res);
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      return await res.text();
    } catch (err) {
      if (attempt >= 3) throw err;
      await sleep(2000 * attempt);
      return this.request(form, attempt + 1);
    }
  }
}

function viewState(html) {
  const m = html.match(/name="javax\.faces\.ViewState"[^>]*value="([^"]+)"/g);
  if (!m) throw new Error("No ViewState on the Edugate page");
  return m[m.length - 1].match(/value="([^"]+)"/)[1];
}

function options(html, id) {
  const block = html.match(new RegExp(`id="myForm:${id}"[\\s\\S]*?</select>`));
  if (!block) return [];
  return [
    ...block[0].matchAll(/<option[^>]*value="([^"]*)"[^>]*>([^<]*)<\/option>/g),
  ].map((m) => ({ value: m[1], label: decode(m[2]) }));
}

function departments(html) {
  // tree.add(id, parent, 'CODE-Arabic name', 'javascript:setIndex(n);')
  const parents = {};
  for (const m of html.matchAll(
    /tree\.add\((\d+),\s*(-?\d+),\s*'([^']*)',\s*''\)/g,
  ))
    parents[m[1]] = decode(m[3]);
  return [
    ...html.matchAll(
      /tree\.add\(\d+,\s*(\d+),\s*'([^']*)',\s*'javascript:setIndex\((\d+)\);'\)/g,
    ),
  ].map((m) => {
    const label = decode(m[2]);
    // "SE-CYS-هندسة البرمجيات (الأمن السيبراني)": the code is everything
    // before the last dash that precedes the Arabic name.
    const split = label.match(/^([^؀-ۿ]*?)\s*-\s*([؀-ۿ].*)$/);
    return {
      index: +m[3],
      code: split ? split[1].trim() : label,
      name: split ? split[2].trim() : label,
      college: parents[m[1]] || "",
    };
  });
}

function toMinutes(clock) {
  // "08:00 ص" (AM) / "01:00 م" (PM)
  const m = clock.match(/(\d{1,2}):(\d{2})\s*([صم])?/);
  if (!m) return null;
  let h = +m[1] % 12;
  if (m[3] === "م") h += 12;
  return h * 60 + +m[2];
}

function parseMeetings(raw) {
  // " ح ثن ثل @t 08:00 ص - 08:50 ص @r W330CYSLAB @n  ر @t ... "
  const meetings = [];
  for (const part of decode(raw).split("@n")) {
    const [daysPart, rest = ""] = part.split("@t");
    const [timePart = "", room = ""] = rest.split("@r");
    const [a, b] = timePart.split(" - ");
    const start = a && toMinutes(a);
    const end = b && toMinutes(b);
    if (start == null || end == null) continue;
    for (const d of daysPart.trim().split(/\s+/)) {
      if (d in DAYS) meetings.push([DAYS[d], start, end, room.trim()]);
    }
  }
  return meetings;
}

function parseExam(raw) {
  // "11-05-2027  04:00 م"
  const m = decode(raw).match(
    /(\d{2})-(\d{2})-(\d{4})\s+(\d{1,2}:\d{2}\s*[صم]?)/,
  );
  if (!m) return null;
  const mins = toMinutes(m[4]);
  const hh = String(Math.floor(mins / 60)).padStart(2, "0");
  const mm = String(mins % 60).padStart(2, "0");
  return `${m[3]}-${m[2]}-${m[1]}T${hh}:${mm}`;
}

function parseRows(html) {
  const rows = [];
  for (const m of html.matchAll(/<tr class="ROW[12]">([\s\S]*?)<\/tr>/g)) {
    const cells = [...m[1].matchAll(/<td[^>]*>([\s\S]*?)<\/td>/g)].map(
      (c) => c[1],
    );
    if (cells.length < 9) continue;
    const hidden = (key) => {
      const h = cells[8].match(
        new RegExp(`:${key}" type="hidden" name="[^"]*" value="([^"]*)"`),
      );
      return h ? h[1] : "";
    };
    rows.push({
      code: text(cells[0]).replace(/\s+/g, ""),
      name: text(cells[1]),
      crn: text(cells[2]),
      group: text(cells[3]),
      activity: ACTIVITY[text(cells[4])] || text(cells[4]),
      hours: parseInt(text(cells[5]), 10) || 0,
      gender: text(cells[6]),
      open: !/مغلق/.test(text(cells[7])),
      instructor: decode(hidden("instructor")),
      meetings: parseMeetings(hidden("section")),
      exam: parseExam(hidden("finalExamDate")),
    });
  }
  return rows;
}

async function scrapeCampusTerm(campus, term) {
  const s = new Session();
  const first = await s.request();
  const base = {
    myForm: "myForm",
    "myForm:select2": CAMPUSES[campus],
    "myForm:select1": DEGREE_BACHELOR,
    "myForm:semesterItems": term,
    "myForm:index": "",
  };
  const tree = await s.request({
    ...base,
    "javax.faces.ViewState": viewState(first),
  });
  const treeState = viewState(tree);
  const depts = departments(tree);
  if (!depts.length) throw new Error(`No departments for ${term}/${campus}`);

  const courses = {};
  const sections = new Map();
  for (const dept of depts) {
    await sleep(DELAY_MS);
    const html = await s.request({
      ...base,
      "myForm:index": String(dept.index),
      "myForm:commandLink": "myForm:commandLink",
      "javax.faces.ViewState": treeState,
    });
    const rows = parseRows(html);
    process.stdout.write(`  ${term}-${campus} ${dept.code}: ${rows.length}\n`);
    for (const r of rows) {
      const c = (courses[r.code] ||= { ar: r.name, h: 0, d: [] });
      if (r.hours > c.h) c.h = r.hours;
      if (!c.d.includes(dept.code)) c.d.push(dept.code);
      if (sections.has(r.crn)) continue;
      const sec = {
        crn: +r.crn,
        c: r.code,
        g: r.group,
        t: r.activity,
        o: r.open ? 1 : 0,
        i: r.instructor,
        m: r.meetings,
      };
      if (r.exam) sec.x = r.exam;
      sections.set(r.crn, sec);
    }
  }
  return {
    depts,
    courses,
    sections: [...sections.values()].sort(
      (a, b) =>
        a.c.localeCompare(b.c) || a.g.localeCompare(b.g) || a.crn - b.crn,
    ),
  };
}

async function main() {
  fs.mkdirSync(OUT_DIR, { recursive: true });
  const probe = new Session();
  const home = await probe.request();
  const terms = options(home, "semesterItems").filter(
    (t) => !arg("term") || t.value === arg("term"),
  );
  const campuses = arg("campus") ? [arg("campus")] : Object.keys(CAMPUSES);
  if (!terms.length) throw new Error("Edugate listed no terms.");

  const indexPath = path.join(OUT_DIR, "index.json");
  const index = fs.existsSync(indexPath)
    ? JSON.parse(fs.readFileSync(indexPath, "utf8"))
    : { files: {} };
  index.source = URL_;
  index.terms = options(home, "semesterItems");
  index.departments = index.departments || [];
  let changed = false;

  for (const term of terms) {
    for (const campus of campuses) {
      console.log(`Fetching ${term.label} (${term.value}), campus ${campus}`);
      const data = await scrapeCampusTerm(campus, term.value);
      if (data.sections.length < 50) {
        console.warn(
          `  only ${data.sections.length} sections; keeping the old file`,
        );
        continue;
      }
      const file = `${term.value}-${campus}.json`;
      const filePath = path.join(OUT_DIR, file);
      const body = { courses: data.courses, sections: data.sections };
      const known = new Set(index.departments.map((d) => d.code));
      for (const d of data.depts)
        if (!known.has(d.code))
          index.departments.push({
            code: d.code,
            name: d.name,
            college: d.college,
          });
      // Only rewrite (and bump updatedAt) when sections really changed, so an
      // unchanged run commits nothing and doesn't redeploy the site.
      if (fs.existsSync(filePath)) {
        const old = JSON.parse(fs.readFileSync(filePath, "utf8"));
        if (
          JSON.stringify({ courses: old.courses, sections: old.sections }) ===
          JSON.stringify(body)
        ) {
          console.log(`  ${file}: no changes`);
          continue;
        }
      }
      const updatedAt = new Date().toISOString();
      fs.writeFileSync(
        filePath,
        JSON.stringify({
          term: term.value,
          termLabel: term.label,
          campus,
          updatedAt,
          ...body,
        }),
      );
      index.files[file] = { updatedAt, sections: data.sections.length };
      changed = true;
      console.log(`  wrote ${file}: ${data.sections.length} sections`);
    }
  }
  index.updatedAt = new Date().toISOString();
  fs.writeFileSync(indexPath, JSON.stringify(index, null, 2) + "\n");
}

main().catch((err) => {
  console.error(err.stack || err.message || err);
  process.exit(1);
});
