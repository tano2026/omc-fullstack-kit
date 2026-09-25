# AI Proxy Diagnostics & Troubleshooting

> Absorbed from `ai-proxy-troubleshooting` (Jul 2026)

## Diagnostic Workflow

When AI requests through a proxy gateway (9Router, OmniRoute, or custom) fail, follow this systematic workflow:

### Step 1: Is the proxy running?

```bash
# Local proxy (9Router)
curl -s --connect-timeout 5 http://localhost:20128/v1/models > /dev/null 2>&1 && echo "ALIVE" || echo "DEAD"

# VPS proxy (OmniRoute)  
curl -s --connect-timeout 5 http://<VPS_IP>:20128/v1/models -o /dev/null -w "%{http_code}"
```

### Step 2: Check proxy logs

```bash
# 9Router logs
cat ~/.9router/logs/access.log | tail -20

# OmniRoute logs
journalctl -u omniroute --no-pager -n 20
# or
cat /var/log/omniroute/access.log | tail -20
```

### Step 3: Test bypassing Hermes

Direct API call through proxy:
```bash
curl -s http://localhost:20128/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{"model":"ds/deepseek-chat","messages":[{"role":"user","content":"hi"}],"max_tokens":10}'
```

### Step 4: Test bypassing proxy (direct to provider)

```bash
curl -s https://api.openai.com/v1/chat/completions \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"model":"gpt-4o-mini","messages":[{"role":"user","content":"hi"}],"max_tokens":10}'
```

### Step 5: Narrow the failure

| Test Result | Meaning |
|------------|---------|
| Direct works, proxy fails | Proxy config/credentials issue |
| Both fail | Provider issue or network |
| Proxy works, Hermes fails | Hermes config issue |

## Common Proxy Failure Patterns

| Pattern | Likely Cause | Fix |
|---------|-------------|-----|
| `401 Unauthorized` on proxy call | Missing or invalid `api_key` in Hermes config for custom proxy | Set `api_key: anything` (9Router/OmniRoute accept any key) |
| `502 Bad Gateway` | Upstream provider returned error to proxy | Check provider credentials in proxy config |
| `Connection refused` | Proxy not running | Start proxy service |
| Empty/truncated response | Proxy timeout or upstream rate limit | Increase proxy timeout or add fallback |
| `Ambiguous model` error | Model ID missing provider prefix | Use prefixed ID (e.g. `ds/deepseek-chat`) |
| `No active credentials` | Proxy dashboard needs provider setup | Add credentials in proxy web UI |
| SSL errors | Let's Encrypt cert expired on VPS | Renew cert or use HTTP internally |
| Slow first request | Cold start — proxy caches provider connection | Warm up with dummy request before use |
| `stream` returns garbled SSE | Response was streamed but caller expected JSON | Add `"stream": false` to request |

## VPS-Specific Debugging

```bash
# Check network connectivity to VPS
ping -c 2 <VPS_IP>

# Check if port is open
nc -zv <VPS_IP> 20128

# Check VPS firewall
sudo iptables -L -n | grep 20128
# or
sudo ufw status

# Check proxy process on VPS
ssh <user>@<VPS_IP> "ps aux | grep omniroute | grep -v grep"

# VPS resource check
ssh <user>@<VPS_IP> "free -h && df -h"
```

## Configuration Drift Detection

If proxy was working before but stopped:

1. Check if proxy was updated/reinstalled (config reset?)
2. Check if VPS IP changed (DHCP, reboot)
3. Check if API keys expired or rotated
4. Check if `.env` file was modified
5. Check if port 20128 is still free (collision with another service)
