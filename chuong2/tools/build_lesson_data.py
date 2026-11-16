from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "chuong2"
OUT.mkdir(exist_ok=True)

def part(letter, name, x, y, description, short, aliases=()):
    return dict(id=letter, name=name, x=x, y=y, description=description,
                short=short, aliases=[name, *aliases])

def figure(fid, image, caption, parts, source):
    return dict(id=fid, image="content/resources/" + image, caption=caption,
                parts=parts, source=source)

ONE = figure("one", "T1_image69.png", "Hình 2.1 — Ly hợp ma sát lò xo màng",
    [
        part("A", "Bánh đà", 26, 29, "Gắn với trục khuỷu; tạo một bề mặt ma sát và truyền mômen từ động cơ vào bộ ly hợp.", "Nhận mômen từ trục khuỷu và tạo mặt tựa ma sát."),
        part("B", "Đĩa ép", 43, 23, "Ép đĩa ma sát vào bánh đà khi ly hợp đóng; dịch ra để giải phóng lực ép khi ngắt.", "Ép đĩa ma sát vào bánh đà."),
        part("C", "Lò xo màng", 51, 35, "Tạo lực ép và làm việc như đòn bẩy khi ổ bi bạc mở tác động vào đầu trong.", "Tạo lực ép và làm đòn bẩy khi ngắt."),
        part("D", "Đĩa ma sát", 40, 66, "Nhận mômen qua các bề mặt ma sát rồi truyền tới moayơ và trục sơ cấp hộp số.", "Nhận mômen ma sát để truyền tới trục sơ cấp.", ("đĩa bị động", "đĩa ly hợp")),
        part("E", "Ổ bi bạc mở", 60, 49, "Tiếp nhận tác động của càng mở và truyền lực tới đầu trong lò xo màng.", "Truyền lực của càng mở tới lò xo màng.", ("bạc mở", "bi tê", "vòng bi bạc mở", "ổ bi mở")),
        part("F", "Đòn bẩy", 80, 69, "Truyền chuyển động của dẫn động điều khiển đến ổ bi bạc mở.", "Đưa chuyển động điều khiển tới ổ bi bạc mở.", ("càng mở", "càng ngắt", "càng mở ly hợp")),
    ], "2.2.1")

TWO = figure("two", "T1_image81.png", "Hình 2.13b — Ly hợp hai đĩa ma sát",
    [
        part("A", "Bánh đà", 15, 79, "Bộ phận chủ động gắn với trục khuỷu; tạo mặt ma sát phía trong.", "Tạo mặt ma sát phía động cơ."),
        part("B", "Đĩa ma sát phía trong", 29, 78, "Đĩa bị động phía bánh đà, cùng đĩa phía ngoài truyền mômen tới trục bị động.", "Đĩa bị động ở phía bánh đà.", ("đĩa ma sát trong",)),
        part("C", "Đĩa ép trung gian", 43, 78, "Nằm giữa hai đĩa ma sát và tạo thêm các bề mặt truyền mômen.", "Nằm giữa hai đĩa ma sát.", ("đĩa trung gian",)),
        part("D", "Đĩa ma sát phía ngoài", 55, 78, "Đĩa bị động thứ hai, ở phía cụm đĩa ép ngoài.", "Đĩa bị động ở phía cụm đĩa ép ngoài.", ("đĩa ma sát ngoài",)),
        part("E", "Lò xo màng", 76, 79, "Tạo lực ép cho cả cụm và đổi trạng thái khi cơ cấu mở tác động.", "Tạo lực ép cho cụm hai đĩa."),
    ], "2.2.2")

MULTI = figure("multi", "T1_image82.png", "Hình 2.14 — Ly hợp nhiều đĩa",
    [
        part("A", "Đĩa ma sát", 28, 51, "Các đĩa bị động ăn khớp với moayơ, xen kẽ với các đĩa chủ động.", "Các đĩa bị động ăn khớp với moayơ.", ("đĩa bị động",)),
        part("B", "Vỏ ly hợp", 50, 27, "Mang các rãnh liên kết với các đĩa chủ động.", "Mang các rãnh liên kết với các đĩa chủ động."),
        part("C", "Piston", 69, 49, "Dịch chuyển dưới áp suất dầu để ép chặt chồng đĩa.", "Biến áp suất dầu thành lực ép.", ("pít tông", "pittông")),
        part("D", "Đường dầu áp suất", 80, 74, "Dẫn dầu có áp vào buồng tác động lên piston.", "Đưa dầu có áp vào buồng tác động.", ("đường dầu", "đường cấp dầu", "áp suất dầu")),
        part("E", "Trục sơ cấp hộp số", 69, 78, "Nhận mômen từ cụm đĩa qua moayơ.", "Nhận mômen từ moayơ đĩa ma sát.", ("trục sơ cấp", "trục bị động")),
        part("F", "Đĩa ép", 25, 70, "Các đĩa chủ động xen kẽ với đĩa ma sát để tạo nhiều cặp tiếp xúc.", "Các đĩa chủ động xen kẽ đĩa ma sát."),
    ], "2.2.2")

