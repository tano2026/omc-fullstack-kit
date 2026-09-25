# Hermes Fallback Providers

## Config key

`fallback_providers` in `~/.hermes/config.yaml` accepts a JSON array of backup provider+model pairs. When the primary provider is unreachable or returns errors, Hermes falls through the chain automatically.

## Format

```json
[{"provider": "PROVIDER_NAME", "model": "MODEL_ID"}]
```

## Set via CLI

```bash
hermes config set fallback_providers '[{"provider": "google", "model": "gemini-2.5-flash"}, {"provider": "openrouter", "model": "deepseek-chat"}]'
```

## Current setup (TANO-AGENCY)

```
Primary:    custom:omniroute → HHTech (deepseek-v4)
Fallback 1: openrouter       → deepseek-chat
```

## Critical: avoid fake backups

The fallback provider MUST point to a different API endpoint than the primary. Example of a **fake backup**:
```yaml
# Primary
custom:omniroute:
  base_url: https://hhtechapi.com/v1

# Fallback (ALSO hits hhtechapi — useless!)
deepseek:
  base_url: https://hhtechapi.com/v1
```

If the primary goes down because `hhtechapi.com` is unreachable, the fallback fails identically. Always verify fallback providers use independent endpoints.

## Testing API key health

### OpenRouter
```python
import json, urllib.request
key = "sk-or-..."
req = urllib.request.Request(
    "https://openrouter.ai/api/v1/auth/key",
    headers={"Authorization": f"Bearer {key}"}
)
resp = urllib.request.urlopen(req)
data = json.loads(resp.read())
# data["data"]["limit_remaining"] — null = unlimited
# data["data"]["usage"] — total spend
```

### Google Gemini
```bash
curl -s "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash?key=AIza..."
```
Response `"API_KEY_INVALID"` = key is dead. Get a new one from [Google AI Studio](https://aistudio.google.com/).

## Pitfalls

- Google Gemini keys expire or get revoked silently — test periodically if used as fallback
- OpenRouter keys from third-party (HHTech, etc.) may not be real OpenRouter keys — verify via `/v1/auth/key` endpoint
- Setting fallback_providers with a dead key doesn't error — Hermes will just fail through to the next entry
- Order matters: list most reliable fallback first
