#!/usr/bin/env node
/**
 * Question banks for the mock exam builder (/academics/mock-exam/).
 *
 * Reads every course's exam pages (docs/academics/<track>/<course>/exams/**),
 * pulls out the questions they already contain and writes one bank per course
 * to docs/academics/mock-exam/banks/<course>.json, plus banks/index.json with
 * the course list.
 *
 * The quizzes come from many builders, so nothing here depends on one of them:
 *   - JS data: any array literal of question objects in an inline script (or a
 *     local *.js beside the page) is evaluated in a sandbox, and its fields are
 *     mapped by name (q/question/prompt/stem/text, options/opts/o/choices,
 *     correct/answer/ans/a/c/key, why/explain/explanation/exp/ex/e, ...).
 *   - Markup: radio groups with a data-correct / data-answer marker, or with an
 *     answer key object in the page's script keyed by the radio name (q1: ...).
 *     Written questions with a model answer come along as self-marked.
 *
 * Each question is tagged with a chapter id from the course's exam analysis
 * (docs/account/calendar/exam-analysis/<course>-final.json), so mock exam
 * scores line up with the calendar's Study Plan chapters. Exam scopes from the
 * same file become the "Midterm / Final" presets.
 *
 * ETHCS303 (paid, sealed at deploy) and the worked-problem math exams are left
 * out. Matching questions are not supported yet and are skipped.
 *
 *     node scripts/build-mock-exam-banks.js            # write every bank
 *     node scripts/build-mock-exam-banks.js --report   # also print where each page's questions went
 *     node scripts/build-mock-exam-banks.js se423      # only these courses (index.json keeps the rest)
 */
"use strict";

const fs = require("fs");
const path = require("path");
const vm = require("vm");

const ROOT = path.resolve(__dirname, "..");
const DOCS = path.join(ROOT, "docs");
const ACADEMICS = path.join(DOCS, "academics");
const ANALYSIS = path.join(DOCS, "account", "calendar", "exam-analysis");
const OUT = path.join(ACADEMICS, "mock-exam", "banks");

// ETHCS303 is paid. CS223's papers are LaTeX worked problems whose data keeps
// the answer in the question field, so they don't make fair MCQs.
const SKIP_COURSES = new Set(["ethcs303", "cs223"]);
const SKIP_TRACKS = new Set(["review", "study-pack", "mock-exam"]);
// Worked math problems (interactive-exam.html) are marked by hand on paper.
const SKIP_FILES = /(^|[\\/])interactive-exam\.html$/;
const MIN_QUESTIONS = 10;

// ETHCS303 is paid: its pages in docs/ are access gates. The real exams live in
// the private source (git-ignored), and its bank is written there too, next to
// the lessons, so the course-access Worker serves it only to approved buyers at
// /academics/other-courses/ethcs303/mock-exam-bank.json. It never goes in docs/.
// Without the private source (e.g. in CI) the existing index entry is kept.
const ETHICS_COURSE = "ethcs303";
const ETHICS_REL = path.join("academics", "other-courses", "ethcs303");
const ETHICS_BANK_URL = "/academics/other-courses/ethcs303/mock-exam-bank.json";
// Chapters and matching rules from scripts/ethics_course_structure.py (CHAPTERS, chapter()).
const ETHICS_CHAPTERS = [
  "Introduction · Moral Systems & Ethical Concepts",
  "Chapter 2 · Ethical Theories",
  "Professional Ethics",
  "Chapter 4 · Systems Analysis & Software Development",
  "Network Security & Privacy",
  "Chapter 7 · Privacy in Cyberspace & Cloud Computing",
  "Chapter 8 · Social Media Ethics & Security",
  "Chapter 9 · Business Ethics",
  "Chapter 9 · Social Engineering",
  "Chapter 9 · Ethical Hacking",
  "Chapter 10 · Intellectual Property",
  "Chapter 11 · Cyber Law in Saudi Arabia",
];
const ETHICS_RULES = [
  [9, ["ethical hacking"]], [7, ["business ethics"]],
  [6, ["social media"]], [5, ["cloud", "cyberspace", "privacy policies"]],
  [3, ["systems analysis", "software engineering", "ethical security issues", "sa and sd"]],
  [2, ["professional", "acm", "ieee", "whistle"]],
  [4, ["network security"]],
  [8, ["social engineering", "phishing", "smishing", "vishing", "impersonation", "dumpster", "fraud"]],
  [10, ["intellectual property", "patent", "trademark", "trade secret", "chapter 10"]],
  [11, ["cyber law"]],
  [1, ["kant", "utilitarian", "social contract", "divine command", "virtue ethics", "ethical theories", "moral theories"]],
  [0, ["moral systems", "introduction to ethics", "ethical concepts"]],
];
function ethicsChapter(text) {
  const v = String(text).toLowerCase().replace(/-/g, " ");
  if (v.includes("moral systems")) return 0;
  for (const [i, terms] of ETHICS_RULES) if (terms.some((t) => v.includes(t))) return i;
  return -1;
}

const args = process.argv.slice(2);
const REPORT = args.includes("--report");
const ONLY = new Set(args.filter((a) => !a.startsWith("--")).map((a) => a.toLowerCase()));
const ethicsArg = args.find((a) => a.startsWith("--ethics-src="));
const ETHICS_SRC = path.resolve(ROOT, ethicsArg ? ethicsArg.slice("--ethics-src=".length) : ".private-courses/ethics");

/* ------------------------------------------------------------------ files */

function isDir(p) {
  try {
    return fs.statSync(p).isDirectory();
  } catch (_) {
    return false;
  }
}
function list(dir) {
  try {
    return fs.readdirSync(dir).sort();
  } catch (_) {
    return [];
  }
}
function walkHtml(dir, out = []) {
  for (const name of list(dir)) {
    const full = path.join(dir, name);
    if (isDir(full)) walkHtml(full, out);
    else if (name.endsWith(".html") && name !== "index.html" && !SKIP_FILES.test(full)) out.push(full);
  }
  return out;
}
// The site root being read: docs/, or the private ETHCS303 source, whose
// files are served by the course-access Worker at the same URLs.
let SITE_ROOT = DOCS;
function urlOf(file) {
  return "/" + path.relative(SITE_ROOT, file).split(path.sep).join("/");
}
// The page a student opens: the folder when its index.html wraps this file.
function pageUrl(file) {
  const dir = path.dirname(file);
  const others = list(dir).filter((n) => n.endsWith(".html") && n !== "index.html");
  if (fs.existsSync(path.join(dir, "index.html")) && others.length === 1) return urlOf(dir) + "/";
  return urlOf(file).replace(/\.html$/, "");
}

