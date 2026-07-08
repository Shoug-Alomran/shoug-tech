#!/usr/bin/env node

const fs = require('fs');
const path = require('path');

const root = path.resolve(__dirname, '..');
const docs = path.join(root, 'docs');
const courseRoot = path.join(docs, 'academics', 'other-courses', 'math221');

const sections = {
  slides: [
    ['01-1-1-summary', '1-1', '1-1.pdf', '1.1'],
    ['02-1-2-1-3', '1-2-1-3', '1-2-1-3.pdf', '1.2, 1.3'],
    ['03-2-1-bisection-method', '2-1', '2-1.pdf', '2.1'],
    ['19-ch-2-4', '2-4', '2-4.pdf', '2.4'],
    ['20-ch-2-5', '2-5', '2-5.pdf', '2.5'],
    ['23-chapter-2-3-math221ppt', '2-3', '2-3.pdf', '2.3'],
    ['21-ch-3-1-math221', '3-1', '3-1.pdf', '3.1'],
    ['3-2', '3-2', '3-2.pdf', '3.2'],
    ['05-3-3', '3-3', '3-3.pdf', '3.3'],
    ['06-3-4-2', '3-4', '3-4.pdf', '3.4'],
    ['07-3-5', '3-5', '3-5.pdf', '3.5'],
    ['22-ch-4-1', '4-1', '4-1.pdf', '4.1'],
    ['08-4-3', '4-3', '4-3.pdf', '4.3'],
    ['09-4-4', '4-4', '4-4.pdf', '4.4'],
    ['5-1', '5-1', '5-1.pdf', '5.1'],
    ['11-5-2', '5-2', '5-2.pdf', '5.2'],
    ['12-5-3', '5-3', '5-3.pdf', '5.3'],
    ['13-6-1', '6-1', '6-1.pdf', '6.1'],
    ['14-6-2-pivoting-strategies', '6-2', '6-2.pdf', '6.2'],
    ['15-6-3-linear-algebra-and-matrix-inversion', '6-3', '6-3.pdf', '6.3'],
    ['16-7-1', '7-1', '7-1.pdf', '7.1'],
    ['17-7-2', '7-2', '7-2.pdf', '7.2'],
    ['18-7-3', '7-3', '7-3.pdf', '7.3'],
  ],
  'extra-resources': [
    ['01-1-3', '1-3', '1-3.pdf', '1.3'],
    ['02-2-1', '2-1', '2-1.pdf', '2.1'],
    ['03-2-2', '2-2', '2-2.pdf', '2.2'],
    ['04-2-3', '2-3', '2-3.pdf', '2.3'],
    ['05-2-4', '2-4', '2-4.pdf', '2.4'],
    ['06-2-5', '2-5', '2-5.pdf', '2.5'],
    ['07-2-6', '2-6', '2-6.pdf', '2.6'],
    ['08-3-1', '3-1', '3-1.pdf', '3.1'],
    ['09-3-2', '3-2', '3-2.pdf', '3.2'],
    ['10-3-3', '3-3', '3-3.pdf', '3.3'],
    ['11-3-4', '3-4', '3-4.pdf', '3.4'],
    ['12-3-5', '3-5', '3-5.pdf', '3.5'],
    ['13-4-1', '4-1', '4-1.pdf', '4.1'],
    ['14-4-3', '4-3', '4-3.pdf', '4.3'],
    ['15-4-4', '4-4', '4-4.pdf', '4.4'],
    ['16-rules', 'rules', 'rules.pdf', 'Rules'],
  ],
};

const staleSlideRoutes = {
  '02-1-2-1-3-math221-9275ebf0f413b5fb40a4fd060b24c4cb': '1-2-1-3',
  '04-3-2-math221-076a7fc61939ecb54b72ed20443f1745-3': '3-2',
  '05-3-3-math221ppt-63b97476e2819f5c47184369626b8969': '3-3',
  '06-3-4-math221-2': '3-4',
  '07-3-5-math221-4033cc10dc0e70c1dc0e3a08f0326f09': '3-5',
  '10-5-1': '5-1',
  '19-ch-2-4-math221-8341bf5e0b5a245802c407764ccd4ac0': '2-4',
  '20-ch-2-5-copy-143781afcf1f91af197ccacda591426b': '2-5',
  '21-ch-3-1-math221': '3-1',
  '22-ch-4-1-math221-72e2bca378bdc9c83126682f5af0b83e': '4-1',
  '23-chapter-2-3-math221ppt': '2-3',
};

function walk(directory) {
  return fs.readdirSync(directory, { withFileTypes: true }).flatMap((entry) => {
    const fullPath = path.join(directory, entry.name);
    return entry.isDirectory() ? walk(fullPath) : [fullPath];
  });
}

