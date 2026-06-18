// ============ QUIZ FUNCTIONS ============
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
