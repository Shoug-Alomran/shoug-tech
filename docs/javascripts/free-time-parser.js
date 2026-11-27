/**
 * Free time in plain words, for the schedule planner.
 *
 *   ShougFreeTime.parse("Thursdays off, nothing before 10, done by 2 on Mondays")
 *   → { rules: [{ days: [4], from: 420, to: 1320, label: "Thursday off" }, …],
 *       maxDays: null, preferGaps: false, unknown: [] }
 *
 * Understands common English and Arabic phrasing: days off, "before / after
 * <time>", "finish by <time>", ranges ("3-6", "from 1 to 3"), "only 9 to 2",
 * mornings / afternoons / evenings, "no 8 AMs", "except Sunday",
 * "only 3 days", "no gaps". Clauses it can't read come back in `unknown`;
 * the planner then asks the AI worker (/v1/free-time), which returns the same
 * shape.
 *
 * Times are minutes after midnight. Days: 0 Sunday … 4 Thursday.
 */
(function () {
  "use strict";

  var DAY_FULL = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday"];
  var DAY_SHORT = ["Sun", "Mon", "Tue", "Wed", "Thu"];
  var DAY_PATTERNS = [
    /\bsun(day)?s?\b|الأحد|الاحد|\bاحد\b/,
    /\bmon(day)?s?\b|الاثنين|الإثنين|اثنين/,
    /\btues?(day)?s?\b|الثلاثاء|الثلاثا|ثلاثاء/,
    /\bwed(nes|s)?(day)?s?\b|الأربعاء|الاربعاء|اربعاء/,
    /\bthu(rs?)?(day)?s?\b|الخميس|خميس/,
  ];
  var ALL_DAYS = /\b(every ?day|daily|weekdays|all days|any day|all week)\b|كل يوم|كل الايام|كل الأيام|يوميا|يومياً/;
  var DAY_START = 7 * 60;
  var DAY_END = 22 * 60;
  var NUM_WORDS = {
    one: 1, two: 2, three: 3, four: 4, five: 5,
    يومين: 2, ثلاث: 3, ثلاثة: 3, اربع: 4, أربع: 4, اربعة: 4, أربعة: 4, خمس: 5, خمسة: 5,
  };
  var TIME = "(\\d{1,2})(?::(\\d{2}))?\\s*(a\\.?m\\.?|p\\.?m\\.?|ص|م|صباحا|صباحاً|مساء|مساءً|الصبح|الظهر|العصر)?";
  var TIME_RE = new RegExp(TIME);
  var RANGE_RE = new RegExp(
    "(?:\\bfrom\\b|\\bbetween\\b|من|بين)?\\s*" + TIME +
      "\\s*(?:-|–|—|\\bto\\b|\\btill\\b|\\buntil\\b|\\band\\b|الى|إلى|لين|حتى|لحد|و)\\s*" + TIME,
  );
  var FINISH = /\b(finish|finished|end|ending|done|leave|out|home)\b|اخلص|أخلص|اطلع|أطلع|اروح|أروح|انتهي|أنتهي/;
  var BEFORE = /\b(start|begin|starting)\b.*\b(at|after|from)\b|\bbefore\b|\blater than\b|قبل|ابدأ|ابدا|أبدأ|ابدى|يبدأ|تبدأ|أصحى|اصحى/;
  var AFTER = /\b(after|past)\b|بعد/;
  var NEGATE = /\bno\b|\bnot\b|\bavoid\b|بدون|ما ابي|ماابي|\bلا\b/;
  var DAY_OFF = /\b(off|free|no|nothing|don'?t|dont|avoid|skip|not|without|empty|rest)\b|اجازة|إجازة|اجازه|فاضي|فاضية|فاضيه|بدون|ما ابي|ماابي|لا اريد|لا أريد|مافي|ما في|راحة|راحه|اوف|أوف/;
  var EXCEPT = /\b(except|apart from|other than|besides|but not)\b|ما عدا|ماعدا|\bعدا\b|\bالا\b|\bإلا\b|\bغير\b/;
  var FILLER = /^(i|i'?d|i would|i want|i'?d like|want|like|please|prefer|ideally|maybe|if possible)\b|^(ابي|أبي|ابغى|أبغى|اريد|أريد|لو سمحت|ياليت|يا ليت)/;

  function normalize(text) {
    return String(text || "")
      .toLowerCase()
      .replace(/[٠-٩]/g, function (d) { return String("٠١٢٣٤٥٦٧٨٩".indexOf(d)); })
      .replace(/\bnoon\b|\bmidday\b/g, "12:00pm")
      .replace(/[’`]/g, "'")
      .replace(/\s+/g, " ")
      .trim();
  }

  function toMinutes(h, min, suf) {
    h = +h;
    min = +(min || 0);
    suf = suf || "";
    if (h > 23 || min > 59) return null;
    if (/^p|^م|مساء|العصر/.test(suf)) { if (h < 12) h += 12; }
    else if (/^a|^ص|صباح|الصبح/.test(suf)) { if (h === 12) h = 0; }
    else if (/الظهر/.test(suf)) { if (h < 11) h += 12; }
    else if (h >= 1 && h <= 6) h += 12; // "after 2" at university means 2 PM
    return h * 60 + min;
  }

  function clock(mins) {
    var h = Math.floor(mins / 60), m = mins % 60;
    return (h % 12 || 12) + (m ? ":" + String(m).padStart(2, "0") : "") + (h >= 12 ? " PM" : " AM");
  }

  function daysIn(text) {
    if (ALL_DAYS.test(text)) return [0, 1, 2, 3, 4];
    var out = [];
    DAY_PATTERNS.forEach(function (re, i) { if (re.test(text)) out.push(i); });
    return out;
  }

  function daysLabel(days) {
    if (days.length === 5) return "";
    if (days.length === 1) return DAY_FULL[days[0]];
    var run = days.every(function (d, i) { return !i || d === days[i - 1] + 1; });
    if (run && days.length > 2) return DAY_SHORT[days[0]] + "–" + DAY_SHORT[days[days.length - 1]];
    return days.map(function (d) { return DAY_SHORT[d]; }).join(", ");
  }

  function splitClauses(text) {
    return text
      .split(/[,;.\n،؛]|\band\b|\bbut\b|\balso\b|\bplus\b| و(?=\s)| ولكن | لكن /)
      .map(function (c) { return c.trim(); })
      .filter(Boolean);
  }

  /** One clause → { days, except, actions: [...] }. */
  function readClause(clause) {
    var at = clause.search(EXCEPT);
    var main = at > -1 ? clause.slice(0, at) : clause;
    var found = { days: daysIn(main), except: at > -1 ? daysIn(clause.slice(at)) : [], actions: [] };
    var add = function (a) { found.actions.push(a); };

    if (/\b(no|fewer|less|without|minimi[sz]e|avoid)\s+(long\s+)?gaps?\b|\bcompact\b|back.to.back|بدون فراغات|بدون فراغ|متواصل|ورا بعض/.test(clause))
      add({ type: "gaps" });

    var nd = clause.match(/(\d|one|two|three|four|five|يومين|ثلاث|ثلاثة|اربع|أربع|اربعة|أربعة|خمس|خمسة)\s*(?:days?\b|ايام|أيام)/);
    if (nd && !/\bdays? off\b/.test(clause)) {
      var n = NUM_WORDS[nd[1]] || +nd[1];
      if (n >= 1 && n <= 5) add({ type: "maxDays", n: n });
    }

    var r = main.match(RANGE_RE);
    if (r) {
      var a = toMinutes(r[1], r[2], r[3]), b = toMinutes(r[4], r[5], r[6]);
      if (a != null && b != null) {
        if (b <= a && b + 720 > a) b += 720;
        if (/\bonly\b|\bjust\b|بس|فقط/.test(main))
          add({ type: "only", from: a, to: b });
        else add({ type: "range", from: a, to: b, kind: "range", label: "Free " + clock(a) + "–" + clock(b) });
        return found;
      }
    }

    var t = main.match(TIME_RE);
    var tm = t ? toMinutes(t[1], t[2], t[3]) : null;
    if (tm != null) {
      if (FINISH.test(main) || (AFTER.test(main) && !BEFORE.test(main)))
        add({ type: "range", from: tm, to: DAY_END, kind: "after", label: "No classes after " + clock(tm) });
      else if (BEFORE.test(main))
        add({ type: "range", from: DAY_START, to: tm, kind: "before", label: "No classes before " + clock(tm) });
      else if (NEGATE.test(main) || /\d\s*(am|pm)?s\b/.test(main)) {
        var h0 = Math.floor(tm / 60) * 60;
        add({ type: "range", from: h0, to: h0 + 60, kind: "hour", label: "No " + clock(h0) + " classes" });
      }
      if (found.actions.some(function (x) { return x.type === "range"; })) return found;
    }

    if (/\bmornings?\b|الصباح|صباحا|صباحاً|الصبح/.test(main))
      add({ type: "range", from: DAY_START, to: 12 * 60, kind: "morning", label: "No morning classes" });
    else if (/\bearly\b|بدري/.test(main))
      add({ type: "range", from: DAY_START, to: 9 * 60, kind: "early", label: "No early classes (before 9 AM)" });
    if (/\bafternoons?\b|بعد الظهر|العصر/.test(main))
      add({ type: "range", from: 13 * 60, to: 17 * 60, kind: "afternoon", label: "No afternoon classes" });
    if (/\bevenings?\b|\bnights?\b|المساء|الليل/.test(main))
      add({ type: "range", from: 17 * 60, to: DAY_END, kind: "evening", label: "No evening classes" });
    if (found.actions.some(function (x) { return x.type === "range"; })) return found;

    if (found.days.length && DAY_OFF.test(main)) add({ type: "dayoff" });
    return found;
  }

  function build(actions, days, except) {
    var rules = [];
    actions.forEach(function (a) {
      var base = { days: days.slice(), except: except };
      if (a.type === "dayoff") rules.push(Object.assign(base, { from: DAY_START, to: DAY_END, dayoff: true, kind: "dayoff" }));
      else if (a.type === "only") {
        var label = "Classes only " + clock(a.from) + "–" + clock(a.to);
        // Two blocks (before and after the window), one rule for the student.
        rules.push(Object.assign(base, { from: DAY_START, to: a.from, base: label, kind: "only", window: [a.from, a.to], extra: [{ from: a.to, to: DAY_END }] }));
      } else if (a.type === "range") rules.push(Object.assign(base, { from: a.from, to: a.to, base: a.label, kind: a.kind || "range" }));
    });
    return rules;
  }

  /** Final days (minus exceptions) and a readable label. */
  function finish(r) {
    var list = (r.days.length ? r.days : [0, 1, 2, 3, 4]).filter(function (d, i, all) {
      return all.indexOf(d) === i && r.except.indexOf(d) < 0;
    }).sort();
    var label;
    if (r.dayoff) label = (list.length === 5 ? "Every day" : list.map(function (d) { return DAY_FULL[d]; }).join(" and ")) + " off";
    else if (r.except.length) label = r.base + " except " + r.except.map(function (d) { return DAY_FULL[d]; }).join(" and ");
    else label = r.base + (daysLabel(list) ? " on " + daysLabel(list) : "");
    // `kind`, `except` and `window` let the planner write the label in either language.
    var out = { days: list, from: r.from, to: r.to, label: label, kind: r.kind, except: r.except.slice() };
    if (r.window) out.window = r.window;
    if (r.extra) out.extra = r.extra;
    return out;
  }

  function parse(text) {
    var out = { rules: [], maxDays: null, preferGaps: false, unknown: [] };
    var norm = normalize(text);
    if (!norm) return out;
    var raw = [], lastRules = null, pendingDays = [];
    splitClauses(norm).forEach(function (clause) {
      var f = readClause(clause);
      f.actions.forEach(function (a) {
        if (a.type === "gaps") out.preferGaps = true;
        if (a.type === "maxDays") out.maxDays = a.n;
      });
      var timeActions = f.actions.filter(function (a) { return a.type === "range" || a.type === "only" || a.type === "dayoff"; });
      if (!timeActions.length) {
        // "Sunday and Monday off": "sunday" arrives alone, so hold it for the
        // next clause. "before 9 on Sunday and Tuesday": add to the last rule.
        if (f.days.length) {
          if (lastRules) lastRules.forEach(function (r) { r.days = r.days.concat(f.days); });
          else pendingDays = pendingDays.concat(f.days);
        } else if (!f.actions.length && !FILLER.test(clause) && /[a-z؀-ۿ]{3,}/.test(clause)) {
          out.unknown.push(clause);
        } else if (!f.actions.length && FILLER.test(clause) && clause.split(" ").length > 3) {
          out.unknown.push(clause);
        }
        return;
      }
      lastRules = build(timeActions, f.days.concat(pendingDays), f.except);
      pendingDays = [];
      raw = raw.concat(lastRules);
    });
    if (pendingDays.length)
      out.unknown.push(pendingDays.map(function (d) { return DAY_FULL[d]; }).join(" and ") + " (free when?)");
    out.rules = raw.map(finish).filter(function (r) { return r.days.length && r.to >= r.from; });
    return out;
  }

  /** Rules → hour keys "day-hour" the planner blocks (any hour the rule touches). */
  function hours(rules) {
    var keys = {};
    (rules || []).forEach(function (r) {
      [{ from: r.from, to: r.to }].concat(r.extra || []).forEach(function (span) {
        if (span.to <= span.from) return;
        r.days.forEach(function (d) {
          for (var h = Math.floor(span.from / 60); h * 60 < span.to; h++) keys[d + "-" + h] = true;
        });
      });
    });
    return Object.keys(keys);
  }

  window.ShougFreeTime = { parse: parse, hours: hours, clock: clock };
})();
