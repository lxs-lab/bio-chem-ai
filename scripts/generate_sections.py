"""
生成所有小节的独立HTML页面
每小节包括：教学目标、情境导入、知识探究、重难点解析、测验、项目链接、思维导图、教材查看
"""
import json, os, shutil, re

DATA_DIR = r'E:\Applications in E\workBuddy\2026~AI课程\bio-chem-ai\data'
OUTPUT_DIR = r'E:\Applications in E\workBuddy\2026~AI课程\bio-chem-ai\sections'
CSS_FILE = 'section.css'
JS_FILE = 'section.js'

# Subject metadata
SUBJECTS_META = {
    "bio": {"name": "生物学", "icon": "🧬", "color": "#10b981", "grade": 7, "en": "Biology"},
    "chem": {"name": "化学", "icon": "⚗️", "color": "#8b5cf6", "grade": 9, "en": "Chemistry"},
    "geo": {"name": "地理", "icon": "🗺️", "color": "#f59e0b", "grade": 7, "en": "Geography"},
    "phy": {"name": "物理", "icon": "⚡", "color": "#ef4444", "grade": 8, "en": "Physics"},
    "math": {"name": "数学", "icon": "📐", "color": "#3b82f6", "grade": 7, "en": "Math"},
    "cn": {"name": "语文", "icon": "📖", "color": "#ec4899", "grade": 7, "en": "Chinese"},
    "eng": {"name": "英语", "icon": "🔤", "color": "#06b6d4", "grade": 7, "en": "English"},
    "hist": {"name": "历史", "icon": "🏛️", "color": "#78716c", "grade": 7, "en": "History"},
    "pol": {"name": "道德与法治", "icon": "⚖️", "color": "#14b8a6", "grade": 7, "en": "Politics"},
}

# Load teaching methods
from teaching_methods import SUBJECT_METHODS, SUBJECT_PROJECTS, TEACHING_PRINCIPLES

def load_data(subject_key):
    """Load subject data file"""
    path = os.path.join(DATA_DIR, f'{subject_key}_data.json')
    if not os.path.exists(path):
        print(f'  WARN: {path} not found')
        return []
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

def generate_context_import(subject_key, item):
    """Generate situational introduction based on subject and section"""
    subject = SUBJECTS_META.get(subject_key, {})
    section = item.get('section', '')
    
    # Try to find night market / game scene
    case_text = item.get('nightMarketCase', '') or item.get('gameScene', '') or item.get('gameDesign', '')
    
    if case_text:
        return f'<div class="context-box"><span class="context-icon">💡</span><div class="context-text">{case_text}</div></div>'
    
    # Generic introductions based on subject
    intros = {
        "bio": f'<div class="context-box"><span class="context-icon">💡</span><div class="context-text">同学们，你有没有想过——为什么切开的苹果放久了会变色？为什么小猫小狗需要吃东西才能长大？今天我们就来探索<span class="highlight">「{section}」</span>，从生活中的现象出发，揭开生命科学的奥秘。</div></div>',
        "chem": f'<div class="context-box"><span class="context-icon">💡</span><div class="context-text">化学其实就在我们身边！炒菜时的油烟、喝汽水时的气泡、铁门生锈……这些现象背后都隐藏着化学原理。今天我们来学习<span class="highlight">「{section}」</span>，看看物质世界发生了怎样的变化。</div></div>',
        "geo": f'<div class="context-box"><span class="context-icon">💡</span><div class="context-text">如果我给你一张没有方向标记的地图，你能找到目的地吗？地理学帮助我们理解世界的空间格局。今天我们来学习<span class="highlight">「{section}」</span>，掌握读懂世界的方法。</div></div>',
        "phy": f'<div class="context-box"><span class="context-icon">💡</span><div class="context-text">坐车急刹车时身体会往前倾，为什么？筷子插在水里看起来是弯的，为什么？物理就是从这些生活现象中提炼出的科学道理。今天我们来探究<span class="highlight">「{section}」</span>。</div></div>',
        "math": f'<div class="context-box"><span class="context-icon">💡</span><div class="context-text">数学不是冰冷的公式，而是解决问题的工具。从购物算钱到规划路线，数学无处不在。今天我们来学习<span class="highlight">「{section}」</span>，掌握一个重要的数学工具。</div></div>',
        "cn": f'<div class="context-box"><span class="context-icon">💡</span><div class="context-text">文字是思想的翅膀，好的文章能带我们穿越时空、感受别样人生。今天我们一起走进<span class="highlight">「{section}」</span>，品味语言的魅力。</div></div>',
        "eng": f'<div class="context-box"><span class="context-icon">💡</span><div class="context-text">Language is the key to the world. 语言是打开世界的钥匙。今天我们来学习<span class="highlight">「{section}」</span>，掌握用英语交流的新技能。</div></div>',
        "hist": f'<div class="context-box"><span class="context-icon">💡</span><div class="context-text">站在今天回望过去，每一段历史都像一部精彩的电影。今天我们来了解<span class="highlight">「{section}」</span>，看看千百年前的人们是如何生活的。</div></div>',
        "pol": f'<div class="context-box"><span class="context-icon">💡</span><div class="context-text">道德与法治不只是课本上的知识，它和我们每天的成长息息相关。今天我们来探讨<span class="highlight">「{section}」</span>，思考如何更好地成长。</div></div>',
    }
    return intros.get(subject_key, f'<div class="context-box"><span class="context-icon">💡</span><div class="context-text">今天我们来学习<span class="highlight">「{section}」</span>，这是一个重要的知识点。</div></div>')

def generate_learning_objectives(subject_key, item):
    """Generate three-dimensional learning objectives"""
    keypoints = item.get('keypoints', [])
    exam_points = item.get('examPoints', [])
    section = item.get('section', '')
    
    kp_html = '\n'.join(f'<li>{kp}</li>' for kp in keypoints)
    ep_html = '\n'.join(f'<li>{ep}</li>' for ep in exam_points) if exam_points else '<li>理解本节核心内容</li>'
    
    return f'''<div class="objectives-grid">
    <div class="obj-card">
        <div class="obj-title">📚 知识目标</div>
        <ul>{kp_html}</ul>
    </div>
    <div class="obj-card">
        <div class="obj-title">🔬 能力目标</div>
        <ul><li>能运用所学知识分析和解释相关现象</li><li>掌握本节相关的科学方法和探究技能</li><li>培养观察、分析和归纳的能力</li></ul>
    </div>
    <div class="obj-card">
        <div class="obj-title">💡 素养目标</div>
        <ul>{ep_html}</ul>
    </div>
</div>'''

