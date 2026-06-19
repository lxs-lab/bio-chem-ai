import json, re, os

all_tocs_path = r'E:\Applications in E\workBuddy\2026~AI课程\bio-chem-ai\all_tocs.json'
with open(all_tocs_path, 'r', encoding='utf-8') as f:
    all_tocs = json.load(f)


def parse_bio_chem(text):
    entries = []
    current_unit = None
    current_chapter = None

    for line in text.split('\n'):
        line = line.strip()
        if not line or len(line) < 3:
            continue
        if any(kw in line for kw in ['栏目介绍', '致同学', '写在前面', '前言']):
            continue

        m = re.match(r'第([一二三四五六七八九十]+)单元\s+(.+)', line)
        if m:
            current_unit = {'unit': f'第{m.group(1)}单元', 'unit_name': m.group(2).strip(), 'chapters': []}
            entries.append(current_unit)
            current_chapter = None
            continue

        m = re.match(r'第([一二三四五六七八九十\d]+)章\s+(.+)', line)
        if m:
            current_chapter = {'chapter': f'第{m.group(1)}章', 'chapter_name': m.group(2).strip(), 'sections': []}
            if current_unit:
                current_unit['chapters'].append(current_chapter)
            else:
                entries.append(current_chapter)
            continue

        m = re.match(r'(第[一二三四五六七八九十\d]+节|课题\d+)\s+(.+)', line)
        if m:
            sec_label = m.group(1)
            sec_name = m.group(2).strip()
            if current_chapter:
                current_chapter['sections'].append({'section': sec_label, 'section_name': sec_name})
            elif current_unit:
                current_unit.setdefault('sections', []).append({'section': sec_label, 'section_name': sec_name})
            continue

        if re.match(r'^\d{1,3}$', line):
            continue

    return entries


def parse_phy(text):
    entries = []
    current_chapter = None

    for line in text.split('\n'):
        line = line.strip()
        if not line or len(line) < 3:
            continue
        if any(kw in line for kw in ['栏目介绍', '致同学', '前言']):
            continue

        m = re.match(r'第([一二三四五六七八九十\d]+)章\s+(.+)', line)
        if m:
            current_chapter = {'chapter': f'第{m.group(1)}章', 'chapter_name': m.group(2).strip(), 'sections': []}
            entries.append(current_chapter)
            continue

        m = re.match(r'第([一二三四五六七八九十\d]+)节\s+(.+)', line)
        if m:
            sec_label = f'第{m.group(1)}节'
            sec_name = m.group(2).strip()
            if current_chapter:
                current_chapter['sections'].append({'section': sec_label, 'section_name': sec_name})
            continue

    return entries


def parse_math(text):
    entries = []
    current_chapter = None

    for line in text.split('\n'):
        line = line.strip()
        if not line or len(line) < 3:
            continue
        if any(kw in line for kw in ['栏目介绍', '致同学', '前言', '本册导引']):
            continue

        m = re.match(r'第([一二三四五六七八九十\d]+)章\s+(.+)', line)
        if m:
            current_chapter = {'chapter': f'第{m.group(1)}章', 'chapter_name': m.group(2).strip(), 'sections': []}
            entries.append(current_chapter)
            continue

        # 匹配半角数字: 1.1, 2.3 等
        m = re.match(r'(\d+\.\d+)\s+(.+)', line)
        if m and current_chapter:
            sec_label = m.group(1)
            sec_name = m.group(2).strip()
            if any(kw in sec_name for kw in ['数学活动', '小结', '复习题', '阅读与思考']):
                continue
            current_chapter['sections'].append({'section': sec_label, 'section_name': sec_name})
            continue
        
        # 匹配全角数字: １．１, ２．３ 等（PDF提取的常见格式）
        m = re.match(r'([\uff10-\uff19]+[．.][\uff10-\uff19]+)\s+(.+)', line)
        if m and current_chapter:
            sec_label = m.group(1)
            sec_name = m.group(2).strip()
            if any(kw in sec_name for kw in ['数学活动', '小结', '复习题', '阅读与思考']):
                continue
            # 转换为半角
            sec_label_normal = sec_label.translate(str.maketrans(
                '\uff10\uff11\uff12\uff13\uff14\uff15\uff16\uff17\uff18\uff19\uff0e',
                '0123456789.'
            ))
            current_chapter['sections'].append({'section': sec_label_normal, 'section_name': sec_name})
            continue

        if re.match(r'^(小结|复习题|数学活动)', line):
            continue

    return entries


