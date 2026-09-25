# FastAPI Dashboard — VPS Deployment

> Deploy pipeline-dashboard (or any FastAPI app) from Windows dev machine to Linux VPS.
> Covers packaging, transfer, path fix, dependency install, and daemon management.

## Prerequisites

- VPS with SSH access (user `ubuntu` or similar)
- SSH key-based auth configured
- VPS has Python 3 and pip

## Deployment Steps

### 1. Package the app

From Windows (git-bash):

```bash
cd "D:/path/to/project"
tar czf app.tar.gz backend/ templates/ static/ 2>&1
```

### 2. Transfer to VPS

```bash
scp app.tar.gz ubuntu@YOUR_VPS_IP:/tmp/
```

### 3. Extract on VPS

```bash
ssh ubuntu@YOUR_VPS_IP
sudo mkdir -p /opt/app-name
sudo tar xzf /tmp/app.tar.gz -C /opt/app-name/
sudo chown -R ubuntu:ubuntu /opt/app-name/
```

### 4. Fix hardcoded Windows paths

If the code has hardcoded `D:/MMO Du an/...` paths, fix with sed:

```bash
sed -i 's|D:/MMO Du an/GMSP|/opt/app-name|g' /opt/app-name/backend/main.py
sed -i 's|D:/MMO Du an/GMSP-SAAS|/opt/app-name|g' /opt/app-name/backend/main.py
# Repeat for any other Windows-specific paths
```

### 5. Install dependencies

```bash
pip3 install fastapi uvicorn jinja2 python-multipart aiofiles sqlalchemy --break-system-packages
```

> **Note:** `--break-system-packages` is needed on Debian/Ubuntu (PEP 668). For cleaner setup, use `pipx` or a venv.

### 6. Create directories referenced by the app

```bash
mkdir -p /opt/app-name/pipeline
```

### 7. Start the server

```bash
cd /opt/app-name
nohup python3 -m uvicorn backend.main:app --host 0.0.0.0 --port 8137 > /tmp/app-name.log 2>&1 &
```

### 8. Verify

```bash
# Health check
curl -s -o /dev/null -w "%{http_code}" http://localhost:8137/

# Check HTML response
curl -s http://localhost:8137/ | head -10

# Check logs
cat /tmp/app-name.log
```

## Common Pitfalls

### SQLite "unable to open database file"

- **Cause:** Hardcoded Windows path in Python code (e.g., `D:/MMO Du an/GMSP-SAAS/gmsp.db`) doesn't exist on Linux.
- **Fix:** Run `sed` to replace Windows paths with Linux paths (step 4 above). Or use relative paths:
  ```python
  from pathlib import Path
  BASE_DIR = Path(__file__).parent.parent  # Resolves to /opt/app-name
  DB_PATH = BASE_DIR / "gmsp.db"
  ```

### pip fails with "externally-managed-environment"

- **Cause:** Debian/Ubuntu PEP 668 restriction.
- **Fix:** Use `--break-system-packages` or create a venv:
  ```bash
  python3 -m venv venv
  source venv/bin/activate
  pip install ...
  ```

### uvicorn not found in PATH

- **Cause:** pip installs to `~/.local/bin` which isn't in the nohup environment.
- **Fix:** Use full path or export PATH:
  ```bash
  export PATH=$HOME/.local/bin:$PATH
  nohup python3 -m uvicorn ... &
  ```

### Port already in use

```bash
# Find PID
lsof -ti :8137
# Or
ps aux | grep uvicorn | grep -v grep | awk '{print $2}'

# Kill
kill -9 PID

# Or one-liner
kill -9 $(lsof -ti :8137) 2>/dev/null
```

### Path resolution issues in template directories

When using `Path("templates/")` in code deployed from Windows, the relative path resolves to the CWD. On VPS, always use an absolute path derived from a known location:

```python
# Good: resolves relative to the file itself
BASE_DIR = Path(__file__).resolve().parent.parent
TEMPLATES_DIR = BASE_DIR / "templates"

# Bad: depends on CWD at runtime
TEMPLATES_DIR = Path("templates")
```

## Making it Permanent (systemd)

For production, create a systemd service:

```bash
sudo tee /etc/systemd/system/app-name.service << 'EOF'
[Unit]
Description=GMSP Dashboard
After=network.target

[Service]
Type=simple
User=ubuntu
WorkingDirectory=/opt/app-name
ExecStart=/usr/bin/python3 -m uvicorn backend.main:app --host 0.0.0.0 --port 8137
Restart=always
RestartSec=5
Environment=PATH=/home/ubuntu/.local/bin:/usr/bin:/usr/local/bin

[Install]
WantedBy=multi-user.target
EOF

sudo systemctl daemon-reload
sudo systemctl enable app-name
sudo systemctl start app-name
sudo systemctl status app-name
```

## Exposing to Mobile (5G)

- **VPS public IP** works directly if the VPS has a public IP and port is open
- For VPS behind NAT (like 100.64.x.x), use **Cloudflare Tunnel** or **ngrok**
- Alternatively, serve through a reverse proxy (Caddy, Nginx) on the VPS
