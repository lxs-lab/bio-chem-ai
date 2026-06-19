"""
将 curriculum_structured.json 转换为 index.html 可用的 ALL_DATA 格式
新格式：按 科目 → 年级 → 学期 → 知识点 组织
每个知识点有：id, subject, grade, semester, unit, chapter, section, title
"""
import json, re

with open(r'E:\Applications in E\workBuddy\2026~AI课程\bio-chem-ai\curriculum_structured.json', 'r', encoding='utf-8') as f:
    curriculum = json.load(f)

# 英汉数字转换
CN_NUM = {'一':'1','二':'2','三':'3','四':'4','五':'5','六':'6','七':'7','八':'8','九':'9','十':'10',
          '十一':'11','十二':'12','十三':'13','十四':'14','十五':'15','十六':'16','十七':'17','十八':'18',
          '十九':'19','二十':'20','二十一':'21','二十二':'22','二十三':'23','二十四':'24'}

def cn_to_num(s):
    for cn, num in CN_NUM.items():
        s = s.replace(cn, num)
    return s

# 学科中英文映射
SUBJ_MAP = {
    'bio': {'cn': '生物学', 'icon': '🧬', 'color': '#4CAF50'},
    'chem': {'cn': '化学', 'icon': '⚗️', 'color': '#FF9800'},
    'phy': {'cn': '物理', 'icon': '⚡', 'color': '#2196F3'},
    'math': {'cn': '数学', 'icon': '📐', 'color': '#E91E63'},
    'cn': {'cn': '语文', 'icon': '📖', 'color': '#9C27B0'},
    'eng': {'cn': '英语', 'icon': '🌍', 'color': '#00BCD4'},
    'hist': {'cn': '历史', 'icon': '🏛️', 'color': '#795548'},
    'geo': {'cn': '地理', 'icon': '🌏', 'color': '#8BC34A'},
    'pol': {'cn': '道德与法治', 'icon': '⚖️', 'color': '#607D8B'},
}

GRADE_NAMES = {7: '七年级', 8: '八年级', 9: '九年级'}
SEM_NAMES = {'上': '上册', '下': '下册', '全': '全一册'}

all_items = []

# 英语的硬编码Unit列表（从"致同学"页面提取）
ENG_UNITS = {
    'eng-7上': [
        ('Starter Unit 1', 'Hello! 打招呼'),
        ('Starter Unit 2', 'Keep Tidy! 摆放物品'),
        ('Starter Unit 3', 'Welcome! 参观农家小院'),
        ('Unit 1', "You and Me 结识新朋友"),
        ('Unit 2', "We're Family! 介绍家庭"),
        ('Unit 3', "My School 熟悉校园"),
        ('Unit 4', "My Favourite Subject 谈论科目喜好"),
        ('Unit 5', "Fun Clubs 加入学校社团"),
        ('Unit 6', "A Day in the Life 做好时间安排"),
        ('Unit 7', "Happy Birthday! 庆祝生日"),
    ],
    'eng-7下': [
        ('Unit 1', 'Animal Friends 谈论动物'),
        ('Unit 2', 'No Rules, No Order 规章制度'),
        ('Unit 3', 'Keep Fit 运动与锻炼'),
        ('Unit 4', 'Eat Well 健康饮食'),
        ('Unit 5', 'Here and Now 时区与生活'),
        ('Unit 6', 'Rain or Shine 天气与情绪'),
        ('Unit 7', 'A Day to Remember 难忘的一天'),
        ('Unit 8', 'Once upon a Time 中外经典故事'),
    ],
    'eng-8上': [
        ('Unit 1', 'Where did you go on vacation? 假期经历'),
        ('Unit 2', "How often do you exercise? 家庭与'家'的内涵"),
        ('Unit 3', "I'm more outgoing than my sister. 和而不同"),
        ('Unit 4', "What's the best movie theater? 神奇的动植物"),
        ('Unit 5', 'Do you want to watch a game show? 烹饪中西方美食'),
        ('Unit 6', "I'm going to study computer science. 自我提升计划"),
        ('Unit 7', 'Will people have robots? 畅想未来'),
        ('Unit 8', 'How do you make a banana milk shake? 沟通交流'),
    ],
    'eng-8下': [
        ('Unit 1', "What's the matter? 学习与休闲平衡"),
        ('Unit 2', "I'll help to clean up the city parks. 生命安全"),
        ('Unit 3', 'Could you please clean your room? 积极乐观心态'),
        ('Unit 4', "Why don't you talk to your parents? 自然奇观"),
        ('Unit 5', 'What were you doing when the rainstorm came? 自然灾害'),
        ('Unit 6', "An old man tried to move the mountains. 跨文化沟通"),
        ('Unit 7', "What's the highest mountain in the world? 经典文学"),
        ('Unit 8', 'Have you read Treasure Island yet? 环境保护'),
    ],
    'eng-9全': [
        ('Unit 1', 'How can we become good learners? 学习方法'),
        ('Unit 2', 'I think that mooncakes are delicious! 节日文化'),
        ('Unit 3', 'Could you please tell me where the restrooms are? 礼貌询问'),
        ('Unit 4', 'I used to be afraid of the dark. 成长变化'),
        ('Unit 5', 'What are the shirts made of? 中国制造'),
        ('Unit 6', 'When was it invented? 发明创造'),
        ('Unit 7', 'Teenagers should be allowed to choose their own clothes. 规则与自由'),
        ('Unit 8', 'It must belong to Carla. 推理与猜测'),
        ('Unit 9', 'I like music that I can dance to. 音乐与电影'),
        ('Unit 10', "You're supposed to shake hands. 文化礼仪"),
        ('Unit 11', 'Sad movies make me cry. 情绪与感受'),
        ('Unit 12', "Life is full of the unexpected. 意外事件"),
        ('Unit 13', "We're trying to save the earth! 环境保护"),
        ('Unit 14', 'I remember meeting all of you in Grade 7. 毕业回忆'),
    ],
}

