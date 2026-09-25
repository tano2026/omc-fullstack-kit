# RIO v2.0 Modules — Architecture Reference

> Cập nhật từ code thực tế (Jul 2026).
> Build từ daily-hot-mcp (MIT) + httpx/urllib pattern.

## Module Structure (rio-bot/modules/)

```
modules/
├── __init__.py           # Auto-discover + test import
├── cn_trends.py          # 9 Chinese social media sources
├── global_trends.py      # 6 global trending sources
├── web_research.py       # DDG→Bing→Wikipedia chain
├── deep_research.py      # L0-L3 research tiers
├── video_extract.py      # YouTube metadata + transcript
└── report_gen.py         # Watchlist, history, formatting
```

## Key Design Decisions

1. **No API keys needed** — all sources free/scrape-able
2. **Triple fallback** per source: httpx → urllib → simulate
3. **60s cache** via @lru_cache(maxsize=1)
4. **3-tier strategy** per platform: live (httpx) → mirror (json hosting) → mock (static data)
5. **Timeout = 10s** per source — Telegram long-poll can't block more than 35s total

## Commands → Module Map

| Command | Module | Sources |
|---------|--------|---------|
| `/trend cn` | cn_trends | Douyin, Weibo, Xiaohongshu, Bilibili, Kuaishou, Baidu, Zhihu, 36Kr, Hupu |
| `/trend global` | global_trends | GitHub, Google, Reddit, Twitter, Product Hunt, NewsAPI |
| `/research <q>` | web_research | DuckDuckGo → Wikipedia → Bing |
| `/research deep <q>` | deep_research (L2) | Top 5 search results → extract content → LLM synthesis |
| `/research quick <q>` | deep_research (L0) | DuckDuckGo → top 3 snippets |
| `/brief <topic>` | deep_research (L1) | Multi-term search → category summary |
| `/video <url>` | video_extract | yt-dlp metadata → yt-dlp transcript (vi/en) |
| `/niche <topic> [market]` | deep_research | Market structure → competitors → gap analysis |
| `/watch <keyword>` | report_gen | Append to watchlist.json |
| `/watch list` | report_gen | Read watchlist.json → format |
| `/watch rm <kw>` | report_gen | Remove from watchlist.json |
| `/trending [date]` | report_gen | Read history.json → format |

## Individual Module Details

### cn_trends.py — 9 Chinese Sources

```python
def get_cn_trends(source="all") -> dict:
    """Fetch Chinese social media trends. Source: 'douyin' | 'weibo' | 'all'"""

def fetch_weibo_hot() -> list[dict]:
    """Weibo Hot Search list — 50 trending topics"""
    # Strategy: weibo.com/ajax/jsonp/hottopics → mirror → mock

def fetch_baidu_hot() -> list[dict]:
    """Baidu Hot Search — https://top.baidu.com/board"""
    # Strategy: httpx → urllib → mock

def fetch_douyin_hot() -> list[dict]:
    """Douyin Hot List — 抖音热点榜"""
    # Strategy: douyin.com/aweme/v1/web/hot/search/list → mirror → mock

def fetch_bilibili_hot() -> list[dict]:
    """Bilibili Hot — api.bilibili.com/x/web-interface/popular"""
    # Strategy: httpx → urllib → mock

def fetch_xiaohongshu_hot() -> list[dict]:
    """Xiaohongshu Trending — 小红书热搜"""
    # Strategy: edith.xiaohongshu.com/api/sns/web/v1/search/trending → mock

def fetch_kuaishou_hot() -> list[dict]:
    """Kuaishou Hot — 快手热榜"""
    # Strategy: www.kuaishou.com → mock

def fetch_zhihu_hot() -> list[dict]:
    """Zhihu Hot — www.zhihu.com/hot"""
    # Strategy: zhihu.com/api/v3/feed/topstory → mock

def fetch_36kr_hot() -> list[dict]:
    """36Kr Hot — 36氪热搜"""
    # Strategy: mock (36kr blocks non-browser clients)

def fetch_hupu_hot() -> list[dict]:
    """Hupu Hot — https://bbs.hupu.com/all-gambia"""
    # Strategy: mock
```

**Crawl strategy tri-fallback:**
```
httpx.get(url, headers=CHROME, timeout=10, follow_redirects=True)
   → urllib.request(req, timeout=10)
      → return []  # mock empty
```

### global_trends.py — 6 Global Sources

