window.NTBridge.ready.then(function(){
(function () {
  'use strict';
  var data = window.OTO_ALL_DATA;
  if (!data) return;
  var esc = function (v) { return String(v).replace(/[&<>"']/g, function (c) { return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]; }); };
  function shuffle(input) {
    var a=input.slice();
    for(var i=a.length-1;i>0;i--) {var j=Math.floor(Math.random()*(i+1)),t=a[i];a[i]=a[j];a[j]=t;}
    return a;
  }
  function shuffledOrder(n) {
    var a=shuffle(Array.from({length:n},function (_,i) {return i;}));
    if(n>1 && a.every(function (v,i) {return v===i;})) a.push(a.shift());
    return a;
  }
  function permutation(a,n) {return Array.isArray(a)&&a.length===n&&new Set(a).size===n&&a.every(function (v) {return Number.isInteger(v)&&v>=0&&v<n;});}
  function normal(v) {return String(v).toLowerCase().normalize('NFD').replace(/[\u0300-\u036f]/g,'').replace(/đ/g,'d').replace(/[^a-z0-9]/g,'');}
  document.querySelectorAll('.c2-lab[data-lesson]').forEach(function (root) {
    var lesson=data.lessons[root.dataset.lesson];
    if(!lesson) return;
    var prefix=root.dataset.rootPrefix||'../',key='oto-cap2-v3:'+lesson.code,storageOK=true,timer=null;
    var state={view:'explore',figure:0,mode:'learn',part:null,challenge:null,identified:{},idFeedback:'',idCorrect:false,
      sim:0,step:0,playing:false,speed:2,exercise:0,picked:null,notice:'',ex:{}};
    function blank(ex) {
      return {checked:false,answer:null,order:shuffledOrder(ex.type==='predict'?ex.options.length:ex.type==='order'?ex.items.length:ex.targets.length),values:{}};
    }
    lesson.exercises.forEach(function (ex) {state.ex[ex.id]=blank(ex);});
    try {
      var stored=JSON.parse(window.NTBridge.storage.getItem(key)||'null');
      if(!stored && lesson.chapter===2) {var legacy=JSON.parse(window.NTBridge.storage.getItem('oto-chuong2-v2:'+lesson.code)||'null');if(legacy&&legacy.ex){stored=legacy;stored.version=data.version;}}
      if(stored && stored.version===data.version) {
        lesson.exercises.forEach(function (ex) {
          if(stored.contentRevision!==data.contentRevision&&(data.revisedExercises[lesson.code]||[]).includes(ex.id))return;
          var old=stored.ex&&stored.ex[ex.id],s=state.ex[ex.id];
          if(!old || typeof old!=='object') return;
          if(permutation(old.order,s.order.length)) s.order=old.order;
          if(ex.type==='predict' && Number.isInteger(old.answer)&&old.answer>=0&&old.answer<ex.options.length) s.answer=old.answer;
          if(ex.type==='label' && old.values && typeof old.values==='object') ex.targets.forEach(function (id) {
            if(typeof old.values[id]==='string') s.values[id]=old.values[id].slice(0,200);
          });
          if(ex.type==='match' && old.values && typeof old.values==='object') {
            var seen=[];
            ex.targets.forEach(function (id) {var v=old.values[id];if(Number.isInteger(v)&&v>=0&&v<ex.targets.length&&seen.indexOf(v)<0){s.values[id]=v;seen.push(v);}});
          }
          s.checked=old.checked===true;
        });
        if(stored.identified && typeof stored.identified==='object') lesson.figures.forEach(function (fig) {
          var ids=stored.identified[fig.id];if(Array.isArray(ids)) state.identified[fig.id]=Array.from(new Set(ids.filter(function (id) {return fig.parts.some(function (p) {return p.id===id;});})));
        });
      }
    } catch(_) {storageOK=false;}
    function persist() {
      try {window.NTBridge.storage.setItem(key,JSON.stringify({version:data.version,contentRevision:data.contentRevision,ex:state.ex,identified:state.identified,updatedAt:new Date().toISOString()}));}
      catch(_) {storageOK=false;}
    }
    function exFigure(ex) {return lesson.figures.find(function (f) {return f.id===ex.figure;});}
    function targetParts(ex) {var f=exFigure(ex);return ex.targets.map(function (id) {return f.parts.find(function (p) {return p.id===id;});});}
    function evaluate(ex) {
      var s=state.ex[ex.id],details=[],correct=0,total=1;
      if(ex.type==='predict') {
        correct=s.answer===ex.answer?1:0;
        details.push('Đáp án: '+ex.options[ex.answer]);
      } else if(ex.type==='order') {
        total=ex.items.length;correct=s.order.filter(function (v,i) {return v===i;}).length;
        details=ex.items.map(function (v,i) {return (i+1)+'. '+v;});
      } else {
        var parts=targetParts(ex);total=parts.length;
        parts.forEach(function (p,i) {
          var ok=ex.type==='label'?p.aliases.some(function (a) {return normal(a)===normal(s.values[p.id]||'');}):s.values[p.id]===i;
          if(ok) correct++;
          details.push('Vị trí '+p.id+': '+p.name+' — '+(ok?'đúng':(ex.type==='label'?'cần sửa':'cần ghép lại'))+'. '+p.short);
        });
      }
      return {correct:correct,total:total,passed:correct===total,details:details};
    }
    function ready(ex) {
      var s=state.ex[ex.id];
      if(ex.type==='predict') return Number.isInteger(s.answer);
      if(ex.type==='order') return true;
      return ex.targets.every(function (id) {return ex.type==='label'?!!String(s.values[id]||'').trim():Number.isInteger(s.values[id]);});
    }
    function btn(action,label,attrs,cls) {
      return '<button type="button" class="c2-btn '+(cls||'')+'" data-c2-action="'+action+'" '+(attrs||'')+'>'+esc(label)+'</button>';
    }
    function calloutLines(parts) {
      return '<svg class="all-callouts" viewBox="0 0 100 100" preserveAspectRatio="none" aria-hidden="true">'+parts.filter(function(p){return p.markerX!==undefined&&(p.markerX!==p.x||p.markerY!==p.y);}).map(function(p){return '<line x1="'+p.x+'" y1="'+p.y+'" x2="'+p.markerX+'" y2="'+p.markerY+'" stroke="#174d7d" stroke-width="1.3" vector-effect="non-scaling-stroke"/><circle cx="'+p.x+'" cy="'+p.y+'" r=".7" fill="#ce770f"/>';}).join('')+'</svg>';
    }
    function pinboard(fig,mode,targets,values,checked,ex) {
      var parts=targets?fig.parts.filter(function (p) {return targets.indexOf(p.id)>=0;}):fig.parts;
      return '<figure class="c2-figure"><div class="c2-pinboard"><img src="'+esc(prefix+fig.image)+'" alt="'+esc(fig.caption)+'" width="700" loading="lazy">'+calloutLines(parts)+parts.map(function (p) {
        var cls='',aria='Vị trí '+p.id;
        if(mode==='learn') {aria+=': '+p.name;if(state.part===p.id) cls=' selected';}
        if(mode==='identify' && (state.identified[fig.id]||[]).indexOf(p.id)>=0) cls=' good';
        if(checked && ex) {
          var ix=ex.targets.indexOf(p.id),ok=ex.type==='match'?values[p.id]===ix:p.aliases.some(function (a) {return normal(a)===normal(values[p.id]||'');});
          cls=ok?' good':' bad';
        }
        return '<button type="button" class="c2-pin'+cls+'" style="left:'+(p.markerX===undefined?p.x:p.markerX)+'%;top:'+(p.markerY===undefined?p.y:p.markerY)+'%" data-c2-action="'+(mode==='match'?'slot':mode==='learn'||mode==='identify'?'part':'location')+'" data-part="'+p.id+'" aria-label="'+esc(aria)+'"'+((checked||mode==='label')?' disabled':'')+'>'+p.id+'</button>';
      }).join('')+'</div><figcaption class="c2-caption">'+esc(fig.caption)+(fig.reference2026?' · Tập 2/2026, trang PDF '+fig.reference2026.page:'')+'<br>Bấm hình để phóng lớn. Các điểm chữ được bổ sung cho hoạt động; đường nối mảnh chỉ tới vị trí trên hình. Tên gọi đối chiếu theo bài nguồn. <a href="'+esc(prefix+data.lessons[fig.source].file)+'">Nguồn: bài '+esc(fig.source)+'</a>.</figcaption></figure>';
    }
    function source() {
      var refs=Array.from(new Set(lesson.figures.map(function(f){return f.source;})));
      return '<p class="c2-source">Tên gọi và nội dung đối chiếu các bài '+refs.map(function(code){return '<a href="'+esc(prefix+data.lessons[code].file)+'">'+esc(code)+'</a>';}).join(', ')+'. Sơ đồ nguyên lý giản lược để quan sát quan hệ tác động. Một số tác động xảy ra đồng thời được tách thành bước để học. <a href="'+esc(prefix+'tuong_tac/index.html?chapter='+lesson.chapter)+'">Mục lục chương '+lesson.chapter+'</a> · <a href="'+esc(prefix+'tuong_tac/thuat-ngu.html')+'">Tra thuật ngữ</a>.</p>';
    }
    function gallery() {
      if(!lesson.sourceGallery || !lesson.sourceGallery.length)return '';
      return '<details class="all-source-gallery"><summary>Đối chiếu hình gốc trong bài '+esc(lesson.code)+'</summary><div>'+lesson.sourceGallery.map(function(g){return '<a href="'+esc(prefix+g.image)+'" target="_blank" rel="noopener"><img src="'+esc(prefix+g.image)+'" loading="lazy" alt="'+esc(g.caption)+'"><span>'+esc(g.caption)+'</span></a>';}).join('')+'</div><p class="c2-small">Bấm hình để mở kích thước đầy đủ. Các hình khác có trong phần tài liệu bên dưới.</p></details>';
    }
    function explore() {
      var fig=lesson.figures[state.figure],identified=state.identified[fig.id]||[],learn=state.mode==='learn';
      if(!state.part||!fig.parts.some(function (p) {return p.id===state.part;})) state.part=fig.parts[0].id;
      if(!state.challenge||!fig.parts.some(function (p) {return p.id===state.challenge;})) nextChallenge();
      var chosen=fig.parts.find(function (p) {return p.id===state.part;}),target=fig.parts.find(function (p) {return p.id===state.challenge;});
      var toolbar=lesson.figures.length>1?'<label class="c2-small">Chọn hình <select class="c2-figure-choice" data-c2-select="figure">'+lesson.figures.map(function (f,i) {return '<option value="'+i+'"'+(i===state.figure?' selected':'')+'>'+esc(f.caption)+'</option>';}).join('')+'</select></label>':'';
      var side=learn?'<div class="c2-parts">'+fig.parts.map(function (p) {return '<button type="button" class="c2-part-btn'+(p.id===state.part?' selected':'')+'" data-c2-action="part" data-part="'+p.id+'"><span class="c2-letter">'+p.id+'</span>'+esc(p.name)+'</button>';}).join('')+'</div><div class="c2-info"><h4>'+esc(chosen.name)+'</h4><p>'+esc(chosen.description)+'</p></div>':
        '<div class="c2-info"><h4>'+(identified.length===fig.parts.length?'Đã nhận diện toàn bộ hình':'Hãy tìm: '+esc(target.name))+'</h4><p>Bấm điểm trên hình hoặc chọn vị trí bên dưới. Tên và công dụng chỉ hiện trong chế độ khám phá.</p></div><div class="c2-toolbar" style="margin-top:12px">'+fig.parts.map(function (p) {return btn('part','Vị trí '+p.id,'data-part="'+p.id+'"');}).join('')+'</div><p class="c2-small">Đã nhận diện '+identified.length+'/'+fig.parts.length+' vị trí trong hình này.</p>'+
        (state.idFeedback?'<div class="c2-notice" role="status">'+esc(state.idFeedback)+'</div>':'')+
        (state.idCorrect&&identified.length<fig.parts.length?btn('next-part','Chi tiết tiếp theo',null,'primary'):'')+
        (identified.length===fig.parts.length?btn('reset-identify','Nhận diện lại hình này'):'');
      return '<div class="c2-toolbar">'+btn('learn','Khám phá','aria-pressed="'+learn+'"')+btn('identify','Tự nhận diện','aria-pressed="'+(!learn)+'"')+toolbar+'</div>'+
        '<p class="c2-small">'+(learn?'Bấm điểm chữ hoặc tên ở danh sách để xem công dụng / mô tả.':'Tìm đúng chi tiết được yêu cầu; phản hồi xuất hiện ngay sau khi chọn.')+'</p>'+
        '<div class="c2-figure-layout">'+pinboard(fig,learn?'learn':'identify')+'<div>'+side+'</div></div>'+gallery()+source();
    }
    function nextChallenge() {
      var fig=lesson.figures[state.figure],done=state.identified[fig.id]||[];
      var todo=fig.parts.filter(function (p) {return done.indexOf(p.id)<0;});
      state.challenge=(shuffle(todo)[0]||fig.parts[0]).id;state.idCorrect=false;state.idFeedback='';
    }
    function principle() {
      var sim=lesson.simulations[state.sim],step=sim.steps[state.step];
      var chooser=lesson.simulations.length>1?'<label class="c2-small">Chọn nguyên lý <select class="c2-figure-choice" data-c2-select="sim">'+lesson.simulations.map(function (s,i) {return '<option value="'+i+'"'+(i===state.sim?' selected':'')+'>'+esc(s.title)+'</option>';}).join('')+'</select></label>':'<strong>'+esc(sim.title)+'</strong>';
      return '<div class="c2-toolbar">'+chooser+'</div><div class="c2-sim-frame '+(state.playing?'':'paused')+'" tabindex="0" aria-label="Sơ đồ nguyên lý; có thể cuộn ngang trên màn hình nhỏ">'+
        window.OTO_ALL_SIMULATION.render(sim,step,lesson.code)+'</div>'+window.OTO_ALL_SIMULATION.legend(sim)+
        '<p class="c2-small">Trên màn hình nhỏ có thể kéo ngang sơ đồ. Mũi tên và màu thể hiện quan hệ đang được quan sát; tốc độ nét chạy chỉ giúp theo dõi đường tác động.</p>'+
        '<div class="c2-step-map" aria-label="Chọn bước nguyên lý">'+sim.steps.map(function (s,i) {return '<button type="button" class="c2-step-dot" data-c2-action="step" data-index="'+i+'"'+(i===state.step?' aria-current="step"':'')+' aria-label="Bước '+(i+1)+': '+esc(s.title)+'">'+(i+1)+'</button>';}).join('')+'</div>'+
        '<div class="c2-step-card" aria-live="polite"><p class="c2-small">Bước '+(state.step+1)+' / '+sim.steps.length+'</p><h4>'+esc(step.title)+'</h4><p>'+esc(step.text)+'</p></div>'+
        '<div class="c2-toolbar">'+btn('prev-step','Bước trước',state.step===0?'disabled':'')+btn('play',state.playing?'Dừng':'Chạy từng bước',null,'primary')+btn('next-step','Bước tiếp',state.step===sim.steps.length-1?'disabled':'')+btn('reset-step','Về bước đầu')+
        '<label class="c2-small">Thời gian mỗi bước <select class="c2-figure-choice" data-c2-select="speed">'+[2,4,6].map(function (n) {return '<option value="'+n+'"'+(state.speed===n?' selected':'')+'>'+n+' giây</option>';}).join('')+'</select></label></div>'+source();
    }
    function feedback(ex) {
      var result=evaluate(ex),label=ex.type==='order'?'bước đúng vị trí':ex.type==='predict'?'câu đúng':'vị trí đúng';
      return '<div class="c2-feedback '+(result.passed?'':'wrong')+'" role="status"><h4>'+(result.passed?'Đúng toàn bộ hoạt động':'Cần xem lại')+'</h4><p>'+result.correct+'/'+result.total+' '+label+'.</p><ul>'+result.details.map(function (v) {return '<li>'+esc(v)+'</li>';}).join('')+'</ul><p>'+esc(ex.explanation)+'</p></div>';
    }
    function exercises() {
      var ex=lesson.exercises[state.exercise],s=state.ex[ex.id],checked=s.checked;
      var nav='<div class="c2-ex-nav" role="tablist" aria-label="Các hoạt động thực hành">'+lesson.exercises.map(function (x,i) {
        var status=state.ex[x.id].checked?(evaluate(x).passed?'Đã kiểm tra · đúng':'Đã kiểm tra · cần sửa'):'Chưa kiểm tra';
        return '<button type="button" role="tab" aria-selected="'+(i===state.exercise)+'" aria-controls="c2-ex-panel-'+lesson.code+'" data-c2-action="exercise" data-index="'+i+'"><strong>'+(i+1)+'. '+esc(x.title)+'</strong>'+status+'</button>';
      }).join('')+'</div>';
      var content='';
      if(ex.type==='predict') {
        content='<div class="c2-options" role="radiogroup" aria-label="Chọn dự đoán">'+s.order.map(function (oi) {
          var cls=checked?(oi===ex.answer?' good':oi===s.answer?' bad':''):'';
          return '<label class="c2-option'+cls+'"><input type="radio" name="c2-answer-'+lesson.code+'" value="'+oi+'" data-c2-input="predict"'+(oi===s.answer?' checked':'')+(checked?' disabled':'')+'><span>'+esc(ex.options[oi])+'</span></label>';
        }).join('')+'</div>';
      } else if(ex.type==='order') {
        content='<p class="c2-small">Dùng nút Lên / Xuống hoặc kéo thả để đổi thứ tự. Sắp xếp từ bước đầu tới bước cuối.</p><ol class="c2-order-list">'+s.order.map(function (oi,pos) {
          return '<li class="c2-order-row" draggable="'+(!checked)+'" data-c2-drag="order" data-item="'+oi+'" data-order-position="'+pos+'"><span class="c2-order-number">'+(pos+1)+'</span><span class="c2-order-text">'+esc(ex.items[oi])+'</span><span class="c2-order-controls">'+
            btn('move-up','Lên','data-position="'+pos+'" aria-label="Đưa bước '+(pos+1)+' lên"'+(checked||pos===0?' disabled':''))+
            btn('move-down','Xuống','data-position="'+pos+'" aria-label="Đưa bước '+(pos+1)+' xuống"'+(checked||pos===s.order.length-1?' disabled':''))+'</span></li>';
        }).join('')+'</ol>';
      } else {
        var fig=exFigure(ex),parts=targetParts(ex);
        var side;
        if(ex.type==='label') {
          side='<div class="c2-form">'+parts.map(function (p) {return '<label class="c2-field">Tên chi tiết tại vị trí '+p.id+'<input type="text" autocomplete="off" maxlength="200" data-c2-input="label" data-part="'+p.id+'" value="'+esc(s.values[p.id]||'')+'"'+(checked?' disabled':'')+'></label>';}).join('')+'</div>';
        } else {
          side='<div class="c2-tokens" aria-label="Các công dụng cần ghép">'+s.order.map(function (i) {
            var used=ex.targets.some(function (id) {return s.values[id]===i;});
            return '<button type="button" class="c2-token'+(state.picked===i?' picked':'')+(used?' used':'')+'" data-c2-action="pick" data-token="'+i+'" data-c2-drag="match" draggable="'+(!checked)+'" aria-pressed="'+(state.picked===i)+'"'+(checked?' disabled':'')+'>'+esc(parts[i].short)+(used?' · đã ghép':'')+'</button>';
          }).join('')+'</div><div class="c2-slots">'+parts.map(function (p,i) {
            var token=s.values[p.id],cls=checked?(token===i?' good':' bad'):'';
            return '<div class="c2-slot-row"><button type="button" class="c2-slot'+cls+'" data-c2-action="slot" data-part="'+p.id+'"'+(checked?' disabled':'')+'><strong>Vị trí '+p.id+':</strong> '+(Number.isInteger(token)?esc(parts[token].short):'chưa ghép')+'</button>'+
              btn('clear','×','data-part="'+p.id+'" aria-label="Bỏ ghép vị trí '+p.id+'"'+(checked||!Number.isInteger(token)?' disabled':''))+'</div>';
          }).join('')+'</div>';
        }
        content='<div class="c2-figure-layout">'+pinboard(fig,ex.type,ex.targets,s.values,checked,ex)+'<div>'+side+'</div></div>';
      }
      return nav+'<div id="c2-ex-panel-'+lesson.code+'" role="tabpanel"><p class="c2-kicker">Hoạt động '+(state.exercise+1)+' / '+lesson.exercises.length+'</p><h3 class="c2-question">'+esc(ex.prompt)+'</h3>'+content+
        (state.notice?'<div class="c2-notice" role="status">'+esc(state.notice)+'</div>':'')+
        (checked?feedback(ex):'')+'<div class="c2-actions">'+
        (checked?btn('retry-ex','Làm lại hoạt động'):btn('check-ex','Kiểm tra',ready(ex)?'':'disabled','primary'))+
        (state.exercise<lesson.exercises.length-1?btn('next-ex','Hoạt động tiếp'):'')+btn('to-principle','Xem lại nguyên lý')+'</div></div>'+source();
    }
    function render(restoreFocus) {
      var active=document.activeElement,focusData=null;
      if(restoreFocus&&root.contains(active)) {
        focusData={action:active.dataset.c2Action,input:active.dataset.c2Input,part:active.dataset.part,index:active.dataset.index,position:active.dataset.position,token:active.dataset.token,value:active.value};
      }
      var checked=lesson.exercises.filter(function (x) {return state.ex[x.id].checked;}).length;
      var passed=lesson.exercises.filter(function (x) {return state.ex[x.id].checked&&evaluate(x).passed;}).length;
      root.innerHTML='<div class="c2-head"><div class="c2-kicker">Chương '+lesson.chapter+' · '+esc(lesson.chapterTitle)+'</div><h2>'+esc(lesson.code+' · '+lesson.title)+'</h2><ul class="c2-objectives">'+lesson.objectives.map(function (v) {return '<li>'+esc(v)+'</li>';}).join('')+'</ul><div class="c2-statusline"><span class="c2-chip">'+lesson.figures.length+' hình tương tác</span><span class="c2-chip">4 hoạt động trong bài</span><span class="c2-chip">Đã kiểm tra '+checked+'/4 · đúng trọn vẹn '+passed+'/4</span><span class="c2-chip">'+(storageOK?'Lưu trên trình duyệt khi được phép':'Đang dùng trong phiên; trình duyệt chưa cho lưu')+'</span></div></div>'+
        '<div class="c2-tabs" role="tablist" aria-label="Chọn cách học">'+[['explore','1. Khám phá hình'],['principle','2. Nguyên lý từng bước'],['exercises','3. Thực hành']].map(function (entry) {
          return '<button type="button" role="tab" class="c2-tab" data-c2-action="view" data-view="'+entry[0]+'" id="c2-tab-'+lesson.code+'-'+entry[0]+'" aria-controls="c2-panel-'+lesson.code+'" aria-selected="'+(state.view===entry[0])+'">'+entry[1]+'</button>';
        }).join('')+'</div><div class="c2-panel" id="c2-panel-'+lesson.code+'" role="tabpanel" aria-labelledby="c2-tab-'+lesson.code+'-'+state.view+'">'+(state.view==='explore'?explore():state.view==='principle'?principle():exercises())+'</div>';
      if(focusData) {
        var selector=focusData.action?'[data-c2-action="'+focusData.action+'"]':focusData.input?'[data-c2-input="'+focusData.input+'"]':null;
        if(selector) {
          var el=Array.from(root.querySelectorAll(selector)).find(function (candidate) {
            return (!focusData.part||candidate.dataset.part===focusData.part)&&(!focusData.index||candidate.dataset.index===focusData.index)&&(!focusData.position||candidate.dataset.position===focusData.position)&&(!focusData.token||candidate.dataset.token===focusData.token)&&(!focusData.input||candidate.value===focusData.value);
          });
          if(el&&!el.disabled) el.focus({preventScroll:true});
        }
      }
    }
    function stop() {if(timer!==null){clearInterval(timer);timer=null;}state.playing=false;}
    function play() {
      stop();var sim=lesson.simulations[state.sim];
      if(state.step>=sim.steps.length-1) state.step=0;
      state.playing=true;
      timer=setInterval(function () {
        if(state.view!=='principle'||document.hidden){stop();render(true);return;}
        state.step++;
        if(state.step>=sim.steps.length-1){state.step=sim.steps.length-1;stop();}
        render(true);
      },state.speed*1000);
    }
    function assign(id,token) {
      var ex=lesson.exercises[state.exercise],s=state.ex[ex.id];
      if(ex.type!=='match'||s.checked||ex.targets.indexOf(id)<0||!Number.isInteger(token)||token<0||token>=ex.targets.length) return;
      var old=s.values[id],other=ex.targets.find(function (p) {return p!==id&&s.values[p]===token;});
      if(other) {if(Number.isInteger(old)) s.values[other]=old;else delete s.values[other];}
      s.values[id]=token;state.picked=null;state.notice='Đã ghép tại vị trí '+id+'. Có thể đổi mô tả hoặc bấm × để bỏ ghép.';persist();render(true);
    }
    function changeExercise(index) {
      if(!Number.isInteger(index)||index<0||index>=lesson.exercises.length) return;
      state.exercise=index;state.picked=null;state.notice='';render(true);
    }
    root.addEventListener('click',function (event) {
      var button=event.target.closest('button[data-c2-action]');
      if(!button||button.disabled) return;
      var action=button.dataset.c2Action,ex=lesson.exercises[state.exercise],s=state.ex[ex.id];
      if(action==='view') {stop();state.view=button.dataset.view;state.notice='';render(false);root.querySelector('[data-view="'+state.view+'"]').focus({preventScroll:true});return;}
      if(action==='learn'||action==='identify') {state.mode=action;state.idFeedback='';state.idCorrect=false;if(action==='identify')nextChallenge();render(true);return;}
      if(action==='part') {
        var fig=lesson.figures[state.figure],id=button.dataset.part;
        if(state.mode==='learn'){state.part=id;render(true);return;}
        if(state.idCorrect) return;
        if(id===state.challenge) {
          var ids=state.identified[fig.id]||[];if(ids.indexOf(id)<0)ids.push(id);state.identified[fig.id]=ids;
          state.idFeedback='Đúng: vị trí '+id+' là '+fig.parts.find(function (p) {return p.id===id;}).name+'.';state.idCorrect=true;persist();
        } else state.idFeedback='Chưa đúng. Hãy quan sát lại vị trí của chi tiết được yêu cầu và thử tiếp.';
        render(true);return;
      }
      if(action==='next-part'){nextChallenge();render(true);return;}
      if(action==='reset-identify'){state.identified[lesson.figures[state.figure].id]=[];nextChallenge();persist();render(true);return;}
      if(action==='play'){if(state.playing)stop();else play();render(true);return;}
      if(action==='prev-step'||action==='next-step'||action==='reset-step'||action==='step') {
        stop();var max=lesson.simulations[state.sim].steps.length-1;
        state.step=action==='reset-step'?0:action==='step'?Number(button.dataset.index):state.step+(action==='next-step'?1:-1);
        state.step=Math.max(0,Math.min(max,state.step));render(true);return;
      }
      if(action==='exercise'){changeExercise(Number(button.dataset.index));return;}
      if(action==='next-ex'){changeExercise(state.exercise+1);return;}
      if(action==='to-principle'){state.view='principle';render(false);root.querySelector('[data-view="principle"]').focus({preventScroll:true});return;}
      if(action==='retry-ex'){state.ex[ex.id]=blank(ex);state.picked=null;state.notice='';persist();render(false);return;}
      if(s.checked) return;
      if(action==='check-ex'){if(ready(ex)){window.NTBridge.emit({type:'checked',code:lesson.code,exercise:ex.id,passed:evaluate(ex).passed});s.checked=true;state.notice='';state.picked=null;persist();render(false);var panel=root.querySelector('.c2-feedback');if(panel){panel.tabIndex=-1;panel.focus({preventScroll:true});}}return;}
      if(action==='pick'){state.picked=Number(button.dataset.token);state.notice='Đã chọn mô tả. Bấm điểm trên hình hoặc nút vị trí để ghép.';render(true);return;}
      if(action==='slot'){if(state.picked===null){state.notice='Chọn một mô tả trước khi ghép.';render(true);}else assign(button.dataset.part,state.picked);return;}
      if(action==='clear'){delete s.values[button.dataset.part];persist();render(true);return;}
      if(action==='move-up'||action==='move-down') {
        var pos=Number(button.dataset.position),to=pos+(action==='move-up'?-1:1);
        if(to>=0&&to<s.order.length){var item=s.order[pos];s.order[pos]=s.order[to];s.order[to]=item;persist();render(false);root.querySelector('[data-order-position="'+to+'"] [data-c2-action="'+action+'"]')?.focus({preventScroll:true});}return;
      }
    });
    root.addEventListener('input',function (event) {
      if(event.target.dataset.c2Input!=='label') return;
      var ex=lesson.exercises[state.exercise],s=state.ex[ex.id];if(ex.type!=='label'||s.checked)return;
      s.values[event.target.dataset.part]=event.target.value;persist();
      var check=root.querySelector('[data-c2-action="check-ex"]');if(check)check.disabled=!ready(ex);
    });
    root.addEventListener('change',function (event) {
      var field=event.target,select=field.dataset.c2Select;
      if(select==='figure'){var n=Number(field.value);if(n>=0&&n<lesson.figures.length){state.figure=n;state.part=null;state.challenge=null;state.idCorrect=false;state.idFeedback='';render(false);}return;}
      if(select==='sim'){stop();state.sim=Number(field.value);state.step=0;render(false);return;}
      if(select==='speed'){var running=state.playing;state.speed=Number(field.value);if(running)play();render(false);return;}
      if(field.dataset.c2Input==='predict') {
        var ex=lesson.exercises[state.exercise],s=state.ex[ex.id],value=Number(field.value);
        if(ex.type==='predict'&&!s.checked&&Number.isInteger(value)&&value>=0&&value<ex.options.length){s.answer=value;persist();render(true);}
      }
    });
    root.addEventListener('keydown',function (event) {
      var tab=event.target.closest('[role="tab"]');if(!tab || !['ArrowLeft','ArrowRight','Home','End'].includes(event.key))return;
      var list=tab.closest('[role="tablist"]'),tabs=Array.from(list.querySelectorAll('[role="tab"]')),i=tabs.indexOf(tab);
      var next=event.key==='Home'?0:event.key==='End'?tabs.length-1:(i+(event.key==='ArrowRight'?1:-1)+tabs.length)%tabs.length;
      event.preventDefault();tabs[next].click();
      var newList=list.classList.contains('c2-ex-nav')?root.querySelector('.c2-ex-nav'):root.querySelector('.c2-tabs');
      newList.querySelectorAll('[role="tab"]')[next].focus({preventScroll:true});
    });
    root.addEventListener('dragstart',function (event) {
      var el=event.target.closest('[data-c2-drag]'),ex=lesson.exercises[state.exercise];
      if(!el||state.view!=='exercises'||state.ex[ex.id].checked){event.preventDefault();return;}
      event.dataTransfer.setData('text/plain',JSON.stringify({scope:lesson.code,type:el.dataset.c2Drag,value:Number(el.dataset.token||el.dataset.item)}));event.dataTransfer.effectAllowed='move';
    });
    root.addEventListener('dragover',function (event) {
      var dest=event.target.closest('[data-c2-action="slot"],[data-order-position]');
      if(dest&&!state.ex[lesson.exercises[state.exercise].id].checked){event.preventDefault();dest.classList.add('dragover');event.dataTransfer.dropEffect='move';}
    });
    root.addEventListener('dragleave',function (event) {var dest=event.target.closest('.dragover');if(dest)dest.classList.remove('dragover');});
    root.addEventListener('drop',function (event) {
      var dest=event.target.closest('[data-c2-action="slot"],[data-order-position]');if(!dest)return;
      event.preventDefault();dest.classList.remove('dragover');
      var payload;try{payload=JSON.parse(event.dataTransfer.getData('text/plain'));}catch(_){return;}
      var ex=lesson.exercises[state.exercise],s=state.ex[ex.id];
      if(!payload||payload.scope!==lesson.code||s.checked||!Number.isInteger(payload.value))return;
      if(payload.type==='match'&&ex.type==='match')assign(dest.dataset.part,payload.value);
      else if(payload.type==='order'&&ex.type==='order') {
        var from=s.order.indexOf(payload.value),to=Number(dest.dataset.orderPosition);
        if(from>=0&&Number.isInteger(to)&&to>=0&&to<s.order.length){s.order.splice(to,0,s.order.splice(from,1)[0]);persist();render(false);}
      }
    });
    document.addEventListener('visibilitychange',function () {if(document.hidden&&state.playing){stop();render(false);}});
    window.addEventListener('pagehide',stop);
    render(false);
  });
}());

});
