# abtrip.vn Booking DOM Structure (June 2026)

Verified from production debugging session (SGN→PQC, VN1829, 15/07/2026).

## Card Structure (Search Results)

```
DIV.air-options
  DIV.air-item                               ← one per flight
    DIV.flight-present
      DIV.flight-sum
        DIV.airline-logo
          SPAN.flight-num                    ← contains flight number as text node (e.g. "VN1829")
        ...
      DIV.flight-action-select
        DIV.action-button
          SPAN "Chọn"                        ← NOT a <button>! This is clickable
          SPAN "»"
```

## Crash Course: What Works vs What Doesn't

### ❌ What DOES NOT work
- `querySelectorAll('button')` — returns 0. "Chọn" is NOT a `<button>`
- `page.evaluate(f"...\"{fn}\"...")` with f-string — causes JS SyntaxError `Unexpected token '('`
- `page.evaluate` with `await` inside JS — evaluate() is synchronous
- `browser tools` on abtrip.vn — Next.js SPA cuts params, redirects to homepage

### ✅ What WORKS
```python
# Click flight card
click_js = """
(fn) => {
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
}
"""
await page.evaluate(click_js, flight_number)

# Fill passenger form — use name attributes, not CSS class
await page.fill('input[name="passengers.adults.0.firstName"]', "NGUYEN")
await page.fill('input[name="passengers.adults.0.lastName"]', "NGOC TAN")
# Gender via label click
glabels = await page.query_selector_all('label:has(input[name="passengers.adults.0.gender"])')
await glabels[0].click()  # 0=Nam, 1=Nữ
await page.fill('input[name="passengers.adults.0.dob"]', "01/01/1990")
await page.fill('input[name="contact.name"]', "NGUYEN NGOC TAN")
await page.fill('input[name="contact.phone"]', "0904598388")
await page.fill('input[name="contact.email"]', "info@abtrip.vn")

# Submit
submit = await page.query_selector('button:has(span:text("Đặt vé"))')
await submit.scroll_into_view_if_needed()
await submit.click()
```

## Form Fields (Complete)

| Name Attribute | Placeholder | Type | Notes |
|---|---|---|---|
| `passengers.adults.0.firstName` | Nhập họ | text | Họ (không dấu) |
| `passengers.adults.0.lastName` | Nhập tên đệm và tên | text | Tên đệm + tên (không dấu) |
| `passengers.adults.0.gender` | — | radio | 2 inputs, click label, not input |
| `passengers.adults.0.dob` | dd/mm/yyyy | text | Format: dd/mm/yyyy |
| `contact.name` | Nhập họ và tên | text | Họ và tên người liên hệ |
| `contact.phone` | Nhập số điện thoại | tel | — |
| `contact.email` | Nhập email | text | — |

## Playwright `page.evaluate` Pitfalls

### Trap 1: f-string + `\"` causing SyntaxError
```python
# ❌ BROKEN — causes JS "Unexpected token '('"
await page.evaluate(f"""...\"{fn}\"...""")

# ✅ FIXED — pass arg separately
js = "(fn) => { return fn; }"
await page.evaluate(js, flight_number)
```

### Trap 2: `await` inside evaluate()
```python
# ❌ BROKEN — evaluate() is synchronous
js = "await new Promise(r => setTimeout(r, 500));"

# ✅ FIXED — handle timing in Python side
await page.wait_for_timeout(500)
js = "return document.title;"
await page.evaluate(js)
```

### Trap 3: `evaluate(expr, arg)` accepts exactly 1 arg
```python
# ❌ BROKEN
await page.evaluate("(a, b) => a + b", val1, val2)

# ✅ FIXED — use array destructuring
await page.evaluate("(args) => { const [a, b] = args; return a + b; }", [val1, val2])
```

## Debugging Sequence (Reproduction Recipe)

When book_flight fails with "Không tìm thấy chuyến bay X để đặt":

1. **Run debug script** on VPS to check "Chọn" button existence:
   ```python
   all_btns = await page.evaluate("""
   () => document.querySelectorAll('div.action-button span').length
   """)
   ```
   If 0 → card structure changed (CSS class rename likely).

2. **Check flight numbers rendering**:
   ```python
   walker = await page.evaluate("""
   () => {
       const results = [];
       const w = document.createTreeWalker(document.body, 4);
       let n;
       while (n = w.nextNode()) {
           const t = (n.textContent || '').trim();
           if (/^[A-Z]{2}\\d{3,4}$/.test(t)) results.push(t);
       }
       return results;
   }
   """)
   ```

3. **Check current URL** after navigation — abtrip.vn may strip params:
   ```python
   print(await page.evaluate("document.location.href"))
   ```

## URL Pattern for Direct Search (Bypass Homepage)

```
https://abtrip.vn/flight?adults=1&children=0&infants=0&tripType=one-way&segments[0][startPoint]={SGN}&segments[0][endPoint]={PQC}&segments[0][departDate]={15072026}
```

Works in Playwright headless. In live browser tool, Next.js cuts params and redirects to `/flight`.
