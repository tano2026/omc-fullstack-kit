# ResearchTask.TYPES Sync Error

## Error

```
Unknown research type: general. Must be one of {'kpi', 'forecast', 'competitor', 'trend', 'sentiment', 'deep', 'market', 'swot'}
```

## Root Cause

`chat_brain.py` `detect_intent()` trả về `rtype` = `"general"` (hoặc `"data"`, `"comparison"`, `"advice"`, `"factual"`) — nhưng `ResearchTask.TYPES` trong `brain.py` không include các type này.

```python
# brain.py — BEFORE (Jul 17, 2026)
TYPES = {
    "market", "swot", "sentiment", "forecast", "kpi",
    "deep", "competitor", "trend",
}

# AFTER
TYPES = {
    "market", "swot", "sentiment", "forecast", "kpi",
    "deep", "competitor", "trend",
    "general", "data", "comparison", "advice", "factual",
}
```

## Fix Steps

1. Add new types to `ResearchTask.TYPES` in `brain.py`
2. Add same types to `VerificationLoop.verify()` type-specific checks in `brain.py`
3. Update `chat_brain.py` routing if needed (all intents → brain pipeline, not restricted)
4. Kill old bot + launch new instance

## Verification

ChatBrain V2 + RIOBrain V2.1: ALL 9 types (market, swot, sentiment, forecast, kpi, deep, competitor, trend, general, data, comparison, advice, factual) pass through `ResearchTask.__init__()` without ValueError.

## Prevention Rule

**Every new ChatBrain intent MUST be added to ResearchTask.TYPES simultaneously.** If you add an intent keyword in `chat_brain.py` but forget `brain.py`, the bot crashes on first matching user query.

The `get_sub_questions()` fallback to "deep" templates for unknown types is graceful — so even general/data/etc. produce reasonable sub-questions. But the `ResearchTask` constructor is a hard gate that raises ValueError.
