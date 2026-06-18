"""
精准提取所有9科教材的完整目录结构
输出：每个科目的 单元→课→节 层级结构 + 每节的页码
"""
import fitz, json, os, re

BASE = r'C:\Users\27170\WPSDrive\383859682\WPS云盘\Thought\AI教育\2026.05_AI教育课程设计\lxs\初中生课程培训\资源'

# All subjects with exact PDF paths
# Pattern: (subject_key, grade, pdf_path, pdf_filename_for_web)
SUBJECTS = [
    ('bio', 7, BASE + '/生物学/（根据2022年版课程标准修订）义务教育教科书·生物学七年级上册.pdf', '生物学七年级上册.pdf'),
    ('chem', 9, BASE + '/化学/（根据2022年版课程标准修订）义务教育教科书·化学九年级上册.pdf', '化学九年级上册.pdf'),
    ('geo', 7, BASE + '/地理/（根据2022年版课程标准修订）义务教育教科书·地理七年级上册.pdf', '地理七年级上册.pdf'),
    ('phy', 8, BASE + '/物理/（根据2022年版课程标准修订）义务教育教科书·物理八年级上册.pdf', '物理八年级上册.pdf'),
    ('math', 7, BASE + '/数学/（根据2022年版课程标准修订）义务教育教科书·数学七年级上册.pdf', '数学七年级上册.pdf'),
    ('cn', 7, BASE + '/语文/（根据2022年版课程标准修订）义务教育教科书·语文七年级上册.pdf', '语文七年级上册.pdf'),
    ('eng', 7, BASE + '/英语/（根据2022年版课程标准修订）义务教育教科书 英语 七年级 上册.pdf', '英语七年级上册.pdf'),
    ('hist', 7, BASE + '/历史/（根据2022年版课程标准修订）义务教育教科书·中国历史七年级上册.pdf', '中国历史七年级上册.pdf'),
    ('pol', 7, BASE + '/道德与法治/（根据2022年版课程标准修订）义务教育教科书·道德与法治七年级上册.pdf', '道德与法治七年级上册.pdf'),
]

CN = '一二三四五六七八九十'

def extract_clean_toc(pdf_path, subject_key):
    """Extract unit→chapter→section structure from PDF TOC pages"""
    doc = fitz.open(pdf_path)
    total_pages = doc.page_count
    
    # Extract all text spans from first 10 pages (TOC area)
    all_spans = []
    for pg in range(min(10, total_pages)):
        page = doc[pg]
        blocks = page.get_text('dict')['blocks']
        for b in blocks:
            if 'lines' not in b:
                continue
            for l in b['lines']:
                line_spans = []
                for s in l['spans']:
                    line_spans.append({
                        'text': s['text'].strip(),
                        'size': round(s['size'], 1),
                        'pg': pg + 1
                    })
                if line_spans:
                    all_spans.extend(line_spans)
    
    doc.close()
    
    # Build structured TOC
    units = []
    current_unit = None
    current_chapter = None
    in_toc = False
    page_num_buffer = None
    
    for span in all_spans:
        text = span['text']
        size = span['size']
        
        if not text:
            continue
            
        # Check if we're in TOC section
        if text in ['目录', '目  录', '目 录'] and size >= 16:
            in_toc = True
            continue
        
        if not in_toc:
            continue
        
        # Unit detection: "第一单元" + title
        unit_match = re.match(r'第([' + CN + r']+)单元$', text)
        if unit_match and size >= 13:
            # Next span should be the unit title
            continue
        
        # Check if this is a unit title (follows "第X单元")
        if current_unit is None and len(units) < 4:
            # Look for unit-like text
            if re.match(r'第([' + CN + r']+)单元', text) and size >= 13:
                # This might be "第X单元" + title together
                full = text
                title_part = re.sub(r'第[' + CN + r']+单元\s*', '', full)
                current_unit = {
                    'unit_title': full if title_part else text,
                    'page': None,
                    'chapters': []
                }
        
        # Chapter detection
        ch_match = re.match(r'第([' + CN + r']+)课\s*(.*)', text)
        if ch_match and size >= 11:
            ch_title = ch_match.group(0).strip()
            ch_num = ch_match.group(1)
            if current_unit:
                current_chapter = {
                    'chapter_title': ch_title,
                    'page': None,
                    'sections': []
                }
                current_unit['chapters'].append(current_chapter)
            continue
        
        # Section detection: plain text title at ~10-12pt, no "第X课" prefix
        # Sections are usually the text that follows a chapter and is at ~11pt with a number after
        page_num_match = re.match(r'^(\d+)$', text)
        if page_num_match and size >= 10:
            page_num_buffer = int(page_num_match.group(1))
            continue
        
        # If we have a page number buffer and the next text looks like a section title
        if page_num_buffer is not None and len(text) >= 2 and size >= 10 and size <= 12:
            if current_chapter and not re.match(r'第[' + CN + r']+[课单元章]', text) and not re.match(r'^\d+$', text) and text not in ['单元思考与行动', '复习与提高']:
                current_chapter['sections'].append({
                    'section_title': text,
                    'page': page_num_buffer
                })
                page_num_buffer = None
                continue
    
    return units

# Instead of trying to parse from spans, let's use a different approach:
# Extract text block by block from TOC pages

