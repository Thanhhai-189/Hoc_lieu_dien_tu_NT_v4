from pathlib import Path
from html import escape

FIGURES = {}

def F(key, source, image, caption, rows):
    parts = []
    for i, (name, x, y, description) in enumerate(rows):
        parts.append(dict(id=chr(65+i), name=name, x=x, y=y,
                          description=description, short=description, aliases=[name]))
    FIGURES[key] = dict(id=key, source=source, image='content/resources/'+image,
                        caption=caption, parts=parts, origin='original')
    return key

def C(key, source, title, rows):
    # Concept diagrams are for taxonomy, purposes and parameters, not physical assemblies.
    parts = []
    for i, (name, hint, description) in enumerate(rows):
        col=i%2; row=i//2
        aliases=[name]
        if '×' in name:aliases.append(name.replace('×','x'))
        parts.append(dict(id=chr(65+i), name=name, x=8+col*50, y=18+row*31,
                          description=description, short=description, aliases=aliases, hint=hint))
    FIGURES[key] = dict(id=key, source=source, image='tuong_tac/diagrams/'+key+'.svg',
                        caption=title+' — sơ đồ học tập biên soạn từ bài '+source,
                        parts=parts, origin='concept')
    return key

F('driveline','1.2.2','T1_image51.png','Hình 1.33 — Hệ thống truyền động của ô tô',[
 ('Hộp số',62,58,'Biến đổi mô men quay và tốc độ quay để phù hợp điều kiện chuyển động.'),
 ('Trục các đăng',40,36,'Truyền mô men giữa các cụm có đường tâm không nằm trên một đường thẳng.'),
 ('Cầu xe',25,26,'Nhận mô men từ hệ thống truyền lực để dẫn động bánh xe chủ động.'),
 ('Ly hợp',75,62,'Nối hoặc ngắt mô men truyền từ động cơ tới hộp số.')])
F('gear3','3.2.2','T1_image127.png','Hình 3.13 — Sơ đồ hộp số 3 trục 5 cấp số',[
 ('Trục sơ cấp',24,32,'Nhận mô men từ ly hợp, mang bánh răng liền trục sơ cấp.'),
 ('Trục thứ cấp',89,32,'Truyền mô men ra khỏi hộp số.'),
 ('Trục trung gian',56,61,'Mang các bánh răng truyền trung gian.'),
 ('Khớp đồng tốc gài số 3,4',52,30,'Gài bánh răng số 3 hoặc nối trực tiếp trục sơ cấp với trục thứ cấp.'),
 ('Bánh răng gài số lùi',66,79,'Tham gia đường truyền đảo chiều quay của trục thứ cấp.')])
F('gear2','3.2.3','T1_image140.png','Hình 3.26 — Hộp số hai trục trên dòng xe Kia, kiểu M5CF1',[
 ('Trục sơ cấp',72,29,'Nhận mô men từ ly hợp, mang các bánh răng phía chủ động.'),
 ('Trục thứ cấp',48,40,'Nhận mô men qua cặp bánh răng đã chọn và truyền tới truyền lực chính.'),
 ('Truyền lực chính',65,63,'Nhận đầu ra hộp số; vỏ được bố trí liền với vỏ hộp số.')])
F('cross','6.2.1','T1_image263.png','Hình 6.3 — Sơ đồ nguyên lý khớp các đăng đơn',[
 ('Nạng chủ động',30,29,'Nhận mô men từ trục chủ động theo ký hiệu 1.'),
 ('Nạng bị động',68,61,'Đưa mô men tới trục bị động theo ký hiệu 2.'),
 ('Trục chữ thập',46,45,'Liên kết hai nạng và cho phép truyền động khi hai trục lệch góc.')])
F('crossparts','6.2.2','T1_image277.png','Hình 6.8 — Cấu tạo của khớp các đăng',[
 ('Trục chữ thập',21,45,'Liên kết hai nạng của khớp các đăng.'),
 ('Nắp vòng bi',27,55,'Chứa ổ bi kim, được giữ trong lỗ trên nạng.'),
 ('Vòng chặn',31,55,'Giữ vị trí nắp ổ theo kết cấu minh họa.'),
 ('Trục rỗng (Khớp nối trượt)',10,64,'Bù thay đổi chiều dài trong quá trình các cụm chuyển động tương đối.')])
