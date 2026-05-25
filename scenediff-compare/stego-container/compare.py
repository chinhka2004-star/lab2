import os
import sys
import math
import shutil
import argparse
import subprocess
from PIL import Image

def calculate_frame_difference(img1_path, img2_path):
    """
    TÁC VỤ 2.1: Tính toán sai lệch tuyệt đối trung bình thang xám giữa 2 khung hình
    Yêu cầu:
    - Mở 2 hình ảnh bằng Pillow, chuyển sang hệ màu Grayscale ('L').
    - Tính tổng hiệu tuyệt đối giữa các pixel cùng vị trí của 2 hình ảnh.
    - Trả về giá trị hiệu trung bình (tổng hiệu / tổng số pixel).
    """
    # TODO: Sinh viên hoàn thành code tại đây
    pass

def detect_scene_changes(frames_dir, num_frames, threshold):
    """
    TÁC VỤ 2.2: Phát hiện chuyển cảnh
    Yêu cầu:
    - Duyệt qua toàn bộ danh sách khung hình từ 1 đến num_frames - 1.
    - So sánh frame(i) và frame(i-1) bằng hàm calculate_frame_difference.
    - Nếu độ sai lệch > threshold, thêm index i vào danh sách chuyển cảnh.
    - Trả về danh sách indices chuyển cảnh.
    """
    # TODO: Sinh viên hoàn thành code tại đây
    pass

def get_message_bits(message):
    msg_bytes = (message + '\0').encode('utf-8')
    bits = []
    for byte in msg_bytes:
        for i in range(8):
            bits.append((byte >> (7 - i)) & 1)
    return bits

def embed_bits_to_frame(frame_path, bits):
    """
    TÁC VỤ 2.3: Nhúng thông điệp bit LSB vào kênh màu RGB của khung hình
    Yêu cầu:
    - Mở hình ảnh bằng Pillow, lấy ma trận pixel.
    - Duyệt qua từng pixel và nhúng tuần tự các bit trong mảng `bits` vào LSB của kênh R, sau đó đến G, rồi đến B.
    - Ghi đè hình ảnh đã chỉnh sửa vào `frame_path`.
    """
    # TODO: Sinh viên hoàn thành code tại đây
    pass

def calculate_psnr(img1_path, img2_path):
    """
    TÁC VỤ 2.4: Tính toán Peak Signal-to-Noise Ratio (PSNR) giữa 2 hình ảnh
    Yêu cầu:
    - Mở 2 hình ảnh, tính toán sai số bình phương trung bình (MSE) trên cả 3 kênh màu R, G, B.
    - Công thức MSE: sum((R1-R2)**2 + (G1-G2)**2 + (B1-B2)**2) / (3 * Width * Height).
    - Công thức PSNR = 10 * log10(255**2 / MSE).
    - Lưu ý xử lý trường hợp MSE = 0 để trả về giá trị mặc định là 100.0 dB.
    """
    # TODO: Sinh viên hoàn thành code tại đây
    pass

def calculate_shannon_entropy(bits):
    """
    TÁC VỤ 2.5: Tính toán Entropy Shannon của chuỗi bit
    Yêu cầu:
    - Tính tỷ lệ phân bổ của bit 0 và bit 1 trong mảng `bits`.
    - Tính Entropy: H = - p0*log2(p0) - p1*log2(p1).
    """
    # TODO: Sinh viên hoàn thành code tại đây
    pass

def analyze_lsb_entropy(frame_path, max_pixels=2000):
    img = Image.open(frame_path)
    pixels = img.load()
    width, height = img.size
    
    bits = []
    pixel_count = 0
    
    for y in range(height):
        for x in range(width):
            if pixel_count >= max_pixels:
                break
            r, g, b = pixels[x, y]
            bits.append(r & 1)
            bits.append(g & 1)
            bits.append(b & 1)
            pixel_count += 1
            
    return calculate_shannon_entropy(bits)

