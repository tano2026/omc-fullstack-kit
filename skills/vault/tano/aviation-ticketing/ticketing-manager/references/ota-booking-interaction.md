# Kỹ thuật Tự động hóa & Tương tác với Website Đặt vé (OTA)

Tài liệu này tổng hợp các giải pháp xử lý DOM và kỹ thuật vượt qua hạn chế giao diện khi thực hiện tra cứu vé máy bay tự động trên các website đại lý (OTA) phổ biến như ABTRIP, và các hệ thống đặt chỗ tương tự.

## 1. Vượt qua Hạn chế của Ô nhập ngày (Readonly Datepicker Bypass)
Hầu hết các website OTA sử dụng thư viện Datepicker (như Flatpickr, jQuery UI Datepicker) và đặt thuộc tính `readonly="readonly"` trên ô input để ngăn người dùng gõ tay. Khi tự động hóa bằng trình duyệt:
*   **Vấn đề:** Trình duyệt không thể nhập liệu trực tiếp bằng hành động gõ phím (`browser_type`). Việc click mở lịch và chọn ngày bằng giao diện trực quan rất dễ lỗi và chậm do cấu trúc HTML của bảng lịch thay đổi liên tục.
*   **Giải pháp (Javascript Injection):**
    1. Xóa thuộc tính `readonly`.
    2. Gán giá trị ngày mới đúng định dạng mong muốn.
    3. Phát lệnh kích hoạt sự kiện `input` và `change` để mã JS phía dưới của website nhận diện và lưu trạng thái mới.

### Đoạn Code Thực thi (Sử dụng Console):
```javascript
(() => {
  const el = document.getElementById("date_di"); // Hoặc class selector phù hợp
  if (el) {
    el.removeAttribute("readonly");
    el.value = "02/06/2026"; // Gán ngày mong muốn
    el.dispatchEvent(new Event("input", { bubbles: true }));
    el.dispatchEvent(new Event("change", { bubbles: true }));
    return "Thành công thiết lập ngày: " + el.value;
  }
  return "Không tìm thấy ô nhập ngày";
})()
```

---

## 2. Tương tác với Hộp tìm kiếm Điểm đi/Điểm đến (Autocomplete & Dropdown Selection)
Nhiều OTA sử dụng cơ chế Autocomplete. Khi gõ mã sân bay (ví dụ: `DAD`), ô nhập liệu sẽ kích hoạt một danh sách gợi ý đổ xuống (dropdown) và bắt buộc người dùng phải click vào một item cụ thể để hệ thống ghi nhận giá trị sân bay và mã IATA vào form ẩn.
*   **Vấn đề:** If chỉ đặt `value = "DAD"` trên input, khi nhấn tìm kiếm hệ thống sẽ báo lỗi hoặc tự động reset về điểm đến mặc định do sự kiện chọn item chưa được kích hoạt.
*   **Giải pháp chuẩn:**
    1. Click vào ô điểm đi hoặc điểm đến công cộng để kích hoạt hộp chọn dropdown.
    2. Xác định class của các phần tử gợi ý (ví dụ: `.item-diem-di`, `.item-diem-den`, hoặc sảnh danh sách).
    3. Tìm phần tử chứa tên thành phố mong muốn (ví dụ: "Đà Nẵng") và thực hiện hành động `click()` thông qua Javascript để mô phỏng chính xác hành vi của khách hàng.

### Đoạn Code Thực thi mẫu:
```javascript
(() => {
  // 1. Click mở hộp chọn điểm đến
  document.querySelector(".bt-diem-den").click();
  
  // 2. Tìm và click chọn item Đà Nẵng
  const el = Array.from(document.querySelectorAll(".item-diem-den"))
                  .find(x => x.innerText.includes("Đà Nẵng"));
  if (el) {
    el.click();
    return "Đã click chọn điểm đến Đà Nẵng";
  }
  return "Không tìm thấy lựa chọn điểm đến";
})()
```

---

## 3. Xử lý Lỗi Kết nối & Dự phòng Domain (Subdomain Fallback Strategy)
Khi truy cập một trang tra cứu cụ thể (ví dụ: `booking.abtrip.vn`) mà gặp lỗi kết nối (như `502 Proxy Error`, Timeout, hoặc Server down):
*   **SOP xử lý:**
    1. Kiểm tra ngay phản hồi tiêu đề HTTP của domain gốc bằng `curl -sI https://abtrip.vn` hoặc dùng trình duyệt truy cập thẳng trang chủ.
    2. Rất nhiều hệ thống OTA tích hợp widget tìm kiếm vé máy bay trực tiếp ngay tại trang chủ (`abtrip.vn`).
    3. Nếu trang chủ hoạt động, hãy tận dụng widget này để thiết lập form tìm kiếm, hệ thống sẽ tự động xử lý và chuyển tiếp sang luồng kết quả chuẩn của backend.

---

## 4. Xử lý Lỗi Giữ Chỗ Sát Giờ & Phương Thức Thanh Toán Đi kèm (Hold Failures & Bank Transfer Booking Bypass)
Khi đặt vé chặng bay sát giờ hoặc bay trong ngày (Same-day departure) thường gặp dòng cảnh báo "Vé không thể giữ chỗ, cần thanh toán ngay".
*   **Vấn đề:** Nếu chọn hình thức "THANH TOÁN SAU" (Pay Later / Book now pay later), server của đại lý (như abtrip.vn) có thể trả về lỗi `500 Server Error` (tại endpoint `/flight/postPayment`) do hệ thống GDS/hãng từ chối tạo PNR giữ chỗ không thanh toán cho chuyến bay trong ngày.
*   **Giải pháp (Workaround):**
    1. Sử dụng lệnh `browser_back` để quay lại trang Payment trước đó.
    2. Giữ nguyên lựa chọn **"THANH TOÁN NGAY"**.
    3. Chọn phương thức thanh toán **"Thẻ nội địa"** (hoặc ATM nội địa). Trên hệ thống abtrip.vn, khi tích chọn mục này, giao diện sẽ tải động bảng hướng dẫn chuyển khoản ngân hàng thủ công (ví dụ: MB Bank - Số tài khoản 699990505) thay vì chuyển tiếp sang cổng thanh toán trực tuyến.
    4. Gõ nội dung ghi chú nếu cần và thực hiện submit form qua JS:
       ```javascript
       document.querySelector('form').submit();
       ```
    5. Trang web sẽ chuyển sang trạng thái "HOÀN TẤT" thành công, cung cấp Mã đơn hàng cụ thể (ví dụ: `ABTxxxxx`) và chi tiết tài khoản thụ hưởng để chuyển khoản thủ công mà không gặp lỗi server.
