# External Ecosystem — Tử Vi & Chiêm Tinh Học

> Catalog các MCP server, thư viện, repo mã nguồn mở liên quan đến Tử Vi, Bát Tự, Chiêm Tinh, huyền học phương Đông. Cập nhật: 03/06/2026.

## MCP Servers (có thể tích hợp ngay)

### 1. `cantian-ai/bazi-mcp` ⭐385
- **Bát Tự MCP Server** — tính toán và phân tích Tứ Trụ Bát Tự
- TypeScript, npm install / npx
- Link: https://github.com/cantian-ai/bazi-mcp

### 2. `shunshi-ai/bazi-reader-mcp` ⭐4 (v0.2.0)
- Bát Tự MCP đa ngôn ngữ (CN/EN/JP/KR)
- Có **true solar time correction** (hiệu chỉnh giờ mặt trời thực)
- v0.2.0 thêm: **Hoàng Lịch (黄历)** tool
- Có Cloudflare Worker cho remote deployment
- Sử dụng: `npx shunshi-bazi-mcp`
- Link: https://github.com/shunshi-ai/bazi-reader-mcp

### 3. `hhszzzz/taibu` — gói `taibu-mcp` ⭐199
- Full divination system có MCP server riêng (gói npm `taibu-mcp`)
- Hỗ trợ: Bát Tự, Tử Vi, Lục Hào, Mai Hoa Dịch Số, Kỳ Môn Độn Giáp, Đại Lục Nhâm, Tiểu Lục Nhâm, Chiêm Tinh, Thái Ất Thần Số, Tarot, MBTI, Tướng Mặt/Tay, Giải Mộng
- Đã có sẵn skills folder trong repo
- Link: https://github.com/hhszzzz/taibu

## Thư viện Tử Vi Core (thuật toán an sao)

### 4. `SylarLong/iztro` ⭐3.8k ⭐ ĐANG DÙNG
- Thư viện TypeScript #1 về Tử Vi Đẩu Số
- Generate lá số đầy đủ: 12 cung, chính tinh, phụ tinh, tập tinh, tứ hóa, đại hạn
- Đa ngôn ngữ (Việt, Trung, Anh)
- 42 tags, 614 commits, active nhất cộng đồng
- Link: https://github.com/SylarLong/iztro

### 5. `SylarLong/react-iztro` ⭐516
- React component wrapper của iztro
- Vẽ lá số trực quan trên web
- Link: https://github.com/SylarLong/react-iztro

### 6. `Renhuai123/ziwei-doushu` ⭐1.2k
- Dựa trên hệ thống **倪海夏《天纪》**
- Full: an sao engine, tứ hóa, cách cục knowledge base, cổ thư
- TypeScript / Next.js
- Link: https://github.com/Renhuai123/ziwei-doushu

### 7. `ruijayfeng/ziwei` (ZiweiKnows) ⭐344
- Tử Vi open source với **AI reading pipeline**
- Self-hosted, multi-model (OpenAI, Claude, etc.)
- Cấu trúc MVC rõ ràng, dễ học
- Update 2 ngày trước (active)
- Link: https://github.com/ruijayfeng/ziwei

## Hệ thống Huyền Học Toàn Diện

### 8. `Horace-Maxwell/Horosa` ⭐260
- "十项全能玄学术数工作站" — Workstation huyền học đa năng
- Bao gồm: Tử Vi + Bát Tự + Chiêm Tinh + Lục Nhâm + Độn Giáp + Thái Ất + Lục Hào + Phong Thủy + Hà Lạc + Chính Độ Pháp (Primary Direction)
- **Có bản Windows riêng**: Horace-Maxwell/Horosa-Web-App-comprehensively-improved-Windows
- Built-in AI analysis + các kỹ thuật suy luận cao cấp
- Link: https://github.com/Horace-Maxwell/Horosa-Web-App-comprehensively-improved-MacOS

### 9. `hhszzzz/taibu` ⭐199
- Xem mục #3 ở trên. Đáng chú ý: có MCP + Skills folder sẵn, học cấu trúc để tham khảo
- Full stack: supabase backend, web app, Android, iOS

### 10. `masterai-top/Bazi-Ziwei-Qimen-Dunjia-Divination-System` ⭐46
- Java full system: Bát Tự + Tử Vi + Kỳ Môn Độn Giáp + Thất Chính Tứ Dư + Đại Lục Nhâm
- Web realtime, có thể vận hành thương mại
- Link: https://github.com/masterai-top/Bazi-Ziwei-Qimen-Dunjia-Divination-System-Source-Code

## Visualize / Khác

### 11. `miounet11/life-kline` ⭐134
- "人生K线" — Biểu đồ cuộc đời dạng K-line chứng khoán
- AI + Bát Tự + visualization
- React + Node.js, self-hosted
- Link: https://github.com/miounet11/life-kline

## Gợi ý Tích Hợp

| Mục tiêu | Nên dùng | Lý do |
|---|---|---|
| Thay core engine MCP tử vi | `iztro` ⭐3.8k | Đã dùng, chuẩn nhất |
| Thêm Bát Tự + Hoàng Lịch | `shunshi-bazi-mcp` | `npx` 1 lệnh, miễn phí |
| Luận giải AI tử vi | `ruijayfeng/ziwei` ⭐344 | Đã có AI reading pipeline |
| Học kiến thức chiêm tinh Đông phương | `Horosa` ⭐260 | Bách khoa toàn thư |
| Mở rộng sang Kỳ Môn/Lục Nhâm/Thái Ất | `taibu` ⭐199 | Có MCP + skills sẵn |

## Keywords tìm kiếm trên GitHub
- Topics: `ziwei-doushu`, `chinese-astrology`, `bazi`, `qimen`, `divination`, `fortune-telling`
- Các topic này có 18-105 public repos mỗi topic
