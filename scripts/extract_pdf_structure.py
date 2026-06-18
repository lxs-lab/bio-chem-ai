"""Extract chapter/section structure from textbook PDFs."""
import fitz, os, re, json

PDFS = [
    ('bio', 'pdf/生物学7年级上册.pdf'),
    ('chem', 'pdf/化学9年级上册.pdf'),
    ('geo', 'pdf/地理7年级上册.pdf'),
    ('math', 'pdf/数学7年级上册.pdf'),
    ('phy', 'pdf/物理8年级上册.pdf'),
]

for label, path in PDFS:
    if not os.path.exists(path):
        print(f"=== {label}: FILE NOT FOUND ===")
        continue
    doc = fitz.open(path)
    print(f"\n{'='*60}")
    print(f"  {label}: {path} ({len(doc)} pages)")
    print(f"{'='*60}")
    
    # Extract text from first 30 pages to find TOC
    all_text = ""
    for i in range(min(30, len(doc))):
        page = doc[i]
        text = page.get_text("text")
        all_text += text
    
    # Find lines that look like chapter/section titles
    lines = all_text.split('\n')
    chapter_patterns = [
        r'第[一二三四五六七八九十]+单元',
        r'第[一二三四五六七八九十]+章',
        r'第[一二三四五六七八九十]+节',
        r'课题\d+',
        r'绪论',
    ]
    
    found = []
    for line in lines:
        line = line.strip()
        if not line or len(line) < 3 or len(line) > 50:
            continue
        for pat in chapter_patterns:
            if re.search(pat, line):
                if line not in found:
                    found.append(line)
    
    if found:
        for f in found:
            print(f"  >> {f}")
    else:
        # Fallback: print first 100 meaningful lines
        for line in lines[:80]:
            line = line.strip()
            if line and len(line) > 3:
                print(f"    {line[:80]}")
    
    doc.close()
