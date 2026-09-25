# Booking Flow DOM Reference (abtrip.vn)

Updated 20/06/2026 — debugged from live Playwright headless sessions on VPS.

**WARNING: abtrip.vn is a Next.js SPA (Ant Design). DOM structure differs fundamentally from a traditional HTML page.**
**No `<button>` elements for flight selection — the "Chọn" is a `<SPAN>` inside `<DIV>`.**

---

## 1. Search Results Page

URL: `https://abtrip.vn/flight?adults=1&children=0&infants=0&tripType=one-way&segments%5B0%5D%5BstartPoint%5D=SGN&segments%5B0%5D%5BendPoint%5D=PQC&segments%5B0%5D%5BdepartDate%5D=15072026`

> **⚠️ Bypass URL chỉ hoạt động trong Playwright headless (abtrip_browser.py) — live browser bị cắt query params và redirect.**

### Page Load Timing

- Route có ít chuyến (UIH→SGN): ~15-20s
- Route đông (HAN→DAD 45 chuyến): ~30-40s
- Use a loop: `wait_for_timeout(3000)` × up to 10 retries + check for `"Có " in body and " chuyến bay" in body`

### Card Structure (Verified 20/06/2026)

```
DIV.air-options (parent container — has 14 children for 14 flights)
  DIV.air-item (1 flight card)
    DIV.flight-present
      DIV.flight-sum  (flex container with 6 children)
        DIV.airline-logo
          SPAN.flight-num     ← TEXT NODE: "VN1829" (flight number as innerText)
          BR
        ...
      DIV.flight-action-select
        DIV.action-button
          SPAN                ← "Chọn" (NO wrapper with onclick — plain span)
          SPAN                ← "»"
```

### Key Points About Cards

- **Flight number** is a `<SPAN class="flight-num">` with the flight number as its **text node** (e.g., `VN1829`)
- **"Chọn"** is a `<SPAN>` with text `"Chọn"` — **NOT a `<button>` tag**
- There is exactly 1 "Chọn" per card, inside `DIV.action-button > SPAN`
- Cards are identified by traveler: Type A (long-haul) and B (short-haul) are structurally same

**CRITICAL: `document.querySelectorAll('button')` returns ZERO elements on the search results page.**
The entire page uses divs and spans with Ant Design event handlers.

### Selector Strategy for Clicking "Chọn"

```javascript
// ✅ CORRECT — find div.air-item containing flight number, then find SPAN "Chọn"
const items = document.querySelectorAll('div.air-item');
for (const item of items) {
    if (item.innerText.includes('VN1829')) {
        const spans = item.querySelectorAll('span');
        for (const s of spans) {
            if (s.innerText.trim() === 'Chọn') {
                s.scrollIntoView({block: 'center'});
                s.click();
                return true;
            }
        }
    }
}
```

### Page contains 14 flights (from debug output — SGN→PQC, 15/07/2026):

```
VJ331, VJ325, VJ329, VJ339, VJ321, VJ327,
BL6103, VN1835, VN1821, VJ335, VN1829, VN1827, VN1823, VN1825
```

---

## 2. Passenger Form (after clicking "Chọn")

URL stays same (`/flight?...`) — SPA navigation, no page reload. Form appears ~3-5s after click.

### Input Names Verified (20/06/2026)

| Name | Placeholder | Type | Example |
|------|-------------|------|---------|
| `passengers.adults.0.firstName` | Nhập họ | text | `NGUYEN` |
| `passengers.adults.0.lastName` | Nhập tên đệm và tên | text | `NGOC TAN` |
| `passengers.adults.0.gender` | — | radio (2) | index 0=Nam, 1=Nữ |
| `passengers.adults.0.dob` | dd/mm/yyyy | text | `01/01/1990` |
| `contact.name` | Nhập họ và tên | text | `NGUYEN NGOC TAN` |
| `contact.phone` | Nhập số điện thoại | tel | `0904598388` |
| `contact.email` | Nhập email | text | `info@abtrip.vn` |

### Gender Selection

```python
gender_labels = await page.query_selector_all('label:has(input[name="passengers.adults.0.gender"])')
# gender_labels[0] = "Nam", gender_labels[1] = "Nữ"
await gender_labels[0].click()  # Select Nam
```

### Filling form — Playwright code

