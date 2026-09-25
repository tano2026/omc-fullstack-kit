# 5 Dịch vụ Phòng Vé AI — Pricing & Tích hợp
> Cho skill ticketing-manager. Ngày: 20/07/2026

## Tổng quan

5 dịch vụ cốt lõi cho CTV/đại lý:
1. Vé máy bay — real-time (ABTrip AGT Cấp 1)
2. Fast Track Nội Bài — giá cố định (An Bình onsite 24/7)
3. Visa — giá cố định (partner API + thủ công)
4. Hộ chiếu online — chatbot hướng dẫn (ko có API)
5. eSIM du lịch — giá cố định (IST1 + Airalo)

## 1. Vé máy bay 🛫

**Hạ tầng:** ABTrip AGT Cấp 1 (test OK PNR PYVEP8, ZUG39P, ABT00349)
**Fallback:** Playwright scraper abtrip.vn
**LLM:** Gemini 2.5 Flash + OmniRoute
**MCP Flight:** search, filter, book

| Khoản mục | Giá TB | Margin |
|-----------|--------|--------|
| Vé nội địa | 1.5-3tr | 50-150K/vé |
| Vé quốc tế | 5-15tr | 200-500K/vé |

**Quy trình:** CTV chat tự nhiên → AI parse → search AGT → chọn chuyến → book → trả PNR

## 2. Fast Track Nội Bài 🛩️

**Nhà cung cấp:** An Bình Fast Track (chính chủ)
**USP:** Onsite staff 24/7 — đơn vị duy nhất tại HAN
**Brand:** Teal #006885 + Gold #DBA011 (đổi tên do quy định sân bay)
**Contact:** 0869.320.320 / info@fasttracknoibai.com

| Dịch vụ | Giá vốn | Giá bán lẻ | Giá CTV | Margin CTV |
|---------|---------|-----------|---------|-----------|
| Fast Track Arrival | 400K | 950K | 700K | 300K |
| Fast Track Departure | 350K | 850K | 620K | 270K |
| VIP B Lounge | 300K | 650K | 500K | 200K |
| Combo FT + Lounge | 650K | 1.4tr | 1.1tr | 450K |
| *Phụ thu đêm 23:00-06:00* | +200K | +300K | +250K | |

**Lợi thế cạnh tranh:** Đối thủ (Visana, Klook, GetYourGuide, Trip.com) đều là trung gian giá cao hơn 30-50%. An Bình có thể undercut vì là chính chủ.

## 3. Visa 🛂

**Phân khúc ưu tiên (margin cao nhất):**

| Loại Visa | Giá vốn | Giá bán | Margin | API |
|-----------|---------|---------|--------|:---:|
| E-Visa VN (cho người nước ngoài) | $25 | $45-60 | $20-35 | ✅ visa5s |
| Visa Trung Quốc | $45-70 | 2.7-3.3tr | 1.5-2tr | ✅ visanuocngoai |
| Visa Hàn Quốc multi 5 năm | $80-150 | 3.5-9.2tr | 2-5tr | ❌ Thủ công |

**Đối tác API:**
- visa5s.vn — E-Visa VN (REST API, margin 20-30%)
- visanuocngoai.vn — Visa TQ + Hàn + đa quốc gia (REST API, margin 15-50%)
- visacvip.com — Chuyên Trung Quốc (REST API, margin 15-25%)

**E-Visa VN flow:** Khách gửi ảnh passport + ảnh chân dung → AI điền form → thanh toán → auto submit evisa.gov.vn → trả PDF sau 3-5 ngày.

## 4. Hộ chiếu online 📄

**⚠️ KHÔNG có API public** từ Cục QL Xuất nhập cảnh / Bộ Công an.
**Lệ phí Nhà nước:** 100-200K (giảm 50% đến 12/2026).
**Phương án:** Chỉ chatbot hướng dẫn + template SMS/Email.
**Lý do giữ:** User muốn đủ 5 dịch vụ trong danh mục — khách hỏi là có câu trả lời.
**Không cần code** — chỉ canned response trong chatbot.

## 5. eSIM du lịch 📱

**Nhà cung cấp:**
- IST1 (có source code archive trong project abtrip) — VN + ĐNA, margin 15-25%
- Airalo Affiliate API — 200+ quốc gia, margin 10-20%, dễ tích hợp nhất

| Gói eSIM | Giá vốn | Giá bán | Margin |
|----------|---------|---------|--------|
| VN 7 ngày 3GB | $3-3.5 | 100-150K | 30-40K |
| VN 10 ngày 5GB | $5-6 | 120-200K | 40-60K |
| VN 15 ngày 10GB | $8-9 | 200-250K | 60-80K |
| Châu Á 7 ngày | $6-7 | 150-200K | 40-60K |
| Toàn cầu 7 ngày | $12-13 | 200-250K | 50-70K |

**Flow:** Chat → chọn gói → thanh toán → auto QR delivery (30s active).

## Mô hình kinh doanh 3 gói

| Gói | Giá | Đối tượng | Tính năng |
|-----|-----|-----------|-----------|
| CTV Cơ bản | Free | Cá nhân, bán lẻ | Chat AI book vé + 5 dịch vụ, margin chia sẻ |
| Đại Lý Pro | 199K/tháng | CTV chuyên | Dashboard riêng, hoa hồng cao hơn 5%, báo cáo |
| White-label | 1.5tr/tháng | Cty du lịch nhỏ | Brand riêng, API key, user riêng, full dashboard |

## Revenue dự kiến 1 CTV Pro

| Dịch vụ | Đơn/tháng | Margin/đơn | Revenue CTV |
|---------|:---------:|:----------:|:-----------:|
| Vé máy bay nội địa | 30 vé | 50-150K | 1.5-4.5tr |
| Vé máy bay quốc tế | 6 vé | 200-500K | 1.2-3tr |
| Fast Track | 5 đơn | 270-300K | 1.35-1.5tr |
| eSIM | 8 đơn | 40-60K | 320-480K |
| E-Visa VN | 2 hồ sơ | 300-500K | 600K-1tr |
| Visa TQ/Hàn | 1 hồ sơ | 1.5-2tr | 1.5-2tr |
| **Tổng** | | | **6.5-12.5tr/tháng** |

## Revenue platform (50 CTV Pro)

- Margin vé: 25-75tr
- Fast Track: 15-30tr
- eSIM: 2.5-5tr
- Visa: 5-15tr
- Phí Pro 50 CTV × 199K: ~10tr
- White-label 2 cty × 1.5tr: 3tr
- **Tổng: 55-130tr/tháng**

## Lộ trình Phase (12 tuần)

| Phase | Thời gian | Mục tiêu |
|-------|-----------|----------|
| P0 | Tuần 1-2 | Book vé được + Fast Track tay |
| P1 | Tuần 3-5 | 4/5 dịch vụ tự động |
| P2 | Tuần 6-8 | 3 gói CTV chính thức |
| P3 | Tuần 9-12 | Scale 50 CTV |

## Cashflow 6 tháng

- Tháng 1: -5tr (xây dựng)
- Tháng 2: +10tr (5 CTV)
- Tháng 3: +30tr (15 CTV)
- Tháng 4: +60tr (30 CTV)
- Tháng 5: +90tr (50 CTV)
- Tháng 6: +150tr (100 CTV)

> **Break-even:** Tháng 2
> **Kế hoạch đầy đủ:** `D:\MMO Du an\AI Agent Future\KE_HOACH_5_DICH_VU.md`
