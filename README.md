# 智慧学堂 - 初中全科 AI 学习平台

这是一个可直接部署到 GitHub Pages 的静态学习网站，覆盖初中多学科教材目录、知识点罗列、随堂测试、教材 PDF 对应页查看和右侧 AI 问答。

## 在线访问

如果 GitHub Pages 已启用，访问：

```text
https://lxs-lab.github.io/bio-chem-ai/
```

分享给别人时，直接发送这个链接即可。页面内每个小节都会生成 `#section=...` 形式的链接，打开后可以直达对应课程。

## 本地运行

```bash
npm start
```

然后打开：

```text
http://localhost:3000
```

不建议直接双击 `index.html`，因为浏览器可能限制本地 `fetch` 读取 `data/full_courses.json`。

## 数据说明

- `data/full_courses.json`：全量课程数据，包含 747 个有效小节/课题。
- `pdf/`：教材与课程标准 PDF。
- `scripts/build_full_app.py`：从全量目录和已有精修数据生成统一课程数据。
- `scripts/render_full_index.py`：生成新的动态主页。

重新生成数据和主页：

```bash
python scripts/build_full_app.py
python scripts/render_full_index.py
```

## 教材页码

系统同时显示：

- 书本页码：教材目录中的印刷页码，例如 `P2`。
- PDF 页码：浏览器 PDF 查看器实际跳转页码，例如 `PDF 第 8 页`。

两者不同是正常现象，因为 PDF 前面包含封面、版权页、目录等页面。

## 上传 GitHub

```bash
git add .
git commit -m "Build full curriculum learning workspace"
git push origin master
```

推送后，如果仓库启用了 GitHub Pages，等待 Pages 自动部署完成即可通过线上链接访问。
