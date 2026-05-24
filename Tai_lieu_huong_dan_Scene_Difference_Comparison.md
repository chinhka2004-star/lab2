BÀI THỰC HÀNH: SO SÁNH GIẤU TIN CHUYỂN CẢNH THÍCH ỨNG VÀ TUẦN TỰ
Mục tiêu bài thực hành
Trong bài lab này, sinh viên sẽ tìm hiểu và so sánh định lượng hai kỹ thuật giấu tin LSB (Least Significant Bit) trên video:
1. Adaptive LSB Steganography (Nhúng thích ứng): Chỉ nhúng thông điệp vào LSB của các khung hình chuyển cảnh (Scene Change) có độ biến động nội dung lớn.
2. Sequential LSB Steganography (Nhúng tuần tự): Nhúng thông điệp liên tục từ khung hình đầu tiên (frame 0) trở đi mà không quan tâm đến nội dung.

Sinh viên sẽ thực hiện đo lường chất lượng hình ảnh bằng chỉ số PSNR (Peak Signal-to-Noise Ratio) và kiểm định thống kê bằng Shannon Entropy để thấy rõ sự khác biệt và tối ưu hóa trong bảo mật thông tin đa phương tiện.

Kỹ năng đạt được
- Hiểu và lập trình thành thạo giải thuật nhúng tin thích ứng (Adaptive) và tuần tự (Sequential) LSB trên video.
- Nắm vững công thức toán học và cách lập trình tính toán chỉ số PSNR và Shannon Entropy.
- Kỹ năng đánh giá định lượng chất lượng hình ảnh và phân tích độ bảo mật thống kê.
- Kỹ năng kiểm thử tự động bài lab thông qua hệ thống kết xuất tang chứng vật lý tự động của Labtainer framework.

Yêu cầu đối với sinh viên
- Có kiến thức nền tảng về xác suất thống kê và lý thuyết thông tin.
- Có khả năng lập trình Python cơ bản và xử lý ảnh thông qua thư viện Pillow (PIL).
- Có khả năng sử dụng các lệnh điều khiển Linux nâng cao, quản lý gói phần mềm hệ thống.

Kiến thức bổ trợ
1. Công thức PSNR (Peak Signal-to-Noise Ratio)
PSNR đo chất lượng ảnh sau khi bị tác động (ở đây là nhúng stego) so với ảnh gốc. Cho ảnh màu RGB kích thước W x H:
$$MSE = \frac{1}{3 \times W \times H} \sum_{c \in \{R,G,B\}} \sum_{y=0}^{H-1} \sum_{x=0}^{W-1} (I_{cover}(x,y,c) - I_{stego}(x,y,c))^2$$
$$PSNR = 10 \cdot \log_{10} \left( \frac{255^2}{MSE} \right)$$
Nếu ảnh stego giống hệt ảnh gốc (MSE = 0), PSNR mặc định đạt 100.0 dB.

2. Lý thuyết Shannon Entropy dòng bit LSB
Shannon Entropy đo độ hỗn loạn của dòng bit trích xuất từ LSB của các kênh màu RGB. Khi nhúng stego (thường là dữ liệu ngẫu nhiên hoặc đã nén/mã hóa), dòng bit sẽ trở nên hỗn loạn hơn, đưa Entropy tiệm cận 1.0 (so với < 0.95 ở các khung hình gốc tự nhiên).

Thông tin lab
| Thông tin | Chi tiết |
| :--- | :--- |
| Tên lab | scenediff-compare |
| Container | ubuntu |
| Công cụ chính | python3, pip, pillow, ffmpeg, ffprobe |
| Phương pháp | LSB Adaptive vs LSB Sequential + PSNR & Shannon Entropy Comparison |
| Dữ liệu đầu vào | Video cover sạch (input_video.mp4) |