F('winch','12.2.2','C12_image27.jpeg','Hình 12.27 — Sơ đồ bố trí chung hệ thống tời',[
 ('Hộp trích công suất',90,23,'Nhận công suất từ hộp số chính để dẫn động thiết bị phụ.'),
 ('Trục các đăng',72,34,'Truyền mô men giữa hộp trích công suất và hộp giảm tốc.'),
 ('Hộp giảm tốc',32,42,'Giảm tốc và tăng mô men tới trống tời.'),
 ('Trống tời',41,49,'Quấn hoặc nhả dây cáp để tạo tác động kéo.'),
 ('Dây cáp',38,53,'Truyền lực kéo từ trống tời tới điểm kéo.')])
F('shift','3.3.2','T1_image169.png','Cơ cấu điều khiển và định vị trong hộp số',[
 ('Cần số',42,31,'Nhận thao tác chọn và dịch chuyển cơ cấu gài số.'),
 ('Trục trượt',65,63,'Dẫn hướng chuyển động của càng gài số.'),
 ('Càng gài số',74,77,'Đẩy ống gài hoặc bánh răng tới vị trí gài số.'),
 ('Cơ cấu định vị',62,60,'Giữ trục trượt ở vị trí xác định, tránh tự ra hoặc vào số.'),
 ('Chốt hãm',55.5,63,'Tham gia cơ cấu ngăn gài đồng thời hai số.')])
F('dct','4.2.1','T1_image197.png','Hình 4.1 — Hộp số ly hợp kép 6 cấp sử dụng ly hợp ma sát ướt',[
 ('Ly hợp 1',22,31,'Nối hoặc ngắt nhánh truyền lực tới các cấp số lẻ trong hình 4.1.'),
 ('Ly hợp 2',22,63,'Nối hoặc ngắt nhánh truyền lực tới các cấp số chẵn trong hình 4.1.'),
 ('Trục chủ động 1',54,47,'Nhận mô men từ ly hợp 1 theo nhánh màu đỏ.'),
 ('Trục chủ động 2',49,40,'Nhận mô men từ ly hợp 2 theo nhánh màu xanh.')])
F('converter','4.3.1','T1_image199.png','Hình 4.3 — Cấu tạo biến mô thủy lực',[
 ('Bánh bơm',38,29,'Nhận chuyển động từ động cơ và đưa năng lượng vào dòng dầu.'),
 ('Bánh tua-bin',30,29,'Nhận năng lượng dòng dầu và truyền mô men tới trục sơ cấp hộp số.'),
 ('Stato',34,39,'Đổi hướng dòng dầu từ bánh tua-bin trở về bánh bơm.'),
 ('Khớp một chiều',34,46,'Giữ hoặc giải phóng stato theo chiều tác động của dòng dầu.')])
F('cvt','4.4.1','T1_image253.png','Hình 4.57 — Bộ truyền đai vô cấp trên hộp số xe Ford CTX',[
 ('Puli V sơ cấp',32,43,'Nhận mô men đầu vào và tạo bán kính làm việc phía chủ động.'),
 ('Puli V thứ cấp',37,74,'Nhận mô men qua đai truyền và đưa tới trục đầu ra.'),
 ('Đai truyền',45,62,'Truyền mô men giữa hai cặp bề mặt ma sát hình côn.'),
 ('Bánh răng mặt trời',68,36,'Là phần tử của bộ bánh răng hành tinh đổi chiều quay.')])
F('transfer','5.2.1','T1_image254.png','Hình 5.1 — Cấu tạo hộp phân phối đơn giản',[
 ('Bánh răng chủ động',55,24,'Nhận mô men từ trục vào hộp phân phối.'),
 ('Bánh răng trung gian',55,51,'Truyền giữa bánh răng chủ động và bị động, bảo đảm chiều quay trong sơ đồ.'),
 ('Bánh răng bị động',55,76,'Truyền mô men tới các trục ra.'),
 ('Khớp gài cầu trước',45,76,'Nối hoặc tách trục ra cầu trước khỏi đường truyền mô men.')])
F('transferlow','5.2.1','T1_image255.png','Hình 5.2 — Cấu tạo hộp phân phối hai cấp số truyền',[
 ('Bánh răng gài số',23,26,'Dịch chuyển để chọn số truyền thẳng hoặc số truyền thấp.'),
 ('Bánh răng ra cầu sau',30,27,'Truyền mô men tới trục ra cầu sau.'),
 ('Bánh răng số thấp',23,50,'Tạo tỷ số truyền lớn hơn ở cấp số truyền thấp.'),
 ('Bánh răng gài cầu trước',30,50,'Nối đường truyền tới cầu trước.'),
 ('Bánh răng ra cầu trước',30,76,'Truyền mô men tới trục ra cầu trước.')])
