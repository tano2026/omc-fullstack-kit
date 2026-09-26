@echo off
chcp 65001 >nul
echo =====================================================================
echo 🔄 OMC FULLSTACK MASTER AUTO-UPDATE (CẬP NHẬT 1-CLICK)
echo =====================================================================
echo.
echo Đang kiểm tra và đồng bộ bản cập nhật mới nhất từ GitHub...
echo.

git --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ⚠️ Không tìm thấy Git trên máy.
    pause
    exit /b 1
)

git pull origin main
if %errorlevel% equ 0 (
    echo.
    echo ✅ CẬP NHẬT THÀNH CÔNG! Dữ liệu Obsidian và tri thức được bảo toàn.
) else (
    echo.
    echo ⚠️ Cập nhật không thành công. Vui lòng kiểm tra kết nối mạng.
)

echo.
pause
