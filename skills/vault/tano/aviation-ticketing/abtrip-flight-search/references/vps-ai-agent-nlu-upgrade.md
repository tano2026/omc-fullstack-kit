# ABTRIP VPS AI Agent — NLU & Knowledge Upgrade

## Current State (20/06/2026)

**AI Agent path:** `/opt/hermes/ticketing-agent/backend/ai_agent.py`
**Frontend:** `/opt/hermes/ticketing-agent/frontend/` (Alpine.js SPA)
**Knowledge file:** `/opt/hermes/ticketing-agent/.hermes-knowledge.md`

The AI Agent uses DeepSeek (`deepseek-chat`) with function calling, with Gemini fallback for vision tasks.

## What was done this session (20/06/2026 — Round 2)

### ✅ Updated `.hermes-knowledge.md` with:
- **Sun PhuQuoc Airways (9G)**: Full airline profile, baggage, routes, fleet, fare classes. Full-service carrier — vital distinction from LCC.
- **Nguồn tra cứu hàng không tổng hợp**: Timatic (Emirates, IATA), FlightRadar24, Google Flights, GDS (Amadeus commands), Aerolopa, website các hãng.
- **Số hiệu chuyến bay theo mã hãng**: VN, VJ, QH, VU, 9G, BL.

### ✅ Updated ticketing-manager skill:
- Added **Sun PhuQuoc Airways (9G)** sub-section with full details
- Added **section 3a: Nguồn tra cứu hàng không** (Timatic, FR24, Google Flights, flight status tools, GDS)
- Added reference file `references/nguon-tra-cuu-hang-khong.md`
- Added website list + flight number patterns for all 5 domestic airlines

### ❌ Still pending: ai_agent.py code upgrades
Same as before — SSH timeout prevented deployment. The code patches are ready and documented above.

### ✅ Created `.hermes-knowledge.md`
Written to VPS at `/opt/hermes/ticketing-agent/.hermes-knowledge.md` containing:
- Airline policies for VN, VJ, QH, VU (baggage, fare rules, check-in)
- Reference flight times for domestic routes
- Verified booking history (PNRs)
- Aviation terminology glossary

### ❌ Pending: ai_agent.py code upgrades
Code was prepared locally but NOT deployed due to SSH quoting/timeout issues. The changes include:

**1. Updated TOOLS array (8 tools instead of 5):**
- `search_flights` — unchanged
- `book_flight` — **softened**: only `passenger_name` required, all others have defaults (DOB→1990-01-01, phone→0788320320, email→info@abtrip.vn, gender→inferred from name)
- `get_live_flight_status` — unchanged
- `get_live_airport_board` — unchanged
- `get_aircraft_layout` — unchanged
- `explain_fare_policy` — **NEW**: lookup from built-in DB (VN/VJ/QH/VU fare classes, change/refund rules)
- `get_baggage_allowance` — **NEW**: lookup hand carry + checked baggage per airline
- `get_checkin_guide` — **NEW**: online check-in instructions per airline

**2. Gender inference logic (in `execute_tool` → `book_flight`):**
```python
feminine_names = ["VY", "ANH", "HOA", "THU", "THANH", "MAI", "HUONG", "TRANG",
                  "LINH", "NGOC", "HA", "HIEN", "NHUNG", "THAO", "QUYNH", "DIEM",
                  "KIEU", "YEN", "NHI", "CHI", "TUYET", "PHUONG", "HONG", "DUNG"]
# Check last word of last_name or first_name
if last_word in feminine_names or first_word in feminine_names:
    gender = "Nữ"
else:
    gender = "Nam"
```

**3. System prompt overhaul:**
- Shorter, more focused on natural language understanding
- Explicit instruction: "if customer says 'book for Nguyen Van A, phone 098xxx', call book_flight IMMEDIATELY"
- Removed over-confirmation patterns

## To apply the pending changes

```bash
# 1. Backup
cp /opt/hermes/ticketing-agent/backend/ai_agent.py /opt/hermes/ticketing-agent/backend/ai_agent.py.bak2

# 2. Write the new version
# (Use the patch script from Hermes local or write directly)

# 3. Restart the server
# Check process first:
ps aux | grep uvicorn
# Then restart:
sudo systemctl restart ticketing-agent
# Or kill + restart uvicorn:
kill <PID>
cd /opt/hermes/ticketing-agent && source venv/bin/activate
nohup uvicorn backend.main:app --host 0.0.0.0 --port 8080 > /tmp/ticketing.log 2>&1 &
```

## Architecture notes

### Files on VPS

| File | Path | Purpose |
|------|------|---------|
| `main.py` | `backend/main.py` | FastAPI app, WebSocket, REST endpoints |
| `ai_agent.py` | `backend/ai_agent.py` | DeepSeek + function calling, tools, system prompt |
| `config.py` | `backend/config.py` | Configuration |
| `abtrip_browser.py` | `backend/abtrip_browser.py` | Playwright automation for abtrip.vn |
| `abtrip_client.py` | `backend/abtrip_client.py` | Alternative client |
| `flight_monitor.py` | `backend/flight_monitor.py` | Flight monitoring background loop |
| `telegram_bot.py` | `backend/telegram_bot.py` | Telegram bot integration |
| `zalo_listener.py` | `backend/zalo_listener.py` | Zalo OA listener |
| `personas.json` | `backend/personas.json` | 3 personas: vyvy, hamy, minhquan |
| `.hermes-knowledge.md` | `ticketing-agent/.hermes-knowledge.md` | Airline knowledge base |
| `.env` | `ticketing-agent/.env` | API keys (DeepSeek, Gemini) |
| `index.html` | `frontend/index.html` | Alpine.js SPA |
| `app.js` | `frontend/app.js` | Alpine.js logic |
| `style.css` | `frontend/style.css` | Styles with theme support |

### Model stack
- **Main:** `deepseek-chat` via `api.deepseek.com/v1`
- **Vision:** `gemini-2.5-flash` via Google Gemini OpenAI-compatible endpoint
- **Fallback:** Gemini if DeepSeek fails

### Tools (current — before upgrade)
1. `search_flights` — Playwright search on abtrip.vn
2. `book_flight` — REQUIRES all fields (too strict)
3. `get_live_flight_status` — FlightRadar24API
4. `get_live_airport_board` — FlightRadar24API
5. `get_aircraft_layout` — Built-in DB of seat configs

### Restart
```bash
cd /opt/hermes/ticketing-agent && source venv/bin/activate
ps aux | grep uvicorn  # find PID
kill <PID>
nohup uvicorn backend.main:app --host 0.0.0.0 --port 8080 > /tmp/ticketing.log 2>&1 &
```
