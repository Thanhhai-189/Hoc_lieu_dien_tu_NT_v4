(function(){
'use strict';const base=window.OTO_ALL_SIMULATION;if(!base)return;
const esc=v=>String(v).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
function svg(sim,step,code){const air=sim.kind==='nt-abs-air',m=step.mode,inc=m==='increase',dec=m==='decrease',uid='ntabs-'+code.replace(/\./g,'')+'-'+(air?'air':'oil'),col=air?'#218461':'#177e9a',off='#ced9df';let s=[];
function text(x,y,a,size=17,color='#294b5d'){a=Array.isArray(a)?a:[a];return '<text x="'+x+'" y="'+y+'" text-anchor="middle" font-family="Segoe UI,Arial,sans-serif" font-size="'+size+'" fill="'+color+'">'+a.map((t,i)=>'<tspan x="'+x+'" dy="'+(i?23:0)+'">'+esc(t)+'</tspan>').join('')+'</text>';}
function box(x,y,w,h,a,active=true){s.push('<rect x="'+x+'" y="'+y+'" width="'+w+'" height="'+h+'" rx="9" fill="'+(active?'#f0f8f5':'#f8fafb')+'" stroke="'+(active?col:off)+'" stroke-width="2"/>',text(x+w/2,y+h/2-(a.length-1)*11+6,a));}
function path(d,on){s.push('<path d="'+d+'" stroke="'+(on?col:off)+'" stroke-width="'+(on?5:2)+'" fill="none" marker-end="url(#'+uid+(on?'-on':'-off')+')"'+(on?' class="all-active-edge"':' stroke-dasharray="6 4"')+'/>');}
s.push('<rect width="1000" height="470" fill="#f9fcfc" rx="10"/>',text(500,32,air?'ABS khí nén — mô hình chức năng':'ABS thủy lực — ví dụ mạch van nạp / van xả',20));
box(35,95,185,76,air?['Nguồn khí từ','van phanh tổng']:['Xi-lanh chính /','đường áp suất']);box(330,95,165,76,['Van '+(air?'cấp':'nạp'),inc?'MỞ':'ĐÓNG'],inc);box(740,95,215,76,air?['Bầu phanh']:['Xi-lanh bánh xe /','cơ cấu phanh']);
path('M220 133 H321',inc);path('M495 133 H732',inc);box(740,255,215,69,['Van xả',dec?'MỞ':'ĐÓNG'],dec);path('M847 171 V247',dec);
if(air){box(380,255,190,69,['Khí trời'],dec);path('M740 290 H578',dec);s.push(text(490,370,'Giữ áp: cô lập bầu phanh, cả hai đường đóng.',17));}
else{box(430,255,190,69,['Bình tích áp thấp'],dec);box(105,255,180,69,['Bơm hồi dầu'],dec);path('M740 290 H628',dec);path('M430 290 H293',dec);path('M195 255 V209 H275 V133',dec);s.push(text(475,370,'Thời điểm chạy bơm tùy ECU; màu minh họa đường cấp / xả.',16));}
s.push('<rect x="310" y="405" width="380" height="42" rx="8" fill="#e6f2ec"/>',text(500,432,'Trạng thái: '+(inc?'TĂNG ÁP':dec?'GIẢM ÁP':'GIỮ ÁP'),18,'#1e6b4c'),text(500,465,'ECU chọn chế độ theo trạng thái bánh xe, không theo một vòng cố định.',14,'#72858f'));
const defs='<defs>'+['on','off'].map(k=>'<marker id="'+uid+'-'+k+'" markerWidth="9" markerHeight="9" refX="8" refY="4.5" orient="auto" markerUnits="userSpaceOnUse"><path d="M0 0L9 4.5L0 9Z" fill="'+(k==='on'?col:off)+'"/></marker>').join('')+'</defs>';
return '<svg viewBox="0 0 1000 490" role="img" aria-labelledby="'+uid+'-title '+uid+'-desc"><title id="'+uid+'-title">'+esc(sim.title)+' — '+esc(step.title)+'</title><desc id="'+uid+'-desc">'+esc(step.text)+'</desc>'+defs+s.join('')+'</svg>';
}
window.OTO_ALL_SIMULATION={render(sim,step,code){return sim.kind.startsWith('nt-abs-')?svg(sim,step,code):base.render(sim,step,code)},legend(sim){return sim.kind.startsWith('nt-abs-')?'<div class="c2-legend"><span style="--legend-color:'+(sim.kind==='nt-abs-air'?'#218461':'#177e9a')+'">'+(sim.kind==='nt-abs-air'?'Khí nén đang lưu thông':'Dầu đang lưu thông')+'</span><span style="--legend-color:#ced9df">Đường không tô trong trạng thái minh họa</span></div>':base.legend(sim)}};
})();
