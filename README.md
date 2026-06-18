# 智慧学堂 · 初中 AI 辅助学习

面向初中生物、化学、地理地图专题的 AI 辅助学习项目。当前版本保留静态单页能力，同时新增 Node 后端 API，方便后续扩展资料库、课程数据、AI 服务和用户系统。

地理七上第二章“地图”已升级为“长征路上的地图课”：用遵义、赤水、泸定桥、夹金山、吴起五个长征场景串联方向、比例尺、图例、等高线、分层设色、地形剖面图和综合读图训练。

## 本地运行

```bash
npm start
```

打开：

```text
http://localhost:3000
```

## API

- `GET /api/health`：服务健康检查
- `GET /api/courses`：三科课程概览
- `GET /api/courses/bio`：生物课程数据
- `GET /api/courses/chem`：化学课程数据
- `GET /api/courses/geo`：地理地图专题数据
- `GET /api/resources`：WPS 课程资料索引，支持 `subject`、`type`、`q` 查询参数

## 资料同步

项目同步了 WPS 资料库中的关键资料：

- `docs/course-design/`：课程设计文档
- `pdf/义务教育地理课程标准2022版.pdf`
- `pdf/义务教育地理七年级上册.pdf`
- `data/resource_manifest.json`：WPS 资料库全量索引

刷新资源索引：

```bash
npm run sync:resources
```

如果资料根目录变化，可以指定：

```bash
COURSE_SOURCE_ROOT=/path/to/初中生课程培训 npm run sync:resources
```

## 部署说明

`index.html` 仍可作为静态页面运行，适合 GitHub Pages。通过 `node server.js` 运行时，前端会优先从 `/api/courses/:subject` 加载数据；API 不可用时会自动使用页面内置数据作为回退。

## 地理数据生成

长征叙事版地理数据由脚本生成：

```bash
npm run build:geo
```

该命令会同步更新 `data/geo_data.json` 和 `index.html` 中的静态 `GEO_DATA` 回退数据。
