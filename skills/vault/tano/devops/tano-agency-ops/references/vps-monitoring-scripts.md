# VPS Monitoring & Recovery Scripts

> Script collection for keeping web apps alive on low-memory VPS.

## healthcheck.sh — Restart App on Crash

Place at `/root/healthcheck.sh`, chmod +x.

```bash
#!/bin/bash
APP_PORT=8137
APP_NAME="gmsp-saas"
PROJECT_DIR="/root/gmsp-saas"
LOG_FILE="/var/log/app-health.log"

HTTP_CODE=$(curl -s -o /dev/null -w '%{http_code}' --connect-timeout 5 http://localhost:$APP_PORT)

if [ "$HTTP_CODE" != "200" ]; then
    echo "[$(date)] $APP_NAME down (HTTP $HTTP_CODE). Restarting..." >> $LOG_FILE
    
    cd $PROJECT_DIR
    nohup $PROJECT_DIR/venv/bin/uvicorn backend.main:app --host 0.0.0.0 --port $APP_PORT > app.log 2>&1 &
    
    sleep 3
    NEW_CODE=$(curl -s -o /dev/null -w '%{http_code}' --connect-timeout 5 http://localhost:$APP_PORT)
    
    if [ "$NEW_CODE" == "200" ]; then
        echo "[$(date)] Restart OK" >> $LOG_FILE
    else
        echo "[$(date)] Restart FAILED" >> $LOG_FILE
    fi
fi
```

### Crontab — Run Every 5 Minutes

```
*/5 * * * * /root/healthcheck.sh
```

### Crontab — Daily Process Snapshot (debug OOM)

```
0 */6 * * * ps aux --sort=-%mem | head -20 > /var/log/ps-snapshot-$(date +\%Y\%m\%d-\%H\%M).log
```

## memwatch.sh — Detect & Alert OOM

```bash
#!/bin/bash
MEM_FREE=$(free -m | awk '/^Mem:/ {print $4}')
SWAP_USED=$(free -m | awk '/^Swap:/ {print $3}')
THRESHOLD=50  # Alert if free RAM below 50MB

if [ "$MEM_FREE" -lt "$THRESHOLD" ]; then
    logger -t "MEMWATCH" "CRITICAL: ${MEM_FREE}MB free RAM, ${SWAP_USED}MB swap used"
    # Could add Telegram/webhook alert here
fi
```

## Remote Diagnostics Sequence

Use this order when user reports "can't access":

1. **Ping test** — If fails, VPS is fully down
2. **Traceroute** — If 1 hop, VPS is directly reachable on network
3. **SSH test** — If timeout but ping works → SSH daemon issue or OOM
4. **Curl to port** — If timeout, check UFW or app binding
5. **Curl to localhost from SSH** — Distinguishes app issue vs network/firewall

## Prevention Checklist

- [ ] App starts on boot (systemd: Restart=always, or crontab @reboot)
- [ ] Healthcheck script installed + crontab active
- [ ] UFW rules allow app port
- [ ] App binds to 0.0.0.0 not 127.0.0.1
- [ ] Swap file configured if RAM < 1GB
- [ ] `kernel.panic=10` in sysctl for crash auto-reboot
- [ ] Log rotation active (logrotate for app logs)
