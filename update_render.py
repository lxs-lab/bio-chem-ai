"""
更新 index_new.html 中的渲染逻辑以支持年级→学期分层
"""
with open(r'E:\Applications in E\workBuddy\2026~AI课程\bio-chem-ai\index_new.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# ===== 1. renderCourseCards (line 544-556) =====
new_renderCourseCards = '''// ============ HOME: COURSE CARDS ============
function renderCourseCards() {
  const grid = document.getElementById('courseGrid');
  grid.innerHTML = Object.entries(SUBJECTS).map(([id, s]) => {
    const gradeSet = new Set(s.semesters.map(sm => sm.grade));
    const grades = [...gradeSet].sort().map(g => g + '年级').join('·');
    const totalItems = s.semesters.reduce((sum, sm) => sum + sm.count, 0);
    return `<div class="course-card" style="--cc-accent:${s.color}" onclick="openGradeSemesterModal('${id}')">
      <span class="cc-icon">${s.icon}</span>
      <div class="cc-name">${s.name}</div>
      <div class="cc-grade">${grades} · ${totalItems}个知识点</div>
      <div class="cc-desc">点击选择年级学期开始学习</div>
    </div>`;
  }).join('');
}
'''

# ===== 2. openGradeModal → openGradeSemesterModal (line 558-589) =====
new_grade_modal = '''// ============ GRADE-SEMESTER MODAL ============
let currentSemester = '';

function openGradeSemesterModal(subjId) {
  const s = SUBJECTS[subjId];
  if (!s) return;
  
  document.getElementById('gmIcon').textContent = s.icon;
  document.getElementById('gmTitle').textContent = s.name;
  document.getElementById('gmSubtitle').textContent = '请选择年级和学期';
  
  const semesters = s.semesters;
  const gradesDiv = document.getElementById('gmGrades');
  
  // Group by grade
  const byGrade = {};
  semesters.forEach(sm => {
    if (!byGrade[sm.grade]) byGrade[sm.grade] = [];
    byGrade[sm.grade].push(sm);
  });
  
  let html = '';
  for (const [grade, sems] of Object.entries(byGrade).sort()) {
    html += `<div style="margin-bottom:12px">
      <div style="font-weight:700;color:var(--gray-500);font-size:.8rem;margin-bottom:6px">${GRADE_NAMES[grade] || grade+'年级'}</div>`;
    sems.sort((a,b) => a.semester.localeCompare(b.semester)).forEach(sm => {
      html += `<button class="grade-btn" data-grade="${sm.grade}" data-sem="${sm.semester}" onclick="selectGradeSemester(this,${sm.grade},'${sm.semester}')">
        ${SEM_NAMES[sm.semester] || sm.semester} <span style="font-size:.7rem;opacity:.7">(${sm.count}个知识点)</span>
      </button>`;
    });
    html += '</div>';
  }
  gradesDiv.innerHTML = html;
  
  currentSubject = subjId;
  currentGrade = semesters[0]?.grade || 7;
  currentSemester = semesters[0]?.semester || '上';
  
  document.getElementById('gradeModal').style.display = 'flex';
}

function selectGradeSemester(btn, grade, sem) {
  document.querySelectorAll('#gmGrades .grade-btn').forEach(b => b.classList.remove('selected'));
  btn.classList.add('selected');
  currentGrade = grade;
  currentSemester = sem;
}

function closeGradeModal() {
  document.getElementById('gradeModal').style.display = 'none';
}

function confirmGrade() {
  closeGradeModal();
  navigateTo('syllabus', currentSubject);
}
'''

# ===== 3. renderSyllabus (line 591-670) =====
new_renderSyllabus = '''// ============ SYLLABUS (CHAPTER OUTLINE) ============
function renderSyllabus() {
  const s = SUBJECTS[currentSubject];
  if (!s) return;
  
  const semName = SEM_NAMES[currentSemester] || currentSemester;
  const gradeName = GRADE_NAMES[currentGrade] || currentGrade + '年级';
  
  document.getElementById('syIcon').textContent = s.icon;
  document.getElementById('syTitle').textContent = s.name + ' · ' + gradeName + semName;
  document.getElementById('sySubtitle').textContent = '人教版 · 2024版 · ' + (ALL_DATA[currentSubject] || []).filter(i => i.grade === currentGrade && i.semester === currentSemester).length + '个知识点';
  document.getElementById('syBreadcrumb').innerHTML = 
    `<span onclick="navigateTo('home')" style="cursor:pointer;color:var(--blue-500)">首页</span> / <span onclick="openGradeSemesterModal('${currentSubject}')" style="cursor:pointer;color:var(--blue-500)">${s.name}</span> / <span class="current">${gradeName}${semName}</span>`;
  
  // Filter items by grade + semester
  const allItems = (ALL_DATA[currentSubject] || []);
  const items = allItems.filter(i => i.grade === currentGrade && i.semester === currentSemester);
  
  if (items.length === 0) {
    document.getElementById('syContent').innerHTML = '<div style="text-align:center;padding:40px;color:var(--gray-400)">暂无该学期数据，请选择其他学期</div>';
    return;
  }
  
  // Group by unit
  const units = {};
  items.forEach(item => {
    const unitKey = item.unit || '未分类';
    if (!units[unitKey]) units[unitKey] = { name: unitKey, chapters: {} };
    const chKey = item.chapter || '其他';
    if (!units[unitKey].chapters[chKey]) units[unitKey].chapters[chKey] = [];
    units[unitKey].chapters[chKey].push(item);
  });
  
  let html = '';
  let unitIdx = 0;
  Object.entries(units).forEach(([unitKey, unitData]) => {
    unitIdx++;
    html += `<div style="margin-bottom:20px">
      <div style="font-size:.95rem;font-weight:700;color:var(--gray-700);margin-bottom:10px;display:flex;align-items:center;gap:8px">
        <span style="width:28px;height:28px;border-radius:8px;background:var(--blue-100);color:var(--blue-700);display:flex;align-items:center;justify-content:center;font-size:.75rem;font-weight:700">${unitIdx}</span>
        ${unitKey}
      </div>`;
    
    Object.entries(unitData.chapters).forEach(([chKey, sections]) => {
      const chId = 'ch-' + unitIdx + '-' + chKey.replace(/[^a-zA-Z0-9\\u4e00-\\u9fff]/g,'');
      html += `<div class="chapter-card" id="${chId}">
        <div class="chapter-header" onclick="toggleChapter('${chId}')">
          <div class="ch-left">
            <div class="ch-num">${chKey.length > 8 ? chKey.substring(0,8)+'…' : chKey}</div>
            <span class="ch-title">${chKey.length > 24 ? chKey.substring(0,24)+'…' : chKey}</span>
            <span class="ch-count">${sections.length}节</span>
          </div>
          <span class="ch-arrow">▼</span>
        </div>
        <div class="chapter-body">`;
      
      sections.forEach(sec => {
        html += `<div class="section-item" onclick="openSectionById('${sec.id}')">
          <span class="si-dot"></span>
          <span class="si-title">${sec.title.length > 40 ? sec.title.substring(0,40)+'…' : sec.title}</span>
          <span class="si-badge">学习</span>
        </div>`;
      });
      
      html += `</div></div>`;
    });
    html += '</div>';
  });
  
  document.getElementById('syContent').innerHTML = html;
  
  // Update semester switcher
  updateSemesterSwitcher();
}

function updateSemesterSwitcher() {
  const s = SUBJECTS[currentSubject];
  if (!s) return;
  const switcher = document.getElementById('sySemesterSwitcher');
  if (!switcher) return;
  
  let html = '';
  s.semesters.forEach(sm => {
    const isActive = sm.grade === currentGrade && sm.semester === currentSemester;
    html += `<button class="sem-btn${isActive ? ' active' : ''}" onclick="switchSemester(${sm.grade},'${sm.semester}')">${GRADE_NAMES[sm.grade]}${SEM_NAMES[sm.semester]}</button>`;
  });
  switcher.innerHTML = html;
}

function switchSemester(grade, sem) {
  currentGrade = grade;
  currentSemester = sem;
  renderSyllabus();
  window.scrollTo({ top: 0, behavior: 'smooth' });
}
'''

# ===== 4. 需要替换的 CSS（学期切换器样式）=====
# 找到 </style> 前插入样式

# 现在执行替换
# 找到每个函数的精确行范围并替换

# 替换 renderCourseCards (lines 544-556, 0-indexed: 543-555)
lines[543:556] = [new_renderCourseCards + '\n']

# 替换 openGradeModal → selectGrade → closeGradeModal → confirmGrade (lines 558-589, 0-indexed: 557-588)
lines[557:589] = [new_grade_modal + '\n']

# 替换 renderSyllabus (lines 591-670, 0-indexed: 590-669)
lines[590:670] = [new_renderSyllabus + '\n']

# Write back
with open(r'E:\Applications in E\workBuddy\2026~AI课程\bio-chem-ai\index_new.html', 'w', encoding='utf-8') as f:
    f.writelines(lines)

print("Done! Updated renderCourseCards, grade modal, and renderSyllabus.")
print(f"Total lines: {len(lines)}")
