# abtrip.vn DOM Structure — June 2026

Vertical: Next.js + Ant Design (React). SPA with SSR fallback.

## Key Discovery: "Chọn" buttons are `<SPAN>`, NOT `<button>`

`querySelectorAll('button')` returns 0 results on the flight results page.
All "Chọn" elements are `<SPAN>` inside `<DIV class="action-button">`.

## Flight Results Page Structure

```
DIV.air-options                          ← container for all flights
  DIV.air-item                           ← one per flight
    DIV.flight-present
      DIV.flight-sum                     ← horizontal flex row
        DIV.airline-logo                 ← left: logo + flight number
          IMG (airline logo)
          SPAN.flight-num                ← text node = "VN1829"
        ... (departure/arrival time, duration)
        DIV.flight-action-select         ← right: price + select button
          (price text)
          DIV.action-button
            SPAN → "Chọn"               ← THIS IS THE BUTTON
            SPAN → "»"
```

## Correct Selector Strategy

```javascript
// Method 1: find div.air-item containing flight number, then find "Chọn" span
const items = document.querySelectorAll('div.air-item');
for (const item of items) {
    if (item.innerText.includes(flightNumber)) {
        const spans = item.querySelectorAll('span');
        for (const s of spans) {
            if (s.innerText.trim() === 'Chọn') {
                s.click();
                return true;
            }
        }
    }
}
```

## Passenger Form (after clicking "Chọn")

All inputs use `input[name="..."]` selectors:

| Field | name attribute | placeholder |
|-------|---------------|-------------|
| First name (Họ) | `passengers.adults.0.firstName` | "Nhập họ" |
| Last name (Tên đệm và tên) | `passengers.adults.0.lastName` | "Nhập tên đệm và tên" |
| Gender (radio) | `passengers.adults.0.gender` | — |
| DOB | `passengers.adults.0.dob` | "dd/mm/yyyy" |
| Contact name | `contact.name` | "Nhập họ và tên" |
| Phone | `contact.phone` | "Nhập số điện thoại" |
| Email | `contact.email` | "Nhập email" |

### Gender Selection

Must click the **label** wrapping the radio input, not the radio itself:
```python
glabels = await page.query_selector_all('label:has(input[name="passengers.adults.0.gender"])')
for gl in glabels:
    t = (await gl.inner_text()).strip().lower()
    if t == gender_wanted:
        await gl.click()
```

2 radio buttons: Nam (index 0), Nữ (index 1).

### Submit Button

`<BUTTON class="ant-btn ... action-button action"><SPAN>Đặt vé</SPAN></BUTTON>`

Selector: `button:has(span:text("Đặt vé"))`

## URL-based Search

Works: `https://abtrip.vn/flight?adults=1&children=0&infants=0&tripType=one-way&segments[0][startPoint]=SGN&segments[0][endPoint]=PQC&segments[0][departDate]=15072026`

URL params are parsed by the Next.js app. No need to interact with the search form.

Wait ~3-9s for SSR + client-side hydration. Check for "Có X chuyến bay" text to confirm loaded.

## Timing (VPS)

- Page load: 3-9s (Next.js SSR)
- Form appearance after click: ~3-5s
- Form fill + submit: ~2s
- Total book flow: ~30-60s

## Verified Booking (test_book3.py)

SGN→PQC, VN1829, 15/07/2026 → `{"success": true, "message": "Đã gửi yêu cầu đặt vé."}`