def parse_hist(text):
    """历史目录特殊格式：课在前，单元标题在课之间插入"""
    entries = []
    current_unit = None
    
    # Two-pass approach: first extract all lessons with their page numbers,
    # then find unit boundaries
    lessons = []
    unit_positions = []  # (line_idx, unit_label, unit_name)
    
    lines = text.split('\n')
    for i, line in enumerate(lines):
        line = line.strip()
        if not line or len(line) < 3:
            continue
        if any(kw in line for kw in ['栏目介绍', '致同学', '前言']):
            continue
        
        # Unit header: standalone line with "第X单元" followed by subtitle on next line
        m = re.match(r'第([一二三四五六七八九十]+)单元\s*$', line)
        if m:
            # Check next line for unit name
            unit_name = ''
            if i + 1 < len(lines):
                unit_name = lines[i + 1].strip()
            unit_positions.append((i, f'第{m.group(1)}单元', unit_name))
            continue
        
        # Unit with name on same line
        m = re.match(r'第([一二三四五六七八九十]+)单元\s+(.+)', line)
        if m:
            unit_positions.append((i, f'第{m.group(1)}单元', m.group(2).strip()))
            continue
        
        # Lesson
        m = re.match(r'第([一二三四五六七八九十\d]+)课\s+(.+)', line)
        if m:
            lesson_name = m.group(2).strip()
            # Remove trailing dots and page numbers
            lesson_name = re.sub(r'\s*[·．.…]+\s*\d+$', '', lesson_name)
            lessons.append((i, f'第{m.group(1)}课', lesson_name))
            continue
    
    # Assign lessons to units based on position
    if not unit_positions:
        # No units found - just return lessons as flat list
        for _, label, name in lessons:
            entries.append({'lesson': label, 'lesson_name': name})
        return entries
    
    # Create unit entries with their lessons
    for idx, (pos, unit_label, unit_name) in enumerate(unit_positions):
        next_pos = unit_positions[idx + 1][0] if idx + 1 < len(unit_positions) else float('inf')
        unit_lessons = [l for l in lessons if pos < l[0] < next_pos]
        unit_entry = {'unit': unit_label, 'unit_name': unit_name, 'lessons': []}
        for _, lesson_label, lesson_name in unit_lessons:
            unit_entry['lessons'].append({'lesson': lesson_label, 'lesson_name': lesson_name})
        if unit_entry['lessons']:
            entries.append(unit_entry)
    
    # Also add lessons that come before the first unit
    first_unit_pos = unit_positions[0][0] if unit_positions else float('inf')
    pre_lessons = [l for l in lessons if l[0] < first_unit_pos]
    if pre_lessons and entries:
        for _, lesson_label, lesson_name in pre_lessons:
            entries[0]['lessons'].insert(0, {'lesson': lesson_label, 'lesson_name': lesson_name})
    
    return entries


def parse_geo(text):
    entries = []
    current_chapter = None

    for line in text.split('\n'):
        line = line.strip()
        if not line or len(line) < 3:
            continue
        if any(kw in line for kw in ['栏目介绍', '致同学', '前言']):
            continue

        m = re.match(r'第([一二三四五六七八九十\d]+)章\s+(.+)', line)
        if m:
            current_chapter = {'chapter': f'第{m.group(1)}章', 'chapter_name': m.group(2).strip(), 'sections': []}
            entries.append(current_chapter)
            continue

        m = re.match(r'第([一二三四五六七八九十\d]+)节\s+(.+)', line)
        if m:
            sec_label = f'第{m.group(1)}节'
            sec_name = m.group(2).strip()
            if current_chapter:
                current_chapter['sections'].append({'section': sec_label, 'section_name': sec_name})
            continue

    return entries


def parse_pol(text):
    entries = []
    current_unit = None
    current_lesson = None

    for line in text.split('\n'):
        line = line.strip()
        if not line or len(line) < 3:
            continue
        if any(kw in line for kw in ['栏目介绍', '致同学', '前言']):
            continue

        m = re.match(r'第([一二三四五六七八九十]+)单元\s+(.+)', line)
        if m:
            current_unit = {'unit': f'第{m.group(1)}单元', 'unit_name': m.group(2).strip(), 'lessons': []}
            entries.append(current_unit)
            current_lesson = None
            continue

        m = re.match(r'第([一二三四五六七八九十\d]+)课\s+(.+)', line)
        if m:
            current_lesson = {'lesson': f'第{m.group(1)}课', 'lesson_name': m.group(2).strip(), 'frames': []}
            if current_unit:
                current_unit['lessons'].append(current_lesson)
            continue

        m = re.match(r'(第[一二三四五六七八九十\d]+框)\s*(.+)', line)
        if m:
            frame_label = m.group(1)
            frame_name = m.group(2).strip() if m.group(2) else ''
            if current_lesson:
                current_lesson['frames'].append({'frame': frame_label, 'frame_name': frame_name})
            continue

    return entries


