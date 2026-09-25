---
name: tuvi-ecommerce-system
category: tuvi
description: >
  Build a complete Tử Vi auto-sales e-commerce system: Paint Point Engine,
  FastAPI backend, Momo/VNPay payment, PDF generation, landing page with
  demo funnel, and product catalog (39+ auto-generated products).
  Company-of-one model — 100% automated, zero human hours.
version: "1.3"
related_skills:
  - tuvi-agent
  - tuvi-dau-so-expert
  - hermes-agent
---

# 🛒 TỬ VI E-COMMERCE SYSTEM — Hệ Thống Bán Hàng Chính (Kênh Tử Vi)

> **VỊ TRÍ CHIẾN LƯỢC:** Đây là landing page + e-commerce backend cho **kênh Tử Vi** — kênh chính bán sản phẩm luận giải, tư vấn, combo.  
> **Nguồn traffic:** GMSP (Giải Mã Số Phận) là social funnel trên YouTube/TikTok/Facebook dẫn người xem vào đây mua hàng.  
> **Port:** 8139 | **Folder:** `D:\MMO Du an\Tu Vi\`  
> Xem `tuvi-agent` skill cho chi tiết luận giải và đóng gói sản phẩm.

> Công ty 1 người, auto 100%. Từ Paint Point Engine → Landing Page → Thanh toán → PDF Delivery.

## 🎯 KHI NÀO DÙNG

- User muốn bán sản phẩm Tử Vi online (PDF, dịch vụ)
- User hỏi về thanh toán (Momo/VNPay), landing page, form nhập lá số
- User cần hệ thống funnel: demo miễn phí → upsell → purchase
- User muốn build "Bộ Não Phán" / "Tử Vi" commercial system

---

## 📁 CẤU TRÚC DỰ ÁN (ACTUAL — built 20/07/2026)

```
D:\MMO Du an\Tử Vi\
├── engine│
│   ├── __init__.py               # Module exports
│   ├── paint_point_engine.py     # 21 rules + 6 insights, class-based (512 lines)
│   └── tuvi_mcp_client.py        # MCP client wrapper (singleton JSON-RPC, 7 tools)
├── backend\
│   └── main.py                   # monolithic FastAPI app (port 8139, ~500 lines)
│                                  # ALL endpoints + DB + payment in ONE file
├── frontend\
│   └── index.html                # Landing page (mobile-first, dark-theme gold, ~400 lines)
├── templates\                    # (empty — index.html served directly)
├── tuvi.db                       # SQLite database (auto-created)
```

---

## 🔥 PAINT POINT ENGINE v2.0 — 21 Rules (Class-based)

> Built session 20/07/2026. File: `engine/paint_point_engine.py`

### Kiến trúc

```
Input: chart_json from mcp_tuvi_calculate_chart
  │
  ▼
normalize_star_name()  ← MCP trả về "Thien Co", rules dùng "Thiên Cơ"
  │  STAR_ALIASES dict maps 50+ tên sao không dấu → có dấu
  │
  ▼
Rule Engine (21 detection rules × 6 psychology frameworks)
  │  Mỗi rule: {cung, [sao_pattern], optional (sao_hãm, sao_hóa)}
  │  → confidence scoring (base ± boosts ± penalties)
  │
  ▼
PaintPointEngine.detect() → {
  "hits": [{rule_id, name, type, confidence, pain, hook, solution, psychology, stars, cung}, ...],
  "total_rules": 21,
  "matches": N (0-21),
  "top_type": "tính_cách" | "tiền_bạc" | "sự_nghiệp" | ...
}

