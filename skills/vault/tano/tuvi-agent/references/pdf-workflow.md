# PDF Report Generation Workflow

Tạo báo cáo Tử Vi PDF giao cho khách (Gói Cơ bản → Gia tộc).

## Pipeline tổng quan

```
GATHER MCP DATA → STRUCTURE SECTIONS → BUILD PDF (fpdf2) → SAVE → DELIVER (Telegram/file)
```

## Bước 1: Gather data (gọi MCP tools song song)

Dùng `mcp_tuvi_*` tools đồng loạt (tất cả trong 1-2 batch gọi):

```python
# Các tool BẮT BUỘC:
mcp_tuvi_calculate_chart(year, month, day, hour, gender, 'vi')    # Lá số 12 cung
mcp_tuvi_four_pillars(...)                                         # Tứ trụ Bát tự
mcp_tuvi_analyze_destiny(...)                                      # Phân tích Mệnh/Tài/Quan chính
mcp_tuvi_life_timeline(...)                                        # Đại hạn 0-120
mcp_tuvi_current_decadal_fortune(...)                              # Đại hạn hiện tại
mcp_tuvi_divination(..., focus='all')                              # Luận giải tổng thể
mcp_tuvi_yearly_detailed(...)                                      # Lưu niên năm nay

# Các tool MỞ RỘNG (gói Cao cấp trở lên):
mcp_tuvi_palace_detail(..., palace='Mệnh')                         # Phân tích chuyên sâu từng cung
mcp_tuvi_palace_detail(..., palace='Tài Bạch')
mcp_tuvi_palace_detail(..., palace='Quan Lộc')
mcp_tuvi_palace_detail(..., palace='Điền Trạch')
mcp_tuvi_palace_detail(..., palace='Phu Thê')
mcp_tuvi_palace_detail(..., palace='Tật Ách')
mcp_tuvi_empty_palace_analysis(...)                                # Phân tích VCD
mcp_tuvi_weekly_fortune(...)                                       # Tuần này
mcp_tuvi_daily_fortune(...)                                        # Ngày này
mcp_tuvi_yearly_fortune(...)                                       # Năm cụ thể
mcp_tuvi_compatibility(...)                                        # Tương tác 2 lá số
```

## Bước 2: Cấu trúc PDF

### Chapter layout

```
Trang bìa → Trang phụ (disclaimer + mục lục) → Chương 1..N → Trang kết
```

Mỗi chương = `chapter_separator(num, title)` (full page title card) + nội dung.

### Chapter sequence cho Gói Đặc biệt (40-50 trang)

| Chương | Nội dung | Tool cần |
|--------|----------|----------|
| 1 | Tứ trụ, Ngũ hành, Nạp âm | four_pillars |
| 2 | Lá số 12 cung tổng quan + sơ đồ + Tứ hóa | calculate_chart |
| 3-4 | Phân tích 12 cung (A:6 cung đầu, B:6 cung cuối) | palace_detail x6 + calculate_chart |
| 5 | VCD & Tứ hóa chuyên sâu | empty_palace_analysis |
| 6 | Đại hạn dòng đời 0-120 (bảng) | life_timeline |
| 7 | Đại hạn hiện tại (chuyên sâu nhất) | current_decadal_fortune |
| 8 | Lưu niên năm nay | yearly_detailed |
| 9 | Tương tác/Compatibility | compatibility |
| 10 | Kinh Dịch | cast_hexagram + get_hexagram_detail |
| 11 | Chiến lược tổng thể | divination (tổng hợp) |
| 12 | Phụ lục A: Ý nghĩa sao | tính từ calculate_chart |
| 13+ | Phụ lục B: Luận giải tuần/ngày | weekly_fortune, daily_fortune |
```

## Bước 3: fpdf2 setup (Windows)

```python
from fpdf import FPDF

class TuViPDF(FPDF):
    def __init__(self):
        super().__init__('P', 'mm', 'A4')
        # Windows fonts hỗ trợ Vietnamese Unicode
        self.add_font('Arial', '', 'C:/Windows/Fonts/arial.ttf')
        self.add_font('Arial', 'B', 'C:/Windows/Fonts/arialbd.ttf')
        self.add_font('Arial', 'I', 'C:/Windows/Fonts/ariali.ttf')
        self.add_font('Arial', 'BI', 'C:/Windows/Fonts/arialbi.ttf')
        self.set_auto_page_break(True, 22)
```

## Bước 4: Kỹ thuật fpdf2 key

### Chapter separator (trang title card đầy trang)

```python
def chapter_separator(self, num, title):
    self.add_page()
    self.ln(50)
    self.set_draw_color(180, 160, 120)
    self.set_line_width(0.3)
    self.line(30, self.get_y(), 180, self.get_y())
    self.ln(8)
    self.set_font('Arial', 'B', 14)
    self.set_text_color(140, 120, 90)
    self.cell(0, 8, f'CHƯƠNG {num}', new_x='LMARGIN', new_y='NEXT', align='C')
    self.ln(5)
    self.set_font('Arial', 'B', 22)
    self.set_text_color(26, 35, 53)
    self.multi_cell(0, 12, title, align='C')
