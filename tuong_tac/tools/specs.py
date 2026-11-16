from figures import C

SPECS = {}
def L(code, figure, steps, nodes=None, kind='torque', links=None, quiz=None, title=None, order_prompt=None):
    SPECS[code] = dict(figure=figure, steps=steps, nodes=nodes, kind=kind, links=links,
                       quiz=quiz, sim_title=title, order_prompt=order_prompt)

def Q(prompt, correct, wrong1, wrong2, explanation):
    return dict(prompt=prompt, options=[correct,wrong1,wrong2], answer=0, explanation=explanation)

# Each step is (action/title, explanation, active node IDs, active path IDs).
def S(title, explanation, nodes='', paths=''):
    return dict(title=title, text=explanation, active=list(nodes), paths=paths.split() if paths else [])

C('vehicles','1.1.1','Phân loại ô tô theo kết cấu',[
 ('Ô tô du lịch','Chở người, hành lý gọn nhẹ','Có các khoang động cơ, chở người và hành lý.'),
 ('Ô tô khách','Vận chuyển hành khách','Được thiết kế để chở người với số ghế theo nhóm xe.'),
 ('Ô tô tải','Không gian chứa hàng lớn','Mục đích chính là vận tải hàng hóa.'),
 ('HTTL cơ khí','Các cụm truyền cơ khí','Bao gồm ly hợp, hộp số, trục truyền các đăng và cầu chủ động.')])
L('1.1.1','vehicles',[
 S('Xác định đối tượng chuyên chở','Đọc mục đích sử dụng: người, hành lý hay hàng hóa.','ABC'),
 S('Quan sát các khoang của xe','Ô tô du lịch có khoang động cơ, khoang chở người và khoang hành lý.','A'),
 S('Đối chiếu kết cấu phục vụ công dụng','Ô tô tải cần không gian chứa hàng lớn; ô tô khách ưu tiên chở người.','BC'),
 S('Kết luận theo đúng tiêu chí','Phân loại công dụng và phân loại HTTL là hai tiêu chí riêng.','ABCD')],kind='concept',title='Trình tự phân biệt nhóm ô tô')
C('bodynames','1.1.2','Tên gọi các kiểu ô tô',[
 ('Sedan','Ba khoang, cốp thấp hơn nóc','Có khoang hành lý riêng, nắp ca pô và cốp thấp hơn nóc khoang hành khách.'),
 ('Hatchback','Cốp nối với kính sau','Nắp cốp liền với kính sau và nối lên trần khoang hành khách.'),
 ('Coupe','Hai cửa, dáng thể thao','Có thiết kế giống Sedan nhưng hai cửa và kiểu dáng thể thao theo bài học.'),
 ('Pick up','Khoang hàng tách buồng lái','Ô tô bán tải, thuộc các tên gọi được trình bày trong bài.')])
L('1.1.2','bodynames',[
 S('Quan sát hình dáng thân xe','Nhận diện số khoang, cửa và phần đuôi xe.','ABCD'),
 S('Kiểm tra quan hệ cốp và kính sau','Cốp tách riêng gợi ý Sedan; cốp liền kính sau gợi ý Hatchback.','AB'),
 S('Đối chiếu cửa và khoang hàng','Coupe có hai cửa theo mô tả; Pick up là ô tô bán tải.','CD'),
 S('Chọn tên gọi phù hợp','Dùng đúng tên gọi được ghi dưới hình trong bài 1.1.2.','ABCD')],kind='concept',title='Trình tự nhận biết hình dáng vỏ xe')
C('wheelcode','1.1.3','Công thức bánh xe A×B',[
 ('A','Tổng số bánh xe','Số bánh xe theo quy ước: mỗi cụm bánh kép được tính như một bánh.'),
 ('B','Số bánh xe chủ động','Số bánh xe nhận mô men dẫn động, cũng tính bánh kép theo quy ước.'),
 ('4×2','Bốn bánh, hai bánh nhận mô men','Có bốn vị trí bánh xe, hai vị trí chủ động.'),
 ('6×4','Sáu bánh, bốn bánh nhận mô men','Có sáu vị trí bánh xe, bốn vị trí chủ động.')])
L('1.1.3','wheelcode',[
 S('Quy đổi cụm bánh kép','Mỗi cụm bánh kép được xem như một bánh khi lập công thức.','A'),
 S('Đếm tổng số bánh theo quy ước','Giá trị đếm được là A.','A'),
 S('Đếm số bánh xe chủ động','Xác định các vị trí nhận mô men dẫn động để có B.','B'),
 S('Viết công thức A×B','Ví dụ A=6, B=4 thì công thức là 6×4.','D')],kind='concept',title='Trình tự xác định công thức bánh xe')
C('powerplant','1.2.1','Nguồn động lực trên ô tô',[
 ('Động cơ xăng','Động cơ đốt trong dùng xăng','Một trong hai loại động cơ đốt trong thông dụng được nêu trong bài.'),
 ('Động cơ Diesel','Động cơ đốt trong dùng Diesel','Một loại nguồn động lực đốt trong được nêu trong bài.'),
 ('Động cơ điện','Nguồn động lực bằng điện','Được đề cập như một xu hướng nguồn động lực ô tô.'),
 ('Máy phát điện','Thiết bị nhận dẫn động','Có thể được dẫn động bởi động cơ ô tô.')])
L('1.2.1','powerplant',[
 S('Động cơ phát mô men quay','Động cơ là nguồn động lực của ô tô.','A'),
 S('Mô men đi vào hệ thống truyền lực','Các bộ phận truyền lực đưa mô men tới bánh xe chủ động.','AB','AB'),
 S('Bánh xe chủ động nhận mô men','Tác động giữa bánh xe và mặt đường tạo điều kiện cho xe chuyển động.','ABC','AB BC'),
 S('Thiết bị phụ nhận dẫn động','Động cơ còn dẫn động máy phát điện, máy nén khí và thiết bị khác theo bài.','AD','AD')],nodes='Động cơ|Hệ thống truyền lực|Bánh xe chủ động|Máy phát điện',links='AB BC AD',title='Đường truyền từ nguồn động lực')
L('1.2.2','driveline',[
 S('Động cơ phát mô men','Mô men từ động cơ đi tới ly hợp.','AB','AB'),
 S('Ly hợp nối với hộp số','Ly hợp đóng để truyền mô men; hộp số biến đổi mô men và tốc độ.','ABC','AB BC'),
 S('Các đăng truyền tới cầu xe','Theo sơ đồ bố trí, trục các đăng nối các cụm truyền lực.','ABCDE','AB BC CD DE'),
 S('Bánh xe chủ động nhận mô men','Cầu xe phân phối mô men tới bánh xe chủ động.','ABCDEF','AB BC CD DE EF')],nodes='Động cơ|Ly hợp|Hộp số|Trục các đăng|Cầu xe|Bánh xe chủ động',links='AB BC CD DE EF')
L('1.2.3','steer',[
 S('Người lái quay vành tay lái','Thao tác điều khiển đưa chuyển động vào hệ thống lái.','A'),
 S('Trục lái truyền chuyển động','Trục lái nối vành tay lái với cơ cấu lái.','AB','AB'),
 S('Cơ cấu lái tác động dẫn động lái','Lực và chuyển động được truyền tới các thanh dẫn động.','ABCD','AB BC CD'),
 S('Bánh xe dẫn hướng đổi góc','Bánh xe dẫn hướng quay theo yêu cầu để thay đổi hướng chuyển động.','ABCDE','AB BC CD DE')],nodes='Vành tay lái|Trục lái|Cơ cấu lái|Dẫn động lái|Bánh xe dẫn hướng',kind='control',links='AB BC CD DE')
L('1.2.4','drum',[
 S('Người lái yêu cầu giảm tốc','Lực điều khiển được đưa vào dẫn động phanh.','A'),
 S('Dẫn động tác động cơ cấu phanh','Dẫn động truyền tác động tới cơ cấu phanh bánh xe.','AB','AB'),
 S('Cơ cấu phanh tạo mô men cản','Tiếp xúc ma sát tại cơ cấu phanh chống lại sự quay của bánh xe.','ABC','AB BC'),
 S('Xe giảm tốc hoặc được giữ đứng yên','Công dụng hệ thống còn bao gồm giữ xe khi đỗ theo thiết kế.','ABCD','AB BC CD')],nodes='Điều khiển phanh|Dẫn động phanh|Cơ cấu phanh|Bánh xe',kind='control',links='AB BC CD')
L('1.2.5','frame',[
 S('Các cụm tạo tải trọng lên khung','Khung, vỏ là nơi giá đỡ các cụm và hệ thống trên ô tô.','A'),
 S('Khung, vỏ tiếp nhận tải trọng','Kết cấu chịu lực đỡ và định vị các cụm lắp trên xe.','AB','AB'),
 S('Tải được truyền qua hệ thống treo','Liên kết với hệ thống treo đưa tải xuống cầu và bánh xe.','ABC','AB BC'),
 S('Bánh xe truyền tải xuống mặt đường','Khung, vỏ đồng thời tạo không gian bảo vệ người trên xe.','ABCD','AB BC CD')],nodes='Các cụm trên xe|Khung, vỏ|Hệ thống treo|Bánh xe',kind='force',links='AB BC CD',title='Quan hệ đỡ tải của khung, vỏ')
L('1.2.6','coilspring',[
 S('Bánh xe gặp mấp mô','Bánh xe chịu kích động từ mặt đường.','A'),
 S('Bộ phận đàn hồi biến dạng','Liên kết mềm giữa bánh xe và khung vỏ giúp giảm chấn động.','AB','AB'),
 S('Giảm chấn dập dao động','Giảm chấn phối hợp phần tử đàn hồi để dao động giảm nhanh.','ACD','AC CD'),
 S('Khung, vỏ được đỡ êm dịu','Hệ thống treo đỡ khối lượng khung vỏ và các bộ phận trên đó.','ABCD','AB BD AC CD')],nodes='Bánh xe|Bộ phận đàn hồi|Giảm chấn|Khung, vỏ',kind='force',links='AB BD AC CD')
C('electric','1.2.7','Các hệ thống điện ô tô',[
 ('Hệ thống khởi động','Accu và máy khởi động điện','Cung cấp tác động khởi động với các relay điều khiển và bảo vệ.'),
 ('Hệ thống cung cấp điện','Accu, máy phát, bộ tiết chế','Cung cấp điện và điều chỉnh chế độ nạp.'),
 ('Hệ thống đánh lửa','Bobine và bougie','Tạo tác động đánh lửa theo mạch được nêu trong bài.'),
 ('Hệ thống chiếu ánh sáng và tín hiệu','Đèn, còi và công tắc','Phục vụ chiếu sáng và phát tín hiệu của xe.')])
L('1.2.7','electric',[
 S('Accu cấp điện cho khởi động','Hệ thống khởi động gồm accu, máy khởi động và các relay.','A'),
 S('Máy khởi động nhận điện','Relay điều khiển và bảo vệ tham gia mạch; máy khởi động đưa tác động quay tới động cơ.','ABC','AB BC'),
 S('Động cơ dẫn động máy phát','Khi động cơ làm việc, máy phát được dẫn động cơ khí.','CD','CD'),
 S('Bộ tiết chế điều chỉnh nạp','Hệ thống cung cấp điện có accu, máy phát và bộ tiết chế.','ADE','DE EA')],nodes='Accu|Máy khởi động điện|Động cơ|Máy phát điện|Bộ tiết chế điện',kind='signal',links='AB:signal BC:torque CD:torque DE:signal EA:signal',title='Quan hệ khởi động và cung cấp điện')
C('dimensions','1.3.1','Thông số hình học cơ bản',[
 ('Chiều dài cơ sở','Khoảng cách hai tâm cầu xa nhất','Khoảng cách từ tâm bánh xe trước đến tâm bánh xe sau; xe nhiều cầu lấy hai cầu xa nhất.'),
 ('Chiều rộng cơ sở','Khoảng cách tâm lốp trái–phải','Khoảng cách từ tâm lốp bên trái đến tâm lốp bên phải.'),
 ('Khoảng sáng gầm','Điểm thấp nhất gầm tới mặt đất','Khoảng cách từ mặt đất đến điểm thấp nhất của gầm xe.'),
 ('Bán kính quay vòng tối thiểu','Tâm quay tới bánh ngoài cùng','Được xác định khi đánh lái hết cỡ, đo tới bánh xe ngoài cùng theo bài.')])
L('1.3.1','dimensions',[
 S('Chọn tâm bánh trước và sau','Xác định hai tâm cầu để xét chiều dài cơ sở.','A'),
 S('Chọn tâm lốp trái và phải','Quan sát cùng một cầu để xét chiều rộng cơ sở.','B'),
 S('Chọn điểm thấp nhất của gầm','Đo khoảng cách từ điểm này tới mặt đất để có khoảng sáng gầm.','C'),
 S('Đánh lái hết cỡ để xét vòng quay','Xét bán kính từ tâm quay tới bánh ngoài cùng theo tài liệu.','D')],kind='concept',title='Trình tự nhận biết thông số hình học',order_prompt='Sắp xếp trình tự khảo sát các thông số trong phần minh họa: dọc xe → ngang xe → dưới gầm → quay vòng.')
