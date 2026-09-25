---
name: abtrip-flight-search
category: aviation-ticketing
description: >-
  Tra cứu giá vé và đặt chỗ máy bay nội địa từ abtrip.vn.
  BA HỆ THỐNG - abtrip_browser.py (Playwright) cho KH thật,
  API B2B test cho backend dev, Browser tool/MCP cho DOM inspection.
---

# abtrip-flight-search

Tra cứu giá vé và đặt chỗ máy bay nội địa từ [abtrip.vn](https://abtrip.vn/).

## 🆕 V2 Architecture — AI Agent Platform (June 2026 — STABLE)

### 🆕 V3 — Smart Agent Phase 1 (July 20, 2026 — BUILT)

**User preference: use DeepSeek V4 or R1 for all reasoning-heavy and code work** on the ticketing bot (intent parser, chat flow, testing). These models handle Vietnamese slang, dialect, and complex logic better than smaller models for this task class. Do NOT default to Gemini 2.5 Flash for this project unless DeepSeek endpoints are unreachable.

**ABTrip được mở rộng thành Smart Agent (brand: Travel Tech Hybrid) với 5 dịch vụ + 3-tier CTV platform trên port 6969.**

```diff
+ ┌─── FASTAPI PORT 6969 ──────────────────────────┐
+ │  24 routes mới, 11 modules                      │
+ │                                                  │
+ │  🛍️ Landing page /main (37KB, dark gold)        │
+ │  💬 Chat AI Engine (31KB, intent parser)         │
+ │  🔐 Auth: JWT + API key middleware               │
+ │  📊 Dashboard CTV (mobile-first, Chart.js)       │
+ │                                                  │
+ │  ┌─ API Layer ───────────────────────────────┐  │
+ │  │ /api/v1/flights/search|book|pnr            │  │
+ │  │ /api/v1/fasttrack/packages|orders          │  │
+ │  │ /api/v1/esim/packages|orders               │  │
+ │  │ /api/v1/visa/requirements|consultations    │  │
+ │  └────────────────────────────────────────────┘  │
+ │                                                   │
+ │  ┌─ CTV Platform ────────────────────────────┐  │
+ │  │ /api/v1/auth/register|login|api-key|profile│  │
+ │  │ /main (landing) + /dashboard CTV            │  │
+ │  └────────────────────────────────────────────┘  │
+ └──────────────────────────────────────────────────┘
```

**3 gói:** CTV Cơ bản (free) → Đại Lý Pro (199K/tháng) → White-label (1.5tr/tháng)
**5 dịch vụ:** ✈️ Vé máy bay (AGT) | 🛂 Fast Track Nội Bài | 📱 eSIM (8 gói) | 🛂 Visa (7 nước) | 💬 Chat AI tư vấn

**🖥️ VPS deploy & test:** Xem [references/vps-deploy-and-test-guide.md](references/vps-deploy-and-test-guide.md) — quy trình deploy từ Windows lên Ubuntu VPS, pitfalls (externally-managed Python, debug path leak, port conflict), test suite thiết kế.

## 🆕 V2 Architecture — AI Agent Platform (June 2026 — STABLE)

**ABTrip đã chuyển đổi từ form-based booking → LLM/NLP chat interface với 3 Agent và landing page bán hàng 5 dịch vụ mở rộng:**

```
┌──────────────────────────────────────────┐
│  Landing Page Bán Hàng 5 Dịch Vụ         │
│  ✈️ Vé máy bay | 🛂 Fast Track | 🛂 Visa │
│  📱 eSIM | 🆔 Hộ chiếu (tư vấn)          │
│  + Chat AI tư vấn (1 chat cho 5 dịch vụ) │
└────────────────┬─────────────────────────┘
                 │ POST /api/chat {message, agent, session}
                 ▼
┌──────────────────────────────────────────┐
│  LLM Gateway (OmniRoute DeepSeek V4)     │
│  Intent Parser → Tool Router              │
└──┬──────────┬──────────┬──────────┬───────┘
   │          │          │          │
   ▼          ▼          ▼          ▼
┌──────┐ ┌──────┐ ┌──────┐ ┌──────────┐
│AGT   │ │Fast  │ │eSIM  │ │Visa (tư  │
│API   │ │Track │ │API   │ │vấn, thủ  │
│B2B   │ │(tay) │ │(IST1)│ │công)     │
└──────┘ └──────┘ └──────┘ └──────────┘
```

**Thay đổi chính (July 2026):**
              - ❌ **BỎ**: Form-based search/booking (SearchForm cũ)
              - ✅ **THÊM**: Chat interface — tất cả tương tác bằng ngôn ngữ tự nhiên
              - ✅ **THÊM**: 3 tab Agent — Ticketing | SIM (thay Tour) | Visa
              - ✅ **THÊM**: White-label — CTV có brand riêng, cấu hình phí riêng
              - ✅ **THÊM**: LLM Engine — Gemini 2.5 Flash + OmniRoute parse intent
              - ✅ **PWA**: Mobile-first, install được trên điện thoại

              **Backend (FastAPI, giữ nguyên + mở rộng):**
              - Giữ nguyên: AGT API client, models, booking routes
              - ✅ **ĐÃ THÊM**: `api/chat.py` — POST /api/chat (LLM chat endpoint)
              - ✅ **ĐÃ THÊM**: `services/llm_gateway.py` — Gemini 2.5 Flash + OpenAI fallback
              - ✅ **ĐÃ THÊM**: `services/aviation_db.py` — 20 airport codes, 5 airlines, alias lookup
              - ⏳ Chưa: `admin.py` (CTV management)

              **Frontend (Next.js 14, giữ layout + thay nội dung):**
              - Giữ nguyên: Layout, routing
              - ✅ **ĐÃ THAY**: `page.tsx` → ChatInterface (không còn SearchForm)
              - ✅ **ĐÃ THÊM**: `components/chat/` (ChatInterface, ChatMessage, ChatInput)
              - ⏳ Chưa: FlightResultCard component, booking flow trong chat

              **LLM Gateway chi tiết:**
              - Model: Gemini 2.5 Flash (primary) → OpenAI-compatible (fallback: 9Router/OmniRoute)
              - System prompt: aviation expert với airport DB + airline policy knowledge
              - Tool call: LLM trả JSON `{"tool": "search_flight", "args": {...}}` → backend gọi AGT API → LLM format lại kết quả
              - Intent parser built-in: hiểu tiếng Việt tự nhiên, địa danh (SG=SGN, HN=HAN), ngày tương đối (ngày mai, ngày kia, cuối tuần)
              - Xem [references/llm-gateway-system-prompt.md](references/llm-gateway-system-prompt.md) cho full system prompt
              - **Chat endpoint (V3)**: POST `/api/chat` với confirm-before-search flow, 24/24 slang tests passed (Jul 2026). Xem [references/chat-api-intent-parser-v3.md](references/chat-api-intent-parser-v3.md)
              - **Pitfalls** (Jul 2026): policy intent bi hijack boi flight search path (#9 — FIXED: policy_responses dict), reverse_location hien ten Anh thay vi Viet (#10 — FIXED: _AIRPORT_VIET dict), sg dict removal gay crash 11 tests (#11 — FIXED: same-code dedup), DeepSeek preferred over Gemini (#12 — set model pref), English date July 20 regex fails (#17 — FIXED: full month pattern + [:3] extract), test session contamination (#18 — FIXED: fresh UUID per test), partial parse for single-location queries (#19 — FIXED: return partial dict even with 1 location), awaiting_confirm reparse lost context (#20 — FIXED: merge all pending_data fields, not just date), VPS deploy: externally-managed Python + debug path leak 500 + no rsync (#21 — FIXED: venv + remove C: path + tar+scp), nginx reverse proxy for browser access (#22 — FIXED: nginx config + static chat HTML), flight results code-block format user disliked (#23 — FIXED: structured JSON + frontend card rendering pattern in references/smart-agent-backend-architecture.md). Chi tiet trong `references/chat-api-intent-parser-v3.md` va `references/vps-deploy-and-test-guide.md` va `references/smart-agent-backend-architecture.md`.

              **SIM Agent data:** eSIM supplier IST1 API tại `references/sim-api-ist1-reference.md` (DOCX: `D:\MMO Du an\AI Agent Future\SIM API_IST1_2026.docx`)

**Chi tiết plan:** Xem `references/ai-agent-platform-plan-2026-06-30.md`
              **Phase 1 (Chat Ticketing Bot):** ✅ IMPLEMENTED — commit `d14abb1`

---

## ⚠️ BA HỆ THỐNG

| Hệ thống | Mục đích | Cách dùng |
|----------|----------|-----------|
| **abtrip_browser.py (Playwright)** | Tra cứu + đặt vé THẬT cho KH **<-- Ưu tiên** | `import abtrip_browser; search_flights("UIH","SGN","29062026")` hoặc CLI `python scripts/abtrip_browser_cli.py search --start=UIH --end=SGN --date=29062026` |
| **API B2B** (`abtrip.timtrungtam.com`) | Chuẩn bị backend, dev/test | Script Python (stdlib) `scripts/abtrip_search.py`, nhanh 2-3s, dùng chung 3 agent |
| **Browser tool / MCP** | Research/DOM inspection | Dùng browser tool khi cần inspect DOM hoặc debug |

> ⚠️ **Rule quan trọng**: API B2B là **hệ test** — KHÔNG dùng thông tin từ API B2B để trả lời giá vé / đặt vé cho khách hàng thật.
> Luôn dùng **abtrip_browser.py** cho thông tin thật và giao dịch thật.
>
> 🆕 **Cập nhật (June 2026)**: API B2B trả `Availability` (số ghế trống thật) và `TotalFare` — dùng để **canh chỗ background**. Khi API báo đạt điều kiện, gọi `abtrip_browser.book_flight()` 1 lần duy nhất để book thật. Xem section "Seat & Price Monitoring" bên dưới.

## ⚠️ Anti-bot Detection

**abtrip.vn detect Playwright headless** — khi chạy abtrip_browser.py hoặc browser tool trực tiếp, có thể gặp lỗi "Đã có lỗi xảy ra". Giải pháp:

1. Dùng **bypass URL** với query params: `https://abtrip.vn/flight?adults=1&tripType=one-way&segments[0][startPoint]=HAN&segments[0][endPoint]=DAD&segments[0][departDate]=20062026` — chỉ hoạt động trong Playwright code, không phải live browser.
2. API B2B **không bị anti-bot** — lý do nên dùng API B2B cho canh chỗ, Playwright chỉ cho booking.

## ✅ Current State (20/06/2026) — BOOK FLOW FIXED

`book_flight` đã được rewrite hoàn chỉnh với DOM structure của abtrip.vn (Next.js + Ant Design). **Đã test thành công SGN→PQC VN1829.**

DOM structure chi tiết, code mẫu selectors, form fields (name attributes), và Playwright evaluate pitfalls:  
Xem [references/abtrip-booking-dom-june2026.md](references/abtrip-booking-dom-june2026.md)

### Changes made (patch_abtrip2.py on VPS):
1. **Removed `_try_flight_select`** — thay bằng inline `page.evaluate(js, flight_number)` correct approach
2. **Selectors đúng:** `div.air-item` + `span:has-text("Chọn")` — không dùng `querySelectorAll('button')`
3. **Form fill dùng `input[name]`** — `passengers.adults.0.firstName`, `.lastName`, `.dob`, `contact.name`, `.phone`, `.email`
4. **Gender chọn qua label click** — `label:has(input[name="passengers.adults.0.gender"])`
5. **Submit:** `<BUTTON>` với text "Đặt vé" — `button:has(span:text("Đặt vé"))`
6. **Không dùng f-string escape** — tất cả JS evaluate dùng `(fn) => ...` pattern

**Verified DOM structure (VPS, SGN→PQC 15/07/2026):**
```
DIV.air-options
  DIV.air-item
    DIV.flight-present
      DIV.flight-sum
        DIV.airline-logo → SPAN.flight-num (chứa "VN1829")
        DIV.flight-action-select → DIV.action-button → SPAN "Chọn"
```

### Form Fill — Correct Approach
```python
# First name
el = await page.query_selector('input[name="passengers.adults.0.firstName"]')
if el: await el.fill(first_name)

# Gender — CLICK LABEL, không click input radio trực tiếp
glabels = await page.query_selector_all('label:has(input[name="passengers.adults.0.gender"])')
for gl in glabels:
    t = (await gl.inner_text()).strip().lower()
    if t == gender_wanted:
        await gl.click()
        break

# DOB — format dd/mm/yyyy
el = await page.query_selector('input[name="passengers.adults.0.dob"]')
if el: await el.fill("01/01/1990")

# Submit button
submit = await page.query_selector('button:has(span:text("Đặt vé"))')
```

### ⚠️ VPS path khác Windows path
- **VPS:** `/opt/hermes/ticketing-agent/backend/abtrip_browser.py`
- **Local:** `D:\AI Store\Hermes Agent\abtrip_browser.py`
- Các lần patch VPS dùng `scp` từ local lên VPS, không sync tự động
- Xem [references/vps-abtrip-browser-deployment.md](references/vps-abtrip-browser-deployment.md)

## ⚠️ flight_value pipe-separated payload (CRITICAL)

When `ai_agent.py` receives a book_flight request, the LLM passes `flight_value` from the tool — which is the **full pipe-separated string** like `VN1833|SGN|PQC|20/06/2026 18:30|20/06/2026 19:30|Vietnam Airlines|1728000`, NOT just the flight number.

**AI Agent handler must parse:**
```python
flight_number = args.get("flight_value", "").split("|")[0].strip()
```

**Without this fix**, `book_flight()` receives the entire pipe-separated payload as the flight number, causing: `"Không tìm thấy chuyến bay VN1833|SGN|PQC|... trên trang kết quả để đặt."`

**Verified fix applied** (VPS, June 2026): `sed -i` replaced `args.get("flight_value", "")` with `args.get("flight_value", "").split("|")[0].strip()` in ai_agent.py.

## Book Flow — DOM Structure Reference

**Xem [references/abtrip-vn-dom-structure-june2026.md](references/abtrip-vn-dom-structure-june2026.md)** cho DOM structure chi tiết (Next.js + Ant Design), selectors chính xác, form field names.

DOM structure verified (June 2026):
- "Chọn" button là `<SPAN>` bên trong `<DIV.action-button>`, KHÔNG phải `<button>`
- querySelectorAll('button') trả về 0 trên trang kết quả
- Form fields dùng `input[name]` với `passengers.adults.0.firstName/lastName/dob` và `contact.name/phone/email`
- Submit button là `<BUTTON>` với text "Đặt vé" (thực sự là `<BUTTON>`, không phải `<SPAN>`)

## Booking Flow — ĐÃ TEST THÀNH CÔNG (June 2026)

Flow đặt vé thật trên abtrip.vn đã test thành công route **SGN→HAN, VJ120, 15/06/2026**:

| Bước | Kết quả |
|------|---------|
| Search | ✅ Bypass URL → 55 chuyến bay |
| Chọn chuyến | ✅ Click `.flight-action-select` đúng VJ120 |
| Form load | ✅ Input `passengers.adults.0.firstName` visible |
| Fill form | ✅ Họ/tên/giới tính/DOB + contact |
| Submit | ✅ Click "Đặt vé" → redirect /payment |
| **PNR** | **✅ PYVEP8** |
| **Order** | **✅ #ABT00349** |
| **Time Limit** | **✅ 02:58 12/06/2026** |

## Quy trình Web abtrip.vn (Playwright/Browser — cho KH thật)

### Bước 1: Mở form search

```python
page.goto("https://abtrip.vn/")
# Trang chủ có sẵn form tìm kiếm Ant Design
```

### Bước 2: Chọn loại vé (nếu cần)

```python
# Click "Một chiều" (e19)
page.locator('[ref="e19"]').click()
# Verify: ngày về textbox (e55) sẽ disabled
```

### Bước 3: Chọn sân bay đi

```python
# Click textbox Khởi hành từ (e52)
page.locator('[ref="e52"]').click()
# Dropdown mở ra, snapshot thấy e66-e88
# Mỗi ref mapping với IATA code:
# e66=BMV, e67=CAH, e68=CXR, e69=DAD, e70=DIN,
# e71=DLI, e72=HAN, e73=HPH, e74=HUI, e75=NHA,
# e76=PQC, e77=PXU, e78=SGN, e79=TBB, e80=THD,
# e81=UIH, e82=VCA, e83=VCL, e84=VCS, e85=VDO,
# e86=VDH, e87=VII, e88=VKG
page.locator('[ref="e72"]').click()  # HAN
```

### Bước 4: Chọn sân bay đến

```python
# Click textbox "Nơi đến" (e53) để mở dropdown
page.locator('[ref="e53"]').click()
# Chọn từ dropdown e66-e88
page.locator('[ref="e69"]').click()  # DAD
```

### Bước 5: Chọn ngày đi

```python
# Click textbox "Ngày đi" (e54) → calendar popup
page.locator('[ref="e54"]').click()
# Click vào cell ngày trong DatePicker
```

### Bước 6: Click Tìm kiếm (e24)

```python
page.locator('[ref="e24"]').click()
# Chờ load trang kết quả
```

### Cấu trúc refs form search

```
e9  → container radio "Một chiều" + "Khứ hồi"
  e19 → radio "Một chiều"
  e20 → dropdown "1 người lớn"
e21 → container điểm đi
  e47 → wrapper clickable
    e52 → textbox "Khởi hành từ"
e22 → button đổi chỗ (icon swap)
e23 → container điểm đến
  e48 → wrapper clickable
    e53 → textbox "Nơi đến"
  e49 → dropdown container (Ant Design)
    e61-e65 → tabs (Việt Nam, Châu Á...)
    e66-e88 → options (23 airport)
e50 → container ngày tháng
  e54 → textbox "Ngày đi" (DatePicker)
  e55 → textbox "Ngày về" (disabled khi Một chiều)
e24 → button "Tìm kiếm"
```

| Trả lời KH về giá vé | **abtrip_browser.py** (Playwright) | Giá API B2B không chính xác |
| Test/dev backend | **API B2B** (script Python) | Mục đích của hệ test |
| Chuyển NV xuất vé | **abtrip_browser.py** (Playwright) | Phải có booking code thật |

## 🧩 OpenClaw / Gateway Integration

Thằng Claw chạy qua gateway, không thể `import abtrip_browser` trực tiếp được như Hermes. Có **3 cách** để nó dùng:

### 🏎️ Performance Note: Hermes search nhanh hơn OpenClaw

Hermes gọi `abtrip_browser.py` native Python (1 process), OpenClaw qua MCP gateway (3 layers). Benchmark: Hermes ~3-5s, Claw ~15-30s.

**Flow chuẩn:**
1. 🔹 **Hermes** — search nhanh (abtrip_browser.py native)
2. Thông báo kết quả Telegram-style (pseudo-table header + data rows)
3. 🔸 **OpenClaw** — book khi đã chốt (qua MCP abtrip-flight)

Xem [references/team-bot-workflow.md](references/team-bot-workflow.md).

### Cách 1: MCP Server (recommended) ⭐

File: `D:\AI Store\Hermes Agent\mcp-abtrip-server.py`

MCP server stdio transport, expose 2 tool:
- `search_flights(start_point, end_point, depart_date)`
- `book_flight(start_point, end_point, depart_date, flight_number, first_name, last_name, gender, dob, phone, email)`

**Cấu hình trong OpenClaw Gateway:**
```yaml
mcpServers:
  abtrip:
    command: python
    args: ["D:\\AI Store\\Hermes Agent\\mcp-abtrip-server.py"]
```

### Cách 2: Script absolute path (fallback)

```bash
python "D:\\AI Store\\Hermes Agent\\scripts\\abtrip_browser_cli.py" search --start=SGN --end=DAD --date=20062026
python "D:\\AI Store\\Hermes Agent\\scripts\\abtrip_browser_cli.py" book --start=SGN --end=HAN --date=15062026 --flight=VJ120
```

### Cách 3: Sync code từ Hermes → OpenClaw MCP

Khi Hermes test book OK với code mới, copy `abtrip_browser.py` + `mcp-abtrip-server.py` sang thư mục MCP server của OpenClaw. Cả 2 file đã wrapper sẵn.

---

## Phân Biệt: "Landing Page Bán Hàng" vs "Dashboard Quản Lý" (CRITICAL)

User có thể yêu cầu "trang bán hàng" hoặc "giao diện website" — cần xác định rõ LOẠI giao diện:

| Loại | Mục đích | UX | Ví dụ |
|------|----------|----|-------|
| 🛍️ **Landing Page Bán Hàng** | Khách hàng + CTV tra cứu & đặt dịch vụ | Hero search + service cards + chat AI + kết quả inline | "trang bán hàng", "landing page", "web cho khách", "trang thương mại điện tử" |
| ⚙️ **Dashboard Quản Lý (OPC)** | Chủ shop/admin quản lý đơn hàng, doanh thu, CTV | Sidebar nav + tables + charts + filters | "OPC", "quản lý đơn", "admin", "dashboard", "trang quản trị" |

**Khi user nói "giao diện của trang bán hàng" → ý là LOẠI 1 (landing page bán hàng).** Không suy luận ra OPC/dashboard.

**Khi user nói "xây dashboard cho CTV" → ý là LOẠI 2** — dashboard riêng.

## Không dùng khi:

- Cần tra cứu quốc tế → abtrip chỉ hỗ trợ domestic
- API B2B sandbox — cấm dùng cho KH thật, giá là test data
- Cần tra Amadeus GDS → dùng ticketing-manager skill

## Prerequisites

- Python 3.10+
- **abtrip_browser.py** (hệ thật): cần Playwright (`pip install playwright` + `playwright install chromium`)
- **API B2B** (hệ test): chỉ cần stdlib

## File paths

| File | Path (dùng cho cả 3 agent) |
|------|---------------------------|
| abtrip_browser.py (Playwright—hệ THẬT) | `D:\AI Store\Hermes Agent\abtrip_browser.py` |
| CLI wrapper (Playwright—hệ THẬT) | `D:\AI Store\Hermes Agent\scripts\abtrip_browser_cli.py` |
| API B2B (hệ test) | `D:\AI Store\Hermes Agent\scripts\abtrip_search.py` |

## Usage — abtrip_browser.py (Playwright — hệ THẬT cho KH)

### Cú pháp CLI

```bash
python scripts/abtrip_browser_cli.py search --start=UIH --end=SGN --date=29062026
python scripts/abtrip_browser_cli.py book --start=HAN --end=TBB --date=20082026 --flight=VN7651
```

> ⚠️ **CLI book dùng hardcoded passenger info**: `NGUYEN NGOC TAN` (Nam, DOB 20/10/1990, phone 0788320320, email info@abtrip.vn).
> 🚫 `--first-name/--last-name/--gender/--dob/--phone/--email` **KHÔNG tồn tại** trong CLI parser — chỉ có `--start/--end/--date/--flight`.
> ✅ Muốn book với passenger khác → dùng Python import (`book_flight()` function) — xem section bên dưới.

### Cú pháp Python (import)

```python
import sys; sys.path.append(r"D:\AI Store\Hermes Agent")
import abtrip_browser
import asyncio
res = asyncio.run(abtrip_browser.search_flights("UIH", "SGN", "29062026"))
print(res)
```

### Booking

```python
import sys; sys.path.append(r"D:\\AI Store\\Hermes Agent")
import abtrip_browser, asyncio

# 1 khách
passengers = [{"first_name": "NGUYEN", "last_name": "NGOC TAN", "gender": "Nam", "dob": "20/10/1990"}]
contact = {"name": "NGUYEN NGOC TAN", "phone": "0788320320", "email": "info@abtrip.vn"}
res = asyncio.run(abtrip_browser.book_flight("UIH", "SGN", "29062026", "VN1397", passengers, contact))

# ✅ Trả về: {"success": True, "pnr": "PYVEP8", "order_id": "#ABT00349", "time_limit": "02:58 12/06/2026"}
```

### Book CLI (thông tin hardcoded — chỉ dùng cho NGUYEN NGOC TAN)

```bash
python scripts/abtrip_browser_cli.py book --start=SGN --end=HAN --date=15062026 --flight=VJ120
python scripts/abtrip_browser_cli.py book --start=HAN --end=TBB --date=20082026 --flight=VN7651
```

> ⚠️ **CLI book KHÔNG nhận params passenger** — hardcoded info: Tân, Nam, DOB 20/10/1990, phone 0788320320, email info@abtrip.vn.
> ✅ Muốn book cho người khác → dùng Python API `book_flight()`.

## Usage — API B2B (hệ test — backend dev)

### Cú pháp

```bash
python scripts/abtrip_search.py --start=HAN --end=DAD --date=30/06/2026 [--compact|--table|--markdown|--simple|--json]
```

### Options

| Flag | Mặc định | Mô tả |
|------|----------|-------|
| `--start` | HAN | Mã sân bay đi (3 ký tự) |
| `--end` | PQC | Mã sân bay đến |
| `--date` | hôm nay | Định dạng DD/MM/YYYY |
| `--compact` | — | **Telegram ưu tiên** — bullet groups theo hãng |
| `--simple` | — | Minimal: Số hiệu + Ngày + Nơi + Giờ (bỏ giá, TG bay) |
| `--markdown` | — | Bảng Markdown trong code block |
| `--table` | — | Bảng ASCII |
| `--json` | default | JSON đầy đủ — cho xử lý tiếp |
| `--timeout` | 0 | **Bị ignore** — API tự timeout 15s server-side |

### ⛔ IMPORTANT: Telegram output format — CHUẨN DUY NHẤT

Telegram KHÔNG có table syntax. Dùng format dưới đây — **KHÔNG BAO GIỜ** dùng pipe tables hay ASCII box.

**Format chuẩn cho search kết quả nhiều chuyến:**

━━━━━━━━━━━━━━━━
**{Đi} → {Đến} | {ngày/tháng}**

🟢 **{Hãng}**
　{chuyến} · {giờ}→{giờ} · **{giá}k**
　{chuyến} · {giờ}→{giờ} · {giá}k

🔴 **{Hãng}**
　{chuyến} · {giờ}→{giờ} · {giá}k

💡 **Rẻ:** {chuyến} — {giá}k
━━━━━━━━━━━━━━━━

**Luật:**
- Dòng đầu: `**{Đi} → {Đến} | {ngày/tháng}**` — route + ngày rút gọn (2 số, ko năm)
- Tên hãng: viết ngắn (Bamboo, Vietjet, VNA) — ko ghi "Airways/Airlines"
- Emoji: 🟢 Bamboo, 🔴 Vietjet, 🔵 VNA, 🟠 Pacific, 🟡 Vietravel
- Mỗi chuyến 1 dòng: `　{chuyến} · {giờ}→{giờ} · **{giá}k**`
  - Dùng `·` (middle dot) separator
  - Giá viết kiểu rút gọn: `1.732k`, `2.056k` — ko ghi `₫` hay `VND`
  - **Bold** giá rẻ nhất route
  - Dùng `+1` nếu qua ngày hôm sau
- Sort trong mỗi hãng: theo giá tăng dần
- Sort hãng: Bamboo → Vietjet → VNA → Pacific → Vietravel
- Cuối: `💡 **Rẻ:** {chuyến} — {giá}k`
- Dùng `━━━━━━━━━━━━━━━━` line đầu + cuối

**Format cho 1 chuyến (xác nhận booking) — Style Ticket Card:**

━━━━━━━━━━
╔══════════════════════════╗
║ ✈️ **ABTRIP**            ║
║ **ĐẶT VÉ THÀNH CÔNG**   ║
║                          ║
║  {Đi} **→** {Đến}       ║
║  {giờ}→{giờ}             ║
║  **{ngày/tháng}**        ║
║                          ║
║  {Hãng} — **{chuyến}**   ║
║                          ║
║  **{PNR}**               ║
║  **{giá}₫**              ║
║                          ║
║  ⏳ {status}             ║
╚══════════════════════════╝
━━━━━━━━━━

**Quy tắc confirm:**
- Tên hãng viết ngắn: Bamboo, Vietjet, VNA, Vietravel
- `{Hãng} — **{chuyến}**` (tên thường, số hiệu bold)
- Giá dùng `₫` — format `.` cho nghìn: `1.754.000₫`
- Ngày/tháng 2 số: `15/06`
- PNR bold
- Nếu có hành lý: thêm `🧳 {baggage}`
- Nếu có link check-in: thêm `Check in [tại đây]({url})`

### Output examples

**--compact** (Telegram ưu tiên):
```text
🔵 Vietnam Airlines (1h20m)
  06:05→07:25 · 1,593,000₫
  07:50→09:10 · 1,593,000₫

🟡 Vietjet Air (1h35m)
  06:00→07:35 · 1,166,000₫
  17:35→19:05 · 1,166,000₫

→ Rẻ nhất: 1,166,000₫
```

**--simple** (Minimal):
```text
📋 **HAN → DAD** | **30/06/2026** | 14 chuyến

• VN171 · 30/06/2026 · HAN→DAD · 06:05→07:25
• VJ396 · 30/06/2026 · HAN→DAD · 15:35→17:05

📌 14 chuyến · HAN→DAD · 30/06/2026
```

**--table**:
```text
─── HAN → DAD | 30/06/2026 | 14 chuyến bay ───
Hãng                    Chuyến  Giờ đi   Giờ đến   TG bay   Giá từ
Vietnam Airlines        VN171   06:05→   07:25     1 giờ 20p  1,593,000₫
Vietjet Air             VJ396   15:35→   17:05     1 giờ 30p  1,166,000₫
```

## Cấu trúc response API B2B

API trả về JSON:
```
{
  "Success": true,
  "ListGroup": [{
    "ListAirOption": [{
      "Airline": "VJ",
      "ListFareOption": [{"OptionId": 0, "TotalFare": 990000, "Availability": 9, "Unavailable": false, ...}],
      "ListFlightOption": [{
        "OptionId": 0,
        "ListFlight": [{
          "FlightNumber": "VJ123",
          "Operator": "VJ",
          "DepartDate": "30062026 0935",
          "ArriveDate": "30062026 1135",
          "Duration": 120,
          "StopNum": 0
        }]
      }]
    }]
  }]
}
```

**Key fields**:\n- `Operator` — hãng thực tế khai thác (quan trọng: code-share flights)\n- `TotalFare` — giá vé theo OptionId\n- `Availability` — **⚠️ SỐ GHẾ TRỐNG (int, thật)**. Giá trị: `0` = hết chỗ, `1-4` = còn ít (nguy cơ hết), `>=5` = còn nhiều. **Đã verify giá trị thật** — không hardcoded, có thể là 4,5,6,8,9 tuỳ fare.\n- `Unavailable` — boolean, `true` = hết chỗ hẳn\n- `Duration` — phút (int)\n- `DepartDate`/`ArriveDate` — format `DDMMYYYY HHMM`\n- `FareFamily` — tên hạng vé VN: "Phổ thông tiết kiệm", "Phổ thông linh hoạt",...\n\n**⚠️ PITFALL: `Price` và `Currency` không nằm ở ListFlight — chỉ ở ListAirOption**\n\n`Price`/`Currency` chỉ ở **`ListAirOption`** level, KHÔNG có ở `ListFlight` bên trong:\n```\nListGroup[]\n  → ListAirOption[i]          ← Price, Currency tại đây\n    → ListFlightOption[j]\n      → ListFlight[k]         ← KHÔNG có Price!\n```\nKhi format, lấy `Price` từ `air_option` và gán cho từng flight trong `ListFlight`:\n```python\nfor air_option in group.get(\"ListAirOption\", []):\n    price = float(air_option.get(\"Price\", 0) or 0)\n    for fo in air_option.get(\"ListFlightOption\", []):\n        for fl in fo.get(\"ListFlight\", []):\n            parsed.append({**fl, \"price\": price})\n```\n**Đã verify** với endpoint `https://api-abtrip.timtrungtam.com/v1` (PrivateKey=a3f2b9e1c8d4..., ApiAccount=ABTRIP, ApiPassword=CtTXgjVX8AQ1): SGN→HAN → JSON trả về 52 ListAirOption, Price từ 650k-2.8M.\n\n**⚠️ Hệ test chỉ chấp nhận ngày hiện tại (current date):** sandbox trả HTTP 500 nếu `DepartDate` không phải hôm nay. Dùng `datetime.now().strftime(\"%d%m%Y\")` khi test.\n---

## 🔄 Seat & Price Monitoring — Cơ chế canh chỗ

API B2B (`scripts/abtrip_search.py`) trả về 2 trường quan trọng cho canh chỗ:
- **`Availability`** — số ghế trống (int). Giá trị thật, không hardcoded: có thể là 0-9. 0 = hết chỗ, 1-4 = còn ít, >=5 = còn nhiều.
- **`Unavailable`** — boolean, `true` = hết chỗ hẳn (khi Availability = 0 AND Unavailable = True)
- **`TotalFare`** — giá hiện tại

> ✅ API B2B trả Availability thật đã được verify: các fare có Avail=4,5,6,8,9 khác nhau. Không phải hardcoded.
> ⚠️ `Availability` hiện tại KHÔNG được parse/trả về bởi `abtrip_search.py` — cần patch nếu dùng monitoring.
>
> ⚠️ **API B2B payload format BẮT BUỘC đúng**: `{System, Adt, Chd, Inf, ListRoute: [{Leg, StartPoint, EndPoint, DepartDate}], RequestInfo: {PrivateKey, ApiAccount, ApiPassword}}`. Format phẳng `{StartPoint, EndPoint, DepartureDate, Account, Password}` gây 400 Bad Request.

### Hai tình huống canh chỗ

| # | Tình huống | Trigger | Hành động |
|---|-----------|---------|-----------|
| 1 | 🔴 **Hết chỗ** | `Availability` = 0 | Poll API mỗi ~10p, khi `Availability` > 0 → auto-book qua `abtrip_browser.book_flight()` |
| 2 | 💰 **Giá cao** | `TotalFare` > ngưỡng user | Poll API mỗi ~10p, khi `TotalFare` ≤ ngưỡng → **đặt mới song song**, không hủy vé cũ trước |

### ⚠️ RULE QUAN TRỌNG: Đặt song song, KHÔNG hủy trước (user preference)

Khi canh giá xuống (tình huống 2):
- **Luôn đặt vé mới TRƯỚC**, không hủy vé cũ
- Chỉ khi nào vé mới đã đặt thành công (có PNR), mới thông báo user
- User tự quyết định hủy vé cũ sau
- Lý do: nếu hủy trước mà không đặt được vé mới → mất chỗ hoàn toàn

### ⚠️ `monitor_type` là field BẮT BUỘC

Khi tạo watcher qua API `/api/watcher/create`, payload **phải** có `monitor_type`:
- `"availability"` — canh chỗ trống (trigger khi Availability > 0)
- `"price"` — canh giá (trigger khi TotalFare ≤ max_price)

Nếu thiếu `monitor_type`, API trả về lỗi `"Thiếu trường bắt buộc: monitor_type"`.

Các field optional: `min_availability` (default null), `max_price` (default null), `interval` (default 10 phút).

### Kiến trúc: 2 bộ riêng biệt — API Watcher + Scraper

```\n┌──────────────────────────────────────┐\n│   BỘ 1: API WATCHER (`watcher_api/`)   │ ← Chạy background mỗi 10p (tối thiểu 5p)\n│   - api_checker.py + checker_manager.py │
│   - Gọi API B2B, nhanh 2-3s           │
│   - Check Availability + Fare          │
│   - Khi đạt → trigger Scraper          │
└──────────────┬───────────────────────┘
               ▼
┌──────────────────────────────────────┐
│   BỘ 2: SCRAPER (`watcher_scraper/`)  │ ← Chạy 1 lần duy nhất
│   (scraper_booker.py → Playwright)     │
│   - Mất 30-60s (khởi động browser)     │
│   - Book vé thật trên abtrip.vn       │
│   - Báo kết quả Telegram + link       │
│   - Note: vé cũ chưa hủy              │
└──────────────────────────────────────┘

> ⚠️ **Không trộn lẫn**: API Watcher check với API B2B, Scraper chỉ book với Playwright. Playwright KHÔNG dùng để poll. Poll interval phải ≥ 5 phút (mặc định 10p) — hãng phạt nếu check quá dày.
```

### Flow chi tiết

```
User nhập:
  - Chuyến: VJ120 HAN→SGN 30/06
  - Hành khách: Nguyễn Văn A, Nam, 20/10/1990, 0984190918, a@email.com
  - Ngưỡng: giá ≤ 1.5tr (hoặc auto nếu canh chỗ)
  - Mode: availability | price
  - Interval: 10 phút (mặc định)

→ Lưu watcher queue (JSON file, watchers/ dir)
→ Mỗi 10p (hoặc interval tuỳ watcher): API B2B check
  → Nếu đạt điều kiện:
    → Gọi scraper_booker.book() với passenger info đã lưu
    → Đặt thành công? Gửi Telegram: "Đã đặt vé mới! Vé cũ chưa hủy. Link: ..."
    → Xóa watcher khỏi queue
  → Chưa đạt? Bỏ qua, chờ lần sau
```

### ⚠️ Lưu ý kỹ thuật

1. **API B2B vs Playwright**: API B2B search nhanh (2-3s) — dùng để check định kỳ. Booking THẬT vẫn qua Playwright (`scraper_booker.book()`). **Không dùng Playwright để poll.**
2. **API B2B không bị anti-bot** — không giống abtrip.vn (Playwright headless bị detect "Đã có lỗi xảy ra").
3. **Polling interval — ⚠️ tối thiểu 5 phút**: Hãng bay phạt nếu check quá dày. Mặc định 10p, configurable per watcher (field `interval_minutes`). Không bao giờ < 5 phút.
4. **Booking timeout**: Playwright booking có thể mất 30-60s + form fill. Background worker không bị ràng buộc bởi HTTP request timeout.
5. **Không hủy vé cũ trước khi đặt mới** — luôn đặt song song.
6. **API payload format** — dùng `{System, Adt, Chd, Inf, ListRoute, RequestInfo}`. Format phẳng `{StartPoint, EndPoint, Account, Password}` gây 400 Bad Request.

### Cấu trúc watcher queue (JSON)

```json
{
  "id": "watcher_vj120_3006",
  "mode": "price",  // "availability" cho TH hết chỗ
  
  "flight": {
    "from": "HAN", "to": "SGN",
    "date": "2026-06-30",
    "flight_code": "VJ120",
    "departure_time": "06:30",
    "arrival_time": "08:30"
  },
  
  "threshold": {
    "max_price": 1500000,
    "min_availability": 1
  },
  
  "passenger": {
    "name": "Nguyễn Văn A",
    "gender": "male",
    "dob": "20/10/1990",
    "phone": "0984190918",
    "email": "a@example.com"
  },
  
  "notify_telegram": true,
  "created_at": "2026-06-12T11:01:00",
  "existing_booking": null
}
```

### File paths

- Watcher API checker: `D:\\AI Store\\Hermes Agent\\flight-booking-webapp\\watcher_api\\api_checker.py`
- Watcher manager: `D:\\AI Store\\Hermes Agent\\flight-booking-webapp\\watcher_api\\checker_manager.py`
- Scraper booker (Playwright): `D:\\AI Store\\Hermes Agent\\flight-booking-webapp\\watcher_scraper\\scraper_booker.py`
- Scraper manager: `D:\\AI Store\\Hermes Agent\\flight-booking-webapp\\watcher_scraper\\scraper_manager.py`
- Watcher queue files: `D:\\AI Store\\Hermes Agent\\flight-booking-webapp\\watchers\\*.json`
- Script search API B2B: `D:\\AI Store\\Hermes Agent\\scripts\\abtrip_search.py`
- Script book thật (Playwright): `D:\\AI Store\\Hermes Agent\\abtrip_browser.py`
- Web app (Flask): `D:\\AI Store\\Hermes Agent\\app.py` + `templates/index.html`

### Verified API Routes (Flask web app, port 5000)

All routes verified working on `http://192.168.1.253:5000`:

| Route | Method | Purpose | Verified |
|-------|--------|---------|----------|
| `/api/status` | GET | Server health check | ✅ 200 |
| `/api/search` | POST | Search flights via API B2B | ✅ |
| `/api/book` | POST | Book via Playwright scraper | ✅ |
| `/api/watcher/list` | GET | List all watchers | ✅ 200 |
| `/api/watcher/create` | POST | Create watcher (requires `monitor_type`) | ✅ |
| `/api/watcher/get/<id>` | GET | Get watcher details | ✅ |
| `/api/watcher/delete/<id>` | POST | Delete watcher | ✅ |
| `/api/watcher/check-now/<id>` | POST | Force check single watcher | ✅ 200 |
| `/api/watcher/check-flights` | POST | Check all active watchers | ✅ |
| `/api/watcher/worker/start` | POST | Start background scheduler | ✅ |
| `/api/watcher/worker/stop` | POST | Stop background scheduler | ✅ |
| `/api/trigger/book` | POST | Trigger booking via scraper | ✅ |
| `/api/trigger/logs` | GET | Get trigger history | ✅ |

**Watcher create payload** (required fields):
```json
{
  "from": "HAN", "to": "SGN", "date": "12062026",
  "monitor_type": "availability" | "price",
  "min_availability": 1,
  "max_price": 1500000,
  "interval": 10
}
```

---

## Sắp xếp

Theo mã hãng → theo giờ khởi hành.

## Các mã sân bay hỗ trợ — 23 sân bay dân dụng

**Miền Bắc (7):** HAN (Hà Nội/Nội Bài), HPH (Hải Phòng/Cát Bi), VDO (Vân Đồn/Quảng Ninh), VII (Vinh/Nghệ An), THD (Thọ Xuân/Thanh Hóa), DIN (Điện Biên Phủ)

**Miền Trung (10):** DAD (Đà Nẵng), HUI (Huế/Phú Bài), CXR (Cam Ranh/Nha Trang), NHA (Nha Trang), UIH (Quy Nhơn/Phù Cát), TBB (Tuy Hòa/Phú Yên), VCL (Chu Lai/Quảng Nam), PXU (Pleiku/Gia Lai), BMV (Buôn Ma Thuột/Đắk Lắk), VDH (Đồng Hới/Quảng Bình)

**Miền Nam (6):** SGN (Tân Sơn Nhất/TP.HCM), PQC (Phú Quốc/Kiên Giang), VCA (Cần Thơ), DLI (Đà Lạt/Liên Khương), VCS (Côn Đảo), VKG (Rạch Giá/Kiên Giang)

> ⚠️ **DLI (Đà Lạt/Liên Khương)** — đóng cửa 4/3/2026 → 1/9/2026 nâng cấp đường băng (nguồn: Báo Chính phủ, VTV, VnExpress, Dân trí, Thanh niên)

## CLOSED_AIRPORTS guard

Script tự động kiểm tra và từ chối search nếu route có điểm đi/đến là DLI:
```
⚠️  Sân bay Liên Khương (Đà Lạt) tạm đóng cửa từ 4/3/2026 → 1/9/2026...
   Route: DLI → HAN không khả dụng.
   Gợi ý: bay từ sân bay gần nhất (SGN, DAD) hoặc đi xe/limousine.
```

## Default Booking Fields (khi user yêu cầu đặt vé)

| Field | Giá trị mặc định |
|-------|-----------------|
| Email | info@abtrip.vn |
| Phone | 0788320320 |
| DOB | 20/10/1990 |

## Cách gọi từ các agent

**Hermes Agent** (terminal trực tiếp):
```bash
# Hệ thật (Playwright)
python scripts/abtrip_browser_cli.py search --start=UIH --end=SGN --date=29062026

# Hệ test (API B2B)
python scripts/abtrip_search.py --start=HAN --end=DAD --date=30/06/2026 --compact
```

**OpenClaw / Goose** (dùng absolute path):
```bash
# Hệ thật
python "D:\AI Store\Hermes Agent\scripts\abtrip_browser_cli.py" search --start=SGN --end=PQC --date=23/06/2026
# Hệ test
python "D:\AI Store\Hermes Agent\scripts\abtrip_search.py" --start=SGN --end=PQC --date=23/06/2026 --table
```

## Booking Flow (đã test thành công — June 2026)

Flow: `search → select flight → fill form → submit → confirm`

### Code mẫu đặt vé

```python
import sys; sys.path.append(r"D:\AI Store\Hermes Agent")
from abtrip_browser import book_flight
import asyncio

passengers = [
    {"first_name": "NGUYEN", "last_name": "NGOC TAN", "gender": "Nam", "dob": "20/10/1990"}
]
contact = {"name": "NGUYEN NGOC TAN", "phone": "0788320320", "email": "info@abtrip.vn"}

result = asyncio.run(book_flight("SGN", "HAN", "15062026", "VJ120", passengers, contact))
# result = {"success": True, "pnr": "PYVEP8", "order_id": "#ABT00349", "time_limit": "02:58 12/06/2026"}
```

### Thứ tự các bước trong code

1. **Search** → bypass URL với query params
2. **Chọn chuyến bay** — tìm `.flight-action-select` có chứa flight number
3. **Fill form** — `passengers.adults.0.*` + `contact.*`
4. **Click "Đặt vé"** — nút `.ant-btn` text "Đặt vé"
5. **Parse PNR** — từ URL `/payment?code=...` và text trên trang

### Pitfall: `page.evaluate` chỉ nhận 1 arg

Playwright `page.evaluate(expression, arg)` chỉ chấp nhận **1 arg duy nhất** type `Any`. Để truyền ElementHandle + string, dùng destructuring:

```python
# ✅ ĐÚNG
text = await page.evaluate(
    "(args) => { const [el, fn] = args; return el.textContent; }",
    [element_handle, flight_number]
)

# ❌ SAI — error "arguments is not defined"
text = await page.evaluate(
    "(element, fn) => ...", element_handle, flight_number
)
```

Xem thêm `references/booking-flow-dom.md` cho DOM structure chi tiết.

### ⚠️ `page.evaluate` + f-string escaping trap

Khi dùng `page.evaluate(f"""...""", arg)`, **KHÔNG** nhúng biến vào f-string với `\"` — kết quả là SyntaxError JS. Dùng plain string + arg riêng:

```python
# ✅ ĐÚNG
js = "(fn) => { return document.querySelectorAll(fn); }"
await page.evaluate(js, flight_number)

# ❌ SAI — gây "Unexpected token '('"
await page.evaluate(f"""..."""{{fn}}\"""")
```

Xem [references/playwright-evaluate-pitfall.md](references/playwright-evaluate-pitfall.md) cho phân tích chi tiết + demo các lỗi thường gặp.

## Pitfalls & quirks

### API B2B (hệ test)

### Playwright DOM Debug Methodology

Khi book_flight thất bại và cần debug DOM structure của abtrip.vn, xem [references/playwright-dom-debug-methodology.md](references/playwright-dom-debug-methodology.md). Bao gồm 5-phase debug flow, hierarchy tracing, và key pitfalls từ các session debug thực tế (June 2026).

1. **`DEFAULT_AIRLINE` missing causes compact format crash** — `format_compact()` dùng `AIRLINE_COLORS.get(g["code"], DEFAULT_AIRLINE)`. Nếu hằng số `DEFAULT_AIRLINE` không được định nghĩa (VD sau khi edit script hoặc thêm hãng mới mà quên), lỗi `NameError: name 'DEFAULT_AIRLINE' is not defined` xảy ra khi dùng `--compact`. Fix: thêm `DEFAULT_AIRLINE = "⬜"` gần `AIRLINE_COLORS` dict.

2. **API không kiểm tra route tồn tại** — một số cặp sân bay không có đường bay nội địa trực tiếp (VD SGN→VCA) API vẫn trả empty list. Đây là behavior đúng — script báo "Không tìm thấy chuyến bay".

3. **DLI đóng cửa** — script báo trước khi search. KHÔNG dùng dữ liệu từ API cho route liên quan đến DLI.

4. **Không timeout config cần** — API tự timeout ~15s server-side. Flag `--timeout` giữ lại cho backward compatibility nhưng bị ignore.

5. **Code-share flights** — `Operator` field quan trọng hơn `Airline`. VD chuyến VN số hiệu nhưng do BL khai thác.

6. **Duration là phút (int)** — script tự parse thành "X giờ Yp". Fallback regex nếu là string.

7. **Next-day detection** — dựa vào giờ đến < giờ đi (cross-midnight). Đánh dấu "+1".

8. **Cả 3 agent dùng chung script** — sync script ở `D:\\AI Store\\Hermes Agent\\scripts\\abtrip_search.py` (workspace).

9. **Credentials trong script** — PrivateKey, ApiAccount, ApiPassword hardcoded. KHÔNG commit lên public repo.

10. **Một số sân bay không bay đêm** — DIN (Điện Biên), VCS (Côn Đảo), VKG (Rạch Giá). Không có chuyến sau 18h.

### abtrip_browser.py (Playwright — hệ THẬT cho KH)

10. **Bypass URL** — dùng query params `https://abtrip.vn/flight?adults=1&tripType=one-way&segments[0][startPoint]=HAN&segments[0][endPoint]=DAD&segments[0][departDate]=20062026` — bỏ qua trang chủ, tiết kiệm token. **Chỉ hoạt động trong Playwright headless** (abtrip_browser.py). Live browser tool bị cắt params và redirect về homepage.
11. **Timeout** — route có ít chuyến (UIH→SGN) load nhanh 15-20s, route đông (HAN→DAD 45 chuyến) có thể 30-40s. `_wait_for_flights` tự động chờ tối đa 40s.
12. **DOM khác nhau giữa các route** — UIH→SGN dùng layout cũ (walk từ .flight-num lên ancestor), HAN→DAD dùng layout mới (.flight-item card). `_extract_flights` tự động detect và xử lý cả 2.
13. **Tuyệt đối không dùng tên thử nghiệm** — khi book vé, bắt buộc tên thật. Hãng phạt ADM nếu phát hiện tên test.
14. **Chỉ giữ chỗ (Hold)** — code chỉ lấy PNR, KHÔNG tự động thanh toán/xuất vé.
15. **PNR parsing** — regex quét "Mã đặt chỗ" + 6 ký tự alphanumeric. Fallback pattern nếu format khác. **Đã test thành công**: SGN→HAN VJ120 trả về `PYVEP8` + order `#ABT00349` + time limit `02:58 12/06/2026`.
16. **`page.evaluate(expr, arg)` chỉ nhận 1 arg** — Playwright API limitation. Truyền nhiều giá trị qua destructuring: `(args) => { const [el, fn] = args; ... }` với `[element_handle, string_val]` làm arg.
17. **`.flight-action-select`** — mỗi card có 1 nút này. Click đúng chuyến bằng cách evaluate parent DOM tìm flight number match.
18. **Form input names đã verify** — `passengers.adults.0.firstName`, `.lastName`, `.gender` (radio: index 0=Nam, 1=Nữ), `.dob` (dd/mm/yyyy); `contact.name`, `.phone`, `.email`.
19. **Nút "Đặt vé"** — `button:has-text("Đặt vé")`. Có thể cần scroll xuống nếu viewport nhỏ.
20. **Booking form load ~3-5s** sau click "Chọn" — SPA transition + Ant Design form render. Dùng `wait_for_selector('input[name="passengers.adults.0.firstName"]', timeout=20000)`.
21. **Không cần chọn fare** — mặc định fare đầu tiên được chọn tự động khi click "Chọn".
28. **Script chưa hỗ trợ multi-passenger đầy đủ** — code hiện lặp qua `passengers` list vào các input `passengers.adults.0`, `passengers.adults.1`, ... (dùng `{idx}`). Đã verify: 4 passengers được điền đúng trên form, submit thành công.

29. **`flight_value` từ tool AI Agent chứa pipe-separated payload** — VD: `VN1833|SGN|PQC|20/06/2026 18:30|...|1728000`. Khi gọi `book_flight()`, cần parse `flight_value.split("|")[0]` để lấy mã chuyến bay. Đã fix trong ai_agent.py dòng `flight_number=args.get("flight_value", "").split("|")[0].strip()`.

### Vietjet Booking (Form Validation — CRITICAL)

24. **⚠️ MAPPING firstName/lastName NGƯỢC với convention quốc tế!**
   
   Form Vietjet trên abtrip.vn dùng trường:
   - `passengers.adults.0.firstName` = **HỌ** (họ + tên đệm, ví dụ `PHAN THANH`)
   - `passengers.adults.0.lastName` = **TÊN** (chỉ tên riêng, ví dụ `VINH`)

   Đây là mapping ngược với convention quốc tế (nơi firstName=tên, lastName=họ). Luôn xác nhận mapping này trước khi fill form.

25. **Họ (firstName) tối đa 10 ký tự — ĐÃ TEST QUẬT** — Form Vietjet validate `firstName` ≤ 10 ký tự. Nếu họ + tên đệm vượt 10 (VD "PHAN DUC GIA" = 11 ký tự kể cả khoảng trắng), form trả lỗi: `"Họ không được vượt quá 10 ký tự"`.

   **Giải pháp — split lại first/last name:**
   - Nếu họ + đệm > 10 ký tự → chuyển một phần đệm sang `lastName`
   - VD "PHAN DUC GIA HUNG": `first_name="PHAN DUC"` (8 ký tự ✓), `last_name="GIA HUNG"` (8 ký tự ✓)
   - VD "PHAN THANH VINH": `first_name="PHAN THANH"` (10 ký tự ✓), `last_name="VINH"` (4 ký tự ✓)
   - VD "LE THANH HONG": `first_name="LE THANH"` (8 ký tự ✓), `last_name="HONG"` (4 ký tự ✓)
   - Không mất thông tin — hãng ghép `firstName + " " + lastName` khi xuất vé
   - **Luôn trim khoảng trắng** khi đếm ký tự

26. **Tên (lastName) cũng có giới hạn** — chưa test chính xác. Nếu tên dài (VD "NGUYEN NGOC QUOC BAO"), cần kiểm tra và split tương tự. Luôn đọc lỗi validate từ terminal output — hãng trả về tiếng Việt rõ ràng.

27. **Cả 4 hành khách book đồng loạt OK khi split đúng** — Đã test book VJ561 cho 4 người với họ dài thành công trong 1 lần submit. Form Vietjet xử lý multi-passenger tốt khi mỗi trường đều ≤ 10 ký tự.

### Child/Infant trên abtrip.vn

29. **Trẻ em ≥12 tuổi = giá người lớn** — abtrip.vn / Vietjet tính trẻ em (child) là 2-11 tuổi. Trẻ ≥12 tuổi book vé người lớn với DOB thật. Đã test: PHAN DUC GIA HUNG (30/04/2014 → 09/07/2026 = 12 tuổi 2 tháng) book thành công với fare adult 977k và DOB thật.

30. **Không cần tham số child cho trường hợp này** — gọi `book_flight()` với passengers list, tất cả đều là adult (không truyền child field). Hãng tự động xác định tuổi từ DOB.

31. **Script abtrip_browser.py hiện hardcode children=0** (line 209) — nếu cần book trẻ em <12 thực sự, cần sửa code để truyền child thay vì adult passenger.
### CLI booking: KHÔNG có params tùy chỉnh

32. **CLI `book` chưa có params passenger** — `--first-name/--last-name/--gender/--dob/--phone/--email` KHÔNG tồn tại trong argparse parser. Chỉ có `--start/--end/--date/--flight`. Muốn custom passenger → dùng Python import trực tiếp `book_flight()`.
34. **`__init__.py` cần tồn tại** — nếu package import ra `ModuleNotFoundError`, kiểm tra có `__init__.py` trong thư mục không.

### Watcher API/Scraper — Flask integration pitfalls

35. **Import từ watcher_api trong app.py**

26. **Import từ watcher_api trong app.py** — Khi app.py chạy trong cùng thư mục với `watcher_api/`, import trực tiếp không cần prefix: 
    ```python
    # ✅ Đúng
    from checker_manager import create_watcher, list_watchers, run_check, WatcherScheduler
    from api_checker import check_route as api_check_route, check_flight_condition
    from scraper_manager import execute_booking_sync, list_previous_bookings
    ```
    Không dùng `from watcher_api.xxx import ...` vì app.py không chạy từ package context.

36. **Flask debug reloader (`debug=True`) CRASHES Playwright booking** — Khi `app.py` chạy với `debug=True`, Flask reloader restart process khi có thay đổi file. Playwright khởi tạo browser ở process cũ → bị kill khi reload. Triệu chứng: server crash không rõ nguyên nhân, lỗi Playwright transport. **Fix: luôn chạy `python app.py` không debug khi có booking**, hoặc dùng `app.run(debug=True, use_reloader=False)`.    Tốt nhất: chạy production mode riêng cho booking.

37. **Duplicate Flask endpoint error** — Khi copy-paste route decorators, dễ bị trùng function name. Lỗi: `AssertionError: View function mapping is overwriting an existing endpoint function: api_watcher_worker_stop`. Fix: `grep -n "def api_watcher_" app.py` để tìm function trùng, xóa 1 cái.    Trong context compaction session, file có thể bị duplicate dù grep chỉ show 1 — cần verify file on disk, không chỉ session cache.

38. **Frontend-backend field mismatch khi update/create watcher** — Frontend gửi `start/end/type` nhưng backend route `create_watcher` expect `from/to/monitor_type`. Flask route phải map thủ công:
    ```python
    if 'start' in data and 'from' not in data:
        data['from'] = data.pop('start')
    if 'end' in data and 'to' not in data:
        data['to'] = data.pop('end')
    if 'type' in data and 'monitor_type' not in data:
        data['monitor_type'] = data.pop('type')
    ```
    Kiểm tra frontend actual payload bằng browser console hoặc log `request.json` trước khi assume.

39. **WatcherScheduler.start() KHÔNG nhận interval_seconds argument** — method `scheduler.start()` khởi động worker với interval mặc định (600s = 10 phút). Đừng pass args vào `start()`:
    ```python
    scheduler = WatcherScheduler()
    scheduler.start()              # ✅ đúng
    # scheduler.start(600)        # ❌ TypeError: start() takes 1 positional argument
    scheduler.running             # ✅ property bool
    scheduler.stop()              # ✅ stop worker
    run_check(watcher_id)         # ✅ toplevel function check 1 watcher
    ```

31. **API checker toplevel functions** — trong `api_checker.py`:
    - `check_route(from_code, to_code, date)` — check 1 route
    - `check_flight_condition(...)` — check với điều kiện
    - `search_flight(...)` — search API B2B

32. **Context compaction + file mismatch trap** — File hiển thị trong LLM session cache có thể KHÔNG giống file thật trên disk. Luôn `grep`/`cat` trực tiếp file khi debug lỗi import/route, đừng tin session cache 100%.

### Booking History Verified
|-------|--------|------|-----|-------|------------|
| SGN→HAN | VJ120 | 15/06/2026 | PYVEP8 | #ABT00349 | 02:58 12/06 |
| HAN→TBB | VN7651 | 20/08/2026 | 5YG8UZ | #ABT00352 | 09:58 12/06 |
| HAN→HUI | VJ561 | 09/07/2026 | ZUG39P | #ABT00391 | 23:21 12/06 |
| HAN→HUI | VJ561 | 09/07/2026 | **8DW7A6** | **#ABT00392** | **23:24 12/06** |

### Web abtrip.vn (Browser tool — cho research/DOM inspection)

16. **Ant Design virtualization** — dropdown options (e66-e88) trong snapshot KHÔNG hiển thị text, chỉ hiện ref. Dùng `browser_vision(annotate=True)` để map ref→text, hoặc dùng DOM inspection qua browser_console().
17. **Ref IDs thay đổi mỗi lần remount** — KHÔNG hardcode ref làm "số thứ tự cố định". Luôn lấy snapshot mới, dùng vision annotate để map.
18. **Cần click textbox để mở dropdown** — click vào textbox (e52/e53), không click container (e21/e23).
19. **Ant Design tabs** — dropdown có 5 tab (Việt Nam, Châu Á, Châu Âu, Hoa kỳ-Canada, Châu úc-Châu Phi). Mặc định là "Việt Nam". Click tab khác nếu cần airport quốc tế.
20. **"Một chiều" vs "Khứ hồi"** — click e19 (Một chiều) thì ngày về disabled. Click e9 thì cả 2 ngày đều hiện.
21. **Button "Tìm kiếm" (e24)** — trang kết quả là client-side render, không cào được bằng web_extract. Luôn dùng browser tool.
22. **Thời gian phản hồi** — abtrip.vn search có thể mất 15-30s do Ant Design render. Kiên nhẫn chờ.

## Flask Webapp Reference

Chi tiết về lỗi thường gặp khi chạy server, import conflicts, debug mode + Playwright crash, duplicate endpoint errors:
Xem [references/flask-webapp-pitfalls.md](references/flask-webapp-pitfalls.md)

## Related: Web App for Employees

A chat-style web app wrapping `abtrip_browser.py` exists at:
`D:\AI Store\Hermes Agent\flight-booking-webapp\`

- Non-technical employees can use it without CLI
- Natural language input: "Hà Nội đi Sài Gòn 30/6"
- Runs on Flask port 5000 (LAN accessible)
- Uses the same `abtrip_browser.py` module as backend

See skill `internal-tool-web-wrapper` for the pattern to build
chat-style web UIs for internal tools.

## 🚀 VPS Deployment (hotline.abtrip.vn)

ABTRIP Hotline web app chạy trên VPS 43.156.72.127 (Tencent SG, Ubuntu 24.04):

| Component | Location | Port |
|-----------|----------|------|
| Nginx (SSL) | System | 443 → `hotline.abtrip.vn` |
| Ticketing Agent (FastAPI) | `/opt/hermes/ticketing-agent/` | 8080 |
| OpenClaw frontend | `/opt/openclaw/workspace/ticketing-agent/frontend` | Route `/abtrip` |
| OpenClaw API | — | 5001 → `/abtrip/api/` |
| n8n (Docker) | — | 5678 → `/n8n/` |

> **SSH:** `ssh -i ~/.ssh/hermes_key_vps.pem ubuntu@43.156.72.127`
> **AI Agent kiến trúc:** Xem [references/vps-ai-agent-architecture.md](references/vps-ai-agent-architecture.md)
> **Tri thức hàng không (.hermes-knowledge.md):** Xem [references/vps-hermes-knowledge-system.md](references/vps-hermes-knowledge-system.md)
> **NLU & Knowledge Upgrade:** Xem [references/vps-ai-agent-nlu-upgrade.md](references/vps-ai-agent-nlu-upgrade.md) — **đã update Sun PhuQuoc Airways + Timatic + nguồn tra cứu**
> **Kiến trúc VPS:** Xem [references/vps-ticketing-agent-deployment.md](references/vps-ticketing-agent-deployment.md)

## Hãng nội địa — tất cả 5 hãng (2026)

| Hãng | Mã IATA | Loại | Hành lý mặc định (Economy) |
|------|---------|------|---------------------------|
| Vietnam Airlines | VN | Full-service | 23kg ký gửi + 10kg xách tay |
| Vietjet Air | VJ | LCC | 0kg ký gửi + 7kg xách tay |
| Bamboo Airways | QH | Full-service | 23kg ký gửi + 10kg xách tay |
| Vietravel Airlines | VU | Hybrid | 0-20kg ký gửi + 7kg xách tay |
| Sun PhuQuoc Airways | 9G | Full-service leisure | 23kg ký gửi + 7kg xách tay |

> ⚠️ **Full-service (VN, QH, 9G)**: Hành lý ký gửi đã bao gồm trong giá vé.
> **LCC (VJ)**: Phải mua thêm hành lý ký gửi. Giá vé chỉ bao gồm xách tay.
> **Hybrid (VU)**: Tùy loại vé.

### Sun PhuQuoc Airways chi tiết
- Chủ sở hữu: Sun Group. Bay từ 11/2025.
- Hub: PQC (Phú Quốc), SGN, HAN
- Đội bay: 10 (A320neo, A321-200, A321neo)
- Website: sunphuquocairways.com
- Số hiệu: 9G + 3-4 số (VD: 9G501)
- Đường bay nội địa: PQC↔SGN/HAN/DAD, HAN↔SGN, SGN↔DAD, HPH, CXR, VDO
- Hạng Business: xách tay 14kg (2 kiện) + ký gửi 46kg (2 kiện)
- Full-service: ghế da, suất ăn nhẹ trong giá

### v0.4.0 — Seat & Price Monitoring (June 2026)
- 🆕 Thiết kế 2 bộ: API Watcher (poll B2B) + Scraper (Playwright book)
- 🆕 API B2B có `Availability` (số ghế trống — int, verified real data)
- 🆕 Xác nhận user preference: đặt song song, không hủy vé cũ trước
- 🆕 Reference file `references/flight-monitoring-strategy.md`
- 🆕 Anti-bot detection note: abtrip.vn block Playwright headless
See [references/flight-monitoring-strategy.md](references/flight-monitoring-strategy.md)

## AGT cấp 1 API V1.1 (Postman Analysis)

The complete 10-endpoint ABTrip B2B API (SearchFlight, BookFlight, IssueTicket, GetAirports, etc.) with body-based auth (`RequestInfo.PrivateKey/ApiAccount/ApiPassword`) and booking flow:
[references/abtrip-api-v1.1-analysis.md](references/abtrip-api-v1.1-analysis.md)

**Key differences from the older API version:**
- Auth moved from HTTP headers to JSON body `RequestInfo`
- Search uses `ListRoute[]` array format with `Leg`, `StartPoint`, `EndPoint`, `DepartDate`
- 10 endpoints total (added IssueTicket, GetAncillary, GetSeatMap)
- Session strings returned from SearchFlight, reused in subsequent calls

### FastAPI Backend + Chat-First Frontend (Repo: tano2026/agent.tkt)\n\nA complete system was built from the Postman analysis at `D:\\MMO Du an\\AI Agent Future\\agent.tkt\\` (GitHub: `tano2026/agent.tkt`):\n\n**Cấu hình .env lưu ý:** Xem [references/pydantic-settings-dotenv-gotchas.md](references/pydantic-settings-dotenv-gotchas.md) — quotes trong .env bị pydantic-settings đọc literal, gây lỗi URL không resolve được.

**Backend (FastAPI, 13 files, 8 routes):**
- `backend/app/main.py` — FastAPI entry, CORS (localhost:4321), lifespan
- `backend/app/models/abtrip.py` — 23 Pydantic models (SearchFlight, BookFlight, etc.)
- `backend/app/services/abtrip_client.py` — Async HTTPX client, auto-injects RequestInfo auth
- `backend/app/services/llm_gateway.py` — LLM Gateway (OmniRoute → Gemini fallback)
- ⚠️ **PITFALL:** `main.py` imports `close_llm` from `llm_gateway.py` for lifespan shutdown. If missing, backend crashes: `ImportError: cannot import name 'close_llm'`. Fix: add `async def close_llm() -> None: pass` stub. See [references/direct-run-no-docker.md](references/direct-run-no-docker.md).
- `backend/app/api/bookings.py` — POST /api/bookings/search, /book, /issue-ticket, GET /api/bookings/{code}
- `backend/app/api/reference.py` — GET /api/reference/airports, /airlines, /aircrafts
- Backend runs on port 8138 (from BACKEND_PORT env var). Docker compose maps 8765:8000 — when running WITHOUT Docker, use port 8138 directly. See [references/direct-run-no-docker.md](references/direct-run-no-docker.md).

**Frontend (Next.js 14 + TailwindCSS, 20 files) — User preference: CHAT-FIRST interface:**
- User explicitly requested: "1 ô chat, làm tất cả bằng ngôn ngữ tự nhiên" — NOT form-based
- `frontend/app/page.tsx` renders `<ChatBot />` full-screen chat
- `frontend/components/ChatBot.tsx` — NLU parsing for flight intents
- `frontend/components/ChatMessage.tsx` — 6 message types (user, bot, flight-card, booking-confirm, error, loading)
- Natural language examples: "Đặt vé từ Hà Nội đi Đà Nẵng ngày 15/7"
- `frontend/lib/api.ts` — API client with mock fallback data
- Runs on port 4321

**Docker Compose (odd ports):** frontend=4321, backend=8765, db=5987, redis=7103
**Hybrid:** Local Dev (Docker) + VPS Prod (Nginx + CI/CD)

### v0.3.0 — Book flight tested (June 2026)
- 🆕 Booking flow đã test thành công: SGN→HAN VJ120 → PNR `PYVEP8`, order `#ABT00349`, time limit `02:58 12/06/2026`
- 🆕 CLI book command với `--start/--end/--date/--flight/--first-name/--last-name/--gender/--dob/--phone/--email`
- 🆕 Booking flow section + DOM reference file
- 🆕 Pitfalls #16-22: page.evaluate quirk, form names, booking timing, multi-passenger note
- 🔧 Fixed numbering collision giữa abtrip_browser và web pitfalls sections
