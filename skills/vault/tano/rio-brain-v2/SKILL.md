---
title: RIO Brain v2.0 — Research & Intelligence Officer
name: rio-brain-v2
description: Full brain architecture cho RIO bot — Pipeline 7 stage (INTAKE→PLAN→COLLECT→VALIDATE→ANALYZE→SYNTHESIZE→VERIFY→DELIVER) + ChatBrain natural language layer, code-driven state machine, zero API key mặc định, adapter registry pattern.
author: Tano Agency
---

# RIO Brain v2.0 — Bộ não cho Research Bot

## Tổng quan

Brain cho @Tano_research_pro_bot với 2 lớp:
- **RIOBrain** (brain.py) — pipeline 7 stage, command-based routing
- **ChatBrain** (chat_brain.py) — natural language layer trên RIOBrain

Kế thừa từ analytics.py (8 classes) và các skill Hermes.

**Zero dependency:** Chỉ dùng stdlib (sqlite3, re, html.parser, time, threading, urllib)

## Architecture — 2 lớp brain

```
rio-bot/
├── ratelimit.py              # Token bucket + cache-first + exponential backoff
├── modules/
│   ├── memory.py             # SQLite 4 bảng
│   ├── validator.py          # Sanitize HTML/JS + fact rating ✅🟡🔄 + anti-hallucination
│   ├── brain.py              # RIOBrain — Pipeline 7 stage + adapter registry
│   ├── chat_brain.py         # ChatBrain — Natural language intent detection
│   └── (analytics.py)        # Kế thừa — 8 classes
└── rio_bot.py                # Wire cả 2 brain vào polling loop
```

## Pipeline 7 Stage (RIOBrain)

```
INTAKE → PLAN → COLLECT → VALIDATE → ANALYZE → SYNTHESIZE → VERIFY → DELIVER
  │       │        │          │          │           │          │        │
  │       │        │          │          │           │          │        └─ chunk 4096, log memory
  │       │        │          │          │           │          └─ checklist + 1 retry
  │       │        │          │          │           └─ analytics.py or template synthesis
  │       │        │          │          └─ SentimentMiner/TrendForecaster/KPIDashboard etc.
  │       │        │          └─ sanitize() + rate_fact() → ✅🟡🔄 rating
  │       │        └─ web_search + sub-questions via adapter registry
  │       └─ sub-question templates (5 per research type)
  └─ parse → ResearchTask
```

## ChatBrain — Natural Language Layer

**Vấn đề mà ChatBrain giải quyết:** User không muốn gõ command. Họ muốn nói tự nhiên và bot tự hiểu.

### V1 → V2 → V3 → V4 Evolution (Jul 2026)

**V5 changes (Jul 18):** Migrated LLM backend from OpenRouter → DeepSeek API direct
- **CRITICAL CHANGE:** ALL LLM calls now use `DEEPSEEK_API_KEY` env var + `https://api.deepseek.com/v1/chat/completions` + `model: "deepseek-chat"` — NOT OpenRouter anymore.
- **Why:** RIO bot had no `OPENROUTER_API_KEY` in .env. `_cross_reference()`, `_implication()`, `_llm_analysis()` all checked `os.environ.get("OPENROUTER_API_KEY")` → got empty → silently skipped every LLM step → output was raw snippet dump with no synthesis.
- **Fix pattern:** Introduced `_call_llm(system, prompt, temperature, max_tokens)` helper in both `brain.py` (RIOBrain class method) and `chat_brain.py` (ChatBrain class method). Every LLM call that was an inline `urllib.request` block now goes through this single helper.
- **Sync:** `_template_synthesis()` checks `DEEPSEEK_API_KEY` instead of `OPENROUTER_API_KEY`
- **Sync:** `_optimize_search_query()` default model changed from `deepseek/deepseek-chat` (OpenRouter model string) to `deepseek-chat` (DeepSeek native), default URL from `api.openrouter.ai` to `api.deepseek.com`
- **Sync:** ChatBrain init changed: `self.llm_api_key = os.environ.get("DEEPSEEK_API_KEY", "")`, URL and model updated
- **Sync:** `rio_bot.py` must read `DEEPSEEK_API_KEY` from .env and set into environ. The `.env` now needs both `RIO_BOT_TOKEN` and `DEEPSEEK_API_KEY`.
- **PITFALL:** f-string with `\n` in patch content gets double-escaped (`\\n`). Always verify newlines after patching.
- **PITFALL:** When migrating from OpenRouter, 4 separate code blocks use the old API call pattern. Check ALL of them — missing one means that LLM feature silently fails.
- **Pattern:** Any standalone LLM-powered bot should use a `_call_llm()` helper from day one. Inline urllib blocks are copy-paste magnets that rot when the API changes.