def generate_key_concepts(subject_key, item):
    """Generate key concepts and difficult points section"""
    keypoints = item.get('keypoints', [])
    section = item.get('section', '')
    
    kp_cards = '\n'.join(f'''
    <div class="concept-card">
        <span class="concept-num">{i+1}</span>
        <div class="concept-body">
            <div class="concept-title">{kp}</div>
            <div class="concept-detail">{generate_concept_detail(subject_key, kp)}</div>
        </div>
    </div>''' for i, kp in enumerate(keypoints))
    
    return f'''
<div class="key-concepts">
    <h3>🔑 核心知识点</h3>
    <div class="concept-cards">{kp_cards}</div>
</div>'''

def generate_concept_detail(subject_key, keypoint):
    """Generate detailed explanation for each key point"""
    # Provide richer explanations based on topic
    if '观察' in keypoint:
        return '🔍 科学观察是有目的、有计划的感知活动。观察不是"随便看看"，而是要带着问题、按一定顺序、如实记录。观察时要调动多种感官——不仅用眼看，还可以用耳听、用鼻闻、用手触。记录观察结果要客观真实，不能加入自己的想象。'
    elif '生物' in keypoint or '非生物' in keypoint:
        return '🌿 生物的共同特征：需要营养、能呼吸、能排出废物、能对外界刺激作出反应、能生长和繁殖、有遗传和变异、由细胞构成（病毒除外）。记住这些特征，就能判断任何物体是不是生物。比如：机器人能"动"，但不具备生命活动，不是生物。'
    elif '显微镜' in keypoint:
        return '🔬 显微镜是生物学研究的基本工具。目镜和物镜的乘积等于放大倍数。使用时注意：低倍镜找目标，高倍镜看细节；对光时光圈要对准通光孔；调焦时先用粗准焦螺旋，再用细准焦螺旋。'
    elif '细胞' in keypoint:
        return '🧫 细胞是生物体结构和功能的基本单位（病毒除外）。植物细胞有细胞壁、液泡和叶绿体，动物细胞没有。细胞膜控制物质进出，细胞核含有遗传物质，细胞质是生命活动的场所。记住"膜质核"→细胞的核心结构。'
    elif '化学' in keypoint and '变化' in keypoint:
        return '⚗️ 化学变化的本质是有新物质生成，常伴随发光、放热、颜色变化、生成气体或沉淀。物理变化没有新物质生成，只是形态改变。判断标准：是否有新物质生成。'
    elif '方向' in keypoint or '地图' in keypoint:
        return '🗺️ 地图的方向判断方法：①一般地图"上北下南左西右东"；②有指向标时按指向标定向；③有经纬网时经线指南北、纬线指东西；④野外可用太阳、北极星、树冠和年轮辅助定向。'
    elif '速度' in keypoint or '运动' in keypoint:
        return '⚡ 速度是描述物体运动快慢的物理量。公式 v = s/t（速度=路程÷时间），单位 m/s 或 km/h（1m/s=3.6km/h）。匀速直线运动是最简单的运动，实际生活中多为变速运动，用平均速度近似描述。'
    elif '正数' in keypoint or '负数' in keypoint or '有理数' in keypoint:
        return '🔢 正数和负数是表示相反意义量的工具。0是正数和负数的分界，既不是正数也不是负数。比如+5℃表示零上5度，-3℃表示零下3度，收入记为正，支出记为负。'
    elif '中' in keypoint and ('学' in keypoint or '生活' in keypoint):
        return '🏫 初中是人生的重要阶段。新课程、新同学、新环境带来了新的机遇和挑战。要以积极的心态面对变化，珍视当下的每一天。凡事预则立，不预则废——做好规划是成功的第一步。'
    else:
        return f'💡 这是理解本节内容的关键知识点，请结合教材和课堂讲解深入学习。尝试用生活中的例子来帮助理解和记忆。'

def generate_mind_map_section(item):
    """Generate a simple text-based mind map"""
    keypoints = item.get('keypoints', [])
    section = item.get('section', '')
    
    nodes = '\n'.join(f'<div class="mm-node">{kp[:40]}</div>' for kp in keypoints[:6])
    
    return f'''
<div class="mind-map">
    <h3>🧠 思维导图</h3>
    <div class="mind-map-container">
        <div class="mm-center">{section}</div>
        <div class="mm-branches">{nodes}</div>
    </div>
</div>'''

def generate_quiz_section(item):
    """Generate interactive quiz section"""
    quiz = item.get('quiz', [])
    if not quiz:
        return ''
    
    quiz_items = ''
    for i, q in enumerate(quiz):
        q_type = q.get('type', 'mc')
        if q_type == 'mc':
            options_html = '\n'.join(
                f'<label class="quiz-opt" data-q="{i}" data-a="{j}"><input type="radio" name="q{i}" onchange="checkAnswer({i},{j},{q["answer"]})"> {chr(65+j)}. {q["options"][j]}</label>'
                for j in range(len(q.get('options', [])))
            )
            quiz_items += f'''
            <div class="quiz-item" id="quiz{i}">
                <div class="quiz-q">{i+1}. {q["q"]}</div>
                <div class="quiz-options">{options_html}</div>
                <div class="quiz-feedback" id="fb{i}"></div>
            </div>'''
        elif q_type == 'fill':
            quiz_items += f'''
            <div class="quiz-item" id="quiz{i}">
                <div class="quiz-q">{i+1}. {q["q"]}</div>
                <input class="quiz-fill" id="fill{i}" placeholder="输入答案..." onkeydown="if(event.key==='Enter')checkFill({i},'{q.get("answer","").replace(chr(39),chr(92)+chr(39))}')">
                <button class="btn btn-sm btn-primary" onclick="checkFill({i},'{q.get("answer","").replace(chr(39),chr(92)+chr(39))}')">提交</button>
                <div class="quiz-feedback" id="fb{i}"></div>
            </div>'''
    
    return f'''
<div class="quiz-section">
    <h3>📝 随堂测试</h3>
    <div class="quiz-grid">{quiz_items}</div>
    <div class="quiz-score" id="quizScore" style="display:none"></div>
    <button class="btn btn-primary" onclick="showScore({len(quiz)})" style="margin-top:12px">📊 查看成绩</button>
    <button class="btn btn-ghost" onclick="resetQuiz()" style="margin-left:8px;margin-top:12px">🔄 重做</button>
</div>
<script>
window._quizTotal = {len(quiz)};
window._quizAnswers = {json.dumps([q.get("answer") for q in quiz])};
window._quizTypes = {json.dumps([q.get("type","mc") for q in quiz])};
</script>'''

