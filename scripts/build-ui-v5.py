"""Build the v5 index.html with redesigned UI, resource library, and full-subject support."""
import re, json, os

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HTML_PATH = os.path.join(BASE, 'index.html')
LIBRARY_PATH = os.path.join(BASE, 'data', 'resource_library.json')
OUT_PATH = os.path.join(BASE, 'index_v5.html')

# Read existing index.html
with open(HTML_PATH, 'r', encoding='utf-8') as f:
    html = f.read()

# Extract the <script> block (everything from <script> to </script>)
script_match = re.search(r'<script>\s*(// ============ DATA ============.*?)</script>', html, re.DOTALL)
script_content = script_match.group(1) if script_match else ''

# Read library data
with open(LIBRARY_PATH, 'r', encoding='utf-8') as f:
    library = json.load(f)

# Generate library HTML sections
def gen_standards_html():
    """Generate standards cards for homepage"""
    cards = []
    for s in library['standards']:
        name = s['name'].replace('.20220428161149','').replace('.20240918113747','').replace('.20220428160444','').replace('.20220428160350','').replace('.20220428160315','').replace('.20220428161129','').replace('.20220428161048','').replace('.20220428161016','').replace('.20220428160938','').replace('.20220428160837','').replace('.20220428160631','')
        if len(name) > 30:
            name = name[:30] + '...'
        cards.append(f'''        <div class="std-card">
          <div class="std-icon">📋</div>
          <div class="std-title">{name}</div>
          <div class="std-desc">2022年版 · 教育部制定</div>
          <a href="pdf/{s['file']}" target="_blank" class="btn-sm btn-outline">📖 在线预览</a>
        </div>''')
    return '\n'.join(cards)

def gen_textbook_html():
    """Generate textbook cards for resource library view"""
    sections = []
    for subj_id, subj in library['subjects'].items():
        items = []
        for tb in subj['textbooks']:
            items.append(f'''            <div class="tb-item">
              <span class="tb-grade">{tb['grade']}年级{tb['term']}</span>
              <span class="tb-name">{tb['name']}</span>
              <a href="pdf/{tb['file']}" target="_blank" class="btn-sm btn-outline" style="font-size:.7rem;padding:4px 10px">📖 预览</a>
            </div>''')
        sections.append(f'''      <div class="lib-subject-section">
        <h3 class="lib-subj-title"><span class="lib-subj-icon">{SUBJ_ICONS.get(subj_id,'📚')}</span> {subj['name']} <span class="lib-count">{len(subj['textbooks'])}册</span></h3>
        <div class="tb-list">
{chr(10).join(items)}
        </div>
      </div>''')
    return '\n'.join(sections)

SUBJ_ICONS = {
    'bio': '🧬', 'chem': '⚗️', 'geo': '🗺️', 'phy': '⚡', 'math': '📐',
    'cn': '📖', 'eng': '🔤', 'hist': '🏛️', 'pol': '⚖️'
}
SUBJ_NAMES = {
    'bio': '生物学', 'chem': '化学', 'geo': '地理', 'phy': '物理', 'math': '数学',
    'cn': '语文', 'eng': '英语', 'hist': '历史', 'pol': '道德与法治'
}
SUBJ_COLORS = {
    'bio': '#5b9a6b', 'chem': '#4a90b8', 'geo': '#8B6914', 'phy': '#e87d4b', 'math': '#4a90b8',
    'cn': '#8b6baa', 'eng': '#e87d4b', 'hist': '#8B6914', 'pol': '#2E8B85'
}
SUBJ_DESCS = {
    'bio': '探索生命奥秘，从细胞到生态系统', 'chem': '物质变化的魔法，从分子认识世界',
    'geo': '学会看地图，打开探索世界的钥匙', 'phy': '力学、热学、光学——万物之理',
    'math': '数与形的基础，逻辑思维训练场', 'cn': '阅读与写作，母语素养根基',
    'eng': 'Hello World! 打开国际交流之门', 'hist': '以史为鉴，理解中华与世界',
    'pol': '立德树人，做新时代好少年'
}
SUBJ_GRADES = {
    'bio': '7-8年级', 'chem': '9年级', 'geo': '7-8年级', 'phy': '8-9年级', 'math': '7-9年级',
    'cn': '7-9年级', 'eng': '7-9年级', 'hist': '7-9年级', 'pol': '7-9年级'
}

def gen_course_cards():
    cards = []
    for subj_id in ['bio','chem','geo','phy','math','cn','eng','hist','pol']:
        color = SUBJ_COLORS[subj_id]
        cards.append(f'''        <div class="cc-card" style="--cc-accent:{color}" onclick="navigateTo('syllabus','{subj_id}')">
          <div class="cc-icon-wrap" style="background:{color}15">
            <span class="cc-icon">{SUBJ_ICONS[subj_id]}</span>
          </div>
          <div class="cc-body">
            <div class="cc-name">{SUBJ_NAMES[subj_id]}</div>
            <div class="cc-grade">{SUBJ_GRADES[subj_id]}</div>
            <div class="cc-desc">{SUBJ_DESCS[subj_id]}</div>
          </div>
        </div>''')
    return '\n'.join(cards)

