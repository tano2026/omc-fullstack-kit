# Research: Phòng Vé AI Mini Cho CTV — "Bán cần câu, ko bán cá"

> Tham khảo cho business model layer trên nền tảng ticketing-manager. File này chứa research tổng hợp thị trường CTV du lịch VN.

## Mô hình chiến lược

Cung cấp GIẢI PHÁP phòng vé mini cho CTV/đại lý/hotel, không bán lẻ cho khách cuối. 3 gói:

| Gói | Giá | Target |
|-----|-----|--------|
| CTV Cơ Bản | Miễn phí | Sinh viên, người mới |
| Đại Lý Pro | 199K/tháng | CTV chuyên, phòng vé nhỏ |
| White-label Hotel | 1.5tr/tháng | Hotel, DMC, Travel agency |

## Thị trường CTV

- **150K-250K CTV** (part-time 100-150K, full-time 30-50K, đại lý nhỏ 20-30K)
- **95% dùng Zalo, 80% Excel** — thủ công gần như hoàn toàn
- **Chỉ 2-3% dùng AI** — khoảng trống mênh mông
- Thu nhập: part-time 2-8tr, full-time 8-15tr, đại lý 30-100tr/tháng
- Pain points: check giá chậm (10-30 phút), ko có dashboard so sánh, cập nhật KM rời rạc
- Group FB chính: Hội CTV Du Lịch VN (~50K), Hội Bán Tour Online (~80-100K)

## Đối thủ — điểm yếu chết người

| Đối thủ | Điểm yếu |
|---------|----------|
| BestPrice | Không có tool cho CTV cá nhân (chỉ B2B đại lý có pháp nhân) |
| Vé Tốt | Không có affiliate/CTV — web bán lẻ thuần |
| Traveloka Affiliate | Hoa hồng 0.5-1% (quá thấp), tracking kém, support EN, ko đặt hộ được |
| VNTravel | Tool sơ sài, hay lỗi, load chậm, quy trình phức tạp |
| iVivu | Dashboard cũ kỹ, ko đặt hộ, UX tồi |

**Khoảng trống:** Không đối thủ nào có tool **tự động cho CTV** (so sánh giá, book hộ, tracking hoa hồng real-time).

## Hotel/DMC tiềm năng

- **12K-15K hotel nhỏ (30-50 phòng)** cần phòng vé nhưng ko đủ sức nuôi NV riêng
- **500-800 DMC vừa & nhỏ** xử lý 200-500 booking/tháng, sẵn sàng chia 30-50% hoa hồng
- Cơ hội đặc biệt cho Fast Track/Lounge Nội Bài — exclusive, đối thủ không có

## Pháp lý & Vận hành

- Ko cần giấy phép lữ hành (chỉ vé bay thuần) — Luật Du lịch 2017
- **BẮT BUỘC** đăng ký GPKD (hộ KD ~500K)
- Rủi ro lớn nhất: CTV bùng nợ → ký quỹ 5-10tr/CTV + KYC
- Payment: ký quỹ + chuyển khoản + webhook (Selly/Onepay)
- ABTrip API có rate limit: ~10-30 req/s, cần cache + queue

## Số liệu thị trường VN

- Vé nội địa: ~50-52 triệu vé (2025E), CAGR 8-10%
- Thị trường: ~210.000-230.000 tỷ (2025E)
- Online booking penetration: 55-60% — **40% vẫn offline** (~80.000-90.000 tỷ)
- Tăng trưởng online travel: CAGR ~22%, $3.5B (2023) → $5.2B (2025E)
- Visa mở rộng, T3 TSN + Long Thành sắp vận hành

## Cửa sổ cơ hội

**12-18 tháng** — trước khi OTA lớn (Traveloka, VNBooking) ra AI agent. First-mover ở mảng AI check giá + so sánh đa hãng cho CTV.

*Research bởi TANO-AGENCY, 20/07/2026. Nguồn: web search + tổng hợp từ 6 research subagents.*
