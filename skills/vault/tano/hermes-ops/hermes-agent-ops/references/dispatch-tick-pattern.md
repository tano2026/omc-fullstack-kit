# Dispatch Tick — HQ Queued Jobs Report

## Purpose
The dispatch tick reads queued jobs from `data/hq.db`, organizes them by priority (P0 → P1 → P2), and sends a structured Telegram report to the CEO. It runs as a Hermes cron job at 09:00 / 14:00 / 20:00 (see `scripts/cron_dispatch.py`).

## Cron execution
Use the standard cron-safe pattern (detailed in `references/cron-job-script-pattern.md`):
1. Read data directly from the HQ SQLite database
2. Build message inline (no helper function exists specifically for dispatch — unlike EOD/morning brief which have `hq.morning_brief()`)
3. Send via `hermes send --to telegram:<chat_id> --file <path>` — this uses the gateway's managed credentials and **always works**, unlike raw API calls which fail if the `.env` token is stale (401 Unauthorized)

## Database query

```python
import sqlite3

DB = r"D:\MMO Du an\TANO-AGENCY\PLATFORM\agent-core\data\hq.db"
conn = sqlite3.connect(DB)
conn.row_factory = sqlite3.Row
cur = conn.cursor()

queued = cur.execute("""
    SELECT * FROM jobs WHERE status='queued'
    ORDER BY CASE priority
        WHEN 'P0' THEN 0 WHEN 'P1' THEN 1 WHEN 'P2' THEN 2 ELSE 3
    END, created DESC
""").fetchall()
conn.close()
```

The `jobs` table schema (key columns):
| Column | Type | Purpose |
|--------|------|---------|
| `id` | INTEGER | Auto-increment job ID |
| `pack` | TEXT | Project pack (e.g. `abtrip`, `gmsp`, `noi-bo`) |
| `role` | TEXT | Target agent role (`dev`, `marketing`, `sales`, etc.) |
| `brief` | TEXT | Job description |
| `status` | TEXT | `queued`, `doing`, `done`, `review` |
| `priority` | TEXT | `P0` (critical), `P1` (high), `P2` (normal) |
| `created` | TEXT | Auto-set creation timestamp |

## Telegram format (priority-grouped)

```
🏢 *TANO HQ — Dispatch Tick*
⏰ <HH:MM DD/MM/YYYY>

📋 *Jobs đang chờ: <N>*

🔴 *P0 — <N> job (khẩn cấp)*
  • #<id> [<pack>/<role>] <brief[:80]>

🟡 *P1 — <N> job (cao)*
  • #<id> [<pack>/<role>] <brief[:80]>

🟢 *P2 — <N> job (thường)*
  • #<id> [<pack>/<role>] <brief[:80]>

---
✅ *Doing:* <N> · 🔄 *Review:* <N> · ✅ *Done:* <N>
💡 Gõ lệnh để giao việc hoặc OK/NO <job_id>
```

## Sending the report (in cron mode)

**DO NOT use raw Telegram API calls** — the token in `.env` may be stale/invalid (401 Unauthorized). Use `hermes send` instead, which uses the gateway's managed credentials:

```bash
# Step 1: Write the message to a temp file (via write_file tool)
# Step 2: Send via hermes send (from terminal tool)
hermes send --to telegram:762010475 --file /tmp/dispatch_report.txt
```

**Full cron-safe flow** (no `python -c`, no `execute_code`):
```python
# 1. Query DB + build message into a temp .txt file
from hermes_tools import write_file, terminal

write_file(
    path=r"D:\MMO Du an\TANO-AGENCY\PLATFORM\agent-core\scripts\_report_tmp.txt",
    content="...dispatch report text..."
)

# 2. Send via hermes send (uses gateway credentials, always works)
terminal("hermes send --to telegram:762010475 --file \"D:\\MMO Du an\\TANO-AGENCY\\PLATFORM\\agent-core\\scripts\\_report_tmp.txt\"")

# 3. Clean up
terminal("rm -f \"D:\\MMO Du an\\TANO-AGENCY\\PLATFORM\\agent-core\\scripts\\_report_tmp.txt\"")
```

To discover available Telegram targets:
```bash
hermes send --list telegram
# Shows: telegram:Nguyễn Ngọc Tân [762010475], telegram:Tan Tan [-1003887635890], etc.
```


## Status summary query

## Status summary query

```python
cur.execute("SELECT status, COUNT(*) as cnt FROM jobs GROUP BY status")
summary = {}
for r in cur.fetchall():
    summary[r["status"]] = r["cnt"]
```

## Key differences from other reports

| Report | Focus | Helper function | When |
|--------|-------|----------------|------|
| Dispatch Tick | Queued jobs by priority | None (inline) | 09:00 / 14:00 / 20:00 |
| Morning Brief | Pending approvals + escalations | `hq.morning_brief()` | 08:00 daily |
| EOD Report | Today's completed + in-progress | `hq.get_summary()` + inline | 17:00 daily |

## Pitfalls

- **sqlite3 CLI may not be in PATH** — always query via Python's `sqlite3` module
- **Inline `python -c` blocked in cron** — write temp `.py`, run via `terminal()`, then `rm -f`
- **Telegram 4096-char limit** — messages over 4096 chars must be chunked. The dispatch report is usually short (<1500 chars for 10+ jobs), but chunk defensively:
  ```python
  for i in range(0, len(msg), 4096):
      chunk = msg[i:i+4096]
      # send chunk
  ```
- **Markdown parsing errors** — send with `parse_mode=Markdown` first; if `ok=False`, resend as plain text
- **Priority ties** — within the same priority level, newer jobs (created DESC) come first. This is already handled by the SQL ORDER BY.
