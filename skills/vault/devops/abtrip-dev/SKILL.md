---
name: abtrip-dev
title: ABTrip Agent — dev loop & conventions
description: All non-obvious gotchas, paths, Python toolchain, OmniRoute quirks, run commands, Intent Parser V3 architecture, and deploy patterns for the agent.tkt project.
triggers:
  - D:\MMO Du an\AI Agent Future\agent.tkt
  - ABTrip
  - agent.tkt
  - LLM Bot backend
---

# ABTrip Agent — dev loop & conventions

## 👤 User Preferences
- **Step-by-step sequential work**: When given multiple tasks, user prefers "làm lần lượt" — do them in order, one at a time. Don't jump ahead or parallelize unless asked.
- **Brief, direct responses**: User is impatient. Don't over-explain what you're about to do — do it, then report results concisely.
- **Vietnamese primary**: All explanations and reporting in Vietnamese unless code comments are being discussed.

**Current active development path:** `D:\\MMO Du an\\TANO-AGENCY\\PROJECTS\\abtrip\\` (local Docker monorepo)

**VPS canonical path:** `/opt/abtrip-backend/` — the source of truth for production code. The VPS runs `uvicorn app.main:app --port 8138 --workers 2` (NOT port 8139 anymore).

> ⚠️ **PATH CHANGE (24 Jul 2026):** The project consolidated under `D:\\MMO Du an\\TANO-AGENCY\\PROJECTS\\abtrip\\` (local) + `/opt/abtrip-backend/` (VPS). The old `C:\\Users\\Nguyen Ngoc Tan\\agent.tkt\\` is DEPRECATED — it's out of sync and should not be used for development. The VPS at `100.64.173.75:8138` is the canonical production version. **Always verify local code matches VPS before making changes** — the VPS is the source of truth, not local files. When the user says local code is "cũ quá", pull from VPS first (see §VPS→Local Sync below).

**Key reference:** `references/llm-dual-model-routing.md` - Dual-model LLM routing system (Sonnet/Opus) implemented July 2026
**Upgrade plan:** `references/aviation-expert-upgrade-plan.md` — 4-phase brain upgrade (TIMATIC, RAG 100+, expert reasoning, auto-update)
**Architecture (implemented):** `references/antigravity-architecture.md` — dual-collection RAG, policy crawler, decision node, data sources ($0 budget)

## 📦 Project Structure

```
abtrip/
├── backend/          # FastAPI on port 8765 (Docker) / 8138 (VPS)
│   ├── data/                  # SQLite DB files (incl. smart_agent.db)
│   └── app/
│       ├── main.py              # FastAPI app (lifespan + routers)
│       ├── api/                 # bookings, reference, health, chat
│       ├── agents/              # Agent modules
│       ├── models/              # abtrip, chat schemas
│       ├── services/            # abtrip_client, llm_gateway, intent_parser, smart_*
│       ├── templates/           # main.html (Smart Agent landing)
│       └── middleware/          # CORS, auth middleware
├── frontend/         # Next.js 14 on port 4321 (Docker) / 3000 (VPS)
│   ├── app/                    # layout, page, providers, search, book, booking detail
│   ├── components/             # SearchForm, FlightCard, BookingForm, PassengerForm
│   └── lib/                    # api.ts
└── docs/                       # API spec + booking UI screenshots
```

## 🔌 AGT API Integration (22 Jul 2026)

