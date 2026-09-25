---
name: codebase-audit
description: Comprehensive multi-lens codebase audit methodology — scan, read layers, apply frameworks, categorize severity, produce actionable report. Works with any project (Python/JS/TS/etc.)
---

# Codebase Audit — Multi-Lens Methodology

## TL;DR
Systematic codebase review: **scan → read layers → apply frameworks → categorize → report → batch fix**. Load relevant skills (superpowers, harness-engineering, taste-frontend, etc.) as analysis lenses.

## When to Use
- User asks "rà soát bộ code này", "review code", "kiểm tra project", "audit codebase"
- User drops a folder path and wants comprehensive analysis
- Joining a new project / onboarding
- Pre-deploy quality check
- Legacy code evaluation

## Step-by-Step Process

### Phase 1: Scan & Map
```python
# Use execute_code with Python glob for reliable scanning:
import glob, os
project_root = r"<project_path>"
exclude_dirs = {'.next', '__pycache__', 'node_modules', 'dist', 'build', '.git', 'venv', '.venv', '__pycache__'}

all_files = []
for root, dirs, files in os.walk(project_root):
    dirs[:] = [d for d in dirs if d not in exclude_dirs]
    for f in files:
        fpath = os.path.join(root, f)
        relpath = os.path.relpath(fpath, project_root)
        size = os.path.getsize(fpath)
        all_files.append((relpath, size))
```

Output a table: total files, total bytes, sorted by directory.

### Phase 2: Read in Order (3 passes)
Pass 1 — **Backend Core** (if Python/FastAPI/etc.):
- `main.py` / entrypoint → architecture & routes
- Each `services/*.py` → business logic
- Each `api/*.py` → endpoints
- `models/*.py` → data structures
- `config.py` / `.env` → configuration

Pass 2 — **Frontend Core** (if Next.js/React/etc.):
- `layout.tsx` → app shell
- `page.tsx` (home) → main interaction
- Each major component → UI logic
- `lib/api.ts` → API client
- `package.json` → deps

Pass 3 — **Config & Infrastructure**:
- `Dockerfile`(s), `docker-compose*.yml`
- `.env`, `.env.local`, `.gitignore`
- `README.md`, any `*.md` docs
- `tailwind.config.js`, `tsconfig.json`
- Test files

### Phase 3: Apply Analysis Lenses
Load these skills and apply their lens:

| Lens | What it catches |
|------|----------------|
| **superpowers** | Senior dev quality: think-before-code, test-driven, self-review, incremental patterns |
| **harness-engineering** | Engineering gaps: CI/CD, testing infra, error handling, observability |
| **taste-frontend** | Frontend smell: anti-patterns, naming, component structure |
| **mattpococks** | TypeScript hygiene: token waste, type safety, `any` usage |
| **ui-ux-pro-max** | UX gaps: loading states, error boundaries, mobile responsiveness, accessibility |
| **vibe-coder-assistant** | Code clarity: is this readable? Would a beginner understand? |

### Phase 4: Categorize by Severity
Use emoji + severity labels consistently. With Vietnamese-speaking users, use Vietnamese labels:

```
🔴 CAO — Cần sửa gấp (sẽ crash / mất data / lỗi bảo mật nếu không fix)
🟡 TRUNG BÌNH — Cần cải thiện (gây khó maintain, performance issue, hoặc Phase 1 OK nhưng cần plan)
🟢 THẤP — Nên sửa (best practice, code smell, nice to have)
```

For English reports use:
```
🔴 CRITICAL — Must fix immediately (crash / data loss / security)
🟡 HIGH — Should fix soon (maintainability, performance)
🟢 MEDIUM — Best practice / code smell
⚪ LOW — Nice to have
```

