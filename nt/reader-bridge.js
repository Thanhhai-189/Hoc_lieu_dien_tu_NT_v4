(function(){
'use strict';
const embedded=window.parent!==window,cache=new Map();let resolveReady,readyDone=false;
const ready=new Promise(r=>resolveReady=r),ns='nt-learning';
function emit(m){if(embedded)parent.postMessage({ns,...m},'*');}
function finish(){if(!readyDone){readyDone=true;resolveReady();}}
const storage={getItem(k){if(cache.has(k))return cache.get(k);if(embedded&&readyDone)return null;try{return localStorage.getItem(k);}catch(e){return null;}},setItem(k,v){cache.set(k,String(v));if(embedded){emit({type:'write',key:k,value:String(v)});}else localStorage.setItem(k,String(v));}};
function reveal(target) {
  if (!target) return;
  if (embedded) {
    emit({type:'reveal', top:target.getBoundingClientRect().top});
  } else {
    target.scrollIntoView({block:'start', behavior:'instant'});
  }
}
window.NTBridge={ready,storage,emit,reveal};
window.addEventListener('message',e=>{
  if(e.source!==parent||e.data?.ns!==ns)return;
  const m=e.data;
  if(m.type==='snapshot'){
    for(const[k,v]of Object.entries(m.entries||{}))cache.set(k,v);
    finish();
  }
  if(m.scale)document.documentElement.style.setProperty('--nt-scale',Math.max(.9,Math.min(1.35,Number(m.scale)||1)));
  if(m.type==='tab'){
    document.querySelector('[data-c2-action="view"][data-view="'+m.tab+'"]')?.click();
    reveal(document.querySelector('.c2-lab'));
  }
  if(m.type==='reading')reveal(document.querySelector('article.box'));
  if(m.type==='review')reveal(document.querySelector('.auto-review'));
});
if(embedded){document.documentElement.classList.add('nt-embedded');emit({type:'ready'});setTimeout(finish,1800);}else finish();
document.addEventListener('DOMContentLoaded',()=>{document.body.classList.add('nt-reader');if(!embedded){const back=document.createElement('a');back.href=(location.pathname.includes('/html/')||location.pathname.includes('/on_tap/')||location.pathname.includes('/tuong_tac/'))?'../index.html':'index.html';back.className='nt-standalone-home';back.textContent='← Học liệu điện tử tương tác NT · Mở trang chủ';document.body.prepend(back);}
document.querySelectorAll('.exe-text-template figure').forEach(figure=>{
  const images=figure.querySelectorAll('img');
  const caption=figure.querySelector('figcaption')?.textContent.trim();
  if(images.length===1&&caption&&!images[0].hasAttribute('alt'))images[0].alt=caption;
});
document.addEventListener('click',e=>{const img=e.target.closest('.c2-pinboard img');if(img){const a=document.createElement('a');a.href=img.src;a.target='_blank';a.rel='noopener';a.click();return;}const a=e.target.closest('a[href]');if(!a||!embedded||a.target==='_blank'||a.hasAttribute('download'))return;const u=new URL(a.href,location.href);if(u.pathname.endsWith('.pdf')){a.target='_blank';return;}const data=window.OTO_ALL_DATA;let code;if(data)code=Object.keys(data.lessons).find(c=>u.pathname.endsWith('/'+data.lessons[c].file));if(code){e.preventDefault();emit({type:'navigate',hash:'#lesson='+code});return;}if(u.pathname===location.pathname&&u.hash)return;if(/\/index\.html$/.test(u.pathname)){e.preventDefault();emit({type:'navigate',hash:u.pathname.includes('/on_tap/')?'#review':'#home'});}});
let previous=0;function resize(){document.querySelectorAll('.box-toggle').forEach(b=>{b.title='Thu gọn / mở nội dung';b.setAttribute('aria-label','Thu gọn / mở nội dung');});if(!embedded)return;const h=Math.ceil(document.body.getBoundingClientRect().height);if(Math.abs(h-previous)>4){previous=h;emit({type:'height',height:h});}}const observer=new ResizeObserver(()=>requestAnimationFrame(resize));observer.observe(document.body);window.addEventListener('load',resize);setTimeout(resize,400);
});
})();