MECHANICAL = figure("mechanical", "T1_image83.jpeg", "Hình 2.15 — Dẫn động điều khiển bằng cơ khí",
    [
        part("A", "Bàn đạp ly hợp", 81, 69, "Nhận lực chân người lái và làm quay đòn dẫn động.", "Nhận lực chân người lái.", ("bàn đạp",)),
        part("B", "Cáp kéo", 55, 62, "Truyền lực kéo từ bàn đạp tới đòn liên kết của cơ cấu mở.", "Truyền lực kéo từ bàn đạp.", ("cáp ly hợp", "dây cáp",)),
        part("C", "Đòn liên kết", 20, 27, "Truyền chuyển động tới cơ cấu mở và ổ bi bạc mở.", "Truyền chuyển động tới cơ cấu mở.", ("đòn bẩy", "càng mở")),
        part("D", "Ổ bi bạc mở", 28, 41, "Trượt trên bạc dẫn hướng và tác động vào cơ cấu tách.", "Tác động vào cơ cấu tách ly hợp.", ("bạc mở", "bi tê", "vòng bi bạc mở")),
        part("E", "Lò xo hồi vị bàn đạp", 76, 32, "Đưa bàn đạp trở về vị trí ban đầu khi người lái thôi tác động.", "Đưa bàn đạp về vị trí ban đầu.", ("lò xo hồi vị",)),
    ], "2.3.1")

HYDRAULIC = figure("hydraulic", "T1_image84.png", "Hình 2.16 — Dẫn động điều khiển bằng thủy lực",
    [
        part("A", "Bàn đạp ly hợp", 78, 38, "Truyền lực qua cần đẩy tới piston xi lanh chính.", "Truyền lực chân tới xi lanh chính.", ("bàn đạp",)),
        part("B", "Xi lanh chính", 56, 36, "Biến lực từ bàn đạp thành áp suất dầu điều khiển.", "Tạo áp suất dầu từ lực bàn đạp.", ("xilanh chính", "xi lanh tổng")),
        part("C", "Đường ống dẫn dầu", 48, 53, "Nối xi lanh chính với xi lanh công tác, truyền áp suất thủy lực.", "Truyền áp suất tới xi lanh công tác.", ("ống dẫn dầu", "đường dầu")),
        part("D", "Xi lanh công tác", 60, 63, "Biến áp suất dầu thành lực trên piston và chốt đẩy.", "Biến áp suất dầu thành lực trên chốt đẩy.", ("xi lanh con", "xilanh công tác", "xi lanh phụ")),
        part("E", "Chốt đẩy", 48, 64, "Truyền lực từ piston xi lanh công tác tới càng ngắt.", "Truyền lực piston tới càng ngắt.", ("cần đẩy",)),
        part("F", "Vít xả khí", 69, 60, "Dùng để xả không khí lẫn trong dẫn động thủy lực khi bảo dưỡng.", "Dùng để xả không khí lẫn trong dẫn động.", ("ốc xả khí",)),
    ], "2.3.2")

MASTER = figure("master", "T1_image85.png", "Hình 2.17 — Xi lanh chính",
    [
        part("A", "Piston", 53, 70, "Dịch chuyển theo cần đẩy và làm tăng áp suất trong buồng công tác.", "Dịch chuyển để tạo áp suất.", ("pít tông", "pittông")),
        part("B", "Cần đẩy piston", 90, 71, "Nhận tác động của bàn đạp để đẩy piston.", "Đưa lực bàn đạp tới piston.", ("cần đẩy",)),
        part("C", "Vòng làm kín sơ cấp", 66, 71, "Làm kín buồng tạo áp suất ở phía trước piston.", "Làm kín buồng tạo áp suất.", ("phớt sơ cấp",)),
        part("D", "Đầu nối với xi lanh công tác", 5, 66, "Nối đường dầu có áp tới xi lanh công tác.", "Nối đường dầu tới xi lanh công tác.", ("đầu nối dầu",)),
    ], "2.3.2")

SLAVE = figure("slave", "T1_image86.png", "Hình 2.18 — Xi lanh công tác",
    [
        part("A", "Chốt đẩy", 19, 58, "Đưa lực của piston tới đòn bẩy ly hợp.", "Đưa lực piston tới đòn bẩy.", ("cần đẩy",)),
        part("B", "Piston", 56, 59, "Nhận áp suất dầu để tạo chuyển động tịnh tiến.", "Nhận áp suất dầu để dịch chuyển.", ("pít tông", "pittông")),
        part("C", "Vít xả khí", 84, 29, "Mở đường thoát cho không khí khi xả khí hệ thống.", "Tạo đường xả không khí khi bảo dưỡng.", ("ốc xả khí",)),
        part("D", "Đầu nối ống dầu", 70, 30, "Nối xi lanh công tác với đường dầu từ xi lanh chính.", "Nhận dầu từ xi lanh chính.", ("đầu nối", "đầu nối ống dẫn")),
    ], "2.3.2")

ASSIST = figure("assist", "T1_image87.png", "Hình 2.19b — Dẫn động cơ khí có trợ lực khí nén",
    [
        part("A", "Bàn đạp ly hợp", 83, 83, "Điều khiển dẫn động cơ khí và van phân phối.", "Điều khiển dẫn động và van phân phối.", ("bàn đạp",)),
        part("B", "Van phân phối", 64, 69, "Đóng đường xả và mở đường cấp khí khi cần trợ lực; xả khí khi hồi vị.", "Điều khiển đường cấp và đường xả khí.", ("van điều khiển",)),
        part("C", "Ống dẫn khí nén", 53, 86, "Đưa khí nén từ nguồn tới cụm phân phối và bộ trợ lực.", "Đưa khí nén tới bộ trợ lực.", ("đường dẫn khí nén", "ống khí")),
        part("D", "Màng cao su piston", 60, 21, "Nhận áp suất khí nén để tạo lực phụ trợ.", "Nhận áp suất khí nén để tạo lực trợ giúp.", ("màng piston", "màng cao su")),
        part("E", "Cần đẩy piston", 74, 21, "Truyền lực phụ trợ tới cơ cấu mở ly hợp.", "Truyền lực phụ trợ tới cơ cấu mở.", ("cần đẩy",)),
        part("F", "Ổ bi bạc mở", 75, 40, "Truyền lực tới cơ cấu tách để ngắt ly hợp.", "Truyền lực tới cơ cấu tách.", ("bạc mở", "bi tê", "vòng bi bạc mở")),
    ], "2.3.3")

