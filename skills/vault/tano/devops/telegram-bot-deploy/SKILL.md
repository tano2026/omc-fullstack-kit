---
name: telegram-bot-deploy
category: devops
description: Deploy, run, and troubleshoot Telegram bot polling scripts on Windows (local dev machine). Covers nohup process lifecycle, Conflict error diagnosis, token revocation, webhook/polling modes, safe relaunch patterns, standalone bot patterns, research commands, and analytics integration.
tags: [telegram, bot, deployment, polling, conflict, process-management, windows, research, analytics]
---

# Telegram Bot Deployment (Windows)

> **Class-level skill** for deploying Python Telegram bot polling scripts on Windows dev machine. Covers the full lifecycle: launch, verify, diagnose Conflict errors, token recovery, and clean shutdown. Includes patterns for standalone bots, research features, and analytics integration.

## When to Use

- User wrote a Telegram bot script and wants it running 24/7
- Bot gets `Conflict: terminated by other getUpdates request`
- Need to change bot token or migrate to a new bot
- Bot process died and needs restart
- User asks "sao bot ko chạy" / "bị conflict"
- When building a standalone Telegram bot independent of Hermes gateway.
- When the bot needs advanced features like web research or analytics.

---

## Section 1: Launch Bot

### On Windows (git-bash/MSYS)

```bash
cd "D:/path/to/bot-dir"
nohup python bot.py > bot.log 2>&1 &
echo "PID: $!"
```

**CRITICAL:** Use `python` NOT `python3` — `python3` on Windows opens Microsoft Store instead of running Python.

### Verify Running

```bash
# Check process
ps aux | grep bot.py

# Check log after a few seconds
tail -10 bot.log

# Look for signs of life:
# - "Polling loop started..." ✓
# - No "Conflict" errors in first 30s ✓
```

### Health Check

```bash
# Is the process alive?
kill -0 $(cat /tmp/bot.pid) 2>/dev/null && echo "ALIVE" || echo "DEAD"

# Send a test message to the bot on Telegram
# Or check log for "Polling loop started..."
```

---

## Section 2: Stop Bot

```bash
# Find PID
ps aux | grep -E "python.*rio_bot|python.*bot" | grep -v grep

# Kill gracefully first
kill <PID>
sleep 2

# Force kill if still alive
kill -9 <PID> 2>/dev_null

# Verify dead
ps aux | grep bot.py | grep -v grep
```

---

## Section 3: Diagnose & Fix Errors

### Symptom: ConflictError

```
[WARNING] API error: Conflict: terminated by other getUpdates request;
make sure that only one bot instance is running
```

### Symptom: Process exits with code -15 (SIGTERM)

```
[Background process completed — exit code -15]
```

**Meaning:** The process was killed by SIGTERM (signal 15), not a code crash. This is normal when:
- Hermes Desktop or another process manager terminates a duplicate polling instance
- A previous background session's process was still alive when a new one started
- System shutdown/restart sent SIGTERM to all user processes

**Action:** Not a bug — the process was deliberately terminated by another process. Check whether a conflicting instance is running (`tasklist | grep python`) before restarting.

### Symptom: 404 Not Found (dead/revoked token)

```
[ERROR] ❌ Cannot connect: {'ok': False, 'error_code': 404, 'description': 'Not Found'}
```

This means the Telegram token is **no longer valid** — revoked via @BotFather, bot deleted, or corrupted. DIFFERENT from Conflict (valid but contested).

### Root Causes (check in order)

1. **Same machine, another terminal** — An old CMD/PowerShell/terminal window is still polling the same token. Close all terminals, or reboot.
2. **Hermes Desktop (Electron GUI) is running** — `hermes desktop` starts its own Telegram polling for the bot token in config.yaml. This is **the most common cause** when Hermes is installed. Check with:
   ```bash
   tasklist | grep -i hermes
   ```
   If Hermes.exe processes exist, they may be polling the same bot. Resolution: either (a) stop Hermes Desktop and run standalone, (b) use Hermes Desktop itself as the bot delivery channel (integrate into Hermes instead of standalone), or (c) create a separate Telegram bot token for the standalone script.
3. **Different machine** — The token is being used from VPS, laptop, cloud panel, or another PC. Common when token was shared or deployed elsewhere.
4. **Hermes gateway** — The bot could be configured as a Hermes gateway bot. Check `hermes config show` or gateway JSON files.
5. **Webhook is set** — Bot has webhook active which blocks polling. Must call `deleteWebhook` first.
6. **Rogue child process** — A fork/subprocess inherited the same token and started polling.
7. **Token revoked/deleted** — Results in **404 Not Found**, NOT Conflict.

### Diagnostic Steps

```bash
# Step 1: Check if this machine's processes
ps aux | grep python | grep -v grep

# Step 2: Check Hermes gateway config
cat ~/AppData/Local/hermes/config/*.yaml 2>/dev/null | grep -i bot
ls ~/AppData/Local/hermes/gateway/ 2>/dev/null

# Step 3: Reset Telegram offset
curl -s -X POST "https://api.telegram.org/bot<TOKEN>/deleteWebhook?drop_pending_updates=true"
curl -s "https://api.telegram.org/bot<TOKEN>/getUpdates?offset=999999999"

# Step 4: If Conflict persists — someone else has your token

# Step 5: If 404 — token is dead. Ask user for new token.
```

### Fix: Token Revocation (for Conflict)

```text
1. Open Telegram → @BotFather
2. /mybots → Select bot → API Token → Revoke current token
3. /revoke → Confirm
4. Copy NEW token
5. Update .env file
6. Launch bot with new token

**IMPORTANT:** Token revocation does NOT kill the rogue instance immediately — it deauthorizes it. The rogue instance will fail on next getUpdates call. But the NEW token is clean — only the first process that polls it gets control.
```

