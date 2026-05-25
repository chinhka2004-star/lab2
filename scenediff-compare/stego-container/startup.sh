#!/bin/bash
# startup.sh - Tu dong chay khi sinh vien khoi dong container

echo "=================================================================="
echo "    CHAO MUNG DEN VOI BAI THUC HANH: SCENE DIFFERENCE COMPARISON"
echo "=================================================================="
echo ""
echo "[*] Dang tu dong sinh video cover (input_video.mp4)..."
python3 generate_video.py

echo ""
echo "[+] Moi truong thuc hanh da san sang!"
echo "    Hay doc file instructions.txt de biet chi tiet cac nhiem vu:"
echo "    cat instructions.txt"
echo "=================================================================="