```

### Body text với line spacing

```python
def body_text(self, text):
    self.set_font('Arial', '', 10)
    self.set_text_color(50, 50, 50)
    self.multi_cell(0, 6, text)  # line height = 6mm
```

### Info row (label: value)

```python
def info_row(self, label, value):
    self.set_font('Arial', 'B', 10)
    self.cell(55, 7, label)
    self.set_font('Arial', '', 10)
    self.cell(0, 7, value, new_x='LMARGIN', new_y='NEXT')
```

### Quote box (highlight text)

```python
def quote_box(self, text):
    self.set_fill_color(245, 242, 235)
    self.set_draw_color(180, 170, 150)
    self.set_font('Arial', 'I', 10)
    self.set_text_color(80, 70, 60)
    self.set_x(18)
    self.multi_cell(175, 6, text, border=1, fill=True)
```

### Table (tra cứu 2 cột)

```python
# Header
pdf.set_font('Arial', 'B', 9)
pdf.set_fill_color(200, 190, 170)
pdf.cell(30, 7, 'Title', border=1, align='C', fill=True)
pdf.cell(160, 7, 'Content', border=1, align='C', fill=True)
pdf.ln()
# Rows
for name, data in items:
    pdf.set_font('Arial', '', 8)
    pdf.cell(30, 6, name, border=1, fill=True)
    pdf.cell(160, 6, data, border=1, fill=True)
    pdf.ln()
```

### Font size guide

| Element | Size | Style |
|---------|------|-------|
| Title page name | 32 | Bold |
| Chapter title | 22 | Bold |
| Chapter number | 14 | Bold, gold |
| Section title | 13 | Bold |
| Sub-section | 11 | Bold |
| Body text | 10 | Normal |
| Small body | 9 | Normal |
| Table header | 8-9 | Bold |
| Table data | 7-8 | Normal |
| Footer/Header | 7-8 | Italic |

### Màu sắc (Dark Academia palette)

| Element | Hex |
|---------|-----|
| Text chính | #323232 |
| Tiêu đề chương | #1A2335 |
| Nâu đậm | #8C785A |
| Nâu nhạt | #B4A87A |
| Highlight background | #F5F2EB |
| Table header | #C8BEB5 |
| Table row | #F8F5EE |
| Border | #B4AA96 |
| Footer text | #A0A0A0 |

## Bước 5: Gói sản phẩm & độ dài tương ứng

| Gói | Số trang | Những chương cần |
|-----|----------|------------------|
| Cơ bản (199k) | 10-15 | 1, 2, 6, 7, 11 |
| Tiêu chuẩn (999k) | 30-40 | 1→8 + 11 |
| Cao cấp (4tr) | 60-80 | 1→11 + phụ lục A+B |
| Đặc biệt/Gia tộc (10tr+) | 40-100+ | 1→13 + thêm compatibility, tương tác, chiến lược nhiều người |

## Bước 6: Save & Deliver

```python
# Save
out_path = os.path.expanduser('~/full_tuvi_baocao.pdf')
pdf.output(out_path)
print(f'PDF saved: {out_path} ({pdf.page_no()} pages)')

# Gửi Telegram
# → Dùng send_message với MEDIA:path trong message
# send_message(target='telegram', message=f'MEDIA:{out_path}\nThông điệp...')
```

## Pitfalls

1. **fpdf2 line breaks**: multi_cell(0, 6, text) với text có \n sẽ tự động xuống dòng. Dùng multi_cell cho đoạn dài, cell cho label/value ngắn.
2. **🐍 Unicode symbols**: fpdf2 Arial missing ★⚠✧ glyphs. Thay thế: * → (sao), ! → (cảnh báo), # → (ngôi sao). Hoặc dùng ký tự ASCII đơn giản.
3. **Page break**: auto_page_break = True, margin 22mm. Nếu nội dung multi_cell bị cut, giảm font size hoặc thêm add_page() trước.
4. **Table row height**: cell() chiều cao cố định. Với multi-line trong table, dùng multi_cell và set_y() để căn chỉnh.
5. **new_x/new_y**: fpdf2 ≥2.8.x dùng new_x='LMARGIN', new_y='NEXT' (deprecated `ln`). Tương thích ngược với 2.7.x bằng `ln=1`.
6. **File path trên Windows**: dùng ~/ hoặc os.path.expanduser() — MSYS git-bash convert path ok.
7. **Script lớn (>900 dòng)**: chia thành functions, giữ mỗi function < 100 dòng. Dùng class methods.
