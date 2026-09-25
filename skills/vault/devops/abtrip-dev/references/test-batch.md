# AGT Booking Integration — Batch Test Script

Quick 7-case test suite for the `POST /api/smart-agent/chat` endpoint with AGT flight search wired in.

**Script location:** `D:\MMO Du an\TANO-AGENCY\PROJECTS\abtrip\test_batch.py`

## Prerequisites

Server must be running on port 8765 with AGT env vars set:

```bash
cd "D:/MMO Du an/TANO-AGENCY/PROJECTS/abtrip/backend" && \
AGT_API_HOST="https://api-abtrip.timtrungtam.com/v1" \
AGT_API_ACCOUNT="ABTRIP" AGT_API_PASSWORD=*** \
AGT_PRIVATE_KEY="a3f2b9e1c8d4a7f6b2e0c9d5a4b1f8d32" \
GEMINI_API_KEY=*** \
python -u -m uvicorn app.main:app --host 0.0.0.0 --port 8765 --log-level warning
```

Note: Clear `__pycache__` before restart if you've patched any `.py` files (see Pitfall #32).

## Run

```bash
cd "D:/MMO Du an/TANO-AGENCY/PROJECTS/abtrip" && python test_batch.py
```

## Test Cases

| # | Label | Input | Expected Signal |
|---|-------|-------|-----------------|
| 1 | VeSG-HN | `vé SG đi Hà Nội mai, 1 người` | ✈️ flight results + 💰 prices |
| 2 | Alias-DN | `vé sài gòn đến đà nẵng thứ 7, 2 người` | ✈️ flight + 💰 prices + alias resolved |
| 3 | DateNum | `vé HAN vào SGN ngày 15/8, 3 người` | ✈️ flight + dd/mm parsed correctly |
| 4 | OpsRefund | `chính sách hoàn vé máy bay` | 📚 RAG context injected |
| 5 | Missing | `vé đi Hà Nội ngày mai` | ❓ bot asks for missing origin |
| 6 | Short | `hn → sgn mai` | ✈️ short alias resolved |
| 7 | HCM-NT | `vé HCM đi Nha Trang ngày 20/8` | ✈️ HCM→CXR route |

## Success Criteria

- All 7 tests return HTTP 200
- No `name 'flow' is not defined` errors
- Tests 1-3, 6-7 show flight results with prices from AGT API
- Test 4 shows RAG context (policy/hoàn vé keywords)
- Test 5 shows a clarification question (bot asks for missing info)
