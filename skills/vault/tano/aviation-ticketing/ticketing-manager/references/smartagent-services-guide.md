# SmartAgent — Multi-Service Architecture Guide

> Tích hợp vào `ticketing-manager` skill: kiến trúc 5 service cho chat bot phòng vé.

## Kiến trúc tổng quan

```
UI (chat.html) → API (POST /api/chat) → _handle_ticketing()
                                            │
                              classify_service(message)
                                            │
              ┌────────────────┬────────────┼────────────┬────────────┐
              ▼                ▼            ▼            ▼            ▼
          fasttrack          esim        visa        passport     flight
      smart_fasttrack.py  smart_esim.py  smart_ /home/ubuntu/dev/hermes/workspace/backend/app/services/
    
```

## Service handler pattern

Mỗi service có:
1. Module: `smart_<service>.py` trong `app/services/`
2. Format function: `handle_<service>(message: str) -> str` — nhận message, trả reply text
3. Data dictionary: service info, pricing, features
4. Auto-detect function: `_get_xxx_key(text)` — map user message → service item

### Định dạng reply

- Dùng emoji prefix: `⚡ Fast Track`, `📶 eSIM`, `🛂 Visa`, `📄 Passport`, `✈️ Flight`
- Bold headings: `**Service Name**`
- Bullet points: `•` với indent 2 spaces
- Giá: `**giá**` bold
- Kết thúc: `💡 Bạn muốn...` + suggestions list
- Italic note: `*note text*`

### Cấu trúc file

```python
"""smart_<service>.py — Smart Agent Service

Cung cấp thông tin dịch vụ X.
"""

from typing import Optional

_DATA = {
    "item_key": {
        "name": "...",
        "description": "...",
        "features": [...],
        "price": {"retail": int, "agent": int},
        "hours": "...",
        "note": "...",
    }
}

def _get_key(text: str) -> Optional[str]:
    """Map user input → item key."""
    text_lower = text.lower()
    mapping = {...}
    for keyword, key in mapping.items():
        if keyword in text_lower:
            return key
    return None

def format_info(item_key: Optional[str] = None) -> str:
    """Format as HTML-friendly string."""
    ...

def handle_<service>(message: str) -> str:
    """Main handler."""
    key = _get_key(message)
    return format_info(key)
```

## Routing trong chat.py

```python
# STEP 0: SmartAgent Service Router
from app.services.smart_fasttrack import handle_fasttrack
from app.services.smart_esim import handle_esim
from app.services.smart_visa import handle_visa
from app.services.smart_passport import handle_passport
from app.services.intent_parser import classify_service

async def _handle_smart_service(message, session_id, session, service):
    """Route to correct service handler."""
    handlers = {
        "fasttrack": (handle_fasttrack, ["Fast Track Nội Bài", "..."]),
        "esim": (handle_esim, ["eSIM Châu Á", "..."]),
        "visa": (handle_visa, ["Visa Nhật Bản", "..."]),
        "passport": (handle_passport, ["Làm hộ chiếu", "..."]),
    }
    handler_fn, suggestions = handlers.get(service, (None, []))
    reply = handler_fn(message)
    session["history"].append(...)
    return ChatResponse(reply=reply, type="text", suggestions=suggestions)
```

## classify_service() trong intent_parser.py

```python
def classify_service(message: str) -> str:
    """Trả về: flight, fasttrack, esim, visa, passport"""
    msg = message.strip().lower()
    if any(kw in msg for kw in ["fast track", "ưu tiên", "vip"]):
        return "fasttrack"
    if any(kw in msg for kw in ["esim", "sim", "4g", "5g", "internet", "data"]):
        return "esim"
    if any(kw in msg for kw in ["visa", "thị thực"]):
        return "visa"
    if any(kw in msg for kw in ["hộ chiếu", "passport"]):
        return "passport"
    return "flight"  # default
```

## Các service hiện có

| Service | File | Item keys | Notes |
|---------|------|-----------|-------|
| ✈️ Flight | chat.py + intent_parser | IATA airport codes | Full confirm flow + AGT/mock |
| ⚡ Fast Track | smart_fasttrack.py | noi_bai, tan_son_nhat, da_nang, international | 4 airport tiers, 24/7 at Nội Bài |
| 📶 eSIM | smart_esim.py | Châu Á, Châu Âu, Châu Mỹ, Toàn cầu, Việt Nam | 5 plan tiers, auto detect region |
| 🛂 Visa | smart_visa.py | 8 countries | Details + processing time + fee |
| 📄 Passport | smart_passport.py | (single page) | First issue + express + notes |

## Deploy note

- Service modules deploy cùng backend — `app/services/smart_*.py` chỉ cần tar + scp
- Static HTML copy riêng qua sudo (file do root sở hữu trên VPS)
- CORS mở `"*"` cho production, frontend gọi qua nginx proxy
