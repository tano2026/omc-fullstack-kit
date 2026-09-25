# Company HQ — 7-Bảng SQLite + Job Lifecycle

Phiên bản implement thực tế của mô hình Claude COORDINATION-v2 + ORG-v2 + DECISION-MATRIX trong SQLite local (ko cần Airtable).

## Schema Overview

File: `dashboard/hq.py` — 401 lines, module `hq.py`.

### 7 Tables

| Table | Fields | Mục đích |
|-------|--------|----------|
| `agents` | id, role, runtime, model_tier, role_pack_url, status, kpi_chinh, escalation_rule | Sổ nhân sự AI (seed 8 roles) |
| `jobs` | id, pack, role, brief, status, priority, output_url, depends_on, requested_by, sop, due, created, updated | Job queue + lifecycle |
| `sops` | id, name, role, trigger, steps, version, updated | Thư viện quy trình chuẩn |
| `kpis` | id, metric, pack, role, target, actual, week, note | KPI weekly theo role × domain |
| `approvals` | id, job_id, action, risk_type, risk_level, status, decided_at | Cổng duyệt CEO |
| `escalations` | id, job_id, role, reason, resolution, resolved, created | Sự cố cần CEO |
| `activity_log` | id, role, job_id, event, tokens, ts | Append-only audit trail |

### Seed 8 Agents

```python
roles = [
    ("research", "hermes", "reasoning", "Nghiên cứu thị trường, insight cho các role khác"),
    ("marketing", "hermes", "balanced", "Chiến lược kênh, lead/traffic, content calendar"),
    ("sales", "hermes", "balanced", "Tư vấn, báo giá, chốt deal, CSKH trước bán"),
    ("content", "hermes", "creative", "Script, bài viết, kịch bản video"),
    ("designer", "hermes", "creative", "Visual, thumbnail, brand identity"),
    ("media", "hermes", "cheap", "Đăng bài, lịch đăng, engagement"),
    ("dev", "hermes", "balanced", "Hạ tầng, tool, automation cho 7 role"),
    ("ops-finance", "hermes", "cheap", "Fulfillment đơn, sổ thu chi, P&L theo domain"),
]
```

### Key Functions

```python
# Jobs CRUD
create_job(pack, role, brief, priority="P2", requested_by="ceo", due="") -> job_id
get_jobs(status=None, pack=None, role=None, limit=50) -> list[dict]
get_job(job_id) -> dict | None
move_job(job_id, to_status)  # queued → doing → review → awaiting_approval → done
set_job_url(job_id, url)

# Approvals
create_approval(job_id, action, risk_type="publish", risk_level="L2")
get_pending_approvals(limit=20) -> list[dict]  # JOIN with jobs
approve(job_id, decision)  # "approved" → done | "rejected" → doing

# Escalations
create_escalation(job_id, role, reason)
get_open_escalations() -> list[dict]  # JOIN with jobs

# KPIs
set_kpi(metric, pack, role, target, week)
update_kpi(kpi_id, actual, note)
get_kpis(week=None) -> list[dict]  # default = current ISO week

# SOPs
create_sop(name, role, trigger, steps)
get_sops(role=None) -> list[dict]

# Activity
log_activity(role, job_id, event, tokens=0)
get_activity(limit=50, since=None) -> list[dict]

# Summary
get_summary() -> dict {status: count, "total": N}

# Morning Brief
morning_brief() -> str  # Formatted Telegram message
```

### Database

- Path: `agent-core/data/hq.db`
- WAL mode + foreign keys ON
- Init on import: `init()` creates tables + seeds 8 agents

## Job Lifecycle

```
CEO tạo job via Telegram /dashboard
    │ create_job()
    ▼
queued ──→ doing ──→ review ──→ awaiting_approval ──→ done
                             │                          ↑
                             └── rejected ──────────────┘
```

1. **queued** — Created by CEO, waiting dispatch
2. **doing** — Dispatch tick assigned to agent
3. **review** — Agent finished, cross-review needed
4. **awaiting_approval** — Has approval record pending CEO OK/NO
5. **done** — Approved + executed (or no-approval needed)
6. **blocked** — Escalated, waiting CEO decision

