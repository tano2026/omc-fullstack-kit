# LLM Provider Troubleshooting — Generic

> Absorbed from `llm-provider-troubleshooting` (Jul 2026)

## When to Use
- Provider API returns 4xx/5xx errors  
- Provider consistently returns garbled / empty / truncated responses
- You need to switch providers due to rate limits or outages

## Diagnostic Flow

### 1. Check provider status page
```bash
# OpenRouter
curl -s https://status.openrouter.ai/ | grep -oP '"indicator":"\w+"'

# Anthropic  
curl -s https://status.anthropic.com/api/v2/status.json | jq .status.indicator

# xAI/Grok
curl -s https://www.xai-corp.com/status | # ...
```

### 2. Verify config
```bash
grep -A5 'provider:' ~/.hermes/hermes/config.yaml | head -20
```

### 3. Test with direct API call
```bash
curl -s https://openrouter.ai/api/v1/chat/completions \
  -H "Authorization: Bearer $OPENROUTER_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"model":"openai/gpt-4o","messages":[{"role":"user","content":"hi"}]}' | head -c 500
```

## Common Failure Patterns

| Symptom | Likely Cause | Fix |
|---------|-------------|-----|
| `401 Unauthorized` | API key invalid/expired | Regenerate key in provider dashboard |
| `402 Payment Required` | Insufficient credits | Top up account |
| `429 Too Many Requests` | Rate-limited | Back off, add delay between calls |
| Empty/truncated response | Context window exceeded | Reduce max_tokens or shorten input |
| Garbled Unicode | Wrong encoding | Force UTF-8 in headers |
| `400 invalid_model` | Model renamed/removed | Update model string |
| Timeout >120s | Provider overwhelmed | Retry with fallback model |
| `CF-*` errors (Cloudflare) | IP blocked / geo-restricted | Switch to different IP or use proxy |

## Provider-Specific Patterns

### OpenRouter
- Free tier: limited to 20 req/min, certain models excluded
- Key format: `sk-or-v1-...`
- Status check: `https://openrouter.ai/api/v1/auth/key` returns remaining credits

### Anthropic
- Key format: `sk-ant-...`
- Rate limits: Requests/min varies by tier. 5 RPD for free
- API: `https://api.anthropic.com/v1/messages`

### Custom providers (Ollama, LM Studio, etc.)
- Check if server is running: `curl http://localhost:11434/api/tags`
- Firewall: ensure port is accessible
