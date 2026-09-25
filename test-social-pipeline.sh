#!/bin/bash
echo "======================================================================"
echo "   🚀 KIỂM THỬ QUY TRÌNH RESEARCH, VIDEO TIKTOK & CHATBOT ĐA KÊNH"
echo "======================================================================"
echo ""

echo "[1/3] Kích hoạt Video Script Generator (TikTok / Reels 45s)..."
python3 engines/media/video_script_generator.py --topic "3 Bí Mật Giữ Chân Khách Hàng Cho Spa" --duration 45
echo ""

echo "[2/3] Kích hoạt Chatbot Đa Kênh Zalo, Facebook, TikTok..."
python3 gateway/social_gateway.py
echo ""

echo "[3/3] Kiểm tra bảng lưu trữ Lead trong Obsidian Second Brain..."
cat "obsidian-vault/02 - Projects/CRM-Leads.md"
echo ""
echo "======================================================================"
echo "   🎉 QUY TRÌNH RESEARCH, MEDIA & SOCIAL CHATBOT HOÀN TẤT THÀNH CÔNG!"
echo "======================================================================"