C('parameters','1.3.2','Thông số kết cấu ô tô',[
 ('Dung tích xi lanh','Thể tích được pit-tông quét','Thể tích xi lanh quét bởi pit-tông từ điểm chết trên đến điểm chết dưới.'),
 ('Công suất','Thông số khả năng phát động lực','Thông số biểu đạt sức mạnh của động cơ theo bảng thông số trong bài.'),
 ('Mô men xoắn','Tác động quay của động cơ','Thông số tác động quay gắn với khả năng chịu tải theo bài học.'),
 ('Hệ thống truyền lực','FWD, RWD, 4WD, AWD','Nhóm thông số mô tả dạng dẫn động của xe.')])
L('1.3.2','parameters',[
 S('Đọc nhóm thông số động cơ','Xác định dung tích xi lanh trong bảng thông số.','A'),
 S('Đọc công suất được công bố','Ghi nhận công suất theo đơn vị trong tài liệu.','B'),
 S('Đọc mô men xoắn','Phân biệt mô men xoắn với công suất, không dùng thay tên cho nhau.','C'),
 S('Đọc dạng dẫn động','Đối chiếu FWD, RWD, 4WD hoặc AWD trong nhóm hệ thống truyền lực.','D')],kind='concept',title='Trình tự đọc nhóm thông số kết cấu')

# Chapter 3 — mechanical gearboxes
L('3.1.1','gear3',[
 S('Nhận mô men ở trục sơ cấp','Hộp số nhận mô men từ ly hợp.','A'),
 S('Chọn cấp số truyền','Cặp bánh răng được chọn làm thay đổi mô men và tốc độ quay.','AB','AB'),
 S('Truyền ra bánh xe chủ động','Đường truyền từ trục thứ cấp đi tới các cụm phía sau hộp số.','ABC','AB BC'),
 S('Chuyển về số trung gian khi cần ngắt','Số trung gian cho phép ngắt dòng truyền lực lâu dài khi động cơ vẫn làm việc.','A')],nodes='Trục sơ cấp|Cặp bánh răng|Trục thứ cấp',links='AB BC')
C('gearclasses','3.1.2','Phân loại hộp số chính',[
 ('Trục cố định','Các trục giữ vị trí','Một dạng phân loại theo đặc điểm bố trí trục hộp số.'),
 ('Trục di động','Bộ bánh răng hành tinh','Các trục bánh răng hành tinh có thể di động theo cần dẫn.'),
 ('Hộp số hai trục','Chủ động và bị động','Có hai trục chính theo cách phân loại trong bài.'),
 ('Hộp số ba trục','Thêm trục trung gian','Có trục chủ động, trục bị động và trục trung gian.')])
L('3.1.2','gearclasses',[
 S('Xét trạng thái trục','Phân biệt trục cố định với trục di động.','AB'),
 S('Đếm số trục chính','Phân biệt hai trục, ba trục hoặc hai trục bị động theo sơ đồ.','CD'),
 S('Xét số cấp số truyền','Số cấp truyền là một tiêu chí khác số trục.'),
 S('Xét phương pháp điều khiển','Kết luận từng tiêu chí riêng: bằng tay hay tự động.','ABCD')],kind='concept',title='Trình tự phân loại hộp số')
C('gearsymbols','3.2.1','Kiểu liên kết bánh răng với trục',[
 ('Bánh răng lắp cố định với trục','Không quay tương đối','Bánh răng quay cùng trục, không trượt dọc trục.'),
 ('Bánh răng trượt dọc trên trục','Quay cùng, trượt dọc','Liên kết bằng then hoa cho phép dịch chuyển theo đường trục.'),
 ('Bánh răng quay trơn','Có thể quay tương đối','Chưa bị cố định với trục nếu cơ cấu gài chưa nối.'),
 ('Bộ đồng tốc','Đồng đều tốc độ trước gài','Giúp cân bằng tốc độ và nối bánh răng được chọn với trục.')])
L('3.2.1','gearsymbols',[
 S('Xác định ký hiệu trục và bánh răng','Đọc phần biểu diễn liên kết thay vì chỉ nhìn hình dáng.','ABCD'),
 S('Kiểm tra khả năng quay tương đối','Lắp cố định quay cùng trục; quay trơn cho phép quay tương đối.','AC'),
 S('Kiểm tra khả năng trượt dọc trục','Bánh răng lắp trượt then hoa có thể dịch chuyển dọc trục.','B'),
 S('Đối chiếu cơ cấu gài hoặc đồng tốc','Chỉ kết luận đường truyền khi cơ cấu gài nối đúng phần tử.','D')],kind='concept',title='Trình tự đọc ký hiệu vẽ quy ước')
L('3.2.2','gear3',[
 S('Số trung gian','Các khớp gài chưa nối bánh răng được chọn với trục thứ cấp.','AB','AB'),
 S('Gài một số tiến gián tiếp','Mô men qua trục sơ cấp, trục trung gian và cặp bánh răng được chọn tới trục thứ cấp.','ABCD','AB BC CD'),
 S('Gài số truyền thẳng','Khớp gài nối trục sơ cấp trực tiếp với trục thứ cấp; tỷ số truyền bằng 1.','AD','AD'),
 S('Gài số lùi','Bánh răng trung gian số lùi tham gia đường truyền để đảo chiều trục thứ cấp.','ABED','AB BE ED')],nodes='Trục sơ cấp|Trục trung gian|Bánh răng số tiến|Trục thứ cấp|Bánh răng gài số lùi',links='AB BC CD AD BE ED',title='Các đường truyền của hộp số 3 trục',order_prompt='Sắp xếp các trạng thái theo thứ tự khảo sát trong minh họa: trung gian → số tiến gián tiếp → truyền thẳng → số lùi.',quiz=Q('Khi khớp gài nối trục sơ cấp trực tiếp với trục thứ cấp, tỷ số truyền là bao nhiêu?','i = 1','i lớn hơn 1','Trục thứ cấp không quay','Số truyền thẳng nối hai trục trực tiếp, không đi qua cặp bánh răng giảm tốc.'))
L('3.2.3','gear2',[
 S('Trục sơ cấp nhận mô men','Hộp số hai trục nhận mô men từ ly hợp.','A'),
 S('Đồng tốc nối bánh răng được chọn','Cơ cấu gài cố định bánh răng của cấp số đã chọn với trục.','C'),
 S('Cặp bánh răng truyền tới trục thứ cấp','Đường truyền qua cặp bánh răng ứng với cấp số, không qua trục trung gian như hộp số ba trục.','ABCD','AB BC CD'),
 S('Truyền lực chính nhận đầu ra','Ở dạng transaxles, vỏ hộp số liền với vỏ truyền lực chính.','ABCDE','AB BC CD DE')],nodes='Trục sơ cấp|Cặp bánh răng đã chọn|Bộ đồng tốc|Trục thứ cấp|Truyền lực chính',links='AB BC CD DE',title='Đường truyền trong hộp số hai trục')
C('gearparts','3.2.4','Bánh răng, trục và ổ đỡ',[
 ('Bánh răng trụ răng thẳng','Thường dùng gài số lùi','Bánh răng răng thẳng được dùng ở bộ phận gài số lùi được mô tả.'),
 ('Bánh răng trụ răng nghiêng','Nhiều răng cùng tiếp xúc','Hoạt động êm hơn và phát sinh lực dọc trục.'),
 ('Ổ đỡ cố định','Định vị theo hướng trục','Chịu lực hướng trục và không được di động theo hướng trục.'),
 ('Ổ đỡ di động','Cho phép bù giãn nở','Có một vòng được phép di động theo hướng trục để bù dung sai và giãn nở.')])
L('3.2.4','gearparts',[
 S('Bánh răng truyền mô men','Cặp bánh răng ăn khớp truyền mô men giữa các trục.','A'),
 S('Trục tiếp nhận các tải tác dụng','Trục và ổ đỡ phải chịu các lực do ăn khớp gây ra.','AB','AB'),
 S('Ổ đỡ cố định định vị hướng trục','Lực hướng trục được tiếp nhận ở ổ đỡ cố định.','ABC','AB BC'),
 S('Ổ đỡ di động bù giãn nở','Vòng được phép dịch chuyển giúp tránh căng cứng do giãn nở.','BD','BD')],nodes='Bánh răng|Trục|Ổ đỡ cố định|Ổ đỡ di động',kind='force',links='AB BC BD',title='Quan hệ truyền lực và định vị trục')
L('3.3.1','shift',[
 S('Chọn cửa gài số','Cần số chọn bánh răng di động hoặc bộ đồng tốc cần thiết.','A'),
 S('Dịch chuyển trục trượt','Thao tác đúng hướng đưa chuyển động tới trục trượt.','AB','AB'),
 S('Càng gài số đẩy cơ cấu gài','Càng gài đẩy ống gài số hoặc bánh răng tới vị trí yêu cầu.','ABC','AB BC'),
 S('Định vị ở vị trí gài đủ','Viên bi và lò xo định vị giữ vị trí đã chọn.','ABCD','AB BC CD')],nodes='Cần số|Trục trượt|Càng gài số|Cơ cấu định vị',kind='control',links='AB BC CD')
L('3.3.2','shift',[
 S('Ống trượt tiến tới bánh răng','Thao tác gài làm ống trượt và vành ma sát dịch chuyển.','A'),
 S('Mặt côn tạo mô men ma sát','Mặt côn vành đồng ma sát tỳ vào mặt côn bánh răng.','AB','AB'),
 S('Tốc độ được làm đồng đều','Mô men ma sát làm giảm chênh lệch tốc độ trước khi ăn khớp răng gài.','ABC','AB BC'),
 S('Răng gài ăn khớp hoàn toàn','Ống trượt nối bánh răng với trục; cơ cấu định vị giữ vị trí gài.','ABCD','AB BC CD')],nodes='Ống trượt|Vành đồng ma sát|Bánh răng gài số|Trục',kind='control',links='AB BC CD',title='Quá trình đồng tốc và gài số',quiz=Q('Nếu tốc độ bánh răng và trục chưa đồng đều, bộ đồng tốc cần làm gì trước khi gài răng?','Tạo mô men ma sát ở mặt côn','Khóa cứng hai số cùng lúc','Bỏ qua mặt côn và gài ngay','Mặt côn tạo mô men ma sát để đồng đều tốc độ; cơ cấu khóa hãm có nhiệm vụ khác.'))

# Chapter 4 — automatic transmissions
L('4.1.1','dct',[
 S('Thu nhận điều kiện chuyển động','Trạng thái xe và yêu cầu công suất cung cấp thông tin điều khiển.','A'),
 S('Chọn tỷ số truyền thích hợp','Bộ điều khiển xác định tỷ số truyền theo điều kiện chuyển động.','AB','AB'),
 S('Cơ cấu chấp hành chuyển số','Các phần tử chấp hành thực hiện thay đổi đường truyền.','ABC','AB BC'),
 S('Tiếp tục truyền mô men','Quá trình được tổ chức để chuyển số êm dịu theo loại hộp số.','ABCD','AB BC CD')],nodes='Điều kiện chuyển động|Điều khiển hộp số|Cơ cấu chấp hành|Đường truyền mô men',kind='signal',links='AB BC CD',title='Quan hệ điều khiển tự động chọn số')
C('autotypes','4.1.2','Các loại hộp số tự động',[
 ('Hộp số tự động có cấp với biến mô thủy lực','Biến mô và các cấp truyền','Có các tỷ số truyền theo cấp, được trình bày ở mục 4.3.'),
 ('Hộp số tự động vô cấp (CVT)','Tỷ số truyền thay đổi liên tục','Dạng truyền động vô cấp được trình bày ở mục 4.4.'),
 ('Hộp số cơ khí được tự động hóa','Điều khiển thao tác cơ khí','Bộ điều khiển và chấp hành thực hiện đóng ngắt, gài số.')])
L('4.1.2','autotypes',[
 S('Xác định cơ cấu truyền chính','Quan sát biến mô, bộ bánh răng hoặc bộ truyền vô cấp.','ABC'),
 S('Xét các cấp số truyền','Phân biệt tỷ số theo cấp với thay đổi liên tục.','AB'),
 S('Xét cơ cấu thực hiện chuyển số','Đối chiếu bộ điều khiển và các cơ cấu chấp hành.','C'),
 S('Gọi đúng loại hộp số','Chọn tên loại được dùng trong mục 4.1.2.','ABC')],kind='concept',title='Trình tự phân biệt hộp số tự động')
