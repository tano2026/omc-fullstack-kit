# Ant Design Select Dropdown Strategy — abtrip.vn

## Problem
abtrip.vn uses Ant Design `Select` component with Ant Design virtualization. 
The options in the dropdown (e66-e88) show ref IDs but **no visible text** in the Playwright snapshot.

## Strategy (Hermes browser tool — updated 11/06/2026)

### Method 1: Direct ref click (nhanh nhất)
```
# Biết trước mapping ref→IATA của 23 airport Việt Nam:
# e66=BMV, e67=CAH, e68=CXR, e69=DAD, e70=DIN,
# e71=DLI, e72=HAN, e73=HPH, e74=HUI, e75=NHA,
# e76=PQC, e77=PXU, e78=SGN, e79=TBB, e80=THD,
# e81=UIH, e82=VCA, e83=VCL, e84=VCS, e85=VDO,
# e86=VDH, e87=VII, e88=VKG

# Bước 1: Click textbox để mở dropdown
browser_click(ref="e52")  # hoặc e53 cho điểm đến
# Bước 2: Browser snapshot để xác nhận refs còn valid
browser_snapshot()
# Bước 3: Click option
browser_click(ref="e69")  # DAD
```

### Method 2: Vision annotate (khi không biết mapping)
```
browser_click(ref="e52")  # Mở dropdown
# Dùng vision để annotate từng option
browser_vision(question="map the 23 options to their IATA codes", annotate=True)
# Click theo số [N] hiển thị trên screenshot
browser_click(ref="e69")
```

### Method 3: DOM inspection (cho trường hợp snapshot lỗi)
```
browser_console(expression="""
const tabp = document.querySelector('[role="tabpanel"]');
tabp.querySelectorAll('.item, [class*="option"]').forEach(el => {
  console.log(el.querySelector('span')?.innerText, el.querySelector('strong')?.innerText);
});
""")
```

## ⚠️ Critical: DO NOT hardcode ref IDs
Ref IDs (e66, e69, etc.) **thay đổi mỗi lần remount** trang. 
Undefined behavior nếu hardcode — mỗi lần browser_navigate, snapshot mới sẽ mapping lại.

## Known stable mapping (dựa trên thứ tự Ant Design render)
Ant Design render options theo thứ tự alphabet trong tabpanel.
23 airport Việt Nam — thứ tự cố định theo tên tiếng Việt.

## Flow steps (Hermes browser tool)
1. `browser_navigate("https://abtrip.vn")` — form search sẵn
2. Nếu cần Một chiều: `browser_click(ref="e19")`
3. `browser_click(ref="e52")` — mở dropdown điểm đi
   - Hoặc click textbox điểm đến `browser_click(ref="e53")`
4. `browser_snapshot()` — lấy refs mới
5. `browser_vision(annotate=True)` — map ref→IATA nếu cần
6. `browser_click(ref="e72")` — chọn HAN
7. Lặp lại cho điểm đến
8. Click DatePicker (e54) → chọn ngày
9. Click "Tìm kiếm" (e24)
