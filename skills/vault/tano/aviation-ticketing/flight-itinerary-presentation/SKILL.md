---
name: flight-itinerary-presentation
category: aviation-ticketing
description: Hướng dẫn trình bày hành trình bay (Itinerary) dưới dạng bảng ASCII/Unicode hoặc định dạng khối trực quan, giúp phòng vé gửi báo giá cho khách duyệt cực kỳ chuyên nghiệp và dễ hiểu.
---

# Kỹ năng Trình bày Hành trình Bay (Flight Itinerary Presentation)

Mục tiêu chính là biến các dòng lệnh GDS thô hoặc danh sách chuyến bay lộn xộn thành một bản đề xuất (Proposal) chuyên nghiệp, dễ đọc trên cả máy tính lẫn điện thoại di động (không bị vỡ khung).

## 1. Nguyên tắc thiết kế Itinerary cho khách hàng
*   **Chia nhóm rõ ràng:** Luôn tách biệt **Chiều đi (Outbound Options)**, **Các chặng giữa/nội địa (Fixed Segments)**, và **Chiều về (Inbound Options)**.
*   **Múi giờ:** Ghi rõ "Giờ địa phương" để khách tránh nhầm lẫn về thời gian transit.
*   **Thời gian Transit:** Bôi đậm thời gian chờ tại các sân bay trung chuyển để khách chuẩn bị tâm lý (đặc biệt nhắc nhở nếu thời gian transit quá ngắn hoặc quá dài).
*   **Hành lý & Hạng vé:** Luôn đính kèm thông tin hành lý ký gửi (ví dụ: 23kg, 2P...) và dòng máy vận hành nếu có.

## 2. Định dạng bảng ASCII Monospace chuẩn di động

> ⚠️ **CẢNH BÁO:** Format bảng ASCII này chỉ dùng trên **Email/Zalo/Web**. **Telegram KHÔNG hỗ trợ table syntax** — pipe tables (`|`) và ASCII box (`+---+`) bị vỡ. Khi output trên Telegram, dùng **mục 3a** bên dưới.

Để bảng hiển thị đẹp mắt và không bị vỡ trên màn hình điện thoại di động hẹp, sử dụng định dạng bảng ASCII có độ rộng tối ưu (khoảng 50-60 ký tự):

```text
=====================================================
 Chặng | Số hiệu | Hành trình | Giờ bay   | Ngày bay 
-------+---------+------------+-----------+----------
 Đi    | SU 293  | SGN - SVO  | 10:45-17:05| 27/06    
 (SU)  | SU 1470 | SVO - SVX  | 23:35-04:05| 27/06    
=====================================================
```

## 3. Định dạng Khối (Row-group Block) thay thế cho Mobile
Nếu bảng ASCII quá dài, hãy dùng định dạng Khối (mô phỏng bảng bằng Emojis và thụt lề):

✈️ **CHIỀU ĐI (Ngày 27/06) — OPTION 1: HÃNG AEROFLOT (SU)**
*   `SU 293` | **SGN ➔ SVO** | **10:45 - 17:05** *(Bay thẳng 10h 20m)*
*   *Transit tại Moscow (SVO): 6 tiếng 30 phút (Thoải mái làm thủ tục nhập cảnh)*
*   `SU 1470`| **SVO ➔ SVX** | **23:35 - 04:05** *(Hạ cánh ngày 28/06)*

## 3a. Định dạng Telegram — Bullet List Compact (bắt buộc dùng trên Telegram)

Telegram **KHÔNG hỗ trợ table syntax**. Khi trình bày nhiều chuyến bay trên Telegram, dùng format này.

**⚠️ Lưu ý chi phí:** User (Nobitano) rất nhạy cảm với token cost. Ưu tiên lightweight approach (curl, web_extract) hơn browser tools. Browser = last resort.

### Nhiều chuyến (danh sách option) — Format Compact:

━━━━━━━━━━━━━━━━
**{Đi} → {Đến} | {ngày/tháng}**

🟢 **{Hãng}**
　{chuyến} · {giờ}→{giờ} · **{giá}k**
　{chuyến} · {giờ}→{giờ} · {giá}k

🔴 **{Hãng}**
　{chuyến} · {giờ}→{giờ} · {giá}k

💡 **Rẻ:** {chuyến} — {giá}k
━━━━━━━━━━━━━━━━

Ví dụ:

━━━━━━━━━━━━━━━━
**SGN → PQC | 29/06**

🟢 **Bamboo**
　QH192 · 06:30→08:00 · **1.125k**
　QH194 · 11:55→13:30 · 1.125k

