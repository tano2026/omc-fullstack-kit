# Telegram Bot Session Commands — Reference

## Problem

User chats naturally on Telegram. CEO bot must know which project they're talking about. 
Old approach: keyword detection only ("dự án GMSP...") → unreliable on follow-up messages.
New approach: explicit session locking + keyword fallback.

## Session Architecture

```python
_project_sessions: dict[int, str] = {}  # chat_id → project name

def handle(chat_id, text):
    if text.startswith("/"):
        cmd = parse_command(text)
        if cmd == "gmsp":
            _project_sessions[chat_id] = "GMSP"
            return send(chat_id, "🗂️ Đã chuyển sang dự án *GMSP*...")
        # ... repeat for airfare, abtrip, tuvi, fasttrack
        if cmd in ("thoát", "all", "tổng quát"):
            _project_sessions.pop(chat_id, None)
            return send(chat_id, f"🗂️ Đã thoát dự án *{old}*...")
        if cmd in ("new", "reset", "clear"):
            _project_sessions.pop(chat_id, None)
            return send(chat_id, "🗂️ Đã reset session... Lịch sử cũ vẫn lưu.")
```

## Priority

1. **Session** (`_project_sessions.get(chat_id)`) — if user typed `/gmsp`, all messages use GMSP
2. **Keyword** (`_detect_project(text)`) — auto-detect from message text
3. **Global** — neither → CEO responds generally

## Keyword Map

```python
PROJECT_NAMES = {
    "gmsp": "GMSP",
    "giải mã": "GMSP", "giai ma": "GMSP",
    "abtrip": "ABTrip", "ab trip": "ABTrip",
    "tử vi": "Tử Vi", "tu vi": "Tử Vi", "bói": "Tử Vi",
    "airfare": "AirFares Decoded", "airfares": "AirFares Decoded",
    "fast track": "Fast Track", "nội bài": "Fast Track", "noi bai": "Fast Track",
    "trùm du lịch": "ABTrip", "trùm sân bay": "Fast Track",
}
```

## "CEO đang nghĩ..." Anti-Pattern

**DO NOT**: send a placeholder message "CEO đang nghĩ..." then another with the response.
**DO**: use Telegram's `sendChatAction` typing indicator (fire-and-forget).

```python
def cmd_natural(chat_id, text):
    t0 = time.time()
    # Fire-and-forget typing indicator — no user-visible message
    tg_no_wait("sendChatAction", chat_id=chat_id, action="typing")
    
    project = _project_sessions.get(chat_id) or _detect_project(text)
    # ... build system prompt, call LLM ...
    
    # ONLY 1 message sent to user
    if out:
        send(chat_id, out)
    else:
        send(chat_id, "CEO ko tra loi duoc...")

def tg_no_wait(method, **params):
    """Fire-and-forget — ko đợi response, ko log error."""
    data = urllib.parse.urlencode(params).encode("utf-8")
    try:
        req = urllib.request.Request(f"{API}/{method}", data=data)
        urllib.request.urlopen(req, timeout=5)
    except:
        pass
```

## Session Lifecycle

```
User: /gmsp
Bot: 🗂️ Đã chuyển sang dự án GMSP [session set]
User: script EP02 đâu rồi?
Bot: [trả lời về GMSP — session context]
User: còn background music dùng gì?
Bot: [vẫn GMSP — session chưa thoát]
User: /thoát
Bot: 🗂️ Đã thoát dự án GMSP [session cleared]
User: /new
Bot: 🗂️ Đã reset session [same as /thoát but explicit intent]
```
