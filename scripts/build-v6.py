#!/usr/bin/env python3
"""
Build bio-chem-ai v6.0 index.html
- Blue theme (primary: #2563eb)
- Grade selection before chapters
- Clean sidebar + content + AI assistant layout
- DeepSeek API integration
- Paywall / unlock logic
"""

import json
import os

OUTPUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'index_v6.html')
DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data')

SUBJECTS = {
    'bio':  {'name':'生物学','icon':'🧬','grades':[7,8],'color':'#10b981','emoji':'🌿'},
    'chem': {'name':'化学','icon':'⚗️','grades':[9],'color':'#8b5cf6','emoji':'🧪'},
    'geo':  {'name':'地理','icon':'🗺️','grades':[7,8],'color':'#f59e0b','emoji':'🌍'},
    'phy':  {'name':'物理','icon':'⚡','grades':[8,9],'color':'#ef4444','emoji':'🔬'},
    'math': {'name':'数学','icon':'📐','grades':[7,8,9],'color':'#3b82f6','emoji':'🔢'},
    'cn':   {'name':'语文','icon':'📖','grades':[7,8,9],'color':'#ec4899','emoji':'✍️'},
    'eng':  {'name':'英语','icon':'🔤','grades':[7,8,9],'color':'#06b6d4','emoji':'🌐'},
    'hist': {'name':'历史','icon':'🏛️','grades':[7,8,9],'color':'#78716c','emoji':'📜'},
    'pol':  {'name':'道德与法治','icon':'⚖️','grades':[7,8,9],'color':'#14b8a6','emoji':'🏛️'},
}

# Load all data
all_data = {}
for subj_id in SUBJECTS:
    fname_map = {
        'bio':'bio_data.json','chem':'chem_data.json','geo':'geo_data.json',
        'phy':'phy_data.json','math':'math_data.json','cn':'cn_data.json',
        'eng':'eng_data.json','hist':'hist_data.json','pol':'pol_data.json'
    }
    try:
        with open(os.path.join(DATA_DIR, fname_map[subj_id]), 'r', encoding='utf-8') as f:
            all_data[subj_id] = json.load(f)
    except:
        all_data[subj_id] = []

# Build grade data
grade_data = {}
for subj_id, items in all_data.items():
    for item in items:
        gid = item.get('grade', SUBJECTS[subj_id]['grades'][0])
        if subj_id not in grade_data:
            grade_data[subj_id] = {}
        if gid not in grade_data[subj_id]:
            grade_data[subj_id][gid] = []
        grade_data[subj_id][gid].append(item)