**V4 changes (Jul 17):** LLM-powered search + content extraction (legacy, now uses V5 DeepSeek backend)
- **NEW: `_optimize_search_query()`** — replaces static `_build_search_query()`. Calls LLM to rewrite user query into short focused Vietnamese search queries (≤5 words). Removes generic keywords ("thị trường", "đối thủ", "giá cả") that cause DDG to match irrelevant results (Amazon, SellerSprite).
  - Example: `"nghiên cứu ngách bán fastrack sân bay"` → `"fastrack sân bay nội bài"` instead of `"ngách bán fastrack thị trường đối thủ giá cả"`
  - Config: DEEPSEEK_API_KEY env var, model deepseek-chat
  - Fallback: clean topic without keyword suffixes
- **NEW: `fetch_page_content()`** in web_research.py — fetches real HTML content from result URLs using stdlib HTMLParser. Skips script/style/nav/footer. Plain text up to 3K chars. Zero dependencies.
- **NEW: `_llm_analysis()`** in brain.py — replaces template synthesis. Pipeline: fetch real content from each URL → feed to LLM → LLM filters off-topic results, classifies [FACT]/[ƯỚC TÍNH]/[CẦN XÁC MINH], responds using only real content. Falls back to template synthesis on failure.
- **Fix for DDG irrelevant results:** Root cause 1 — generic query suffixes matched commercial platforms. Root cause 2 — template synthesis grouped by rating without content analysis. Fix — LLM both optimizes search query AND filters/analyzes results.
- **Pattern:** When search results are irrelevant, fix at TWO points: (1) improve the search query to be more precise, (2) add a result-filtering layer that discards off-topic content before synthesis.

**V3 changes (Jul 17):****
- **NEW intents:** `market` (weight 1.2) + `competitor` (weight 1.1)
- market keywords: thị trường, ngách, niche, phân khúc, quy mô, tiềm năng, cơ hội, nhu cầu, khách hàng, target, đối tượng, nghiên cứu thị trường, segment, demand, bán, kinh doanh, mở, buôn, bán hàng
- competitor keywords: đối thủ, cạnh tranh, competitor, competition, ai là, so với, thắng, thua, lợi thế, điểm yếu, swot, thị phần, market share, positioning, đánh giá, review, chất lượng, uy tín
- **Improved depth detection:** thêm "nghiên cứu", "ngách", "thị trường", "đối thủ", "cạnh tranh", "swot", "research", "market" → deep
- **Lowered depth threshold:** từ 8 từ xuống 5 từ (phát hiện query phức tạp sớm hơn)
- **V3 search query per intent:**
  - `market` → `"{topic} thị trường đối thủ giá cả"`
  - `competitor` → `"{topic} đối thủ cạnh tranh review đánh giá"`
- **V3 response format:** thêm case cho market ("phân tích thị trường:") + competitor ("phân tích đối thủ:")

**Trigger cho V3:** User hỏi "nghiên cứu ngách bán fastrack sân bay nội bài" → detect thành `general` + search "ngách fastrack sân bay nội" (0 kết quả). Thiếu hẳn keyword market/competitor dẫn đến intent sai → search query sai → 0 sources.

### V1 → V2 Evolution (Jul 2026)

| Aspect | V1 (đã chết) | V2 (hiện tại) |
|--------|-------------|--------------|
| Intent types | 7 types (market/competitor/trend/sentiment/forecast/swot/deep) | 4 core types (comparison/data/trend/advice) + factual/general |
| Stop words | Không có — search query giữ nguyên "mày thấy", "có vẻ", "ko khớp lắm nhỉ" | 60+ VI stop words filtered + prefix/suffix cleanup |
| Topic extraction | Regex prefix removal cơ bản | Multi-layer: prefix → suffix → stop word token filter |
| Output format | Template-based với rating badges ✅🟡🔄 | Natural language — expert advisor tone, no badges |
| Brain pipeline routing | Luôn gọi brain.run() với rtype detect → pipeline trả lời form cứng | Chỉ gọi brain cho data/comparison/general, factual/advice search trực tiếp |
| Intent fallback | "deep" với confidence 0.3 → research 6 câu hỏi | "general" với kiểm tra factual/opinion trước |
| send_action | Không gửi typing indicator | `send_action(chat_id, "typing")` trước khi xử lý |