🔴 **Vietjet**
　VJ323 · 06:00→07:30 · 1.489k
　VJ325 · 12:00→13:30 · 1.489k
　VJ321 · 15:15→16:45 · 1.851k

💡 **Rẻ:** QH192 — 1.125k
━━━━━━━━━━━━━━━━

**Quy tắc trình bày (tuyệt đối tuân thủ):**
- **Dòng đầu:** `**{Đi} → {Đến} | {ngày/tháng}**` — route + ngày rút gọn (2 số, ko năm)
- **Header mỗi nhóm hãng:** emoji + **tên hãng ngắn** — `🟢 **Bamboo**` (KO ghi mã VJ, KO ghi Airways/Airlines, KO ghi thời gian bay)
- **Mỗi chuyến:** `　{chuyến} · {giờ}→{giờ} · **{giá}k**`
  - Dùng `·` (middle dot) separator
  - Giá rút gọn: `1.125k`, `2.056k` — KO ghi `₫` hay `VND`
  - **Bold** giá rẻ nhất toàn route
  - Thụt đầu dòng (fullwidth space 　)
  - Ghi `+1` nếu qua ngày hôm sau
- **Sort trong mỗi hãng:** theo giá tăng dần
- **Sort hãng:** Bamboo → Vietjet → VNA → Pacific → Vietravel
- **Cuối:** `💡 **Rẻ:** {chuyến} — {giá}k`
- **Dùng `━━━━━━━━━━━━━━━━`** line đầu + cuối
- **KO** có giải thích thêm, KO có cảnh báo, KO có thông tin phụ
- Emoji: 🟢 Bamboo, 🔴 Vietjet, 🔵 VNA, 🟠 Pacific, 🟡 Vietravel

### 1 chuyến (xác nhận booking) — Style Ticket Card:

━━━━━━━━━━
╔══════════════════════════╗
║ ✈️ **ABTRIP**            ║
║ **ĐẶT VÉ THÀNH CÔNG**   ║
║                          ║
║  {Đi} **→** {Đến}       ║
║  {giờ}→{giờ}             ║
║  **{ngày/tháng}**        ║
║                          ║
║  {Hãng} — **{chuyến}**   ║
║                          ║
║  **{PNR}**               ║
║  **{giá}₫**              ║
║                          ║
║  ⏳ {status}             ║
╚══════════════════════════╝
━━━━━━━━━━

Ví dụ:

━━━━━━━━━━
╔══════════════════════════╗
║ ✈️ **ABTRIP**            ║
║ **ĐẶT VÉ THÀNH CÔNG**   ║
║                          ║
║  SGN **→** HAN           ║
║  14:25→16:25             ║
║  **15/06**               ║
║                          ║
║  Vietjet — **VJ120**     ║
║                          ║
║  **PYVEP8**              ║
║  **1.754.000₫**          ║
║                          ║
║  ⏳ Giữ chờ              ║
╚══════════════════════════╝
━━━━━━━━━━

**Quy tắc:**
- Hãng viết ngắn (Bamboo, Vietjet, VNA, Vietravel)
- `{Hãng} — **{chuyến}**`
- Giá `₫`, format `.`: `1.754.000₫`
- Ngày/tháng 2 số: `15/06`
- PNR bold
- Thêm `🧳 {baggage}` nếu có, `Check in [tại đây]({url})` cuối

## 4. Mẫu tin nhắn xác nhận Đặt vé / Vé điện tử gửi cho Khách hàng (ABTRIP)

Để khách hàng đọc phát hiểu ngay thông tin vé trên màn hình điện thoại di động, sử dụng cấu trúc khối tối ưu tích hợp trường VIP, số thẻ Khách hàng thường xuyên (FFP Card), ghi chú hành lý và lưu ý riêng.

### 4a. Mẫu nhắn tin cho khách hàng cuối (B2C):
```text
✈️ ABTRIP - Vé máy bay của Anh/Chị:
---------------------------------
• Mã đặt vé: [MÃ_PNR]
• Khách bay:
  1. [Họ_Tên_1] - [👑 VIP] [💳 Thẻ: Số_thẻ_1]
  2. [Họ_Tên_2] - [👑 VIP] [💳 Thẻ: Số_thẻ_2]
• Chặng: [Nơi_đi] - [Nơi_đến] ([Số_hiệu_bay])
• Giờ bay: [Giờ_bay] - Ngày [Ngày_bay]
• Hành lý: XT [X_kg] + KG [Y_kg] (mỗi khách)
• Ghi chú: [Nội_dung_Note...]

Hotline hỗ trợ 24/7: 0788 320 320.
```