def generate_project_link(subject_key, item):
    """Generate project-based learning connection"""
    projects = SUBJECT_PROJECTS.get(subject_key, [])
    section_id = item.get('id', '')
    
    # Find related projects
    related = []
    for proj in projects:
        if section_id in proj.get('related_sections', []):
            related.append(proj)
    
    if not related:
        # Show a generic project placeholder
        return f'''
<div class="project-link">
    <h3>🚀 项目制学习</h3>
    <div class="project-placeholder">
        <div class="pp-icon">🔧</div>
        <div class="pp-text">本知识点的项目制学习模块正在建设中</div>
        <div class="pp-hint">我们将设计融合本节重难点的真实项目任务，敬请期待！</div>
    </div>
</div>'''
    
    proj_html = '\n'.join(f'''
    <div class="project-card">
        <div class="pc-header">
            <span class="pc-icon">🎯</span>
            <span class="pc-title">项目：{proj['title']}</span>
            <span class="pc-badge">{proj['difficulty']}</span>
        </div>
        <div class="pc-question">❓ 驱动问题：{proj['driving_question']}</div>
        <div class="pc-meta">
            <span>⏱ {proj.get('duration','')}</span>
            <span>🎯 {', '.join(proj.get('skills',[])[:3])}</span>
        </div>
        <div class="pc-output">📦 产出：{proj.get('output','')}</div>
        <a href="../projects/#{proj['id']}" class="btn btn-outline">查看项目详情 →</a>
    </div>''' for proj in related)
    
    return f'''
<div class="project-link">
    <h3>🚀 项目制学习</h3>
    <div class="project-cards">{proj_html}</div>
</div>'''

def generate_extended_reading(subject_key, item):
    """Generate extended reading section"""
    section = item.get('section', '')
    subject = SUBJECTS_META.get(subject_key, {})
    
    readings = {
        "bio": [{"title": "为什么变色龙会变色？", "desc": "探索动物适应环境的奇妙能力"}],
        "chem": [{"title": "厨房里的化学实验室", "desc": "探索日常生活中的化学变化"}],
        "geo": [{"title": "世界上最难读的地图", "desc": "探索人类绘制地图的历史"}],
        "phy": [{"title": "牛顿与苹果的故事", "desc": "探索物理学史上的经典发现"}],
        "math": [{"title": "负数的历史", "desc": "从古代中国到欧洲——负数概念的发展"}],
        "cn": [{"title": "作者生平与创作背景", "desc": f"了解「{section}」的创作故事"}],
        "eng": [{"title": "Greetings Around the World", "desc": "世界各国不同的问候方式"}],
        "hist": [{"title": "考古发现中的历史", "desc": "从地下文物解读古代文明"}],
        "pol": [{"title": "名人的成长故事", "desc": "学习榜样人物的人生态度"}],
    }
    
    items = readings.get(subject_key, [{"title": "拓展阅读", "desc": "了解更多相关内容"}])
    items_html = '\n'.join(f'''
    <div class="reading-item">
        <div class="ri-title">📖 {item["title"]}</div>
        <div class="ri-desc">{item["desc"]}</div>
    </div>''' for item in items)
    
    return f'''
<div class="extended-reading">
    <h3>📖 拓展阅读</h3>
    <div class="reading-list">{items_html}</div>
</div>'''

def generate_pdf_button(item):
    """Generate PDF viewing button"""
    if not item.get('pdf_file'):
        return ''
    page = item.get('pdf_page', 1)
    return f'''
<div class="pdf-section">
    <button class="btn-pdf" onclick="openPdf()">
        📖 查看教材（{item.get("page","")}）
    </button>
</div>'''

def generate_methodology_insight(subject_key):
    """Generate teaching methodology insight sidebar"""
    methods = SUBJECT_METHODS.get(subject_key, {})
    if not methods:
        return ''
    
    approach = methods.get('learning_approach', '')
    key_methods = methods.get('key_methods', [])[:3]
    inspirations = methods.get('teaching_inspiration', [])[:2]
    
    methods_html = '\n'.join(f'<li>{m}</li>' for m in key_methods)
    insp_html = '\n'.join(f'<div class="insight-item">💬 {insp}</div>' for insp in inspirations)
    
    return f'''
<div class="method-sidebar">
    <div class="ms-title">🎓 学习思路</div>
    <div class="ms-approach">{approach}</div>
    <div class="ms-section">
        <div class="ms-label">学习方法</div>
        <ul>{methods_html}</ul>
    </div>
    <div class="ms-section">
        <div class="ms-label">名师启发</div>
        {insp_html}
    </div>
</div>'''

def generate_navigation_links(subject_key, all_items, current_item):
    """Generate prev/next navigation"""
    current_idx = next((i for i, d in enumerate(all_items) if d['id'] == current_item.get('id')), -1)
    prev_item = all_items[current_idx - 1] if current_idx > 0 else None
    next_item = all_items[current_idx + 1] if current_idx < len(all_items) - 1 else None
    
    # Build breadcrumb
    prev_link = f'<a href="./{prev_item["id"]}.html" class="nav-link">← {prev_item["section"][:15]}</a>' if prev_item else '<span class="nav-link disabled">← 已是第一节</span>'
    next_link = f'<a href="./{next_item["id"]}.html" class="nav-link">{next_item["section"][:15]} →</a>' if next_item else '<span class="nav-link disabled">已是最后一节 →</span>'
    
    subject = SUBJECTS_META.get(subject_key, {})
    
    return f'''
<div class="section-nav">
    <div class="breadcrumb">
        <a href="../">🧬 智慧学堂</a> / 
        <a href="../index.html#{subject_key}">{subject.get("icon","")} {subject.get("name","")}</a> / 
        <span>{current_item.get("unit","")}</span> / 
        <span class="bc-current">{current_item.get("section","")}</span>
    </div>
    <div class="nav-links">
        {prev_link}
        <span class="nav-pos">{current_idx + 1} / {len(all_items)}</span>
        {next_link}
    </div>
</div>'''

