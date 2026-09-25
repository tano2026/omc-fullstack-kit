# abtrip.vn DOM & Form Analysis

> Cập nhật: 11/06/2026
> Mục đích: Tài liệu tham khảo chi tiết cho các agent cần tự động hóa search/booking trên abtrip.vn

## 1. Công nghệ

- **Framework:** Next.js (React Server Components)
- **UI Library:** Ant Design (antd)
- **State management:** React internal state (useState/useReducer trong component)
- **Routing:** Next.js App Router

## 2. Cấu trúc Form Search

### 2.1 Form Fields (Snapshot 06/2026)

```
[Logo ABTRIP]  [GIỚI THIỆU▼] [DỊCH VỤ▼] [TIN TỨC] [TIỆN ÍCH▼] [LIÊN HỆ]  [0868.320.320]
─────────────────────────────────────────────────────────────────────────────────────────
  ◉ Một chiều  ○ Khứ hồi                                              ▼ 1 người lớn
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│ [Khởi hành từ]  ↔  [Nơi đến]       [Ngày đi       ]  [             ]  [ Tìm kiếm ] │
│  Hà Nội, VN         HCM, VN          T5 11/06/2026                                   │
└─────────────────────────────────────────────────────────────────────────────────────────┘
```

### 2.2 Container Hierarchy

```
main
  └── generic (search section wrapper)
        ├── tabs: "Một chiều" / "Khứ hồi" — Ant Design Radio Button
        ├── passenger selector: "1 người lớn" — Ant Design Dropdown
        └── flight search form container
              ├── input "Khởi hành từ" (origin)
              ├── button swap (↔) — đảo origin/destination
              ├── input "Nơi đến" (destination)
              ├── input "Ngày đi" (depart date) — Ant Design DatePicker
              ├── input "Ngày về" (return date) — disabled unless round-trip
              └── button "Tìm kiếm"
```

### 2.3 CSS Class Patterns (Ant Design)

- **Origin input:** `input[placeholder="Khởi hành từ"]`
- **Destination input:** `input[placeholder="Nơi đến"]`
- **Date inputs:** `.ant-picker input[placeholder*="Ngày"]`
- **Search button:** `button.search-btn.enable` (hoặc 'Tìm kiếm' text match)
- **Passenger dropdown:** `.ant-select-dropdown` với các tùy chọn người lớn/trẻ em
- **Tab "Một chiều":** `.ant-radio-button-wrapper` (radio group)

## 3. Destination Dropdown (Airport Picker)

### 3.1 Mở dropdown

Click vào `input[placeholder="Nơi đến"]` sẽ kích hoạt Ant Design modal/overlay với:

- **Position:** Absolute overlay, thường centered hoặc below input
- **Tabs (Ant Design Tabs):**
  - Tab "Việt Nam" (default active)
  - Tab "Châu Á"
  - Tab "Châu Âu"
  - Tab "Hoa kỳ-Canada"
  - Tab "Châu úc-Châu Phi"
- **Tabpanel:** `[role="tabpanel"]` — active panel content

### 3.2 Grid Layout

```
                    Col 1              Col 2              Col 3
                   ──────────         ──────────         ──────────
Hàng 1 (row 1):    BMV (Buôn MT)      CXR (Nha Trang)     DAD (Đà Nẵng)
Hàng 2 (row 2):    DIN (Điện Biên)    DLI (Đà Lạt)        HAN (Hà Nội)
Hàng 3 (row 3):    HPH (Hải Phòng)    HUI (Huế)           PQC (Phú Quốc)
Hàng 4 (row 4):    PXU (Pleiku)       SGN (TP HCM)        TBB (Tuy Hòa)
Hàng 5 (row 5):    THD (Thanh Hóa)    VCL (Quảng Nam)     VII (Vinh)
Hàng 6 (row 6):    VCS (Côn Đảo)
```

**⚠️ Column-major ordering:** Items đi theo cột trước, hàng sau. Cột 1 hết rồi đến cột 2, cột 3.

**HTML item structure:**
```html
<div class="item ant-flex">
  <span>Phú Quốc</span>
  <strong>(PQC)</strong>
</div>
```

Grid container:
```html
<div role="tabpanel" class="ant-tabs-tabpane ant-tabs-tabpane-active">
  <div class="ant-row runway-items">
    <div class="ant-col ant-col-xs-24 ant-col-sm-8">
      <!-- cột 1: items theo chiều dọc -->
      <div class="item ant-flex"><span>Buôn Ma Thuột</span><strong>(BMV)</strong></div>
      <div class="item ant-flex"><span>Điện Biên Phủ</span><strong>(DIN)</strong></div>
      <div class="item ant-flex"><span>Hải Phòng</span><strong>(HPH)</strong></div>
      ...
    </div>
    <div class="ant-col ant-col-xs-24 ant-col-sm-8">
      <!-- cột 2: items theo chiều dọc -->
      <div class="item ant-flex"><span>Cam Ranh</span><strong>(CXR)</strong></div>
      ...
    </div>
    <div class="ant-col ant-col-xs-24 ant-col-sm-8">
      <!-- cột 3: items theo chiều dọc -->
      ...
    </div>
  </div>
</div>
```

### 3.3 Item Selection (Pitfall Detail)