def parse_cn(text):
    entries = []
    current_unit = None

    for line in text.split('\n'):
        line = line.strip()
        if not line or len(line) < 3:
            continue

        m = re.match(r'第([一二三四五六七八九十]+)单元\s*(.*)', line)
        if m and ('阅读' in line or '活动' in line or len(line) < 15):
            unit_name = m.group(2).strip() if m.group(2) else ''
            current_unit = {'unit': f'第{m.group(1)}单元', 'unit_name': unit_name, 'items': []}
            entries.append(current_unit)
            continue

        m = re.match(r'(\d+)\s+(.+)', line)
        if m and current_unit:
            item_name = m.group(2).strip()
            if any(kw in item_name for kw in ['阅读', '写作', '综合性学习', '名著导读', '课外古诗词', '口语交际']):
                parts = item_name.split(None, 1)
                current_unit['items'].append({'type': parts[0] if parts else '', 'name': item_name})
            elif len(item_name) > 3:
                current_unit['items'].append({'type': '课文', 'name': item_name})
            continue

        for tag in ['阅读', '写作', '综合性学习', '名著导读', '课外古诗词诵读', '口语交际']:
            if tag in line:
                if current_unit:
                    current_unit['items'].append({'type': tag, 'name': line.strip()})
                break

    return entries


def parse_eng(text):
    """英语目录：Unit 1 xxx，有时目录在靠后页面"""
    entries = []
    for line in text.split('\n'):
        line = line.strip()
        if not line or len(line) < 3:
            continue
        m = re.match(r'Unit\s+(\d+)\s+(.+)', line, re.IGNORECASE)
        if m:
            entries.append({'unit': f'Unit {m.group(1)}', 'unit_name': m.group(2).strip()})
            continue
    return entries


def extract_eng_toc_smart(fpath):
    """英语教材：从Contents页提取Unit编号，从正文页获取完整标题"""
    doc = fitz.open(fpath)
    units = {}
    
    # Pass 1: find Contents page (pages 3-8 typically) and extract Unit numbers
    for i in range(min(10, len(doc))):
        text = doc[i].get_text()
        if 'CONTENTS' in text or 'Contents' in text:
            lines = text.split('\n')
            for line in lines:
                line = line.strip()
                m = re.match(r'Unit\s+(\d+)\s+(.+)', line)
                if m:
                    units[m.group(1)] = m.group(2).strip()
                m = re.match(r'Unit\s+(\d+)\s*$', line)
                if m and m.group(1) not in units:
                    units[m.group(1)] = ''
    
    # Pass 2: if no titles found, scan body pages for Unit headings
    if not units or all(v == '' for v in units.values()):
        for i in range(min(80, len(doc))):
            text = doc[i].get_text()
            m = re.findall(r'Unit\s+(\d+)\s*\n+(.+)', text)
            for unit_num, unit_name in m:
                unit_name = unit_name.strip()
                if unit_num not in units or len(unit_name) > len(units.get(unit_num, '')):
                    units[unit_num] = unit_name
    
    doc.close()
    
    toc_lines = []
    for num in sorted(units.keys(), key=int):
        name = units[num]
        toc_lines.append(f'Unit {num} {name}')
    
    return '\n'.join(toc_lines)


parsers = {
    'bio': parse_bio_chem,
    'chem': parse_bio_chem,
    'phy': parse_phy,
    'math': parse_math,
    'hist': parse_hist,
    'geo': parse_geo,
    'pol': parse_pol,
    'cn': parse_cn,
    'eng': parse_eng,
}

curriculum = {}

# Also need to import fitz for eng extraction
import fitz

for key, data in sorted(all_tocs.items()):
    subj = data['subject_en']
    text = data['toc_text']

    # For English, use smart extractor
    if subj == 'eng' and len(text) < 100:
        fpath = os.path.join(
            r'C:\Users\27170\WPSDrive\383859682\WPS云盘\Thought\AI教育\2026.05_AI教育课程设计\lxs\初中生课程培训\资源',
            data['subject_cn'], data['file']
        )
        if os.path.exists(fpath):
            text = extract_eng_toc_smart(fpath)
            print(f'  -> eng smart extract: {len(text)} chars')

    if subj in parsers:
        entries = parsers[subj](text)
    else:
        entries = []

    curriculum[key] = {
        'subject_cn': data['subject_cn'],
        'subject_en': subj,
        'grade': data['grade'],
        'semester': data['semester'],
        'file': data['file'],
        'entries': entries,
        'entry_count': len(entries)
    }

    sec_count = 0
    for e in entries:
        if 'sections' in e:
            sec_count += len(e['sections'])
        if 'chapters' in e:
            for ch in e['chapters']:
                if 'sections' in ch:
                    sec_count += len(ch['sections'])
        if 'lessons' in e:
            sec_count += len(e.get('lessons', []))
        if 'items' in e:
            sec_count += len(e.get('items', []))

    print(f'{key}: {len(entries)} entries, ~{sec_count} sections')

out_path = r'E:\Applications in E\workBuddy\2026~AI课程\bio-chem-ai\curriculum_structured.json'
with open(out_path, 'w', encoding='utf-8') as f:
    json.dump(curriculum, f, ensure_ascii=False, indent=2)
print(f'\nSaved to {out_path}')