F('crossdouble','6.3.1','T1_image278.png','Hình 6.9 — Cấu tạo các đăng đồng tốc kiểu chữ thập kép',[
 ('Trục chủ động',17,65,'Đưa mô men vào khớp chữ thập kép.'),
 ('Khớp chữ thập',36,19,'Liên kết chuyển động giữa các nạng của khớp.'),
 ('Giá chạc kép',45,37,'Liên kết hai khớp chữ thập đặt liền kề.'),
 ('Trục bị động',70,23,'Nhận mô men từ khớp chữ thập kép.')])
F('cam','6.3.2','T1_image279.png','Hình 6.10a — Cấu tạo khớp các đăng đồng tốc loại cam',[
 ('Nạng chủ động',31,23,'Liên kết trục chủ động với cam thứ nhất.'),
 ('Cam',42,23,'Bề mặt nửa hình trụ phối hợp với nạng và đĩa truyền lực.'),
 ('Đĩa',53,22,'Nằm trong rãnh hai cam để liên kết truyền động.'),
 ('Nạng bị động',73,21,'Nhận tác động từ cam và truyền tới trục bị động.')])
F('veise','6.3.4','T1_image281.png','Hình 6.12 — Cấu tạo các đăng đồng tốc bi kiểu Veise',[
 ('Nạng chủ động',31,36,'Nhận mô men đầu vào; có các rãnh chứa bi truyền lực.'),
 ('Bi truyền lực',48,28,'Bốn bi ngoài đảm nhận truyền mô men giữa hai nạng.'),
 ('Bi giữa định tâm',50,40,'Viên bi thứ năm đặt tại tâm khớp để định tâm.'),
 ('Nạng bị động',72,57,'Nhận mô men qua các viên bi trong rãnh.')])
F('rzeppa','6.3.5','T1_image282.png','Hình 6.13 — Cấu tạo các đăng đồng tốc bi kiểu Rzeppa',[
 ('Nạng chủ động',24,78,'Phần khớp mang rãnh ngoài để truyền mô men qua bi theo ký hiệu 1.'),
 ('Nạng bị động',37,80,'Phần khớp đối ứng theo ký hiệu 2, phối hợp với các rãnh bi.'),
 ('Vòng định vị',44,80,'Giữ các bi trên mặt phẳng phân giác của góc giữa hai trục.'),
 ('Bi truyền lực',48,70,'Truyền mô men trong các rãnh của hai phần khớp.')])
F('tripod','6.3.6','T1_image283.png','Hình 6.14 — Cấu tạo các đăng đồng tốc kiểu Tripod',[
 ('Nạng chủ động',25,23,'Phần đầu vào truyền mô men tới chạc ba.'),
 ('Chạc ba',40,72,'Mang ba con lăn của khớp.'),
 ('Con lăn',45,58,'Truyền lực trong rãnh và cho phép dịch chuyển dọc trục.'),
 ('Nạng bị động',83,72,'Thân bao có ba rãnh dọc nhận tác động của các con lăn.')])
F('finaldrive','7.2.1','T1_image286.png','Hình 7.2 — Bộ truyền lực chính bánh răng côn răng thẳng',[
 ('Bánh răng côn chủ động',46,27,'Nhận mô men từ đường truyền vào.'),
 ('Bánh răng côn bị động',31,58,'Giảm tốc, tăng mô men và truyền tới vỏ vi sai.')])
F('diff','7.2.2','T1_image295.png','Hình 7.11 — Cấu tạo bộ vi sai bánh răng côn đối xứng',[
 ('Vỏ vi sai',31,69,'Nhận mô men từ bánh răng bị động truyền lực chính.'),
 ('Bánh răng mặt trời (bán trục)',60,46,'Ăn khớp bánh răng vi sai và truyền mô men tới bán trục.'),
 ('Bánh răng hành tinh (vi sai)',47,85,'Tự quay khi cần tạo chênh lệch tốc độ giữa các bán trục.'),
 ('Trục bánh răng vi sai',50,50,'Mang và định vị các bánh răng vi sai.'),
 ('Khớp khóa vi sai',12,75,'Hạn chế chuyển động quay tương đối khi khóa vi sai.')])
