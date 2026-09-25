# Domain Vocabulary — ABTRIP Ticketing (Intent Parser)

## Words that mislead LLMs

In ABTRIP ticketing context, these words have **domain-specific meanings** different from everyday usage:

| Word | Everyday meaning | In ABTRIP | Example |
|------|-----------------|-----------|---------|
| "hàng" | goods/products | **Ticket inventory / availability** | "Có hàng SG-HN không?" = "Are there tickets available SGN→HAN?" |
| "giá" | price | **Fare / ticket price** | "Báo giá HN-PQ" = "Quote fare HAN→PQC" |
| "chặng" | road segment | **Flight segment** | "Chặng SG-HN mấy tiếng?" = "How long is the SGN→HAN segment?" |
| "mở" | open | **Ticket sale opens** | "Khi nào mở bán?" = "When does the sale open?" |
| "đóng" | close | **Ticket sale closes / deadline** | "Đóng bán lúc nào?" = "What's the ticketing deadline?" |
| "chốt" | conclude | **Finalize booking / issue ticket** | "Chốt vé giúp em" = "Finalize/issue the ticket for me" |
| "cọc" | deposit | **Hold booking with deposit** | "Cọc vé này giữ chỗ" = "Put a deposit on this ticket to hold" |
| "xuất" | print/export | **Issue ticket** | "Xuất vé cho khách" = "Issue the ticket for the passenger" |
| "hủy" | discard | **Cancel booking / refund ticket** | "Hủy booking này giúp" = "Cancel this booking" |

## Slang dictionary (currently in `intent_parser.py`)

### Ticket office slang:
- "có hàng" → check availability
- "kiểm tra hàng" → check availability
- "còn hàng" → check availability
- "báo giá" → quote price
- "xin giá" → quote price
- "có vé" → check availability
- "chốt vé" → book / finalize
- "xuất vé" → issue ticket
- "mua vé" → book flight

### Airport code slang (notable ones):
- "sg" → SGN (but conflicts with "tphcm", "saigon") — use word-boundary matching
- "hn" → HAN
- "dng" → DAD (Đà Nẵng)
- "bmt" → BMV (Buôn Ma Thuột)
- "nt" → CXR (Nha Trang / Cam Ranh)
- "pq" → PQC (Phú Quốc)
- "krung thep" → BKK (Bangkok — Vietnamese slang)
- "dai bac" → TPE (Đài Bắc)
- "tphcm" → SGN

### Date slang:
- "bữa nay", "hôm ni" → today
- "ngày kia" → day after tomorrow
- "July 20", "july 20th" → 20/07 (English format with full month name)

## Intent classification priority order

When `classify_intent()` runs, it checks in this order:

1. Policy baggage keywords (hành lý, xách tay, ký gửi...)
2. Policy change/cancel/documents/general
3. Fare rule / retrieve booking / book intent
4. Flight search (if location slang or search keywords match)
5. Greeting / default

**Critical:** Policy MUST be checked before flight search, otherwise "hành lý VNA bao nhiêu kg" gets classified as search (because "hành" substring matches). Fixed via word-boundary matching.