for code in ['4.2.1','4.2.2']:
 L(code,'dct',[
  S('Nhánh số 2 đang truyền mô men','Ly hợp 2 đóng, nhánh số chẵn đang truyền mô men.','ABDF','AB BD DF'),
  S('Chọn trước số 3 trên nhánh còn lại','Ly hợp 1 còn ngắt; cơ cấu điều khiển chọn bánh răng số 3.','C'),
  S('Chuyển tác động giữa hai ly hợp','Giảm tác động ly hợp 2 đồng thời tăng tác động ly hợp 1. Đây là bước chuyển tiếp, không khóa cứng hai nhánh.','ABCDEF','AB BD DF AC CE EF'),
  S('Nhánh số 3 tiếp nhận mô men','Ly hợp 1 đóng và nhánh số lẻ truyền mô men tới đầu ra.','ACEF','AC CE EF')],nodes='Động cơ|Ly hợp 2|Ly hợp 1|Nhánh số 2|Nhánh số 3|Trục thứ cấp và bộ vi sai',links='AB BD DF AC CE EF',title='Ví dụ chuyển từ số 2 sang số 3',quiz=Q('Khi đang chạy số 2 và đã chọn trước số 3, thao tác chuyển số thực hiện thế nào?','Ngắt ly hợp 2, đóng ly hợp 1 theo điều khiển','Đóng cứng cả hai ly hợp ở hai cấp số','Dùng bàn đạp ly hợp để gài thủ công','Trong ví dụ của bài, điều khiển chuyển mô men từ nhánh số chẵn sang nhánh số lẻ.'))
L('4.3.1','converter',[
 S('Bánh bơm được động cơ dẫn động','Bánh bơm đưa năng lượng vào dầu trong biến mô.','A'),
 S('Dầu tác động bánh tua-bin','Dòng dầu làm bánh tua-bin quay và truyền mô men tới hộp số.','AB','AB'),
 S('Stato đổi hướng dòng dầu trở về','Ở chế độ biến mô, stato được khớp một chiều giữ theo chiều tác động.','ABC','AB BC CA'),
 S('Stato được giải phóng ở chế độ ly hợp','Khi điều kiện dòng dầu thay đổi, khớp một chiều cho stato quay theo.','ABC','AB BC CA')],nodes='Bánh bơm|Bánh tua-bin|Stato',kind='fluid',links='AB BC CA',title='Vòng tuần hoàn dầu trong biến mô',quiz=Q('Dòng dầu ra khỏi bánh tua-bin trở về bánh bơm qua bộ phận nào?','Stato','Cơ cấu định vị số','Càng gài số','Stato nhận dòng dầu từ bánh tua-bin và đổi hướng dòng trở về bánh bơm.'))
C('planetary','4.3.2','Bộ bánh răng hành tinh',[
 ('Bánh răng mặt trời','Bánh răng ở tâm bộ truyền','Một trong ba phần tử cơ bản quyết định trạng thái truyền động.'),
 ('Bánh răng bao','Vành răng trong bên ngoài','Phần tử ngoài ăn khớp các bánh răng hành tinh.'),
 ('Bánh răng hành tinh','Các bánh răng trên cần dẫn','Có thể quay quanh trục của mình và chuyển động quanh bánh răng mặt trời.'),
 ('Cần dẫn','Mang trục bánh răng hành tinh','Phần tử mang các bánh răng hành tinh và có thể làm đầu vào hoặc đầu ra.')])
L('4.3.2','planetary',[
 S('Giữ bánh răng mặt trời','Trong ví dụ chế độ giảm tốc, bánh răng mặt trời là phần tử được giữ.','A'),
 S('Dẫn động bánh răng bao','Bánh răng bao quay và tác động lên các bánh răng hành tinh.','BC','BC'),
 S('Bánh răng hành tinh chuyển động','Các bánh răng hành tinh vừa quay vừa chuyển động quanh mặt trời.','BCD','BC CD'),
 S('Cần dẫn tạo đầu ra giảm tốc','Tốc độ cần dẫn nhỏ hơn tốc độ bánh răng bao theo tỷ số răng của bộ truyền.','BCD','BC CD')],nodes='Bánh răng mặt trời|Bánh răng bao|Bánh răng hành tinh|Cần dẫn',links='BC CD',title='Ví dụ giảm tốc của bộ truyền hành tinh',quiz=Q('Trong ví dụ bánh răng mặt trời được giữ và bánh răng bao dẫn động, đầu ra giảm tốc là phần tử nào?','Cần dẫn','Vỏ hộp số','Bánh răng mặt trời đang bị giữ','Cần dẫn nhận chuyển động qua bánh răng hành tinh và quay chậm hơn bánh răng bao.'))
C('ect','4.3.3','Điều khiển hộp số điện – thủy lực',[
 ('Bơm dầu','Nguồn áp suất thủy lực','Được động cơ dẫn động để tạo áp suất cần cho hoạt động hộp số.'),
 ('Van điều áp sơ cấp','Điều chỉnh áp suất cơ bản','Điều chỉnh áp suất dầu do bơm tạo ra.'),
 ('Van điện từ','Nhận lệnh điện từ ECU','Tác động các van chuyển số để đổi đường dẫn dầu.'),
 ('Bộ tích năng','Áp suất tăng dần khi chuyển số','Làm giảm chấn động khi áp suất tới ly hợp, phanh tăng dần.')])
L('4.3.3','ect',[
 S('Bơm dầu tạo nguồn áp suất','Dầu có áp được đưa vào mạch điều khiển.','A'),
 S('Van điều áp điều chỉnh áp suất','Áp suất cơ bản được điều chỉnh theo yêu cầu.','AB','AB'),
 S('ECU điều khiển van điện từ','Tín hiệu điện làm thay đổi trạng thái van điện từ và van chuyển số.','CDE','CD DE'),
 S('Dầu tới ly hợp hoặc phanh','Đường dẫn dầu đã chọn làm ly hợp và phanh của bộ truyền hoạt động.','ABEF','AB BE EF')],nodes='Bơm dầu|Van điều áp sơ cấp|ECU động cơ & ECT|Van điện từ|Van chuyển số|Ly hợp và phanh',kind='fluid',links='AB CD DE BE EF',title='Tạo áp suất và chuyển mạch dầu')
for code in ['4.4.1','4.4.2']:
 L(code,'cvt',[
  S('Hai mặt côn sơ cấp xa nhau','Đai truyền làm việc ở bán kính nhỏ hơn phía sơ cấp.','A'),
  S('Hai mặt côn thứ cấp gần nhau','Phía thứ cấp tạo bán kính lớn hơn, phối hợp với phía sơ cấp.','AB'),
  S('Dịch chuyển các mặt côn ngược chiều','Sơ cấp gần lại, thứ cấp xa ra; hai bán kính làm việc thay đổi phối hợp.','AB'),
  S('Tỷ số truyền thay đổi liên tục','Đai truyền đưa mô men giữa hai trục khi bán kính làm việc được điều chỉnh.','ABC','AC CB')],nodes='Cặp mặt côn sơ cấp|Cặp mặt côn thứ cấp|Đai truyền',links='AC CB',title='Điều chỉnh bán kính làm việc của CVT',quiz=Q('Nếu hai mặt côn ở trục sơ cấp tiến lại gần nhau, bán kính làm việc của đai ở đó thay đổi thế nào?','Tăng lên','Giảm xuống','Không đổi','Hai mặt côn tiến gần đẩy đai ra xa tâm trục; quá trình phía thứ cấp diễn ra phối hợp.'))

# Chapter 5 — transfer cases
L('5.1.1','transfer',[
 S('Nhận mô men từ hộp số chính','Hộp số phân phối đặt sau hộp số chính trên xe nhiều cầu chủ động.','A'),
 S('Đưa mô men vào hộp phân phối','Các phần tử truyền phân chia đường truyền theo kết cấu.','AB','AB'),
 S('Phân phối tới cầu sau','Trục ra đưa mô men tới cầu chủ động phía sau.','ABC','AB BC'),
 S('Phân phối tới cầu trước khi được nối','Nhánh cầu trước nhận mô men theo trạng thái của hộp phân phối.','ABD','AB BD')],nodes='Hộp số chính|Hộp số phân phối|Cầu sau|Cầu trước',links='AB BC BD')
C('transferclasses','5.1.2','Phân loại hộp số phân phối',[
 ('Số lượng cấp số truyền','Một cấp hoặc hai cấp','Tiêu chí số tỷ số truyền của hộp phân phối.'),
 ('Số lượng trục ra','Hai hoặc ba trục ra','Tiêu chí số đầu ra truyền tới các cầu.'),
 ('Đặc điểm phân chia mô men truyền','Cố định hoặc qua bộ vi sai','Tiêu chí phân phối mô men tới các cầu.'),
 ('Phương pháp dẫn động','Thường xuyên hoặc gián đoạn','Tiêu chí tổ chức dẫn động các cầu theo tài liệu.')])
L('5.1.2','transferclasses',[
 S('Đếm cấp số truyền','Một cấp hay hai cấp là đặc điểm tỷ số truyền.','A'),
 S('Đếm các trục ra','Số trục ra độc lập với số cấp số truyền.','B'),
 S('Xét cách phân chia mô men','Phân biệt mô men cố định hay có bộ vi sai.','C'),
 S('Xét cách dẫn động các cầu','Kết luận thường xuyên hoặc gián đoạn theo sơ đồ.','D')],kind='concept',title='Trình tự phân loại hộp phân phối')
L('5.2.1','transfer',[
 S('Chế độ một cầu chủ động','Khớp gài mở; mô men truyền tới cầu sau trong sơ đồ đơn giản.','ABC','AB BC'),
 S('Chuẩn bị nối cầu trước','Với khớp gài vấu răng của sơ đồ, tài liệu yêu cầu thực hiện khi xe đứng yên.','D'),
 S('Đóng khớp gài cầu trước','Khớp gài nối bánh răng bị động với trục ra cầu trước.','ABDE','AB BD DE'),
 S('Hai cầu cùng nhận mô men','Cầu trước và sau được nối; trên đường tốt cần tách cầu trước theo tài liệu.','ABCDE','AB BC BD DE')],nodes='Trục vào|Bánh răng bị động|Cầu sau|Khớp gài cầu trước|Cầu trước',links='AB BC BD DE',title='Nối và tách cầu trước ở hộp phân phối đơn giản')
L('5.2.2','transferlow',[
 S('Gài cầu trước trước','Cơ cấu khóa hãm yêu cầu nối cầu trước trước khi dùng số truyền thấp.','A'),
 S('Gài số truyền thấp','Bánh răng gài số ăn khớp bánh răng số thấp, mô men tăng và tốc độ giảm.','AB','AB'),
 S('Nhả số truyền thấp trước','Khi trở lại số truyền thẳng, phải nhả số thấp trước khi tách cầu trước.','BC','BC'),
 S('Nhả cầu trước sau','Chỉ sau khi nhả số thấp mới nhả cầu trước theo cơ cấu khóa hãm của hình 5.2.','CD','CD')],nodes='Gài cầu trước|Gài số truyền thấp|Nhả số truyền thấp|Nhả cầu trước',kind='control',links='AB BC CD',title='Trình tự khóa hãm ở hộp phân phối hai cấp',quiz=Q('Theo cơ cấu khóa hãm của hình 5.2, muốn gài số truyền thấp phải làm gì trước?','Gài cầu trước','Nhả cầu trước','Tách trục ra cầu sau','Tài liệu yêu cầu gài cầu trước trước khi gài số thấp và nhả số thấp trước khi nhả cầu trước.'))
C('awd','5.3.1','Các bộ vi sai trong dẫn động AWD',[
 ('Bộ vi sai trung tâm','Giữa nhánh trước và sau','Cho phép chênh lệch tốc độ giữa đường truyền tới cầu trước và cầu sau.'),
 ('Bộ vi sai trước','Giữa hai bánh phía trước','Phân phối mô men tới các bánh chủ động của cầu trước.'),
 ('Bộ vi sai sau','Giữa hai bánh phía sau','Phân phối mô men tới các bánh chủ động của cầu sau.'),
 ('Khớp thủy lực','Tác động khi có chênh lệch','Tham gia truyền mô men giữa các nhánh theo kết cấu được trình bày.')])
for code in ['5.3.1','5.3.2']:
 L(code,'awd',[
  S('Mô men tới bộ vi sai trung tâm','Đường truyền vào được chia thành nhánh trước và nhánh sau.','A'),
  S('Hai nhánh truyền tới các cầu','Bộ vi sai trước và sau phân phối tới các bánh của từng cầu.','ABC','AB AC'),
  S('Các cầu có thể khác tốc độ khi quay vòng','Bộ vi sai trung tâm cho phép chênh lệch tốc độ giữa hai nhánh.','ABC','AB AC'),
  S('Khớp thủy lực tác động khi chênh lệch','Trong kết cấu mô tả, khớp góp phần truyền lực khi có chênh lệch trước–sau.','AD','AD')],nodes='Bộ vi sai trung tâm|Bộ vi sai trước|Bộ vi sai sau|Khớp thủy lực',links='AB AC AD',title='Phân phối mô men trong dẫn động thường xuyên',quiz=Q('Khi quay vòng, bộ phận nào cho phép hai nhánh cầu trước và sau có tốc độ khác nhau?','Bộ vi sai trung tâm','Khớp gài nối cứng hai cầu','Cơ cấu định vị số','Vi sai trung tâm xử lý chênh lệch tốc độ giữa các cầu; vi sai tại cầu xử lý chênh lệch giữa hai bánh.'))

