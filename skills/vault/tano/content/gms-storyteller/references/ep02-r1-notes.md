# R1 Script Writer — Prompt + Output Notes

## Prompt v1 → v2 evolution

### v1 (bad)
- Only said "Viết script 12-15 phút"
- No per-section char targets
- Output: 9,292 chars (8.4 min) — too short
- User: "hơi ngắn"

### v2 (good)
- Đưa exact char target cho mỗi section
- "HOOK ~1000-1400, BỐI CẢNH ~3300-4400, TỬ VI ~2800-3800..."
- "TỔNG: 13,000-16,500 ký tự. Đừng viết ngắn."
- Output: 13,313 chars — đạt yêu cầu

## Common R1 output issues to fix manually

1. **Thiếu CTA ở HOOK** — R1 thường quên, cần thêm: "Nhấn đăng ký trước khi tôi kể tiếp"
2. **Brand mention trùng** — R1 viết 2 lần trong cùng đoạn → fix: chuyển 1 lần ra câu riêng
3. **Encoding lỗi** — "Hóa Kỵ" → "Hóa K�ị" (check Unicode sau gen)
4. **Tiếng Anh lạc** — "coffee", "subscribe" → sửa về Việt
5. **Section không đều** — BỐI CẢNH và GIẢI PHÁP thường thiếu nhất

## R1 v2 prompt template (đã test hoạt động)

```json
{
  "model": "auto/best-reasoning",
  "messages": [
    {
      "role": "system",
      "content": "Bạn là GMSP Storyteller — viết script YouTube cho kênh \"Giải Mã Số Phận\".\n\nPHONG CÁCH: Một người đàn ông từng trải, đang kể cho đàn em...\n\nCẤU TRÚC 6 SECTION — TỔNG 13000-16000 ký tự = 12-15 phút:\n1. HOOK ~1000-1400 ký tự\n2. BỐI CẢNH ~3300-4400 ký tự\n3. TỬ VI ~2800-3800 ký tự\n4. TÂM LÝ & ĐỊNH LUẬT ~2800-3800 ký tự\n5. GIẢI PHÁP ~2800-3800 ký tự\n6. CLIFFHANGER ~800-1000 ký tự\n\nQUY TẮC: CÓ tên nhân vật. KHÔNG số liệu ảo. Tử Vi dịch ra đời thường.\n3 CTA + 3 lần \"Giải Mã Số Phận\". KO nhắc tên kênh 2 lần trong cùng 1 đoạn văn.\nNhịp luân phiên dài/ngắn/hỏi/beat/điệp.\nKết section = câu kéo.\nĐỪNG VIẾT NGẮN."
    }
  ],
  "max_tokens": 32768,
  "temperature": 0.65,
  "stream": false
}
```