F('tire','8.1.1','T1_image329.png','Hình 8.1 — Cấu tạo của lốp',[
 ('Hoa lốp',26,59,'Tiếp xúc với mặt đường, truyền lực kéo và lực phanh.'),
 ('Lớp sợi bố',29,71,'Tạo kết cấu chịu tải của lốp.'),
 ('Lớp lót trong',22,82,'Lớp phía trong của lốp, giữ kín khí ở lốp không săm.'),
 ('Dây mép lốp',12,94,'Giữ mép lốp chắc trên vành bánh xe.')])
F('balance','8.2.3','T1_image349.png','Hình 8.13 — Cân bằng bánh xe',[
 ('Điểm nặng',11,40,'Khối lượng tập trung không đều gây lực ly tâm khi quay.'),
 ('Cân bằng tĩnh',14,22,'Xét sự cân bằng khối lượng khi cụm bánh đứng yên.'),
 ('Cân bằng động',66,20,'Xét sự cân bằng của cụm bánh khi quay, gồm tác động gây mô men rung.')])
F('worm','9.2.1','C9_image3.png','Hình 9.3 — Cơ cấu lái trục vít – bánh vít',[
 ('Trục vít',44,33,'Nhận chuyển động quay từ trục tay lái.'),
 ('Bánh vít',75,38,'Nhận chuyển động qua ăn khớp với trục vít.'),
 ('Trục đòn quay đứng',43,69,'Đưa tác động từ bánh vít tới dẫn động lái.')])
F('roller','9.2.2','C9_image4.png','Hình 9.4 — Cơ cấu lái trục vít lõm – con lăn',[
 ('Trục vít',20,22,'Trục vít dạng glô-bô-it nhận chuyển động quay đầu vào.'),
 ('Con lăn',20,77,'Ăn khớp với ren trục vít, thay tiếp xúc trượt bằng tiếp xúc lăn.'),
 ('Trục đòn quay đứng',33,72,'Nhận tác động từ giá con lăn và truyền ra dẫn động lái.')])
F('rack','9.2.3','C9_image6.jpeg','Hình 9.6 — Cơ cấu lái trục răng – thanh răng',[
 ('Bánh răng',47,40,'Nhận chuyển động quay từ trục lái.'),
 ('Thanh răng',30,34,'Dịch chuyển tịnh tiến khi bánh răng quay.'),
 ('Đòn kéo',9,19,'Truyền tác động từ thanh răng tới bánh xe dẫn hướng.'),
 ('Trụ đứng',45,87,'Tạo trục quay cho bánh xe dẫn hướng theo sơ đồ.')])
F('recirculating','9.2.4','C9_image8.png','Hình 9.8 — Cơ cấu trục vít – đai ốc – thanh răng – cung răng',[
 ('Trục vít',29,44,'Nhận chuyển động quay từ trục lái.'),
 ('Đai ốc bi',50,41,'Dịch chuyển dọc trục nhờ các bi lăn trong rãnh.'),
 ('Viên bi',50,49,'Thay ma sát trượt bằng ma sát lăn trong bộ truyền.'),
 ('Bánh răng (hình rẽ quạt)',47,66,'Nhận tác động từ đai ốc để quay trục đòn quay đứng.')])
F('steer','9.3.1','C9_image9.png','Hình 9.9 — Bố trí chung của hệ thống lái',[
 ('Vành tay lái',40,29,'Nhận lực và chuyển động điều khiển của người lái.'),
 ('Trục lái',36,43,'Nối vành tay lái với cơ cấu lái.'),
 ('Dẫn động lái',25,62,'Truyền tác động của cơ cấu lái tới bánh xe dẫn hướng.'),
 ('Cơ cấu lái',27,55,'Biến đổi lực và chuyển động từ trục lái.')])
F('angles','9.3.3','C9_image23.png','Hình 9.23 — Các góc đặt bánh xe dẫn hướng',[
 ('Góc camber',11,26,'Góc nghiêng ngang của mặt phẳng bánh xe khi nhìn từ trước.'),
 ('Góc nghiêng ngang trục lái đứng',34,22,'Góc nghiêng của trục quay lái khi nhìn từ trước.'),
 ('Góc caster',87,19,'Góc nghiêng dọc của trục quay lái khi nhìn từ bên.'),
 ('Độ chụm',18,84,'Quan hệ khoảng cách hai bánh ở phía trước và phía sau khi nhìn từ trên.')])
