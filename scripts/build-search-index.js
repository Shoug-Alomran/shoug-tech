#!/usr/bin/env node
/**
 * Generates docs/search-index.json by scanning all .html files under docs/.
 *
 * Run from repo root:
 *   node scripts/build-search-index.js
 */

"use strict";

const fs   = require("fs");
const path = require("path");

const ROOT      = path.resolve(__dirname, "..");
const DOCS      = path.join(ROOT, "docs");
const OUT       = path.join(DOCS, "search-index.json");

// First-level directories inside docs/ to skip entirely
const SKIP_DIRS = new Set(["assets", "javascripts", "stylesheets", "fonts", ".git", "__pycache__", "node_modules"]);

// Exact URLs to exclude
const SKIP_URLS = new Set(["/account/"]);

// Map first URL segment → section key used by the search UI
const SECTION_MAP = {
  "academics":            "academics",
  "academic-plan-themes": "academic-plan-themes",
  "work":                 "work",
  "workshops":            "workshops",
  "resources":            "resources",
  "about":                "about",
  "policy":               "policy",
  "career-development":   "career-development",
};

/** Recursively collect all .html file paths under a directory, skipping SKIP_DIRS. */
function walkHtml(dir, results) {
  results = results || [];
  let entries;
  try {
    entries = fs.readdirSync(dir, { withFileTypes: true });
  } catch (_) {
    return results;
  }
  for (const entry of entries) {
    if (entry.isDirectory()) {
      if (!SKIP_DIRS.has(entry.name)) {
        walkHtml(path.join(dir, entry.name), results);
      }
    } else if (entry.isFile() && entry.name.endsWith(".html")) {
      results.push(path.join(dir, entry.name));
    }
  }
  return results;
}

/** Decode common HTML entities in a string. */
function decodeEntities(str) {
  return str
    .replace(/&amp;/g, "&")
    .replace(/&lt;/g, "<")
    .replace(/&gt;/g, ">")
    .replace(/&quot;/g, '"')
    .replace(/&#39;/g, "'")
    .replace(/&nbsp;/g, " ");
}

/** Extract (title, description, body) from raw HTML text. */
function extract(html) {
  // Strip <head> entirely first — removes all <style>, <script>, <meta> blocks at once
  let stripped = html.replace(/<head[\s\S]*?<\/head>/gi, " ");

  // Then strip any remaining <script> and <style> blocks inside <body>
  stripped = stripped
    .replace(/<script[\s\S]*?<\/script>/gi, " ")
    .replace(/<style[\s\S]*?<\/style>/gi, " ");

  // Title: from original html <title> tag, fallback to first <h1>
  let title = "";
  const titleM = html.match(/<title[^>]*>([^<]+)<\/title>/i);
  if (titleM) {
    title = decodeEntities(titleM[1].trim());
  } else {
    const h1M = stripped.match(/<h1[^>]*>([\s\S]*?)<\/h1>/i);
    if (h1M) {
      title = decodeEntities(h1M[1].replace(/<[^>]+>/g, "").trim());
    }
  }

  // Description: from original html <meta name="description">
  let desc = "";
  let descM = html.match(/<meta\b[^>]*\bname=["']description["'][^>]*\bcontent=["']([^"']*)["']/i);
  if (!descM) {
    descM = html.match(/<meta\b[^>]*\bcontent=["']([^"']*)["'][^>]*\bname=["']description["']/i);
  }
  if (descM) {
    desc = decodeEntities(descM[1].trim());
  } else {
    const pM = stripped.match(/<p[^>]*>([\s\S]*?)<\/p>/i);
    if (pM) {
      desc = decodeEntities(pM[1].replace(/<[^>]+>/g, "").trim().slice(0, 160));
    }
  }

  // Body: all visible text, stripped, collapsed, truncated
  const body = decodeEntities(
    stripped
      .replace(/<[^>]+>/g, " ")
      .replace(/\s+/g, " ")
      .trim()
      .slice(0, 500)
  );

  return { title, desc, body };
}

/** Convert an absolute file path under DOCS to a URL path. */
function fileToUrl(filePath) {
  const rel = path.relative(DOCS, filePath);          // e.g. "academics/cs285/index.html"
  const parts = rel.split(path.sep);                  // split on OS separator

  if (parts[parts.length - 1] === "index.html") {
    // Strip "index.html" → trailing slash
    const dirs = parts.slice(0, -1);
    return dirs.length === 0 ? "/" : "/" + dirs.join("/") + "/";
  } else {
    // Keep the filename
    return "/" + parts.join("/");
  }
}

function build() {
  const htmlFiles = walkHtml(DOCS);

  // Exclude the search-index.json itself (not HTML, but just in case)
  // and build entries
  const entries = [];
  const offlinePlaceholders = [];

  for (const filePath of htmlFiles) {
    // Skip if path contains node_modules (belt-and-suspenders)
    if (filePath.includes("node_modules")) continue;

    const url = fileToUrl(filePath);

    if (SKIP_URLS.has(url)) continue;

    let raw;
    try {
      const stat = fs.statSync(filePath);
      if (stat.size > 0 && stat.blocks === 0) {
        offlinePlaceholders.push(filePath);
        continue;
      }
      raw = fs.readFileSync(filePath, "utf8");
    } catch (_) {
      continue;
    }

    const { title, desc, body } = extract(raw);

    if (!title || title.length < 2) continue;

    const urlParts = url.split("/").filter(Boolean);
    const firstSeg = urlParts[0] || "";
    const section  = SECTION_MAP[firstSeg] || firstSeg || "home";

    entries.push({ title, description: desc, url, section, body });
  }

  // Sort by URL for stable output
  entries.sort((a, b) => a.url < b.url ? -1 : a.url > b.url ? 1 : 0);

  return { entries, offlinePlaceholders };
}

function main() {
  const { entries, offlinePlaceholders } = build();
  fs.writeFileSync(OUT, JSON.stringify(entries, null, 2), "utf8");
  console.log(`[ok] search-index.json → ${entries.length} pages`);
  if (offlinePlaceholders.length) {
    console.log(`[warn] search index skipped ${offlinePlaceholders.length} offline filesystem placeholders`);
  }
}

main();
