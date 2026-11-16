(function () {
  'use strict';
  var palette = { torque: '#bd6500', control: '#176ca9', signal: '#7a46a4', air: '#187850', idle: '#bac8d5' };
  var esc = function (v) { return String(v).replace(/[&<>"']/g, function (c) { return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]; }); };
  function render(sim, step, key) {
    var uid = 'c2-svg-' + key.replace(/[^a-z0-9]/gi, '') + '-' + sim.id;
    var draw = [];
    function text(x, y, lines, small, anchor) {
      return '<text x="' + x + '" y="' + y + '" text-anchor="' + (anchor || 'middle') + '"' + (small ? ' class="c2-svg-small"' : '') + '>' +
        lines.map(function (line,i) { return '<tspan x="' + x + '" dy="' + (i ? 20 : 0) + '">' + esc(line) + '</tspan>'; }).join('') + '</text>';
    }
    function box(x,y,w,h,lines,active,type) {
      var color = active ? palette[type || 'control'] : palette.idle;
      return '<rect x="' + x + '" y="' + y + '" width="' + w + '" height="' + h + '" rx="9" fill="' + (active ? '#fff' : '#f1f5f8') + '" stroke="' + color + '" stroke-width="' + (active ? 3 : 1.5) + '"/>' +
        text(x+w/2, y+h/2-(lines.length-1)*10+5, lines);
    }
    function arrow(path, active, type) {
      var name = active ? (type || 'control') : 'idle';
      return '<path d="' + path + '" fill="none" stroke="' + palette[name] + '" stroke-width="' + (active ? 5 : 3) + '" marker-end="url(#' + uid + '-' + name + ')"' +
        (active ? ' class="c2-flow-on"' : ' stroke-dasharray="5 5"') + '/>';
    }
    function torqueRow(y, torque, label) {
      draw.push(box(35,y,150,58,['Động cơ'],true,'torque'));
      draw.push(box(330,y,180,58,[label || 'Ly hợp ma sát',torque ? 'Đang truyền mômen' : 'Ngắt mômen'],!!torque,'torque'));
      draw.push(box(690,y,180,58,['Trục sơ cấp','Hộp số'],!!torque,'torque'));
      draw.push(arrow('M185 '+(y+29)+' H325',true,'torque'));
      draw.push(arrow('M510 '+(y+29)+' H682',!!torque,'torque'));
    }
    if (sim.kind === 'clutch') {
      var gap = step.gap || 0, pressureX = (sim.double ? 307 : 266) + gap * 40;
      draw.push(box(30,25,145,52,['Động cơ'],true,'torque'));
      draw.push(box(245,25,160,52,['Bánh đà / vỏ'],true,'torque'));
      draw.push(box(475,25,170,52,['Các mặt ma sát'],!!step.torque,'torque'));
      draw.push(box(725,25,155,52,['Trục sơ cấp'],!!step.torque,'torque'));
      draw.push(arrow('M175 51 H237',true,'torque'),arrow('M405 51 H467',!!step.torque,'torque'),arrow('M645 51 H717',!!step.torque,'torque'));
      draw.push('<line x1="135" y1="234" x2="795" y2="234" stroke="#7794ac" stroke-width="11"/>');
      draw.push('<rect x="220" y="131" width="26" height="206" rx="4" fill="#becbd7" stroke="#5b7287" stroke-width="2"/>');
      draw.push('<rect x="'+(246+gap*(sim.double?6:12))+'" y="152" width="20" height="164" rx="3" fill="#f1cf9a" stroke="#99591e" stroke-width="2"/>');
      if (sim.double) {
        draw.push('<rect x="'+(266+gap*17)+'" y="139" width="21" height="190" rx="3" fill="#bdcbd8" stroke="#5b7287" stroke-width="2"/>');
        draw.push('<rect x="'+(287+gap*25)+'" y="152" width="20" height="164" rx="3" fill="#f1cf9a" stroke="#99591e" stroke-width="2"/>');
      }
      draw.push('<rect x="'+pressureX+'" y="140" width="28" height="188" rx="4" fill="#d7e5ef" stroke="#4f728d" stroke-width="2"/>');
      draw.push('<path d="M'+(pressureX+28)+' 170 L'+(pressureX+76)+' 200 L'+(pressureX+28)+' 235 L'+(pressureX+76)+' 268 L'+(pressureX+28)+' 304" fill="none" stroke="#7a5b80" stroke-width="5"/>');
      draw.push('<rect x="'+(480-gap*25)+'" y="210" width="45" height="48" rx="5" fill="#c0d6e6" stroke="#3b7195" stroke-width="3"/>');
      draw.push('<path d="M220 132 L195 122 M'+(pressureX+14)+' 140 L355 122" fill="none" stroke="#7992a6" stroke-width="1.5"/>');
      draw.push(text(185,116,['Bánh đà']),text(sim.double?277:257,360,[sim.double?'Hai đĩa ma sát':'Đĩa ma sát']));
      draw.push(text(360,116,['Đĩa ép']),text(415,300,['Lò xo ép']),text(525,186,['Bạc mở']));
      draw.push(text(735,225,['Trục bị động'],true));
      draw.push(box(30,367,145,45,['Bàn đạp'],!!step.control));
      draw.push(arrow('M175 390 H505 V269',!!step.control,'control'));
      draw.push(text(720,385,[gap>=1?'Các mặt ma sát được tách':step.torque===0.5?'Giai đoạn tiếp nối / trượt':'Lực ép kẹp các mặt ma sát'],true));
      if (gap>=1) draw.push(text(335,337,['Khe hở minh họa'],true));
    } else if (sim.kind === 'drive') {
      var hyd = sim.drive === 'hydraulic';
      var names = hyd ? [['Bàn đạp'],['Xi lanh chính'],['Đường dầu'],['Xi lanh công tác']] :
        [['Bàn đạp'],['Cáp kéo'],['Đòn liên kết'],['Bạc mở']];
      var xs = [35,265,495,725], on = step.active || [];
      names.forEach(function (name,i) { draw.push(box(xs[i],40,155,70,name,on.indexOf(i)>=0)); });
      for(var i=0;i<3;i++) draw.push(arrow('M'+(xs[i]+155)+' 75 H'+(xs[i+1]-8),on.indexOf(i+1)>=0,'control'));
      draw.push(arrow('M802 110 V200 H420 V270',on.length>=4,'control'));
      draw.push(text(785,152,[hyd?'Chốt đẩy → càng mở':'Cơ cấu tách'],true));
      torqueRow(285,step.torque);
      draw.push(text(440,226,[hyd?'Đường xanh: dẫn động thủy lực':'Đường xanh: tác động cơ khí'],true));
      draw.push(text(450,390,[step.gap>=1?'Cơ cấu mở giải phóng lực ép giữa các mặt ma sát':'Lực lò xo duy trì hoặc khôi phục tiếp xúc ma sát'],true));
    } else if (sim.kind === 'multi') {
      draw.push(box(35,35,160,65,['Dầu điều khiển'],!!step.pressure));
      draw.push(box(310,35,190,65,['Buồng áp suất','Piston'],!!step.pressure));
      draw.push(box(665,35,205,65,['Lực ép chồng đĩa'],!!step.torque));
      draw.push(arrow('M195 68 H302',!!step.pressure,'control'),arrow('M500 68 H657',!!step.pressure,'control'));
      draw.push('<rect x="278" y="159" width="300" height="165" rx="9" fill="#e1ebf3" stroke="#6b869b" stroke-width="2"/>');
      for(var j=0;j<8;j++) draw.push('<rect x="'+(310+j*26)+'" y="172" width="13" height="140" fill="'+(j%2?'#b9d0df':'#edbc76')+'" stroke="#657c90"/>');
      draw.push('<rect x="'+(step.pressure?540:566)+'" y="165" width="26" height="152" fill="#93b8d2" stroke="#276d9d" stroke-width="3"/>');
      draw.push(arrow('M766 100 V141 H558 V157',!!step.pressure,'control'));
      draw.push(text(442,343,['Các đĩa chủ động / bị động xen kẽ'],true));
      draw.push(box(35,207,150,58,['Nguồn mômen'],true,'torque'),box(687,207,180,58,['Moayơ → trục'],!!step.torque,'torque'));
      draw.push(arrow('M185 236 H270',!!step.torque,'torque'),arrow('M580 236 H679',!!step.torque,'torque'));
      draw.push(text(450,395,[step.pressure?'Áp suất tạo lực ép; ma sát truyền mômen':'Không còn áp suất tác động: lực ép được giải phóng'],true));
    } else if (sim.kind === 'assist') {
      var st = step.stage, airOn = st===2 || st===3, commandOn = st>=1 && st<=3, ventOn = st===0 || st===4;
      draw.push(box(30,30,160,64,['Bàn đạp / cơ khí'],commandOn));
      draw.push(box(270,30,160,64,['Van phân phối'],commandOn));
      draw.push(box(510,30,160,64,['Màng / piston'],airOn,'air'));
      draw.push(box(745,30,145,64,['Cơ cấu mở'],commandOn));
      draw.push(arrow('M190 62 H262',commandOn,'control'),arrow('M430 62 H502',airOn,'air'),arrow('M670 62 H737',airOn,'air'));
      draw.push(box(30,173,160,60,['Nguồn khí nén'],airOn,'air'),box(270,173,160,60,['Đường xả khí',ventOn?'Mở':'Đóng'],ventOn,'air'));
      draw.push(arrow('M190 203 H225 V110 H347 V100',airOn,'air'),arrow('M350 100 V165',ventOn,'air'));
      draw.push(arrow('M110 94 V131 H815 V100',commandOn,'control'));
      draw.push(text(607,177,['Lực khí nén bổ sung lực cơ khí'],true));
      draw.push(arrow('M818 94 V278 H420 V297',commandOn,'control'));
      torqueRow(308,step.torque);
      draw.push(text(450,410,[airOn?'Van cấp mở; áp suất buồng trợ lực tăng':ventOn?'Van cấp đóng; đường xả mở để hồi vị':'Đóng đường xả trước khi mở đường cấp khí'],true));
    } else if (sim.kind === 'acs') {
      var stage = step.stage;
      draw.push(box(35,30,180,65,['Cảm biến / CAN'],true,'signal'));
      draw.push(box(325,30,180,65,['Bộ điều khiển'],stage>=1,'signal'));
      draw.push(box(650,30,205,65,['Động cơ điện'],stage>=2,'signal'));
      draw.push(arrow('M215 63 H317',true,'signal'),arrow('M505 63 H642',stage>=1,'signal'));
      draw.push(box(650,155,205,65,['Trục vít – bánh vít'],stage>=2));
      draw.push(box(325,155,180,65,['Xi lanh chính'],stage>=2));
      draw.push(box(35,155,180,65,['Xi lanh con'],stage>=2));
      draw.push(arrow('M752 95 V147',stage>=2,'signal'),arrow('M650 187 H513',stage>=2,'control'),arrow('M325 187 H223',stage>=2,'control'));
      draw.push(arrow('M125 220 V273 H420 V297',stage>=2 && stage<=3,'control'));
      torqueRow(308,step.torque);
      draw.push(text(450,410,[stage===4?'Bộ điều khiển điều chỉnh nối lại và độ trượt phù hợp':'Tín hiệu điện điều khiển chấp hành; thủy lực tác động cơ cấu mở'],true));
    } else if (sim.kind === 'dual') {
      draw.push(box(25,167,145,70,['Động cơ'],true,'torque'));
      draw.push(box(265,55,145,66,['C1',step.c1===1?'Nối':step.c1?'Chuyển tiếp':'Ngắt'],!!step.c1,'torque'));
      draw.push(box(265,281,145,66,['C2',step.c2===1?'Nối':step.c2?'Chuyển tiếp':'Ngắt'],!!step.c2,'torque'));
      draw.push(box(490,55,145,66,['IS1 — trục đặc','Nhóm số lẻ'],!!step.c1,'torque'));
      draw.push(box(490,281,145,66,['IS2 — trục rỗng','Nhóm số chẵn'],!!step.c2,'torque'));
      draw.push(box(755,167,140,70,['Đầu ra hộp số'],!!(step.c1||step.c2),'torque'));
      draw.push(arrow('M170 192 H211 V88 H257',!!step.c1,'torque'),arrow('M170 213 H211 V314 H257',!!step.c2,'torque'));
      draw.push(arrow('M410 88 H482',!!step.c1,'torque'),arrow('M410 314 H482',!!step.c2,'torque'));
      draw.push(arrow('M635 88 H710 V190 H747',!!step.c1,'torque'),arrow('M635 314 H710 V214 H747',!!step.c2,'torque'));
      draw.push(text(450,209,[step.selected]));
      draw.push(text(450,399,[step.c1===0.5?'Trùng lặp có kiểm soát; không khóa cứng cả hai nhánh':'Chọn trước số ở nhánh ly hợp đang ngắt'],true));
    } else if (sim.kind === 'dualtype') {
      var target = sim.wet ? 'C1' : 'C2', connected = sim.wet ? step.c1 : step.c2;
      draw.push(box(35,30,180,65,['Dầu điều khiển'],!!step.pressure));
      draw.push(box(330,30,205,65,sim.wet?['Buồng áp suất','Piston C1']:['Xi lanh con','Càng đóng C2'],!!step.pressure));
      draw.push(box(695,30,180,65,['Lực ép '+target],!!connected));
      draw.push(arrow('M215 63 H322',!!step.pressure,'control'),arrow('M535 63 H687',!!step.pressure,'control'));
      draw.push(box(35,220,150,70,['Động cơ'],true,'torque'));
      draw.push(box(330,220,205,70,[sim.wet?'C1 — cụm đĩa ướt':'C2 — đĩa ma sát khô',connected?'Nối mômen':'Ngắt mômen'],!!connected,'torque'));
      draw.push(box(695,220,180,70,[sim.wet?'Trục đặc IS1':'Trục rỗng IS2'],!!connected,'torque'));
      draw.push(arrow('M185 255 H322',!!connected,'torque'),arrow('M535 255 H687',!!connected,'torque'),arrow('M785 95 V166 H432 V212',!!step.pressure,'control'));
      draw.push(text(450,347,sim.wet?['Các mặt ma sát làm việc trong dầu.','Buồng cân bằng bù tác động lực ly tâm của dầu.']:['Các mặt ma sát không ngâm trong dầu.','Dầu được dùng ở dẫn động xi lanh con.'],false));
      draw.push(text(450,411,['Minh họa riêng nhánh '+target+'; trạng thái nhánh còn lại phụ thuộc chế độ vận hành.'],true));
    }
    var defs = Object.keys(palette).map(function (name) {
      return '<marker id="'+uid+'-'+name+'" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto" markerUnits="userSpaceOnUse"><path d="M0 0 L8 4 L0 8 Z" fill="'+palette[name]+'"/></marker>';
    }).join('');
    return '<svg viewBox="0 0 920 450" role="img" aria-labelledby="'+uid+'-title '+uid+'-desc"><title id="'+uid+'-title">'+esc(sim.title)+' — '+esc(step.title)+'</title><desc id="'+uid+'-desc">'+esc(step.text)+'</desc><defs>'+defs+'</defs>'+draw.join('')+'</svg>';
  }
  window.OTO_C2_SIMULATION = {render:render};
}());
