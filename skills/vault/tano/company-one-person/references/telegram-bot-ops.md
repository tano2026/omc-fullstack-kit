# Telegram Bot Operations — Token Rotation, Verification, Restart

## Overview

Telegram bot `@Tano_CEO_bot` chạy long-polling qua `main.py`. Thỉnh thoảng token hết hạn hoặc bị revoke → cần rotate + restart.

## Token rotation flow

```
1. User revokes old token on @BotFather
2. @BotFather returns new token (e.g. YOUR_TELEGRAM_BOT_TOKEN...)
3. Update .env → patch TELEGRAM_BOT_TOKEN in agent-core/.env
4. Verify new token works: tg("getMe") → ok=True
5. KILL old bot process (if running with old token) — it won't answer messages
6. START new bot with new token via env vars in background
```

**IMPORTANT SEQUENCE:** new token + new process first; only kill old AFTER new is verified. This avoids zero coverage where both instances are dead.

## Verification commands

```python
import os, urllib.request, urllib.parse, json
TOKEN="8963...nAPI = f"https://api.telegram.org/bot{TOKEN}"

# Test token validity
data = urllib.parse.urlencode({}).encode()
r = urllib.request.urlopen(f"{API}/getMe", data=data)
print(json.loads(r.read()).get("ok"))  # True = valid token
```

Also check pending updates:
```python
data = urllib.parse.urlencode({"offset": 0}).encode()
r = urllib.request.urlopen(f"{API}/getUpdates", data=data)
updates = json.loads(r.read()).get("result", [])
print(f"Pending updates: {len(updates)}")
```

## Starting the bot (correct method)

```python
# In Hermes context via terminal(background=true):
cmd = 'cd "D:/MMO Du an/TANO-AGENCY/PLATFORM/agent-core" && TELEGRAM_BOT_TOKEN="8963...nCHAT_ID="762010475" python main.py'

terminal(background=true, command=cmd)
```

Bot reads env via `os.environ.get("TELEGRAM_BOT_TOKEN")`. Truyền qua env là an toàn — ko leak token vào filesystem hay commandline visible.

**DO NOT** write `run_bot.py` with token hardcoded — token leaks into filesystem.

## Killing old bot process

On git-bash (MSYS), standard `taskkill` fails because MSYS interprets `/PID` as git path:

```
# FAILS on git-bash:
taskkill /F /PID 2380
# ERROR: Invalid argument/option - 'C:/Program Files/Git/PID'
```

**Working fixes:**

```python
# Option A (Python — Hermes sandbox safe):
import subprocess
subprocess.run(['taskkill', '/F', '/PID', '2380'], shell=True)

# Option B (PowerShell from git-bash):
powershell "Stop-Process -Id 2380 -Force"

# Option C (cmd escape from git-bash):
cmd.exe //c "taskkill /F /PID 2380"

# Option D (kill by PID if no other process matters):
# Just start new bot and let old one idle. Only 1 poller actually responds.
```

## main.py architecture

- **Long-polling**: `tg("getUpdates", offset=offset, timeout=30)` — 30s timeout per poll
- **Single-chat whitelist**: `CHAT_WHITELIST` from env — only processes messages from `TELEGRAM_CHAT_ID`
- **Natural language**: non-`/` messages → `cmd_natural()` → CEO analyze → dispatch
- **Commands**: `/agents`, `/board`, `/status`, `/run`, `/learn`, `/<agent> <task> <topic>`
- **Budget (CRITICAL — #1 performance lever)**: `PER_COMMAND_BUDGET = dict(max_iterations=1, max_llm_tokens=2000, max_seconds=15)`

---

⚠️ **Budget tuning history (Jul 2026):** Original budget was `max_iterations=2, max_llm_tokens=12000, max_seconds=180` → caused **240s** latency per user message. User complained "nó cứ đơ đơ, phản hồi rõ chậm". After reducing to `max_iterations=1, max_llm_tokens=2000, max_seconds=15` → **12s** per message. Single iteration is sufficient for chat queries; Harness loop with multiple iterations kills responsiveness.

Additionally, `cmd_natural()` now wraps `Harness.run()` in try/except so a timeout doesn't crash the polling loop.

If still too slow (options not applied yet):
1. Send "Đang xử lý..." ack immediately, then run Harness async
2. Cache simple replies (hello/thanks/bye — bypass Harness entirely)
3. Bypass Harness for pattern-matched simple intents

---

## How main.py reads env

```python
BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "")  # Read from env each startup
API = f"https://api.telegram.org/bot{BOT_TOKEN}"
CHAT_WHITELIST = os.environ.get("TELEGRAM_CHAT_ID", "").strip()  # Empty = respond to all
```

Does NOT re-read dotenv — env must be set before launching Python.

## Relationship with cron delivery

The Telegram delivery cron (`cron_telegram.py`, "TANO-AGENCY Telegram Delivery" every 15m) reads `.env` from `agent-core/` directly on each tick — as a `no_agent=True` script it has no Hermes tool context.

**Critical discovery (Jul 2026):** Even with correct token, if `TELEGRAM_CHAT_ID` is empty in `.env`, delivery cron silently skips sending. User had `TELEGRAM_CHAT_ID=` → cron ran but nothing arrived. Fix: set `TELEGRAM_CHAT_ID=762010475`.

| Component | Reads .env at | Restart needed on token change? |
|-----------|--------------|--------------------------------|
| `main.py` (polling bot) | Startup | **Yes** — `os.environ` loaded once |
| `cron_telegram.py` (delivery) | Each tick | **No** — reads `.env` file fresh |
| Cron scripts (morning/afternoon) | N/A | No — they write `~/.hermes/outbox/` files, don't call API |

| Problem | Symptom | Fix |
|---------|---------|-----|
| Token revoked | `tg("getMe")` returns 401 | Revoke @BotFather → update .env → restart |
| Token updated but old process still runs | Bot doesn't reply | Kill old PID or just start new instance |
| CHAT_ID empty | Bot replies to EVERYONE | Set `TELEGRAM_CHAT_ID` in env |
| Multiple polling instances | Updates race — some messages dropped | Ensure only 1 `main.py` active |
| `.env` updated but main.py doesn't see it | Still uses old token | main.py reads `os.environ` at startup, not dotenv. Restart required |
| `taskkill /PID` fails on git-bash | `C:/Program Files/Git/PID` | Use `cmd.exe //c` prefix or `subprocess.run(['taskkill'...])` |