```python
def get_global_trends(source="all") -> dict:
    """Fetch global trends. Source: 'github' | 'reddit' | 'all'"""

def fetch_github_trending(language="") -> list[dict]:
    """GitHub Trending — github.com/trending"""
    # Parse HTML for repo name, stars, description, language

def fetch_google_trending() -> list[dict]:
    """Google Daily Trends"""
    # Parse news.google.com/topstories → titles + sources

def fetch_reddit_hot(subreddit="all") -> list[dict]:
    """Reddit Hot — reddit.com/r/all/hot.json"""
    # Free JSON endpoint — most reliable

def fetch_twitter_trending(woeid=23424975) -> list[dict]:
    """Twitter Trending — trend via proxy (limited)"""
    # Mock — Twitter API requires auth

def fetch_producthunt_hot() -> list[dict]:
    """Product Hunt Trending"""
    # Mock — PH requires API key

def fetch_newsapi_hot() -> list[dict]:
    """NewsAPI top headlines (free tier, 100/day)"""
    # Uses newsapi.org free tier
```

### web_research.py

```python
def research(query: str, max_results: int = 5) -> list[dict]:
    """Multi-engine search: DDG → Bing → Wikipedia"""
    # Returns unified [{title, url, snippet, source}] format

def search_duckduckgo(query, max_results=5) -> list[dict]:
    """DuckDuckGo HTML endpoint — no API key needed"""

def search_bing(query, max_results=5) -> list[dict]:
    """Bing HTML search — fallback if DDG fails"""

def search_wikipedia(query, max_results=3) -> list[dict]:
    """Wikipedia API — structured content, high quality"""
```

### deep_research.py — L0-L3 Tiers

```python
def deep_research(topic: str, tier: str = "L2") -> dict:
    """Tiered research:
    L0: DDG top 3 snippets only
    L1: DDG top 5 + Wikipedia + extract top 2 URLs
    L2: L1 + Bing + extract top 5 URLs + LLM synthesis
    L3: L2 + multi-term search + cross-reference
    """

def extract_url_content(url: str, max_chars: int = 3000) -> str:
    """Fetch + strip HTML → plain text"""

def synthesize_results(query: str, results: list[dict]) -> str:
    """LLM synthesis of multiple sources into coherent summary"""

# Format: markdown with sections:
# ## Executive Summary
# ## Key Findings
# ## Sources
```

### video_extract.py

```python
def extract_video(url: str) -> dict:
    """Extract metadata + transcript from video URL.
    Works best with YouTube (yt-dlp).
    Returns {title, duration, views, description, transcript, error}
    """

def get_youtube_metadata(video_id: str) -> dict:
    """yt-dlp --print-json for title, duration, upload_date, view_count"""

def get_youtube_transcript(video_id: str, lang: str = "vi") -> str:
    """yt-dlp --write-subs --sub-langs vi,en --convert-subs srt"""

def format_transcript(transcript: str) -> str:
    """Clean SRT → readable text (remove timestamps, join lines)"""
```

### report_gen.py

```python
def format_trends(data: list[dict], source_name: str, max_items: int = 15) -> str:
    """Format trend list as compact Markdown:
    #🔥 Weibo Hot Search
    1. Title (热度 N万) — snippet
    2. Title (热度 N万) — snippet
    """

def manage_watchlist(action: str, keyword: str = None) -> list:
    """watchlist.json CRUD: add/list/remove"""

def save_history(entry: dict):
    """Append to history.json with timestamp"""

def format_history(date: str = None) -> str:
    """Format history.json → readable Markdown"""
```

## Caching Strategy

```python
from functools import lru_cache
import time

@lru_cache(maxsize=1)
def fetch_cached(url: str, ttl: int = 60) -> str:
    """Cache URL content for `ttl` seconds.
    Cache key = url, auto-invalidates after ttl.
    """
    # httpx → urllib → mock
```

## Pitfalls

1. **Chinese sites block non-Chinese IPs** — 36Kr, Xiaohongshu return 403/302 from non-CN IPs; mock fallback returns empty
2. **Douyin API changes frequently** — the `aweme/v1/web/hot/search/list` endpoint changes signature; mirror fallback essential
3. **Rate limiting** — httpx 10s timeout + 60s cache prevents accidental flooding
4. **Mock data** — when all sources return empty, show graceful "Unavailable — try /trend global instead"
5. **yt-dlp on Windows** — needs to be in PATH; use `which yt-dlp || where yt-dlp` before calling
6. **Transcript languages** — YouTube auto-captions often have only `a.en` (auto English); try `vi`, `en`, `a.en` in order
