# Kế Hoạch Mở Rộng 5 Dịch Vụ — ABTrip Platform

> **Context:** July 2026 — user wants to keep all 5 services (flight, fast track, visa, eSIM, passport) on ONE landing page for selling, not an OPC/dashboard.
> **Hạ tầng sẵn có:** ABTrip FastAPI backend (port 8138), AGT API client, LLM Gateway (OmniRoute), Next.js frontend (22 components, 3 tabs).

## 5 Dịch Vụ — Chiến Lược Từng Cái

| # | Dịch Vụ | Giá | Hạ Tầng | API? | Tự Động? | Vai Trò |
|---|---------|-----|---------|------|---------|---------|
| 1 | ✈️ Vé máy bay | Real-time | AGT API + Playwright | ✅ Có | ✅ Cao | Món chính, keo dính |
| 2 | 🛂 Fast Track NB | Cố định | An Bình (chính chủ) | ❌ Manual | 🟡 Trung bình | Margin cao, độc quyền |
| 3 | 🛂 Visa | Cố định | Partner thủ công | ❌ Manual | ❌ Thấp | Margin cao nhất (1.5-5tr) |
| 4 | 📱 eSIM | Cố định | IST1 / Airalo | ❌ Tùy | 🟡 Trung bình | Cross-sell, auto delivery |
| 5 | 🆔 Hộ chiếu | Cố định | Không có | ❌ | ❌ | Chỉ tư vấn, ko bán |

## UX Priority

**User preference:** Landing page bán hàng **duy nhất**, không dashboard quản lý.

1. **Hero search** — form search flight (chiếm 70% không gian)
2. **Service tabs** — 4 tab (bỏ hộ chiếu khỏi tabs, chỉ tư vấn trong chat)
3. **Chat AI** — 1 chat cho tất cả dịch vụ, ko cần agent switching
4. **Kết quả** — flight card + Fast Track card + eSIM card inline trong chat

## Ai Làm Research?

**User preference (July 2026):** "từ nay mỗi lần cần hẹn research làm gì thì mày gọi thẳng tao chứ đừng dispatch qua agent khác"

→ Research tự làm với terminal + web_search, không dispatch delegate_task cho research.