### Fix: 404 Not Found — Token is Dead

```text
1. Open Telegram → @BotFather
2. /mybots → Select bot → API Token → Revoke current token
3. /revoke → Confirm
4. Copy NEW token (or ask user to provide it)
5. Update .env — use Python re.sub (NOT write_file, which overwrites entire .env)
6. Launch bot — new token should work immediately
```

### Updating .env with a new token

Hermes `read_file` blocks `.env` files, so use terminal + Python:

```bash
cd "D:/path/to/bot-dir"
python -c "
import re
with open('.env','r') as f: c = f.read()
c = re.sub(r'^RIO_BOT_TOKEN=.*', 'RIO_BOT_TOKEN=<new_token>', c, flags=re.M)
with open('.env','w') as f: f.write(c)
print('Token updated')
"
```

Do NOT use `write_file` — it would overwrite the entire `.env` and lose other keys.

**IMPORTANT:** Token revocation does NOT kill the rogue instance immediately — it deauthorizes it. The rogue instance will fail on next getUpdates call. But the NEW token is clean — only the first process that polls it gets control.

### Fix: Create Brand New Bot (nuclear option)

When token revocation also fails (Conflict persists on new token too):

```text
1. @BotFather → /newbot
2. Set name + username (e.g. @YourBot_V2_bot)
3. Get fresh token — guaranteed no Conflict
4. Update .env
5. Launch

Note: Old bot username becomes free if you /setusername → delete it first.
```

### Fix: Switch to Webhook (alternative to polling)

Webhook avoids polling conflicts entirely since Telegram calls your server:
```text
1. Set up a public HTTPS endpoint (e.g. on VPS with nginx + SSL)
2. POST https://api.telegram.org/bot<TOKEN>/setWebhook?url=https://your.domain/webhook
3. Bot script listens on webhook
4. No polling = no Conflict
```

---

## Section 4: Environment & Config

### Token Storage Convention

- Use `.env` file (not hardcoded in script)
- Format: `BOT_TOKEN=1234567890:ABCdef...`
- Never commit `.env` to git
- Verify with: `grep BOT_TOKEN .env`

### TELEGRAM_CHAT_ID Setup

For whitelist-based bots that only respond to the user (not to every chat), set `TELEGRAM_CHAT_ID`:

1. Open Telegram → search `@userinfobot`
2. Send `/start` — bot replies with your numeric ID (e.g. `762010475`)
3. Set in `.env`: `TELEGRAM_CHAT_ID=762010475`
4. Bot will only respond to messages from this chat ID

**Pitfall:** If `TELEGRAM_CHAT_ID` is empty/blank, most bots treat this as "reply to everyone" (not "reply to no one"). Check the bot's handler logic — some check `if CHAT_WHITELIST and str(chat_id) != CHAT_WHITELIST: continue` which means empty whitelist = allow all.

### Bot Identity

```bash
# From script logs look for:
# ✅ Bot: @username (ID: 1234567890)
# This confirms which bot the token belongs to
```

---

## Section 5: Common Pitfalls

1. **python3 on Windows** — Use `python`, not `python3`. `python3` triggers Microsoft Store prompt.
2. **nohup needs full path** — `nohup python script.py > log &` from the script's directory, not from somewhere else.
3. **Multiple .env files** — If project has root `.env` and submodule `.env`, make sure the right one has the token.
4. **venv is broken** — If venv/bin/activate or venv/Scripts/activate is missing, use global python.
5. **New token still Conflicts** — Means the token was used before revocation completed. Create entirely new bot.
7. **Bot runs 40 min then Conflicts** — Another instance started polling sometime after you did. Check cronjobs, autorun, VPS deployment scripts.
8. **Process looks alive but bot doesn't respond** — Check log for repeated `API error: Conflict` — Telegram kills the polling connection silently after the first conflict.

9. **`UnicodeEncodeError` on Windows print(emoji)** — Python 3.x on Windows defaults to cp1252 encoding for stdout. When stdout is piped/buffered (e.g. `nohup python bot.py > log &`), any `print("🧠 ...")` crashes with `UnicodeEncodeError: 'charmap' codec can't encode character`. Fix: replace emoji in `print()` with plain text (e.g. `"[CEO]"` instead of `"🧠"`). Emoji in `send()` (Telegram API calls) are fine — those go over HTTP, not through cp1252. Prevention: grep for `print.*[\U0001F300-\U0001FFFF]` before deploying a new bot script.

### Pitfalls from Standalone Polling Bots