const replacements = [];
for (const [section, lessons] of Object.entries(sections)) {
  const sectionRoot = path.join(courseRoot, section);
  for (const [oldFolder, newFolder, newPdf, label] of lessons) {
    const oldDirectory = path.join(sectionRoot, oldFolder);
    const newDirectory = path.join(sectionRoot, newFolder);
    if (!fs.existsSync(oldDirectory) && !fs.existsSync(newDirectory)) continue;
    const workingDirectory = fs.existsSync(oldDirectory) ? oldDirectory : newDirectory;
    const currentPdf = fs.readdirSync(workingDirectory).find((name) => name.toLowerCase().endsWith('.pdf'));
    if (currentPdf && currentPdf !== newPdf) {
      fs.renameSync(path.join(workingDirectory, currentPdf), path.join(workingDirectory, newPdf));
    }
    if (oldDirectory !== newDirectory) {
      if (fs.existsSync(oldDirectory) && fs.existsSync(newDirectory)) throw new Error(`Target folder exists: ${newDirectory}`);
      if (fs.existsSync(oldDirectory)) fs.renameSync(oldDirectory, newDirectory);
    }
    const oldRoute = `/academics/other-courses/math221/${section}/${oldFolder}/`;
    const newRoute = `/academics/other-courses/math221/${section}/${newFolder}/`;
    replacements.push({ oldRoute, newRoute, currentPdf, newPdf, label, directory: newDirectory });
  }
}

const htmlFiles = walk(courseRoot).filter((file) => file.endsWith('.html'));
for (const htmlFile of htmlFiles) {
  let contents = fs.readFileSync(htmlFile, 'utf8');
  for (const item of replacements) {
    contents = contents.split(item.oldRoute).join(item.newRoute);
    if (item.currentPdf && item.currentPdf !== item.newPdf) {
      contents = contents.split(item.currentPdf).join(item.newPdf);
    }
  }
  for (const [oldFolder, newFolder] of Object.entries(staleSlideRoutes)) {
    contents = contents.split(`/academics/other-courses/math221/slides/${oldFolder}/`).join(`/academics/other-courses/math221/slides/${newFolder}/`);
  }
  for (const item of replacements) {
    const escapedRoute = item.newRoute.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
    const rowPattern = new RegExp(`(<a href="${escapedRoute}" class="dir-row"[\\s\\S]*?<div class="dir-title">)[\\s\\S]*?(<\\/div>)`, 'g');
    contents = contents.replace(rowPattern, `$1${item.label}$2`);
    const treePattern = new RegExp(`(<a class="tree-file" href="${escapedRoute}">)(?:<span class="status-dot"><\\/span>)?[^<]*(<\\/a>)`, 'g');
    contents = contents.replace(treePattern, (match, start, end) => `${start}${match.includes('status-dot') ? '<span class="status-dot"></span>' : ''}${item.label}${end}`);
  }
  fs.writeFileSync(htmlFile, contents);
}

for (const item of replacements) {
  const viewer = path.join(item.directory, 'index.html');
  if (!fs.existsSync(viewer)) continue;
  let contents = fs.readFileSync(viewer, 'utf8');
  contents = contents.replace(/<title>.*?<\/title>/, `<title>MATH221 | ${item.label}</title>`);
  contents = contents.replace(/<span class="current">.*?<\/span>/, `<span class="current">${item.label}</span>`);
  contents = contents.replace(/<h1 class="ch-title">.*?<\/h1>/, `<h1 class="ch-title">${item.label}</h1>`);
  contents = contents.replace(/(<iframe class="embed-frame"[^>]* title=")[^"]*(")/, `$1${item.label}$2`);
  fs.writeFileSync(viewer, contents);
}

function lessonKey(value) {
  const numbers = value.match(/\d+(?:\.\d+)?/g);
  if (!numbers) return [Number.MAX_SAFE_INTEGER];
  return numbers.flatMap((number) => number.split('.').map(Number));
}

function compareLessons(left, right) {
  const a = lessonKey(left);
  const b = lessonKey(right);
  for (let index = 0; index < Math.max(a.length, b.length); index += 1) {
    const difference = (a[index] ?? -1) - (b[index] ?? -1);
    if (difference) return difference;
  }
  return left.localeCompare(right, undefined, { numeric: true });
}

for (const section of ['slides', 'extra-resources']) {
  const indexFile = path.join(courseRoot, section, 'index.html');
  let contents = fs.readFileSync(indexFile, 'utf8');
  const containerStart = contents.indexOf('<div class="directory-container">');
  const rightsStart = contents.indexOf('\n\n            <div style="margin: 32px', containerStart);
  if (containerStart === -1 || rightsStart === -1) continue;
  const container = contents.slice(containerStart, rightsStart);
  const rows = [...container.matchAll(/<a href="[^"]+" class="dir-row"[^>]*>[\s\S]*?<\/a>/g)].map((match) => match[0]);
  if (!rows.length) continue;
  rows.sort((left, right) => {
    const leftLabel = left.match(/<div class="dir-title">([\s\S]*?)<\/div>/)?.[1].trim() || '';
    const rightLabel = right.match(/<div class="dir-title">([\s\S]*?)<\/div>/)?.[1].trim() || '';
    return compareLessons(leftLabel, rightLabel);
  });
  const numberedRows = rows.map((row, index) => row.replace(/<div class="dir-num">.*?<\/div>/, `<div class="dir-num">${String(index + 1).padStart(2, '0')}</div>`));
  const firstRow = container.search(/<a href="[^"]+" class="dir-row"/);
  const lastRowEnd = container.lastIndexOf('</a>') + 4;
  const sortedContainer = container.slice(0, firstRow) + numberedRows.join('\n                            ') + container.slice(lastRowEnd);
  contents = contents.slice(0, containerStart) + sortedContainer + contents.slice(rightsStart);
  fs.writeFileSync(indexFile, contents);
}

console.log(`Simplified ${replacements.length} MATH221 lesson folders and their PDFs.`);
