# OpenRouter Troubleshooting

> Absorbed from `openrouter-troubleshooting` (Jul 2026)

## Diagnostic Workflow

### Step 1: Check API Key
```bash
curl -s https://openrouter.ai/api/v1/auth/key \
  -H "Authorization: Bearer $OPENROUTER_API_KEY" | jq .
```
Expected: `{"data":{"key":"sk-or-...","credits":0.5,...}}`

### Step 2: Check Remaining Credits
```bash
curl -s https://openrouter.ai/api/v1/auth/key \
  -H "Authorization: Bearer $OPENROUTER_API_KEY" | jq '.data.credits'
```
If `0` or `null` → out of credits.

### Step 3: Test Specific Model
```bash
curl -s -X POST https://openrouter.ai/api/v1/chat/completions \
  -H "Authorization: Bearer $OPENROUTER_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"model":"anthropic/claude-sonnet-4","messages":[{"role":"user","content":"hi"}],"max_tokens":10}' | jq .
```

### Step 4: Verify Hermes Config
```bash
grep -A10 'openrouter:' ~/.hermes/config.yaml
```

## Known Issues & Fixes

| Issue | Solution |
|-------|----------|
| Key shows `0 credits` | Top up at openrouter.ai/credits |
| `402` on Claude Sonnet / Opus | Free tier doesn't have access — need paid credits |
| `CF-*` errors | OpenRouter using Cloudflare — IP may be blocked; use proxy/vpn |
| Model not found | Model may be deprecated — check openrouter.ai/models |
| Rate limit exceeded | Add 1-2s delay between requests or use `max_retries` |
| Empty response | Increase `max_tokens` — response was clipped |
| Hermes shows `error: 502` | OpenRouter upstream provider issue — check status.openrouter.ai |
| Key rotation needed | Generate new key at openrouter.ai/keys, update config.yaml |

## Useful Endpoints

```bash
# List available models
curl -s https://openrouter.ai/api/v1/models | jq '.data[].id'

# Check key balance
curl -s https://openrouter.ai/api/v1/auth/key -H "Authorization: Bearer $KEY" | jq '{credits: .data.credits, limit: .data.limit}'

# Provider status
curl -s https://status.openrouter.ai/api/v1/uptime | jq '.'
```