# Chapter 6 — propeller shafts and constant velocity joints
L('6.1.1','crossparts',[
 S('Cụm chủ động phát mô men','Truyền động các đăng nối các cụm có vị trí tương đối thay đổi.','A'),
 S('Khớp các đăng truyền khi lệch góc','Khớp cho phép truyền mô men giữa các đường tâm không thẳng hàng.','AB','AB'),
 S('Khớp trượt bù thay đổi chiều dài','Then hoa cho phép thân trục thay đổi chiều dài trong giới hạn làm việc.','ABC','AB BC'),
 S('Cụm bị động nhận mô men','Truyền động vừa bảo đảm truyền lực vừa thích ứng chuyển động tương đối.','ABCD','AB BC CD')],nodes='Cụm chủ động|Khớp các đăng|Khớp trượt|Cụm bị động',links='AB BC CD',title='Thích ứng góc lệch và thay đổi chiều dài')
C('cardanclasses','6.1.2','Phân loại truyền động các đăng',[
 ('Các đăng khác tốc','Tốc độ tức thời không bằng nhau','Khớp đơn lệch góc có tốc độ đầu ra biến thiên khi đầu vào quay đều.'),
 ('Các đăng đồng tốc','Tốc độ tức thời bằng nhau','Đảm bảo quan hệ đồng tốc trong phạm vi làm việc của kết cấu.'),
 ('Truyền động các đăng kín','Có ống bọc bao ngoài','Các bộ phận đặt trong ống bọc bảo vệ theo phân loại trong bài.'),
 ('Truyền động các đăng hở','Không có ống bọc chung','Được phân biệt với loại kín theo kết cấu bao che.')])
L('6.1.2','cardanclasses',[
 S('Xác định công dụng của bộ truyền','Xác định các cụm được nối: hộp số, hộp phân phối, cầu hoặc bánh xe.'),
 S('Xét quan hệ tốc độ tức thời','Phân biệt khác tốc và đồng tốc, không chỉ nhìn tốc độ trung bình.','AB'),
 S('Đếm thân trục và khớp','Số thân, số khớp và gối đỡ là tiêu chí bố trí.'),
 S('Xét kết cấu kín hoặc hở','Quan sát ống bọc và kết luận theo tiêu chí kết cấu.','CD')],kind='concept',title='Trình tự phân loại các đăng')
L('6.2.1','cross',[
 S('Nạng chủ động quay','Nạng 1 nhận chuyển động từ trục chủ động.','A'),
 S('Trục chữ thập liên kết hai nạng','Các chốt chữ thập chuyển động trong lỗ các nạng.','AB','AB'),
 S('Nạng bị động quay theo','Khi lệch góc, tốc độ tức thời của đầu ra không đều dù đầu vào quay đều.','ABC','AB BC'),
 S('Hai khớp phối hợp bù khác tốc','Hai góc làm việc bằng nhau và nạng trung gian đúng pha là điều kiện bố trí được nêu.','ABCD','AB BC CD')],nodes='Nạng chủ động|Trục chữ thập|Nạng bị động|Khớp thứ hai',links='AB BC CD',title='Khớp khác tốc và điều kiện phối hợp hai khớp',quiz=Q('Nếu chỉ dùng một khớp chữ thập lệch góc và trục vào quay đều, tốc độ tức thời trục ra thế nào?','Biến thiên không đều','Luôn bằng tốc độ trục vào','Bằng không ở mọi vị trí','Khớp chữ thập đơn là khớp khác tốc khi hai đường tâm lệch góc.'))
L('6.2.2','crossparts',[
 S('Mô men vào nạng thứ nhất','Nạng và thân trục đưa mô men tới khớp chữ thập.','A'),
 S('Chốt chữ thập làm việc trong ổ bi kim','Ổ bi kim liên kết chốt chữ thập với lỗ trên nạng.','AB','AB'),
 S('Nạng thứ hai nhận mô men','Nắp và vòng hãm giữ ổ bi đúng vị trí khi khớp làm việc.','ABC','AB BC'),
 S('Then hoa bù thay đổi chiều dài','Hai phần thân trục liên kết then hoa để đáp ứng chuyển động tương đối.','CD','CD')],nodes='Nạng thứ nhất|Trục chữ thập|Nạng thứ hai|Khớp then hoa',links='AB BC CD',title='Truyền mô men và bù chiều dài')
L('6.3.1','crossdouble',[
 S('Trục chủ động đưa mô men vào','Khớp chữ thập thứ nhất nhận tác động từ đầu vào.','AB','AB'),
 S('Khớp thứ nhất truyền tới giá chạc kép','Giá chạc kép liên kết hai trục chữ thập liền kề.','ABC','AB BC'),
 S('Khớp thứ hai nhận tác động','Hai khớp phối hợp theo bố trí để bù sự khác tốc.','ABCD','AB BC CD'),
 S('Trục bị động nhận mô men','Đoạn giữa được thu ngắn, vừa đủ nối hai trục chữ thập theo kết cấu bài học.','ABCDE','AB BC CD DE')],nodes='Trục chủ động|Khớp chữ thập thứ nhất|Giá chạc kép|Khớp chữ thập thứ hai|Trục bị động',links='AB BC CD DE')
L('6.3.2','cam',[
 S('Nạng chủ động tác động cam','Cam nửa hình trụ nằm trong phần lõm của nạng.','AB','AB'),
 S('Cam thứ nhất truyền qua đĩa','Đĩa nằm trong rãnh của cả hai cam.','ABC','AB BC'),
 S('Cam thứ hai tiếp nhận tác động','Liên kết cam–đĩa phối hợp khi góc giữa các trục thay đổi.','ABCD','AB BC CD'),
 S('Nạng bị động đưa mô men ra','Khớp làm việc tương tự khớp kép theo mô tả trong bài.','ABCDE','AB BC CD DE')],nodes='Nạng chủ động|Cam thứ nhất|Đĩa|Cam thứ hai|Nạng bị động',links='AB BC CD DE')
C('ballplane','6.3.3','Điều kiện đồng tốc của khớp bi',[
 ('Trục chủ động','Đường tâm phía đầu vào','Truyền mô men tới các điểm tiếp xúc bi.'),
 ('Trục bị động','Đường tâm phía đầu ra','Nhận mô men qua các điểm truyền lực.'),
 ('Mặt phẳng phân giác','Chia đôi góc giữa hai đường tâm','Các điểm truyền lực phải được giữ trên mặt phẳng này để bảo đảm đồng tốc.'),
 ('Vòng định vị','Giữ vị trí các viên bi','Một phương pháp giữ các viên bi đúng vị trí theo sơ đồ nguyên lý.')])
L('6.3.3','ballplane',[
 S('Xác định góc giữa hai đường tâm','Góc truyền mô men được tạo bởi trục chủ động và trục bị động.','AB'),
 S('Xác định mặt phẳng phân giác','Mặt phẳng này chia đôi góc tạo bởi hai đường tâm.','C'),
 S('Định vị các viên bi trên phân giác','Rãnh hoặc vòng định vị giữ điểm truyền lực đúng vị trí.','CD'),
 S('Truyền mô men với điều kiện đồng tốc','Giữ các điều kiện hình học trong phạm vi làm việc của khớp.','ABCD')],kind='concept',title='Trình tự giải thích điều kiện đồng tốc',quiz=Q('Điều kiện quan trọng để khớp bi đồng tốc là các điểm truyền lực nằm ở đâu?','Trên mặt phẳng phân giác của góc hai trục','Bất kỳ mặt phẳng nào đi qua trục vào','Chỉ trên mặt phẳng vuông góc với trục ra','Mặt phẳng phân giác giữ quan hệ động học đồng tốc giữa hai trục.'))
L('6.3.4','veise',[
 S('Nạng chủ động nhận mô men','Rãnh cong của nạng tạo vị trí cho các bi truyền lực.','A'),
 S('Bốn bi ngoài truyền mô men','Các bi ngoài làm việc trong rãnh của hai nạng.','AB','AB'),
 S('Bi giữa giữ định tâm','Viên bi thứ năm ở tâm khớp có nhiệm vụ định tâm, không thay nhiệm vụ bốn bi ngoài.','C'),
 S('Nạng bị động nhận mô men','Rãnh ôm hai mặt phối hợp các bi khi góc giữa hai trục thay đổi.','ABD','AB BD')],nodes='Nạng chủ động|Bốn bi truyền lực|Bi giữa định tâm|Nạng bị động',links='AB BD',title='Phân biệt bi truyền lực và bi định tâm')
L('6.3.5','rzeppa',[
 S('Phần chủ động đưa mô men tới rãnh','Các rãnh trên phần chủ động nhận các viên bi.','A'),
 S('Bi truyền mô men giữa hai phần','Sáu viên bi nằm trong các rãnh đối ứng của khớp.','AB','AB'),
 S('Vòng định vị giữ mặt phẳng phân giác','Vòng định vị giữ các bi theo điều kiện đồng tốc.','BD'),
 S('Phần bị động nhận mô men','Bôi trơn bằng mỡ và vỏ cao su dạng xếp bảo vệ khớp theo tài liệu.','ABC','AB BC')],nodes='Phần chủ động|Bi truyền lực|Phần bị động|Vòng định vị',links='AB BC',title='Truyền mô men qua khớp Rzeppa')
L('6.3.6','tripod',[
 S('Trục đầu vào truyền tới phần khớp','Hai phần khớp liên kết với các trục bằng then hoa theo kết cấu.','AB','AB'),
 S('Rãnh thân bao tác động con lăn','Ba con lăn làm việc trong ba rãnh dọc của thân bao.','ABC','AB BC'),
 S('Con lăn truyền lực qua chạc ba','Chạc ba mang các con lăn; rãnh dọc cho phép bù dịch chuyển dọc trục.','BCD','BC CD'),
 S('Mô men được đưa tới trục đầu ra','Khớp phối hợp góc truyền và bù chiều dài trong phạm vi làm việc.','ABCDE','AB BC CD DE')],nodes='Trục đầu vào|Thân bao hình trụ|Con lăn|Chạc ba|Trục đầu ra',links='AB BC CD DE')

# Chapter 7 — driving axles
L('7.1.1','diff',[
 S('Truyền lực chính nhận mô men','Mô men từ hộp số được tăng thêm, tốc độ quay giảm.','A'),
 S('Vỏ vi sai được dẫn động','Bánh răng bị động truyền lực chính gắn với vỏ vi sai.','AB','AB'),
 S('Vi sai phân phối tới các bán trục','Cho phép tốc độ hai bánh khác nhau khi quay vòng.','ABCD','AB BC BD'),
 S('Bánh xe chủ động nhận mô men','Bán trục đưa mô men từ vi sai ra bánh xe chủ động.','ABCDE','AB BC BD CE DE')],nodes='Truyền lực chính|Bộ vi sai|Bán trục trái|Bán trục phải|Bánh xe chủ động',links='AB BC BD CE DE')
C('axleclasses','7.1.2','Phân loại cầu chủ động',[
 ('Truyền lực chính đơn','Một cặp bánh răng','Phân loại theo số cặp bánh răng truyền lực chính.'),
 ('Truyền lực chính kép','Hai cặp bánh răng','Hai cặp truyền giảm tốc, có thể bố trí tập trung hoặc phân tán.'),
 ('Vi sai giữa các bánh xe','Phân phối trên một cầu','Phân loại vi sai theo công dụng, khác vi sai giữa các cầu.'),
 ('Bán trục giảm tải hoàn toàn','Chủ yếu truyền mô men xoắn','Phân loại bán trục theo mức chịu tải nhờ bố trí ổ đỡ.')])
L('7.1.2','axleclasses',[
 S('Đếm cặp bánh răng truyền lực chính','Một cặp là đơn, hai cặp là kép.','AB'),
 S('Xét công dụng bộ vi sai','Phân biệt giữa bánh xe, giữa cầu xe và giữa truyền lực cạnh.','C'),
 S('Xét mức chịu tải của bán trục','Đối chiếu bố trí ổ đỡ phía ngoài và tải trọng uốn của bán trục.','D'),
 S('Xét kết cấu dầm cầu','Cầu liền hay cầu cắt là tiêu chí kết cấu riêng.','ABCD')],kind='concept',title='Trình tự phân loại các phần tử cầu chủ động')
