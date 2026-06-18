// build-resource-library.mjs
// Scan resource folder and generate resource_library.json + pdf directory links
import { readdirSync, statSync, copyFileSync, existsSync, mkdirSync, writeFileSync } from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.resolve(__dirname, '..');

// Source: WPS Drive resource folder
const RESOURCE_ROOT = process.env.RESOURCE_ROOT || 
  'C:/Users/27170/WPSDrive/383859682/WPS云盘/Thought/AI教育/2026.05_AI教育课程设计/lxs/初中生课程培训/资源';

// PDF destination under project
const PDF_DIR = path.join(ROOT, 'pdf');
const MANIFEST_PATH = path.join(ROOT, 'data', 'resource_library.json');

// Subject mapping
const SUBJECT_MAP = {
  '生物学': { id: 'bio', name: '生物学', grades: [7, 8] },
  '化学': { id: 'chem', name: '化学', grades: [9] },
  '地理': { id: 'geo', name: '地理', grades: [7, 8] },
  '物理': { id: 'phy', name: '物理', grades: [8, 9] },
  '数学': { id: 'math', name: '数学', grades: [7, 8, 9] },
  '历史': { id: 'hist', name: '历史', grades: [7, 8, 9] },
  '语文': { id: 'cn', name: '语文', grades: [7, 8, 9] },
  '英语': { id: 'eng', name: '英语', grades: [7, 8, 9] },
  '道德与法治': { id: 'pol', name: '道德与法治', grades: [7, 8, 9] }
};

function scanDir(dir, depth = 0) {
  const results = [];
  if (!existsSync(dir)) return results;
  const entries = readdirSync(dir);
  for (const entry of entries) {
    const fullPath = path.join(dir, entry);
    const stat = statSync(fullPath);
    if (stat.isDirectory()) {
      results.push(...scanDir(fullPath, depth + 1));
    } else if (entry.endsWith('.pdf')) {
      results.push({ fullPath, relativePath: path.relative(RESOURCE_ROOT, fullPath), name: entry, depth });
    }
  }
  return results;
}

function parsePdfInfo(pdf) {
  const name = pdf.name.replace('.pdf', '');
  const category = pdf.relativePath.split(path.sep)[0];
  
  // Determine subject and grade
  let subject = null;
  let grade = null;
  let term = null;
  let isStandard = category === '00 义务教育课程标准(2022年版)';
  
  for (const [key, info] of Object.entries(SUBJECT_MAP)) {
    if (name.includes(key)) {
      subject = info;
      break;
    }
  }
  
  // Try subject from folder name
  if (!subject) {
    for (const [key, info] of Object.entries(SUBJECT_MAP)) {
      if (category.includes(key)) {
        subject = info;
        break;
      }
    }
  }
  
  // Extract grade
  const gradeMatch = name.match(/([七八九]|7|8|9)年[级级]/);
  if (gradeMatch) {
    const g = gradeMatch[1];
    const gradeMap = { '七': 7, '八': 8, '九': 9, '7': 7, '8': 8, '9': 9 };
    grade = gradeMap[g] || null;
  }
  
  // Extract term
  if (name.includes('上册') || name.includes('全一册')) term = '上册';
  else if (name.includes('下册')) term = '下册';
  
  // Generate display name
  let displayName = name;
  if (isStandard) {
    displayName = name.replace(/^\d+\./, '').trim();
  }
  
  // Generate safe filename for copying
  let safeName = name.replace(/[（）()]/g, '').replace(/\s+/g, '') + '.pdf';
  if (subject && grade && term) {
    safeName = `${subject.name}${grade}年级${term}.pdf`;
  }
  if (isStandard) {
    safeName = name.replace(/^\d+\./, '').replace(/\s+/g, '') + '.pdf';
  }
  
  return {
    sourcePath: pdf.fullPath,
    destName: safeName,
    displayName,
    subject: subject ? subject.name : (isStandard ? '课程标准' : category),
    subjectId: subject ? subject.id : (isStandard ? 'standard' : null),
    grade,
    term,
    isStandard,
    category
  };
}

console.log('🔍 Scanning resource directory...');
const allPdfs = scanDir(RESOURCE_ROOT);
console.log(`   Found ${allPdfs.length} PDFs`);

const parsed = allPdfs.map(parsePdfInfo);

// Create library structure
const library = {
  generated: new Date().toISOString(),
  sourceRoot: RESOURCE_ROOT,
  totalPdfs: parsed.length,
  standards: [],
  subjects: {}
};

// Classify
for (const item of parsed) {
  if (item.isStandard) {
    library.standards.push({
      name: item.displayName,
      file: item.destName,
      source: item.sourcePath
    });
  } else if (item.subjectId) {
    if (!library.subjects[item.subjectId]) {
      library.subjects[item.subjectId] = {
        name: item.subject,
        id: item.subjectId,
        textbooks: []
      };
    }
    library.subjects[item.subjectId].textbooks.push({
      name: item.displayName,
      grade: item.grade,
      term: item.term,
      file: item.destName,
      source: item.sourcePath
    });
  }
}

// Sort textbooks by grade then term
for (const [id, subj] of Object.entries(library.subjects)) {
  subj.textbooks.sort((a, b) => {
    if (a.grade !== b.grade) return a.grade - b.grade;
    if (a.term === '上册') return -1;
    if (b.term === '上册') return 1;
    return 0;
  });
}

// Ensure pdf directory exists
if (!existsSync(PDF_DIR)) mkdirSync(PDF_DIR, { recursive: true });

// Copy PDFs
console.log('📋 Copying PDFs to project...');
let copied = 0;
for (const item of parsed) {
  const dest = path.join(PDF_DIR, item.destName);
  if (!existsSync(dest)) {
    try {
      copyFileSync(item.sourcePath, dest);
      copied++;
    } catch (err) {
      console.error(`   ⚠️  Failed to copy: ${item.sourcePath} -> ${dest}`);
      console.error(`      ${err.message}`);
    }
  }
}
console.log(`   Copied ${copied} new PDFs (${parsed.length - copied} already exist)`);

// Write manifest
writeFileSync(MANIFEST_PATH, JSON.stringify(library, null, 2), 'utf8');
console.log(`✅ Resource library written to: ${MANIFEST_PATH}`);
console.log(`   Standards: ${library.standards.length}`);
console.log(`   Subjects: ${Object.keys(library.subjects).length}`);
for (const [id, subj] of Object.entries(library.subjects)) {
  console.log(`     ${subj.name}: ${subj.textbooks.length} textbooks`);
}