ACS = figure("acs", "T1_image91.png", "Hình 2.23 — Hệ thống ly hợp tự động ACS",
    [
        part("A", "Bộ điều khiển ly hợp", 52, 77, "Xử lý tín hiệu đầu vào để tính toán trạng thái và hành trình đóng/ngắt ly hợp.", "Xử lý tín hiệu và phát lệnh chấp hành.", ("bộ điều khiển", "ecu")),
        part("B", "Động cơ điện", 53, 58, "Nhận lệnh điều khiển và dẫn động bộ truyền trục vít – bánh vít.", "Dẫn động bộ truyền trục vít – bánh vít."),
        part("C", "Bộ truyền trục vít bánh vít", 53, 46, "Truyền chuyển động từ động cơ điện tới cơ cấu tạo áp suất.", "Truyền chuyển động tới cơ cấu tạo áp suất.", ("trục vít bánh vít",)),
        part("D", "Xi lanh chính", 53, 36, "Tạo áp suất thủy lực cho cơ cấu đóng/ngắt trung tâm.", "Tạo áp suất cho cơ cấu đóng/ngắt.", ("xilanh chính",)),
        part("E", "Xi lanh con", 49, 19, "Tác động trực tiếp lên cơ cấu đóng/ngắt ly hợp.", "Tác động lên cơ cấu đóng/ngắt trung tâm.", ("xi lanh công tác", "cơ cấu đóng ngắt trung tâm")),
        part("F", "Tín hiệu đầu vào", 79, 85, "Gồm tín hiệu sang số, tốc độ, vị trí ga và các thông tin CAN-bus theo sơ đồ.", "Cung cấp thông tin trạng thái cho bộ điều khiển.", ("tín hiệu cảm biến", "các tín hiệu đầu vào")),
    ], "2.4.1")

DUAL = figure("dual", "T1_image92.png", "Hình 2.24 — Ly hợp kép và hai trục sơ cấp",
    [
        part("A", "Ly hợp C1", 76, 16, "Nối mômen tới trục đặc IS1, phụ trách các cấp số lẻ trong sơ đồ bài học.", "Nối mômen tới trục đặc IS1.", ("c1",)),
        part("B", "Ly hợp C2", 76, 28, "Nối mômen tới trục rỗng IS2, phụ trách các cấp số chẵn và số lùi trong sơ đồ.", "Nối mômen tới trục rỗng IS2.", ("c2",)),
        part("C", "Trục đặc IS1", 13, 55, "Nhận mômen qua C1 và nối với nhóm số lẻ.", "Nhận mômen qua C1, nối nhóm số lẻ.", ("is1", "trục đặc", "trục sơ cấp is1")),
        part("D", "Trục rỗng IS2", 38, 54, "Nhận mômen qua C2 và nối với nhóm số chẵn.", "Nhận mômen qua C2, nối nhóm số chẵn.", ("is2", "trục rỗng", "trục sơ cấp is2")),
    ], "2.4.2")

WET = figure("wet", "T1_image94.png", "Hình 2.26 — Ly hợp kép ma sát ướt, nhánh C1",
    [
        part("A", "Đường cấp dầu áp suất", 17, 74, "Đưa dầu điều khiển tới buồng áp suất của ly hợp được chọn.", "Đưa dầu điều khiển tới buồng áp suất.", ("đường dầu", "đường cấp dầu", "áp suất dầu")),
        part("B", "Buồng áp suất", 39, 49, "Dầu có áp tác dụng lên piston để ép cụm đĩa.", "Tạo lực tác dụng lên piston."),
        part("C", "Buồng cân bằng dầu", 48, 43, "Bù tác động lực ly tâm của dầu, hạn chế ly hợp tự nối ở tốc độ cao.", "Bù tác động lực ly tâm của dầu.", ("buồng cân bằng",)),
        part("D", "Piston tác động", 47, 25, "Biến áp suất dầu thành lực ép cụm đĩa.", "Biến áp suất dầu thành lực ép.", ("piston", "pít tông")),
        part("E", "Ly hợp C1", 65, 17, "Cụm ly hợp ngoài; nối với trục đặc theo sơ đồ của bài.", "Cụm ly hợp ngoài nối với trục đặc.", ("c1",)),
        part("F", "Ly hợp C2", 65, 41, "Cụm ly hợp trong; nối với trục rỗng theo sơ đồ của bài.", "Cụm ly hợp trong nối với trục rỗng.", ("c2",)),
    ], "2.4.3")

DRY = figure("dry", "T1_image96.png", "Hình 2.28 — Ly hợp kép ma sát khô: a) đóng C1; b) đóng C2",
    [
        part("A", "Đĩa ép C1", 34, 18, "Ép đĩa ly hợp C1 khi càng đóng dài tác động.", "Ép đĩa ly hợp C1.", ("đĩa ép ly hợp c1",)),
        part("B", "Đĩa ly hợp C1", 28, 65, "Đĩa ma sát nối với trục đặc.", "Đĩa ma sát nối với trục đặc.", ("đĩa ma sát c1",)),
        part("C", "Càng đóng ly hợp C1", 16, 65, "Nhận lực từ xi lanh con để tác động vào cơ cấu đóng C1.", "Truyền lực xi lanh con để đóng C1.", ("càng đóng c1",)),
        part("D", "Xi lanh con", 9, 85, "Dẫn động càng đóng ly hợp bằng thủy lực.", "Dẫn động càng đóng bằng thủy lực.", ("xi lanh công tác",)),
        part("E", "Càng đóng ly hợp C2", 65, 54, "Càng đóng ngắn tác động vào cơ cấu đóng C2.", "Càng đóng ngắn điều khiển C2.", ("càng đóng c2",)),
        part("F", "Đĩa ép C2", 76, 70, "Ép đĩa ly hợp C2 để nối mômen tới trục rỗng.", "Ép đĩa ly hợp C2.", ("đĩa ép ly hợp c2",)),
    ], "2.4.3")

