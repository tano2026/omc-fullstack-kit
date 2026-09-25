# Per-Project Chat Isolation

## Problem

CEO bot on Telegram uses 1 LLM session per user. If user asks about AirFares then GMSP, the LLM's context window still has AirFares history → responses bleed between projects.

## Solution

1. **SQLite per-project chat storage** — `project_chat` table has a `project` column
2. **Session locking** — user locks to 1 project via `/gmsp` etc
3. **Context injection** — only facts + decisions + chat history of the ACTIVE project go into the LLM system prompt

## Code pattern

### Dashboard (`/api/chat`)

```python
@app.post("/api/chat")
async def api_chat(request):
    body = await request.json()
    message = body.get("message", "")
    session_type = body.get("session_type", "")  # "GMSP", "ABTrip", "" = global
    session_id = body.get("session_id", "dashboard")
    
    if session_type:
        context = build_project_context(session_type)
        # Inject into system prompt
        system += f"=== DỰ ÁN HIỆN TẠI: {session_type} ===\n{context}\n"
        system += "QUY TẮC: Chỉ trả lời về dự án được hỏi, KO lẫn sang dự án khác.\n"
        # Load chat history for THIS project only
        history = load_chat_history(session_type, 10)
    
    # ... call LLM ...
    save_chat(session_type, "user", message)
    save_chat(session_type, "assistant", response)
    extract_facts_from_message(session_type, message)
```

### Telegram bot (`cmd_natural`)

```python
project = _project_sessions.get(chat_id) or _detect_project(text)
if project:
    context = build_project_context(project)
    system += f"=== DỰ ÁN HIỆN TẠI: {project} ===\n{context}\n"

out = llm.chat(text, system=system, ...)
save_chat(project, "user", text)
save_chat(project, "assistant", out or "")
if project:
    extract_facts_from_message(project, text)
    # Parse [LƯU FACT] and [QUYẾT ĐỊNH] tags
```

## Dashboard sidebar integration

In `updateProjectsSidebar()`:
```javascript
projectsData.forEach(p => {
    html += `<button class="sidebar-btn" onclick="openProjectModal('${p.name}')">
      ${p.icon}<span class="sb-label">${p.name}</span>
      <span class="status-dot ${p.status === 'active' ? 'green' : 'red'}" style="margin-left:auto"></span>
    </button>`;
});
```

Project modal loads:
- Facts from `/api/memory/facts?project=X`
- Decisions from `/api/memory/decisions?project=X`
- Inline chat with `session_type: projectName` and `session_id: 'proj_' + projectName`
- Button "🧠 Thêm kiến thức" → manual fact entry via prompt → POST `/api/memory/facts`

## DB Schema

```sql
CREATE TABLE project_chat (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    project TEXT NOT NULL DEFAULT '',  -- 'GMSP', 'ABTrip', ''=global
    role TEXT NOT NULL,                -- 'user' | 'assistant'
    content TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE facts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    project TEXT NOT NULL DEFAULT '',
    fact TEXT NOT NULL,
    category TEXT DEFAULT 'note',      -- 'contact', 'link', 'note', 'config'
    confidence REAL DEFAULT 0.5,
    source TEXT DEFAULT '',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE decisions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    project TEXT NOT NULL DEFAULT '',
    decision TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```
