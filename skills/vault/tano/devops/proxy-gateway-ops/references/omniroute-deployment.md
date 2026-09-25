# OmniRoute v3.8 — VPS Gateway

> Absorbed from `omniroute-config-debug` (Jul 2026)

## What is OmniRoute?

Standalone npm package (v3.8+) running on VPS. Provides cost-aware routing with automatic failover, multi-provider support, and model caching.

## Architecture (Preferred Setup)

```
Hermes (local) → OmniRoute (VPS:20128) → Free/Paid LLM APIs
OpenClaw (VPS) → OmniRoute (VPS:20128) → Free/Paid LLM APIs
```

Both Hermes and OpenClaw route through the same OmniRoute instance on VPS.

## Installation

```bash
npm install -g omniroute
```

## Lifecycle Management

```bash
# Check if running
ps aux | grep omniroute | grep -v grep

# Test endpoint
curl -I http://localhost:20128/v1

# Restart after config changes
PID=$(ps aux | grep 'node /usr/bin/omniroute' | grep -v grep | awk '{print $2}')
sudo kill $PID
sudo -u <user> omniroute serve --daemon
```

## .env Management

**Key files**: `.env` at `/home/<user>/.omniroute/.env` — required after every API key addition.

```bash
# Add or update a key
export OMNIROUTE_OPENROUTER_KEY="sk-or-v1-..."
echo "OMNIROUTE_OPENROUTER_KEY=$OMNIROUTE_OPENROUTER_KEY" >> .env
```

**Pitfalls**:
- `.env` with empty key lines causes `Credential file not found` errors
- PowerShell `echo KEY=val >> .env` creates UTF-16 LE with null bytes — always use bash
- After modifying `.env`, verify with `cat -v .env` to check for ^@ null bytes

## Model Routing Config

```yaml
# omniroute.yaml
routing:
  strategy: priority
  fallback: true
  models:
    claude-sonnet-4:
      provider: anthropic
    gpt-4o:
      provider: openai
    "*":
      provider: openrouter  # catch-all
```

## Key Provider Integration

| Provider | Config Key | Notes |
|----------|-----------|-------|
| OpenCode (free) | `OC_API_KEY` | Free tier, 1M context, tool calling |
| OpenRouter | `OMNIROUTE_OPENROUTER_KEY` | Paid routed access |
| DeepSeek | `OMNIROUTE_DEEPSEEK_KEY` | Cheap direct API |
| Google AI | `OMNIROUTE_GOOGLE_KEY` | Free tier available |

## OpenClaw Integration

In OpenClaw's `vars.yaml`:
```yaml
model: omni/oc/deepseek-v4-flash-free
```
This routes through OmniRoute to the OpenCode provider.

## Hermes Config for OmniRoute

```yaml
model:
  default: oc/deepseek-v4-flash-free
  provider: custom:omniroute
providers:
  custom:omniroute:
    base_url: http://<VPS_IP>:20128/v1
    api_key: anything
```

## Diagnostics

```bash
# Quick health check
curl -s -o /dev/null -w "%{http_code}" http://localhost:20128/v1/models

# Test specific model
curl -s http://localhost:20128/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{"model":"oc/deepseek-v4-flash-free","messages":[{"role":"user","content":"hi"}],"max_tokens":10}'

# Check catalog
curl -s http://localhost:20128/v1/models | jq '.data[].id'
```

## Common Issues

| Issue | Fix |
|-------|-----|
| `connection refused` | OmniRoute not running — check process |
| `No active credentials` | Add API keys in Dashboard UI (even if .env has them) |
| `Ambiguous model` | Use prefixed model IDs (e.g. `oc/deepseek-v4-flash-free`) |
| Key rotation not taking effect | Edit `.env`, restart OmniRoute |
| `Credential file not found` | Empty key line in `.env` — remove or fill it |
| UTF-16 corrupted `.env` | Recreate with bash `echo`, verify with `cat -v` |
| OpenCode models return SSE | Always set `"stream": false` |