**Vấn đề:** Khi dùng Pydoll/Playwright `browser_click` vào một `.item` trong tabpanel, DOM event được nhận nhưng **React synthetic event có thể không propagate** — nghĩa là click thành công ở DOM level nhưng `useState` của component không được cập nhật.

**Biểu hiện:** Giá trị `input[placeholder="Nơi đến"]` vẫn giữ nguyên "Hồ Chí Minh, Việt Nam" dù đã click "Phú Quốc (PQC)".

**Nguyên nhân:**
- Ant Design dùng `onMouseDown` (không phải `onClick`) để xử lý chọn item trong Select component
- Pydoll's `browser_click` dispatch `click` event nhưng không dispatch `mousedown`
- React synthetic event system yêu cầu event propagation đúng thứ tự `mousedown → mouseup → click`

**Workarounds (thử nghiệm không thành công trên abtrip.vn 06/2026):**
1. `browser_click` vào `.item` → không update React state
2. JS `.click()` qua `browser_console` → vẫn không update React state
3. Dispatch `mousedown` + `mouseup` + `click` → vẫn không
4. `element.dispatchEvent(new MouseEvent('mousedown', { bubbles: true }))` + tương tự cho mouseup/click → thất bại

**Giải pháp thay thế:**
- **Option A:** Dùng CloakBrowser (MCP tool `cloakbrowser_execute`) — anti-bot Chromium có thể bypass các React state guard tốt hơn
- **Option B:** Dùng `mcp_flight_search_flight_web` — scrape directly from abtrip.vn search results page via URL parameters
- **Option C:** Dùng Google Flights (xem section 1.6 của ticketing-manager skill)

## 4. Date Picker

Ant Design DatePicker — không có `readonly` attribute. Structure:
```html
<div class="ant-picker">
  <input placeholder="Ngày đi" readonly="">
  <!-- Ant Design popup calendar khi focus -->
</div>
```

Lưu ý: Input có `readonly=""` attribute thật. Để nhập ngày qua JS:
```javascript
const inputs = document.querySelectorAll('.ant-picker input');
inputs[0].value = '12/06/2026'; // DD/MM/YYYY format
inputs[0].dispatchEvent(new Event('input', { bubbles: true }));
inputs[0].dispatchEvent(new Event('change', { bubbles: true }));
```

## 5. Search Button

```
Tag: button
Class: search-btn (thêm 'enable' khi form đủ điều kiện)
Text: "Tìm kiếm"
```

Click bằng:
```javascript
document.querySelector('button.search-btn.enable').click();
```
hoặc:
```javascript
Array.from(document.querySelectorAll('button')).find(b => b.textContent.trim() === 'Tìm kiếm')?.click();
```

## 6. Search Results Page

Sau khi search thành công, URL pattern:
```
https://abtrip.vn/search?startPoint=HAN&endPoint=PQC&departDate=2026-06-12&...
```

Giá vé được render dưới dạng Ant Design Table hoặc custom cards.

## 7. Kỹ thuật Debug cho Future Sessions

### 7.1 Inspect nhanh cấu trúc form
```javascript
// Liệt kê tất cả input/select/button
JSON.stringify(Array.from(document.querySelectorAll('input, select, button, textarea')).map(el => ({
  tag: el.tagName, type: el.type, name: el.name, id: el.id,
  placeholder: el.placeholder || el.getAttribute('placeholder') || '',
  value: el.value, className: el.className.slice(0,80)
})))
```

### 7.2 Verify React state
```javascript
// Kiểm tra giá trị thực tế của input (React state)
document.querySelector('input[placeholder="Nơi đến"]')?.value;
```

### 7.3 Tìm item trong dropdown bằng text
```javascript
// Chọn sân bay bằng text matching — fallback khi browser_click không hiệu quả
const panel = document.querySelector('[role="tabpanel"]');
if (panel) {
  const items = panel.querySelectorAll('.item');
  for (let i = 0; i < items.length; i++) {
    if (items[i].textContent.includes('Phú Quốc')) {
      items[i].click();
      break;
    }
  }
}
```

### 7.4 Lấy toàn bộ danh sách sân bay
```javascript
// Xem tất cả sân bay có sẵn trong dropdown
const allAirports = Array.from(document.querySelectorAll('[role="tabpanel"] .item'))
  .map(el => el.textContent.trim());
```

### 7.5 Kiểm tra dispatch event có thành công không
```javascript
// Override native addEventListener để log tất cả event
// Chạy TRƯỚC khi mở dropdown
const origAdd = EventTarget.prototype.addEventListener;
EventTarget.prototype.addEventListener = function(type, fn, opts) {
  if (type === 'click' || type === 'mousedown') {
    console.log('[EVENT]', type, this.className || this.tagName, this.textContent?.trim().slice(0,30));
  }
  return origAdd.call(this, type, fn, opts);
};
```

## 8. Lưu ý khi tích hợp

- **KHÔNG hardcode ref IDs** — các ref `@e66`-`@e88` thay đổi mỗi lần component mount
- **Luôn dùng `browser_vision(annotate=true)`** để inspect form state trước khi thao tác
- **React state bug là rào cản chính** — nếu không chọn được destination đúng, chuyển sang Google Flights hoặc B2B API
- **Token budget:** form interaction tốn ~50-100x so với web_extract — ưu tiên lightweight approach