for key, data in sorted(curriculum.items()):
    subj = data['subject_en']
    grade = data['grade']
    sem = data['semester']
    entries = data['entries']
    
    # Handle English separately
    if subj == 'eng':
        if key in ENG_UNITS:
            for unit_label, unit_name in ENG_UNITS[key]:
                all_items.append({
                    'id': f"{subj}-{grade}{sem}-{unit_label.replace(' ','-')}",
                    'subject': subj,
                    'grade': grade,
                    'semester': sem,
                    'title': f"{unit_label}: {unit_name}",
                    'unit': unit_label,
                    'type': 'unit'
                })
        continue
    
    # Handle other subjects
    item_idx = 0
    for entry in entries:
        unit_name = entry.get('unit_name', '')
        
        # Case 1: has non-empty chapters with sections (bio, phy, math, geo)
        if entry.get('chapters') and len(entry['chapters']) > 0:
            for ch in entry['chapters']:
                ch_name = ch.get('chapter_name', '')
                for sec in ch.get('sections', []):
                    sec_name = sec.get('section_name', '')
                    item_idx += 1
                    all_items.append({
                        'id': f"{subj}-{grade}{sem}-{item_idx:03d}",
                        'subject': subj,
                        'grade': grade,
                        'semester': sem,
                        'title': sec_name,
                        'unit': entry.get('unit', ''),
                        'unit_name': unit_name,
                        'chapter': ch.get('chapter', ''),
                        'chapter_name': ch_name,
                        'section': sec.get('section', ''),
                        'type': 'section'
                    })
        
        # Case 2: has lessons (hist, pol)
        elif 'lessons' in entry:
            for lesson in entry.get('lessons', []):
                lesson_name = lesson.get('lesson_name', '')
                item_idx += 1
                all_items.append({
                    'id': f"{subj}-{grade}{sem}-{item_idx:03d}",
                    'subject': subj,
                    'grade': grade,
                    'semester': sem,
                    'title': lesson_name,
                    'unit': entry.get('unit', ''),
                    'unit_name': unit_name,
                    'lesson': lesson.get('lesson', ''),
                    'type': 'lesson'
                })
        
        # Case 3: direct sections (some bio/chem entries)
        elif 'sections' in entry:
            for sec in entry.get('sections', []):
                sec_name = sec.get('section_name', '')
                item_idx += 1
                all_items.append({
                    'id': f"{subj}-{grade}{sem}-{item_idx:03d}",
                    'subject': subj,
                    'grade': grade,
                    'semester': sem,
                    'title': sec_name,
                    'unit': entry.get('unit', ''),
                    'unit_name': unit_name,
                    'section': sec.get('section', ''),
                    'type': 'section'
                })
        
        # Case 4: items (cn 语文)
        elif 'items' in entry:
            for item in entry.get('items', []):
                item_name = item.get('name', '')
                item_idx += 1
                all_items.append({
                    'id': f"{subj}-{grade}{sem}-{item_idx:03d}",
                    'subject': subj,
                    'grade': grade,
                    'semester': sem,
                    'title': item_name,
                    'unit': entry.get('unit', ''),
                    'unit_name': unit_name,
                    'item_type': item.get('type', ''),
                    'type': 'item'
                })

# Build summary
summary = {}
for subj_code in SUBJ_MAP:
    subj_items = [i for i in all_items if i['subject'] == subj_code]
    if not subj_items:
        continue
    grades = sorted(set(i['grade'] for i in subj_items))
    grade_data = {}
    for g in grades:
        sems = sorted(set(i['semester'] for i in subj_items if i['grade'] == g))
        sem_data = {}
        for s in sems:
            sem_items = [i for i in subj_items if i['grade'] == g and i['semester'] == s]
            sem_data[s] = {
                'name': f"{GRADE_NAMES[g]}{SEM_NAMES[s]}",
                'count': len(sem_items),
                'items': sem_items
            }
        grade_data[str(g)] = sem_data
    summary[subj_code] = {
        **SUBJ_MAP[subj_code],
        'grades': grade_data,
        'total_items': len(subj_items)
    }
    print(f"{subj_code}({SUBJ_MAP[subj_code]['cn']}): {len(subj_items)} items across {len(grades)} grades")

# Save
out = {
    'subjects': SUBJ_MAP,
    'all_items': all_items,
    'curriculum': summary
}

out_path = r'E:\Applications in E\workBuddy\2026~AI课程\bio-chem-ai\curriculum_new.json'
with open(out_path, 'w', encoding='utf-8') as f:
    json.dump(out, f, ensure_ascii=False, indent=2)
print(f'\nTotal: {len(all_items)} items saved to {out_path}')
