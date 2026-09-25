# VPS Architectural Notes (20/06/2026 — Round 3)

## ai_agent.py patch results

After 22 patch iterations (v1→v22), the following was deployed successfully:

### ✅ Deployed (SYNTAX PASSED)

| Patch | Change | Status |
|-------|--------|--------|
| Required fields | `book_flight` only needs `passenger_name` | ✅ |
| 4 knowledge tools | `explain_fare_policy`, `get_baggage_allowance`, `get_checkin_guide`, `check_visa_requirement` | ✅ |
| `else:` fallback | Replaced `return f"Lỗi..."` with proper `else:` block | ✅ |
| System prompt | "Đặt vé linh hoạt. Hỏi giới tính + SĐT. Auto DOB=1990-01-01, email=info@abtrip.vn" | ✅ |
| `_try_flight_select` | Replaced f-string eval with `page.evaluate(js, fn)` | ✅ Syntax |
| Server restart | HTTP 200 | ✅ |

### ❌ Not deployed (broken book_flight — DOM structure)

**Root cause:** abtrip.vn uses Next.js SPA. Flight card "Chọn" buttons are `<SPAN>` elements, not `<BUTTON>`. The old `_try_flight_select` and `book_flight` code never matched the DOM.

**DOM discovered:**
```
DIV.air-item → DIV.flight-present → DIV.flight-sum → DIV.airline-logo → SPAN.flight-num (flight number)
DIV.air-item → DIV.flight-present → DIV.flight-action-select → DIV.action-button → SPAN "Chọn"
```

- `querySelectorAll('button')` on search results page = 0 elements
- Submit "Đặt vé" IS a `<BUTTON>`, but "Chọn" is `<SPAN>`
- Page loads in ~6-9s (retry loop: 3s × 8 iterations, check for `"Có " in body and " chuyến bay" in body`)

**patch_bookflow.py** was written but failed syntax due to leftover code from patch_select.py overlapping with old code. Need to:
1. Restore `abtrip_browser.py` from clean backup
2. Apply one atomic patch that replaces the entire `book_flight` function

### Key indent rule for patching ai_agent.py

When inserting into `execute_tool()`:
- `try:` block body = 8 spaces (indent level 2)
- `if func_name == "..." / elif func_name == "..."` = 8 spaces
- Body of each handler = 12 spaces
- `else:` (fallback) = 8 spaces, its body = 12 spaces
- Knowledge tools (k_tools) body = 8 spaces (same level as `elif func_name`)
- `text.rfind("return f\"Lỗi\"")` with the exact string from the .bak file is the reliable insertion marker

## Patch deployment checklist

```bash
# 1. SCP patch script
scp -i ~/.ssh/hermes_key_vps.pem patch_v22.py ubuntu@43.156.72.127:/tmp/

# 2. Restore from .bak, apply, verify syntax
ssh ... "cd /opt/hermes/ticketing-agent/backend && cp ai_agent.py.bak ai_agent.py && python3 /tmp/patch_v22.py"

# 3. If syntax OK: backup patched file
ssh ... "cd /opt/hermes/ticketing-agent/backend && cp ai_agent.py ai_agent.py.bak_patched"

# 4. Restart uvicorn
ssh ... "cd /opt/hermes/ticketing-agent && nohup venv/bin/uvicorn backend.main:app --host 0.0.0.0 --port 8080 > hotline.log 2>&1 &"

# 5. Verify
ssh ... "curl -s -o /dev/null -w '%{http_code}' http://127.0.0.1:8080/"
```

## abtrip_browser.py — current state

- `.bak` (original) and patched versions on VPS
- `patch_select.py` replaced `_try_flight_select` — syntax OK but not tested
- `patch_bookflow.py` failed syntax due to leftover code collision
- Current file has mixed code: new `_try_flight_select` + old `book_flight` that calls `_try_flight_select` + leftover `flight_found` lines

**To fix:** restore from .bak, apply one clean patch replacing entire `book_flight` function at once.