L('7.2.1','finaldrive',[
 S('Bánh răng chủ động nhận mô men','Đường truyền vào tác động bánh răng côn chủ động.','A'),
 S('Cặp bánh răng côn ăn khớp','Mô men truyền sang bánh răng côn bị động.','AB','AB'),
 S('Đổi hướng và giảm tốc','Trong sơ đồ trục giao nhau, đường truyền được đổi hướng và tốc độ giảm theo tỷ số răng.','AB','AB'),
 S('Vỏ vi sai được dẫn động','Bánh răng bị động gắn với vỏ vi sai để truyền tiếp tới các bán trục.','ABC','AB BC')],nodes='Bánh răng côn chủ động|Bánh răng côn bị động|Vỏ vi sai',links='AB BC',title='Đường truyền qua truyền lực chính')
L('7.2.2','diff',[
 S('Đi thẳng với lực cản hai bên bằng nhau','Bánh răng vi sai quay theo vỏ, không tự quay tương đối quanh trục của nó.','ABCDE','AB BC BD CE DE'),
 S('Hai bánh có quãng đường khác khi quay vòng','Bánh ngoài cần tốc độ lớn hơn bánh trong.','CD'),
 S('Bánh răng vi sai tự quay','Chuyển động tự quay tạo tốc độ khác nhau giữa hai bánh răng bán trục.','BCD','BC BD'),
 S('Hai bán trục truyền mô men ở tốc độ khác nhau','Vi sai cho phép chênh lệch tốc độ; khóa vi sai là một trạng thái khác.','ABCDE','AB BC BD CE DE')],nodes='Vỏ vi sai|Bánh răng vi sai|Bánh răng bán trục trái|Bánh răng bán trục phải|Bánh xe chủ động',links='AB BC BD CE DE',title='Đi thẳng và quay vòng với vi sai đối xứng',quiz=Q('Khi xe quay vòng, bánh răng vi sai có thêm chuyển động nào?','Tự quay quanh trục của nó','Dừng quay theo vỏ vi sai','Khóa cứng hai bánh răng bán trục','Tự quay của bánh răng vi sai tạo chênh lệch tốc độ giữa hai đầu ra.'))
C('halfshafts','7.2.3','Bán trục và vỏ cầu',[
 ('Bán trục giảm tải một nửa','Truyền xoắn và tham gia chịu uốn','Ổ đỡ phía ngoài lắp trực tiếp trên bán trục theo sơ đồ.'),
 ('Bán trục giảm tải hoàn toàn','Chủ yếu truyền xoắn','Moay ơ được đỡ trên vỏ bán trục nên giảm tải uốn cho bán trục.'),
 ('Vỏ cầu','Giá đỡ và bao che cụm cầu','Đỡ và bảo vệ các phần tử truyền lực, liên kết với hệ thống treo.'),
 ('Khớp các đăng đồng tốc','Truyền khi góc bán trục đổi','Đáp ứng truyền động ở cầu với hệ thống treo độc lập.')])
L('7.2.3','halfshafts',[
 S('Bánh răng bán trục nhận mô men','Bộ vi sai đưa mô men tới bán trục.','AB','AB'),
 S('Bán trục truyền tới moay ơ','Mô men truyền ra bánh xe chủ động.','ABC','AB BC'),
 S('Ổ đỡ tiếp nhận tải bánh xe','Mức tải uốn trên bán trục phụ thuộc cách bố trí ổ đỡ phía ngoài.','CD','CD'),
 S('Vỏ cầu truyền tải về hệ thống treo','Vỏ cầu làm giá đỡ và bao che; phân biệt đường truyền tải và mô men.','DE','DE')],nodes='Bánh răng bán trục|Bán trục|Moay ơ bánh xe|Ổ đỡ|Vỏ cầu',kind='force',links='AB:torque BC:torque CD:force DE:force',title='Phân biệt đường mô men và đường chịu tải')

# Chapter 8 — wheels and tyres
L('8.1.1','tire',[
 S('Tải trọng xe tác dụng lên lốp','Lốp được bơm khí có áp và đỡ tải trọng xe.','A'),
 S('Kết cấu lốp truyền tới vết tiếp xúc','Lớp bố và các lớp lốp phối hợp chịu tải.','AB','AB'),
 S('Hoa lốp tiếp xúc mặt đường','Lực dẫn động và lực phanh được truyền giữa xe và đường tại vùng tiếp xúc.','ABC','AB BC'),
 S('Lốp biến dạng qua mấp mô','Biến dạng lốp góp phần giảm chấn động; áp suất không phù hợp gây mòn bất thường.','ABCD','AB BC CD')],nodes='Tải trọng xe|Kết cấu lốp|Hoa lốp|Mặt đường',kind='force',links='AB BC CD',title='Quan hệ chịu tải và tiếp xúc mặt đường')
C('tread','8.1.2','Các kiểu hoa lốp',[
 ('Kiểu sọc','Rãnh chạy theo chu vi','Thường dùng trên đường lát phẳng và xe cao tốc theo bài.'),
 ('Kiểu vấu','Rãnh, vấu tăng tác động kéo','Ưu tiên lực kéo trên đường không lát.'),
 ('Sọc kết hợp vấu','Kết hợp rãnh chu vi và vấu','Kết hợp đặc điểm của hai dạng hoa lốp.'),
 ('Kiểu định hướng','Có chiều quay quy định','Cần được lắp đúng chiều quay của lốp.')])
L('8.1.2','tread',[
 S('Quan sát hướng rãnh chính','Rãnh theo chu vi gợi ý kiểu sọc.','A'),
 S('Quan sát vấu và rãnh ngang','Đối chiếu kiểu vấu và đặc điểm dùng trên đường không lát.','B'),
 S('Kiểm tra dạng kết hợp','Xác định sọc kết hợp vấu nếu có hai dạng đặc trưng.','C'),
 S('Kiểm tra chiều quay quy định','Hoa lốp định hướng phải được lắp theo chiều quy định.','D')],kind='concept',title='Trình tự nhận diện hoa lốp')
C('rim','8.2.1','Thông số vành bánh xe',[
 ('Chiều rộng vành','Bề rộng theo ký hiệu vành','Một thông số kích thước lắp của vành trong hình ký hiệu.'),
 ('Dạng mép của vành','Biên dạng mép lắp lốp','Đặc trưng hình dạng mép cần phù hợp với lốp.'),
 ('Đường kính lắp với lốp','Kích thước đường kính lắp','Phải phù hợp với đường kính lắp của lốp.'),
 ('Kiểu vành đối xứng','Ký hiệu dạng bố trí vành','Được chỉ ra trong hình ký hiệu vành của bài.')])
L('8.2.1','rim',[
 S('Đọc chiều rộng vành','Đối chiếu ký hiệu kích thước vành.','A'),
 S('Đọc dạng mép của vành','Nhận diện dạng mép để ghép đúng loại lốp.','B'),
 S('Đọc đường kính lắp lốp','So sánh đường kính vành với kích thước lắp của lốp.','C'),
 S('Đối chiếu toàn bộ dạng vành','Vành cần cứng vững, phù hợp lốp và có tính cân bằng động tốt.','D')],kind='concept',title='Trình tự đọc thông số vành')
C('wheeljoint','8.2.2','Liên kết vành – moay ơ – lốp',[
 ('Bu lông','Chi tiết mối ghép ren','Cùng ê cu tạo lực kẹp giữ bánh xe trên moay ơ.'),
 ('Ê cu định tâm','Giữ chặt và định tâm','Mối ghép phải được siết đúng mô men quy định.'),
 ('Moay ơ','Vị trí lắp cụm bánh','Tiếp nhận và định tâm mâm vành bánh xe.'),
 ('Vành bánh xe','Giữ biên dạng và mép lốp','Liên kết với moay ơ và lắp lốp tạo cụm bánh xe.')])
L('8.2.2','wheeljoint',[
 S('Định tâm mâm vành trên moay ơ','Mối ghép phải giữ đúng tâm cụm bánh.','CD'),
 S('Bu lông và ê cu tạo lực kẹp','Các bề mặt lắp được ép chặt nhờ mối ghép ren.','AB'),
 S('Mối ghép giữ chắc bằng ma sát','Mô men siết đúng quy định tạo lực kẹp phù hợp.','ABCD'),
 S('Vành giữ lốp khi cụm bánh làm việc','Liên kết phải chịu các tải tác dụng trong quá trình bánh xe làm việc.','D')],kind='concept',title='Quan hệ định tâm và giữ chặt mối ghép',order_prompt='Sắp xếp trình tự giải thích mối ghép: định tâm → tạo lực kẹp → giữ bằng ma sát → làm việc với lốp.')
L('8.2.3','balance',[
 S('Cụm vành lắp lốp có điểm nặng','Khối lượng không đồng đều tạo mất cân bằng.','A'),
 S('Bánh quay sinh tác động ly tâm','Điểm nặng gây rung khi cụm bánh quay.','AB','AB'),
 S('Xác định cân bằng tĩnh và động','Cân bằng tĩnh xét đứng yên; cân bằng động xét khi quay.','BC'),
 S('Hiệu chỉnh phân bố khối lượng','Cân bằng cả cụm vành đã lắp lốp, không nhầm với hiệu chỉnh độ đảo hình học.','CD','CD')],nodes='Điểm nặng|Lực ly tâm|Cân bằng tĩnh và động|Hiệu chỉnh khối lượng',kind='force',links='AB CD',title='Tác động của mất cân bằng bánh xe',quiz=Q('Nếu bánh rung do khối lượng phân bố không đều, thao tác phù hợp là gì?','Cân bằng cụm vành đã lắp lốp','Chỉ đổi góc camber','Chỉ sửa sai khác kích thước gọi là độ đảo','Cân bằng xử lý phân bố khối lượng; độ đảo là vấn đề hình học khác.'))
C('rotation','8.2.4','Điều kiện luân chuyển lốp',[
 ('Tải trọng đặt lên lốp','Trước và sau không giống nhau','Tải trọng khác nhau làm mức mòn lốp khác nhau.'),
 ('Lốp có chiều quay xác định','Giữ đúng hướng quay','Không đổi giữa bên phải và bên trái theo lưu ý trong tài liệu.'),
 ('Lốp trước và sau khác cỡ','Giữ vị trí theo kích thước','Không đổi trước–sau nếu cỡ lốp không phù hợp.'),
 ('Sơ đồ đảo lốp','Phụ thuộc kiểu xe','Chọn sơ đồ trong bài phù hợp dạng dẫn động và loại lốp.')])
L('8.2.4','rotation',[
 S('Kiểm tra kích thước lốp trước và sau','Nếu khác cỡ, không tự ý thay giữa trước và sau.','C'),
 S('Kiểm tra chiều quay của lốp','Lốp có chiều quay xác định không đổi phải–trái theo tài liệu.','B'),
 S('Chọn sơ đồ phù hợp kiểu xe','Đối chiếu sơ đồ đảo lốp và dạng dẫn động trong hình 8.14.','D'),
 S('Luân chuyển theo sơ đồ đã chọn','Mục đích là giúp mức mòn lốp đồng đều hơn.','A')],kind='concept',title='Trình tự lựa chọn sơ đồ đảo lốp',quiz=Q('Lốp có chiều quay xác định có được đảo bên phải sang bên trái theo lưu ý của tài liệu không?','Không','Có, trong mọi trường hợp','Chỉ cần bỏ qua ký hiệu chiều quay','Cần giữ đúng chiều quay; tài liệu nêu không thay giữa phải và trái với loại lốp này.'))

# Chapter 9 — steering
L('9.1.1','steer',[
 S('Người lái tạo yêu cầu đổi hướng','Vành tay lái nhận thao tác trực tiếp.','A'),
 S('Truyền tới cơ cấu lái','Trục lái đưa chuyển động vào cơ cấu lái.','AB','AB'),
 S('Dẫn động đổi góc bánh dẫn hướng','Các đòn dẫn động truyền tác động tới bánh.','ABCD','AB BC CD'),
 S('Xe đi theo hướng được điều khiển','Hệ thống cần duy trì hướng ổn định và phản hồi phù hợp.','D')],nodes='Vành tay lái|Cơ cấu lái|Dẫn động lái|Bánh xe dẫn hướng',kind='control',links='AB BC CD')
C('steerclasses','9.1.2','Phân loại hệ thống lái',[
 ('Bố trí vành tay lái','Bên trái hoặc bên phải','Tiêu chí vị trí người điều khiển và vành tay lái.'),
 ('Kết cấu cơ cấu lái','Trục vít hoặc bánh răng–thanh răng','Tiêu chí kiểu bộ truyền của cơ cấu lái.'),
 ('Trợ lực thủy lực','Dầu có áp tạo lực hỗ trợ','Tiêu chí nguồn tạo lực trợ lái.'),
 ('Trợ lực điện','Mô-tơ tạo mô men hỗ trợ','EPS sử dụng động cơ điện theo bài học.')])
L('9.1.2','steerclasses',[
 S('Xét vị trí vành tay lái','Phân biệt bố trí bên trái và bên phải.','A'),
 S('Xét bộ truyền của cơ cấu lái','Xác định trục vít, con lăn, thanh răng hoặc dạng kết hợp.','B'),
 S('Xét nguồn tạo trợ lực','Phân biệt dầu có áp với mô-tơ điện.','CD'),
 S('Kết luận theo từng tiêu chí','Không dùng tên loại trợ lực thay tên cơ cấu truyền.','ABCD')],kind='concept',title='Trình tự phân loại hệ thống lái')
