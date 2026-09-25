# Pricelist User Corrections (Session Jul 2026)

## Font Sizing (user: "chữ bé quá")
All sizes increased +15-20% from initial design:

| Element | Initial (rejected) | Final (approved) |
|---------|:-:|:-:|
| body | 9pt | **10.5pt** |
| .svc-name | 8pt | **9.5pt** |
| .svc-detail | 6.8pt | **8pt** |
| .svc-en | 6.5pt | **7.5pt** |
| .price | 7.8pt | **9pt** |
| .price .usd | 6pt | **7pt** |
| h1 | 15pt | **16pt** |
| .tag | 5.5pt | **6.5pt** |
| .surcharge | 7pt | **8pt** |
| .policy-box | 7pt | **8pt** |
| .footer | 6.5pt | **7.5pt** |
| .cta-box | 7.5pt | **8.5pt** |
| .cta-box.big | 11pt | **12pt** |
| .meta | 7pt | **8pt** |

## Column Width (user: "cột STT rộng quá")
User progressively narrowed STT across 3 iterations:
1. Initial: width:24px → user said OK
2. Self-correction: 18px → user still unhappy
3. First reduction: 14px → user said "thu còn 8px thôi"
4. **Final: width:8px**

Key: user prefers **very narrow** counter column.

## Service Name Column
From 18% → 15% to give more room to Details.

## Details Column (user: "đỡ xuống dòng nhiều")
From 36% → 38-46% (maximized).

## Commission Tiers Removal
User explicitly said "mày bỏ cái ô này đi nhé" about the commission structure box in pricelist-agent.html.
Replace with: night surcharge warning instead.

## Night Surcharge (new addition)
User specifically asked to add: "bổ sung cái phần phụ thu ngoài giờ"
- Timing: 23:00-06:00
- Amount: +200,000₫/khách
- Applies: all Fast Track & VIP B services (NOT Lounge)
- Visual: yellow warning box `#FFF8E1` with `#DBA011` accent

## Excel Pricelist Corrections
User said "bản excel này ko khoa học lắm" — recreated with:
- Proper headers with teal bg
- Category rows with light teal bg
- Prices formatted as `[value]₫` (not `[value]₫`)
- Right-aligned price columns
- Night surcharge row highlighted
- Policy footer row
- Sheet names: FAST TRACK, LOUNGE (uppercase)
