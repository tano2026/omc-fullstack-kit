# CEO Telegram Outbox Flow

## Problem

`_ceo_telegram_report()` cần gửi báo cáo qua Telegram, nhưng `hermes_tools.send_message()` chỉ có sẵn khi chạy trong Hermes context (dashboard chat, cron LLM job). Khi chạy ngoài Hermes (Python script thuần, no_agent=True cron), import `hermes_tools` bị ImportError.

## Solution: 3-layer fallback

```python
def _ceo_telegram_report(spec, task, sources, adapters, memory):
    msg = " Bao cao CEO\n\n" + task.topic

    # Layer 1: Hermes send_message
    try:
        from hermes_tools import send_message
        result = send_message(target="telegram", message=msg)
        if isinstance(result, dict) and result.get("ok"):
            return "Da gui bao cao Telegram thanh cong"
        return "Da gui bao cao"
    except ImportError:
        pass

    # Layer 2: outbox file (Hermes cron Telegram Delivery doc)
    try:
        import json
        from pathlib import Path
        op = Path.home() / ".hermes" / "outbox"
        op.mkdir(parents=True, exist_ok=True)
        fout = op / "ceo_report.json"
        with open(fout, "a", encoding="utf-8") as f:
            f.write(json.dumps({
                "target": "telegram",
                "message": msg,
                "from": "ceo",
                "ts": str(__import__("time").time())
            }, ensure_ascii=False) + "\n")
        return "Da ghi vao outbox de Hermes gui Telegram"
    except Exception as e:
        return "Ko the gui Telegram\n\nNoi dung:\n" + msg[:500] + "\n\nLoi: " + str(e)[:100]
```

## Outbox file format

Mỗi dòng là 1 JSON object. Cron Telegram Delivery doc tung dong, parse, gui.

```json
{"target": "telegram", "message": "...", "from": "ceo", "ts": "1784378246.274886"}
```

## Cron flow

```
cron_morning.py (8h) ──┬──> outbox/ ──> cron_telegram.py (every 15m) ──> Telegram API
cron_afternoon.py (17h) ┘
```

## File

- `agents/ceo/adapters.py` — `_ceo_telegram_report()` function (≈40 lines)
- Cron Telegram delivery: `~/.hermes/scripts/cron_telegram.py` — reads outbox, sends pending, marks delivered

## Note

`_ceo_initiative()` không tự gọi `telegram_report` — chỉ trả về text cho dashboard chat.