### ⚠️ CRITICAL: ResearchTask.TYPES Sync

**ChatBrain detect_intent() trả về rtype → phải có trong ResearchTask.TYPES, nếu không bot crash.**

ResearchTask.TYPES trong brain.py phải luôn include mọi rtype mà ChatBrain có thể trả về:

```python
# brain.py
TYPES = {
    "market", "swot", "sentiment", "forecast", "kpi",
    "deep", "competitor", "trend",
    "general", "data", "comparison", "advice", "factual",  # ChatBrain types
}
```

**Rule:** Khi thêm intent mới trong ChatBrain, phải add đồng thời vào ResearchTask.TYPES. Nếu quên → bot crash với "Unknown research type: {x}. Must be one of ..."

**VerificationLoop.verify() cũng cần sync** — các type mới cần được check ở cùng level với market/deep/competitor (exec_summary + rating + sources_min_2).

### ### V4 Intent Detection + Optimization Architecture

```
User query
  │
  ├─ 1. detect_intent() — phân loại (like V3)
  │
  ├─ 2. _optimize_search_query() — LLM query rewrite
  │   ├─ Gửi raw_query + intent cho DeepSeek
  │   ├─ LLM viết lại thành 1-2 query ngắn (≤5 từ)
  │   ├─ QUAN TRỌNG: bỏ từ khóa generic gây nhiễu
  │   └─ Fallback → clean topic
  │
  ├─ 3. search_fn(search_query)
  │
  ├─ 4. _llm_analysis() — content extraction + LLM synthesis
  │   ├─ fetch_page_content() từng URL → content thật
  │   ├─ Gửi content cho DeepSeek phân tích
  │   ├─ LLM lọc kết quả lạc đề, phân loại FACT/ƯỚC TÍNH
  │   └─ Trả về natural language analysis
  │
  └─ 5. _build_vi() — fallback khi LLM ko available
```
  │   ├─ Remove prefix patterns: "cho tao hỏi", "mày thấy", "phân tích"
  │   ├─ Remove suffix patterns: "thế nào", "ra sao", "nhỉ", "à"
  │   └─ Token filter: 60+ VI_STOP_WORDS + remove single chars
  │
  ├─ 2. detect_intent() — phân loại
  │   ├─ comparison keywords → "comparison"
  │   ├─ data keywords → "data"
  │   ├─ trend keywords → "trend"
  │   ├─ advice keywords → "advice"
  │   ├─ factual patterns → "factual"
  │   ├─ opinion patterns → "advice" (low conf)
  │   └─ default → "general"
  │
  ├─ 3. Route — ALL intents go through brain pipeline (V2.1+)
  │   ├─ Mọi rtype → brain.run(rtype, topic, ...)
  │   ├─ Brain output dài (>2K) → _summarize_brain_output()
  │   └─ Brain fail → fallback direct search
  │
  └─ 4. _build_vi() / _build_en() — natural language
      ├─ Mở đầu: "Số liệu về {topic}:" / "so sánh thế này:"
      ├─ Nội dung: số thứ tự + snippet, mỗi cái 1 dòng
      ├─ Link: 🔗 url
      └─ Kết: tùy rtype (kết luận / tóm lại / lưu ý số liệu)
```

**Important routing change (V2 → V2.1):** Originally only `data`/`comparison`/`general` went through brain pipeline; `factual`/`advice` used direct search. After user reported bugs, changed to ALL intents → brain pipeline (the brain's template synthesis handles unknown types gracefully via `get_sub_questions` fallback to "deep").

### Intent Detection Pattern (V2)

| Câu hỏi mẫu | rtype | Route (V2.1+) |
|-------------|-------|-------|
| "thị trường X thế nào?" | data / general | brain pipeline |
| "so sánh A vs B" | comparison | brain pipeline |
| "xu hướng X 2026" | trend | brain pipeline |
| "nên làm YouTube gì?" | advice | brain pipeline |
| "giá token DeepSeek?" | data | brain pipeline |
| "ai là CEO của OpenAI?" | factual | brain pipeline |
| "cách kiếm tiền online" | advice | brain pipeline |

### ChatBrain V5 Code Structure (current)

```python
class ChatBrain:
    def __init__(self, adapters):
        self.llm_api_key = os.environ.get("DEEPSEEK_API_KEY", "")
        self.llm_api_url = "https://api.deepseek.com/v1/chat/completions"
        self.llm_model = "deepseek-chat"
    
    def _call_llm(self, system, prompt, temperature=0.3, max_tokens=1000):
        """Single helper for all LLM calls. Reads self.llm_api_key."""
        ...
    
    def chat(self, query):
        intent = detect_intent(query)
        search_query = self._optimize_search_query(query, intent)
        ...
    
    def _llm_synthesis(self, sources, topic, rtype, lang):
        """V5: LLM synthesizes search results into natural language response.
           Replaces raw snippet dump from V2 _build_vi()."""
        ...
    
    def _quick_search(self, query, topic, intent):
        search_query = self._optimize_search_query(query, intent)
        ...
    
    def _optimize_search_query(self, raw_query, intent):
        """LLM rewrites user query → short focused search query."""
        if not self.llm_api_key:
            return self._fallback_query(intent)
        # Uses self._call_llm() via _call_llm() helper
        ...

