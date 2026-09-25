# Web Search Adapter Recipe (DuckDuckGo HTML Scrape)

Zero-API-key web search cho AgentBrain adapters. Không cần SerpAPI, không cần Firecrawl, không cần token nào — chỉ stdlib Python + DuckDuckGo HTML endpoint.

## Implementation

```python
import urllib.parse
import urllib.request
import re

def _web_search(query, max_results=5, **kw):
    """
    Web search thật — gọi DuckDuckGo HTML scraper.
    Brain gọi search-like adapters với (query, max_results=5).
    fallback: brain gọi (topic=..., **params).
    Dùng **kw để bắt cả 2 convention.
    """
    q = query or kw.get("topic", "")
    if not q:
        return [{"title": "[search] empty query", "url": "", "snippet": "..."}]

    try:
        encoded = urllib.parse.quote(q)
        url = f"https://html.duckduckgo.com/html/?q={encoded}"
        req = urllib.request.Request(url, headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "Accept": "text/html,application/xhtml+xml",
        })
        with urllib.request.urlopen(req, timeout=15) as resp:
            html = resp.read().decode("utf-8", errors="replace")

        items = []
        for result in html.split('<div class="result__body"')[1:max_results+1]:
            title = ""
            snippet = ""
            link = ""
            tm = re.search(r'<a[^>]*class="result__a"[^>]*>(.*?)</a>', result, re.DOTALL)
            if tm:
                title = re.sub(r'<[^>]+>', '', tm.group(1)).strip()
            lm = re.search(r'href="(https?://[^"]+)"', result)
            if lm:
                link = lm.group(1)
            sm = re.search(r'<a[^>]*class="result__snippet"[^>]*>(.*?)</a>', result, re.DOTALL)
            if sm:
                snippet = re.sub(r'<[^>]+>', '', sm.group(1)).strip()
            if title or snippet:
                items.append({
                    "title": title or link[:80],
                    "url": link,
                    "snippet": snippet or title or "",
                })
        return items if items else [
            {"title": f"[search] {q[:40]}", "url": "",
             "snippet": f"Kết quả tìm kiếm cho: {q}"}
        ]
    except Exception as e:
        return [{"title": f"[search error] {e}", "url": "", "snippet": str(e)}]
```

## Integration Pattern

### 1. Trong agents/__init__.py — auto-inject

```python
def get_brain(name: str, live: dict = None, ...):
    if live is None:
        live = {}
    try:
        from real_adapters import build_real_registry
        real_adapters = build_real_registry(name)
        for k, v in real_adapters.items():
            if k not in live:
                live[k] = v
    except ImportError:
        pass
    registry = mod.build_registry(**live)
    return AgentBrain(mod.SPEC, adapters=registry, ...)
```

### 2. Trong real_adapters.py — per-agent factory

```python
def build_real_registry(agent_name: str) -> dict:
    adapters = {
        "search": _web_search,
        "web_search": _web_search,
        "lead_search": _web_search,
        "seo": _web_search,
        "trends": _web_search,
        "social_search": _web_search,
    }
    if agent_name == "dev":
        adapters.update({
            "repo": _repo_info,        # git status, file list
            "infra": _infra_health,    # disk, uptime
        })
    elif agent_name == "operations":
        adapters.update({
            "infra": _infra_health,
            "db": _db_query,           # SQLite schema scan
        })
    elif agent_name == "support":
        adapters.update({
            "ticket": _ticket_system,  # KV-store tickets
            "reply_out": _delivery_outbox,  # write to JSON outbox
        })
    # ... etc
    return adapters
```

## ⚠️ Critical: SEARCH_LIKE set

Trong `core/brain.py`, có 1 set tên adapters được coi là "search-like":

```python
SEARCH_LIKE = {"search", "serp", "web", "web_search", "social_search",
               "trends", "news", "discover", "lead_search", "seo",
               "social", "kb", "footage"}
```

**Nếu mày thêm 1 adapter search mới (vd `lead_search`, `social_search`, `kb`), phải thêm tên nó vào set này.** Nếu không, brain sẽ gọi adapter với `fn(topic=task.topic)` thay vì `fn(query, max_results=5)` → adapter nhận `topic=` thay vì `query=` → lặng lẽ fail hoặc trả về rỗng.

**Triệu chứng khi quên:**
- COLLECT stage ra 0 items (hoặc 1 item lỗi)
- Verify fail vì "min_sources_2"
- Adapter log `_web_search() got an unexpected keyword argument 'topic'`

**Cách fix nhanh (nếu không edit core):** thêm `**kw` vào signature hàm search để bắt cả 2 convention:

```python
def _my_search(query, max_results=5, **kw):
    q = query or kw.get("topic", "")
```

## Other Common Adapter Types

### Infra Health
```python
def _infra_health(topic=None, **kw):
    import subprocess
    items = []
    try:
        result = subprocess.run(["df", "-h", "/"], capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            lines = result.stdout.strip().split("\n")
            if len(lines) >= 2:
                parts = lines[1].split()
                items.append({"title": "Disk usage (/)",
                    "snippet": f"Total: {parts[1]}, Used: {parts[2]}, Avail: {parts[3]}, Use%: {parts[4]}"})
    except Exception:
        pass
    return items
```

### DB Scan
```python
def _db_query(topic=None, **kw):
    import sqlite3
    from pathlib import Path
    items = []
    for db_path in Path("data").glob("*.db"):
        try:
            conn = sqlite3.connect(str(db_path))
            cur = conn.execute("SELECT name FROM sqlite_master WHERE type='table' LIMIT 10")
            tables = [r[0] for r in cur.fetchall()]
            conn.close()
            items.append({"title": f"🗄️ {db_path.name}", "snippet": f"Tables: {', '.join(tables)}"})
        except Exception:
            pass
    return items
```

### Delivery Outbox
```python
def _delivery_outbox(task=None, chunks=None, report=None, **kw):
    """Ghi output vào JSON outbox — Hermes/TG bot pick up."""
    import json, time, os
    entry = {
        "ts": time.time(),
        "agent": task.agent if task else "?",
        "ttype": task.ttype if task else "?",
        "chunks": chunks,
        "report": (report or "")[:2000],
    }
    outbox_path = "outbox.json"
    existing = []
    if os.path.exists(outbox_path):
        with open(outbox_path, "r") as f:
            existing = json.load(f)
    existing.append(entry)
    with open(outbox_path, "w") as f:
        json.dump(existing[-50:], f, ensure_ascii=False, indent=2)
    return {"sent": True, "channel": "outbox.json", "note": "Đã ghi vào outbox."}
```