def main():
    parser = argparse.ArgumentParser(description="Scene Difference Steganography Comparison Tool")
    parser.add_argument('-i', '--input', required=True, help="Input MP4 video file")
    parser.add_argument('-m', '--message', required=True, help="Secret message to hide")
    parser.add_argument('-o', '--output', default="comparison_report.txt", help="Output comparison report file path")
    parser.add_argument('-t', '--threshold', type=float, default=10.0, help="Grayscale difference threshold")
    args = parser.parse_args()
    
    temp_clean = 'temp_clean'
    temp_adaptive = 'temp_adaptive'
    temp_seq = 'temp_seq'
    
    for d in [temp_clean, temp_adaptive, temp_seq]:
        os.makedirs(d, exist_ok=True)
        
    # 1. Giải nén video cover sạch
    subprocess.run([
        'ffmpeg', '-y', '-i', args.input,
        os.path.join(temp_clean, 'frame_%04d.png')
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    frames = sorted([f for f in os.listdir(temp_clean) if f.endswith('.png')])
    num_frames = len(frames)
    
    if num_frames == 0:
        print("[!] Không thể giải nén video.")
        sys.exit(1)
        
    # Copy sang các thư mục để xử lý
    for idx, f_name in enumerate(frames):
        src = os.path.join(temp_clean, f_name)
        dst_clean = os.path.join(temp_clean, f"frame_{idx:04d}.png")
        if src != dst_clean:
            os.rename(src, dst_clean)
            
        shutil.copy(dst_clean, os.path.join(temp_adaptive, f"frame_{idx:04d}.png"))
        shutil.copy(dst_clean, os.path.join(temp_seq, f"frame_{idx:04d}.png"))
        
    # 2. Phát hiện chuyển cảnh
    scene_changes = detect_scene_changes(temp_clean, num_frames, args.threshold)
    
    if scene_changes is None:
        scene_changes = []
        
    print(f"[+] Phát hiện {len(scene_changes)} khung hình chuyển cảnh: {scene_changes}")
    
    # 3. Thực hiện nhúng Adaptive LSB
    message_bits = get_message_bits(args.message)
    adaptive_modified = []
    for sc in scene_changes:
        frame_path = os.path.join(temp_adaptive, f"frame_{sc:04d}.png")
        embed_bits_to_frame(frame_path, message_bits)
        adaptive_modified.append(sc)
        
    # 4. Thực hiện nhúng Sequential LSB
    # Nhúng tuần tự từ frame 0 trở đi
    seq_modified = [0]
    embed_bits_to_frame(os.path.join(temp_seq, "frame_0000.png"), message_bits)
    
    # 5. Đánh giá so sánh chất lượng hình ảnh (PSNR) và thống kê (Entropy)
    # Tính PSNR trung bình của các frame bị sửa đổi ở Adaptive
    adaptive_psnrs = []
    adaptive_entropies = []
    for frame_idx in adaptive_modified:
        clean_path = os.path.join(temp_clean, f"frame_{frame_idx:04d}.png")
        stego_path = os.path.join(temp_adaptive, f"frame_{frame_idx:04d}.png")
        
        psnr = calculate_psnr(clean_path, stego_path)
        entropy = analyze_lsb_entropy(stego_path)
        
        if psnr is not None:
            adaptive_psnrs.append(psnr)
        if entropy is not None:
            adaptive_entropies.append(entropy)
        
    avg_adaptive_psnr = sum(adaptive_psnrs) / len(adaptive_psnrs) if adaptive_psnrs else 100.0
    avg_adaptive_entropy = sum(adaptive_entropies) / len(adaptive_entropies) if adaptive_entropies else 0.0
    
    # Tính PSNR trung bình của các frame bị sửa đổi ở Sequential
    seq_psnrs = []
    seq_entropies = []
    for frame_idx in seq_modified:
        clean_path = os.path.join(temp_clean, f"frame_{frame_idx:04d}.png")
        stego_path = os.path.join(temp_seq, f"frame_{frame_idx:04d}.png")
        
        psnr = calculate_psnr(clean_path, stego_path)
        entropy = analyze_lsb_entropy(stego_path)
        
        if psnr is not None:
            seq_psnrs.append(psnr)
        if entropy is not None:
            seq_entropies.append(entropy)
        
    avg_seq_psnr = sum(seq_psnrs) / len(seq_psnrs) if seq_psnrs else 100.0
    avg_seq_entropy = sum(seq_entropies) / len(seq_entropies) if seq_entropies else 0.0
    
    # 6. Đóng gói video đầu ra
    subprocess.run([
        'ffmpeg', '-y', '-framerate', '30',
        '-i', os.path.join(temp_adaptive, 'frame_%04d.png'),
        '-c:v', 'libx264rgb', '-crf', '0', 'video_adaptive.mp4'
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    subprocess.run([
        'ffmpeg', '-y', '-framerate', '30',
        '-i', os.path.join(temp_seq, 'frame_%04d.png'),
        '-c:v', 'libx264rgb', '-crf', '0', 'video_sequential.mp4'
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    # Dọn dẹp các thư mục tạm
    for d in [temp_clean, temp_adaptive, temp_seq]:
        shutil.rmtree(d)
        
    # Ghi báo cáo kết quả
    with open(args.output, 'w', encoding='utf-8') as f:
        f.write("=== PHÂN TÍCH SO SÁNH GIẤU TIN CHUYỂN CẢNH ===\n")
        f.write(f"VIDEO GỐC: {os.path.basename(args.input)}\n")
        f.write(f"ĐỘ DÀI TIN NHÚNG (BITS): {len(message_bits)}\n")
        f.write("\n")
        f.write("1. PHƯƠNG PHÁP THÍCH ỨNG (ADAPTIVE LSB):\n")
        f.write(f"   - Các khung hình bị sửa đổi: {','.join(map(str, adaptive_modified))}\n")
        f.write(f"   - PSNR trung bình (dB): {avg_adaptive_psnr:.4f}\n")
        f.write(f"   - Shannon Entropy trung bình: {avg_adaptive_entropy:.6f}\n")
        f.write("\n")
        f.write("2. PHƯƠNG PHÁP TUẦN TỰ (SEQUENTIAL LSB):\n")
        f.write(f"   - Các khung hình bị sửa đổi: {','.join(map(str, seq_modified))}\n")
        f.write(f"   - PSNR trung bình (dB): {avg_seq_psnr:.4f}\n")
        f.write(f"   - Shannon Entropy trung bình: {avg_seq_entropy:.6f}\n")
        
    print(f"[+] Báo cáo đối sánh đã được lưu tại {args.output}")

if __name__ == '__main__':
    main()
