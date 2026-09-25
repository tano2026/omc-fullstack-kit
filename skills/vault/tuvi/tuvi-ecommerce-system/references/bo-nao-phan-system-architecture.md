# Bộ Não Phán → Tử Vi — System Architecture & Session Notes

> Build date: 2026-07-20
> Project path: D:\MMO Du an\Tử Vi\
> Brand renamed from "Bộ Não Phán" to "Tử Vi" (Jul 2026)
> Server: running on port 8139

## Complete File Inventory

### Engine (52KB Python)
- `engine/paint_point_engine.py` — 20 rules, 6 psych theories, pure Python
- `engine/test_chart.json` — Real chart for Nguyễn Ngọc Tân (1984/5/1, 9h, male)
- `engine/test_engine.py` — 24/24 test cases passing

### Backend (FastAPI + SQLite, port 8139)
All endpoints verified working:
- `GET /health` → OK (status/version)
- `GET /` → Landing page (58KB, HTTP 200)
- `POST /api/order/create` → Both Momo + VNPay payment URLs generated
- `POST /api/order/create-demo` → Returns 7-item demo with chart_summary + pain points + CTA
- `GET /api/order/status/{id}` → Order status check
- `POST /api/order/momo-ipn` → Momo callback (signature verified)
- `GET /api/order/vnpay-ipn` → VNPay callback (signature verified)

### Files
- `backend/main.py` — App entry, CORS, static mount, error handler
- `backend/config.py` — Momo/VNPay keys from env (sandbox defaults)
- `backend/database.py` — SQLAlchemy: Order (name, birth, product, status, payment_method, payment_id), Product (name, price, category), PaymentTransaction
- `backend/seeds.py` — 39 products → DB (auto-skip if already seeded)
- `backend/requirements.txt` — fastapi, uvicorn, sqlalchemy, weasyprint, httpx, pydantic, python-multipart, aiofiles
- `backend/orders.db` — SQLite database (39 products seeded)
- `backend/api/orders.py` — 5 endpoints: create, create-demo, momo-ipn, vnpay-ipn, status
- `backend/api/payment_momo.py` — MomoPayment class (HMAC SHA256, sandbox)
- `backend/api/payment_vnpay.py` — VNPayPayment class (HMAC SHA512, sandbox)
- `backend/api/tuvi_client.py` — Mock chart (MCP not available in FastAPI context)
- `backend/api/pdf_generator.py` — weasyprint PDF from HTML template (text fallback)
- `backend/api/pdf_templates/report.html` — Dark academia PDF template

### Frontend
- `frontend/templates/index.html` — Landing page (1075 lines, light theme, gold accent, mobile-first)
- `frontend/static/` — Empty dir for future assets

## Issues Log

### 1. GET / returns "unhashable type: 'dict'"
**Root cause:** Jinja2 template cache conflict when `StaticFiles` is mounted before serving `.html` via `TemplateResponse`. The static file mount catches the `index.html` first and returns a dict representation instead of passing through to the template engine.
**Current fix:** main.py now reads index.html as plain text and returns `HTMLResponse(content)` — no Jinja2 template dependency.

### 2. UnicodeEncodeError in logging on Windows
**Error:** `'charmap' codec can't encode character '\u0111'`
**Root cause:** Windows cp1252 can't encode Vietnamese characters
**Fix:** Set `PYTHONIOENCODING=utf-8` or configure StreamHandler with `encoding='utf-8'`

### 3. MCP tools not available in FastAPI
MCP Tử Vi tools (`mcp_tuvi_calculate_chart`, etc.) are only accessible inside Hermes agent context, not from a standalone FastAPI server.
**Dev workaround:** `api/tuvi_client.py` with mock chart data
**Production path:** Build a Hermes-to-FastAPI bridge (HTTP call to Hermes API endpoint that runs the MCP tool)

### 4. read_file fails on paths with Vietnamese characters
read_file() tool errors on paths like `D:\MMO Du an\Tử Vi\...`.
**Fix:** Always use `cat` via terminal for files under paths containing diacritics.

### 5. PowerShell commands via bash terminal corrupt with path injection
When running PowerShell commands through git-bash terminal, any path with spaces/special chars in the CWD gets injected into the PowerShell command string causing parse errors.
**Fix:** Use POSIX alternatives: `df -h /c/` for disk space, not Get-PSDrive.

### 6. Landing page still shows "Bộ Não Phán" branding
User renamed project to "Tử Vi" but index.html still has old brand name in logo, title, and footer. Awaiting user decision on final brand name before updating.

## Competitor Research Summary (5 sites)

| Site | Model | Price Range | Key Differentiator |
|------|-------|-------------|-------------------|
| AItuvi.com | Nạp xu | 109K→1,399K | App + Affiliate 30% |
| Luangiai.vn | PDF | 289K→789K | Form miễn phí → CV, funnel tốt |
| Tuvinhuanphap.top | PDF+Coaching | 199K→5.8tr | Claim "không AI", thủ công |
| Tuvilogy | Map cá nhân | Unknown | Style conversational |
| Tuviglobal | Free→Premium | Unknown | Membership model |

**Bộ Não Phán USP:** Multi-lens (Tử Vi + Kinh Dịch + Tâm lý học + Game Theory + Định luật) — đối thủ ko có. Auto 100% → giá rẻ hơn. Recurring MRR + Affiliate + API B2B.
