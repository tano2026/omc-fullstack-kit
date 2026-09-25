# OpenRouter Model Management

> Absorbed from `openrouter-model-management` (Jul 2026)

## Principles

1. **Prefer OpenRouter model names** over Hermes short names — explicitly versioned
2. **Pin by alias** not by hash — use `~/.hermes/config.yaml` `openrouter_models` section
3. **Track model roster changes** — models are added/removed weekly
4. **Pre-declare connections** before batch API calls to avoid cold-start timeouts
5. **Organize by capability** — each family needs a clear fallback chain

## Model Roster Pattern

```yaml
# In config.yaml openrouter_models section:
openrouter_models:
  # Primary — best overall
  primary: "openai/gpt-4o"
  # Fast — cheap, quick tasks
  fast: "gryphe/mythomax-l2-13b"
  # Fallback chain (ordered)
  fallbacks:
    - "openai/gpt-4o-mini"
    - "anthropic/claude-3-haiku"
    - "google/gemini-pro-1.5"
```

## Model Selection Guide

| Task | Recommended Model | Fallback |
|------|------------------|----------|
| Reasoning / Coding | anthropic/claude-sonnet-4 | openai/gpt-4o |
| Creative writing | openai/gpt-4o | anthropic/claude-sonnet-4 |
| Content gen (Vietnamese) | deepseek/deepseek-v4 | google/gemini-2.0-flash |
| Quick classification | openai/gpt-4o-mini | anthropic/claude-3-haiku |
| Vision analysis | anthropic/claude-sonnet-4 | openai/gpt-4o |
| Image generation | Recraft (separate) | FAL/Flux |

## Fallback Strategy

```yaml
# In llm.py or provider config:
fallback_chain:
  - provider: openrouter
    model: anthropic/claude-sonnet-4
  - provider: openrouter
    model: openai/gpt-4o
  - provider: openrouter
    model: google/gemini-2.0-flash
```

## Cost Management

| Tier | Models | Monthly Est. |
|------|--------|-------------|
| Primary | Claude Sonnet 4, GPT-4o | $20-50 |
| Fast | GPT-4o-mini, Gemini Flash | $5-10 |
| Free | MythoMax, Gemma 2 | $0 |

## Provisioning Checklist

- [ ] Model exists on OpenRouter (check `/api/v1/models`)
- [ ] Account has sufficient credits
- [ ] Key has model access enabled
- [ ] Fallback chain defined in config
- [ ] Test with `curl` before production use
- [ ] Monitor usage at openrouter.ai/activity
