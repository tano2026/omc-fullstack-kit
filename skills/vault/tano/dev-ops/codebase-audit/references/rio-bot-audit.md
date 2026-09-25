# RIO Bot v2.0 Codebase Audit — Session Reference (Jul 2026)

> RIO = Research & Intelligence Officer — Python Telegram bot for market research.
> Codebase: `D:\MMO Du an\TANO-AGENCY\rio-bot\`

## Issues Found (7 total)

### 🟠 CRASH — Standalone `def` using `self`
- **File**: `modules/chat_brain.py` line 154
- **`_optimize_search_query(self, ...)`** is a standalone `def` (not inside a class) but uses `self.llm_api_key`, `self.llm_api_url`, `self.llm_model`
- **Crash**: `AttributeError` on any call
- **Fix**: Remove `self`, add explicit params `api_key`, `api_url`, `model` as kwargs
- **Updates required**: All callers in `chat()`, `_quick_search()` must pass the new params

### 🟠 CRASH — Wrong variable in return
- **File**: `modules/chat_brain.py` line 519
- `_build_en()` builds list `lines = []` but returns `"\n".join(results)`
- **`results` is undefined** → `NameError` when user queries in English
- **Fix**: `return "\n".join(lines)`

### 🟡 TOKEN WASTE — Duplicate LLM call
- **File**: `modules/chat_brain.py`
- `chat()` calls `_optimize_search_query()` at line 323
- `_quick_search()` (called from chat) calls `_optimize_search_query()` AGAIN at line 381
- **Fix**: Pass `search_query` as param to `_quick_search()`, only compute once

### 🟡 REQ BROKEN — Wrong package in requirements.txt
- **File**: `requirements.txt` line 6
- Source code imports `from ddgs import DDGS` — package name is `ddgs`
- requirements.txt has `fourdigits>=0.1.2` — wrong package name
- **Fix**: Replace `fourdigits` with `ddgs`

### 🟡 NO FILTER — Commerce results not discarded
- **Missing**: Content filter for Amazon/eBay/Etsy/Alibaba/Shopify product pages
- **Brain pipeline** (`brain.py` stage VALIDATE) passes raw search results directly
- **Fix**: Added `filter_results()` to `web_research.py` + integrated in `brain.py` stage VALIDATE

### 🟡 FLOW BUG — search_query computed before early return
- **File**: `modules/chat_brain.py`
- `chat()` computes `search_query` at line 318 even when query < 4 chars (early return at line 327)
- **Fix**: Move search_query computation after all early return checks

### ⚪ NICE — ChatBrain inherits filtered sources from Brain
- ChatBrain's `chat()` already passes to `brain.run()` and uses chunks[0] if available
- When brain has results, it uses `_summarize_brain_output` — already filtered
- No fix needed, mechanism was correct

## Fix Process

1. **Read all files**: chat_brain.py, brain.py, web_research.py, analytics.py, rio_bot.py, requirements.txt
2. **Categorize**: 2 crash 🟠, 3 high 🟡, 1 done ⚪
3. **Fix in order**: crash first, then high, then nice-to-have
4. **Verify each fix**: syntax check, class instantiation test, runtime test

## Verification Script

```bash
# Step 1: Syntax check all modules
cd "D:\MMO Du an\TANO-AGENCY\rio-bot"
python -c "import modules.chat_brain; import modules.brain; import modules.web_research; import modules.validator; import modules.analytics; print('All modules OK')"

# Step 2: Class instantiation test
python -c "from modules.chat_brain import ChatBrain; cb = ChatBrain(); print('ChatBrain OK')"

# Step 3: Feature test — standalone function
python -c "
from modules.chat_brain import _optimize_search_query
result = _optimize_search_query('fastrack sân bay', {'rtype':'market','topic':'fastrack sân bay'}, api_key='')
print(f'optimize_search_query -> {result}')
"

# Step 4: Feature test — content filter
python -c "
from modules.web_research import filter_results
r = [{'title':'Amazon Dot','url':'https://amazon.com/dot','snippet':'buy now'},
     {'title':'Blog Review','url':'https://blog.vn/fastrack','snippet':'dịch vụ tốt'}]
f = filter_results(r, context_topic='fastrack')
print(f'Filter: {len(r)}->{len(f)} (expect 1)')
"

# Step 5: Deploy + health check
python rio_bot.py
# Wait 5s, check log for "✅ Bot: @username" + no ERROR lines
```