### Phase 5: Report Structure
```
## 📋 BÁO CÁO RÀ SOÁT — <PROJECT NAME>

### 🏗️ KIẾN TRÚC TỔNG THỂ
<1-2 paragraph overview>

### 🔴 CRITICAL
1. **Issue name** — description, where, why
   Fix: specific action

### 🟡 HIGH
...

### 🟢 MEDIUM
...

### ⚪ LOW
...

### 📊 METRICS TỔNG QUAN
| Metric | Value |
|--------|-------|
| Total files | N |
| Backend | N files |
| Frontend | N files |
| Dead code estimate | ~N% |
| Critical bugs | N |
| Test coverage | ~N% |

### 🎯 BATCH FIX
Fix all clearly correct Critical/High bugs immediately. No phased timeline.
```
✅ lỗi_1 — route mismatch (api.ts → fixed)
✅ lỗi_2 — alert() → inline validation (BookingForm.tsx → fixed)
⏳ lỗi_3 — async client (needs architect review)
❌ lỗi_4 — removing dead code (ask user before deleting files)
```
Log each fix with ✅ done, ⏳ needs input, ❌ blocked.
```

### Phase 6: Batch Fix — Execute Immediately

After the report, **fix everything that's clearly correct right now**. Do not present a phased timeline asking "which first" — the user wants delivery, not deliberation.

**Exception: Audit-only mode.** If the user only asked "rà soát" / "review" / "audit" without saying "fix" or "sửa", produce the report first and ask if they want fixes applied. The sequence is: report → "muốn tao fix luôn?" → if yes, execute.

