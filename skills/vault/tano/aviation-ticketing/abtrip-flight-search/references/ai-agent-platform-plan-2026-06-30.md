# ABTrip AI Agent Platform — Implementation Plan (Refined)

> **Kiến trúc mới:** LLM/NLP chat interface thay thế form-based booking.
> **3 Agent:** Ticketing | SIM | Visa & Passport.
> **White-label:** CTV có brand riêng, cấu hình phí riêng.

---

## Kiến trúc Frontend (Mobile-first Chat)

```
┌──────────────────────────────────┐
│  Header (dynamic brand)          │
├──────────────────────────────────┤
│  [🛩️ Vé] [📱 SIM] [🛂 Visa]     │ ← tab bar (luôn trên cùng)
├──────────────────────────────────┤
│  ┌── Chat Messages ───────────┐  │
│  │ User: "vé HN SG ngày mai"   │  │
│  │ Bot:  ✈️ Đang tìm...        │  │
│  │       [Card kết quả bay]    │  │
│  │ User: "chuyến 7h30"         │  │
│  │ Bot:  VN230, 1.250.000₫…   │  │
│  └────────────────────────────┘  │
│  ┌── Chat Input ──────────────┐  │
│  │ [ Nhắn tin tự nhiên... ] 📎 │  │
│  └────────────────────────────┘  │
├──────────────────────────────────┤
│  Footer                          │
└──────────────────────────────────┘
```

## Tech Stack

| Layer | Công nghệ | Ghi chú |
|-------|-----------|---------|
| Frontend | Next.js 14 + TailwindCSS | PWA-ready, mobile-first |
| Backend | FastAPI (existing) | Thêm routes mới |
| LLM | Gemini 2.5 Flash + OmniRoute | Parse intent từ chat |
| DB | SQLite (POC) → PostgreSQL sau | Tenant, Fee, Chat history |
| Auth | JWT cho CTV | AGT cấp 1 tạo tài khoản |

## 3 Agent

### 🛩️ Ticketing Agent
- Chat → LLM parse → AGT API → card kết quả
- Book trong chat → xác nhận PNR
- Tra cứu booking, hủy, đổi

### 📱 SIM Travel Agent
- Chat → tìm gói SIM theo quốc gia
- Data từ supplier (folder SIM)
- Mua eSIM/SIM du lịch

### 🛂 Visa & Passport Agent
- Chat tư vấn loại visa, thủ tục
- Hỏi giấy tờ cần thiết
- Chuyển nhân viên chốt

## White-label + CTV

```
AGT cấp 1 tạo CTV → CTV có:
  - Brand riêng (logo, màu, tên)
  - Cấu hình phí dịch vụ (fixed/percent)
  - API key riêng
  - Link riêng: abtrip.vn/ctv/<slug>

KHÔNG có share link (phase hiện tại)
```

## Backend API (FastAPI)

### New Routes
```
POST /api/chat                    — LLM chat endpoint
  {message, agent, session_id, tenant_id}
  → {type, content, suggestions, session_id}

POST /api/admin/tenants           — AGT tạo CTV
GET  /api/admin/tenants           — danh sách CTV
PUT  /api/admin/tenants/:id       — update CTV
PUT  /api/admin/tenants/:id/fees  — update phí

POST /api/sim/search              — tìm SIM package
POST /api/sim/order               — đặt SIM

POST /api/visa/consult            — tư vấn visa
POST /api/visa/handoff            — chuyển nhân viên
```

### Existing Routes (giữ nguyên)
```
POST /api/bookings/search         — AGT SearchFlight
POST /api/bookings/book           — AGT BookFlight
POST /api/bookings/issue-ticket   — AGT IssueTicket
GET  /api/bookings/{code}         — AGT RetrieveBooking
GET  /api/reference/airports      — AGT GetAirports
GET  /api/reference/airlines      — AGT GetAirlines
```

## LLM Intent Parser Flow

```python
# Input từ user
user_message = "tìm vé Hà Nội Sài Gòn 20/7 2 người"

# LLM parse → structured intent
{
  "intent": "search_flight",
  "entities": {
    "origin": "HAN",
    "destination": "SGN",
    "date": "20072026",
    "adults": 2,
    "children": 0,
    "infants": 0
  }
}

# Backend: gọi AGT API → format kết quả
{
  "type": "flight_results",
  "content": {
    "flights": [...],
    "summary": "Tìm thấy 5 chuyến bay HAN→SGN ngày 20/07"
  },
  "suggestions": [
    "chuyến 7h30",
    "chuyến giá rẻ nhất",
    "chuyến bay thẳng"
  ]
}
```

## Chat States

```typescript
type ChatSession = {
  id: string;
  agent: 'ticketing' | 'sim' | 'visa';
  tenant_id?: string;
  messages: Message[];
  context: {
    pendingAction?: 'search' | 'book' | 'confirm_passenger' | 'issue_ticket';
    sessionData?: SearchSession | BookingSession;
  };
};

type Message = {
  role: 'user' | 'assistant';
  content: string;
  type?: 'text' | 'flight_results' | 'booking_confirm'
       | 'sim_results' | 'visa_info' | 'handoff';
  data?: FlightResult[] | BookingResult | SimPackage[] | VisaInfo;
};
```

## Implementation Order

```
Phase 1: Chat Ticketing (LLM + Frontend)
├── Backend: LLM Gateway + /api/chat
└── Frontend: ChatInterface + FlightResultCard

Phase 2: White-label + CTV Admin
├── Backend: Tenant DB + Admin API
└── Frontend: CTV Admin Panel

Phase 3: SIM Agent
├── SIM Backend
└── SIM Frontend

Phase 4: Visa Consultant Bot
├── Visa Bot Backend
└── Visa Bot Frontend

Phase 5: PWA + Mobile
├── PWA manifest + service worker
└── Mobile UX refinements
```

## Key Design Decisions

| Decision | Lý do |
|----------|-------|
| Chat full-width, bottom input sticky | Mobile-first UX, quen thuộc với user |
| Tab bar luôn ở trên cùng | Dễ chuyển đổi giữa 3 agent |
| Card kết quả trong chat (không popup) | Giữ flow liên tục, không mất context |
| Click card để tiếp tục conversation | Hành vi chat tự nhiên |
| CTV do AGT tạo (không self-signup) | User preference — kiểm soát chất lượng |
| Gemini + OmniRoute | User có sẵn, tiết kiệm cost |

## Risks

| Risk | Mitigation |
|------|-----------|
| LLM parse sai intent | Fallback về confirmation step |
| Chi phí LLM mỗi request | Cache intent parsing cho câu phổ biến |
| AGT API rate limit | Queue + retry mechanism |
| CTV markup quá cao | Server-enforced min/max fee |
