#!/bin/bash
# checkwork.sh - Script tu dong cham diem tai cho cho sinh vien (100 diem)

SCORE_ADAPTIVE=0
SCORE_SEQUENTIAL=0
SCORE_PSNR=0
SCORE_REPORT=0

echo "=================================================================="
echo "          BAT DAU QUA TRINH GIAM DINH & CHAM DIEM TU DONG"
echo "=================================================================="
echo ""

# 1. Kiem tra xem ma nguon compare.py co ton tai khong
if [ ! -f "compare.py" ]; then
    echo "[!] LOI: Khong tim thay file compare.py cua sinh vien!"
    exit 1
fi

# 2. Xoa cac video va bao cao cu truoc khi kiem tra
rm -f video_adaptive.mp4 video_sequential.mp4 comparison_report.txt

# 3. Chay compare.py cua sinh vien de tao ra ket qua
echo "[*] Dang chay compare.py cua sinh vien de nhung tin..."
python3 compare.py -i input_video.mp4 -m "BI_MAT_QUOC_GIA_PTIT_2026" -o comparison_report.txt -t 10.0 > /dev/null 2>&1

if [ ! -f "video_adaptive.mp4" ] || [ ! -f "video_sequential.mp4" ] || [ ! -f "comparison_report.txt" ]; then
    echo "[-] KHONG DAT: Sinh vien chua tao ra video_adaptive.mp4, video_sequential.mp4 hoac comparison_report.txt!"
else
    # 4. Kiem tra ti le nhung Adaptive (30 diem)
    # Giai nen cac frame de kiem tra
    mkdir -p check_clean check_adaptive check_seq
    ffmpeg -y -i input_video.mp4 check_clean/frame_%04d.png > /dev/null 2>&1
    ffmpeg -y -i video_adaptive.mp4 check_adaptive/frame_%04d.png > /dev/null 2>&1
    ffmpeg -y -i video_sequential.mp4 check_seq/frame_%04d.png > /dev/null 2>&1

    # Dem su khac biet cac frame o Adaptive
    # Chi co cac frame chuyen canh 30 va 60 la duoc phep khac biet
    ADAPTIVE_CORRECT=1
    for i in {0..119}; do
        idx_str=$(printf "%04d" $i)
        diff_val=$(cmp -s check_clean/frame_${idx_str}.png check_adaptive/frame_${idx_str}.png; echo $?)
        
        if [ $i -eq 30 ] || [ $i -eq 60 ]; then
            # Frame 30 va 60 BAT BUOC phai khac biet (do co nhung)
            if [ $diff_val -eq 0 ]; then
                ADAPTIVE_CORRECT=0
            fi
        else
            # Cac frame khac BAT BUOC phai giong het nhau (khong duoc nhung)
            if [ $diff_val -ne 0 ]; then
                ADAPTIVE_CORRECT=0
            fi
        fi
    done

    if [ $ADAPTIVE_CORRECT -eq 1 ]; then
        echo "[+] DAT: Nhung Adaptive chinh xac chi o cac khung hinh chuyen canh. (+30 diem)"
        SCORE_ADAPTIVE=30
    else
        echo "[-] KHONG DAT: Nhung Adaptive bi loi (nhung sai khung hinh hoac khong thay doi du lieu)."
    fi

    # 5. Kiem tra ti le nhung Sequential (30 diem)
    # Chi co frame 0 duoc phep khac biet
    SEQ_CORRECT=1
    for i in {0..119}; do
        idx_str=$(printf "%04d" $i)
        diff_val=$(cmp -s check_clean/frame_${idx_str}.png check_seq/frame_${idx_str}.png; echo $?)
        
        if [ $i -eq 0 ]; then
            if [ $diff_val -eq 0 ]; then
                SEQ_CORRECT=0
            fi
        else
            if [ $diff_val -ne 0 ]; then
                SEQ_CORRECT=0
            fi
        fi
    done

    if [ $SEQ_CORRECT -eq 1 ]; then
        echo "[+] DAT: Nhung Sequential chinh xac tu frame 0. (+30 diem)"
        SCORE_SEQUENTIAL=30
    else
        echo "[-] KHONG DAT: Nhung Sequential bi loi (nhung sai khung hinh hoac khong thay doi du lieu)."
    fi

    # 6. Kiem tra chi so PSNR va Entropy (20 diem)
    # Chay file giai cua giao vien de lay gia tri tham chieu
    rm -f ref_report.txt
    python3 solution/compare_sol.py -i input_video.mp4 -m "BI_MAT_QUOC_GIA_PTIT_2026" -o ref_report.txt -t 10.0 > /dev/null 2>&1
    
    # Trich xuat PSNR tu hai file bao cao
    STUDENT_ADAPTIVE_PSNR=$(grep "1. PHUONG PHAP THICH UNG" -A 2 comparison_report.txt | grep "PSNR trung binh" | awk '{print $5}')
    if [ -z "$STUDENT_ADAPTIVE_PSNR" ]; then
        # Thử không có dấu tiếng Việt
        STUDENT_ADAPTIVE_PSNR=$(grep -i "ADAPTIVE" -A 2 comparison_report.txt | grep "PSNR" | awk -F': ' '{print $2}' | tr -d ' dbdB')
    fi
    
    REF_ADAPTIVE_PSNR=$(grep "1. PHUONG PHAP THICH UNG" -A 2 ref_report.txt | grep "PSNR trung binh" | awk '{print $5}')
    if [ -z "$REF_ADAPTIVE_PSNR" ]; then
        REF_ADAPTIVE_PSNR=$(grep -i "ADAPTIVE" -A 2 ref_report.txt | grep "PSNR" | awk -F': ' '{print $2}' | tr -d ' dbdB')
    fi

    # So sanh hai gia tri PSNR (so khop chuoi vi day la float)
    if [ "$STUDENT_ADAPTIVE_PSNR" = "$REF_ADAPTIVE_PSNR" ]; then
        echo "[+] DAT: Tinh toan chinh xac chi so PSNR va Entropy. (+20 diem)"
        SCORE_PSNR=20
    else
        # So sanh cat bot de lay gia tri lam tron gan dung
        STUDENT_ROUNDED=$(echo "$STUDENT_ADAPTIVE_PSNR" | cut -d'.' -f1)
        REF_ROUNDED=$(echo "$REF_ADAPTIVE_PSNR" | cut -d'.' -f1)
        if [ "$STUDENT_ROUNDED" = "$REF_ROUNDED" ] && [ ! -z "$STUDENT_ROUNDED" ]; then
            echo "[+] DAT: Tinh toan chi so PSNR va Entropy (dung sai chap nhan). (+20 diem)"
            SCORE_PSNR=20
        else
            echo "[-] KHONG DAT: Chi so PSNR hoac Entropy tinh toan sai lech qua lon (Hoc vien: $STUDENT_ADAPTIVE_PSNR, Ref: $REF_ADAPTIVE_PSNR)."
        fi
    fi

    # 7. Kiem tra dinh dang file bao cao (20 diem)
    HAS_TITLE=$(grep -q "PHÂN TÍCH SO SÁNH GIẤU TIN CHUYỂN CẢNH" comparison_report.txt; echo $?)
    HAS_ADAPTIVE_SEC=$(grep -q "1. PHƯƠNG PHÁP THÍCH ỨNG" comparison_report.txt; echo $?)
    HAS_SEQ_SEC=$(grep -q "2. PHƯƠNG PHÁP TUẦN TỰ" comparison_report.txt; echo $?)
    
    if [ $HAS_TITLE -eq 0 ] && [ $HAS_ADAPTIVE_SEC -eq 0 ] && [ $HAS_SEQ_SEC -eq 0 ]; then
        echo "[+] DAT: File bao cao comparison_report.txt dung dinh dang yeu cau. (+20 diem)"
        SCORE_REPORT=20
    else
        # Kiem tra khong dau
        HAS_TITLE_ND=$(grep -q "PHAN TICH SO SANH GIAU TIN CHUYEN CANH" comparison_report.txt; echo $?)
        HAS_ADAPT_ND=$(grep -q "1. PHUONG PHAP THICH UNG" comparison_report.txt; echo $?)
        HAS_SEQ_ND=$(grep -q "2. PHUONG PHAP TUAN TU" comparison_report.txt; echo $?)
        if [ $HAS_TITLE_ND -eq 0 ] && [ $HAS_ADAPT_ND -eq 0 ] && [ $HAS_SEQ_ND -eq 0 ]; then
            echo "[+] DAT: File bao cao comparison_report.txt dung dinh dang yeu cau. (+20 diem)"
            SCORE_REPORT=20
        else
            echo "[-] KHONG DAT: Bao cao thieu cac truong thong tin bat buoc."
        fi
    fi

    # Don dep
    rm -rf check_clean check_adaptive check_seq ref_report.txt