def phase(title, text, **state):
    return dict(title=title, text=text, **state)

CLUTCH = dict(id="clutch", kind="clutch", title="Đóng → ngắt → đóng lại: ly hợp ma sát thường đóng",
    steps=[
        phase("Đóng ly hợp", "Bàn đạp được nhả. Lò xo ép kẹp đĩa ma sát giữa bánh đà và đĩa ép; mômen truyền tới trục sơ cấp.", gap=0, torque=1, control=0),
        phase("Bắt đầu đạp bàn đạp", "Dẫn động đưa ổ bi bạc mở tới đầu trong lò xo màng. Lực ép bắt đầu thay đổi.", gap=0.15, torque=0.7, control=1),
        phase("Ngắt hoàn toàn", "Đĩa ép tách khỏi đĩa ma sát, đường truyền mômen bị ngắt. Trục bị động vẫn có thể quay do quán tính.", gap=1, torque=0, control=1),
        phase("Nhả bàn đạp từ từ", "Lực tác động lên bạc mở giảm; lò xo ép đưa đĩa ép trở lại. Các bề mặt có thể trượt trong giai đoạn tiếp nối.", gap=0.4, torque=0.5, control=0.5),
        phase("Đóng trở lại", "Các bề mặt được ép chặt; đường truyền mômen được thiết lập trở lại.", gap=0, torque=1, control=0),
    ])

TWO_SIM = dict(id="two", kind="clutch", title="Ly hợp hai đĩa ma sát thường đóng", double=True,
    steps=[
        phase("Cụm hai đĩa được ép chặt", "Bánh đà, hai đĩa ma sát, đĩa ép trung gian và đĩa ép ngoài tạo các cặp tiếp xúc truyền mômen.", gap=0, torque=1, control=0),
        phase("Tác động cơ cấu mở", "Ổ bi bạc mở tác động vào cần tách hoặc lò xo màng, làm đĩa ép ngoài dịch ra.", gap=0.3, torque=0.6, control=1),
        phase("Tách các mặt ma sát", "Cơ cấu chống dính giúp đĩa ép trung gian tách khỏi các đĩa ma sát. Đường truyền mômen bị ngắt.", gap=1, torque=0, control=1),
        phase("Đóng lại", "Khi thôi tác động cơ cấu mở, lực lò xo kẹp chặt cụm đĩa và mômen được truyền trở lại.", gap=0, torque=1, control=0),
    ])

MULTI_SIM = dict(id="multi", kind="multi", title="Ly hợp nhiều đĩa đóng bằng áp suất dầu",
    steps=[
        phase("Chưa cấp áp suất tác động", "Các đĩa chưa được piston ép chặt; nhánh ly hợp này chưa truyền mômen.", pressure=0, torque=0),
        phase("Cấp dầu điều khiển", "Dầu có áp vào buồng tác động, tạo lực trên piston.", pressure=1, torque=0),
        phase("Piston ép chồng đĩa", "Piston ép các đĩa chủ động và bị động xen kẽ; mômen được truyền qua moayơ.", pressure=1, torque=1),
        phase("Giảm áp để ngắt", "Van điều khiển giảm áp trong buồng tác động; lực ép được giải phóng và đường truyền mômen bị ngắt.", pressure=0, torque=0),
    ])

MECH_SIM = dict(id="mechanical", kind="drive", title="Dẫn động cơ khí: mở và hồi vị", drive="mechanical",
    steps=[
        phase("Bàn đạp được nhả", "Cáp chưa tạo lực mở. Ly hợp thường đóng đang truyền mômen.", active=[], gap=0, torque=1),
        phase("Đạp bàn đạp", "Lực chân làm bàn đạp quay và kéo cáp.", active=[0,1], gap=0.1, torque=0.9),
        phase("Cáp kéo cơ cấu mở", "Cáp và đòn liên kết đưa ổ bi bạc mở tới lò xo màng hoặc cần tách.", active=[0,1,2,3], gap=0.5, torque=0.5),
        phase("Ly hợp ngắt", "Cơ cấu tách giải phóng lực ép. Đường truyền mômen sang hộp số bị ngắt.", active=[0,1,2,3], gap=1, torque=0),
        phase("Thôi tác động bàn đạp", "Lò xo hồi vị và lò xo ép đưa các cơ cấu trở lại; ly hợp đóng.", active=[], gap=0, torque=1),
    ])

HYD_SIM = dict(id="hydraulic", kind="drive", title="Dẫn động thủy lực: đường truyền áp suất", drive="hydraulic",
    steps=[
        phase("Bàn đạp được nhả", "Chưa tạo áp suất mở ly hợp. Ly hợp thường đóng đang truyền mômen.", active=[], gap=0, torque=1),
        phase("Đạp bàn đạp, đẩy piston chính", "Lực từ bàn đạp làm piston xi lanh chính dịch chuyển để tạo áp suất.", active=[0,1], gap=0.1, torque=0.9),
        phase("Áp suất truyền trong đường dầu", "Áp suất thủy lực truyền qua đường ống tới xi lanh công tác.", active=[0,1,2], gap=0.3, torque=0.7),
        phase("Xi lanh công tác tác động càng mở", "Piston và chốt đẩy đưa càng mở tác động lên bạc mở; lực ép được giải phóng.", active=[0,1,2,3], gap=1, torque=0),
        phase("Nhả bàn đạp, hồi vị", "Cơ cấu hồi vị đưa các piston trở về; áp suất mở giảm và ly hợp đóng trở lại.", active=[], gap=0, torque=1),
    ])