### 4b. Mẫu booking confirmation nội bộ (ABTRIP — simplified format)

Dùng khi báo kết quả đặt vé cho quản lý / chủ phòng vé / đồng nghiệp.

**Cấu trúc chuẩn (chỉ hiển thị trường CÓ dữ liệu, trường rỗng bỏ qua):**

```text
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ DAT VE THANH CONG
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Ma dat cho: [BookingCode]

Ten khach: [HO VA TEN] (in hoa, không dấu)

Hanh trinh: [ThanhPho (MaSB)] → [ThanhPho (MaSB)]
*Ga di: [MaSB - TenGa] → Ga den: [MaSB - TenGa]*

Ngay bay: [DD/MM/YYYY]
Gio bay: [GioDi] → [GioDen] · Bay thang · [ThoiGianBay]
Hang: [MaHang]

Gia: [SoTien]d
Hanh ly ky gui: [SoKg]kg

Trang thai: ⏳ Giu cho — chua thanh toan

Zalo: [SoDienThoai]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Hotline: [SoHotline]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

**Trường có điều kiện (chỉ hiển thị nếu có dữ liệu):**
- Mã đơn hàng — từ payment page (`.info-booking-id`)
- Hạn xuất vé + Thông tin CK → chỉ khi chưa xuất
- Số vé → chỉ khi đã xuất (`.ticketIssued`)
- Số thẻ (PNR hãng) + VIP → chỉ khi có
- Số ghế → chỉ khi có

**Quy tắc format bắt buộc:**

1. **Tên khách:** KHÔNG dấu tiếng Việt. VD: `TAN NGUYEN NGOC` (viết HOA)
2. **Sân bay:** Viết tên thành phố + mã. VD: `Nha Trang (CXR)` — kèm nhà ga cho sân bay có nhiều terminal (CXR: Ga nội địa/Ga QT, HAN: T1/T2, SGN: T1/T2, DAD: T1/T2)
3. **Giờ bay:** Luôn kèm cả giờ đi & giờ đến. Format: `19:05 → 21:05`
4. **Chỉ hiển thị trường có dữ liệu** — trường trống KHÔNG xuất hiện trong message
5. **Dùng `━━━` lines** phân cách section
6. **Bôi đậm** label chính
7. **Trạng thái:** ⏳ giữ chờ / ✅ đã xuất
8. **Liên hệ:** ghi `Zalo:` + SĐT (bỏ email trong confirmation)
9. **Giọng văn:** người thật, dứt khoát, không bot
10. **Hỏi thẳng:** "Cần thanh toán luôn không?" — không vòng vo

**Terminal mapping (sân bay có nhiều ga, chú ý domestic vs international):**

| Airport | Domestic | International |
|---------|----------|--------------|
| Nội Bài (HAN) | T1 | T2 |
| Cam Ranh (CXR) | Ga nội địa | Ga quốc tế |
| Tân Sơn Nhất (SGN) | T1 | T2 |
| Đà Nẵng (DAD) | T1 | T2 |

**Baggage mặc định cho VNA nội địa:**
- PT (Promotion, PT LH): **20kg**
- TG (Business): 30kg

**Nguồn dữ liệu (từ booking.abtrip.vn payment page):**

| Trường | Vị trí trên trang |
|--------|-------------------|
| Mã đơn hàng | `.info-booking-id` → `Mã đơn hàng: ABT8xxxx` |
| Mã đặt chỗ | URL path `/flight/payment/{BookingCode}` + form field `bookingId` |
| Tên khách | `.info-customer` → `TAN NGUYEN NGOC` |
| Hành trình | `.goAirLine` / `.desAirLine` → tên sân bay + mã |
| Ngày bay | `.goAirLine` → `31/05/2026` |
| Giờ bay | `.goAirLine` / `.desAirLine` → `19:05` / `21:05` |
| Hạng chỗ | `.infoAirLine` → `Hạng chỗ: B` |
| Máy bay | `.infoAirLine` → `Airbus A321-100/200` |
| Tổng tiền | `.total-price` → `3.821.000` |
| Thông tin CK | `.collapseCardLocal` → MB Bank, STK 699990505, CTY ABTRIP, CN Hai Bà Trưng |
| Hotline | `.tel-call` → `0868.320.320` |

Xem chi tiết field mapping và payment page structure tại [references/abtrip-booking-confirmation.md](references/abtrip-booking-confirmation.md).

## 5. Các thông tin bổ sung bắt buộc khi làm phương án bay
*   **Transit details:** Nhập cảnh lấy đồ hay gửi thẳng.
*   **Recommendation:** Đưa ra đánh giá chuyên môn để khách dễ chọn (Lựa chọn nào khỏe nhất, rẻ nhất, đẹp nhất).

## 6. HTML Web Table Format (ABTrip AI Agent Demo)

> Dùng khi làm trang demo web / kết quả search trên web app cho phòng vé.
> KHÔNG dùng trên Telegram — dùng mục 3a.

### Nguyên tắc (từ user preference đã sửa 2 lần):

1. **Sắp xếp theo hãng bay, không theo giờ** — group riêng từng hãng (VJ, BL, QH, VN, VU, 9G)
2. **Bỏ cột thời gian bay** (2h00, 1h30) — trên bảng kết quả chỉ cần: Số hiệu | Giờ | Giá
3. **Mã chuyến sạch — không trùng mã hãng** — `VJ407` đúng, `VJVJ407` sai
4. **HTML table real `<table>`** — có `<thead>` với column headers, từng airline block riêng
5. **Nút "Copy bảng"** — text copy format cũng theo hãng, không duration

### Cấu trúc HTML table:

```html
<div class="airline-block">
  <div class="airline-title">🔴 Vietjet</div>
  <span class="airline-subprice">từ 1.250.000₫</span>
  <table>
    <thead>
      <tr><th>Số hiệu</th><th>Giờ</th><th>Giá (VND)</th><th></th></tr>
    </thead>
    <tbody>
      <tr><td>VJ407</td><td>07:30→09:30</td><td>1.250.000₫</td><td></td></tr>
      <tr><td>VJ635</td><td>12:30→14:30</td><td>1.350.000₫</td><td></td></tr>
    </tbody>
  </table>
