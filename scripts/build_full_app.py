import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
PDF_DIR = ROOT / "pdf"

SUBJECTS = {
    "bio": {"name": "生物学", "short": "生物", "icon": "B", "color": "#16a34a"},
    "chem": {"name": "化学", "short": "化学", "icon": "C", "color": "#7c3aed"},
    "phy": {"name": "物理", "short": "物理", "icon": "P", "color": "#dc2626"},
    "math": {"name": "数学", "short": "数学", "icon": "M", "color": "#2563eb"},
    "cn": {"name": "语文", "short": "语文", "icon": "Y", "color": "#db2777"},
    "eng": {"name": "英语", "short": "英语", "icon": "E", "color": "#0891b2"},
    "hist": {"name": "历史", "short": "历史", "icon": "H", "color": "#78716c"},
    "geo": {"name": "地理", "short": "地理", "icon": "G", "color": "#d97706"},
    "pol": {"name": "道德与法治", "short": "道德与法治", "icon": "F", "color": "#0f766e"},
}

BOOK_OFFSETS = {
    # Verified from rendered/extracted table-of-contents pages: PDF page = printed book page + offset.
    "bio": 6,
    "chem": 6,
    "geo": 5,
    "phy": 5,
    "math": 4,
    "cn": 3,
    "eng": 4,
    "hist": 3,
    "pol": 3,
}

METHODS = {
    "bio": ["观察比较", "结构与功能", "生命观念"],
    "chem": ["宏观辨识", "微观探析", "实验探究"],
    "phy": ["情境建模", "实验验证", "公式应用"],
    "math": ["概念辨析", "例题迁移", "规范表达"],
    "cn": ["整体感知", "语言品味", "读写迁移"],
    "eng": ["听说输入", "语境操练", "输出表达"],
    "hist": ["时空定位", "史料实证", "因果分析"],
    "geo": ["读图定位", "区域比较", "综合分析"],
    "pol": ["情境辨析", "价值判断", "行动建议"],
}


def clean_name(value):
    value = str(value or "").replace("\u3000", " ")
    value = re.sub(r"[.·…]{2,}", " ", value)
    value = re.sub(r"\s+", " ", value).strip()
    value = re.sub(r"\s*\d+\s*$", "", value).strip()
    return value


def canonical_title(value):
    value = clean_name(value)
    value = re.sub(r"^第[一二三四五六七八九十0-9]+[章节课]\s*", "", value)
    value = re.sub(r"^课题\s*[一二三四五六七八九十0-9]+\s*", "", value)
    value = re.sub(r"^\d+(\.\d+)*\s*", "", value)
    return value.strip()


def page_number(value):
    value = str(value or "").replace("\u3000", " ")
    nums = re.findall(r"(\d+)\s*$", value)
    return int(nums[-1]) if nums else None


def load_existing():
    merged = {}
    for key in SUBJECTS:
        path = DATA / f"{key}_data.json"
        if not path.exists():
            continue
        items = json.loads(path.read_text(encoding="utf-8"))
        for item in items:
            title = canonical_title(item.get("section") or item.get("title"))
            merged[(key, title)] = item
    return merged


def find_pdf(subject, grade, semester, pdfs):
    short = SUBJECTS[subject]["short"]
    if subject == "eng":
        if grade == 7 and semester == "上":
            needles = ["英语", "七年级_上册"]
        elif grade == 7 and semester == "下":
            needles = ["英语", "七年级_下册"]
        elif grade == 8 and semester == "上":
            needles = ["英语八年级上册"]
        elif grade == 8 and semester == "下":
            needles = ["英语八年级下册"]
        else:
            needles = ["英语九年级全一册"]
    elif semester == "全":
        needles = [short, f"{grade}年级", "全一册"]
        if subject == "phy":
            needles = [short, f"{grade}年级上册"]
    else:
        needles = [short, f"{grade}年级{semester}册"]

    for name in pdfs:
        if all(n in name for n in needles):
            return name
    for name in pdfs:
        if short in name and str(grade) in name:
            return name
    return ""


