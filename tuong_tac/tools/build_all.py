from pathlib import Path
from html import escape
from lxml import html
import json,re,shutil,copy,unicodedata,subprocess
from figures import FIGURES,render_concept
from specs import SPECS
from wmf_formula import render_equation

PACKAGED=Path(__file__).resolve().parent.name=='tools'
BASE=Path(__file__).resolve().parents[1]
ROOT=Path(__file__).resolve().parents[2] if PACKAGED else BASE/'build/Tai_lieu_dien_tu_Cap2_ToanBo'
ORIGINAL=ROOT/'tuong_tac/tools/source_pages' if PACKAGED else BASE/'audit_411/original'
OUT=ROOT/'tuong_tac'
OUT.mkdir(exist_ok=True)
(OUT/'diagrams').mkdir(exist_ok=True)
bank=json.loads((ROOT/'on_tap/ngan_hang_cau_hoi.json').read_text())
source=json.loads((ROOT/'tuong_tac/tools/source.json' if PACKAGED else BASE/'audit_all/source.json').read_text())
chapter2=json.loads((ROOT/'chuong2/lesson-data.json').read_text())

CHAPTERS={1:'Giới thiệu tổng quát về ô tô',2:'Ly hợp',3:'Hộp số chính',4:'Hộp số tự động',
 5:'Hộp số phân phối',6:'Truyền động các đăng',7:'Cầu chủ động',8:'Cụm bánh xe',
 9:'Hệ thống lái',10:'Hệ thống phanh',11:'Hệ thống treo',12:'Khung vỏ và thiết bị phụ trên ô tô'}
def norm(t):
    t=unicodedata.normalize('NFD',t.lower()).replace('đ','d')
    return re.sub(r'[^a-z0-9]','',t)
def model(spec,code,title=None):
    names=(spec.get('nodes') or '').split('|') if spec.get('nodes') else [p['name'] for p in FIGURES[spec['figure']]['parts']]
    nodes=[dict(id=chr(65+i),label=n) for i,n in enumerate(names)]
    edges=[]
    for token in (spec.get('links') or '').split():
        key,_,kind=token.partition(':')
        edges.append(dict(id=key,from_id=key[0],to_id=key[1],kind=kind or spec['kind']))
    return dict(id='model-'+code.replace('.','-'),kind='graph',channel=spec['kind'],
                title=title or spec.get('sim_title') or 'Nguyên lý: '+source[code]['title'].split(' ',1)[-1],
                nodes=nodes,edges=edges,steps=copy.deepcopy(spec['steps']),source=code)

for fig in FIGURES.values():
    if fig['origin']=='concept':
        (ROOT/fig['image']).write_text(render_concept(fig))