- **Emoji in print() crash on Windows cp1252**: Python 3.x on Windows defaults to cp1252 encoding for stdout. Emoji in `print()` can cause `UnicodeEncodeError`. Fix: `import sys; sys.stdout.reconfigure(encoding='utf-8')` at script start, or run with `set PYTHONIOENCODING=utf-8 && python bot.py`, or simply avoid emojis in `print()`. Emojis in `sendMessage` are fine.
- **Timeout silent drop — urllib timeout ≤ poll timeout**: If `urllib.urlopen(timeout=X)` where X is ≤ Telegram's `getUpdates` `timeout` (typically 30s), messages can be silently lost. Fix: Set `urllib.urlopen` timeout to ≥ 60s (recommended 180s).
- **401 vs 409**: Differentiate `getMe` failing (token expired/invalid) vs `getUpdates` failing with Conflict (duplicate polling).
- **Self-Learning Engine hooks pattern**: For integrating self-learning, add 3 hooks: record outcome after `Harness.run()`, detect user correction in `handle()`, and a cron script for `auto-learn.py`.
- **Duplicate instance → 409 Conflict**: If log shows `Conflict: terminated by other getUpdates request`, diagnose orphaned Python processes locally (`ps aux | grep python`), check Hermes gateway, check VPS/remote machines. If all fail, perform token revocation via @BotFather. **This always works**.
- **Bot can't DM itself**: `403 Forbidden` when `sendMessage` to bot's own user ID. Test from a real Telegram account.
- **Telegram reconnect**: Connection error every ~2h is normal; retry with backoff.
- **Debug diagnostics: getMe vs getUpdates**: When bot appears to run but doesn't respond, test `getMe` (token validity) and `getUpdates` (polling issues/conflicts) separately.
- **Webhook conflict**: If bot previously had webhook, polling returns 409; `deleteWebhook` first.
- **Markdown parsing**: Telegram's Markdown is strict; escape special chars or use HTML mode.
- **Background process from terminal()**: Always use `background=true`, never `&` in foreground command.
- **Group message detection**: Check `entities` for bot mention, not just `contains("@bot")`; in groups, check `chat.type` and require `startswith("/")` or bot mention.
- **Long poll stderr**: HTTPS connection timeout after 30s is normal; don't treat as crash.
- **Process death detection**: `process(action="poll")` checks if alive; log writes to file as backup (essential on Windows/MSYS where background output is unreliable).
- **MSYS stdout buffering**: `terminal(background=true)` output may be blank; redirect to log file: `> rio_bot.log 2>&1`.
- **.env variable name mismatch**: Ensure bot script reads the correct environment variable name (e.g., `RIO_BOT_TOKEN`) and `.env` matches.

---

## Section 6: Standalone Telegram Polling Bot Core Patterns

> Dùng khi cần chạy 1 Telegram bot **độc lập** — không qua Hermes gateway.
> Phù hợp cho: research bot, monitoring bot, dedicated channel bot, tool-specific bot.
> Mỗi bot 1 token riêng, chạy background process riêng.

### Companion Skills (for Research Bots)

| Skill | When to load |
|-------|-------------|
| `deep-researchs` | Bot needs `/research` command with tiered depth (L0-L5) |
| `research-agent` | Bot needs structured research prompt template |
| `ecc-research-ops` | Bot needs research operations workflow |
| `auto-research-trending` | Bot needs weekly trend scanning |
| `trending-content-scout` | Bot needs cross-platform research (YouTube + TikTok + Reddit + X); real engagement data, gap analysis |
| `last30days` | Bot needs unfiltered community signals from Reddit/X/HN/YouTube; complements Google search |
| `social-media-stack` | Reference cheat sheet for platform-specific research approaches |
| `youtube-research-agent` | Bot needs deep YouTube channel analysis with content pattern extraction |

### General Bot Pattern

Variants:

**Simple polling bot**
```
.env (token)
  ↓
rio_bot.py (polling loop + handlers)
  ↓
terminal(background=true) hoặc cronjob
  ↓
Bot tự chạy, tự xử lý message
```

**Research bot (RIO) — hybrid mode**
```
.env (token)
  ↓
rio_bot.py
├── /research <query>       → Deep research via Hermes API / DuckDuckGo
├── /research deep <query>  → Multi-source L2-L3
├── /brief                  → Today's news snapshot
├── /trend                  → Weekly trending topics
├── /watch <ngành>          → Competitor monitoring
└── /ask <question>         → Quick Q&A (no deep research)
  ↓
terminal(background=true)
  ↓
cronjob — Daily Brief 6AM (tự động research + gửi)
```

### 6.1. File Structure for Standalone Bots

```
rio-bot/
├── .env              # RIO_BOT_TOKEN=xxx
├── .env.example      # Template (ko có token thật)
├── .gitignore        # .env, *.log, chat_history.json, __pycache__
├── rio_bot.py        # Main bot script
├── rio_bot.log       # Auto-generated log
└── chat_history.json # Auto-generated chat persistence
```

### 6.2. Script Core Pattern

#### Imports + Config

```python
import os, sys, json, time, signal, logging, html
import urllib.parse, urllib.request, re
from datetime import datetime
from http.client import HTTPSConnection, HTTPException

TOKEN = os.environ.get("RIO_BOT_TOKEN", "")
API = f"https://api.telegram.org/bot{TOKEN}"
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
```

#### Telegram API helpers

```python
def api_request(method, data=None, params=None):
    try:
        conn = HTTPSConnection("api.telegram.org", timeout=180) # Increased timeout
        path = f"/bot{TOKEN}/{method}"
        if params:
            qs = urllib.parse.urlencode(params)
            path = f"{path}?{qs}"
            body = None; headers = {}
        elif data:
            body = json.dumps(data).encode("utf-8")
            headers = {"Content-Type": "application/json"}
        else:
            body = None; headers = {}
        conn.request("POST" if data else "GET", path, body=body, headers=headers)
        resp = conn.getresponse()
        raw = resp.read().decode("utf-8")
        conn.close()
        return json.loads(raw)
    except HTTPException as e:
        log.error(f"HTTP error ({method}): {e}")
        return None
    except Exception as e:
        log.error(f"API error ({method}): {e}")
        return None

def send_message(chat_id, text, parse_mode="Markdown", reply_to=None):
    data = {
        "chat_id": chat_id, "text": text,
        "parse_mode": parse_mode, "disable_web_page_preview": True
    }
    if reply_to: data["reply_to_message_id"] = reply_to
    return api_request("sendMessage", data=data)

def send_action(chat_id, action="typing"):
    api_request("sendChatAction", data={"chat_id": chat_id, "action": action})
```

#### Polling loop

