# UFW Cheatsheet — VPS Web Deployment

> Common port issues when deploying web apps on Ubuntu VPS.

## Status & Verification

```bash
# Check status (active/inactive) + rules
ufw status verbose

# If inactive — enable it
ufw --force enable

# Default policy (usually deny incoming)
ufw default deny incoming
ufw default allow outgoing
```

## Common Port Rules

```bash
# SSH — ALWAYS keep open
ufw allow 22/tcp

# Web app ports
ufw allow 8137/tcp    # FastAPI dashboard
ufw allow 8000/tcp    # Common dev port
ufw allow 3000/tcp    # Node.js
ufw allow 5000/tcp    # Flask
ufw allow 8080/tcp    # Alternative HTTP

# Proxy gateways
ufw allow 20128/tcp   # 9Router / OmniRoute

# Allow all on a port range
ufw allow 8000:9000/tcp
```

## Delete Rules

```bash
# By rule number (first get numbers)
ufw status numbered
ufw delete 3

# By specification
ufw delete allow 8137/tcp
```

## Rate Limiting

```bash
# Rate limit SSH to prevent brute force
ufw limit 22/tcp
```

## Logging

```bash
# Enable logging to debug dropped packets
ufw logging on

# Check logs
tail -f /var/log/ufw.log
```

## Reset

```bash
# Reset to defaults (careful! closes everything)
ufw reset
```

## Most Common Cause of "App Unreachable"

```
App runs locally (curl localhost:PORT returns 200)
BUT external requests fail
→ 90% chance UFW blocks the port
→ Fix: ufw allow PORT/tcp
```

The other 10%:
- App binds to 127.0.0.1 not 0.0.0.0
- Cloud firewall (AWS SG, GCP FW rules) — separate from UFW
- ISP blocks port (rare for non-standard ports >1024)