CSS = r'''
:root {
  --blue-50: #eff6ff; --blue-100: #dbeafe; --blue-200: #bfdbfe;
  --blue-400: #60a5fa; --blue-500: #3b82f6; --blue-600: #2563eb;
  --blue-700: #1d4ed8; --blue-800: #1e40af;
  --gray-50: #f8fafc; --gray-100: #f1f5f9; --gray-200: #e2e8f0;
  --gray-300: #cbd5e1; --gray-400: #94a3b8; --gray-500: #64748b;
  --gray-600: #475569; --gray-700: #334155; --gray-800: #1e293b; --gray-900: #0f172a;
  --white: #ffffff;
  --radius: 12px; --radius-sm: 8px; --radius-lg: 16px;
  --shadow-sm: 0 1px 2px rgba(0,0,0,.05);
  --shadow: 0 1px 3px rgba(0,0,0,.1), 0 1px 2px rgba(0,0,0,.06);
  --shadow-md: 0 4px 6px -1px rgba(0,0,0,.1), 0 2px 4px -2px rgba(0,0,0,.1);
  --shadow-lg: 0 10px 15px -3px rgba(0,0,0,.1), 0 4px 6px -4px rgba(0,0,0,.1);
  --transition: .2s cubic-bezier(.4,0,.2,1);
}
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:"PingFang SC","Microsoft YaHei","Noto Sans SC",-apple-system,sans-serif;background:#f0f4ff;color:var(--gray-800);min-height:100vh;line-height:1.6;overflow-x:hidden}
::-webkit-scrollbar{width:5px}::-webkit-scrollbar-track{background:transparent}::-webkit-scrollbar-thumb{background:var(--gray-300);border-radius:10px}

/* ===== VIEWS ===== */
.view{display:none}
.view.active{display:block;animation:viewIn .3s ease}
@keyframes viewIn{from{opacity:0;transform:translateY(8px)}to{opacity:1;transform:translateY(0)}}

/* ===== HOME PAGE ===== */
.home-page{min-height:100vh}
.home-hero{background:linear-gradient(135deg,#1e3a5f 0%,#2563eb 40%,#3b82f6 70%,#60a5fa 100%);padding:60px 24px 80px;text-align:center;position:relative;overflow:hidden}
.home-hero::before{content:'';position:absolute;top:-100px;right:-100px;width:400px;height:400px;border-radius:50%;background:rgba(255,255,255,.04)}
.home-hero::after{content:'';position:absolute;bottom:-80px;left:-80px;width:300px;height:300px;border-radius:50%;background:rgba(255,255,255,.03)}
.home-hero h1{font-size:2.2rem;font-weight:800;color:#fff;margin-bottom:8px;letter-spacing:.5px;position:relative;z-index:1}
.home-hero .subtitle{font-size:.95rem;color:rgba(255,255,255,.8);max-width:500px;margin:0 auto 24px;position:relative;z-index:1}
.home-hero .hero-stats{display:flex;justify-content:center;gap:40px;position:relative;z-index:1}
.home-hero .hero-stat{text-align:center}
.home-hero .hero-stat .num{font-size:2rem;font-weight:800;color:#fff}
.home-hero .hero-stat .lbl{font-size:.75rem;color:rgba(255,255,255,.65);margin-top:2px}
.course-section{max-width:1200px;margin:-40px auto 0;padding:0 24px;position:relative;z-index:2}
.course-section h2{font-size:1.3rem;font-weight:700;color:var(--gray-800);margin-bottom:16px}
.course-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(160px,1fr));gap:10px}
.course-card{background:var(--white);border-radius:var(--radius-lg);padding:18px 14px;border:1px solid var(--gray-200);box-shadow:var(--shadow-sm);cursor:pointer;transition:var(--transition);text-align:center;position:relative;overflow:hidden}
.course-card:hover{transform:translateY(-3px);box-shadow:var(--shadow-lg);border-color:var(--blue-200)}
.course-card .cc-icon{font-size:2rem;display:block;margin-bottom:6px}
.course-card .cc-name{font-size:.9rem;font-weight:700;color:var(--gray-800);margin-bottom:2px}
.course-card .cc-grade{font-size:.7rem;color:var(--gray-400);margin-bottom:4px}
.course-card .cc-desc{font-size:.72rem;color:var(--gray-500);line-height:1.4}
.course-card::before{content:'';position:absolute;top:0;left:0;right:0;height:3px;background:var(--cc-accent,#2563eb)}

/* ===== GRADE SELECTION MODAL ===== */
.modal-overlay{position:fixed;top:0;left:0;right:0;bottom:0;background:rgba(0,0,0,.4);z-index:1000;display:flex;align-items:center;justify-content:center;animation:fadeIn .2s ease}
@keyframes fadeIn{from{opacity:0}to{opacity:1}}
.grade-modal{background:var(--white);border-radius:var(--radius-lg);padding:32px;max-width:420px;width:90%;box-shadow:var(--shadow-lg);text-align:center;animation:slideUp .3s ease}
@keyframes slideUp{from{opacity:0;transform:translateY(20px)}to{opacity:1;transform:translateY(0)}}
.grade-modal .gm-icon{font-size:3rem;margin-bottom:10px}
.grade-modal h3{font-size:1.2rem;font-weight:700;margin-bottom:4px;color:var(--gray-800)}
.grade-modal .gm-subtitle{font-size:.82rem;color:var(--gray-500);margin-bottom:20px}
.grade-modal .gm-grades{display:flex;gap:12px;justify-content:center;flex-wrap:wrap}
.grade-btn{padding:14px 32px;border-radius:var(--radius);border:2px solid var(--gray-200);background:var(--white);cursor:pointer;font-size:.95rem;font-weight:600;transition:var(--transition);min-width:80px}
.grade-btn:hover{border-color:var(--blue-400);background:var(--blue-50);color:var(--blue-700)}
.grade-btn.selected{border-color:var(--blue-600);background:var(--blue-50);color:var(--blue-700)}
.grade-modal .gm-actions{margin-top:20px;display:flex;gap:10px;justify-content:center}
.btn{padding:10px 24px;border-radius:var(--radius);border:none;cursor:pointer;font-size:.85rem;font-weight:600;transition:var(--transition)}
.btn-primary{background:var(--blue-600);color:#fff}
.btn-primary:hover{background:var(--blue-700);transform:scale(1.02)}
.btn-ghost{background:transparent;color:var(--gray-500);border:1px solid var(--gray-200)}
.btn-ghost:hover{background:var(--gray-50)}

/* ===== SYLLABUS PAGE (CHAPTER OUTLINE) ===== */
.syllabus-page{min-height:100vh}
.sy-header{background:rgba(255,255,255,.95);backdrop-filter:blur(10px);padding:12px 20px;position:sticky;top:0;z-index:100;border-bottom:1px solid var(--gray-200);display:flex;align-items:center;gap:12px}
.sy-header .sy-back{display:flex;align-items:center;gap:4px;color:var(--blue-600);cursor:pointer;font-size:.82rem;font-weight:500;border:none;background:none;padding:6px 10px;border-radius:var(--radius-sm);transition:var(--transition)}
.sy-header .sy-back:hover{background:var(--blue-50)}
.sy-header .sy-breadcrumb{font-size:.82rem;color:var(--gray-500);flex:1}
.sy-header .sy-breadcrumb .current{color:var(--gray-700);font-weight:600}
.sy-body{max-width:900px;margin:0 auto;padding:24px 20px}
.sy-hero{text-align:center;padding:8px 0 24px}
.sy-hero .sh-icon{font-size:3.5rem;margin-bottom:8px}
.sy-hero h2{font-size:1.5rem;font-weight:700;color:var(--gray-800);margin-bottom:4px}
.sy-hero p{color:var(--gray-500);font-size:.85rem}

/* Chapter tree */
.chapter-card{background:var(--white);border-radius:var(--radius);border:1px solid var(--gray-200);margin-bottom:8px;overflow:hidden;transition:var(--transition)}
.chapter-card:hover{border-color:var(--blue-200)}
.chapter-header{padding:14px 18px;cursor:pointer;display:flex;align-items:center;justify-content:space-between;transition:var(--transition)}
.chapter-header:hover{background:var(--gray-50)}
.chapter-header .ch-left{display:flex;align-items:center;gap:10px}
.chapter-header .ch-num{width:30px;height:30px;border-radius:8px;background:var(--blue-100);color:var(--blue-700);display:flex;align-items:center;justify-content:center;font-size:.78rem;font-weight:700;flex-shrink:0}
.chapter-header .ch-title{font-weight:600;font-size:.9rem;color:var(--gray-800)}
.chapter-header .ch-count{font-size:.7rem;color:var(--gray-400);margin-left:8px}
.chapter-header .ch-arrow{font-size:.7rem;color:var(--gray-400);transition:transform .3s}
.chapter-card.open .ch-arrow{transform:rotate(180deg)}
.chapter-body{display:none;padding:0 18px 12px;border-top:1px solid var(--gray-100)}
.chapter-card.open .chapter-body{display:block}
.section-item{display:flex;align-items:center;gap:8px;padding:8px 10px;border-radius:8px;cursor:pointer;transition:var(--transition);margin:2px 0;font-size:.82rem;color:var(--gray-600)}
.section-item:hover{background:var(--blue-50);color:var(--blue-700)}
.section-item .si-dot{width:6px;height:6px;border-radius:50%;background:var(--blue-400);flex-shrink:0}
.section-item .si-name{flex:1}
.section-item .si-page{font-size:.7rem;color:var(--gray-400)}
.section-item .si-quiz{font-size:.68rem;color:var(--blue-500);background:var(--blue-50);padding:1px 6px;border-radius:4px}

/* ===== LEARNING PAGE ===== */
.learning-page{min-height:100vh;display:flex;flex-direction:column}
.lp-topbar{background:rgba(255,255,255,.95);backdrop-filter:blur(10px);padding:10px 16px;position:sticky;top:0;z-index:100;border-bottom:1px solid var(--gray-200);display:flex;align-items:center;gap:10px}
.lp-topbar .lp-back{display:flex;align-items:center;gap:4px;color:var(--blue-600);cursor:pointer;font-size:.8rem;font-weight:500;border:none;background:none;padding:5px 8px;border-radius:6px;transition:var(--transition)}
.lp-topbar .lp-back:hover{background:var(--blue-50)}
.lp-topbar .lp-breadcrumb{font-size:.78rem;color:var(--gray-500);flex:1}
.lp-topbar .lp-breadcrumb .current{color:var(--gray-700);font-weight:600}
.lp-topbar .unlock-badge{font-size:.72rem;padding:3px 10px;border-radius:12px;font-weight:600}
.unlock-badge.free{background:#d1fae5;color:#065f46}
.unlock-badge.locked{background:#fee2e2;color:#991b1b}

.lp-main{display:flex;flex:1;overflow:hidden}

/* Sidebar */
.lp-sidebar{width:260px;background:var(--white);border-right:1px solid var(--gray-200);overflow-y:auto;flex-shrink:0;padding:12px 0}
.lp-sidebar .sidebar-title{font-size:.72rem;font-weight:700;color:var(--gray-400);text-transform:uppercase;letter-spacing:.5px;padding:0 16px 8px}
.sidebar-chapter{margin-bottom:2px}
.sidebar-chapter .sc-header{padding:8px 16px;cursor:pointer;display:flex;align-items:center;gap:6px;font-size:.78rem;font-weight:600;color:var(--gray-600);transition:var(--transition)}
.sidebar-chapter .sc-header:hover{background:var(--gray-50);color:var(--gray-800)}
.sidebar-chapter .sc-header .sc-dot{width:5px;height:5px;border-radius:50%;background:var(--gray-300);flex-shrink:0}
.sidebar-chapter .sc-sections{padding:2px 0}
.sidebar-chapter .sc-sections .sc-item{padding:6px 16px 6px 32px;cursor:pointer;font-size:.75rem;color:var(--gray-500);transition:var(--transition);display:flex;align-items:center;gap:6px;border-left:2px solid transparent}
.sidebar-chapter .sc-sections .sc-item:hover{background:var(--blue-50);color:var(--blue-700);border-left-color:var(--blue-400)}
.sidebar-chapter .sc-sections .sc-item.active{background:var(--blue-50);color:var(--blue-700);border-left-color:var(--blue-600);font-weight:600}

/* Content area */
.lp-content{flex:1;overflow-y:auto;padding:24px 28px 40px}
.lp-content .content-header{margin-bottom:24px;padding-bottom:16px;border-bottom:2px solid var(--gray-100)}
.lp-content .content-header .ch-section-num{font-size:.78rem;font-weight:600;color:var(--blue-500);margin-bottom:4px;text-transform:uppercase;letter-spacing:.5px}
.lp-content .content-header h2{font-size:1.4rem;font-weight:700;color:var(--gray-800);margin-bottom:4px}
.lp-content .content-header .ch-page{font-size:.78rem;color:var(--gray-400)}
.lp-content .content-header .ch-exam-tags{margin-top:8px;display:flex;gap:6px;flex-wrap:wrap}
.lp-content .content-header .exam-tag{font-size:.7rem;padding:3px 10px;border-radius:12px;font-weight:500}
.exam-tag.hot{background:#fef3c7;color:#92400e}
.exam-tag.normal{background:var(--gray-100);color:var(--gray-500)}

/* Knowledge section */
.knowledge-section{background:var(--white);border-radius:var(--radius);border:1px solid var(--gray-200);padding:20px;margin-bottom:16px}
.knowledge-section h3{font-size:.95rem;font-weight:700;color:var(--gray-800);margin-bottom:12px;display:flex;align-items:center;gap:8px}
.knowledge-section h3 .icon{font-size:1.1rem}
.knowledge-section ul{padding-left:20px}
.knowledge-section li{font-size:.84rem;color:var(--gray-600);margin-bottom:6px;line-height:1.6}
.knowledge-section li::marker{color:var(--blue-400)}

/* Scene / Case box */
.scene-box{background:linear-gradient(135deg,#eff6ff,#dbeafe);border-radius:var(--radius);padding:16px 20px;margin-bottom:16px;border-left:4px solid var(--blue-500)}
.scene-box .scene-label{font-size:.72rem;font-weight:700;color:var(--blue-600);text-transform:uppercase;letter-spacing:.5px;margin-bottom:4px}
.scene-box .scene-text{font-size:.84rem;color:var(--gray-700);line-height:1.6}

/* Textbook columns */
.col-box{background:var(--gray-50);border-radius:var(--radius);padding:14px 18px;margin-bottom:16px}
.col-box h4{font-size:.8rem;font-weight:600;color:var(--gray-500);margin-bottom:6px;text-transform:uppercase}
.col-box ul{padding-left:18px}
.col-box li{font-size:.8rem;color:var(--gray-600);margin-bottom:3px}

/* Quiz section */
.quiz-section{background:var(--white);border-radius:var(--radius);border:1px solid var(--gray-200);padding:20px;margin-bottom:16px}
.quiz-section h3{font-size:.95rem;font-weight:700;color:var(--gray-800);margin-bottom:12px;display:flex;align-items:center;gap:8px}
.quiz-progress{font-size:.75rem;color:var(--gray-400);margin-left:auto}
.quiz-card{background:var(--gray-50);border-radius:var(--radius-sm);padding:16px;margin-bottom:10px}
.quiz-card .q-text{font-size:.85rem;font-weight:600;color:var(--gray-800);margin-bottom:10px}
.quiz-card .q-options{display:flex;flex-direction:column;gap:6px}
.quiz-card .q-opt{padding:10px 14px;border-radius:8px;border:1.5px solid var(--gray-200);cursor:pointer;font-size:.82rem;color:var(--gray-600);transition:var(--transition);background:var(--white)}
.quiz-card .q-opt:hover{border-color:var(--blue-300);background:var(--blue-50)}
.quiz-card .q-opt.selected{border-color:var(--blue-500);background:var(--blue-50);color:var(--blue-700);font-weight:600}
.quiz-card .q-opt.correct{border-color:#10b981;background:#d1fae5;color:#065f46}
.quiz-card .q-opt.wrong{border-color:#ef4444;background:#fee2e2;color:#991b1b}
.quiz-card .q-feedback{font-size:.78rem;color:var(--gray-500);margin-top:8px;padding:8px 12px;background:var(--gray-50);border-radius:6px;display:none}
.quiz-card .q-feedback.show{display:block}
.quiz-nav{display:flex;gap:8px;justify-content:center;margin-top:12px}
.quiz-nav button{padding:8px 20px;border-radius:var(--radius-sm);border:none;cursor:pointer;font-size:.8rem;font-weight:600;transition:var(--transition)}
.quiz-nav .qn-prev{background:var(--gray-100);color:var(--gray-600)}
.quiz-nav .qn-prev:hover{background:var(--gray-200)}
.quiz-nav .qn-next{background:var(--blue-600);color:#fff}
.quiz-nav .qn-next:hover{background:var(--blue-700)}
.quiz-nav .qn-restart{background:var(--gray-100);color:var(--gray-500);font-size:.75rem}

/* ===== AI CHAT PANEL ===== */
.ai-panel{width:320px;background:var(--white);border-left:1px solid var(--gray-200);display:flex;flex-direction:column;flex-shrink:0}
.ai-panel .ai-header{padding:14px 16px;border-bottom:1px solid var(--gray-200);display:flex;align-items:center;gap:10px}
.ai-panel .ai-avatar{width:36px;height:36px;border-radius:50%;background:var(--blue-100);display:flex;align-items:center;justify-content:center;font-size:1.1rem}
.ai-panel .ai-name{font-size:.82rem;font-weight:700;color:var(--gray-800)}
.ai-panel .ai-role{font-size:.7rem;color:var(--gray-400)}
.ai-panel .ai-body{flex:1;overflow-y:auto;padding:12px;display:flex;flex-direction:column;gap:8px}
.ai-msg{font-size:.78rem;line-height:1.5;padding:8px 12px;border-radius:12px;max-width:90%}
.ai-msg.assistant{background:var(--blue-50);color:var(--gray-700);align-self:flex-start;border-bottom-left-radius:4px}
.ai-msg.user{background:var(--blue-600);color:#fff;align-self:flex-end;border-bottom-right-radius:4px}
.ai-msg.system{font-size:.72rem;color:var(--gray-400);text-align:center;align-self:center}
.ai-panel .ai-input-wrap{padding:12px;border-top:1px solid var(--gray-200);display:flex;gap:8px}
.ai-panel .ai-input{flex:1;padding:8px 12px;border-radius:20px;border:1px solid var(--gray-200);font-size:.8rem;outline:none;font-family:inherit;transition:var(--transition)}
.ai-panel .ai-input:focus{border-color:var(--blue-400);box-shadow:0 0 0 3px rgba(59,130,246,.1)}
.ai-panel .ai-send{width:36px;height:36px;border-radius:50%;border:none;background:var(--blue-600);color:#fff;cursor:pointer;font-size:.9rem;transition:var(--transition);flex-shrink:0;display:flex;align-items:center;justify-content:center}
.ai-panel .ai-send:hover{background:var(--blue-700)}

/* ===== PAYWALL / UNLOCK ===== */
.unlock-overlay{position:fixed;top:0;left:0;right:0;bottom:0;background:rgba(0,0,0,.5);z-index:999;display:flex;align-items:center;justify-content:center}
.unlock-dialog{background:var(--white);border-radius:var(--radius-lg);padding:32px;max-width:400px;width:90%;text-align:center;box-shadow:var(--shadow-lg)}
.unlock-dialog .ud-icon{font-size:3rem;margin-bottom:10px}
.unlock-dialog h3{font-size:1.1rem;font-weight:700;color:var(--gray-800);margin-bottom:6px}
.unlock-dialog p{font-size:.82rem;color:var(--gray-500);margin-bottom:16px;line-height:1.5}
.unlock-dialog .ud-input{padding:10px 14px;border-radius:var(--radius-sm);border:1.5px solid var(--gray-200);width:100%;font-size:.85rem;text-align:center;font-family:inherit;margin-bottom:12px;outline:none}
.unlock-dialog .ud-input:focus{border-color:var(--blue-400)}
.unlock-dialog .ud-error{font-size:.75rem;color:#ef4444;margin-bottom:8px;display:none}
.unlock-dialog .ud-hint{font-size:.72rem;color:var(--gray-400);margin-top:8px}

/* ===== RESOURCE SECTION ===== */
.resource-section{max-width:1200px;margin:48px auto;padding:0 24px}
.resource-section h2{font-size:1.2rem;font-weight:700;color:var(--gray-800);margin-bottom:16px}
.res-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(420px,1fr));gap:14px}
.res-subject{background:var(--white);border-radius:var(--radius);border:1px solid var(--gray-200);padding:16px 18px}
.res-subject .rs-title{font-size:.9rem;font-weight:700;margin-bottom:10px;display:flex;align-items:center;gap:8px}
.res-subject .rs-list{display:flex;flex-direction:column;gap:5px}
.res-item{display:flex;align-items:center;gap:8px;padding:6px 8px;background:var(--gray-50);border-radius:6px;font-size:.78rem;color:var(--gray-600);transition:var(--transition)}
.res-item:hover{background:var(--blue-50);color:var(--blue-700)}
.res-item .ri-grade{font-size:.65rem;font-weight:600;color:var(--blue-600);background:var(--blue-50);padding:1px 6px;border-radius:4px;white-space:nowrap}

/* Mobile responsive */
@media(max-width:768px){
  .course-grid{grid-template-columns:repeat(auto-fill,minmax(140px,1fr))}
  .home-hero{padding:40px 16px 60px}
  .home-hero h1{font-size:1.6rem}
  .lp-main{flex-direction:column}
  .lp-sidebar{width:100%;max-height:200px;border-right:none;border-bottom:1px solid var(--gray-200)}
  .ai-panel{width:100%;max-height:300px;border-left:none;border-top:1px solid var(--gray-200)}
  .res-grid{grid-template-columns:1fr}
}

/* Float bar */
.floating-bar{position:fixed;bottom:16px;right:16px;display:flex;gap:8px;z-index:200;display:none}
.floating-bar .fb-btn{width:44px;height:44px;border-radius:50%;background:var(--white);border:1px solid var(--gray-200);box-shadow:var(--shadow-md);cursor:pointer;font-size:1.1rem;display:flex;align-items:center;justify-content:center;transition:var(--transition)}
.floating-bar .fb-btn:hover{background:var(--blue-50);transform:scale(1.05)}

/* Toggle sidebar on mobile */
@media(max-width:768px){
  .lp-sidebar.collapsed{display:none}
  .ai-panel.collapsed{display:none}
}
'''