def generate_section_page(subject_key, item, all_items):
    """Generate complete HTML page for one section"""
    subject = SUBJECTS_META.get(subject_key, {})
    
    context_import = generate_context_import(subject_key, item)
    objectives = generate_learning_objectives(subject_key, item)
    key_concepts = generate_key_concepts(subject_key, item)
    mind_map = generate_mind_map_section(item)
    quiz = generate_quiz_section(item)
    project = generate_project_link(subject_key, item)
    reading = generate_extended_reading(subject_key, item)
    pdf_btn = generate_pdf_button(item)
    nav = generate_navigation_links(subject_key, all_items, item)
    method_sidebar = generate_methodology_insight(subject_key)
    
    # Textbook columns
    columns = item.get('textbookColumns', [])
    columns_html = ''
    if columns:
        cols = '\n'.join(f'<div class="tb-column"><span class="tb-col-icon">📋</span> {col}</div>' for col in columns)
        columns_html = f'''
<div class="textbook-columns">
    <h3>📖 教材栏目对应</h3>
    <div class="tb-col-grid">{cols}</div>
</div>'''
    
    page = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{item["section"]} - {subject["name"]} | 智慧学堂</title>
<link rel="stylesheet" href="../{CSS_FILE}">
</head>
<body>
<div class="section-page">
    {nav}
    
    <div class="section-layout">
        <main class="section-main">
            <article class="section-article">
                <header class="article-header">
                    <div class="article-meta">{item.get("unit","")} · {item.get("chapter","")}</div>
                    <h1>{item["section"]}</h1>
                    <div class="article-tags">
                        <span class="tag page-tag">📄 {item.get("page","")}</span>
                        <span class="tag {'free-tag' if item.get('free') else 'locked-tag'}">{'🆓 免费' if item.get('free') else '🔒 需解锁'}</span>
                        {pdf_btn}
                    </div>
                </header>
                
                {context_import}
                {objectives}
                {key_concepts}
                {columns_html}
                {mind_map}
                {quiz}
                {project}
                {reading}
            </article>
        </main>
        
        <aside class="section-sidebar">
            {method_sidebar}
            
            <div class="sidebar-toc">
                <div class="toc-title">📑 本节目录</div>
                <ul class="toc-list">
                    <li><a href="#context">💡 情境导入</a></li>
                    <li><a href="#objectives">🎯 学习目标</a></li>
                    <li><a href="#concepts">🔑 核心知识点</a></li>
                    <li><a href="#mindmap">🧠 思维导图</a></li>
                    <li><a href="#quiz">📝 随堂测试</a></li>
                    <li><a href="#project">🚀 项目制学习</a></li>
                    <li><a href="#reading">📖 拓展阅读</a></li>
                </ul>
            </div>
            
            <div class="sidebar-back">
                <a href="../index.html#{subject_key}" class="btn-back">← 返回大纲</a>
            </div>
        </aside>
    </div>
    
    <!-- PDF Viewer Modal -->
    <div class="pdf-modal-overlay" id="pdfModal" style="display:none" onclick="if(event.target===this)closePdf()">
        <div class="pdf-modal">
            <div class="pdf-modal-header">
                <h3>📖 {item["section"]} — {item.get("page","")}</h3>
                <button class="pm-close" onclick="closePdf()">✕</button>
            </div>
            <div class="pdf-modal-body">
                <div class="pdf-paywall" id="pdfPaywall" style="display:none">
                    <div class="pp-icon">🔒</div>
                    <div class="pp-text">教材PDF属于付费内容<br>请先解锁全部课程后查看</div>
                    <button class="btn btn-primary" onclick="closePdf();location.href='../index.html'">🔓 返回解锁</button>
                </div>
                <iframe id="pdfIframe" src="" style="display:none;width:100%;height:100%;border:none"></iframe>
            </div>
            <div class="pdf-modal-controls">
                <button onclick="pdfZoom(-25)">🔍-</button>
                <span id="pdfZoomVal">100%</span>
                <button onclick="pdfZoom(25)">🔍+</button>
                <button onclick="pdfZoom(0)">↺ 重置</button>
            </div>
        </div>
    </div>
</div>

<script src="../{JS_FILE}"></script>
<script>
window._pdfFile = '{item.get("pdf_file","")}';
window._pdfPage = {item.get("pdf_page",1)};
window._sectionId = '{item.get("id","")}';
window._subjectKey = '{subject_key}';
</script>
</body>
</html>'''
    return page

def generate_section_css():
    """Generate the shared CSS file for section pages"""
    return '''/* ============ SECTION PAGE STYLES ============ */
:root {
  --blue-50: #eff6ff; --blue-100: #dbeafe; --blue-200: #bfdbfe;
  --blue-500: #3b82f6; --blue-600: #2563eb; --blue-700: #1d4ed8;
  --green-500: #10b981; --green-100: #d1fae5;
  --amber-500: #f59e0b; --amber-100: #fef3c7;
  --red-500: #ef4444; --red-100: #fee2e2;
  --purple-500: #8b5cf6; --purple-100: #ede9fe;
  --gray-50: #f8fafc; --gray-100: #f1f5f9; --gray-200: #e2e8f0;
  --gray-300: #cbd5e1; --gray-400: #94a3b8; --gray-500: #64748b;
  --gray-600: #475569; --gray-700: #334155; --gray-800: #1e293b;
  --white: #ffffff;
  --radius: 12px; --radius-sm: 8px;
  --shadow: 0 1px 3px rgba(0,0,0,.1);
  --shadow-md: 0 4px 6px -1px rgba(0,0,0,.1);
  --shadow-lg: 0 10px 15px -3px rgba(0,0,0,.1);
}
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:"PingFang SC","Microsoft YaHei","Noto Sans SC",sans-serif;background:#f0f4ff;color:var(--gray-800);line-height:1.8;min-height:100vh}
a{color:var(--blue-600);text-decoration:none}
a:hover{text-decoration:underline}

/* Navigation */
.section-nav{background:rgba(255,255,255,.95);backdrop-filter:blur(10px);padding:10px 24px;position:sticky;top:0;z-index:100;border-bottom:1px solid var(--gray-200);display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:8px}
.breadcrumb{font-size:.78rem;color:var(--gray-500)}
.breadcrumb .bc-current{color:var(--gray-700);font-weight:600}
.nav-links{display:flex;align-items:center;gap:12px}
.nav-link{padding:6px 14px;border-radius:20px;background:var(--gray-100);font-size:.78rem;font-weight:500;transition:.2s}
.nav-link:hover{background:var(--blue-50);color:var(--blue-700);text-decoration:none}
.nav-link.disabled{color:var(--gray-300);cursor:default;pointer-events:none}
.nav-pos{font-size:.72rem;color:var(--gray-400)}

