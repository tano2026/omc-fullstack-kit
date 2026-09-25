# Chat CEO History — SQLite (19/07/2026)

## Vấn đề

Chat history được lưu trong RAM (`_CHAT_HISTORY: dict[str, list[dict]]`). F5 hoặc restart server → mất toàn bộ lịch sử trò chuyện.

User phản hồi: "F5 phát lại là mất hết"

## Fix: SQLite

Chuyển từ in-memory dict sang SQLite table `chat_history` trong `data/chat_history.db`.

### Schema

```sql
CREATE TABLE IF NOT EXISTS chat_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id TEXT NOT NULL,
    role TEXT NOT NULL,
    content TEXT NOT NULL,
    created_at REAL DEFAULT (strftime('%s','now'))
);
CREATE INDEX IF NOT EXISTS idx_chat_session ON chat_history(session_id, id);
```

### Code pattern (dashboard/app.py)

```python
_CHAT_DB = DATA / "chat_history.db"
_MAX_HISTORY = 20  # 10 lượt hỏi-đáp tối đa

def _ensure_chat_db():
    conn = sqlite3.connect(str(_CHAT_DB))
    conn.execute("CREATE TABLE IF NOT EXISTS ...")
    conn.commit(); conn.close()

def _load_chat_history(session_id, limit=20):
    conn = sqlite3.connect(str(_CHAT_DB))
    conn.row_factory = sqlite3.Row
    rows = conn.execute(
        "SELECT role, content FROM chat_history WHERE session_id=? ORDER BY id DESC LIMIT ?",
        (session_id, limit)
    ).fetchall()
    conn.close()
    return [{"role": r["role"], "content": r["content"]} for r in reversed(rows)]

def _save_chat_message(session_id, role, content):
    conn = sqlite3.connect(str(_CHAT_DB))
    conn.execute("INSERT INTO chat_history (session_id, role, content) VALUES (?,?,?)", (session_id, role, content))
    conn.commit(); conn.close()
```

### API flow

1. `_ensure_chat_db()` ở đầu mỗi request
2. Load history từ SQLite (reversed desc → asc order)
3. Gửi messages (system + history + current) lên LLM
4. Lưu user + assistant messages vào SQLite

## Key points

- Không giới hạn. SQLite lưu tất cả.
- Chỉ load 20 messages gần nhất (10 lượt) để gửi lên LLM — token budget
- session_id client gửi lên để phân biệt các cuộc trò chuyện (dashboard_quick vs dashboard_tab)
- Không cần trim. SQLite disk nhỏ (chat text ~1KB/lượt, 1000 lượt = 1MB)
