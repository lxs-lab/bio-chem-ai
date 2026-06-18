import { createServer } from 'node:http';
import { readFile } from 'node:fs/promises';
import { createReadStream, existsSync } from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const PORT = Number(process.env.PORT || 3000);

const SUBJECTS = {
  bio: { name: '生物学', icon: '🧬', color: '#5b9a6b', dataFile: 'bio_data.json', grades: [7, 8] },
  chem: { name: '化学', icon: '⚗️', color: '#4a90b8', dataFile: 'chem_data.json', grades: [9] },
  geo: { name: '地理', icon: '🗺️', color: '#8B6914', dataFile: 'geo_data.json', grades: [7, 8] },
  phy: { name: '物理', icon: '⚡', color: '#e87d4b', dataFile: 'phy_data.json', grades: [8, 9] },
  math: { name: '数学', icon: '📐', color: '#4a90b8', dataFile: 'math_data.json', grades: [7, 8, 9] },
  cn: { name: '语文', icon: '📖', color: '#8b6baa', dataFile: 'cn_data.json', grades: [7, 8, 9] },
  eng: { name: '英语', icon: '🔤', color: '#e87d4b', dataFile: 'eng_data.json', grades: [7, 8, 9] },
  hist: { name: '历史', icon: '🏛️', color: '#8B6914', dataFile: 'hist_data.json', grades: [7, 8, 9] },
  pol: { name: '道德与法治', icon: '⚖️', color: '#2E8B85', dataFile: 'pol_data.json', grades: [7, 8, 9] }
};

const MIME_TYPES = {
  '.html': 'text/html; charset=utf-8',
  '.css': 'text/css; charset=utf-8',
  '.js': 'application/javascript; charset=utf-8',
  '.json': 'application/json; charset=utf-8',
  '.pdf': 'application/pdf',
  '.md': 'text/markdown; charset=utf-8',
  '.txt': 'text/plain; charset=utf-8',
  '.png': 'image/png',
  '.jpg': 'image/jpeg',
  '.jpeg': 'image/jpeg',
  '.svg': 'image/svg+xml',
  '.ico': 'image/x-icon'
};

async function readJson(relativePath) {
  const filePath = path.join(__dirname, relativePath);
  const text = await readFile(filePath, 'utf8');
  return JSON.parse(text);
}

function sendJson(res, data, status = 200) {
  const body = JSON.stringify(data, null, 2);
  res.writeHead(status, {
    'Content-Type': 'application/json; charset=utf-8',
    'Cache-Control': 'no-store'
  });
  res.end(body);
}

function sendError(res, status, message) {
  sendJson(res, { error: message, status }, status);
}

function normalizeStaticPath(urlPath) {
  const decoded = decodeURIComponent(urlPath);
  const requested = decoded === '/' ? '/index.html' : decoded;
  const safePath = path.normalize(requested).replace(/^(\.\.[/\\])+/, '');
  return path.join(__dirname, safePath);
}

async function handleApi(req, res, url) {
  if (url.pathname === '/api/health') {
    sendJson(res, { ok: true, app: 'bio-chem-ai', version: '6.0.0' });
    return;
  }

  if (url.pathname === '/api/courses') {
    const courses = await Promise.all(Object.entries(SUBJECTS).map(async ([id, meta]) => {
      const data = await readJson(`data/${meta.dataFile}`);
      const quizCount = data.reduce((sum, item) => sum + (item.quiz ? item.quiz.length : 0), 0);
      const gameTypes = [...new Set(data.filter(item => item.gameType).map(item => item.gameType))];
      return {
        id, name: meta.name, icon: meta.icon, color: meta.color,
        knowledgeCount: data.length, quizCount,
        gameTypeCount: gameTypes.length, gameTypes
      };
    }));
    sendJson(res, courses);
    return;
  }

  // Resource library API - full textbook & standards catalog
  if (url.pathname === '/api/library') {
    const library = await readJson('data/resource_library.json');
    sendJson(res, library);
    return;
  }

  const courseMatch = url.pathname.match(/^\/api\/courses\/([a-z]+)$/);
  if (courseMatch) {
    const subject = courseMatch[1];
    const meta = SUBJECTS[subject];
    if (!meta) {
      sendError(res, 404, 'Unknown subject');
      return;
    }
    const data = await readJson(`data/${meta.dataFile}`);
    sendJson(res, { id: subject, name: meta.name, items: data });
    return;
  }

  if (url.pathname === '/api/resources') {
    const manifest = await readJson('data/resource_manifest.json');
    const subject = url.searchParams.get('subject');
    const type = url.searchParams.get('type');
    const q = (url.searchParams.get('q') || '').trim().toLowerCase();
    let files = manifest.files;
    if (subject) files = files.filter(file => file.subject === subject);
    if (type) files = files.filter(file => file.type === type);
    if (q) {
      files = files.filter(file =>
        file.name.toLowerCase().includes(q) ||
        file.relativePath.toLowerCase().includes(q)
      );
    }
    sendJson(res, {
      generatedAt: manifest.generatedAt,
      totalFiles: manifest.totalFiles,
      totalSizeMB: manifest.totalSizeMB,
      count: files.length,
      files
    });
    return;
  }

  sendError(res, 404, 'API route not found');
}

function serveStatic(req, res, url) {
  const filePath = normalizeStaticPath(url.pathname);
  if (!filePath.startsWith(__dirname) || !existsSync(filePath)) {
    sendError(res, 404, 'File not found');
    return;
  }
  const ext = path.extname(filePath).toLowerCase();
  res.writeHead(200, {
    'Content-Type': MIME_TYPES[ext] || 'application/octet-stream',
    'Cache-Control': ext === '.html' ? 'no-store' : 'public, max-age=3600'
  });
  createReadStream(filePath).pipe(res);
}

createServer(async (req, res) => {
  try {
    const url = new URL(req.url || '/', `http://${req.headers.host || 'localhost'}`);
    if (url.pathname.startsWith('/api/')) {
      await handleApi(req, res, url);
      return;
    }
    serveStatic(req, res, url);
  } catch (error) {
    console.error(error);
    sendError(res, 500, 'Internal server error');
  }
}).listen(PORT, () => {
  console.log(`Bio Chem AI server running at http://localhost:${PORT}`);
});
