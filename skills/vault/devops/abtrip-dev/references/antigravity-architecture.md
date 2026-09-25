# Antigravity Architecture — Aviation Expert Brain

**Date:** 24 Jul 2026
**Status:** Phase 1-3 implemented, Phase 4 pending

## Data Sources (realistic, $0 budget)

### 1. TIMATIC / Visa-Passport
| Source | Type | Feasible? |
|---|---|---|
| IATA TravelCentre (`iatatravelcentre.com`) | Web public | ✅ Scrapable |
| Wikipedia "Visa requirements for Vietnamese citizens" | Wiki table | ✅ Structured, community-updated |
| Emirates/Turkish Airlines visa tool | Web tool | ✅ Free, TIMATIC-licensed data |
| IATA TIMATIC API | Official API | ❌ $5000+/year |

**Strategy:** Crawl Wikipedia + IATA TravelCentre → build offline visa/passport DB.

### 2. Airline Policies (Vietnamese carriers)
| Airline | IATA | Source URL |
|---|---|---|
| Vietnam Airlines | VN | `vietnamairlines.com/vn/vi/travel-information/baggage` |
| VietJet Air | VJ | `vietjetair.com/vi/hanh-ly` |
| Bamboo Airways | QH | `bambooairways.com/vn-en/travel-information/baggage/` |
| Pacific Airlines | BL | `pacificairlines.com.vn/vi/hanh-ly` |
| Vietravel Airlines | VU | `vietravelairlines.vn/hanh-ly` |
| Sun PhuQuoc Airways | 9G | `sunphuquocairways.com/baggage` |

### 3. IATA / Industry Knowledge
- IATA Passenger Standards Conference Manual (public PDFs)
- FlyerTalk, Airliners.net (community knowledge)
- ATPCO/Fare Basis decoder articles
- OAG/FlightGlobal industry news

### 4. Auto-Update Sources
- VnExpress Kinh doanh > Hàng không (RSS)
- Cục Hàng không VN (`caa.gov.vn`)
- Airline Facebook pages (VJ changes policies via FB)
- Simple Flying (international news)

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│                  User Query (chat input)                 │
└──────────────────────┬──────────────────────────────────┘
                       │
                       ▼
         ┌─────────────────────────────┐
         │   is_operational_query()    │
         │   regex: 85+ aviation       │
         │   keywords vs booking terms │
         └──────────┬──────────────────┘
                    │
        ┌───────────┴───────────┐
        │                       │
        ▼ (Ops)                 ▼ (Booking)
┌───────────────┐      ┌──────────────────┐
│  RagService   │      │  Flight MCP      │
│  .query()     │      │  (abtrip_client) │
└───┬───────┬───┘      └──────────────────┘
    │       │
    ▼       ▼
┌────────┐ ┌──────────────────┐
│aviation│ │airline_policies  │
│  _kb   │ │                  │
│ IATA   │ │ Hãng VN (6):     │
│ airports│ │ baggage, fees,   │
│ airlines│ │ checkin, meals   │
└────────┘ └───────┬──────────┘
                   │
                   ▼
         ┌──────────────────┐
         │  Policy Crawler  │
         │  (cron: every 6h)│
         │  aiohttp + bs4   │
         └──────────────────┘
```

## Implementation Status

### ✅ Done (24 Jul 2026)
- [x] `rag_service.py` — dual-collection RAG (rewrote from `rag_knowledge.py`)
- [x] `is_operational_query()` — operational vs booking classifier
- [x] `aviation_db.py` — Sun PhuQuoc Airways (9G/SPQ) added
- [x] `policy_crawler.py` — scraper for 6 VN airlines
- [x] `RagService.upsert_policy()` — crawler integration point

### 🔄 Pending
- [ ] Decision node in `smart_agent.py` `/chat` — inject RAG context before LLM
- [ ] Hermes cron for policy_crawler (every 6h or daily)
- [ ] TIMATIC/Wikipedia scraper for visa/passport data
- [ ] International airline policies (600+ airlines)
- [ ] RSS auto-update from aviation news sources

## Key Design Decisions

1. **$0 budget** — all data from public web scraping, no paid APIs
2. **Dual collection** — separates permanent IATA knowledge from frequently-updated airline policies
3. **Crawler → RAG pipeline** — crawler scrapes HTML, upserts directly to `airline_policies` collection
4. **Regex classifier** — `is_operational_query()` is fast, deterministic, no LLM cost for routing
5. **Backward compatible** — existing `rag_format_context()` works with new dual-collection merge