/* Layout */
.section-layout{max-width:1200px;margin:0 auto;padding:24px;display:grid;grid-template-columns:1fr 300px;gap:24px}
@media(max-width:900px){.section-layout{grid-template-columns:1fr}}
.section-main{min-width:0}
.section-article{background:var(--white);border-radius:var(--radius);padding:32px;box-shadow:var(--shadow);margin-bottom:24px}
.section-sidebar{position:sticky;top:80px;align-self:start}

/* Article Header */
.article-header{margin-bottom:28px;padding-bottom:16px;border-bottom:2px solid var(--blue-100)}
.article-meta{font-size:.75rem;color:var(--gray-400);text-transform:uppercase;letter-spacing:.5px;margin-bottom:6px}
.article-header h1{font-size:1.8rem;font-weight:800;color:var(--gray-800);line-height:1.3}
.article-tags{display:flex;gap:8px;margin-top:12px;flex-wrap:wrap;align-items:center}
.tag{padding:3px 10px;border-radius:12px;font-size:.7rem;font-weight:600}
.page-tag{background:var(--gray-100);color:var(--gray-500)}
.free-tag{background:var(--green-100);color:var(--green-500)}
.locked-tag{background:var(--amber-100);color:var(--amber-500)}

/* Context Box */
.context-box{background:linear-gradient(135deg,#eff6ff,#f0fdf4);border-left:4px solid var(--blue-500);padding:18px 20px;border-radius:0 var(--radius-sm) var(--radius-sm) 0;margin-bottom:28px;display:flex;gap:12px;align-items:flex-start}
.context-icon{font-size:1.4rem;flex-shrink:0}
.context-text{font-size:.88rem;color:var(--gray-700);line-height:1.8}
.highlight{color:var(--blue-600);font-weight:600}

/* Learning Objectives */
.objectives-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:14px;margin:24px 0}
.obj-card{background:var(--gray-50);border-radius:var(--radius-sm);padding:16px 18px;border:1px solid var(--gray-200)}
.obj-title{font-size:.9rem;font-weight:700;margin-bottom:8px;color:var(--gray-700)}
.obj-card ul{padding-left:18px;font-size:.82rem;color:var(--gray-600);line-height:1.9}
.obj-card li{margin-bottom:3px}

/* Key Concepts */
.key-concepts{margin:28px 0}
.key-concepts h3,.quiz-section h3,.project-link h3,.extended-reading h3,.textbook-columns h3{margin-bottom:16px;color:var(--gray-700);display:flex;align-items:center;gap:8px;padding-bottom:8px;border-bottom:2px solid var(--gray-100)}
.concept-cards{display:flex;flex-direction:column;gap:10px}
.concept-card{display:flex;gap:14px;background:var(--gray-50);border-radius:var(--radius-sm);padding:14px 16px;border:1px solid var(--gray-200);transition:.2s}
.concept-card:hover{border-color:var(--blue-200);background:var(--blue-50)}
.concept-num{width:28px;height:28px;border-radius:50%;background:var(--blue-600);color:#fff;display:flex;align-items:center;justify-content:center;font-size:.8rem;font-weight:700;flex-shrink:0}
.concept-body{flex:1;min-width:0}
.concept-title{font-size:.88rem;font-weight:600;color:var(--gray-800);margin-bottom:4px}
.concept-detail{font-size:.8rem;color:var(--gray-500);line-height:1.7}

/* Textbook Columns */
.tb-col-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:8px;margin:12px 0}
.tb-column{padding:10px 14px;background:var(--purple-50, #ede9fe);border-radius:var(--radius-sm);font-size:.8rem;color:var(--gray-600);display:flex;align-items:center;gap:6px}

/* Mind Map */
.mind-map{margin:28px 0}
.mind-map-container{background:linear-gradient(135deg,#faf5ff,#eff6ff);border-radius:var(--radius);padding:24px;text-align:center;border:1px dashed var(--gray-300);display:flex;flex-wrap:wrap;justify-content:center;align-items:center;gap:20px}
.mm-center{background:var(--blue-600);color:#fff;padding:14px 22px;border-radius:24px;font-size:.95rem;font-weight:700;box-shadow:0 4px 12px rgba(37,99,235,.25)}
.mm-branches{display:flex;flex-wrap:wrap;gap:8px;justify-content:center}
.mm-node{padding:8px 14px;background:var(--white);border:1.5px solid var(--blue-200);border-radius:16px;font-size:.78rem;color:var(--gray-600);transition:.2s}
.mm-node:hover{border-color:var(--blue-500);color:var(--blue-700)}

/* Quiz */
.quiz-grid{display:flex;flex-direction:column;gap:16px}
.quiz-item{background:var(--gray-50);border-radius:var(--radius-sm);padding:16px;border:1px solid var(--gray-200)}
.quiz-q{font-size:.88rem;font-weight:600;color:var(--gray-700);margin-bottom:10px}
.quiz-options{display:flex;flex-direction:column;gap:6px}
.quiz-opt{display:flex;align-items:center;gap:8px;padding:8px 12px;border-radius:6px;cursor:pointer;font-size:.82rem;transition:.15s}
.quiz-opt:hover{background:var(--blue-50)}
.quiz-opt.correct{background:#d1fae5;color:#065f46}
.quiz-opt.wrong{background:#fee2e2;color:#991b1b}
.quiz-feedback{font-size:.78rem;margin-top:8px;padding:8px;border-radius:6px;display:none}
.quiz-feedback.show{display:block}
.quiz-feedback.correct{background:#d1fae5;color:#065f46}
.quiz-feedback.wrong{background:#fee2e2;color:#991b1b}
.quiz-fill{padding:8px 12px;border:1.5px solid var(--gray-200);border-radius:6px;font-size:.82rem;width:200px;font-family:inherit;outline:none}
.quiz-fill:focus{border-color:var(--blue-400)}
.quiz-score{text-align:center;font-size:1rem;font-weight:700;margin-top:16px;padding:12px;background:var(--blue-50);border-radius:var(--radius-sm)}

/* Project Link */
.project-cards{display:flex;flex-direction:column;gap:12px}
.project-card{background:linear-gradient(135deg,#fef3c7,#fef9c3);border:1.5px solid #fde68a;border-radius:var(--radius-sm);padding:16px 18px}
.pc-header{display:flex;align-items:center;gap:8px;margin-bottom:8px}
.pc-icon{font-size:1.2rem}
.pc-title{font-weight:700;font-size:.88rem;color:var(--gray-800)}
.pc-badge{font-size:.7rem;padding:2px 8px;background:var(--amber-500);color:#fff;border-radius:10px}
.pc-question{font-size:.82rem;color:var(--gray-600);margin-bottom:8px;line-height:1.6}
.pc-meta{display:flex;gap:16px;font-size:.72rem;color:var(--gray-400);margin-bottom:6px}
.pc-output{font-size:.78rem;color:var(--gray-500);margin-bottom:10px}
.project-placeholder{text-align:center;padding:32px;background:var(--gray-50);border-radius:var(--radius-sm);border:1px dashed var(--gray-300)}
.pp-icon{font-size:2rem;margin-bottom:8px}
.pp-text{font-size:.85rem;color:var(--gray-600);margin-bottom:4px}
.pp-hint{font-size:.75rem;color:var(--gray-400)}

/* Extended Reading */
.reading-list{display:flex;flex-direction:column;gap:8px}
.reading-item{padding:12px 16px;background:var(--gray-50);border-radius:var(--radius-sm);border:1px solid var(--gray-200);transition:.2s}
.reading-item:hover{background:var(--blue-50);border-color:var(--blue-200)}
.ri-title{font-size:.85rem;font-weight:600;color:var(--gray-700);margin-bottom:3px}
.ri-desc{font-size:.78rem;color:var(--gray-500)}

/* Sidebar */
.method-sidebar{background:var(--white);border-radius:var(--radius);padding:18px;box-shadow:var(--shadow);margin-bottom:16px}
.ms-title{font-size:.85rem;font-weight:700;color:var(--gray-800);margin-bottom:8px}
.ms-approach{font-size:.78rem;color:var(--blue-600);font-weight:600;margin-bottom:12px;padding:8px;background:var(--blue-50);border-radius:6px;text-align:center}
.ms-section{margin-top:10px}
.ms-label{font-size:.72rem;color:var(--gray-400);text-transform:uppercase;font-weight:600;margin-bottom:4px}
.ms-section ul{padding-left:16px;font-size:.75rem;color:var(--gray-600);line-height:1.8}
.insight-item{font-size:.75rem;color:var(--gray-500);padding:6px 8px;background:var(--gray-50);border-radius:6px;margin-bottom:4px;line-height:1.6}

.sidebar-toc{background:var(--white);border-radius:var(--radius);padding:18px;box-shadow:var(--shadow);margin-bottom:16px}
.toc-title{font-size:.85rem;font-weight:700;color:var(--gray-800);margin-bottom:10px}
.toc-list{list-style:none;padding:0}
.toc-list li{margin-bottom:6px}
.toc-list a{font-size:.78rem;color:var(--gray-500);transition:.2s;display:block;padding:4px 8px;border-radius:4px}
.toc-list a:hover{color:var(--blue-600);background:var(--blue-50);text-decoration:none}
.sidebar-back{margin-top:16px}
.btn-back{display:block;text-align:center;padding:10px;border-radius:var(--radius-sm);background:var(--gray-100);color:var(--gray-600);font-size:.82rem;font-weight:500;transition:.2s}
.btn-back:hover{background:var(--gray-200);text-decoration:none}

/* Buttons */
.btn{padding:8px 18px;border-radius:var(--radius-sm);border:none;cursor:pointer;font-size:.82rem;font-weight:500;transition:.2s;font-family:inherit}
.btn-primary{background:var(--blue-600);color:#fff}
.btn-primary:hover{background:var(--blue-700)}
.btn-ghost{background:transparent;color:var(--gray-500);border:1px solid var(--gray-200)}
.btn-ghost:hover{background:var(--gray-50)}
.btn-outline{padding:6px 14px;border-radius:var(--radius-sm);border:1.5px solid var(--blue-300);background:var(--white);color:var(--blue-600);font-size:.78rem;font-weight:500;cursor:pointer;transition:.2s;text-decoration:none;display:inline-block;margin-top:8px}
.btn-outline:hover{background:var(--blue-50)}
.btn-sm{padding:5px 12px;font-size:.75rem}
.btn-pdf{display:inline-flex;align-items:center;gap:4px;padding:6px 14px;border-radius:var(--radius-sm);border:1.5px solid var(--blue-300);background:var(--blue-50);color:var(--blue-700);cursor:pointer;font-size:.78rem;font-weight:600;transition:.2s;font-family:inherit}
.btn-pdf:hover{background:var(--blue-100);border-color:var(--blue-400)}

/* PDF Modal */
.pdf-modal-overlay{position:fixed;top:0;left:0;right:0;bottom:0;background:rgba(0,0,0,.65);z-index:2000;display:flex;align-items:center;justify-content:center}
.pdf-modal{background:var(--white);border-radius:var(--radius);width:95%;max-width:1000px;height:85vh;display:flex;flex-direction:column;box-shadow:0 20px 60px rgba(0,0,0,.3);overflow:hidden}
.pdf-modal-header{display:flex;align-items:center;justify-content:space-between;padding:12px 20px;border-bottom:1px solid var(--gray-200)}
.pdf-modal-header h3{font-size:.9rem;font-weight:700}
.pm-close{width:32px;height:32px;border-radius:50%;border:none;background:var(--gray-100);cursor:pointer;font-size:1rem;display:flex;align-items:center;justify-content:center}
.pm-close:hover{background:var(--gray-200)}
.pdf-modal-body{flex:1;position:relative;overflow:hidden}
.pdf-paywall{position:absolute;top:0;left:0;right:0;bottom:0;display:flex;flex-direction:column;align-items:center;justify-content:center;background:rgba(255,255,255,.95);backdrop-filter:blur(12px);z-index:10;gap:14px}
.pdf-modal-controls{display:flex;align-items:center;justify-content:center;gap:8px;padding:8px 12px;border-top:1px solid var(--gray-200)}
.pdf-modal-controls button{padding:6px 12px;border-radius:6px;border:1px solid var(--gray-200);background:var(--white);cursor:pointer;font-size:.78rem}

@media(max-width:768px){
  .section-layout{grid-template-columns:1fr;padding:12px}
  .section-article{padding:20px}
  .article-header h1{font-size:1.4rem}
  .section-sidebar{position:static}
}
'''

def generate_section_js():
    """Generate shared JS for section pages"""
    return '''// ============ QUIZ FUNCTIONS ============
let userAnswers = {};

function checkAnswer(qIdx, selectedIdx, correctIdx) {
    if (userAnswers[qIdx] !== undefined) return; // Already answered
    userAnswers[qIdx] = selectedIdx;
    
    const container = document.getElementById('quiz' + qIdx);
    const feedback = document.getElementById('fb' + qIdx);
    const options = container.querySelectorAll('.quiz-opt');
    
    options.forEach((opt, i) => {
        if (i === correctIdx) opt.classList.add('correct');
        else if (i === selectedIdx && i !== correctIdx) opt.classList.add('wrong');
        opt.querySelector('input').disabled = true;
    });
    
    feedback.className = 'quiz-feedback show';
    feedback.textContent = selectedIdx === correctIdx 
        ? '✅ 正确！太棒了！' 
        : '❌ 正确答案是 ' + String.fromCharCode(65 + correctIdx);
    feedback.classList.add(selectedIdx === correctIdx ? 'correct' : 'wrong');
}

function checkFill(qIdx, answer) {
    if (userAnswers[qIdx] !== undefined) return;
    
    const input = document.getElementById('fill' + qIdx);
    const val = input.value.trim();
    if (!val) return;
    
    userAnswers[qIdx] = val;
    const isCorrect = val === answer;
    
    const feedback = document.getElementById('fb' + qIdx);
    feedback.className = 'quiz-feedback show';
    feedback.textContent = isCorrect 
        ? '✅ 正确！' 
        : '❌ 正确答案：' + answer;
    feedback.classList.add(isCorrect ? 'correct' : 'wrong');
    
    input.disabled = true;
}

function showScore(total) {
    if (!window._quizTypes || !window._quizAnswers) return;
    
    let correct = 0, answered = 0;
    for (let i = 0; i < total; i++) {
        if (userAnswers[i] !== undefined) {
            answered++;
            const userAns = window._quizTypes[i] === 'mc' ? userAnswers[i] : String(userAnswers[i]).trim();
            const correctAns = window._quizTypes[i] === 'mc' ? window._quizAnswers[i] : String(window._quizAnswers[i]).trim();
            if (userAns === correctAns) correct++;
        }
    }
    
    const scoreDiv = document.getElementById('quizScore');
    scoreDiv.style.display = 'block';
    const pct = Math.round(correct / total * 100);
    const emoji = pct >= 80 ? '🎉' : pct >= 60 ? '👍' : '💪';
    scoreDiv.innerHTML = `${emoji} 成绩：${correct}/${total} (${pct}分) — ${answered < total ? '还有' + (total-answered) + '题未答' : '全部完成！'}`;
    scoreDiv.scrollIntoView({behavior:'smooth'});
}

function resetQuiz() {
    userAnswers = {};
    location.reload();
}

// ============ PDF VIEWER ============
let pdfZoomLevel = 100;

function openPdf() {
    const modal = document.getElementById('pdfModal');
    const iframe = document.getElementById('pdfIframe');
    const paywall = document.getElementById('pdfPaywall');
    
    // Check unlock (read from localStorage set by main index.html)
    const isUnlocked = localStorage.getItem('bioChemUnlocked') === 'true';
    
    if (!isUnlocked) {
        paywall.style.display = 'flex';
        iframe.style.display = 'none';
    } else {
        paywall.style.display = 'none';
        iframe.style.display = 'block';
        iframe.src = '../pdf/' + window._pdfFile + '#page=' + window._pdfPage + '&view=FitH';
    }
    
    modal.style.display = 'flex';
}

function closePdf() {
    document.getElementById('pdfModal').style.display = 'none';
    document.getElementById('pdfIframe').src = '';
}

function pdfZoom(delta) {
    if (delta === 0) pdfZoomLevel = 100;
    else pdfZoomLevel = Math.max(50, Math.min(300, pdfZoomLevel + delta));
    document.getElementById('pdfZoomVal').textContent = pdfZoomLevel + '%';
    document.getElementById('pdfIframe').style.transform = 'scale(' + (pdfZoomLevel/100) + ')';
    document.getElementById('pdfIframe').style.transformOrigin = 'top center';
}
'''

def generate_index_page(all_sections):
    """Generate an index page listing all sections"""
    html = '''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>智慧学堂 - 全部章节</title>
<style>
body{font-family:"PingFang SC","Microsoft YaHei",sans-serif;background:#f0f4ff;max-width:900px;margin:0 auto;padding:24px}
h1{font-size:1.5rem;margin-bottom:24px;color:#1e293b}
.subject-group{margin-bottom:32px}
.sg-title{font-size:1.1rem;font-weight:700;margin-bottom:12px;padding:8px 14px;border-radius:8px;color:#fff}
.sg-list{display:flex;flex-direction:column;gap:6px}
.sg-item{display:flex;align-items:center;gap:10px;padding:6px 10px;background:#fff;border-radius:6px;font-size:.82rem;transition:.2s}
.sg-item:hover{background:#eff6ff}
.sg-item a{color:#2563eb;text-decoration:none;flex:1}
.sg-item a:hover{text-decoration:underline}
.sg-page{font-size:.7rem;color:#94a3b8}
.sg-badge{font-size:.65rem;padding:2px 8px;border-radius:10px;font-weight:600}
.badge-free{background:#d1fae5;color:#065f46}
.badge-paid{background:#fef3c7;color:#92400e}
</style>
</head>
<body>
<h1>📚 智慧学堂 — 全部章节索引</h1>
'''
    
    subjects_order = ['bio','chem','geo','phy','math','cn','eng','hist','pol']
    colors = {'bio':'#10b981','chem':'#8b5cf6','geo':'#f59e0b','phy':'#ef4444','math':'#3b82f6','cn':'#ec4899','eng':'#06b6d4','hist':'#78716c','pol':'#14b8a6'}
    names = {'bio':'🧬 生物学','chem':'⚗️ 化学','geo':'🗺️ 地理','phy':'⚡ 物理','math':'📐 数学','cn':'📖 语文','eng':'🔤 英语','hist':'🏛️ 历史','pol':'⚖️ 道德与法治'}
    
    total = 0
    for sk in subjects_order:
        sections = all_sections.get(sk, [])
        if not sections: continue
        total += len(sections)
        color = colors.get(sk, '#64748b')
        name = names.get(sk, sk)
        
        html += f'<div class="subject-group"><div class="sg-title" style="background:{color}">{name} ({len(sections)}节)</div><div class="sg-list">'
        
        for sec in sections:
            badge = '<span class="sg-badge badge-free">免费</span>' if sec.get('free') else '<span class="sg-badge badge-paid">需解锁</span>'
            html += f'<div class="sg-item">{badge}<a href="{sk}/{sec["id"]}.html">{sec["section"]}</a><span class="sg-page">{sec.get("page","")}</span></div>'
        
        html += '</div></div>'
    
    html += f'<div style="text-align:center;margin-top:30px;color:#94a3b8;font-size:.8rem">共 {total} 个小节</div>'
    html += '</body></html>'
    return html

def generate_projects_page():
    """Generate the projects listing page"""
    from teaching_methods import SUBJECT_PROJECTS
    
    all_projects = []
    for sk, projects in SUBJECT_PROJECTS.items():
        for proj in projects:
            all_projects.append({**proj, 'subject_key': sk, 'subject': SUBJECTS_META.get(sk, {})})
    
    proj_cards = '\n'.join(f'''
    <div class="proj-card" id="{p['id']}">
        <div class="pc-header">
            <span class="pc-subj-icon">{p['subject'].get('icon','')}</span>
            <span class="pc-subj">{p['subject'].get('name','')}</span>
            <span class="pc-diff">{p.get('difficulty','')}</span>
        </div>
        <h3>{p['title']}</h3>
        <p class="pc-dq">❓ {p.get('driving_question','')}</p>
        <div class="pc-meta">
            <span>⏱ {p.get('duration','')}</span>
            <span>🎯 {', '.join(p.get('skills',[])[:3])}</span>
        </div>
        <div class="pc-output">📦 产出：{p.get('output','')}</div>
        <span class="pc-status">🏗 模板（待完善）</span>
    </div>''' for p in all_projects)
    
    color_map = {'bio':'#10b981','chem':'#8b5cf6','geo':'#f59e0b','phy':'#ef4444','math':'#3b82f6','cn':'#ec4899','eng':'#06b6d4','hist':'#78716c','pol':'#14b8a6'}
    
    return f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>项目制学习 | 智慧学堂</title>
<style>
*{{margin:0;padding:0;box-sizing:border-box}}
body{{font-family:"PingFang SC","Microsoft YaHei",sans-serif;background:#f0f4ff;color:#1e293b;line-height:1.6}}
.header{{background:linear-gradient(135deg,#1e3a5f,#2563eb);color:#fff;padding:40px 24px;text-align:center}}
.header h1{{font-size:1.8rem;margin-bottom:8px}}
.header p{{font-size:.9rem;opacity:.8}}
.container{{max-width:1100px;margin:0 auto;padding:24px}}
.proj-grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(320px,1fr));gap:16px}}
.proj-card{{background:#fff;border-radius:12px;padding:20px;box-shadow:0 1px 3px rgba(0,0,0,.1);border:1px solid #e2e8f0;transition:.2s}}
.proj-card:hover{{box-shadow:0 4px 12px rgba(0,0,0,.1);transform:translateY(-2px)}}
.pc-header{{display:flex;align-items:center;gap:8px;margin-bottom:10px}}
.pc-subj-icon{{font-size:1.2rem}}
.pc-subj{{font-size:.75rem;font-weight:600;color:#64748b}}
.pc-diff{{font-size:.7rem;padding:2px 8px;background:#fef3c7;color:#92400e;border-radius:10px;margin-left:auto}}
.proj-card h3{{font-size:1rem;margin-bottom:8px;color:#1e293b}}
.pc-dq{{font-size:.82rem;color:#64748b;margin-bottom:10px;line-height:1.5}}
.pc-meta{{display:flex;gap:16px;font-size:.72rem;color:#94a3b8;margin-bottom:8px}}
.pc-output{{font-size:.78rem;color:#64748b;margin-bottom:8px}}
.pc-status{{font-size:.7rem;color:#94a3b8;background:#f1f5f9;padding:3px 8px;border-radius:10px}}
.nav-back{{text-align:center;margin-top:32px}}
.nav-back a{{color:#2563eb;text-decoration:none;font-size:.9rem;font-weight:500}}
</style>
</head>
<body>
<div class="header">
    <h1>🚀 项目制学习</h1>
    <p>以真实问题驱动的跨学科探究项目，融汇课程重难点</p>
</div>
<div class="container">
    <div class="proj-grid">{proj_cards}</div>
    <div class="nav-back">
        <a href="./">← 返回章节索引</a> | <a href="../">← 返回首页</a>
    </div>
</div>
</body>
</html>'''

def main():
    print('=' * 60)
    print('Generating section pages...')
    print('=' * 60)
    
    # Create output directories
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    for sk in SUBJECTS_META:
        os.makedirs(os.path.join(OUTPUT_DIR, sk), exist_ok=True)
    
    # Write shared CSS and JS
    with open(os.path.join(OUTPUT_DIR, CSS_FILE), 'w', encoding='utf-8') as f:
        f.write(generate_section_css())
    print(f'✅ {CSS_FILE} written')
    
    with open(os.path.join(OUTPUT_DIR, JS_FILE), 'w', encoding='utf-8') as f:
        f.write(generate_section_js())
    print(f'✅ {JS_FILE} written')
    
    # Generate section pages for each subject
    all_sections = {}
    total_pages = 0
    
    for sk, meta in SUBJECTS_META.items():
        items = load_data(sk)
        if not items:
            print(f'⚠️  {sk}: no data')
            continue
        
        all_sections[sk] = items
        
        for item in items:
            page_html = generate_section_page(sk, item, items)
            filename = f'{item["id"]}.html'
            filepath = os.path.join(OUTPUT_DIR, sk, filename)
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(page_html)
            total_pages += 1
        
        print(f'✅ {sk} ({meta["name"]}): {len(items)} pages')
    
    # Generate index page
    index_html = generate_index_page(all_sections)
    with open(os.path.join(OUTPUT_DIR, 'index.html'), 'w', encoding='utf-8') as f:
        f.write(index_html)
    print(f'✅ Index page written')
    
    # Generate projects page
    projects_html = generate_projects_page()
    os.makedirs(os.path.join(OUTPUT_DIR, '..', 'projects'), exist_ok=True)
    with open(os.path.join(OUTPUT_DIR, '..', 'projects', 'index.html'), 'w', encoding='utf-8') as f:
        f.write(projects_html)
    print(f'✅ Projects page written')
    
    print(f'\n{"="*60}')
    print(f'TOTAL: {total_pages} section pages generated')
    print(f'Output: {OUTPUT_DIR}')
    print(f'{"="*60}')

if __name__ == '__main__':
    main()