PaintPointEngine.get_urgency_text() → markdown text for UI
PaintPointEngine.get_demo_report() → 7-items demo report with basic_info + top_issues
```

### ⚠️ CRITICAL: MCP Star Name Normalization

MCP `calculate_chart` returns star names **with diacritics** (e.g. "Thiên Cơ", "Thái Âm", "Địa Kiếp") — this is correct. The normalize function is still needed for:\n1. Alternate/duplicate names like "Thiên Hình" vs "Thiên Hình_2" (same star in different palaces)\n2. Fallback data sources that may not preserve diacritics\n3. Future-proofing against MCP server updates

**Always include `normalize_star_name()` and `STAR_ALIASES` dict** when building the engine. Without it, detect() matches ZERO hits despite rules being perfect.

The alias map covers 50+ star names. Add new ones as needed when MCP returns unmapped names.

### Confidence Scoring

| Factor | Adjustment |
|--------|-----------|
| Base confidence | Per-rule (0.70-0.95) |
| Thân cư this palace | +10% |
| Sao có Hóa (any) | +5% |
| Sao có Hóa Lộc | +10% |
| Có Tuần/Triệt | -5% |

Minimum confidence floor: 0.30 (no negative scores).

### 6 Psychology Frameworks Used

| Framework | Applied to |
|-----------|-----------|
| Loss Aversion | 8 rules (sợ mất → hành động gấp) |
| Confirmation Bias | 4 rules (xác nhận định kiến sẵn có) |
| Uncertainty Aversion | 5 rules (bất định → tìm câu trả lời) |
| Social Proof | 3 rules (người khác làm → mình cũng làm) |
| Sunk Cost | 4 rules (đã bỏ nhiều → không bỏ được) |
| Ego Trap | 4 rules (bản ngã → khen đúng chỗ) |

### 21 Rules Detail (ACTUAL — built 20/07/2026)

Engine file has 21 detection rules + 6 pregenerated insights. The actual rules differ from the design spec — always read the current `engine/paint_point_engine.py` for the canonical list. Key rule groups:

**NHÓM TÍNH CÁCH (Mệnh)**
- Overthinking Loop (90%) — Thiên Cơ + Thiên Hình → phân tích tới kiệt sức
- Lone Wolf Curse (80%) — Cô Thần + Quả Tú → tự làm mọi thứ một mình
- Destiny Warrior (85%) — Tử Vi + Phá Quân → làm việc lớn nhưng dễ sa vào battle
- Status Seeker (85%) — Tử Vi + Thiên Phủ → mắc bẫy giữ thể diện

**NHÓM TÀI CHÍNH (Tài Bạch)**
- Money Feast or Famine (85%) — Thái Dương + Cự Môn → tiền đến ào ạt rồi đi
- Invisible Burn Rate (80%) — Thiên Đồng + Thiên Lương → chi tiêu không tên
- Cash Trap (85%) — Hóa Kỵ → dòng tiền chậm/bị chiếm dụng
- Easy Come Easy Go (80%) — Lộc Tồn + Thiên Mã → đa nguồn nhưng không giữ được

**NHÓM SỰ NGHIỆP (Quan Lộc)**
- Career Plateau (80%) — Thái Âm + Địa Kiếp → sự nghiệp chững lại
- Boss Cage (85%) — Địa Kiếp → công việc là cái lồng
- Glass Ceiling (80%) — Tử Vi + Phá Quân + Hóa Kỵ → tài năng bị giới hạn

**NHÓM GIA ĐÌNH (Điền Trạch + Phụ Mẫu)**
- Home Front Battlefield (85%) — Kình Dương → gia đình/gia tài không yên
- Father Shadow (85%) — Tử Vi + Phá Quân + Hóa Quyền → áp lực từ cha mẹ
- Family Burden (80%) — Kình Dương + Địa Kiếp → gia đình là gánh nặng

**NHÓM TÌNH CẢM (Phu Thê)**
- Emotional Drain (85%) — Thái Dương + Hóa Kỵ → cho nhiều hơn nhận
- Love Delay (80%) — Cô Thần + Quả Tú → duyên đến muộn
- One-Sided Give (85%) — Hóa Kỵ → hy sinh lâu dần thành gánh nặng

**NHÓM SỨC KHỎE (Tật Ách)**
- Stress Overload (85%) — Thiên Hình → cơ thể lên tiếng
- Health Warning (80%) — Kình Dương + Hỏa Tinh → nguy cơ bệnh đột ngột

**NHÓM CƠ HỘI (Di Chuyển)**
- Reputation Attack (80%) — Địa Kiếp + Địa Không → uy tín bị ảnh hưởng
- Missed Chances (80%) — Thái Âm + Địa Kiếp → cơ hội đến rồi đi

**6 PREGENERATED INSIGHTS** (always appended)
- Thiên Cơ Biến Hóa (90%) — bộ não chiến lược
- Tài Lộc Đa Dạng (90%) — kinh doanh thiên bẩm
- Văn Tinh Chiếu Mệnh (85%) — khiếu viết lách
- Phá Quân Hóa Quyền (85%) — phá cách đổi mới
- Thiên Hình Cảnh Giác (85%) — pháp luật, kiện tụng
- Dịch Mã Phát Triển (85%) — phát triển khi dịch chuyển

Normalize function `_normalize_star_name()` strips all diacritics for matching.
`_star_match()` does flexible comparison (with or without diacritics).
Chart data parser handles multiple MCP response formats (dict vs list, string vs dict stars).

### ⚙️ MCP Integration via Persistent JSON-RPC Subprocess (v2 — verified 20/07/2026)

The MCP Tử Vi server (Node.js, `@modelcontextprotocol/sdk`, StdioServerTransport) CAN be called from external Python. The **recommended approach** is a **singleton process** that keeps the Node.js process alive across calls, avoiding ~3-5s re-init per call.

#### Architecture: Singleton `_MCPProcess`

File: `engine/tuvi_mcp_client.py`

```python
import subprocess, json, threading, time