lessons={}
for code,original_lesson in bank['lessons'].items():
    title=re.sub(r'^'+re.escape(code)+r'\.?\s*','',original_lesson['title']).strip()
    if code=='9.2.1':title='Cơ cấu lái kiểu trục vít – bánh vít' # Body and figure 9.3 use the correct name.
    title=' '.join(unicodedata.normalize('NFC',title).split())
    if code.startswith('2.'):
        lesson=copy.deepcopy(chapter2['lessons'][code])
        lesson['title']=title
        for f in lesson['figures']:
            f['origin']='original'
            for p in f['parts']:
                # Only accept names attested in chapter 2; remove colloquial substitutes.
                chapter_text=' '.join(' '.join(s['paragraphs']) for s in source.values() if s['chapter']==2)
                p['aliases']=list(dict.fromkeys([p['name']]+[v for v in p['aliases'] if norm(v) in norm(chapter_text)]))
        for s in lesson['simulations']:s['source']=code
    else:
        spec=SPECS[code]
        figs=[copy.deepcopy(FIGURES[k]) for k in [spec['figure']]+spec.get('extra_figures',[])]
        sims=[model(spec,code)]
        for j,extra in enumerate(spec.get('extra_models',[])):
            extra={**extra,'sim_title':extra['title']}
            s=model(extra,code,extra['title']);s['id']+='-'+str(j+1);sims.append(s)
        q=copy.deepcopy(spec.get('quiz') or next(q for q in original_lesson['questions'] if q['type']=='choice'))
        q['type']='predict';q['id']='predict';q['title']='Dự đoán / vận dụng'
        q.pop('lesson',None)
        f=figs[0];targets=[p['id'] for p in f['parts'][:4]]
        concept=f['origin']=='concept'
        sequence=[s['title'] for s in spec['steps']]
        order_prompt=spec.get('order_prompt') or 'Sắp xếp trình tự quan sát và giải thích trong minh họa: '+sims[0]['title']+'.'
        exercises=[q,dict(id='order',type='order',title='Sắp xếp trình tự',prompt=order_prompt,
          items=sequence,explanation=' '.join(s['text'] for s in spec['steps'])),
          dict(id='label',type='label',title='Điền thuật ngữ',figure=f['id'],targets=targets,
            prompt=('Điền thuật ngữ ứng với các ô kiến thức trên sơ đồ.' if concept else 'Điền tên các chi tiết tại vị trí được đánh dấu trên hình.'),
            explanation='Dùng tên gọi theo tài liệu. Có thể xem lại phần khám phá; khi kiểm tra, chữ hoa và dấu tiếng Việt không ảnh hưởng kết quả.'),
          dict(id='match',type='match',title='Ghép trên hình',figure=f['id'],targets=targets,
            prompt=('Ghép mô tả với đúng ô kiến thức trên sơ đồ.' if concept else 'Ghép công dụng với đúng vị trí chi tiết trên hình.'),
            explanation='Đối chiếu tên gọi và công dụng ở phần khám phá hình; mỗi mô tả chỉ dùng cho một vị trí.')]
        lesson=dict(code=code,title=title,file=original_lesson['file'],figures=figs,simulations=sims,exercises=exercises,
                    objectives=['Nhận diện và gọi đúng các chi tiết hoặc khái niệm trọng tâm trong bài.',
                                'Giải thích '+sims[0]['title'][0].lower()+sims[0]['title'][1:]+'.'])
    lesson['chapter']=original_lesson['chapter']
    lesson['chapterTitle']=CHAPTERS[lesson['chapter']]
    # Local original figures provide direct comparison with the teaching diagram.
    seen=set();gallery=[]
    for im in source[code]['images']:
        name=im['src'].split('/')[-1]
        if name in seen or name.lower().endswith(('.wmf','.emf')):continue
        seen.add(name);gallery.append(dict(image='content/resources/'+name,caption='Hình gốc trong bài '+code))
        if len(gallery)==6:break
    lesson['sourceGallery']=gallery
    lessons[code]=lesson

data=dict(version='2026-10-14-full-v3',storageSchema=1,lessons=lessons,chapters=CHAPTERS,
          scope='102 bài, 12 chương; ba nhóm hoạt động tương tác',originalQuestionBankCount=411)
data['counts']=dict(lessons=len(lessons),chapters=12,figures=sum(len(l['figures']) for l in lessons.values()),
 simulations=sum(len(l['simulations']) for l in lessons.values()),activities=sum(len(l['exercises']) for l in lessons.values()))
# Offset crowded callout buttons while keeping their physical source points unchanged.
from PIL import Image
for l in lessons.values():
    for f in l['figures']:
        if f.get('origin')!='original':continue
        with Image.open(ROOT/f['image']) as im:w,h=im.size
        vh=300*h/w;placed=[]
        for p in f['parts']:
            candidates=[(p['x'],p['y'])]
            for r in [34,50,65,80]:
                for dx,dy in [(0,-1),(0,1),(-1,0),(1,0),(-.7,-.7),(.7,.7),(-.7,.7),(.7,-.7)]:
                    candidates.append((p['x']+dx*r/3,p['y']+dy*r/vh*100))
            for x,y in candidates:
                x=max(6,min(94,x));y=max(4,min(96,y))
                if all(((x-a)*3)**2+((y-b)*vh/100)**2>=33**2 for a,b in placed):break
            p['markerX']=round(x,2);p['markerY']=round(y,2);placed.append((x,y))
(OUT/'lesson-data.json').write_text(json.dumps(data,ensure_ascii=False,indent=2))
(OUT/'lesson-data.js').write_text('window.OTO_ALL_DATA = '+json.dumps(data,ensure_ascii=False,separators=(',',':'))+';\n')

