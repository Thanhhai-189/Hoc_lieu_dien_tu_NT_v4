window.NTBridge.ready.then(function(){
(function () {
  'use strict';
  const data = window.OTO_REVIEW_DATA;
  const root = document.querySelector('.auto-review[data-review-page]');
  if (!root || !data) return;
  const pageId = root.dataset.reviewPage;
  const page = data.pages[pageId];
  if (!page) return;
  const prefix = root.dataset.rootPrefix || '';
  const pool = page.codes.flatMap(code => data.lessons[code].questions);
  const byId = new Map(pool.map(q => [q.id, q]));
  const key = 'oto-on-tap-v1:' + (page.canonical || pageId);
  let storageOK = true;
  let saved = {};
  try { saved = JSON.parse(window.NTBridge.storage.getItem(key) || '{}') || {}; }
  catch (_) { storageOK = false; }
  let attempt = saved.attempt || null;
  function validOrder(order, length) { return Array.isArray(order) && order.length === length && new Set(order).size === length && order.every(i => Number.isInteger(i) && i >= 0 && i < length); }
  if (attempt && (!Array.isArray(attempt.ids) || !attempt.ids.length || new Set(attempt.ids).size !== attempt.ids.length || !attempt.ids.every(id => byId.has(id)) || !attempt.orders || !attempt.answers || !attempt.checked || !attempt.ids.every(id => validOrder(attempt.orders[id], byId.get(id).type === 'choice' ? byId.get(id).options.length : byId.get(id).pairs.length)))) attempt = null;
  if (attempt) {
    attempt.pos = Math.max(0, Math.min(attempt.ids.length-1, Number(attempt.pos)||0));
    attempt.ids.forEach(id => {
      const q = byId.get(id), a = attempt.answers[id];
      if (q.type === 'choice') {
        if (!Number.isInteger(a) || a < 0 || a >= q.options.length) delete attempt.answers[id];
      } else if (!Array.isArray(a) || a.length !== q.pairs.length || !a.every(v => v === null || (Number.isInteger(v) && v >= 0 && v < q.pairs.length)) || new Set(a.filter(v => v !== null)).size !== a.filter(v => v !== null).length) delete attempt.answers[id];
    });
  }
  let mode = 'intro', picked = null, notice = '';
  const escape = value => String(value).replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
  const shuffle = input => {
    const a = input.slice();
    for (let i=a.length-1;i>0;i--) { const j=Math.floor(Math.random()*(i+1)); [a[i],a[j]]=[a[j],a[i]]; }
    return a;
  };
  function persist() {
    saved.attempt = attempt;
    try { window.NTBridge.storage.setItem(key, JSON.stringify(saved)); }
    catch (_) { storageOK = false; }
  }
  const done = q => q.type === 'choice' ? Number.isInteger(attempt.answers[q.id]) : Array.isArray(attempt.answers[q.id]) && attempt.answers[q.id].length === q.pairs.length && attempt.answers[q.id].every(v => v !== null && Number.isInteger(v));
  const correct = q => q.type === 'choice' ? attempt.answers[q.id] === q.answer : done(q) && attempt.answers[q.id].every((v,i) => v === i);
  function answersHTML(q, answer) {
    if (q.type === 'choice') return Number.isInteger(answer) ? escape(q.options[answer]) : 'Chưa trả lời';
    return '<ul class="rv-correct-list">' + q.pairs.map((p,i) => '<li>'+escape(p.left)+' → '+(Array.isArray(answer) && Number.isInteger(answer[i]) ? escape(q.pairs[answer[i]].right) : 'Chưa ghép')+'</li>').join('')+'</ul>';
  }
  function correctHTML(q) { return answersHTML(q, q.type === 'choice' ? q.answer : q.pairs.map((_,i) => i)); }
  function pageNumbers(pages) {
    const groups=[]; let start=pages[0], end=start;
    pages.slice(1).forEach(n => { if(n===end+1) end=n; else {groups.push(start===end ? String(start) : start+'–'+end);start=end=n;} });
    groups.push(start===end ? String(start) : start+'–'+end);
    return groups.join(', ');
  }
  function reference(q) {
    const l = data.lessons[q.lesson];
    const topic = l.source_volume === 1 ? 'mục '+l.code : 'Chương '+l.chapter+', '+l.title.replace(/^\d+\.\d+\.\d+\.?\s*/, '');
    return '<p class="rv-reference">Đối chiếu: Cấu tạo ô tô, Tập '+l.source_volume+' · '+escape(topic)+' · trang PDF '+pageNumbers(l.pdf_pages)+'. <a href="'+escape(prefix+l.file)+'">Đọc lại bài học</a></p>';
  }
  function feedback(q) {
    const ok = correct(q);
    return '<div class="rv-feedback '+(ok?'':'wrong')+'" role="status"><h4>'+(ok?'Đúng':'Chưa đúng')+'</h4>'+(!ok?'<div><strong>Đáp án đúng:</strong> '+correctHTML(q)+'</div>':'')+'<p>'+escape(q.explanation)+'</p>'+reference(q)+'</div>';
  }
  function header() {
    const choice = pool.filter(q => q.type==='choice').length, match=pool.length-choice;
    return '<div class="rv-head"><div class="rv-kicker">'+(page.kind==='chapter'?'Ôn tập chương':page.kind==='all'?'Ôn tập toàn học phần':page.kind==='group'?'Ôn tập mục':'Ôn tập bài học')+'</div><h2>Tự kiểm tra sau khi học</h2><p class="rv-subtitle">'+escape(page.title)+'</p><div class="rv-chips"><span class="rv-chip">'+pool.length+' câu trong ngân hàng</span><span class="rv-chip">'+choice+' chọn đáp án</span>'+(match?'<span class="rv-chip">'+match+' kéo thả, ghép đôi</span>':'')+'</div></div>';
  }
  function intro() {
    const resumable = attempt && !attempt.completed;
    const defaultSize = Math.min(12,pool.length);
    const sizeOptions = [...new Set([defaultSize,20,30,pool.length].filter(n => n<=pool.length))].sort((a,b)=>a-b);
    return '<div class="rv-body"><p>Ôn lại công dụng, cấu tạo và nguyên lý hoạt động. Chọn một đáp án đúng hoặc ghép các mô tả với chi tiết tương ứng.</p><div class="rv-tip rv-small">Mỗi câu được tính 1 điểm. Câu ghép đôi cần đúng toàn bộ các cặp để được tính đúng. Bạn có thể kiểm tra từng câu để xem giải thích, rồi xem kết quả cả lượt.</div>'+(pool.length>12?'<div class="rv-size"><label for="rv-question-count">Số câu trong lượt:</label><select id="rv-question-count">'+sizeOptions.map(n=>'<option value="'+n+'"'+(n===defaultSize?' selected':'')+'>'+(n===pool.length?'Toàn bộ '+n+' câu':n+' câu')+'</option>').join('')+'</select></div>':'')+'<div class="rv-actions">'+(resumable?'<button class="rv-button" data-action="resume">Tiếp tục lượt đang làm</button>':'')+'<button class="rv-button '+(resumable?'secondary':'')+'" data-action="new">'+(resumable?'Làm lượt mới':'Bắt đầu ôn tập')+'</button>'+(attempt&&attempt.completed?'<button class="rv-button secondary" data-action="result">Xem kết quả lần gần nhất</button>':'')+'</div><p class="rv-history">'+(saved.best!==undefined?'Kết quả tốt nhất của các lượt ôn: '+Number(saved.best).toFixed(0)+'%. ':'')+(resumable?'Lượt đang làm: '+attempt.ids.map(id=>byId.get(id)).filter(done).length+'/'+attempt.ids.length+' câu đã trả lời. ':'')+'Kết quả được lưu trên trình duyệt đang sử dụng khi trình duyệt cho phép.</p></div>';
  }
  function questionView() {
    const q = byId.get(attempt.ids[attempt.pos]);
    const locked = !!attempt.checked[q.id];
    const answered = attempt.ids.map(id=>byId.get(id)).filter(done).length;
    let controls = '';
    if (q.type==='choice') {
      controls = '<div class="rv-options" role="radiogroup" aria-labelledby="rv-prompt">'+attempt.orders[q.id].map((oi,j) => {
        const selected = attempt.answers[q.id]===oi;
        const cls = locked ? (oi===q.answer?'correct':selected?'incorrect':'') : selected?'selected':'';
        return '<label class="rv-option '+cls+'"><input type="radio" name="rv-answer" value="'+oi+'"'+(selected?' checked':'')+(locked?' disabled':'')+'><span class="rv-letter">'+String.fromCharCode(65+j)+'.</span><span class="rv-option-text">'+escape(q.options[oi])+'</span></label>';
      }).join('')+'</div>';
    } else {
      const a = attempt.answers[q.id] || q.pairs.map(()=>null);
      controls = '<p class="rv-small">Kéo một mô tả vào ô phù hợp. Bạn cũng có thể bấm chọn mô tả, rồi bấm ô cần ghép; dùng Tab và Enter để thao tác bằng bàn phím.</p><div class="rv-match-pool" aria-label="Các mô tả để ghép">'+attempt.orders[q.id].map(i=>'<button class="rv-token '+(picked===i?'picked ':'')+(a.includes(i)?'used':'')+'" data-action="pick" data-token="'+i+'" draggable="'+(!locked)+'" aria-pressed="'+(picked===i)+'"'+(locked?' disabled':'')+'>'+escape(q.pairs[i].right)+(a.includes(i)?'<span class="rv-small"> · đã ghép</span>':'')+'</button>').join('')+'</div><div class="rv-pairs">'+q.pairs.map((p,i)=>'<div class="rv-pair"><span class="rv-left" id="rv-left-'+i+'">'+escape(p.left)+'</span><button class="rv-slot '+(a[i]!==null?'filled ':'')+(locked?(a[i]===i?'correct':'incorrect'):'')+'" data-action="slot" data-slot="'+i+'" aria-labelledby="rv-left-'+i+' rv-value-'+i+'"'+(locked?' disabled':'')+'><span id="rv-value-'+i+'">'+(a[i]!==null?escape(q.pairs[a[i]].right):'Chọn mô tả hoặc thả vào đây')+'</span></button><button class="rv-clear" data-action="clear" data-slot="'+i+'" aria-label="Bỏ ghép '+escape(p.left)+'"'+(locked||a[i]===null?' disabled':'')+'>×</button></div>').join('')+'</div>';
    }
    const map=attempt.ids.map((id,i)=>{const x=byId.get(id);return '<button data-action="goto" data-index="'+i+'" class="'+(i===attempt.pos?'current ':'')+(attempt.checked[id]?(correct(x)?'correct':'incorrect'):done(x)?'answered':'')+'"'+(i===attempt.pos?' aria-current="step"':'')+' aria-label="Câu '+(i+1)+(attempt.checked[id]?(correct(x)?', đúng':', chưa đúng'):done(x)?', đã trả lời':', chưa trả lời')+'">'+(i+1)+'</button>';}).join('');
    return '<div class="rv-body"><div class="rv-topline"><strong>Câu '+(attempt.pos+1)+' / '+attempt.ids.length+'</strong><span class="rv-small">Đã trả lời '+answered+'/'+attempt.ids.length+'</span></div><div class="rv-meter" role="progressbar" aria-label="Tiến độ trả lời" aria-valuemin="0" aria-valuemax="'+attempt.ids.length+'" aria-valuenow="'+answered+'"><span style="width:'+(100*answered/attempt.ids.length)+'%"></span></div><div class="rv-topline"><span class="rv-type">'+(q.type==='choice'?'Chọn một đáp án đúng':'Kéo thả · ghép đôi')+'</span><span class="rv-small">Bài '+escape(q.lesson)+'</span></div><h3 id="rv-prompt" tabindex="-1">'+escape(q.prompt)+'</h3>'+controls+(locked?feedback(q):'<button class="rv-button secondary" data-action="check"'+(!done(q)?' disabled':'')+'>Kiểm tra câu này</button>')+'<div class="rv-footer"><div class="rv-actions"><button class="rv-button secondary" data-action="prev"'+(attempt.pos===0?' disabled':'')+'>Câu trước</button><button class="rv-button" data-action="next"'+(attempt.pos===attempt.ids.length-1?' disabled':'')+'>Câu tiếp</button><button class="rv-button secondary" data-action="finish">Kết thúc và chấm điểm</button></div><div class="rv-map" role="group" aria-label="Chuyển tới câu hỏi">'+map+'</div><p class="rv-small" style="margin-top:10px">Câu chưa trả lời được tính chưa đúng khi kết thúc lượt.</p><div class="rv-status" role="status" aria-live="polite">'+escape(notice)+'</div></div></div>';
  }
  function resultView() {
    const items=attempt.ids.map(id=>byId.get(id));
    const n=items.filter(correct).length, percent=Math.round(100*n/items.length), skipped=items.filter(q=>!done(q)).length;
    return '<div class="rv-body"><div class="rv-score"><div class="rv-score-circle">'+percent+'%</div><div><h3>'+n+' / '+items.length+' câu đúng</h3><p>Điểm quy đổi: '+(10*n/items.length).toFixed(1)+' / 10'+(skipped?' · '+skipped+' câu chưa trả lời':'')+'</p><p class="rv-small">'+(n===items.length?'Bạn đã trả lời đúng toàn bộ lượt ôn này.':'Mở từng câu bên dưới để xem đáp án và giải thích.')+(attempt.isRetry?' Đây là lượt ôn lại câu chưa đúng.':'')+'</p></div></div><div class="rv-actions">'+(n<items.length?'<button class="rv-button" data-action="retry">Ôn lại câu chưa đúng</button>':'')+'<button class="rv-button secondary" data-action="new">Làm lượt mới</button><button class="rv-button secondary" data-action="print">In kết quả</button></div><p class="rv-small" style="margin-top:14px">'+(storageOK?'Kết quả đã được lưu trên trình duyệt này.':'Kết quả đang hiển thị trong phiên này; trình duyệt chưa cho phép lưu.')+'</p><div class="rv-result-list">'+items.map((q,i)=>'<details class="rv-result-item"><summary><span class="rv-badge '+(correct(q)?'':'wrong')+'">'+(correct(q)?'Đúng':done(q)?'Chưa đúng':'Chưa trả lời')+'</span>Câu '+(i+1)+'. '+escape(q.prompt)+'</summary><div class="rv-result-content"><div><strong>Bạn trả lời:</strong> '+answersHTML(q,attempt.answers[q.id])+'</div><div><strong>Đáp án đúng:</strong> '+correctHTML(q)+'</div><p>'+escape(q.explanation)+'</p>'+reference(q)+'</div></details>').join('')+'</div></div>';
  }
  function printView() {
    if (!attempt || mode!=='result') return '';
    const items=attempt.ids.map(id=>byId.get(id)), n=items.filter(correct).length;
    return '<div class="rv-print"><h2>Kết quả ôn tập – Học liệu điện tử tương tác</h2><p>'+escape(page.title)+'</p><p>'+n+'/'+items.length+' câu đúng · Điểm '+(10*n/items.length).toFixed(1)+'/10 · '+new Date(attempt.finished).toLocaleString('vi-VN')+'</p>'+items.map((q,i)=>'<article><h4>Câu '+(i+1)+'. '+escape(q.prompt)+'</h4><div><strong>Bạn trả lời:</strong> '+answersHTML(q,attempt.answers[q.id])+'</div><div><strong>Đáp án đúng:</strong> '+correctHTML(q)+'</div><p>'+escape(q.explanation)+'</p>'+reference(q)+'</article>').join('')+'</div>';
  }
  function render(focus) {
    root.innerHTML = '<div class="rv-screen">'+header()+(mode==='intro'?intro():mode==='quiz'?questionView():resultView())+'</div>'+printView();
    if (focus) {
      const el = root.querySelector('#rv-prompt, .rv-body h3, .rv-head h2');
      if (el) {
        el.setAttribute('tabindex', '-1');
        el.focus({preventScroll: true});
        window.NTBridge.reveal(el);
      }
    }
  }
  function newAttempt(ids,isRetry) {
    attempt={ids:shuffle(ids),orders:{},answers:{},checked:{},pos:0,started:new Date().toISOString(),completed:false,isRetry:!!isRetry};
    attempt.ids.forEach(id=>{const q=byId.get(id);attempt.orders[id]=shuffle((q.type==='choice'?q.options:q.pairs).map((_,i)=>i));});
    picked=null;notice='';mode='quiz';persist();render(true);
  }
  function chooseQuestions(count) {
    // Lấy luân phiên từ các bài con để lượt tổng hợp không chỉ lấy một bài.
    const groups=shuffle(page.codes).map(c=>shuffle(data.lessons[c].questions.map(q=>q.id)));
    const selected=[];
    while(selected.length<count && groups.some(g=>g.length)) for(const g of groups) if(g.length && selected.length<count) selected.push(g.pop());
    return selected;
  }
  function assign(slot,token) {
    const q=byId.get(attempt.ids[attempt.pos]);
    if(q.type!=='match'||attempt.checked[q.id]||!Number.isInteger(token)||token<0||token>=q.pairs.length||slot<0||slot>=q.pairs.length)return;
    const a=(attempt.answers[q.id]||q.pairs.map(()=>null)).slice();
    const prior=a.indexOf(token), replaced=a[slot];
    if(prior!==-1&&prior!==slot)a[prior]=replaced;
    a[slot]=token;attempt.answers[q.id]=a;picked=null;notice='Đã ghép. Bạn có thể đổi mô tả hoặc bấm × để bỏ ghép.';persist();render(false);
    const target=root.querySelector('[data-action="slot"][data-slot="'+slot+'"]');if(target)target.focus({preventScroll:true});
  }
  root.addEventListener('change', event=>{
    if(mode!=='quiz'||event.target.name!=='rv-answer')return;
    const q=byId.get(attempt.ids[attempt.pos]);if(attempt.checked[q.id])return;
    const value=Number(event.target.value);if(!Number.isInteger(value)||value<0||value>=q.options.length)return;
    attempt.answers[q.id]=value;notice='';persist();render(false);
    const selected=root.querySelector('input[name="rv-answer"][value="'+value+'"]');if(selected)selected.focus({preventScroll:true});
  });
  root.addEventListener('click', event=>{
    const button=event.target.closest('button[data-action]');if(!button||button.disabled)return;
    const action=button.dataset.action;
    if(action==='new'){const count=Number(root.querySelector('#rv-question-count')?.value)||Math.min(12,pool.length);newAttempt(chooseQuestions(count),false);return;}
    if(action==='resume'){mode='quiz';notice='';render(true);return;}
    if(action==='result'){mode='result';render(true);return;}
    if(action==='print'){window.print();return;}
    if(action==='retry'){newAttempt(attempt.ids.filter(id=>!correct(byId.get(id))),true);return;}
    if(mode!=='quiz')return;
    const q=byId.get(attempt.ids[attempt.pos]);
    if(action==='pick'){picked=Number(button.dataset.token);notice='Đã chọn mô tả. Bấm ô tương ứng để ghép.';render(false);const el=root.querySelector('[data-action="pick"][data-token="'+picked+'"]');if(el)el.focus({preventScroll:true});return;}
    if(action==='slot'){if(picked===null){notice='Chọn một mô tả ở phía trên trước khi ghép.';render(false);}else assign(Number(button.dataset.slot),picked);return;}
    if(action==='clear'){const a=attempt.answers[q.id];if(a){a[Number(button.dataset.slot)]=null;persist();render(false);}return;}
    if(action==='check'){if(done(q)){attempt.checked[q.id]=true;picked=null;notice='';persist();render(false);}return;}
    if(action==='finish'){
      attempt.completed=true;attempt.finished=new Date().toISOString();
      const percent=100*attempt.ids.filter(id=>correct(byId.get(id))).length/attempt.ids.length;
      if(!attempt.isRetry)saved.best=Math.max(Number(saved.best)||0,percent);
      saved.history=(saved.history||[]).concat([{date:attempt.finished,percent,count:attempt.ids.length,isRetry:attempt.isRetry}]).slice(-5);
      window.NTBridge.emit({type:'review-finished',title:page.title,count:attempt.ids.length,correct:attempt.ids.filter(id=>correct(byId.get(id))).length,retry:attempt.isRetry});mode='result';persist();render(true);return;
    }
    if(action==='prev')attempt.pos=Math.max(0,attempt.pos-1);
    if(action==='next')attempt.pos=Math.min(attempt.ids.length-1,attempt.pos+1);
    if(action==='goto')attempt.pos=Math.max(0,Math.min(attempt.ids.length-1,Number(button.dataset.index)));
    picked=null;notice='';persist();render(true);
  });
  root.addEventListener('dragstart', event=>{
    const chip=event.target.closest('[data-token]');if(!chip||chip.disabled||mode!=='quiz')return;
    event.dataTransfer.setData('text/plain',chip.dataset.token);event.dataTransfer.effectAllowed='move';
  });
  root.addEventListener('dragover', event=>{const slot=event.target.closest('[data-slot][data-action="slot"]');if(slot&&!slot.disabled){event.preventDefault();event.dataTransfer.dropEffect='move';slot.classList.add('dragover');}});
  root.addEventListener('dragleave', event=>{const slot=event.target.closest('[data-slot][data-action="slot"]');if(slot)slot.classList.remove('dragover');});
  root.addEventListener('drop', event=>{
    const slot=event.target.closest('[data-slot][data-action="slot"]');if(!slot||slot.disabled)return;
    event.preventDefault();const token=event.dataTransfer.getData('text/plain');if(/^\d+$/.test(token))assign(Number(slot.dataset.slot),Number(token));
  });
  render(false);
}());

});
