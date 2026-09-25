# Project Memory System — Detailed Reference

## SQLite Schema (project_memory.db)

```sql
-- Per-project chat history
CREATE TABLE IF NOT EXISTS project_chat (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    project TEXT NOT NULL,
    role TEXT NOT NULL,
    content TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX IF NOT EXISTS idx_pc_project ON project_chat(project);
CREATE INDEX IF NOT EXISTS idx_pc_ts ON project_chat(created_at);

-- Global (non-project) chat
CREATE TABLE IF NOT EXISTS global_chat (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    role TEXT NOT NULL,
    content TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Facts (confirmed knowledge)
CREATE TABLE IF NOT EXISTS facts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    project TEXT NOT NULL DEFAULT '__global__',
    fact TEXT NOT NULL,
    category TEXT NOT NULL DEFAULT 'note',
    confidence REAL NOT NULL DEFAULT 1.0,
    source TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX IF NOT EXISTS idx_facts_project ON facts(project);
CREATE INDEX IF NOT EXISTS idx_facts_cat ON facts(project, category);

-- Decisions
CREATE TABLE IF NOT EXISTS decisions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    project TEXT NOT NULL DEFAULT '__global__',
    decision TEXT NOT NULL,
    context TEXT,
    status TEXT NOT NULL DEFAULT 'active',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX IF NOT EXISTS idx_dec_project ON decisions(project);

-- User preferences (key-value JSON)
CREATE TABLE IF NOT EXISTS preferences (
    key TEXT PRIMARY KEY,
    value TEXT NOT NULL,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Skills (cross-project reusable)
CREATE TABLE IF NOT EXISTS skills (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,
    description TEXT,
    category TEXT NOT NULL DEFAULT 'general',
    tools TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## Flow: Chat with Project Context

### 1. Detect project
```python
PROJECT_NAMES = {
    "gmsp": "GMSP", "giải mã": "GMSP", "giai ma": "GMSP",
    "abtrip": "ABTrip", "ab trip": "ABTrip",
    "tử vi": "Tử Vi", "tu vi": "Tử Vi", "bói": "Tử Vi",
    "airfare": "AirFares Decoded", "airfare decoded": "AirFares Decoded", "airfares": "AirFares Decoded",
    "fast track": "Fast Track", "nội bài": "Fast Track", "noi bai": "Fast Track",
    "trùm du lịch": "ABTrip", "trùm sân bay": "Fast Track",
}
```

### 2. Build context (injected into CEO system prompt)
```
=== DỰ ÁN HIỆN TẠI: GMSP ===
🧠 Kiến thức đã lưu:
- email: contact@gmsptv.com [contact]
- số đt: 0901234567 [contact]
- pipeline: Research→Script→TTS→Media→Render [note]

📋 Quyết định:
- 2026-07-19: Chốt EP01 base video chung cho mọi tập
- 2026-07-18: Dùng Resona TTS, ko BGM

=== KỸ NĂNG CÓ THỂ DÙNG ===
- GMSP Pipeline: 7-stage video production
- Vietnamese TTS: Edge TTS NamMinhNeural
- Image Gen: FAL dark academia

QUY TẮC RIÊNG CHO DỰ ÁN NÀY:
1. Chỉ trả lời về dự án được hỏi, KO lẫn sang dự án khác.
2. Khi biết thông tin mới, viết: [LƯU FACT: nội dung] [CATEGORY: contact/note/link]
3. Khi có quyết định, viết: [QUYẾT ĐỊNH: nội dung]
```

### 3. Auto-extract from user messages
```python
EMAIL_RE = re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b')
PHONE_RE = re.compile(r'(0|\+84)[3-9][0-9]{8}\b')
URL_RE = re.compile(r'https?://\S+')