# Free functions (not methods):
def _clean_query(query):  # called by detect_intent(), not self
def detect_intent(query):  # returns dict with rtype, depth, topic
def _optimize_search_query(raw_query, intent, api_key, api_url, model):  # standalone fallback
```

**Routing change in V4:** `chat()` and `_quick_search()` both call `_optimize_search_query()` directly. The old `_build_search_query()` still exists as dead code but is no longer called anywhere. Remove it in V5 cleanup.

### ChatBrain V2 Key Differences from V1

1. **Stop word filtering is MANDATORY** — without it, search queries include Vietnamese conversation filler ("mày thấy", "có vẻ", "ko khớp") which produces garbage search results. The VI_STOP_WORDS set has 60+ entries for Vietnamese only (not English — English queries are typically precise).

2. **Template-based output is DEAD** — V1 used SHALLOW_TEMPLATE/DEEP_TEMPLATE with rating badges. V2 uses `_build_vi()` / `_build_en()` which produces raw natural language. No "📊 Nguồn: 5 | Độ tin cậy: 3✅ 2🟡" footer.

3. **Brain pipeline is NOT always the answer** — when user asks factual questions ("ai là?", "bao nhiêu?", "có nên?") or advice, direct search + natural response is better than running the full 7-stage pipeline which produces a formal report.

4. **Brain output summarization** — if brain output exceeds 2K chars, V2 extracts only the executive summary + conclusion sections instead of dumping the full report.

### Integration into rio_bot.py

```python
# In handle_message():
if modules_loaded.get("chat_brain") and chat_brain:
    try:
        send_action(chat_id, "typing")  # MUST send typing first
        response = chat_brain.chat(text)
        if len(response) > 4000:
            for i in range(0, len(response), 4000):
                send_message(chat_id, response[i:i+4000])
        else:
            send_message(chat_id, response)
        return
    except Exception as e:
        log.warning(f"ChatBrain error: {e}")

