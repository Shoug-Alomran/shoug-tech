#!/usr/bin/env node
"use strict";

const fs = require("fs");
const path = require("path");
const crypto = require("crypto");
const { execFileSync } = require("child_process");

const SOURCE_URL = "https://psu.edu.sa/en/academiccalendar";
const OUTPUT = path.join(__dirname, "..", "docs", "javascripts", "psu-academic-calendar.js");
const MONTHS = {
  january: "01", february: "02", march: "03", april: "04", may: "05", june: "06",
  july: "07", august: "08", september: "09", october: "10", november: "11", december: "12"
};

function decodeEntities(value) {
  return String(value || "")
    .replace(/&nbsp;/gi, " ")
    .replace(/&amp;/gi, "&")
    .replace(/&quot;/gi, '"')
    .replace(/&#39;|&apos;/gi, "'")
    .replace(/&lt;/gi, "<")
    .replace(/&gt;/gi, ">");
}

function stripHtml(html) {
  return decodeEntities(html)
    .replace(/<script[\s\S]*?<\/script>/gi, " ")
    .replace(/<style[\s\S]*?<\/style>/gi, " ")
    .replace(/<br\s*\/?>/gi, "\n")
    .replace(/<[^>]+>/g, "\n")
    .replace(/[ \t\r\f\v]+/g, " ")
    .replace(/\n\s+/g, "\n")
    .replace(/\n{2,}/g, "\n")
    .trim();
}

function slug(value) {
  return String(value || "")
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, "-")
    .replace(/^-|-$/g, "");
}

function parseDateParts(value) {
  const matches = String(value || "").matchAll(/(\d{1,2})(?:\s*-\s*(\d{1,2}))?\s+([A-Za-z]+)\s+(\d{4})/g);
  let match = null;
  for (const candidate of matches) {
    if (MONTHS[candidate[3].toLowerCase()]) match = candidate;
  }
  if (!match) return null;
  const month = MONTHS[match[3].toLowerCase()];
  const startDay = match[1].padStart(2, "0");
  const endDay = (match[2] || match[1]).padStart(2, "0");
  return {
    start: `${match[4]}-${month}-${startDay}`,
    end: `${match[4]}-${month}-${endDay}`
  };
}

function termLabel(type, year) {
  if (type === "Summer") return `Summer ${year}`;
  return `${type} Semester ${year}`;
}

function addEvent(events, id, title, date, endDate) {
  if (!date || events.some((event) => event.id === id)) return;
  const event = { id, title, date, kind: "academic" };
  if (endDate && endDate !== date) event.endDate = endDate;
  events.push(event);
}

function dayBefore(date) {
  if (!date) return "";
  const value = new Date(`${date}T00:00:00Z`);
  value.setUTCDate(value.getUTCDate() - 1);
  return value.toISOString().slice(0, 10);
}

function rowCells(rowHtml) {
  const cells = [];
  const cellRegex = /<td\b[^>]*>([\s\S]*?)<\/td>/gi;
  let match;
  while ((match = cellRegex.exec(rowHtml))) cells.push(stripHtml(match[1]));
  return cells;
}

function findRow(rows, phrase) {
  const regex = new RegExp(phrase, "i");
  return rows.find((row) => regex.test(row.event));
}