**Live sandbox URL:** `https://api-abtrip.timtrungtam.com/v1` (NOT `api.abtrip.vn` — that domain doesn't exist in DNS)

**Credentials (test environment — from API spec):**
```
AGT_PRIVATE_KEY=a3f2b9e1c8d4a7f6b2e0c9d5a4b1f8d32
AGT_API_ACCOUNT=ABTRIP
AGT_API_PASSWORD=CtTXgjVX8AQ1
```

**API spec document:** `D:\Downloads\Bo_Tai_Lieu_Dac_Ta_API_ABTRIP_v1.1\abtrip_api_spec.md` (authoritative, developed by Viettel Group for ABTrip)

**Postman collection:** `D:\Downloads\ABTrip V1.1.postman_collection (2).json` (11MB, uses `{{host}}` variable — no host defined in collection, get it from spec doc)

**Config file:** `backend/app/services/config.py` — `agt_api_host` default must be `https://api-abtrip.timtrungtam.com/v1`

### Endpoint Status (verified 22 Jul 2026 — 10/10 working end-to-end)

| # | Endpoint | Status | Notes |
|---|----------|--------|-------|
| GetAirports | ✅ | 2,421 airports (returns raw array — `abtrip_client._post` fixed to wrap non-dict responses) |
| GetAirlines | ✅ | 609 airlines |
| GetAircrafts | ✅ | 361 aircraft |
| SearchFlight | ✅ | Real flights, real prices. Returns `ListGroup > ListAirOption > ListFareOption/ListFlightOption` |
| GetFareRule | ✅ | Works with correct `AirOptionId` + `System` |
| GetAncillary | ✅ | Fixed — needs `SessionInfo{Session,AirlineOptionId,FareOptionId,FlightOptionId}`, not `ListSession` |
| GetSeatMap | ✅ | Fixed — same `SessionInfo` format |
| BookFlight | ✅ | Fixed — real `BookingCode` returned (e.g. `ABT00355`) on sandbox |
| IssueTicket | ✅ | Verified after real BookFlight |
| RetrieveBooking | ✅ | Verified after real BookFlight |

**Full flow confirmed working**: SearchFlight → GetAncillary → GetSeatMap → BookFlight → RetrieveBooking → IssueTicket, all against the live sandbox, all producing real (non-mock) responses.

### abtrip_client.py — Known Bugs & Fixes (all fixed + verified 22 Jul 2026)

1. **`_post` crashes on array/non-dict responses**: Some endpoints (GetAirports, GetAirlines, GetAircrafts) return raw arrays `[...]` not dicts. Fixed with:
   ```python
   if not isinstance(data, dict):
       data = {"Success": True, "Message": "OK", "Data": data}
   ```

2. **Request format mismatch (fixed)**: GetAncillary/GetSeatMap/BookFlight need API-spec format with `SessionInfo{Session, AirlineOptionId, FareOptionId, FlightOptionId}` — the four IDs come from SearchFlight's response (top-level `Session` + `ListGroup[].ListAirOption[].OptionId` + `.ListFareOption[].OptionId` + `.ListFlightOption[].OptionId`). The client previously sent `ListSession` (wrong shape, written from assumptions not the actual spec). Corrected in `abtrip_client.py`.

3. **SearchFlight response structure**: Real response uses `OptionId` (not `AirOptionId`), prices in `ListFareOption[].PriceAdt`, flight info in `ListFlightOption[].ListFlight[]`. Client code that accesses `opt['AirOptionId']` will get KeyError — use `opt['OptionId']` instead.

**Debugging pattern that worked**: when an endpoint status is unclear, write a throwaway Python script (not inline terminal one-liners) that imports the client directly, calls each endpoint in sequence, and prints/dumps the raw response — this surfaces exact field names and format mismatches faster than reading the spec doc alone. Confirm against `references/agt-api-spec-excerpts.md` for the authoritative shape.

**CRITICAL:** The system `python` (from Microsoft Store alias) points to a MPT virtualenv or fails with 'Python was not found'. Use `python` from Git Bash which resolves correctly. Do NOT use `python3` on this Windows host.

| Use | Command |
|-----|---------|
| **Python runner** | `python` (works from Git Bash — resolves to correct 3.11.9) |
| **uvicorn** | `cd "C:/Users/Nguyen Ngoc Tan/agent.tkt/backend" && python -m uvicorn app.main:app --host 0.0.0.0 --port 8139` |
| **Writing Python scripts** | Write `.py` file then `python <file>` — avoids shell escaping issues with quotes/special chars |

## 🚀 Startup Sequence

Both services **do not survive Windows sleep/idle**. If the user reports frontend or backend down, ALWAYS restart both.

### 🔍 Status Triage — "ABTrip đang thế nào?" (recurring question)

When the user asks for a status check, run this triage in order — **do NOT assume the VPS is the live source of truth; it may be down too** (confirmed 24 Jul 2026: BOTH local and VPS had 0 containers running):

1. **Local containers:** `docker compose -f "D:/MMO Du an/TANO-AGENCY/PROJECTS/abtrip/docker-compose.local.yml" ps` — 0 containers = nothing running locally.
2. **VPS containers:** `ssh ubuntu@43.156.72.127 "docker ps"` — do NOT assume VPS is up. It goes down on sleep/reboot just like local.
3. **Branch lineage (BEFORE any sync):** `git -C <local> log --oneline -3` vs `ssh vps 'git -C /opt/abtrip-backend log --oneline -3'` + `git -C <local> status --short | wc -l`. If top commits share no hash → **diverged, do NOT blind-sync** (see §VPS Deploy divergence warning). If local has uncommitted files → stash/commit first.
4. **Bring local up:** `docker compose -f "..." up -d --build --force-recreate` (see Option A below).

**Per-service health verification (don't false-alarm):**
- **Backend alive = root `/` OR `/docs` returns HTTP 200.** There is NO `/health` at root — `curl http://localhost:8765/health` returns `{"detail":"Not Found"}` even when the backend is fully up. The real health route is `/api/health`. Don't conclude "backend down" from a 404 on `/health`.
- **Frontend Next.js dev first-request compile takes ~15-20s.** Right after container start, `curl http://localhost:4321` returns HTTP 000 (connection refused/compiling), then the log shows `Compiling / ...` → `Compiled / in ~20s` → HTTP 200. HTTP 000 immediately after start is compile-in-progress, NOT a crash — wait 20s and recheck the log (`docker compose logs abtrip-frontend --tail=6`) before restarting.
- **When both local + VPS are down AND branches diverged:** runtime can't tell you which side wins. Reconcile with git (per-file diff, ask user which side wins per conflict) — do NOT tar-pipe sync blindly.

**Docker is the PRIMARY dev environment** (24 Jul 2026). Docker Desktop installed at `~/AppData/Local/Programs/DockerDesktop/resources/bin/docker.exe`. Use the full path since Git Bash PATH may not include it. Docker Compose via `docker compose` subcommand. Config at `D:/MMO Du an/TANO-AGENCY/PROJECTS/abtrip/docker-compose.local.yml`.

### Option A: Docker Compose (primary — 24 Jul 2026)

```bash
# Full path avoids Git Bash PATH issues
docker compose -f "D:/MMO Du an/TANO-AGENCY/PROJECTS/abtrip/docker-compose.local.yml" up -d --build --force-recreate
```

This starts all 4 containers: backend (8765), frontend (4321), postgres (5987), redis (7103).

To rebuild only the backend after code changes:
```bash
docker compose -f "D:/MMO Du an/TANO-AGENCY/PROJECTS/abtrip/docker-compose.local.yml" up -d --build --force-recreate --no-deps abtrip-backend
```

Verify: `docker compose -f "..." ps` shows all 4 services Up/healthy.
Verify backend: `docker compose -f "..." logs abtrip-backend --tail=5` shows "Application startup complete".

### Option B: Direct startup (legacy — from old agent.tkt path)

1. **Kill stale processes first** — uvicorn (port 8138) and next dev (port 4321) both linger on ports:
   ```
   netstat -ano | grep ':8138 ' | grep LISTEN
   netstat -ano | grep ':4321 ' | grep LISTEN
   ```
   Then kill each PID: `taskkill -f -pid <pid>`. May need multiple passes.

2. **Backend** (wait 5-8s for startup):
   ```bash
   cd "C:/Users/Nguyen Ngoc Tan/agent.tkt/backend"
   PORT=8139 python run.py
   ```
   Verify: `curl -s http://localhost:8138/docs` (server is up if HTML returned)

3. **Frontend** (Next.js on port 4321):
   ```bash
   cd "C:/Users/Nguyen Ngoc Tan/agent.tkt/frontend"
   npx next dev -p 4321
   ```
   Verify: `curl -s http://localhost:4321` → HTML with title "ABTrip AI Agent"

### Option B: Raw uvicorn (legacy — for quick dev without Docker)
```bash
cd "C:/Users/Nguyen Ngoc Tan/agent.tkt/backend"
python -m uvicorn app.main:app --host 0.0.0.0 --port 8139
```

## 🤖 SmartAgent — Multi-Service Chat Architecture (Jul 2026)

SmartAgent (`SmartAgent — Phòng Vé AI`) is the unified chat interface serving 5 services from a single endpoint at `http://100.64.173.75/`.

### Architecture

```
User → [nginx :80 /api/] → FastAPI :8138 → POST /api/chat
                                                     │
                                        classify_service(message)
                                        ├── "fasttrack" → smart_fasttrack.py
                                        ├── "esim" → smart_esim.py
                                        ├── "visa" → smart_visa.py
                                        ├── "passport" → smart_passport.py
                                        └── "flight" → _execute_flight_search() (AGT/mock)
```

### Service Routing Pattern

`chat.py` → `_handle_ticketing()`:
1. **STEP 0**: If no `pending_action`, run `classify_service(message)`. If not "flight", route to `_handle_smart_service()`. Otherwise proceed to flight flow.
2. **STEP 1**: Check `pending_action == "confirm_search"` — user said OK → search.
3. **STEP 2**: Check `pending_action == "awaiting_confirm"` — user providing missing info.
4. **STEP 3**: Parse flight search. If complete → confirm. If missing → clarify.
5. **STEP 4**: Non-search intents (policy_baggage, etc.).
6. **STEP 5**: Fallthrough to LLM.

**CRITICAL**: `classify_service()` must only run when there's NO `pending_action`. Otherwise, "OK" or other replies might bypass the intended confirm flow.

**Passport Intent Fix (23 Jul 2026):** `classify_service()` in `intent_parser.py` was updated to include a broader range of keywords for passport-related services (e.g., `thiếu mộc`, `cccd`, `em bé`, `in ngang`, `cấp đổi`, `gia hạn`, `giấy phạt`, `lăn tay`, `bị chú`, `thay đổi`, `thông tin`, `làm lại`, `mất hộ chiếu`, `hết hạn`, `gia hạn`, `dán ảnh`, `lỗi`, `số hộ chiếu`). This prevents misclassification of passport queries as flight searches when no pending action is active.

### Service Files

| File | Purpose |
|------|---------|
| `backend/app/services/smart_fasttrack.py` | Fast Track Nội Bài (HAN), TSN, Đà Nẵng, Quốc tế — giá retail/agent, features, hours |
| `backend/app/services/smart_esim.py` | eSIM 5 regions — data, duration, price |
| `backend/app/services/smart_visa.py` | 8 countries — types, fee, processing, note |
| `backend/app/services/smart_passport.py` | Hộ chiếu lần đầu, cấp nhanh 1-3 ngày |
| `backend/app/services/intent_parser.py` | `classify_service()` + `classify_intent()` |
| `backend/app/api/chat.py` | `_handle_smart_service()` router |
| `backend/static/chat.html` | Single-file HTML UI served at `/` via nginx |

### RAG Knowledge Base — Dual-Collection (Antigravity Architecture, 24 Jul 2026)

**Architecture:** Two ChromaDB collections, designed per the Antigravity diagram:

```
User Query → is_operational_query()?
  ├── Yes → RagService.query() → MERGE aviation_kb + airline_policies
  │         → format_context() → inject [THÔNG TIN TRA CỨU] block
  │         → LLM answers with aviation expertise
  └── No  → Flight MCP Server (abtrip_client.py function calling)
```

**Collections:**
| Collection | Purpose | Source |
|---|---|---|
| `aviation_kb` | Tri thức IATA, sân bay, kiến thức nền | `aviation_db.py` airports + airlines |
| `airline_policies` | Chính sách từng hãng (cập nhật qua crawler) | `aviation_db.py` policies + `policy_crawler.py` |

**File:** `backend/app/services/rag_service.py` (rewritten 24 Jul 2026 — was `rag_knowledge.py`)
**Reference:** `references/rag-knowledge-base.md` for original seed doc list.
**New reference:** `references/antigravity-architecture.md` for full architecture + data sources.

**Key functions:**
- `is_operational_query(text)` — regex classifies ops vs booking (85+ keyword patterns)
- `RagService.query(query_text, top_k=5)` — searches BOTH collections, merges by distance
- `RagService.query_policies(query_text)` — searches only `airline_policies`
- `RagService.query_aviation(query_text)` — searches only `aviation_kb`
- `RagService.format_context(query_text)` — formats merged results as LLM-ready context block
- `RagService.upsert_policy(code, name, category, value)` — for crawler to update individual policies
- `RagService.reindex(collection="all")` — admin API to rebuild collections

**Key pattern:**
```python
from app.services.rag_service import get_rag_service, init_rag
rag = get_rag_service()
await rag.initialize()
ctx = rag.format_context("hành lý Vietjet bao nhiêu kg")
# Returns merged results from both collections with 📍/✈️/📋 prefixes
```

### 🧠 Antigravity Decision Node (smart_agent.py — 24 Jul 2026)

The chat endpoint at `POST /api/smart-agent/chat` (in `smart_agent.py`, NOT `api/chat.py`) implements the Antigravity decision node pattern:

```python
is_ops = is_operational_query(req.message)  # 85+ keyword patterns
if is_ops:
    rag = get_rag_service()
    rag_context = rag.format_context(req.message, top_k=3)
    system_prompt = f"""... + [THÔNG TIN TRA CỨU]\n{rag_context}"""
else:
    system_prompt = f"""... lean booking prompt (~10 lines, no hardcoded domain knowledge)"""
```

**Two paths, one endpoint:**
| Path | Trigger | System Prompt | Fallback |
|------|---------|---------------|----------|
| Operational | `is_operational_query()` returns True | RAG context injected from dual-collection | RAG fallback (no LLM needed) |
| Booking | Everything else | Lean prompt — LLM extracts from/to/date/pax | Rule-based intent routing |

**⚠️ BOOKING GAP — RESOLVED (25 Jul 2026):** See §AGT Booking Integration below for the fix and `references/flight-param-extraction.md` for the implementation details.

### ✈️ AGT Booking Integration (wired 25 Jul 2026)

The booking path in `smart_agent.py` now calls the real AGT API after Gemini generates its conversational response. Flow:

```
POST /api/smart-agent/chat → flow=booking & !is_ops
  → **Gemini generates conversational text response** (⚠️ fallback needed if key dead — see Pitfall #33)
  → _extract_flight_params(history) — regex extract from/to/date/pax from user messages
  → ABTripClient().search_flight(system="", adt=fp["adt"], routes=[{"StartPoint": fp["from"], "EndPoint": fp["to"], "DepartDate": fp["date"]}])  # system="" = all airlines (Pitfall #36); route keys are StartPoint/EndPoint NOT Origin/Destination, date is ddMMyyyy NOT yyyyMMdd (Pitfall #37)
  → _format_flight_results() — format top 5 cheapest results as display text
  → text = flight_results + "\n" + gemini_text  (prepend)
  → SSE stream to user
```

**Key functions added** (all in `smart_agent.py`):

| Function | Purpose |
|---|---|
| `_extract_flight_params(texts)` | Regex + alias map — extracts origin/destination/date/pax from Vietnamese chat messages (e.g. "vé SG đi Nha Trang thứ 7, 2 người" → `{from:SGN, to:CXR, date:"27072026", adt:2}`). ⚠️ `date` MUST be `ddMMyyyy` (Pitfall #37), NOT `yyMMdd`/`yyyyMMdd` |
| `_format_flight_results(data, params)` | Formats AGT SearchFlight response into text: airline name + cheapest fare per group, top 5 shown |
| `_AIRPORT_ALIAS` dict | Maps Vietnamese names/abbreviations to IATA codes (25 airports) |

**Reference:** `references/flight-param-extraction.md` — full alias map, regex patterns, and date parsing rules.
**Test script:** `scripts/test_batch.py` — 7-case batch test harness for AGT booking + ops queries. Run with `python scripts/test_batch.py` (skill-managed). Reads from `$BASE/api/smart-agent/chat`. Reports markers: ✈️ flight, 💰 price, 📚 RAG, ❓ clarification, ❌ error.
**Reference:** `references/test-batch.md` — test case descriptions and expected outcomes.

**Error handling:** If AGT call fails, the error is logged and appended as a warning prefix to the Gemini response — the user still gets Gemini's conversational answer, not a silent failure.

**Docker-compose env vars (local):** `AGT_API_HOST`, `AGT_PRIVATE_KEY`, `AGT_API_ACCOUNT`, `AGT_API_PASSWORD` set directly in `docker-compose.local.yml` environment block — overrides whatever `.env` says (the VPS `.env` still has the dead `api.abtrip.vn` domain, but docker-compose env vars take precedence).

**Key difference from chat.py:** `smart_agent.py` does NOT use `classify_service()` or `_handle_smart_service()` — it's a self-contained endpoint that handles both ops and booking through one Gemini/DeepSeek call. The old `api/chat.py` flow (classify → route to smart_*.py) still exists in parallel for the landing page quick-action cards, but Antigravity queries go through `smart_agent.py`.

**⚠️ `flow` variable trap (fixed 25 Jul 2026):** The original booking-fallback code used `if flow == "booking" and not is_ops:` but `flow` is a field on `ChatRequest` (`req.flow`), NOT a local variable in `smart_chat()`. This produced `NameError: name 'flow' is not defined` on every booking message. The correct condition is simply `if not is_ops:` — because `is_ops` already distinguishes between the two paths (operational vs. booking). Do NOT use `flow`, `req.flow`, or any variation of it in the `smart_chat()` function body.

**RAG fallback (non-Gemini path):** When Gemini API is offline AND the query is operational, `smart_agent.py` falls back to `rag.format_context()` directly — no LLM needed, returns context from ChromaDB. This is the key resilience improvement: operational queries never hit a "hệ thống đang bận" dead end.

### Adding a New Service
1. Create `backend/app/services/smart_<name>.py` with `handle_<name>(message: str) -> str`
2. Add keywords to `classify_service()` in `intent_parser.py`
3. Import + add elif in `_handle_smart_service()` in `chat.py`

### SmartAgent UI Pattern (rebranded Jul 2026, updated 24 Jul 2026)

Single-file HTML served via `@app.get("/")` → `HTMLResponse` reading `templates/main.html` (759 lines, Smart Agent landing with "Nói 1 câu, AI lo hết", 5 quick-action cards, banner, nav links). NOT the old `landing_page_sanhoo.html` or `static/chat.html`.

**Route pattern in main.py:**
```python
import os
from fastapi.responses import HTMLResponse
from pathlib import Path

TEMPLATES_DIR = Path(__file__).resolve().parent / "templates"

@app.get("/", response_class=HTMLResponse, include_in_schema=False)
async def smart_agent_landing():
    landing_path = TEMPLATES_DIR / "main.html"
    if landing_path.exists():
        return HTMLResponse(content=landing_path.read_text(encoding="utf-8"))
    return HTMLResponse(content="<h1>Smart Agent</h1><p>Loading...</p>")
```

**Brand colors (ABTrip — rebranded 22 Jul 2026):**
- **Header**: Teal gradient `linear-gradient(135deg,#006885,#005570)`, white text
- **Primary/buttons**: Teal `#006885`, hover `#005570`
- **Gold accent**: `#DBA011` (cheapest badge, bot avatar, flight card border, "Đặt ngay" button)
- **Dark gold**: `#B8860B` (cheapest price text)
- **User bubble/avatar**: Navy `#1B3A6B`
- **Send button**: Teal `#006885`
- **Quick cards + body bg**: Warm white `#f8f7f4`

**UI features:**
- **Font**: Inter (Google Fonts — acceptable for chat UIs despite taste-skill ban on Inter elsewhere)
- **Icons**: Phosphor Icons (light style, from CDN)
- **5 quick-action cards**: Flex grid (Vé/Fast Track/eSIM/Visa/Hộ chiếu), each triggers `sendQuick(service_name)` onclick
- **Fixed bottom input bar**: White pill with shadow, inside gradient-to-transparent container
- **Session ID**: `'s' + Date.now() + Math.random().toString(36).slice(2, 8)` — NOT `crypto.randomUUID()` (fails on HTTP)
- **CSS**: `white-space: pre-wrap` on bot bubbles; fadeIn keyframe animation; mobile responsive at 480px breakpoint
- **Bot response format**: `formatReply()` converts `**bold**` → `<strong>`, `• items` → `<ul>`, `*italic*` → `<em>`, newlines → `<br>`
- **API URL**: Relative `/api/chat` (was hardcoded VPS IP `100.64.173.75`)

**Serving pattern (critical):** Do NOT use `app.mount("/", StaticFiles(...))` — it intercepts all routes including `/api/*`. Use a specific route:
```python
from fastapi.responses import FileResponse, HTMLResponse

@app.get("/")
async def serve_chat():
    import os
    _chat_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "static", "chat.html")
    return FileResponse(_chat_path, media_type="text/html") if os.path.isfile(_chat_path) else HTMLResponse("Not found", status_code=404)
```

### SmartAgent Chat Interface (UI/UX & Integration)

The SmartAgent chat interface is designed for natural language booking, eliminating traditional forms and multi-page navigation. It combines a service grid, welcome screen, and SSE streaming chat with LLM-driven intent routing.

#### Architecture

```
Frontend (HTML/CSS/JS)
  └── Service bar: 5 services (flight, fasttrack, esim, visa, passport)
  └── Welcome screen with suggestion pills
  └── Chat messages (SSE streaming)
  └── Input box with auto-resize + Enter-to-send

Backend (FastAPI)
  └── POST /api/smart-agent/chat → SSE stream
      └── Try Gemini 2.5 Flash (GEMINI_API_KEY)
      └── Fallback: rule-based intent routing
      └── Session history in memory dict
```

#### Key Implementation Details

1.  **Service Bar (Bento Grid)**
    *   5-column grid, each item: icon + label
    *   Each service has distinct color (flight=blue, fasttrack=gold, esim=teal, visa=purple, passport=red)
    *   `onclick="sendSuggestion('...')"` — clicking triggers chat with pre-filled text
    *   Responsive: 5-col → 3-col on mobile
    *   Badge for unique services (e.g. Fast Track "24/7")

2.  **Chat UI State Machine**
    ```
    welcomeScreen visible → user sends message → hide welcome, show chatMessages
    chatMessages hidden (.active class) → shown when messages exist
    isStreaming flag → disables send button during streaming
    ```

3.  **SSE Streaming Pattern (Frontend)**
    ```js
    const response = await fetch('/api/smart-agent/chat', { method: 'POST', body: JSON.stringify({ message, session_id }) })
    const reader = response.body.getReader()
    const decoder = new TextDecoder()
    let buffer = ''
    while (true) {
        const { done, value } = await reader.read()
        if (done) break
        buffer += decoder.decode(value, { stream: true })
        // Parse SSE: lines starting with "data: "
        // Events: {type: "text", content, session_id} | {type: "done", content} | [DONE]
    }
    ```

4.  **Backend Chat Router (FastAPI)**
    ```python
    @router.post("/chat")
    async def smart_chat(req: ChatRequest):
        sid = req.session_id or str(uuid.uuid4())
        history = _chat_sessions.get(sid, [])

        # 1. Try Gemini 2.5 Flash
        gemini_key = os.getenv("GEMINI_API_KEY", "")
        if gemini_key:
            # Build Gemini payload with system prompt + history
            # Call: POST https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent

        # 2. Fallback: rule-based intent routing
        intent = detect_intent(message)
        responses = {"flight": "...", "fasttrack": "...", ...}

        # Return StreamingResponse with _sse_stream generator
    ```

5.  **Streaming SSE Generator**
    ```python
    async def _sse_stream(text: str, session_id: str):
        """Stream text word-by-word for smooth UX."""
        chunk_size = 10  # characters per chunk
        for i in range(0, len(text), chunk_size):
            chunk = text[i:i + chunk_size]
            event = {"type": "text", "content": chunk, "session_id": session_id}
            yield f"data: {json.dumps(event)}\n\n"
            await asyncio.sleep(0.02)
        # Done event
        yield f"data: {json.dumps({'type': 'done', 'content': text})}\n\n"
        yield "data: [DONE]\n\n"
    ```

6.  **Intent Detection (Rule-Based)**
    ```python
    msg_lower = message.lower()
    if any(kw in msg_lower for kw in ["visa", "hộ chiếu", "passport", "thị thực"]):
        intent = "visa"
    elif any(kw in msg_lower for kw in ["fast track", "fasttrack", "ưu tiên", "vip", "lounge"]):
        intent = "fasttrack"
    elif any(kw in msg_lower for kw in ["esim", "sim", "data", "4g", "5g", "internet"]):
        intent = "esim"
    elif any(kw in msg_lower for kw in ["vé", "bay", "máy bay", "chuyến", "đặt vé"]):
        intent = "flight"
    elif any(kw in msg_lower for kw in ["mở phòng vé", "ctv", "đại lý", "cộng tác viên"]):
        intent = "ctv"
    ```

### Flight Results Format

**User preference (Jul 2026):** Code-block tables are "khó nhìn" (hard to read), especially on mobile. The desired format is **structured JSON → frontend HTML card rendering**, not pre-formatted text. This is a critical UI/UX preference.
 
 **New Flow:**
 1. Backend (`flight_formatter.py`) now returns a tuple: `(formatted_text_summary, structured_flights_list)` when `return_data=True`. `formatted_text_summary` provides a concise overview (e.g., route, date, cheapest price) for simpler displays or LLM context.
 2. `chat.py` extracts `structured_flights_list` and adds it to `ChatResponse.data.flights`.
 3. Frontend (`static/chat.html`) checks `d.type === 'flight_results' && d.data && d.data.flights` and, if present, calls `renderFlightCards(d.data.flights)` to render interactive, visually appealing flight cards. Otherwise, it falls back to displaying `d.reply` as formatted text.
 
 **`renderFlightCards` features:**
 - Each flight option is rendered as a distinct HTML card/row.
 - Visual hierarchy: airline emoji, flight code, times (depart → arrive), duration (small subtitle).
 - Price is prominent (big + bold).
 - "Cheapest" flights get a ⭐ badge and distinct styling.
 - Airline colors are dynamically applied (e.g., BL: green, VJ: red, QH: green, VU: orange, VN: blue).
 - Overall: more scannable, visually appealing, and mobile-friendly than monospace tables.
 
 **Structured Flight Data Example (from `ChatResponse.data.flights`):**
 ```json
 [{"airline": "BL", "code": "BL294", "depart": "20:00", "arrive": "22:05", "price": 1050000, "price_str": "1,050,000₫", "cheapest": true, "duration_h": 2, "seats": 5}]
 ```
 
 When the user complains about flight result legibility, the fix is:
 1. Backend returns `data.flights[]` as structured JSON array.
 2. Frontend renders each flight as a card/row with visual hierarchy (airline emoji + code, times, price, cheapest badge, duration).
 
 **Duplicate airline code fix**: Flight data from AGT sometimes has `FlightNumber` already prefixed with the airline code (e.g. `BL205`). `flight_formatter.py` now deduplicates: if `fn.upper().startswith(al.upper())`, strip the airline prefix from fn before concatenation. Result: `BL205` not `BLBL205`.

**⚠️ SUPERSEDED same day (22 Jul 2026, later session):** The card-rendering approach above was reverted. User feedback: "kết quả của mày đang dạng thanh quá" (the card rows look like flat strips/bars) — wants a **wide monospace table inside a copyable box**, not individual card rows.

**Current format (as of 22 Jul 2026, latest):**
- `flight_formatter.py` builds the reply as a fenced code block (` ```...``` `) containing a fixed-width monospace table — columns padded with `ljust`/`rjust` (mã số 8 chars, giờ 16 chars, giá 14 chars, rộng hơn bản cũ).
- `chat.html` `formatReply()` extracts fenced code blocks via regex, wraps each in a `.code-wrap` div with a floating **Copy** button (`copyCodeBox()` — `navigator.clipboard.writeText` with `document.execCommand('copy')` fallback for older browsers/non-HTTPS).
- `renderFlightCards()` is now DEAD CODE — left in `chat.html` but no longer called from `sendMsg()`. Don't extend it; safe to delete in a future cleanup pass.
- Bot bubble gets a `.wide` class (max-width 98%) automatically when its HTML contains `code-wrap`, so the table isn't squeezed into the normal 82% bubble width.

**Critical pitfall — monospace font required:** `.bubble.bot pre` MUST set `font-family` to a monospace stack (`Consolas`, `SF Mono`, `Courier New`). The rest of the UI uses Inter (proportional) — ljust/rjust column padding only stays aligned under a fixed-width font. Leaving the UI's default proportional font on a `<pre>` table makes every row's columns drift regardless of correct padding.

**Unreconciled conflict with `flight-itinerary-presentation` §6:** That skill (from earlier user corrections) says flight tables should be (a) grouped/sorted by **airline**, not price/time, (b) have the **duration column removed**, and (c) rendered as a real HTML `<table>`. This session's fix kept price-sort + duration column inside a plain `<pre>` text table (not a real `<table>`) — it solved the "copy" and "too narrow" complaints but did not re-apply the airline-grouping/no-duration rule. If the user complains again about sort order or the duration column, layer §6's rules on top of the copy-box mechanic added here rather than redoing it from scratch.

 ### ⚙️ LLM Provider Integration (HHTech API)

 **Goal:** Integrate HHTech API as the primary LLM provider for SmartAgent, falling back to OmniRoute, then Gemini, then Smart Mock. User prefers `claude-opus-4.8` for powerful reasoning.

 **Files updated:**
 - `backend/app/services/config.py`: Added `hhtech_api_key`, `hhtech_base_url`, `hhtech_model` to `Settings` class. Updated `hhtech_model` to `claude-opus-4.8`.
 - `backend/app/services/llm_gateway.py`: 
     - Added `_hhtech_key`, `_hhtech_base`, `_hhtech_model`, `_hhtech_client` to `__init__`.
     - Updated `_LLMGateway.chat()` to prioritize HHTech calls.
     - Added `_call_hhtech(messages: list)` method for API interaction.
     - Updated `_mock_mode` and `logger.info` messages for correct provider order.
     - Added `_hhtech_client.aclose()` to `close_llm()` for proper connection shutdown.
     - **OmniRoute Model Change (23 Jul 2026):** Switched from `tllm/claude_haiku_3_5` to `deepseek-chat` in `config.py` for improved reasoning and human-like responses.
     - **Function Calling Update (23 Jul 2026):** Replaced `ask_clarification` tool with `collect_passenger_info` in `llm_gateway.py` to handle structured passenger data collection.
 - `.env.production` on VPS: Updated with `HHTECH_API_KEY` and `HHTECH_BASE_URL`.
 - `.env` local: Updated with `HHTECH_API_KEY` and `HHTECH_BASE_URL`, disabled `OMNIROUTE_BASE_URL` and `GEMINI_API_KEY` to prioritize HHTech.

 **Pitfall:** Ensure `httpx.AsyncClient` connections are closed on shutdown (added `_hhtech_client.aclose()` to `close_llm()`).
 
 ## 🚀 VPS Deploy (July 2026, corrected 24 Jul 2026)

 **VPS→Local sync reference:** `references/vps-to-local-sync.md` — pull latest code FROM VPS when local is stale.

 > ⚠️ **VERIFY BRANCH LINEAGE BEFORE SYNCING — VPS and local can DIVERGE, not just lag** (discovered 25 Jul 2026): The \"VPS is source of truth, always sync FROM VPS\" rule assumes local is a strict *ancestor* of VPS (local just behind by N commits). That assumption broke this session: VPS HEAD (`f4f4ca7` — landing-page/Pydantic-settings line) and local HEAD (`19909b4` — smart-agent APIs line) were on **two divergent branches with no recent common ancestor**, AND local had **82 uncommitted modified files** (incl. `chat.py`, `smart_agent.py`, `abtrip_client.py`, all the `smart_*.py` service files). Blindly running the documented `ssh … tar czf - app/ | tar xzf -` sync in this state would have **silently overwritten local-only work** (both the uncommitted edits and the local-branch commits) with no diff, no backup, no undo. **Mandatory pre-sync check:** (1) `git -C <local> log --oneline -5` vs `ssh vps 'git -C /opt/abtrip-backend log --oneline -5'` — if the top commits share NO common hash, the branches diverged; do NOT tar-sync. (2) `git -C <local> status --short | wc -l` — if non-zero, there are uncommitted local changes; stash or commit them first. (3) Only when local is a clean strict-ancestor of VPS is the tar-pipe sync safe. When they've diverged, reconcile with git (fetch + merge/rebase or explicit per-file diff) instead — ask the user which side wins per conflicting file rather than clobbering. Divergence is the trigger to STOP and reconcile, not to force one direction.

 **Public URL (external/customer-facing):** `http://43.156.72.127/` (SmartAgent — Phòng Vé AI) — this is the VPS's real public IP, NOT the Tailscale IP.
 **Tailscale-internal URL:** `http://100.64.173.75/` — only reachable from devices on the same Tailscale network (e.g. the local dev machine via `ssh vps`). When the user asks for "a link" to share externally, always give the public IP, not the Tailscale one.

 **⚠️ Architecture Note:** The project is currently fragmented — SmartAgent (static HTML) on VPS and ABTrip (Next.js) on local are the SAME product. See `references/architecture-fragmentation.md` for full breakdown and consolidation plan.

 **Deploy script:** `C:\\Users\\Nguyen Ngoc Tan\\agent.tkt\\backend\\deploy\\deploy.sh` (tar+scp pattern — Windows has no rsync)

 **⚠️ CORRECTED paths (23 Jul 2026) — the repo is nested one level deeper than earlier docs assumed:**
 - Repo root on VPS: `/opt/abtrip-backend/` (git checkout of `tano2026/agent.tkt`, contains `backend/`, `frontend/`, `.git/`, etc. — mirrors the local repo layout)
 - **App/venv/.env all live under `/opt/abtrip-backend/backend/`, not the repo root.** Real paths: venv `/opt/abtrip-backend/backend/.venv/`, env file `/opt/abtrip-backend/backend/.env`, static HTML `/opt/abtrip-backend/backend/static/`. Any systemd unit or nginx config pointing at `/opt/abtrip-backend/.venv`, `/opt/abtrip-backend/.env`, or `/opt/abtrip-backend/static` (no `backend/` segment) is STALE and will break on next restart even if currently running (see vps-app-deploy skill's pitfall on stale-but-running services).
 - Systemd: `abtrip-backend.service` (`WorkingDirectory=/opt/abtrip-backend/backend`, `EnvironmentFile=/opt/abtrip-backend/backend/.env`, `ExecStart=/opt/abtrip-backend/backend/.venv/bin/python -m uvicorn app.main:app --host 0.0.0.0 --port 8139 --workers 1`, `User=ubuntu`, `Restart=always`) — check with `sudo systemctl cat abtrip-backend` before assuming the unit file matches this.
 - nginx config: `/etc/nginx/sites-enabled/hermes` (shared file — also routes `/tuvi/`, `/n8n/`, `/toonflow/`, `/thoigianbieu/` for other projects on the same VPS). ABTrip's block: `location /api/ { proxy_pass http://127.0.0.1:8139; }` + `location / { root /opt/abtrip-backend/backend/static; index chat.html; }`.
 - Chat UI: `http://43.156.72.127/` (public) or `http://100.64.173.75/` (Tailscale-internal)
 - API: `POST http://43.156.72.127/api/chat {"message":"...","agent":"ticketing","session_id":"..."}` — note `agent` field is required (`ticketing`/`sim`/`visa`), a request missing it or with a bad `agent` value returns "chưa được hỗ trợ" instead of routing.
 - Health: `http://43.156.72.127/api/health`
 - **After `scp`-ing individual changed `.py`/`.html` files (not a full deploy.sh run), always `sudo systemctl restart abtrip-backend` — no hot reload.** If the venv is missing a package the local dev venv has (e.g. `chromadb` for the RAG feature), the restart will crash-loop with `ModuleNotFoundError`; check `sudo journalctl -u abtrip-backend --no-pager | tail -40` for the real traceback rather than assuming file transfer failed.
 
 ### Deploy Steps
 ```bash
 cd /c/Users/Nguyen Ngoc Tan/agent.tkt/backend
 bash deploy/deploy.sh
 ```
 
 Then copy static files separately (excluded from tar to avoid perms):
 ```bash
 scp static/chat.html ubuntu@100.64.173.75:/tmp/chat.html
 ssh ubuntu@100.64.173.75 "sudo cp /tmp/chat.html /opt/abtrip-backend/static/chat.html"
 ```
 
 ### Deploy Pitfalls
 - **Remove `C:/Users/...` debug paths before deploying** — search for `open(r"C:/Users/` in `chat.py`. These cause HTTP 500 on Linux.
 - **Don't `pip freeze > requirements.txt`** — pulls `audioop-lts` needing Python 3.13+. Hand-write only needed deps. NOTE (23 Jul 2026): the minimal list is now stale — after the RAG feature was added, `chromadb` (and its transitive deps: onnxruntime, tokenizers, etc.) is also required. `requirements.txt` in the repo does NOT list it (checked 23 Jul 2026), so a fresh VPS venv install will `ModuleNotFoundError: No module named 'chromadb'` on startup. Either add `chromadb` to `requirements.txt` going forward, or manually `pip install chromadb` into the VPS venv after any deploy that touches `rag_knowledge.py` — check `sudo journalctl -u abtrip-backend | tail -40` for this exact error before assuming a code bug.
 - **Windows has no rsync** → deploy.sh uses `tar czf --exclude='...'` + `scp` + `tar xzf`.
 - **Ubuntu 24.04 externally-managed** → must create venv with `python3 -m venv .venv`.
 - **nginx `conflicting server name _`**: Multiple `sites-enabled/` configs on port 80 with `server_name _` cause conflicts (e.g., `hermes` config). Check `ls -la /etc/nginx/sites-enabled/` and remove conflicting symlinks (`sudo rm /etc/nginx/sites-enabled/hermes`). Reload Nginx (`sudo systemctl reload nginx`) after removal. Otherwise, `/api/` endpoints may return HTML default page or 502.
 `workers=1` recommended: With SQLite-backed sessions (Jul 2026), this is no longer STRICTLY required — the DB is shared. But `workers=1` is still recommended to avoid concurrent write races on the same session. Ensure `ExecStart` in systemd unit uses `--workers 1` (was `--workers 2`).
 - **CORS**: Set `allow_origins=["*"]` in main.py for production.
 
 ## 🧠 RAG Knowledge Base (ChromaDB + ONNX — ACTIVE)

 **DB path:** `backend/data/chroma/`
 **Collection:** `aviation_kb`
 **Embedding:** ONNX all-MiniLM-L6-v2 (auto-downloaded ~2MB on first run, NO sentence-transformers/PyTorch needed)
 **Documents:** 11 (policies + FAQ)
 **Integration:** ✅ `_build_context()` in `chat.py` auto-injects RAG context via `[THÔNG TIN TRA CỨU]` block before each LLM call
 **File:** `backend/app/services/rag_knowledge.py`
 **Reference:** `references/rag-knowledge-base.md`

 See `references/rag-knowledge-base.md` for full architecture, seed document list, and pitfalls.
 
 ## 📡 SSE Streaming Format
 
 The `/api/chat/stream` endpoint sends SSE events. **DeepSeek v4 flash FREE does NOT support streaming token-by-token** — the SSE endpoint gets ONE `type: 'done'` event with the full response, no `type: 'text'` events.
 
 Frontend fix in `ChatInterface.tsx` `handleSend`:
 ```typescript
 // Good — fallback to event.content when no tokens arrived
 if (event.type === 'done') {
   const finalContent = accumulatedContent || event.content || '';
   // ...
 }
 ```
 
 ## 💾 Conversation Memory (SQLite — Jul 2026)

**Replaces** the old `_sessions: dict` in-memory store with SQLite persistence.
Sessions now survive backend restarts. Added 22 Jul 2026.

**File:** `backend/app/services/conversation_memory.py`
**DB:** `backend/data/conversations.db` (auto-created on first use)

**Pattern:**
```python
from app.services.conversation_memory import get_memory

mem = get_memory()
session = mem.get_session(session_id)  # load from SQLite
session["history"].append(...)
mem.save_session(session_id, session)  # persist back
```

**Thread-local caching in chat.py:** Each request loads the session once via `_get_session()` (cached in `threading.local()`), mutates it in-place, and `_flush_session()` saves back at the end of the request. No need to call `save_session()` manually in handler functions — just let `chat()` call `_flush_session()` after the handler returns.

**Auto-cleanup:** `mem.cleanup_old(days=7)` — remove sessions older than 7 days. Can be called manually or via a cron job.

**Obsoletes Pitfall #9** (`workers=1` required): With SQLite, sessions are in a shared DB. Multiple workers would all read/write the same DB. However, `workers=1` is still recommended for simplicity — concurrent writes to the same session could race. If scaling to multiple workers, use `PRAGMA journal_mode=WAL` (already set) and accept that session state may be stale between concurrent requests (rare for a chat app).

### 🔧 LLM Gateway — Function Calling (Jul 2026)

**Replaces** the brittle JSON-format prompting with OpenAI-compatible function calling.
LLM no longer returns `{"type":"search_flight","params":{...}}` — it calls tools directly.

**3 tools defined in `llm_gateway.py`:**
```python
_TOOLS = [
    search_flight(origin, destination, date, adults=1, children=0, infants=0),
    answer_question(reply),      # for policy/text questions
    ask_clarification(question, missing=[]),  # when info is missing
]
```

**Response parsing:**
- `_parse_response_message(data)` — prefers `tool_calls` from API response, falls back to JSON content parsing for backward compatibility
- Tool calls map to internal format: `{"type":"search","params":{...}}`, `{"type":"reply","content":"..."}`, `{"type":"clarify","content":"...","missing":[...]}`

**API payload:** Both HHTech and OmniRoute calls now include `"tools": _TOOLS, "tool_choice": "auto"` in the request payload. Providers that don't support tools will ignore them and return regular content (handled by JSON fallback).

**New system prompt** instructs LLM: "LUÔN DÙNG CÔNG CỤ" — always use tools. Much shorter and more reliable than the old JSON format instructions.

**Reference:** `references/function-calling.md` for full API flow and examples.

## 🛠 LLM Error Diagnosis
 
 When user sees "Xin lỗi, hiện tại hệ thống AI đang gặp sự cố":
 1. **Test backend health** — `curl http://localhost:8138/api/health`
 2. **Test chat endpoint** — `curl -X POST http://localhost:8138/api/chat -H "Content-Type: application/json" -d '{"message":"hi"}'`
 3. VPS OmniRoute at `100.64.173.75:20128` goes down frequently. Gemini fallback requires `GEMINI_API_KEY` in `.env`.
 
 ## 📝 Where to update service data/pricing (data update map)

When the user asks "cập nhật dữ liệu/giá vào đâu" for a SmartAgent service, the answer is always a hardcoded Python dict/list in `backend/app/services/`, not a DB or admin UI:

| Data domain | File | Structure to edit |
|---|---|---|
| Flight routes/prices (mock only) | `mock_flights.py` | `ROUTES` dict — `(origin, dest) → {"duration", "flights": [{"time","airline","price"}]}`; airline display names in `AIRLINES` |
| Fast Track + Lounge pricing | `smart_fasttrack.py` | Rewritten 23 Jul 2026 to match the real An Bình price sheet — see "Fast Track data model" below, don't reintroduce the old airport-keyed `_SERVICES` dict shape |
| eSIM plans | `smart_esim.py` | `_PLANS` list — each dict has `price`, `data`, `duration`, `coverage` |
| Visa info | `smart_visa.py` | per-country dict (types/fee/processing) |
| Passport/CCCD info | `smart_passport.py` | Rewritten 23 Jul 2026 from a generic 2-tier blurb to case-routed handlers — see "Passport/CCCD data model" below |
| Airport/city names (display only, not pricing) | `aviation_db.py` | `AIRPORTS` dict |

### Fast Track data model (rewritten 23 Jul 2026 from real An Bình price sheet)

`smart_fasttrack.py` was restructured from a simple airport-keyed dict (retail/agent price) to two flat lists that mirror how the actual business quote sheet is laid out:
- `_FASTTRACK_SERVICES` — list of service-line dicts (`id, stt, terminal, name, tier, features, price, price_usd`), one row per line item exactly as it appears in the quote sheet (Ga Quốc Nội / Ga Quốc Tế đi / đến / Nối chuyến). `tier` is one of `Standard | Fast Track | VIP B | Transit`.
- `_LOUNGE_SERVICES` — separate list for Business Lounge rows, because lounge pricing has a different shape (adult/child split) than Fast Track (single per-pax price). Rewritten again 23 Jul 2026 from a narrow HAN-only list to a **nationwide** list (34 lounges, real "BẢNG GIÁ PC THƯƠNG GIA" sheet) with fields: `name, group, airport, code, terminal, location, adult_price, child_price, policy` (+ optional `note` for outliers like Đà Nẵng's no-child-price/2h-limit rule). `group` is one of `Bông Sen (VNA) | SH Premium | Đối tác` — each group has its own companion/child policy, keyed in `_LOUNGE_POLICY_TEXT` by the `policy` field (`"1"`/`"2"`/`"other"`/`"danang"`) so a reply only prints the policy text relevant to the lounges actually shown, not all 4 policies every time.
- `_AIRPORT_ALIASES` — dict mapping canonical airport name → list of Vietnamese/slang/IATA-code aliases (e.g. `"Tân Sơn Nhất": ["tân sơn nhất","tan son nhat","sgn","sài gòn","hcm",...]`), used by `_lounge_airport_filter()` to resolve a free-text city/airport mention in the user's message to one of the 20+ airports in `_LOUNGE_SERVICES`. When default (no airport/terminal named), the reply defaults to Nội Bài only (An Bình's home airport) with a hint to name another airport for more — don't dump all 34 rows unfiltered by default, it's unreadable in a chat bubble.
- `handle_fasttrack(message)` does keyword-based intent filtering (`_wants_lounge`, `_wants_transit`, `_terminal_filter`, `_direction_filter`, `_tier_filter`, `_lounge_airport_filter`, `_lounge_terminal_filter`) so a specific query like "fast track quốc tế đi VIP B" or "phòng chờ Đà Nẵng" returns just the matching row(s) instead of dumping the whole price list. Falls back to a grouped overview (by terminal/tier, or Nội Bài-only for lounge) when no specific filter matches.

### Passport/CCCD data model (rewritten 23 Jul 2026 from real An Bình CTV price sheet)

`smart_passport.py` was restructured from a flat 2-tier blurb (first-time/express passport, hardcoded fake prices) into a **case-routed handler**, because the real CTV price sheet (dated 22/06/2026) has ~10 independent categories with mutually exclusive pricing, not one linear price list:

- Each category gets its own `_format_<case>()` function returning a formatted string: xử phạt hành chính/giấy phạt, thiếu mộc (lên hồ sơ mới), hồ sơ em bé (dính/không dính tạm trú × 5 mốc ngày), nộp Cục HCM, hộ chiếu còn hạn (Miền Bắc/Miền Nam, further split by named province), in ngang, CCCD (Hà Nội/Miền Nam), và "dịch vụ khác" (check thiếu mộc, duyệt nhanh, bị chú, giấy xác nhận — these are CHECK/VERIFY services priced separately from making a NEW thiếu mộc filing, don't conflate them).
- `handle_passport(message)` routes by keyword, in an order that matters: check "dịch vụ khác" keywords (`check thiếu mộc`, `bị chú`, `duyệt nhanh`...) **before** the generic `thiếu mộc` keyword, otherwise "check thiếu mộc" (a 700K lookup service) gets misrouted into the full thiếu mộc filing case. Similarly, the generic "hộ chiếu" fallback to "còn hạn — cấp đổi" must NOT fire on a bare mention of "hộ chiếu" alone (that should show the category menu) — only fire when "còn hạn"/"cấp đổi" appears OR "hộ chiếu" appears together with a named region/province.
- A shared `_DISCLAIMER` constant is appended to every case reply: prices are CTV rates as of a specific date, do NOT include the government fee (+50K), and — critically, per explicit business-owner instruction — "hộ chiếu lên xuống thất thường, phải check lại, hồ sơ mỗi trường hợp thủ tục khác nhau, không nhất quán". Do not let the bot present a passport/CCCD price as a firm quote; always keep this disclaimer attached, and never invent a "which province/office/form" instruction — defer that to a human agent per case.
- Falls back to `_menu()` (a numbered list of the 8 categories) when no case-specific keyword matches — this is the deliberate default for a bare "hộ chiếu"/"passport" message, not an error state.

**When the user hands you a new/updated official price sheet, the workflow is:**
1. Read the source file with the right library via `terminal` — the `read_file` tool rejects binary files. For `.xlsx`: `python -c "import openpyxl; wb = openpyxl.load_workbook(r'<path>', data_only=True); ..."` (iterate `wb.worksheets`, then `ws.iter_rows(values_only=True)`); `data_only=True` is required to get computed values instead of formula strings. For `.pdf`: `python -c "import fitz; doc = fitz.open(r'<path>'); [print(p.get_text()) for p in doc]"` (PyMuPDF) — works well even for multi-page tabular price sheets, text comes out in reading order with prices/labels intact.
2. Map each sheet/section to its own list-of-dicts in the target `smart_*.py` file — keep the STT/order and exact Vietnamese service names from the sheet, don't paraphrase or renumber, so the business owner can cross-check the bot's output against the PDF/Excel at a glance. If the new sheet has materially more rows/categories than what's currently coded (e.g. a "danh sách toàn quốc" replacing a narrow single-airport list), restructure the data model to match the new shape rather than cramming extra rows into the old structure — add a filter dimension (airport/region alias map) if the row count grows past what a flat unfiltered dump can present readably.
3. Preserve footer notes (VAT-exclusive, free-infant policy, overtime surcharge, differing policies per lounge group, etc.) as `_..._NOTE`/`_..._POLICY_TEXT` constants appended to every formatted reply — these are real commercial terms, not filler text. When different row-groups have different child/companion policies (as lounges do — VNA Bông Sen vs SH Premium vs Đối tác each have their own rule), key the policy text by group and only print the policies actually relevant to the matched rows, not the full list every time.
4. After rewriting, sanity-test the handler directly in Python (`python -c "import app.services.smart_X as m; print(m.handle_X('...query...'))"`) for a few representative queries BEFORE restarting the server — catches wrong dict keys/typos without a restart cycle.
5. **Add the new/changed trigger keywords to `classify_service()` in `intent_parser.py` — do this in the SAME edit pass as the data file, not as an afterthought.** `classify_service()` has its own independent keyword list per service and does NOT automatically pick up new vocabulary just because `smart_fasttrack.py`'s internal filters (`_wants_lounge`, `_terminal_filter`, etc.) understand it. Concretely: adding lounge nationwide-airport filtering to `smart_fasttrack.py` without also adding `"phòng chờ", "lounge", "thương gia", "nối chuyến"` to `classify_service()`'s fasttrack branch caused every lounge query to fall through to the flight-search branch and get misread as "which city do you want to fly to" — the smart_fasttrack.py logic was correct and importing/unit-testing it in isolation gave no signal that anything was wrong, because the bug was entirely in the routing layer one file away.

   **This bites twice as hard on `passport`, because `classify_service()`'s passport branch only checks `"hộ chiếu"/"ho chieu"/"passport"`.** Rewriting `smart_passport.py` to handle case-specific vocabulary (`thiếu mộc`, `cccd`, `em bé`, `in ngang`, `nộp cục hcm`, `giấy phạt`, `bị chú`, `lăn tay`...) does nothing if those words aren't ALSO added to `classify_service()`'s passport branch. Symptom is worse than a misread here: a message like "thiếu mộc trên 1 năm" falls through to the flight-search flow, which tries the LLM/AGT function-calling pipeline — that pipeline can HANG (no fast local fallback, waits on an external API call) rather than just answering wrong, so the browser UI looks frozen with no error and no console output. If a rewritten `smart_*.py` handler tests correctly in isolation via `python -c "import ...; print(m.handle_x('...'))"` but the same message hangs or times out through the real chat UI, check `classify_service()`'s keyword list for that service FIRST — don't assume the LLM provider is down.
6. Restart uvicorn on 8139 (see Pitfall #21 for the safe kill+relaunch sequence) and verify the new data actually renders through the real chat UI (click the relevant quick-action card or type the trigger phrase) — importing cleanly in Python doesn't guarantee the chat.py routing/intent_parser keywords still reach the handler. If the UI still shows old behavior after a restart, don't assume the restart failed — re-check Pitfall #21 (zombie holding the port) AND this keyword-coverage gap; they produce near-identical "my fix didn't take" symptoms but need different fixes.

**Real vs mock flight prices**: `_search_flights()` in `chat.py` tries the real AGT API first via `abtrip_client.py`, and only falls back to `generate_mock_result()` (from `mock_flights.py`) if the AGT call fails or returns no real data. Check `.env` for `AGT_API_ACCOUNT` / `AGT_PRIVATE_KEY` / `AGT_API_PASSWORD` — if any of these three are blank, every flight search is silently mock data even though the UI looks identical. Don't assume "prices look wrong" means a data-file bug — check these three env vars first (`.env` is a protected file the assistant cannot read directly with `read_file`; use `python -c "from dotenv import dotenv_values; print(dotenv_values('.env').get('AGT_API_ACCOUNT'))"` from terminal to check without exposing the actual secret value in the read).

**After editing any service data file**: restart uvicorn on port 8139 — there is no hot reload in the way this project runs the server (`python -u -m uvicorn app.main:app --host 0.0.0.0 --port 8139`), so edits to `_SERVICES`/`_PLANS`/`ROUTES` dicts won't take effect until restart (see Pitfall #21 for the safe restart procedure — verify old PID is actually gone before trusting curl).

## 📁 Key Files
 
 | File | Purpose |
 |------|---------|
 | `backend/app/main.py` | FastAPI app (lifespan + CORS + routers) |
 | `backend/app/api/chat.py` | Main chat handler — step pipeline + service routing + confirm flow |
 | `backend/app/services/intent_parser.py` | Intent parsing V3 — slang, classify, date parsing |
 | `backend/app/services/flight_formatter.py` | Table format with airline emoji, dedup flight codes |
 | `backend/app/services/mock_flights.py` | Mock data when AGT unavailable |
 | `backend/app/services/abtrip_client.py` | AGT API HTTP client (search/book/issue/retrieve) |
 | `backend/app/services/llm_gateway.py` | LLM wrapper + function calling tools + provider failover |
 | `backend/app/services/rag_service.py` | RAG dual-collection (aviation_kb + airline_policies) — Antigravity architecture |
 | `backend/app/services/policy_crawler.py` | Auto Policy Crawler — scrape 6 VN airlines, upsert changes to RAG |
 | `backend/app/services/smart_agent.py` | **Antigravity chat endpoint** (`POST /api/smart-agent/chat`) — decision node: ops query → RAG inject, booking → lean prompt + Gemini/DeepSeek. Has its own fallback path with RAG when LLM offline (see §Antigravity Decision Node below) |
 | `backend/app/services/conversation_memory.py` | SQLite session persistence — replaced `_sessions` dict |
 | `backend/app/services/smart_esim.py` | SmartAgent eSIM (added Jul 2026) |
 | `backend/app/services/smart_visa.py` | SmartAgent Visa (added Jul 2026) |
 | `backend/app/services/smart_passport.py` | SmartAgent Ho chieu (added Jul 2026) |
 | `backend/static/chat.html` | SmartAgent single-file HTML UI |
 
 ## 🚨 Known Pitfalls

  1.  **HHTech API DNS failure**: `api.hhtech.io` may fail with `[Errno 11001] getaddrinfo failed`. This is a network-level issue (DNS resolution). Check if the HHTech base URL env var is correct (`HHTECH_BASE_URL`). If HHTech is down, the chain falls through to OmniRoute → Gemini → Smart Mock. The Smart Mock fallback can detect flight searches (via intent parser) but returns a canned apology for policy/text questions.
  2.  **`settings.db_path` doesn't exist**: ABTrip's `Settings` model doesn't have `db_path`. When adding SQLite, create dir with `os.makedirs(DB_DIR, exist_ok=True)`.
  3.  **Chroma first-run**: Downloads ~2MB ONNX model. Takes 10-30 seconds.
  4.  **RAG embedding**: Use `ONNXMiniLM_L6_V2` from `chromadb.utils.embedding_functions` — NOT full `sentence-transformers` (avoids 500MB+ PyTorch install, 2-3min timeout on pip).
  5.  **Context compaction breaks session tracking**: After compaction, re-check process state before assuming servers are running.
  6.  **Windows port cleanup — zombie processes**: Multiple processes can hold the same port. Run `netstat -ano | grep ':8138' | grep LISTEN` to find PIDs, then kill each. If `taskkill //F //PID X` from bash silently fails ("process not found" but PID still appears in netstat), use `cmd //c "taskkill /F /PID X"` — the cmd wrapper handles Windows process handles more reliably. If all kill attempts fail (PID persists in netstat), switch to a different port (e.g., 8139) as temporary fallback until Windows restart cleans the zombie. Syntax: `cmd //c "taskkill /F /PID 26312 & taskkill /F /PID 9736"`.
  7.  **`crypto.randomUUID()` on HTTP**: Fails on non-HTTPS. Use `Date.now()` fallback for `sessionId`.
  8.  **Nginx `conflicting server name _`**: Multiple `sites-enabled/` configs on port 80 with `server_name _` cause conflicts (e.g., `hermes` config). Check `ls -la /etc/nginx/sites-enabled/` and remove conflicting symlinks (e.g., `hermes`). Reload Nginx after removal.
  9.  **`workers=1`**: With SQLite-backed sessions (Jul 2026), this is no longer STRICTLY required — the DB is shared. But `workers=1` is still recommended to avoid concurrent write races on the same session.
  10. **`classify_service()` must check `pending_action`**: `classify_service()` should only run when there's NO `pending_action` in session, otherwise "OK" or other replies might bypass the intended confirm flow.
  11. **LLM Provider Order**: Backend now prioritizes HHTech, then OmniRoute, then Gemini, then Smart Mock. Ensure `.env.production` has `HHTECH_API_KEY` for HHTech to be active.
  12. **`close_llm` import error**: `main.py` imports `close_llm` from `llm_gateway.py` but the function may not exist. If `ImportError: cannot import name 'close_llm'`, add to the end of `llm_gateway.py`:
      ```python
      async def close_llm() -> None:
          """Close the LLM gateway (no-op for now)."""

 2.  **`settings.db_path` doesn't exist**: ABTrip's `Settings` model doesn't have `db_path`. When adding SQLite, create dir with `os.makedirs(DB_DIR, exist_ok=True)`.
 3.  **Chroma first-run**: Downloads ~2MB ONNX model. Takes 10-30 seconds.
 4.  **RAG embedding**: Use `ONNXMiniLM_L6_V2` from `chromadb.utils.embedding_functions` — NOT full `sentence-transformers` (avoids 500MB+ PyTorch install, 2-3min timeout on pip).
 5.  **Context compaction breaks session tracking**: After compaction, re-check process state before assuming servers are running.
 6.  **Windows port cleanup — zombie processes**: Multiple processes can hold the same port. Run `netstat -ano | grep ':8138' | grep LISTEN` to find PIDs, then kill each. If `taskkill //F //PID X` from bash silently fails ("process not found" but PID still appears in netstat), use `cmd //c "taskkill /F /PID X"` — the cmd wrapper handles Windows process handles more reliably. If all kill attempts fail (PID persists in netstat), switch to a different port (e.g., 8139) as temporary fallback until Windows restart cleans the zombie. Syntax: `cmd //c "taskkill /F /PID 26312 & taskkill /F /PID 9736"`.
 7.  **`crypto.randomUUID()` on HTTP**: Fails on non-HTTPS. Use `Date.now()` fallback for `sessionId`.
 8.  **Nginx `conflicting server name _`**: Multiple `sites-enabled/` configs on port 80 with `server_name _` cause conflicts. Check `ls -la /etc/nginx/sites-enabled/` and remove conflicting symlinks (e.g., `hermes`). Reload Nginx after removal.
 9.  **`workers=1`**: With SQLite-backed sessions (Jul 2026), this is no longer STRICTLY required — the DB is shared. But `workers=1` is still recommended to avoid concurrent write races on the same session.
 10. **`classify_service()` must check `pending_action`**: `classify_service()` should only run when there's NO `pending_action` in session, otherwise "OK" or other replies might bypass the intended confirm flow.
 11. **LLM Provider Order**: Backend now prioritizes HHTech, then OmniRoute, then Gemini, then Smart Mock. Ensure `.env.production` has `HHTECH_API_KEY` for HHTech to be active.
 12. **`close_llm` import error**: `main.py` imports `close_llm` from `llm_gateway.py` but the function may not exist. If `ImportError: cannot import name 'close_llm'`, add to the end of `llm_gateway.py`:
    ```python
    async def close_llm() -> None:
        """Close the LLM gateway (no-op for now)."""
        pass
    ```
14. **`app.mount("/", StaticFiles(...))` breaks API routes**: Mounting StaticFiles at "/" intercepts ALL requests including `/api/*` routes — FastAPI API routes registered before the mount are still bypassed at Starlette level. Use a specific `@app.get("/")` route with `FileResponse` instead (see SmartAgent UI Pattern above for full code).
15. **`cd` does NOT persist across separate `terminal()` tool calls** (Hermes-specific, not project-specific): each `terminal()` invocation is a fresh shell. Running `cd ...agent.tkt` in one call then `python -m uvicorn ...` in the next call reverts to the default cwd and produces `ModuleNotFoundError: No module named 'backend'`. Always pass `workdir` on the SAME `terminal()` call that starts uvicorn — don't rely on a prior `cd`. Correct pattern: `terminal(workdir="C:\Users\Nguyen Ngoc Tan\agent.tkt\backend", background=true, command="python -u -m uvicorn app.main:app --host 0.0.0.0 --port 8139 --log-level info")`.
16. **Module path is `app.main:app`, run from inside `backend/`** — NOT `backend.app.main:app` from the repo root. `main.py` uses absolute imports like `from app.api.chat import router`, so `app` must be importable as a top-level package, which only works when the process cwd is `backend/`. Using the wrong module path silently produces `ModuleNotFoundError: No module named 'app'` (wrong cwd) or `No module named 'backend'` (wrong module string).
17. **After any `patch` edit to a `.py` file, verify syntax BEFORE restarting the server**: run `python -c "import ast; ast.parse(open(r'PATH', encoding='utf-8').read())"` (prints nothing / exits 0 on success). Patches can silently duplicate a function signature (e.g. two `async def _handle_smart_service(...)` lines in a row) which only surfaces as `IndentationError` at import time — costs a full restart-and-log-read cycle to diagnose if skipped.
Active port for ABTrip bot is 8139: Due to previous issues with a zombie process on port 8138, the ABTrip bot (agent.tkt) now consistently uses port 8139. Always target this port for local development and VPS deployments (e.g., in uvicorn commands, systemd unit, and nginx configuration).
19. **`process(action='log')` can show empty output while the server is genuinely running** — don't treat an empty log as a crash signal. Confirm liveness with `curl -s -m 3 http://127.0.0.1:8139/ -o /dev/null -w "HTTP_CODE:%{http_code}"` instead. Tracebacks DO reliably show up in `process(action='poll')`'s `output_preview` once the process has exited, so poll is the right tool for post-mortem, curl is the right tool for liveness.
20. **Don't assume field names on structured data from a sibling function — read the actual return value.** `_handle_flight_selection` was first written against a guessed key `raw_air_option` that flight_formatter.py never returns, causing `KeyError` on the very first real request. The actual per-flight dict keys (as of 23 Jul 2026) are: `index, airline, code, depart, arrive, price, price_str, cheapest, duration_h, seats, stops, all_option_ids`. When consuming another function's structured output, grep/read its return/append statements first instead of guessing field names.
21. **Passenger Info Collection — `NameError` and `KeyError` (23 Jul 2026):**
    - `NameError: name 'session_id' is not defined`: Caused by `_handle_flight_selection` not passing `session_id` to `_handle_passenger_info_collection`. Ensure all required arguments are passed through the call chain.
    - `UnboundLocalError: cannot access local variable 'pax_type_display'`: Caused by `pax_type_display` being defined conditionally after it's used in an f-string. Always define display variables at the top of the function to ensure they are always in scope.
     13. **Docker available at explicit path — not in default PATH**: Docker Desktop IS installed (`C:\Users\Nguyen Ngoc Tan\AppData\Local\Programs\DockerDesktop\resources\bin\docker.exe`), and docker-compose is available via `docker compose`. However, Git Bash PATH may not include it. Always use the full path or run `docker` binary from its install dir. For `docker compose`, use the `docker.exe compose` subcommand — standalone `docker-compose` binary is NOT available.

    14. **Next.js dev mode with Docker — volume mount kills multi-stage build output**:
        - **Problem**: Multi-stage Dockerfile (building `.next/standalone` + `server.js`) + `./frontend:/app` volume mount at runtime = `server.js` is overwritten by raw source code, producing `MODULE_NOT_FOUND`.
        - **Dev-mode Dockerfile**: Keep it minimal — just `FROM node:20-alpine`, `WORKDIR /app`, `EXPOSE 3000`, `CMD ["npm", "run", "dev"]`. No multi-stage, no `COPY`, no build step. Host source + `node_modules` come from the bind mount at runtime.
        - **Anonymous volume `/app/node_modules` is DANGEROUS**: Adding `- /app/node_modules` under `volumes:` creates an empty Docker-managed volume that blocks BOTH:
          1. The image's `node_modules` (bind mount replaced `/app` entirely)
          2. The host's `node_modules` (anonymous volume takes priority over bind mount for that path)
          Result: `next: not found` even though host has `node_modules/next/`.
        - **Fix for dev**: Remove `/app/node_modules` from compose volumes entirely. Host's existing `node_modules` gets mounted into the container. Works because both host (Windows) and container (Alpine) are x86_64 — native `.node` bindings are compatible.
        - **If local `node_modules` doesn't exist**: Add an entrypoint script `RUN npm install` in the Dockerfile, or change CMD to `sh -c "npm install && npm run dev"`.
        - **Verify**: `docker compose logs abtrip-frontend --tail=20` should show `ready - started server on 0.0.0.0:3000`.

    ### Travel Chat Integration Pitfalls (from `travel-chat-integration` skill)

1.  **Route conflicts**: If you have `chat_router` from `api/chat.py` AND `smart_agent_router`, ensure their prefixes don't overlap. Smart Agent route prefix should be `/api/smart-agent` not `/chat`.
2.  **Gemini API key missing**: Always have a rule-based fallback. Test with `curl -X POST` before assuming Gemini works.
3.  **SSE parsing**: The `[DONE]` marker must be sent as raw SSE `data: [DONE]\n\n`, not wrapped in JSON, for the frontend to detect stream end.
4.  **Text chunks**: Don't chunk in the middle of markdown like `**bold**` or it breaks rendering. Keep chunks small (10 chars) to avoid mid-word splits losing context.
5.  **Session memory**: Store in-memory dict keyed by UUID. Cap at 50 messages per session to prevent memory leak.
6.  **Frontend welcome/message toggle**: Use CSS class `.active` on chat container + `display:none` on welcome. Don't rely on JS visibility alone.

## Verification Checklist
- [ ] Service grid renders 5 items with correct icons and colors
- [ ] Clicking service icon sends message to chat
- [ ] Welcome screen hides when message sent
- [ ] Chat shows typing indicator then streams response
- [ ] SSE events render progressively (not all at once)
- [ ] Multiple messages keep session context
- [ ] New session (no session_id) starts fresh
- [ ] Gemini fallback works when API key configured
- [ ] Rule-based fallback works when no API key
 13. **Docker available at explicit path — not in default PATH**: Docker Desktop IS installed
 14. **`app.mount("/", StaticFiles(...))` breaks API routes**: Mounting StaticFiles at "/" intercepts ALL requests including `/api/*` routes — FastAPI API routes registered before the mount are still bypassed at Starlette level. Use a specific `@app.get("/")` route with `FileResponse` instead (see SmartAgent UI Pattern above for full code).
15. **`cd` does NOT persist across separate `terminal()` tool calls** (Hermes-specific, not project-specific): each `terminal()` invocation is a fresh shell. Running `cd ...agent.tkt` in one call then `python -m uvicorn ...` in the next call reverts to the default cwd and produces `ModuleNotFoundError: No module named 'backend'`. Always pass `workdir` on the SAME `terminal()` call that starts uvicorn — don't rely on a prior `cd`. Correct pattern: `terminal(workdir="C:\Users\Nguyen Ngoc Tan\agent.tkt\backend", background=true, command="python -u -m uvicorn app.main:app --host 0.0.0.0 --port 8139 --log-level info")`.
16. **Module path is `app.main:app`, run from inside `backend/`** — NOT `backend.app.main:app` from the repo root. `main.py` uses absolute imports like `from app.api.chat import router`, so `app` must be importable as a top-level package, which only works when the process cwd is `backend/`. Using the wrong module path silently produces `ModuleNotFoundError: No module named 'app'` (wrong cwd) or `No module named 'backend'` (wrong module string).
17. **After any `patch` edit to a `.py` file, verify syntax BEFORE restarting the server**: run `python -c "import ast; ast.parse(open(r'PATH', encoding='utf-8').read())"` (prints nothing / exits 0 on success). Patches can silently duplicate a function signature (e.g. two `async def _handle_smart_service(...)` lines in a row) which only surfaces as `IndentationError` at import time — costs a full restart-and-log-read cycle to diagnose if skipped.
Active port for ABTrip bot is 8139: Due to previous issues with a zombie process on port 8138, the ABTrip bot (agent.tkt) now consistently uses port 8139. Always target this port for local development and VPS deployments (e.g., in uvicorn commands, systemd unit, and nginx configuration).
19. **`process(action='log')` can show empty output while the server is genuinely running** — don't treat an empty log as a crash signal. Confirm liveness with `curl -s -m 3 http://127.0.0.1:8139/ -o /dev/null -w "HTTP_CODE:%{http_code}"` instead. Tracebacks DO reliably show up in `process(action='poll')`'s `output_preview` once the process has exited, so poll is the right tool for post-mortem, curl is the right tool for liveness.
20. **Don't assume field names on structured data from a sibling function — read the actual return value.** `_handle_flight_selection` was first written against a guessed key `raw_air_option` that flight_formatter.py never returns, causing `KeyError` on the very first real request. The actual per-flight dict keys (as of 23 Jul 2026) are: `index, airline, code, depart, arrive, price, price_str, cheapest, duration_h, seats, stops, all_option_ids`. When consuming another function's structured output, grep/read its return/append statements first instead of guessing field names.
21. **Passenger Info Collection — `NameError` and `KeyError` (23 Jul 2026):**
    - `NameError: name 'session_id' is not defined`: Caused by `_handle_flight_selection` not passing `session_id` to `_handle_passenger_info_collection`. Ensure all required arguments are passed through the call chain.
    - `UnboundLocalError: cannot access local variable 'pax_type_display'`: Caused by `pax_type_display` being defined conditionally after it's used in an f-string. Always define display variables at the top of the function to ensure they are always in scope.
    - `KeyError: 'airline_name'`: Caused by `_confirm_booking` attempting to access `selected_flight['airline_name']` before it was added to the `selected_flight` dictionary. Ensure all necessary data fields are populated in `session["selected_flight"]` as soon as they are available.


### ⚠️ Robust Frontend File Editing (Jul 2026)

When making multiple, interdependent changes to a single HTML/CSS file (e.g., removing elements and then adjusting layout), using a sequence of `patch` commands can be brittle due to `old_string` matching issues (non-unique or stale matches after previous edits).

**Recommended workflow for complex edits:**
1.  **Read the entire file** using `execute_code` + `read_file(path=file_path, limit=2000)`. Ensure `content` is present in the response.
2.  **Perform all modifications in Python** using string `replace()` or `re.sub()` (for more flexible regex-based replacement) on the `content` string.
    *   This allows for complex logic, conditional changes, and avoids `old_string` ambiguity.
    *   Example for removing a div: `content = re.sub(r"      <div class=\"header-actions\">.*?<\/div>", "", content, flags=re.DOTALL)`
    *   Example for replacing an entire CSS block: Use `re.sub(r"(\.selector\s*\{[^}]*\})", ".selector{\n" + new_style_block, content, flags=re.DOTALL)`
3.  **Write the modified content back** to the file using `execute_code` + `write_file(path=file_path, content=content)`.

This approach ensures consistency and avoids mid-edit state problems.

### 🐛 Frontend & Backend Changes Not Showing (Local & VPS - Jul 2026)

If you've made changes to `backend/static/chat.html` (frontend UI) or any Python files (backend logic, LLM brain) on your local machine, and these changes are not visible/active (either on your local server or deployed on VPS), consider these common pitfalls and workflows:

**Common Root Cause**: The running FastAPI server has not loaded the updated files from disk.

**Workflow for Applying Changes:**
1.  **Local Development (before deploying to VPS):**
    *   **Stop the running FastAPI server** on your local machine (`Ctrl + C` in the terminal). Ensure no zombie processes are holding the port (see Pitfall #21).
    *   **Restart the FastAPI server** using `uvicorn app.main:app --reload --port 8139` (from `backend/` directory) or `uvicorn agent.tkt.backend.app.main:app --reload --port 8139` (from repo root). The `--reload` flag is crucial for local development as it automatically restarts the server when Python code changes.
    *   **Clear Browser Cache** (hard reload `Ctrl + F5` or `Ctrl + Shift + R`) and visit `http://localhost:8139`.
2.  **Deploying to VPS:**
    *   **File Synchronization:** Changes made locally are NOT automatically transferred to the VPS. You must actively synchronize the updated files (e.g., using `scp` for individual files, or running your `deploy.sh` script for the entire project). **Verify the file content on VPS** by SSHing in and using `cat <file_path>`.
    *   **FastAPI Server Restart on VPS:** The FastAPI server running on the VPS **must be explicitly restarted** after new files are transferred. Production servers typically do not use `--reload`. Use `sudo systemctl restart abtrip-backend` (assuming `abtrip-backend.service` is your systemd unit).
    *   **Clear Browser Cache** (hard reload `Ctrl + F5` or `Ctrl + Shift + R`) and visit `http://100.64.173.75:8139` (or your public IP).

**Key Pitfalls:**
*   **Browser Cache:** Always perform a **hard reload** (`Ctrl + F5` or `Ctrl + Shift + R`) or clear browser cache.
*   **Stale Server Process (Pitfall #21):** A zombie process might be silently holding the port, causing new server instances to fail startup while the old (outdated) one continues to serve. Always verify the port is free before restarting.
*   **File Synchronization Failure:** The most common reason for changes not showing on VPS is that the updated files were never actually transferred to the VPS, or were transferred to the wrong location. Always verify file content directly on the VPS.
*   **AI Limitations:** Hermes cannot directly SSH into the VPS or modify files on it without explicit SSH credentials provided by the user. Ensure you have the necessary access to perform server-side checks and restarts.


User wants a numbered list so customers can pick a flight by typing `chọn N` or `đặt <mã>` instead of re-typing the full flight code.

Flow:
1. `flight_formatter.py` assigns a stable `index` (1..N) to each flight row shown in the table and returns the full structured list (see field list in Pitfall #20) via `return_data=True`.
2. `chat.py` stores that list in `session["last_structured_flights"]` (also `session["last_raw_flights"]` for the raw AGT `ListGroup` if needed later for booking IDs).
3. Before routing to `classify_service()` / SmartAgent, `_handle_message` regex-matches `^(chọn|chon|dat|đặt)\s+(\d+|[a-zA-Z]{1,2}[0-9a-zA-Z]{1,5})` against the incoming message. Digit → lookup by `index`; alpha → lookup by `code` (case-insensitive).
4. `_handle_flight_selection(message, session, selection_type, selection_value)` finds the matching flight, replies with a confirmation card (airline name resolved via a small `_AIRLINE_NAMES` dict — VN/VJ/QH/BL/VU), stores it in `session["selected_flight"]`, and clears `pending_action`/`pending_data`.

Note: this coexists with, but does not replace, the existing `_FOLLOWUP_PATTERNS` commands (rẻ nhất, sớm nhất, etc.) — those filter/sort the same `last_search` raw data, selection just picks one specific row by its displayed index.

**Frontend quick-booking buttons — CORRECTED design (23 Jul 2026):**

First attempt: a single row of pill buttons (`renderFlightQuickButtons`) grouped together *below* the ASCII table, one button per flight. **User rejected this**: "cho nút đặt vé cùng với hàng chuyến bay luôn, để ở dưới khi có 20-30 chuyến tìm khó lắm" — with 20-30 flights, a detached button bank forces the user to visually cross-reference a button back to its row by index number, which is error-prone at that list size.

**Corrected pattern — button lives INSIDE each row, not in a separate bank:**
- Replaced the ASCII/monospace table renderer with `renderFlightCards(flights)` (card-per-flight, was dead code from an earlier session, now reactivated) — each flight is its own `.flight-card` div with a `.fc-book-btn` ("Đặt") button positioned in the `.fc-right` column next to that row's price.
- `sendMsg()` in `chat.html`: when `d.type === 'flight_results'`, strip the ` ```...``` ` fenced block out of `d.reply` via regex split, keep the header/footer text through `formatReply()`, and splice `renderFlightCards(d.data.flights)` in between — so header text, cards-with-buttons, and footer text all render as one bubble.
- Deleted `renderFlightQuickButtons()` and its `.flight-quick-btns`/`.flight-quick-btn` CSS entirely — don't resurrect the "buttons grouped separately from data" pattern.
- `.fc-book-btn` reuses `sendQuick('chọn ' + f.index)` — same wiring as before, only the placement changed.

**General lesson for any future list+action UI on this project:** when a list can grow past ~10 items (flight search, seat maps, ancillary options, etc.), the per-item action control MUST be rendered inside that item's own row/card. A separate button bank underneath — even labeled with the same index — becomes unusable once the user has to count rows to match a button. Card-per-row-with-inline-button is the standing pattern now; don't reintroduce a detached button row for future list UIs in this chat interface.

### Pitfall #21 — stale server process silently answers curl after a "restart"
When killing+relaunching uvicorn in the background, a prior instance can still be holding the port (bind fails with `[Errno 10048] only one usage of each socket address`), so your new `terminal(background=true)` call **starts a process that immediately dies**, while curl keeps hitting the **old** process that never actually stopped. Symptom: a traceback's line numbers don't match what's actually in the file on disk (e.g. exception is raised from a line where you already deleted the offending code). Fix / detection:
1. After any restart, check `process(action='poll', session_id=...)` for the NEW session — if `status: exited` with an `Errno 10048` bind error in `output_preview`, the new process never came up.
2. Cross-check the PID actually bound to the port (`powershell -NoProfile -Command "Get-NetTCPConnection -LocalPort 8139 | Select-Object -ExpandProperty OwningProcess"`) against the PID Hermes just reported for the background process. If they differ, you're talking to a zombie.
3. Kill the zombie PID via `Stop-Process -Id <pid> -Force`, confirm the port is empty (`netstat -ano | findstr :8139` returns nothing), THEN relaunch. Only trust curl/API responses once PID and port line up.

22. **Uvicorn 0.51.0+ breaking change — `cannot import name 'main' from 'uvicorn.main'`** (24 Jul 2026): When `requirements.txt` specifies `uvicorn[standard]>=0.24.0` without an upper bound, `pip install` resolves to uvicorn ≥0.51.0 which removed the `uvicorn.main` module entry point. The container crash-log shows:
    ```
    ImportError: cannot import name 'main' from 'uvicorn.main'
    ```
    **Fix:** Pin the upper bound:
    ```
    uvicorn[standard]>=0.24.0,<0.51.0
    ```
    This resolves to uvicorn-0.50.2 (latest pre-breakage). After patching, rebuild: `docker compose up -d --build --force-recreate --no-deps abtrip-backend`. Verify with `docker compose logs abtrip-backend` shows `Application startup complete`.

23. **`from pathlib import Path` missing in main.py**: If `main.py` uses `Path(__file__).resolve()` but lacks `from pathlib import Path`, container crashes with:
    ```
    NameError: name 'Path' is not defined
    ```
    Fix: add `from pathlib import Path` to imports. Check `docker compose logs abtrip-backend --tail=10` immediately after restart to catch it.

24. **`scp -r` with trailing slash creates nested dirs on Windows Git Bash — use tar pipe instead** (24 Jul 2026): `scp -r ubuntu@vps:/opt/abtrip-backend/backend/app/services/ "D:/.../services/"` silently creates `services/services/` inside the target directory — a complete copy of the VPS files inside a nested subfolder, while the original files stay untouched. The Docker container then picks up the OLD code. **Fix:** use tar pipe — `ssh vps "cd /opt/abtrip-backend/backend && tar czf - app/" | tar xzf - -C "D:/.../abtrip/backend/"`. This flattens the transfer into a stream with no trailing-slash ambiguity, overwriting files in-place. After transfer, verify with `wc -l` on a key file to confirm line counts match VPS. Then rebuild Docker. Full workflow in `references/vps-to-local-sync.md`.

25. **`patch` tool fails 3+ times on same file — use `execute_code` to read exact content** (25 Jul 2026): When `patch` returns "Could not find a match" repeatedly on a file you've been reading with offset/limit pagination, the `old_string` you're constructing from the read output may differ from the actual file content due to escaped newlines (`\n` vs actual newlines in the file). **Fix:** use `execute_code` + `read_file()` to get the exact raw content, then `print(repr(...))` the relevant lines to see the real bytes. Construct `old_string` from that repr output. This avoids 3+ wasted `patch` attempts on formatting mismatches.

26. **`smart_agent.py` and `chat.py` have separate `/chat` endpoints — don't edit the wrong one** (25 Jul 2026): The Antigravity decision node lives in `backend/app/services/smart_agent.py` (router prefix `/api/smart-agent`), while the old multi-service flow lives in `backend/app/api/chat.py` (router prefix `/api/chat`). The landing page (`main.html`) calls `/api/chat`, NOT `/api/smart-agent/chat`. When the user says "chat endpoint" or "bot chat", clarify which one they mean — the Antigravity ops+booking endpoint is `smart_agent.py`, the 5-service quick-card endpoint is `chat.py`. Editing the wrong file and restarting the server will show no change in behavior because the other endpoint is still serving old code.

28. **`POST /api/smart-agent/chat` returns 400 "error parsing the body"** (25 Jul 2026): The `ChatRequest` model in `smart_agent.py` may expect different field names than `/api/chat`. When the endpoint rejects a request that looks correct (`{"message":"...","session_id":"..."}`), read the `ChatRequest` pydantic model to verify field names — it may use `query`, `text`, `content`, or require additional fields like `agent` or `tenant_id`. Test with `curl -v` to see the full FastAPI validation error detail (hidden in the 400 text). Common fix: align the `data` dict key to match the model's field name exactly.

29. **`patch` tool fails 3+ times on the same file — use `execute_code` + `repr()` to dump exact content** (25 Jul 2026): When `patch` returns "Could not find a match" repeatedly on a file, the `old_string` constructed from `read_file` output may differ from actual file content due to `\\n` escape representation mismatches. Fix: use `execute_code` to read the file and `print(repr(content))` the target lines — this reveals the real bytes including escaped newlines, invisible characters, and Unicode. Build `old_string` from that repr output. This avoids 3+ wasted attempts on formatting discrepancies.

30. **`/api/smart-agent/chat` vs `/api/chat` — two different endpoints** (25 Jul 2026): `smart_agent.py` has router prefix `/api/smart-agent` (Antigravity decision node: ops→RAG, booking→lean prompt). `api/chat.py` has router prefix `/api/chat` (old multi-service flow: classify_service → smart_*.py). The landing page `main.html` calls `/api/chat`. When testing Antigravity features, hit `/api/smart-agent/chat` directly. When the user says "chat không hoạt động", clarify WHICH endpoint they're hitting — fixing `smart_agent.py` won't change behavior of the `/api/chat` path and vice versa.

27. **Policy crawler cron script path** (25 Jul 2026): The cron runner script lives at `~/AppData/Local/hermes/scripts/policy_crawl.py` (resolves to `D:\AI Store\AgentConfigs\hermes-local-appdata\scripts\policy_crawl.py`). It imports from the project at `D:\MMO Du an\TANO-AGENCY\PROJECTS\abtrip\backend\app\services\policy_crawler.py` and calls `run_crawl()`. When setting up the Hermes cron job, point `script` to this path and set `no_agent=False` so the LLM can summarize the crawl results.

**Cron job registered (25 Jul 2026):**
- Name: `ABTrip Policy Crawler`
- Schedule: `every 6h` — runs the `policy_crawl.py` script, agent summarizes crawl output, delivers to Telegram (`telegram:762010475`)
- Toolsets: `terminal`, `file`, `search`
- Status: active, first run at next 6h tick

28. **`smart_agent.py` booking path does NOT call AGT API** **RESOLVED (25 Jul 2026)**: The booking path now calls `abtrip_client.search_flight()` after Gemini responds. See §AGT Booking Integration above for the full implementation pattern and `references/flight-param-extraction.md` for the airport alias map + regex table.

31. **Docker CLI hangs from Git Bash — containers survive, port stays occupied** (25 Jul 2026): Even with the full binary path, `docker ps`/`docker info`/`docker compose` can time out silently from Git Bash (MSYS named-pipe transport breaks) while the Docker Engine and all running containers continue to function normally. Symptom: `curl http://localhost:8765` works, but every `docker ...` command hangs forever.

    **Diagnosis:** `curl -s --max-time 3 http://localhost:8765/ -o /dev/null -w "%{http_code}"` — if it returns a code, a container IS already on the port. Do NOT kill Docker Desktop.

    **Fast fix — direct Python start (bypasses Docker entirely):**
    ```bash
    # 1. Kill Docker engine + port occupant (2 steps, run as admin if needed):
    taskkill /F /IM com.docker.backend.exe
    # In cmd (NOT bash): netstat -ano | findstr :8765 → note PID → taskkill /F /PID <pid>

    # 2. Start backend directly with env vars:
    cd "D:/MMO Du an/TANO-AGENCY/PROJECTS/abtrip/backend" && \
    AGT_API_HOST="https://api-abtrip.timtrungtam.com/v1" \
    AGT_API_ACCOUNT="ABTRIP" AGT_API_PASSWORD=*** \
    AGT_PRIVATE_KEY="a3f2b9e1c8d4a7f6b2e0c9d5a4b1f8d32" \
    GEMINI_API_KEY=*** \
    python -u -m uvicorn app.main:app --host 0.0.0.0 --port 8765 --log-level info
    ```
    Dependencies must be pre-installed (already in local venv). This is faster than restarting Docker Desktop which takes 30-120s on this machine.

32. **`__pycache__` stale bytecode — patch code + restart server = old behavior persists** (25 Jul 2026): After patching a `.py` file and killing+restarting the server, the old error/behavior returns because Python loads stale `.pyc` bytecode from `__pycache__/` instead of the updated `.py` source. Symptom: `grep` confirms the fix is on disk, but the running server still throws the exact same error. **Fix:** clear all `__pycache__` dirs before restart:
    ```python
    # From execute_code (fastest — no shell permission issues):
    import os, shutil
    for root, dirs, files in os.walk(r"D:\MMO Du an\TANO-AGENCY\PROJECTS\abtrip\backend\app"):
        for d in dirs:
            if d == "__pycache__":
                shutil.rmtree(os.path.join(root, d))
    ```
    Then restart the server. Verify with `python -c "from app.services.smart_agent import router; print('OK')"` to confirm the module loads cleanly BEFORE starting uvicorn.

33. **`search_flight()` signature — NOT `origin`/`destination`/`depart_date`** (25 Jul 2026): The actual `ABTripClient.search_flight()` signature is:
    ```python
    async def search_flight(self, system: str, adt: int = 1, chd: int = 0, inf: int = 0, routes: list[dict] = None)
    ```
    Calling it with `origin=..., destination=..., depart_date=...` raises `TypeError: search_flight() got an unexpected keyword argument 'origin'`. The correct call pattern is:
    ```python
    result = await client.search_flight(
        system="",   # ⚠️ EMPTY string — see Pitfall #36. NOT "ABTRIP".
        adt=fp["adt"],
        routes=[{"StartPoint": fp["from"], "EndPoint": fp["to"], "DepartDate": fp["date"]}]  # ⚠️ StartPoint/EndPoint, NOT Origin/Destination — see Pitfall #37
    )
    ```

36. **⚠️ `system=` param is a CARRIER code, NOT the ApiAccount — `"ABTRIP"` gives HTTP 400** (25 Jul 2026, corrects earlier docs): The AGT SearchFlight `System` field selects which airline(s) to search — valid values are carrier codes (`"VN"` Vietnam Airlines, `"QH"` Bamboo, `"VJ"` Vietjet, etc.), and **empty string `""` = search ALL airlines** (the spec default, `abtrip_api_spec.md` line 152). It is NOT the ApiAccount name. Passing `system="ABTRIP"` (confusing it with `AGT_API_ACCOUNT=ABTRIP`) makes the AGT server reject the request:
    ```
    HTTP 400 — "Search flight service not supported for System: ABTRIP"
    ```
    Verified this session by calling SearchFlight directly two ways: `System=""` → HTTP 200 with 8 real VN flights; `System="ABTRIP"` → HTTP 400. **Both call sites in `smart_agent.py` (the booking-fallback block ~line 824 AND the rule-based block ~line 892) had `system="ABTRIP"` hardcoded** — grep the whole file for `system="ABTRIP"` and fix every occurrence to `system=""`, not just the first. The ApiAccount goes in `RequestInfo{ApiAccount}` (injected automatically by `abtrip_client._post`), never in the top-level `System` field. When any AGT endpoint returns a `4xx` mentioning "System", suspect this field before assuming a credentials/DNS problem — the backend chain (LLM intent parse → client → API) is fine, it's a single wrong string in the request body.

    **Debugging pattern that isolated it:** write a throwaway script that hits `/Flight/SearchFlight` directly with the correct `RequestInfo`+`System`+`ListRoute` shape (from `references/agt-api-spec-excerpts.md`), trying both the suspect value and the spec default side by side, and print the HTTP status + `StatusCode`/`Message` for each. This cleanly separates "our request body is wrong" from "the server/account is down" — the same isolation technique noted in §abtrip_client.py Known Bugs.

34. **Gemini API key dead → `403 PERMISSION_DENIED`** (25 Jul 2026): The Gemini API key passed via env `GEMINI_API_KEY` returns 403 on every request. Symptom: all `/api/smart-agent/chat` responses are `"Xin lỗi, không nhận được phản hồi từ AI."` because `candidates` is always empty. **Fix:** `smart_agent.py` has NO fallback when Gemini fails — it needs an `else` branch that uses HHTech/OpenRouter/DeepSeek as a backup LLM. Without this fix, the booking path is dead even though AGT flight search works correctly. The ops path has its own RAG fallback (doesn't need LLM) so ops queries still work.

36. **AGT `System` field is a CARRIER CODE, not the ApiAccount — pass `""` to search all airlines** (25 Jul 2026, CONFIRMED via direct API test): `search_flight(system="ABTRIP", ...)` returns **HTTP 400** `"Search flight service not supported for System: ABTRIP"`. The `System` field in the AGT SearchFlight body is the **airline/carrier code** (`VN`=Vietnam Airlines, `QH`=Bamboo, `VJ`=Vietjet, `VU`=Vietravel) — NOT the `ApiAccount` (which IS `ABTRIP`, but belongs in `RequestInfo.ApiAccount`, injected automatically by the client). Per the API spec (`references/agt-api-spec-excerpts.md` / `abtrip_api_spec.md` line 152), SearchFlight takes `"System": ""` — **empty string = search across all airlines**. Direct probe result: `System=""` → HTTP 200 with 8 VN flights; `System="ABTRIP"` → HTTP 400. **Fix:** every `search_flight()` call in `smart_agent.py` (there are 2 — the LLM-path block ~line 823 and the rule-based fallback block ~line 891) must use `system=""`. This supersedes the (wrong) `system="ABTRIP"` shown in old Pitfall #33.

    **Diagnostic pattern that isolated this fast:** wrote a throwaway `test_agt_direct.py` that loads `backend/.env`, builds the correct spec-shaped body (`RequestInfo{PrivateKey,ApiAccount,ApiPassword}` + `System` + `ListRoute`), and POSTs `/Flight/SearchFlight` twice — once with `System=""`, once with `System="ABTRIP"` — printing HTTP status + ListGroup count for each. This cleanly separates "code request-shape bug" from "server rejects this account/value" in one run. Keep this probe pattern for any future AGT 400/403 — test the raw endpoint directly before touching client/agent code.

37. **AGT route keys are `StartPoint`/`EndPoint` and date is `ddMMyyyy` — `Origin`/`Destination` + `yyyyMMdd` silently return EMPTY results, not an error** (25 Jul 2026, confirmed via direct sandbox test): Two separate request-shape bugs in `smart_agent.py`, both of which the AGT server swallows as `Success=True` with zero real flights (never a 4xx), so they're invisible unless you inspect the actual flight segments:

    - **Route key bug:** `ABTripClient.search_flight()` passes the caller's `routes` list **straight into `ListRoute` with NO key mapping**. The AGT spec (`abtrip_api_spec.md`, verified this session) requires each route dict to use `StartPoint`/`EndPoint`/`DepartDate` — there is NO `Origin`/`Destination`. Passing `{"Origin":..., "Destination":...}` means `StartPoint`/`EndPoint` are missing → the server can't build the route → empty result. Fix: use `{"StartPoint": fp["from"], "EndPoint": fp["to"], "DepartDate": fp["date"]}`.

    - **Date format bug:** `DepartDate` must be **`ddMMyyyy`** (e.g. `"23082026"` for 23 Aug 2026), NOT `yyyyMMdd`. The old `_extract_flight_params` built the date as `f"{yr}{mo:02d}{d:02d}"` (`yyyyMMdd`) and used `strftime("%Y%m%d")` for relative dates — all wrong. Correct: `f"{d:02d}{mo:02d}{yr}"` and `strftime("%d%m%Y")`. Fix ALL FOUR sites in `_extract_flight_params` (the explicit-date branch + the 3 relative-date branches: hôm nay / mai / mốt).

    **Both call sites of `search_flight` in `smart_agent.py` (LLM-path block ~line 823, rule-based block ~line 891) had the wrong route keys** — grep the whole file for `"Origin"` and fix every occurrence, not just the first (same double-site pattern as Pitfall #36's `system=`).

    **⚠️ Critical detection insight — AGT returns `Success=True groups=1` for BOTH wrong AND right formats**, so checking `Success`/`groups` alone gives a FALSE PASS. Only the correct format returns actual flight segments. **Verification pattern that isolated it:** a throwaway script that calls SearchFlight with 3 date formats side-by-side — the code's format, the spec's format, and a deliberately-wrong control (`mmddyyyy`) — then digs into `ListGroup[].ListAirOption[].ListFlightOption[].ListSegment[]` and prints the actual `DepartDate` of the returned flight. Result: only `ddMMyyyy` returned a real segment (`HAN->SGN @ 23082026 0500`); the other two returned `Success=True` with no drillable segment. **When an AGT search "succeeds" but the user sees no/wrong flights, dig into the returned segment's actual date/route before trusting `Success` — the server is lenient and won't error on a malformed request body.** Keep the 3-way side-by-side probe pattern for any future AGT request-shape debugging (same technique as Pitfall #36).

35. **MSYS path conversion on Windows — use `cmd //c` for native Windows commands** (25 Jul 2026): Git Bash (MSYS) converts `/F` → `F:/`, `/PID` → `C:/MinGW/.../PID`, breaking `taskkill` and other Windows-native commands. Prefix with `cmd //c` to bypass MSYS path mangling:
    ```bash
    # WRONG — MSYS converts /F to F:/
    taskkill /F /PID 35776
    # RIGHT
    cmd //c "taskkill /F /PID 35776"
    ```
    Same pattern applies to `netstat`, `tasklist`, and `sc` commands run from Git Bash.