# Web Search Resilience — Lessons Learned

## Problem

RIO Bot's `web_research.py` search_ddg() used DuckDuckGo HTML scraping (`https://html.duckduckgo.com/html/`). When DDG changed their HTML layout, **all searches returned 0 results** for weeks without detection. The regex patterns:

```python
# BROKEN: DDG changed layout
blocks = re.findall(r'<a rel="nofollow" class="result__a" ...>', html_content)
snippets = re.findall(r'<a class="result__snippet" ...>', html_content)
```

## Root Causes

1. **Fragile parsing:** Regex depends on exact HTML structure. Any DDG layout change breaks silently (returns `[]`, not an error).
2. **No fallback test:** `_search_bing()` also broke — Bing, Google, Brave all return captcha/block pages from this host.
3. **No health check:** The bot reported "0 sources" without distinguishing "no content found" from "search engine blocked".

## Solution: Replace with `ddgs` library

```bash
pip install ddgs
```

```python
from ddgs import DDGS

def search_ddg(query, max_results=8) -> list:
    """DuckDuckGo search via ddgs library — API-based, not HTML scraping.
    
    Fallback chain: DDGS → Bing → Wikipedia
    Không fallback khi có kết quả, chỉ fallback khi DDGS fail/0 results.
    """
    if not HAVE_DDGS:
        return _search_bing(query, max_results)  # fallback immediately
    
    try:
        with DDGS() as ddgs:
            raw = list(ddgs.text(query, max_results=max_results))
    except Exception as e:
        log.warning(f"DDGS error: {e} → fallback Bing")
        return _search_bing(query, max_results)
    
    if not raw:
        return _search_bing(query, max_results)  # 0 results → fallback
    
    results = []
    for r in raw:
        results.append({
            "title": r.get("title", "").strip(),
            "url": r.get("href", r.get("link", "")).strip(),
            "snippet": r.get("body", r.get("snippet", "")).strip(),
        })
    return results or _search_bing(query, max_results)
```

## DDGS on Windows MSYS — Known Behaviors

- **Context manager reconnect:** Mỗi lần `with DDGS():` tạo connection mới. Không cache session. Trên Windows MSYS (git-bash), reconnect overhead ~300-500ms nhưng ổn định.
- **Rate limit:** DDGS có internal rate limiting. Nếu gọi 5+ query nhanh liên tiếp, có thể bị trả về 0 results. Giải pháp: đã có ratelimit.py (1 req/2s).
- **Fallback chain quan trọng:** Nếu DDGS trả về 0 results (rate limit), auto fallback Bing → Wikipedia. Không để bot im lặng với 0 sources.
- **Import guard:** Luôn wrap trong try/except với HAVE_DDGS flag, vì DDGS không phải stdlib. Nếu chưa pip install, bot fallback Bing thay vì crash.

## Alternative search engines tested (Jul 2026)

| Engine | Method | Status |
|--------|--------|--------|
| DuckDuckGo lite | `html.duckduckgo.com` HTML scrape | ❌ Layout change + rate limit |
| DuckDuckGo | `ddgs` library (API) | ✅ Working |
| Google | `google.com/search` scrape | ❌ Captcha block |
| Bing | `bing.com/search` scrape | ❌ Captcha block |
| Brave | `search.brave.com` scrape | ❌ HTTP 429 |
| Qwant | `lite.qwant.com` scrape | ❌ 0 results |

## Prevention

- **Don't rely on HTML scraping** for search engines. Use libraries (`ddgs`, `googlesearch-python`, etc.) that handle API changes internally.
- **Add search health check** — periodic test query + result count alert.
- **Log search failures with detail** — log "DDG returned {n} results" vs "DDG exception: {e}" so you can distinguish content gaps from search engine blocks.

## Quick verification

To test if DDG search works from a given host:

```python
from ddgs import DDGS
with DDGS() as ddgs:
    results = list(ddgs.text('fastrack noi bai', max_results=3))
    print(f"Results: {len(results)}")
    for r in results:
        print(f"  [{r['title'][:50]}] {r['href'][:60]}")
```
