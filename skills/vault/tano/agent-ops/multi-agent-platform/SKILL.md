---
name: tano-agency-architecture
description: "Full architecture reference for TANO-AGENCY platform — multi-agent OS, web dashboard, company HQ, VPS, projects"
---

# TANO-AGENCY Platform — Full Architecture Reference

## Latest State: 2026-07-19

The platform has evolved beyond the original 8-agent Telegram pipeline. Current architecture is 3 layers.

## Layer 1 — Core Engine (`agent-core/`)
Multi-agent Telegram bot (CEO + 8 departments), 7-stage pipeline, harness loop, SQLite memory.
Bot runs polling, `/gmsp` etc. for per-project session, `/thoát` to exit session, `/new` to reset.
See SKILL.md TL;DR section for full 7-stage pipeline detail.

## Layer 2 — Web Dashboard (`agent-core/dashboard/`)
FastAPI + Jinja2 SPA, mobile-first, single-screen with sidebar. Port 8138. Pass: `tano2026`.
- `/api/projects` — 5 projects (GMSP, Fast Track, ABTrip, Tử Vi, AirFares Decoded)
- `/api/hq/*` — Company HQ (7 tables: jobs, agents, approvals, etc.)
- `/api/chat` — CEO chat with per-project memory (SQLite)
- `/api/memory/*` — Facts, decisions, preferences, skills
- `/api/kanban` — Legacy kanban cards
- `/api/health` — PowerShell system stats (CPU, RAM, disk)

## Layer 3 — Company HQ (`dashboard/hq.py`)
401 lines. 7-table SQLite implementation of Airtable-style company operations.
See `references/company-hq-schema.md` for schema, functions, API endpoints, SQL pitfalls.

### Cron Schedule
Hermes cronjobs (no_agent=True) under `~/hermes/scripts/tano/`:
- 07:00 Morning Brief
- 09:00 / 14:00 / 20:00 Dispatch ticks
- 21:00 EOD Report
- T2 08:00 KPI Review (planned)

### Key Files
| File | Lines | Purpose |
|------|-------|---------|
| `dashboard/hq.py` | 401 | Company HQ 7 tables + functions |
| `dashboard/app.py` | 771 | FastAPI server (28 routes, incl. all /api/hq/) |
| `dashboard/project_memory.py` | 372 | Per-project facts, decisions, chat history |
| `dashboard/templates/dashboard.html` | ~5000 chars | SPA with sidebar, task feed, chat |
| `dashboard/image_gen.py` | 116 | FAL.ai image generation wrapper |
| `main.py` | ~500 | Telegram bot: CEO per-project memory, /gmsp etc. |
| `scripts/cron_*.py` | ~50 each | Cron job scripts for HQ rhythm |

## Layer 4 — Skill Library (`AI-Vibe-Toolkit/`)
Git repo `tano2026/AI-Vibe-Toolkit` (sync cron 9am daily).
Contains: ORG-v2, COORDINATION-v2, DECISION-MATRIX, OPERATING-RHYTHM, all role packs.
Push from local (Windows), pull from VPS.

## VPS
- IP: 100.64.173.75, path: `/opt/openclaw`
- OpenClaw + Claude Code (for heavy tasks)
- Infrastructure cron for Telegram notifications

## Projects (5)
1. **GMSP** 🚀 — Pipeline 7 bước, HyperFrames render, GMSP Writing Formula v2
2. **Fast Track** ✈️ — An Bình Fast Track Nội Bài, brand teal+gold, 3 bảng giá
3. **ABTrip** 🌴 — AGT API, chat UI per-project
4. **Tử Vi** 🔮 — Tử Vi + Kinh Dịch + Phong Thủy engine
5. **AirFares Decoded** ✈️ — Airfare education channel, KAYAK affiliate

## Governance
- Guard files: I/O guard (D:/MMO Du an, Desktop, Documents only), terminal guard (no dangerous commands), budget cap
- Decision Matrix: L0→L3 via approvals table
- Self-Learning: SQLite observations + instincts, auto-evolve at confidence ≥ 0.7

## Pitfalls
- SQL spacing bug in get_jobs(): prefix every clause with space
- sqlite3.Row has no .get() — use `row["field"]` or ` or ""`
- WAL mode on every connection to avoid "database is locked"
- Jinja2Templates bug with Python 3.14 + Starlette 1.3.1 — use raw jinja2.Environment