def extract_toc_blocks(pdf_path):
    """Extract TOC from the PDF by reading blocks line-by-line"""
    doc = fitz.open(pdf_path)
    total_pages = doc.page_count
    
    toc_lines = []
    in_toc = False
    
    for pg in range(min(10, total_pages)):
        page = doc[pg]
        blocks = page.get_text('dict')['blocks']
        for b in blocks:
            if 'lines' not in b:
                continue
            for l in b['lines']:
                # Combine all spans in this line
                texts = [s['text'].strip() for s in l['spans'] if s['text'].strip()]
                sizes = [round(s['size'], 1) for s in l['spans'] if s['text'].strip()]
                if not texts:
                    continue
                full_line = ''.join(texts)
                avg_size = sum(sizes) / len(sizes) if sizes else 0
                toc_lines.append({
                    'text': full_line,
                    'size': avg_size,
                    'max_size': max(sizes) if sizes else 0,
                    'page_toc': pg + 1
                })
    
    doc.close()
    return toc_lines, total_pages

def parse_toc_to_structure(toc_lines, total_pages):
    """Parse TOC lines into structured format"""
    structure = []
    current_unit = None
    current_chapter = None
    current_section = None
    
    # First pass: find units
    for i, line in enumerate(toc_lines):
        text = line['text']
        m = re.match(r'第([' + CN + r']+)单元\s*(.+)', text)
        if m and line['max_size'] >= 13:
            title = m.group(0)
            # Try to find page number (next lines or inline)
            page_num = None
            # Look at next few lines for page number
            for j in range(i+1, min(i+4, len(toc_lines))):
                pn_match = re.match(r'^(\d{1,3})$', toc_lines[j]['text'])
                if pn_match:
                    page_num = int(pn_match.group(1))
                    break
            unit = {
                'unit_title': title,
                'page': page_num,
                'chapters': []
            }
            structure.append(unit)
            current_unit = unit
            current_chapter = None
    
    # Second pass: find chapters
    for i, line in enumerate(toc_lines):
        text = line['text']
        m = re.match(r'第([' + CN + r']+)课\s*(.+)', text)
        if m and line['max_size'] >= 11:
            if not structure:
                continue
            # Find which unit this belongs to
            # Find nearest previous unit
            chapter_title = m.group(0)
            page_num = None
            for j in range(i+1, min(i+3, len(toc_lines))):
                pn_match = re.match(r'^(\d{1,3})$', toc_lines[j]['text'])
                if pn_match:
                    page_num = int(pn_match.group(1))
                    break
            ch = {
                'chapter_title': chapter_title,
                'page': page_num,
                'sections': []
            }
            structure[-1]['chapters'].append(ch)
            current_chapter = ch
    
    # Third pass: find sections (text lines with page numbers around 11pt)
    for i, line in enumerate(toc_lines):
        text = line['text']
        # Skip if it's a unit/chapter heading
        if re.match(r'第[' + CN + r']+[单元课章]', text):
            continue
        if text in ['单元思考与行动', '复习与提高', '目录', '目  录']:
            continue
        
        # Check if next line is a page number
        if i + 1 < len(toc_lines):
            pn_match = re.match(r'^(\d{1,3})$', toc_lines[i+1]['text'])
            if pn_match and line['max_size'] >= 10 and len(text) >= 2:
                # This looks like a section title with page number
                if current_chapter and structure:
                    current_chapter['sections'].append({
                        'section_title': text,
                        'page': int(pn_match.group(1))
                    })
    
    return {
        'total_pages': total_pages,
        'structure': structure
    }

# Main
all_results = {}

for key, grade, pdf_path, web_name in SUBJECTS:
    print(f'\n=== {key} (grade {grade}) ===')
    
    if not os.path.exists(pdf_path):
        print(f'  FILE NOT FOUND: {pdf_path}')
        all_results[key] = {'error': 'file not found', 'grade': grade}
        continue
    
    # Check alt path for English
    if key == 'eng' and not os.path.exists(pdf_path):
        alt = BASE + '/英语/（根据2022年版课程标准修订）义务教育教科书·英语七年级上册.pdf'
        if os.path.exists(alt):
            pdf_path = alt
            print(f'  Using alt path')
    
    toc_lines, total_pages = extract_toc_blocks(pdf_path)
    result = parse_toc_to_structure(toc_lines, total_pages)
    
    print(f'  Total pages: {result["total_pages"]}')
    print(f'  Units: {len(result["structure"])}')
    
    total_sections = 0
    for unit in result['structure']:
        print(f'    {unit["unit_title"]} (p.{unit["page"]})')
        for ch in unit['chapters']:
            print(f'      {ch["chapter_title"]} (p.{ch["page"]})')
            for sec in ch['sections']:
                print(f'        {sec["section_title"]} (p.{sec["page"]})')
                total_sections += 1
    
    print(f'  Total sections: {total_sections}')
    all_results[key] = result
    all_results[key]['grade'] = grade
    all_results[key]['pdf_web_name'] = web_name

# Save
output_path = r'E:\Applications in E\workBuddy\2026~AI课程\bio-chem-ai\data\toc_extracted.json'
with open(output_path, 'w', encoding='utf-8') as f:
    json.dump(all_results, f, ensure_ascii=False, indent=2)
print(f'\n=== Saved to {output_path} ===')
