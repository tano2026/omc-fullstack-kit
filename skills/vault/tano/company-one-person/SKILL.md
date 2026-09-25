---
name: company-one-person
description: Full pipeline + architecture cho công ty 1 người với 9 AI agent (CEO/Dev/Sales/Marketing/Ops/Support/Analytics/Media/Research), Telegram điều khiển, tool thật $0 (DDGS+PowerShell+SQLite+git).
---

# Công Ty 1 Người — 9 AI Agent (v5 — Full Tools + Embedded ECC Skills + Skill Organization)

## Kiến trúc (v5.1 — Full Real Tools + English Channel + Media nâng cấp)

```
Web Dashboard (uvicorn :8137)  ←  mobile-first, 5 tabs SPA (v3, 19/07/2026) + click-to-detail modals + web chat CEO + auto backup D:\Backups\
    │
    ▼
CEO (trợ lý LLM) → intake → plan → HỎI chủ tịch → dispatch
    │
    ├─ 💻 Dev      (code thật: tạo file + terminal + TDD)
    ├─ 🎨 Media    (image gen: FAL cho GMSP / Pollinations cho Airfare Decoded + HyperFrames CLI + Edge TTS Anh/Việt auto-detect)
    ├─ 🔍 Research (web_search Hermes + multi-query niche)
    ├─ 🛒 Sales    (DuckDuckGo lead search)
    ├─ 📢 Marketing(brand-voice + content-engine ECC)
    ├─ ⚙️ Ops      (PowerShell real healthcheck)
    ├─ 🎫 Support  (SQLite ticket + knowledge-ops)
    ├─ 📊 Analytics(SQL query + CSV export)
    └─ 🤖 Auto-Learn (self-learning engine)
```

```
Web Dashboard (uvicorn :8137)  ←  mobile-first, 7 tabs (Chat/Health/Kanban/Tickets/Outbox/Agents/Văn Phòng)

## Cronjob tự động (Hermes scheduler) — 7 jobs (updated 18/07/2026)

| Cronjob | Schedule | Script | Chức năng |
|---------|----------|--------|-----------|
| Auto Dispatch | every 30m | `cron_dispatch.py` | Quét Kanban, dispatch task `ready` → agents, move card qua `running` → `review` / `blocked` |
| Telegram Delivery | every 15m | `cron_telegram.py` | Quét `outbox.json`, gửi pending items lên Telegram API |
| Morning Briefing | 0 8 * * * | `cron_morning.py` | CEO tóm tắt sáng: taskboard + 5 dự án — ghi outbox → cron Telegram gửi |
| Afternoon Briefing | 0 17 * * * | `cron_afternoon.py` | CEO tổng kết chiều: xong/dang dở/checklist — ghi outbox → cron Telegram gửi |
| Skill Sync | 0 9 * * * | `sync-skills.sh` | Push local skills → GitHub (mirror) |
| Auto Learn | */30 * * * * | `auto-learn.py` | Self-learning engine (correction/error/repetition/workflow patterns) |
| Daily Backup | 0 3 * * * | `backup.py` (no_agent) | Sao lưu DB + config + code → D:\\Backups\\TANO-AGENCY\\, giữ 7 ngày |

Scripts đặt trong `~/.hermes/scripts/` (Hermes yêu cầu path relative).
Telegram delivery cần `TELEGRAM_BOT_TOKEN` + `TELEGRAM_CHAT_ID` trong `.env` của `agent-core/.env`.

**Cron path pitfall:** không dùng `Path(__file__).parent` trong Hermes cron context. Fix:
```python
AGENT_DIR = Path.home() / "AppData" / "Local" / "hermes" / "scripts"
AGENT_CORE = Path("D:/MMO Du an/TANO-AGENCY/PLATFORM/agent-core")
sys.path.insert(0, str(AGENT_CORE))
```

**Note:** Các script báo cáo ghi vào `~/.hermes/outbox/` → cron Telegram mỗi 15p gửi lên API — không gọi Telegram API trực tiếp từ script (ko có Hermes tool context).

## Não
- **LLM**: DeepSeek (chính) → OpenRouter → Gemini (fallback)
- **Tay chân**: `real_adapters.py` — tự động inject khi gọi `get_brain()`
- **Memory**: SQLite (`core/memory.py`) — tasks, evidence_cache, domain_scores, lessons, kv_store
- **Harness**: `core/harness.py` — budget, retry, human gate

## Thư mục

```
TANO-AGENCY/
  PLATFORM/agent-core/
    run.py                    # CLI smoke test: --stub / --real
    main.py                   # Telegram command center
    real_adapters.py           # Tool thật cho 8 agent ($0)
    .env                      # DeepSeek + OpenRouter + Gemini keys
    core/
      brain.py                # AgentBrain pipeline
      harness.py              # Budget + gate
      memory.py               # SQLite memory
      llm.py                  # Multi-provider router
      validator.py            # Rating system + anti-hallucination
      ratelimit.py            # TokenBucket + backoff
    agents/
      __init__.py             # get_brain() auto-injects real adapters
      ceo/                    # Dispatch agent
      dev/                    # Code + infra agent
      sales/                  # Lead search
      marketing/              # Content + publish
      operations/             # Takeover + incident
      support/                # Reply + ticket
      analytics/              # Report
      media/                  # Video + design
      research/               # Research Officer (agent thứ 9, dùng ddgs library)
```

## Cronjob tự động (Hermes scheduler)

| Cronjob | Schedule | Chức năng |
|---------|----------|-----------|
| Auto Dispatch | every 30m | Quét Kanban, dispatch task `ready` → agents, move card qua `running` → `review` / `blocked` |
| Telegram Delivery | every 15m | Quét `outbox.json`, gửi pending items lên Telegram API |
| Morning Briefing | 0 8 * * * | CEO tóm tắt sáng: taskboard + 4 dự án |
| Afternoon Briefing | 0 17 * * * | CEO tổng kết chiều: xong/dang dở/checklist |
| Skill Sync | 0 9 * * * | Push local skills → GitHub (mirror) |
| Auto Learn | */30 * * * * | Self-learning engine (correction/error/repetition/workflow patterns) |

Scripts đặt trong `~/.hermes/scripts/`. Telegram delivery cần `TELEGRAM_BOT_TOKEN` + `TELEGRAM_CHAT_ID` trong `.env`.

**Cron path pitfall:** không dùng `Path(__file__).parent` trong Hermes cron. Fix hardcode path `D:/MMO Du an/TANO-AGENCY/PLATFORM/agent-core`.

**Note:** Các script báo cáo sáng/chiều ghi vào `~/.hermes/outbox/` → cron Telegram mỗi 15p gửi lên API. Script `no_agent=True` nên ko thể gọi `hermes_tools.send_message()` — phải dùng outbox 2-step.

**Lưu ý:** `TELEGRAM_CHAT_ID` trong `.env` phải được set, nếu không cron Telegram bỏ qua. Giá trị: `762010475` (chat ID của user từ @userinfobot).

## Disk C constraint
**Ổ C rất hạn chế (171GB, thường 0-14GB free).** Luôn ưu tiên cài đặt mọi thứ sang ổ D:
- Hermes venv: D:\\ (đã có)
- Pip cache: set `pip config set global.cache-dir D:/pip-cache`
- TEMP: set env `TEMP=D:\Temp` và `TMP=D:\Temp`
- Các tools cache (.gemini, .cursor, .vscode): dọn định kỳ
- Docker images: chưa dùng — nếu dùng thì cài trên D

**Biggest C: cleaners (19/07/2026):**
- `.gemini` — 6.8GB (xoá an toàn)
- `.cursor` Cache — 2.1GB (xoá an toàn)
- `.vscode` extensions — 1.9GB (cài lại được)
- `.cache` — 1GB (cache pip/hermes/uv)
- `AppData\Local\Temp` — 2.6GB

**Clean script mẫu:** `scripts/deep_clean.ps1` — xoá .gemini, .cursor cache, .vscode extensions, npm cache, TEMP

| ECC Skill | Agent | Phương pháp | File | Chi tiết |
|-----------|-------|-------------|------|----------|
| **brand-voice** | Marketing | Prompt embedding | `agents/marketing/adapters.py` | Brand color #0D0D12+#FFD700+#8B0000, tone gai góc, formula truth→hidden→urgency |
| **content-engine** | Marketing | Code embedding | `real_adapters.py` | 1 source → multi-platform pipeline + quality gate |
| **knowledge-ops** | Support, Analytics | Code embedding | `real_adapters.py` | 6-layer: GitHub→Memory→MCP→KB→External→Archive |
| **verification-loop** | Dev | Code embedding | `real_adapters.py` | 6 phase: build→type→lint→test→security→diff |
| **team-orchestration** | CEO | Code embedding | `real_adapters.py` | SQLite Kanban: backlog→ready→running→review→blocked→merged→archived |
| **python-testing** | Dev | Prompt embedding | `agents/dev/adapters.py` | TDD: test trước code, mock external deps, edge cases |
| **security-review** | Dev | Prompt embedding + Code | `agents/dev/adapters.py` | Checklist: secrets exposure, input validation, path traversal, SQL injection, resource exhaustion. Nhúng vào 3-layer guard (budget → file I/O → terminal). |
| **fal-ai-media** | Media | Prompt embedding | `agents/media/adapters.py` | Image prompt tiếng Anh chuẩn FAL format |
| **git-workflow** | Dev | Prompt embedding | `agents/dev/adapters.py` | Conventional commits, branch naming feat/fix |

**Phương pháp:**
- **Prompt embedding:** skill pattern/directive → nhúng vào `llm.make_analyzer(system_prompt=...)` — không cần code mới
- **Code embedding:** skill có workflow actionable → viết function Python trong `real_adapters.py`

**Skill đã review không nhúng:** `ecc-autonomous-loops` (đã có brain.run + budget), `ecc-token-budget-advisor` (cho Hermes), `ecc-deep-research` (cần Exa/Firecrawl trả phí), `ecc-lead-intelligence` (cần X API), `ecc-social-publisher` (cần SocialClaw).

Chi tiết: `references/ecc-skill-embedding-map.md`

## Skill Organization (tách Hermes generic vs dự án)

Cấu trúc thư mục skills sau khi dọn dẹp (Jul 2026):

```
skills/
├── 📁 tano/              ← 140 skills dự án của user
│   ├── company-one-person/  (skill này)
│   ├── tuvi/                (Tử Vi)
│   ├── hyperframes/         (Content Pipeline)
│   ├── gmsp-video-production/
│   └── ...                  (HyperFrames, kế toán, marketing, coding rules, v.v.)
├── 📁 ecc-*/              ← 270 ECC generic skills (Hermes ecosystem)
│   ├── ecc-brand-voice/
│   ├── ecc-python-testing/
│   ├── ecc-fal-ai-media/
│   └── ...
├── 📁 agent-skills/       (generic)
├── 📁 analytics/          (generic)
└── ...

