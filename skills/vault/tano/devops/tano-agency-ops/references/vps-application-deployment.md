---
name: vps-app-deploy
category: devops
description: Deploy, run, and monitor web applications on VPS (Ubuntu). Covers manual deployment via nc/SSH, UFW port management, process lifecycle (systemd/nohup), health monitoring, crash recovery, and SSH troubleshooting.
tags: [vps, deployment, ubuntu, ufw, systemd, monitoring, process-management]
---

# VPS Application Deployment

> **Class-level skill** for deploying web applications (FastAPI, Node.js, etc.) to Ubuntu VPS. Covers the full lifecycle: transfer code, install deps, configure firewall, run as service, monitor health, recover from crash.

## When to Use

- User built a web app and wants it accessible from internet
- App needs to survive VPS reboot
- Dashboard/service unreachable but VPS pings
- Need to check if VPS is alive, SSH works, and app is running
- Deploy code from Windows dev machine to VPS

## User Preference — Don't Pause for Confirmation on Routine Deploy Fixes

This user gets impatient ("làm gì làm đi" — "just go ahead and do it") when an agent stops mid-deploy-debug to ask permission for a low-risk, reversible, single-purpose command — e.g. `chmod`/`chown` on a config/env file, `systemctl restart <service>`, `nginx -t && systemctl reload nginx`, installing one missing pip package. These are exactly the kind of "medium-risk, mention what you're doing but proceed" actions the safety guidelines already allow — don't downgrade them to "ask first" just because `sudo` is in the command. Reserve actual confirmation pauses for genuinely destructive/hard-to-reverse ops (deleting data, dropping DB tables, force-push, wiping a directory) — not for routine service-file permission fixes during a deploy troubleshooting loop the user already asked you to do ("mày cho cái X lên vps đi").

---

## Section 1: Deployment Pipeline

### Step 1: Package Code

```bash
# On Windows dev machine
cd /d/project
tar czf deploy.tar.gz --exclude='.git' --exclude='__pycache__' --exclude='venv' --exclude='.env' .
```

### Step 2: Transfer to VPS

```bash
# Direct SCP (if SSH works)
scp deploy.tar.gz root@<VPS_IP>:/root/

# Fallback: netcat (for 1GB+ or when SCP path issues)
# On VPS: nc -l -p 1234 | tar xz -C /root/project
# On Windows: cat deploy.tar.gz | nc -q 0 <VPS_IP> 1234
# Or manually on Windows: type deploy.tar.gz | nc <VPS_IP> 1234
```

### Step 3: Install Dependencies

```bash
# Create venv if Python project
python3 -m venv /root/project/venv
source /root/project/venv/bin/activate
pip install -r /root/project/requirements.txt

# Missing packages during startup? Check with:
/root/project/venv/bin/python -c "import uvicorn" 2>&1
# Install one by one until everything imports
```

### Step 4: Configure Firewall

```bash
# MUST-DO: Open the port before starting
ufw allow <PORT>/tcp
ufw status verbose  # Verify

# Ports commonly blocked by default: 8000, 8137, 3000, 5000
# As well as non-standard ports!
```

> **CRITICAL PITFALL:** UFW often denies non-standard ports by default. If app starts but is unreachable, `ufw status` is FIRST check — NOT network issues, NOT app config.

### Step 5: Start the App

**Option A — systemd service (preferred for production):**
```bash
cat > /etc/systemd/system/<app>.service << 'EOF'
[Unit]
Description=<App Description>
After=network.target

[Service]
User=root
WorkingDirectory=/root/project
ExecStart=/root/project/venv/bin/uvicorn backend.main:app --host 0.0.0.0 --port <PORT>
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
EOF

systemctl daemon-reload
systemctl enable <app>
systemctl start <app>
systemctl status <app>  # Verify
```

**Option B — nohup (quick test):**
```bash
cd /root/project
nohup /root/project/venv/bin/uvicorn backend.main:app --host 0.0.0.0 --port <PORT> > app.log 2>&1 &
echo $PID  # Save PID
```

**Option C — tmux/screen (interactive debugging):**
```bash
tmux new -s <app>
# ... start app ...
# Ctrl+B D to detach
# tmux attach -t <app> to reattach
```

### Step 6: Verify

```bash
# From VPS itself
curl -s -o /dev/null -w '%{http_code}' http://localhost:<PORT>

# From anywhere
curl -s -o /dev/null -w '%{http_code}' http://<VPS_IP>:<PORT>
```

---

## Section 2: Health Monitoring

### Weekly Check Script

Put this in `/root/healthcheck.sh` and add to crontab:

```bash
#!/bin/bash
# Run: crontab -e → */15 * * * * /root/healthcheck.sh

APP_PORT=8137
APP_NAME="<app>"
PROJECT_DIR="/root/project"
LOG_FILE="/var/log/<app>-health.log"

# Test HTTP
HTTP_CODE=$(curl -s -o /dev/null -w '%{http_code}' --connect-timeout 5 http://localhost:$APP_PORT)

if [ "$HTTP_CODE" != "200" ]; then
    echo "[$(date)] $APP_NAME down (HTTP $HTTP_CODE). Restarting..." >> $LOG_FILE
    
    # Try restart
    cd $PROJECT_DIR
    nohup $PROJECT_DIR/venv/bin/uvicorn backend.main:app --host 0.0.0.0 --port $APP_PORT > app.log 2>&1 &
    
    sleep 3
    NEW_CODE=$(curl -s -o /dev/null -w '%{http_code}' --connect-timeout 5 http://localhost:$APP_PORT)
    
    if [ "$NEW_CODE" == "200" ]; then
        echo "[$(date)] Restart succeeded." >> $LOG_FILE
    else
        echo "[$(date)] Restart FAILED! Need manual intervention." >> $LOG_FILE
    fi
else
    echo "[$(date)] $APP_NAME healthy." >> $LOG_FILE
fi
```

