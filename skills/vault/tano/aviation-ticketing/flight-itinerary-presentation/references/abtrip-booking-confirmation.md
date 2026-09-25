# ABTRIP Booking Confirmation — Field Mapping

Nguồn: booking.abtrip.vn payment page (Laravel, HTTP)

## URL Pattern
```
GET /flight/payment/{bookingCode}
GET /flight/book?session={sessionId}&departFlightId={id}
POST /flight/postBook (form-urlencoded)
```

## Booking Page (GET /flight/book)

| Field | HTML Name | Notes |
|-------|-----------|-------|
| First Name | `FirstName[]` | Value only (no label) |
| Last Name | `LastName[]` | Value only (no label) |
| Gender | `Gender[ADT1]` | `true` = Male |
| ID Card | `IdCard[]` | CCCD number |
| Passport | `PassportNumber[]` | Empty if using CCCD |
| Day | `Day[]` | Hidden, set via select2 datepicker |
| Month | `Month[]` | Hidden, set via select2 datepicker |
| Year | `Year[]` | Hidden, set via select2 datepicker |
| Passenger Type | `Type[]` | ADT, CHD, INF |
| Baggage | `BaggageDepart[]` | Select dropdown, 0 = no baggage |
| Contact FirstName | `ContactInfo[FirstName]` | |
| Contact LastName | `ContactInfo[LastName]` | |
| Contact Phone | `ContactInfo[Phone]` | |
| Contact Email | `ContactInfo[Email]` | |
| Session | `session` | From search URL |
| Depart Flight ID | `departFlightId` | Integer, from search results |
| Fare Data ID | `fareDataId` | Empty string if not specified |
| CSRF Token | `_token` | Must be fresh + cookies preserved |

## PostBook Response
```json
{"status":1,"bookingId":"157DUVj7"}
```
- `status: 1` → cần thanh toán (redirect /flight/payment)
- `status: 3` → auto-issue (đã xuất vé tự động)

## Payment Page (GET /flight/payment/{bookingId})

### Order Info (`.info-booking-id`)
- **Mã đơn hàng:** `ABT80057` format (ABT + 5 digits)
- **Khách hàng:** `TAN NGUYEN NGOC` (all caps, no accents)
- **Email:** `Tan@anbinhairlines.vn`
- **Phone:** `0788320320`

### Flight Info (`.info-flight`)
- **Hãng:** VN (Vietnam Airlines)
- **Số hiệu:** VN1562
- **Hành trình:** Cam Ranh (CXR) → Nội Bài (HAN)
- **Ngày:** 31/05/2026
- **Giờ đi:** 19:05 (`time_in`)
- **Giờ đến:** 21:05 (`time_out`)
- **Thời gian bay:** 2h00m
- **Hạng chỗ:** B (PT LH - Economy Light)
- **Máy bay:** Airbus A321
- **Số vé:** (trống nếu chưa xuất)

### Payment Methods (`.option-payment-radio`)
| Value | Method | How it works |
|-------|--------|-------------|
| 3 | Thẻ nội địa | Redirect to ATM/Internet Banking |
| 5 | Visa/Master | Redirect + fee 2.75% (105.078đ on 3.821.000đ) |
| 1 | Hình thức chuyển khoản | Show bank account info |
| (various) | Appota/MoMo/VNPT/ShopeePay | Currently commented out in HTML |

### Bank Transfer Info (`.collapseCardLocal`)
- **Ngân hàng:** TMCP Quân Đội (MB Bank)
- **Tên tài khoản:** CÔNG TY TNHH THƯƠNG MẠI DU LỊCH VÀ DỊCH VỤ HÀNG KHÔNG ABTRIP
- **Số tài khoản:** 699990505
- **Chi nhánh:** Hai Bà Trưng - Hà Nội
- **QR Code:** `/images/icon/mb_qr.jpg`

### Contact Info
- **Hotline:** 0868.320.320
- **Sân bay:** 0868.320.320
- **Trụ sở:** Số 6 ngõ 113, đường Ngọc Thụy, Tổ 1, Ngọc Thụy, Long Biên, Hà Nội
- **VP:** Số 6 ngõ 113, đường Ngọc Thụy, Tổ 1, Ngọc Thụy, Long Biên, Hà Nội
- **CN Sân bay:** Tầng 3 nhà Ga T2, sân bay Quốc tế Nội Bài, Hà Nội

## Date Format CẢNH BÁO 

`departDate` format CHANGED from `DD/MM/YYYY` to `DD-MM-YYYY` (dấu gạch ngang, không phải dấu gạch chéo). Nếu dùng sai format, search trả về HTML với date `01/01/1970` và thông báo "Không tìm thấy chuyến bay".

```bash
# Sai format  date = 01/01/1970, no results:
departDate=31/05/2026

# Đúng format  date = 31/05/2026, full results:
departDate=31-05-2026
```

## Terminal / NHÀ GA mapping

| Sân bay | Nội địa | Quốc tế |
|---------|---------|---------|
| Nội Bài (HAN) | T1 | T2 |
| Cam Ranh (CXR) | Ga nội địa | Ga quốc tế |
| Tân Sơn Nhất (SGN) | T1 | T2 |
| Đà Nẵng (DAD) | T1 | T2 |

**Ghi rõ ga trong Hanh trinh khi báo booking  khách đi nhầm ga là vỡ mồm.**

## Baggage mặc định VNA nội địa

| Hạng | Hành lý ký gửi |
|------|---------------|
| PT (Promotion) | 20kg |
| TG (Business) | 30kg |

## curl Booking Workflow (complete example)

```bash
# 1. Search flights (dùng DD-MM-YYYY)
curl -s "http://booking.abtrip.vn/flight/ajaxSearch?startPoint=CXR&endPoint=HAN&itinerary=oneway&departDate=31-05-2026&adt=1&chd=0&inf=0" > search.html

# 2. Get booking page (save cookies)
curl -s -c cookies.txt "http://booking.abtrip.vn/flight/book?session={SESSION_ID}&departFlightId={FLIGHT_ID}" > book.html
TOKEN=$(grep -oP '_token.*?value="\K[^"]+' book.html)

# 3. Submit booking
curl -s -b cookies.txt -X POST "http://booking.abtrip.vn/flight/postBook" \
  -d "_token=$TOKEN" \
  -d "session={SESSION_ID}" \
  -d "departFlightId={FLIGHT_ID}" \
  -d "fareDataId=" \
  -d "FirstName[]=Tan" \
  -d "LastName[]=Nguyen Ngoc" \
  -d "Gender[ADT1]=true" \
  -d "IdCard[]=01983839920" \
  -d "PassportNumber[]=" \
  -d "Day[]=1" -d "Month[]=5" -d "Year[]=1984" \
  -d "Type[]=ADT" \
  -d "BaggageDepart[]=0" \
  -d "ContactInfo[FirstName]=Tan" \
  -d "ContactInfo[LastName]=Nguyen Ngoc" \
  -d "ContactInfo[Phone]=0788320320" \
  -d "ContactInfo[Email]=Tan@anbinhairlines.vn" \
  -d "btnSubmitBooking="
```

## Notes
- Session ID format: `DC9683{CXR}{HAN}{DDMMYY}{random}-DTC099`
- departFlightId corresponds to `<tr rel="flight{N}">` in search HTML
- Price per passenger is in `priceDepart{N}` attribute (e.g., `priceDepart6="3821000"`)
- CSRF token + cookies must be from the SAME request to book page
- Day/Month/Year fields are hidden; values come from select2 datepicker