Phân loại: skills dự án = có frontmatter + nội dung liên quan tới business của user.
ECC = skills từ kho cộng đồng, giữ nguyên tên, ko move vào tano/.
```

**Nguyên tắc:**
- Skill nào user từng dùng hoặc do Hermes sinh ra trong quá trình build dự án → `tano/`
- Skill nào có tiền tố `ecc-` hoặc generic pattern → giữ nguyên root
- Khi dùng: load bằng `skill_view("tano/<tên>")` hoặc `skill_view("ecc-<tên>")`

1. **Load skill** — `skill_view("ecc-<tên>")` đọc SKILL.md
2. **Phân loại**:
   - Skill pattern/directive (vd: brand-voice, content-engine) → viết hàm mới trong `real_adapters.py`
   - Skill code/infra (vd: mcp-server-patterns, dashboard-builder) → cài CLI/MCP + config
3. **Map pattern → code**:
   - `When to Activate` → xác định agent nào cần
   - Hard bans / quality gates → code vào hàm (regex check, rule list)
   - Workflow steps → không copy verbatim, tóm thành logic function
   - Output contract → dùng làm schema response
4. **Inject vào registry** — `build_real_registry()` thêm {tên: callable}
5. **Smoke test** — `python run.py --real` (phải 13/13 pass)
6. **Update skill** — lưu skill reference vào SKILL.md

### Pitfalls khi cắm skill

| Vấn đề | Giải pháp |
|--------|-----------|
| Skill từ kho là markdown, không phải code | Phải tự viết function mapping. Không copy-paste markdown vào code. |
| Skill tưởng free nhưng cần API key trả phí | Kiểm tra required_environment_variables + required_credentials trước. Exa/Firecrawl/SocialClaw đều trả tiền — tránh. |
| Skill có references/scripts nhưng không kèm file | skill_view kiểm tra linked_files — nếu null thì skill chỉ có pattern, không có code sẵn. |
| Nhiều skill overlap | brand-voice x content-engine (brand-voice là canonical voice layer). knowledge-ops x kb_search (knowledge-ops thay thế kb_search cũ). |
| Agent không nhận ra adapter mới | Phải thêm tên adapter vào SEARCH_LIKE set trong core/brain.py, nếu không brain sẽ bỏ qua COLLECT phase. |
| `_agent_kanban` cần DB riêng | Tạo _ensure_kanban_db() tách biệt khỏi AgentMemory — không lẫn với memory của agent khác. |
| `_kb_ingest` có thể tạo duplicate | Luôn check dedup trước khi store — dùng AgentMemory.retrieve_lessons() so sánh prefix 100 chars. |
| **Adapter registry ≠ spec task_types** | Adding `reg.register("initiative", ...)` is NOT enough. Must also add the task type to `SPEC.task_types` in `spec.py` — otherwise `brain.run('initiative', ...)` returns "không hỗ trợ task type". The `"analyze"` field in spec must match the registry name. |

### Agent Kanban commands

```python
from real_adapters import _agent_kanban

# Thêm card
_agent_kanban(task, action='add', title='Build feature X', owner='dev', state='ready')

# Move card
_agent_kanban(task, card_id='agent-card-abc123', action='move', to_state='running')

# Ghi handoff note
_agent_kanban(task, card_id='agent-card-abc123', action='handoff', note='Tests pass, ready for review')

# Xem board (mặc định)
_agent_kanban(task)
```

Columns: backlog → ready → running → review → blocked → merged → archived

Mỗi card có: id, title, owner, state, branch, worktree, acceptance, merge_gate, handoff, evidence.

### Knowledge Ops layers

| Layer | Tên | Implementation | Use case |
|-------|-----|---------------|----------|
| 1 | GitHub/Linear | (manual) | Active execution truth |
| 2 | AgentMemory | `core/memory.py` lessons + kv_store | Cross-session quick access ✅ |
| 3 | MCP Memory Graph | MCP server entities/relations | Semantic search |
| 4 | KB repo | File search `.md`/`.txt`/`.json` | Durable document store ✅ |
| 5 | External DB | Supabase/PostgreSQL | Large doc search |
| 6 | Local archive | `data/` folder | Human-facing notes ✅ |

Dùng `_kb_ingest()` để auto classify/dedup/store. Dùng `_kb_search_v2()` để multi-layer retrieval.

## CEO v2 — Trợ lý thông minh (LLM-powered)

CEO được nâng cấp từ rule-based lên LLM-powered. 6 adapter chính:

| Adapter | LLM | Fallback | Mô tả |
|---------|-----|----------|-------|
| `clarifier` | DeepSeek | `_fallback_intake()` | Phân tích mệnh lệnh: mục tiêu, phạm vi, phòng ban, deadline, câu hỏi làm rõ |
| `planner` | DeepSeek | `_fallback_planner()` | Phân rã nhiệm vụ — output tự nhiên, KO format bảng corporate (đã bỏ JSON parsing tháng 7/2026). Nói như trò chuyện, không icon |
| `reporter` | DeepSeek (summarize) | `_ceo_reporter()` | Executive brief từ taskboard: tiến độ, điểm nổi bật, vướng mắc, đề xuất |
| `dispatch` | — (code) | — | Ghi taskboard → auto gọi brain.run() từng phòng ban (ThreadPoolExecutor + 90s timeout) |
| `taskboard` | — (code) | — | SQLite kv_store 'assignments' — mission group, trạng thái, kết quả |
| `initiative` | DeepSeek | `_ceo_initiative()` | Chủ động gợi ý dự án đang làm dở + kickstart |

**Không cần format cứng.** Nói tiếng Việt bất kỳ:
- "ra mắt dịch vụ Fast Track tháng sau"
- "kiểm tra sức khoẻ hệ thống"
- "viết content về AI du lịch"

**Luồng chat — CEO xác nhận trước, dispatch sau:**
```
User: "làm landing page Fast Track"
  → CEO intake: LLM phân tích → JSON
  → CEO delegate: LLM lập kế hoạch → JSON bảng phân công
  → CEO track: đọc taskboard cũ
  → CEO DỪNG — HỎI Chủ tịch xác nhận
     (KHÔNG dispatch tự động)

User: "ok" / "làm đi" / bấm nút [✅ Duyệt — Triển khai]
  → CEO dispatch: ghi taskboard + gọi brain.run() cho từng phòng ban
```

**Confirm keywords (dashboard detect):** ok, làm, làm đi, triển khai, đồng ý, ừ, go, duyệt, chạy, dispatch

**QUAN TRỌNG:** CEO KHÔNG được tự động dispatch. Luôn trình plan → chờ confirm → mới chạy.
Code confirm logic ở `web/dashboard.py` — endpoint `/api/chat` kiểm tra message có match confirm keywords không, dispatch_results chỉ populate khi is_confirm=True. Frontend hiển thị nút "✅ Duyệt — Triển khai" khi `data.needs_confirm === true`.

**File:** `agents/ceo/adapters.py` (21KB)
**File:** `web/dashboard.py` — `/api/chat` endpoint chứa confirm logic

## Web Dashboard (mobile-first) — v5 Single-Screen SAAS (19/07/2026, redesign)
**IMPORTANT:** The dashboard was COMPLETELY REDESIGNED on 19/07/2026. No more tabs. Single-screen layout.

### Single-screen architecture (v5, 19/07/2026)

```
┌───────────────────────────────────┐
│ TANO.AGENCY  📁5/5  📋3/10  🟢OK │ Header: tình hình chung
├────┬──────────────────────────────┤
│    │ 📋 Công việc                  │
│ 👔 │ ┌──────────────────────────┐ │
│ 💻 │ │ 💻 Landing Page GMSP    │ │ ← Bấm → modal: chi tiết + chat inline
│ 🎯 │ │   Developer · 2h      🟢 │ │
│ 📢 │ ├──────────────────────────┤ │
│ ⚙️ │ │ 🎯 KPI tháng 7         │ │
│ 🎧 │ │   Sales · 1ng        🟡 │ │
│ 📊 │ └──────────────────────────┘ │
│ 🎨 │                              │
│ 🔬 │ ┌──────────────────────────┐ │
│ 🏠 │ │ 💬 Chat CEO              │ │ ← Chat bar cố định (luôn visible)
│    │ └──────────────────────────┘ │
│    │     [📋] [📊] [🏛️]         │ ← Quick tools (Giao việc/Báo cáo/Họp)
└────┴──────────────────────────────┘
```

| Component | What | API |
|-----------|------|-----|
| **Header** | Project count, task count, health dot | /api/projects, /api/kanban |
| **Sidebar** | 9 agents + "Tất cả" — click to filter tasks | Filter client-side |
| **Feed** | Task cards sorted by priority (running > ready > review > blocked > backlog > done). Each card shows: agent icon + title + owner + time ago + state badge. Click → modal. | /api/kanban |
| **Chat bar** | Fixed at bottom. Enter to send. CEO responds via /api/chat with project context. | POST /api/chat |
| **Quick tools** | 📋 Giao việc mới (modal: title + phòng ban + priority) | POST /api/kanban/add |
| | 📊 Báo cáo nhanh (system health + task stats + projects) | /api/health, /api/kanban_summary |
| | 🏛️ Họp (shortcut: gửi "/ceo họp khẩn") | POST /api/chat |

### Task Modal (click any task card)
- Tiêu đề + agent icon + màu sắc
- **State dropdown** — chọn trạng thái mới + nút cập nhật
- Thông tin: created_at, current state
- **Nút 🤝 Giao CEO** — gửi lệnh qua API, hiện toast, ko chuyển tab
- **Nút 💬 Chỉ đạo** — chuyển tab Chat + điền sẵn `/agent_name`
- **💬 Chat CEO inline** — ô chat ngay trong modal, session_id riêng (`task_<id>`), CEO trả lời ngay trong modal

### Giao việc Modal (📋 quick tool)
- Tiêu đề input
- Phòng ban dropdown (9 agents)
- Ưu tiên: "Làm ngay" (ready) / "Để sau" (backlog)
- Nút 🚀 Giao việc → POST /api/kanban/add

### Báo cáo Modal (📊 quick tool)
- Hệ thống: CPU, RAM, Ổ C, Ổ D
- Công việc: tổng/đang chạy/sẵn sàng/bị chặn
- Dự án: 5 items với ✅/❌
- Nút "Yêu cầu CEO báo cáo" → gửi chat `/ceo báo cáo tổng quan`

### Design tokens (light theme — user preference, CONFIRMED 19/07/2026)
```css
:root {
  --bg: #F5F5F7;       /* xám nhạt */
  --card: #FFFFFF;      /* trắng */
  --card-hover: #EBEBF0;
  --border: #D4D4D8;
  --text: #1A1A2E;      /* đen chì */
  --text-muted: #6B6B80;
  --gold: #B8860B;      /* vàng đậm */
  --green: #16A34A;
  --red: #DC2626;
}
```
**⚠️ USER PREFERENCE — LIGHT THEME ONLY.** User explicitly rejected dark theme. Never suggest or offer dark theme. Default confirmed 19/07/2026:
```css
:root {
  --bg: #F5F5F7;       /* xám nhạt */
  --card: #FFFFFF;      /* trắng */
  --card-hover: #EBEBF0;
  --border: #D4D4D8;
  --text: #1A1A2E;      /* đen chì */
  --text-muted: #6B6B80;
  --gold: #B8860B;      /* VÀNG ĐẬM — not #FFD700, not #D4A843 */
  --green: #16A34A;
  --red: #DC2626;
}
```

### Sidebar (left) — confirmed design 19/07/2026
- **180px wide** on desktop, 50px on mobile (<480px)
- **Section titles** visible on desktop: "Phòng ban" / "Chung" / "Dự án" (hidden on mobile)
- Each agent: icon + **full name** (e.g. 👔 CEO, 💻 Developer) — NOT just icon
- "Tất cả" button under "Chung" — gold bg when active
- **"Dự án" section** — auto-populated from `/api/projects` via `updateProjectsSidebar()`. Each project button: icon + name + green/red dot (active/inactive). Click → `openProjectModal(name)` — shows facts, decisions, inline chat.
- Mobile (<480px): collapses to 50px, labels and section titles hidden

### Key interactive patterns
- **30s auto-refresh** — `setInterval(loadAll, 30000)`
- **Toast notifications** — position fixed bottom-100px, fade out 3.5s
- **Modal scrollable** — `.modal { max-height: 85vh; overflow-y: auto; animation: slideUp .25s }`
- **Enter to send** — chat input + modal chat both support Enter key
- **Inline modal chat** — separate session_id per modal instance, CEO remembers context within that modal

### API changes from v4 → v5
New endpoints added:
- `GET /api/memory/facts` — facts by project/category/search
- `POST /api/memory/facts` — add a fact
- `GET /api/memory/decisions` — decisions by project
- `POST /api/memory/decisions` — add a decision
- `GET /api/memory/projects` — list projects with memory
- `GET /api/preferences` — all user preferences
- `POST /api/preferences` — set a preference
- `GET /api/skills` — all skills
- `POST /api/skills` — add a skill

### Port note
Dashboard runs on port **8138** (8137 left in TIME_WAIT by stale process on 19/07/2026). Stick with 8138 — 8137 may become available but switching back is low priority. User accesses via http://localhost:8138.
```python
def run():
    port = 8138  # was 8137, changed due to persistent TIME_WAIT
    uvicorn.run(app, host="0.0.0.0", port=port)