### SSH Keepalive Check

When VPS becomes unreachable via SSH but still pings:
```
1. Try SSH with verbose: ssh -vvv root@<VPS_IP>
2. If SSH hangs → likely SSH daemon crashed or OOM killed
3. No remote fix possible — need console access to reboot
4. Prevention: add systemd service with Restart=always
```

### Resource Monitoring

Quick snapshot:
```bash
# Memory usage
free -h

# CPU + process list
ps aux --sort=-%cpu | head -5

# Disk
df -h

# Top process by memory
ps aux --sort=-%mem | head -5
```

---

## Section 3: SSH Troubleshooting

### When SSH fails but ping succeeds

Common causes:
1. **Out of memory (OOM)** — `sshd` killed, can't fork new connections
2. **SSH daemon crash** — rare but happens on low-memory VPS (512MB-1GB)
3. **Kernel panic / hang** — rarer, usually accompanies ping loss too
4. **iptables/UFW blocked your IP** — check `ufw status` on next console access

**Cannot fix remotely without:**
- Console access (VNC/IPMI provided by VPS provider)
- Out-of-band management (iDRAC, iLO, etc.)
- Cloud provider web console

**Prevention (must be set BEFORE crash):**
```bash
# Option 1: systemd for app (Restart=always) — auto-start after power-on
# Option 2: cron heartbeat (above) for HTTP recovery
# Option 3: kernel panic auto-reboot
echo "kernel.panic=10" >> /etc/sysctl.conf
```

### Diagnostics when SSH is alive

```bash
# Test app locally
curl -sI http://localhost:<PORT>

# Check what's listening
ss -tlnp | grep <PORT>

# Check UFW
ufw status verbose

# Check process memory
ps aux | grep -E '(uvicorn|node|python)' | grep -v grep
```

---

## Section 4: Common Pitfalls

1. **UFW blocks port** — Most common reason "app runs but unreachable". Check FIRST before network debugging.
2. **Hardcoded paths** — Windows paths (`D:/MMO Du an/...`) break on Linux. Use sed replace or env vars.
3. **A long-running systemd service can be silently masking a stale/moved deployment.** A process holds its binary, cwd, and open env file via file descriptors set at launch time — if the directory it was launched from is later moved/renamed/rebuilt (e.g. a project restructure that nests the app one level deeper, like `backend/` moving under a repo root), the OLD process keeps running and answering `curl` fine. The break only surfaces on the NEXT restart, when systemd re-resolves `ExecStart`/`WorkingDirectory`/`EnvironmentFile` against current disk state and finds nothing there (`Failed to spawn 'start' task: No such file or directory` / `code=exited, status=203/EXEC`). Before trusting "service is active" as proof the on-disk paths are correct, run `systemctl cat <service>` and `ls -la` each path it references — don't assume config drift will show up as a current outage; it shows up as a *future* restart failure.
4. **`EnvironmentFile=`/`.env` must be readable by the service's `User=`, not just by root/sudo.** Copying or regenerating a `.env` with `sudo cp` preserves restrictive source permissions (or resets ownership to root) — the service then fails with `PermissionError: [Errno 13] Permission denied: '.env'` even though the file objectively exists and `sudo cat` can read it. After writing/copying any file referenced by `EnvironmentFile=`, always `chown <service User>:<group>` and `chmod 640` (or looser) it, then verify by restarting — a passing `cat` via sudo tells you nothing about whether the unprivileged service user can open it.
5. **nginx `root` directive path must be verified against the actual filesystem, not assumed from the app's documented structure.** A stale or hand-edited site config can point `root` at a directory that doesn't exist or moved (e.g. app restructured from `app/static` to `backend/static`), producing a silent 404 on `/` while `/api/*` proxy routes work fine (different location blocks). Check with `ls -la <root path>` before debugging anything else when only the static/root route 404s but proxied API routes succeed.
6. **Redeploying updated code to an existing VPS venv does not pick up new dependencies automatically.** If the local codebase gained a new feature since the last deploy (e.g. a RAG module importing `chromadb`) and you only copy/sync the changed `.py` files without diffing `requirements.txt`, the restart crashes with `ModuleNotFoundError` even though every file transferred fine. After syncing updated code (not just on first deploy), diff local vs remote `requirements.txt`/`pip freeze` and `pip install` anything new BEFORE restarting the service — don't wait for the crash log to tell you.
7. **Missing deps** — `pip install` error only shows on runtime, not on import. Test all imports.
8. **Binding to 127.0.0.1** — Must be `0.0.0.0` to accept external connections.
9. **nohup dies on SSH exit** — If you logged out, nohup session dies. Use systemd or tmux.
10. **Port collision** — `Address already in use`. Kill old process first: `kill $(lsof -t -i:<PORT>)`.
11. **VPS low memory** — Headless VPS often has 512MB-1GB. App + deps can OOM. Check `free -m`.
12. **File size limits** — `nc` transfer larger than 1GB may fail silently. Use SCP for big files.
13. **max_connections in databases** — If app uses SQLite, concurrent writes can fail.
14. **No swap** — Add swapfile on small VPS to prevent OOM kills.

---

## Reference Files

| File | Description |
|------|-------------|
| `references/ufw-cheatsheet.md` | UFW commands: allow/deny, status, logging, delete rules |
| `references/systemd-service-template.md` | systemd unit file template for Python apps |
| `references/vps-monitoring-scripts.md` | Health check scripts + crontab setup |