# Render WMF/EMF resources for browser use; retain the originals alongside them.
metafiles=sorted({im['src'].split('/')[-1] for s in source.values() for im in s['images'] if im['src'].lower().endswith(('.wmf','.emf'))})
converted={};conversion=[]
(ROOT/'content/resources/browser').mkdir(exist_ok=True)
for name in metafiles:
    target=ROOT/'content/resources/browser'/str(Path(name).with_suffix('.png'))
    equation=name.lower().endswith('.wmf') and name not in ['T1_image31.wmf','T1_image35.wmf']
    metafile=(ROOT if PACKAGED else ORIGINAL)/'content/resources'/name
    equation_svg=target.with_suffix('.svg')
    if equation and not equation_svg.exists():
        svg=render_equation(metafile);equation_svg.write_text(svg)
        temp_svg=Path('/tmp')/('oto-equation-'+equation_svg.name);temp_svg.write_text(svg)
        temp_png=temp_svg.with_suffix('.png')
        run=subprocess.run(['inkscape',str(temp_svg),'--export-type=png','--export-width=1200',
            '--export-filename='+str(temp_png)],capture_output=True,text=True,timeout=40)
        if run.returncode:raise RuntimeError('Không hiển thị được công thức '+name)
        with Image.open(temp_png) as im:im.load()
        target.write_bytes(temp_png.read_bytes())
    valid=False
    if target.exists():
        try:
            with Image.open(target) as im:im.load()
            valid=True
        except Exception:pass
    if not valid:
        temp=Path('/tmp')/('oto-'+target.name)
        raster_source=equation_svg if equation_svg.exists() else metafile
        run=subprocess.run(['inkscape',str(raster_source),'--export-type=png',
          '--export-width=1200','--export-filename='+str(temp)],capture_output=True,text=True,timeout=40)
        if run.returncode or not temp.exists():raise RuntimeError('Không chuyển được '+name+': '+run.stderr[-300:])
        with Image.open(temp) as im:im.load()
        target.write_bytes(temp.read_bytes())
    converted['content/resources/'+name]='content/resources/browser/'+target.name
    conversion.append(dict(original=name,browser='browser/'+target.name))

def cards(codes,prefix):
    return '<div class="c2-grid">'+''.join('<a class="c2-card-link" href="'+prefix+lessons[c]['file']+'#hoc-tuong-tac">'+
      '<span class="c2-kicker">Bài '+c+'</span><h3>'+escape(lessons[c]['title'])+'</h3><p>Khám phá hình · nguyên lý từng bước · 4 hoạt động</p></a>' for c in codes)+'</div>'

integrated=[]
for file,pmeta in bank['pages'].items():
    if not pmeta['codes'] or file=='all':continue
    raw=(ORIGINAL/file).read_text()
    raw=raw.replace('Skip to content','Chuyển tới nội dung')
    raw=re.sub(r'bánh ví(?!t)','bánh vít',raw)
    prefix='' if file=='index.html' else '../'
    for old,new in converted.items():raw=raw.replace(prefix+old,prefix+new)
    codes=pmeta['codes']
    if len(codes)==1:
        code=codes[0]
        block='<section class="c2-lab" id="hoc-tuong-tac" data-lesson="'+code+'" data-root-prefix="'+prefix+'" aria-label="Học tương tác bài '+code+'"><noscript>Bật JavaScript để sử dụng các hoạt động tương tác.</noscript></section>'
    else:
        block='<section class="c2-catalog inline-catalog" id="hoc-tuong-tac"><p class="c2-kicker">Học tương tác theo bài</p><h2>Khám phá hình, nguyên lý và thực hành</h2>'+cards(codes,prefix)+'</section>'
    raw=raw.replace('</head>','<link rel="stylesheet" href="'+prefix+'tuong_tac/interactive.css">\n</head>')
    marker=re.search(r'<div[^>]+class="page-content"[^>]*>',raw)
    if not marker:raise RuntimeError('Thiếu vị trí chèn '+file)
    raw=raw[:marker.end()]+block+raw[marker.end():]
    raw=raw.replace('</body>','<script src="'+prefix+'tuong_tac/lesson-data.js"></script>\n<script src="'+prefix+'tuong_tac/simulation.js"></script>\n<script src="'+prefix+'tuong_tac/interactive.js"></script>\n</body>')
    nav='<div class="all-quick-nav"><a href="'+prefix+'tuong_tac/index.html">Mục lục tương tác 12 chương</a><a href="#hoc-tuong-tac">Học tương tác</a><a href="'+prefix+'on_tap/index.html">Ôn tập 411 câu</a></div>'
    raw=raw.replace('</header>',nav+'</header>',1)
    (ROOT/file).write_text(raw)
    integrated.append(dict(file=file,kind=pmeta['kind'],codes=codes))

