# Price List / Bảng Giá — Design Guide

## Sources
- Original: `BaoGia_DichVuSanBay_AnBinh (FULL).xlsx` (2 sheets: FAST TRACK, BUSINESS LOUNGE)
- Read with: `openpyxl.load_workbook(path, data_only=True)` — `data_only=True` is MANDATORY for Excel files with formulas, otherwise you get `None`

## 3 Versions Required

| File | Audience | Price Columns | Extra |
|------|----------|:---:|-------|
| `pricelist-retail.html` | Khách lẻ (retail) | 1 | CTA box lớn, policy đơn giản |
| `pricelist-agent.html` | Đại lý & CTV | 2 (Agent / Retail) | Commission tiers 15/20/25/30%, watermark, badge ĐỐI TÁC |
| `pricelist.html` | Corporate & Gov | 3 (Agent / Corp / Retail) | Full detail |

## User Preferences (Vietnamese airport services context)
- **STT column**: 18px (width:18px) — user wants SMALL counter
- **Service name column**: 18%
- **Details column**: 42-46% — WIDE to prevent word wrap
- **Price columns**: 11-12% each
- **CTA box**: navy background `#1B3A6B`, link gold `#FFD700`, large text 11pt
- **Service details**: ALWAYS full bullet points — never simplify (user complaint: "mày làm mất hết chi tiết dịch vụ")
- **English text**: grey colour `#aaa` at 6.2pt, visually subordinate to VN

## Structure (Fast Track sheet)

Sheet has 22 rows x 8 cols. Structure:

- Rows 1-4: Header (company name, airport, contact)
- Row 5: Category header "I. HỖ TRỢ THỦ TỤC - FAST TRACK"
- Row 6: Table headers (STT, DỊCH VỤ, NỘI DUNG, 3 price columns, GHI CHÚ)
- Row 7+: Data categorized by terminal:
  - **Domestic (T1)**: Fast Track Departure, Fast Track Arrival
  - **Int'l Departure (T2)**: Standard, Fast Track, VIP B
  - **Int'l Arrival (T2)**: Standard, Fast Track, VIP B
  - **Transit**: Int'l→Domestic, Domestic→Int'l
- Last rows: Note (infants free, prices exclude VAT, USD for reference)

### Key observation
The original Excel has **duplicate row numbers** (e.g. two rows labelled "3", two labelled "5"). Each duplicate represents a variation (same base service, different detail for departure vs? Actually the 2nd "3" is a different service with same number). **Should be sequential 1-N.**

## 3 Price Tiers
| Column | Vietnamese | English | Notes |
|--------|-----------|---------|-------|
| Col 4 | Đại lý & CTV | Agents & Affiliates | Lowest — wholesale |
| Col 5 | Bộ, Ban ngành, Công ty & Tập đoàn | Ministries, Gov, Companies & Corporations | Mid — corporate |
| Col 6 | Khách lẻ | Individual customers | Highest — retail |

## Pricing Table in the HTML Deliverable