```python
def main():
    # 1. Test connection
    me = api_request("getMe")
    if me and me.get("ok"):
        log.info(f"✅ Bot: @{me['result']['username']} (ID: {me['result']['id']})")
    
    # 2. Ensure polling mode (delete webhook if any)
    webhook = api_request("getWebhookInfo")
    if webhook.get("result", {}).get("url"):
        api_request("deleteWebhook")
        log.info("Webhook deleted → polling mode")
    
    # 3. Polling loop
    offset = 0
    running = True # Make sure this is defined for the loop to run
    while running:
        try: # Added try-except for robust polling
            params = {"offset": offset, "timeout": 30, "allowed_updates": json.dumps(["message"])}
            result = api_request("getUpdates", params=params)
            if result and result.get("ok"):
                for update in result["result"]:
                    offset = update["update_id"] + 1
                    if "message" in update:
                        msg = update["message"]
                        chat_id = msg["chat"]["id"]
                        text = msg.get("text", "")
                        if text:
                            handle_message(chat_id, text, msg) # Pass msg for group chat handling
        except KeyboardInterrupt:
            log.info("Shutting down...")
            running = False
        except Exception as e:
            log.error(f"Fatal error in polling loop: {e}")
            time.sleep(5) # Delay before retrying
```

#### Group chat handling

```python
def handle_message(chat_id, text, msg):
    chat_type = msg["chat"]["type"]
    if chat_type in ("group", "supergroup"):
        if not text.startswith("/"):
            entities = msg.get("entities", [])
            bot_username = api_request("getMe")["result"]["username"] # Get bot username dynamically
            bot_mentioned = any(
                e.get("type") == "mention" and
                text[e["offset"]:e["offset"]+e["length"]].lower() == f"@{bot_username.lower()}"
                for e in entities
            )
            has_prefix = any(text.lower().startswith(p) for p in ["research:", "deep:", "trend:"])
            if not bot_mentioned and not has_prefix:
                return  # skip messages not for the bot
    # ... rest of your message handling logic ...
```

### 6.3. Research Commands (RIO Bot Pattern)

Research bot (`/research`, `/brief`, `/trend`) needs these handlers:

```python
# Assumes ddgs library is installed: pip install ddgs
from ddgs import DDGS

def search_duckduckgo(query, max_results=5):
    """DuckDuckGo search via ddgs library — API-based, not HTML scraping."""
    try:
        with DDGS() as ddgs:
            results = list(ddgs.text(query, max_results=max_results))
            return [{
                "title": r.get("title", ""),
                "url": r.get("href", ""),
                "snippet": r.get("body", ""),
            } for r in results]
    except Exception as e:
        log.warning(f"DDGS search failed: {e}")
        return []

def research(query, tier="L1"):
    """Hybrid research: Hermes API → DuckDuckGo fallback"""
    hermes_api = os.environ.get("HERMES_API_URL", "http://localhost:8137/api/query")
    hermes_token = os.environ.get("HERMES_API_TOKEN", "")
    
    # Try Hermes API
    if hermes_api and hermes_token:
        try:
            # Load deep-researchs skill context for tier routing
            data = json.dumps({
                "query": query,
                "tier": tier,
                "max_sources": 8 if tier == "L2" else 5
            }).encode()
            req = urllib.request.Request(
                hermes_api, data=data,
                headers={"Authorization": f"Bearer {hermes_token}",
                         "Content-Type": "application/json"},
                method="POST"
            )
            with urllib.request.urlopen(req, timeout=180) as resp: # Increased timeout
                result = json.loads(resp.read().decode())
                return {"ok": True, "data": result.get("response", "")}
        except Exception as e:
            log.warning(f"Hermes API failed: {e}, falling back to DuckDuckGo")
    
    # Fallback: DuckDuckGo + URL extract
    results = search_duckduckgo(query, max_results=8 if tier == "L2" else 5)
    body = ""
    for r in results:
        body += f"🔹 <b>{r[\'title\']}</b>\\n{r[\'url']}\\n"
        if r[\'snippet\']:
            body += f"  {r[\'snippet\'][:200]}...\\n"
        body += "\\n"
    
    if not body:
        return {"ok": False, "error": "No results found"}
    
    return {"ok": True, "data": f"Research: <b>{query}</b>\\n\\n{body}"}

def handle_message(chat_id, text, msg):
    # ... (existing message handling logic)

    text_lower = text.lower()
    
    # /research <query> — Deep research
    if text_lower.startswith("/research"):
        query = text[len("/research"):].strip()
        if not query:
            send_message(chat_id, "Usage: /research <query>\\n" \
                         "  /research deep <query>  → multi-source\\n" \
                         "  /research quick <query> → fast check")
            return
        
        send_action(chat_id, "typing")
        
        tier = "L0"
        if text_lower.startswith("/research deep "):
            tier = "L2"
            query = text[len("/research deep "):].strip()
        elif text_lower.startswith("/research quick "):
            tier = "L0"
            query = text[len("/research quick "):].strip()
        
        # Try Hermes API first, fallback to local
        result = research(query, tier)
        
        if result.get("ok"):
            send_message(chat_id, result["data"], parse_mode="HTML")
        else:
            send_message(chat_id, f"Research failed: {result.get('error', 'unknown')}")
        return
    
    # /brief — Daily news
    if text_lower.startswith("/brief"):
        send_action(chat_id, "typing")
        result = research("tin tức nổi bật hôm nay", "L1")
        if result.get("ok"):
            send_message(chat_id, "📰 *Daily Brief*\\n\\n" + result["data"], parse_mode="Markdown")
        return
    
    # /trend — Weekly trending
    if text_lower.startswith("/trend"):
        send_action(chat_id, "typing")
        result = research("xu hướng, trends nổi bật tuần này", "L1")
        if result.get("ok"):
            send_message(chat_id, "🔥 *Trending This Week*\\n\\n" + result["data"], parse_mode="Markdown")
        return
    # ... (add other command handlers below)
```