function extractEvents(html) {
  const events = [];
  const headingRegex = /<h4[^>]*>\s*(First|Second|Summer)\s+Semester\s+\d+H\/(\d{4})G\s+\(Term\s+(\d+)\)\s*<\/h4>/gi;
  const headings = [];
  let match;
  while ((match = headingRegex.exec(html))) {
    headings.push({ index: match.index, type: match[1], year: match[2], term: match[3], heading: match[0] });
  }

  headings.forEach((heading, index) => {
    const next = headings[index + 1] ? headings[index + 1].index : html.length;
    const section = html.slice(heading.index, next);
    const rows = [];
    const rowRegex = /<tr\b[^>]*>([\s\S]*?)<\/tr>/gi;
    let rowMatch;
    while ((rowMatch = rowRegex.exec(section))) {
      const cells = rowCells(rowMatch[0]);
      if (cells.length >= 3) rows.push({ date: parseDateParts(cells[1]), event: cells.slice(2).join(" ") });
    }
    const base = `psu-${heading.term}`;
    const classesBegin = findRow(rows, "Classes begin");
    const eventYear = classesBegin && classesBegin.date ? classesBegin.date.start.slice(0, 4) : heading.year;
    const label = termLabel(heading.type, eventYear);

    addEvent(events, `${base}-classes-begin`, `PSU Classes Begin - ${label}`, classesBegin && classesBegin.date && classesBegin.date.start);

    const classesEnd = findRow(rows, "Last Day of Classes");
    addEvent(events, `${base}-classes-end`, `PSU Last Day of Classes - ${label}`, classesEnd && classesEnd.date && classesEnd.date.start);

    const finalsStart = findRow(rows, "(?:Final Exams start|Start of University-Level Final Exams)");
    const finalsEnd = findRow(rows, "Final Exams end");
    addEvent(
      events,
      `${base}-finals`,
      `PSU Final Exams - ${label}`,
      finalsStart && finalsStart.date && finalsStart.date.start,
      finalsEnd && finalsEnd.date && finalsEnd.date.start
    );

    const nationalDay = findRow(rows, "Saudi National Day Holiday");
    addEvent(events, `${base}-national-day`, "PSU Saudi National Day Holiday", nationalDay && nationalDay.date && nationalDay.date.start, nationalDay && nationalDay.date && nationalDay.date.end);

    const fitrStart = findRow(rows, "Beginning of Eidul-Fitr Holiday");
    const fitrResume = findRow(rows, "Classes resume after Eidul-Fitr");
    addEvent(events, `${base}-eid-fitr`, "PSU Eidul-Fitr Holiday", fitrStart && fitrStart.date && fitrStart.date.start, dayBefore(fitrResume && fitrResume.date && fitrResume.date.start));
    addEvent(events, `${base}-classes-resume-fitr`, "PSU Classes Resume after Eidul-Fitr", fitrResume && fitrResume.date && fitrResume.date.start);

    const adhaStart = findRow(rows, "Beginning of Eidul-Adha Holiday");
    const adhaResume = findRow(rows, "Classes resume after Eidul-?\\s*Adha");
    addEvent(events, `${base}-eid-adha`, "PSU Eidul-Adha Holiday", adhaStart && adhaStart.date && adhaStart.date.start, dayBefore(adhaResume && adhaResume.date && adhaResume.date.start));
    addEvent(events, `${base}-classes-resume-adha`, "PSU Classes Resume after Eidul-Adha", adhaResume && adhaResume.date && adhaResume.date.start);
  });

  return events.sort((a, b) => a.date.localeCompare(b.date) || a.id.localeCompare(b.id));
}

function render(events) {
  const latestTerm = events.reduce((latest, event) => {
    const term = (event.id.match(/^psu-(\d+)/) || [])[1] || "";
    return term > latest ? term : latest;
  }, "");
  const hash = crypto.createHash("sha256").update(JSON.stringify(events)).digest("hex").slice(0, 10);
  const version = latestTerm ? `term-${latestTerm}-${hash}` : hash;
  return `(function(){
  "use strict";
  window.SHOUG_PSU_ACADEMIC_CALENDAR=${JSON.stringify({
    sourceUrl: SOURCE_URL,
    version,
    events
  }, null, 2)};
})();
`;
}

async function main() {
  const events = extractEvents(await fetchCalendarHtml());
  if (events.length < 6) throw new Error(`Only found ${events.length} PSU calendar events; refusing to overwrite.`);
  fs.writeFileSync(OUTPUT, render(events));
  console.log(`Wrote ${events.length} PSU calendar events to ${path.relative(process.cwd(), OUTPUT)}`);
}

async function fetchCalendarHtml() {
  try {
    const response = await fetch(SOURCE_URL, { headers: { "user-agent": "shoug-tech-calendar-sync/1.0" } });
    if (!response.ok) throw new Error(`PSU calendar request failed: ${response.status}`);
    return response.text();
  } catch (error) {
    console.warn(`Node fetch failed (${error.cause && error.cause.code ? error.cause.code : error.message}); retrying with curl.`);
    return execFileSync("curl", ["-fsSL", SOURCE_URL], { encoding: "utf8", maxBuffer: 10 * 1024 * 1024 });
  }
}

main().catch((error) => {
  console.error(error.message || error);
  process.exit(1);
});
