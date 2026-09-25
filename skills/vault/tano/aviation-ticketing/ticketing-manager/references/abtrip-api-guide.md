# Hướng dẫn Tích hợp & Kiểm thử ABTrip API (B2B/B2C)

Tài liệu này ghi lại toàn bộ thông số kỹ thuật, endpoint, quy tắc xác thực và các lỗi/ràng buộc đặc thù được phát hiện trong quá trình kiểm thử hệ thống API của ABTrip.

## 1. Thông tin Kết nối & Xác thực (Auth Info)
*   **Base URL (Test):** `https://api-abtrip.timtrungtam.com/v1`
*   **Tham số xác thực:** Toàn bộ request gọi đến các hàm nghiệp vụ đều yêu cầu truyền kèm thông tin tài khoản đại lý bên trong thuộc tính `RequestInfo` của body:
    ```json
    "RequestInfo": {
        "PrivateKey": "a3f2b9e1c8d4a7f6b2e0c9d5a4b1f8d32",
        "ApiAccount": "ABTRIP",
        "ApiPassword": "CtTXgjVX8AQ1"
    }
    ```

---

## 2. Danh sách Endpoints quan trọng (Case-Sensitive!)
**LƯU Ý ĐẶC BIỆT:** Hệ thống backend NestJS phân biệt chữ hoa/chữ thường (Case-sensitive) đối với đường dẫn. Nếu viết sai định dạng viết hoa, hệ thống sẽ trả về lỗi `404 Not Found`.

| Chức năng | Phương thức | Endpoint đúng |
| :--- | :--- | :--- |
| Tra cứu danh sách hãng bay | POST | `/v1/Flight/GetAirlines` |
| Tìm kiếm chuyến bay | POST | `/v1/Flight/SearchFlight` |
| Đặt giữ chỗ (Book) | POST | `/v1/Flight/BookFlight` |
| Kiểm tra đơn hàng (Retrieve) | POST | `/v1/Flight/RetrieveBooking` |
| Xuất vé (Issue) | POST | `/v1/Flight/IssueTicket` |

---

## 3. Ràng buộc & Cạm bẫy đặc thù trên Hệ Test (Pitfalls)

### A. Ràng buộc về Ngày bay (Departure Date Limit)
*   **Hiện tượng:** Khi thực hiện Đặt chỗ (`BookFlight`) với ngày cất cánh trong tương lai (ví dụ: `16062026` hay `20062026`), hệ thống core test của sandbox sẽ trả về lỗi **HTTP 500 Internal Server Error**.
*   **Nguyên nhân:** Sandbox test của hệ thống chỉ hỗ trợ tính toán và giữ chỗ đối với các chuyến bay cất cánh trong **ngày hiện tại (CURRENT/TODAY'S date)**.
*   **Giải pháp:** Để kiểm thử luồng đặt giữ chỗ thành công trên môi trường test, bắt buộc phải đổi ngày cất cánh trong payload tìm kiếm về ngày hôm nay (ví dụ: ngày chạy test hiện tại là `28052026`).

### B. Giới hạn Đặt chỗ Multi-leg (Open-Jaw / Nhiều chặng độc lập)
*   **Hiện tượng:** Thực hiện tìm kiếm 2 chặng cùng lúc (Leg 0: HAN-SGN và Leg 1: VCA-HAN) trong một cuộc gọi `/Flight/SearchFlight` thành công lấy được `Session`. Nhưng khi truyền cả 2 lựa chọn chặng vào mảng `ListAirOption` của hàm `/Flight/BookFlight`, hệ thống báo lỗi 500: `Cannot set properties of undefined (setting 'IssueTicket')`.
*   **Giải pháp:** 
    *   Hệ thống test không hỗ trợ gộp 2 chặng bay hở độc lập (open-jaw) vào chung một đơn đặt chỗ qua API.
    *   **Quy trình chuẩn:** Tách thành **2 chu kỳ Search & Book độc lập**. Mỗi chu kỳ tự tìm kiếm chặng đơn, lấy Session riêng và gọi hàm đặt chỗ riêng để tạo ra 2 đơn hàng giữ chỗ (`BookingCode`) riêng biệt.

### C. Cấu trúc ListAirOption bắt buộc có System
*   Khi gọi `/Flight/BookFlight`, mỗi phần tử trong mảng `ListAirOption` bắt buộc phải có thuộc tính `"System"` (giá trị: `"VN"`, `"QH"`, `"VJ"`, hoặc `"1A"`), nếu không hệ thống sẽ trả về lỗi `HTTP 400 Bad Request` with thông báo: `ListAirOption.0.System is required`.

### D. Tránh Timeout / Chậm trễ khi chạy Test Tìm kiếm (SearchFlight)
*   **Hiện tượng:** Gọi `/Flight/SearchFlight` với `"System": "VN"` (Vietnam Airlines kết nối qua GDS Amadeus Sandbox) có thể phản hồi rất chậm (>15 giây) hoặc bị lỗi timeout do đường kết nối test GDS chập chờn.
*   **Giải pháp:**
    1.  Để test nhanh luồng API Search & Book, hãy đổi sang dùng `"System": "VJ"` (VietJet) hoặc `"System": "QH"` (Bamboo Airways) - các hãng này xử lý trực tiếp trên Core Sandbox nên phản hồi gần như lập tức (<2 giây).
    2.  Để kiểm thử nhanh tính xác thực của thông tin kết nối (`RequestInfo`), hãy ưu tiên gọi endpoint `/Flight/GetAirlines`. Đây là endpoint nhẹ, không quét chuyến bay thực tế nên phản hồi cực nhanh (HTTP 201 Created) giúp cô lập nhanh lỗi mạng hoặc sai thông tin đăng nhập.