F('assiststeer','9.4.1','C9_image31.png','Hình 9.30a — Các kiểu bố trí trợ lực lái trên ô tô',[
 ('Van phân phối',31,22,'Điều khiển đường dầu tới các khoang xi-lanh lực.'),
 ('Cơ cấu lái',27,25,'Biến đổi chuyển động cơ khí của người lái.'),
 ('Xi-lanh lực',28,28,'Biến áp suất dầu thành lực trợ lái.'),
 ('Bơm dầu',44,17,'Cung cấp dầu có áp cho mạch trợ lực.')])
F('eps','9.4.2','C9_image38.png','Hình 9.37 — Sơ đồ trợ lực lái điện',[
 ('Cảm biến mô-men',49,42,'Nhận biết tác động điều khiển của người lái trên trục lái.'),
 ('ECU',91,55,'Nhận tín hiệu và tính toán lệnh trợ lực điện.'),
 ('Mô-tơ điện',70,67,'Sinh mô men hỗ trợ thông qua bộ truyền.'),
 ('Cơ cấu lái',49,84,'Đưa tác động tổng hợp tới bánh xe dẫn hướng.')])
F('drum','10.2.1','C10_image2.jpeg','Hình 10.2 — Cơ cấu phanh guốc',[
 ('Mâm phanh',16,42,'Giá cố định để lắp các chi tiết của cơ cấu phanh.'),
 ('Guốc phanh',23,49,'Mang má phanh áp sát mặt trong trống phanh khi phanh.'),
 ('Trống phanh',90,47,'Phần quay cùng bánh xe, tiếp xúc với má phanh.'),
 ('Cam phanh',66,24,'Đẩy guốc phanh ra theo sơ đồ dẫn động bằng cam.'),
 ('Lò xo hồi vị',32,33,'Kéo guốc phanh về sau khi thôi tác động phanh.')])
F('disc','10.2.2','C10_image19.jpeg','Hình 10.18 — Cấu tạo phanh đĩa',[
 ('Má phanh',90,78,'Tạo bề mặt ma sát với hai mặt đĩa phanh.'),
 ('Giá đỡ xi-lanh',51,78,'Chứa pít-tông và đỡ cụm tác động phanh.'),
 ('Vít xả',37,31,'Dùng để xả khí khỏi cụm xi-lanh khi bảo dưỡng.'),
 ('Đĩa phanh',71,32,'Quay cùng bánh xe và tạo mặt ma sát với má phanh.')])
F('brakemechanical','10.3.1','C10_image32.png','Hình 10.28 — Dẫn động phanh cơ khí',[
 ('Bàn đạp phanh',20,11,'Nhận lực điều khiển từ người lái.'),
 ('Đòn dẫn động',37,52,'Truyền lực giữa các đòn quay.'),
 ('Cam phanh',35,73,'Đẩy các guốc phanh áp sát trống phanh.'),
 ('Guốc phanh',41,85,'Tạo lực ma sát với mặt trong trống phanh.')])
F('brakehydraulic','10.3.2','C10_image38.png','Hình 10.34 — Sơ đồ dẫn động điều khiển phanh bằng thủy lực',[
 ('Bàn đạp',79,56,'Truyền lực người lái tới cần đẩy pít-tông.'),
 ('Xi-lanh chính',34,35,'Biến lực bàn đạp thành áp suất chất lỏng.'),
 ('Đường ống dẫn',10,64,'Truyền áp suất chất lỏng tới cơ cấu phanh.'),
 ('Xi-lanh công tác',24,83,'Biến áp suất chất lỏng thành lực tác động guốc phanh.')])
F('brakeair','10.3.3','C10_image52.png','Hình 10.45 — Sơ đồ nguyên lý hệ thống phanh khí nén',[
 ('Máy nén khí',13,20,'Tạo nguồn không khí nén cho hệ thống.'),
 ('Bình khí',38,8,'Tích trữ năng lượng khí nén.'),
 ('Van phanh tổng',30,58,'Điều khiển cấp và xả khí theo thao tác bàn đạp.'),
 ('Bầu phanh',17,72,'Biến áp suất khí thành lực cơ khí tác động phanh.')])
