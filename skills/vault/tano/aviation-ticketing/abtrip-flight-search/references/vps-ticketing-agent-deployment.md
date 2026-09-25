# VPS Ticketing Agent Deployment (hotline.abtrip.vn)

> **Discovered:** June 2026 | **VPS:** 43.156.72.127 (Tencent SG, Ubuntu 24.04)

## Overview

ABTRIP Hotline web app chạy trên VPS, serve qua Nginx + SSL. Giao diện chat-style hỗ trợ du lịch & vé máy bay 24/7 (Alpine.js frontend).

## Architecture

```
Internet → Nginx (443 SSL) → uvicorn (8080) → backend.main
                              ├── /abtrip → OpenClaw frontend (port 5001 API)
                              └── /n8n/ → n8n (port 5678)
```

### Components

| Component | Location | Port | Technology |
|-----------|----------|------|------------|
| Nginx (SSL) | System | 443 | Reverse proxy + Let's Encrypt |
| Nginx (HTTP) | System | 80 | Catch-all → 8080 |
| Ticketing Agent | `/opt/hermes/ticketing-agent/` | 8080 | FastAPI/uvicorn, Python 3.11 |
| OpenClaw frontend | `/opt/openclaw/workspace/ticketing-agent/frontend` | — | Static files, route `/abtrip` |
| OpenClaw API | — | 5001 | Route `/abtrip/api/` |
| n8n | Docker | 5678 | Route `/n8n/` |
| Ollama | Docker | 11434 | Local LLM |

### Nginx Config

**`/etc/nginx/sites-enabled/hermes`** — main config:
- Port 80 catch-all → proxy `127.0.0.1:8080` (default)
- Route `/abtrip` → static files at `/opt/openclaw/workspace/ticketing-agent/frontend`
- Route `/abtrip/api/` → proxy `127.0.0.1:5001/`
- Route `/n8n/` → proxy `127.0.0.1:5678` (with rewrite)

**`/etc/nginx/sites-enabled/hotline.abtrip.vn`** — dedicated subdomain:
- `server_name hotline.abtrip.vn`
- SSL (Let's Encrypt) + HTTP→HTTPS redirect
- Root: `/var/www/hotline/index.html`
- Proxy: `http://127.0.0.1:8080`

### Process

```bash
# Ticketing Agent (uvicorn)
2156274 ubuntu /opt/hermes/ticketing-agent/venv/bin/python3.11 venv/bin/uvicorn backend.main:app --host 0.0.0.0 --port 8080
```

## Access URLs

- **Public:** `https://hotline.abtrip.vn` (HTTPS)
- **Direct IP:** `http://43.156.72.127` (redirects to agent UI)

## SSH Access

```bash
ssh -i ~/.ssh/hermes_key_vps.pem ubuntu@43.156.72.127
```

## Discovery Checklist (when asking "what's on the VPS?")

1. `ls -la /etc/nginx/sites-enabled/` — list all active sites
2. `sudo nginx -t` — verify config
3. `ss -tlnp | grep -E ':(80|443|3000|5000|8000|8080|8888|3001)'` — find listening web processes
4. `sudo docker ps` — check containers
5. `systemctl list-units --type=service --state=running | grep -iE '(nginx|apache|flask|app|web)'` — system services
6. `certbot certificates` — check SSL domains
