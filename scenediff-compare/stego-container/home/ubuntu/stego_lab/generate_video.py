import os
import math
import subprocess
from PIL import Image, ImageDraw

def generate_base_frames(width, height, num_frames):
    frames_dir = 'temp_raw_frames'
    os.makedirs(frames_dir, exist_ok=True)
    
    for i in range(num_frames):
        # Thiết lập các scene change đột ngột
        if 0 <= i < 30:
            bg_color = (0, 0, 240)      # Cảnh 1: Xanh dương
        elif 30 <= i < 60:
            bg_color = (240, 0, 0)      # Cảnh 2: Đỏ (Scene change tại frame 30)
        elif 60 <= i < 90:
            bg_color = (0, 240, 0)      # Cảnh 3: Xanh lá (Scene change tại frame 60)
        else:
            bg_color = (240, 240, 0)    # Cảnh 4: Vàng (Scene change tại frame 90)
            
        img = Image.new('RGB', (width, height), bg_color)
        draw = ImageDraw.Draw(img)
        
        # Vật thể chuyển động tuần hoàn
        cx = int(width / 2 + 80 * math.cos(2 * math.pi * i / 60))
        cy = int(height / 2 + 60 * math.sin(2 * math.pi * i / 60))
        draw.ellipse([cx - 15, cy - 15, cx + 15, cy + 15], fill=(255, 255, 255))
        
        img.save(os.path.join(frames_dir, f"frame_{i:04d}.png"))
    return frames_dir

def build_video_from_frames(frames_dir, output_path):
    subprocess.run([
        'ffmpeg', '-y',
        '-framerate', '30',
        '-i', os.path.join(frames_dir, 'frame_%04d.png'),
        '-c:v', 'libx264rgb', '-crf', '0',
        output_path
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def generate():
    width, height = 320, 240
    num_frames = 120
    
    print("[*] Đang khởi tạo các khung hình cơ sở cho video mẫu...")
    raw_dir = generate_base_frames(width, height, num_frames)
    
    print("[*] Đang đóng gói video đầu vào: input_video.mp4...")
    build_video_from_frames(raw_dir, 'input_video.mp4')
    
    # Dọn dẹp
    for f in os.listdir(raw_dir):
        os.remove(os.path.join(raw_dir, f))
    os.rmdir(raw_dir)
    print("[+] Sinh video input_video.mp4 thành công!")

if __name__ == '__main__':
    generate()
