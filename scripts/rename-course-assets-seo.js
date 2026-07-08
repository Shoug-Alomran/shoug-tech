#!/usr/bin/env node

const fs = require('fs');
const path = require('path');

const root = path.resolve(__dirname, '..');
const docs = path.join(root, 'docs');
const courseRoots = [
  path.join(docs, 'academics', 'other-courses', 'math221'),
  path.join(docs, 'academics', 'other-courses', 'com201'),
];

const filenameOverrides = new Map([
  ['academics/other-courses/math221/slides/1-1-summary.pdf', 'section-1-1-summary.pdf'],
  ['academics/other-courses/math221/slides/1-2-1-3.pdf', 'sections-1-2-and-1-3.pdf'],
  ['academics/other-courses/math221/slides/1-2.pdf', 'sections-1-2-and-1-3.pdf'],
  ['academics/other-courses/math221/slides/1-2-1-3-math221-9275ebf0f413b5fb40a4fd060b24c4cb.pdf', 'sections-1-2-and-1-3.pdf'],
  ['academics/other-courses/math221/slides/3-2-math221-076a7fc61939ecb54b72ed20443f1745-3.pdf', 'section-3-2.pdf'],
  ['academics/other-courses/math221/slides/3-3-math221ppt-63b97476e2819f5c47184369626b8969.pdf', 'section-3-3.pdf'],
  ['academics/other-courses/math221/slides/3-4-math221-2.pdf', 'section-3-4.pdf'],
  ['academics/other-courses/math221/slides/3-5-math221-4033cc10dc0e70c1dc0e3a08f0326f09.pdf', 'section-3-5.pdf'],
  ['academics/other-courses/math221/slides/ch-2-4-math221-8341bf5e0b5a245802c407764ccd4ac0.pdf', 'chapter-2-4.pdf'],
  ['academics/other-courses/math221/slides/ch-2-5-copy-143781afcf1f91af197ccacda591426b.pdf', 'chapter-2-5.pdf'],
  ['academics/other-courses/math221/slides/ch-3-1-math221.pdf', 'chapter-3-1.pdf'],
  ['academics/other-courses/math221/slides/ch-4-1-math221-72e2bca378bdc9c83126682f5af0b83e.pdf', 'chapter-4-1.pdf'],
  ['academics/other-courses/math221/slides/chapter-2-3-math221ppt.pdf', 'chapter-2-3.pdf'],
]);

function slugify(stem) {
  return stem
    .normalize('NFKD')
    .replace(/[\u0300-\u036f]/g, '')
    .replace(/&/g, ' and ')
    .replace(/[^a-zA-Z0-9]+/g, '-')
    .replace(/^-+|-+$/g, '')
    .toLowerCase();
}

function walk(directory) {
  return fs.readdirSync(directory, { withFileTypes: true }).flatMap((entry) => {
    const fullPath = path.join(directory, entry.name);
    return entry.isDirectory() ? walk(fullPath) : [fullPath];
  });
}

const renames = [];
for (const courseRoot of courseRoots) {
  for (const file of walk(courseRoot)) {
    const extension = path.extname(file).toLowerCase();
    if (!['.pdf', '.docx'].includes(extension)) continue;
    const relative = path.relative(docs, file).split(path.sep).join('/');
    let stem = path.basename(file, path.extname(file));
    if (relative.toLowerCase() === 'academics/other-courses/com201/com201.pdf') {
      stem = 'com201-syllabus';
    }
    const override = filenameOverrides.get(relative);
    const target = path.join(path.dirname(file), override || `${slugify(stem)}${extension}`);
    if (target === file) continue;
    let caseOnly = false;
    if (fs.existsSync(target)) {
      const sourceStat = fs.statSync(file);
      const targetStat = fs.statSync(target);
      caseOnly = sourceStat.dev === targetStat.dev && sourceStat.ino === targetStat.ino;
      if (!caseOnly) throw new Error(`Cannot rename ${file}: target already exists at ${target}`);
    }
    renames.push({ source: file, target, caseOnly });
  }
}

for (const { source, target, caseOnly } of renames) {
  if (caseOnly) {
    const temporary = `${source}.seo-rename-tmp`;
    fs.renameSync(source, temporary);
    fs.renameSync(temporary, target);
  } else {
    fs.renameSync(source, target);
  }
}

const htmlFiles = courseRoots.flatMap((courseRoot) => walk(courseRoot)).filter((file) => file.endsWith('.html'));
for (const htmlFile of htmlFiles) {
  let contents = fs.readFileSync(htmlFile, 'utf8');
  let updated = contents;
  for (const { source, target } of renames) {
    const oldUrl = `/${path.relative(docs, source).split(path.sep).join('/')}`;
    const newUrl = `/${path.relative(docs, target).split(path.sep).join('/')}`;
    updated = updated.split(oldUrl).join(newUrl);
    updated = updated.split(encodeURI(oldUrl)).join(encodeURI(newUrl));
    updated = updated.split(encodeURIComponent(oldUrl)).join(encodeURIComponent(newUrl));
  }
  if (updated !== contents) fs.writeFileSync(htmlFile, updated);
}

console.log(`Renamed ${renames.length} course assets and updated ${htmlFiles.length} HTML files.`);
for (const { source, target } of renames) {
  console.log(`${path.relative(root, source)} -> ${path.relative(root, target)}`);
}
