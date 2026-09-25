# Social Platform Research — From Telegram Polling Bot

> Khi research từ Telegram bot (ko có browser, ko có API key), đây là các platform có thể crawl + cách tối ưu.

## Coverage Matrix

| Platform | Web search | Accuracy | Best for | Workaround |
|----------|-----------|----------|----------|------------|
| **YouTube** | `site:youtube.com <query>` | 📺 Medium (view counts from snippet) | Titles + views + channel | Use `youtube-research-agent` skill for deep analysis (browser) |
| **TikTok** | `site:tiktok.com <query>` | 🎵 Low (titles only, no views) | Content discovery only | TikTok blocks most scraping; DuckDuckGo returns limited results |
| **Reddit** | `site:reddit.com <query>` | 🟦 High (snippets have upvotes) | Real discussions + sentiment | `.json` endpoint adds structured data |
| **X/Twitter** | `site:x.com <query>` | 𝕏 Medium (trending posts) | Real-time trends | X API free tier exists (1.5K reads/mo) |
| **GitHub** | `site:github.com <query>` | 💻 High (stars + desc in snippet) | Trending repos | GitHub API free tier generous |
| **Douyin (抖音)** | — (use API) | 🔥 High (direct from Douyin internal API) | Trung Quốc hot trends, social topics | GET `douyin.com/aweme/v1/web/hot/search/list/` — no auth, returns real-time trending with `hot_value` |
| **Weibo (微博)** | — (use API) | 🔥 High (direct from Weibo internal API) | Trung Quốc tin tức, sự kiện, giải trí | GET `weibo.com/ajax/side/hotSearch` — returns `realtime` array with `num` (heat score) |
| **Xiaohongshu (小红书)** | — (use API) | 📗 High (likes/comments/shares) | Lifestyle/beauty/fashion trends TQ | XHS web API hot notes or hot search list; has fallback logic |
| **Bilibili (B站)** | — (use API) | 📺 High (view/like/coin) | Giới trẻ TQ, gaming, anime | Bilibili ranking API — `api.bilibili.com/x/web-interface/ranking/v2` |
| **Baidu** | — (use API) | 🔥 High | Tổng hợp tin tức TQ | Baidu hot search list |
| **Zhihu (知乎)** | — (use API) | 💬 High (Q&A discussions) | Tâm lý xã hội TQ, debates | Zhihu hot list API |

## Platform-Specific Caveats

### TikTok
- **No public API** for content discovery (only Ads API — paid)
- `site:tiktok.com` on DuckDuckGo returns inconsistent results
- TikTok aggressively blocks headless browsers
- **Alternative**: use `trending-content-scout` skill's keyword analysis pattern (web_search fallback)
- For Tano Agency: TikTok research ≈ content inspiration, not reliable competitive data

### Chinese Platforms — Direct API (No Auth, No API Key)

Vietnamese audiences follow Chinese trends closely. These platforms expose internal trending APIs that return structured JSON without authentication:

**Douyin (抖音) — Hot Search List**
```
GET https://www.douyin.com/aweme/v1/web/hot/search/list/?device_platform=webapp&aid=6383&detail_list=1
```
Response: `word_list[]` with `word` (title), `hot_value` (heat score), `sentence_id` (→ link `douyin.com/hot/{sentence_id}`), `event_time` (timestamp)
Note: Sometimes needs `passport_csrf_token` cookie — fetch from `/passport/general/login_guiding_strategy/` first

**Weibo (微博) — Hot Search**
```
GET https://weibo.com/ajax/side/hotSearch
```
Response: `realtime[]` with `word` (title), `num` (heat score, e.g. 2,575,321), `word_scheme` (URL), `is_ad` (skip if 1), `note`
Filter: skip items where `is_ad=1`

**Xiaohongshu (小红书) — Trending Notes**
Primary:
```
GET https://www.xiaohongshu.com/web_api/sns/v3/page/notes?sort=hot&page_size=20
```
Response: `notes[]` with `note_card` (title, desc, interact_info with liked_count/comment_count/share_count, user info, cover, note_id)
Fallback (hot search keywords):
```
GET https://www.xiaohongshu.com/web_api/sns/v1/search/hot_list
```
Response: `queries[]` with hot search keywords

**Bilibili (B站) — Ranking**
```
GET https://api.bilibili.com/x/web-interface/ranking/v2?rid=0&type=all
```
Response: `data.list[]` with `title`, `stat` (view/like/coin/share), `owner` (name/face/mid), `pic` (cover), `short_link_v2`

**Baidu Hot Search**
```
GET https://top.baidu.com/board?tab=realtime
```
Also: various aggregate APIs for Baidu trending

