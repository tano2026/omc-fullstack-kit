# Claude Company v2 — Merge Guide

Claude (via AI-Vibe-Toolkit repo, commit `d4de1cb`) designed a full company operating system for the one-person company. This doc captures what it is, how it differs from the current TANO-AGENCY system, and how to merge them.

## Where to Find the Files

All at `D:\MMO Du an\AI-Vibe-Toolkit\agents\company\`:
- `ORG-v2.md` — 121 lines, replaces ORG.md
- `COORDINATION-v2.md` — 204 lines, replaces COORDINATION.md
- `OPERATING-RHYTHM.md` — 93 lines, new
- `DECISION-MATRIX.md` — 85 lines, new
- `roles/ops-finance.md` — new role pack

## What Claude Designed

### ORG v2 — 8 AI Roles (added Ops & Finance)

| # | Role | LLM Tier | KPI |
|---|------|----------|-----|
| 1 | Research & Analytics | reasoning | Insight reports cited by other roles |
| 2 | Marketing | balanced | Lead/traffic vs target |
| 3 | Sales | balanced | Deals closed + pipeline value |
| 4 | Content Creator | creative | Content ready-to-publish on time |
| 5 | Dev & Automation | balanced (coding) | Uptime 3 runtimes + tickets <7d |
| 6 | Designer | creative | Visuals on spec, reusable templates |
| 7 | Media | cheap | Posts on schedule + engagement |
| 8 | Ops & Finance | cheap→balanced | Orders <SLA + P&L 100% updated |

**Key change:** Ops & Finance added — no one was tracking fulfillment or P&L. Dev moved to infrastructure layer (serves all roles, not a standalone job role). Each role has JD / KPI / SOP / escalation rule.

### COORDINATION v2 — 7-Table Schema (Airtable `company-hq`)

Originally designed for Airtable, the schema is database-agnostic and can be adapted to SQLite:

| Table | Purpose | Key Fields |
|-------|---------|------------|
| `agents` | Staff roster | role, runtime, model_tier, role_pack_url, status, kpi_chinh, escalation_rule |
| `jobs` | Heart of the system | job_id, pack, role, brief, status (queued→doing→review→awaiting_approval→done/blocked), priority (P0/P1/P2), output_url, depends_on, requested_by, sop, due |
| `sops` | Procedure library | sop_id, name, role, trigger, steps, version |
| `kpis` | Scoreboard | metric, pack, role, target, actual, week, note |
| `approvals` | Approval gate | job_id, action, risk_type, risk_level (L2/L3), status (pending/approved/rejected/expired) |
| `escalations` | Incident log | ts, job_id, role, reason, resolution, resolved |
| `activity_log` | Append-only audit | ts, role, job_id, event, tokens |

**5 required Airtable views:** CEO Cockpit (awaiting_approval + blocked + done in 24h), Queue by role, Client view, KPI this week, Pending approvals.

**Job lifecycle (6 steps):**
1. CEO Telegram: `/job [PACK: x] role=y P1 due=T5 — brief 5 phần`
2. OpenClaw dispatch → status=queued→doing
3. Runtime pushes artifact → output_url → status=review
4. Review chéo → done (safe) OR awaiting_approval (risky) OR back to doing
5. Telegram approval: `OK 12` / `NO 12` / expired (24h = cancel)
6. Blocked >24h or 3x error → auto escalate to next morning brief

**Review chéo matrix:**
| Output from | Reviewer | Check |
|------------|----------|-------|
| Content | Research | Claims sourced |
| Designer | Content | Message + brand voice correct |
| Media (schedule) | Marketing | Right channel, frequency, project |
| Sales (outreach) | Marketing | Positioning + pricing correct |
| Marketing (ad spend) | Research | Base data verified |
| Ops & Finance (weekly) | Research | P&L matches activity_log + revenue source |

### OPERATING RHYTHM — Daily & Weekly Schedule

**Daily:**
| Time | Task | Runner | Output |
|------|------|--------|--------|
| 06:45 | Healthcheck 3 runtimes | Antigravity | Telegram ONLY on failure (silent = healthy) |
| 07:00 | **Morning Brief** | OpenClaw | Telegram CEO (≤12 lines) |
| 08:00 | Research daily scan (rotating domain) | Hermes | .md → repo |
| 09:00 | Dispatch tick #1 | OpenClaw | activity_log |
| 14:00 | Dispatch tick #2 + approval reminders | OpenClaw | Telegram if pending |
| 18:00 | Media pull engagement metrics | Hermes | Update kpis.actual |
| 20:00 | Dispatch tick #3 (P2 tasks) | OpenClaw | activity_log |
| 21:00 | **EOD Report** | OpenClaw | Telegram CEO: X done / Y doing / Z blocked / N pending |

**Research scan rotation:** T2=abtrip+an-binh, T3=trum-san-bay, T4=airfare-decoded, T5=gmsp, T6=ai-review, T7=competitor synthesis, CN=off (weekly report).

**Weekly:**
| When | Task | Runner | Output |
|------|------|--------|--------|
| T2 08:00 | **KPI Review** — previous week actual vs target | OpenClaw | Telegram: ≤8 lines + roles <70% target |
| T2 08:00 | Weekly priority: 3 most important jobs | OpenClaw proposes, CEO decides | CEO chốt in Telegram |
| T6 16:00 | Content calendar next week (all channels) | Content + Media | 1 batch approval |
| CN 20:00 | Weekly report by pack + by role + token usage (P&L) | Hermes | .md → repo/reports/ |
| CN 20:30 | Ops & Finance close week: revenue/expense by domain | Hermes | Line item in T2 morning brief |

**5 numbers on CEO desk every T2:**
1. Revenue last week by domain (Ops & Finance)
2. Jobs done / total (throughput)
3. KPI roles <70% target (red flags)
4. Token usage & % free tier (Dev)
5. 3 recommended priority jobs this week

### DECISION MATRIX — 4 Levels L0→L3

| Level | Name | Mechanism |
|-------|------|-----------|
| L0 | Auto | Do it, no questions, no logging |
| L1 | Auto + log | Do it, log to activity_log |
| L2 | Review → CEO approve | Cross-review → approval record → `OK <job-id>` |
| L3 | CEO decides from start | ASK before doing, don't draft-then-ask |

**3 inviolable red lines:**
1. AI cannot spend money
2. AI cannot publish public content
3. AI cannot commit to customers (pricing, deadlines, scope)

**Anti-prompt-injection:** Any job with scraped content input (web/comment/email) → all L1+ actions auto-upgrade 1 level.

### ops-finance.md — New Role Pack

Covers: Order fulfillment (Fast Track bookings, Tano Cafe orders), P&L by domain, invoice/receipt tracking, weekly close-out reports. LLM tier: cheap→balanced (cheap for routine ops, balanced for financial analysis).

## Key Differences vs Current TANO-AGENCY

| Aspect | Current (TANO-AGENCY) | Claude (AI-Vibe-Toolkit) |
|--------|----------------------|--------------------------|
| **State/DB** | SQLite local (project_memory.db, agent_kanban.db) | Airtable `company-hq` (7 tables) |
| **Giao diện** | Dashboard web localhost:8138 | Telegram CEO + 1 Airtable view |
| **CEO chat** | Per-project memory SQLite, facts/decisions | OK/NO `<job-id>` via Telegram |
| **Job track** | Kanban 5 cột | Jobs lifecycle 6 bước |
| **Dispatch** | Manual + auto cron | OpenClaw 3x/ngày dispatch tick |
| **Schedule** | 7 Hermes cron jobs | 8 cron slots (Antigravity crontab) |
| **Roles** | 9 agents (Dev standalone) | 8 roles (Dev=infra, added Ops&Finance) |
| **Decision** | CEO via chat confirm | 4-level matrix L0-L3 |
| **Anti-injection** | Dev guards (file I/O + terminal) | Decision-level: scraped → +1 level |

## Merge Strategy

**Keep SQLite as backbone, adopt Claude's structure + rhythm.**

### Phase 1 — Add Claude's 7-table schema to SQLite
Add tables: `jobs`, `sops`, `kpis`, `approvals`, `escalations`, `activity_log` to existing `data/project_memory.db`. See `COORDINATION-v2.md` for full schema.

### Phase 2 — Adopt ORG v2
- Add **Ops & Finance** adapter in `real_adapters.py`
- Dev → infrastructure layer (no standalone job role)
- Update CEO system prompt with 8-role org chart

### Phase 3 — Implement operating rhythm as Hermes cron
- `morning-brief.py` (07:00), `dispatch-tick.py` (09/14/20), `eod-report.py` (21:00)
- `kpi-review.py` (T2), `content-calendar-reminder.py` (T6)

### Phase 4 — Decision Matrix integration
- `risk_level` field in kanban/approval flow
- `OK <job-id>` approval parsing
- Auto-nâng level khi input có scraped content

## Principles to Adopt

1. **CEO nhìn 1 view duy nhất mỗi sáng** — Morning Brief ≤12 lines
2. **5 numbers every T2** — revenue, throughput, red KPIs, token cost, 3 priorities
3. **No approval record = no execution** — written approval only
4. **Scraped content → decision level +1** — anti-prompt-injection
5. **3 red lines** — AI can't spend/publish/commit
6. **Silent = healthy** — healthchecks only on failure

## Recommended First Job (from Claude)

> **1 TikTok video Trùm Sân Bay quảng bá Fast Track Nội Bài.** Proven pipeline (GMSP EP01), runs 4 roles (Research→Content→Designer→Media), hits real approval (publish=L2), costs $0, revenue-connected.