def gen_lp_tabs():
    tabs = []
    for subj_id in ['bio','chem','geo','phy','math','cn','eng','hist','pol']:
        tabs.append(f'          <button class="lp-tab" onclick="switchSubject(\'{subj_id}\')">{SUBJ_ICONS[subj_id]} {SUBJ_NAMES[subj_id]}</button>')
    return '\n'.join(tabs)

# Build the new HTML
new_html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>智慧学堂 - 初中全科 AI 教学</title>
<script src="https://cdn.jsdelivr.net/npm/phaser@3.60.0/dist/phaser.min.js"></script>
<style>
:root {{
  --bg: #f9f7f3;
  --bg2: #f3efe7;
  --card: #ffffff;
  --warm: #e87d4b;
  --warm2: #f4a261;
  --warm-light: #fef5ed;
  --warm-deep: #d4723f;
  --green: #5b9a6b;
  --green-light: #eaf5ec;
  --green-deep: #4a8659;
  --blue: #4a90b8;
  --blue-light: #e8f2f8;
  --brown: #8B6914;
  --brown-light: #f7f2e3;
  --teal: #2E8B85;
  --teal-light: #e6f5f4;
  --purple: #8b6baa;
  --purple-light: #f4f0f8;
  --text: #2d2a24;
  --text2: #6b6357;
  --text3: #a09888;
  --border: #e6ded0;
  --shadow-sm: 0 1px 3px rgba(0,0,0,.04);
  --shadow: 0 2px 12px rgba(0,0,0,.06);
  --shadow-lg: 0 8px 30px rgba(0,0,0,.1);
  --radius: 14px;
  --radius-sm: 10px;
  --radius-lg: 20px;
  --transition: .25s cubic-bezier(.4,0,.2,1);
}}
*{{margin:0;padding:0;box-sizing:border-box}}
body{{font-family:"PingFang SC","Microsoft YaHei","Noto Sans SC",-apple-system,sans-serif;background:var(--bg);color:var(--text);min-height:100vh;line-height:1.65;overflow-x:hidden}}
::-webkit-scrollbar{{width:5px}}::-webkit-scrollbar-track{{background:transparent}}::-webkit-scrollbar-thumb{{background:var(--border);border-radius:10px}}

/* ====== VIEW SYSTEM ====== */
.view{{display:none}}
.view.active{{display:block;animation:viewIn .35s ease}}
@keyframes viewIn{{from{{opacity:0;transform:translateY(10px)}}to{{opacity:1;transform:translateY(0)}}}}

/* ====== HOME PAGE ====== */
.home-page{{min-height:100vh;padding-bottom:40px}}
.home-hero{{background:linear-gradient(170deg,#fef8f0 0%,#fdf2e5 35%,#faf6ee 70%,#f9f4eb 100%);padding:50px 24px 44px;text-align:center;position:relative;overflow:hidden}}
.home-hero::before{{content:'';position:absolute;top:-80px;right:-80px;width:280px;height:280px;border-radius:50%;background:radial-gradient(circle,rgba(244,162,97,.1),transparent 65%)}}
.home-hero::after{{content:'';position:absolute;bottom:-60px;left:-60px;width:240px;height:240px;border-radius:50%;background:radial-gradient(circle,rgba(91,154,107,.08),transparent 65%)}}
.home-hero .logo-icon{{font-size:3rem;margin-bottom:10px;display:inline-block;animation:float 3s ease-in-out infinite}}
@keyframes float{{0%,100%{{transform:translateY(0)}}50%{{transform:translateY(-6px)}}}}
.home-hero h1{{font-size:2rem;font-weight:800;color:var(--text);margin-bottom:6px;letter-spacing:.5px}}
.home-hero h1 .hl{{color:var(--warm)}}
.home-hero .subtitle{{font-size:.95rem;color:var(--text2);max-width:520px;margin:0 auto 20px;line-height:1.6}}
.home-hero .hero-badge{{display:inline-flex;align-items:center;gap:6px;background:var(--warm-light);color:var(--warm);padding:6px 16px;border-radius:20px;font-size:.78rem;font-weight:600}}
.home-hero .hero-stats{{display:flex;justify-content:center;gap:32px;margin-top:18px}}
.home-hero .hero-stat{{text-align:center}}
.home-hero .hero-stat .num{{font-size:1.5rem;font-weight:700;color:var(--warm)}}
.home-hero .hero-stat .lbl{{font-size:.72rem;color:var(--text3);margin-top:2px}}

/* Course Cards Grid */
.course-grid-section{{max-width:1100px;margin:-28px auto 0;padding:0 20px;position:relative;z-index:2}}
.course-grid-section h2{{text-align:center;font-size:1.2rem;font-weight:700;margin-bottom:18px;color:var(--text)}}
.cc-grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(200px,1fr));gap:12px}}
.cc-card{{background:var(--card);border-radius:var(--radius-lg);padding:18px 16px;border:1px solid var(--border);box-shadow:var(--shadow-sm);cursor:pointer;transition:var(--transition);display:flex;align-items:flex-start;gap:12px;position:relative;overflow:hidden}}
.cc-card::before{{content:'';position:absolute;top:0;left:0;right:0;height:3px;background:var(--cc-accent,#e87d4b)}}
.cc-card:hover{{transform:translateY(-3px);box-shadow:var(--shadow-lg)}}
.cc-card .cc-icon-wrap{{width:42px;height:42px;border-radius:12px;display:flex;align-items:center;justify-content:center;flex-shrink:0}}
.cc-card .cc-icon{{font-size:1.4rem}}
.cc-card .cc-body{{flex:1;min-width:0}}
.cc-card .cc-name{{font-size:.9rem;font-weight:700;color:var(--text);margin-bottom:2px}}
.cc-card .cc-grade{{font-size:.7rem;color:var(--text3);margin-bottom:4px}}
.cc-card .cc-desc{{font-size:.74rem;color:var(--text2);line-height:1.5;display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;overflow:hidden}}

/* Features */
.features-section{{max-width:1100px;margin:40px auto;padding:0 20px}}
.features-section h2{{text-align:center;font-size:1.2rem;font-weight:700;margin-bottom:20px}}
.feature-grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:14px}}
.feature-item{{background:var(--card);border-radius:var(--radius);padding:20px;border:1px solid var(--border);text-align:center;transition:var(--transition)}}
.feature-item:hover{{box-shadow:var(--shadow);transform:translateY(-2px)}}
.feature-item .fi-icon{{font-size:2rem;margin-bottom:8px}}
.feature-item .fi-title{{font-weight:700;font-size:.9rem;margin-bottom:4px}}
.feature-item .fi-desc{{font-size:.76rem;color:var(--text2);line-height:1.5}}

/* Standards & Library Sections */
.std-section{{max-width:1100px;margin:32px auto;padding:0 20px}}
.std-section h2{{text-align:center;font-size:1.2rem;font-weight:700;margin-bottom:16px}}
.std-grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(240px,1fr));gap:10px}}
.std-card{{background:var(--card);border-radius:var(--radius);padding:16px;border:1px solid var(--border);text-align:center;transition:var(--transition)}}
.std-card:hover{{box-shadow:var(--shadow)}}
.std-card .std-icon{{font-size:1.6rem;margin-bottom:6px}}
.std-card .std-title{{font-weight:600;font-size:.82rem;margin-bottom:4px;line-height:1.3}}
.std-card .std-desc{{font-size:.72rem;color:var(--text3);margin-bottom:10px}}