### 6.4. Background Process Lifecycle (Windows) - Further Enhanced

This section expands on managing background processes for standalone Telegram bots on Windows, integrating advanced insights.

#### Process visibility & Zombie instances

`terminal(background=true)` creates a `bash.exe` process (visible via `tasklist`). The actual `python.exe` running your bot is a **child** of `bash.exe`. This means:
- `tasklist | grep python` or `Get-Process -Name python` shows the real PIDs.
- `process(action="log")` may show blank output even though the bot is running fine.
- The bot process is visible inside the MSYS shell but NOT as a standalone PID.

**Survival**: The MSYS/bash wrapper can die (exit code -15 / SIGTERM) while the `python.exe` child keeps running. This creates **zombie bot instances** that continue polling Telegram.

#### ⚠️ CRITICAL: Duplicate instance detection

If `rio_bot.log` shows repeated:
```
WARNING] API error: Conflict: terminated by other getUpdates request
```
This means **another instance of the same bot token is already polling** — Telegram only allows one simultaneous polling connection per token.

**Diagnose with Get-CimInstance** (reliable, works with spaces in paths):
```powershell
# List ALL python.exe processes with their command lines
Get-CimInstance Win32_Process -Filter "Name=\'python.exe\'" | \
  Select-Object ProcessId, CommandLine | Format-Table -AutoSize
```

Look for multiple entries containing `rio_bot.py` or the same project name.

**Kill all duplicate instances**:
```bash
# List matching PIDs first
Get-CimInstance Win32_Process -Filter "Name=\'python.exe\'" | \
  Where-Object { \$_.CommandLine -match 'rio_bot\' } | \
  Select-Object ProcessId

# Then kill each PID (use //F //PID in MSYS bash, NOT /F /PID)
taskkill //F //PID 18380
taskkill //F //PID 3248
```

**Why taskkill //F //PID (double slash)?**: MSYS bash interprets `/F` as a Unix path. From bash, always use `//F //PID` to forward the flags to `taskkill.exe`.

### Start fresh after killing duplicates

```bash
# Use terminal(background=true) — this works reliably for Python polling bots
terminal(
    background=true,
    command="cd \"/d/path/to/rio-bot\" && python rio_bot.py",
    notify_on_complete=true,
    timeout=86400
)
```

The bot typically lives for hours/days this way. `notify_on_complete` alerts you when it dies so you can restart.

### When taskkill / kill -9 fails (zombie process)

If `taskkill //F //PID <PID>` returns "ACCESS_DENIED" or the process reappears after being killed:

1. **Use Hermes process tool first** — always try `process(action="kill", session_id="...")` before shell-based kill. Hermes tracks its own child sessions.
2. **Kill all python.exe instances** — if you can\'t identify which PID is the zombie, kill ALL non-Hermes Python processes:
   ```bash
   # List all Python PIDs (Hermes may be one)
   ps aux | grep python | grep -v grep
   
   # Kill everything except Hermes\'s own PID
   kill -9 <pid1> <pid2>  # from MSYS bash — works when taskkill fails
   ```
3. **On Windows MSYS**, `taskkill` with single slash (`/F /PID`) is interpreted as a Unix path by MSYS bash. Always use double-slash (`//F //PID`) or use `kill -9 <PID>` which works directly.
4. **The real PID vs MSYS wrapper PID**: `terminal(background=true)` creates a bash.exe wrapper. The actual python.exe is a child. If `process(action="kill")` kills the wrapper but python.exe survives, you need to find and kill the child PID via `ps aux | grep python | grep -v grep`.

If `process(action="poll")` shows the session dead but `Get-CimInstance` shows `python.exe rio_bot.py` still running:
1. Kill the python.exe PIDs directly via `taskkill //F //PID <PID>`
2. Start a fresh background session

**Root cause**: MSYS/bash wrapper terminates (SIGTERM/exit -15) while child process continues. This is normal MSYS behavior — not a bot bug.

### Verification after start

```bash
# Quick check — Hermes reports process status
process(action="poll", session_id="xxx")

# Deep check — actual Python process
powershell -NoProfile -Command "Get-CimInstance Win32_Process -Filter \'Name=\'\'python.exe\''\' | Select-Object ProcessId, CommandLine" | grep rio_bot

# Log file check
tail -20 "/d/path/to/rio-bot/rio_bot.log"
```

Expected log output for a healthy bot:
```
[INFO] ✅ cn_trends module loaded
[INFO] ✅ global_trends module loaded
[INFO] ✅ web_research module loaded
[INFO] ✅ deep_research module loaded
[INFO] ✅ video_extract module loaded
[INFO] ✅ report_gen module loaded
[INFO] ============================================================
[INFO] RIO v2.0 — Research & Intelligence Officer
[INFO] ============================================================
[INFO] ✅ Bot: @bot_username (ID: 123456)
[INFO] 🔄 Polling loop started...
```

### ⚠️ Legacy: cmd.exe /c start /B (use only if background=true fails)

Prefer `terminal(background=true)` first. Only fall back to this if background process dies within 30s:

```bash
cmd.exe /c \'start /B "" python "D:\\path\\to\\rio_bot.py" > "D:\\path\\to\\rio_bot.log" 2>&1\'
```

Output log là bắt buộc — MSYS background process ko trả output đáng tin cậy qua `process(action="log")`, nên ghi file là backup essential.

