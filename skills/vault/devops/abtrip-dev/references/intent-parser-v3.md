# Intent Parser V3 — ABTrip Ticketing Bot

Source: `backend/app/services/intent_parser.py`

## Architecture

Rule-based intent parser (no LLM calls for simple queries — cheaper, faster):

```
user message
  → parse_flight_search()       # Extract structured search params
  → classify_intent()           # Determine intent type
  → check_missing_info()        # What's still needed
  → generate_clarify_question() # Vietnamese human-readable question
```

## Intent Types

| Intent | Trigger | Action |
|--------|---------|--------|
| `search_flight` | Location + date keywords | Confirm → search |
| `policy_baggage` | "hành lý", "xách tay", "bao nhiêu kg" | Local response |
| `policy_cancel` | "hủy", "hoàn vé" | Local response |
| `policy_change` | "đổi vé", "thay đổi" | Local response |
| `policy_documents` | "giấy tờ", "cần mang" | Local response |
| `policy_payment` | "thanh toán", "trả góp" | Local response |
| `greeting` | "chào", "xin chào", "hello" | Welcome message |
| `general` | Fallthrough | LLM gateway |

## Slang & Dialect Support (60+ entries)

`_LOCATION_SLANG` dictionary maps Vietnamese slang/abbreviations to IATA codes:

```python
_LOCATION_SLANG = {
    "sg": "SGN", "sgn": "SGN", "saigon": "SGN", "tphcm": "SGN",
    "tp.hcm": "SGN", "tân sơn nhất": "SGN", "tan son nhat": "SGN",
    "hn": "HAN", "hanoi": "HAN", "hà nội": "HAN", "ha noi": "HAN", "nội bài": "HAN",
    "dng": "DAD", "d nẵng": "DAD", "dn": "DAD", "đà nẵng": "DAD",
    "pq": "PQC", "phú quốc": "PQC", "phu quoc": "PQC",
    "nt": "CXR", "nha trang": "CXR",
    "hp": "HPH", "hải phòng": "HPH", "hai phong": "HPH",
    "dl": "DLI", "đà lạt": "DLI", "da lat": "DLI",
    "hue": "HUI", "huế": "HUI",
    "vt": "VII", "vinh": "VII", "vinh": "VII",
    "ct": "VCA", "cần thơ": "VCA", "can tho": "VCA",
    "bt": "BMV", "ban mê thuột": "BMV", "buôn ma thuột": "BMV",
    "py": "UIH", "quy nhơn": "UIH", "quy nhon": "UIH",
    "tuy hòa": "TBB", "tbb": "TBB",
}
```

## Date Parsing

Supports multiple formats:
- `DD/MM` / `DD/MM/YYYY` — "20/7", "20/07/2026"
- `DD-MM` / `DD-MM-YYYY`
- English: `Month DD` — "July 20", "Jul 20", "july 20th"
- Relative: "ngày mai", "mai", "ngày kia", "ngày mốt"
- Vietnamese: "mùng X tháng Y"

## Confirm Flow

```
Step 0: Parse → classify
Step 1: If search_flight + missing info → clarify question
Step 2: User provides more → merge with pending_data
Step 3: Complete → show confirmation → "OK? (gõ OK/Có)"
Step 4: User says OK → search → flight_results
Step 4: Non-search intent (policy) → local response
```

## De-duplicate Logic

`_find_locations()` uses `matched_codes = set()` to prevent double-matching same IATA code (e.g., `"sg tphcm"` → only 1 SGN, not 2).

## Vietnamese Airport Names

`_AIRPORT_VIET` dict in `convert_to_vietnamese_name()` maps IATA → familiar Vietnamese names for clarify questions:
```
SGN → TP.HCM, HAN → Hà Nội, DAD → Đà Nẵng, CXR → Nha Trang, etc.
```

## Test Coverage

27 end-to-end tests in `agent.tkt/abtrip_full_test.py` (categories A-E):
- A: Slang/dialect parsing (12 tests)
- B: Policy intents (5 tests)
- C: Greetings (3 tests)
- D: Multi-turn confirm flow (4 tests + 1 follow-up command)
- E: Extra fields tolerance (1 test)