### Layout
- Retail: 4 columns (#, Service, Details, Retail Price)
- Agent: 5 columns (#, Service, Details, Agent Price, Retail Price)
- Full: 6 columns (#, Service, Details, Agent, Corporate, Retail)
- Category rows with colored background (`#E8F4F8`) and teal border
- Tags: Fast Track (yellow), VIP B (red), Standard (grey), Transit (like FT)

### Service Detail Format (REQUIRED — full bullets, never simplify)

**Fast Track Departure (Domestic):**
- Đón khách tại điểm đón trên sân bay
- Hỗ trợ check-in & gửi hành lý tại quầy
- Soi chiếu an ninh ưu tiên
- Hướng dẫn đến cửa ra tàu bay
- EN: Meet at meeting point, assist check-in, priority security, guide to boarding gate

**Fast Track Arrival (Domestic):**
- Trưng biển đón tại băng chuyền hành lý
- Hỗ trợ lấy hành lý và tiễn ra xe
- EN: Pick up at baggage claim, assist luggage, escort to car

**Standard Departure (Int'l):**
- Đón khách tại điểm đón trên sân bay
- Hỗ trợ check-in & gửi hành lý
- Hướng dẫn khu vực xuất cảnh
- EN: Meet at meeting point, assist check-in, guide immigration

**Fast Track Departure (Int'l):**
- Đón khách tại điểm đón trên sân bay
- Hỗ trợ check-in & gửi hành lý
- Soi chiếu an ninh ưu tiên
- Thủ tục xuất cảnh ưu tiên
- Hướng dẫn cửa ra máy bay
- EN: Meet, assist check-in, priority security, priority immigration, guide to gate

**VIP B Departure (Int'l):**
- Đón khách tại điểm đón trên sân bay
- Check-in tại quầy ưu tiên
- Thay mặt khách làm thủ tục xuất cảnh
- Soi chiếu an ninh ưu tiên
- Thủ tục xuất cảnh ưu tiên
- Hướng dẫn cửa ra máy bay
- EN: Meet, priority check-in, handle immigration on behalf, priority security, guide to gate

**Standard Arrival (Int'l):**
- Trưng biển đón tại khu vực nhập cảnh
- Hướng dẫn khu vực lấy visa (nếu cần)
- Hướng dẫn khách làm thủ tục nhập cảnh
- Hướng dẫn khu vực lấy hành lý
- EN: Pick up at immigration, guide visa area (if needed), guide immigration, guide luggage

**Fast Track Arrival (Int'l):**
- Trưng biển đón tại khu vực nhập cảnh
- Hướng dẫn khu vực lấy visa (nếu cần)
- Hỗ trợ qua bục nhập cảnh ưu tiên
- Hướng dẫn khu vực lấy hành lý
- EN: Pick up at immigration, guide visa, assist priority immigration, guide luggage

**VIP B Arrival (Int'l):**
- Trưng biển đón tại khu vực nhập cảnh
- Dẫn thẳng xuống khu vực lấy hành lý
- Thay mặt khách làm thủ tục nhập cảnh
- Hỗ trợ lấy hành lý và dẫn ra xe
- EN: Pick up at immigration, escort directly to baggage, handle immigration on behalf, assist luggage

**Int'l → Domestic Transit:**
- Đón & nhập cảnh qua bục ưu tiên
- Hỗ trợ lấy hành lý, di chuyển sang ga nội địa
- Check-in chuyến bay tiếp nối
- Hướng dẫn soi chiếu & cửa ra tàu bay
- EN: Pick up, priority immigration, get luggage, move to domestic terminal, check-in next flight, guide to security & gate

**Domestic → Int'l Transit:**
- Đón tại sảnh đến ga nội địa
- Di chuyển sang ga quốc tế
- Check-in & thủ tục xuất cảnh
- Hướng dẫn soi chiếu & cửa ra tàu bay
- EN: Pick up at domestic arrival, escort to international terminal, check-in, guide security & immigration & gate

### Key policies to include
1. **Night surcharge**: 23:00–06:00, +200,000₫/pax, applies to all services EXCEPT lounge
2. **Infants**: <2 years FREE (max 2 per adult). Children ≥2: adult rate. 2nd child onward (any age): adult rate.
3. **VAT**: All prices exclude VAT. VAT invoices available for corporate.
4. **Group**: 10+ pax — contact for volume rates
5. **Lead time**: Min 2h booking ahead. WhatsApp response within 5 min.
6. **Cancellation**: Free up to 24h before service. Late: 50% fee.

### Agent Commission Structure (only in pricelist-agent.html)
| Tier | Volume | Rate | Benefits |
|------|--------|:---:|----------|
| Tier 1 — Mới | 0-50 pax/mo | 15% | Referral code, CRM access |
| Tier 2 — Phát triển | 51-150 pax/mo | 20% | Marketing support + banner |
| Tier 3 — VIP | 150+ pax/mo | 25% | Priority account, 24/7 support |
| Tour/Group | 10+ pax | 30% | Net-15 payment |

### Brand colors for price list
- Primary: `#006885` (teal/blue from logo)
- Accent: `#DBA011` (gold from logo)
- Text: `#1C1C1E` (charcoal)
- Table header: `#006885` with white text
- Category row: `#E8F4F8` (light teal tint)
- Surcharge box: `#FFF8E1` with `#DBA011` left border
- Agent price text: `#006885` (teal)
- Retail price text: `#888` (grey)
- CTA box: `#1B3A6B` bg, `#FFD700` link
- Policy cards: `#F9F9F9`

### Typography for price list
- Font: Inter (sans-serif), all weights 300-700
- Service name: 7.8-8pt, weight 500-600, navy `#1B3A6B`
- English subtitle: 6.5pt, weight 400, grey `#888`
- Details: 6.8pt, alternating lines with `•` bullet
- Price: 7.8pt, weight 600, right-aligned
- USD note: 6pt, weight 400, `#999`

### Print setup
```css
@page{size:A4;margin:8mm 8mm}
@media print{body{-webkit-print-color-adjust:exact;print-color-adjust:exact}}
```

### Business Lounge sheet (separate page)
- Header: "PHÒNG CHỜ THƯƠNG GIA NỘI BÀI"
- Table header background: `#1B3A6B` (navy — different from Fast Track teal)
- Category rows: `#E8EEF8` (blue tint — different from teal tint)
- 4 lounges: NASCO-LOTUS Int'l, SH Premium Ha Noi East, NASCO-LOTUS Domestic, SH Premium Ha Noi
- Column: Lounge, Location, Adult (VND), Child (VND), Note
- Time limit: Max 3 hours. Overtime: 50%/guest/3h block
- Infants <2: 1 free per adult

## Data Extraction Pattern
```python
import openpyxl
wb = openpyxl.load_workbook('file.xlsx', data_only=True)
for name in wb.sheetnames:
    ws = wb[name]
    for row in ws.iter_rows(min_row=1, max_row=ws.max_row, values_only=True):
        vals = [c for c in row]
        if any(v is not None for v in vals):
            # process — expecting columns: STT, Tên DV, Mô tả, Giá Agent, Giá Corp, Giá Retail, Note
            print(vals[:8])
```
