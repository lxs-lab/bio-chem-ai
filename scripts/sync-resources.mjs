import { readdir, stat, writeFile } from 'node:fs/promises';
import path from 'node:path';

const defaultSourceRoot = 'C:/Users/27170/WPSDrive/383859682/WPS云盘/Thought/AI教育/2026.05_AI教育课程设计/lxs/初中生课程培训';
const sourceRoot = process.env.COURSE_SOURCE_ROOT || defaultSourceRoot;
const outputFile = process.env.RESOURCE_MANIFEST || 'data/resource_manifest.json';

function detectType(name, extension) {
  if (name.includes('教科书')) return '教材';
  if (name.includes('课程标准')) return '课程标准';
  if (extension === 'md') return '方案文档';
  if (extension === 'py') return '脚本';
  if (extension === 'txt') return '链接清单';
  return '资源';
}

function detectSubject(relativePath) {
  const parts = relativePath.split('/');
  if (parts[0] !== '资源') return '课程设计';
  return parts[2] ? parts[1] : '资源总表';
}

async function walk(directory, files = []) {
  const entries = await readdir(directory, { withFileTypes: true });
  for (const entry of entries) {
    if (entry.name === 'desktop.ini') continue;
    const fullPath = path.join(directory, entry.name);
    if (entry.isDirectory()) {
      await walk(fullPath, files);
      continue;
    }

    const fileStat = await stat(fullPath);
    const relativePath = path.relative(sourceRoot, fullPath).split(path.sep).join('/');
    const extension = path.extname(entry.name).slice(1).toLowerCase();
    const grade = (entry.name.match(/[七八九]年级(?:上|下|全一)?册?/) || [''])[0];

    files.push({
      id: Buffer.from(relativePath).toString('base64url'),
      name: entry.name,
      relativePath,
      subject: detectSubject(relativePath),
      type: detectType(entry.name, extension),
      grade,
      extension,
      size: fileStat.size,
      sizeMB: Number((fileStat.size / 1024 / 1024).toFixed(2)),
      sourceRoot
    });
  }
  return files;
}

const files = await walk(sourceRoot);
files.sort((a, b) => a.subject.localeCompare(b.subject, 'zh-CN') || a.name.localeCompare(b.name, 'zh-CN'));

const totalSize = files.reduce((sum, file) => sum + file.size, 0);
const manifest = {
  generatedAt: new Date().toISOString(),
  sourceRoot,
  totalFiles: files.length,
  totalSize,
  totalSizeMB: Number((totalSize / 1024 / 1024).toFixed(2)),
  files
};

await writeFile(outputFile, `${JSON.stringify(manifest, null, 2)}\n`, 'utf8');
console.log(`Indexed ${manifest.totalFiles} files (${manifest.totalSizeMB} MB) from ${sourceRoot}`);
