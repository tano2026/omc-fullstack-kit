# ABTrip AI Agent — LLM Chat Backend (Phase 1, July 2026)

> **Mô tả:** Backend LLM chat xử lý tìm kiếm vé, chính sách hãng, và tư vấn
> bằng ngôn ngữ tự nhiên (Gemini 2.5 Flash + OmniRoute fallback).
> Gom tất cả intent parsing + aviation domain knowledge vào 1 backend.

**Repo:** `tano2026/agent.tkt` (local: `C:\Users\Nguyen Ngoc Tan\agent.tkt`)
**Backend port:** 8137 (FastAPI, uvicorn)
**Frontend port:** 3000 (Next.js 14 dev)

## Kiến trúc

```
User: "tìm vé SG HN ngày mai 2 người"
  ↓
[ChatPanel.tsx] → POST /api/chat {message, agent, session_id}
  ↓
[api/chat.py] _handle_ticketing()
  ├── classify_intent(message)  → "search_flight" | "policy_baggage" | ...
  ├── parse_flight_search()       → structured params
  ├── _search_flights(params)     → AGT API SearchFlight
  └── format_flight_results()     → markdown + emoji
  ↓
User sees: "✈️ Hồ Chí Minh → Hà Nội | 22/07
             VN246  7:00→9:00  **1,250,000₫** ⭐ Rẻ
             VJ122  8:15→10:05 **1,390,000₫** 🚀 Nhanh"
```

## Files đã tạo (July 2026)

### Backend services

| File | Vai trò | Key feature |
|------|---------|-------------|
| `services/llm_gateway.py` | Gemini 2.5 Flash gateway | mock mode khi không có API key, system prompt aviation expert |
| `services/intent_parser.py` | Rule-based NLP parser | hiểu địa danh SG=HCM=SGN, ngày tương đối (ngày mai, cuối tuần), hãng bay |
| `services/aviation_db.py` | Aviation knowledge base | 18 nội địa + 11 quốc tế airports, 11 airlines, aliases, chính sách |
| `services/flight_formatter.py` | Kết quả → markdown đẹp | Group theo khung giờ, highlight rẻ nhất/nhanh nhất |

### Backend API

| File | Endpoint | Mô tả |
|------|----------|-------|
| `api/chat.py` | `POST /api/chat` | Main chat handler — classify intent → AGT API → format |

### Frontend

| File | Mô tả |
|------|-------|
| `components/ChatPanel.tsx` | Chat interface — bubble, quick actions, typing indicator, mobile-first |
| `app/page.tsx` | 3 tab pill (Ticketing / SIM / Visa) với state riêng |
| `app/layout.tsx` | Full-height layout, no scroll, meta tags PWA |

## Nguyên lý hoạt động

### Intent classification (rule-based, không LLM)

```python
intent = classify_intent(message)
# "vé SG HN ngày mai"     → search_flight
# "hành lý VNA"           → policy_baggage
# "đổi vé VietJet"        → policy_change
# "đặt vé VN246"          → book_flight
# "chào bạn"              → greeting
```

### Flight search parsing (fast path, không LLM)

```python
params = parse_flight_search("vé từ hcm ra nha trang 20/7 2 trẻ em")
# → {"origin": "SGN", "destination": "CXR", "date": "20072026",
#     "adults": 1, "children": 2}
```

### LLM fallback (khi intent không rõ)

Khi `classify_intent` trả về `"greeting"` hoặc không match, fallback qua Gemini:
- System prompt: aviation expert (địa danh, hãng bay, chính sách)
- LLM có thể trả JSON tool call: `{"tool": "search_flight", "params": {...}}`
- Hoặc reply text: `{"reply": "Chào bạn..."}`

### Flight result format

```
✈️ Hồ Chí Minh → Hà Nội | 22/07/2026

🌅 Sáng
  VN246  7:00→9:00  **1,250,000₫** ⭐ Rẻ
  VJ122  8:15→10:05 **1,390,000₫** 🚀 Nhanh

☀️ Chiều
  QH203  14:00→15:50 **1,450,000₫**

📊 1 người lớn
💰 Tổng thấp nhất: **1,250,000₫**

👉 Bạn muốn chọn chuyến nào?
```

## Aviation DB trọng tâm

**18 sân bay nội địa + 11 quốc tế** với alias full:
```python
LOCATION_ALIASES = {
    "hà nội": "HAN", "hn": "HAN", "sài gòn": "SGN", "hcm": "SGN",
    "đà nẵng": "DAD", "nha trang": "CXR", "phú quốc": "PQC",
    # ... cộng 60+ aliases nữa ...
}
```

**5 hãng nội địa** + 6 quốc tế với chính sách hành lý/đổi/hủy:
```python
POLICIES = {
    "hành lý": {"VN": "...", "VJ": "...", ...},
    "đổi vé": {"VN": "...", ...},
    "hủy vé": {},
    "giấy tờ": {"nội địa": "...", "quốc tế": "..."},
}
```

## 3 Tab Agent

| Agent | Tab | Handler |
|-------|-----|---------|
| Ticketing | 🛩️ Vé máy bay | `_handle_ticketing()` — kết nối AGT API + chính sách |
| SIM | 📱 SIM du lịch | `_handle_sim()` — LLM generic + IST1 API sau này |
| Visa | 🛂 Visa & Hộ chiếu | `_handle_visa()` — LLM tư vấn, chuyển nhân viên chốt |

Lưu ý: session state giữa các lần chat qua `_sessions[session_id]` dict in-memory (sẽ upgrade lên Redis sau).

## Cấu hình

```bash
# .env
GEMINI_API_KEY="..."     # Gemini 2.5 Flash API key
AGT_PRIVATE_KEY="..."    # AGT cấp 1
AGT_API_ACCOUNT="..."
AGT_API_PASSWORD="..."
BACKEND_PORT=8137        # odd port
```

## Chạy

```bash
# Backend
cd agent.tkt/backend
uvicorn app.main:app --reload --port 8137

# Frontend
cd agent.tkt/frontend
npm run dev              # port 3000 mặc định
```

## Phase tiếp theo

1. **Phase 2**: White-label + CTV Admin (tenant DB, fee config, login)
2. **Phase 3**: SIM Agent (parse IST1 API doc → structured packages)
3. **Phase 4**: Visa Consultant Bot (knowledge base + referral to agent)
4. **Phase 5**: PWA (manifest, service worker, installable)
