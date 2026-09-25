# TANO-AGENCY Platform — Full Architecture Reference

## Session: 2026-07-17 Codebase Deep-Dive

## 2 thành phần chính

| Thành Phần | Vị Trí | Mục Đích |
|---|---|---|
| **RIO Bot** | `rio-bot/` | Telegram bot nghiên cứu — chạy riêng, polling riêng |
| **Tano Agency Platform** | `PLATFORM/agent-core/` | Multi-agent OS — 8 phòng ban AI |

---

## 1. RIO Bot (`rio-bot/`)

Polling Telegram bot `@Tano_research_pro_bot`. Modules:
- `cn_trends.py` — Trend Trung Quốc (Douyin, Weibo, Baidu)
- `global_trends.py` — Trend toàn cầu (Google, Reddit, YouTube)
- `deep_research.py` — Research sâu multi-source
- `web_research.py` — Crawl web + summarize
- `video_extract.py` — Extract transcript + metadata từ video URL
- `report_gen.py` — Generate report từ research data
- `analytics.py` — Phân tích dữ liệu thị trường
- `brain.py` / `chat_brain.py` — Logic xử lý intent, routing tin nhắn
- `memory.py` / `validator.py` / `ratelimit.py` — Core utilities (riêng)

Bot chạy qua: `rio_bot.py` (935 lines, 10 commands, long-polling).

## 2. Agent-Core Platform (`PLATFORM/agent-core/`)

### Core Engine (`core/`)

| File | Dòng | Chức năng chính |
|---|---|---|
| `brain.py` | 281 | AgentBrain — state machine 7 stage, hook-driven, default implementations |
| `spec.py` | 200 | AgentSpec + Task + VerificationLoop + chunk_report |
| `harness.py` | 161 | Harness loop: budget, cost-cap, diminishing, human gate, retry |
| `memory.py` | 265 | AgentMemory SQLite: 5 bảng, auto-schema versioning |
| `registry.py` | 53 | AdapterRegistry: inject tool callable by name |
| `llm.py` | 192 | Multi-provider chain: DeepSeek → OpenRouter → Gemini |
| `validator.py` | 177 | Sanitize, Fact Rating (✅🟡🔄🟠❓), Anti-hallucination |
| `ratelimit.py` | 187 | TokenBucket, ExponentialBackoff, CallCache, ThrottledCaller |

### 8 Agents — Spec Overview

| Agent | Icon | Task Types | Key Verify Rules |
|---|---|---|---|
| **CEO** | 👔 | intake, delegate, track, report | has_goal, has_scope, has_assignment, has_priority, has_summary |
| **Dev** | 💻 | build, review, fix, deploy, infra, handover | has_plan, has_test, has_findings, has_rootcause, has_checklist, has_runbook |
| **Sales** | 🎯 | lead, account, qualify, outreach, pipeline | has_contact, min_sources_2, bant (budget/authority/need/timeline), has_cta |
| **Marketing** | 📢 | content, seo, campaign, social, trend | has_headline, has_cta, has_keywords, has_plan, has_schedule, min_sources_2 |
| **Operations** | ⚙️ | takeover, healthcheck, incident, runbook, order, schedule, automate, monitor, inventory | has_checklist, has_verdict, has_status, has_severity, has_action, has_steps, has_signal |
| **Support** | 🎧 | reply, faq, ticket, escalate, sentiment | has_greeting, has_resolution, has_answer, has_priority, has_context |
| **Analytics** | 📊 | report, kpi, dashboard, anomaly, forecast | has_metric, require_rating, has_kpi, has_widgets, has_anomaly, has_forecast |
| **Media** | 🎨 | design, image, video, resize, asset | has_spec, has_brand, has_prompt, has_script, has_format, has_sizes, has_list |

### Adapter Injection Pattern

Mỗi agent có `build_registry(**live)` — gọi `build_registry(search=my_real_fn)` để thay stub bằng tool thật.

**Mặc định = stub chạy được ngay.** Các stub đều trả về mẫu có chú thích _"Cắm <tool> để chạy thật."_

