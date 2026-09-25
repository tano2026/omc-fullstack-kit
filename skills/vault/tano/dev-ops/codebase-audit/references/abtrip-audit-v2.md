# ABTrip Smart Agent — Audit V2 (21/07/2026)

**Project:** `D:\MMO Du an\TANO-AGENCY\PROJECTS\abtrip`  
**Stack:** FastAPI (backend) + Next.js (frontend) + Docker Compose  
**Mode:** Audit-only (report delivered, fixes pending user go-ahead)

## Architecture at a Glance

```
abtrip/
├── backend/
│   └── app/
│       ├── main.py              ← Entrypoint, includes ALL routers
│       ├── services/
│       │   ├── smart_agent.py   ← NEW: router /api/v1/smart — FULL agent (chat, booking, esim, dashboard)
│       │   ├── chat.py          ← OLD: router /api/chat — legacy agent (1500+ lines)
│       │   ├── api_flights.py   ← Mock: /api/v1/flights — in-memory
│       │   ├── api_fasttrack.py ← Mock: /api/v1/fasttrack — in-memory
│       │   ├── api_esim.py      ← Mock: /api/v1/esim — in-memory
│       │   ├── api_visa.py      ← Mock: /api/v1/visa — in-memory
│       │   ├── rag_service.py   ← DEAD: FAISS+embeddings, never imported
│       │   ├── llm_gateway.py   ← Built but unused by smart_agent.py
│       │   ├── session_service.py
│       │   ├── config.py
│       │   └── abtrip_client.py
│       └── api/
│           └── bookings.py      ← REAL: wraps AGT API (search, book, issue, retrieve)
├── frontend/ (Next.js)
│   ├── app/layout.tsx
│   ├── app/page.tsx
│   ├── components/chat/ChatInterface.tsx
│   └── lib/api.ts
└── docker-compose.local.yml
```

## Critical Findings (🔴)

| # | Issue | File | Detail |
|---|-------|------|--------|
| 1 | **Dual agent conflict** | `main.py` + `chat.py` + `smart_agent.py` | 2 routers active: `/api/chat` (old) and `/api/v1/smart/chat` (new). User gets different bot depending on endpoint. |
| 2 | **API key in URL query param** | `smart_agent.py:716` | `?key={gemini_key}` in URL instead of `Authorization: Bearer`. Leaked via logs, proxy, referer. |
| 3 | **Mock price lookup wrong** | `api_flights.py:310-314` | `for ... in ROUTE_PRICES: break` — grabs HAN-SGN for every booking regardless of actual route. |
| 4 | **Dead RAG module** | `rag_service.py` | 300+ lines, FAISS + embeddings, but zero imports anywhere. |

## Medium Findings (🟡)

| # | Issue | File | Detail |
|---|-------|------|--------|
| 5 | Missing `.gitignore` | root | No `.gitignore` — .env can leak on public push |
| 6 | In-memory chat history | `smart_agent.py` | `_chat_sessions: Dict[str, list]` — lost on restart |
| 7 | Missing env vars in Settings | `config.py` | GEMINI_API_KEY, OPENROUTER_API_KEY used via raw `os.getenv` |
| 8 | No Pydantic validation | `bookings.py` | `dict[str, Any]` instead of BaseModel |
| 9 | Fast Track price below cost | `api_fasttrack.py` | FT Basic=250K < actual cost 350-400K |

## Low Findings (🟢)

| # | Issue | Detail |
|---|-------|--------|
| 10 | No health check endpoint | Add `GET /health` |
| 11 | Docker no internal network | All services exposed to host |
| 12 | Frontend no error state | ChatInterface: spinner on failure forever |
| 13 | session_service.py over-engineered | ~300 lines for simple async sessionmaker |

## Key Detection Patterns Used

1. **Dual router**: Check `main.py` for ALL `app.include_router()` calls — count how many chat agents exist
2. **Direct API key**: Grep for `?key={`, `api_key=`, `apikey=` in URL strings
3. **Mock price lookup**: Check if dict iteration uses `break` on first entry instead of `dict.get(key)`
4. **Dead module**: Grep for import of each services/*.py in the rest of the codebase
5. **In-memory state**: Search for `_store: Dict`, `_sessions: Dict`, module-level mutable collections