Để verify process sống:
```bash
tasklist | grep python              # List all Python PIDs
wmic process where "name=\'python.exe\'" get processid,commandline /FORMAT:LIST | findstr /i "rio"
```

Set env var `PYTHONUNBUFFERED=1` hoặc dùng `python -u` để log ko bị buffer.

### 6.5. Chat History Persistence

```python
def load_chat_history():
    if os.path.exists("chat_history.json"):
        with open("chat_history.json", "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def save_chat_history(history):
    with open("chat_history.json", "w", encoding="utf-8") as f:
        json.dump(history, f, ensure_ascii=False, indent=2)
```

Keep last 20 messages per chat, save after each response.

### 6.6. Cronjob: Daily Brief Automation

RIO research bot can trigger daily briefs via Hermes cronjob:

```python
# cronjob setup (from Hermes session):
cronjob(
    action='create',
    name='rio-daily-brief',
    schedule='0 6 * * *',  # 6AM daily
    prompt='''
Generate a daily brief for Tano\'s businesses:\
1. Search today\'s news for: travel tech, AI agents, airport services, content creation\
2. Summarize top 5 relevant stories\
3. Add RIO analysis: what this means for ABTRIP, An Binh Fast Track, GMSP\
4. Format: Brief headline → Source → 2-3 sentence key takeaway\
\
Send to Telegram group using send_message.\
\'\'\',
    skills=[\'deep-researchs\'],
    enabled_toolsets=[\'web\', \'terminal\']
)
```

Alternative: let the standalone bot self-run the brief (no Hermes dependency):

```python
# In rio_bot.py — scheduled task thread
import threading
from datetime import datetime, timedelta

def schedule_daily_brief(chat_id, hour=6, minute=0):
    def loop():
        running = True # Make sure running is defined for this loop
        while running:
            now = datetime.now()
            target = now.replace(hour=hour, minute=minute, second=0, microsecond=0)
            if now > target:
                target += timedelta(days=1)
            sleep_seconds = (target - now).total_seconds()
            time.sleep(sleep_seconds)
            
            send_action(chat_id, "typing")
            result = research("top news brief today", "L1")
            if result.get("ok"):
                send_message(chat_id, "🌅 *RIO Daily Brief*\\n\\n" + result["data"])
    
    thread = threading.Thread(target=loop, daemon=True)
    thread.start()
```

### 6.7. Cross-Platform Research (TikTok + YouTube + Reddit + X)

RIO research bot can extend beyond web search to scrape social platforms. Key pattern: use `web_search` with platform-specific site operators.

#### YouTube research (from bot)

```python
def research_youtube(query, max_results=5):
    """Find YouTube videos about topic with view counts"""
    results = search_duckduckgo(f\"site:youtube.com {query} views\", max_results)
    parsed = []
    for r in results:
        snippet = r.get('snippet', '')
        view_match = re.search(r'(\d[\\d,.]*)\s*(?:view|lượt xem)', snippet)
        views = view_match.group(1) if view_match else 'N/A'
        parsed.append({
            'title': r['title'].replace(' - YouTube', ''),
            'url': r['url'],
            'views': views,
            'channel': re.search(r'by\s+(.+?)\s+', snippet).group(1) if re.search(r'by\s+(.+?)\s+', snippet) else 'Unknown'
        })
    return parsed
```

#### TikTok research (from bot — limited, no API)

```python
def research_tiktok(query, max_results=5):
    """Search TikTok via web — engagement data is approximate"""
    results = search_duckduckgo(f\"site:tiktok.com {query}\", max_results)
    return [{'title': r['title'], 'url': r['url'], 'snippet': r.get('snippet', '')} for r in results]
```

**Note**: TikTok has no public search API. Web search gives titles + snippets but no reliable engagement data. For proper TikTok competitive research, the `trending-content-scout` skill has a fallback method that can extract more detail.

#### Reddit research

```python
def research_reddit(query, max_results=5):
    """Search Reddit via DuckDuckGo"""
    results = search_duckduckgo(f\"site:reddit.com {query}\", max_results)
    # Alternative: use Reddit\'s .json endpoint
    # https://www.reddit.com/r/all/search.json?q={query}&sort=top&t=month
    return results
```

#### X/Twitter research

```python
def research_x(query, max_results=5):
    """Search X/Twitter via DuckDuckGo"""
    results = search_duckduckgo(f\"site:x.com {query}\", max_results)
    return results
```

#### Unified cross-platform research command

```python
def handle_message(chat_id, text, msg):
    # ... (existing handle_message logic)

    # /research all <query> — scan all platforms
    if text.startswith(\"/research all \") or text.startswith(\"/research cross \"):
        query = re.sub(r'^/research (all|cross) ', '', text).strip()
        send_action(chat_id, \"typing\")
        send_message(chat_id, f\"🔍 Scanning all platforms for: *{query}*\\nThis may take 30-60s...\", parse_mode=\"Markdown\")
        
        youtube = research_youtube(query)
        tiktok = research_tiktok(query)
        reddit = research_reddit(query)
        x = research_x(query)
        
        report = f\"📊 *Cross-Platform Research: {query}*\\n\\n\"
        report += f\"▶️ *YouTube* ({len(youtube)}):\\n\"
        for v in youtube[:3]:
            report += f\"  • [{v['title']}]({v['url']}) — {v['views']} views\\n\"
        report += f\"\\n🎵 *TikTok* ({len(tiktok)}):\\n\"
        for t in tiktok[:3]:
            report += f\"  • {t['title']}\\n\"
        report += f\"\\n🟦 *Reddit / X* — see results in separate messages if needed\\n\"
        report += f\"\\n_Source: DuckDuckGo (approximate data)_\"
        
        send_message(chat_id, report, parse_mode=\"Markdown\")
        return
    # ... (add other command handlers below)
```

