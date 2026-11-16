(function(){
 'use strict';
 var data=window.OTO_ALL_DATA,root=document.getElementById('chapter-list');if(!data||!root)return;
 var lessons=Object.values(data.lessons),search=document.getElementById('lesson-search'),chapter=document.getElementById('chapter-filter'),status=document.getElementById('status-filter');
 var esc=function(v){return String(v).replace(/[&<>"']/g,function(c){return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c];});};
 var norm=function(v){return String(v).toLowerCase().normalize('NFD').replace(/[\u0300-\u036f]/g,'').replace(/đ/g,'d').replace(/×/g,'x');};
 var answerNorm=function(v){return norm(v).replace(/[^a-z0-9]/g,'');};
 var storageOK=true;
 function read(lesson){
  try{var s=JSON.parse(localStorage.getItem('oto-cap2-v3:'+lesson.code)||'null');
   if(!s&&lesson.chapter===2){var legacy=JSON.parse(localStorage.getItem('oto-chuong2-v2:'+lesson.code)||'null');if(legacy&&legacy.ex){legacy.version=data.version;s=legacy;}}
   return s&&s.version===data.version?s:null;
  }catch(_){storageOK=false;return null;}
 }
 function passed(lesson,ex,s){
  if(!s||!s.checked)return false;
  if(ex.type==='predict')return s.answer===ex.answer;
  if(ex.type==='order')return Array.isArray(s.order)&&s.order.length===ex.items.length&&s.order.every(function(v,i){return v===i;});
  var f=lesson.figures.find(function(f){return f.id===ex.figure;});
  return ex.targets.every(function(id,i){var p=f.parts.find(function(p){return p.id===id;});return ex.type==='match'?s.values&&s.values[id]===i:p.aliases.some(function(v){return answerNorm(v)===answerNorm(s.values&&s.values[id]||'');});});
 }
 function progress(lesson){var s=read(lesson),n=0,checked=0;if(s)lesson.exercises.forEach(function(ex){var v=s.ex&&s.ex[ex.id];if(v&&v.checked)checked++;if(passed(lesson,ex,v))n++;});return {passed:n,checked:checked,state:n===4?'complete':checked?'active':'new'};}
 function render(){
  var q=norm(search.value).trim(),total=0,checked=0,shown=0,complete=0,ps={};
  lessons.forEach(function(l){var p=progress(l);ps[l.code]=p;total+=p.passed;checked+=p.checked;if(p.passed===4)complete++;});
  document.getElementById('progress-text').textContent=complete+'/102 bài đúng cả 4 hoạt động · '+total+'/408 hoạt động đúng · '+checked+' hoạt động đã kiểm tra';
  document.getElementById('progress-bar').value=total;
  document.getElementById('storage-note').textContent=storageOK?'Kết quả lưu trong trình duyệt này. Sao lưu để chuyển máy hoặc trước khi xóa dữ liệu trình duyệt.':'Trình duyệt đang hạn chế lưu kết quả. Có thể học trong từng phiên; dùng Sao lưu khi trình duyệt cho phép.';
  var text='';
  for(var c=1;c<=12;c++){
   var rows=lessons.filter(function(l){var terms=l.figures.flatMap(function(f){return f.parts.map(function(p){return p.name;});}).join(' ');return l.chapter===c&&(chapter.value==='all'||Number(chapter.value)===c)&&(status.value==='all'||ps[l.code].state===status.value)&&(!q||norm(l.code+' '+l.title+' '+l.chapterTitle+' '+terms).includes(q));});
   if(!rows.length)continue;shown+=rows.length;
   var done=lessons.filter(function(l){return l.chapter===c&&ps[l.code].passed===4;}).length;
   text+='<section class="all-chapter"><div class="all-chapter-title"><h2>'+c+'. '+esc(data.chapters[c])+'</h2><span>'+done+' bài hoàn thành · '+rows.length+' bài đang hiển thị</span></div><div class="c2-grid">'+rows.map(function(l){var p=ps[l.code];return '<a class="c2-card-link '+p.state+'" data-code="'+l.code+'" href="../'+l.file+'#hoc-tuong-tac"><span class="c2-kicker">Bài '+l.code+'</span><h3>'+esc(l.title)+'</h3><p>'+l.figures.length+' hình / sơ đồ tương tác · '+l.simulations.length+' nguyên lý / trình tự</p><div class="all-card-status">'+(p.state==='complete'?'✓ Đúng cả 4 hoạt động':p.checked?'Đã kiểm tra '+p.checked+'/4 · đúng '+p.passed+'/4':'Bắt đầu khám phá và thực hành')+' →</div></a>';}).join('')+'</div></section>';
  }
  root.innerHTML=text||'<p class="c2-info">Chưa có bài phù hợp. Thử đổi từ khóa hoặc bộ lọc.</p>';
  document.getElementById('search-count').textContent='Hiển thị '+shown+' / 102 bài';
 }
 var param=new URLSearchParams(location.search).get('chapter');if(param&&Number(param)>=1&&Number(param)<=12)chapter.value=param;
 search.addEventListener('input',render);chapter.addEventListener('change',render);status.addEventListener('change',render);window.addEventListener('pageshow',render);window.addEventListener('storage',render);
 function notice(t){document.getElementById('catalog-notice').textContent=t;}
 document.getElementById('export-progress').addEventListener('click',function(){
  var records={};lessons.forEach(function(l){var s=read(l);if(s)records[l.code]=s;});
  var result={format:'oto-cap2-progress',schema:1,contentVersion:data.version,exportedAt:new Date().toISOString(),records:records};
  var a=document.createElement('a'),url=URL.createObjectURL(new Blob([JSON.stringify(result,null,2)],{type:'application/json'}));a.href=url;a.download='Ket_qua_hoc_Cau_tao_o_to_'+new Date().toISOString().slice(0,10)+'.json';a.click();setTimeout(function(){URL.revokeObjectURL(url);},1000);notice('Đã tạo tệp sao lưu cho '+Object.keys(records).length+' bài có dữ liệu.');
 });
 function clean(lesson,s){
  if(!s||s.version!==data.version||!s.ex||typeof s.ex!=='object')throw Error('Phiên bản dữ liệu bài không phù hợp.');
  var out={version:data.version,ex:{},identified:{},updatedAt:new Date().toISOString()};
  lesson.exercises.forEach(function(ex){var old=s.ex[ex.id];if(!old)return;var n=ex.type==='predict'?ex.options.length:ex.type==='order'?ex.items.length:ex.targets.length;
   if(!Array.isArray(old.order)||old.order.length!==n||new Set(old.order).size!==n||!old.order.every(function(v){return Number.isInteger(v)&&v>=0&&v<n;}))throw Error('Thứ tự câu trả lời không hợp lệ.');
   var v={order:old.order.slice(),checked:old.checked===true,answer:null,values:{}};
   if(ex.type==='predict'){if(old.answer!==null&&(!Number.isInteger(old.answer)||old.answer<0||old.answer>=n))throw Error('Lựa chọn không hợp lệ.');v.answer=old.answer;}
   if(ex.type==='label'||ex.type==='match')ex.targets.forEach(function(id){var a=old.values&&old.values[id];if(a===undefined)return;if(ex.type==='label'){if(typeof a!=='string'||a.length>200)throw Error('Thuật ngữ nhập không hợp lệ.');v.values[id]=a;}else{if(!Number.isInteger(a)||a<0||a>=n)throw Error('Ghép vị trí không hợp lệ.');v.values[id]=a;}});
   if(ex.type==='match'&&new Set(Object.values(v.values)).size!==Object.keys(v.values).length)throw Error('Một mô tả đang ghép nhiều vị trí.');
   out.ex[ex.id]=v;
  });
  lesson.figures.forEach(function(f){var a=s.identified&&s.identified[f.id];if(Array.isArray(a))out.identified[f.id]=Array.from(new Set(a.filter(function(id){return f.parts.some(function(p){return p.id===id;});})));});
  return out;
 }
 document.getElementById('import-progress').addEventListener('change',async function(){var file=this.files[0];if(!file)return;
  try{if(file.size>10*1024*1024)throw Error('Tệp sao lưu quá lớn.');var backup=JSON.parse(await file.text());if(backup.format!=='oto-cap2-progress'||backup.schema!==1||backup.contentVersion!==data.version||!backup.records||typeof backup.records!=='object')throw Error('Tệp hoặc phiên bản sao lưu không phù hợp.');
   var writes=Object.keys(backup.records).map(function(code){var l=data.lessons[code];if(!l)throw Error('Bài không có trong tài liệu: '+code);return {key:'oto-cap2-v3:'+code,value:JSON.stringify(clean(l,backup.records[code]))};});
   // Validate the whole backup before any write; roll back if storage fails mid-batch.
   var old=writes.map(function(w){return localStorage.getItem(w.key);});
   try{writes.forEach(function(w){localStorage.setItem(w.key,w.value);});}catch(e){writes.forEach(function(w,i){try{if(old[i]===null)localStorage.removeItem(w.key);else localStorage.setItem(w.key,old[i]);}catch(_){}});throw e;}
   render();notice('Đã khôi phục kết quả của '+writes.length+' bài từ tệp sao lưu.');
  }catch(e){notice('Chưa khôi phục: '+e.message);}this.value='';
 });
 render();
}());