catalog='''<!doctype html><html lang="vi"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>Cấu tạo ô tô — Học tương tác 12 chương</title><link rel="stylesheet" href="interactive.css"></head><body class="c2-page"><main class="c2-page-shell c2-catalog all-catalog"><nav class="c2-page-nav" aria-label="Điều hướng"><a href="../index.html">Tài liệu gốc</a><a href="../on_tap/index.html">Ôn tập 411 câu</a><a href="thuat-ngu.html">Thuật ngữ trong hoạt động</a><a href="../HUONG_DAN_SU_DUNG.html">Hướng dẫn</a></nav><header class="all-hero"><div><p class="c2-kicker">Cấu tạo ô tô · Học liệu tương tác</p><h1>Hiểu cấu tạo.<br>Nắm nguyên lý.<br>Tự thực hành.</h1><p>Học trên hình kỹ thuật, xem đường tác động theo từng bước và nhận phản hồi ngay trong bài.</p><div class="c2-statusline"><span class="c2-chip">12 chương</span><span class="c2-chip">102 bài</span><span class="c2-chip">408 hoạt động trong bài</span><span class="c2-chip">Chạy ngoại tuyến</span></div></div><div class="all-hero-art" aria-hidden="true"><svg viewBox="0 0 500 300"><path d="M60 205H450L424 149H332L278 98H158L115 148H79Z" fill="none" stroke="currentColor" stroke-width="4"/><path d="M140 143L170 109H270L302 143Z" fill="currentColor" opacity=".2"/><circle cx="143" cy="205" r="34" fill="#102f45" stroke="currentColor" stroke-width="4"/><circle cx="381" cy="205" r="34" fill="#102f45" stroke="currentColor" stroke-width="4"/><path d="M163 180H365M245 180V160" stroke="#e4ab53" stroke-width="5" stroke-dasharray="10 6"/><circle cx="244" cy="180" r="8" fill="#e4ab53"/><text x="83" y="275" fill="currentColor" font-family="Arial,sans-serif" font-size="18">KHÁM PHÁ → GIẢI THÍCH → VẬN DỤNG</text></svg></div></header><section class="all-progress" aria-label="Tiến độ"><div><strong id="progress-text">Đang đọc tiến độ…</strong><progress id="progress-bar" max="408" value="0"></progress><p class="c2-small" id="storage-note">Kết quả được lưu trong trình duyệt khi trình duyệt cho phép.</p></div><div class="c2-toolbar"><button class="c2-btn" id="export-progress">Sao lưu kết quả</button><label class="c2-btn" for="import-progress">Khôi phục kết quả</label><input type="file" id="import-progress" accept="application/json,.json" hidden></div><p id="catalog-notice" class="c2-small" role="status"></p></section><section class="all-filter" aria-label="Tìm bài"><label>Tìm bài hoặc thuật ngữ<input type="search" id="lesson-search" placeholder="Ví dụ: đồng tốc, xi-lanh, 10.3.5…" autocomplete="off"></label><label>Chương<select id="chapter-filter"><option value="all">Tất cả 12 chương</option>'''+''.join('<option value="'+str(c)+'">'+str(c)+'. '+escape(t)+'</option>' for c,t in CHAPTERS.items())+'''</select></label><label>Tiến độ<select id="status-filter"><option value="all">Tất cả bài</option><option value="new">Chưa thực hành</option><option value="active">Đang thực hành</option><option value="complete">Đúng cả 4 hoạt động</option></select></label></section><p class="c2-small" id="search-count"></p><div id="chapter-list"></div><p class="c2-small all-footer">Chọn bài → khám phá / tự nhận diện → xem từng bước → thực hành. Hình bổ sung và sơ đồ nguyên lý được ghi rõ nguồn bài học; hình gốc và nội dung giáo trình vẫn có ngay trong từng bài.</p></main><script src="lesson-data.js"></script><script src="catalog.js"></script></body></html>'''
(OUT/'index.html').write_text(catalog)
redirect='<!doctype html><html lang="vi"><head><meta charset="utf-8"><meta http-equiv="refresh" content="0; url=tuong_tac/index.html"><title>Bắt đầu học tương tác</title></head><body><p><a href="tuong_tac/index.html">Mở tài liệu tương tác 12 chương</a></p></body></html>'
(ROOT/'BAT_DAU.html').write_text(redirect)
(ROOT/'BAT_DAU_CHUONG_2.html').write_text(redirect.replace('tuong_tac/index.html','tuong_tac/index.html?chapter=2'))
(ROOT/'chuong2/index.html').write_text(redirect.replace('tuong_tac/index.html','../tuong_tac/index.html?chapter=2'))

