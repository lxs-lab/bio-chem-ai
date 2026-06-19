"""
生成新的 index.html — 保留原有 UI/样式/AI聊天/游戏功能，
只替换 SUBJECTS、ALL_DATA 和相关的渲染逻辑。
"""
import json, re

# 读取新数据
with open(r'E:\Applications in E\workBuddy\2026~AI课程\bio-chem-ai\curriculum_new.json', 'r', encoding='utf-8') as f:
    new_data = json.load(f)

# 读取旧 index.html
with open(r'E:\Applications in E\workBuddy\2026~AI课程\bio-chem-ai\index.html', 'r', encoding='utf-8') as f:
    old_html = f.read()

# ===== 1. 构建新的 SUBJECTS =====
subjects_js = {}
for subj_code, info in new_data['subjects'].items():
    cur = new_data['curriculum'].get(subj_code, {})
    grade_data = cur.get('grades', {})
    semesters = []
    for g_str, sem_data in sorted(grade_data.items()):
        for sem_str, sem_info in sorted(sem_data.items()):
            semesters.append({
                'grade': int(g_str),
                'semester': sem_str,
                'name': sem_info['name'],
                'count': sem_info['count']
            })
    subjects_js[subj_code] = {
        'name': info['cn'],
        'icon': info['icon'],
        'color': info['color'],
        'semesters': semesters
    }

# ===== 2. 构建新的 ALL_DATA =====
# 按 subject 分组，每个知识点只保留核心字段（去掉了旧版复杂的 keypoints/examPoints 等）
all_data_js = {}
for item in new_data['all_items']:
    subj = item['subject']
    if subj not in all_data_js:
        all_data_js[subj] = []
    
    # 构建标题
    title = item.get('title', '')
    
    # 构建层级标签
    unit_info = item.get('unit_name', '') or item.get('unit', '')
    chapter_info = item.get('chapter_name', '') or item.get('chapter', '') or item.get('lesson', '')
    
    all_data_js[subj].append({
        'id': item['id'],
        'grade': item['grade'],
        'semester': item['semester'],
        'title': title,
        'unit': unit_info,
        'chapter': chapter_info,
        'section': item.get('section', '') or item.get('item_type', ''),
        'type': item.get('type', 'section')
    })

# ===== 3. 构建 JavaScript 代码 =====
subjects_str = json.dumps(subjects_js, ensure_ascii=False, separators=(',', ':'))
all_data_str = json.dumps(all_data_js, ensure_ascii=False)

# ===== 4. 找到替换边界 =====
# SUBJECTS 从 "const SUBJECTS = " 开始到第一个 ";" 
# ALL_DATA 从 "const ALL_DATA = {};" 到下一个 "// ============" 标记之前

subjects_start = old_html.find('const SUBJECTS = {')
subjects_end = old_html.find(';\n\n// ============ ALL DATA', subjects_start)
if subjects_end < 0:
    subjects_end = old_html.find(';\n\n//', subjects_start)

all_data_start = old_html.find('const ALL_DATA = {};')
all_data_end = old_html.find('\n// ============ RESOURCE LIBRARY', all_data_start)

print(f"SUBJECTS: {subjects_start} -> {subjects_end}")
print(f"ALL_DATA: {all_data_start} -> {all_data_end}")

if subjects_start < 0 or all_data_start < 0:
    print("ERROR: Could not find boundaries!")
    exit(1)

# ===== 5. 替换 =====
new_subjects_block = f'const SUBJECTS = {subjects_str};\n\n// 年级-学期信息\nconst GRADE_NAMES = {{7: "七年级", 8: "八年级", 9: "九年级"}};\nconst SEM_NAMES = {{"上": "上册", "下": "下册", "全": "全一册"}};'

new_all_data_block = f'const ALL_DATA = {all_data_str};'

# 执行替换
new_html = old_html[:subjects_start] + new_subjects_block + old_html[subjects_end+1:all_data_start] + new_all_data_block + old_html[all_data_end:]

# ===== 6. 更新渲染函数 =====
# 找到 renderCourseCards 函数并替换
# 需要修改的逻辑：
# 1. renderCourseCards: 主页面显示9门学科卡片（不变）
# 2. 点击学科后：显示该学科的年级→学期选择
# 3. 选好学期后：显示知识点大纲

# 找到 openSubject 相关逻辑
# 搜索 "function openSubject" 或类似的函数
# 如果没有，需要找到点击学科卡片后的处理逻辑

# 先找到 renderCourseCards 函数
cards_func = new_html.find('function renderCourseCards')
print(f"renderCourseCards at: {cards_func}")

# 找到 view 切换逻辑
view_patterns = ['currentView', 'openSubject', 'switchView', 'showSyllabus']
for p in view_patterns:
    pos = new_html.find(p)
    if pos >= 0:
        line = new_html[:pos].count('\n') + 1
        ctx = new_html[max(0,pos-30):pos+80]
        print(f"  {p} at line {line}: ...{ctx}...")

# 保存
out_path = r'E:\Applications in E\workBuddy\2026~AI课程\bio-chem-ai\index_new.html'
with open(out_path, 'w', encoding='utf-8') as f:
    f.write(new_html)
print(f'\nSaved to {out_path} ({len(new_html)} chars)')