L('9.2.1','worm',[
 S('Vành tay lái làm trục vít quay','Trục vít nhận chuyển động từ trục tay lái.','A'),
 S('Trục vít ăn khớp bánh vít','Bộ truyền đổi tác động quay với tỷ số truyền của cơ cấu.','AB','AB'),
 S('Trục đòn quay đứng chuyển động','Trục ra đưa tác động từ bánh vít tới đòn quay đứng.','ABC','AB BC'),
 S('Dẫn động tác động bánh dẫn hướng','Ma sát trượt lớn là nhược điểm của kiểu truyền được trình bày.','ABCD','AB BC CD')],nodes='Trục vít|Bánh vít|Trục đòn quay đứng|Dẫn động lái',kind='control',links='AB BC CD')
L('9.2.2','roller',[
 S('Trục vít lõm quay','Trục vít dạng glô-bô-it nhận tác động từ người lái.','A'),
 S('Con lăn ăn khớp và lăn theo ren','Tiếp xúc lăn giảm ma sát so với kiểu trục vít–bánh vít.','AB','AB'),
 S('Giá con lăn tác động trục ra','Con lăn phối hợp với giá gắn trên trục đòn quay đứng.','ABC','AB BC'),
 S('Trục đòn quay đứng truyền ra dẫn động','Dẫn động tiếp nhận tác động để đổi góc bánh dẫn hướng.','ABCD','AB BC CD')],nodes='Trục vít lõm|Con lăn|Trục đòn quay đứng|Dẫn động lái',kind='control',links='AB BC CD')
L('9.2.3','rack',[
 S('Bánh răng nhận chuyển động quay','Trục lái đưa chuyển động quay vào bánh răng.','A'),
 S('Thanh răng dịch chuyển tịnh tiến','Ăn khớp biến chuyển động quay thành chuyển động tịnh tiến.','AB','AB'),
 S('Đòn kéo truyền tác động','Đòn kéo và khớp nối đưa lực tới cam quay.','ABC','AB BC'),
 S('Bánh dẫn hướng đổi góc','Quan hệ hình học dẫn động cho phép bánh xe quay theo tác động lái.','ABCD','AB BC CD')],nodes='Bánh răng|Thanh răng|Đòn kéo|Bánh xe dẫn hướng',kind='control',links='AB BC CD',quiz=Q('Khi bánh răng của cơ cấu lái quay, thanh răng chuyển động thế nào?','Tịnh tiến','Chỉ quay cùng bánh răng','Đứng yên ở mọi trạng thái','Ăn khớp bánh răng–thanh răng biến chuyển động quay thành tịnh tiến.'))
L('9.2.4','recirculating',[
 S('Trục vít quay','Chuyển động vào tác động hệ rãnh xoắn và các viên bi.','A'),
 S('Bi lăn trong rãnh','Bi tuần hoàn thay ma sát trượt bằng ma sát lăn.','AB','AB'),
 S('Đai ốc bi dịch chuyển','Đai ốc thực hiện chuyển động tịnh tiến theo trục vít.','ABC','AB BC'),
 S('Cung răng quay trục đòn quay đứng','Tác động từ đai ốc truyền tới cung răng và đầu ra.','ABCD','AB BC CD')],nodes='Trục vít|Bi tuần hoàn|Đai ốc bi|Cung răng',kind='control',links='AB BC CD')
L('9.3.1','steer',[
 S('Vành tay lái nhận thao tác','Người lái tạo lực và chuyển động điều khiển.','A'),
 S('Trục lái nối đến cơ cấu lái','Trục có thể liền hoặc gồm nhiều đoạn ghép nối.','AB','AB'),
 S('Cơ cấu lái biến đổi tác động','Hộp giảm tốc làm việc theo tỷ số truyền thiết kế.','ABC','AB BC'),
 S('Dẫn động tới bánh xe dẫn hướng','Các đòn và khớp truyền tác động ra bánh.','ABCDE','AB BC CD DE')],nodes='Vành tay lái|Trục lái|Cơ cấu lái|Dẫn động lái|Bánh xe dẫn hướng',kind='control',links='AB BC CD DE')
C('steerparts','9.3.2','Các chi tiết dẫn động lái',[
 ('Vành tay lái','Điều khiển trong khoang lái','Nhận lực điều khiển trực tiếp từ người lái.'),
 ('Trục lái','Nối vành lái tới hộp lái','Truyền mô men và có thể có nhiều đoạn nối khớp.'),
 ('Khớp chữ thập','Liên kết các đoạn lệch góc','Cho phép truyền mô men khi các đoạn trục không thẳng hàng.'),
 ('Rô-tuyn','Khớp cầu trên thanh kéo','Truyền lực trong khi góc giữa đòn và thanh kéo thay đổi.')])
L('9.3.2','steerparts',[
 S('Vành tay lái đưa mô men vào trục','Liên kết vành tay lái và trục lái bằng then hoa hoặc bu lông theo bài.','AB','AB'),
 S('Khớp chữ thập truyền giữa các đoạn','Các đoạn trục có thể lệch góc mà vẫn truyền được mô men.','BC','BC'),
 S('Cơ cấu lái đưa tác động ra thanh kéo','Đầu ra của hộp lái liên kết với dẫn động.','CD','CD'),
 S('Rô-tuyn thích ứng góc liên kết','Khớp cầu cho phép các đòn quay ở những mặt phẳng khác nhau.','DE','DE')],nodes='Vành tay lái|Trục lái|Khớp chữ thập|Cơ cấu lái|Rô-tuyn thanh kéo',kind='control',links='AB BC CD DE')
L('9.3.3','angles',[
 S('Nhìn từ trước để xét camber','Góc nghiêng ngang bánh xe là góc của mặt phẳng bánh với phương thẳng đứng.','A'),
 S('Vẫn nhìn từ trước để xét trục đứng','Xét góc nghiêng ngang trục quay lái, khác với mặt phẳng bánh.','B'),
 S('Nhìn từ bên để xét caster','Góc nghiêng dọc trục quay lái có vai trò ổn định hướng và hồi vị theo bài.','C'),
 S('Nhìn từ trên để xét độ chụm','So sánh khoảng cách trước và sau của hai bánh dẫn hướng.','D')],kind='concept',title='Các hướng quan sát góc đặt bánh xe',order_prompt='Sắp xếp các bước khảo sát theo hướng nhìn trong minh họa: trước (bánh xe) → trước (trục đứng) → bên → trên.')
L('9.4.1','assiststeer',[
 S('Bơm dầu cung cấp nguồn có áp','Nguồn dầu trợ lực được đưa tới van phân phối.','AB','AB'),
 S('Người lái tác động van phân phối','Van đổi đường dầu theo yêu cầu quay vòng.','BC','BC'),
 S('Dầu tác động xi-lanh lực','Áp suất trên các khoang tạo lực hỗ trợ lái.','BCD','BC CD'),
 S('Lực trợ lực phối hợp dẫn động','Cơ cấu lái và xi-lanh lực phối hợp đưa tác động tới bánh xe.','BCDE','BC CD DE')],nodes='Bơm dầu|Van phân phối|Khoang xi-lanh lực|Pít-tông|Dẫn động lái',kind='fluid',links='AB BC CD:force DE:control',title='Dòng dầu và lực trợ lái')
L('9.4.2','eps',[
 S('Cảm biến nhận tác động người lái','Mô-men trên trục lái được nhận biết bởi cảm biến.','A'),
 S('ECU nhận thêm tốc độ xe','ECU tính mức trợ lực phù hợp mô-men và tốc độ.','ABC','AB CB'),
 S('ECU điều khiển mô-tơ điện','Dòng điện được điều khiển để tạo mô men hỗ trợ.','BD','BD'),
 S('Mô men trợ lực tác động cơ cấu lái','Khi chạy nhanh, mức hỗ trợ giảm theo nguyên lý trong bài.','DE','DE')],nodes='Cảm biến mô-men|ECU|Cảm biến tốc độ xe|Mô-tơ điện|Cơ cấu lái',kind='signal',links='AB CB BD DE:control',title='Thu nhận tín hiệu và tạo trợ lực EPS',quiz=Q('Theo nguyên lý EPS trong bài, khi tốc độ xe tăng cao, mức hỗ trợ thường thay đổi thế nào?','Giảm để giữ cảm giác lái và ổn định','Tăng tối đa ở mọi tình huống','Mất mọi liên kết cơ khí','ECU sử dụng tín hiệu tốc độ để giảm trợ lực khi chạy nhanh.'))
C('ehps','9.4.3','Trợ lực thủy lực điều khiển điện tử',[
 ('Bộ điều khiển điện tử trợ lực lái (ECU)','Xử lý trạng thái xe','Tính lệnh điều chỉnh trợ lực dựa vào tín hiệu đầu vào.'),
 ('Van điện từ','Điều tiết mạch dầu','Điều chỉnh mạch thủy lực theo lệnh điện tử.'),
 ('Bơm trợ lực','Cấp nguồn thủy lực','Có thể được điều khiển điện để thay đổi cấp nguồn theo kết cấu.'),
 ('Xi-lanh lực','Tạo lực từ áp suất dầu','Thủy lực vẫn tạo lực hỗ trợ tại cơ cấu chấp hành.')])
L('9.4.3','ehps',[
 S('Cảm biến cung cấp trạng thái xe','Tốc độ và tác động lái đưa thông tin tới điều khiển.','AB','AB'),
 S('ECU tính mức hỗ trợ','Yêu cầu trợ lực thay đổi theo điều kiện vận hành.','B'),
 S('Điều khiển van hoặc bơm','Tùy kết cấu, lệnh tác động van điện từ hoặc bơm trợ lực.','BC','BC'),
 S('Xi-lanh lực tạo trợ lái','Áp suất dầu tạo lực hỗ trợ, phân biệt với EPS tạo mô men bằng mô-tơ.','CD','CD')],nodes='Cảm biến|ECU|Van hoặc bơm trợ lực|Xi-lanh lực',kind='signal',links='AB BC CD:fluid',title='Điều khiển điện tử nguồn trợ lực thủy lực')

# Chapter 10 — braking
C('brakepurpose','10.1.1','Công dụng hệ thống phanh',[
 ('Phanh chính','Giảm tốc hoặc dừng khi vận hành','Đáp ứng yêu cầu điều khiển giảm tốc và dừng xe.'),
 ('Phanh đỗ','Giữ xe đứng yên','Giữ xe khi đỗ trên đường bằng hoặc trên dốc.'),
 ('Phanh chậm dần','Kiểm soát tốc độ xuống dốc','Phối hợp giảm tải cho cơ cấu phanh khi xuống dốc dài.'),
 ('ABS','Hạn chế bó cứng bánh xe','Hệ thống điều khiển hỗ trợ duy trì khả năng điều khiển khi phanh.')])
L('10.1.1','brakepurpose',[
 S('Người lái yêu cầu giảm tốc','Tác động phanh chính được đưa tới dẫn động.','A'),
 S('Cơ cấu phanh tạo mô men cản','Mô men phanh chống lại sự quay của bánh xe.','AB','AB'),
 S('Lốp truyền tác động với mặt đường','Tác động tại vết tiếp xúc làm xe giảm tốc.','ABC','AB BC'),
 S('Giữ xe khi đỗ bằng phanh đỗ','Chức năng giữ đứng yên khác với điều khiển giảm tốc khi đang chạy.','D')],nodes='Dẫn động phanh|Cơ cấu phanh|Lốp và mặt đường|Phanh đỗ',kind='force',links='AB BC',title='Giảm tốc và giữ xe khi đỗ')
C('brakeclasses','10.1.2','Phân loại hệ thống phanh',[
 ('Theo công dụng','Chính, đỗ, dự phòng','Tiêu chí nhiệm vụ làm việc của hệ thống phanh.'),
 ('Theo cơ cấu phanh','Tang trống hoặc đĩa','Tiêu chí kết cấu tạo mô men phanh.'),
 ('Theo dẫn động','Cơ khí, thủy lực, khí nén','Tiêu chí phương pháp truyền tác động điều khiển.'),
 ('Theo mức điều khiển','Có điều khiển điện tử','Tiêu chí sự tham gia của các hệ thống điều khiển.')])
L('10.1.2','brakeclasses',[
 S('Xét nhiệm vụ phanh','Phân biệt chính, đỗ và dự phòng.','A'),
 S('Xét bề mặt tạo ma sát','Phân biệt tang trống với đĩa.','B'),
 S('Xét phương pháp dẫn động','Nhận diện cơ khí, chất lỏng, khí nén hoặc liên hợp.','C'),
 S('Xét phần điều khiển điện tử','Xác định các chức năng hỗ trợ như ABS theo tài liệu.','D')],kind='concept',title='Trình tự phân loại hệ thống phanh')