Default sort: priority (P0→P2) then created DESC.

## Decision Matrix (L0→L3)

From DECISION-MATRIX.md, implemented in approval flow:

| Level | Name | Mechanism | Example |
|-------|------|-----------|---------|
| L0 | Auto | No log | Internal draft |
| L1 | Auto + log | `log_activity()` | Free tier usage |
| L2 | CEO approve | `create_approval()` → `OK job_id` | Publish content, spend money |
| L3 | CEO decide first | Must ask before acting | Pricing, delete data, change SOP |

**3 red lines (never auto):** AI cannot spend money, publish public, or commit to customers.

## Operating Rhythm (Cron Schedule)

| Time | Job | Script | Hermes Cron |
|------|-----|--------|-------------|
| 06:45 | Healthcheck | (not yet) | - |
| 07:00 | Morning Brief | `cron_morning_brief.py` | ✅ `0 7 * * *` |
| 09:00 | Dispatch #1 | `cron_dispatch.py` | ✅ `0 9 * * *` |
| 14:00 | Dispatch #2 | `cron_dispatch.py` | ✅ `0 14 * * *` |
| 20:00 | Dispatch #3 | (not yet) | - |
| 21:00 | EOD Report | (not yet) | - |
| T2 08:00 | KPI Review | (not yet) | - |

### Hermes Cron Pattern (no_agent=True)

```bash
# Copy script to Hermes scripts dir
cp scripts/*.py ~/AppData/Local/hermes/scripts/tano/

# Register via cronjob tool:
#   no_agent=true  → script stdout = delivery message
#   script="tano/<file>"  → relative to ~/hermes/scripts/
#   prompt required even for no_agent
```

## API Endpoints (from app.py)

All under `/api/hq/`:
- `GET /api/hq/summary` — Job counts by status
- `GET /api/hq/jobs` — List with filters (?status=queued,doing&pack=gmsp&role=content)
- `GET /api/hq/jobs/{id}` — Single job
- `POST /api/hq/jobs` — Create job
- `POST /api/hq/jobs/{id}/move` — Move status
- `GET /api/hq/approvals` — Pending approvals
- `POST /api/hq/approvals/{id}/approved` — Approve
- `POST /api/hq/approvals/{id}/rejected` — Reject
- `GET /api/hq/escalations` — Open escalations
- `GET /api/hq/kpis` — KPI table
- `GET /api/hq/agents` — Agent roster
- `GET /api/hq/sops` — SOP library
- `GET /api/hq/activity` — Activity log
- `GET /api/hq/brief` — Morning Brief text

## Pitfalls

### SQL Spacing Bug
`get_jobs()` constructs SQL by joining list parts. Initial version had:
```
"WHERE " + " AND ".join(where)  → "jobsWHERE" (no space)
"ORDER BY..." → "DESCLIMIT" (no space)
```
Fix: prefix every clause with a space:
```python
parts.append(" WHERE " + " AND ".join(where))
parts.append(" ORDER BY ...")
parts.append(str(f" LIMIT {limit}"))
```

### sqlite3.Row Caveats
- `sqlite3.Row` has NO `.get()` method — use `row["field"] or ""`
- Always use `row_factory = sqlite3.Row` for dict-like access
- Tuple params: `.execute(sql, tuple(params))` — list is deprecated in Python 3.14

### WAL Mode
Add `PRAGMA journal_mode=WAL` and `PRAGMA foreign_keys=ON` on every connection to avoid "database is locked" errors.

## Files
- `dashboard/hq.py` — Full implementation (401 lines, init on import)
- `dashboard/app.py` — 14 endpoints at `/api/hq/*` (lines 672-754)
- `scripts/cron_morning_brief.py` — Morning Brief generator
- `scripts/cron_dispatch.py` — Dispatch tick (take queued → doing)
- `scripts/cron_eod.py` — EOD report generator
