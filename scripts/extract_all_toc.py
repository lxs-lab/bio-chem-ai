"""
Extract comprehensive TOC from all 9 subject textbooks.
Parses PDF text to find unit/chapter/section headings.
Outputs toc_all.json with full structure for data file generation.
"""
import fitz, json, os, re, sys

BASE = r'C:\Users\27170\WPSDrive\383859682\WPS云盘\Thought\AI教育\2026.05_AI教育课程设计\lxs\初中生课程培训\资源'

# Map subjects to PDF paths
SUBJECT_PDFS = {
    '生物': BASE + '/生物学/（根据2022年版课程标准修订）义务教育教科书·生物学七年级上册.pdf',
    '化学': BASE + '/化学/（根据2022年版课程标准修订）义务教育教科书·化学九年级上册.pdf',
    '地理': BASE + '/地理/（根据2022年版课程标准修订）义务教育教科书·地理七年级上册.pdf',
    '物理': BASE + '/物理/（根据2022年版课程标准修订）义务教育教科书·物理八年级上册.pdf',
    '数学': BASE + '/数学/（根据2022年版课程标准修订）义务教育教科书·数学七年级上册.pdf',
    '语文': BASE + '/语文/（根据2022年版课程标准修订）义务教育教科书·语文七年级上册.pdf',
    '英语': BASE + '/英语/（根据2022年版课程标准修订）义务教育教科书 英语 七年级 上册.pdf',
    '历史': BASE + '/历史/（根据2022年版课程标准修订）义务教育教科书·中国历史七年级上册.pdf',
    '道法': BASE + '/道德与法治/（根据2022年版课程标准修订）义务教育教科书·道德与法治七年级上册.pdf',
}

# Chinese number mapping for page scanning
CN_NUMS = '一二三四五六七八九十'

def is_heading(text, font_size, is_bold=False):
    """Determine if text is a heading based on font size and content"""
    text = text.strip()
    if not text or len(text) < 2:
        return False
    # Unit patterns
    if re.match(r'第[' + CN_NUMS + r']+单元', text):
        return 'unit'
    # Chapter/课 patterns
    if re.match(r'第[' + CN_NUMS + r']+[课章]', text):
        return 'chapter'
    # Common section patterns
    if re.match(r'第[' + CN_NUMS + r']+[节框框题框]', text):
        return 'section'
    # Large font size text in table of contents pages
    if font_size >= 15:
        return 'maybe_heading'
    return False

def extract_toc_from_text(pdf_path):
    """Extract table of contents by scanning PDF text"""
    doc = fitz.open(pdf_path)
    total_pages = doc.page_count
    
    units = []
    current_unit = None
    current_chapter = None
    
    # Strategy: look for TOC pages (typically first few pages) and scan headings
    all_blocks = []
    for page_num in range(min(20, total_pages)):  # Scan first 20 pages for TOC
        page = doc[page_num]
        blocks = page.get_text('dict')['blocks']
        for b in blocks:
            if 'lines' in b:
                for l in b['lines']:
                    for s in l['spans']:
                        size = round(s['size'], 1)
                        text = s['text'].strip()
                        if not text:
                            continue
                        # Record blocks worth examining
                        all_blocks.append({
                            'page': page_num + 1,
                            'size': size,
                            'bold': 'Bold' in s.get('font', ''),
                            'text': text,
                            'bbox_y': round(s['bbox'][1], 0)
                        })
    
    # Find TOC by looking for "目录" heading
    toc_start = 0
    for i, b in enumerate(all_blocks):
        if b['text'] in ['目录', '目  录'] and b['size'] >= 14:
            toc_start = b['page']
            break
    
    # Also look at the first large-font text on each page for unit/chapter detection
    # This is fallback when TOC extraction fails
    
    # Scan entire document for heading patterns
    all_headings = []
    for page_num in range(total_pages):
        page = doc[page_num]
        blocks = page.get_text('dict')['blocks']
        page_headings = []
        for b in blocks:
            if 'lines' in b:
                for l in b['lines']:
                    for s in l['spans']:
                        size = round(s['size'], 1)
                        text = s['text'].strip()
                        if not text or len(text) < 3:
                            continue
                        heading_type = is_heading(text, size)
                        if heading_type:
                            page_headings.append({
                                'type': heading_type,
                                'text': text,
                                'size': size,
                                'bold': 'Bold' in s.get('font', ''),
                                'page': page_num + 1,
                            })
        if page_headings:
            all_headings.extend(page_headings)
    
    doc.close()
    
    # Build structure from headings
    structure = []
    for h in all_headings:
        if h['type'] == 'unit':
            unit_info = {
                'title': h['text'],
                'page': h['page'],
                'chapters': []
            }
            # If duplicate unit found (e.g. heading repeats), skip
            if not structure or structure[-1]['title'] != h['text']:
                structure.append(unit_info)
        elif h['type'] == 'chapter' and structure:
            ch_info = {
                'title': h['text'],
                'page': h['page'],
                'sections': []
            }
            structure[-1]['chapters'].append(ch_info)
        elif h['type'] == 'section' and structure and structure[-1]['chapters']:
            structure[-1]['chapters'][-1]['sections'].append({
                'title': h['text'],
                'page': h['page']
            })
    
    return {
        'total_pages': total_pages,
        'toc_scan_start': toc_start,
        'structure': structure,
        'all_headings': all_headings
    }

def extract_toc_from_builtin(pdf_path):
    """Try built-in TOC first"""
    doc = fitz.open(pdf_path)
    toc = doc.get_toc()
    doc.close()
    if not toc:
        return None
    
    structure = []
    prev_unit = None
    
    for entry in toc:
        level, title, page = entry[0], entry[1], entry[2]
        
        if level == 1:
            unit_info = {'title': title, 'page': page, 'chapters': []}
            structure.append(unit_info)
            prev_unit = unit_info
        elif level == 2 and structure:
            ch_info = {'title': title, 'page': page, 'sections': []}
            structure[-1]['chapters'].append(ch_info)
        elif level == 3 and structure and structure[-1]['chapters']:
            sec_info = {'title': title, 'page': page}
            structure[-1]['chapters'][-1]['sections'].append(sec_info)
    
    return structure

# Main extraction
all_toc = {}
for subject, path in SUBJECT_PDFS.items():
    if not os.path.exists(path):
        print(f'SKIP {subject}: file not found')
        all_toc[subject] = {'error': 'file not found'}
        continue
    
    print(f'\n=== {subject} ===')
    print(f'  File: {os.path.basename(path)}')
    
    # Try built-in TOC first
    result = extract_toc_from_text(path)
    
    if result['structure']:
        print(f'  Method: text scanning')
    else:
        print(f'  No structure found')
    
    print(f'  Total pages: {result["total_pages"]}')
    print(f'  Units found: {len(result["structure"])}')
    
    for unit in result['structure']:
        print(f'    {unit["title"]} (p.{unit["page"]})')
        for ch in unit['chapters']:
            print(f'      {ch["title"]} (p.{ch["page"]})')
            for sec in ch['sections']:
                print(f'        {sec["title"]} (p.{sec["page"]})')
    
    all_toc[subject] = result

# Save result
output_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'data', 'toc_all.json')
with open(output_path, 'w', encoding='utf-8') as f:
    json.dump(all_toc, f, ensure_ascii=False, indent=2)
print(f'\nSaved to {output_path}')
