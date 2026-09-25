# Telegram `sendChatAction` — No-spam typing indicator

**Problem:** Sending "CEO đang nghĩ..." creates 2 messages per chat (spammy, user complained).

**Fix:** Use Telegram `sendChatAction` — shows "...đang gõ" indicator WITHOUT sending a message.

## Implementation (from `main.py`)

```python
def tg_no_wait(method, **params):
    """Fire-and-forget — ko đợi response, ko block."""
    data = urllib.parse.urlencode(params).encode("utf-8")
    try:
        req = urllib.request.Request(f"{API}/{method}", data=data)
        urllib.request.urlopen(req, timeout=5)
    except:
        pass

# Usage before LLM call:
tg_no_wait("sendChatAction", chat_id=chat_id, action="typing")
```

## Flow
1. User sends message
2. `tg_no_wait("sendChatAction", action="typing")` — Tele shows "CEO đang gõ..."
3. LLM call (blocking, could be 3-15s)
4. `send(chat_id, response)` — 1 message only, no intermediate spam

## Available actions
- `typing` — for text messages
- `upload_photo` — for images
- `upload_video` — for videos
- `find_location` — for location

## Key difference from old pattern
Before: `send(chat_id, "CEO đang nghĩ...")` then `send(chat_id, response)` = 2 messages
After: `tg_no_wait(typing)` then `send(chat_id, response)` = 1 message + indicator
