# Dashboard 1-Person Company Layout — v4 (19/07/2026)

Thiết kế lại sau khi user chê giao diện cũ "nhàm quá, chả biết thông tin gì".

## Kiến trúc 4 tab

```
🏢 Văn Phòng  |  📋 Bảng Tin  |  🏛️ Phòng Họp  |  💬 Chat
```

### Tab 🏢 Văn Phòng — Agent office grid

9 agent cards in 2-col (mobile) / 3-col (desktop) grid. Each card has:
- Accent color bar (ceo=gold, dev=cyan, sales=orange, marketing=pink, ops=purple, support=green, analytics=blue, media=red, research=teal)
- Large emoji icon
- Agent name + role subtitle
- Status dot: 🟢 if has running tasks, 🟡 if idle, 🔴 if blocked
- Task count badge

Click → **full-page scrollable modal**:

```
┌────────────────────────────┐
│  👤 TÔI LÀ AI              │
│  Vietnamese introduction    │
├────────────────────────────┤
│  🎯 NHIỆM VỤ CỦA TÔI       │
│  Mission statement          │
├────────────────────────────┤
│  🛠️ TÔI CÓ GÌ              │
│  [Tool1] [Tool2] [Tool3]    │
│  Skills: ...               │
├────────────────────────────┤
│  📋 TÔI ĐANG LÀM GÌ        │
│  • Task 1 (running)        │
│  • Task 2 (review)          │
│  (fetched from kanban)      │
├────────────────────────────┤
│  [💬 Chat với tôi]          │
│  → switches to Chat tab     │
└────────────────────────────┘
```

### Tab 📋 Bảng Tin — Live task feed

Fetches ALL kanban cards with state != merged/archived. Shows:
- Agent icon + name
- Task title
- Time ago (from created_at timestamp)
- State badge (running/review/backlog/blocked)
- Auto-refresh every 30s

### Tab 🏛️ Phòng Họp — Projects + Weekly Plan + Alerts

- 5 project cards from /api/projects (GMSP, Fast Track, ABTrip, Tử Vi, AirFares Decoded)
- Each: icon, name, status (active/inactive), path
- "Kế Hoạch Sắp Tới" — hardcoded weekly plan:
  - Thứ 2: Họp CEO — review tiến độ GMSP
  - Thứ 3: Check ticket tồn
  - Thứ 4: Review content AirFares Decoded
  - Thứ 5: Họp dự án — cập nhật Kanban
  - Thứ 6: Báo cáo cuối tuần
- "Cảnh Báo" — check /api/health, warn if disk_c > 90%

### Tab 💬 Chat — same as before

## Agent Profiles (hardcoded in JS)

9 profiles with Vietnamese descriptions. Each has: intro, mission, tools (as tag chips), skills text.

## Chat History — SQLite

**Switched from in-memory dict to SQLite after user complained "F5 phát lại mất hết".**

```python
def _ensure_chat_db():
    conn = sqlite3.connect("data/chat_history.db")
    conn.execute("""CREATE TABLE IF NOT EXISTS chat_history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        session_id TEXT NOT NULL,
        role TEXT NOT NULL,
        content TEXT NOT NULL,
        created_at REAL DEFAULT (strftime('%%s','now'))
    )""")
    conn.execute("CREATE INDEX IF NOT EXISTS idx_chat_session ON chat_history(session_id, id)")

def _load_chat_history(session_id, limit=20):
    rows = conn.execute(
        "SELECT role, content FROM chat_history WHERE session_id=? ORDER BY id DESC LIMIT ?",
        (session_id, limit)
    ).fetchall()
    return [{"role": r["role"], "content": r["content"]} for r in reversed(rows)]

def _save_chat_message(session_id, role, content):
    conn.execute("INSERT INTO chat_history (session_id, role, content) VALUES (?,?,?)", ...)
```

Two session IDs used: `dashboard_quick` (inline chat), `dashboard_tab` (full tab). Max 20 messages sent to LLM to stay under token limit.

## Dashboard Deploy Pitfall

After updating `app.py` or `dashboard.html`:
1. Old `__pycache__` files serve stale code — must clear ALL pycache in agent-core tree
2. Zombie Python processes hold port 8137 — kill by PID from `netstat -ano | grep 8137`
3. Triple-verify: `netstat` then `curl /api/projects` 