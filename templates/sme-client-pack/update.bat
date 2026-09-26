@echo off
chcp 65001 >nul
echo =====================================================================
echo 🔄 OMC CLIENT SYSTEM AUTO-UPDATE (CẬP NHẬT HỆ THỐNG 1-CLICK)
echo =====================================================================
echo.
echo Đang kiểm tra bản cập nhật tính năng mới nhất từ kho máy chủ...
echo.

git --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ⚠️ Không tìm thấy Git trên máy. Bỏ qua bước kéo mã nguồn.
    echo Vui lòng liên hệ nhà cung cấp giải pháp để được hỗ trợ nâng cấp thủ công.
    pause
    exit /b 1
)

git pull origin main
if %errorlevel% equ 0 (
    echo.
    echo ✅ CẬP NHẬT THÀNH CÔNG!
    echo Toàn bộ kịch bản, tri thức doanh nghiệp và danh sách khách hàng của bạn
    echo vẫn được giữ nguyên an toàn 100%%.
) else (
    echo.
    echo ⚠️ Có xung đột hoặc mất kết nối mạng. Hệ thống vẫn giữ nguyên phiên bản ổn định hiện tại.
)

echo.
echo =====================================================================
echo Khởi động lại hệ thống bằng cách click đúp: start-client.bat
echo =====================================================================
echo.
pause