# Legacy fallback
handle_research(chat_id, text)
```

### Pitfalls — ChatBrain V2/V4

1. ✅ **Stop word critical** — Nếu thiếu stop word filter, search query bị nhiễm tiếng Việt nói (kéo dài 0.5h debug mới phát hiện). Luôn kiểm tra `_clean_query()` output trong log.
2. ✅ **Brain pipeline vẫn trả lời form cứng** — V1 gọi brain.run() → brain trả về market report với 6 section. V2 fix bằng cách chỉ gọi brain cho data/comparison/general, và summarization khi dài.
3. ✅ **Natural response ≠ no structure** — V2 vẫn có structure (mở đầu → N bullets → kết luận), nhưng dùng ngôn ngữ tự nhiên thay vì template placeholder.
4. ⚠️ **send_action before heavy work** — Luôn gọi `send_action(chat_id, "typing")` *trước* khi gọi chat_brain.chat() (có thể mất 10-30s cho deep research). Không gọi sau.
5. ⚠️ **Language detection** — V2 vẫn dùng diacritics regex (giống V1). Tiếng Việt không dấu detect thành EN. Hậu quả: response tiếng Anh cho câu hỏi Việt không dấu.
6. ⚠️ **Follow-up detection fragile** — short query heuristic có thể false positive.
7. ⚠️ **Summarization lossy** — `_summarize_brain_output()` có thể bỏ qua phân tích chi tiết.
8. ⚠️ **LLM-dependent features** — `_optimize_search_query()` và `_llm_analysis()` cần OPENROUTER_API_KEY. Nếu key expired hoặc rate-limit, bot tự fallback về template synthesis. Luôn kiểm tra log để biết LLM có hoạt động không.
9. ⚠️ **fetch_page_content timeout** — Fetch từng URL trong `_llm_analysis()` có timeout 10s. Nếu nhiều URLs cùng chậm (site chết, chặn bot), tổng thời gian có thể lên 50s+. Cần giới hạn max 5 URLs, timeout 10s mỗi cái.
10. ⚠️ **LLM temperature** — `_optimize_search_query()` dùng temperature 0.1 (deterministic). `_llm_analysis()` dùng 0.3 (creative analysis). Nếu lẫn, query optimize sẽ thêm từ không cần thiết hoặc analysis quá cứng nhắc.
12. ⚠️ **`_clean_query()` là function, không phải method** — detect_intent() gọi `_clean_query()` như free function, không phải self._clean_query(). Nếu vô tình đổi thành method, detect_intent sẽ crash với TypeError.
13. ⚠️ **Double search_query assignment bug** — Khi patch `_quick_search()`, dễ duplicate `search_query = ...` và `try:` block. Luôn kiểm tra syntax sau patch.
14. ⚠️ **LLM-powered bot .env needs key** — Nếu brain.py/chat_brain.py kiểm tra `os.environ.get("DEEPSEEK_API_KEY")` mà key không có trong .env, mọi LLM feature silently skip. Luôn verify .env khi deploy.
15. ⚠️ **User preference: cron notifications = spam** — User không muốn cron job báo mỗi lần chạy. Set `deliver=local` hoặc dùng `no_agent=True` script pattern. Chỉ báo khi có phát sinh mới.
16. 🔴 **FILE PATH MISMATCH: PLATFORM/rio-brain/ DOES NOT EXIST** — RIO bot code actually lives at `D:/MMO Du an/TANO-AGENCY/rio-bot/modules/`. The old path `PLATFORM/rio-brain/core/brain.py` was an assumption that never materialised. If you patch files at `PLATFORM/rio-brain/`, you are wasting effort. Always verify actual file paths with `search_files()` before editing. RIO bot layout: `rio-bot/rio_bot.py` (entry point), `rio-bot/modules/brain.py`, `rio-bot/modules/chat_brain.py`, `rio-bot/.env`.

## 4 Modules nền tảng

### 1. ratelimit.py — 3 classes
- `TokenBucket(rate=0.5, capacity=3)` — thread-safe, 1 req/2s
- `ExponentialBackoff(base=2, max=60)` — jitter randomization
- `SearchCache(ttl=24h)` — file-based, SHA256 key, auto-cleanup
- `ThrottledSearcher` — wrapper: check cache → acquire token → retry 3x với backoff → store cache

### 2. memory.py — SQLite 4 bảng
- `research_history` — (rtype, topic, result_summary, source_count, duration_ms, status) — UNIQUE(rtype, topic)
- `evidence_cache` — (url UNIQUE, domain, title, snippet, rating, ttl_hours) — TTL-based expiry
- `source_scores` — (domain UNIQUE, score, hit_count, fail_count) — ELO-style learning
- `lessons` — (lesson, context, severity, created_at) — error/learning log
- Schema versioning: `schema_version` table, auto-migration

### 3. validator.py — 3 functions
- `sanitize(raw)` — strip HTML/script/style/event-handlers, remove null bytes/control chars, truncate
- `rate_fact(text, url, source_count)` → ✅/🟡/🔄/🟠/❓ with source_score + reason
  - ✅ Confirmed: ≥2 sources domain khác nhau
  - 🟡 Single-source: 1 domain, trust level High/Medium/Low
  - 🔄 Inference: bot's reasoning, zero sources
  - 🟠 Likely wrong: contains red flag keywords + low trust domain
- `check_report(text)` — detect_orphan_numbers + detect_generic_ai → PASS/WARN/FAIL
- RED_FLAG_KEYWORDS: "revolutionary", "game-changing", "đột phá", "mang tính cách mạng"...

### 4. brain.py — RIOBrain class
- `RIOBrain(adapters=dict)` — adapters injected từ rio_bot.py, không import cứng
- `run(rtype, topic, **kwargs) → list[str]` — full pipeline, returns chunks
- `get_sub_questions(rtype, topic, language)` — 5 templates mỗi type (support EN+VI)
- `VerificationLoop` — type-specific checks:
  - Generic: has_content, has_sources, anti-hallucination
  - market/deep: exec_summary, rating, sources≥2
  - swot: has 4 sections
  - forecast: confidence/triển vọng
- `chunk_report(text, max=4096)` — smart split, không cắt giữa table
- Cache-check trước: kiểm tra research_history trước khi gọi search

## Sub-question templates

Research type → 5 sub-questions (VI + EN):
- market: size, competitors, trends, challenges, CAGR
- swot: strengths, weaknesses, opportunities, threats, reviews
- sentiment: public opinion, news, reviews, controversies
- forecast: past, present, future, related tech, risks
- competitor: products, pricing, position, reviews, developments
- deep: overview, developments, expert analysis, stats, outlook
- trend: latest, patterns, viral, community

## Anti-hallucination

1. **Orphan number detector:** phát hiện %/$/users không gắn evidence nearby
2. **Generic AI language detector:** "trong thời đại 4.0", "game-changing", "đột phá"...
3. **Verification loop:** checklist code-driven trước deliver, fail thì warn không im lặng
4. **Fact ledger ✅🟡🔄:** mọi source đều có rating, không có evidence = không in

## Telegram Bot Conflict — Debug & Fix

**Khi launch bot mới mà báo `Conflict: terminated by other getUpdates request`:**

### Root cause
Một instance khác (thường là bot cũ chưa kill sạch, hoặc VPS/OpenClaw instance từ xa) đang poll cùng bot token. Telegram chỉ cho phép 1 getUpdates connection.

### Fix steps (thứ tự ưu tiên)
1. **Kill all python processes** — `ps aux | grep python | grep -v grep` → kill toàn bộ, không chỉ riêng bot
2. **Reset webhook** — `curl -s "https://api.telegram.org/bot${TOKEN}/deleteWebhook?drop_pending_updates=true"`
3. **Reset getUpdates offset** — `curl -s "https://api.telegram.org/bot${TOKEN}/getUpdates?offset=999999999"` (đặt offset rất cao để clear queue)
4. **Verify** — `curl -s "https://api.telegram.org/bot${TOKEN}/getUpdates?offset=-1"` → `ok:true, results:0`
5. **Launch** — chỉ 1 instance duy nhất, đảm bảo không có instance cạnh tranh (VD từ VPS OpenClaw)

### Prevention
- Nếu bot dùng polling riêng (không qua Hermes gateway), chỉ deploy ở 1 máy duy nhất
- Khi có nhiều máy cùng dùng 1 token, chuyển 1 instance sang webhook pattern
- Hoặc deploy bot qua Hermes gateway (gateway quản lý 1 instance duy nhất)

## Linked Files

- [ChatBrain full source](references/chat-brain-source.md) — 17KB code, intent detection, templates, follow-up logic
- [ResearchTask.TYPES Sync Error](references/research-type-sync-error.md) — must-add-new-types rule
- [Web Search Resilience](references/web-search-resilience.md) — DDG library replacement, tested engines, prevention, fallback chain pattern
- [Market Research Analyst Pattern](references/market-research-analyst.md) — LLM query optimization + content extraction pattern applied in V4 (lưu ý: skill chính là `market-research-analyst` trong category `research`)

## Web Search Layer — web_research.py

### Architecture

```
search_ddg(query)          # DDGS library (primary, NOT HTML scraping)
  ├─ fail/0 results → _search_bing(query)   # Bing HTML scrape (fallback)
  │    └─ fail/0 results → _search_wikipedia(query)  # Wikipedia API (last resort)
  └─ success → return results[]
```

### Critical: Fallback Chain

DDG changed their HTML layout mid-2026 breaking all regex-based scraping. **`search_ddg()` now uses the `ddgs` library** (pip install ddgs).

- Three-tier fallback: DDGS → Bing → Wikipedia. Bot never sits at 0 sources without trying alternatives.
- Each fallback logs the reason (exception vs 0 results) so you can distinguish rate-limit from content gap.
- `HAVE_DDGS` import guard: if library not installed, skips immediately to Bing instead of crashing.
- On Windows MSYS (git-bash), DDGS context manager reconnects each call (~300-500ms overhead). Ratelimit.py (1 req/2s) prevents rate-limiting.

### Quick Test

```python
from modules.web_research import search_ddg
r = search_ddg('fastrack sân bay nội bài', max_results=5)
print(f'Results: {len(r)}')
```