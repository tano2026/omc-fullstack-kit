# Hermes Config Management — Model Switching, Fallback & Live Edits

## Location

Config file: `~/.hermes/config.yaml` (resolves to `C:\\Users\\<user>\\.hermes\\config.yaml` on Windows)

## Model Switching

To switch models mid-session, edit `model.default` and `model.provider`:

```yaml
model:
  default: <model-name>
  provider: <provider-name>   # e.g. google, openrouter, anthropic
```

### Common switches

| Need | default | provider | Notes |
|------|---------|----------|-------|
| Default (Cheap) | `oc/deepseek-v4-flash-free` | `openrouter` | Fast but no vision |
| Vision (screenshots) | `gemini-2.5-flash` | `google` | Supports image input |
| Reasoning | `anthropic/claude-sonnet-4` | `openrouter` | Complex debugging |

### Signal to switch

If `vision_analyze()` returns `unknown variant image_url`, the current model doesn't support vision. Switch to Gemini 2.5 Flash.

If the user says "mày nhìn ảnh này" or attaches a screenshot and the model keeps rejecting it → Gemini.

## Fallback Providers (Auto-Failover)

When the primary provider is unreachable (API down, network issue, rate-limit), Hermes automatically tries fallback providers in order.

### Config format

```yaml
fallback_providers: '[{"provider": "google", "model": "gemini-2.5-flash"}, {"provider": "openrouter", "model": "deepseek-v4"}]'
```

Setting via CLI:

```bash
hermes config set fallback_providers '[{"provider": "google", "model": "gemini-2.5-flash"}, {"provider": "openrouter", "model": "deepseek-v4"}]'
```

### Common fallback chains for HHTech users

Primary: `custom:omniroute` (HHTech API, deepseek-v4)

| Priority | Provider | Model | Key needed | Notes |
|----------|----------|-------|------------|-------|
| 1st fallback | `google` | `gemini-2.5-flash` | `GOOGLE_API_KEY` | Free tier generous |
| 2nd fallback | `openrouter` | `deepseek-v4` | `OPENROUTER_API_KEY` | Usually separate from HHTech key |
| 3rd fallback | `deepseek` | `deepseek-chat` | `DEEPSEEK_API_KEY` | Only if using official DeepSeek endpoint |

### Critical pitfall

**Do NOT chain the same base URL as your primary.** If the primary uses `hhtechapi.com/v1` and the fallback also points there, both fail when HHTech goes down. The fallback must point to a genuinely different API endpoint.

Real-world example (before fix):
```yaml
# BAD — both die together
primary: custom:omniroute → hhtechapi.com/v1
fallback[0]: deepseek → hhtechapi.com/v1   # useless!

# GOOD — second source
primary: custom:omniroute → hhtechapi.com/v1
fallback[0]: google → gemini-2.5-flash       # real backup
fallback[1]: openrouter → deepseek-v4        # real backup
```

### Verification

After setting fallback_providers, verify it's stored:

```bash
grep "fallback_providers" ~/.hermes/config.yaml
```

Or read the file directly. Note: `hermes config show` does NOT display fallback_providers in its summary output — you must read config.yaml directly.

## Pitfall

- Never edit config while a message is being generated — the change is picked up on the *next* message, not mid-stream
- After switching provider, the new provider's API key must exist in `.env` or environment
- The `base_url` under `model` is only used by OpenRouter-like providers. Google provider ignores it.
- `hermes config set` is the ONLY safe way to modify config.yaml — direct file edits via patch/write_file are blocked by Hermes security layer. Use the CLI command.
- Fallback providers are tried **sequentially**, not in parallel. If the primary API responds with a non-200 but non-fatal status (e.g., 429 Too Many Requests), the fallback chain may not activate depending on the error classification.
