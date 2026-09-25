# Backend main.py Architecture (updated 20/07/2026)

## Overview

Monolithic `backend/main.py` (~530 lines) — single file containing:
1. Database models (SQLAlchemy: Order, Product)
2. API endpoints (12 routes)
3. Momo payment integration (inline)
4. VNPay payment integration (inline)
5. Paint Point Engine integration (via tuvi_mcp_client.py)
6. Seed data (39 products)
7. HTML pages (order-success, order-failed)

## Key Design Decisions

### Why monolithic, not split?
- No router/module overhead needed at this scale
- All payment config in one place (test keys)
- Easier to copy to VPS as a single file
- 39 products seed inline, no separate seeds.py

### Database
- SQLite (`tuvi.db`), auto-created
- 2 tables: `orders`, `products`
- `Product` auto-seeded on first GET /api/products call

### Payment Integration
```python
MOMO_ENDPOINT = "https://test-payment.momo.vn/v2/gateway/api/create"
MOMO_PARTNER_CODE = "MOMO"
MOMO_ACCESS_KEY = "F8BBA842ECF85"
MOMO_SECRET_KEY = "K951..."  # sandbox

VNPAY_ENDPOINT = "https://sandbox.vnpayment.vn/paymentv2/vpcpay.html"
VNPAY_TMN_CODE = "TEST_TMN"
VNPAY_HASH_SECRET = "TEST..."
```

## MCP Integration (updated 20/07/2026)

**OLD approach (failed):** `_call_mcp_chart()` tried to spawn a Python subprocess to import from a non-existent `mcp_tuvi` module — fell back to generic gender-based fallback.

**NEW approach (working):** `_call_mcp_chart()` calls `engine.tuvi_mcp_client.TuviMCPClient` which connects to the Node.js MCP server via JSON-RPC stdin/stdout. See `references/mcp-integration-pattern.md` for protocol details.

```python
def _call_mcp_chart(year, month, day, hour, gender):
    from engine.tuvi_mcp_client import TuviMCPClient, chart_to_engine_format
    client = TuviMCPClient()
    chart = client.calculate_chart(year, month, day, hour, gender)
    return chart_to_engine_format(chart)
```

## Verified Endpoints

| Method | Path | Status | Notes |
|--------|------|--------|-------|
| GET | /api/health | ✅ | `{"status":"ok","time":"..."}` |
| GET | / | ✅ | Landing page HTML |
| POST | /api/demo | ⚠️ | Falls back to generic if MCP unavailable |
| GET | /api/products | ✅ | 39 products JSON |
| POST | /api/order/create | ✅ | Returns order_id + payment_url |
| GET | /api/order/{id} | ✅ | Order status |

## Common Errors & Fixes

- **`unhashable type: 'dict'`** — Jinja2 + StaticFiles conflict. Fix: serve HTML as plain text via `open().read()` + `HTMLResponse()`.
- **`Template not found`** — Use absolute path for Jinja2 loader, or skip Jinja2 entirely for landing page.
- **Port 8139 already in use** — Kill old process: `process(action='kill', session_id=...)`.
- **MCP return `None`** — Check MCP server is running (`hermes mcp list`), or server may have crashed (auto-restart not implemented).