/* --------------------------------------------------------------- text/html */

const ENTITIES = { amp: "&", lt: "<", gt: ">", quot: '"', apos: "'", nbsp: " ", ndash: "–", mdash: "—", rarr: "→", larr: "←", hellip: "…", times: "×", le: "≤", ge: "≥", ne: "≠" };
function decode(s) {
  return String(s).replace(/&(#x[0-9a-f]+|#\d+|[a-z]+);/gi, (m, e) => {
    if (e[0] === "#") {
      const n = e[1] === "x" || e[1] === "X" ? parseInt(e.slice(2), 16) : parseInt(e.slice(1), 10);
      return Number.isFinite(n) ? String.fromCodePoint(n) : m;
    }
    return ENTITIES[e.toLowerCase()] ?? m;
  });
}
function escapeHtml(s) {
  return String(s).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
}
const KEEP = new Set(["b", "strong", "i", "em", "u", "code", "sub", "sup", "br", "pre", "mark", "small", "img"]);
const LOOKS_HTML = /<\/?(?:b|strong|i|em|u|code|sub|sup|br|pre|span|p|div|mark|small|img|ul|ol|li)\b[^>]*>|&(?:#\d+|#x[0-9a-f]+|[a-z]+);/i;

/** Plain text or HTML in, a small safe HTML subset out. */
function cleanHtml(value, base) {
  if (value == null) return "";
  if (Array.isArray(value)) return value.map((v) => cleanHtml(v, base)).filter(Boolean).join("<br>");
  let s = String(value);
  // A few pages store prose with hyphens for spaces ("True.-Merge-Sort-always-...").
  if (!/\s/.test(s) && (s.match(/-/g) || []).length >= 4) s = s.replace(/-/g, " ");
  if (!LOOKS_HTML.test(s)) return escapeHtml(s.replace(/\s+/g, " ").trim());
  s = s.replace(/<(script|style)\b[\s\S]*?<\/\1>/gi, "").replace(/<!--[\s\S]*?-->/g, "");
  s = s.replace(/<(\/?)([a-z0-9]+)\b([^>]*)>/gi, (m, close, tag, attrs) => {
    tag = tag.toLowerCase();
    if (tag === "p" || tag === "div" || tag === "li" || tag === "tr") return close ? " " : " ";
    if (!KEEP.has(tag)) return "";
    if (tag === "br") return "<br>";
    if (tag === "img") {
      const src = /\bsrc\s*=\s*["']([^"']+)["']/i.exec(attrs);
      const alt = /\balt\s*=\s*["']([^"']*)["']/i.exec(attrs);
      if (!src || close) return "";
      const url = resolveUrl(src[1], base);
      return url ? `<img src="${escapeHtml(url)}" alt="${escapeHtml(alt ? alt[1] : "")}">` : "";
    }
    return `<${close}${tag}>`;
  });
  // Re-escape stray "<" that aren't one of the tags we kept.
  s = s.replace(/<(?!\/?(?:b|strong|i|em|u|code|sub|sup|br|pre|mark|small|img)\b)/gi, "&lt;");
  return s.replace(/\s+/g, " ").replace(/\s*<br>\s*/g, "<br>").trim();
}
function textOf(html) {
  return decode(String(html).replace(/<[^>]*>/g, " ")).replace(/\s+/g, " ").trim();
}
function resolveUrl(src, base) {
  if (!src || /^data:/i.test(src)) return "";
  if (/^https?:\/\//i.test(src)) return src;
  if (src.startsWith("/")) return src;
  if (!base) return "";
  return path.posix.normalize(path.posix.join(path.posix.dirname(base), src));
}

/* ------------------------------------------------------------ html parser */

const VOID = new Set(["area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "source", "track", "wbr"]);
const RAW = new Set(["script", "style", "textarea"]);

function parseHtml(src) {
  const root = { tag: "#root", attrs: {}, children: [], parent: null };
  let cur = root;
  const re = /<!--[\s\S]*?-->|<!\w[^>]*>|<\/([a-zA-Z][\w-]*)\s*>|<([a-zA-Z][\w-]*)((?:\s+[^\s=>\/]+(?:\s*=\s*(?:"[^"]*"|'[^']*'|[^\s>]+))?)*)\s*(\/?)>/g;
  let last = 0, m;
  while ((m = re.exec(src))) {
    if (m.index > last) cur.children.push({ text: src.slice(last, m.index) });
    last = re.lastIndex;
    if (m[1]) {
      const tag = m[1].toLowerCase();
      let n = cur;
      while (n && n.tag !== tag) n = n.parent;
      if (n && n.parent) cur = n.parent;
      continue;
    }
    if (!m[2]) continue;
    const tag = m[2].toLowerCase();
    const attrs = {};
    const ar = /([^\s=>\/]+)(?:\s*=\s*(?:"([^"]*)"|'([^']*)'|([^\s>]+)))?/g;
    let a;
    while ((a = ar.exec(m[3] || ""))) attrs[a[1].toLowerCase()] = decode(a[2] ?? a[3] ?? a[4] ?? "");
    const el = { tag, attrs, children: [], parent: cur };
    cur.children.push(el);
    if (RAW.has(tag)) {
      const end = src.toLowerCase().indexOf("</" + tag, last);
      const stop = end < 0 ? src.length : end;
      el.children.push({ text: src.slice(last, stop) });
      const close = src.indexOf(">", stop);
      last = re.lastIndex = close < 0 ? src.length : close + 1;
      continue;
    }
    if (!VOID.has(tag) && !m[4]) cur = el;
  }
  if (last < src.length) cur.children.push({ text: src.slice(last) });
  return root;
}
function* nodes(el) {
  for (const c of el.children || []) {
    if (c.tag) {
      yield c;
      yield* nodes(c);
    }
  }
}
function cls(el) {
  return " " + (el.attrs.class || "") + " ";
}
function hasCls(el, re) {
  return re.test(el.attrs.class || "");
}
function innerHtml(el) {
  let out = "";
  for (const c of el.children || []) {
    if (!c.tag) out += c.text;
    else if (c.tag === "script" || c.tag === "style") continue;
    else {
      const attrs = c.tag === "img" ? ` src="${escapeHtml(c.attrs.src || "")}" alt="${escapeHtml(c.attrs.alt || "")}"` : "";
      out += VOID.has(c.tag) ? `<${c.tag}${attrs}>` : `<${c.tag}>${innerHtml(c)}</${c.tag}>`;
    }
  }
  return out;
}
function contains(a, b) {
  for (let n = b; n; n = n.parent) if (n === a) return true;
  return false;
}
function closest(el, test) {
  for (let n = el; n && n.tag !== "#root"; n = n.parent) if (test(n)) return n;
  return null;
}

/* -------------------------------------------------------------- js data */

function matchBracket(s, i) {
  let depth = 0, q = null;
  for (let j = i; j < s.length; j++) {
    const c = s[j];
    if (q) {
      if (c === "\\") { j++; continue; }
      if (c === q) q = null;
      continue;
    }
    if (c === '"' || c === "'" || c === "`") { q = c; continue; }
    if (c === "/" && s[j + 1] === "/") { j = s.indexOf("\n", j); if (j < 0) return -1; continue; }
    if (c === "/" && s[j + 1] === "*") { j = s.indexOf("*/", j + 2) + 1; if (j <= 0) return -1; continue; }
    if (c === "[" || c === "{" || c === "(") depth++;
    else if (c === "]" || c === "}" || c === ")") {
      depth--;
      if (depth === 0) return j;
    }
  }
  return -1;
}
/** Every `name = [ ... ]` / `name = { ... }` literal in a script that evaluates on its own. */
function literals(script) {
  const out = [];
  const re = /(?:(?:const|let|var)\s+([A-Za-z_$][\w$]*)|((?:window\.)?[A-Z_$][\w$]*))\s*=\s*([\[{])/g;
  let m;
  while ((m = re.exec(script))) {
    const st = re.lastIndex - 1, en = matchBracket(script, st);
    if (en < 0) continue;
    try {
      const v = vm.runInNewContext("(" + script.slice(st, en + 1) + ")", {}, { timeout: 250 });
      out.push({ name: m[1] || m[2], value: v });
      re.lastIndex = en + 1;
    } catch (_) {
      /* uses functions or variables from the page: not plain data */
    }
  }
  return out;
}

const Q_KEYS = ["q", "question", "prompt", "stem", "text", "statement"];
const O_KEYS = ["options", "opts", "o", "choices"];
const A_KEYS = ["correct", "answer", "ans", "a", "c", "key", "accept", "accepted"];
const E_KEYS = ["why", "explain", "explanation", "exp", "ex", "e", "rationale"];
const M_KEYS = ["modelAnswer", "modelAns", "model", "mockAnswer", "sampleAnswer", "solution"];
const T_KEYS = ["ch", "chapter", "topic", "tag", "section", "src", "s", "source"];
function pick(o, keys) {
  for (const k of keys) if (o[k] !== undefined && o[k] !== null && o[k] !== "") return o[k];
  return undefined;
}
function looksLikeQuestions(arr) {
  const objs = arr.filter((x) => x && typeof x === "object" && !Array.isArray(x));
  return objs.length > 0 && objs.filter((o) => typeof pick(o, Q_KEYS) === "string").length >= Math.max(1, objs.length * 0.6);
}
function questionArrays(v, out, depth = 0, ctx = {}) {
  if (depth > 6 || !v || typeof v !== "object") return out;
  if (Array.isArray(v)) {
    if (looksLikeQuestions(v)) {
      out.push({ items: v, ctx });
      return out;
    }
    v.forEach((x) => questionArrays(x, out, depth + 1, ctx));
    return out;
  }
  // A section object ({title, qs: [...]}) passes its title down as the topic.
  const title = typeof v.title === "string" ? v.title : typeof v.name === "string" ? v.name : ctx.topic;
  for (const k of Object.keys(v)) questionArrays(v[k], out, depth + 1, { topic: title, ch: v.ch ?? ctx.ch });
  return out;
}
/** `{ q1: {ans: "B", explanation}, q2: "C" }` answer keys, by radio name. */
function answerKeys(v, out) {
  if (!v || typeof v !== "object" || Array.isArray(v)) return out;
  const keys = Object.keys(v);
  if (keys.length && keys.filter((k) => /^q[_-]?\d+[a-z]?$/i.test(k)).length >= keys.length * 0.6) {
    for (const k of keys) {
      const x = v[k];
      if (typeof x === "string" || typeof x === "number" || typeof x === "boolean") out[k.toLowerCase()] = { ans: x };
      else if (x && typeof x === "object") out[k.toLowerCase()] = { ans: pick(x, A_KEYS), explain: pick(x, E_KEYS), model: pick(x, M_KEYS) };
    }
  }
  return out;
}

/* ------------------------------------------------------------- normalize */

const LETTERS = "abcdefghijklmnopqrstuvwxyz";
function optionText(o) {
  if (o == null) return "";
  if (typeof o === "string" || typeof o === "number") return String(o);
  if (Array.isArray(o)) return o.length >= 2 ? String(o[1]) : String(o[0] ?? "");
  if (typeof o === "object") return String(pick(o, ["t", "text", "label", "option", "value", "html"]) ?? "");
  return "";
}
function optionKey(o, i) {
  if (Array.isArray(o) && o.length >= 2) return String(o[0]).toLowerCase();
  if (o && typeof o === "object" && !Array.isArray(o) && (o.id || o.key)) return String(o.id || o.key).toLowerCase();
  return LETTERS[i];
}
function stripMarker(s) {
  return String(s).replace(/^\s*(?:\(?[a-h]\)|[a-h][.)]|\(?(?:i|ii|iii|iv|v|vi)\)|(?:i|ii|iii|iv|v|vi)\.)\s+/i, "");
}
/** Index of the correct option from whatever the page stored. */
function answerIndex(ans, opts, keys) {
  if (typeof ans === "number" && Number.isInteger(ans)) return ans >= 0 && ans < opts.length ? ans : -1;
  if (typeof ans === "boolean") {
    const t = opts.findIndex((o) => /^\s*true\s*$/i.test(textOf(o)));
    const f = opts.findIndex((o) => /^\s*false\s*$/i.test(textOf(o)));
    return ans ? t : f;
  }
  if (typeof ans !== "string") return -1;
  const a = ans.trim();
  if (/^\d+$/.test(a) && +a < opts.length && !opts.some((o) => textOf(o) === a)) return +a;
  const low = a.toLowerCase();
  let i = keys.indexOf(low);
  if (i >= 0) return i;
  if (/^[a-h]$/i.test(a)) return LETTERS.indexOf(low) < opts.length ? LETTERS.indexOf(low) : -1;
  if (low === "true" || low === "false" || low === "t" || low === "f") return answerIndex(low[0] === "t", opts, keys);
  const plain = textOf(a).toLowerCase();
  i = opts.findIndex((o) => textOf(o).toLowerCase() === plain);
  if (i >= 0) return i;
  // "b) Transport" or "B - ..." style keys.
  const lead = /^\(?([a-h])[).:\s-]/i.exec(a);
  return lead ? LETTERS.indexOf(lead[1].toLowerCase()) : -1;
}

/**
 * One question object (any of the shapes above) to the bank format:
 *   { t: "mcq"|"tf"|"multi"|"fill"|"written", q, o?, a, m?, e?, hint? }
 * a is the option index (mcq/tf), sorted indexes (multi) or accepted answers
 * (fill). Returns null when the answer can't be worked out.
 */
function normalize(raw, ctx, base) {
  if (!raw || typeof raw !== "object") return null;
  const qText = pick(raw, Q_KEYS);
  if (typeof qText !== "string" || textOf(qText).length < 6) return null;
  let type = String(raw.type || raw.kind || "").toLowerCase();
  const rawOpts = pick(raw, O_KEYS);
  let ans = pick(raw, A_KEYS);
  const explainRaw = pick(raw, E_KEYS);
  const model = pick(raw, M_KEYS);
  const hint = [pick(raw, T_KEYS), ctx.topic, ctx.ch].filter((x) => x != null && x !== "").map(String);
  const q = { q: cleanHtml(qText, base) };
  if (raw.figure || raw.image || raw.img) {
    const f = raw.figure || raw.image || raw.img;
    const src = typeof f === "string" ? f : f && (f.src || f.url);
    const url = resolveUrl(src, base);
    if (url) q.q += `<br><img src="${escapeHtml(url)}" alt="">`;
    else if (f) return null; // refers to a figure we can't show
  }
  if (raw.past || raw.pastExam) q.p = 1;

  let opts = null, keys = null;
  if (Array.isArray(rawOpts)) {
    opts = rawOpts.map((o) => cleanHtml(stripMarker(optionText(o)), base));
    keys = rawOpts.map(optionKey);
  } else if (rawOpts && typeof rawOpts === "object") {
    keys = Object.keys(rawOpts).map((k) => k.toLowerCase());
    opts = Object.values(rawOpts).map((o) => cleanHtml(stripMarker(optionText(o)), base));
  }
  if (!opts && (type === "tf" || type === "true-false" || type === "truefalse" || typeof ans === "boolean")) {
    opts = ["True", "False"];
    keys = ["true", "false"];
    type = "tf";
  }

  let explain = explainRaw;
  if (Array.isArray(explainRaw)) explain = undefined; // per-option reasons; picked below

  if (opts && opts.length >= 2 && !/^(fill|short|essay|written|long)/.test(type)) {
    if (opts.some((o) => !o)) return null;
    if (type === "multi" || type === "multiple" || type === "checkbox" || Array.isArray(ans)) {
      const list = (Array.isArray(ans) ? ans : [ans]).map((x) => answerIndex(x, opts, keys));
      if (!list.length || list.some((i) => i < 0)) return null;
      q.t = list.length > 1 ? "multi" : "mcq";
      q.a = list.length > 1 ? [...new Set(list)].sort((a, b) => a - b) : list[0];
    } else {
      const i = answerIndex(ans, opts, keys);
      if (i < 0) return null;
      q.t = opts.length === 2 && opts.every((o) => /^(true|false)$/i.test(textOf(o))) ? "tf" : "mcq";
      q.a = i;
      if (Array.isArray(explainRaw) && explainRaw[i]) explain = explainRaw[i];
      if (!explain && Array.isArray(rawOpts) && rawOpts[i] && typeof rawOpts[i] === "object" && rawOpts[i].why) explain = rawOpts[i].why;
    }
    q.o = opts;
  } else if (/^fill/.test(type) || (type === "" && Array.isArray(raw.accept || raw.accepted))) {
    let acc = raw.accept || raw.accepted || raw.kw || ans;
    acc = (Array.isArray(acc) ? acc : [acc]).filter((x) => typeof x === "string" && x.trim()).map((x) => textOf(x));
    if (typeof ans === "string" && !acc.includes(textOf(ans))) acc.unshift(textOf(ans));
    if (!acc.length) return null;
    q.t = "fill";
    q.a = [...new Set(acc)];
  } else {
    const m = model || (typeof ans === "string" && textOf(ans).length > 20 ? ans : undefined);
    if (!m) return null;
    q.t = "written";
    q.m = cleanHtml(m, base);
  }
  const e = typeof explain === "string" ? cleanHtml(explain, base) : "";
  if (e) q.e = e;
  q._hint = hint;
  return q;
}

/* ----------------------------------------------------------- markup quizzes */

const QTEXT_CLS = /(^|\s)(q-text|question-text|q-stem|stem|prompt|q-prompt|q-title|question-title|mcq-prompt|written-label)(\s|$)/;
const EXPLAIN_CLS = /(^|\s)(explanation|explain|why|feedback|answer-explanation|rationale)(\s|$)/;
const MODEL_CLS = /(^|\s)(model-answer|model-answer-content|sample-answer|model|answer-key)(\s|$)/;
const NOISE_CLS = /(^|\s)(question-number|q-num|num|number|marks|points|q-pts|question-points|tag|badge|chip|past-exam-badge|past-exam-tag|generated-tag|ch-tag|n|ol|option-circle|option-marker|q-number|key-label)(\s|$)/;

function cleanText(el, dropOptions) {
  const copy = (function clone(n) {
    if (!n.tag) return { text: n.text };
    if (n.tag === "input" || n.tag === "button" || n.tag === "textarea" || n.tag === "script" || n.tag === "style") return null;
    if (hasCls(n, NOISE_CLS)) return null;
    if (dropOptions && (hasCls(n, EXPLAIN_CLS) || hasCls(n, MODEL_CLS) || n.tag === "label" || hasCls(n, /(^|\s)(options?|opts|choices|options-list|mcq-options|tf-options)(\s|$)/))) return null;
    return { tag: n.tag, attrs: n.attrs, children: n.children.map(clone).filter(Boolean) };
  })(el);
  return copy ? innerHtml(copy) : "";
}
function stripExplainLabel(h) {
  let prev;
  do {
    prev = h;
    h = h
      .replace(/^\s*(?:<(strong|b)>\s*)?(?:explanation|why|answer explanation)\s*:?\s*(?:<\/\1>)?\s*:?\s*/i, "")
      .replace(/^\s*<(strong|b)>\s*correct answer\s*:?[^<]*<\/\1>\s*(?:<br>)?\s*[-–:.]?\s*/i, "")
      .replace(/^\s*correct answer\s*:\s*\(?[a-h]\)?(?=[\s.:-])[.:\s-]*/i, "")
      .replace(/^\s*<br>\s*/i, "");
  } while (h !== prev);
  return h.trim();
}
function explanationOf(box, base) {
  for (const n of nodes(box)) {
    if (hasCls(n, EXPLAIN_CLS)) {
      // Headings and blocks become spaces first, so the label is at the start.
      const h = stripExplainLabel(cleanHtml(cleanText(n, false).replace(/<\/?h\d>/gi, " "), base));
      if (textOf(h)) return h;
    }
  }
  return "";
}
function correctMarker(box, stop) {
  const own = box.attrs["data-correct"] ?? box.attrs["data-answer"] ?? box.attrs["data-ans"];
  if (own != null && own !== "") return own;
  for (const n of nodes(box)) {
    if (stop && stop(n)) continue;
    const v = n.attrs["data-correct"] ?? n.attrs["data-answer"] ?? n.attrs["data-ans"];
    if (v != null && v !== "" && n.tag !== "input") return v;
  }
  return null;
}
function questionTextOf(box) {
  for (const n of nodes(box)) if (hasCls(n, QTEXT_CLS)) return cleanText(n, true);
  // First paragraph or header that isn't an option, explanation or badge.
  for (const n of nodes(box)) {
    if (!/^(p|h3|h4|legend|div|span)$/.test(n.tag)) continue;
    if (closest(n, (x) => x.tag === "label" || hasCls(x, EXPLAIN_CLS) || hasCls(x, MODEL_CLS) || hasCls(x, /(^|\s)(options?|opts|choices)(\s|$)/))) continue;
    if (n.tag !== "p" && !hasCls(n, /question-header|q-head|card-head/)) continue;
    const h = cleanText(n, true);
    if (textOf(h).length >= 8) return h;
  }
  return "";
}

function markupQuestions(html, keys, base) {
  const root = parseHtml(html);
  const radios = [...nodes(root)].filter((n) => n.tag === "input" && /^(radio|checkbox)$/i.test(n.attrs.type || "") && n.attrs.name);
  const groups = new Map();
  for (const r of radios) {
    if (!groups.has(r.attrs.name)) groups.set(r.attrs.name, []);
    groups.get(r.attrs.name).push(r);
  }
  const out = [];
  const used = new Set();
  for (const [name, inputs] of groups) {
    if (inputs.length < 2) continue;
    // Smallest ancestor holding the whole group, grown until it holds a prompt.
    let box = inputs[0].parent;
    while (box && !inputs.every((i) => contains(box, i))) box = box.parent;
    let qHtml = "";
    for (let n = box, hops = 0; n && n.tag !== "#root" && hops < 6; n = n.parent, hops++) {
      const other = radios.some((r) => r.attrs.name !== name && contains(n, r));
      if (other) break;
      box = n;
      qHtml = questionTextOf(n);
      if (qHtml && (correctMarker(n) != null || keys[name.toLowerCase()] || inputs.some((i) => i.attrs["data-correct"]))) break;
    }
    if (!box || used.has(box) || !qHtml) continue;
    used.add(box);
    const opts = [], vals = [];
    for (const inp of inputs) {
      const label = closest(inp, (x) => x.tag === "label") || (inp.attrs.id && [...nodes(box)].find((x) => x.tag === "label" && x.attrs.for === inp.attrs.id)) || inp.parent;
      opts.push(cleanHtml(stripMarker(textOf(cleanText(label, false)) ? cleanText(label, false) : ""), base));
      vals.push(String(inp.attrs.value ?? "").toLowerCase());
    }
    const key = keys[name.toLowerCase()];
    // Some pages mark the right input itself: <input ... data-correct="true">.
    const flagged = inputs.filter((i) => /^(true|1|yes|correct)$/i.test(i.attrs["data-correct"] || i.attrs["data-answer"] || ""));
    const marker = flagged.length ? flagged.map((i) => String(i.attrs.value ?? "")).join(",") : correctMarker(box, (n) => n.tag === "input");
    const ans = marker != null ? marker : key && key.ans;
    if (ans == null) continue;
    const isMulti = inputs[0].attrs.type.toLowerCase() === "checkbox";
    const parts = isMulti ? String(ans).split(/[\s,|]+/).filter(Boolean) : [String(ans)];
    const idx = parts.map((p) => {
      const v = vals.indexOf(p.toLowerCase());
      return v >= 0 ? v : answerIndex(p, opts, vals);
    });
    if (idx.some((i) => i < 0) || opts.some((o) => !textOf(o))) continue;
    const q = { q: cleanHtml(qHtml, base), o: opts };
    if (idx.length > 1) { q.t = "multi"; q.a = idx.sort((a, b) => a - b); }
    else { q.a = idx[0]; q.t = opts.length === 2 && opts.every((o) => /^(true|false)$/i.test(textOf(o))) ? "tf" : "mcq"; }
    // The explanation can sit just outside the prompt's box (CS331 papers).
    let e = "";
    for (let n = box, hops = 0; n && n.tag !== "#root" && hops < 3 && !e; n = n.parent, hops++) {
      if (hops && radios.some((r) => r.attrs.name !== name && contains(n, r))) break;
      e = explanationOf(n, base);
    }
    if (!e && key && key.explain) e = cleanHtml(key.explain, base);
    if (e) q.e = e;
    if (/past/i.test(cls(box)) || [...nodes(box)].some((n) => hasCls(n, /past-exam/))) q.p = 1;
    q._hint = [box.attrs["data-ch"], box.attrs["data-chapter"], box.attrs["data-topic"]].filter(Boolean).concat(
      [...nodes(box)].filter((n) => hasCls(n, /(^|\s)ch-tag(\s|$)/)).map((n) => textOf(innerHtml(n))),
    );
    out.push(q);
  }
  // Written questions: a textarea next to a model answer.
  for (const ta of [...nodes(root)].filter((n) => n.tag === "textarea")) {
    let box = ta.parent, modelEl = null;
    for (let hops = 0; box && box.tag !== "#root" && hops < 4; box = box.parent, hops++) {
      if (radios.some((r) => contains(box, r))) { box = null; break; }
      modelEl = [...nodes(box)].find((n) => hasCls(n, MODEL_CLS));
      if (modelEl) break;
    }
    if (!box || !modelEl || used.has(box)) continue;
    const content = [...nodes(modelEl)].find((n) => hasCls(n, /model-answer-content/)) || modelEl;
    const model = cleanHtml(cleanText(content, false).replace(/^\s*<h\d>[\s\S]*?<\/h\d>/i, ""), base);
    const qHtml = questionTextOf(box);
    if (!textOf(model) || !qHtml) continue;
    used.add(box);
    // A shared scenario above several written parts belongs to each part's question.
    let scenario = "";
    for (let n = box.parent, hops = 0; n && n.tag !== "#root" && hops < 2 && !scenario; n = n.parent, hops++) {
      const sc = [...nodes(n)].find((x) => hasCls(x, /(^|\s)(scenario-box|scenario|case-study|passage)(\s|$)/) && !contains(box, x));
      if (sc) scenario = cleanText(sc, false);
    }
    const qFull = scenario ? cleanHtml(scenario, base) + "<br><br>" + cleanHtml(qHtml, base) : cleanHtml(qHtml, base);
    out.push({ t: "written", q: qFull, m: model, _hint: [box.attrs["data-ch"]].filter(Boolean) });
  }
  return out;
}

/* --------------------------------------------------------------- chapters */

const STOP = new Set("a an and the of in on to for with by from vs quiz quizzes chapter chapters ch lecture lectures topic topics practice exam exams test part section question questions intro introduction basics overview final midterm major paper mock review set bank version".split(" "));
function tokens(s) {
  return String(s)
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, " ")
    .split(" ")
    .filter((w) => w && !STOP.has(w) && !/^\d+$/.test(w))
    .map((w) => w.replace(/(ies)$/, "y").replace(/([^s])s$/, "$1"));
}
function loadChapters(course) {
  if (course === ETHICS_COURSE) {
    const chapters = ETHICS_CHAPTERS.map((title, i) => ({ id: "e" + i, title, num: "", kind: "", tok: new Set(tokens(title)), link: "" }));
    return { chapters, scopes: [], name: "ETHCS 303", ethics: true };
  }
  const file = path.join(ANALYSIS, course + "-final.json");
  if (!fs.existsSync(file)) return { chapters: [], scopes: [], name: "" };
  const d = JSON.parse(fs.readFileSync(file, "utf8"));
  const chapters = (d.chapters || []).map((c) => {
    const m = /^(Ch|Chapter|Lecture|Topic|L)\.?\s*([\d.]+)/i.exec(c.title || "");
    return {
      id: c.id,
      title: c.title,
      num: m ? m[2].replace(/\.$/, "") : "",
      kind: m ? m[1].toLowerCase() : "",
      tok: new Set(tokens((c.title || "").replace(/^[^·]*·/, ""))),
      link: ((c.links || [])[0] || {}).url || "",
    };
  });
  const scopes = (d.exam_scopes || [])
    .map((s) => ({ label: s.label, type: s.type, chapters: (s.chapters || []).filter((id) => chapters.some((c) => c.id === id)) }))
    .filter((s) => s.chapters.length);
  return { chapters, scopes, name: d.course || "" };
}
function byNumber(chapters, n) {
  if (n == null || n === "") return null;
  const s = String(n).replace(/^0+(?=\d)/, "");
  return chapters.find((c) => c.num === s) || null;
}
/** Chapter named in a hint like "Ch 3", "Ch.1 · Components", "L1 · Block 2", 4, "Lecture 2". */
function chapterFromHint(chapters, hint) {
  if (typeof hint === "number" || /^\s*\d+(\.\d+)?\s*$/.test(hint)) return byNumber(chapters, String(hint).trim());
  const m = /\b(?:ch(?:apter)?|lecture|lec|topic|l)\.?\s*(\d+(?:\.\d+)?)/i.exec(hint);
  if (m) return byNumber(chapters, m[1]) || byNumber(chapters, m[1].split(".")[0]);
  return null;
}
function chapterFromWords(chapters, text) {
  const t = tokens(text);
  if (!t.length) return null;
  const words = new Set(t);
  let best = null, bestScore = 0, tie = false;
  for (const c of chapters) {
    const hit = [...words].filter((w) => c.tok.has(w)).length;
    // The chapter title must hold most of the words ("development approach"
    // is in "Development approach, agile, Scrum and DevOps"); among those,
    // the closest title wins, so "asymptotic notation practice" doesn't take
    // a page about "algorithm analysis and asymptotic notation".
    if (hit / words.size < 0.6) continue;
    const score = hit / (words.size + c.tok.size - hit);
    if (score > bestScore) { best = c; bestScore = score; tie = false; }
    else if (score === bestScore) tie = true;
  }
  return best && !tie ? best : null;
}
/** Chapter a page is about, when it's about exactly one. */
function pageChapter(chapters, file, title) {
  const slug = path.basename(path.dirname(file)) + " " + path.basename(file, ".html");
  const multi = /chapters?[-\s]+\d+[-\s]+(?:and|to|&)?[-\s]*\d+|midterm|final|major|exam-\d|paper|comprehensive|semester|\d{3}\b|quiz-\d/i;
  const name = path.basename(file, ".html");
  const m = /(?:^|[-_ ])(?:chapter|ch|lecture|lec|topic)[-_ ]?(\d+(?:[-_.]\d+)?)(?=$|[-_ ])/i.exec(name) || /(?:^|[-_ ])(?:chapter|ch|lecture|lec|topic)[-_ ]?(\d+)(?=$|[-_ ])/i.exec(slug);
  if (m && !/chapters?-\d+-(?:and|to)?-?\d+/i.test(slug)) {
    const c = byNumber(chapters, m[1].replace(/[-_]/, ".")) || byNumber(chapters, m[1].split(/[-_.]/)[0]);
    if (c) return c;
  }
  if (multi.test(slug)) return null;
  return chapterFromWords(chapters, name.replace(/^\d+-/, "")) || chapterFromWords(chapters, title || "");
}

/* --------------------------------------------------------------- per page */

function pageTitle(html, file) {
  const h1 = /<h1\b[^>]*>([\s\S]*?)<\/h1>/i.exec(html);
  const t = /<title>([\s\S]*?)<\/title>/i.exec(html);
  let s = textOf(h1 ? h1[1] : t ? t[1] : "");
  if (!s || s.length > 90) s = textOf(t ? t[1] : "");
  s = s.replace(/\s*[|·—–-]\s*SHOUG\.TECH.*$/i, "").replace(/^SHOUG\.TECH\s*(?:\/\/|\||·)\s*/i, "").trim();
  if (!s) s = path.basename(file, ".html").replace(/^\d+-/, "").replace(/-/g, " ");
  return s.slice(0, 90);
}
function scriptsOf(html, file) {
  const out = [];
  const re = /<script\b([^>]*)>([\s\S]*?)<\/script>/gi;
  let m;
  while ((m = re.exec(html))) {
    if (/ld\+json/i.test(m[1])) continue;
    const src = /\bsrc\s*=\s*["']([^"']+)["']/i.exec(m[1]);
    if (!src) { out.push(m[2]); continue; }
    // Local data files beside the page (e.g. final-242-bank.js), not site-wide scripts.
    if (/^(https?:)?\/\//i.test(src[1]) || src[1].startsWith("/")) continue;
    const local = path.resolve(path.dirname(file), src[1].split("?")[0]);
    if (local.startsWith(path.dirname(path.dirname(file))) && fs.existsSync(local)) out.push(fs.readFileSync(local, "utf8"));
  }
  return out;
}

function extractPage(file) {
  const html = fs.readFileSync(file, "utf8");
  const base = urlOf(file);
  const found = [];
  const keys = {};
  for (const script of scriptsOf(html, file)) {
    for (const { value } of literals(script)) {
      for (const { items, ctx } of questionArrays(value, [])) {
        for (const raw of items) {
          const q = normalize(raw, ctx, base);
          if (q) found.push(q);
        }
      }
      answerKeys(value, keys);
    }
  }
  if (!found.length) found.push(...markupQuestions(html, keys, base));
  return { html, found, title: pageTitle(html, file) };
}

// "What does the following code do?" with the code left behind on the page.
const NEEDS_CONTEXT = /\b(?:following|below|above|shown|given|this|attached)\s+(?:code|figure|diagram|table|graph|program|snippet|output|class|method|function|query|queries|schema|relations?|tree|network|image|picture|chart|er diagram|erd|scenario|case|data ?set|pseudo-?code|algorithm)\b|\b(?:in|from|see|use|using) the (?:figure|diagram|table|code|graph|image|chart|scenario)\b|\bfig(?:ure)?\.?\s*\d/i;
function missingContext(q) {
  if (/<(?:pre|img|code)\b/i.test(q.q)) return false;
  return NEEDS_CONTEXT.test(textOf(q.q));
}

/* ------------------------------------------------------------------- main */

function hash(s) {
  let h = 2166136261;
  for (let i = 0; i < s.length; i++) {
    h ^= s.charCodeAt(i);
    h = Math.imul(h, 16777619);
  }
  return (h >>> 0).toString(36);
}
function courseDirs() {
  const out = [];
  for (const track of list(ACADEMICS)) {
    const tdir = path.join(ACADEMICS, track);
    if (SKIP_TRACKS.has(track) || !isDir(tdir)) continue;
    for (const course of list(tdir)) {
      const exams = path.join(tdir, course, "exams");
      if (SKIP_COURSES.has(course) || !isDir(exams)) continue;
      out.push({ track, course, exams });
    }
  }
  return out;
}
function displayName(course, fromAnalysis) {
  if (fromAnalysis) return fromAnalysis;
  const m = /^([a-z]+)(\d+)$/i.exec(course);
  return m ? m[1].toUpperCase() + " " + m[2] : course.toUpperCase();
}

function buildCourse({ track, course, exams }) {
  const { chapters, scopes, name, ethics } = loadChapters(course);
  const sources = [];
  const questions = [];
  const seen = new Set();
  const report = [];
  let dropped = 0;
  for (const file of walkHtml(exams)) {
    let page;
    try {
      page = extractPage(file);
    } catch (e) {
      report.push(`  ! ${path.relative(exams, file)}: ${e.message}`);
      continue;
    }
    if (!page.found.length) continue;
    let pageCh;
    if (ethics) {
      // Topic quizzes take the page's chapter; mixed papers go question by question.
      const mixed = /quiz-\d|major|final|practice|bank|section/i.test(path.basename(path.dirname(file)));
      const i = mixed ? -1 : ethicsChapter(path.basename(path.dirname(file)) + " " + page.title);
      pageCh = i >= 0 ? chapters[i] : null;
    } else pageCh = pageChapter(chapters, file, page.title);
    const srcIndex = sources.push({ title: page.title, url: pageUrl(file) }) - 1;
    const tally = {};
    let added = 0;
    for (const q of page.found) {
      if (missingContext(q)) { dropped++; continue; }
      if (q.t === "tf") {
        q.o = q.o.map((o) => (/^\s*true\s*$/i.test(textOf(o)) ? "True" : "False"));
        q.q = q.q.replace(/^\s*(?:true\s*(?:or|\/)\s*false|t\s*\/\s*f)\s*[:.)-]\s*/i, "");
      }
      if (q.e) q.e = stripExplainLabel(q.e);
      if (q.e === "") delete q.e;
      const keyText = textOf(q.q).toLowerCase().replace(/[^a-z0-9]+/g, " ").trim() + "|" + (q.o ? q.o.map((o) => textOf(o).toLowerCase()).join("|") : "");
      if (seen.has(keyText)) continue;
      seen.add(keyText);
      let ch = null;
      for (const h of q._hint || []) if ((ch = chapterFromHint(chapters, h))) break;
      if (!ch) ch = pageCh;
      if (!ch && ethics) {
        const i = ethicsChapter((q._hint || []).join(" ") + " " + textOf(q.q));
        if (i >= 0) ch = chapters[i];
      }
      if (!ch) for (const h of q._hint || []) if (typeof h === "string" && (ch = chapterFromWords(chapters, h))) break;
      delete q._hint;
      q.id = hash(course + "|" + keyText);
      q.c = ch ? ch.id : null;
      q.s = srcIndex;
      questions.push(q);
      tally[q.c || "—"] = (tally[q.c || "—"] || 0) + 1;
      added++;
    }
    report.push(`  ${String(added).padStart(4)}  ${path.relative(exams, file).split(path.sep).join("/")}  →  ${Object.entries(tally).map(([k, v]) => k + "×" + v).join(" ")}`);
  }
  // Keep only chapters that have questions, in course order.
  const usedCh = new Set(questions.map((q) => q.c).filter(Boolean));
  if (dropped) report.push(`  (${dropped} questions dropped: they point at a figure or code the page shows outside the question)`);
  return {
    bank: {
      course,
      name: displayName(course, name),
      page: `/academics/${track}/${course}/`,
      chapters: chapters.filter((c) => usedCh.has(c.id)).map((c) => (c.link ? { id: c.id, title: c.title, link: c.link } : { id: c.id, title: c.title })),
      scopes: scopes.map((s) => ({ ...s, chapters: s.chapters.filter((id) => usedCh.has(id)) })).filter((s) => s.chapters.length),
      sources,
      questions,
    },
    report,
  };
}

function summary(bank, extra) {
  const types = {};
  bank.questions.forEach((q) => (types[q.t] = (types[q.t] || 0) + 1));
  const tagged = bank.questions.filter((q) => q.c).length;
  console.log(`${bank.name.padEnd(9)} ${String(bank.questions.length).padStart(5)} questions, ${Math.round((100 * tagged) / bank.questions.length)}% tagged to a chapter, ${bank.sources.length} pages${extra || ""}`);
  return { course: bank.course, name: bank.name, count: bank.questions.length, tagged, types };
}

/** ETHCS303 from the private source; its bank stays private. Returns questions added. */
function buildEthics(previous, update) {
  const stray = path.join(OUT, ETHICS_COURSE + ".json");
  if (fs.existsSync(stray)) fs.unlinkSync(stray); // never public
  const exams = path.join(ETHICS_SRC, ETHICS_REL, "exams");
  const kept = previous.find((c) => c.course === ETHICS_COURSE);
  update((index) => index.filter((c) => c.course !== ETHICS_COURSE));
  if (!isDir(exams)) {
    if (kept) update((index) => index.concat([kept]));
    console.log(`ETHCS 303: private source not found at ${path.relative(ROOT, ETHICS_SRC) || "."}; ` + (kept ? "kept the existing index entry" : "not listed"));
    return 0;
  }
  SITE_ROOT = ETHICS_SRC;
  let built;
  try {
    built = buildCourse({ track: "other-courses", course: ETHICS_COURSE, exams });
  } finally {
    SITE_ROOT = DOCS;
  }
  const { bank, report } = built;
  if (bank.questions.length < MIN_QUESTIONS) {
    console.log(`ETHCS 303: only ${bank.questions.length} questions found, not listed`);
    return 0;
  }
  const file = path.join(ETHICS_SRC, ETHICS_REL, "mock-exam-bank.json");
  fs.writeFileSync(file, JSON.stringify(bank) + "\n");
  const entry = Object.assign(summary(bank, " (private: served by the course-access Worker)"), {
    track: "other-courses",
    locked: true,
    bank: ETHICS_BANK_URL,
  });
  update((index) => index.concat([entry]));
  if (REPORT) console.log(report.join("\n"));
  return bank.questions.length;
}

function main() {
  fs.mkdirSync(OUT, { recursive: true });
  const indexFile = path.join(OUT, "index.json");
  const previous = fs.existsSync(indexFile) ? JSON.parse(fs.readFileSync(indexFile, "utf8")).courses || [] : [];
  let index = ONLY.size ? previous.slice() : [];
  let total = 0;
  for (const dir of courseDirs()) {
    if (ONLY.size && !ONLY.has(dir.course)) continue;
    const { bank, report } = buildCourse(dir);
    index = index.filter((c) => c.course !== dir.course);
    const file = path.join(OUT, dir.course + ".json");
    if (bank.questions.length < MIN_QUESTIONS) {
      if (fs.existsSync(file)) fs.unlinkSync(file);
      if (REPORT && bank.questions.length) console.log(`${dir.course}: only ${bank.questions.length} questions, skipped`);
      continue;
    }
    fs.writeFileSync(file, JSON.stringify(bank) + "\n");
    index.push(Object.assign(summary(bank), { track: dir.track }));
    total += bank.questions.length;
    if (REPORT) console.log(report.join("\n"));
  }
  if (!ONLY.size || ONLY.has(ETHICS_COURSE)) total += buildEthics(previous, (fn) => (index = fn(index)));
  index.sort((a, b) => a.name.localeCompare(b.name, "en", { numeric: true }));
  fs.writeFileSync(indexFile, JSON.stringify({ generated: new Date().toISOString().slice(0, 10), courses: index }, null, 1) + "\n");
  console.log(`Mock exam banks: ${index.length} courses${ONLY.size ? "" : ", " + total + " questions"}`);
}

main();