ASSIST_SIM = dict(id="assist", kind="assist", title="Trợ lực khí nén hỗ trợ dẫn động cơ khí",
    steps=[
        phase("Bàn đạp được nhả", "Đường cấp khí đóng, đường xả mở; bộ trợ lực chưa tạo lực mở ly hợp.", stage=0, torque=1),
        phase("Bàn đạp điều khiển van", "Dẫn động cơ khí đưa van phân phối tới vị trí đóng đường xả trước.", stage=1, torque=0.8),
        phase("Mở đường cấp khí", "Khí nén từ nguồn đi vào buồng trợ lực; lực khí nén bổ sung cho lực người lái.", stage=2, torque=0.5),
        phase("Ngắt ly hợp", "Piston/màng và cần đẩy tác động cơ cấu mở, làm mất lực ép giữa các bề mặt ma sát.", stage=3, torque=0),
        phase("Nhả bàn đạp, xả khí", "Van cấp đóng; đường xả mở để giảm áp buồng trợ lực, các cơ cấu hồi vị.", stage=4, torque=1),
    ])

ACS_SIM = dict(id="acs", kind="acs", title="ACS: nhận dạng sang số → ngắt → nối lại",
    steps=[
        phase("Tiếp nhận tín hiệu", "Cảm biến nhận dạng dự tính sang số gửi thông tin; bộ điều khiển còn nhận tốc độ và các tín hiệu liên quan.", stage=0, torque=1),
        phase("Bộ điều khiển xử lý", "Bộ điều khiển tính toán lệnh đóng/ngắt và phát lệnh tới cơ cấu chấp hành.", stage=1, torque=1),
        phase("Cơ cấu chấp hành tạo áp suất", "Động cơ điện và bộ truyền trục vít – bánh vít tác động xi lanh chính; áp suất được truyền tới xi lanh con.", stage=2, torque=0.5),
        phase("Ly hợp ngắt để sang số", "Xi lanh con tác động cơ cấu mở. Đường truyền mômen bị ngắt trong giai đoạn sang số.", stage=3, torque=0),
        phase("Nối lại có điều khiển", "Sau khi nhận dạng số đã gài, bộ điều khiển điều chỉnh cơ cấu chấp hành để ly hợp đóng lại với độ trượt phù hợp.", stage=4, torque=1),
    ])

DUAL_SIM = dict(id="dual", kind="dual", title="Chuyển từ số 1 sang số 2",
    steps=[
        phase("Đang chạy số 1", "C1 nối mômen tới IS1 và số 1. C2 chưa truyền mômen.", c1=1, c2=0, selected="Số 1"),
        phase("Chọn trước số 2", "Số 2 được chọn ở nhánh IS2 khi C2 vẫn ngắt; C1 tiếp tục truyền mômen cho số 1.", c1=1, c2=0, selected="Số 2 chọn trước"),
        phase("Chuyển tiếp có kiểm soát", "Khả năng truyền mômen của C1 giảm dần, C2 tăng dần. Đây là giai đoạn trùng lặp có kiểm soát, không phải khóa cứng cả hai nhánh.", c1=0.5, c2=0.5, selected="Chuyển tiếp 1 → 2"),
        phase("Đang chạy số 2", "C1 ngắt; C2 nối mômen tới IS2 và số 2.", c1=0, c2=1, selected="Số 2"),
        phase("Chọn trước số 3", "Số 3 được chọn ở nhánh IS1 khi C1 vẫn ngắt; C2 duy trì truyền mômen cho số 2.", c1=0, c2=1, selected="Số 3 chọn trước"),
    ])

WET_SIM = dict(id="wet", kind="dualtype", title="Ly hợp kép ướt: tác động C1", wet=True,
    steps=[
        phase("C1 chưa nhận áp suất đóng", "Cụm C1 chưa được ép chặt; nhánh C1 chưa truyền mômen trong minh họa.", pressure=0, c1=0, c2=0),
        phase("Cấp dầu vào buồng áp suất", "Dầu điều khiển có áp được dẫn tới buồng áp suất của C1.", pressure=1, c1=0, c2=0),
        phase("Piston ép cụm đĩa C1", "Áp suất tác động lên piston, kẹp các đĩa và thiết lập đường truyền mômen tới trục đặc.", pressure=1, c1=1, c2=0),
        phase("Giảm áp để ngắt C1", "Giải phóng áp suất tác động làm mất lực ép và ngắt nhánh C1.", pressure=0, c1=0, c2=0),
    ])

DRY_SIM = dict(id="dry", kind="dualtype", title="Ly hợp kép khô: tác động C2", wet=False,
    steps=[
        phase("C2 chưa được tác động", "Cụm C2 chưa được cơ cấu đóng ép chặt.", pressure=0, c1=0, c2=0),
        phase("Xi lanh con tác động càng đóng", "Dầu điều khiển tác động xi lanh con để dịch chuyển càng đóng C2. Dầu nằm trong dẫn động, không ngâm các mặt ma sát khô.", pressure=1, c1=0, c2=0),
        phase("Ép đĩa C2", "Càng đóng ngắn tác động cơ cấu ép C2, thiết lập đường truyền mômen tới trục rỗng.", pressure=1, c1=0, c2=1),
        phase("Thôi tác động C2", "Giải phóng tác động của cơ cấu đóng; nhánh C2 ngắt.", pressure=0, c1=0, c2=0),
    ])