MCP_SERVER_ARGS = [r"D:\AI Store\Hermes Agent\tuvi-mcp-server\index.mjs"]

class _MCPProcess:
    """Singleton: giữ 1 process MCP server, dùng chung cho mọi call."""
    
    def start(self):
        self._proc = subprocess.Popen(
            ["node"] + MCP_SERVER_ARGS,
            stdin=subprocess.PIPE, stdout=subprocess.PIPE,
            stderr=subprocess.PIPE, text=True, encoding='utf-8', bufsize=1
        )
        # Reader thread — đọc stdout liên tục
        def _reader():
            for line in self._proc.stdout:
                resp = json.loads(line.strip())
                rid = resp.get("id")
                if rid in self._pending:
                    self._pending[rid]["result"] = resp
                    self._pending[rid]["event"].set()
        threading.Thread(target=_reader, daemon=True).start()
        self._send_initialize()
    
    def call(self, tool_name, params):
        self.start()  # no-op if already started
        call_id = f"call_{tool_name}_{int(time.time()*1000)}"
        event = threading.Event()
        self._pending[call_id] = {"event": event, "result": None}
        
        req = json.dumps({"jsonrpc":"2.0","id":call_id,
            "method":"tools/call",
            "params":{"name":tool_name,"arguments":params}}) + "\n"
        self._proc.stdin.write(req)
        self._proc.stdin.flush()
        
        event.wait(timeout=30)
        response = self._pending[call_id]["result"]
        # Extract content[0].text → parse JSON
        text = response["result"]["content"][0]["text"]
        return json.loads(text)
```

**Protocol Details:**
1. Open ONE process via `subprocess.Popen` with all 3 pipes
2. Send `initialize` JSON-RPC message on stdin
3. Reader thread captures responses from stdout as they arrive
4. Each `call()` sends JSON-RPC on stdin, waits for matching `call_id` response via `threading.Event`
5. Close process on shutdown via `self._proc.stdin.close()`

**This is ~3-5x faster** than re-spawning per call (1s vs 4-6s).

#### Fallback: One-shot call (if threading unavailable)

For simple single-call scenarios where you don't need persistence:

```python
import subprocess, json, time

def mcp_single_call(tool_name, params):
    proc = subprocess.Popen(
        ["node", r"D:\AI Store\Hermes Agent\tuvi-mcp-server\index.mjs"],
        stdin=subprocess.PIPE, stdout=subprocess.PIPE,
        stderr=subprocess.PIPE, text=True, encoding='utf-8', bufsize=1
    )
    # Send initialize
    init = json.dumps({"jsonrpc":"2.0","id":"init","method":"initialize",
        "params":{"protocolVersion":"2024-11-05","capabilities":{},
                  "clientInfo":{"name":"client","version":"1.0"}}}) + "\n"
    proc.stdin.write(init)
    proc.stdin.flush()
    time.sleep(0.5)
    # Send tool call
    req = json.dumps({"jsonrpc":"2.0","id":"call","method":"tools/call",
        "params":{"name":tool_name,"arguments":params}}) + "\n"
    proc.stdin.write(req)
    proc.stdin.flush()
    # Read responses
    responses = []
    while len(responses) < 2:
        line = proc.stdout.readline().strip()
        if line:
            responses.append(json.loads(line))
    proc.stdin.close()
    text = responses[1]["result"]["content"][0]["text"]
    return json.loads(text)
