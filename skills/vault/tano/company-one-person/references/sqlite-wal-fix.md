# SQLite WAL Mode Fix for Dashboard Kanban (Jul 2026)

## Problem
When adding or moving kanban cards via POST endpoints (`/api/kanban/add`, `/api/kanban/move`), concurrent access by multiple Python processes caused:
```
sqlite3.OperationalError: database is locked
```

## Root Cause
Default SQLite journal mode (DELETE) creates a lock file (`agent_kanban.db-journal`) that blocks concurrent writes. Multiple FastAPI workers or the main Telegram bot process both write to the same `data/agent_kanban.db`.

## Fix: WAL mode + timeout

```python
@app.post("/api/kanban/add")
async def api_kanban_add(request: Request):
    conn = sqlite3.connect(str(DATA / "agent_kanban.db"), timeout=10)
    conn.execute("PRAGMA journal_mode=WAL")  # Enable WAL mode
    conn.execute(
        "INSERT INTO agent_cards (title, owner, state) VALUES (?, ?, ?)",
        (body.get("title", ""), body.get("owner", "unassigned"), body.get("state", "backlog"))
    )
    conn.commit()
    conn.close()
    return JSONResponse({"ok": True})
```

## Key points
- `PRAGMA journal_mode=WAL` must be called on EACH connection
- `timeout=10` gives 10 seconds retry before raising OperationalError
- WAL mode allows concurrent reads + writes (writers don't block readers)
- Apply to BOTH add and move endpoints
- Does NOT affect existing reads via `query_db()` helper (those use `with` context manager)
- WAL creates two additional files: `agent_kanban.db-wal` and `agent_kanban.db-shm` (managed automatically)