Vấn đề kỹ thuật
1. Thuật toán phát hiện chuyển cảnh (Scene Change Detection)
Hệ thống sử dụng phép so khớp sự sai khác trung bình của ma trận ảnh thang xám giữa hai khung hình kề nhau để khoanh vùng các khung hình chuyển cảnh có khả năng cao bị lợi dụng để nhúng tin ẩn.
2. So sánh chất lượng và bảo mật (PSNR & Entropy)
Khi nhúng tuần tự, nhiễu LSB xuất hiện ở các khung hình tĩnh hoặc nền phẳng, làm giảm mạnh PSNR cục bộ và dễ bị phát hiện. Khi nhúng thích ứng vào chuyển cảnh, nhiễu stego được che lấp bởi các chi tiết biến động mạnh của cảnh mới, đồng thời có chất lượng thị giác tự nhiên hơn.

Khởi động Lab
Chuẩn bị môi trường hệ thống:
1. Sử dụng lệnh imodule để nạp cấu hình bài thực hành từ kho lưu trữ về hệ thống cục bộ:
imodule https://github.com/chinhka2004-star/lab2/raw/main/imodule.tar
2. Di chuyển vào không gian làm việc của sinh viên trong framework Labtainer:
cd ~/labtainer/labtainer-student
3. Biên dịch và xây dựng Docker Image cục bộ cho phòng Lab (Bắt buộc đối với bài Lab tùy chỉnh):
rebuild scenediff-compare
4. Khởi chạy bài lab để kích hoạt container ảo Ubuntu:
labtainer scenediff-compare

Nhiệm vụ
Task 1: Khởi động môi trường và kiểm tra các file thành phần
Bước 1: Sau khi hệ thống kích hoạt container thành công, màn hình xuất hiện dấu nhắc lệnh ubuntu@ubuntu:~$
Bước 2: Sử dụng lệnh liệt kê thư mục để xác minh các file kịch bản lập trình có sẵn:
ls -l
Yêu cầu bắt buộc: Sinh viên kiểm tra thấy sự hiện diện đầy đủ của các file: compare.py, generate_video.py, startup.sh và instructions.txt.

Task 2: Cấu hình môi trường và cài đặt các thư viện ảnh chuyên dụng
Bước 1: Tiến hành cập nhật danh sách các kho lưu trữ phần mềm hệ thống:
sudo apt-get update
Bước 2: Cài đặt thư viện xử lý ảnh Pillow cho Python 3:
sudo apt-get install python3-pillow -y
Bước 3: Cài đặt công cụ ffmpeg để giải nén video:
sudo apt-get install ffmpeg -y

Task 3: Thực thi sinh ca kiểm thử tự động
Bước 1: Hệ thống khi khởi động container đã tự động kích hoạt sinh tệp tin video cover gốc. Sinh viên có thể chạy lại thủ công bằng lệnh:
python3 generate_video.py
Bước 2: Kiểm tra sự tồn tại vật lý của file video cover bằng lệnh:
ls -l input_video.mp4

Task 4: Chạy công cụ so sánh và kết xuất báo cáo
Bước 1: Thực thi công cụ compare.py với thông điệp mật mục tiêu để tiến hành so sánh đối chứng cả 2 phương pháp:
python3 compare.py -i input_video.mp4 -m "BI_MAT_QUOC_GIA_PTIT_2026" -o comparison_report.txt -t 10.0
Bước 2: Đọc báo cáo kết quả so sánh đối chứng chất lượng và độ bảo mật:
cat comparison_report.txt

Kết Thúc Bài Lab
Trước khi kết thúc, sinh viên thực hiện kiểm thử tiến độ chấm điểm tự động bằng cách chạy script tại chỗ:
./checkwork.sh
Quay lại Terminal Host và thực thi lệnh giám định của Labtainer:
checkwork scenediff-compare
1. Tại Terminal máy ảo Ubuntu, nhập lệnh thoát:
exit
2. Tại Terminal hệ thống máy Host, gõ lệnh chấm dứt phiên làm việc:
stoplab
Để thực hiện lại bài thực hành từ đầu (Reset toàn bộ cấu hình), sử dụng lệnh cấu hình hệ thống:
labtainer -r scenediff-compare