F('brakecombined','10.3.4','C10_image62.png','Hình 10.54 — Sơ đồ hệ thống phanh thủy lực – khí nén',[
 ('Máy nén khí',88,30,'Cấp nguồn khí nén cho hệ thống.'),
 ('Bình khí',46,19,'Tích trữ khí nén.'),
 ('Van phân phối',14,19,'Điều khiển khí nén tới cụm xi-lanh kép.'),
 ('Cụm xi-lanh kép',64,51,'Biến tác động khí nén thành áp suất chất lỏng.'),
 ('Đường ống dẫn chất lỏng',16,58,'Truyền áp suất thủy lực tới cơ cấu phanh.')])
F('abs','10.3.5','C10_image65.png','Hình 10.57 — Sơ đồ các cụm chức năng cơ cấu ABS thủy lực',[
 ('Cảm biến tốc độ',19,31,'Cung cấp thông tin tốc độ quay bánh xe.'),
 ('Xi-lanh chính',43,13,'Tạo áp suất phanh do người lái tác động.'),
 ('ECU điều khiển',45,90,'Xử lý trạng thái bánh xe và phát lệnh điều chỉnh.'),
 ('Bộ chấp hành thủy lực',42,52,'Thực hiện tăng, giữ hoặc giảm áp suất phanh theo lệnh.')])
F('leaf','11.2.1','C11_image1.png','Hình 11.1 — Lắp nhíp trên xe',[
 ('Khung xe',24,9,'Tiếp nhận tải trọng và liên kết với hai đầu nhíp.'),
 ('Bó nhíp',38,40,'Vừa đàn hồi vừa dẫn hướng trong kết cấu minh họa.'),
 ('Bu lông quang nhíp',48,43,'Bắt chặt bó nhíp với cầu xe.'),
 ('Cầu xe',53,50,'Liên kết hai bánh xe trong hệ thống treo phụ thuộc.')])
F('macpherson','11.2.2','C11_image20.png','Hình 11.16 — Sơ đồ hệ thống treo MacPherson',[
 ('Lò xo',61,26,'Đảm nhận chức năng đàn hồi.'),
 ('Giảm chấn',48,53,'Đồng thời là đòn đứng trong kết cấu MacPherson.'),
 ('Cam quay bánh xe',47,69,'Liên kết bánh xe với bộ phận dẫn hướng.'),
 ('Đòn dưới',65,82,'Dẫn hướng và truyền lực giữa bánh xe với khung.')])
F('coilspring','11.3.1','C11_image26.png','Hình 11.21 — Hệ thống treo có bộ phận đàn hồi là lò xo xoắn',[
 ('Lò xo xoắn',50,72,'Đàn hồi theo hành trình biến dạng, đỡ tải trọng thẳng đứng.'),
 ('Giảm chấn',59,49,'Tiêu tán năng lượng dao động thành nhiệt.'),
 ('Đòn trên',71,48,'Tham gia cơ cấu dẫn hướng bánh xe.'),
 ('Đòn dưới',68,79,'Tham gia truyền lực và xác định quỹ đạo bánh xe.')])
F('airspring','11.3.2','C11_image39.png','Hình 11.32 — Bộ phận đàn hồi khí nén',[
 ('Vỏ cao su',29,20,'Bao kín thể tích khí và biến dạng theo hành trình.'),
 ('Vành kim loại',15,57,'Giữ phần mép của vỏ cao su theo kết cấu.'),
 ('Màng cao su',73,41,'Biến dạng để thay đổi thể tích khí trong phần tử đàn hồi.'),
 ('Vỏ kim loại',85,12,'Giới hạn buồng khí trong kết cấu dùng màng cao su.')])
F('monodamper','11.4.1','C11_image46.png','Hình 11.39 — Giảm chấn kiểu ống đơn',[
 ('Cần pit tông',36,24,'Dẫn chuyển động dao động tới pit tông thủy lực.'),
 ('Pit tông thủy lực',36,42,'Chia khoang dầu và mang các đường van nén, trả.'),
 ('Pit tông khí',35,67,'Dịch chuyển để bù thay đổi thể tích do cần pit tông chiếm chỗ.'),
 ('Khoang III',32,77,'Chứa chất khí có thể nén để bù thể tích.')])
