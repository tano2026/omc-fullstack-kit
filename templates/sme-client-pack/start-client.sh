#!/bin/bash
echo "======================================================================"
echo "   🏢 ĐANG KHỞI ĐỘNG HỆ ĐIỀU HÀNH NHÂN VIÊN AI 24/7"
echo "   Bao gồm 5 Nhân sự AI: CSKH 24/7 + Video/Social + Soi Đối Thủ + Thư Ký CEO"
echo "======================================================================"
which xdg-open > /dev/null && xdg-open http://localhost:19888 || open http://localhost:19888 2>/dev/null || true
python3 gateway/webhook_server.py
