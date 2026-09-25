@echo off
chcp 65001 >nul
title HỆ ĐIỀU HÀNH DOANH NGHIỆP AI 24/7 (SME COMMAND CENTER)
echo ======================================================================
echo    🏢 ĐANG KHỞI ĐỘNG HỆ ĐIỀU HÀNH NHÂN VIÊN AI 24/7
echo    Bao gồm 5 Nhân sự AI: CSKH 24/7 + Video/Social + Soi Đối Thủ + Thư Ký CEO
echo ======================================================================
echo.
echo 👉 Đang mở Bảng Điều Khiển Web Chat: http://localhost:19888
start "" http://localhost:19888
python gateway\webhook_server.py
pause
