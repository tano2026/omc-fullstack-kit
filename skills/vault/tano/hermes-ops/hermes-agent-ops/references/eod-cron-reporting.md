# EOD Cron Reporting — HQ Database

## Location
`data/hq.db` under agent-core root: `D:\MMO Du an\TANO-AGENCY\PLATFORM\agent-core\data\hq.db`

## Tables (for reporting)
| Table | Purpose |
|-------|---------|
| `jobs` | All tasks — key columns: `id`, `pack`, `role`, `brief`, `status`, `priority`, `created`, `updated` |
| `approvals` | Approval decisions — `job_id`, `action`, `risk_type`, `risk_level`, `status`, `decided_at` |
| `activity_log` | Event log — `role`, `job_id`, `event`, `ts` |

## Job status values
- `done` — completed
- `doing` — in progress
- `queued` — waiting for dispatch
- `review` — awaiting CEO approval

## Priority levels
- `P0` — critical
- `P1` — high
- `P2` — normal

## Cron-safe querying (no sqlite3 CLI)

The `sqlite3` CLI binary may not be in PATH. `python -c "..."` is **blocked by cron mode** (config: `approvals.cron_mode`). The safe pattern:

```bash
# Write query script, then run it
python eod_report.py
```

Script pattern:
```python
import sqlite3, datetime

today = datetime.date.today().isoformat()
conn = sqlite3.connect("D:/MMO Du an/TANO-AGENCY/PLATFORM/agent-core/data/hq.db")
conn.row_factory = sqlite3.Row
c = conn.cursor()

# Today's jobs
c.execute("SELECT * FROM jobs WHERE date(created) = date(?)", (today,))
today_jobs = c.fetchall()

# Status distribution
c.execute("SELECT status, COUNT(*) FROM jobs GROUP BY status")
status_counts = dict(c.fetchall())

# Doing / Review details
c.execute("SELECT * FROM jobs WHERE status IN ('doing','review') ORDER BY priority")
active = c.fetchall()

conn.close()
```

## EOD report format (Telegram, ≤10 lines)

```
📊 EOD Report — <DAY> <DD/MM/YYYY>

✅ Done hôm nay: <N> jobs (<summary>)
🔄 Doing: <brief> (<priority>)
⏳ Chờ duyệt (review): <brief> (<priority>)
📋 Queued: <N> jobs (<top brief>)
⚠️ Blocked: <N> / none
💡 Highlight: <one-liner>
```

## Morning Brief vs EOD

The **morning brief** (`dashboard/hq.morning_brief()`) and **EOD report** serve different purposes:

| Brief | When | Content |
|-------|------|---------|
| Morning Brief | 08:00 daily | Pending approvals + escalations + status counts + CEO action prompts |
| EOD Report | 17:00 daily | Today's done jobs + in-progress + queued count + highlights |

Both use the same cron-safe script pattern detailed in `references/cron-job-script-pattern.md`.

## Cleanup
Always delete temp `.py` files after running: `rm -f ~/eod_report.py ~/eod_detail.py`