</div>
```

### Thứ tự airline (chuẩn):

| Thứ tự | Mã | Emoji | Tên |
|--------|-----|-------|-----|
| 1 | VJ | 🔴 | Vietjet |
| 2 | BL | 🟠 | Pacific |
| 3 | QH | 🟢 | Bamboo |
| 4 | VN | 🔵 | VNA |
| 5 | VU | 🟡 | Vietravel |
| 6 | 9G | 🟣 | Sun PhuQuoc |

### Copy text format (plaintext cho phòng vé gửi Zalo/Telegram):

```text
✈️ SGN → HAN | 05/07/2026 | 👥 2 người lớn
──────────────────────────────────────────────────
[🔴 Vietjet]
  VJ407    07:30→09:30  1.250.000₫
  VJ635    12:30→14:30  1.350.000₫
──────────────────────────────────────────────────
[🟠 Pacific]
  BL391    10:00→12:00  1.150.000₫
  BL197    21:00→23:00  1.090.000₫  ★
──────────────────────────────────────────────────
Tổng thấp nhất: 2.180.000₫ (2 người lớn)
```

**★ = badge "Rẻ nhất"**, chỉ gắn cho 1 chuyến rẻ nhất toàn route.

### Single flight card format (khi click chọn 1 chuyến):

```
┌─────────────────────────────────────┐
│  VJ407      🔴 Vietjet              │
│                                     │
│  07:30 → 09:30                      │
│  ✈️ Bay thẳng  🧳 Theo hạng vé      │
│                                     │
│  👉 Gõ "đặt VJ407" để đặt vé        │
│  • Click để copy                    │
└─────────────────────────────────────┘
```

- Flight code + hãng (emoji + tên ngắn) trên cùng
- Giá to bên phải
- Không duration
- Copy hint + action hint ở cuối
- Click toàn bộ card → copy text: `{code} {depart}→{arrive} {price}`

### Suggestion chips dưới kết quả:

- **Chuyến rẻ nhất** → scroll đến chuyến có badge ★
- **Chuyến sớm nhất** → chuyến khởi hành sớm nhất
- **Bay thẳng** → direct flights
- **Đổi ngày bay** → reset search
- (Sau khi chọn 1 chuyến): **Đặt vé này**, **Chuyến sớm nhất**, **Bay thẳng**, **Tìm tuyến khác**

### UX details:

- **Màu nền mỗi dòng đan xen** airline-color tinted (opacity thấp)
- **Row cursor pointer** — có thể click để chọn
- **Hover highlight** — highlight khi rê chuột
- **Summary box** cuối cùng: `👥 Hành khách: 2 người lớn | Tổng thấp nhất: 2.180.000₫`
- **Toast notification** khi copy: `✅ Đã copy!` (auto-fade 1.8s)
- **Avatar bot** ✈️ trước mỗi tin nhắn

### Triển khai JavaScript (pattern):

```javascript
// Group flights by airline
const airlines = {};
allFlights.forEach(f => {
  if (!airlines[f.airline]) airlines[f.airline] = [];
  airlines[f.airline].push(f);
});