F('twindamper','11.4.2','C11_image47.png','Hình 11.40 — Giảm chấn kiểu ống kép',[
 ('Cần pit tông',38,33,'Truyền chuyển động dao động tới pit tông.'),
 ('Pit tông',39,63,'Chia khoang I và II trong vỏ trong.'),
 ('Vỏ trong',57,74,'Tạo xi-lanh làm việc của giảm chấn.'),
 ('Vỏ ngoài',68,72,'Bao ngoài và tạo khoảng không cho khoang bù.'),
 ('Đế van',41,83,'Mang đường van trao đổi dầu với khoang bù.')])
F('hydractive','11.5.1','C11_image52.png','Hình 11.45 — Các bộ phận và hệ thống của khung gầm Hydractive',[
 ('Cảm biến đo độ cao',40,63,'Cung cấp độ cao tương đối của khung gầm.'),
 ('Cụm thủy lực',22,53.5,'Cấp và điều khiển dòng dầu tới các phần tử đàn hồi.'),
 ('Quả cầu lò xo ở giữa',43,66.5,'Bổ sung thể tích khí khi được nối vào mạch để tạo chế độ mềm.'),
 ('Bộ điều khiển',38,76,'Nhận tín hiệu để quyết định trạng thái của hệ thống.')])
F('cdc','11.5.2','C11_image55.png','Hình 11.48 — Sơ đồ nối mạch của bộ giảm chấn điện tử',[
 ('Nút chọn',20,25,'Nhận lựa chọn chế độ chuyển động của người lái.'),
 ('Bộ điều khiển',49,44,'Tính toán và phát lệnh điều chỉnh lực giảm chấn.'),
 ('Các cảm biến đo độ cao của xe',12,75,'Cung cấp thông tin trạng thái dao động của xe.'),
 ('Các van thay đổi lực giảm chấn',61,73,'Điều chỉnh đường dầu để thay đổi lực cản giảm chấn.')])
F('frame','12.1.2','C12_image4.png','Hình 12.4a — Cấu tạo khung xe tải',[
 ('Dầm dọc',42,12,'Thành phần chịu lực chính chạy theo chiều dài khung.'),
 ('Dầm ngang',62,12,'Liên kết hai dầm dọc và gia cường độ cứng vững.'),
 ('Giá đỡ',45,22,'Tạo vị trí lắp và định vị các cụm tổng thành.')])
F('tipper','12.2.2','C12_image33.png','Hình 12.33 — Sơ đồ bố trí hệ thống nâng hạ thùng xe Kamaz 65115',[
 ('Thùng dầu thủy lực',14,76,'Chứa dầu cho hệ thống nâng hạ.'),
 ('Hộp trích công suất từ hộp số chính',13,46,'Truyền công suất để dẫn động bơm dầu thủy lực.'),
 ('Van điều khiển',16,18,'Chọn đường dầu ứng với nâng, giữ hoặc hạ thùng.'),
 ('Xy lanh thủy lực',34,52,'Biến áp suất dầu thành lực nâng thùng.'),
 ('Van giới hạn nâng sàn',46,64,'Giới hạn nâng theo cơ cấu của hệ thống minh họa.')])

def render_concept(fig):
    height=110+145*((len(fig['parts'])+1)//2)
    # Coordinates expressed in percentages to stay aligned at any screen width.
    for i,p in enumerate(fig['parts']):
        p['x']=8+(i%2)*50
        p['y']=100*(87+(i//2)*145)/height
    drawing=[]
    for i,p in enumerate(fig['parts']):
        x=18+i%2*420;y=35+i//2*145
        drawing.append(f'<rect x="{x}" y="{y}" width="384" height="122" rx="16" fill="#f2f7fa" stroke="#bdcedb" stroke-width="2"/>')
        hint=p['hint'];words=hint.split();lines=[];line=''
        for w in words:
            if len(line+' '+w)>29:lines.append(line);line=w
            else:line=(line+' '+w).strip()
        if line:lines.append(line)
        for n,v in enumerate(lines):
            drawing.append(f'<text x="{x+84}" y="{y+40+n*24}" fill="#233f55" font-family="Arial,sans-serif" font-size="18">{escape(v)}</text>')
        drawing.append(f'<text x="{x+84}" y="{y+105}" fill="#687f91" font-family="Arial,sans-serif" font-size="14">Ô kiến thức {p["id"]}</text>')
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 840 {height}"><rect width="840" height="{height}" fill="white"/>'+''.join(drawing)+'</svg>'