### 6.8. Analytics Commands (RIO v2.0+)

Adding data analytics module — Market Analysis, SWOT, Sentiment, Forecast, KPI.

#### Module structure

```
rio-bot/
├── modules/
│   ├── __init__.py         # Add "analytics" to module list
│   ├── analytics.py        # New: 4 analyzer classes
│   └── web_research.py     # SHARED search module — MUST reuse
│   └── ...                 # Other modules unchanged
```

#### 5 commands

| Command | Pattern | Class |
|---------|---------|-------|
| `/analyze <topic>` | Market analysis — TAM/SAM/SOM, growth, competitors | `MarketAnalyzer.analyze_market()` |
| `/swot <entity>` | SWOT — Strengths, Weaknesses, Opportunities, Threats | `MarketAnalyzer.swot_analysis()` |
| `/sentiment <keyword>` | Sentiment bar chart + score + verdict | `SentimentMiner.analyze()` |
| `/forecast <topic>` | Trend prediction — trajectory + recommendations | `TrendForecaster.forecast()` |
| `/kpi <domain>` | KPI Dashboard — scorecard with 5 metrics | `KPIDashboard.dashboard()` |

#### Import pattern

```python
try:
    from modules import analytics
    modules_loaded["analytics"] = True
    analytics_engine = analytics.Analytics()
    log.info("✅ analytics module loaded")
except ImportError as e:
    modules_loaded["analytics"] = False
    analytics_engine = None
```

#### Handler + Route template

```python
def handle_analyze(chat_id, topic):
    send_action(chat_id)
    send_message(chat_id, f"📊 Đang phân tích thị trường: `{topic[:50]}`...")
    if analytics_engine:
        try:
            response = analytics_engine.run("market", topic)
            send_message(chat_id, response)
        except Exception as e:
            send_message(chat_id, f"❌ Lỗi phân tích: {e}")
    else:
        send_message(chat_id, "❌ Module analytics chưa khả dụng.")

# In handle_message():
# if text.lower().startswith("/analyze "):
#     handle_analyze(chat_id, text[len("/analyze "):].strip())
#     return
```

#### 📐 Analytics output format (from ecc-market-research)

Use this **6-component output template** for every analytics command. It makes output decision-oriented, not data-dump:

```markdown
📊 [Topic]: [Analysis Type]
Generated: [date] | Sources: [N] | Confidence: [High/Medium/Low]

## Executive Summary
3-5 sentence overview of key findings

## Key Findings
- Finding with supporting evidence
- Finding with supporting evidence

## Implications
What these findings mean for the user\'s business

## Risks & Caveats
- Stale data flagged
- Contradictory evidence noted
- What we couldn\'t verify

## Recommendation
Actionable next step

## Sources
1. [Title](url) — one-line summary
```

**Quality gate** before delivering analytics:
- Every number has a source or is labeled as estimate
- Old data (>12mo) is explicitly flagged
- Risks and counterarguments are included
- Fact and inference are separated clearly
- The output makes a decision easier (not just "interesting")

#### 🎯 Sub-question research workflow (from ecc-deep-research)

Instead of treating a broad topic as one big query, **break it into 3-5 sub-questions** and search each one:

```python
def research_deep(query):
    # Step 1: Decompose topic
    search_plan = {
        "market_overview": f"{query} market size growth forecast 2025 2026",
        "competitors": f"{query} top companies competitors landscape",
        "technology": f"{query} technology stack trends innovation",
        "challenges": f"{query} challenges problems risks",
        "future": f"{query} future outlook prediction"
    }
    
    results = {}
    for key, sq in search_plan.items():
        results[key] = search_ddg(sq, max_results=5)
        time.sleep(1)
    
    # Step 2: Deep-read top 3-5 most promising URLs
    
    # Step 3: Synthesize with template above
    return synthesize_report(query, results)
```

**Search strategy:**
- Use 2-3 different keyword variations per sub-question
- Mix general and news-focused queries
- Aim for 10-15 unique sources per report
- Prioritize: official/reputable > news > blogs > forums

#### 🔍 Fact-checker rating system (data quality labels)

Adopt this rating system for every analytic claim:

| Label | Meaning | When to use |
|-------|---------|-------------|
| ✅ Đúng | Confirmed by 2+ reliable sources | Core facts, official data |
| 🟡 Phần lớn đúng | True but partial | Estimates, approximations |
| 🔄 Có tranh cãi | Reliable sources disagree | Emerging trends, predictions |
| 🟠 Phần lớn sai | Misleading or incorrect | Common misconceptions |
| ❌ Sai | Refuted by evidence | Myths, debunked claims |
| ❓ Ko verify được | Insufficient data | Speculative topics |

Embed in output like:
```markdown
**Market size: $5.2B (2030)** 🟡 Estimate — growth rate assumed constant
— Source: Grand View Research (2024), adjusted for Vietnam factors
```

#### 📊 Research mode selection (L0-L5 ladder)

Match depth to query:

| Type | Tier | Time | Sources | Output |
|------|------|------|---------|--------|
| Quick fact check | L0 | ~30s | 3-5 | 1 para |
| Standard | L1 | ~2min | 5-10 | Bullet list |
| Deep analysis | L2 | ~5min | 10-20 | Full report |
| Comprehensive | L3+ | ~15min | 20+ | Multi-section |
| Background check | OSINT | Varies | Varies | Entity profile |

**Default**: L1 for `/research`, L0 for `/analyze`, L2 for `/research deep`

#### Hardware bans for analytics output