if project:
    for email in EMAIL_RE.findall(message):
        add_fact(project, f"email: {email}", "contact", 1.0, "chat:auto_extract")
    for phone in PHONE_RE.findall(message):
        add_fact(project, f"số điện thoại: {phone}", "contact", 1.0, "chat:auto_extract")
    for url in URL_RE.findall(message):
        add_fact(project, f"link: {url}", "link", 0.9, "chat:auto_extract")
```

### 4. Parse CEO response brackets
```python
for line in response.split("\n"):
    if "[LƯU FACT:" in line:
        parts = line.split("[LƯU FACT:")[1].split("] [CATEGORY:")
        fact_text = parts[0].strip()
        cat = parts[1].split("]")[0].strip().lower() if len(parts) > 1 else "note"
        add_fact(project, fact_text, cat, 0.8, "chat:ceo_tele")
    if "[QUYẾT ĐỊNH:" in line:
        dec = line.split("[QUYẾT ĐỊNH:")[1].split("]")[0].strip()
        add_decision(project, dec)
```

## Dashboard Integration

### Sidebar project section
```javascript
function updateProjectsSidebar(){
  const el = document.getElementById('sidebar-projects');
  let html = '';
  projectsData.forEach(p => {
    const statusClass = p.status === 'active' ? 'green' : 'red';
    html += `<button class="sidebar-btn" onclick="openProjectModal('${p.name}')" title="${p.name}">
      ${p.icon}<span class="sb-label">${p.name}</span>
      <span class="status-dot ${statusClass}" style="margin-left:auto;flex-shrink:0"></span>
    </button>`;
  });
  el.innerHTML = html;
}
```

### Project modal (facts + decisions + inline chat)
```javascript
function openProjectModal(projectName){
  // Loads: /api/memory/facts?project=X + /api/memory/decisions?project=X
  // Renders: project info + facts list + decisions list + inline chat
  // chat uses session_type: projectName -> per-project history
}

function sendProjectChat(projectName){
  API.post('/api/chat', {
    message: text, 
    session_type: projectName,  // KEY: tells backend which project context to load
    session_id: 'proj_' + projectName
  });
}
```

## Telegram Integration (main.py)

Import pattern:
```python
import sys, os
sys.path.insert(0, os.path.join(BASE_DIR, "dashboard"))
from project_memory import (
    save_chat, load_chat_history,
    add_fact, get_facts,
    add_decision, get_decisions,
    build_project_context, extract_facts_from_message,
    get_skills,
)
```

`cmd_natural()` rewrite:
1. `_detect_project(text)` → get project name
2. `build_project_context(project)` → facts + decisions + skills
3. Inject into system prompt (per-project section)
4. `save_chat(project, ...)` after response
5. `extract_facts_from_message(project, text)` for auto-extraction
6. Parse `[LƯU FACT]` / `[QUYẾT ĐỊNH]` brackets from CEO response

## Port Conflict Recovery

```bash
# Find what's on port
netstat -ano | findstr ":8137"

# Kill
taskkill /F /PID 12345

# If TIME_WAIT persists (can take 2+ min):
# Either wait, or change port in app.py run()
def run():
    port = 8138  # <-- change to 8138
    uvicorn.run(app, host="0.0.0.0", port=port)
```

## Design Decisions

- **Why SQLite not vector DB:** Simple key-value + text search is enough for <100 facts per project. Vector adds complexity with no benefit at this scale.
- **Why shared DB (dashboard + tele):** Facts learned on Telegram appear on dashboard immediately and vice versa. Single source of truth.
- **Why bracket parsing not structured JSON:** CEO outputs natural text. Brackets are least-intrusive markup that can be regex-extracted without breaking the conversational flow.
- **Why keyword detection not ML classifier:** 5 projects → 5-10 keywords each → 100% accurate. ML would hallucinate and add latency.
- **Why per-project not per-agent:** The confusion was between projects (GMSP vs Airfare), not between agents (Dev vs Media). Per-agent would split the same conversation across multiple tables.
