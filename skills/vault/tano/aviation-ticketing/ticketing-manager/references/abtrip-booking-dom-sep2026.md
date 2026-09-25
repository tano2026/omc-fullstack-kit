# abtrip.vn Booking Flow — DOM Structure (Verified 20/06/2026)

> Tham khảo cho `book_flight` trong `abtrip_browser.py`
> Verified by: Playwright debug experiment trên VPS ubuntu@43.156.72.127

## 1. URL-Based Search (No Form Interaction Needed)

abtrip.vn supports query-param navigation. Kết quả hiển thị trực tiếp:

```
https://abtrip.vn/flight?adults=1&children=0&infants=0&tripType=one-way&segments[0][startPoint]=SGN&segments[0][endPoint]=PQC&segments[0][departDate]=15072026
```

**Field mapping:**
| Query param | Mô tả | Ví dụ |
|------------|-------|-------|
| `adults` | Số người lớn | 1 |
| `children` | Số trẻ em | 0 |
| `infants` | Số em bé | 0 |
| `tripType` | Loại vé | one-way |
| `segments[0][startPoint]` | Mã sân bay đi (IATA) | SGN |
| `segments[0][endPoint]` | Mã sân bay đến (IATA) | PQC |
| `segments[0][departDate]` | Ngày đi (DDMMYYYY) | 15072026 |

## 2. Page Render Timing (Next.js SSR)

Cần đợi SSR hoàn tất:

```python
loaded = False
for i in range(10):
    await page.wait_for_timeout(3000)
    body = await page.inner_text("body")
    if "Có " in body and " chuyến bay" in body:
        loaded = True
        break
```

**Signal:** `Có N chuyến bay` — typically loads at 3-6 seconds.

## 3. Flight Card DOM Structure

Card `div.air-item` trong `div.air-options`:

```
div.air-options
  └── div.air-item
        ├── div.flight-present
        │     ├── div.flight-sum
        │     │     ├── div.airline-logo
        │     │     │     ├── <img>
        │     │     │     └── <span.flight-num>VN1829</span>
        │     │     └── ...
        │     └── div.flight-action-select
        │           └── div.action-button
        │                 ├── <span>Chọn</span>  ← not a <button>!
        │                 └── <span>»</span>
        └── ...
```

**Key:** "Chọn" là `<SPAN>` — `querySelectorAll('button')` trả về 0.

## 4. Click "Chọn" Code

```python
clicked = await page.evaluate("""(fn) => {
    const items = document.querySelectorAll("div.air-item");
    for (const item of items) {
        if (item.innerText.includes(fn)) {
            const spans = item.querySelectorAll("span");
            for (const s of spans) {
                if (s.innerText.trim() === "Chọn") {
                    s.click();
                    return true;
                }
            }
        }
    }
    return false;
}""", flight_number)
```

## 5. Passenger Form Fields

| input `name` | Label | Type |
|-------------|-------|------|
| `passengers.adults.0.firstName` | Họ (không dấu) | text |
| `passengers.adults.0.lastName` | Tên đệm và tên (không dấu) | text |
| `passengers.adults.0.gender` | Giới tính | radio (click <label>) |
| `passengers.adults.0.dob` | Ngày sinh | text (dd/mm/yyyy) |
| `contact.name` | Họ và tên | text |
| `contact.phone` | Số điện thoại | tel |
| `contact.email` | Email | text |

**Gender:** Click `label:has(input[name="passengers.adults.0.gender"])`.

## 6. Submit Button

```
<BUTTON.ant-btn.action-button.action>
  <SPAN>Đặt vé</SPAN>
</BUTTON>
```

Selector: `button:has(span:text("Đặt vé"))`.

## 7. Flow Summary

```
Navigate URL params → wait 3-9s render
  → find div.air-item + flight_number
  → click span "Chọn" via evaluate()
  → wait 5s for form
  → fill firstName/lastName/gender/dob/contact.*
  → wait 2s
  → find button "Đặt vé" → scroll + click
  → return success
```

## 8. Pitfalls

- **flight_value** là pipe-delimited `VN1833|SGN|PQC|...|1728000` — cần `.split("|")[0]`
- **"Chọn"** là SPAN, không phải button
- **Gender** click label, không click input
- **DOB** cần `dd/mm/yyyy`, convert từ `YYYY-MM-DD`