```

**IMPORTANT PROTOCOL DETAILS:**
1. **`initialize` MUST come first** — Server reads one JSON-RPC msg per line. Without init, tools/call returns empty.
2. **Wait for init response before sending tool call** — ~500ms delay. Without this, the tool call may arrive before the server processes init and get ignored.
3. **`StdioServerTransport` vs `StreamServerTransport`** — TuVi MCP uses Stdio (line-based readline), not raw stream. Each JSON message MUST be on its own line with `\n` delimiter.
4. **Stderr may contain Node.js console.log output** — Either suppress with `2>/dev/null` or ignore (not JSON-RPC).
5. **Response order is deterministic** — Line 1 = init response, Line 2 = tool response. The `id` field in the response distinguishes them.

### 🔄 MCP Output Format Adapter (chart → engine)

MCP `calculate_chart` returns data with **Vietnamese keys** — different from what `PaintPointEngine.detect()` expects. You MUST adapt the format:

```python
def adapt_mcp_output(mcp_chart: dict) -> dict:
    """Chuyển đổi format MCP → format Paint Point Engine."""
    from thongTinCoBan = mcp_chart.get("thongTinCoBan", {})
    cacCung = mcp_chart.get("cacCung", [])
    
    adapted_palaces = []
    for c in cacCung:
        star_names = [s.get("ten", "") for s in c.get("sao", [])]
        adapted_palaces.append({
            "name": c.get("cung", ""),
            "stars": star_names
        })
    
    return {
        "thongTinCoBan": thongTinCoBan,
        "palaces": adapted_palaces
    }

# Usage:
# raw_chart = call_mcp_tuvi(1984, 5, 1, 9, "male")
# engine_chart = adapt_mcp_output(raw_chart)
# results = PaintPointEngine().detect(engine_chart)
```

**MCP output structure:**
```json
{
  "thongTinCoBan": {
    "gioiTinh": "Nam",
    "ngayDuong": "1984-5-1",
    "menhCung": "Tý",
    "thanCung": "Tuất",
    "nguhanhCuc": "Thủy Nhị Cục",
    "menh": "Tham Lang",
    ...
  },
  "cacCung": [
    {
      "cung": "Mệnh",
      "thienCan": "Giáp",
      "diaChi": "Tý",
      "thanCung": false,
      "daiHan": "22-31 tuổi",
      "sao": [
        {"ten": "Thiên Cơ", "loai": "chinhTinh", "doSang": "Miếu", "hoa": ""},
        {"ten": "Thiên Hình", "loai": "phuTinh", "doSang": ""}
      ]
    },
    ...
  ]
}
```

**Engine `detect()` input format (adapted):**
```json
{
  "thongTinCoBan": {...},
  "palaces": [
    {"name": "Mệnh", "stars": ["Thiên Cơ", "Thiên Hình", ...]},
    {"name": "Tài Bạch", "stars": ["Thiên Đồng", "Thiên Lương", ...]},
    ...
  ]
}
```

Key differences:
- `cacCung` → `palaces` (key rename)
- `c.sao[].ten` → just array of star name strings
- Vietnamese diacritics are preserved (MCP returns them correctly)
- Each palace also has `thienCan`, `diaChi`, `daiHan`, `thanCung` — keep in original but engine only uses `name` + `stars`

## 📊 ADMIN DASHBOARD

### Kiến trúc

Một file HTML duy nhất (`templates/admin.html`) + 3 API routes trong `backend/main.py`:

```python
# === Thêm vào imports ===
from fastapi.responses import HTMLResponse
from fastapi import Request

# === Models ===
class DemoLog(Base):
    __tablename__ = "demo_logs"
    id = Column(Integer, primary_key=True)
    session_id = Column(String(50))
    birth_year = Column(Integer)
    birth_month = Column(Integer)
    birth_day = Column(Integer)
    birth_hour = Column(Integer, default=0)
    gender = Column(String(10))
    num_paint_points = Column(Integer, default=0)
    chart_found = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

# === Routes ===
@app.get("/admin", response_class=HTMLResponse)
async def admin_dashboard():
    with open(admin_template_path, encoding="utf-8") as f:
        return HTMLResponse(f.read())

@app.get("/api/admin/orders")
async def admin_orders():
    orders = db.query(Order).order_by(Order.id.desc()).limit(50).all()
    return [{...} for o in orders]