// Build airline blocks
airlineOrder.forEach(al => {
  const flights = airlines[al];
  if (!flights || !flights.length) return;
  html += `<div class="airline-block">`;
  html += `<div class="airline-title">${emoji} ${name}</div>`;
  html += `<table><thead><tr><th>Số hiệu</th><th>Giờ</th><th>Giá</th></tr></thead><tbody>`;
  flights.forEach(f => {
    html += `<tr><td>${f.code}</td><td>${f.depart}→${f.arrive}</td><td>${f.price}</td></tr>`;
  });
  html += `</tbody></table></div>`;
});
```

### Pitfalls:

- **Quên sắp xếp theo hãng** — user từng sửa: "sắp xếp theo hãng dc ko" (session 06/07/2026)
- **Để trùng mã hãng trong code** — `VJVJ407` làm user khó chịu. Luôn kiểm tra data trước khi render
- **Để cột duration trong table** — user: "bỏ cái cột thời gian bay 2h00 đi" — trên bảng kết quả, duration ko cần. Chỉ để trong single flight card hoặc omit completely
- **Màu hồng/magenta** — user ghét, ko dùng làm màu accent
- **Dùng pipe tables | trên Telegram** — vỡ format. Telegram chỉ bullet list (mục 3a)

**⚠️ Web app implementation drifted from these rules (22 Jul 2026):** On the ABTrip web chat (`agent.tkt` project, `chat.html`), a later session replaced HTML `<table>` card rendering with a plain-text monospace table inside a copyable code box (fixes "quá thanh/quá hẹp, muốn copy được" complaints), but that fix sorted by **price** again and kept the **duration column** — reverting §6's airline-grouping and no-duration rules. If asked to fix ABTrip's web flight table again, apply §6's content rules (group by airline, drop duration, sort ascending within airline) on top of the copy-box + monospace-font mechanic documented in `abtrip-dev` skill's Flight Results Format section — don't rebuild the copy mechanic from scratch.

## 7. Pitfalls (Bẫy cần tránh — tổng hợp)

*   **⚠️ ABTRIP B2B API = TEST DATA, KHÔNG PHẢI GIÁ THẬT:** API `api-abtrip.timtrungtam.com/v1/` là sandbox. Giá từ `SearchFlight`/`BookFlight` là mock — **cấm dùng để báo giá khách**. Chỉ dùng API để test luồng. Giá thật phải lấy từ web abtrip.vn (browser/curl) hoặc Google Flights hoặc GDS terminal. Phân biệt rõ: `mcp_flight_search_flight` = API (test data), `mcp_flight_search_flight_web` = web scraping (giá thật).

*   **Lỗi gửi file Telegram khi đường dẫn có khoảng trắng:** Khi gửi file đính kèm bằng cú pháp `MEDIA:<path>` qua Telegram, nếu đường dẫn thư mục có dấu cách (khoảng trắng - ví dụ: `D:\\AI Store\\...`), parser của hệ thống sẽ bị lỗi chia chuỗi và báo không tìm thấy file. 
    *   *Cách khắc phục:* Luôn sao chép hoặc tạo file ở đường dẫn tuyệt đối hoàn toàn không có khoảng trắng (ví dụ: `D:\\Phuong_An_Bay_2026.xlsx`) trước khi gọi lệnh gửi file.
*   **Telegram KHÔNG support table syntax:** Không dùng pipe tables (`|`) hay ASCII box drawing (`+---+`) trên Telegram. Dùng bullet list format ở mục 3a.
*   **Giới hạn quyền hạ cánh của hãng hàng không (Bilateral Air Services Agreement):** Tuyệt đối tránh các lỗi sơ đẳng về đường bay do hạn chế pháp lý. Ví dụ: **Emirates (EK) không có quyền bay đến Berlin (BER)**, họ chỉ được phép khai thác 4 sân bay tại Đức (FRA, MUC, DUS, HAM). Nếu bay từ BER về, phải tư vấn chặng nối chuyến qua hãng khác như Turkish Airlines (TK) hay Qatar Airways (QR), hoặc chặng nội địa châu Âu nối chuyến ra các Hub của EK.
