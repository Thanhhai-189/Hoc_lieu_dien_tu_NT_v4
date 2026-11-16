# Học liệu điện tử tương tác NT v4.3

- Trang chủ `index.html`, giao diện `nt/app.css`, điều hướng / tiến độ `nt/app.js`.
- Bài học HTML trong `html/`, dữ liệu trong `tuong_tac/lesson-data.json` và bản đóng gói JS tương ứng.
- `nt/reader-bridge.js` gửi dữ liệu giữa khung bài và trang chủ bằng postMessage, kiểm tra cửa sổ nguồn; tránh tách tiến độ theo từng tệp khi mở file://.
- Cơ chế chấm tương tác tại `tuong_tac/interactive.js`; chấm ôn tập tại `on_tap/review.js`. Hai bộ đều chờ bridge sẵn sàng trước khi đọc kết quả.
- `nt/engineering-sim.js` bổ sung sơ đồ ABS thủy lực / khí nén; các sơ đồ còn lại dùng trình hiển thị chung.
- `version` của dữ liệu giữ giá trị cũ để đọc sao lưu v3. `contentRevision` đánh dấu nội dung v4; `revisedExercises` chỉ định mục cần làm lại. Không xóa trường này khi sửa dữ liệu.
- Tệp `nt/doi-chieu-hinh.json` ghi số hình, trang PDF và đường ảnh bản 2026. Không đối chiếu ảnh khác phiên bản chỉ bằng số hình.
- `nt/tai-lieu-tap2-2026.pdf` giữ nguyên bytes tệp nguồn. Báo cáo phản biện có PDF và HTML tại thư mục nt.
- Công cụ và các trang nguồn trong tuong_tac/tools là phần kế thừa v3. Không chạy công cụ tái sinh cũ lên bản v4 vì có thể ghi đè bộ tích hợp mới.

- `nt/assistant/panel.js` quản lý khung chat. Trình duyệt tải chỉ mục khi mở trợ lý, tra cứu bằng `retrieval.js` và gợi ý từ `study.js`.
- `nt/assistant/study-glossary.js` chứa thẻ Việt–Anh từ gói đính kèm. Một số mục được hiệu chỉnh và gắn bài liên quan. Hình minh họa tra cứu nằm trong `nt/assistant/vocabulary/`.
- `nt/assistant/topics.json` chứa câu trả lời kỹ thuật ngắn có dẫn nguồn. Nếu sửa tệp này, chạy `python nt/assistant/build-corpus.py` với PyMuPDF và lxml để cập nhật chỉ mục.
- `BAT_DAU.html` mở học liệu trực tiếp. Python, PyMuPDF và lxml chỉ dùng khi người bảo trì tạo lại chỉ mục.
