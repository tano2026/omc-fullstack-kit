# Project Memory Architecture (v3.0 — Jul 2026)

Per-project long-term memory for CEO, shared between Dashboard + Telegram bot.

## Problem Solved

CEO bot lẫn lộn dự án: đang nói AirFares lại trả lời về GMSP vì dùng chung 1 LLM session.
Solution: **per-project context isolation** + **shared SQLite DB** giữa dashboard và Tele bot.

## Database Schema (`project_memory.db`)

Single SQLite file, 6 tables:

```sql
-- Chat history riêng từng dự án (và global)
CREATE TABLE project_chat (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    project TEXT NOT NULL DEFAULT '',     -- 'GMSP', 'ABTrip', '' = global
    role TEXT NOT NULL,                   -- 'user' | 'assistant'
    content TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Kiến thức đã xác nhận
CREATE TABLE facts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    project TEXT NOT NULL DEFAULT '',
    fact TEXT NOT NULL,
    category TEXT DEFAULT 'note',         -- 'contact', 'link', 'note', 'config'
    confidence REAL DEFAULT 0.5,
    source TEXT DEFAULT '',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Quyết định đã đưa ra
CREATE TABLE decisions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    project TEXT NOT NULL DEFAULT '',
    decision TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Preferences (user settings)
CREATE TABLE preferences (
    key TEXT PRIMARY KEY,
    value TEXT NOT NULL,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Kỹ năng dùng chung giữa các dự án
CREATE TABLE skills (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,
    description TEXT,
    template TEXT,
    category TEXT DEFAULT 'general',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## File: `dashboard/project_memory.py`

Module quản lý, import được từ cả `app.py` (dashboard) và `main.py` (Tele bot).

### Key Functions

```python
# Chat
save_chat(project: str | None, role: str, content: str)
load_chat_history(project: str | None, limit: int = 20) -> list[dict]
search_chat(project: str | None, query: str) -> list[dict]

# Facts
add_fact(project: str | None, fact: str, category: str, confidence: float, source: str)
get_facts(project: str | None, category: str = '', search: str = '', limit: int = 20) -> list[dict]
search_facts(query: str) -> list[dict]
extract_facts_from_message(project: str | None, message: str)
# Tự động detect: email, phone, URL, giá tiền trong message → add_fact

# Decisions
add_decision(project: str | None, decision: str)
get_decisions(project: str | None, limit: int = 20) -> list[dict]

# Context building — dùng để inject vào LLM system prompt
build_project_context(project: str) -> str
# Returns: "=== FACTS ===\n- email: abc@xyz [contact]\n...\n=== DECISIONS ===\n- Đã chốt dùng FAL..."
```

### Project Context Injection Pattern

```python
# Trong cmd_natural (Tele bot) và /api/chat (Dashboard):
project = _detect_project(text)  # OR session-based
if project:
    context = build_project_context(project)
    system_prompt += f"=== DỰ ÁN HIỆN TẠI: {project} ===\n{context}\n"
    system_prompt += (
        "QUY TẮC RIÊNG CHO DỰ ÁN NÀY:\n"
        "1. Chỉ trả lời về dự án được hỏi, KO lẫn sang dự án khác.\n"
        "2. Khi biết thông tin mới, viết: [LƯU FACT: nội dung] [CATEGORY: contact/note/link]\n"
        "3. Khi có quyết định, viết: [QUYẾT ĐỊNH: nội dung]\n"
    )
```

### Auto-Extract Facts from CEO Response

Sau mỗi LLM call, parse response để lưu facts tự động:

```python
for line in (out or "").split("\n"):
    if "[LƯU FACT:" in line:
        parts = line.split("[LƯU FACT:")[1].split("] [CATEGORY:")
        fact_text = parts[0].strip()
        cat = parts[1].split("]")[0].strip().lower()
        add_fact(project, fact_text, cat, 0.8, "chat:ceo")
    if "[QUYẾT ĐỊNH:" in line:
        dec = line.split("[QUYẾT ĐỊNH:")[1].split("]")[0].strip()
        add_decision(project, dec)
