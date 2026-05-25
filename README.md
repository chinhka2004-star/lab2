# lab2: HỆ THỐNG PHÒNG THỰC HÀNH SO SÁNH GIẤU TIN CHUYỂN CẢNH

Chào mừng thầy/cô và các bạn sinh viên đến với **lab2**! Đây là kho lưu trữ chứa bài thực hành so sánh kỹ thuật giấu tin mật mã nâng cao trong video được đóng gói chuẩn hóa dưới dạng **Labtainers IModule** để chạy trên hệ điều hành ảo hóa Debian/Ubuntu.

## 🔬 Chủ đề: So sánh Giấu tin Chuyển cảnh Thích ứng và Tuần tự (Scene Difference Comparison)

Bài thực hành **`scenediff-compare`** được thiết kế nhằm giúp sinh viên hiểu rõ sự khác biệt định lượng giữa hai chiến thuật giấu tin LSB trên video:
1. **Adaptive LSB Steganography:** Chỉ nhúng thông điệp vào các khung hình chuyển cảnh (Scene Changes) - nơi mắt người kém nhạy cảm nhất do hiện tượng che mắt tạm thời (temporal masking).
2. **Sequential LSB Steganography:** Nhúng thông điệp liên tục từ khung hình đầu tiên (frame 0) trở đi, không quan tâm đến nội dung.

Sinh viên sẽ lập trình cả 2 phương pháp và so sánh mức độ suy giảm chất lượng hình ảnh thông qua chỉ số **PSNR (Peak Signal-to-Noise Ratio)** và tính hỗn loạn thống kê thông qua **Shannon Entropy**.

---

## 📂 1. Cấu trúc bài Lab `scenediff-compare`

```text
/
├── imodule.tar                                      # Gói cài đặt Labtainers đóng gói sẵn
├── Tai_lieu_huong_dan_Scene_Difference_Comparison.md # Tài liệu hướng dẫn chi tiết (bản in ấn)
├── Tai_lieu_huong_dan_Scene_Difference_Comparison.docx # Tài liệu Word (.docx) để sinh viên nộp báo cáo
├── README.md                                        # Tài liệu trang chủ hướng dẫn nhanh
└── scenediff-compare/                               # Thư mục cấu hình bài Lab
    ├── config/
    │   ├── start.config                             # Cấu hình container stego-container
    │   └── lab.conf                                 # Mô tả bài lab
    ├── dockerfiles/
    │   └── Dockerfile.scenediff-compare.stego-container.student # Định nghĩa Dockerfile học viên
    ├── instr_config/
    │   ├── results.config                           # Khai báo biến trích xuất điểm số
    │   └── goals.config                             # Quy chuẩn mục tiêu đánh giá tự động
    └── stego-container/
        ├── compare.py                           # Khung mã nguồn sinh viên cần hoàn thiện (TODO)
        ├── generate_video.py                    # Tự động sinh video gốc cover
        ├── startup.sh                           # Tập lệnh tự chạy khi kích hoạt lab
        ├── instructions.txt                     # Hướng dẫn nhiệm vụ trong container
        ├── checkwork.sh                         # Kịch bản tự chấm điểm tại chỗ (100 điểm)
        └── solution/
            └── compare_sol.py                   # Giải pháp mẫu hoàn chỉnh của giảng viên
```

---

## 🛠️ 2. Quy trình Cài đặt & Khởi chạy dành cho Sinh viên

Sinh viên chỉ cần thực hiện các bước lệnh đơn giản trực tiếp trên máy ảo Labtainers để bắt đầu:

### Bước 1: Nạp bài Lab từ lab2 về hệ thống cục bộ
```bash
imodule https://github.com/chinhka2004-star/lab2/raw/main/imodule.tar
```

### Bước 2: Di chuyển vào không gian làm việc sinh viên
```bash
cd ~/labtainer/labtainer-student
```

### Bước 3: Biên dịch Docker Image cục bộ cho phòng Lab (Bắt buộc)
```bash
rebuild scenediff-compare
```

### Bước 4: Kích hoạt Container ảo Ubuntu và làm bài
```bash
labtainer scenediff-compare
```

---

## 🧪 3. Cơ chế Đánh giá & So sánh (Evaluation Logic)

- **PSNR (Peak Signal-to-Noise Ratio):** Đo lường chất lượng hình ảnh của khung hình stego so với ảnh cover gốc. Trị số PSNR càng cao thể hiện chất lượng ảnh càng ít bị suy giảm.
- **Shannon Entropy:** Đo lường độ hỗn loạn trên dòng bit LSB. Sự xuất hiện của thông điệp được mã hóa ngẫu nhiên sẽ làm Entropy tiệm cận $1.0$ trên các khung hình bị nhúng, làm tăng khả năng bị phát hiện bởi các công cụ Steganalysis.

---

## 📈 4. Hệ thống Chấm điểm tự động (Grading Matrix)

Khi sinh viên chạy `./checkwork.sh` bên trong container hoặc hệ thống máy host chấm điểm bằng `checkwork scenediff-compare`, thang điểm 100 được tính như sau:

| STT | Tiêu chí đánh giá | Điểm số | Điều kiện đạt |
| :-: | :--- | :-: | :--- |
| **1** | Nhúng thích ứng (Adaptive) | **30 điểm** | Dữ liệu chỉ được nhúng ở các frame chuyển cảnh (30, 60) |
| **2** | Nhúng tuần tự (Sequential) | **30 điểm** | Dữ liệu được nhúng tuần tự từ frame 0 trở đi |
| **3** | Tính toán PSNR & Entropy | **20 điểm** | Kết quả tính toán PSNR và Entropy trong báo cáo khớp với lời giải mẫu |
| **4** | Đúng định dạng báo cáo | **20 điểm** | File `comparison_report.txt` chứa đủ thông tin đối so sánh |

---

## 🛡️ Bản quyền & Thiết kế
- **Giảng viên thiết kế:** Kỹ sư An toàn thông tin & Giảng viên An ninh mạng.
- **Môi trường vận hành:** Tự động hóa hoàn toàn thông qua **Labtainer Framework**.
- **GitHub Repository:** [chinhka2004-star/lab2](https://github.com/chinhka2004-star/lab2)
