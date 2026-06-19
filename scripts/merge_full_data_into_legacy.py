import json
import re
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "index.html"
FULL = ROOT / "data" / "full_courses.json"

ICONS = {
    "bio": "🧬", "chem": "⚗️", "phy": "⚡", "math": "📐", "cn": "📖",
    "eng": "🌍", "hist": "🏛️", "geo": "🌏", "pol": "⚖️",
}
COLORS = {
    "bio": "#4CAF50", "chem": "#FF9800", "phy": "#2196F3", "math": "#E91E63",
    "cn": "#9C27B0", "eng": "#00BCD4", "hist": "#795548", "geo": "#8BC34A",
    "pol": "#607D8B",
}
GRADE_NAMES = {7: "七年级", 8: "八年级", 9: "九年级"}
SEM_NAMES = {"上": "上册", "下": "下册", "全": "全一册"}


def concept_detail(subject, title):
    method = {
        "bio": "观察现象、比较结构与功能，并联系生命活动来理解。",
        "chem": "从宏观现象、微观粒子和实验事实三个层面共同解释。",
        "phy": "先明确物理量和情境，再用实验或公式验证结论。",
        "math": "先辨析概念和条件，再通过例题迁移到新问题。",
        "cn": "结合文本内容、语言表达和作者情感进行分析。",
        "eng": "放到真实语境中理解词句，再进行听说读写输出。",
        "hist": "用时间线、地点和史料证据解释历史变化。",
        "geo": "结合地图、图表和区域特征进行综合判读。",
        "pol": "联系生活情境，完成价值判断和行动选择。",
    }.get(subject, "结合教材例子理解，并能迁移到练习中。")
    return f"围绕“{title}”，{method}"


def normalize_question(q):
    text = q.get("q") or q.get("question") or ""
    opts = q.get("options") or []
    opts = [re.sub(r"^[A-D][.．、]\s*", "", str(o)) for o in opts]
    qtype = q.get("type", "mc")
    answer = q.get("answer", "")
    if qtype not in {"mc", "fill"}:
        qtype = "fill"
        items = q.get("items") or opts
        if items:
            answer = " → ".join(str(x) for x in items)
            text = text + "（请按顺序填写）"
    return {
        "question": text,
        "options": opts if qtype == "mc" else [],
        "type": qtype,
        "fillPlaceholder": q.get("hint") or q.get("fillPlaceholder") or "输入答案...",
        "answer": answer,
        "explanation": q.get("explanation", ""),
    }


def build_payload():
    full = json.loads(FULL.read_text(encoding="utf-8"))
    grouped = defaultdict(list)
    free_counter = defaultdict(int)

    for item in full["items"]:
        subject = item["subject"]
        group_key = (subject, item["grade"], item["semester"])
        free_counter[group_key] += 1
        title = item["title"]
        if item.get("sectionLabel") and not title.startswith(item["sectionLabel"]):
            title = f"{item['sectionLabel']} {title}"
        book_page = item.get("bookPage") or 1
        pdf_real_page = item.get("pdfPage") or book_page
        keypoints = item.get("keypoints") or []
        quiz = item.get("quiz") or []
        old = {
            "id": item["id"],
            "title": title,
            "unitChapter": " · ".join([x for x in [item.get("unit"), item.get("chapter")] if x]),
            "pageTag": item.get("pageLabel") or f"P{book_page}",
            "isFree": free_counter[group_key] <= 3,
            "pdfFile": item.get("pdfFile"),
            "pdfPage": book_page,
            "pdfRealPage": pdf_real_page,
            "context": f"本节学习“{title}”。先查看教材对应页，再梳理知识点，最后完成随堂测试。",
            "concepts": [
                {"num": i + 1, "title": kp, "detail": concept_detail(subject, title)}
                for i, kp in enumerate(keypoints)
            ],
            "quizzes": [normalize_question(q) for q in quiz],
            "projects": [],
            "readings": [],
            "objectives": {
                "knowledge": keypoints,
                "ability": ["能结合教材材料解释本节核心问题", "能用本节方法完成基础与迁移练习"],
                "literacy": item.get("examPoints") or keypoints[:3],
            },
            "mindMap": {"center": title, "nodes": keypoints[:6]},
            "methods": {
                "approach": "教材阅读—知识梳理—练习反馈",
                "methods": item.get("methods") or [],
                "insights": [],
            },
            "grade": item["grade"],
            "semester": item["semester"],
        }
        grouped[subject].append(old)

    subjects = {}
    for subject, meta in full["subjects"].items():
        sem_counts = defaultdict(int)
        for item in grouped[subject]:
            sem_counts[(item["grade"], item["semester"])] += 1
        semesters = []
        for (grade, sem), count in sorted(sem_counts.items(), key=lambda x: (x[0][0], x[0][1])):
            semesters.append({
                "grade": grade,
                "semester": sem,
                "name": f"{GRADE_NAMES.get(grade, str(grade)+'年级')}{SEM_NAMES.get(sem, sem)}",
                "count": count,
            })
        subjects[subject] = {
            "name": meta["name"],
            "icon": ICONS.get(subject, meta.get("icon", "")),
            "color": COLORS.get(subject, meta.get("color", "#2563eb")),
            "semesters": semesters,
        }

    return subjects, dict(grouped)


