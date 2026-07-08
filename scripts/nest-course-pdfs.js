#!/usr/bin/env node

const fs = require('fs');
const path = require('path');

const root = path.resolve(__dirname, '..');
const docs = path.join(root, 'docs');
const courseRoots = [
  path.join(docs, 'academics', 'other-courses', 'math221'),
  path.join(docs, 'academics', 'other-courses', 'com201'),
];

function walk(directory) {
  return fs.readdirSync(directory, { withFileTypes: true }).flatMap((entry) => {
    const fullPath = path.join(directory, entry.name);
    return entry.isDirectory() ? walk(fullPath) : [fullPath];
  });
}

const htmlFiles = courseRoots.flatMap(walk).filter((file) => file.endsWith('.html'));
const movesBySource = new Map();

for (const htmlFile of htmlFiles) {
  if (path.basename(htmlFile) !== 'index.html') continue;
  const viewerDirectory = path.dirname(htmlFile);
  const relativeViewer = path.relative(docs, viewerDirectory).split(path.sep).join('/');
  if (!/\/(slides|extra-resources|exams)\/.+/.test(`/${relativeViewer}`)) continue;

  const contents = fs.readFileSync(htmlFile, 'utf8');
  const pdfUrls = [...contents.matchAll(/(?:href|src)="(\/academics\/other-courses\/(?:math221|com201)\/[^"?#]+\.pdf)"/gi)]
    .map((match) => decodeURI(match[1]));

  for (const pdfUrl of new Set(pdfUrls)) {
    const source = path.join(docs, pdfUrl.replace(/^\//, ''));
    if (!fs.existsSync(source) || path.dirname(source) === viewerDirectory) continue;
    const target = path.join(viewerDirectory, path.basename(source));
    const existing = movesBySource.get(source);
    if (existing && existing !== target) {
      throw new Error(`PDF is assigned to multiple viewer folders: ${source}`);
    }
    if (fs.existsSync(target)) throw new Error(`Target already exists: ${target}`);
    movesBySource.set(source, target);
  }
}

const moves = [...movesBySource.entries()].map(([source, target]) => ({ source, target }));
for (const { source, target } of moves) fs.renameSync(source, target);

for (const htmlFile of htmlFiles) {
  const contents = fs.readFileSync(htmlFile, 'utf8');
  let updated = contents;
  for (const { source, target } of moves) {
    const oldUrl = `/${path.relative(docs, source).split(path.sep).join('/')}`;
    const newUrl = `/${path.relative(docs, target).split(path.sep).join('/')}`;
    updated = updated.split(oldUrl).join(newUrl);
    updated = updated.split(encodeURI(oldUrl)).join(encodeURI(newUrl));
    updated = updated.split(encodeURIComponent(oldUrl)).join(encodeURIComponent(newUrl));
  }
  if (updated !== contents) fs.writeFileSync(htmlFile, updated);
}

console.log(`Moved ${moves.length} PDFs into their viewer folders and updated ${htmlFiles.length} HTML files.`);
for (const { source, target } of moves) {
  console.log(`${path.relative(root, source)} -> ${path.relative(root, target)}`);
}