L('10.2.1','drum',[
 S('Cam phanh nhận tác động','Trong hình 10.2, dẫn động làm cam phanh quay.','A'),
 S('Guốc phanh dịch ra ngoài','Cam đẩy guốc và má phanh về phía mặt trong trống.','AB','AB'),
 S('Ma sát tạo mô men phanh','Má phanh ép trống đang quay, chống lại chuyển động bánh xe.','ABC','AB BC'),
 S('Lò xo hồi vị kéo guốc về','Khi thôi phanh, lò xo kéo guốc về và khôi phục khe hở.','BD','DB')],nodes='Cam phanh|Guốc và má phanh|Trống phanh|Lò xo hồi vị',kind='force',links='AB BC DB',title='Phanh và nhả ở cơ cấu tang trống')
L('10.2.2','disc',[
 S('Dầu có áp tác động pít-tông','Pít-tông trong cụm xi-lanh tạo lực ép lên má phanh.','AB','AB'),
 S('Hai má ép hai mặt đĩa','Ở càng di động, phản lực làm càng trượt để ép má phía đối diện.','BC','BC'),
 S('Ma sát cản đĩa đang quay','Đĩa gắn với moay-ơ và quay cùng bánh xe.','BCD','BC CD'),
 S('Phớt đàn hồi góp phần hồi vị','Khi áp suất giảm, biến dạng đàn hồi giúp pít-tông hồi một phần để tạo khe hở.','B')],nodes='Dầu có áp|Pít-tông|Má phanh|Đĩa phanh',kind='fluid',links='AB BC:force CD:force',title='Tạo lực ép và hồi vị của phanh đĩa',quiz=Q('Ở càng phanh di động, vì sao má phía đối diện cũng ép vào đĩa?','Phản lực làm càng phanh trượt','Đĩa phanh tự dừng trước khi má tiếp xúc','Lò xo hồi vị đẩy má ra để phanh','Pít-tông ép một phía; phản lực làm càng di động trượt và ép má còn lại.'))
L('10.3.1','brakemechanical',[
 S('Người lái tác động bàn đạp','Bàn đạp làm quay trục và đòn quay.','A'),
 S('Đòn dẫn động truyền lực','Các đòn và thanh kéo đưa lực tới trục cam.','AB','AB'),
 S('Cam phanh quay và mở guốc','Cam biến tác động dẫn động thành dịch chuyển của guốc.','ABC','AB BC'),
 S('Guốc áp sát trống phanh','Ma sát tạo mô men phanh; phanh đỗ dùng cơ cấu giữ theo kết cấu.','ABCD','AB BC CD')],nodes='Bàn đạp phanh|Đòn dẫn động|Cam phanh|Guốc phanh',kind='control',links='AB BC CD')
L('10.3.2','brakehydraulic',[
 S('Bàn đạp tác động xi-lanh chính','Lực người lái đẩy pít-tông trong xi-lanh chính.','AB','AB'),
 S('Áp suất truyền qua đường ống','Chất lỏng có áp truyền tác động tới các xi-lanh công tác.','BCD','BC CD'),
 S('Xi-lanh công tác tác động guốc','Áp suất biến thành lực ép tại cơ cấu phanh bánh xe.','DE','DE'),
 S('Nhả bàn đạp, hệ thống hồi vị','Áp suất giảm, cơ cấu phanh hồi về; khí lẫn trong đường dầu làm tăng tính nén.','ABE','AB')],nodes='Bàn đạp|Xi-lanh chính|Đường ống dẫn|Xi-lanh công tác|Guốc phanh',kind='fluid',links='AB:control BC CD DE:force',title='Truyền tác động bằng áp suất chất lỏng',quiz=Q('Nếu đường dầu lẫn không khí, hiệu quả truyền tác động thay đổi thế nào?','Giảm do mạch tăng tính nén','Tăng do không khí không chịu nén','Không ảnh hưởng hành trình bàn đạp','Không khí chịu nén làm tăng hành trình và giảm hiệu quả truyền tác động thủy lực.'))
L('10.3.3','brakeair',[
 S('Máy nén nạp các bình khí','Khí có áp được tích trữ để cung cấp năng lượng phanh.','AB','AB'),
 S('Bàn đạp điều khiển van phanh tổng','Van điều khiển lượng khí cấp tới bầu phanh.','BC','BC'),
 S('Bầu phanh tạo lực cơ khí','Màng hoặc pít-tông nhận áp suất khí để tác động cơ cấu phanh.','BCD','BC CD'),
 S('Thôi phanh, khí từ bầu được xả','Van mở đường xả, lò xo hồi vị đưa cơ cấu về.','DE','DE')],nodes='Máy nén khí|Bình khí|Van phanh tổng|Bầu phanh|Khí trời',kind='air',links='AB BC CD DE',title='Nạp khí, tác động phanh và xả khí')
L('10.3.4','brakecombined',[
 S('Van phân phối cấp khí','Khí từ bình được đưa tới phần xi-lanh khí nén.','AB','AB'),
 S('Pít-tông khí tạo lực đẩy','Pít-tông khí nén qua thanh đẩy tác động phần chất lỏng.','BC','BC'),
 S('Pít-tông chất lỏng tạo áp suất','Xi-lanh chất lỏng tạo áp suất đưa tới mạch phanh bánh xe.','CD','CD'),
 S('Chất lỏng tác động cơ cấu phanh','Dạng truyền cuối cùng tới cơ cấu phanh trong sơ đồ là thủy lực.','DE','DE')],nodes='Van phân phối|Xi-lanh khí nén|Thanh đẩy|Xi-lanh chất lỏng|Cơ cấu phanh',kind='air',links='AB BC:force CD:force DE:fluid',title='Chuyển tác động khí nén sang thủy lực')
L('10.3.5','abs',[
 S('Cảm biến cung cấp tốc độ bánh xe','ECU nhận trạng thái quay bánh để phát hiện xu hướng bó cứng.','AB','AB'),
 S('Giữ áp khi cần hạn chế tăng phanh','Bộ chấp hành đóng các đường cần thiết để giữ áp suất ở cơ cấu phanh.','BC','BC'),
 S('Giảm áp khi bánh có xu hướng bó cứng','Đường giảm áp được mở theo lệnh để bánh phục hồi tốc độ quay.','CD','CD'),
 S('Tăng áp trở lại khi điều kiện cho phép','Chu trình tăng, giữ, giảm được điều khiển lặp lại theo trạng thái bánh xe.','CE','CE')],nodes='Cảm biến tốc độ|ECU điều khiển|Bộ chấp hành thủy lực|Giảm áp suất|Tăng áp suất',kind='signal',links='AB BC CD:fluid CE:fluid',title='Phát hiện trạng thái và điều chỉnh ABS',order_prompt='Sắp xếp chu trình minh họa này: nhận tín hiệu → giữ áp → giảm áp → tăng áp trở lại. Đây là ví dụ theo một tình huống; ECU có thể đổi trực tiếp giữa các chế độ theo trạng thái bánh.',quiz=Q('Khi bánh xe có xu hướng bó cứng, ECU cần cho bộ chấp hành thực hiện gì?','Giảm áp suất phanh tại bánh được điều khiển','Tăng áp tối đa liên tục','Khóa cố định bánh xe','Giảm áp giúp bánh phục hồi tốc độ; ABS điều chỉnh lặp lại theo tín hiệu tốc độ bánh.'))

# Chapter 11 — suspension
L('11.1.1','coilspring',[
 S('Bánh xe gặp kích động mặt đường','Dao động bắt đầu ở phần bánh và cầu xe.','A'),
 S('Bộ phận đàn hồi biến dạng','Lò xo thu nhận năng lượng biến dạng và đỡ tải.','AB','AB'),
 S('Bộ phận dẫn hướng truyền lực','Dẫn hướng truyền lực dọc, ngang và mô men, xác định quỹ đạo bánh.','AC','AC'),
 S('Giảm chấn tiêu tán năng lượng','Giảm chấn biến năng lượng dao động thành nhiệt để dao động giảm nhanh.','AD','AD')],nodes='Bánh xe|Bộ phận đàn hồi|Bộ phận dẫn hướng|Bộ phận giảm chấn',kind='force',links='AB AC AD',title='Phối hợp đàn hồi, dẫn hướng và giảm chấn')
C('suspclasses','11.1.2','Phân loại hệ thống treo',[
 ('Hệ thống treo phụ thuộc','Hai bánh nối dầm cầu cứng','Dao động một bánh ảnh hưởng bánh kia do liên kết bằng dầm cầu.'),
 ('Hệ thống treo độc lập','Mỗi bánh có bộ phận treo riêng','Không có dầm cầu cứng nối hai bánh như dạng phụ thuộc.'),
 ('Hệ thống treo điều khiển điện tử','Đặc tính thay đổi theo lệnh','Điều khiển điện tử tham gia thay đổi đặc tính làm việc.'),
 ('MacPherson','Một dạng treo độc lập','Giảm chấn làm đòn đứng, phối hợp đòn dưới và lò xo.')])
L('11.1.2','suspclasses',[
 S('Quan sát liên kết hai bánh cùng cầu','Tìm dầm cầu cứng chung hoặc cơ cấu treo riêng.','AB'),
 S('Xét quan hệ dao động hai bánh','Liên kết bằng dầm cứng làm một bánh ảnh hưởng bánh kia.','A'),
 S('Xác định dạng dẫn hướng','Đối chiếu MacPherson và các dạng đòn độc lập trong tài liệu.','D'),
 S('Xét phần điều khiển đặc tính','Điều khiển điện tử là tiêu chí bổ sung về phương pháp làm việc.','C')],kind='concept',title='Trình tự phân biệt hệ thống treo')
L('11.2.1','leaf',[
 S('Cầu xe tiếp nhận tác động bánh xe','Dầm cầu cứng liên kết các bánh ở treo phụ thuộc.','A'),
 S('Quang nhíp truyền tới bó nhíp','Bu lông quang nhíp giữ chặt bó nhíp với cầu.','AB','AB'),
 S('Bó nhíp biến dạng và dẫn hướng','Trong kết cấu này nhíp vừa đàn hồi vừa truyền các lực và mô men.','ABC','AB BC'),
 S('Hai đầu nhíp truyền tới khung','Liên kết bản lề hoặc gối đỡ cho phép biến dạng phù hợp hành trình.','ABCD','AB BC CD')],nodes='Cầu xe|Bu lông quang nhíp|Bó nhíp|Khung xe',kind='force',links='AB BC CD',title='Dẫn hướng và đàn hồi bằng bó nhíp')
L('11.2.2','macpherson',[
 S('Bánh xe dịch chuyển theo mặt đường','Bánh và cam quay chuyển động theo cơ cấu dẫn hướng.','A'),
 S('Đòn dưới xác định quỹ đạo','Đòn dưới liên kết cam quay với khung qua khớp.','AB','AB'),
 S('Giảm chấn làm đòn đứng','Trong MacPherson, đầu dưới giảm chấn gắn với cam quay, đầu trên liên kết khung.','AC','AC'),
 S('Lò xo đỡ tải theo hành trình','Lò xo đảm nhận đàn hồi, phối hợp giảm chấn và dẫn hướng.','AD','AD')],nodes='Cam quay bánh xe|Đòn dưới|Giảm chấn|Lò xo',kind='force',links='AB AC AD',title='Quan hệ dẫn hướng của treo MacPherson')
L('11.3.1','coilspring',[
 S('Lò xo tiếp nhận tải thẳng đứng','Lò xo xoắn biến dạng để đỡ tải theo hành trình.','A'),
 S('Năng lượng tích trong biến dạng','Nhíp uốn, thanh xoắn chịu xoắn, lò xo xoắn nén hoặc giãn theo dạng phần tử.','AB','AB'),
 S('Phần tử phục hồi khi tải thay đổi','Năng lượng đàn hồi được giải phóng khi phần tử phục hồi.','BA','BA'),
 S('Giảm chấn phối hợp dập dao động','Phần tử đàn hồi không tự thay thế nhiệm vụ của giảm chấn và dẫn hướng.','C')],nodes='Tải trọng|Biến dạng đàn hồi|Giảm chấn',kind='force',links='AB BA',title='Thu nhận và giải phóng năng lượng đàn hồi')
L('11.3.2','airspring',[
 S('Tải làm buồng khí giảm thể tích','Bộ phận đàn hồi khí nén sử dụng khả năng nén của chất khí.','AB','AB'),
 S('Áp suất khí tăng','Khí bị nén tạo tác động đàn hồi chống lại biến dạng.','BC','BC'),
 S('Lực đàn hồi đỡ khung xe','Vỏ cao su hoặc màng biến dạng theo hành trình.','CD','CD'),
 S('Giảm tải, khí giãn và phục hồi','Đặc tính khí nén là phi tuyến theo tài liệu; cao su còn dùng hạn chế hành trình.','BCD')],nodes='Tải trọng|Thể tích khí|Áp suất khí|Khung xe',kind='air',links='AB:force BC CD:force',title='Đàn hồi nhờ nén và giãn khí')
