# Provider Switch: Stale base_url & Wrong API Key

## The Problem

When switching Hermes from a custom proxy provider to an official provider (or to a different provider reusing the same slot), the old provider's `base_url` and `api_key` can persist in `~/AppData/Local/hermes/config.yaml`. This silently routes requests to the wrong endpoint with the wrong credentials.

## Reproduction (2026-07-21 session)

1. User was on `custom:omniroute` provider with model `deepseek-v4-pro`, base_url `https://hhtechapi.com/v1`
2. Switched to `openrouter` provider with model `anthropic/claude-sonnet-4`
3. Result: `⚠️ Provider authentication failed`
4. Root cause: OpenRouter provider in AppData config still had:
   - `base_url: https://hhtechapi.com/v1` (DeepSeek proxy, not OpenRouter)
   - `api_key: sk-9c6...` (HHTech key, not `sk-or-...` OpenRouter key)
5. Fix: Cleared base_url, set correct OpenRouter key from global `~/.hermes/config.yaml` `provider_keys.openrouter`, restarted gateway

## Diagnosis Commands

```bash
# Check the ACTIVE config (AppData, not ~/.hermes/)
cat ~/AppData/Local/hermes/config.yaml | grep -A5 'openrouter'

# Look for stale base_url
hermes config show | grep -B2 -A5 'base_url'

# Check provider_keys in both configs
grep -A3 'provider_keys' ~/.hermes/config.yaml
grep -A3 'provider_keys' ~/AppData/Local/hermes/config.yaml
```

## Two-Config Architecture

Hermes has TWO config files that can diverge:

| Config | Path | Updated By |
|--------|------|-----------|
| Global | `~/.hermes/config.yaml` | Manual edits, initial setup |
| Active | `~/AppData/Local/hermes/config.yaml` | `hermes config set` commands |

The **Active** (AppData) config is the authority at runtime. The global config can have correct values that the active config overrides with stale/wrong ones. Always check both when diagnosing provider issues.

## Fix Recipe

```bash
# 1. Clear stale base_url
hermes config set providers.<name>.base_url ''

# 2. Set correct API key (get from global config or .env)
hermes config set provider_keys.<name> <correct-key>

# 3. Restart gateway
hermes gateway restart

# 4. Verify
hermes gateway status
```
