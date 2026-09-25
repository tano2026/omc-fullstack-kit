# Media Agent v2 — Real Tools Implementation

## Tool thật

### _real_brand() — Brand guide finder
```python
for f in _projects_root.rglob("BRAND_DESIGN.md"):
    # Found: Tano Agency brand
for f in _projects_root.rglob("*brand*"):
    if f.suffix in (".md", ".txt", ".json"):
        # Any brand-adjacent file
```

Fallback: dark theme (#0F0F1A), accent vàng (#FFD700), font system-ui.

### _real_assets() — Asset scanner
Scan D:/MMO Du an cho PNG/JPG/JPEG/SVG/MP4/WEBP. Filter theo topic stem.
Hiển thị: filename + folder + size (KB/MB).

### _real_image_gen() — AI Image Generator
Flow:
1. LLM nhận task → tạo JSON prompt:
```json
{"prompt": "...", "negative": "...", "ratio": "square|landscape|portrait"}
```
2. Gọi Hermes image_generate tool:
```python
from hermes_tools import image_generate
image_generate(prompt=prompt, aspect_ratio=ratio)
```
3. Trả về URL ảnh hoặc lỗi

### Notes
- Image gen chỉ hoạt động trong Hermes context (có hermes_tools)
- Fallback: LLM trả prompt text (không ảnh thật)
- Ratio mapping: square=1:1, landscape=16:9, portrait=9:16