def generic_keypoints(subject, title, unit, chapter):
    methods = METHODS.get(subject, METHODS["math"])
    return [
        f"明确“{title}”的核心概念、适用条件和常见表达方式",
        f"把本节内容放回“{unit} / {chapter}”中，理解它与前后知识的联系",
        f"用{methods[0]}的方法提取关键词、图表信息或文本证据",
        f"用{methods[1]}的方法解释典型例题、实验现象或材料情境",
        f"通过{methods[2]}完成课堂练习，形成可复述、可迁移的学习结论",
    ]


def generic_quiz(subject, title):
    methods = METHODS.get(subject, METHODS["math"])
    return [
        {
            "type": "mc",
            "q": f"学习“{title}”时，最先要抓住的是哪一项？",
            "options": ["核心概念和关键词", "只背页码", "跳过教材", "只看答案"],
            "answer": 0,
            "explanation": "先建立概念框架，再做题和应用，学习效率最高。",
        },
        {
            "type": "mc",
            "q": f"把“{title}”学扎实，最适合的课堂做法是？",
            "options": ["结合教材情境分析", "只抄标题", "不做记录", "完全依赖猜测"],
            "answer": 0,
            "explanation": "教材情境、图表和活动是理解本节重点的重要依据。",
        },
        {
            "type": "fill",
            "q": f"本节复习时，可以用“概念梳理→{methods[0]}→练习反馈”的路径完成闭环，其中第二步是___。",
            "answer": methods[0],
            "hint": "看本节学习方法",
            "explanation": f"{methods[0]}是本节建议的关键学习方法之一。",
        },
    ]


def normalize_quiz(quiz):
    normalized = []
    for q in quiz or []:
        nq = {
            "type": q.get("type", "mc"),
            "q": q.get("q") or q.get("question", ""),
            "options": q.get("options", []),
            "answer": q.get("answer"),
            "hint": q.get("hint", ""),
            "explanation": q.get("explanation", ""),
        }
        if nq["type"] == "fill" and nq["answer"] is None:
            nq["answer"] = ""
        normalized.append(nq)
    return normalized


def build():
    curriculum = json.loads((ROOT / "curriculum_new.json").read_text(encoding="utf-8"))
    existing = load_existing()
    pdfs = [p.name for p in PDF_DIR.glob("*.pdf")]
    items = []
    seen = set()

    for raw in curriculum["all_items"]:
        subject = raw["subject"]
        title = clean_name(raw.get("title"))
        if not title:
            continue
        grade = int(raw["grade"])
        semester = raw.get("semester") or ""
        book_page = page_number(raw.get("title")) or 1
        unit = clean_name(raw.get("unit_name") or raw.get("unit"))
        chapter = clean_name(raw.get("chapter_name") or raw.get("chapter"))
        dedupe_key = (subject, grade, semester, canonical_title(title))
        if dedupe_key in seen:
            continue
        seen.add(dedupe_key)
        existing_item = existing.get((subject, canonical_title(title)), {})
        keypoints = existing_item.get("keypoints") or generic_keypoints(subject, title, unit, chapter)
        quiz = normalize_quiz(existing_item.get("quiz")) or generic_quiz(subject, title)
        pdf_file = existing_item.get("pdf_file") or find_pdf(subject, grade, semester, pdfs)
        pdf_page = max(1, book_page + BOOK_OFFSETS.get(subject, 4))

        items.append({
            "id": raw["id"],
            "subject": subject,
            "subjectName": SUBJECTS[subject]["name"],
            "grade": grade,
            "semester": semester,
            "title": title,
            "unit": unit or raw.get("unit", ""),
            "chapter": chapter or raw.get("chapter", ""),
            "sectionLabel": raw.get("section", ""),
            "bookPage": book_page,
            "pageLabel": f"P{book_page}",
            "pdfFile": pdf_file,
            "pdfPage": pdf_page,
            "isFree": bool(existing_item.get("free", False)) or len(items) < 18,
            "keypoints": keypoints,
            "examPoints": existing_item.get("examPoints") or keypoints[:3],
            "quiz": quiz,
            "methods": METHODS.get(subject, []),
        })

    payload = {
        "subjects": SUBJECTS,
        "offsets": BOOK_OFFSETS,
        "items": items,
    }
    (DATA / "full_courses.json").write_text(
        json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print(f"Wrote {len(items)} items to data/full_courses.json")


if __name__ == "__main__":
    build()