glossary={}
for l in lessons.values():
    for f in l['figures']:
        for p in f['parts']:
            key=(p['name'],f['source'],p['description'])
            glossary[key]=dict(term=p['name'],definition=p['description'],source=f['source'])
rows=sorted(glossary.values(),key=lambda x:norm(x['term']))
terms='<!doctype html><html lang="vi"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>Thuật ngữ trong hoạt động</title><link rel="stylesheet" href="interactive.css"></head><body class="c2-page"><main class="c2-page-shell c2-catalog"><nav class="c2-page-nav"><a href="index.html">← Mục lục tương tác</a></nav><p class="c2-kicker">Đối chiếu tên gọi theo bài</p><h1>Thuật ngữ trong hoạt động</h1><p>Danh mục tên gọi dùng trên hình và sơ đồ tương tác. Cùng một chi tiết có thể được gọi khác theo từng hình hoặc chương; mỗi mục có liên kết về bài nguồn.</p><label class="term-search">Tìm thuật ngữ<input type="search" id="term-search" placeholder="Nhập tên chi tiết…"></label><div class="term-table-wrap"><table class="term-table"><thead><tr><th>Tên gọi</th><th>Công dụng / mô tả</th><th>Bài nguồn</th></tr></thead><tbody>'+''.join('<tr><td>'+escape(r['term'])+'</td><td>'+escape(r['definition'])+'</td><td><a href="../'+lessons[r['source']]['file']+'#hoc-tuong-tac">'+r['source']+'</a></td></tr>' for r in rows)+'</tbody></table></div></main><script>document.getElementById("term-search").addEventListener("input",function(){var q=this.value.toLocaleLowerCase("vi").normalize("NFD").replace(/[\\u0300-\\u036f]/g,"");document.querySelectorAll("tbody tr").forEach(function(r){r.hidden=!r.textContent.toLocaleLowerCase("vi").normalize("NFD").replace(/[\\u0300-\\u036f]/g,"").replace(/đ/g,"d").replace(/×/g,"x").includes(q.replace(/đ/g,"d").replace(/×/g,"x"));});});</script></body></html>'
(OUT/'thuat-ngu.html').write_text(terms)
(OUT/'thuat-ngu.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2))
(OUT/'manifest.json').write_text(json.dumps(dict(counts=data['counts'],integrated_pages=integrated,converted_resources=conversion),ensure_ascii=False,indent=2))
for name in ['HUONG_DAN_CHUONG_2.txt','KIEM_TRA_CHUONG_2.txt']:
    (ROOT/name).unlink(missing_ok=True)
if not PACKAGED:
    for fname in ['figures.py','specs.py','build_all.py','source.json','wmf_formula.py']:
        shutil.copyfile(BASE/'audit_all'/fname,OUT/'tools'/fname)
    for file in bank['pages']:
        if file=='all':continue
        dest=OUT/'tools/source_pages'/file;dest.parent.mkdir(parents=True,exist_ok=True)
        shutil.copyfile(ORIGINAL/file,dest)
print(json.dumps(dict(counts=data['counts'],pages=len(integrated),converted=len(converted)),ensure_ascii=False))