But if the user says "rà soát" in a context where they expect actionable output (e.g. "mày rà soát cho tao" implies they'll want fixes), lean into fixing — produce the report, then immediately offer to batch-fix.

**Fix pattern per issue:**
1. Re-read the buggy file (don't rely on stale context from audit phase)
2. Verify the bug exists (e.g., check if `BACKEND_URL` is actually hardcoded or if it already uses env var fallback)
3. Apply the fix
4. Mark as ✅ in the batch-fix list
5. Move to next issue

**What to fix immediately vs. flag:**
- ✅ **Fix now** — route path mismatches, missing restart policies, missing healthchecks, `alert()` calls, missing metadata, missing error boundaries, .dockerignore files
- ⏳ **Flag for user** — removing dead code (means deleting files — ask), async rewrite (architecture decision), changing DB schemas (data migration)
- ❌ **Skip** — anything that's actually NOT broken (verify before "fixing" — e.g., BACKEND_URL might already use env var fallback)

**Post-fix verification:**
- For frontend fixes: check imports resolve, check TypeScript compilation
- For backend fixes: syntax check Python files
- For Docker fixes: validate docker-compose format
- List remaining ⏳ items for user to decide

## Detection Patterns

### Dead Code Detection
- Look for dual/co-existing implementations of the same feature
- Check which component is actually imported/used in page.tsx
- Flag unimported modules > 200 lines

### API Route Mismatch
- Cross-reference frontend `api.ts` paths with backend router prefixes
- Common: backend `/api/bookings` vs frontend `/api/booking`

### Async Blocking
- Check if sync HTTP libs (requests) are used inside async endpoints
- Should use httpx.AsyncClient or run_in_executor

### Fake/Test Data in Production
- Search for hardcoded passenger profiles, mock payments, fake credentials
- Flag any "generate default" patterns in booking/payment flows

### Dual Router / Dual Agent Conflict (FastAPI)
- Check if TWO separate router files define the same class of endpoint (e.g., `chat.py` at `/api/chat` AND `smart_agent.py` at `/api/v1/smart/chat`)
- Both may be included in `main.py` via `app.include_router()` — creating **two live agent endpoints** with different personalities/behaviors
- Signal: user gets different responses from `/api/chat` vs `/api/v1/smart/chat`
- Fix: choose one as primary, comment out the other's `include_router()` in `main.py`, add a redirect or deprecation notice

### Session State Fragility
- Check if state is in-memory dict (lost on restart)
- Should use Redis/external store (already in docker-compose)
- **Signal: `_chat_sessions: Dict[str, list] = {}` as module-level variable** — common in middleware-less FastAPI agents

### Double Prefix Bug (FastAPI)
- Check if router prefix + route paths double up (e.g., router prefix `/api` + `@router.get(\"/api/chat/history\")` = `/api/api/chat/history`)
- Correct: omit `/api` from the route path when the router already has prefix `/api`

### API Key in URL Query Param (Security)
- Check for patterns like `https://api.example.com/v1/endpoint?key={API_KEY}`
- **Vấn đề:** API key in URL = leaked via server logs, browser history, HTTP Referer headers, proxy logs
- Đúng: `Authorization: Bearer <key>` header
- Check also: direct Gemini API calls hardcoded instead of going through a central `llm_gateway.py` or provider abstraction layer

### Mock Price / Data Lookup with Wrong Route (Logic Bug)
- **Pattern:** A dict is iterated but `break` on first entry instead of matching the requested route:
  ```python
  # BAD — always uses first route's price regardless of actual booking
  base_price_per_pax = 1_200_000
  for (orig, dest), info in ROUTE_PRICES.items():
      base_price_per_pax = info["base"]
      break  # ❌ grabs HAN-SGN even if booking is SGN-DAD
  
  # FIX — match by actual route key
  route_key = (origin, destination)  # extract from request
  price_info = ROUTE_PRICES.get(route_key, {"base": 1_200_000})
  base_price_per_pax = price_info["base"]
  ```
- **Signal:** Mock/flat data dict where all lookups return the same default value — check the lookup logic, not just the data
- **Common in:** Phase 1 mock services (flights, hotels, esim) where dev iterates dict for demo then never returns to fix the lookup

### API Key in URL Query Param (Security)
- **Pattern:** Gemini/OpenAI key passed as `?key={API_KEY}` in URL instead of `Authorization: Bearer` header
  ```python
  # BAD — key leaked via server logs, proxy logs, HTTP Referer
  url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={gemini_key}"
  resp = await client.post(url, json=payload)
  
  # FIX — use Authorization header
  url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent"
  resp = await client.post(
      url,
      headers={
          "Authorization": f"Bearer {gemini_key}",
          "Content-Type": "application/json",
      },
      json=payload,
  )
  ```
- **Signal:** Any URL string containing `?key=`, `?api_key=`, or `?apikey=` followed by a variable
- **Search pattern:** `\?key=` or `\?api_key=` in strings across `.py`/`.js`/`.ts`/`.jsx`/`.tsx` files
- **Fix:** Move to standard `Authorization: Bearer <key>` header. Centralize all API key logic in a single gateway/abstraction layer so raw endpoint formulas aren't scattered across files.

### Dead RAG / Feature Module (Unused Code)
- Check if expensive/infrastructure-heavy modules (FAISS, embeddings, vector stores) are initialized but **never imported, never called, never used**
- Signal: module has 300+ lines, complex dependencies (torch, faiss-cpu, sentence-transformers), but zero references in the rest of the codebase
- Fix: remove file (if confirmed dead) or integrate into the active agent pipeline

### Docker Healthcheck / Restart Gaps
- Every service in docker-compose should have `restart: unless-stopped`
- Data services (DB, Redis) need healthcheck
- Backend API needs healthcheck pointing at its `/health` endpoint
- Frontend dev containers can skip healthcheck if no static health endpoint
- Check Dockerfile for missing system deps needed by healthcheck (e.g., `curl` in slim images)

### Hardcoded Values That Aren't Actually Hardcoded
- Before flagging a "hardcoded `BACKEND_URL`", check if it uses `||` / `??` fallback pattern
- Common: `process.env.NEXT_PUBLIC_BACKEND_URL || 'http://localhost:8765'` — this IS configurable, the fallback is just a default
- Read the actual line before reporting; env-var-fallback patterns are correct by design

### Python Bot-Specific Detection Patterns

#### Method that uses `self` but is a standalone `def`
```python
# BAD — crash on call because `self` is undefined
def _optimize_search_query(self, raw_query, intent):
    if not self.llm_api_key:  # AttributeError
        ...

# FIX — make it standalone, pass params explicitly
def _optimize_search_query(raw_query, intent, api_key=""):
    if not api_key:
        ...
```
- Single most common refactoring bug in Python bot codebases
- Check every `def` that looks like a method (has `self`) but is NOT inside a class
- Fix: remove `self`, add explicit params for what `self.xxx` was accessing

#### Wrong variable name in `return`
```python
# BAD — NameError at runtime
lines = [...]
return "\n".join(results)  # `results` doesn't exist!

# FIX
return "\n".join(lines)
```
- Common in copy-pasted `_build_vi` → `_build_en` patterns
- Signal: function has `lines = []` and `lines.append(...)` throughout, but `return` uses a different variable

#### Duplicate expensive calls (LLM, API)
```python
# BAD — calls LLM twice
response = self._quick_search(query, topic, intent)
# inside _quick_search: search_query = self._optimize_search_query(query, intent)

# FIX — compute once, pass as param
search_query = _optimize_search_query(query, intent)
response = self._quick_search(query, topic, intent, search_query=search_query)
```
- Look for the same method called in parent function AND in the child it calls
- Common with LLM query optimization, search re-ranking, embedding computation

#### Wrong Python package in requirements.txt
```python
# Source code has:
from ddgs import DDGS  # package name: ddgs

# requirements.txt has:
fourdigits>=0.1.2  # WRONG — will InstallError at runtime
```
- Cross-reference `import` statements in source code against `requirements.txt`
- Pay special attention to similar-sounding package names (ddgs vs fourdigits, etc.)

## Post-Fix Verification

After applying all fixes, run these checks in order:

### 1. Syntax Check
```bash
python -c "import module1; import module2; print('All modules syntax OK')"
```
- Import every modified module to catch syntax errors and ImportErrors at import time
- Do this from the project root directory

### 2. Class Instantiation Test
```bash
python -c "from modules.chat_brain import ChatBrain, optimize_search_fn; cb = ChatBrain(); print('ChatBrain OK')"
```
- Instantiate any changed classes to catch `__init__` signature mismatches
- Verify standalone functions work with test params

### 3. Feature-Specific Test
```python
# Test the specific fix with a targeted inline test
from web_research import filter_results
filtered = filter_results(
    [{'title': 'Amazon buy', 'url': 'https://amazon.com/x', 'snippet': 'price low'}],
    context_topic='AI'
)
assert len(filtered) == 0, "filter should discard Amazon"
```
- Write a minimal inline test that exercises each changed code path
- One-liner per fix, all in one `python -c` call

### 4. Process Health
```bash
# Start bot + check log for 5-10 seconds
# Verify: no ERROR/CRITICAL/ConflictError/Traceback in log
# Verify: "Bot: @username" appears (confirms token is valid)
```

## Pitfalls
- Search_files can fail with complex exclusions → use Python glob instead
- Don't skip config/infra files — they often reveal the most problems
- Test files often lie about their coverage — actually read them
- Backend.log files reveal runtime errors not visible in code
- `.hermes/plans/` directories contain design decisions — read them for context
- **CRITICAL: Do NOT present a phased timeline after the report.** Don't say "tuần này fix X, tuần sau fix Y". The user wants everything fixed NOW. If something truly needs discussion (deleting files, architecture changes), flag it as ⏳ but fix everything else immediately.
- **Verify before reporting.** If something looks hardcoded, read the actual line to check for env-var fallback patterns (`||` / `??`). False positives waste user trust.
- **Don't ask permission for each fix.** Batch all clearly-correct fixes and do them in one pass. Only pause for issues with real trade-offs (e.g., "should I delete this file?").
