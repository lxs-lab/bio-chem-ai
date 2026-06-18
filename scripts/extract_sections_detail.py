"""Extract detailed section structure from all textbooks."""
import fitz, os, re

PDFS = {
    'bio': 'pdf/生物学7年级上册.pdf',
    'chem': 'pdf/化学9年级上册.pdf',
    'geo': 'pdf/地理7年级上册.pdf',
    'math': 'pdf/数学7年级上册.pdf',
    'phy': 'pdf/物理8年级上册.pdf',
    'hist': 'pdf/历史7年级上册.pdf',
    'pol': 'pdf/道德与法治7年级上册.pdf',
    'cn': 'pdf/语文7年级上册.pdf',
}

def extract_sections(path, label):
    """Extract all section titles with their page numbers."""
    doc = fitz.open(path)
    sections = []
    
    # Scan all pages for section patterns
    section_patterns = [
        (r'第([一二三四五六七八九十]+)节[\s\u3000]*([^\d].*?)(?:\d+)?$', 3),
        (r'课题(\d+)[\s\u3000]+(.+?)$', 3),
        (r'第([一二三四五六七八九十]+)章[\s\u3000]*(.+?)(?:\d+)?$', 2),
        (r'第([一二三四五六七八九十]+)单元[\s\u3000]*(.+?)(?:\d+)?$', 1),
        (r'绪论[\s\u3000]+(.+?)(?:\d+)?$', 0),
    ]
    
    current_unit = ""
    current_chapter = ""
    
    for page_num in range(len(doc)):
        text = doc[page_num].get_text("text")
        lines = text.split('\n')
        
        for line in lines:
            line = line.strip()
            if len(line) < 4 or len(line) > 80:
                continue
            
            # Check for unit
            m = re.search(r'第([一二三四五六七八九十]+)单元[\s\u3000]+(.+)', line)
            if m and len(line) < 25:
                current_unit = f"第{m.group(1)}单元 {m.group(2).strip()}"
                continue
            
            # Check for chapter
            m = re.search(r'第([一二三四五六七八九十]+)章[\s\u3000]+(.+)', line)
            if m and len(line) < 30:
                current_chapter = f"第{m.group(1)}章 {m.group(2).strip()}"
                continue
            
            # Check for section
            m = re.search(r'第([一二三四五六七八九十]+)节[\s\u3000]+(.+)', line)
            if m and len(line) < 40:
                section = {
                    'unit': current_unit,
                    'chapter': current_chapter,
                    'section': f"第{m.group(1)}节 {m.group(2).strip()}",
                    'page': page_num + 1
                }
                if section not in sections:
                    sections.append(section)
            
            # Check for 课题 (chemistry)
            m = re.search(r'课题(\d+)[\s\u3000]+(.+)', line)
            if m and len(line) < 40:
                section = {
                    'unit': current_unit,
                    'chapter': f"课题{m.group(1)}",
                    'section': f"课题{m.group(1)} {m.group(2).strip()}",
                    'page': page_num + 1
                }
                if section not in sections:
                    sections.append(section)
    
    doc.close()
    return sections

for label, path in PDFS.items():
    if not os.path.exists(path):
        print(f"\n=== {label}: FILE NOT FOUND ===")
        continue
    print(f"\n{'='*70}")
    print(f"  {label}: {os.path.basename(path)}")
    print(f"{'='*70}")
    
    sections = extract_sections(path, label)
    
    prev_unit = ""
    for s in sections:
        if s['unit'] and s['unit'] != prev_unit:
            print(f"\n  📘 {s['unit']}")
            prev_unit = s['unit']
        if s['chapter']:
            print(f"    📖 {s['chapter']}")
        print(f"      📄 {s['section']}  (p{s['page']})")
    
    print(f"\n  Total sections found: {len(sections)}")