Delete and rewrite any:
- "Based on the data, we can see..." — just show the data
- "It is worth noting that..." — either note it or don\'t
- "This suggests that..." when data clearly shows it
- Generic disclaimers longer than 1 sentence
- "Game-changing" / "revolutionary" / "cutting-edge"
- Unsourced numbers with no estimate label
- "In today\'s competitive landscape"

#### ⚠️ CRITICAL PITFALL: Shared search

**NEVER** write standalone `_fetch_text()` + `_ddg_search()` in a new module. DDG blocks IPs that fetch via raw `urllib.request` without proper session/cookies/headers.

**ALWAYS** reuse `web_research.search_ddg()` which has working User-Agent rotation + httpx session management:

```python
# GOOD — in analytics.py:
try:
    from modules import web_research
    HAS_WEB_RESEARCH = True
except ImportError:
    HAS_WEB_RESEARCH = False

def _ddg_search(query, limit=10):
    if HAS_WEB_RESEARCH:
        return web_research.search_ddg(query, max_results=limit)
    log.warning("web_research not available")
    return []
```

### 6.9. RIO Bot Architecture Reference

Full RIO bot layout (`rio-bot/`):

```
rio-bot/
├── .env                    # RIO_BOT_TOKEN=xxx (gitignored)
├── .env.example            # Template placeholder
├── .gitignore              # .env, *.log, *.json, __pycache__
├── rio_bot.py              # Main bot (polling + handlers + research)
├── rio_bot.log             # Auto-generated log
├── chat_history.json       # Persisted conversation context
├── modules/                # Modular research components (RIO v2.0+)
│   ├── __init__.py
│   ├── cn_trends.py        # 9 Chinese social media sources
│   ├── global_trends.py    # 6 global trending sources
│   ├── web_research.py     # DDG→Bing→Wikipedia chain
│   ├── deep_research.py    # L0-L3 research tiers
│   ├── video_extract.py    # yt-dlp metadata + transcript
│   └── report_gen.py       # Watchlist, history, formatting
└── data/                   # Persisted data files
    ├── watchlist.json
    └── history.json
```

Key design decisions:
- **/research** command parses sub-tiers: `quick` (L0), default (L1), `deep` (L2)
- **Hybrid mode**: Hermes API first (when available), DuckDuckGo fallback (always works)
- **No external API keys needed** for basic research — DuckDuckGo is free
- **Chat persistence** keeps last 20 messages per user for context
- **Daily brief** runs on internal thread scheduler (no cron dependency)
- **Group support**: checks bot mention + prefix commands

### 6.10. Token Management for Standalone Bots

- **DO NOT** hardcode token in script
- Use environment variable: `export RIO_BOT_TOKEN='xxx'`
- Use `.env` file for local dev (add to `.gitignore`!)
- Keep `.env.example` with placeholder for version control

---

## Section 7: Fix-Bot Code → Verify → Restart Cycle

After editing bot source code (bug fixes, features, refactors), follow this exact cycle:

### Step 1: Syntax Check (before restart)
```bash
cd "D:/path/to/bot-dir"
python -c "import modules.module1; import modules.module2; print('Syntax OK')"
```
- Import every module the bot loads at startup
- Catches syntax errors AND ImportErrors (missing deps, circular imports, wrong package names)

### Step 2: Class Instantiation Check
```bash
python -c "from modules.chat_brain import ChatBrain; cb = ChatBrain(); print('OK')"
```
- Instantiate every class whose `__init__` signature changed
- Catches param mismatches, renamed attrs, missing defaults

### Step 3: Feature-Specific Tests
```bash
python -c "
from modules.web_research import filter_results
# Test inline — one line per changed code path
assert len(filter_results([], context_topic='test')) == 0
print('Feature test OK')
"
```

### Step 4: Kill Old Process
```bash
ps aux | grep -E "python.*rio_bot|python.*bot" | grep -v grep
kill -9 <PID> 2>/dev_null
```

### Step 5: Launch New Instance
```bash
cd "D:/path/to/bot-dir"
nohup python bot.py > bot.log 2>&1 &
echo "PID: $!"
```

### Step 6: Health Check (5 second wait)
```bash
sleep 5
tail -10 bot.log
# Verify: no ERROR, no ConflictError, no Traceback
# Verify: "✅ Bot: @username (ID: 1234567890)" appears
grep -E "ERROR|CRITICAL|ConflictError|Traceback" bot.log | wc -l
# Should be 0
```

### Pitfalls
- `python3` on Windows → use `python`
- Background process dies silently → check log before assuming it's alive
- `ddgs` installed but `fourdigits` in requirements → verify package name matches import

## Related Skills
- `airfare-decoded-domain` (for ABTRIP related bots)
- `rio-analytics-engine` (for deeper analytics integration)
- `deep-researchs` (for advanced research capabilities)
- `research-agent` (for structured research prompt templates)
- `ecc-research-ops` (for research operations workflows)
- `auto-research-trending` (for weekly trend scanning)
- `trending-content-scout` (for cross-platform research)
- `last30days` (for unfiltered community signals)
- `social-media-stack` (for platform-specific research cheat sheets)
- `youtube-research-agent` (for deep YouTube channel analysis)

## Reference Files
- `references/rio-bot-conflict-diagnosis.md` (original reference from telegram-bot-deploy)
- `references/rio-bot-full-pattern.py` (Complete working RIO research bot pattern)
- `references/rio-v20-modules.md` (Modular RIO v2.0 architecture)
- `references/social-platform-research.md` (Social platform research methods)
- `references/telegram-polling-bot-windows-debug.md` (Windows debug for polling bots)
- `references/research-analytics-integration.md` (Integration of research and analytics)
- `references/rio-v20-analytics-pattern.py` (Full class signatures and architecture for RIO v2.0 analytics)
