# ABTrip Architecture — Fragmentation & Consolidation Plan

> Discovered: 6 Jul 2026

## Current Fragmented State

The ABTrip product exists as **4 separate components** across 2 machines for what should be 1 product:

```
         FRONTEND                          BACKEND
    ┌──────────────────┐            ┌──────────────────┐
VPS │ chat.html (486 dòng)│  ─/api──▶│ FastAPI :8138     │
    │ static, /opt/abtrip- │          │ systemd auto      │
    │ backend/static/      │          │ /opt/abtrip-backend│
    └──────────────────┘            └──────────────────┘
    ┌──────────────────┐            ┌──────────────────┐
Local│ Next.js :4321     │  ─/api──▶│ FastAPI :8138     │
    │ ~/agent.tkt/frontend│         │ ~/agent.tkt/backend│
    │ components, routing │          │ chạy tay          │
    └──────────────────┘            └──────────────────┘
```

## VPS Architecture (100.64.173.75)

### Nginx Routing Table
```
server {
    listen 80 default_server;

    location /           → /opt/abtrip-backend/static/chat.html  (SmartAgent)
    location /api/       → proxy_pass http://127.0.0.1:8138       (ABTrip backend)
    location /tuvi/      → proxy_pass http://127.0.0.1:8149/     (Tử Vi)
    location /toonflow/  → proxy_pass http://127.0.0.1:8787/     (ToonFlow)
    location /n8n/       → proxy_pass http://127.0.0.1:5678      (n8n)
    location /thoigianbieu/ → proxy_pass http://127.0.0.1:5000
}
```

### Systemd Services
- `abtrip-backend.service`: `/opt/abtrip-backend/.venv/bin/python -m uvicorn app.main:app --host 0.0.0.0 --port 8138 --workers 1`
- `gmsp-dashboard.service`: GMSP (Tử Vi dashboard) on port 8137 — **separate project, do NOT merge**
- `nginx.service`: Routes all traffic

### Key Paths
| Path | Purpose |
|------|---------|
| `/opt/abtrip-backend/` | Backend code + static frontend (chat.html) |
| `/opt/abtrip-backend/static/chat.html` | SmartAgent — single-file HTML (486 lines) |
| `/opt/abtrip-backend/.venv/` | Python virtualenv (Ubuntu 24.04 externally-managed) |
| `/opt/abtrip/` | Empty — intended for frontend, never populated |
| `/opt/gmsp-dashboard/` | GMSP — separate project, port 8137 |
| `/opt/openclaw/` | OpenClaw instance (Hermes #2) |

## Local Architecture (Windows)

| Path | Purpose |
|------|---------|
| `~/agent.tkt/backend/` | FastAPI backend clone |
| `~/agent.tkt/frontend/` | Next.js 14 frontend (richer than chat.html) |
| `~/agent.tkt/docker-compose.local.yml` | Docker Compose (unused — no Docker) |

## Consolidation Plan

Goal: **1 repo, 1 deploy target**

| Step | Action |
|------|--------|
| 1 | Merge VPS backend + local Next.js frontend into single `agent.tkt` repo |
| 2 | Build Next.js → static export, deploy to VPS replacing `chat.html` |
| 3 | Keep VPS as production backend (systemd), local for dev only |
| 4 | Nginx: point `/` to Next.js static export instead of `chat.html` |
| 5 | Remove local backend clone (or keep as dev-only with local .env) |

**Result**: 1 repo `tano2026/agent.tkt`, 1 backend (VPS :8138), 1 frontend (Next.js via nginx :80)

## SmartAgent vs ABTrip Differences

| Feature | SmartAgent (VPS) | ABTrip (Local) |
|---------|-----------------|----------------|
| Frontend | Static HTML (486 lines) | Next.js 14 (components, TS, routing) |
| Services | 5 cards (Fly, FastTrack, eSIM, Visa, Passport) | 3 tabs (Fly, eSIM, Visa & Passport) |
| Chat | Fetch-based, no streaming | SSE streaming via `/api/chat/stream` |
| Pages | Single page | Multi-page: search, book, booking detail |
| Backend API | Same — both call `/api/chat` on :8138 | Same |
