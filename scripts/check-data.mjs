import { readFile } from 'node:fs/promises';

const dataFiles = [
  ['bio', 'data/bio_data.json'],
  ['chem', 'data/chem_data.json'],
  ['geo', 'data/geo_data.json']
];

let failed = false;

for (const [subject, file] of dataFiles) {
  const items = JSON.parse(await readFile(file, 'utf8'));
  const ids = new Set();
  const missing = [];

  for (const item of items) {
    if (ids.has(item.id)) missing.push(`duplicate id ${item.id}`);
    ids.add(item.id);

    for (const key of ['id', 'unit', 'section', 'category', 'keypoints', 'examPoints', 'quiz']) {
      if (!(key in item)) missing.push(`${item.id || 'unknown'} missing ${key}`);
    }

    if (item.category !== subject) {
      missing.push(`${item.id} category ${item.category} should be ${subject}`);
    }
  }

  if (missing.length) {
    failed = true;
    console.error(`[${subject}] ${missing.length} issue(s)`);
    missing.slice(0, 20).forEach(issue => console.error(`- ${issue}`));
  } else {
    const quizCount = items.reduce((sum, item) => sum + (item.quiz ? item.quiz.length : 0), 0);
    console.log(`[${subject}] ok: ${items.length} knowledge items, ${quizCount} quiz questions`);
  }
}

const manifest = JSON.parse(await readFile('data/resource_manifest.json', 'utf8'));
console.log(`[resources] ok: ${manifest.totalFiles} files indexed, ${manifest.totalSizeMB} MB source library`);

if (failed) process.exit(1);
