# Hướng dẫn Tích hợp & Gọi REST API Hệ thống ABTrip

Tài liệu này tổng hợp cấu trúc, endpoint và các lưu ý kỹ thuật quan trọng khi tương tác với REST API của hệ thống đặt vé máy bay ABTrip (ví dụ trên môi trường test `https://api-abtrip.timtrungtam.com/v1`).

---

## 1. Xác thực & Khung dữ liệu chung (Authentication)
Mọi API Request đến ABTrip đều là phương thức **POST** và yêu cầu truyền thông tin xác thực trực tiếp bên trong body dưới đối tượng `RequestInfo` (không dùng header/bearer token):

```json
{
    "RequestInfo": {
        "PrivateKey": "a3f2b9e1c8d4a7f6b2e0c9d5a4b1f8d32",
        "ApiAccount": "ABTRIP",
        "ApiPassword": "..."
    }
}
```

---

## 2. Các Endpoint Quan trọng (Case-Sensitive)
⚠️ **CỰC KỲ QUAN TRỌNG:** Hệ thống định tuyến (routing) của backend phân biệt chữ hoa/chữ thường (case-sensitive). Việc gọi sai ký tự hoa/thường sẽ trả về lỗi **404 Not Found**.

*   `POST /Flight/SearchFlight` — Tìm kiếm chuyến bay & lấy mã phiên (`Session`).
*   `POST /Flight/GetAncillary` — Lấy danh sách dịch vụ bổ sung (hành lý, phòng chờ...).
*   `POST /Flight/GetSeatMap` — Lấy sơ đồ ghế ngồi.
*   `POST /Flight/GetFareRule` — Lấy điều kiện vé (Fare Rules).
*   `POST /Flight/BookFlight` — Tạo đơn hàng / giữ chỗ.
*   `POST /Flight/RetrieveBooking` — Kiểm tra/truy xuất thông tin booking hiện tại.
*   `POST /Flight/IssueTicket` — Xuất vé máy bay.
*   `POST /Flight/GetAirlines` — Lấy danh sách hãng hàng không hoạt động.

---

## 3. Chi tiết Luồng Tích hợp & Đặt vé (Booking Flow)

### Bước 1: Tìm kiếm chuyến bay (`SearchFlight`)
*   **Request Payload mẫu:**
    ```json
    {
        "RequestInfo": {
            "PrivateKey": "...",
            "ApiAccount": "ABTRIP",
            "ApiPassword": "..."
        },
        "System": "VN", // Có thể là VN, QH, VJ, 1A
        "Adt": 1,
        "Chd": 0,
        "Inf": 0,
        "ListRoute": [
            {
                "Leg": 0,
                "StartPoint": "VCA",
                "EndPoint": "HAN",
                "DepartDate": "28052026" // Định dạng DDMMYYYY
            }
        ]
    }
    ```
    *   *Lưu ý:* `DepartDate` có định dạng `DDMMYYYY`.
*   **Ví dụ gọi API thực tế (Search SGN-HAN cho 1 hành khách VN hôm nay):**
    ```python
    import json
    from hermes_tools import terminal, shell_quote

    api_endpoint = "https://api-abtrip.timtrungtam.com/v1/Flight/SearchFlight"
    private_key = "a3f2b9e1c8d4a7f6b2e0c9d5a4b1f8d32"
    api_account = "ABTRIP"
    api_password = "CtTXgjVX8AQ1"
    
    today_date = "10062026" # Ngày hiện tại, vì sandbox yêu cầu

    payload = {
        "RequestInfo": {
            "PrivateKey": private_key,
            "ApiAccount": api_account,
            "ApiPassword": api_password
        },
        "System": "VN",
        "Adt": 1,
        "Chd": 0,
        "Inf": 0,
        "ListRoute": [
            {
                "Leg": 0,
                "StartPoint": "SGN",
                "EndPoint": "HAN",
                "DepartDate": today_date
            }
        ]
    }

    json_payload = json.dumps(payload)
    quoted_json_payload = shell_quote(json_payload)

    command = f"curl -X POST -H 'Content-Type: application/json' -d {quoted_json_payload} {api_endpoint}"
    print(terminal(command=command))
    ```
*   **Phản hồi:** Trả về đối tượng JSON chứa danh sách chuyến bay kèm theo một mã phiên `Session` quan trọng (ví dụ: `ABT099-e151c133c701866b230ce981007e4e51`). Mã này sẽ dùng để làm đối số cho các bước tiếp theo.

