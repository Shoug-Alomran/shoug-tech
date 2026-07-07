#!/usr/bin/env node
"use strict";

const fs = require("fs");
const path = require("path");

const ROOT = path.resolve(__dirname, "..");
const DOCS = path.join(ROOT, "docs");
const ACADEMICS = path.join(DOCS, "academics");
const OUT = path.join(DOCS, "javascripts", "course-manifest.js");

const ORDER_OVERRIDES = {
  "other-courses/ethcs303/slides": [
    "moral-systems-ethical-concepts-and-theories",
    "kantianism",
    "utilitarianism",
    "social-contract-theory",
    "ethical-issues-in-systems-analysis-and-software-engineering",
    "network-security-and-privacy",
    "network-security-and-privacy-in-the-cloud",
    "privacy-issues-in-cyberspace",
    "social-media-ethical-legal-security-issues",
    "social-engineering",
    "introduction-to-ethical-hacking",
    "business-ethics",
    "intellectual-property-laws",
    "cyber-laws-in-saudi-arabia",
  ],
};

function walk(dir, results = []) {
  let entries;
  try {
    entries = fs.readdirSync(dir, { withFileTypes: true });
  } catch (_) {
    return results;
  }
  for (const entry of entries) {
    const full = path.join(dir, entry.name);
    if (entry.isDirectory()) walk(full, results);
    else if (entry.isFile() && entry.name === "index.html") results.push(full);
  }
  return results;
}

function decodeEntities(str) {
  return String(str || "")
    .replace(/&amp;/g, "&")
    .replace(/&lt;/g, "<")
    .replace(/&gt;/g, ">")
    .replace(/&quot;/g, '"')
    .replace(/&#39;/g, "'")
    .replace(/&nbsp;/g, " ");
}

function cleanTitle(title) {
  return decodeEntities(title)
    .replace(/^SHOUG\.TECH\s*(?:\/\/|\|)\s*/i, "")
    .replace(/\s+study material.*$/i, "")
    .replace(/\s+/g, " ")
    .trim();
}

function extractTitle(html, fallback) {
  const title = html.match(/<title[^>]*>([\s\S]*?)<\/title>/i);
  if (title) return cleanTitle(title[1]) || fallback;
  const h1 = html.match(/<h1[^>]*>([\s\S]*?)<\/h1>/i);
  if (h1) return cleanTitle(h1[1].replace(/<[^>]+>/g, " ")) || fallback;
  return fallback;
}

function titleFromSlug(slug) {
  return slug
    .replace(/^\d+-/, "")
    .replace(/-/g, " ")
    .replace(/\b\w/g, c => c.toUpperCase());
}

function pageRank(page) {
  const key = page.track + "/" + page.course + "/" + page.section;
  const order = ORDER_OVERRIDES[key];
  if (!order) return Number.POSITIVE_INFINITY;
  const parts = page.url.split("/").filter(Boolean);
  const leaf = parts[parts.length - 1];
  const index = order.indexOf(leaf);
  return index === -1 ? Number.POSITIVE_INFINITY : index;
}

function fileToUrl(file) {
  const rel = path.relative(DOCS, file).split(path.sep);
  return "/" + rel.slice(0, -1).join("/") + "/";
}

function safeDecodeUriPart(value) {
  try {
    return decodeURIComponent(value);
  } catch (_) {
    return value;
  }
}

function localPdfTargets(html, htmlFile) {
  const targets = [];
  const pattern = /(?:href|src|data|value)\s*=\s*["']([^"']+\.pdf(?:[#?][^"']*)?)["']/ig;
  let match;
  while ((match = pattern.exec(html))) {
    let href = match[1].split("#")[0].split("?")[0];
    if (!href || /^(?:https?:|data:|mailto:)/i.test(href)) continue;
    href = safeDecodeUriPart(href);
    const file = href.startsWith("/")
      ? path.join(DOCS, href.replace(/^\/+/, ""))
      : path.resolve(path.dirname(htmlFile), href);
    targets.push({ href, file });
  }
  return targets;
}

function courseInfo(parts) {
  // parts excludes the leading empty segment. All URLs start with academics.
  const track = parts[1];
  if (!track) return null;

  if (track === "other-courses" && parts[2] === "english") {
    const course = parts[3];
    if (!course) return null;
    return {
      track,
      course,
      section: parts[4] || "",
      courseUrl: "/academics/other-courses/english/" + course + "/",
      minContentParts: 6,
    };
  }

  const course = parts[2];
  if (!course) return null;
  return {
    track,
    course,
    section: parts[3] || "",
    courseUrl: "/academics/" + track + "/" + course + "/",
    minContentParts: 5,
  };
}