```python
await page.query_selector_all('input[name="passengers.adults.0.firstName"]')[0].fill("NGUYEN")
await page.query_selector_all('input[name="passengers.adults.0.lastName"]')[0].fill("NGOC TAN")
# gender via label click (not radio input click)
# DOB
await page.query_selector_all('input[name="passengers.adults.0.dob"]')[0].fill("01/01/1990")
# Contact
await page.query_selector_all('input[name="contact.name"]')[0].fill("NGUYEN NGOC TAN")
await page.query_selector_all('input[name="contact.phone"]')[0].fill("0904598388")
await page.query_selector_all('input[name="contact.email"]')[0].fill("info@abtrip.vn")
```

### "Đặt vé" Button

```html
<BUTTON class="ant-btn css-15aulzc ant-btn-default ant-btn-color-default ant-btn-variant-outlined action-button action">
  <SPAN>Đặt vé</SPAN>
</BUTTON>
```

**This IS a `<button>`** — unlike the "Chọn" buttons. Found in `DIV.pay-amount-group`.

```python
# Select strategies:
submit_btn = await page.query_selector('button:has-text("Đặt vé")')
# Or:
all_btns = await page.query_selector_all('button')
for btn in all_btns:
    if "Đặt vé" in await btn.inner_text():
        await btn.scroll_into_view_if_needed()
        await btn.click()
        break
```

---

## 3. Booking Confirmation / Payment Redirect

After clicking "Đặt vé", the SPA navigates to a payment page. The URL may or may not change — in some cases it redirects to `/payment?code=...`.

Check for success indicators:
- `"thanh toán" or "payment" or "redirect"` in body text
- PNR text patterns: 6-char alphanumeric codes

### Verified Booking Result (SGN→HAN, VJ120, 15/06/2026)
```
PNR: PYVEP8
Order: #ABT00349
Time Limit: 02:58 12/06/2026
```

---

## 4. Pitfalls & Lessons

### **4a. `page.evaluate` + f-string = SyntaxError**

**NEVER use f-strings with escaped quotes for JS evaluation:**
```python
# ❌ WRONG — causes "Unexpected token '('"
await page.evaluate(f"""...\"\"\"{{fn}}\\\"\"\"\")""")

# ✅ CORRECT — use parameterized evaluate
js = "(fn) => { document.querySelectorAll('div.air-item') ... }"
await page.evaluate(js, flight_number)
```

### **4b. `querySelectorAll('button')` returns 0 on flight cards**

abtrip.vn uses Ant Design — the "Chọn" button is `<SPAN>`, not `<BUTTON>`. Always use `querySelectorAll('*')` or `querySelectorAll('div.air-item span')` to find clickable elements.

### **4c. Page load vs content load**

- `page.goto()` completes when page DOM loads (70 chars) — not when flights render (1834 chars)
- Must use retry loop with `inner_text("body")` check for `"Có " in body and " chuyến bay" in body`
- 3s × 8 retries = 24s max wait

### **4d. Form validation — Vietjet first name limit**

Vietjet form limits `firstName` (họ) to **10 characters**. If họ + tên đệm exceeds 10 characters, split part of the đệm into `lastName`.

### **4e. No `<button>` in flight select, but `<BUTTON>` exists in form submit**

The form submit button IS a `<BUTTON>` tag. Only the flight card "Chọn" spans are non-button elements.

---

## 5. Debug Scripts (useful for future diagnostics)

For debugging book_flight failures, the following test scripts were created and run on VPS:

| Script | Purpose | File on VPS |
|--------|---------|-------------|
| debug_book.py | Step-by-step page load, flight detection, selector debug | `/tmp/debug_book.py` (overwritten) |
| debug_click.py | Test clicking VN1829, check DOM for button elements | `/tmp/debug_click.py` |
| debug_click2.py | Discover card structure, parent chain, flight number elements | `/tmp/debug_click2.py` |
| debug_click3.py | Fill passenger form, check form fields | `/tmp/debug_click3.py` |
| debug_click4.py | Full flow: click → fill → find submit button | `/tmp/debug_click4.py` |
| test_book.py | Test book_flight() function | `/tmp/test_book.py` |
| test_book2.py | Test book_flight() with new selector | `/tmp/test_book2.py` |

### Debug flow to replicate:

```bash
cd /opt/hermes/ticketing-agent/backend
../venv/bin/python3 /tmp/debug_click4.py  # Tests full flow
```
