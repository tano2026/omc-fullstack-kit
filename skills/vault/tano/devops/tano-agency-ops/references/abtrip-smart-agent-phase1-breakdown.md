# ABTrip Smart Agent — Phase 1 Breakdown (July 20, 2026)

> Pattern: decompose a multi-service backend into independent parallel streams via `delegate_task` (3 subagents).
> Port convention: odd/ugly numbers (user chose **6969** for Smart Agent).

## Execution

**3 teams chạy SONG SONG** via `delegate_task(tasks=[...])`:
- Dev 1: 438s — backend core + landing page + DB + chat AI
- Dev 2: 176s — 4 API services (flights/fasttrack/esim/visa)
- Dev 3: 172s — auth + dashboard + API key

**Kết quả:** 11 files mới, 24 routes, compile OK, server live port 6969.

---

## Architecture

```
FastAPI port 6969
├── services/
│   ├── api_flights.py     — 3 routes: search/book/PNR (mock data Phase 1)
│   ├── api_fasttrack.py   — 3 routes: packages/orders (FT 250K, VIP 550K, Lounge 350K)
│   ├── api_esim.py        — 3 routes: packages/orders (8 gói 79K-499K)
│   ├── api_visa.py        — 4 routes: countries/requirements/consultations (7 nước)
│   ├── auth_service.py    — 4 routes: register/login/api-key/profile (JWT + passlib)
│   ├── llm_gateway.py     — 31KB: parse_intent + chat_response + extract_flight_info
│   └── smart_agent.py     — Core: multi-tenant, billing, commission (có sẵn từ trước)
├── middleware/
│   └── auth_middleware.py — JWT Bearer + X-API-Key composite auth
├── models/
│   └── smart_agent.py     — 6 tables: Tenant, FlightBooking, FastTrackOrder, EsimOrder, VisaConsultation, Payment
├── templates/
│   ├── main.html          — Landing page: hero + 4 service cards + pricing (37KB, dark gold)
│   ├── dashboard.html     — CTV dashboard: overview + orders + API keys + Chart.js
│   └── base.html          — Jinja2 base: sidebar/bottom-nav responsive
└── agents/
    └── __init__.py        — Package init
```

## 24 Routes Summary

| Prefix | Endpoints | Status |
|--------|-----------|--------|
| `/main` | Landing page HTML | ✅ |
| `/api/v1/flights` | `GET /search`, `POST /book`, `GET /pnr/{ref}` | ✅ |
| `/api/v1/fasttrack` | `GET /packages`, `POST /orders`, `GET /orders` | ✅ |
| `/api/v1/esim` | `GET /packages`, `POST /orders`, `GET /orders` | ✅ |
| `/api/v1/visa` | `GET /supported-countries`, `GET /requirements/{c}`, `POST /consultations`, `GET /consultations` | ✅ |
| `/api/v1/auth` | `POST /register`, `POST /login`, `POST /api-key`, `GET /profile` | ✅ |
| `/api/smart-agent` | 10 routes (từ trước): register, tenants, upgrade, ft, esim, payment | ✅ |

## Server Test Results

- `GET /api/health` → `{"status":"ok"}`
- `GET /api/v1/flights/search?origin=HAN&destination=SGN&depart_date=25072026` → 5 flights (1.1M-1.6M)
- `GET /api/v1/fasttrack/packages` → 3 gói (250K-550K)
- `GET /api/v1/esim/packages` → 8 gói (79K-499K)
- `GET /api/v1/visa/supported-countries` → 7 nước
- `GET /api/smart-agent/dashboard/stats` → 0 tenants (DB trống)

## Bug Todo
- `POST /api/v1/flights/book`: `tenant_id` field is `int` model but should be `str` for T001-style IDs. Fix: change BaseModel field type.

## Tech Stack
- **Python global** (Hermes venv uvicorn fails with module import errors) — `python -m uvicorn app.main:app`
- **DB:** file-based SQLite (`smart_agent.db`)
- **Auth:** JWT (python-jose, HS256, 24h) + API key fallback
- **Password:** passlib[bcrypt]
- **Phase 1:** Mock data in-memory — không DB lưu cho API services

## Parallel Dispatch Pattern

```python
# Pattern cho phân rã phase development
tasks = [
    {
        "goal": "Dev 1 — Backend Core: ...",
        "context": "Chi tiết...",
        "toolsets": ["terminal", "file"]
    },
    {
        "goal": "Dev 2 — API Layer: ...",
        "context": "...",
        "toolsets": ["terminal", "file"]
    },
    {
        "goal": "Dev 3 — CTV Platform: ...",
        "context": "...",
        "toolsets": ["terminal", "file"]
    }
]
results = delegate_task(tasks=tasks)
# Mỗi subagent độc lập, terminal riêng, context riêng
# Kết quả return về cùng lúc — verify compile OK sau đó
```