function build() {
  const files = walk(ACADEMICS);
  const urls = files.map(fileToUrl);
  const parentUrls = new Set();
  for (const url of urls) {
    const parts = url.split("/").filter(Boolean);
    for (let i = 1; i < parts.length; i++) {
      parentUrls.add("/" + parts.slice(0, i).join("/") + "/");
    }
  }
  const courseTitles = {};
  const pages = [];
  const skippedMissingPdf = [];
  const skippedOfflineFiles = [];

  for (let i = 0; i < files.length; i++) {
    const file = files[i];
    const url = urls[i];
    const parts = url.split("/").filter(Boolean);
    const info = courseInfo(parts);
    if (!info) continue;

    let html = "";
    let offlinePlaceholder = false;
    try {
      const stat = fs.statSync(file);
      if (stat.size > 0 && stat.blocks === 0) {
        skippedOfflineFiles.push(file);
        offlinePlaceholder = true;
      } else {
        html = fs.readFileSync(file, "utf8");
      }
    } catch (_) {}

    if (url === info.courseUrl) {
      courseTitles[info.track + "/" + info.course] = extractTitle(html, info.course.toUpperCase());
      continue;
    }

    if (parts.length < info.minContentParts) continue;

    if (parentUrls.has(url)) continue;

    const missingPdfTargets = offlinePlaceholder
      ? []
      : localPdfTargets(html, file).filter(target => !fs.existsSync(target.file));
    if (missingPdfTargets.length) {
      skippedMissingPdf.push({
        url,
        pdfs: missingPdfTargets.map(target => target.href),
      });
      continue;
    }

    pages.push({
      url,
      title: extractTitle(html, titleFromSlug(parts[parts.length - 1] || info.course)),
      track: info.track,
      course: info.course,
      section: info.section,
      courseUrl: info.courseUrl,
    });
  }

  // STAT101 uses one query-driven embedded viewer. Each source file still needs
  // a distinct manifest URL so progress can track resources independently.
  const stat101Root = path.join(ACADEMICS, "other-courses", "stat101");
  const stat101ViewerUrls = new Map();
  for (const htmlFile of walk(stat101Root)) {
    let html = "";
    try { html = fs.readFileSync(htmlFile, "utf8"); } catch (_) { continue; }
    const pattern = /href=["'](\/academics\/other-courses\/stat101\/viewer\/\?[^"']+)["']/ig;
    let match;
    while ((match = pattern.exec(html))) {
      const url = decodeEntities(match[1]);
      const query = new URLSearchParams(url.split("?")[1] || "");
      const normalizedUrl = url.split("?")[0] + "?" + query.toString();
      const source = query.get("src") || "";
      if (!source.endsWith(".pdf")) continue;
      let resourceTitle = query.get("title") || titleFromSlug(path.basename(source, ".pdf"));
      if (resourceTitle === "STAT101 Worksheet") {
        resourceTitle = titleFromSlug(path.basename(source, ".pdf"));
      }
      stat101ViewerUrls.set(source, {
        url: normalizedUrl,
        title: resourceTitle,
        track: "other-courses",
        course: "stat101",
        section: (query.get("section") || "study-material").toLowerCase().replace(/\s+/g, "-"),
        courseUrl: "/academics/other-courses/stat101/",
        courseTitle: "STAT101 // Introduction to Probability Theory and Statistics",
      });
    }
  }
  pages.push(...stat101ViewerUrls.values());
  if (courseTitles["other-courses/sci101"]) {
    courseTitles["other-courses/sci101"] = "SCI101 // Introduction to Physical Science";
  }
  if (stat101ViewerUrls.size) {
    courseTitles["other-courses/stat101"] = "STAT101 // Introduction to Probability Theory and Statistics";
  }

  pages.sort((a, b) => {
    const scopeA = a.track + "/" + a.course + "/" + a.section;
    const scopeB = b.track + "/" + b.course + "/" + b.section;
    if (scopeA === scopeB) {
      const rankA = pageRank(a);
      const rankB = pageRank(b);
      if (rankA !== rankB) return rankA - rankB;
    }
    return a.url.localeCompare(b.url);
  });

  for (const page of pages) {
    page.courseTitle = courseTitles[page.track + "/" + page.course] || page.course.toUpperCase();
  }

  const counts = {};
  for (const page of pages) {
    const key = page.track + "/" + page.course;
    counts[key] = (counts[key] || 0) + 1;
  }

  const legacyCounts = {};
  for (const [key, count] of Object.entries(counts)) {
    const course = key.split("/").pop();
    legacyCounts[course] = (legacyCounts[course] || 0) + count;
  }

  const js = [
    "// Auto-generated by scripts/build-course-manifest.js - do not edit by hand.",
    "// Run this script whenever academic pages are added, removed, or renamed.",
    "var COURSE_PAGES = " + JSON.stringify(pages, null, 2) + ";",
    "var COURSE_MANIFEST = " + JSON.stringify(legacyCounts, null, 2) + ";",
    "var COURSE_MANIFEST_BY_TRACK = " + JSON.stringify(counts, null, 2) + ";",
    "",
  ].join("\n");

  fs.writeFileSync(OUT, js, "utf8");
  console.log(`[ok] course-manifest.js -> ${pages.length} content pages`);
  if (skippedMissingPdf.length) {
    console.log(`[warn] skipped ${skippedMissingPdf.length} pages with missing local PDFs`);
    for (const item of skippedMissingPdf.slice(0, 20)) {
      console.log(`  - ${item.url} -> ${item.pdfs.join(", ")}`);
    }
  }
  if (skippedOfflineFiles.length) {
    console.log(`[warn] skipped ${skippedOfflineFiles.length} offline filesystem placeholders`);
    for (const file of skippedOfflineFiles.slice(0, 20)) {
      console.log(`  - ${path.relative(ROOT, file)}`);
    }
  }
}

build();