HTML_HEAD = '''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>智慧学堂 - 初中全科 AI 教学</title>
<script src="https://cdn.jsdelivr.net/npm/phaser@3.60.0/dist/phaser.min.js"></script>
<style>''' + CSS + '''</style>
</head>
<body>
'''

VIEWS_HTML = '''
<!-- ====== HOME VIEW ====== -->
<div id="view-home" class="view active">
  <div class="home-page">
    <div class="home-hero">
      <h1>📚 智慧学堂</h1>
      <div class="subtitle">初中全科 AI 辅助学习平台 — 基础知识 + 随堂测试 + AI答疑</div>
      <div class="hero-stats">
        <div class="hero-stat"><div class="num">9</div><div class="lbl">学科覆盖</div></div>
        <div class="hero-stat"><div class="num" id="stat-textbooks">48</div><div class="lbl">教材资源</div></div>
        <div class="hero-stat"><div class="num" id="stat-quizzes">200+</div><div class="lbl">随堂练习</div></div>
      </div>
    </div>
    <div class="course-section">
      <h2>📖 选择学科开始学习</h2>
      <div class="course-grid" id="courseGrid">
        <!-- filled by JS -->
      </div>
    </div>
    <div class="resource-section">
      <h2>📋 教材资源库</h2>
      <div class="res-grid" id="resourceGrid">
        <!-- filled by JS -->
      </div>
    </div>
  </div>
</div>

<!-- ====== GRADE MODAL ====== -->
<div id="gradeModal" class="modal-overlay" style="display:none" onclick="if(event.target===this)closeGradeModal()">
  <div class="grade-modal">
    <div class="gm-icon" id="gmIcon"></div>
    <h3 id="gmTitle"></h3>
    <div class="gm-subtitle" id="gmSubtitle"></div>
    <div class="gm-grades" id="gmGrades"></div>
    <div class="gm-actions">
      <button class="btn btn-ghost" onclick="closeGradeModal()">取消</button>
      <button class="btn btn-primary" id="gmConfirm" onclick="confirmGrade()">进入学习 →</button>
    </div>
  </div>
</div>

<!-- ====== SYLLABUS VIEW ====== -->
<div id="view-syllabus" class="view">
  <div class="syllabus-page">
    <div class="sy-header">
      <button class="sy-back" onclick="navigateTo('home')">← 首页</button>
      <div class="sy-breadcrumb" id="syBreadcrumb"></div>
    </div>
    <div class="sy-body">
      <div class="sy-hero">
        <div class="sh-icon" id="syIcon"></div>
        <h2 id="syTitle"></h2>
        <p id="sySubtitle"></p>
      </div>
      <div id="chapterTree"></div>
    </div>
  </div>
</div>

<!-- ====== LEARNING VIEW ====== -->
<div id="view-learning" class="view">
  <div class="learning-page">
    <div class="lp-topbar">
      <button class="lp-back" onclick="navigateTo('syllabus',currentSubject)">← 大纲</button>
      <div class="lp-breadcrumb" id="lpBreadcrumb"></div>
      <span class="unlock-badge free" id="unlockBadge" style="display:none">免费</span>
    </div>
    <div class="lp-main">
      <div class="lp-sidebar" id="lpSidebar"></div>
      <div class="lp-content" id="lpContent"></div>
      <div class="ai-panel" id="aiPanel">
        <div class="ai-header">
          <div class="ai-avatar" id="aiAvatar">🤖</div>
          <div>
            <div class="ai-name" id="aiName">AI 助教</div>
            <div class="ai-role" id="aiRole">有问题尽管问</div>
          </div>
        </div>
        <div class="ai-body" id="chatBody">
          <div class="ai-msg system" id="aiGreeting">👋 你好！我是AI学习助手，选一个知识点开始学习吧～</div>
        </div>
        <div class="ai-input-wrap">
          <input class="ai-input" id="chatInput" placeholder="输入问题..." onkeydown="if(event.key==='Enter')sendChat()">
          <button class="ai-send" onclick="sendChat()">➤</button>
        </div>
      </div>
    </div>
  </div>
  <div class="floating-bar" id="floatingBar">
    <button class="fb-btn" onclick="toggleSidebar()" title="目录">📑</button>
    <button class="fb-btn" onclick="toggleAIPanel()" title="AI助手">💬</button>
  </div>
</div>

<!-- ====== UNLOCK MODAL ====== -->
<div id="unlockModal" class="unlock-overlay" style="display:none">
  <div class="unlock-dialog">
    <div class="ud-icon">🔒</div>
    <h3>解锁全部内容</h3>
    <p>输入解锁码即可畅学全部学科，<br>包含所有知识卡片、随堂测试和AI辅导</p>
    <input class="ud-input" id="unlockCode" placeholder="请输入解锁码" onkeydown="if(event.key==='Enter')doUnlock()">
    <div class="ud-error" id="unlockError">解锁码不正确，请重试</div>
    <button class="btn btn-primary" onclick="doUnlock()" style="width:100%">🔓 立即解锁</button>
    <div class="ud-hint">💡 提示：关注公众号获取解锁码</div>
  </div>
</div>
'''