@app.get("/api/admin/demos")
async def admin_demos():
    demos = db.query(DemoLog).order_by(DemoLog.id.desc()).limit(50).all()
    return [{...} for d in demos]

@app.get("/api/admin/stats")
async def admin_stats():
    return {"total_orders": ..., "success_orders": ..., "total_demos": ..., "revenue": ...}
```

### Frontend template pattern

File `templates/admin.html`:
- **1 file HTML** chứa tất cả: CSS inline + HTML + JS
- **No build step** — serve trực tiếp qua `HTMLResponse`
- **4 tab:** Tổng Quan, Đơn Hàng, Demo Requests, MCP Status
- **JS fetch** từ các API endpoint, render DOM
- **Light theme** (vì dashboard cần đọc nhanh, khác với landing page dark)
- Caching: server-side chỉ serve file, client-side JS quyết định tab nào active

### DemoLog logging pattern

```python
# Trong route /api/demo, sau khi detect paint points:
try:
    db = SessionLocal()
    log = DemoLog(session_id=session_id, ...)
    db.add(log)
    db.commit()
    db.close()
except:
    pass  # Không làm hỏng response nếu log lỗi
```

## 🚀 WINDOWS SERVER MANAGEMENT

### Process lifecycle

Python processes started via Hermes `terminal(background=True)` are NOT daemonized — they die when the calling shell exits. On Windows:

- Background process only lives as long as the Hermes terminal session
- To keep a server alive, either: (a) start it from a persistent terminal session, or (b) use `pythonw.exe` (no console window) + write PID file
- When re-deploying, ALWAYS kill stale processes first:

```bash
# Kiểm tra port
netstat -ano | grep 8139

# Kill process bằng PID (Windows)
taskkill //F //PID 26552

# Kill toàn bộ process đang giữ port
for pid in $(netstat -ano | grep 8139 | grep LISTEN | awk '{print $NF}'); do
  kill -9 $pid 2>/dev/null
done
```

### Port conflict resolution

Port 8139 is shared between TuVi and potential other services. Steps:
1. `netstat -ano | grep 8139` → find LISTENING PID
2. `taskkill //F //PID <pid>` → force kill
3. Wait 1-2s, verify with: `netstat -ano | grep 8139 | grep LISTEN || echo "Trống"`
4. Then restart

### SQLAlchemy 2.0 Warning

```python
from sqlalchemy.orm import DeclarativeBase  # Thay thế cho declarative_base
# Hoặc dùng: from sqlalchemy.orm import declarative_base
# Và thêm: __allow_unsubscripted_annotations__ cho type hints
```

Cảnh báo `MovedIn20Warning` về `declarative_base()` không gây lỗi — chỉ là deprecation. Sẽ cần migrate lên SQLAlchemy 2.0 style khi có thời gian.

### ✅ VERIFIED: Test with real data (20/07/2026)

Tested with user Tân's chart (1984/5/1, 9h, Nam):
- MCP returned 12 cung with full stars
- Engine detected **25 paint points** (21 rules + 4 insights from matching conditions)
- Top hits: Money Feast or Famine 95%, Home Front Battlefield 95%, Stress Overload 95%
- Full star list for Tý cung (Mệnh): Thiên Cơ, Thiên Tài, Thiên Hình

### ⚠️ Pitfall: Star name normalization still needed

Even though MCP returns Vietnamese diacritics, `PaintPointEngine._star_match()` still needs the normalize function because:
1. Some stars have alternate duplicate entries (e.g. `Thiên Hình` vs `Thiên Hình_2` for different palaces)
2. Engine rules use specific diacritic versions of star names
3. The STAR_ALIASES dict resolves these — as long as it's loaded and `_normalize_star_name()` is used, matching works

---

## 💳 THANH TOÁN

### Momo (sandbox)
- API: `https://test-payment.momo.vn/v2/gateway/api/create`
- Signature: HMAC SHA256 of `accessKey + amount + extraData + ipnUrl + orderId + orderInfo + partnerCode + redirectUrl + requestId + requestType`
- Flow: POST create → trả về payUrl → redirect user → user pay → Momo gọi IPN (POST /api/order/momo-ipn) → verify signature → update order
- Sandbox keys mặc định: `MOMO`, `F8BBA842ECF85`, `K951B6PE1waDMi640xX08PD3vg6EkVlz`