```

### Import Path for Cron/Bot Context

```python
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "dashboard"))
from project_memory import save_chat, load_chat_history, add_fact, get_facts, build_project_context
```

## Telegram Bot Session Commands

```python
# Session dictionary: chat_id -> project name
_project_sessions = {}

# Keyword-to-project mapping (used for fallback detection)
PROJECT_NAMES = {
    "gmsp": "GMSP",
    "giải mã": "GMSP", "giai ma": "GMSP",
    "abtrip": "ABTrip", "ab trip": "ABTrip",
    "tử vi": "Tử Vi", "tu vi": "Tử Vi", "bói": "Tử Vi",
    "airfare": "AirFares Decoded", "airfares": "AirFares Decoded",
    "fast track": "Fast Track", "nội bài": "Fast Track", "noi bai": "Fast Track",
}
```

### Session-based vs Keyword-based

| Mode | Activation | Behavior |
|------|-----------|----------|
| **Session** | User gõ `/gmsp` | Lock vào dự án, mọi chat sau đó đều dùng project context đó |
| **Keyword** | User gõ "dự án GMSP..." | Tự động detect, chỉ apply cho 1 message |
| **Release** | User gõ `/thoát` hoặc `/all` | Quay về global context |
| **Reset** | User gõ `/new` | Clear session RAM, cũ vẫn lưu DB |

### Priority

```
1. Session (if active) → 2. Keyword detect (if found) → 3. Global
```

## Display on Dashboard (Project Modal)

Khi click project trong sidebar:

```
┌─────────────────────────────────┐
│ DỰ ÁN: 🚀 GMSP                 │
│ Trạng thái: ✅ Đang hoạt động    │
│ Path: D:\...\GMSP               │
│                                  │
│ 🧠 Kiến thức đã lưu              │
│ - email: abc@xyz [contact]      │
│ - phone: 090... [contact]       │
│                                  │
│ 📋 Quyết định đã ghi             │
│ 📌 Đã chốt dùng FAL API         │
│                                  │
│ [💬 Hỏi CEO]  [🧠 Thêm kiến thức]│
│                                  │
│ 💬 Chat riêng dự án              │
│ ┌──[chat bubbles]─────────────┐ │
│ └─────────────────────────────┘ │
│ [input...]            [Gửi]     │
└─────────────────────────────────┘
```

## Skills Table (Shared Across Projects)

```sql
INSERT INTO skills (name, description, template) VALUES
('video-editing', 'kỹ năng edit video với FFmpeg, CapCut', ''),
('tiktok-marketing', 'cách tối ưu content cho TikTok', '');

-- Query: dùng chung cho mọi dự án
skills = get_skills()  # returns all rows
# Inject vào system prompt:
# "=== KỸ NĂNG CÓ THỂ DÙNG ===\n- video-editing: kỹ năng edit video..."
```

## API Endpoints

| Endpoint | Method | Params | Returns |
|----------|--------|--------|---------|
| `/api/memory/facts` | GET | `?project=X&category=Y&q=Z&limit=N` | `{facts: [...]}` |
| `/api/memory/facts` | POST | `{project, fact, category, source}` | `{ok: true}` |
| `/api/memory/decisions` | GET | `?project=X` | `{decisions: [...]}` |
| `/api/memory/decisions` | POST | `{project, decision}` | `{ok: true}` |
| `/api/memory/projects` | GET | — | `{projects: [\"GMSP\",...]}` |
| `/api/preferences` | GET | — | `{theme, ...}` |
| `/api/preferences` | POST | `{key, value}` | `{ok: true}` |
| `/api/skills` | GET | — | `{skills: [...]}` |
| `/api/skills` | POST | `{name, description, category}` | `{ok: true}` |