fi

SCORE_TOTAL=$((SCORE_ADAPTIVE + SCORE_SEQUENTIAL + SCORE_PSNR + SCORE_REPORT))

mkdir -p /home/ubuntu/.local/result
echo "ADAPTIVE_SCORE=$SCORE_ADAPTIVE" > /home/ubuntu/.local/result/compare.grade
echo "SEQUENTIAL_SCORE=$SCORE_SEQUENTIAL" >> /home/ubuntu/.local/result/compare.grade
echo "PSNR_SCORE=$SCORE_PSNR" >> /home/ubuntu/.local/result/compare.grade
echo "REPORT_SCORE=$SCORE_REPORT" >> /home/ubuntu/.local/result/compare.grade
echo "TOTAL_SCORE=$SCORE_TOTAL" >> /home/ubuntu/.local/result/compare.grade

echo ""
echo "=================================================================="
echo "                 KET QUA DANH GIA (GRADES SUMMARY)"
echo "=================================================================="
echo "  1. Nhung Adaptive LSB:                 $SCORE_ADAPTIVE / 30"
echo "  2. Nhung Sequential LSB:               $SCORE_SEQUENTIAL / 30"
echo "  3. Tinh toan PSNR & Entropy:           $SCORE_PSNR / 20"
echo "  4. Dinh dang bao cao (report):         $SCORE_REPORT / 20"
echo "------------------------------------------------------------------"
echo "  TONG SO DIEM DAT DUOC:                 $SCORE_TOTAL / 100"
echo "=================================================================="
echo "[*] Tang chung cham diem da duoc ghi nhan va truyen ve may Host!"
