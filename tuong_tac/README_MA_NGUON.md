# Biên soạn hoạt động tương tác

Tệp `lesson-data.js` cung cấp dữ liệu trực tiếp bằng script, để chạy khi mở bằng file://.
`lesson-data.json` là bản dữ liệu dễ đọc. `interactive.js` quản lý thao tác và phản hồi;
`simulation.js` hiển thị sơ đồ; `catalog.js` tổng hợp tiến độ và sao lưu.

Trong tools/:
- figures.py: tên gọi, công dụng, hình nguồn và tọa độ các điểm bấm.
- specs.py: dữ liệu các bước, đường tác động và bài tập cho 92 bài ngoài chương 2.
- wmf_formula.py: chuyển các bản ghi ký tự/công thức WMF thành SVG, giữ các vị trí GDI.
- source.json và source_pages/: bản nguồn dùng để đối chiếu và dựng lại.
- build_all.py: dựng dữ liệu, mục lục, thuật ngữ và các phần gắn trong bài.

Chương 2 dùng dữ liệu trong chuong2/lesson-data.json. Dữ liệu bài học và ngân hàng
411 câu trong on_tap/ có các mã bài ổn định; các trang lặp liên kết về cùng mã.

Dựng lại bằng Python 3, với lxml, Pillow, reportlab và fontTools. Inkscape được dùng khi
cần chuyển lại tài nguyên hình. Chạy: `python tuong_tac/tools/build_all.py` từ thư mục gói.
Sửa nội dung/tọa độ trong figures.py hoặc specs.py, dựng lại và kiểm tra trên trình duyệt.
Nếu thay đổi ý nghĩa đáp án của bản đã phát hành, cập nhật version và quy tắc chuyển tiến độ.

Dữ liệu lưu gồm đáp án, thứ tự, vị trí ghép, các điểm đã nhận diện và thời điểm cập nhật.
Không gửi kết quả ra mạng. Nhập sao lưu xác thực toàn bộ trước khi ghi, khôi phục dữ liệu
cũ nếu ghi bị lỗi giữa chừng. Chấm tên bỏ dấu và ký tự phân cách nhưng dùng danh sách tên
đã đối chiếu nguồn, không dùng các cách gọi thông tục.