```

### Agent profile modal — 5 MUST sections:
1. 👤 **Tôi là ai** — Vietnamese introduction
2. 🎯 **Nhiệm vụ của tôi** — mission statement
3. 🛠️ **Tôi có gì** — tools as tag chips + skills
4. 📋 **Tôi đang làm gì** — live tasks from /api/kanban filtered by owner
5. 💬 **Chat trực tiếp** — button switches to chat tab and pre-fills "/agent_name "

**Update 19/07/2026 — Mini chat inside modals.** User hated being kicked to chat tab. Now each task and project modal has an inline chat box at the bottom with its own session_id (`modal_<timestamp>`). "Giao CEO" button calls `/api/chat` directly via fetch + shows a toast notification — doesn't switch tabs. "Chỉ đạo trực tiếp" still navigates to chat tab with pre-filled `/agent `.
- Modal chat: `#modal-chat-input` + `#modal-chat-msgs` div + `sendModalChat()` function
- Toast pattern: `document.createElement('div')` positioned `bottom:90px`, fades out after 4s
- `assignToCEO()` posts to `/api/chat` with `session_id='dashboard_assign'`, shows CEO response in toast
- `directChatTask()` stays old flow: close modal → switchTab('chat') → pre-fill input

**Dashboard architecture (v4, 19/07/2026):** Redesigned from 5-tab to 4-tab "Văn Phòng Đại Lý" layout:
- 🏢 VP: 9 agent cards grid. Click → full-page scrollable modal (5 sections)
- 📋 Bảng Tin: Live feed of all non-idle kanban tasks. Click task → detail modal with mini chat + state change
## Project Memory System (new 19/07/2026) — `dashboard/project_memory.py`

**Purpose:** Each project has its own memory — chat history, facts, decisions — so CEO doesn't confuse projects. Skills are shared (cross-project reusable tools).

**⚠️ TELEGRAM CEO RESPONSE: NO "đang nghĩ" MESSAGE.** User explicitly complained about double-message spam. Instead:
- `tg_no_wait("sendChatAction", chat_id=chat_id, action="typing")` — Tele shows "...đang gõ" indicator
- Only send 1 message — the final LLM response
- `tg_no_wait()` helper: fire-and-forget, non-blocking

**Tele session commands (confirmed working 19/07/2026):**
```
/gmsp      → switch to GMSP session
/abtrip    → switch to ABTrip
/airfare   → switch to AirFares Decoded
/tuvi      → switch to Tử Vi
/fasttrack → switch to Fast Track
/thoát     → return to global chat
/new       → reset current session (history still in DB, just clears RAM session)
```
- `_project_sessions[chat_id]` dict persists session per chat
- `/new` does NOT delete history — only pops from session dict
- Fallback: `_detect_project(text)` runs if no active session

### Database: `data/project_memory.db`

| Table | Contents | Key | 
|-------|----------|-----|
| `project_chat` | Per-project chat history | `project` column (name) |
| `global_chat` | Non-project chat | — |
| `facts` | Confirmed knowledge | `project` (or `__global__`), `category`, `confidence` |
| `decisions` | Business decisions made | `project`, `status` |
| `preferences` | User settings (theme, filters...) | `key`/`value` (JSON) |
| `skills` | Cross-project reusable skills | `name`, `category`, `tools` (JSON array) |

### Telegram session commands (NEW 19/07/2026)

```python
_project_sessions = {}  # chat_id -> project name

# Commands in handle():
/gmsp → session switch to GMSP
/abtrip → session switch to ABTrip
/airfare → session switch to AirFares Decoded
/tuvi → session switch to Tử Vi
/fasttrack → session switch to Fast Track
/thoát or /all → return to global chat
```

**Flow:** User gõ `/gmsp` → bot confirm "Đã chuyển sang dự án GMSP" → mọi chat sau đó tự động inject project context. Chỉ cần `/thoát` để quay lại tổng quát.

**Priority:** `_project_sessions.get(chat_id)` > `_detect_project(text)` — nếu đang trong session GMSP, nói "airfare" cũng ko lẫn.

**CEO response style (user preference):**
- KHÔNG gửi "CEO đang nghĩ..." trước — user ghét bị spam 2 tin nhắn
- Dùng `sendChatAction` (typing indicator) thay vì send message tạm — Tele hiện "...đang gõ" mà ko tạo message thật
- Chỉ send 1 tin nhắn duy nhất khi LLM hoàn thành
- `tg_no_wait()` helper: fire-and-forget API call, ko chặn luồng

### Key functions (import from `dashboard.project_memory`)

| Function | Purpose |
|----------|---------|
| `save_chat(project, role, content)` | Save message to correct project table |
| `load_chat_history(project, limit=30)` | Load last N messages for project |
| `add_fact(project, fact, category, confidence, source)` | Store confirmed fact |
| `get_facts(project, category, limit)` | Retrieve facts |
| `search_facts(query, project, limit)` | Search facts by text |
| `add_decision(project, decision, context)` | Record a decision |
| `get_decisions(project, limit)` | Get decisions |
| `set_pref(key, value)` | Save user preference (JSON) |
| `get_pref(key, default)` | Read preference |
| `get_all_prefs()` | All preferences dict |
| `add_skill(name, description, category, tools)` | Add reusable skill |
| `get_skills(category)` | List skills |
| `build_project_context(project)` | Build context string for CEO prompt (facts + decisions + skills) |
| `extract_facts_from_message(project, message, role)` | Auto-extract emails, phones, URLs from messages |

### CEO integration — `/api/chat`

The chat endpoint now accepts `session_type` parameter:
- `"global"` (default) — uses global_chat, no project context
- `"GMSP"` / `"ABTrip"` etc — uses project_chat + injects `build_project_context()` into system prompt

**CEO system prompt now includes:**
1. All available skills (`=== KỸ NĂNG CÓ THỂ DÙNG ===`)
2. Project facts + decisions (`=== DỰ ÁN HIỆN TẠI ===`)
3. Rules to auto-save: `[LƯU FACT: ...] [CATEGORY: ...]` and `[QUYẾT ĐỊNH: ...]`

**Auto-extraction:**
- From user messages: regex for emails, phones, URLs → `add_fact()`
- From CEO responses: parse `[LƯU FACT]` and `[QUYẾT ĐỊNH]` brackets → `add_fact()` / `add_decision()`

### API endpoints

| Endpoint | Method | Params |
|----------|--------|--------|
| `/api/memory/facts` | GET | `?project=GMSP&category=contact&q=search&limit=20` |
| `/api/memory/facts` | POST | `{project, fact, category, confidence, source}` |
| `/api/memory/decisions` | GET | `?project=GMSP&limit=20` |
| `/api/memory/decisions` | POST | `{project, decision, context}` |
| `/api/memory/projects` | GET | Lists projects with memory (facts+decisions+chat counts) |
| `/api/preferences` | GET | All preferences |
| `/api/preferences` | POST | `{key, value}` | Preferences API exists but commonly empty (user never set any). Don't rely on preferences being populated. |
| `/api/skills` | GET | `?category=general` | Skills API exists but commonly empty (0 skills). Don't error if empty — just show "Chưa có kỹ năng nào." |
| `/api/skills` | POST | `{name, description, category, tools[]}` |

### Chat flow (per-project)

```
User: "dự án GMSP có contact gì?"
  → POST /api/chat {message, session_type: "GMSP", session_id: "main_123"}
  → Server builds context: get_facts("GMSP") + get_skills() + load_chat_history("GMSP")
  → DeepSeek receives: [project facts] + [skills] + [last 30 messages]
  → CEO knows it's about GMSP, responds with facts
  → save_chat("GMSP", "user", msg) + save_chat("GMSP", "assistant", response)
  → extract_facts_from_message("GMSP", msg) → auto-save emails/phones
  → Parse CEO response for [LƯU FACT: ...] or [QUYẾT ĐỊNH: ...] → save

User: "còn ABTrip?"  (different session_type: "ABTrip")
  → Same flow, different project context — CEO doesn't confuse
```

**UI Integration:** See `references/project-sidebar-modal.md` for the frontend pattern:
- `session_type: projectName` in inline modal chat
- `openProjectModal()` loads facts + decisions on open
- `projectAddFact()` posts to `/api/memory/facts` via prompt
- Sidebar "Dự án" section shows all projects with active/inactive dots

### Pitfalls
- `project_memory.py` must be importable from `dashboard/` dir → add `sys.path.insert(0, str(BASE / "dashboard"))` before import
- Database path: `DATA / "project_memory.db"` (same DATA dir as other DBs)
- `_extract_bracket()` helper function needed for CEO response parsing

**Critical:** Modal must be `position:fixed; overflow-y:auto; max-height:100vh; overscroll-behavior:contain` — user complained that content wasn't scrollable in the first version.

## Web Dashboard (mobile-first) — 5 tabs (v3 SPA, 19/07/2026)

