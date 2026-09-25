# Flight Parameter Extraction — Regex + Airport Alias Map

Path: `backend/app/services/smart_agent.py`
Functions: `_extract_flight_params()`, `_format_flight_results()`

## Airport Alias Map (`_AIRPORT_ALIAS`)

Maps Vietnamese names/abbreviations → IATA codes. 25 airports covering all domestic routes:

```python
_AIRPORT_ALIAS = {
    # Sài Gòn / Tân Sơn Nhất
    "sg": "SGN", "sgn": "SGN", "sài gòn": "SGN", "saigon": "SGN", "hcm": "SGN",
    # Hà Nội / Nội Bài
    "hn": "HAN", "han": "HAN", "hà nội": "HAN", "hanoi": "HAN",
    # Đà Nẵng
    "đn": "DAD", "dad": "DAD", "đà nẵng": "DAD", "danang": "DAD",
    # Nha Trang / Cam Ranh
    "nt": "CXR", "nha trang": "CXR", "nhatrang": "CXR", "cam ranh": "CXR",
    # Phú Quốc
    "pq": "PQC", "phú quốc": "PQC", "phu quoc": "PQC",
    # Hải Phòng
    "hp": "HPH", "hải phòng": "HPH", "haiphong": "HPH",
    # Huế
    "huế": "HUI", "hue": "HUI",
    # Đà Lạt
    "dl": "DLI", "đà lạt": "DLI", "dalat": "DLI",
    # Vũng Tàu / Côn Đảo
    "vt": "VCA", "vũng tàu": "VCS", "vung tau": "VCS", "côn đảo": "VCS",
    # Buôn Ma Thuột
    "bm": "BMV", "buôn mê": "BMV", "buon me": "BMV",
    # Thanh Hóa
    "thanh hóa": "THD", "thanh hoa": "THD",
    # Đồng Hới / Vinh
    "vđ": "VDH", "vinh": "VII", "đồng hới": "VDH", "dong hoi": "VDH",
    # Quy Nhơn
    "quy nhơn": "UIH", "quy nhon": "UIH",
    # Tuy Hòa
    "tuy hoà": "TBB", "tuy hoa": "TBB",
    # Pleiku
    "pleiku": "PXU",
    # Cần Thơ
    "cần thơ": "VCA", "can tho": "VCA",
    # Rạch Giá
    "rách giá": "VKG",
    # Cà Mau
    "cà mau": "CAH",
}
```

## Origin-Destination Regex Patterns

3 patterns tried in order, first match wins:

```python
od_patterns = [
    # Pattern 1: "từ X đến Y" / "bay từ X đi Y"
    r"(?:từ|bay từ|đi từ)\s+(\S+(?:\s+\S+)?)\s+(?:đến|đi|sang|vào|ra)\s+(\S+(?:\s+\S+)?)",
    # Pattern 2: "X đến Y" / "X -> Y" / "X → Y"
    r"(\S+)\s+(?:đến|=>|->|→|—)\s+(\S+)",
    # Pattern 3: "vé từ X đi Y" / "vé X sang Y"
    r"vé\s+(?:từ\s+)?(\S+(?:\s+\S+)?)\s+(?:đi|đến|sang)\s+(\S+(?:\s+\S+)?)",
]
```

**Note:** Matched text is looked up in `_AIRPORT_ALIAS` first. If not found, takes first 3 uppercase chars of the matched text. This means "hcm" → SGN (alias match), but "CDG" → CDG (pass-through for international codes).

## Date Parsing Rules

3 patterns, priority order:

| Pattern | Example | Output |
|---|---|---|
| `(\d{1,2})[/-](\d{1,2})(?:[/-](\d{2,4}))?` | `15/8`, `15-08-2026` | `15082026` |
| `ngày\s+(\d{1,2})\s*(?:tháng\s*)?(\d{1,2})` | `ngày 15 tháng 8` | `1508YYYY` |
| Relative keywords | `mai`, `ngày mai`, `mốt`, `hôm nay` | today±offset |

Year defaults to current year if omitted. 2-digit years (<100) get +2000.

## Passenger Count

Regex: `(\d+)\s*(?:người|khách|pax|ng)`
Default: 1

## AGT Results Format (`_format_flight_results`)

Shows top 5 cheapest flight groups from `ListGroup`:
- Airline name from `ListAirOption[0].AirlineName`
- Cheapest fare: `ListFareOption[0].TotalFare` + `FareClass` + `FareType`
- If >5 groups: appends "(và N lựa chọn khác)"
- Footer: "📌 Chọn chuyến để giữ chỗ"

## Hook Location in Chat Endpoint

In `POST /api/smart-agent/chat`, after Gemini returns text and history is stored:

```python
# --- AGT flight search for booking flows ---
# ⚠️ Condition is `not is_ops` — NOT `flow == "booking"`. There is no local
#    `flow` variable; `req.flow` exists but `is_ops` already distinguishes the paths.
if not is_ops:
    recent_msgs = [h["content"] for h in history[-8:] if h["role"] == "user"]
    fp = _extract_flight_params(recent_msgs)
    if fp:
        try:
            agt_client = ABTripClient()
            # ⚠️ Correct signature: system="" (all airlines), routes=[{StartPoint,EndPoint,DepartDate}]
            #    NOT origin=/destination=/depart_date= (TypeError) and NOT Origin/Destination keys
            #    (spec uses StartPoint/EndPoint — wrong keys silently yield an empty route → no flights).
            #    DepartDate must be ddMMyyyy (e.g. "23082026"); yyyyMMdd returns groups with no real segments.
            result = await agt_client.search_flight(
                system="", adt=fp["adt"],
                routes=[{"StartPoint": fp["from"], "EndPoint": fp["to"], "DepartDate": fp["date"]}],
            )
            flight_text = _format_flight_results(result, fp)
            text = flight_text + "\n" + text
        except Exception as e:
            text = f"⚠️ ...{error prefix}...\n\n" + text
```

## Credential Source

Docker-compose.local.yml env block (authoritative for local):
```
- AGT_API_HOST=https://api-abtrip.timtrungtam.com/v1
- AGT_PRIVATE_KEY=a3f2b9e1c8d4a7f6b2e0c9d5a4b1f8d32
- AGT_API_ACCOUNT=ABTRIP
- AGT_API_PASSWORD=CtTXgjVX8AQ1
```

These override whatever the VPS `.env` file says (which still has the dead `api.abtrip.vn` domain).
