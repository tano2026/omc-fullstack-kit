# DeepSeek Migration (V5) — Jul 18, 2026

## The Bug

RIO bot's brain.py and chat_brain.py both used `OPENROUTER_API_KEY` for all LLM calls — but the bot's `.env` only had `RIO_BOT_TOKEN` and `HERMES_API_KEY`. No OpenRouter key anywhere.

**Impact:** 4 code blocks silently failed:
1. `_cross_reference()` — checked key → empty → return "" (no cross-ref)
2. `_implication()` — same pattern → return "" (no implication)
3. `_llm_analysis()` — checked key → empty → fell back to template (raw snippet dump)
4. `_optimize_search_query()` — same → fell back to static query builder

**Result:** User saw raw search snippets without any LLM synthesis. Bot looked "ngu."

## The Fix

### brain.py
- Added `_call_llm(system, prompt, temperature, max_tokens)` instance method
- Uses `os.environ.get("DEEPSEEK_API_KEY")` — reads the key user already has
- Endpoint: `https://api.deepseek.com/v1/chat/completions`
- Model: `deepseek-chat` (NOT `deepseek/deepseek-chat` which is OpenRouter model string)
- All 3 existing LLM methods (`_cross_reference`, `_implication`, `_llm_analysis`) refactored to use `self._call_llm()`
- `_template_synthesis()` checks for `DEEPSEEK_API_KEY` instead of `OPENROUTER_API_KEY`

### chat_brain.py
- ChatBrain init: `self.llm_api_key = os.environ.get("DEEPSEEK_API_KEY", "")`
- Added `_call_llm()` instance method (same pattern as brain.py)
- Added `_llm_synthesis()` — new method that takes search results + topic + rtype + lang → LLM produces natural language response
- `_natural_response()` now tries LLM first, falls back to old `_build_vi()`
- `_optimize_search_query()` standalone function: URL changed from `api.openrouter.ai` to `api.deepseek.com`, model from `deepseek/deepseek-chat` to `deepseek-chat`

### rio_bot.py (pending)
- Must read `DEEPSEEK_API_KEY` from .env and set into `os.environ`

### .env (needs update)
- Must add: `DEEPSEEK_API_KEY=sk-...`

## Checklist for Future LLM Migrations

When changing LLM backend in a bot:

- [ ] Find ALL `urllib.request.Request` blocks in the codebase — each one is a call site
- [ ] Find ALL `os.environ.get("OLD_KEY")` references — each env var check gates a feature
- [ ] Find ALL model string references (e.g. `deepseek/deepseek-chat` vs `deepseek-chat`)
- [ ] Find ALL API URL references (`api.openrouter.ai` vs `api.deepseek.com`)
- [ ] Create single `_call_llm()` helper before touching individual call sites
- [ ] Replace each call site with helper — verify syntax after each (f-string `\n` gets double-escaped by patch tool)
- [ ] Update .env.example
- [ ] Verify with live test: send a query and check if LLM synthesis appears in output
