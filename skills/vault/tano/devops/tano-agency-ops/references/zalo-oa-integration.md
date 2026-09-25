# Zalo OA Integration — Pricing & Approach

> Research date: 25/07/2026. Pricing effective from 01/06/2026.

## Gói Zalo OA cần thiết

Để tích hợp Hermes (webhook/OpenAPI), cần **Gói Tăng trưởng**:

| Gói | Giá | Nhân sự | API | Chatbot |
|-----|-----|---------|-----|---------|
| Cơ bản | Miễn phí | 2 | ❌ | ❌ |
| Nâng cao | 99.000đ/tháng | 4 | ❌ | ❌ |
| **Tăng trưởng** | **2.500.000đ/năm (~208.000đ/tháng)** | 15 | ✅ OpenAPI | ✅ |
| Premium | 399.000đ/tháng | 10 | ❌ | ❌ |

## Chi phí tin nhắn

- **8 tin đầu miễn phí** trong 48h từ lần cuối khách chat
- Sau 48h hoặc vượt 8 tin: **55đ/tin**
- Tặng 500 tin Tư vấn miễn phí/tháng (gói Tăng trưởng)
- API Rate Limit: 100 req/phút — thoải mái cho bot

## Tổng chi phí thực tế hàng tháng

~250.000-300.000đ (gói + vài trăm tin vượt mức)

## So sánh Telegram vs Zalo OA

| | Telegram | Zalo OA |
|---|---|---|
| Phí tháng | 0đ | ~250.000đ |
| Độ phủ VN | Thấp | Rất cao |
| API | Mở, dễ | Cần gói Tăng trưởng |
| Tin nhắn | Miễn phí | 55đ/tin sau 8 tin free |

## Cách tích hợp Hermes ↔ Zalo OA

1. Đăng ký Zalo OA doanh nghiệp (xác thực)
2. Đăng ký gói Tăng trưởng để có OpenAPI
3. Build bridge Python: Zalo webhook → Hermes API Server
4. Bot trả lời tự động khách hàng ngay trong Zalo
5. Hermes có API server nhận webhook từ bên ngoài — chỉ cần bridge nối 2 bên

## Lưu ý

- API Zalo đóng hơn Telegram, cần xác thực doanh nghiệp
- Gói Tăng trưởng là gói THẤP NHẤT có OpenAPI
- Nếu chỉ cần chatbot đơn giản (không Hermes), gói Nâng cao 99K/tháng đủ — nhưng mất tích hợp AI agent
- Telegram vẫn là kênh chính cho CEO bot nội bộ; Zalo OA cho khách hàng bên ngoài
