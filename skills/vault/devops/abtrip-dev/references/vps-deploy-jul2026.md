# VPS Deploy — July 2026 (SmartAgent live on VPS)

## Current Live State (21 Jul 2026)

| Component | URL / Path | Status |
|-----------|-----------|--------|
| **SmartAgent UI** | `http://100.64.173.75/` | ✅ Live |
| **API** | `POST http://100.64.173.75/api/chat` | ✅ Live |
| **Health** | `http://100.64.173.75/api/health` | ✅ Running |
| **Backend** | `/opt/abtrip-backend/` | systemd active, 1 worker, ~92MB RAM |
| **nginx** | Port 80, proxy /api/ → 127.0.0.1:8138 | ✅ Running |
| **Venv** | `/opt/abtrip-backend/.venv/` | Python 3.12 |

## Services Deployed (New Jul 2026)

All 5 service modules live on VPS:
- `smart_fasttrack.py` — Fast Track info
- `smart_esim.py` — eSIM plans
- `smart_visa.py` — Visa info for 8 countries
- `smart_passport.py` — Passport service
- `flight_formatter.py` — Updated with table format + dedup fix

## Fix History from This Session

### Problem 1: Confirm flow returns greeting instead of flight results
**Root cause**: `classify_service("OK")` returns `"flight"`, which intercepts before `pending_action == "confirm_search"` check.
**Fix**: Move service routing to only run when `session.get("pending_action")` is falsy.
**Secondary cause**: `workers=2` in systemd — session dict is in-memory, worker 2 doesn't have worker 1's session.
**Fix**: Changed to `--workers 1` in systemd service.

### Problem 2: Duplicate airline codes (BLBL205)
**Root cause**: AGT API returns `FlightNumber` already prefixed with airline code (e.g. `FlightNumber: "BL205"`), code was concatenating `airline + flight_number` → `BLBL205`.
**Fix**: Added dedup logic in `flight_formatter.py` — if `fn.upper().startswith(al.upper())`, strip airline prefix from fn.

### Problem 3: crypto.randomUUID() fails silently on HTTP
**Root cause**: `crypto.randomUUID()` requires secure context (HTTPS). Falls silently on HTTP.
**Fix**: Replace with `'s' + Date.now() + Math.random().toString(36).slice(2, 8)`.

### Problem 4: Windows debug paths cause HTTP 500 on VPS
**Root cause**: `chat.py` had `open(r"C:/Users/Nguyen Ngoc Tan/debug_session.txt", "a")` statements.
**Fix**: Search and remove all hardcoded Windows paths before deploying.
