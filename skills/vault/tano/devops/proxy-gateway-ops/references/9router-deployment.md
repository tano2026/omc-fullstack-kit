# 9Router — Local AI Routing Gateway

> Absorbed from `9-router` (Jul 2026)

## What is 9Router?

Lightweight local proxy that converts any OpenAI-compatible endpoint into a routable API gateway with key management, rate limiting, and model routing.

## Installation

```bash
# Prerequisites: Node.js 18+
npm install -g 9router
```

## Running (Critical: never without `-t`)

```bash
# ALWAYS use --tray for persistence
9router -t

# On Windows Git Bash, the npm wrapper may fail — use direct node path:
node "$(npm root -g)/9router/cli.js" -t
```

**Pitfall**: Without `-t`, 9Router exits immediately after setup (Next.js process finishes).

## Configuration

```yaml
# config.yaml (auto-generated on first run, edit at ~/.9router/config.yaml)
port: 20128
providers:
  anthropic:
    baseUrl: https://api.anthropic.com
    apiKey: ${ANTHROPIC_API_KEY}
  openai:
    baseUrl: https://api.openai.com/v1
    apiKey: ${OPENAI_API_KEY}
  deepseek:
    baseUrl: https://api.deepseek.com/v1
    apiKey: ${DEEPSEEK_API_KEY}
  openrouter:
    baseUrl: https://openrouter.ai/api/v1
    apiKey: ${OPENROUTER_API_KEY}

models:
  claude-sonnet-4:
    provider: anthropic
    model: claude-sonnet-4-20250514
  gpt-4o:
    provider: openai
    model: gpt-4o
  deepseek-chat:
    provider: deepseek
    model: deepseek-chat
```

## Model ID Quirks (Important)

9Router uses **different** model IDs than direct API names or what Hermes expects internally:

| Intended Model | 9Router ID | Direct API ID |
|---------------|-----------|--------------|
| DeepSeek Chat | `ds/deepseek-chat` | `deepseek/deepseek-chat` |
| Claude Sonnet 4 | `anthropic/claude-sonnet-4` | `claude-sonnet-4-20250514` |
| GPT-4o | `openai/gpt-4o` | `gpt-4o` |

Always check the 9Router catalog: `http://localhost:20128/v1/models`

## 3-Tier Cost Strategy

```yaml
# In Hermes config.yaml
model:
  default: oc/deepseek-v4-flash-free
  provider: custom:omniroute
fallback_providers:
  - provider: custom:9router
    model: ds/deepseek-chat
  - provider: openrouter
    model: openrouter/auto
```

Tier 1: Free (OpenCode via OmniRoute VPS) → Tier 2: Cheap (DeepSeek via 9Router local) → Tier 3: Paid (OpenRouter)

## OpenClaw Integration

OpenClaw on VPS routes requests through the same OmniRoute proxy. Configuration in OpenClaw's `vars.yaml`:
```yaml
model: omni/oc/deepseek-v4-flash-free
```

## Hermes Config for 9Router

```yaml
model:
  default: ds/deepseek-chat
  provider: custom:9router
providers:
  custom:9router:
    base_url: http://localhost:20128/v1
    api_key: anything
```

## Python Backend Integration

```python
import httpx
import asyncio

async def proxy_chat(messages, model="ds/deepseek-chat"):
    async with httpx.AsyncClient(base_url="http://localhost:20128") as client:
        resp = await client.post("/v1/chat/completions", json={
            "model": model,
            "messages": messages,
            "stream": False  # essential for OpenCode models!
        })
        return resp.json()
```

## Diagnostics

```bash
# Check if running
curl -s http://localhost:20128/v1/models | head -c 200

# Test chat
curl -s http://localhost:20128/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{"model":"ds/deepseek-chat","messages":[{"role":"user","content":"hi"}],"max_tokens":10}' | jq .
```

## Common Issues

| Issue | Fix |
|-------|-----|
| `connection refused` | 9Router not started or `-t` flag missing |
| `Ambiguous model` | Use prefixed model ID (e.g. `ds/deepseek-chat`) |
| `No active credentials` | Add provider credentials in Dashboard UI |
| `stream` returns SSE garbled | Always set `"stream": false` |
| Dashboard "Security risk" | Set a password in dashboard at first login |
| Silent crash after start | Check process: `ps aux \| grep 9router` |