### VNPay (sandbox)
- API: `https://sandbox.vnpayment.vn/paymentv2/vpcpay.html`
- Signature: HMAC SHA512 of all sorted params
- Flow: build URL → redirect → user pay → VNPay gọi IPN (GET /api/order/vnpay-ipn) → verify `vnp_SecureHash` → update order
- Sandbox keys mặc định: `2QXU4R4K`, `HDVWDWYRHOFJJXKELNCVPEWRTFPUEWCH`

---

## 📦 39 SẢN PHẨM — 8 NHÓM

Seeded into SQLite on first `/api/products` call. All auto-generated.

| Nhóm | Số SP | Giá range | Tier |
|------|-------|-----------|------|
| Báo Cáo Cá Nhân | 10 | 299K → 399K | PDF |
| Combo Báo Cáo | 6 | 499K → 1,499K | Combo |
| Chiến Lược Cá Nhân | 5 | 399K → 499K | PDF |
| Kinh Dịch Ứng Dụng | 4 | 199K → 499K | PDF/Combo |
| Phong Thủy Ứng Dụng | 4 | 299K → 699K | PDF/Combo |
| Membership | 4 | 199K → 1,499K | Membership |
| Affiliate | 2 | 0 → 999K | Affiliate |
| B2B API | 2 | 2,999K → 29,999K | B2B |

### Mô hình 6 tầng thu nhập (income tiers)

1. **FREE** (Demo 7 paint points POST /api/demo) → kéo traffic, xây trust
2. **PDF** (10 báo cáo cá nhân × 299-399K) → mua 1 lần, auto gen
3. **BUNDLE/Combo** (6 combos × 499K-1,499K) → upsell
4. **Membership MRR** (4 gói × 199K-1,499K/m) → recurring
5. **Affiliate** (2 gói CTV, 0-999K) → mở rộng kênh bán
6. **API B2B** (2 gói × 2,999K-29,999K) → doanh nghiệp

---

## 🖥️ LANDING PAGE DESIGN — TWO THEME VARIANTS

> **Brand = 2 themes.** "Bộ Não Phán" uses dark gold. "Giải Mã Số Phận" uses light gold. See `references/landing-page-themes.md` for the full theme matrix, code snippets, and per-section comparison.

