---
name: tuvi-chart-renderer
category: tuvi
description: "Render la so Tu Vi ra HTML layout luc hop 12 cung. Dung MCP calculate_chart, parse, sinh HTML Dark-academia. Interactive: click cung ra popup luan giai. Mo browser de chup/share."
related_skills:
  - tuvi-agent
  - tuvi-dau-so-expert
---

# 🎨 TỬ VI CHART RENDERER

Vẽ lá số Tử Vi dạng HTML layout **lục hợp 12 địa chi**, màu tối Dark Academia — phù hợp thương hiệu Giải Mã Số Phận.

**Chức năng:** Click vào mỗi cung → popup modal hiện luận giải chi tiết + danh sách sao. Luận giải được sinh sẵn từ dữ liệu sao, không cần MCP backend real-time.

## 🎯 KHI NÀO DÙNG

- User muốn xem **hình ảnh lá số** thay vì text
- Cần share chart qua Telegram / web
- Cần snapshot chart để đính kèm vào luận giải

## 📁 Cấu trúc

| File | Chức năng |
|------|---------|
| `scripts/render_chart.py` | Script Python chính: parse JSON → HTML |
| `SKILL.md` | Hướng dẫn tích hợp |

## KIEN TRUC

Script `scripts/render_chart.py` hoat dong theo 2 buoc:

1. **Build du lieu:** Tu JSON chart + bo INTERPRETATIONS co san (12 cung, moi cung 3-5 muc luan giai) -> sinh JSON nhung trong HTML
2. **Render:** Layout luc hop + JS click handler + modal popup

**INTERPRETATIONS** la dictionary trong script, moi cung co:
- `tieuDe`: tieu de luan giai
- `noiDung`: array cac muc `[ten sao/khia canh, noi dung luan giai]`
- `starSummary`: tu dong sinh tu du lieu chart JSON thuc te

**Co che interactive:**
- Moi `td` co `data-cung="Ten cung"` + `onclick="showLuangiai('Ten cung')"`
- Khi click: JS doc tu INTERP_DATA (JSON nhung trong `<script>`), hien thi modal
- Modal dong bang: click overlay / nut X / phim Escape

## Cach dung

### Cach A - Day du (khuyen dung)

Lay ca du lieu chart + luan giai chi tiet 12 cung tu MCP:

```python
# 1. Goi MCP lay chart
chart_data = mcp_tuvi_calculate_chart(year=..., month=..., day=..., hour=..., gender=...)

# 2. (Tuy chon) Goi MCP lay palace_detail cho cac cung chinh
# mcp_tuvi_palace_detail(year=..., month=..., day=..., hour=..., gender=..., palace="Menh")

# 3. Luu JSON chart -> file -> render
write_file(path="/tmp/tuvi_input.json", content=json.dumps(json.loads(chart_data), ensure_ascii=False))
terminal(f"python <skill_path>/scripts/render_chart.py --input /tmp/tuvi_input.json --output /tmp/tuvi_chart.html")
```

**Ket qua:** File HTML tu dong co luan giai cho 12 cung dua tren bo INTERPRETATIONS mau.

### Cach B - Nhanh (chi chart, dung bo luan giai mau)

```python
# PIPE truc tiep data.json tu MCP calculate_chart vao script
# echo 'JSON_DATA' | python <skill_path>/scripts/render_chart.py --output chart.html
```

Luan giai se dung bo mau co san, tu dong map theo ten cung.

### Buoc cuoi - Xem / Gui

```python
# Cach 1 - Mo browser:
# browser_navigate("file:///C:/Users/.../tuvi_chart.html")

# Cach 2 - Gui file HTML qua Telegram:
# send_message(target="telegram", message="La so ...\n\nMEDIA:/path/to/chart.html")

# Cach 3 - Copy ra web server public
```

## 🖼️ Layout output

```
┌──────────────────────────────────────────┐
│ Tỵ(3)  Ngọ(4)  Mùi(5)   Thân(6)        │ ← Nô Bộc, Thiên Di, Tật Ách, Tài Bạch
│ Thìn(2) ──── TRUNG TÂM ──── Dậu(7)     │ ← Quan Lộc, center info, Tử Nữ
│ Mão(1) ──── (info panel) ─── Tuất(8)    │ ← Điền Trạch, center info, Phu Thê
│ Dần(0)  Sửu(11) Tý(10)  Hợi(9)         │ ← Phúc Đức, Phụ Mẫu, Mệnh, Huynh Đệ
└──────────────────────────────────────────┘
```

Mỗi cell: **tên cung** | can chi | đại hạn | chính tinh (vàng) | phụ tinh (xanh) | tạp tinh (xám) | độ sáng | tứ hóa màu

## 🤖 AGENT INTEGRATION

```python
# === Dùng execute_code để render chart ===
from hermes_tools import terminal, write_file, read_file
import json

# 1. Gọi MCP lấy dữ liệu
# result = await mcp_tuvi_calculate_chart(...)  # agent gọi trực tiếp
# data = json.loads(result)

# 2. Lưu tạm
# write_file(path="/tmp/tuvi_input.json", content=json.dumps(data, ensure_ascii=False))

# 3. Chạy render
# skill_dir = "D:\\AI Store\\AgentConfigs\\hermes-local-appdata\\skills\\tuvi\\tuvi-chart-renderer"
# result = terminal(f"python \"{skill_dir}/scripts/render_chart.py\" --input /tmp/tuvi_input.json --output /tmp/tuvi_chart.html")
# chart_path = result["output"].strip()

# 4. Browser snapshot
# terminal(f"cp \"{chart_path}\" /tmp/tuvi_final.html")  # copy ra chỗ dễ tìm
# browser_navigate(f"file:///C:/Users/NGUYEN~1/AppData/Local/Temp/tuvi_final.html")
# browser_vision(question="Check layout lá số tử vi")