lessons = {}
def add(code, title, objectives, figures, simulations, predict, order, task_figure=None, targets=None):
    f = next(f for f in figures if f["id"] == task_figure) if task_figure else figures[0]
    ids = targets or [p["id"] for p in f["parts"][:4]]
    lessons[code] = dict(code=code, title=title, objectives=objectives, figures=figures, simulations=simulations,
        exercises=[
            dict(id="predict", type="predict", title="Dự đoán trước khi xem", prompt=predict[0],
                 options=predict[1], answer=0, explanation=predict[2]),
            dict(id="order", type="order", title="Sắp xếp quy trình", prompt=order[0],
                 items=order[1], explanation=order[2]),
            dict(id="label", type="label", title="Điền tên chi tiết", prompt="Điền tên chi tiết tại các vị trí được đánh dấu. Có thể gõ có dấu hoặc không dấu.",
                 figure=f["id"], targets=ids[:3], explanation="Đối chiếu tên với hình và vai trò của từng chi tiết."),
            dict(id="match", type="match", title="Ghép công dụng trên hình", prompt="Chọn một mô tả rồi bấm vị trí trên hình, hoặc kéo mô tả tới vị trí tương ứng.",
                 figure=f["id"], targets=ids, explanation="Ghép theo công dụng, không theo thứ tự các mô tả."),
        ])

add("2.1.1", "Chức năng của ly hợp",
    ["Giải thích lúc nào cần nối và ngắt mômen.", "Liên hệ các bộ phận với chức năng truyền mômen và khởi hành êm."],
    [ONE], [CLUTCH],
    ("Khi ly hợp ma sát thường đóng được ngắt hoàn toàn, dòng mômen từ động cơ tới trục sơ cấp thay đổi thế nào?",
     ["Bị ngắt; trục sơ cấp vẫn có thể quay do quán tính.", "Luôn truyền toàn bộ mômen vì bánh đà vẫn quay.", "Tăng lên do lực lên bàn đạp tăng.", "Đổi chiều ngay khi đạp bàn đạp."],
     "Ngắt ly hợp giải phóng lực ép giữa các bề mặt ma sát. Việc ngắt mômen không đồng nghĩa trục bị động dừng ngay."),
    ("Sắp xếp một chu trình sang số khái quát với ly hợp điều khiển bằng bàn đạp.",
     ["Đạp bàn đạp để ngắt ly hợp.", "Thực hiện chuyển sang số phù hợp.", "Nhả bàn đạp từ từ để nối lại.", "Ly hợp đóng, truyền mômen qua số đã chọn."],
     "Cần ngắt ly hợp trước khi chuyển số; việc nối lại được thực hiện êm dịu."), targets=["A","B","D","E"])

add("2.1.2", "Phân loại ly hợp",
    ["Phân biệt phương pháp truyền mômen với phương pháp dẫn động.", "Nhận dạng ly hợp ma sát thường đóng dùng lò xo màng."],
    [ONE], [CLUTCH],
    ("Ly hợp ma sát được điều khiển bằng dẫn động thủy lực. Mômen giữa bánh đà và đĩa bị động được truyền chủ yếu bằng gì?",
     ["Lực ma sát giữa các bề mặt được ép chặt.", "Áp suất dầu trong đường dẫn điều khiển.", "Lực kéo của ổ bi bạc mở.", "Dòng điện trong bộ chấp hành."],
     "Dầu trong dẫn động dùng để điều khiển đóng/ngắt; ở ly hợp ma sát, mômen được truyền qua các mặt ma sát."),
    ("Với ly hợp ma sát thường đóng trong hình, sắp xếp một chu trình bắt đầu khi bàn đạp được nhả: đóng → ngắt → đóng lại.",
     ["Bàn đạp được nhả: lực lò xo kẹp các mặt ma sát.", "Đạp bàn đạp: dẫn động tác động cơ cấu mở.", "Giữ bàn đạp ở vị trí ngắt: lực ép được giải phóng.", "Nhả bàn đạp từ từ: lực lò xo khôi phục tiếp xúc ma sát."],
     "Chu trình này áp dụng cho ly hợp ma sát thường đóng minh họa trong hình; các loại ly hợp khác có thể có cách tác động khác."), targets=["A","B","C","D"])

add("2.2.1", "Ly hợp một đĩa ma sát",
    ["Chỉ ra bộ phận chủ động, bị động và cơ cấu mở.", "Giải thích trình tự ngắt ly hợp kiểu ép bằng lò xo màng."],
    [ONE], [CLUTCH],
    ("Ở ly hợp lò xo màng kiểu ngắt bằng cách ép, ổ bi bạc mở tác động trước hết vào đâu?",
     ["Đầu trong của lò xo màng.", "Trực tiếp vào mặt ma sát của bánh đà.", "Moayơ của đĩa bị động.", "Đầu ngoài trục sơ cấp hộp số."],
     "Bạc mở tác động đầu trong lò xo màng; lò xo làm đòn bẩy để giảm lực ép và tách đĩa ép."),
    ("Sắp xếp trình tự ngắt ly hợp một đĩa, lò xo màng, kiểu ép.",
     ["Người lái đạp bàn đạp ly hợp.", "Dẫn động đưa ổ bi bạc mở tới đầu trong lò xo màng.", "Lò xo màng đổi trạng thái, lực ép lên đĩa ép giảm.", "Đĩa ép tách khỏi đĩa ma sát, dòng mômen bị ngắt."],
     "Ổ bi bạc mở điều khiển lò xo màng; không trực tiếp truyền mômen tới hộp số."), targets=["B","C","D","E"])

