# Chat API — Intent Parser V3 (July 2026)

## Overview

The ABTrip chat bot (`POST /api/chat`) uses a **rule-based intent parser** (not LLM) for fast, cost-effective parsing. LLM is only called as fallback when intent parser can't classify the query.

## Architecture

```
User Message
  │
  ├── STEP 0: Check pending_action (confirm_search / awaiting_confirm)
  │     └── handle confirm/cancel/re-parse
  ├── parse_flight_search() + classify_intent()
  ├── STEP 2-3: search_flight → check_missing → clarify/confirm
  ├── STEP 4: policy intents → local response dict
  └── STEP 5: LLM fallback (OmniRoute → DeepSeek V4)
```

## Key Components

### 1. Intent Classification (`classify_intent()`)
- Checks policy keywords first (baggage/change/cancel/documents/general)
- Then fare rule, retrieve booking, booking, flight search
- Falls through to location slang check, airline info, greeting

### 2. Flight Search Parser (`parse_flight_search()`)
- Word-boundary matching on `_LOCATION_SLANG` dict (60+ entries)
- De-duplicate overlapping matches (keep longest) AND same-code duplicates
- Partial match support (single location returned instead of None)
- Direction keywords: "đi/đến/vào/ra/về" → destination, "từ/ở/tại" → origin
- Date parsing: DD/MM, DD-MM, DD/MM/YYYY, Vietnamese "DD tháng MM", English "July 20", relative (ngày mai, ngày kia, cuối tuần)
- Passenger count: supports "pax", "người", "khách", "vé", "nguoi"
- Cabin class: business detection

### 3. Slang & Dialect Support

#### Airport Slang (60+ entries)
```
"sg" → SGN, "hn" → HAN, "dng" → DAD, "pq" → PQC
"tphcm" → SGN, "saigon" → SGN, "sgn" → SGN
"hcm" → SGN (careful: substring of "hành" in "hành lý" — fixed by word boundaries)
"bmt" → BMV (Buôn Ma Thuột)
"nt" → CXR (Nha Trang)
"krung thep" → BKK (Bangkok — Vietnamese slang)
"dai bac" → TPE (Đài Bắc — Vietnamese)
```

#### Date Slang
| Input | Parsed as |
|-------|-----------|
| "ngày mai", "mai" | tomorrow |
| "ngày kia" | day after tomorrow |
| "hôm nay", "bữa nay", "hôm ni" | today |
| "cuối tuần" | next Saturday |
| "tuần sau" | +7 days |
| "5/7" | 05/07 |
| "5 tháng 7" | 05/07 |
| "July 20", "Jul 20", "july 20th" | 20/07 |

#### Ticket Office Slang
| Input | Intent |
|-------|--------|
| "có hàng" | search_flight (ticket availability) |
| "kiểm tra hàng" | search_flight |
| "còn hàng" | search_flight |
| "báo giá" | search_flight |
| "chốt vé" | book_flight |
| "xuất vé" | book_flight |

#### Flight Slang (domain-specific vocabulary that misleads LLMs)
| Word | Everyday meaning | **In ABTRIP** |
|------|-----------------|---------------|
| "hàng" | goods/products | **Ticket inventory availability** |
| "giá" | price | **Fare** |
| "chặng" | road segment | **Flight segment** |
| "chốt" | conclude | **Finalize booking** |
| "cọc" | deposit | **Hold booking** |
| "xuất" | print/export | **Issue ticket** |

> **CRITICAL RULE for "hàng":** When user says "Có hàng chưa" in ABTRIP context, 99% means "Check ticket availability" — NOT goods, NOT repo code. Search flights immediately.

### 4. Confirm Flow (Session State Machine)

```
state: None
  ↓ user sends flight query with all info
state: confirm_search
  → asks "Xác nhận tìm?" (OK/Có)
  ↓ user says OK
state: None
  → executes search, returns results (type: "flight_results")

state: None
  ↓ user sends incomplete query (missing date/destination)
state: awaiting_confirm
  → asks specific question
  ↓ user responds (re-parses with context merge)
state: awaiting_confirm → confirm_search
  → asks "Xác nhận tìm?"
```