### Bước 2: Đặt chỗ chuyến bay (`BookFlight`)
*   **Ràng buộc tham số:** Trong mảng `ListAirOption`, trường `System` là **BẮT BUỘC** và phải nhận một trong các giá trị sau: `VN`, `QH`, `VJ`, `1A`. Nếu thiếu sẽ bị lỗi `400 Bad Request`.
*   **Request Payload mẫu:**
    ```json
    {
        "RequestInfo": {
            "PrivateKey": "...",
            "ApiAccount": "ABTRIP",
            "ApiPassword": "..."
        },
        "GuestContact": {
            "Title": "Mr",
            "Name": "NGUYEN PHUONG TUAN",
            "Phone": "0788320320",
            "Email": "anbinhticket@gmail.com",
            "Language": "vi",
            "ReceiveEmail": true
        },
        "AgentContact": {
            "Title": "MR",
            "Name": "NGUYEN NGOC TAN",
            "Phone": "0788320320",
            "Email": "anbinhticket@gmail.com",
            "Language": "vi",
            "ReceiveEmail": true
        },
        "ListPassenger": [
            {
                "Index": 1,
                "ParentId": -1,
                "Type": "ADT",
                "Title": "Mr",
                "Gender": 1,
                "GivenName": "PHUONG TUAN",
                "Surname": "NGUYEN",
                "DateOfBirth": "24111981",
                "Passport": {}
            }
        ],
        "ListAirOption": [
            {
                "Session": "ABT099-...",
                "System": "VN",
                "AirlineOptionId": 1,
                "FareOptionId": 5,
                "FlightOptionId": 0
            }
        ]
    }
    ```
*   **Ví dụ gọi API thực tế (Book chuyến bay rẻ nhất từ SGN-HAN của VN hôm nay - VN270, giá 1,824,000 VND):**
    ```python
    import json
    from hermes_tools import terminal, shell_quote

    api_endpoint = "https://api-abtrip.timtrungtam.com/v1/Flight/BookFlight"
    private_key = "a3f2b9e1c8d4a7f6b2e0c9d5a4b1f8d32"
    api_account = "ABTRIP"
    api_password = "CtTXgjVX8AQ1"
    session_id = "ABT099-d3ecac6f649de7e6543f640780a8b717" # Thay bằng Session ID thực tế từ SearchFlight

    payload = {
        "RequestInfo": {
            "PrivateKey": private_key,
            "ApiAccount": api_account,
            "ApiPassword": api_password
        },
        "GuestContact": {
            "Title": "Mr",
            "Name": "NGUYEN NGOC TAN",
            "Phone": "0788320320",
            "Email": "anbinhticket@gmail.com",
            "Language": "vi",
            "ReceiveEmail": True
        },
        "AgentContact": {
            "Title": "MR",
            "Name": "NGUYEN NGOC TAN",
            "Phone": "0788320320",
            "Email": "anbinhticket@gmail.com",
            "Language": "vi",
            "ReceiveEmail": True
        },
        "ListPassenger": [
            {
                "Index": 1,
                "ParentId": -1,
                "Type": "ADT",
                "Title": "Mr",
                "Gender": 1,
                "GivenName": "NGOC TAN",
                "Surname": "NGUYEN",
                "DateOfBirth": "01051984",
                "Passport": {}
            }
        ],
        "ListAirOption": [
            {
                "Session": session_id,
                "System": "VN", # Vietnam Airlines
                "AirlineOptionId": 6, # OptionId của chuyến bay VN270 với giá thấp nhất
                "FareOptionId": 0, # OptionId của hạng vé Phổ thông tiết kiệm
                "FlightOptionId": 0 # always 0 for ListFlightOption
            }
        ]
    }
    
    json_payload = json.dumps(payload)
    quoted_json_payload = shell_quote(json_payload)

    command = f"curl -X POST -H 'Content-Type: application/json' -d {quoted_json_payload} {api_endpoint}"
    print(terminal(command=command))
    ```
*   **Phản hồi thành công:**
    ```json
    {
        "StatusCode": "000",
        "Success": true,
        "Message": "Tạo đơn hàng thành công",
        "BookingId": 118,
        "BookingCode": "ABT00118",
        "TotalPrice": 6284000
    }
    ```

### Bước 3: Truy xuất kiểm tra thông tin (`RetrieveBooking`)
Để kiểm tra trạng thái của đơn hàng đã đặt:
*   **Request Payload mẫu:**
    ```json
    {
        "RequestInfo": {
            "PrivateKey": "...",
            "ApiAccount": "ABTRIP",
            "ApiPassword": "..."
        },
        "BookingCode": "ABT00118"
    }
    ```