add("2.2.2", "Ly hợp hai đĩa và nhiều đĩa ma sát",
    ["Nhận dạng đĩa ép trung gian và các đĩa ma sát.", "Phân biệt ly hợp lò xo thường đóng với cụm nhiều đĩa đóng bằng áp suất dầu."],
    [TWO, MULTI], [TWO_SIM, MULTI_SIM],
    ("Với cụm ly hợp nhiều đĩa đóng bằng áp suất dầu như Hình 2.14, giảm áp suất tác động lên piston sẽ có xu hướng nào?",
     ["Giảm lực ép, làm ngắt đường truyền mômen.", "Tăng lực ép do các đĩa có số lượng lớn.", "Giữ nguyên lực ép trong mọi điều kiện.", "Đổi nhóm số lẻ thành nhóm số chẵn."],
     "Ở cụm đóng bằng áp suất dầu, áp suất tạo lực ép piston. Không áp dụng chiều tác động bàn đạp của ly hợp lò xo thường đóng cho mọi loại ly hợp."),
    ("Sắp xếp trình tự đóng cụm ly hợp nhiều đĩa bằng áp suất dầu.",
     ["Van điều khiển cấp dầu có áp vào buồng tác động.", "Áp suất dầu tạo lực lên piston.", "Piston ép các đĩa chủ động và bị động xen kẽ.", "Mômen truyền qua các bề mặt ma sát tới moayơ và trục."],
     "Nguồn điều khiển là áp suất dầu, còn mômen được truyền qua các mặt ma sát."), task_figure="multi", targets=["A","B","C","D"])

add("2.3.1", "Dẫn động điều khiển bằng cơ khí",
    ["Theo dõi đường truyền lực bàn đạp → cáp → cơ cấu mở.", "Giải thích vai trò của hành trình tự do và hồi vị."],
    [MECHANICAL], [MECH_SIM],
    ("Nếu hành trình tự do của bàn đạp quá lớn, điều gì dễ xảy ra khi đạp hết hành trình?",
     ["Cơ cấu mở không đủ hành trình, ly hợp có thể ngắt không dứt khoát.", "Ly hợp luôn ngắt ngay dù chưa đạp.", "Lực ép lò xo tăng tới mức không thể đóng.", "Cáp kéo tự tạo thêm áp suất thủy lực."],
     "Một phần hành trình bị dùng để khắc phục khe hở quá lớn, nên hành trình tác động mở có thể không đủ."),
    ("Sắp xếp đường truyền tác động khi ngắt ly hợp bằng dẫn động cơ khí.",
     ["Bàn đạp nhận lực chân người lái.", "Cáp kéo truyền lực tới đòn liên kết.", "Đòn liên kết đưa ổ bi bạc mở tác động cơ cấu tách.", "Đĩa ép được tách, đường truyền mômen bị ngắt."],
     "Lực điều khiển đi qua cáp và các đòn cơ khí tới cơ cấu tách."), targets=["A","B","C","D"])

add("2.3.2", "Dẫn động điều khiển bằng thủy lực",
    ["Nhận dạng xi lanh chính, xi lanh công tác và đường dầu.", "Theo dõi quá trình biến lực bàn đạp thành lực mở ly hợp."],
    [HYDRAULIC, MASTER, SLAVE], [HYD_SIM],
    ("Khi có không khí lẫn trong dẫn động thủy lực, hiệu quả mở ly hợp có thể giảm vì sao?",
     ["Không khí bị nén, làm giảm hiệu quả truyền chuyển động và áp suất tới xi lanh công tác.", "Không khí làm dầu trở thành chất rắn.", "Không khí luôn làm lực mở tăng gấp đôi.", "Không khí làm ly hợp chuyển thành loại nam châm điện."],
     "Không khí dễ bị nén hơn chất lỏng, nên dẫn động có thể không tạo đủ hành trình mở. Vít xả khí dùng trong quá trình xả khí khi bảo dưỡng."),
    ("Sắp xếp quá trình truyền tác động trong dẫn động thủy lực.",
     ["Bàn đạp và cần đẩy làm piston xi lanh chính dịch chuyển.", "Xi lanh chính tạo áp suất dầu.", "Áp suất truyền qua đường ống tới xi lanh công tác.", "Piston và chốt đẩy tác động càng mở để ngắt ly hợp."],
     "Xi lanh chính tạo áp suất; xi lanh công tác biến áp suất thành lực trên cơ cấu mở."), targets=["B","C","D","F"])

add("2.3.3", "Dẫn động điều khiển có trợ lực",
    ["Nhận dạng đường cơ khí và nguồn khí nén phụ trợ.", "Giải thích thứ tự điều khiển van cấp/xả khí."],
    [ASSIST], [ASSIST_SIM],
    ("Với dẫn động cơ khí có trợ lực khí nén trong bài, khi nguồn khí nén bị mất thì điều khiển ly hợp thế nào?",
     ["Vẫn có thể điều khiển bằng đường cơ khí, nhưng lực bàn đạp tăng.", "Luôn tự động đóng và ngắt mà không cần người lái.", "Đường cơ khí bị loại bỏ hoàn toàn.", "Cáp kéo biến thành đường dẫn dầu."],
     "Đường cơ khí vẫn còn tác dụng; khí nén chỉ bổ sung lực trợ giúp trong kết cấu đang minh họa."),
    ("Sắp xếp trình tự trợ lực khi ngắt ly hợp.",
     ["Bàn đạp tác động dẫn động cơ khí và van phân phối.", "Van đóng đường xả khí.", "Van mở đường cấp khí tới buồng trợ lực.", "Piston/màng và cần đẩy bổ sung lực cho cơ cấu mở."],
     "Đóng đường xả trước khi cấp khí giúp áp suất hình thành trong buồng trợ lực."), targets=["B","C","D","E"])

