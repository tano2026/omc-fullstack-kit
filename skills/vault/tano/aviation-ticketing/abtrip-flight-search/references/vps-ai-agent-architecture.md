# VPS AI Agent Architecture (hotline.abtrip.vn)

## Tổng quan

ABTRIP Hotline chạy FastAPI server trên VPS, tích hợp AI Agent (DeepSeek) với function calling để search & book vé tự động.

| Component | Công nghệ | Location | Port |
|-----------|-----------|----------|------|
| Nginx (SSL) | nginx | System | 443 → hotline.abtrip.vn |
| FastAPI backend | uvicorn | `/opt/hermes/ticketing-agent/` | 8080 |
| Frontend SPA | Alpine.js + CSS | `/opt/hermes/ticketing-agent/frontend/` | served by FastAPI |
| AI Agent | DeepSeek Chat (OpenAI SDK) | `backend/ai_agent.py` | — |
| Playwright scraper | Playwright | `backend/abtrip_browser.py` | — |
| Flight Monitor | Python threading | `backend/flight_monitor.py` | — |
| Telegram Bot | python-telegram-bot | `backend/telegram_bot.py` | — |
| Zalo Listener | zalo_me | `backend/zalo_listener.py` | — |

## File structure

```
/opt/hermes/ticketing-agent/
├── backend/
│   ├── main.py              # FastAPI app, REST + WebSocket endpoints
│   ├── ai_agent.py           # AI Agent: DeepSeek + function calling + chat sessions
│   ├── abtrip_browser.py     # Playwright search & book
│   ├── abtrip_client.py      # API B2B client helper
│   ├── flight_monitor.py     # Background seat/price monitoring loop
│   ├── config.py             # Config (PORT, GOOGLE_API_KEY, etc.)
│   ├── personas.json         # VyVy, HaMy, MinhQuan personas
│   ├── telegram_bot.py       # Telegram polling bot
│   ├── zalo_listener.py      # Zalo OA listener
│   └── zalo_session.json     # Zalo cookies
├── frontend/
│   ├── index.html            # SPA — Alpine.js x-data="appState()"
│   ├── app.js                # Alpine.js state + API calls + WebSocket
│   └── style.css             # Themed CSS
└── .env
```

## AI Agent Architecture (ai_agent.py)

### Model Stack
- **Primary:** `deepseek-chat` via DeepSeek API (`https://api.deepseek.com/v1`)
- **Vision fallback:** `gemini-2.5-flash` via Google Gemini OpenAI-compat endpoint
- **Error fallback:** Gemini (when DeepSeek errors)
- No local models (Ollama runs on VPS but not used by this app)

### Tools Defined (5 tools)

1. **search_flights** — tìm chuyến bay qua Playwright (abtrip_browser.run_search)
2. **book_flight** — đặt vé qua Playwright (abtrip_browser.book_flight)
   - Required params: search_session, flight_value, passenger_name, passenger_gender, passenger_dob, contact_phone, contact_email
3. **get_live_flight_status** — tra cứu chuyến bay realtime (FlightRadarAPI)
4. **get_live_airport_board** — bảng departures/arrivals thực tế (FlightRadarAPI)
5. **get_aircraft_layout** — sơ đồ ghế các hãng nội địa (hardcoded database)

### Chat Flow

1. User message → POST `/api/chat` → `chat_with_agent(session_id, message, persona)`
2. System prompt + time instruction + knowledge file loaded
3. DeepSeek calls → if tool_calls → execute_tool() → append result → loop up to 3x
4. Returns final text response
5. Fallback: if DeepSeek errors → retry with Gemini

### Personas (personas.json)

3 personas for different departments:
- **vyvy** — Hotline Phòng Vé (search + book flights, xưng "em")
- **hamy** — Hotline Tour & Du lịch (hotels, visa, tours)
- **minhquan** — Hotline Sân bay An Bình (VIP fasttrack, lounge, eSIM)

Each has: system_instruction_addon, tone_guidelines, allowed_tools.

### Knowledge File

System tries to load `.hermes-knowledge.md` from:
1. `../../../.hermes-knowledge.md` (project root)
2. `../.hermes-knowledge.md` (ticketing-agent root)
3. `./.hermes-knowledge.md` (backend dir)

Currently no such file exists — all knowledge is in the hardcoded `SYSTEM_PROMPT`.

## Known Issues & Upgrade Needs (June 2026)

### 1. LLM hiểu ngôn ngữ tự nhiên kém
- **Problem:** `book_flight` tool requires ALL fields (name, gender, dob, phone, email) in rigid format. If user says "đặt cho Nguyễn Văn A, sdt 098xxx" → AI can't call tool because DOB/email missing.
- **Fix ideas:**
  - Add `ask_for_info` tool that AI calls when info is missing
  - Make passenger fields optional with sensible defaults
  - Add multi-turn clarification loop (AI asks → user answers → retry)
  - Infer gender from name (convention: names ending in A/Anh/Hoa → Nữ, others → Nam)

### 2. Thiếu tri thức hàng không chuyên gia
- **Problem:** No airline policy knowledge source. Hardcoded aircraft layout DB has basic config but no fare rules, baggage policies, check-in procedures.
- **Fix:**
  - Create `.hermes-knowledge.md` with airline policies (VN, VJ, QH, VU, Pacific)
  - Add tools: `explain_fare_rules`, `check_baggage_policy`, `check_in_info`
  - Each tool scrapes the airline's official website for current info

### 3. booking code sync issues
- `book_flight` in ai_agent.py has mismatched function signature with abtrip_browser.py:
  - ai_agent passes `flight_value` as `flight_number` but abtrip_browser expects actual flight code
  - `search_session` parameter is never actually used by abtrip_browser
  - `start_point`, `end_point`, `depart_date` not passed from tool args to book_flight

### 4. DeepSeek model ambiguity blocks vision
- Model ID 'deepseek-chat' matches multiple versions → vision_analyze fails
- On the VPS, Gemini handles vision separately (ai_agent.py detects data:image URLs)
- The Hermes agent persona should use full model ID 'deepseek/deepseek-chat'

## SSH Access

```bash
ssh -i ~/.ssh/hermes_key_vps.pem ubuntu@43.156.72.127
```

## Restart

```bash
# Systemd service (if configured):
sudo systemctl restart hermes-ticketing

# Or manually:
cd /opt/hermes/ticketing-agent
source venv/bin/activate
sudo kill $(lsof -t -i:8080)
nohup python -m uvicorn backend.main:app --host 0.0.0.0 --port 8080 > server.log 2>&1 &
```
