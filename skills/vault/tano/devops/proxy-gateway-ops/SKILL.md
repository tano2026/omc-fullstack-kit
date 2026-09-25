---
name: proxy-gateway-ops
category: devops
description: Class-level operations for deploying, configuring, and troubleshooting AI routing gateways (9Router, OmniRoute) as local or VPS LLM proxies. Covers installation, provider config, cost optimization via free-tier routing, OpenClaw integration, and proxy diagnostics.
tags: [proxy, gateway, 9router, omniroute, ai-routing, vps, cost-saving, openai-compatible]
---

# AI Proxy Gateway Operations

> **Class-level skill** for all AI routing gateway activities. Covers installation and operation of 9Router (local gateway) and OmniRoute (VPS gateway), plus general proxy troubleshooting.

## When to Use

- User wants to reduce API costs by routing through free/cheap providers
- User asks about 9Router, 9Route, OmniRoute, or proxy setup
- User needs to connect Hermes/Claude Code/Codex to a proxy gateway
- Proxy service crashes, won't start, or returns auth errors
- User wants VPS-based routing (OmniRoute) with OpenClaw integration
- General proxy diagnostics

---

## Section 1: 9Router — Local AI Routing Gateway

### What is 9Router?

Local Next.js app (runs on `localhost:20128`) that provides one OpenAI-compatible endpoint to 60+ providers with smart 3-tier fallback and token compression.

**Installation:**
```bash
npm install -g 9router
```

**Running:**
```bash
# ALWAYS use --tray for persistence
9router -t
```

**Key pitfalls:**
- Without `-t`, 9Router exits immediately (Next.js process finishes)
- On Windows Git Bash, the shell script wrapper may fail — use `node "$(npm root -g)/9router/cli.js" -t` instead
- Model IDs differ from direct API names: use `ds/deepseek-chat` not `deepseek/deepseek-chat`

**Hermes config:**
```yaml
model:
  default: ds/deepseek-chat
  provider: custom:9router
providers:
  custom:9router:
    base_url: http://localhost:20128/v1
    api_key: anything
```

> **See reference file for full details:**
> - `references/9router-deployment.md` — Complete 9Router install, providers, 3-tier strategy, cost comparison, Python backend integration, and all pitfalls

---

## Section 2: OmniRoute — VPS Gateway

### What is OmniRoute?

Standalone npm package (v3.8+) running on VPS, providing cost-aware routing with automatic failover and multi-provider support.

**Lifecycle:**
```bash
# Check status
ps aux | grep omniroute | grep -v grep

# Test endpoint
curl -I http://localhost:20128/v1

# Restart after config changes
PID=$(ps aux | grep 'node /usr/bin/omniroute' | grep -v grep | awk '{print $2}')
sudo kill $PID
sudo -u <user> omniroute serve --daemon
```

**Key files:** `.env` at `/home/<user>/.omniroute/.env` — required after every API key addition

**Architecture (preferred setup):**
```
Hermes (local) → OmniRoute (VPS:20128) → Free/Paid LLM APIs
OpenClaw (VPS) → OmniRoute (VPS:20128) → Free/Paid LLM APIs
```
Both Hermes and OpenClaw route through the same OmniRoute instance on VPS.

> **See reference file for full details:**
> - `references/omniroute-deployment.md` — Complete OmniRoute VPS setup, .env management, restart lifecycle, model catalog, Hermes+OpenClaw config, and all pitfalls

---

## Section 3: Proxy Diagnostics & Troubleshooting

### Common Proxy Issues

> 🔴 **FIRST DIAGNOSTIC when proxy runs but is unreachable:** Check UFW — `ufw status verbose`. If proxy starts OK on localhost but external requests fail, 90% chance UFW blocks the port.

1. **Proxy won't start** — Check if port 20128 is already in use; verify the process didn't exit silently
2. **"No active credentials"** — Provider credentials must be added in the Dashboard UI even if .env has keys
3. **"Ambiguous model"** — Model ID must include provider prefix (e.g., `oc/deepseek-v4-flash-free` not `deepseek-chat`)
4. **Dashboard "Security risk"** — Set a password at first login
5. **OpenCode models return SSE by default** — Always set `"stream": false` in requests
6. **Silent crashes** — Check process uptime; look at dashboard console logs
7. **Model not found** — Check catalog with `curl http://localhost:20128/v1/models`

### Verification Steps
```bash
# Direct test
curl -s http://localhost:20128/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{"model":"oc/deepseek-v4-flash-free","messages":[{"role":"user","content":"hi"}],"max_tokens":10}'
```

### Python Backend Integration
Always set `"stream": false` for OpenCode models. For reasoning models, read `reasoning_content` when `content` is empty. Set `max_tokens` to at least 4096 for reasoning models. Free OpenCode models don't support vision.

> **See reference file for full diagnosis workflow:**
> - `references/proxy-troubleshooting.md` — Systematic proxy diagnosis workflow including VPS debugging, API key verification, silent crash detection, and configuration drift resolution

---

## Reference Files

| File | Source Skill | Description |
|------|-------------|-------------|
| `references/9router-deployment.md` | `9-router` | Full 9Router install, providers, Python backend |
| `references/omniroute-deployment.md` | `omniroute-config-debug` | OmniRoute VPS lifecycle, OpenClaw integration |
| `references/proxy-troubleshooting.md` | `ai-proxy-troubleshooting` | Generic proxy diagnosis workflow |
