# Nguồn tra cứu hàng không

Tổng hợp các nguồn tra cứu cho ticketing/phòng vé.

## 1. Timatic — Visa & Xuất nhập cảnh

| Nguồn | URL | Ghi chú |
|-------|-----|---------|
| Emirates Timatic | https://www.emirates.com/timatic/ | **Nhanh nhất** — không cần đăng nhập |
| IATA Travel Centre | https://www.iatatravelcentre.com | Uy tín, tra visa/quy định |
| TimaticWeb | https://www.timaticweb.com | Cần tài khoản đại lý |

**Cách dùng:** Nhập quốc tịch + điểm đến + mục đích → kết quả ngay.
**Quy tắc:** LUÔN tra Timatic, không trả lời bằng kiến thức cũ.

## 2. Trạng thái chuyến bay thời gian thực

- **FlightRadar24 API** → tool `get_live_flight_status()` (đã tích hợp)
- **FlightRadar24 Web** → https://www.flightradar24.com/data/flights/
- **FlightAware** → https://flightaware.com (fallback)
- **MCP flight** trên VPS → qua OpenClaw gateway

## 3. Lịch bay & giá vé

- **Google Flights** → https://www.google.com/travel/flights
- **abtrip.vn** → Playwright (search + book thật)
- **API B2B** → chỉ test, không báo giá
- **Website hãng** → chính sách chính thức

## 4. Sơ đồ ghế máy bay

- **Aerolopa** → https://www.aerolopa.com (đã tích hợp tool)
- **SeatGuru** → https://www.seatguru.com (fallback)

## 5. Sun PhuQuoc Airways (9G) — Full-service Leisure Carrier

**IATA:** 9G | **ICAO:** SPQ | **Callsign:** SUN LUX
**Owner:** Sun Group | **Commercial flights:** From 01/11/2025
**Hubs:** PQC (Phú Quốc), SGN, HAN
**Fleet:** 10 planes (A320neo, A321-200, A321neo) + 34 orders (A330-200, B787-9)
**Website:** sunphuquocairways.com

### Routes
**Domestic:** PQC↔SGN, PQC↔HAN, PQC↔DAD (primary), HAN↔SGN, SGN↔DAD, HPH (from 25/07/2026), CXR, VDO
**International:** TPE, ICN, HKG (active); SIN (from 25/07), BKK (from 08/08)

### Baggage (included in fare — full-service)
| Class | Hand | Checked |
|-------|------|---------|
| Economy | 7kg (1pc) | **23kg** (1pc free) |
| Business | 14kg (2pc) | **46kg** (2×23kg free) |

**Key talk:** "9G la hang full-service, gia da bao gom 23kg ky gui. Khong phai mua them nhu LCC (VJ)."

## 6. Knowledge tools in ai_agent.py

All 4 new knowledge tools use in-memory Python dicts (no DB):
| Tool | Purpose |
|------|---------|
| `explain_fare_policy(airline, fare_class)` | Chính sách đổi/hoàn/hành lý 5 hãng |
| `get_baggage_allowance(airline)` | Hành lý xách tay + ký gửi chi tiết |
| `get_checkin_guide(airline)` | Hướng dẫn check-in online + sân bay |
| `check_visa_requirement(nat, dest)` | Tra visa-style cho 7 tuyến phổ biến |

## 7. Cross-reference: Web data vs GDS

⚠️ **Codeshare/Wet-lease detection:** Google Flights may show flights that are NOT bookable via Amadeus. Check operating carrier → GDS distribution.
|------|---------|---------|------|-----------------|
| Vietnam Airlines | vietnamairlines.com | VN | Full-service | 23kg (Eco), 32kgx2 (Biz) |
| Vietjet Air | vietjetair.com | VJ | LCC | 0kg (Eco), 20-40kg (mua thêm) |
| Bamboo Airways | bambooairways.com | QH | Full-service | 23kg (Eco), 32kgx2 (Biz) |
| Vietravel Airlines | vietravelairlines.vn | VU | LCC | 0-20kg (tùy vé) |
| Sun PhuQuoc Airways | sunphuquocairways.com | 9G | Full-service leisure | **7+23kg MIỄN PHÍ** (Eco), 14+46kg (Biz) |

Đã tích hợp tools: `explain_fare_policy()`, `get_baggage_allowance()`, `get_checkin_guide()`, `check_visa_requirement()`.

## 6. Timatic — Nguồn Tra Cứu Nhanh
- **Emirates Timatic** (tra nhanh không cần login): https://www.emirates.com/timatic/
- **IATA Travel Centre**: https://www.iatatravelcentre.com
- **Cách dùng Emirates Timatic**: Nhập quốc tịch + điểm đến + mục đích → kết quả ngay
- **Lưu ý:** Quy định visa thay đổi liên tục. LUÔN tra Timatic, KHÔNG trả lời bằng kiến thức cũ.
