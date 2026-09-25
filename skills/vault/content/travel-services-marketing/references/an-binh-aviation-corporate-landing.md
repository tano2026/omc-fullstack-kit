# An Bình Aviation — Corporate Landing Page Reference

**Built:** Jul 2026  
**Domain:** B2B Aviation Services (not B2C Fast Track only)  
**Approach:** Approach A (Traditional Multi-Section) with taste-skill agency-tier design

## Key Decisions

### Theme: Light, not Dark
- Hero + Header: White #FFFFFF (not navy #0F203D)
- Text: Navy #1B3A6B, body #4A4A52
- Accent: Teal #006885, Gold #DBA011
- User explicitly rejected dark theme as "khó đọc", "tối thui"
- **Lesson:** Default to light for Vietnamese SME corporate sites, even aviation

### Logo
- Located at `../../Logo/Horizontal/AB.Horizontal1.png`
- Header size: 48px, Footer: 42px
- Gold drop-shadow: `filter: drop-shadow(0 0 12px rgba(219,160,17,0.2))`

### Service Structure: 6 Pillars (not 5)
1. Đại Diện & Khai Thác Hãng Bay (Airlines Representation)
2. Pháp Lý & Điều Phối Bay (Permits & Slot)
3. VIP & Fast Track (VIP Services)
4. Hậu Cần & Tiện Ích (Crew Logistics)
5. Du Lịch Doanh Nghiệp (Corporate Travel)
6. Vé Máy Bay & Phòng Vé (Airline Ticketing) — added per user request

**Lesson:** Aviation companies separate operations (GSA/permits) from commerce (ticketing/GDS). Always have a ticketing card.

### Advisory Board
- User rejected: "bỏ phần Ban cố Vấn đi"
- Replaced with: "Tại Sao Chọn Chúng Tôi" (Why Choose Us)
- 3 reason cards: (1) Nội Bài Base (2) Đa Ngôn Ngữ (3) Pháp Nhân VN

### Language
- VI (primary) + EN (secondary italic) + CN (small tertiary)
- Added language switcher VI | EN | CN in header per user request
- Implementation: data-vi/en/cn attributes → JS innerHTML swap → localStorage

### Contact
- Hotline 0869.320.320 (24/7)
- Email info@fasttracknoibai.com
- WhatsApp +84 869.320.320
- Address: Tầng 3, Nhà ga T2, Nội Bài
- Form + WhatsApp FAB + 24/7 badge

## Tech Stack
- 1 file HTML, inline CSS+JS
- Plus Jakarta Sans + Prata (serif for headings)
- Phosphor Light icons
- No frameworks, no build step

## Pricing Sheet (separate)
- 3 versions: Full (3 col), Retail (1 col), Agent (2 col + commission)
- PDF output via Chrome headless `--print-to-pdf`
- Excel editable copy: `BaoGia_AnBinh_2026.xlsx`
- Surcharge: 23:00-06:00 +200K
