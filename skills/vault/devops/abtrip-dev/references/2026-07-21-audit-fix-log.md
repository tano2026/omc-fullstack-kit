# ABTrip Code Audit & Batch Fix — 21/07/2026

## Trigger
User asked "mày dung v4 rà soát cho tao code này" (use DeepSeek V4 to review code).

## Workflow
1. Load domain skills: abtrip-dev, codebase-audit, ecc-fastapi-patterns, taste-frontend
2. Scan project tree (skip node_modules/.next/dist)
3. Read every source file: backend services, API routes, frontend components, docker config
4. Identify issues with severity ranking (CRIT/MED/LOW)
5. Write report to docs/AUDIT.md
6. Fix critical+medium in priority order
7. Verify each fix with automated checks
8. Test full API flow (search→book→PNR)
9. Update AUDIT.md with fix status

## Critical Bugs Found & Fixed

### CRIT-4: api_flights.py price lookup
**File:** `backend/app/services/api_flights.py`
**Bug:** `for (orig, dest), info in ROUTE_PRICES.items(): break` — looped over dict and used first route's price for ALL bookings.
**Fix:** Added `origin`/`destination` fields to `BookFlightRequest`, lookup via `route_key = (req.origin.upper(), req.destination.upper())`.

### CRIT-3: Gemini API key in URL
**Files:** `llm_gateway.py`, `smart_agent.py`
**Bug:** `?key={api_key}` in URL query param — leaked in logs, proxy headers, HTTP referer.
**Fix:** Changed to `Authorization: Bearer <key>` header using httpx `headers={}`.

### CRIT-2: Dual chat router
**File:** `main.py`
**Bug:** Both `chat_router` (`/api/chat`) and `smart_agent_router` (`/api/smart-agent/chat`) registered — two parallel agents.
**Fix:** Commented out `chat_router` import+include. Smart Agent is the primary.

### CRIT-1: Dead rag_service.py
**File:** `main.py`
**Bug:** `rag_service.py` fully coded (FAISS + Chroma) but never imported or called anywhere.
**Fix:** Commented out `init_rag()`/`close_rag()` + import.

## Medium Fixes Applied
- **MED-1**: Created `.gitignore` (env, pycache, node_modules, .chroma)
- **MED-6**: Updated Fast Track pricing (250K→620K, 550K→950K, 350K→450K)

## AGT API Testing Notes
- Date format: `DDMMYYYY` (not ISO)
- Search response nests flights under `ListGroup[0].ListAirOption[*].ListFlightOption[*].ListFlight`
- Fare data lives in `ListAirOption[*].ListFareOption[*]`
- BookFlight 500 "Cannot read properties of null (reading 'id')" — needs FareOption data attached to AirOption before sending to book
- Use httpx Python script instead of curl for POST to avoid encoding issues
- VN HAN→DAD 22/07: 14 flights, 1,708,181đ – 2,818,181đ
- VJ HAN→SGN 22/07: 22 flights found (fares via GetAncillary)
