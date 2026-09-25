# ABTrip Backend — VPS Deploy & Test Guide

## Deploy (Windows → Ubuntu VPS)

```bash
cd /c/Users/Nguyen\ Ngoc\ Tan/agent.tkt/backend
bash deploy/deploy.sh
```

Script `deploy.sh` does:
1. Stop old systemd service
2. Create `/opt/abtrip-backend` on VPS
3. `tar` → `scp` source (excludes `__pycache__`, `.pyc`, `.venv`, `deploy/`, `.env`)
4. Create venv + install deps (`uvicorn`, `fastapi`, `pydantic`, `httpx`, `python-dotenv`)
5. Copy `.env.production` as `.env`
6. Create systemd service pointing to `.venv/bin/python`
7. Enable + start service
8. Verify via `curl /api/health`

## Pitfalls (July 21, 2026)

### 1. Externally-managed Python (Ubuntu 24.04)
`pip install` fails with PEP 668 error. **Must use venv:**
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install requirements.txt
```

### 2. Systemd ExecStart path
Point to `.venv/bin/python`, NOT `/usr/bin/python3`:
```
ExecStart=/opt/abtrip-backend/.venv/bin/python -m uvicorn app.main:app --host 0.0.0.0 --port 8138 --workers 2
```

### 3. Debug file path leak
`chat.py` had `open(r"C:/Users/Nguyen Ngoc Tan/debug_session.txt", "a")` — this caused HTTP 500 on VPS because the Windows path doesn't exist. **Remove or conditionalize before deploy.**

Search for: `debug_session.txt` in all files before deploying.

### 4. Port conflict
Use `netstat -ano | grep ':8138 ' | grep LISTEN` → `taskkill -f -pid <PID>`.

### 5. Unicode / locale
If Unicode errors in logs, set `LANG=vi_VN.UTF-8` or `PYTHONIOENCODING=utf-8`.

### 6. nginx reverse proxy
nginx routes `/api/*` to backend and serves chat HTML UI at `/`. Config at `/etc/nginx/sites-available/abtrip`:

```nginx
server {
    listen 80 default_server;
    server_name _;
    client_max_body_size 10m;
    location / {
        root /opt/abtrip-backend/static;
        index chat.html;
    }
    location /api/ {
        proxy_pass http://127.0.0.1:8138;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_cache_bypass $http_upgrade;
    }
}
```

### 7. Chat UI location
Static HTML at `http://100.64.173.75/` — single-file `chat.html` served by nginx from `/opt/abtrip-backend/static/`.
Update: edit `C:\Users\Nguyen Ngoc Tan\agent.tkt\abtrip_chat.html` locally → `scp` to VPS → `/opt/abtrip-backend/static/chat.html`.

## Verification

```bash
curl http://100.64.173.75:8138/api/health
# {"status":"ok","service":"abtrip-backend","timestamp":"..."}

# Quick test
curl -X POST http://100.64.173.75:8138/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message":"xin chào","session_id":"verify-1"}'
```

## Full Test Suite

Run from local Windows:
```bash
cd /c/Users/Nguyen\ Ngoc\ Tan/agent.tkt
python abtrip_full_test.py
```

### Test Design Principles (used in `abtrip_full_test.py`)

- **Fresh UUID per test:** `str(uuid.uuid4())` as session_id prevents cross-test contamination
- **Correct expected types:** API returns `confirm`, `clarify`, `text`, `flight_results` types — NOT just `text`
- **Vietnamese name validation:** Use word-boundary regex (`\btan son nhat\b`), NOT substring match (`"hcm" in "TP.HCM"` = false positive)
- **Policy content check:** Require 2+ keywords OR 1 specific keyword (`"hủy"`, `"đổi"`, `"hoàn"`) for short policy replies
- **Search results check:** Verify airline code (`VJ`, `VN`, `QH`, etc.) + price symbol (`₫`)