L('11.4.1','monodamper',[
 S('Hành trình nén: pit tông đi xuống','Bánh xe tiến gần khung làm pit tông thủy lực dịch xuống.','A'),
 S('Dầu qua van nén từ II sang I','Chênh áp mở đường van nén; nén mạnh mở thêm các nắp van.','BC','BC'),
 S('Pit tông khí bù thể tích','Khoang III chứa khí; pit tông khí dịch chuyển để bù phần thể tích cần chiếm chỗ.','DE','DE'),
 S('Hành trình trả: dầu từ I sang II','Bánh xe rời xa khung, pit tông đi lên; dầu qua đường van trả.','BC','CB')],nodes='Pit tông thủy lực|Khoang II|Khoang I|Pit tông khí|Khoang III',kind='fluid',links='BC CB DE:air',title='Nén, bù thể tích và trả ở giảm chấn ống đơn',quiz=Q('Trong giảm chấn ống đơn, pit tông khí và khoang III giúp xử lý vấn đề gì?','Bù thể tích thay đổi do cần pit tông chiếm chỗ','Tạo đường truyền mô men tới bánh xe','Thay cơ cấu lái khi quay vòng','Chất khí có thể nén và pit tông khí dịch chuyển để thay đổi thể tích khoang dầu.'))
L('11.4.2','twindamper',[
 S('Pit tông dịch chuyển ở hành trình nén','Cần và pit tông làm thay đổi thể tích khoang I, II.','A'),
 S('Dầu trao đổi qua van nén','Dầu đi từ khoang II tới khoang I; phần chênh lệch thể tích trao đổi với khoang bù qua đế van.','BCD','BC BD'),
 S('Khoang bù tiếp nhận thể tích chênh lệch','Khoang III nằm giữa vỏ trong và ngoài bù phần thể tích do cần chiếm chỗ.','D'),
 S('Hành trình trả mở đường van trả','Dầu từ I sang II qua van trả, dầu bù được bổ sung theo hành trình.','BCD','CB DB')],nodes='Pit tông|Khoang II|Khoang I|Khoang III (khoang bù)',kind='fluid',links='BC BD CB DB',title='Trao đổi dầu và bù thể tích ở ống kép')
L('11.5.1','hydractive',[
 S('Chế độ êm dịu nối ba quả cầu','Có thêm đệm khí phụ của quả cầu ở giữa nên đàn hồi mềm hơn.','ABC','AB AC'),
 S('Điều khiển nhận trạng thái xe','Độ cao, góc lái và bàn đạp cung cấp thông tin để lựa chọn trạng thái.','DE','DE'),
 S('Van cắt liên kết quả cầu ở giữa','Lệnh điều khiển tác động bộ điều chỉnh độ cứng, cắt đường nối quả cầu trung tâm.','EF','EF'),
 S('Chế độ thể thao có độ cứng lớn hơn','Thể tích khí tham gia giảm; bộ đàn hồi cứng hơn, hạn chế nghiêng thân.','BC')],nodes='Quả cầu lò xo ở giữa|Lò xo phía trái|Lò xo phía phải|Cảm biến|Bộ điều khiển|Van điện từ',kind='fluid',links='AB AC DE:signal EF:signal',title='Chuyển đặc tính mềm và cứng của Hydractive',quiz=Q('Khi cắt liên kết với quả cầu lò xo ở giữa theo chế độ thể thao, đặc tính đàn hồi thế nào?','Cứng hơn','Mềm hơn do tăng đệm khí','Không thay đổi thể tích khí tham gia','Quả cầu trung tâm bị tách làm giảm thể tích khí tham gia, nên bộ đàn hồi cứng hơn.'))
L('11.5.2','cdc',[
 S('Cảm biến đo trạng thái dao động','Dữ liệu độ cao và chuyển động được đưa tới điều khiển.','AB','AB'),
 S('Bộ điều khiển chọn lực giảm chấn','Phối hợp trạng thái xe và lựa chọn êm dịu hoặc thể thao.','B'),
 S('Dòng điện điều khiển van tỷ lệ','Van làm thay đổi tiết diện lưu thông dầu theo yêu cầu.','BC','BC'),
 S('Lực cản giảm chấn thay đổi','Mức lực giảm chấn được điều chỉnh liên tục theo điều khiển.','CD','CD')],nodes='Cảm biến|Bộ điều khiển|Van tỷ lệ|Dòng dầu qua giảm chấn',kind='signal',links='AB BC CD:fluid',title='Điều chỉnh lực giảm chấn bằng van tỷ lệ',quiz=Q('CDC điều chỉnh chủ yếu đại lượng nào?','Lực giảm chấn','Số cấp số truyền hộp số','Chiều rộng cơ sở','Bộ điều chỉnh điện tử làm thay đổi đặc tính lực giảm chấn theo trạng thái xe.'))

# Chapter 12 — frame/body and auxiliary equipment
C('bodyclasses','12.1.1','Cơ chế chịu lực của khung – vỏ',[
 ('Khung dầm rời chịu lực toàn bộ','Khung nhận tải chính','Khung dầm đỡ các tổng thành, thân vỏ tạo không gian bao ngoài.'),
 ('Thân vỏ liền khối','Thân vỏ tham gia chịu lực','Kết cấu thân vỏ là bộ phận của hệ chịu lực.'),
 ('Khung liền vỏ','Khung và vỏ phối hợp','Kết cấu khung, vỏ liên kết theo dạng được trình bày trong tài liệu.'),
 ('Vỏ ô tô','Không gian và bảo vệ','Bao bên ngoài, tạo không gian chứa người, hàng hóa và bảo vệ trước môi trường.')])
L('12.1.1','bodyclasses',[
 S('Xác định các cụm tạo tải trọng','Động cơ, truyền lực, buồng lái và thùng xe đặt tải lên kết cấu.','A'),
 S('Xác định bộ phận chịu lực chính','Khung dầm hoặc thân vỏ chịu lực tiếp nhận tải theo kết cấu.','AB'),
 S('Theo dõi tải xuống hệ thống treo','Kết cấu chịu lực truyền tải qua các điểm liên kết hệ thống treo.','BC','BC'),
 S('Phân biệt chức năng bao che của vỏ','Vỏ còn tạo không gian và bảo vệ khỏi môi trường, khác chức năng chịu lực.','D')],nodes='Các cụm tổng thành|Khung hoặc thân chịu lực|Hệ thống treo|Vỏ bao ngoài',kind='force',links='AB BC',title='Chịu tải và bao che của khung – vỏ')
L('12.1.2','frame',[
 S('Giá đỡ tiếp nhận tải tổng thành','Các vị trí lắp định vị động cơ, buồng lái và các cụm.','A'),
 S('Dầm dọc chịu tải chính','Hai dầm dọc chạy theo chiều dài khung tải.','AB','AB'),
 S('Dầm ngang liên kết và gia cường','Dầm ngang nối hai dầm dọc, góp phần cứng vững kết cấu.','BC','BC'),
 S('Tải truyền qua hệ thống treo xuống cầu','Khung phải đủ bền, cứng và thuận tiện lắp các tổng thành.','BD','BD')],nodes='Giá đỡ tổng thành|Dầm dọc|Dầm ngang|Hệ thống treo',kind='force',links='AB BC BD',title='Đường chịu tải trên khung xe tải')
C('carbody','12.1.3','Các dạng khung và vỏ xe con',[
 ('Thân vỏ rời','Khung và thân chế tạo riêng','Thân lắp với khung dầm bằng mối ghép theo kết cấu.'),
 ('Thân vỏ chịu tải một phần','Phối hợp khung và vỏ','Cả khung và phần thân tham gia tiếp nhận tải theo dạng được mô tả.'),
 ('Thân vỏ chịu tải hoàn toàn','Kết cấu thân tiếp nhận tải','Hệ sàn và các phần thân tạo kết cấu chịu lực.'),
 ('Khung phụ','Đỡ cụm tại từng vùng','Dùng để lắp các tổng thành như động cơ, truyền lực hoặc treo theo bố trí.')])
L('12.1.3','carbody',[
 S('Xác định dạng liên kết thân và khung','Thân vỏ rời chế tạo tách biệt rồi lắp với khung.','A'),
 S('Đối chiếu mức tham gia chịu tải','Thân chịu tải một phần khác với chịu tải hoàn toàn.','BC'),
 S('Theo dõi các điểm lắp tổng thành','Khung phụ đỡ các cụm tại vùng bố trí.','D'),
 S('Kết luận cơ chế chịu lực','Dựa vào đường truyền tải thay vì chỉ hình dáng bao ngoài.','ABCD')],kind='concept',title='Trình tự nhận biết dạng khung – vỏ xe con')
C('tirepressure','12.2.1','Điều chỉnh áp suất hơi lốp',[
 ('Cụm cung cấp và điều hòa khí nén','Nguồn khí được điều chỉnh','Bao gồm máy nén, bình chứa và phần điều hòa nguồn khí.'),
 ('Van điều khiển','Chọn bơm, giữ hoặc xả','Đổi đường khí theo chế độ điều chỉnh áp suất lốp.'),
 ('Bộ phận dẫn khí nén vào bánh xe','Đưa khí tới phần quay','Truyền khí tới lốp và làm kín khi bánh xe quay.'),
 ('Van giữ hơi','Giữ khí trong lốp','Tham gia giữ kín khí của lốp theo kết cấu trong tài liệu.')])
L('12.2.1','tirepressure',[
 S('Nguồn khí được cấp và bảo vệ','Nguồn khí của phanh được ưu tiên khi áp suất thấp theo van hạn chế.','A'),
 S('Chế độ bơm: nối nguồn với lốp','Van điều khiển cho khí từ nguồn qua bộ phận dẫn tới lốp.','ABC','AB BC'),
 S('Chế độ giữ: đóng đường khí','Đường cấp và xả được đóng để giữ áp suất lốp.','C'),
 S('Chế độ xả: nối lốp với khí trời','Van điều khiển mở đường khí từ lốp ra ngoài.','CD','CD')],nodes='Nguồn khí nén|Van điều khiển|Lốp xe|Khí trời',kind='air',links='AB BC CD',title='Ba chế độ bơm, giữ và xả khí',order_prompt='Sắp xếp các chế độ theo thứ tự khảo sát trong minh họa: nguồn → bơm → giữ → xả. Các chế độ được người điều khiển lựa chọn theo yêu cầu, không phải chu trình bắt buộc.')
L('12.2.2','tipper',[
 S('Hộp trích công suất dẫn động bơm','Bơm hút dầu từ thùng và cấp nguồn áp suất cho mạch.','AB','AB'),
 S('Nâng: dầu tới xy lanh thủy lực','Van điều khiển đưa dầu có áp tới xy lanh để nâng thùng.','BCE','BC CE'),
 S('Giữ: khóa dầu trong xy lanh','Ở vị trí trung gian, dầu trong xy lanh được giữ; dầu từ bơm hồi về thùng.','BCDE','BC CD'),
 S('Hạ: mở đường dầu hồi về thùng','Van cho dầu từ xy lanh về thùng để thùng hạ theo chế độ điều khiển.','CDE','EC CD')],nodes='Hộp trích công suất|Bơm dầu|Van điều khiển|Thùng dầu|Xy lanh thủy lực',kind='fluid',links='AB:torque BC CD CE EC',title='Nâng, giữ và hạ thùng theo điều khiển',order_prompt='Sắp xếp các chế độ theo thứ tự khảo sát: dẫn động bơm → nâng → giữ → hạ. Đây là thứ tự xem minh họa, người lái chọn chế độ theo yêu cầu.',quiz=Q('Muốn giữ thùng ở vị trí trung gian, trạng thái đường dầu tới xy lanh cần thế nào?','Khóa dầu trong xy lanh','Mở liên tục dầu từ xy lanh về thùng','Ngắt mọi liên kết với khung xe','Van ở trung gian giữ dầu trong xy lanh; dầu bơm có đường hồi theo hệ thống được trình bày.'))

# Long lessons contain more than one mechanism; provide a second selectable model.
SPECS['12.2.2']['extra_figures']=['winch']
SPECS['12.2.2']['extra_models']=[dict(title='Đường truyền của tời cơ khí',kind='torque',
 nodes='Hộp trích công suất|Trục các đăng|Hộp giảm tốc|Trống tời|Dây cáp',links='AB BC CD DE:force',steps=[
 S('Hộp trích công suất nhận dẫn động','Công suất động cơ được lấy qua hộp số chính tới hộp trích công suất.','A'),
 S('Các đăng truyền tới hộp giảm tốc','Trục các đăng nối hộp trích công suất với hộp giảm tốc tời.','ABC','AB BC'),
 S('Hộp giảm tốc làm quay trống tời','Giảm tốc làm tăng mô men tại trống tời.','ABCD','AB BC CD'),
 S('Cáp tời truyền lực kéo','Trống quấn hoặc nhả cáp tạo tác động kéo theo chế độ điều khiển.','ABCDE','AB BC CD DE')])]
