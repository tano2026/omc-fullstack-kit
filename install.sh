#!/usr/bin/env bash
set -e

echo "======================================================================"
echo "   🏭 BỘ CÀI ĐẶT TỰ ĐỘNG OMC FULLSTACK MASTER KIT (LINUX / VPS)"
echo "   Bao gồm: Quad-Engine (DSH + Hermes + OpenClaw 2.0 + JEV) + Obsidian"
echo "======================================================================"
echo ""

# 1. Update OS & Cài đặt công cụ nền tảng
echo "[1/5] Cài đặt công cụ hệ thống (Python3, pip, curl, git)..."
if command -v apt-get &> /dev/null; then
    sudo apt-get update -qq
    sudo apt-get install -y -qq python3 python3-pip curl git > /dev/null
fi

# 2. Cài đặt Node.js 20+ nếu chưa có
echo "[2/5] Kiểm tra và cài đặt Node.js LTS..."
if ! command -v node &> /dev/null; then
    echo "[*] Đang cài đặt Node.js qua NodeSource..."
    curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash - > /dev/null
    sudo apt-get install -y -qq nodejs > /dev/null
fi
node --version
npm --version

# 3. Cài đặt thư viện Python
echo "[3/5] Cài đặt Python requirements..."
pip3 install -r requirements.txt --quiet --break-system-packages 2>/dev/null || pip3 install -r requirements.txt --quiet

# 4. Cài đặt OpenClaw 2.0
echo "[4/5] Kiểm tra và cài đặt OpenClaw 2.0 Engine..."
if ! command -v openclaw &> /dev/null; then
    echo "[*] Đang cài đặt OpenClaw 2.0 toàn cục (npm install -g openclaw)..."
    sudo npm install -g openclaw@latest
fi
openclaw --version || true

# 5. Khởi tạo cấu hình .env
echo "[5/5] Thiết lập file cấu hình môi trường..."
if [ ! -f "config/.env" ]; then
    cp config/.env.example config/.env
    echo "[OK] Đã tạo file config/.env từ template."
fi

chmod +x start.sh copilot.sh 2>/dev/null || true

echo ""
echo "======================================================================"
echo "   🎉 CÀI ĐẶT HOÀN TẤT THÀNH CÔNG TRÊN LINUX / VPS!"
echo "======================================================================"
echo ""
echo " Các bước vận hành tiếp theo:"
echo "   1. Chạy './copilot.sh' để trò chuyện trực tiếp với Hermes Master"
echo "   2. Chạy './start.sh' để khởi động Gateway 24/7"
echo "   3. Chạy 'python3 clone_company.py --name \"Ten\" --domain \"Nganh\"' để nhân bản công ty"
echo ""