add("2.4.1", "Hệ thống ly hợp tự động ACS",
    ["Theo dõi tín hiệu đầu vào → điều khiển → chấp hành.", "Giải thích quá trình ngắt/nối lại ly hợp khi sang số."],
    [ACS], [ACS_SIM],
    ("Khi hệ thống ACS nhận dạng người lái dự tính sang số, bộ phận nào xử lý thông tin để phát lệnh chấp hành?",
     ["Bộ điều khiển ly hợp.", "Bản thân đĩa ma sát.", "Xi lanh con tự chọn số bằng cơ khí.", "Bánh đà tự nhận dạng vị trí cần số."],
     "Bộ điều khiển xử lý tín hiệu cảm biến và phát lệnh tới động cơ điện, bộ truyền và dẫn động thủy lực."),
    ("Sắp xếp trình tự ngắt ly hợp của ACS khi nhận dạng sang số.",
     ["Cảm biến nhận dạng dự tính sang số gửi tín hiệu.", "Bộ điều khiển xử lý và phát lệnh tới động cơ điện.", "Động cơ điện, bộ truyền trục vít – bánh vít tác động xi lanh chính.", "Áp suất tới xi lanh con, cơ cấu mở ngắt ly hợp."],
     "ACS dùng thông tin đầu vào để điều khiển cơ cấu chấp hành; trong hệ thống này không cần bàn đạp ly hợp."), targets=["A","B","D","E"])

add("2.4.2", "Hệ thống ly hợp kép",
    ["Xác định C1–IS1 và C2–IS2 theo sơ đồ bài học.", "Giải thích chọn trước số và chuyển tiếp mômen."],
    [DUAL], [DUAL_SIM],
    ("Khi đang chạy số 1 và số 2 đã được chọn trước, trạng thái hai ly hợp trước giai đoạn chuyển tiếp là gì?",
     ["C1 truyền mômen; C2 vẫn ngắt.", "C1 và C2 đều khóa cứng hoàn toàn.", "C1 ngắt và C2 đã truyền toàn bộ mômen.", "Cả hai trục sơ cấp đều bị khóa với vỏ."],
     "Chọn trước số ở nhánh chưa truyền mômen không có nghĩa ly hợp nhánh đó đã đóng. Việc chuyển mômen diễn ra trong giai đoạn chuyển tiếp có kiểm soát."),
    ("Sắp xếp trình tự chuyển từ số 1 sang số 2 theo sơ đồ bài.",
     ["C1 đang truyền mômen ở số 1; số 2 được chọn trước ở nhánh C2.", "Bộ điều khiển bắt đầu giảm truyền mômen qua C1 và tăng qua C2.", "Chuyển tiếp có kiểm soát từ nhánh C1 sang nhánh C2.", "C2 truyền mômen ở số 2; C1 ngắt và có thể chọn trước số 3."],
     "Hai nhánh có giai đoạn trùng lặp có kiểm soát để hạn chế gián đoạn lực kéo; không khóa cứng cả hai nhánh ở hai tỷ số khác nhau."), targets=["A","B","C","D"])

add("2.4.3", "Kết cấu ly hợp kép ướt và khô",
    ["Phân biệt dầu điều khiển với dầu tiếp xúc các mặt ma sát.", "Nhận dạng buồng áp suất, buồng cân bằng và cơ cấu đóng."],
    [WET, DRY], [WET_SIM, DRY_SIM],
    ("Ly hợp kép có các bề mặt ma sát khô nhưng dùng xi lanh con điều khiển. Nhận xét nào đúng?",
     ["Dầu có thể dùng trong dẫn động; các mặt ma sát vẫn không ngâm trong dầu.", "Có xi lanh con thì mọi mặt ma sát bắt buộc ngâm dầu.", "Ly hợp khô không thể có bất kỳ dẫn động thủy lực nào.", "Dầu điều khiển tự truyền mômen thay cho đĩa ma sát."],
     "Tên 'khô/ướt' mô tả điều kiện các mặt ma sát. Dẫn động thủy lực không tự làm một ly hợp ma sát khô trở thành ly hợp ướt."),
    ("Sắp xếp trình tự đóng C1 của ly hợp kép ướt.",
     ["Bộ điều khiển cấp dầu có áp vào buồng áp suất C1.", "Áp suất dầu tạo lực lên piston C1.", "Piston ép cụm đĩa ma sát C1.", "Mômen truyền qua C1 tới trục đặc."],
     "Buồng cân bằng dầu bù tác động lực ly tâm; nó không thay thế buồng áp suất tạo lực đóng."), task_figure="wet", targets=["A","B","C","D"])

bank = json.loads((ROOT / "on_tap/ngan_hang_cau_hoi.json").read_text(encoding="utf-8"))
for code, lesson in lessons.items():
    lesson["file"] = bank["lessons"][code]["file"]
data = dict(version="2.0-chuong2-2026-10-13", lessons=lessons,
            scope="Chương 2 — Ly hợp", originalQuestionBankCount=411)
(OUT / "lesson-data.json").write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
(OUT / "lesson-data.js").write_text("window.OTO_C2_DATA = " + json.dumps(data, ensure_ascii=False, separators=(",", ":")) + ";\n", encoding="utf-8")
print("Written", len(lessons), "lessons;", sum(len(l["exercises"]) for l in lessons.values()), "activities")