**Zhihu (知乎) Hot List**
```
GET https://www.zhihu.com/api/v3/feed/topstory/hot-lists/total?limit=50
```
Response: `data[]` with `target` (title, url, excerpt, metrics area)

**Source**: these endpoint patterns are adapted from `daily-hot-mcp` (fancyboi999, MIT license — github.com/fancyboi999/daily-hot-mcp). Each platform module is 50-100 lines of Python. Use them as standalone modules in your bot script.

### YouTube
- Best platform for bot-based research — DuckDuckGo consistently returns titles, channel names, and view counts in snippets
- View count regex pattern: `(\d[\d,.]*)\s*(?:view|lượt xem)`
- Channel extraction: `by\s+(.+?)\s+` 
- Can supplement with YouTube Data API v3 (free tier: 10K requests/day, needs API key)

### Reddit
- `.json` endpoint (append `.json` to any Reddit URL) returns structured data
- Search: `https://www.reddit.com/r/all/search.json?q={query}&sort=top&t=month`
- Rate limit: 60 requests/minute (unauthed), generous
- Upvotes + comments available in JSON
- **Best free source for real user sentiment**

### X/Twitter
- `site:x.com` works but snippet quality varies
- X API Free tier: 1,500 posts/month, search endpoint limited
- Basic tier ($100/mo): 10K posts/month, full search
- **For Tano Agency**: use only if client needs X monitoring (worth $100/mo)

## Quick Reference: Search URL Patterns

```
YouTube:  site:youtube.com <keyword> views
TikTok:   site:tiktok.com <keyword> OR   <keyword> tiktok
Reddit:   site:reddit.com <keyword>
X:        site:x.com <keyword> OR site:twitter.com <keyword>
GitHub:   site:github.com <keyword>
News:     site:vnexpress.net <keyword> OR site:techcrunch.com <keyword>

# Chinese platforms — use direct API, not web search:
Douyin:   GET douyin.com/aweme/v1/web/hot/search/list/?aid=6383&detail_list=1
Weibo:    GET weibo.com/ajax/side/hotSearch
Xiaohongshu: GET xiaohongshu.com/web_api/sns/v3/page/notes?sort=hot&page_size=20
Bilibili: GET api.bilibili.com/x/web-interface/ranking/v2?rid=0&type=all
Baidu:    GET top.baidu.com/board?tab=realtime
Zhihu:    GET zhihu.com/api/v3/feed/topstory/hot-lists/total?limit=50
```

## Combined Research Workflow (from bot `/research all`)

1. **Phase 1 (5-10s)**: Web search DuckDuckGo for all platforms in parallel
2. **Phase 2 (10-15s)**: Extract + normalize results per platform
3. **Phase 3 (2-3s)**: Build cross-platform report with view counts where available
4. **Delivery**: Send 1 consolidated message (avoid Telegram flood control)

## When to Upgrade from Free

Upgrade to API mode when:
- Client needs **daily competitor monitoring** (TikTok/X → paid APIs)
- Engagement data accuracy matters (YouTube Data API)
- Bot generates revenue (cost is deductible)
- User asks "can you give me exact view counts?"

Otherwise, web_search + DuckDuckGo is sufficient for content inspiration and trend spotting.

## References in AI-Vibe-Toolkit

| Skill | File | Purpose |
|-------|------|---------|
| `trending-content-scout` | `affiliate-skills/research-trending-content-scout.md` | Cross-platform scan with engagement scoring |
| `youtube-research-agent` | `content/youtube-research-agent/SKILL.md` | Deep YouTube channel analysis |
| `last30days` | `last30days/SKILL.md` | Community signal from Reddit/X/HN/YouTube |
| `social-media-stack` | `social-media-stack/SKILL.md` | Platform-specific cheat sheet |
| `x-research` | `x-research/SKILL.md` | Dedicated X/Twitter research (needs Bearer token) |

## External References

| Project | Description | Link |
|---------|-------------|------|
| **daily-hot-mcp** | Python MCP server — 30+ trending sources (60% Chinese). MIT license. Copy individual platform modules into your bot. | [github.com/fancyboi999/daily-hot-mcp](https://github.com/fancyboi999/daily-hot-mcp) |
| **DailyHotApi** | Node.js API server — 45 Chinese + global platforms. Deploy on Vercel free tier. JSON + RSS output. | [github.com/imsyy/DailyHotApi](https://github.com/imsyy/DailyHotApi) |
| **Weibo Trending Archive** | Hourly Weibo hot search archive since 2021. Free historical data. | [github.com/v5tech/weibo-trending-hot-search](https://github.com/v5tech/weibo-trending-hot-search) |
| **TikHub API** | Paid unified API for 16+ platforms (Douyin, Xiaohongshu, Bilibili, Weibo, TikTok, etc.). Free trial via daily check-in. | [tikhub.io](https://tikhub.io/) |