JS_START = '''
<script>
// ============ STATE ============
const UNLOCK_CODE = 'NIGHTSCHOOL2026';
const DEEPSEEK_API_KEY = '';  // Set via localStorage
let currentView = 'home';
let currentSubject = '';
let currentGrade = 7;
let currentSectionId = '';
let currentQuizIdx = 0;
let quizAnswers = {};
let isUnlocked = localStorage.getItem('bioChemUnlocked') === 'true';
let chatHistory = [];

// ============ SUBJECTS CONFIG ============
const SUBJECTS = ''' + json.dumps(SUBJECTS, ensure_ascii=False) + ''';

// ============ ALL DATA (embedded) ============
const ALL_DATA = {};
'''

# Embed all data
for subj_id, items in all_data.items():
    JS_START += f'ALL_DATA["{subj_id}"] = {json.dumps(items, ensure_ascii=False)};\n'

JS_START += '''
// ============ RESOURCE LIBRARY ============
let resourceLibrary = null;

// ============ INIT ============
document.addEventListener('DOMContentLoaded', () => {
  renderCourseCards();
  loadResourceLibrary();
  
  // Handle hash
  const hash = window.location.hash.replace('#', '');
  if (hash) {
    const parts = hash.split('/');
    if (parts[0] === 'syllabus' && parts[1]) {
      currentSubject = parts[1];
      currentGrade = parseInt(parts[2]) || SUBJECTS[currentSubject]?.grades[0] || 7;
      navigateTo('syllabus', currentSubject);
    } else if (parts[0] === 'learning' && parts[1]) {
      currentSubject = parts[1];
      currentSectionId = parts[2] || '';
      navigateTo('learning', currentSubject);
    }
  }
  
  // Restore last subject
  const lastSub = localStorage.getItem('bioChemLastSubject');
  if (lastSub && SUBJECTS[lastSub]) currentSubject = lastSub;
  
  // Load API key
  const savedKey = localStorage.getItem('deepseekApiKey');
  if (savedKey) DEEPSEEK_API_KEY_PROP = savedKey;
});

// ============ API KEY MANAGEMENT ============
let DEEPSEEK_API_KEY_PROP = DEEPSEEK_API_KEY;

function setApiKey(key) {
  DEEPSEEK_API_KEY_PROP = key;
  localStorage.setItem('deepseekApiKey', key);
}

function getApiKey() {
  return DEEPSEEK_API_KEY_PROP || localStorage.getItem('deepseekApiKey') || '';
}

// ============ NAVIGATION ============
function navigateTo(view, param) {
  currentView = view;
  if (param && SUBJECTS[param]) currentSubject = param;
  
  // Update hash
  let hash = '';
  if (view === 'syllabus') hash = `syllabus/${currentSubject}/${currentGrade}`;
  else if (view === 'learning') hash = `learning/${currentSubject}/${currentSectionId}`;
  if (hash && window.location.hash !== '#' + hash) {
    history.pushState(null, '', '#' + hash);
  }
  
  // Show/hide views
  document.querySelectorAll('.view').forEach(v => v.classList.remove('active'));
  const viewMap = { home: 'view-home', syllabus: 'view-syllabus', learning: 'view-learning' };
  const el = document.getElementById(viewMap[view]);
  if (el) el.classList.add('active');
  
  // Floating bar
  const fb = document.getElementById('floatingBar');
  fb.style.display = view === 'learning' ? 'flex' : 'none';
  
  // Render
  if (view === 'syllabus') renderSyllabus();
  if (view === 'learning') renderLearning();
  
  window.scrollTo({ top: 0, behavior: 'smooth' });
}

// ============ HOME: COURSE CARDS ============
function renderCourseCards() {
  const grid = document.getElementById('courseGrid');
  grid.innerHTML = Object.entries(SUBJECTS).map(([id, s]) => {
    const grades = s.grades.map(g => g + '年级').join('·');
    return `<div class="course-card" style="--cc-accent:${s.color}" onclick="openGradeModal('${id}')">
      <span class="cc-icon">${s.icon}</span>
      <div class="cc-name">${s.name}</div>
      <div class="cc-grade">${grades}</div>
      <div class="cc-desc">${s.emoji} 点击选择年级开始学习</div>
    </div>`;
  }).join('');
}

// ============ GRADE MODAL ============
function openGradeModal(subjId) {
  const s = SUBJECTS[subjId];
  document.getElementById('gmIcon').textContent = s.icon;
  document.getElementById('gmTitle').textContent = s.name;
  document.getElementById('gmSubtitle').textContent = '请选择年级开始学习';
  
  const gradesDiv = document.getElementById('gmGrades');
  gradesDiv.innerHTML = s.grades.map(g => 
    `<button class="grade-btn${g===s.grades[0]?' selected':''}" data-grade="${g}" onclick="selectGrade(this,${g})">${g}年级</button>`
  ).join('');
  
  currentSubject = subjId;
  currentGrade = s.grades[0];
  
  document.getElementById('gradeModal').style.display = 'flex';
}

function selectGrade(btn, grade) {
  document.querySelectorAll('#gmGrades .grade-btn').forEach(b => b.classList.remove('selected'));
  btn.classList.add('selected');
  currentGrade = grade;
}

function closeGradeModal() {
  document.getElementById('gradeModal').style.display = 'none';
}

function confirmGrade() {
  closeGradeModal();
  navigateTo('syllabus', currentSubject);
}

// ============ SYLLABUS (CHAPTER OUTLINE) ============
function renderSyllabus() {
  const s = SUBJECTS[currentSubject];
  if (!s) return;
  
  document.getElementById('syIcon').textContent = s.icon;
  document.getElementById('syTitle').textContent = s.name + ' · ' + currentGrade + '年级';
  document.getElementById('sySubtitle').textContent = '人教版 · 2024版';
  document.getElementById('syBreadcrumb').innerHTML = 
    `<span onclick="navigateTo('home')" style="cursor:pointer;color:var(--blue-500)">首页</span> / <span class="current">${s.name} · ${currentGrade}年级</span>`;
  
  // Group by unit
  const items = (ALL_DATA[currentSubject] || []);
  const units = {};
  items.forEach(item => {
    const unit = item.unit || '其他';
    if (!units[unit]) units[unit] = { chapters: {} };
    const ch = item.chapter || '未分类';
    if (!units[unit].chapters[ch]) units[unit].chapters[ch] = [];
    units[unit].chapters[ch].push(item);
  });
  
  let html = '';
  let unitIdx = 0;
  Object.entries(units).forEach(([unitName, unitData]) => {
    unitIdx++;
    html += `<div style="margin-bottom:20px">
      <div style="font-size:.95rem;font-weight:700;color:var(--gray-700);margin-bottom:10px;display:flex;align-items:center;gap:8px">
        <span style="width:28px;height:28px;border-radius:8px;background:var(--blue-100);color:var(--blue-700);display:flex;align-items:center;justify-content:center;font-size:.75rem;font-weight:700">${unitIdx}</span>
        ${unitName}
      </div>`;
    
    Object.entries(unitData.chapters).forEach(([chName, sections]) => {
      const chId = 'ch-' + unitIdx + '-' + chName.replace(/[^a-zA-Z0-9\\u4e00-\\u9fff]/g,'');
      html += `<div class="chapter-card" id="${chId}">
        <div class="chapter-header" onclick="toggleChapter('${chId}')">
          <div class="ch-left">
            <div class="ch-num">${chName.substring(0,4)}</div>
            <span class="ch-title">${chName.length > 20 ? chName.substring(0,20)+'...' : chName}</span>
            <span class="ch-count">${sections.length}节</span>
          </div>
          <span class="ch-arrow">▼</span>
        </div>
        <div class="chapter-body">`;
      
      sections.forEach(sec => {
        const quizCount = sec.quiz ? sec.quiz.length : 0;
        const freeLabel = sec.free ? '🆓' : (isUnlocked ? '✅' : '🔒');
        html += `<div class="section-item" onclick="openSection('${sec.id}')">
          <span class="si-dot"></span>
          <span class="si-name">${sec.section}</span>
          <span class="si-page">${sec.page||''}</span>
          ${quizCount > 0 ? `<span class="si-quiz">${quizCount}题</span>` : ''}
        </div>`;
      });
      
      html += `</div></div>`;
    });
    html += '</div>';
  });
  
  document.getElementById('chapterTree').innerHTML = html || '<p style="text-align:center;color:var(--gray-400);padding:40px">暂无数据，请稍后重试</p>';
}

function toggleChapter(chId) {
  document.getElementById(chId).classList.toggle('open');
}

function openSection(sectionId) {
  // Check if locked
  const allItems = ALL_DATA[currentSubject] || [];
  const item = allItems.find(d => d.id === sectionId);
  if (item && !item.free && !isUnlocked) {
    showUnlockModal();
    return;
  }
  currentSectionId = sectionId;
  navigateTo('learning', currentSubject);
}

// ============ LEARNING PAGE ============
function renderLearning() {
  const s = SUBJECTS[currentSubject];
  const items = ALL_DATA[currentSubject] || [];
  const currentItem = items.find(d => d.id === currentSectionId);
  if (!currentItem && items.length > 0) {
    currentSectionId = items[0].id;
  }
  const item = items.find(d => d.id === currentSectionId);
  if (!item) {
    document.getElementById('lpContent').innerHTML = '<p style="text-align:center;padding:40px;color:var(--gray-400)">请选择一个小节开始学习</p>';
    return;
  }
  
  // Breadcrumb
  document.getElementById('lpBreadcrumb').innerHTML = 
    `<span onclick="navigateTo('syllabus','${currentSubject}')" style="cursor:pointer;color:var(--blue-500)">${s.name}</span> / <span class="current">${item.section}</span>`;
  
  // Unlock badge
  const badge = document.getElementById('unlockBadge');
  badge.style.display = 'inline-block';
  badge.className = 'unlock-badge ' + (item.free || isUnlocked ? 'free' : 'locked');
  badge.textContent = item.free || isUnlocked ? '免费' : '需解锁';
  
  // Render sidebar
  renderSidebar(items, item);
  
  // Render content
  renderContent(item);
  
  // Update AI assistant
  updateAIAssistant();
}

function renderSidebar(items, currentItem) {
  const units = {};
  items.forEach(d => {
    if (!units[d.unit]) units[d.unit] = { chapters: {} };
    const ch = d.chapter || '未分类';
    if (!units[d.unit].chapters[ch]) units[d.unit].chapters[ch] = [];
    units[d.unit].chapters[ch].push(d);
  });
  
  let html = '<div class="sidebar-title">📑 课程目录</div>';
  Object.entries(units).forEach(([unitName, unitData]) => {
    html += `<div style="padding:4px 16px;font-size:.7rem;font-weight:700;color:var(--gray-400);text-transform:uppercase;margin-top:4px">${unitName}</div>`;
    Object.entries(unitData.chapters).forEach(([chName, sections]) => {
      html += `<div class="sidebar-chapter">
        <div class="sc-header"><span class="sc-dot"></span>${chName.substring(0,15)}</div>
        <div class="sc-sections">`;
      sections.forEach(sec => {
        const active = sec.id === currentItem.id;
        html += `<div class="sc-item${active?' active':''}" onclick="selectSection('${sec.id}')">
          <span>${sec.section.substring(0,12)}</span>
        </div>`;
      });
      html += '</div></div>';
    });
  });
  document.getElementById('lpSidebar').innerHTML = html;
}

function selectSection(sectionId) {
  const items = ALL_DATA[currentSubject] || [];
  const item = items.find(d => d.id === sectionId);
  if (item && !item.free && !isUnlocked) {
    showUnlockModal();
    return;
  }
  currentSectionId = sectionId;
  navigateTo('learning', currentSubject);
}

function renderContent(item) {
  const isGeo = item.category === 'geo';
  const isChem = item.category === 'chem';
  
  let html = '';
  
  // Header
  html += `<div class="content-header">
    <div class="ch-section-num">${item.unit || ''} · ${item.chapter || ''}</div>
    <h2>${item.section}</h2>
    <div class="ch-page">📄 ${item.page || ''}</div>`;
  
  if (item.examPoints && item.examPoints.length > 0) {
    html += '<div class="ch-exam-tags">';
    item.examPoints.forEach(ep => {
      html += `<span class="exam-tag ${ep.includes('中考')?'hot':'normal'}">${ep}</span>`;
    });
    html += '</div>';
  }
  html += '</div>';
  
  // Scene / Case box
  const sceneText = isGeo ? item.gameScene : (item.nightMarketCase || '');
  if (sceneText) {
    html += `<div class="scene-box">
      <div class="scene-label">${isGeo ? '🎒 长征场景' : '🏮 生活案例'}</div>
      <div class="scene-text">${sceneText}</div>
    </div>`;
  }
  
  // Knowledge points
  html += `<div class="knowledge-section">
    <h3><span class="icon">📖</span> 核心知识点</h3>
    <ul>`;
  (item.keypoints || []).forEach(kp => {
    html += `<li>${kp}</li>`;
  });
  html += '</ul></div>';
  
  // Textbook columns
  if (item.textbookColumns && item.textbookColumns.length > 0) {
    html += `<div class="col-box">
      <h4>📚 教材栏目</h4>
      <ul>`;
    item.textbookColumns.forEach(col => {
      html += `<li>${col}</li>`;
    });
    html += '</ul></div>';
  }
  
  // Quiz section
  if (item.quiz && item.quiz.length > 0) {
    html += renderQuizSection(item);
  }
  
  // Game hint
  if (item.gameType) {
    html += `<div class="knowledge-section">
      <h3><span class="icon">🎮</span> 互动游戏</h3>
      <p style="font-size:.82rem;color:var(--gray-500)">${item.gameDesign || '点击进入互动学习游戏'}</p>
      <button class="btn btn-primary" style="margin-top:10px" onclick="launchGame('${item.gameType}','${item.id}')">🎮 开始游戏</button>
    </div>`;
  }
  
  document.getElementById('lpContent').innerHTML = html;
  
  // Reset quiz state
  currentQuizIdx = 0;
  quizAnswers = {};
}

function renderQuizSection(item) {
  const quiz = item.quiz || [];
  currentQuizIdx = 0;
  quizAnswers = {};
  
  let html = `<div class="quiz-section">
    <h3><span class="icon">📝</span> 随堂测试 <span class="quiz-progress" id="quizProgress">1/${quiz.length}</span></h3>
    <div id="quizContainer"></div>
    <div class="quiz-nav">
      <button class="qn-prev" onclick="prevQuiz()" id="quizPrev" disabled>← 上一题</button>
      <button class="qn-next" onclick="nextQuiz()" id="quizNext">下一题 →</button>
      <button class="qn-restart" onclick="restartQuiz()">🔄 重做</button>
    </div>
    <div id="quizScore" style="text-align:center;margin-top:8px;font-size:.8rem;color:var(--gray-500);display:none"></div>
  </div>`;
  
  // Defer quiz rendering
  setTimeout(() => renderCurrentQuiz(quiz), 100);
  window._currentQuiz = quiz;
  
  return html;
}

function renderCurrentQuiz(quiz) {
  if (!quiz) quiz = window._currentQuiz;
  if (!quiz || quiz.length === 0) return;
  
  const q = quiz[currentQuizIdx];
  const container = document.getElementById('quizContainer');
  if (!container) return;
  
  document.getElementById('quizProgress').textContent = `${currentQuizIdx+1}/${quiz.length}`;
  document.getElementById('quizPrev').disabled = currentQuizIdx === 0;
  
  const isLast = currentQuizIdx === quiz.length - 1;
  const allDone = Object.keys(quizAnswers).length === quiz.length;
  document.getElementById('quizNext').textContent = isLast ? (allDone ? '查看成绩' : '完成') : '下一题 →';
  
  if (q.type === 'mc') {
    let optionsHtml = q.options.map((opt, i) => {
      let cls = 'q-opt';
      if (quizAnswers[currentQuizIdx] !== undefined) {
        if (i === q.answer) cls += ' correct';
        else if (i === quizAnswers[currentQuizIdx] && i !== q.answer) cls += ' wrong';
      } else if (quizAnswers[currentQuizIdx] === i) {
        cls += ' selected';
      }
      const disabled = quizAnswers[currentQuizIdx] !== undefined ? 'disabled' : '';
      return `<div class="${cls}" onclick="${disabled ? '' : `answerQuiz(${currentQuizIdx},${i},${q.answer})`}" ${disabled}>${String.fromCharCode(65+i)}. ${opt}</div>`;
    }).join('');
    
    container.innerHTML = `<div class="quiz-card">
      <div class="q-text">${currentQuizIdx+1}. ${q.q}</div>
      <div class="q-options">${optionsHtml}</div>
      <div class="q-feedback${quizAnswers[currentQuizIdx]!==undefined?' show':''}" id="feedback${currentQuizIdx}">
        ${quizAnswers[currentQuizIdx]!==undefined ? (quizAnswers[currentQuizIdx]===q.answer ? '✅ 正确！' : '❌ 正确答案是 ' + String.fromCharCode(65+q.answer)) + '<br>' + (q.explanation||'') : ''}
      </div>
    </div>`;
  } else if (q.type === 'fill') {
    const answered = quizAnswers[currentQuizIdx] !== undefined;
    container.innerHTML = `<div class="quiz-card">
      <div class="q-text">${currentQuizIdx+1}. ${q.q}</div>
      <input class="ai-input" id="fillAnswer" placeholder="请输入答案..." style="width:100%;margin-top:8px" ${answered?'disabled':''} onkeydown="if(event.key==='Enter')submitFill(${currentQuizIdx},'${(q.answer||'').replace(/'/g,"\\'")}')">
      ${answered ? `<div style="margin-top:8px;font-size:.8rem;color:${quizAnswers[currentQuizIdx]===q.answer?'#10b981':'#ef4444'}">${quizAnswers[currentQuizIdx]===q.answer ? '✅ 正确！' : '❌ 正确答案：' + q.answer}</div>` : ''}
      <div class="q-feedback${answered?' show':''}" id="feedback${currentQuizIdx}">${q.explanation||''}</div>
    </div>`;
  }
}

function answerQuiz(idx, selected, correct) {
  quizAnswers[idx] = selected;
  renderCurrentQuiz();
  if (selected === correct) {
    totalScore = (totalScore || 0) + 1;
  }
}

function submitFill(idx, correct) {
  const input = document.getElementById('fillAnswer');
  if (!input) return;
  const val = input.value.trim();
  quizAnswers[idx] = val;
  if (val === correct) totalScore = (totalScore || 0) + 1;
  renderCurrentQuiz();
}

function prevQuiz() {
  if (currentQuizIdx > 0) {
    currentQuizIdx--;
    renderCurrentQuiz();
  }
}

function nextQuiz() {
  const quiz = window._currentQuiz;
  if (!quiz) return;
  
  if (quizAnswers[currentQuizIdx] === undefined) {
    // Answer required
    return;
  }
  
  if (currentQuizIdx < quiz.length - 1) {
    currentQuizIdx++;
    renderCurrentQuiz();
  } else {
    // Show score
    const correct = Object.entries(quizAnswers).filter(([k,v]) => {
      const q = quiz[parseInt(k)];
      return q.type === 'mc' ? v === q.answer : String(v).trim() === String(q.answer).trim();
    }).length;
    document.getElementById('quizScore').style.display = 'block';
    document.getElementById('quizScore').innerHTML = `🎯 成绩：${correct}/${quiz.length} (${Math.round(correct/quiz.length*100)}分)`;
  }
}

function restartQuiz() {
  quizAnswers = {};
  currentQuizIdx = 0;
  document.getElementById('quizScore').style.display = 'none';
  renderCurrentQuiz();
}

function launchGame(gameType, itemId) {
  // TODO: Implement game launching
  alert('🎮 游戏功能开发中...\\n游戏类型：' + gameType);
}

// ============ AI ASSISTANT ============
function updateAIAssistant() {
  const s = SUBJECTS[currentSubject];
  const items = ALL_DATA[currentSubject] || [];
  const item = items.find(d => d.id === currentSectionId);
  
  document.getElementById('aiAvatar').textContent = s ? s.icon : '🤖';
  document.getElementById('aiName').textContent = s ? s.name + '助教' : 'AI助教';
  document.getElementById('aiRole').textContent = item ? '当前：' + item.section : '选一个知识点开始吧';
  
  document.getElementById('aiGreeting').textContent = item 
    ? '👋 关于「' + item.section + '」有什么问题？我可以用生活中的例子帮你理解！'
    : '👋 你好！我是AI学习助手，选一个知识点开始学习吧～';
}

async function sendChat() {
  const input = document.getElementById('chatInput');
  const body = document.getElementById('chatBody');
  const msg = input.value.trim();
  if (!msg) return;
  
  input.value = '';
  
  // Add user message
  body.innerHTML += `<div class="ai-msg user">${escapeHtml(msg)}</div>`;
  
  // Add thinking
  const thinkId = 'think-' + Date.now();
  body.innerHTML += `<div class="ai-msg system" id="${thinkId}">思考中...</div>`;
  body.scrollTop = body.scrollHeight;
  
  const apiKey = getApiKey();
  
  if (!apiKey) {
    document.getElementById(thinkId).textContent = '⚠️ 请先设置 DeepSeek API Key。点击下方输入框旁的⚙️按钮设置。';
    return;
  }
  
  try {
    const items = ALL_DATA[currentSubject] || [];
    const item = items.find(d => d.id === currentSectionId);
    const systemPrompt = item 
      ? `你是初中${SUBJECTS[currentSubject]?.name||''}学科AI助教。当前学生在学习「${item.section}」，核心知识点：${(item.keypoints||[]).join('；')}。请用生活化的例子解释，语言简洁，200字以内。`
      : '你是初中全科AI学习助教，请用生活化的例子解释学生的问题，语言简洁，200字以内。';
    
    const resp = await fetch('https://api.deepseek.com/v1/chat/completions', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + apiKey
      },
      body: JSON.stringify({
        model: 'deepseek-chat',
        messages: [
          { role: 'system', content: systemPrompt },
          { role: 'user', content: msg }
        ],
        max_tokens: 500,
        temperature: 0.7
      })
    });
    
    const data = await resp.json();
    document.getElementById(thinkId).remove();
    
    if (data.choices && data.choices[0]) {
      body.innerHTML += `<div class="ai-msg assistant">${escapeHtml(data.choices[0].message.content)}</div>`;
    } else {
      body.innerHTML += `<div class="ai-msg system">❌ API返回异常：${escapeHtml(JSON.stringify(data))}</div>`;
    }
  } catch(e) {
    document.getElementById(thinkId).textContent = '❌ 网络错误：' + e.message + '。请检查API Key和网络连接。';
  }
  
  body.scrollTop = body.scrollHeight;
}

function escapeHtml(str) {
  const div = document.createElement('div');
  div.textContent = str;
  return div.innerHTML;
}

// ============ UNLOCK ============
function showUnlockModal() {
  document.getElementById('unlockModal').style.display = 'flex';
  document.getElementById('unlockError').style.display = 'none';
}

function doUnlock() {
  const code = document.getElementById('unlockCode').value.trim();
  if (code === UNLOCK_CODE) {
    isUnlocked = true;
    localStorage.setItem('bioChemUnlocked', 'true');
    document.getElementById('unlockModal').style.display = 'none';
    // Refresh current view
    if (currentView === 'syllabus') renderSyllabus();
    if (currentView === 'learning') renderLearning();
  } else {
    document.getElementById('unlockError').style.display = 'block';
  }
}

// Close unlock modal on overlay click
document.addEventListener('click', function(e) {
  if (e.target.id === 'unlockModal') {
    document.getElementById('unlockModal').style.display = 'none';
  }
});

// ============ RESOURCE LIBRARY ============
async function loadResourceLibrary() {
  try {
    const resp = await fetch('/api/library');
    resourceLibrary = await resp.json();
    renderResourceGrid();
  } catch(e) {
    console.log('Resource library not loaded:', e.message);
  }
}

function renderResourceGrid() {
  if (!resourceLibrary) return;
  const grid = document.getElementById('resourceGrid');
  
  let html = '';
  
  // Standards first
  if (resourceLibrary.standards) {
    html += `<div class="res-subject">
      <div class="rs-title">📋 课程标准 (${resourceLibrary.standards.length}份)</div>
      <div class="rs-list">`;
    resourceLibrary.standards.forEach(std => {
      html += `<div class="res-item">
        <span>📘</span>
        <span style="flex:1">${std.name}</span>
        <a href="pdf/${std.file}" target="_blank" style="color:var(--blue-500);text-decoration:none;font-size:.7rem">查看</a>
      </div>`;
    });
    html += '</div></div>';
  }
  
  // Subjects
  if (resourceLibrary.subjects) {
    Object.entries(resourceLibrary.subjects).forEach(([subjId, subj]) => {
      if (!subj.textbooks || subj.textbooks.length === 0) return;
      html += `<div class="res-subject">
        <div class="rs-title">${subj.icon||'📚'} ${subj.name} (${subj.textbooks.length}册)</div>
        <div class="rs-list">`;
      subj.textbooks.forEach(tb => {
        html += `<div class="res-item">
          <span class="ri-grade">${tb.grade||''}</span>
          <span style="flex:1">${tb.name}</span>
          <a href="pdf/${tb.file}" target="_blank" style="color:var(--blue-500);text-decoration:none;font-size:.7rem">查看</a>
        </div>`;
      });
      html += '</div></div>';
    });
  }
  
  grid.innerHTML = html;
}

// ============ MOBILE TOGGLE ============
function toggleSidebar() {
  document.getElementById('lpSidebar').classList.toggle('collapsed');
}
function toggleAIPanel() {
  document.getElementById('aiPanel').classList.toggle('collapsed');
}

// ============ SETTINGS ============
function showSettings() {
  const key = getApiKey();
  const newKey = prompt('请输入 DeepSeek API Key（留空取消）：', key ? '●●●●●●●●' : '');
  if (newKey && newKey !== '●●●●●●●●') {
    setApiKey(newKey);
    alert('✅ API Key 已保存！');
  }
}

// Add settings to chat panel
setTimeout(() => {
  const panel = document.getElementById('aiPanel');
  if (panel) {
    const header = panel.querySelector('.ai-header');
    if (header) {
      const btn = document.createElement('button');
      btn.textContent = '⚙️';
      btn.style.cssText = 'margin-left:auto;background:none;border:none;cursor:pointer;font-size:1rem;padding:4px 8px;border-radius:6px;color:var(--gray-400)';
      btn.title = '设置 API Key';
      btn.onclick = showSettings;
      header.appendChild(btn);
    }
  }
}, 500);

console.log('智慧学堂 v6.0 — 蓝色系 · 年级选择 · 章节学习 · AI辅导 · DeepSeek API');
</script>
'''

HTML_FOOT = '''
</body>
</html>
'''

# ============ BUILD ============
def build():
    full_html = HTML_HEAD + VIEWS_HTML + JS_START + HTML_FOOT
    with open(OUTPUT, 'w', encoding='utf-8') as f:
        f.write(full_html)
    size_kb = len(full_html) / 1024
    print(f'✅ Built {OUTPUT} ({size_kb:.0f} KB)')

if __name__ == '__main__':
    build()