.lib-section{{max-width:1100px;margin:32px auto 48px;padding:0 20px}}
.lib-section h2{{text-align:center;font-size:1.2rem;font-weight:700;margin-bottom:20px}}
.lib-grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(460px,1fr));gap:16px}}
.lib-subject-section{{background:var(--card);border-radius:var(--radius-lg);padding:16px 18px;border:1px solid var(--border)}}
.lib-subj-title{{font-size:.95rem;font-weight:700;margin-bottom:12px;display:flex;align-items:center;gap:8px}}
.lib-subj-icon{{font-size:1.2rem}}
.lib-count{{font-size:.7rem;color:var(--text3);font-weight:400;margin-left:auto}}
.tb-list{{display:flex;flex-direction:column;gap:6px}}
.tb-item{{display:flex;align-items:center;gap:10px;padding:8px 10px;background:var(--bg2);border-radius:8px;font-size:.8rem;transition:var(--transition)}}
.tb-item:hover{{background:var(--warm-light)}}
.tb-grade{{background:var(--warm-light);color:var(--warm);padding:2px 8px;border-radius:6px;font-size:.68rem;font-weight:600;white-space:nowrap;flex-shrink:0}}
.tb-name{{color:var(--text);flex:1;min-width:0;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}}

/* Buttons */
.btn-sm{{padding:6px 14px;border-radius:18px;border:none;cursor:pointer;font-size:.76rem;font-weight:500;transition:var(--transition);display:inline-block;text-decoration:none;text-align:center}}
.btn-warm{{background:var(--warm);color:#fff}}
.btn-warm:hover{{background:var(--warm-deep);transform:scale(1.03)}}
.btn-outline{{background:transparent;color:var(--warm);border:1.5px solid var(--warm2)}}
.btn-outline:hover{{background:var(--warm-light)}}
.btn-green{{background:var(--green);color:#fff}}
.btn-green:hover{{background:var(--green-deep)}}
.btn-lg{{padding:10px 28px;border-radius:22px;font-size:.88rem;font-weight:600}}
.btn-nav{{display:inline-flex;align-items:center;gap:4px;background:var(--card);border:1px solid var(--border);border-radius:20px;padding:6px 16px;cursor:pointer;font-size:.8rem;color:var(--text2);transition:var(--transition)}}
.btn-nav:hover{{background:var(--bg2);color:var(--text)}}

/* ====== SYLLABUS PAGE ====== */
.syllabus-page{{min-height:100vh}}
.sy-header{{background:var(--card);padding:12px 20px;position:sticky;top:0;z-index:100;border-bottom:1px solid var(--border);display:flex;align-items:center;gap:12px;backdrop-filter:blur(10px);background:rgba(255,255,255,.92)}}
.breadcrumb{{display:flex;align-items:center;gap:6px;font-size:.82rem}}
.breadcrumb a{{color:var(--warm);text-decoration:none;cursor:pointer;font-weight:500}}
.breadcrumb a:hover{{text-decoration:underline}}
.breadcrumb .sep{{color:var(--text3)}}
.breadcrumb .current{{color:var(--text2);font-weight:600}}
.sy-body{{max-width:1000px;margin:0 auto;padding:20px}}
.sy-hero{{text-align:center;padding:12px 0 24px}}
.sy-hero .sh-icon{{font-size:3rem;margin-bottom:6px}}
.sy-hero h2{{font-size:1.4rem;font-weight:700;margin-bottom:4px}}
.sy-hero p{{color:var(--text2);font-size:.85rem}}
.sy-stats{{display:flex;justify-content:center;gap:24px;margin-bottom:24px}}
.sy-stat{{text-align:center}}
.sy-stat .num{{font-size:1.2rem;font-weight:700;color:var(--warm)}}
.sy-stat .lbl{{font-size:.7rem;color:var(--text3)}}
.unit-card{{background:var(--card);border-radius:var(--radius-lg);border:1px solid var(--border);margin-bottom:12px;overflow:hidden}}
.unit-card-header{{padding:14px 18px;cursor:pointer;display:flex;align-items:center;justify-content:space-between;transition:var(--transition)}}
.unit-card-header:hover{{background:var(--bg2)}}
.uh-left{{display:flex;align-items:center;gap:10px}}
.uh-icon{{width:32px;height:32px;border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:.9rem;flex-shrink:0}}
.uh-icon.bio{{background:var(--green-light);color:var(--green)}}
.uh-icon.chem{{background:var(--blue-light);color:var(--blue)}}
.uh-icon.geo{{background:var(--brown-light);color:var(--brown)}}
.uh-icon.phy{{background:var(--warm-light);color:var(--warm)}}
.uh-icon.math{{background:var(--blue-light);color:var(--blue)}}
.uh-icon.cn{{background:var(--purple-light);color:var(--purple)}}
.uh-icon.eng{{background:var(--warm-light);color:var(--warm)}}
.uh-icon.hist{{background:var(--brown-light);color:var(--brown)}}
.uh-icon.pol{{background:var(--teal-light);color:var(--teal)}}
.uh-title{{font-weight:700;font-size:.9rem}}
.uh-count{{font-size:.7rem;color:var(--text3)}}
.uh-arrow{{font-size:.7rem;color:var(--text3);transition:transform .3s}}
.unit-card.open .uh-arrow{{transform:rotate(180deg)}}
.unit-card-body{{display:none;padding:0 18px 14px;border-top:1px solid var(--border)}}
.unit-card.open .unit-card-body{{display:block;animation:expandIn .3s ease}}
@keyframes expandIn{{from{{opacity:0;max-height:0}}to{{opacity:1;max-height:2000px}}}}
.chapter-list{{display:flex;flex-direction:column;gap:6px;margin-top:10px}}
.chapter-node{{background:var(--bg2);border-radius:var(--radius-sm);padding:10px 14px;cursor:pointer;transition:var(--transition);border:1px solid transparent}}
.chapter-node:hover{{border-color:var(--warm2);background:var(--warm-light)}}
.cn-header{{display:flex;justify-content:space-between;align-items:center}}
.cn-title{{font-weight:600;font-size:.82rem}}
.cn-arrow{{font-size:.65rem;color:var(--text3);transition:transform .3s}}
.chapter-node.open .cn-arrow{{transform:rotate(180deg)}}
.cn-sections{{display:none;margin-top:6px;padding-top:6px;border-top:1px dashed var(--border)}}
.chapter-node.open .cn-sections{{display:block}}
.section-item{{display:flex;align-items:center;gap:6px;padding:5px 6px;border-radius:6px;font-size:.78rem;color:var(--text2);cursor:pointer;transition:var(--transition)}}
.section-item:hover{{background:var(--warm-light);color:var(--warm)}}
.section-item .si-dot{{width:5px;height:5px;border-radius:50%;background:var(--warm2);flex-shrink:0}}
.section-item .si-page{{font-size:.68rem;color:var(--text3);margin-left:auto}}
.sy-actions{{display:flex;gap:10px;justify-content:center;margin:20px 0;flex-wrap:wrap}}
.sy-standards{{max-width:800px;margin:20px auto;padding:0 20px}}
.sy-standards h3{{font-size:1.05rem;font-weight:700;margin-bottom:12px;text-align:center}}
.std-ref-cards{{display:flex;gap:10px;flex-wrap:wrap;justify-content:center}}
.std-ref-card{{background:var(--card);border-radius:var(--radius-sm);padding:14px;border:1px solid var(--border);flex:1;min-width:180px;max-width:280px;text-align:center}}
.std-ref-card .src-icon{{font-size:1.6rem;margin-bottom:4px}}
.std-ref-card .src-title{{font-weight:600;font-size:.78rem;margin-bottom:2px}}
.std-ref-card .src-desc{{font-size:.7rem;color:var(--text3);margin-bottom:8px;line-height:1.4}}
.std-keypoints{{margin-top:14px;display:flex;flex-wrap:wrap;gap:6px;justify-content:center}}
.std-keypoint{{background:var(--warm-light);color:var(--warm);padding:3px 10px;border-radius:10px;font-size:.72rem;font-weight:500}}

/* ====== LEARNING PAGE ====== */
.learning-page{{min-height:100vh}}
.lp-header{{background:var(--card);padding:8px 16px;position:sticky;top:0;z-index:100;border-bottom:1px solid var(--border);display:flex;align-items:center;gap:8px;backdrop-filter:blur(10px);background:rgba(255,255,255,.92)}}
.lp-back{{display:flex;align-items:center;gap:4px;color:var(--warm);cursor:pointer;font-size:.8rem;font-weight:500;padding:5px 10px;border-radius:16px;transition:var(--transition);background:transparent;border:none}}
.lp-back:hover{{background:var(--warm-light)}}
.lp-title{{font-size:.95rem;font-weight:700;flex:1;text-align:center}}
.lp-tabs-wrap{{overflow-x:auto;white-space:nowrap;scrollbar-width:none;-ms-overflow-style:none;padding:0 4px}}
.lp-tabs-wrap::-webkit-scrollbar{{display:none}}
.lp-tabs{{display:inline-flex;gap:3px;background:var(--bg2);border-radius:24px;padding:3px}}
.lp-tab{{padding:5px 14px;border-radius:22px;border:none;cursor:pointer;font-size:.76rem;font-weight:500;color:var(--text2);background:transparent;transition:var(--transition);white-space:nowrap}}
.lp-tab.active{{background:var(--warm);color:#fff;box-shadow:0 2px 8px rgba(232,125,75,.25)}}
.lp-tab:hover:not(.active){{color:var(--warm)}}

.lp-container{{max-width:960px;margin:0 auto;padding:12px 14px 40px}}
.lp-hero{{text-align:center;padding:16px 12px 8px}}
.lp-hero h2{{font-size:1.35rem;font-weight:700;margin-bottom:4px}}
.lp-hero p{{color:var(--text2);font-size:.84rem;max-width:480px;margin:0 auto}}
.lp-stats{{display:flex;justify-content:center;gap:24px;margin-top:12px;flex-wrap:wrap}}
.lp-stat{{text-align:center}}
.lp-stat .num{{font-size:1.2rem;font-weight:700;color:var(--warm)}}
.lp-stat .lbl{{font-size:.7rem;color:var(--text3);margin-top:1px}}

/* Knowledge Cards */
.unit-section{{margin:18px 0 6px}}
.unit-title{{font-size:1rem;font-weight:700;padding:6px 0;border-bottom:2px solid var(--warm-light);margin-bottom:10px;display:flex;align-items:center;gap:8px}}
.unit-title .icon{{width:26px;height:26px;border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:.78rem}}
.unit-title .icon.bio{{background:var(--green-light);color:var(--green)}}
.unit-title .icon.chem{{background:var(--blue-light);color:var(--blue)}}
.unit-title .icon.geo{{background:var(--brown-light);color:var(--brown)}}
.unit-title .icon.phy{{background:var(--warm-light);color:var(--warm)}}
.unit-title .icon.math{{background:var(--blue-light);color:var(--blue)}}
.unit-title .icon.cn{{background:var(--purple-light);color:var(--purple)}}
.unit-title .icon.eng{{background:var(--warm-light);color:var(--warm)}}
.unit-title .icon.hist{{background:var(--brown-light);color:var(--brown)}}
.unit-title .icon.pol{{background:var(--teal-light);color:var(--teal)}}
.knowledge-grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(270px,1fr));gap:10px;margin-bottom:20px}}
.kcard{{background:var(--card);border-radius:var(--radius);padding:16px;border:1px solid var(--border);cursor:pointer;transition:var(--transition);position:relative}}
.kcard:hover{{transform:translateY(-2px);box-shadow:var(--shadow);border-color:var(--warm2)}}
.kcard .kc-top{{display:flex;justify-content:space-between;align-items:flex-start;gap:6px;margin-bottom:6px}}
.kcard .kc-num{{font-size:.66rem;font-weight:600;color:var(--warm);background:var(--warm-light);padding:2px 8px;border-radius:8px;white-space:nowrap}}
.kcard .kc-lock{{font-size:.8rem;opacity:.5}}
.kcard .kc-title{{font-size:.88rem;font-weight:600;margin-bottom:3px;line-height:1.35}}
.kcard .kc-case{{font-size:.74rem;color:var(--text2);line-height:1.5;display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;overflow:hidden}}
.kcard .kc-tags{{display:flex;gap:5px;margin-top:8px;flex-wrap:wrap}}
.kcard .kc-tag{{font-size:.66rem;padding:2px 8px;border-radius:8px;font-weight:500}}
.kcard .kc-tag.exam{{background:var(--purple-light);color:var(--purple)}}
.kcard .kc-tag.game{{background:var(--warm-light);color:var(--warm)}}
.kcard .kc-tag.quiz{{background:var(--green-light);color:var(--green)}}
.kcard .kc-detail{{display:none;margin-top:12px;padding-top:12px;border-top:1px solid var(--border)}}
.kcard.expanded .kc-detail{{display:block}}
.kcard .kc-detail h4{{font-size:.78rem;font-weight:600;margin-bottom:4px}}
.kcard .kc-detail ul{{list-style:none;padding:0;margin:0 0 8px}}
.kcard .kc-detail ul li{{font-size:.76rem;color:var(--text2);padding:2px 0;padding-left:14px;position:relative}}
.kcard .kc-detail ul li:before{{content:'·';position:absolute;left:3px;color:var(--warm2);font-weight:700}}
.kcard .kc-detail .night{{background:var(--warm-light);border-radius:var(--radius-sm);padding:8px 12px;font-size:.76rem;color:var(--warm);margin-bottom:8px;line-height:1.5}}
.kcard .kc-detail .btns{{display:flex;gap:6px;flex-wrap:wrap}}

/* Chat */
.chat-panel{{background:var(--card);border-radius:var(--radius-lg);border:1px solid var(--border);overflow:hidden;margin-top:20px}}
.chat-header{{padding:12px 16px;border-bottom:1px solid var(--border);display:flex;align-items:center;gap:10px;background:var(--bg2)}}
.chat-avatar{{width:36px;height:36px;border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:1.1rem;flex-shrink:0}}
.chat-avatar.bio{{background:var(--green-light)}}
.chat-avatar.chem{{background:var(--blue-light)}}
.chat-avatar.geo{{background:var(--brown-light)}}
.chat-header .name{{font-weight:700;font-size:.85rem}}
.chat-header .role{{font-size:.7rem;color:var(--text3)}}
.chat-body{{padding:14px;max-height:360px;overflow-y:auto;display:flex;flex-direction:column;gap:10px}}
.chat-msg{{max-width:85%;padding:10px 14px;border-radius:14px;font-size:.82rem;line-height:1.5}}
.chat-msg.user{{align-self:flex-end;background:var(--warm);color:#fff;border-bottom-right-radius:4px}}
.chat-msg.ai{{align-self:flex-start;background:var(--bg2);color:var(--text);border-bottom-left-radius:4px}}
.chat-input-row{{display:flex;gap:8px;padding:10px 14px;border-top:1px solid var(--border)}}
.chat-input{{flex:1;padding:10px 14px;border-radius:20px;border:1.5px solid var(--border);font-size:.82rem;background:var(--bg);outline:none;transition:var(--transition);font-family:inherit}}
.chat-input:focus{{border-color:var(--warm2);background:var(--warm-light)}}

/* Floating bar */
.floating-bar{{position:fixed;bottom:16px;left:50%;transform:translateX(-50%);background:var(--card);border:1px solid var(--border);border-radius:28px;padding:4px 6px;display:flex;gap:3px;box-shadow:var(--shadow-lg);z-index:90}}
.floating-bar button{{padding:7px 16px;border-radius:22px;border:none;cursor:pointer;font-size:.76rem;font-weight:500;transition:var(--transition);background:transparent;color:var(--text2);white-space:nowrap}}
.floating-bar button:hover,.floating-bar button.active-b{{background:var(--warm-light);color:var(--warm)}}

/* Quiz Modal (unchanged from original, imported via JS) */
.modal-overlay{{display:none;position:fixed;inset:0;background:rgba(0,0,0,.45);z-index:200;align-items:center;justify-content:center;backdrop-filter:blur(4px)}}
.modal-overlay.show{{display:flex}}
.modal{{background:var(--card);border-radius:18px;width:92%;max-width:540px;max-height:85vh;overflow-y:auto;box-shadow:0 16px 48px rgba(0,0,0,.18);animation:modalIn .3s ease}}
@keyframes modalIn{{from{{opacity:0;transform:translateY(16px)scale(.97)}}to{{opacity:1;transform:translateY(0)scale(1)}}}}
.modal-header{{padding:16px 20px;border-bottom:1px solid var(--border);display:flex;justify-content:space-between;align-items:center;position:sticky;top:0;background:var(--card);z-index:1}}
.modal-header h3{{font-size:1rem;font-weight:700}}
.modal-close{{width:30px;height:30px;border-radius:50%;border:1px solid var(--border);background:var(--bg2);cursor:pointer;font-size:.9rem;transition:var(--transition)}}
.modal-close:hover{{background:var(--warm-light);border-color:var(--warm2)}}
.modal-body{{padding:16px 20px 20px}}
.quiz-progress{{display:flex;align-items:center;gap:8px;margin-bottom:16px}}
.quiz-progress .bar{{flex:1;height:5px;background:var(--bg2);border-radius:3px;overflow:hidden}}
.quiz-progress .bar-fill{{height:100%;background:linear-gradient(90deg,var(--warm),var(--warm2));border-radius:3px;transition:width .4s}}
.quiz-progress .txt{{font-size:.76rem;color:var(--text2);white-space:nowrap}}
.quiz-q{{font-size:1rem;font-weight:600;margin-bottom:16px;line-height:1.55}}
.quiz-img{{text-align:center;margin:10px 0;font-size:2.5rem}}
.quiz-type-badge{{display:inline-block;font-size:.66rem;padding:2px 8px;border-radius:8px;margin-bottom:8px;font-weight:500}}
.quiz-type-badge.mc{{background:var(--blue-light);color:var(--blue)}}
.quiz-type-badge.fill{{background:var(--green-light);color:var(--green)}}
.quiz-type-badge.sort{{background:var(--purple-light);color:var(--purple)}}
.quiz-options{{display:flex;flex-direction:column;gap:8px}}
.quiz-opt{{padding:12px 16px;border-radius:var(--radius-sm);border:2px solid var(--border);cursor:pointer;font-size:.85rem;transition:var(--transition);background:var(--bg2)}}
.quiz-opt:hover{{border-color:var(--warm2);background:var(--warm-light)}}
.quiz-opt.selected{{border-color:var(--warm);background:var(--warm-light);font-weight:600}}
.quiz-opt.correct{{border-color:var(--green);background:var(--green-light);color:var(--green)}}
.quiz-opt.wrong{{border-color:#e74c3c;background:#fdeaea;color:#e74c3c}}
.quiz-fill-input{{padding:12px 16px;border-radius:var(--radius-sm);border:2px solid var(--border);font-size:.9rem;width:100%;background:var(--bg2);font-family:inherit;transition:var(--transition)}}
.quiz-fill-input:focus{{outline:none;border-color:var(--warm2);background:var(--warm-light)}}
.quiz-sort-list{{display:flex;flex-direction:column;gap:6px}}
.quiz-sort-item{{padding:10px 14px;border-radius:var(--radius-sm);border:2px solid var(--border);background:var(--bg2);cursor:grab;font-size:.82rem;transition:var(--transition);display:flex;align-items:center;gap:8px}}
.quiz-sort-item:active{{cursor:grabbing;background:var(--warm-light);border-color:var(--warm2)}}
.quiz-sort-item .num{{width:22px;height:22px;border-radius:50%;background:var(--warm-light);color:var(--warm);display:flex;align-items:center;justify-content:center;font-size:.7rem;font-weight:700;flex-shrink:0}}
.quiz-feedback{{padding:14px;border-radius:var(--radius-sm);margin-top:14px;display:none;animation:fadeIn .3s}}
.quiz-feedback.show{{display:block}}
.quiz-feedback.ok{{background:var(--green-light);color:var(--green)}}
.quiz-feedback.fail{{background:#fdeaea;color:#e74c3c}}
.quiz-feedback .explanation{{margin-top:6px;font-size:.78rem;color:var(--text2);line-height:1.5}}
@keyframes fadeIn{{from{{opacity:0;transform:translateY(-6px)}}to{{opacity:1;transform:translateY(0)}}}}
.quiz-result{{text-align:center;padding:16px 0}}

/* Footer */
.home-footer{{text-align:center;padding:20px;color:var(--text3);font-size:.7rem;border-top:1px solid var(--border);margin-top:16px}}

/* Mobile */
@media (max-width:768px){{
  .cc-grid{{grid-template-columns:repeat(auto-fill,minmax(160px,1fr))}}
  .lib-grid{{grid-template-columns:1fr}}
  .knowledge-grid{{grid-template-columns:1fr}}
  .home-hero h1{{font-size:1.5rem}}
  .home-hero{{padding:36px 16px 32px}}
  .course-grid-section{{margin-top:-20px;padding:0 12px}}
  .lp-tabs{{gap:2px}}
  .lp-tab{{padding:5px 10px;font-size:.7rem}}
  .floating-bar{{bottom:10px;padding:3px 4px}}
  .floating-bar button{{padding:6px 12px;font-size:.7rem}}
}}
</style>
</head>
<body>

<!-- ====== VIEW 1: HOME ====== -->
<div class="view active home-page" id="viewHome">
  <div class="home-hero">
    <div class="logo-icon">🏫</div>
    <h1>智慧<span class="hl">学堂</span></h1>
    <p class="subtitle">初中全科 AI 辅助学习平台 · 9大学科全覆盖 · 与教材同步</p>
    <div class="hero-badge">📚 48册教材 · 11套课程标准 · AI智能答疑</div>
    <div class="hero-stats">
      <div class="hero-stat"><div class="num">9</div><div class="lbl">学科覆盖</div></div>
      <div class="hero-stat"><div class="num">48</div><div class="lbl">教材PDF</div></div>
      <div class="hero-stat"><div class="num">11</div><div class="lbl">课程标准</div></div>
    </div>
  </div>

  <div class="course-grid-section">
    <h2>📚 选择学科开始学习</h2>
    <div class="cc-grid">
{gen_course_cards()}
    </div>
  </div>

  <div class="features-section">
    <h2>✨ 学习功能</h2>
    <div class="feature-grid">
      <div class="feature-item">
        <div class="fi-icon">🤖</div>
        <div class="fi-title">AI 智能问答</div>
        <div class="fi-desc">各学科专属AI助教，用生活类比讲透知识点</div>
      </div>
      <div class="feature-item">
        <div class="fi-icon">🎮</div>
        <div class="fi-title">沙盘互动游戏</div>
        <div class="fi-desc">HTML5互动游戏，在玩中学，抽象概念触手可及</div>
      </div>
      <div class="feature-item">
        <div class="fi-icon">📝</div>
        <div class="fi-title">随堂测验系统</div>
        <div class="fi-desc">选择/填空/排序三大题型，即时反馈巩固效果</div>
      </div>
      <div class="feature-item">
        <div class="fi-icon">📖</div>
        <div class="fi-title">全册教材PDF</div>
        <div class="fi-desc">48册教材在线预览，覆盖全部年级上下册</div>
      </div>
    </div>
  </div>

  <div class="std-section">
    <h2>📋 义务教育课程标准 (2022年版)</h2>
    <div class="std-grid">
{gen_standards_html()}
    </div>
  </div>

  <div class="lib-section">
    <h2>📚 教材资源库（全部年级）</h2>
    <div class="lib-grid">
{gen_textbook_html()}
    </div>
  </div>

  <div class="home-footer">
    智慧学堂 v5.0 | 初中全科 AI 辅助学习 | 基于人教版2024版教材 | 48册教材PDF · 11套课程标准
  </div>
</div>

<!-- ====== VIEW 2: SYLLABUS ====== -->
<div class="view syllabus-page" id="viewSyllabus">
  <div class="sy-header">
    <button class="btn-nav" onclick="navigateTo('home')">← 首页</button>
    <div class="breadcrumb">
      <a onclick="navigateTo('home')">智慧学堂</a>
      <span class="sep">›</span>
      <span class="current" id="syllabusBreadcrumb">生物学</span>
    </div>
  </div>
  <div class="sy-body">
    <div class="sy-hero">
      <div class="sh-icon" id="syllabusIcon">🧬</div>
      <h2 id="syllabusTitle">生物学</h2>
      <p id="syllabusSubtitle">人教版 · 2024版 · 课程知识结构</p>
    </div>
    <div class="sy-stats">
      <div class="sy-stat"><div class="num" id="sy-knowledge">-</div><div class="lbl">知识点</div></div>
      <div class="sy-stat"><div class="num" id="sy-quiz">-</div><div class="lbl">练习题</div></div>
      <div class="sy-stat"><div class="num" id="sy-games">-</div><div class="lbl">游戏设计</div></div>
    </div>
    <div class="unit-map" id="syllabusUnitMap"></div>
    <div class="sy-actions">
      <button class="btn-sm btn-warm" onclick="navigateTo('learning',currentSubject)">🎯 开始学习</button>
      <button class="btn-sm btn-outline" onclick="viewStandards()">📋 查看课程标准</button>
    </div>
    <div class="sy-standards" id="syllabusStandardsWrap">
      <h3>📋 相关课程标准</h3>
      <div class="std-ref-cards" id="syllabusStandards"></div>
      <div class="std-keypoints" id="syllabusKeypoints"></div>
    </div>
  </div>
</div>

<!-- ====== VIEW 3: LEARNING ====== -->
<div class="view learning-page" id="viewLearning">
  <div class="lp-header">
    <button class="lp-back" onclick="navigateTo('syllabus',currentSubject)">← 大纲</button>
    <span class="lp-title" id="lpTitle">🌿 生物七上</span>
    <div class="lp-tabs-wrap">
      <div class="lp-tabs">
{gen_lp_tabs()}
      </div>
    </div>
  </div>
  <div class="lp-container">
    <div class="lp-hero">
      <h2 id="lpHeroTitle">在夜市里学生物</h2>
      <p id="lpHeroSubtitle">发面馒头学细胞分裂，夜市摊位学观察调查</p>
    </div>
    <div class="lp-stats">
      <div class="lp-stat"><div class="num" id="stat-know">-</div><div class="lbl">知识点</div></div>
      <div class="lp-stat"><div class="num" id="stat-quiz">-</div><div class="lbl">练习题</div></div>
      <div class="lp-stat"><div class="num" id="stat-games">-</div><div class="lbl">游戏设计</div></div>
    </div>
    <div class="progress-bar-wrap" id="progressBarWrap" style="margin:12px 0;display:none">
      <div style="height:6px;background:var(--bg2);border-radius:3px;overflow:hidden">
        <div id="progressBar" style="height:100%;background:linear-gradient(90deg,var(--warm),var(--warm2));border-radius:3px;width:0%;transition:width .5s"></div>
      </div>
    </div>
    <div id="knowledgeContainer"></div>
    <div id="chatPanel" class="chat-panel">
      <div class="chat-header">
        <div class="chat-avatar" id="chatAvatar">👨‍🍳</div>
        <div>
          <div class="name" id="chatName">夜市大厨 · 阿火</div>
          <div class="role" id="chatRole">20年老厨师 · 生化知识隐藏大师</div>
        </div>
      </div>
      <div class="chat-body" id="chatBody">
        <div class="chat-msg ai">嘿！我是阿火。烤串20年了，有啥不懂的生物化学问题尽管问——我用夜市的道理给你讲明白！</div>
      </div>
      <div class="chat-input-row">
        <input class="chat-input" id="chatInput" placeholder="输入你的问题..." onkeydown="if(event.key==='Enter')sendChat()">
        <button class="btn-sm btn-warm" onclick="sendChat()">发送</button>
      </div>
    </div>
  </div>
</div>

<!-- ====== MODALS ====== -->
<div class="modal-overlay" id="quizModal">
  <div class="modal">
    <div class="modal-header">
      <h3 id="quizModalTitle">随堂测验</h3>
      <button class="modal-close" onclick="closeQuiz()">✕</button>
    </div>
    <div class="modal-body" id="quizModalBody"></div>
  </div>
</div>

<div class="modal-overlay" id="gameModal">
  <div class="modal" style="max-width:720px">
    <div class="modal-header">
      <h3 id="gameModalTitle">沙盘游戏</h3>
      <button class="modal-close" onclick="closeGame()">✕</button>
    </div>
    <div class="modal-body" id="gameModalBody"></div>
  </div>
</div>

<div class="floating-bar" id="floatingBar" style="display:none">
  <button class="active-b" id="fbAll" onclick="filterKnowledge('all')">全部</button>
  <button id="fbFree" onclick="filterKnowledge('free')">免费</button>
  <button id="fbPaid" onclick="filterKnowledge('paid')">进阶</button>
  <button id="fbGame" onclick="filterKnowledge('game')">🎮 游戏</button>
</div>

<script>
{script_content}
</script>
</body>
</html>'''

# Write output
with open(OUT_PATH, 'w', encoding='utf-8') as f:
    f.write(new_html)

print(f'✅ Generated {OUT_PATH}')
print(f'   Size: {len(new_html):,} bytes')
