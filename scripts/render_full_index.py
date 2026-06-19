from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

HTML = r'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>智慧学堂 - 初中全科 AI 学习平台</title>
<style>
:root{
  --ink:#172033;--muted:#667085;--line:#d9e0ea;--paper:#ffffff;--wash:#f5f7fb;
  --green:#16a34a;--violet:#7c3aed;--red:#dc2626;--blue:#2563eb;--pink:#db2777;
  --cyan:#0891b2;--stone:#78716c;--amber:#d97706;--teal:#0f766e;
  --shadow:0 12px 32px rgba(23,32,51,.10);--radius:8px;
}
*{box-sizing:border-box}
body{margin:0;font-family:-apple-system,BlinkMacSystemFont,"Segoe UI","Microsoft YaHei",Arial,sans-serif;background:var(--wash);color:var(--ink);letter-spacing:0}
button,input,textarea,select{font:inherit}
button{cursor:pointer}
.app{min-height:100vh;display:grid;grid-template-columns:300px minmax(0,1fr) 340px}
.rail{background:#101828;color:#fff;min-height:100vh;padding:18px 14px;position:sticky;top:0;align-self:start}
.brand{padding:10px 8px 18px;border-bottom:1px solid rgba(255,255,255,.12)}
.brand h1{font-size:1.25rem;margin:0 0 8px;font-weight:800}
.brand p{margin:0;color:#cbd5e1;font-size:.82rem;line-height:1.5}
.search{margin:14px 0}
.search input{width:100%;border:1px solid rgba(255,255,255,.18);background:#1d2939;color:#fff;border-radius:6px;padding:10px 12px;outline:none}
.subjects{display:grid;grid-template-columns:1fr 1fr;gap:8px}
.subject-btn{border:1px solid rgba(255,255,255,.13);background:#1d2939;color:#e5e7eb;border-radius:6px;padding:10px;text-align:left;min-height:64px}
.subject-btn.active{background:#fff;color:#111827;border-color:#fff}
.subject-btn b{display:block;font-size:.94rem;margin-bottom:3px}
.subject-btn span{font-size:.72rem;color:inherit;opacity:.72}
.filters{margin-top:16px;display:grid;gap:8px}
.filters select{width:100%;border:1px solid rgba(255,255,255,.16);background:#1d2939;color:#fff;border-radius:6px;padding:9px}
.main{min-width:0;padding:22px}
.topbar{display:flex;align-items:center;justify-content:space-between;gap:16px;margin-bottom:16px}
.headline h2{margin:0;font-size:1.35rem}
.headline p{margin:6px 0 0;color:var(--muted);font-size:.9rem}
.stats{display:flex;gap:8px;flex-wrap:wrap}
.stat{background:var(--paper);border:1px solid var(--line);border-radius:6px;padding:8px 10px;font-size:.8rem;color:var(--muted)}
.workspace{display:grid;grid-template-columns:330px minmax(0,1fr);gap:16px;align-items:start}
.list-panel,.lesson,.ai-panel{background:var(--paper);border:1px solid var(--line);border-radius:var(--radius);box-shadow:var(--shadow)}
.list-panel{max-height:calc(100vh - 122px);overflow:auto}
.list-head{position:sticky;top:0;background:var(--paper);z-index:1;padding:12px;border-bottom:1px solid var(--line)}
.list-head strong{font-size:.95rem}
.section-list{padding:8px}
.unit-title{font-size:.75rem;color:var(--muted);font-weight:800;margin:14px 8px 6px}
.section-row{width:100%;border:1px solid transparent;background:transparent;border-radius:6px;padding:9px 8px;text-align:left;display:grid;grid-template-columns:minmax(0,1fr) auto;gap:8px;color:var(--ink)}
.section-row:hover{background:#eef4ff;border-color:#c7d7fe}
.section-row.active{background:#eff6ff;border-color:#93c5fd}
.section-row b{font-size:.84rem;font-weight:700;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.section-row span{font-size:.72rem;color:var(--muted)}
.lesson{overflow:hidden}
.lesson-header{padding:22px;border-bottom:1px solid var(--line);background:linear-gradient(180deg,#fff,#f9fbff)}
.crumb{font-size:.78rem;color:var(--muted);margin-bottom:9px}
.lesson h3{margin:0 0 10px;font-size:1.55rem;line-height:1.25}
.lesson-meta{display:flex;gap:8px;flex-wrap:wrap}
.pill{border:1px solid var(--line);border-radius:999px;padding:5px 9px;font-size:.76rem;color:#344054;background:#fff}
.lesson-actions{display:flex;gap:8px;flex-wrap:wrap;margin-top:16px}
.primary,.ghost{border-radius:6px;padding:9px 12px;border:1px solid var(--line);background:#fff;color:var(--ink)}
.primary{background:#1f2937;color:#fff;border-color:#1f2937}
.primary:hover{background:#111827}
.ghost:hover{background:#f2f4f7}
.lesson-body{padding:18px;display:grid;gap:14px}
.band{border:1px solid var(--line);border-radius:8px;padding:16px;background:#fff}
.band h4{margin:0 0 12px;font-size:1rem}
.intro{line-height:1.75;color:#344054}
.concepts{display:grid;gap:10px}
.concept{display:grid;grid-template-columns:30px minmax(0,1fr);gap:10px;align-items:start}
.num{width:30px;height:30px;border-radius:6px;background:#eef4ff;color:#1d4ed8;display:grid;place-items:center;font-weight:800;font-size:.82rem}
.concept b{display:block;margin-bottom:4px}
.concept p{margin:0;color:var(--muted);font-size:.88rem;line-height:1.65}
.quiz{display:grid;gap:12px}
.q{border:1px solid #e5e7eb;border-radius:8px;padding:12px;background:#fafafa}
.q-title{font-weight:700;margin-bottom:8px}
.opt{display:block;border:1px solid #e5e7eb;background:#fff;border-radius:6px;padding:8px;margin:6px 0}
.opt.correct{border-color:#16a34a;background:#ecfdf3}
.opt.wrong{border-color:#dc2626;background:#fef2f2}
.fill-line{display:flex;gap:8px;flex-wrap:wrap}
.fill-line input{flex:1;min-width:180px;border:1px solid var(--line);border-radius:6px;padding:8px}
.feedback{font-size:.82rem;margin-top:8px;color:var(--muted)}
.ai-panel{height:100vh;position:sticky;top:0;border-radius:0;border-top:0;border-bottom:0;border-right:0;display:flex;flex-direction:column}
.ai-head{padding:18px;border-bottom:1px solid var(--line)}
.ai-head h3{margin:0 0 6px;font-size:1.05rem}
.ai-head p{margin:0;color:var(--muted);font-size:.82rem;line-height:1.5}
.chat{padding:14px;overflow:auto;flex:1;display:flex;flex-direction:column;gap:10px}
.msg{border-radius:8px;padding:10px 12px;font-size:.88rem;line-height:1.6;max-width:92%}
.msg.bot{background:#f2f4f7;align-self:flex-start}
.msg.user{background:#1f2937;color:#fff;align-self:flex-end}
.ask{border-top:1px solid var(--line);padding:12px;display:grid;gap:8px}
.ask textarea{width:100%;min-height:86px;resize:vertical;border:1px solid var(--line);border-radius:6px;padding:10px}
.quick{display:flex;gap:6px;flex-wrap:wrap}
.quick button{border:1px solid var(--line);border-radius:999px;background:#fff;padding:6px 9px;font-size:.76rem}
.modal{position:fixed;inset:0;background:rgba(15,23,42,.72);display:none;align-items:center;justify-content:center;z-index:20;padding:24px}
.modal.open{display:flex}
.pdf-box{background:#fff;border-radius:8px;box-shadow:var(--shadow);width:min(1120px,96vw);height:90vh;display:flex;flex-direction:column;overflow:hidden}
.pdf-head{padding:10px 12px;border-bottom:1px solid var(--line);display:flex;align-items:center;justify-content:space-between;gap:12px}
.pdf-head b{font-size:.92rem}
.pdf-head button{border:1px solid var(--line);background:#fff;border-radius:6px;padding:7px 10px}
.pdf-box iframe{border:0;width:100%;height:100%;background:#f3f4f6}
.empty{padding:24px;color:var(--muted);text-align:center}
@media (max-width:1180px){.app{grid-template-columns:280px minmax(0,1fr)}.ai-panel{grid-column:1 / -1;height:auto;min-height:360px;position:static;border:1px solid var(--line);border-radius:8px;margin:0 22px 22px}.workspace{grid-template-columns:300px minmax(0,1fr)}}
@media (max-width:820px){.app{display:block}.rail{position:static;min-height:auto}.subjects{grid-template-columns:1fr 1fr 1fr}.main{padding:14px}.topbar{display:block}.workspace{display:block}.list-panel{max-height:360px;margin-bottom:14px}.lesson h3{font-size:1.25rem}.ai-panel{margin:14px}.subjects{grid-template-columns:1fr 1fr}}
</style>
</head>
<body>
<div class="app">
  <aside class="rail">
    <div class="brand">
      <h1>智慧学堂</h1>
      <p>初中全科 AI 学习平台。覆盖教材目录、知识点、随堂测试和教材 PDF 精准跳页。</p>
    </div>
    <div class="search"><input id="searchInput" placeholder="搜索课程、小节或关键词"></div>
    <div class="subjects" id="subjectButtons"></div>
    <div class="filters">
      <select id="gradeFilter"></select>
      <select id="semesterFilter"></select>
    </div>
  </aside>
  <main class="main">
    <div class="topbar">
      <div class="headline">
        <h2 id="courseTitle">课程加载中</h2>
        <p id="courseHint">正在读取全量课程数据</p>
      </div>
      <div class="stats" id="stats"></div>
    </div>
    <div class="workspace">
      <section class="list-panel">
        <div class="list-head"><strong id="listTitle">章节目录</strong></div>
        <div class="section-list" id="sectionList"></div>
      </section>
      <section class="lesson" id="lessonView"></section>
    </div>
  </main>
  <aside class="ai-panel">
    <div class="ai-head">
      <h3>AI 问答</h3>
      <p id="aiContext">选择一个小节后，我会围绕当前教材内容回答。</p>
    </div>
    <div class="chat" id="chat"></div>
    <div class="ask">
      <div class="quick">
        <button data-prompt="帮我用三句话总结本节">总结本节</button>
        <button data-prompt="本节最容易错在哪里">易错点</button>
        <button data-prompt="给我一道类似练习题">出题</button>
      </div>
      <textarea id="askInput" placeholder="输入你的问题，例如：这节课的核心知识是什么？"></textarea>
      <button class="primary" id="askBtn">发送</button>
    </div>
  </aside>
</div>
<div class="modal" id="pdfModal">
  <div class="pdf-box">
    <div class="pdf-head">
      <b id="pdfTitle">教材 PDF</b>
      <button id="closePdf">关闭</button>
    </div>
    <iframe id="pdfFrame" title="教材 PDF"></iframe>
  </div>
</div>
<script>
const $ = (s) => document.querySelector(s);
const state = {data:null, subject:'bio', grade:null, semester:null, section:null, query:''};
const subjectOrder = ['bio','chem','phy','math','cn','eng','hist','geo','pol'];

function esc(text){return String(text ?? '').replace(/[&<>"']/g, m => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[m]));}
function grouped(items){return items.reduce((acc,item)=>{const k = `${item.unit || '未分单元'} - ${item.chapter || ''}`; (acc[k] ||= []).push(item); return acc;},{});}
function currentItems(){
  if(!state.data) return [];
  const q = state.query.trim().toLowerCase();
  return state.data.items.filter(x => x.subject===state.subject && (!state.grade || x.grade===state.grade) && (!state.semester || x.semester===state.semester) && (!q || `${x.title} ${x.unit} ${x.chapter} ${x.keypoints.join(' ')}`.toLowerCase().includes(q)));
}
function allForSubject(){return state.data.items.filter(x=>x.subject===state.subject);}

async function init(){
  try{
    const res = await fetch('data/full_courses.json', {cache:'no-store'});
    state.data = await res.json();
  }catch(err){
    $('#lessonView').innerHTML = '<div class="empty">课程数据加载失败。请通过 GitHub Pages 或 npm start 打开页面。</div>';
    return;
  }
  const hashId = decodeURIComponent(location.hash.replace(/^#section=/,''));
  if(hashId){
    const found = state.data.items.find(x=>x.id===hashId);
    if(found){state.subject=found.subject; state.grade=found.grade; state.semester=found.semester; state.section=found.id;}
  }
  renderSubjects();
  syncFilters();
  render();
  $('#searchInput').addEventListener('input', e=>{state.query=e.target.value; renderList();});
  $('#gradeFilter').addEventListener('change', e=>{state.grade = Number(e.target.value); syncSemester(); pickFirst(); render();});
  $('#semesterFilter').addEventListener('change', e=>{state.semester = e.target.value; pickFirst(); render();});
  $('#closePdf').addEventListener('click', closePdf);
  $('#askBtn').addEventListener('click', ask);
  $('#askInput').addEventListener('keydown', e=>{if(e.key==='Enter' && (e.ctrlKey || e.metaKey)) ask();});
  document.querySelectorAll('.quick button').forEach(btn=>btn.addEventListener('click',()=>{$('#askInput').value=btn.dataset.prompt; ask();}));
}

function renderSubjects(){
  $('#subjectButtons').innerHTML = subjectOrder.map(key=>{
    const meta = state.data.subjects[key];
    const count = state.data.items.filter(x=>x.subject===key).length;
    return `<button class="subject-btn ${key===state.subject?'active':''}" data-subject="${key}" style="border-left:4px solid ${meta.color}"><b>${esc(meta.name)}</b><span>${count} 个小节</span></button>`;
  }).join('');
  document.querySelectorAll('.subject-btn').forEach(btn=>btn.addEventListener('click',()=>{
    state.subject = btn.dataset.subject; state.query=''; $('#searchInput').value=''; syncFilters(); pickFirst(); render();
  }));
}
function syncFilters(){
  const grades = [...new Set(allForSubject().map(x=>x.grade))].sort((a,b)=>a-b);
  state.grade = state.grade && grades.includes(state.grade) ? state.grade : grades[0];
  $('#gradeFilter').innerHTML = grades.map(g=>`<option value="${g}" ${g===state.grade?'selected':''}>${g} 年级</option>`).join('');
  syncSemester();
}
function syncSemester(){
  const semesters = [...new Set(allForSubject().filter(x=>x.grade===state.grade).map(x=>x.semester))];
  state.semester = state.semester && semesters.includes(state.semester) ? state.semester : semesters[0];
  $('#semesterFilter').innerHTML = semesters.map(s=>`<option value="${esc(s)}" ${s===state.semester?'selected':''}>${s==='全'?'全一册':s+'册'}</option>`).join('');
}
function pickFirst(){const items=currentItems(); state.section = items[0]?.id || null;}
function render(){renderSubjects(); renderHeader(); renderList(); renderLesson();}
function renderHeader(){
  const meta = state.data.subjects[state.subject];
  const items = currentItems();
  $('#courseTitle').textContent = `${meta.name} ${state.grade} 年级${state.semester==='全'?'全一册':state.semester+'册'}`;
  $('#courseHint').textContent = '小节可直接点开学习，也可查看教材 PDF 对应页。';
  $('#stats').innerHTML = `<span class="stat">当前 ${items.length} 小节</span><span class="stat">全库 ${state.data.items.length} 条</span><span class="stat">PDF 页码已按偏移映射</span>`;
}
function renderList(){
  const items = currentItems();
  $('#listTitle').textContent = `章节目录（${items.length}）`;
  if(!items.length){$('#sectionList').innerHTML='<div class="empty">没有匹配的小节</div>'; return;}
  if(!state.section || !items.some(x=>x.id===state.section)) state.section = items[0].id;
  const groups = grouped(items);
  $('#sectionList').innerHTML = Object.entries(groups).map(([name, arr]) => `
    <div class="unit-title">${esc(name)}</div>
    ${arr.map(item=>`<button class="section-row ${item.id===state.section?'active':''}" data-id="${esc(item.id)}"><b>${esc(item.title)}</b><span>${esc(item.pageLabel)}</span></button>`).join('')}
  `).join('');
  document.querySelectorAll('.section-row').forEach(btn=>btn.addEventListener('click',()=>selectSection(btn.dataset.id)));
}
function selectSection(id){state.section=id; history.replaceState(null,'',`#section=${encodeURIComponent(id)}`); renderList(); renderLesson();}
function getLesson(){return state.data.items.find(x=>x.id===state.section) || currentItems()[0];}
function renderLesson(){
  const item = getLesson();
  if(!item){$('#lessonView').innerHTML='<div class="empty">请选择一个小节</div>'; return;}
  $('#aiContext').textContent = `当前：${item.subjectName} ${item.grade}${item.semester} - ${item.title}`;
  const concepts = item.keypoints.map((kp,i)=>`<div class="concept"><span class="num">${i+1}</span><div><b>${esc(kp)}</b><p>${esc(conceptDetail(item,kp))}</p></div></div>`).join('');
  const quiz = item.quiz.map((q,i)=>renderQuiz(q,i)).join('');
  $('#lessonView').innerHTML = `
    <div class="lesson-header">
      <div class="crumb">${esc(item.subjectName)} / ${esc(item.unit)} / ${esc(item.chapter)}</div>
      <h3>${esc(item.title)}</h3>
      <div class="lesson-meta">
        <span class="pill">书本页码 ${esc(item.pageLabel)}</span>
        <span class="pill">PDF 第 ${item.pdfPage} 页</span>
        <span class="pill">${esc(item.pdfFile)}</span>
      </div>
      <div class="lesson-actions">
        <button class="primary" id="openPdfBtn">查看教材 PDF</button>
        <button class="ghost" id="copyLinkBtn">复制本节链接</button>
      </div>
    </div>
    <div class="lesson-body">
      <div class="band intro">本节围绕“${esc(item.title)}”展开。学习时先阅读教材对应页，再对照知识点梳理概念、方法和典型问题，最后完成随堂测试形成闭环。</div>
      <div class="band"><h4>知识点罗列</h4><div class="concepts">${concepts}</div></div>
      <div class="band"><h4>学习目标</h4><div class="concepts">${item.examPoints.map((x,i)=>`<div class="concept"><span class="num">${i+1}</span><div><b>${esc(x)}</b><p>能够解释、辨析并在题目或真实情境中运用。</p></div></div>`).join('')}</div></div>
      <div class="band"><h4>随堂测试</h4><div class="quiz">${quiz}</div></div>
    </div>`;
  $('#openPdfBtn').addEventListener('click',()=>openPdf(item));
  $('#copyLinkBtn').addEventListener('click',()=>navigator.clipboard?.writeText(location.href.split('#')[0] + '#section=' + encodeURIComponent(item.id)));
}
function conceptDetail(item,kp){
  if(item.methods?.length) return `建议用“${item.methods.join(' - ')}”的路径学习：先找教材证据，再用自己的话解释，最后做题验证。`;
  return '结合教材例子理解，不只记结论，还要说清条件、过程和应用。';
}
function renderQuiz(q,i){
  if(q.type==='fill') return `<div class="q" data-answer="${esc(q.answer)}"><div class="q-title">${i+1}. ${esc(q.q)}</div><div class="fill-line"><input placeholder="${esc(q.hint || '填写答案')}"><button class="ghost" onclick="checkFill(this)">提交</button></div><div class="feedback"></div></div>`;
  return `<div class="q"><div class="q-title">${i+1}. ${esc(q.q)}</div>${(q.options||[]).map((op,j)=>`<button class="opt" onclick="checkOpt(this,${j},${Number(q.answer)})">${String.fromCharCode(65+j)}. ${esc(op)}</button>`).join('')}<div class="feedback">${esc(q.explanation||'')}</div></div>`;
}
function checkOpt(btn,chosen,answer){
  const box = btn.closest('.q'); box.querySelectorAll('.opt').forEach((b,i)=>{b.disabled=true; if(i===answer)b.classList.add('correct'); if(i===chosen && i!==answer)b.classList.add('wrong');});
}
function checkFill(btn){
  const box = btn.closest('.q'); const input = box.querySelector('input'); const ok = input.value.trim() === box.dataset.answer;
  box.querySelector('.feedback').textContent = ok ? '回答正确。' : `参考答案：${box.dataset.answer}`;
  input.disabled = true; btn.disabled = true;
}
function openPdf(item){
  $('#pdfTitle').textContent = `${item.title} - 书本 ${item.pageLabel} / PDF 第 ${item.pdfPage} 页`;
  $('#pdfFrame').src = `pdf/${encodeURIComponent(item.pdfFile)}#page=${item.pdfPage}&view=FitH`;
  $('#pdfModal').classList.add('open');
}
function closePdf(){ $('#pdfModal').classList.remove('open'); $('#pdfFrame').src=''; }
function addMsg(text,who='bot'){const div=document.createElement('div'); div.className=`msg ${who}`; div.textContent=text; $('#chat').appendChild(div); $('#chat').scrollTop=$('#chat').scrollHeight;}
function ask(){
  const item = getLesson(); const text = $('#askInput').value.trim(); if(!text || !item) return;
  addMsg(text,'user'); $('#askInput').value='';
  const points = item.keypoints.slice(0,4).join('；');
  let answer = `围绕《${item.title}》，可以先抓住：${points}。教材位置是书本 ${item.pageLabel}，PDF 第 ${item.pdfPage} 页。`;
  if(text.includes('题')) answer = `给你一道练习：请说明“${item.title}”中最重要的一个概念，并举一个教材或生活中的例子。答题时要包含关键词、理由和结论。`;
  if(text.includes('错')) answer = `本节易错点通常有三类：只背标题不理解概念；忽略教材图表或材料；做题时没有写出判断依据。建议回到 PDF 第 ${item.pdfPage} 页核对。`;
  if(text.includes('总结')) answer = `三句话总结：本节主题是“${item.title}”。核心知识包括：${points}。学习闭环是读教材、列知识点、做测试、订正解释。`;
  addMsg(answer,'bot');
}
init();
</script>
</body>
</html>
'''

(ROOT / "index.html").write_text(HTML, encoding="utf-8")
print("Wrote index.html")