#### Context Merge Fix (July 21):
When re-parsing user's response during `awaiting_confirm`, the context MUST include ALL known fields from `pending_data`:
```python
reparse_context = message
for _c_key in ("origin", "destination", "date", "adults", "children"):
    if parsed.get(_c_key):
        reparse_context += " " + str(parsed.get(_c_key))
```
Previously only appended date → `"ngày mai"` alone failed to parse because no location words.

### 5. Policy Intents (Local Handler)

Handled BEFORE LLM fallback to avoid LLM misclassifying:

| Intent | Response |
|--------|----------|
| `policy_baggage` | Hand luggage rules + airline-specific baggage |
| `policy_change` | Change fee policies per airline |
| `policy_cancel` | Cancellation / refund policies |
| `policy_documents` | Airport procedures, ID requirements |
| `policy_general` | Menu of policy options |

## Test Results (July 21, 2026)

### Intent Parser — 24/24 slang tests passed
All Vietnamese slang, dialect, text-speak, English dates, business class, multi-passenger variations parsed correctly.

### API Tests — 27 tests total
- **A. Slang/Dialect (12/12)** — all confirm/clarify with correct Vietnamese names
- **B. Policy (5/5)** — correct policy response for baggage/change/cancel/documents/general
- **C. Greetings (3/3)** — standard greeting responses
- **D. Confirm Flow (4/4)** — multi-turn clarify→confirm→search flow works
- **E. Extra fields (1/1)** — extra JSON fields don't crash API

## Bugs Found & Fixed

| # | Bug | Fix | Date |
| * | **VPS deploy: externally-managed Python** | Create venv with `python3 -m venv .venv` + use `.venv/bin/python` in systemd ExecStart. Cannot pip install system-wide on Ubuntu 24.04. Use `requirements.txt` with only needed deps (not full pip freeze which pulls audioop-lts needing Python 3.13+). | Jul 21 |
| * | **Debug file path leak caused 500 on VPS** | Removed `open(r"C:/Users/Nguyen Ngoc Tan/debug_session.txt")` from chat.py — local Windows path doesn't exist on VPS. Always grep for `C:/Users/` debug paths before VPS deploy. | Jul 21 |
| * | **VPS deploy: no rsync on Windows** | Windows lacks rsync. Use `tar czf /tmp/deploy.tar.gz --exclude='__pycache__' --exclude='.venv' --exclude='deploy' . && scp ... && ssh ... tar xzf` pattern. Deploy script at `backend/deploy/deploy.sh`. | Jul 21 |
| * | **VPS deploy: verify .env after scp** | The production .env file must exist on VPS after deploy. Check: `ssh ubuntu@HOST ls -la /opt/abtrip-backend/.env`. Missing .env causes defaults to take effect (wrong URLs/empty keys). | Jul 21 |
| * | **Test suite design flaws** | Fixed: fresh UUID per test (session contamination), correct expected types (`flight_results` not `text`), Vietnamese name validation (word-boundary regex, not substring), policy content check (2+ keywords or 1 specific keyword) | Jul 21 |
|---|-----|-----|------|
| 9 | Policy intent hijacked by flight search path | Added `policy_responses` dict handler before LLM fallback | Jul 21 |
| 10 | `_reverse_location` showed English names ("tan son nhat") | Used `_AIRPORT_VIET` dict in `generate_clarify_question` | Jul 21 |
| 11 | Removing "sg" from dict broke 11 tests | Special handling for same-code duplicate match suppression | Jul 21 |
| 12 | Model preference: DeepSeek V4/R1 preferred over Gemini 2.5 Flash | Added to skill preference | Jul 21 |
| 17 | English date "July 20" regex fails | Full month name pattern + `[:3]` extract for month_map lookup | Jul 21 |
| 18 | Test session contamination between tests | Added fresh `uuid.uuid4()` session_id per test | Jul 21 |
| 19 | Partial match for single-location queries | Return parsed dict even with only 1 location | Jul 21 |
| 20 | `awaiting_confirm` reparse lost context | Full context merge from pending_data | Jul 21 |

## Deployment

- **Local:** port 8138 (FastAPI + uvicorn)
- **VPS:** systemd service `abtrip-backend` at `/opt/abtrip-backend`
- **VPS deploy script:** `backend/deploy/deploy.sh` (tar+scp, uv)
- **VPS resources:** ~90MB RAM, 2 workers, Python 3.12 venv