def replace_const(text, name, value):
    encoded = json.dumps(value, ensure_ascii=False, separators=(",", ":"))
    pattern = rf"const {name} = .*?;\n"
    return re.sub(pattern, f"const {name} = {encoded};\n", text, count=1, flags=re.S)


def patch_index():
    subjects, all_data = build_payload()
    text = INDEX.read_text(encoding="utf-8")
    text = replace_const(text, "SUBJECTS", subjects)
    text = replace_const(text, "ALL_DATA", all_data)

    text = re.sub(
        r"const PDF_OFFSETS = .*?;\nfunction getPdfPage\(pdfFile, textbookPage\) \{\n.*?\n\}\n",
        "function getPdfPage(item) {\n"
        "  return item && item.pdfRealPage ? item.pdfRealPage : (item && item.pdfPage ? item.pdfPage : 1);\n"
        "}\n",
        text,
        count=1,
        flags=re.S,
    )
    text = text.replace(
        "      <button class=\"pdf-btn-inline\" onclick=\"openPdfViewer(ALL_DATA['${currentSubject}'].find(d=>d.id==='${item.id}'))\">📖 查看教材${item.pdfPage?'（第'+item.pdfPage+'页）':''}</button>",
        "      <button class=\"pdf-btn-inline\" onclick=\"openPdfViewer(ALL_DATA['${currentSubject}'].find(d=>d.id==='${item.id}'))\">📖 查看教材${item.pageTag ? '（书本'+item.pageTag+' / PDF第'+(item.pdfRealPage||item.pdfPage)+'页）' : ''}</button>",
    )
    text = text.replace(
        "  document.getElementById('pdfPageBadge').textContent = item.pdfPage ? '第 ' + item.pdfPage + ' 页' : '';",
        "  document.getElementById('pdfPageBadge').textContent = item.pdfPage ? ('书本 P' + item.pdfPage + ' / PDF 第 ' + getPdfPage(item) + ' 页') : '';",
    )
    text = text.replace(
        "    var page = item.pdfPage || 1;\n    var pdfRealPage = getPdfPage(item.pdfFile, page);\n    iframe.src = 'pdf/' + encodeURIComponent(item.pdfFile) + '#page=' + pdfRealPage + '&view=FitH';",
        "    var pdfRealPage = getPdfPage(item);\n    iframe.src = 'pdf/' + encodeURIComponent(item.pdfFile) + '#page=' + pdfRealPage + '&view=FitH';",
    )
    INDEX.write_text(text, encoding="utf-8")
    print(f"Merged {sum(len(v) for v in all_data.values())} sections into legacy index.html")


if __name__ == "__main__":
    patch_index()