### Dark Theme (Bộ Não Phán) — original
- **Theme:** Dark (bg #0a0a1a, cards #12122a, gold accent #c9a84c)
- **Sections:** Header → Hero → 6 Pain Point Cards → Form → 39 SP grid → Footer
- **Product icons:** Emoji (🔮🧠💰)
- **Font:** System-ui stack (no externals)
- **API calls:** Relative paths (served by Flask static)

### Light Theme (Giải Mã Số Phận) — built 20/07/2026
- **Theme:** Light (white bg #FFFFFF, gold #D4A017, gray text #333)
- **Theme info:** `references/landing-page-themes.md`
- **Added sections (not in dark):** Testimonials (3 cards), FAQ (6-item accordion with chevron animation), scroll animations (IntersectionObserver), client-side validation with error messages
- **Icons:** Lucide SVG icons (CDN) instead of emoji
- **Font:** Be Vietnam Pro (Google Fonts)
- **API calls:** `const API_BASE = 'http://localhost:8139'` — full URL for static HTML served outside Flask
- **Paint point type colors:** Per-type (tai-chinh/gia-dinh/suc-khoe/tinh-cach/su-nghiep) with distinct accent colors and icon mapping
- **Footer:** Dark gray #1A1B1E bg with 3-column grid
- **Breakpoints:** 480px / 768px / 1024px
- **Section count:** 8 (vs 5 in dark variant)

## 🔗 FRONTEND INTEGRATION PATTERN (app.js)

File: `frontend/app.js` (17KB, created 20/07/2026 Phase 2)

### Architecture: 4-module pattern

```
app.js
├── Form Handler       # DOM binding + validation + POST /api/demo
├── Result Renderer    # paint points cards + progress bars + type icons
├── Payment Modal      # name/phone/email form → Momo or VNPay choice → redirect
└── Product Loader     # GET /api/products → render grid
```

### Form → API → Result flow

```javascript
// 1. Form submit handler
form.addEventListener('submit', async (e) => {
  e.preventDefault();
  // Validate: year 1900-2010, month 1-12, day 1-31, hour 0-23
  if (!validate()) return;
  
  // 2. Show loading spinner
  loadingEl.classList.add('show');
  resultEl.classList.remove('show');
  errorEl.style.display = 'none';
  
  // 3. Call API
  try {
    const res = await fetch(`${API_BASE}/api/demo`, {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({
        year: +yearInput.value,
        month: +monthInput.value,
        day: +dayInput.value,
        hour: +hourInput.value || 0,
        gender: genderInput.value === 'Nam' ? 'male' : 'female'
      })
    });
    const data = await res.json();
    
    // 4. Render result
    loadingEl.classList.remove('show');
    resultEl.classList.add('show');
    renderPaintPoints(data.paint_points);
  } catch (err) {
    // 5. Error fallback with friendly message
    loadingEl.classList.remove('show');
    errorEl.style.display = 'block';
    errorEl.textContent = '⚠️ Có lỗi xảy ra, vui lòng thử lại sau!';
  }
});

// 6. Paint points render — confidence bars with per-type colors
function renderPaintPoints(points) {
  points.forEach(p => {
    const iconMap = {'tai-chinh': 'dollar-sign', 'gia-dinh': 'home', ...};
    const html = `
      <div class="demo-pain">
        <div class="demo-pain-icon type-${p.type}">
          <i data-lucide="${iconMap[p.type] || 'alert-circle'}"></i>
        </div>
        <span class="demo-pain-name">${p.name}</span>
        <div class="demo-pain-bar">
          <div class="demo-pain-bar-fill" style="width:0%"></div>
        </div>
        <span class="demo-pain-val">${p.confidence}%</span>
      </div>
    `;
    // Animate bar after DOM insert
    requestAnimationFrame(() => {
      bar.style.width = p.confidence + '%';
    });
  });
  lucide.createIcons(); // Re-render SVG icons
}
```

### Payment Modal Flow

1. Click "Chọn Mua" on a product card (has `data-product-id`, `data-product-name`, `data-price`)
2. Modal opens with: name, phone, email + Momo/VNPay radio buttons
3. User fills → clicks "Thanh toán" → `processPayment(productId, method, customerInfo)`
4. `POST /api/payment/{method}` with `PaymentRequest` body
5. Backend returns `{order_id, payment_url, amount, product_name}`
6. Frontend: `window.location.href = payment_url` (redirect to Momo/VNPay sandbox)

### ⚠️ Pitfall: form must use `const API_BASE = ''` or full URL

If HTML is served as static files (not through FastAPI), relative fetch paths break. The subagent used `'http://localhost:8139'` as base URL. When deploying to production, this needs to be configurable or relative.

### ⚠️ Pitfall: product ID must match DB field name

Products in DB have `product_id` column storing values like "PDF01" (see Products table definition). When frontend sends `product_id`, it must match exactly. The **backend lookup** must handle multiple formats:

```python
# Safe product lookup — handles id, TV-{id}, or raw product_id
def _find_product(db, product_id):
    """Try multiple formats: id field, TV-{id} prefix, or raw product_id."""
    product = db.query(Product).filter(
        (Product.product_id == product_id) |
        (Product.product_id == f"TV-{product_id}") |
        (Product.id == product_id)
    ).first()
    if not product:
        # Fallback: exact match
        product = db.query(Product).filter(Product.product_id == product_id).first()
    return product
```

Apply this to ALL payment/order endpoints — momo, vnpay, and order/create.

### Common to both themes
- **Mobile-first:** single-column, 2-3 breakpoints
- **Form:** nhập năm/tháng/ngày/giờ/giới tính — POST /api/demo → 7 animated confidence bars
- **Products:** loaded async from GET /api/products, grid layout
- **Architecture:** Monolithic — all JS inline in index.html, no build step
- **Fallback arrays:** Demo paints + Products, so page never crashes on API failure

---

## 🚀 BUILD PATTERN — Reliable File Creation on Windows

The `write_file` tool and `terminal echo/cat` both have path issues with Vietnamese characters on this Windows setup. Reliable pattern:

```
1. write_file(path_wo_diacritics, content)  — write Python file
2. python file.py → test if execution works   — verify
3. mv to path_with_diacritics if needed       — rename after
```

For building large Python files (500+ lines), write directly with `write_file` — it passes lint checks automatically. If the path has Vietnamese characters, write to a temp path first then `mv`, or use `terminal` to `cat` content from a pipe.

## 🚀 RUN COMMANDS

```bash
# Start server
cd /d/MMO\ Du\ an/Tu\ Vi/backend
python main.py

# API sẽ chạy tại http://localhost:8139
# Landing page: http://localhost:8139/
# Health check: http://localhost:8139/health
```

---

## ⚠️ PITFALLS

1. **Template `unhashable type: 'dict'`** — Jinja2 template cache conflict when using `StaticFiles` and `Jinja2Templates` together. Fix: serve index.html as static HTML via `HTMLResponse` not `TemplateResponse`, or clear template cache.
2. **Unicode logging errors on Windows** — `logging.basicConfig(stream=sys.stdout)` fails on Vietnamese chars because Windows cp1252 can't encode. Fix: set `PYTHONIOENCODING=utf-8` or use `stream=sys.stdout` with `encoding='utf-8'`.
3. **weasyprint on Windows** — needs GTK installed. Download from: https://github.com/tschoonj/GTK-for-Windows-Runtime-Environment-Installer. Alternative: use `pdfkit` (wkhtmltopdf backend) or fallback text report.
4. **Port conflicts** — dashboard on 8137, HQ on 8138, this system uses 8139. Always check before starting.
5. **MCP tools NOT available as Python imports** — MCP tools (`mcp_tuvi_calculate_chart`, etc.) are only available as Hermes agent tools, NOT as Python packages. However, you CAN call the MCP server directly via JSON-RPC subprocess. See section **"MCP Integration via Persistent JSON-RPC Subprocess (v2)"** for the working singleton process pattern. Use `engine/tuvi_mcp_client.py` as the template. DO NOT fall back to generic mock data without trying JSON-RPC first.
6. **read_file fails on paths with Vietnamese characters** — `read_file()` tool errors on paths like `D:\MMO Du an\Tử Vi\...`. Always use `cat` via terminal for files under paths containing diacritics (tiếng Việt).
7. **PowerShell commands via bash terminal corrupt with path injection** — when running PowerShell commands through git-bash terminal, any path with spaces/special chars in the current working directory gets injected into the PowerShell command string causing parse errors. Prefer POSIX alternatives: `df -h /c/` for disk space instead of `Get-PSDrive C`.
8. **Project rename from "Bộ Não Phán" to "Tử Vi"** — folder on disk may still be named "Bo Não Phan" even after user renames on Windows (bash/MSYS path caching). To fully rename: (a) rename folder with `mv`, (b) update `index.html` logo/title/brand references, (c) update `main.py` welcome message and static path, (d) update all template references. Use `find` + `grep` to find all occurrences before editing.

9. **Desktop Control MCP intermittent failure** — `mcp_desktop_control_*` tools can fail with "Không thể kết nối tới máy tính cục bộ: All connection attempts failed." This is a transient connection issue to the local desktop agent. Fallback: use Hermes `terminal` tool for all file operations instead; it works through Hermes directly and doesn't need the desktop bridge.

11. **⚠️ CRITICAL: Code loss from MCP context compaction** — Code written by the agent during a session that is NOT saved to disk via `write_file()` or `terminal echo/cat` will be PERMANENTLY LOST when the session compacts. This happens silently. The agent may believe it wrote the file but the actual bytes never landed on disk. Prevention: (a) verify every write with a `cat` or `python file.py`, (b) do not assume `write_file()` was called on previous turn — confirm before building on top, (c) for critical files, save after EVERY logical chunk, not just at the end, (d) after any context compaction notification, re-verify all written files exist with `ls -la` or `dir`.

---

## 📚 REFERENCES

Xem `tuvi-agent` skill cho:
- Phương pháp luận giải Bộ Não Phán (5 trụ cột)
- Bridge layers (tâm lý học, định luật, game theory)
- Cách viết dễ hiểu, competitor style guide
- Product packaging and pricing strategy

Linked files:
- `references/bo-nao-phan-system-architecture.md` — session notes, file inventory, issues log, competitor research
- `references/payment-endpoint-pattern.md` — Momo/VNPay endpoint specs, signatures, and safe product lookup pattern
- `references/server-restart-windows.md` — port conflict resolution, full test battery after restart
