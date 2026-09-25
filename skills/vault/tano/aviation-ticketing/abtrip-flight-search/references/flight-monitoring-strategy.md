# Flight Monitoring Strategy — Seat & Price Watcher

## Kiến trúc 2 bộ (user requested split)

### Bộ 1: API Watcher (`watcher_api/`)
- **File**: `watcher_api/api_checker.py` + `watcher_api/checker_manager.py`
- **Cơ chế**: Gọi API B2B `POST /v1/Flight/SearchFlight` mỗi 10p
- **Tốc độ**: 2-3s mỗi lần
- **Check**:
  - `Availability` > 0 (còn ghế)
  - `TotalFare` ≤ ngưỡng user set
  - `Unavailable` == false
- **Output**: trigger Scraper nếu đạt điều kiện
- **Lưu queue**: JSON files trong `watchers/` dir

### Bộ 2: Scraper Playwright (`watcher_scraper/`)
- **File**: `watcher_scraper/scraper_booker.py` + `watcher_scraper/scraper_manager.py`
- **Cơ chế**: Dùng `abtrip_browser.book_flight()` 1 lần duy nhất
- **Tốc độ**: 30-60s (khởi động browser)
- **Output**: PNR + booking link
- **Không dùng để poll** — chỉ gọi 1 lần khi API báo đạt

### Đường biên: không trộn lẫn 2 bộ
- API Watcher = check nhanh, chạy background
- Scraper = book thật, chỉ khi trigger
- Không dùng Playwright để poll — quá chậm + dễ bị anti-bot detect

## Polling interval — ⚠️ QUAN TRỌNG

Hãng bay **phạt nếu check quá dày** (tội tấn công hệ thống). User preference:

- **Mặc định: 10 phút** — an toàn tuyệt đối
- **Tối thiểu: 5 phút** — chỉ khi canh chỗ gấp (1-2 ghế)
- **Không < 5 phút** — bị block IP
- Configurable: field `interval_minutes` trong watcher JSON

## API B2B Payload format (BẮT BUỘC đúng format)

```json
{
  "System": "VN",
  "Adt": 1,
  "Chd": 0,
  "Inf": 0,
  "ListRoute": [{
    "Leg": 0,
    "StartPoint": "HAN",
    "EndPoint": "SGN",
    "DepartDate": "30062026"
  }],
  "RequestInfo": {
    "PrivateKey": "a3f2b9e1c8d4a7f6b2e0c9d5a4b1f8d32",
    "ApiAccount": "ABTRIP",
    "ApiPassword": "CtTXgjVX8AQ1"
  }
}
```

Headers: `Content-Type: application/json`

**⚠️ Không dùng format `{StartPoint, EndPoint, DepartureDate, Account, Password}`** — format đó gây 400 Bad Request. Dùng format `{System, Adt, Chd, Inf, ListRoute, RequestInfo}` như trên.

## Watcher web UI

Tích hợp trong Flask web app `flight-booking-webapp/app.py`:

```
GET  /api/watcher/list      → danh sách watcher đang chạy
POST /api/watcher/create    → tạo watcher mới (JSON body)
POST /api/watcher/delete/<id> → xoá 1 watcher
GET  /api/watcher/status    → trạng thái worker (chạy/dừng)
```

Frontend tại `templates/index.html` có 2 tab:
- **Đặt vé**: chat interface tìm kiếm + đặt
- **Theo dõi**: form tạo watcher + danh sách watcher + nút delete

Watcher form fields: `from, to, date, flight_code, mode (price|availability), max_price, interval_minutes, note`

## Flow canh chỗ

### User input
```
Chuyến: VJ120 HAN→SGN 30/06/2026
Hành khách: Nguyễn Văn A, Nam, 20/10/1990, 0984190918, a@example.com
Ngưỡng: giá ≤ 1,500,000₫ (hoặc "auto" nếu hết chỗ)
Mode: price | availability
Interval: 10 phút
```

### Background worker
```
1. Mỗi interval: đọc watchers/ dir
2. Với mỗi watcher:
   a. Gọi API SearchFlight với payload format đúng
   b. Parse response (ListGroup → ListAirOption → ListFareOption → TotalFare + Availability)
   c. Nếu mode=price: check TotalFare ≤ max_price
   d. Nếu mode=availability: check Availability > 0
   e. Đạt → gọi scraper_booker.book() với passenger info
   f. Book xong → gửi Telegram, xóa watcher khỏi queue
   g. Chưa đạt → log + chờ lần sau
```

### Telegram notification mẫu
```
━━━━━━━━━━
╔══════════════════════════╗
║ ⏰ **CANH CHỖ THÀNH CÔNG** ║
║                          ║
║  HAN **→** SGN           ║
║  06:30→08:30             ║
║  **30/06/2026**           ║
║                          ║
║  Vietjet — **VJ120**     ║
║  Giá: **1,200,000₫**     ║
║                          ║
║  **PNR: XYZ123**         ║
║  Link: abtrip.vn/...     ║
║                          ║
║  ⚠️ Vé cũ VJ120 giá      ║
║  2,500,000₫ chưa hủy     ║
║  Muốn hủy ko?            ║
╚══════════════════════════╝
━━━━━━━━━━
```

## Lưu ý quan trọng

1. **API B2B không bị anti-bot** — abtrip.vn detect Playwright headless, nhưng API B2B không bị block.
2. **Payload format sai sẽ bị 400** — dùng format ListRoute + RequestInfo, không dùng StartPoint/EndPoint flat.
3. **Availability là int thật** — đã verify: các fare khác nhau trả Availability khác nhau (4,5,6,8,9).
4. **Không hủy vé cũ trước khi đặt mới** — luôn đặt song song. Chỉ hủy sau khi có PNR mới.
5. **Watcher chạy trên web app** — Flask background thread, không cần cron riêng. Khi Flask restart → worker khởi động lại.
6. **Multiple watchers** — mỗi watcher 1 file JSON. Có thể chạy nhiều watcher cùng lúc với interval khác nhau.
7. **Không dùng Playwright để poll** — chỉ dùng API B2B. Playwright chỉ để book.