**LLM adapter pattern:**
```python
reg.register("writer", live.get("writer") or llm.make_analyzer(
    "Mày là content writer Việt Nam...",
    fallback=_writer  # rule-based fallback nếu LLM không available
))
```

### CEO Dispatch Mechanism

CEO adapters sử dụng:
- `_team()` — lazy-import AGENTS registry → report departments
- `_taskboard()` — kv_store 'assignments' của ceo memory
- `_clarifier()` / `_planner()` / `_reporter()` — LLM-first, fallback rule-based
- `_dispatch()` — parse bảng phân công markdown → ghi vào taskboard
- `run_assignments()` — loop taskboard pending → `get_brain(dept).run(ttype, task)` → ghi kết quả

Keyword matching cho phân loại việc (DEPT_KEYWORDS trong CEO adapters.py):
8 department với keywords riêng + mặc định "research" nếu không match.

### Human Gate

```python
HUMAN_GATE = {
    ("sales", "outreach"), ("support", "reply"), ("support", "escalate"),
    ("marketing", "social"), ("marketing", "content"),
    ("dev", "deploy"), ("media", "video"), ("media", "design"),
}
```
Output gắn 🔒 đầu tiên: `"🔒 **CHỜ CHỦ TỊCH DUYỆT** — output loại này không tự gửi ra ngoài."`

### Project Layer

`projects/__init__.py` — `load_project(name)`:
1. Import `projects.<name>.project`
2. Đọc AGENTS_USED, BRIEF, live_adapters, SPEC_OVERRIDES
3. Deep-copy spec → overlay overrides → tạo AgentBrain riêng với memory riêng

ABTRIP project mẫu: travel tech, AGT cấp 1, support+ops+sales+dev+analytics.

### LLM Routing

Provider chain: DeepSeek trực tiếp → OpenRouter/DeepSeek → OpenRouter/Gemini.

**Cheap tasks** (classify, format, lookup, summarize, extract, translate) + input < 5000 chars → model rẻ (deepseek-chat cả smart lẫn cheap).

**Context pruning:** `llm.prune(text, 4000)` — giữ đầu + cuối, bỏ giữa.

### Memory Schema (SQLite)

5 bảng:
- `task_history` — UNIQUE(agent, ttype, topic)
- `evidence_cache` — UNIQUE(url), TTL 24h
- `source_scores` — domain ELO score (thành công +0.1, fail -0.3)
- `lessons` — agent + lesson + severity
- `kv_store` — UNIQUE(agent, key) — JSON value cho state tùy chỉnh

Mỗi agent 1 file DB mặc định (`<agent>_memory.db` trong `data/`). Override qua `AGENT_CORE_DATA` env.

## Các tool thật cần cắm (hiện đang stub)

| Agent | Stub Adapter | Tool Thật Gợi Ý |
|---|---|---|
| Tất cả | search | RIO web_research / WebSearch MCP |
| Sales | lead_search | vpai / nimble / sales-account-research |
| Sales/Marketing | crm | HubSpot MCP / carta-crm |
| Marketing | seo | searchfit-seo / nimble:seo-intel / Ahrefs MCP |
| Marketing | social | Postiz MCP |
| Marketing | publish | Postiz MCP |
| Marketing | trends | brightdata:brand-listening |
| Support | reply_out | Telegram/Zalo MCP |
| Support | kb | Guru / Intercom MCP |
| Operations | db | Supabase / Airtable MCP |
| Operations | infra | SSH VPS / Docker CLI |
| Operations | alert_out | Telegram/Slack MCP |
| Analytics | sql | Supabase / data:write-query |
| Analytics | viz | data:build-dashboard |
| Media | render | Canva export / ffmpeg |
| Media | designer | Canva MCP generate-design |
| Media | footage | Pexels / Pixabay API |
| Dev | repo | GitHub MCP / desktop-commander |
| Dev | ship | CI/CD script |

## Kích thước codebase (PLATFORM/agent-core/ chỉ)

~2000 lines Python, zero external dependencies (stdlib only: sqlite3, json, urllib, re, html.parser, difflib, hashlib, threading, time, os).
