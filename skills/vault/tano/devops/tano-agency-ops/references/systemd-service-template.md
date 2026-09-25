# systemd Service Template — Python FastAPI App

> Place at `/etc/systemd/system/<app>.service`
> Then: `systemctl daemon-reload && systemctl enable <app> && systemctl start <app>`

## Template

```ini
[Unit]
Description=GMSP SaaS Dashboard
After=network.target

[Service]
User=root
WorkingDirectory=/root/gmsp-saas
ExecStart=/root/gmsp-saas/venv/bin/uvicorn backend.main:app --host 0.0.0.0 --port 8137
Restart=always
RestartSec=5
StandardOutput=append:/var/log/gmsp-saas.log
StandardError=append:/var/log/gmsp-saas.log

[Install]
WantedBy=multi-user.target
```

## Usage

```bash
# Create service file
cat > /etc/systemd/system/gmsp-saas.service << 'EOF'
[Unit]
Description=GMSP SaaS Dashboard
After=network.target

[Service]
User=root
WorkingDirectory=/root/gmsp-saas
ExecStart=/root/gmsp-saas/venv/bin/uvicorn backend.main:app --host 0.0.0.0 --port 8137
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
EOF

# Enable + start
systemctl daemon-reload
systemctl enable gmsp-saas
systemctl start gmsp-saas

# Status check
systemctl status gmsp-saas

# Logs
journalctl -u gmsp-saas -f
```

## Pitfalls

- **ExecStart** MUST be absolute path to the venv's binary, not just `uvicorn`
- **WorkingDirectory** MUST exist and contain the app. If app crashes with ModuleNotFoundError, check this first
- **Restart=always** + **RestartSec=5** — wait 5s between restart attempts to avoid rapid-fail loop
- systemd journals logs by default — use `journalctl -u <app>` not `tail -f app.log`
- After changing service file: always run `systemctl daemon-reload` AND `systemctl restart <app>`

## Key Commands

```bash
systemctl daemon-reload        # After editing .service file
systemctl enable <name>        # Auto-start on boot
systemctl disable <name>       # Remove auto-start
systemctl start <name>         # Start now
systemctl stop <name>          # Stop now
systemctl restart <name>       # Stop + start
systemctl status <name>        # Current state + last few log lines
journalctl -u <name> -f       # Follow logs
journalctl -u <name> --since "10 min ago"  # Recent logs
```