FastAPI + jinja2.Environment (raw, không dùng Jinja2Templates). Single SPA HTML file, giao diện dark theme (#0D0D12 bg + #FFD700 gold + #006885 teal). Chạy port 8137.

Password: tano2026 (hardcode trong app.py, localStorage trên frontend).

### 5 tabs

| Tab | Mô tả |
|-----|-------|
| 📊 **Tổng Quan** | System health (CPU/RAM/Disk C/D từ PowerShell) + 5 project cards (GMSP/Fast Track/ABTrip/Tử Vi/AirFares Decoded — check filesystem) + kanban/tickets/learning stats + outbox list |
| 👥 **Phòng Ban** | 9 agent cards (👔💻🎯📢⚙️🎧📊🎨🔬) với task count từ memory DBs — click vào mở modal info |
| 🏢 **Văn Phòng** | CEO avatar header + kanban board items + agents grid — auto-refresh 30s |
| 📋 **Tasks** | Kanban board (click→detail modal→state change) + tickets (click→detail modal) + nút "Thêm Card" |
| 💬 **Chat** | Chat với CEO — POST /api/chat, 1 LLM call (giống Telegram bot). **Có nhớ lịch sử trò chuyện qua SQLite** (`data/chat_history.db`) — F5/restart không mất. 20 messages gần nhất được gửi lên LLM. Bubbles: user right (gold), CEO left (card). Loading dots animation. Gửi `session_id` để grouping (dashboard_quick, dashboard_tab). |

### API Endpoints

| Endpoint | Method | Mô tả |
|----------|--------|-------|
| `/` | GET | SPA HTML |
| `/login` | POST | Check password tano2026 (JSON hoặc form) |
| `/api/health` | GET | System stats từ PowerShell (CPU/RAM/Disk/Python processes) |
| `/api/projects` | GET | 5 project dirs (check filesystem): GMSP, Fast Track, ABTrip, Tử Vi, AirFares Decoded |
| `/api/chat` | POST | Chat CEO — gọi `core.llm.chat()` trực tiếp. Nhận {message}, trả {ok, response, time_ms} |
| `/api/kanban_summary` | GET | Count cards by state từ agent_kanban.db |
| `/api/kanban` | GET | All kanban cards |
| `/api/kanban/add` | POST | Thêm card mới |
| `/api/kanban/move` | POST | Move card state (click→modal dropdown) |
| `/api/tickets_summary` | GET | Count tickets by status từ tickets.db |
| `/api/tickets` | GET | All tickets |
| `/api/agents` | GET | 9 agents + task counts từ memory DBs |
| `/api/learning` | GET | observations + instincts từ learning.db |
| `/api/outbox` | GET | Files từ ~/.hermes/outbox/ |
| `/api/file/ls` | GET | `?path=...` — list directory (bounded to `D:\\MMO Du an`) |
| `/api/file/read` | GET | `?path=...&offset=1&limit=200` — read text file (ext whitelist) |
| `/api/file/search` | GET | `?path=...&pattern=...&ext=.md` — find files by name |
| `/api/file/ls` | GET | `?path=D:/MMO Du an` — list directory (security: `_safe_path()` only allows under `D:\\MMO Du an`) |
| `/api/file/read` | GET | `?path=...&offset=1&limit=200` — read text file (whitelisted extensions only) |
| `/api/file/search` | GET | `?path=...&pattern=...&ext=.md` — find files by name |

### Detail Modal System

Từ 18/07 — tất cả các thẻ (kanban, ticket, agent, project) đều có **click handler mở modal chi tiết**:
- **Kanban card** → modal: title, owner, state, description (nếu có), created_at, updated_at + state change dropdown
- **Ticket** → modal: id, title, priority, status, customer, description
- **Agent** → modal: icon, name, task count + link
- **Project** → modal: name, status, filesystem path

Dùng MutationObserver để re-attach click handlers sau mỗi lần reload data (dynamic content).

**Important:** Click → modal detail pattern requires 3 parts in the HTML:
1. **overlay HTML** — `.modal-overlay` div with `.modal-content` + `.modal-close`
2. **CSS** — `.modal-overlay { display: flex/block }`, `.modal-content { ... }`, `.modal-close`
3. **JS** — `document.querySelector('.modal-overlay').classList.add('active')` + `renderModalContent(data)` + close on overlay click

Cards use `data-id` attributes for identification. MutationObserver watches `document.getElementById('tab-content')` for new cards.

### Error handling pattern — Chat

Khi `/api/chat` trả về lỗi, frontend hiển thị trong chat bubble:
- `data.error` → "❌ Lỗi: ..."
- `!data.ok || !data.response` → "⚠️ CEO không phản hồi. Thử lại nhé."
- `fetch exception` → "❌ Lỗi kết nối: ..."

### File structure

```
dashboard/
  app.py           # FastAPI app (~400 lines, 13KB)
  templates/
    dashboard.html  # SPA single-page (~1150 lines, 52KB — CSS+JS inline)
```

### Văn Phòng tab (Situation Room)

Mô phỏng văn phòng: 1 bàn họp phát sáng + CEO avatar ở giữa + 8 agent card 2 cột.
Mỗi agent có trạng thái realtime qua CSS class — ring xoay khi running, shake avatar, glow pulse vàng.
JS fetch `/api/kanban` + `/api/agents`, auto-refresh 15s.
Chi tiết CSS class names: `.running`, `.done`, `.blocked`, `.agent-ring`, `@keyframes ring-rotate`, `@keyframes avatar-shake`.

### Critical: Sync checklist when adding NEW project (e.g. Airfare Decoded)

Khi thêm dự án mới, patch CẢ 7 chỗ này — quên 1 chỗ là CEO không biết dự án hoặc dashboard hiển thị sai:

1. **CLIENTS/<PROJECT>/SKILL.md** — pipeline + brand + rules
2. **Media adapter** (`agents/media/adapters.py`) — thêm tools + update `video_pipeline` analyzer
3. **Dev adapter** (`agents/dev/adapters.py`) — thêm keyword→path vào `project_map`
4. **CEO system prompt** (`main.py` `cmd_natural` system string) — thêm vào "5 DỰ ÁN HIỆN TẠI:" section
5. **CEO adapter** (`agents/ceo/adapters.py`) — thêm vào `COMPANY_PROJECTS` dict
6. **Dashboard API** (`dashboard/app.py`) — thêm project entry vào `api_projects()` endpoint (Path check + project dict)
7. **Dashboard JS** (`dashboard/templates/dashboard.html`) — thêm icon+label vào `PROJ_ICONS` và `PROJ_LABELS` constants

**Dashboard deploy pitfall:** sau khi sửa `app.py`, `__pycache__` giữ code cũ. Process mới `python dashboard/app.py` dùng `.pyc` cũ → không thấy thay đổi (ví dụ: API trả về 4 projects dù code có 5). 

Fix: 
1. Xoá toàn bộ `__pycache__` trong agent-core tree. Dùng Python script:
   ```python
   import shutil, os; root = "D:/MMO Du an/TANO-AGENCY/PLATFORM/agent-core"
   [shutil.rmtree(os.path.join(d,'__pycache__')) for d,dirs,_ in os.walk(root) if '__pycache__' in dirs]
   ```
2. Kill ALL old Python processes đang giữ port 8137 — không chỉ PID mới. Process cũ (PID 34520) vẫn LISTENING dù đã kill "tất cả". Dùng:
   ```bash
   netstat -ano | grep 8137   # tìm LISTENING PID
   taskkill /F /PID <PID>     # kill đúng PID đó
   ```
3. Verify port free: `netstat -ano | grep 8137` → ko còn LISTENING
4. Restart dashboard: `python dashboard/app.py`

**Double-kill pattern:** git-bash taskkill thường fail với lỗi "Invalid argument". Dùng: `cmd.exe /c "taskkill /F /PID <PID>"` hoặc `powershell Stop-Process -Id <PID> -Force` qua write_file script.

**Triple-verify:** process mới ≠ process thật. Luôn check `netstat -ano | grep 8137` sau khi restart + `curl http://localhost:8137/api/projects` để confirm code mới.

1. **CLIENTS/<PROJECT>/SKILL.md** — pipeline + brand + rules
2. **Media adapter** (`agents/media/adapters.py`) — thêm tools + update `video_pipeline` analyzer
3. **Dev adapter** (`agents/dev/adapters.py`) — thêm keyword→path vào `project_map`
4. **CEO system prompt** (`main.py` `cmd_natural` system string) — thêm vào "5 DỰ ÁN HIỆN TẠI:" section
5. **CEO adapter** (`agents/ceo/adapters.py`) — thêm vào `COMPANY_PROJECTS` dict

**Pitfalls:**
- `main.py` `cmd_natural` system prompt dùng Python string concatenation — `\n` phải viết là `\\n` (double escape) vì nó là literal string trong source code. Nếu dùng `patch` tool với old_string/new_string chứa `\\`, tool có thể double-escape lại thành `\\\\`. Luôn verify sau patch bằng cách đọc lại file dòng 111-132.
- `agents/ceo/adapters.py` `_ceo_initiative()` dùng `COMPANY_PROJECTS` dict — chỉ cần thêm entry, không cần sửa prompt não của CEO vì nó đọc từ dict runtime.
- **planner adapter** (`plugins/adapters/planner.py`) đã bị xóa (format corporate), không tồn tại trên disk nữa. `main.py` `cmd_natural` là entry point duy nhất cho chat CEO.

## Công ty: 5 trụ cột chính (updated 18/07/2026)

Đăng ký trong CEO adapters (COMPANY_PROJECTS dict):

| # | Dự án | Phòng ban | Mô tả | Trạng thái |
|---|-------|-----------|-------|------------|
| 1 | **GMSP** | research, marketing, media, video | Pipeline video content (Tử Vi, PTBT, Cổ Kim). Đã gộp Giải Mã Số Phận vào pipeline. 7-stage: Research→Script→TTS→Media→Render→Publish→Social. EP01 done, EP02 script. | ✅ active |
| 2 | **ABTrip (Smart Agent)** | dev, ticketing, operations, sales | Đặt vé máy bay + dịch vụ du lịch. **Brand mới: Smart Agent** (Travel Tech Hybrid). Mô hình "bán cần câu" — bán giải pháp phòng vé mini cho CTV. 3 gói: CTV Cơ bản (free) → Đại Lý Pro (199K/tháng) → White-label (1.5tr/tháng). Đối thủ cạnh tranh: AI Travel (Layla, Wander AI, Mindtrip, Roam Around — zero overlap ngách CTV). Cơ hội: 12-18 tháng. Hướng build-to-flip: Hybrid (ưu tiên). Gồm: AGT API, Flight MCP, Fast Track Nội Bài (An Bình), Lounge, eSIM (IST1). Chat LLM UI mobile-first. Backend FastAPI port 8138, Frontend Next.js 14 port 4321. | ✅ active |
| 3 | **An Bình Fast Track** | dev, marketing, media, sales | Fast Track + VIP B + Lounge Nội Bài — đơn vị duy nhất có onsite staff 24/7. Landing page + OTA listing + hotel/DMC partnership. Teal #006885 + gold #DBA011. Đang đổi tên do quy định Nội Bài. | ✅ active |
| 4 | **Tử Vi** | dev, research | Tử Vi Đẩu Số platform — iztro + MCP + Python engine. Đã train + agent v3.0. | ✅ active |
5. **Airfare Decoded** (English Channel) | media, research, marketing | Kênh YouTube English faceless — stick-figure explainer về insider kiến thức vé máy bay. Pipeline: HyperFrames + Pollinations + Edge TTS AndrewNeural. 2 video/tuần. Variation guard (≥3/5 trục khác video trước). | ✅ active (setup 18/07) |

## Onboarding Client Mới — SOP (Standard Operating Procedure)

Khi kickstart dự án mới (VD: Airfare Decoded), cần patch 4 chỗ:

1. **CLIENTS/<PROJECT>/SKILL.md** — pipeline, brand, design tokens, key files, skill references, hard rules
2. **Media adapter** (`agents/media/adapters.py`) — thêm tools mới (`_tool_hyperframes`, `_tool_pollinations`), update `_real_image_gen()` auto-detect context, update `video_pipeline` analyzer prompt, register tools + set workdir constant trong `build_registry()`
3. **Dev adapter** (`agents/dev/adapters.py`) — thêm keyword→path vào `project_map`
4. **CEO adapter** (`agents/ceo/adapters.py`) — thêm vào `COMPANY_PROJECTS` + update intake system prompt list

**Verify:** `python -c "import ast; ast.parse(open('...').read()); print('✅ syntax OK')"` mỗi file + test CEO biết dự án mới.

**Provider fallback rule:** Luôn document alternative providers trong SKILL.md. VD: ElevenLabs cần trả tiền → Edge TTS fallback. Edge TTS AndrewNeural cho English, NamMinhNeural cho Việt.

**Lưu ý:** Dự án số 5 là **English channel**

### CLIENTS/ import pattern

Khi import project mới vào TANO-AGENCY:
1. Tạo `TANO-AGENCY/CLIENTS/<PROJECT>/` folder
2. Viết `SKILL.md` — pipeline + brand + config + skill references từ toolkit
3. Viết supporting docs (architecture, database, roadmap)
4. Link skills từ AI-Vibe-Toolkit qua section "Agent Skills (load from AI-Vibe-Toolkit)"
5. Update `PROJECT-MAP.md` ở TANO-AGENCY/ root — ánh xạ thư mục

**Toolkit skill linking:** không copy skill .md vào CLIENTS/ — chỉ reference bằng tên + description. Agent dùng `skill_view()` để load từ toolkit khi cần.

Ví dụ GMSP import:
```
CLIENTS/GMSP/
├── SKILL.md                ← Pipeline 7-stage + brand + render config
└── gmsp-content-engine.md  ← Skill reference
```

Ví dụ ABTrip import:
```
CLIENTS/ABTRIP/
├── ABTRIP.md               ← Overview + status
├── SKILL.md                ← Ticketing + Fast Track + eSIM
├── ABTRIP-ARCHITECTURE.md
├── ABTRIP-DATABASE.md
├── ABTRIP-ROADMAP.md
└── sub-services/
    └── fast-track.md
```

Ví dụ Airfare Decoded import:
```
CLIENTS/AIRFARE-DECODED/
└── SKILL.md                ← Pipeline 6 scene + brand + variation guard + HyperFrames config + agent skills
```
**Lưu ý:** Airfare Decoded khác GMSP — không có 7-stage pipeline, thay bằng HyperFrames compose→render workflow.
Brand tokens: ink #111111, paper #fdfdfb, accent #d92b2b, display font Patrick Hand, body font Inter.
Voice: Edge TTS en-US-AndrewNeural (không BGM). Render: npx hyperframes render --quality high.
Media agent cần biết _tool_pollinations() cho stick-figure + _tool_hyperframes() cho CLI + _tool_tts() với voice param.
Xem `references/english-channel-hyperframes.md` cho full guide.

### CEO chủ động gợi ý (initiative)

Function `_ceo_initiative()`:
1. Đọc taskboard từ AgentMemory
2. Map task → 4 dự án qua keyword match (project name + key)
3. LLM tổng hợp hiện trạng → JSON {proactive_suggestions, urgent, note}
4. Trả về text format CEO-style: tự nhiên, khích lệ, gợi ý cụ thể

Đăng ký trong registry: `reg.register("initiative", live.get("initiative", _ceo_initiative))`.

**Trigger:** Khi user hỏi "tình hình công ty" / "có gì mới" / dashboard chat gửi lệnh "tình hình".

### Cronjob Morning Briefing (8h daily)

`cron_morning.py` — no_agent=True script, chạy 8h sáng mỗi ngày:
1. Đọc taskboard từ AgentMemory
2. Phân loại task theo 4 dự án (keyword match)
3. Thống kê: done/running/pending/blocked mỗi dự án
4. Dự án không có task → tự gợi ý kickstart
Chi tiết: `references/dashboard-setup.md` → section "Văn Phòng tab"
Script path: copy vào `$HOME/AppData/Local/hermes/scripts/cron_morning.py`

See `references/ceo-telegram-chat-mode.md` for budget history (240s→3s fix) and 1-call architecture.  \nSee `references/ceo-chat-rules-corrected.md` for the user corrections that shaped the chat flow.  \nSee `references/telegram-bot-ops.md` for token rotation after revoke (unkillable PID pattern).  \nSee `references/dashboard-v2.md` for the new SPA 4-tab dashboard (replaces old 7-tab setup).  \n
### CEO Telegram Report (outbox fallback)

Function `_ceo_telegram_report()`:
1. **Try** `hermes_tools.send_message(target="telegram", msg)` — chỉ chạy trong Hermes context
2. **Fail: ImportError** → ghi JSON line vào `~/.hermes/outbox/ceo_report.json`
3. **Cron Telegram Delivery** mỗi 15p → outbox → Telegram API

Format outbox: `{"target": "telegram", "message": "...", "from": "ceo", "ts": "..."}`
Chi tiết: `references/ceo-telegram-outbox.md`

### Cronjob Morning Briefing (8h daily) + Afternoon Briefing (17h daily)

**Override loader không đủ.** Starlette 1.3.1 dùng `lru_cache` trên `get_template()` với dict argument → `TypeError: cannot use 'tuple' as a dict key`.

Fix: bỏ `Jinja2Templates` hoàn toàn, dùng `jinja2.Environment` trực tiếp:
```python
from jinja2 import Environment, FileSystemLoader, select_autoescape
from fastapi.responses import HTMLResponse

_jinja_env = Environment(
    loader=FileSystemLoader("templates/"),
    autoescape=select_autoescape(["html", "xml"]),
)

def _render(name: str, context: dict) -> HTMLResponse:
    template = _jinja_env.get_template(name)
    return HTMLResponse(template.render(**context))
```

---

## 🚀 TEAM DISPATCH — Hermes delegate_task Pattern (20/07/2026)

### Khi nào dùng
User muốn team TANO Agency cùng làm, không tự làm 1 mình. Hoặc task có nhiều mảng độc lập (code + design + content).

### Pattern: CEO → Orchestrator → Workers

```mermaid
Hermes (CEO) → delegate_task(role=orchestrator)
  → Subagent (Orchestrator) đọc kế hoạch
  → Subagent tự spawn worker(s) để làm
  → Workers trả kết quả
  → Orchestrator tổng hợp → trả về Hermes
```

### Steps
1. **Load CEO dispatch trước** — dùng `skill_view('company-one-person')` hoặc viết kế hoạch phân công
2. **Gọi delegate_task với role=orchestrator** — subagent có thể spawn worker riêng
3. **Orchestrator tự chia việc** — đọc CEO plan → tạo tasks → gọi delegate_task
4. **Hermes nhận kết quả** — kiểm tra, verify, báo user

### Lưu ý
- `role='orchestrator'` cho phép subagent gọi delegate_task — leaf thì không
- Context phải đầy đủ (file paths, API endpoints, design tokens)
- Worker bị giới hạn `max_spawn_depth=1` cho user này — orchestrator không spawn được orchestrator nữa
- Mỗi worker có terminal + tool riêng, không ảnh hưởng lẫn nhau
- Sau khi workers xong, orchetrator trả summary → Hermes verify kết quả (re-read file, test API)

### Ví dụ session này
```
User: "Tao muốn công ty Tano Agency cùng làm lấy kinh nghiệm"
→ Hermes: skill_view('company-one-person')
→ delegate_task(role='orchestrator', goal='Dispatch CEO...')
  → CEO phân công 59 tasks cho 8 phòng ban
  → Lưu kế hoạch ra file MD
→ delegate_task(goal='Build landing page...')
  → Subagent tự quyết định strategy, code, test
  → Ghi index.html mới 810 dòng
  → Test API confirm MCP hoạt động
→ Hermes: verify kết quả, báo user
```

### Pitfalls
- **Worker summary là self-report** — luôn verify sau (re-read file, curl test API)
- **Orchestrator mất context** sau khi spawn workers — context phải đủ detail
- **Language contamination** — worker mặc định English nếu ko chỉ định tiếng Việt trong context
- **Quá nhiều task parallel** — max 3 concurrent workers cho user này

### Mobile-first CSS pattern
- Bottom nav fixed (6 items, icon + label)
- Card layout single column
- Chat messages: user right (accent bg), assistant left (card bg)
- System health: 2-column grid, auto-refresh 30s
- All API calls async fetch + loading states

**File:** `web/dashboard.py` (6KB) + `web/templates/index.html` (23KB)

## Tool thật mỗi agent ($0) — v3 Real Adapters

| Dev Agent (đã nâng cấp — tool thật + viết code + guard system)

| Tool | Chức năng | Implementation | File |
|------|-----------|----------------|------|
| `_real_repo()` | Tìm code liên quan trong D:/MMO Du an — keyword map (abtrip/fast track/gmsp/tu vi/tano) + `rg` fallback | pathlib + subprocess | agents/dev/adapters.py |
| `_real_logs()` | Đọc file .log thật trong D:/MMO Du an | pathlib.rglob | agents/dev/adapters.py |
| `_real_infra()` | Kiểm tra port 8137, Python processes, disk | `netstat` + `tasklist` + `wmic`/PowerShell | agents/dev/adapters.py |
| `_real_search()` | Web search: Hermes web_search tool, fallback ddgs | `from hermes_tools import web_search` / ddgs lib | agents/dev/adapters.py |
| `_real_build()` | **Tạo FILE CODE THẬT** — LLM DeepSeek sinh JSON plan → `subprocess` write file + chạy commands. TDD: test trước code | `_tool_terminal()` + `_tool_write_file()` | agents/dev/adapters.py |
| `_is_allowed_path()` | **Guard file I/O** — `_ALLOWED_ROOTS` (D:/MMO Du an, Desktop, Documents) + `_BLOCKED_PREFIXES` (Windows, Program Files, System32) | Path.resolve() + path startswith | agents/dev/adapters.py |
| `_is_safe_command()` | **Guard terminal** — block `del`, `rm -rf`, `shutdown`, `format`, `curl -o`, `powershell -enc`; whitelist `pip`, `python`, `git`, `pytest`, `node`, `cd`, `dir` | starts_with + contains check | agents/dev/adapters.py |
| `_budget_check()` / `_budget_tick()` / `_budget_reset()` | **Budget cap** — tối đa 10 terminal calls, 8 files, 30KB read, 120s runtime. Reset mỗi task session. | `_DEV_BUDGET` dict + time.monotonic() | agents/dev/adapters.py |
| `_is_allowed_path()` / `_is_safe_command()` / `_budget_check()` | **3-layer guard** — path guard (allowed roots + blocked system dirs) → terminal guard (whitelist pip/python/git, blacklist del/shutdown/curl) → budget cap (max calls/files/time) | Path.resolve + starts_with + time.monotonic() | agents/dev/adapters.py |
| `architect` / `reviewer` / `debugger` / `handover_doc` | LLM analyze (DeepSeek) | core/llm chat | agents/dev/adapters.py |

**Budget cap — giới hạn tài nguyên Dev:**
- Tối đa 10 lần terminal call, 8 file tạo, 30KB đọc, 120 giây runtime
- Reset mỗi task mới. Blocked request trả error shape như bình thường
- Budget counter global trong Dev adapter, không phải per-invocation
- Chi tiết: `references/agent-budget-cap.md`

**Guard system chi tiết:**
- File ghi/đọc vào allowed roots → ✅ OK
- File ghi/đọc vào blocked dirs → 🚫 `{"status": "blocked", "error": "..."}`
- `_tool_terminal()` check blacklist + whitelist — lệnh không rõ → block
- `_tool_search_files()` (rg) không bị guard — command nằm trong whitelist rồi
- Hardware info (`_real_infra`) qua PowerShell Get-CimInstance không bị ảnh hưởng

**Đã test:** Dev tạo file thật, guard block `C:\Windows`, `C:\Program Files` mà vẫn cho phép Desktop + D:/MMO Du an.

### 🎨 Media Agent (v5.1 — FAL + Pollinations + HyperFrames CLI + Edge TTS Anh/Việt)

| Tool | Chức năng | Implementation | File |
|------|-----------|----------------|------|
| `_real_brand()` | Tìm BRAND_DESIGN.md hoặc brand\*.md trong D:/MMO Du an | pathlib.rglob | agents/media/adapters.py |
| `_real_assets()` | Scan PNG/JPG/SVG/MP4 filter theo topic + kích thước | pathlib + os.stat | agents/media/adapters.py |
| `_tool_image_gen()` | Sinh ảnh FAL (GMSP style — dark academia) | `from hermes_tools import image_generate` | agents/media/adapters.py |
| `_tool_pollinations()` | **MỚI** Gen stick-figure free qua Pollinations (Airfare Decoded style) — black ink, white bg | urllib.request + Pollinations API | agents/media/adapters.py |
| `_tool_tts()` | **NÂNG CẤP** Edge TTS — auto-detect: VN char→`vi-VN-NamMinhNeural`, English→`en-US-AndrewNeural`. Voice param override được. | subprocess `edge-tts --voice ...` | agents/media/adapters.py |
| `_tool_hyperframes()` | **MỚI** Chạy HyperFrames CLI: check, lint, render, snapshot, browser, doctor. Mặc định workdir=`_AIRFARE_ROOT` | subprocess + npx | agents/media/adapters.py |
| `_real_image_gen()` | **NÂNG CẤP** Auto-detect: topic "airfare"/"decoded" → dùng Pollinations stick-figure. Còn lại → FAL. | LLM prompt + `_tool_pollinations` / `_tool_image_gen` | agents/media/adapters.py |
| `_real_search()` | Web search fallback ddgs (nếu web_search tool ko có) | ddgs | agents/media/adapters.py |
| `video_pipeline` | **NÂNG CẤP** LLM analyzer biết 2 pipeline: GMSP (Việt, FFmpeg) vs Airfare Decoded (English, HyperFrames, Pollinations, Edge TTS AndrewNeural) | llm.make_analyzer(system_prompt=...) | agents/media/adapters.py |
| `hyperframes` | **MỚI** Registry adapter — lambda wrapper `_tool_hyperframes(cmd, workdir=_AIRFARE_ROOT)` | lambda cmd, **kw | agents/media/adapters.py |

### 🔍 Research Agent (đã nâng cấp — web_search tool + multi-query)

| Tool | Chức năng | Implementation | File |
|------|-----------|----------------|------|
| `research()` | Web search 8 kết quả — Hermes web_search tool ưu tiên, ddgs fallback | `from hermes_tools import web_search` / ddgs | agents/research/adapters.py |
| `niche()` | 4-query multi-search (market/competitors/trends/opportunities) | loop _web_search | agents/research/adapters.py |
| `trend()` | Multi-source trending (tech + VN + CN) | loop _web_search | agents/research/adapters.py |

### 👔 CEO Agent (đã nâng cấp — Telegram báo cáo)

| Tool | Chức năng | Implementation |
|------|-----------|----------------|
| `intake` / `planner` / `reporter` | LLM DeepSeek: phân tích lệnh, lập kế hoạch, báo cáo | core/llm chat |
| `dispatch` | ThreadPoolExecutor max 3 workers, 90s timeout — ghi taskboard → gọi brain.run() | concurrent.futures |
| `initiative` | **Chủ động gợi ý dự án đang làm dở** — đọc taskboard → LLM tổng hợp → gợi ý | _ceo_initiative() |
| `telegram_report` | Gửi báo cáo qua Telegram | `from hermes_tools import send_message` |

### 🛒 Sales Agent (giữ nguyên)
| Tool | Nguồn |
|------|-------|
| `lead` / `qualify` / `outreach` / `pipeline` / `account` | DuckDuckGo urllib search + LLM phân tích |

### 📢 Marketing Agent (giữ nguyên)
| Tool | Nguồn |
|------|-------|
| `content` / `seo` / `campaign` / `social` / `trend` | brand-voice ECC skill + DDGS web search |

### ⚙️ Operations Agent (giữ nguyên — PowerShell real data)
| Tool | Nguồn |
|------|-------|
| `_wmic_full()` — disk/CPU/RAM/uptime/process | PowerShell Get-CimInstance + Get-Process |
| `healthcheck` / `monitor` / `incident` / `takeover` | Subprocess + LLM |

### 🎫 Support Agent (giữ nguyên)
| Tool | Nguồn |
|------|-------|
| `_ticket_crud()` — SQLite CRUD | sqlite3 |
| `_kb_search_v2()` — multi-layer search | AgentMemory + file |
| `reply` / `faq` / `sentiment` / `escalate` | LLM + memory |

### 📊 Analytics Agent (giữ nguyên)
| Tool | Nguồn |
|------|-------|
| `_analytics_query()` — SQL query + CSV export | sqlite3, safety check |
| `report` / `kpi` / `forecast` / `anomaly` / `dashboard` | LLM + SQL |

### Ops / Support / Analytics — giữ nguyên

| Agent | Tool | Nguồn |
|-------|------|-------|
| Ops | `_wmic_full()` — PowerShell Get-CimInstance: disk, CPU, RAM, uptime, python tasklist | PowerShell + tasklist |
| Ops | PowerShell fallback: Win32_LogicalDisk, Win32_OperatingSystem, Win32_PhysicalMemory, Win32_ComputerSystem, Get-Process | $ProgressPreference=SilentlyContinue |
| Support | `_ticket_crud()` — SQLite ticket CRUD (add/list/get/close/search) + notes | sqlite3.Row |
| Support | `_kb_search_v2()` — multi-layer search: memory → file | AgentMemory + pathlib |
| Analytics | `_analytics_query()` — SQL query + CSV export, safety check (block DROP/INSERT/UPDATE/DELETE/ALTER) | sqlite3 |
| Sales | `_web_search()` — DuckDuckGo | urllib + re |
| Marketing | `_content_pipeline()` + `_voice_profile()` | brand-voice pattern |
| Tất cả | `_delivery_outbox()` — ghi outbox.json → Hermes gửi Telegram | JSON file |

## Cách chạy

```bash
# === 1. Web Dashboard (khuyên dùng — mobile-friendly) ===
cd D:/MMO Du an/TANO-AGENCY/web
uvicorn dashboard:app --host 0.0.0.0 --port 8137
# Truy cập: http://localhost:8137 (hoặc IP máy trên phone)

# === 2. CLI smoke test ===
cd D:/MMO Du an/TANO-AGENCY/PLATFORM/agent-core

# Smoke test với tool thật
python run.py --real

# Chạy 1 agent cụ thể
python run.py sales lead "khách hàng tiềm năng ngành du lịch"
python run.py support reply "khách hỏi chính sách hoàn vé"
python run.py dev review "review code TANO-AGENCY"
python run.py analytics report "phân tích DB"
python run.py operations incident "API trả lỗi 500"
python run.py operations takeover "check system health"
python run.py marketing trend "content marketing AI 2026"

# === 3. Telegram (nếu dùng) ===
python main.py
```

## Cấu hình .env

```
DEEPSEEK_API_KEY=<key>
OPENROUTER_API_KEY=<key>
GEMINI_API_KEY=<key>
TELEGRAM_BOT_TOKEN=<token>   # Cho main.py
TELEGRAM_CHAT_ID=<chat_id>   # Whitelist
```

## Real-time pipeline

Khi `get_brain(name).run(ttype, topic)` được gọi:

1. **INTAKE** — tạo Task object
2. **PLAN** — LLM sinh sub-questions
3. **COLLECT** — gọi adapter thật (web search, WMIC, git, SQLite...)
4. **VALIDATE** — rating từng nguồn (✅🟡🔄)
5. **ANALYZE** — LLM phân tích findings
6. **SYNTHESIZE** — LLM viết output (báo cáo, reply, incident response...)
7. **VERIFY** — rule match + consistency + anti-hallucination
8. **DELIVER** — trả chunks về CEO / ghi outbox

## Agent Brain Prompts — Design Principles

Mỗi agent có prompt não được nhúng trong `llm.make_analyzer(system_prompt=...)`. Đây là yếu tố quyết định nhất tới "thông minh" của agent.

### Three levels of agent intelligence

| Level | What | When | Cost |
|-------|------|------|------|
| **Brain prompt** | Edit `system_prompt=` string | Agent gives wrong answers/tone/format | 0 code, edit string + restart |
| **Code logic** | Add Python validation/parsing/fallback | Agent hallucinates or ignores data | 10-50 lines |
| **Real tools** | Add terminal/file/web/DB access | Agent knows what to do but can't do it | 50-200 lines |

### Brain audit checklist (dùng khi sửa agent)
1. **Role** — "Mày là software architect..." → agent biết nó là ai
2. **Constraints** — "TUYỆT ĐỐI không bịa số" → agent biết giới hạn
3. **Output format** — "Trả về bảng: | STT | phòng ban | việc | P1/P2/P3 |" → output parse được
4. **Tool awareness** — agent biết nó có tool gì? Nếu có tool thật mà prompt não không nhắc → agent không dùng
5. **Fallback** — "Nếu không xử lý được → escalate" → agent biết làm gì khi bí

### Gap analysis (Jul 2026 audit) — Đã fix
| Agent | Gap | Fix applied |
|-------|-----|-------------|
| **CEO** | prompt não không biết 4 dự án | ✅ Embed 4 dự án + COMPANY_PROJECTS vào prompt |
| **Dev** | prompt não không biết `_real_repo()`, `_tool_terminal()` | ✅ Embed tool list + TDD rule |
| **Sales** | chỉ 1 não copywriter | ✅ Thêm não `lead_analyzer` — đánh giá fit, 3 dự án mục tiêu |
| **Marketing** | brand voice có code nhưng prompt não ko nhắc | ✅ Embed brand voice (màu, giọng, accent từng domain) |
| **Media video_pipeline** | 1 line quá ngắn | ✅ Embed pipeline 7 bước + rules (ko BGM, 1 giọng, no zoompan, dark academia) |

**Nguyên tắc nhúng skill/context vào agent prompts:**
- Skill .md files không được agent code Python đọc — phải **nhúng pattern** vào `llm.make_analyzer(system_prompt=...)` hoặc hard-code rules vào function
- Brand voice, project context, pipeline knowledge, tool capabilities đều phải nằm trong prompt string, không nằm ngoài

Chi tiết: `references/agent-brains.md`

### Prompt não upgrade patterns (Jul 2026 session)

**Pattern 1 — Embed project context into prompts (CEO, Sales)**
```python
# Before: generic
"Phân tích mệnh lệnh của Chủ tịch."

# After: project-aware
"Phân tích mệnh lệnh của Chủ tịch.
=== DỰ ÁN HIỆN TẠI ===
1. GMSP — Content Pipeline
2. An Bình Fast Track — Fast Track & Lounge Nội Bài
3. ABTrip — Ticketing máy bay
4. Tử Vi — AI Engine

Khi Chủ tịch hỏi thăm, kiểm tra COMPANY_PROJECTS và gợi ý."
```

**Pattern 2 — Tell agents their available tools (Dev)**
```python
# Before: tool-blind
"Mày là software architect. Từ yêu cầu, đưa: kiến trúc module..."

# After: tool-aware
"Mày là software architect. ...
=== TOOL CỦA MÀY ===
- _real_repo(): tìm code cũ trong D:/MMO Du an/ trước khi viết mới
- _tool_terminal(): chạy terminal thật — pip install, git, py_compile, pytest
- _tool_write_file(): ghi file thật — LUÔN validate path tồn tại trước khi ghi
- TDD: viết test/test_*.py TRƯỚC, code thật SAU"
```

**Pattern 3 — Embed brand/system rules (Marketing, Media)**
```python
# Before: generic
"Mày là content writer Việt Nam. Viết content theo brief..."

# After: brand-embedded
"Mày là content writer Việt Nam. Viết content theo brief...
=== BRAND VOICE ===
- Brand chính: Giải Mã Số Phận — đen #0D0D12 + vàng #FFD700 + đỏ #8B0000
- Giọng điệu: gai góc, từng trải, brutal truth
- Công thức: truth opening → hidden system → urgency → giải pháp"
```

**Pattern 4 — Embed pipeline knowledge (Media video)**
```python
# Before: too vague
"Mày là video producer. Từ brief: kịch bản timeline..."

# After: pipeline-embedded
"Mày là video producer. ...
=== PIPELINE GMSP ===
Pipeline: Research → Script → TTS → Media → Render → Publish → Social
=== QUY TẮC ===
- Hook 3s đầu — shock/curiosity/brutal truth
- 1 giọng duy nhất xuyên suốt (ko trộn TTS)
- Ko BGM — chỉ voiceover
- Mỗi scene 1 ảnh AI riêng (dark academia)"
```

**Rule of thumb:** If you can remove the prompt and the agent still knows what to do because of the code, the prompt is redundant. If you can remove the code and the prompt still tells the agent what to do, the code is redundant. The prompt should carry KNOWLEDGE the agent can't derive from its training or from code logic alone.

## Telegram Bot Project Isolation (NEW 19/07/2026)

**Vấn đề:** CEO bot trên Telegram dùng 1 system prompt chung → lẫn lộn dự án. Hỏi Airfare trả lời về GMSP.

**Fix:** `main.py` `cmd_natural()` — thêm `_detect_project()` + inject `build_project_context()` per-project.

### Session switching (19/07/2026)
Thêm `_project_sessions` dict + lệnh `/gmsp`, `/abtrip`, `/airfare`, `/tuvi`, `/fasttrack`, `/thoát` trong `handle()`:
- User gõ `/gmsp` → session=GMSP, mọi câu sau đó đều trong GMSP context
- User gõ `/thoát` → về global chat
- `_detect_project()` fallback nếu ko có session
- CEO response style: NO "CEO đang nghĩ..." — sendChatAction typing indicator, 1 response duy nhất

### Key files
- `main.py` — `cmd_natural()`: detect → inject context → save chat → auto-extract facts
- `dashboard/project_memory.py` — shared SQLite DB (dashboard + Tele cùng DB)
- `data/project_memory.db` — 6 tables: project_chat, global_chat, facts, decisions, preferences, skills

### Flow
```
User Telegram: "dự án airfare đang làm gì?"
  → _detect_project("airfare")  → "AirFares Decoded"
  → build_project_context("AirFares Decoded")  → facts + decisions
  → Inject into system prompt: "=== DỰ ÁN HIỆN TẠI: AirFares Decoded ==="
  → CEO response CHỈ về AirFares, ko lẫn
  → save_chat("AirFares Decoded", ...)
  → extract_facts_from_message → auto-save emails/phones/URLs

User: "còn GMSP sao rồi?"
  → _detect_project("gmsp") → "GMSP"
  → build_project_context("GMSP")  → facts của GMSP, ko phải AirFares
```

### Keyword map
```python
PROJECT_NAMES = {
    "gmsp": "GMSP", "giải mã": "GMSP",
    "abtrip": "ABTrip (Smart Agent)", "ab trip": "ABTrip (Smart Agent)", "smart agent": "ABTrip (Smart Agent)",
    "tử vi": "Tử Vi", "tu vi": "Tử Vi",
    "airfare": "AirFares Decoded", "airfares": "AirFares Decoded",
    "fast track": "Fast Track", "nội bài": "Fast Track",
}
```

Chi tiết: `references/telegram-project-context.md`

## HQ Module — Company Headquarters (7 bảng, merged 19/07/2026)

The Claude company v2 design (ORG-v2, COORDINATION-v2 schema, OPERATING-RHYTHM, DECISION-MATRIX) has been **merged into code** at `dashboard/hq.py`.

### What's Implemented

| Claude Concept | Implementation | Status |
|----------------|---------------|--------|
| 7-table Airtable schema | SQLite at `data/hq.db` via `hq.py` — `agents`, `jobs`, `sops`, `kpis`, `approvals`, `escalations`, `activity_log` | ✅ Done |
| Seed 8 agents (ORG v2) | research (reasoning), marketing (balanced), sales (balanced), content (creative), designer (creative), media (cheap), dev (balanced), ops-finance (cheap) | ✅ Done |
| Job lifecycle 6 bước | `create_job()` → `move_job()` → `approve()` + 12 API endpoints | ✅ Done |
| Approval flow | `get_pending_approvals()`, `approve(job_id, decision)` with activity_log | ✅ Done |
| Morning Brief | `morning_brief()` — format: ☀️ date + pending + blocked + summary | ✅ Done |
| Decision Matrix | Not hardcoded — `risk_level` field in approvals table (L2/L3) | ⚡ Inferred |
| Operating Rhythm | 3 Hermes cron registered: Brief 7h, Dispatch 9h/14h | ✅ Partial |

### API Endpoints (in `dashboard/app.py`)

```
GET  /api/hq/summary            — job counts
GET  /api/hq/jobs               — list jobs (?status, pack, role, limit)
GET  /api/hq/jobs/{id}          — single job
POST /api/hq/jobs               — create job
POST /api/hq/jobs/{id}/move     — move job status
GET  /api/hq/approvals          — pending approvals
POST /api/hq/approvals/{id}/{decision}  — approve/reject
GET  /api/hq/escalations        — open escalations
GET  /api/hq/kpis               — KPI by week
GET  /api/hq/agents             — 8 agents roster
GET  /api/hq/sops               — SOPs by role
GET  /api/hq/activity           — activity log
GET  /api/hq/brief              — morning brief text
```

### Cron Scripts (path: `scripts/cron_*.py`, registered as Hermes no_agent cron)

| Script | Schedule | Purpose |
|--------|----------|---------|
| `cron_morning_brief.py` | 07:00 | Daily brief → stdout |
| `cron_dispatch.py` | 09:00, 14:00 | Move queued jobs → doing + log |
| `cron_eod.py` | (pending) | End-of-day summary |

**Cron registration pitfall:** Hermes requires script paths relative to `~/.hermes/scripts/`. Copy scripts there:
```bash
cp "/d/MMO Du an/TANO-AGENCY/PLATFORM/agent-core/scripts/cron_*.py" ~/AppData/Local/hermes/scripts/tano/
```
Register with `script="tano/cron_morning_brief.py"` and `no_agent=True`.

**SQL bug fixed (19/07):** The `get_jobs()` function had missing spaces in SQL concatenation (`jobsWHERE`, `DESCLIMIT`). Fixed by prepending spaces: `" WHERE " + ...`, `" ORDER BY ..."`, `" LIMIT ..."`.

### Remaining from Claude's Design
- Dispatch tick #3 (20:00) + EOD (21:00) — need 2 more cron
- KPI Review cron (T2 08:00) — need new script
- Content calendar reminder (T6 16:00) — need new script
- Weekly report (CN 20:00) — need new script
- Dashboard CEO Cockpit tab — needs HTML update
- Job lifecycle via Telegram OK/NO — needs main.py patch
- Decision Matrix enforce in approval flow — needs code

## Quality Gate + Loop Mode (19/07/2026)

Added after studying OPC (iamtouchskyer/opc) and Paperclip architectures.

### D2 Compound Quality Gate — `dashboard/quality_gate.py`
11 mechanical layers checking eval quality: thinEval, noCodeRefs, lowUniqueContent, singleHeading, lowFindings, fabricatedRefs, lowVariance, aspirational, missingReasoning, missingFix, invalidRefCount. ≥3 fails = FAIL, 1-2 = ITERATE, 0 = PASS. Code-enforced, no LLM judgment. Also checks review independence (byte-identical=ERROR, >70% overlap=WARNING).

### Loop Mode — `dashboard/loop_mode.py`
Atomic checkout pattern: `atomic_checkout(slot)` → `heartbeat(slot)` → `release(slot)`. Prevents double-dispatch from overlapping cron. `dispatch_tick()` wraps the full workflow. Separate `loop_locks.db` to avoid contention with `hq.db`.

**See:** `references/quality-gate-v2.md` for full API + `references/opc-repo-research.md` for all 4 OPC repos studied.

## Goose AI Agent — Installed & Configured (19/07/2026)

### Installation
```bash
curl -fsSL https://github.com/aaif-goose/goose/releases/download/stable/download_cli.sh | CONFIGURE=false bash
```
Binary at: `C:\Users\Nguyen Ngoc Tan\goose\goose.exe` (v1.43.0)

### Provider Config
Claude designed for OpenRouter/Anthropic. For DeepSeek V4 support:

```yaml
# ~/AppData/Roaming/Block/goose/config/config.yaml
providers:
  openai:
    model: deepseek-chat
    api_key_env: DEEPSEEK_API_KEY
    base_url: https://api.deepseek.com/v1
```

**Note:** `deepseek-v4-flash` has thinking mode that causes Goose to 400 on follow-up turns (issue #9041 — `reasoning_content` field not handled). Use `deepseek-chat` for stable operation, or wait for Goose patch.

### Interactive Setup
Goose requires `goose configure` run in an interactive terminal (not via Hermes terminal tool). Steps:
1. Open Git Bash
2. `export DEEPSEEK_API_KEY=*** `
3. `~/goose/goose.exe configure`
4. Choose: OpenAI → model `deepseek-chat` → env `DEEPSEEK_API_KEY` → URL `https://api.deepseek.com/v1`
5. Skip model fetch (may 401) — core config works without it
6. Test: `DEEPSEEK_API_KEY=*** ~/goose/goose.exe session`

### Usage
```bash
# Run a task
DEEPSEEK_API_KEY=*** ~/goose/goose.exe session

# Main commands
~/goose/goose.exe session     # interactive chat
~/goose/goose.exe session list  # list sessions
~/goose/goose.exe doctor      # health check
```

### Project Memory System (19/07/2026) — `dashboard/project_memory.py`

**Problem solved:** CEO confused projects — talking about Airfare while answering about GMSP.

**Architecture:** Per-project SQLite memory, shared between dashboard + Telegram bot.

**Database: `data/project_memory.db`** — 6 tables:

| Table | Key Column | What |
|-------|-----------|------|
| `project_chat` | `project` (name) | Per-project chat history |
| `global_chat` | — | Non-project chat |
| `facts` | `project` (or `__global__`) + `category` | Confirmed knowledge (emails, phones, URLs, decisions) |
| `decisions` | `project` + `status` | Business decisions made |
| `preferences` | `key`/`value` (JSON) | User settings (theme, filters...) |
| `skills` | `name` + `category` | Cross-project reusable skills |

**Key functions** (import from `dashboard.project_memory`):

```python
save_chat(project, role, content)          # Save per-project message
load_chat_history(project, limit=30)       # Load last N messages
add_fact(project, fact, category, conf, src)   # Store fact
get_facts(project, category=None, limit=20)    # Retrieve facts
search_facts(query, project, limit)        # Text search facts
add_decision(project, decision, context)   # Record decision
get_decisions(project, limit=20)           # Get decisions
set_pref(key, value) / get_pref(key, default)  # User prefs
add_skill(name, desc, category, tools)     # Reusable skill
get_skills(category)                       # List skills
build_project_context(project)             # Build CEO context string
extract_facts_from_message(project, msg)   # Auto-extract emails/phones/URLs
```

**Chat flow with project awareness:**

```
User: "dự án GMSP có contact gì?"
  → POST /api/chat {message, session_type: "GMSP", session_id: "..."}
  → Server: build_project_context("GMSP") = facts + decisions + skills + last 30 msgs
  → DeepSeek injects: "=== DỰ ÁN HIỆN TẠI: GMSP ===" 
  → CEO knows context, responds correctly
  → save_chat("GMSP", ...) + extract_facts_from_message() + parse [LƯU FACT] brackets

User Tele: "còn ABTrip sao rồi?"
  → _detect_project("abtrip") = "ABTrip"
  → Only ABTrip facts loaded — different context, no confusion
```

**Telegram `_detect_project()` keyword map:**
```python
PROJECT_NAMES = {
    "gmsp": "GMSP", "giải mã": "GMSP",
    "abtrip": "ABTrip", "ab trip": "ABTrip",
    "tử vi": "Tử Vi", "tu vi": "Tử Vi",
    "airfare": "AirFares Decoded", "airfares": "AirFares Decoded", 
    "fast track": "Fast Track", "nội bài": "Fast Track",
}
```

**CEO response bracket parsing for auto-save:**
- `[LƯU FACT: nội dung] [CATEGORY: contact/note/link]` → `add_fact()`
- `[QUYẾT ĐỊNH: nội dung]` → `add_decision()`

**API endpoints:**
- `GET /api/memory/facts?project=GMSP&category=contact&q=search&limit=20`
- `POST /api/memory/facts` — `{project, fact, category, confidence, source}`
- `GET /api/memory/decisions?project=GMSP&limit=20`
- `POST /api/memory/decisions` — `{project, decision, context}`
- `GET /api/memory/projects` — all projects with memory counts
- `GET /api/preferences` / `POST /api/preferences`
- `GET /api/skills?category=general` / `POST /api/skills`

**Dashboard project sidebar:**
- "Dự án" section in sidebar (under "Chung"), auto-populated from `/api/projects`
- Click project → modal with: facts list, decisions list, inline chat with `session_type: projectName`
- Green/red status dot per project (active/inactive)
- `projectAddFact()` — manual fact entry via prompt → POST API

**Pitfalls:**
- `project_memory.py` at `dashboard/` dir → need `sys.path.insert(0, str(BASE / "dashboard"))` before import
- DB path: uses same `DATA` dir as other DBs (`data/project_memory.db`)
- `_extract_bracket()` helper needed for CEO response bracket parsing — defined in `app.py`
- Dashboard runs on port **8138** (8137 often stuck in TIME_WAIT). Change port in `run()` if 8137 free.
- Port conflict: use `netstat -ano | findstr ":8137"` → kill PID → wait for TIME_WAIT to clear (can take 2+ min)
- Dashboard deploy pitfall: `__pycache__` holds stale `.pyc`. Clear with `shutil.rmtree()` before restart.
- **File endpoint 404 after rewrite:** If `/api/file/ls`, `/api/file/read`, `/api/file/search` return 404 despite Python import showing them registered: clear all `__pycache__` dirs, kill ALL Python processes holding the port, verify with `netstat -ano | grep :8138`, then restart.
- Tele bot: after editing `main.py`, kill old process by PID (not by name — `wmic` unreliable in git-bash), NOT `taskkill /F /IM python.exe` (kills dashboard too)

## Note: Related Skills

`agent-ops/multi-agent-platform` covers the same codebase at `TANO-AGENCY/PLATFORM/agent-core/`. This skill (`company-one-person`) is the **active, updated** version with CEO v2, web dashboard, and 6 upgrade patches. Prefer `company-one-person` for operational queries.

## Tham khảo

- `references/claude-company-v2-merge.md` — Claude's company v2 design (ORG-v2, COORDINATION-v2, OPERATING-RHYTHM, DECISION-MATRIX) + merge strategy to adopt 7-table job lifecycle + operating rhythm + decision matrix into existing system
- `references/agent-brains.md` — Full audit 9 brains: gap analysis per agent, 3 intelligence levels, fix patterns
- `references/agent-budget-cap.md` — Dev budget cap: terminal calls, file creates, read chars, duration limits
- `references/agent-security-guard.md` — Dev guard patterns: file I/O guard + terminal guard + test commands
- `references/brain-upgrade-patterns.md` — 4 prompt patterns (embed projects, tools, brand, pipeline) — from Jul 2026 upgrade session
- `references/ceo-confirm-flow.md` — CEO confirm trước dispatch: backend logic, frontend button, test checklist
- `references/ceo-response-format.md` — CEO chat format rules: line-by-line parser, inline markdown, CSS classes, layout fixes. Dùng khi build/sửa dashboard chat.
- `references/ceo-3-mode-chat.md` — CEO 3-mode system prompt: chat tự nhiên / phân rã / triển khai + `\\n` escaping pitfalls
- `references/ceo-chat-history.md` — CEO chat history pattern: **SQLite** persistence (F5 ko mất), schema, API flow (Jul 2026 upgrade from in-memory)
- `references/ceo-chat-rules-corrected.md` — CEO chat correction history: 240s→3s, 1 LLM call, no dispatch, system prompt with "CHỈ TRẢ LỜI" rule
- `references/ceo-telegram-chat-mode.md` — CEO Telegram chat: budget history, 1-call LLM architecture, system prompt rules
- `references/ceo-telegram-outbox.md` — CEO Telegram outbox fallback: hermes_tools.send_message → outbox JSON → cron
- `references/dashboard-setup.md` — FastAPI dashboard API endpoints, mobile-first template pattern, Jinja2 fix, run command
- `references/dashboard-v2.md` — Dashboard SPA v2: 5-tab mobile-first, web chat tab (POST /api/chat + chat bubble UI), API endpoints, auth pattern
- `references/dev-v2-tools.md` — Dev agent real tools: _real_repo, _real_build (tạo file thật), _real_infra, _real_search, _tool_terminal
- `references/ecc-skill-embedding-map.md` — Full map: 8 ECC skills embedded → which agent, prompt vs code, why others skipped
- `references/english-channel-hyperframes.md` — Mô hình kênh YouTube English faceless với HyperFrames (Airfare Decoded model). Pipeline 6 bước, design tokens, variation guard, cost analysis, onboard guide cho Tano Agency. Tham khảo khi tạo dự án English channel mới.
- `references/media-v2-tools.md` — Media agent real tools: _real_brand, _real_assets, _real_image_gen (FAL)
- `references/situation-room.md` — Văn Phòng tab: CSS animations, agent status, auto-refresh
- `references/telegram-bot-ops.md` — Telegram bot @Tano_CEO_bot: token rotation flow with getMe verification, restart pattern via terminal(background=true), kill process on git-bash (taskkill //PID), main.py polling architecture, env var pass-through
- `references/dashboard-agent-profile-modal.md` — Agent profile modal pattern: 5-section scrollable modal, task click actions (Giao CEO via API toast / Direct chat), project click actions (Yêu cầu CEO / Thêm nhiệm vụ)
- `references/sqlite-wal-fix.md` — SQLite WAL mode fix for concurrent kanban writes
- `references/c-drive-cleanup.md` — C: drive cleanup guide
- `references/5-services-pricing-strategy.md` — 5 dịch vụ cốt lõi (vé máy bay, fast track, visa, eSIM) + pricing + build-to-flip exit strategy
- `references/project-sidebar-modal.md` — Project list in sidebar, click→modal with facts/decisions/chat, manual fact entry, per-project session_type pattern

## Pitfalls — Windows-specific

| Vấn đề | Giải pháp |
|--------|-----------|
| **CEO system prompt `\\n` double-escape** — Python string concat `"\\n"` thành literal `\n` trong prompt | Viết `\\\\n` trong source code = `\\n` trong memory = LLM thấy `\n` = xuống dòng. Nếu dùng `patch` tool, verify sau patch: đọc file, check dòng 114-131 không bị `\\\\\\\\n` |
| **WMIC deprecated** — Windows 10 No. 26200+ không còn wmic.exe | Dùng PowerShell `Get-CimInstance` thay thế. File: `_wmic_full()` trong `real_adapters.py` |
| **FAL key direct call fails on Windows** — Python script Auth header Key {id}:{secret} yields 401 for new keys. Hermes image_gen tool works via Nous subscription backend. | Skip FAL direct. Use Hermes tool or Pollinations free. |
| **Dashboard `__pycache__` stale code** — sau khi sửa `dashboard/app.py` hoặc `dashboard.html`, `__pycache__` giữ `.pyc` cũ → process mới `python dashboard/app.py` không thấy thay đổi (API trả data cũ) | Xoá `__pycache__` trong toàn bộ agent-core tree. Dùng `shutil.rmtree()` qua Python script: `import shutil, os; [shutil.rmtree(os.path.join(d,'__pycache__')) for d in os.walk(root) if '__pycache__' in dirnames]`. Hoặc `rm -rf` nếu đã được approve. Sau đó restart. |
| **FastAPI StaticFiles mount order** — mount sau API routes | Mount AFTER route definitions, nếu không nó bắt url pattern trước |
| **`wmic` từ git-bash** — MSYS2 không tìm được wmic.exe | `cmd.exe //c "command"` hoặc dùng PowerShell thẳng |
| **CEO timeout** — web search DuckDuckGo chậm hoặc bị chặn | `per_task_timeout=90` trong `run_assignments()`. ThreadPoolExecutor shutdown(wait=False) để không treo |
| **DDG HTML scrape chết** — DuckDuckGo thay đổi HTML structure thường xuyên | Dùng `ddgs` library (`pip install ddgs`) thay vì urllib HTML parse. File: `agents/research/adapters.py` đã code sẵn pattern này |
| **Research agent không có __init__.py** — module 'agents.research' không attribute SPEC | Phải tạo `agents/research/__init__.py` export SPEC + build_registry từ spec. Xem các agent khác làm mẫu |
| **CEO chủ động gợi ý** — cần `_ceo_initiative()` trong registry | `reg.register("initiative", live.get("initiative", _ceo_initiative))` — tự check COMPANY_PROJECTS + taskboard + LLM tổng hợp lời gợi ý |
| **Morning / Afternoon cron path** — Hermes cron chạy từ `~/.hermes/scripts/`, không phải agent-core | Script import `from agents import get_brain` phải resolve AGENT_CORE bằng hardcode path: `Path("D:/MMO Du an/TANO-AGENCY/PLATFORM/agent-core"`. Không dùng `Path(__file__)` — không đáng tin trong cron context. |