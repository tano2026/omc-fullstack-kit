# Smart Agent — Phase 0 Architecture Reference

> Built 20/07/2026 on ABTrip FastAPI backend (TANO-AGENCY PROJECTS/abtrip/)

## Brand

- **Name:** Smart Agent
- **Colors:** teal #006885 + gold #DBA011 + white
- **Model:** "Bán cần câu" (A2B) — sell the fishing rod, not the fish
- **Tagline:** "Phòng vé AI — Bán thông minh, Lời tự động"
- **Domain:** Travel Tech Hybrid — travel company with AI, evolving into tech platform
- **Exit:** Build-to-flip (Hybrid: Equity / Full M&A / Franchise)

## 3 Pricing Tiers

| Tier | Price | Commission | Fast Track Margin | Key Feature |
|------|-------|------------|-------------------|-------------|
| CTV Cơ bản | 0₫/tháng | 10-30K/vé | 200K | Free AI booking |
| Đại Lý Pro | 199K/tháng | 50-150K/vé | 300K | Brand link + dashboard |
| White-label | 1.5tr/tháng | 100-300K/vé | 500K | Domain + API key riêng |

## 5 Services

1. **✈️ Vé máy bay** — AGT Cấp 1, search/book/issue real-time
2. **🛩️ Fast Track Nội Bài** — độc quyền, onsite staff 24/7, margin 200-500K/đơn
3. **🛂 Visa & Hộ chiếu** — tư vấn AI chatbot (ko API), margin 1.5-5tr/hồ sơ
4. **📱 eSIM du lịch** — auto delivery via supplier IST1, cross-sell
5. **📋 Dashboard** — real-time orders/revenue/commission + AI support

## Backend File Locations

```
D:\MMO Du an\TANO-AGENCY\PROJECTS\abtrip\backend\app\
  main.py                                — FastAPI entry (route / → Smart Agent landing)
  templates\smart_agent_landing.html     — Landing page HTML (20KB)
  services\smart_agent.py                — Multi-tenant API + subscription + payment
```

## API Endpoints

### Smart Agent (services/smart_agent.py)

| Method | Route | Purpose |
|--------|-------|---------|
| GET | `/api/smart-agent/health` | Health check |
| POST | `/api/smart-agent/register` | Register CTV |
| GET | `/api/smart-agent/tenant/{id}` | Tenant details |
| GET | `/api/smart-agent/tenants` | All tenants |
| GET | `/api/smart-agent/by-phone/{phone}` | Lookup by phone |
| POST | `/api/smart-agent/upgrade` | Upgrade tier |
| POST | `/api/smart-agent/payment/callback` | Payment webhook |
| POST | `/api/smart-agent/fasttrack` | Create Fast Track order |
| GET | `/api/smart-agent/fasttrack/orders` | List FT orders |
| POST | `/api/smart-agent/esim` | Create eSIM order |
| GET | `/api/smart-agent/esim/packages` | 8 eSIM packages |
| GET | `/api/smart-agent/dashboard/stats` | Overall stats |

### ABTrip (existing, reused)

| Method | Route | Purpose |
|--------|-------|---------|
| POST | `/api/bookings/search` | Search flights |
| POST | `/api/bookings/book` | Book flight |
| POST | `/api/bookings/issue-ticket` | Issue ticket |
| GET | `/api/bookings/{code}` | Retrieve booking |
| POST | `/api/chat` | LLM chat (ticketing/sim/visa) |
| GET | `/api/reference/airports` | Airport list |
| GET | `/api/health` | Server health |

## Multi-Tenant DB (SQLite, smart_agent.db)

Tables: tenants, subscriptions, fasttrack_orders, esim_orders, payments

Payment flow: register (free auto) → upgrade (POST /upgrade → Momo/VNPay redirect → callback confirms)

## Landing Page Sections

1. Header — sticky, teal gradient, logo + CTA button
2. Hero — badges (AGT Cấp 1, AI Booking, Fast Track, eSIM), h1 with gold span, sub, CTA
3. Stats — 4x grid (250K CTV, 230K tỷ market, <3 min booking, 5 services)
4. Services — 6 cards (vé, Fast Track, visa, eSIM, dashboard, AI 24/7)
5. How it works — 4 steps with counter circles
6. Pricing — 3 cards, featured (Pro) scaled 1.05 with gold border + badge
7. Testimonials — 4 quotes (2x2 grid)
8. FAQ — accordion, 5 questions
9. CTA — form (name + phone) → POST /api/smart-agent/register
10. Footer — copyright + links

## Key File Paths

- Landing HTML: `D:\MMO Du an\TANO-AGENCY\PROJECTS\abtrip\backend\app\templates\smart_agent_landing.html`
- Backend module: `D:\MMO Du an\TANO-AGENCY\PROJECTS\abtrip\backend\app\services\smart_agent.py`
- Main entry: `D:\MMO Du an\TANO-AGENCY\PROJECTS\abtrip\backend\app\main.py`
