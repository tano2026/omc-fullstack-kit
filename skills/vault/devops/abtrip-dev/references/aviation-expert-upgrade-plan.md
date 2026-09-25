# Aviation Expert Upgrade Plan — ABTrip Brain v2

Plan produced 24 Jul 2026. Goal: turn ABTrip from a basic flight-booker into a true "chuyên gia hàng không" — expert-level knowledge of IATA regulations, TIMATIC, airline policies, fare rules, baggage conditions, and real-time policy updates.

## Current State (Baseline)

| Component | Current | Missing |
|---|---|---|
| Knowledge base | 5 VN airlines (VJ/VN/QH/BL/VU), basic policy strings | 0 international airlines, detailed fare rules |
| RAG | 11 documents (baggage, change/cancel) | TIMATIC, IATA resolutions, fare basis codes |
| System prompt | Generic flight-booking persona | Expert aviation persona with reasoning chain |
| Policy updates | Manual edits to aviation_db.py | 0 automated scraping/monitoring |
| Function calling | 3 tools (search, answer, clarify) | No visa-check, baggage-policy, fare-rules tools |

## Phase 1: Knowledge Foundation (2-3 days)

### 1.1 Expand aviation_db.py → aviation_expert.py
- **600+ international airlines** with IATA/ICAO codes
- Per-airline: baggage policy, fare rules, check-in windows, alliance membership
- **50+ popular airports** from Vietnam routes (Japan, Korea, Taiwan, China, ASEAN, Europe, Australia, US)
- **Fare basis code decoder** (Y/H/K/M/L/V/S/N/Q/T/E → meaning, restrictions, flexibility)

### 1.2 TIMATIC / TravelDoc Module
- Scrape/crawl IATA TravelCentre for passport/visa/health requirements
- Build `timatic_kb.py`: offline database for 100+ nationalities × destinations
- Query pattern: `VN passport → Thailand → visa required?`
- Update cron: weekly refresh

### 1.3 RAG: 11 → 100+ documents
Fare rules domain:
- How to read fare basis codes
- Married segments concept
- Endorsement box interpretation
- Reissue/refund/reroute rules per IATA Resolutions

Baggage domain:
- Pooling rules, special items (ski/bike/golf), dangerous goods
- Sporting equipment, musical instruments
- Excess baggage calculation per zone

Special passengers:
- UM (unaccompanied minor) rules per airline
- WCHR/WCHS/WCHC (wheelchair) codes
- MEDA (medical clearance) requirements
- INF (infant) fare rules and bassinet policies

Operational:
- Codeshare & interline agreements
- MCT (minimum connection time) per airport
- 200+ industry terms glossary (VN + EN)

## Phase 2: Expert Reasoning Engine (3-5 days)

### 2.1 Expert System Prompt Persona
```
Bạn là CHUYÊN GIA HÀNG KHÔNG với 15 năm kinh nghiệm:
- IATA/UFTAA Diploma holder
- Thông thạo IATA Resolutions 735d (reissue), 737 (refund)
- TIMATIC expert — mọi yêu cầu visa/passport/health
- Biết chính sách từng hãng: VNA, VietJet, Bamboo, Pacific, Vietravel
- Fare construction expert: phân biệt published fare vs private/IT/BT/net fare
- Tư vấn hành lý, thủ tục check-in, giấy tờ, transit visa
```

### 2.2 Multi-Step Reasoning Chain
- **Rule Engine FIRST**: before calling LLM, check aviation_db for policy questions → answer immediately (fast + accurate, 0 tokens)
- **RAG-first**: every question goes through RAG first; LLM only used for synthesis + reasoning over retrieved context
- **TIMATIC auto-lookup**: visa/passport questions automatically query timatic_kb before involving LLM

### 2.3 Function Calling Expansion (3 → 7 tools)
```python
search_flight()              # existing
answer_question()            # existing
collect_passenger_info()     # existing
check_visa_requirement(nationality, destination)  # NEW
get_baggage_policy(airline, route, fare_class)    # NEW
get_fare_rules(airline, fare_basis)               # NEW
check_travel_requirements(origin, destination, passport_nationality)  # NEW
```

## Phase 3: Auto-Update Pipeline (2-3 days)

### 3.1 Airline Policy Scraper
- One scraper per airline: VNA, VietJet, Bamboo → scrape baggage/check-in/fare rules pages
- Cron job: every 24h, compare with previous snapshot
- Diff engine: detect policy changes → Telegram alert with highlighted changes
- Auto-commit updated policy to aviation_db

### 3.2 Industry News Monitor
- RSS/API feeds: IATA press releases, Simple Flying, CAPA, VnExpress hàng không
- Filter: articles mentioning policy changes, new routes, regulatory updates
- Auto-summarize → add to RAG if relevant
- Telegram digest: weekly "tin tức hàng không" summary

## Phase 4: Expert UI (1-2 days)

### 4.1 New Quick-Ask Categories
- "Visa đi [country] cần gì?" → TIMATIC lookup
- "Hành lý [airline] đi [route]?" → policy lookup
- "Fare basis [code] nghĩa là gì?" → fare decoder
- "Em bé [age] tuổi đi máy bay cần gì?" → special passenger rules

### 4.2 Knowledge Feedback Loop
- User asks policy question → RAG miss → log to `knowledge_gaps.db`
- User corrects wrong answer → update aviation_db + re-index RAG
- Weekly review of knowledge gaps → prioritize new documents

## Priority Order (do first → last)

1. **Phase 1.2 (TIMATIC module)** — highest value, current bot blind on visa/passport
2. **Phase 1.3 (RAG expansion 11→100+)** — knowledge coverage
3. **Phase 2.1 + 2.3 (Expert Prompt + Function calling)** — reasoning brain
4. **Phase 3.1 (Policy scraper)** — keep knowledge fresh
5. **Phase 4 (Expert UI)** — surface all the new capability
