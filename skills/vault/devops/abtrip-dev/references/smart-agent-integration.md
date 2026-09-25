# Smart Agent — Phòng Vé AI Multi-Tenant

## Overview

Smart Agent is a "bán cần câu" layer on top of ABTrip — allows CTVs (subagents) to sell flights, Fast Track, eSIM under their own brand. 3 tiers: Free → Pro (199K/mo) → White-label (1.5tr/mo).

## Files

| File | Purpose |
|------|---------|
| `backend/app/services/smart_agent.py` | All models, routes, pricing (20KB) |
| `backend/app/templates/smart_agent_landing.html` | Landing page (20KB) |
| `backend/app/main.py` | Line 20 imports router, line 120 includes it, line 133 `/` serves landing |

## Database

SQLite at `backend/data/smart_agent.db` — 5 tables:
- `sa_tenants` — CTV accounts (tier, api_key, commission_rate, booking_limit)
- `sa_subscriptions` — payment history
- `sa_fasttrack_orders` — Fast Track / VIP Lounge orders
- `sa_esim_orders` — eSIM orders
- `sa_payments` — transaction log

Created async on first startup via `@router.on_event("startup")` + `Base.metadata.create_all`.

## API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| POST | `/api/smart-agent/register` | Register CTV (auto API key) |
| GET | `/api/smart-agent/tenant/{id}` | CTV info |
| GET | `/api/smart-agent/tenants` | List CTVs (filter by status/tier) |
| POST | `/api/smart-agent/upgrade` | Upgrade Pro/White-label |
| POST | `/api/smart-agent/fasttrack` | Create Fast Track order |
| GET | `/api/smart-agent/fasttrack/orders` | List FT orders (filter by tenant_id/status) |
| GET | `/api/smart-agent/esim/packages` | 8 eSIM packages |
| POST | `/api/smart-agent/esim` | Create eSIM order |
| GET | `/api/smart-agent/dashboard/stats` | Admin stats |
| POST | `/api/smart-agent/payment/callback` | Payment webhook stub |

## Pricing

| Service | Unit Price | Notes |
|---------|-----------|-------|
| Fast Track | 450K/pax | Night surcharge +200K (23:00-06:00) |
| VIP Lounge | 650K/pax | |
| eSIM Asia | 99K-179K | 7/15 days |
| eSIM Japan | 149K-249K | 7/15 days |
| eSIM Korea | 129K | 7 days |
| eSIM Europe | 199K | 7 days |
| eSIM USA | 179K | 7 days |
| eSIM Global | 499K | 30 days |

## Tiers

| Tier | Price | Commission | Booking Limit |
|------|-------|-----------|---------------|
| Free (CTV Cơ bản) | 0 | 8% | 50/mo |
| Pro (Đại Lý Pro) | 199K/mo | 12% | 300/mo |
| White-label | 1.5tr/mo | 15% | Unlimited |

## Adding a new service module (pattern)

1. Create `backend/app/services/<name>.py` with APIRouter + models
2. Import in `main.py`: `from app.services.<name> import router as <name>_router`
3. Include: `app.include_router(<name>_router)`
4. Create landing page in `templates/`
5. Route `/` serves landing via `HTMLResponse` (no Jinja2 due to Python 3.14 compatibility bug)
