# Telegram Polling Bot Debugging (Windows)

> Reference: class-level troubleshooting for standalone Telegram polling bots on Windows.
> Covers the 4 most common silent failures: 401 auth, 409 conflict, cp1252 emoji crash, 35s timeout drop.

## The 4 Silent Killers

### 1. 401 Unauthorized — Invalid/Expired Token

**Symptom:** Bot starts, runs briefly, then vanishes. Error only visible with `PYTHONUNBUFFERED=1`:
```
telegram.error.Unauthorized: 401
```

**Root cause:** Telegram bot token is invalid or expired — common when:
- User created a NEW bot but copied the OLD token
- Token was regenerated via @BotFather
- Token contains a typo or truncation

**Fix:**
```python
import urllib.request, json
TOKEN = "your_token_here"
resp = urllib.request.urlopen(f"https://api.telegram.org/bot{TOKEN}/getMe", timeout=10)
print(json.loads(resp.read()))  # {"ok": true, "result": {"id": ..., "username": "..."}}
```
Run this test. If `ok != true`, the token is wrong — revoke and regenerate or use getMe to verify.

### 2. 409 Conflict — Old Process Still Polling

**Symptom:** `getUpdates` returns HTTP 409 after restarting the bot. Bot starts but can't receive messages.

**Root cause:** A stale polling loop (old process) is still connected to Telegram's long-poll, blocking the new one.

**Fix on Windows (git-bash):**
```bash
# List Python processes
ps | grep python

# Kill ALL Python processes (⚠️ kills other Python apps too)
cmd.exe /c "taskkill /F /IM python.exe"

# Or kill by PID (less destructive)
kill <PID>
```

**Fix on Linux:**
```bash
pkill -f main.py
# or
kill <PID>
```

**Prevention:** Always `deleteWebhook` before starting polling:
```python
urllib.request.urlopen(f"https://api.telegram.org/bot{TOKEN}/deleteWebhook")
```

### 3. cp1252 Emoji Crash (Windows-Only)

**Symptom:** Bot starts (brief output), then silently exits. `process(action='poll')` shows process gone. No error visible in normal background mode.

**Root cause:** Windows `sys.stdout.encoding='cp1252'` cannot encode emoji (U+1Fxxx). `print("🧠")` raises `UnicodeEncodeError` silently in background mode.

**Diagnosis:**
```bash
# Run in foreground with unbuffered output
PYTHONUNBUFFERED=1 python main.py
# Will show the actual UnicodeEncodeError
```

**Three fixes (pick one):**

1. **Replace emojis in `print()`** — simplest if few occurrences:
   ```python
   print("[CEO] Bot polling...")  # was print("🧠 Bot polling...")
   ```

2. **Reconfigure stdout at script startup** — global fix:
   ```python
   import sys
   if hasattr(sys.stdout, 'reconfigure'):
       sys.stdout.reconfigure(encoding='utf-8')
   ```

3. **Set env var** (adds 1 line to startup command):
   ```bash
   PYTHONIOENCODING=utf-8 python main.py
   ```

**Rule:** Never put emoji in `print()` calls on Windows. Emoji in Telegram API calls (`sendMessage`, `sendChatAction`) are fine — they go over the wire, not through cp1252.

### 4. 35s Timeout Drop — Silent Message Loss

**Symptom:** Bot is running (no crashes), `getMe` works, but bot never receives messages. User says "bot không trả lời" but there's no error.

**Root cause:** `urllib.request.urlopen(timeout=35)` with Telegram's `getUpdates?timeout=30` parameter. If Telegram holds the long-poll connection open for a full 30s before returning an empty response, and the script's TCP read timeout is exactly 35s, network jitter can cause a `socket.timeout` before the response arrives — dropping the message cycle silently.

**Fix:** Increase the HTTP timeout to 180s (or any value safe >> 30s):
```python
# Was:
with urllib.request.urlopen(req, timeout=35) as resp:
# Fix:
with urllib.request.urlopen(req, timeout=180) as resp:
```

**Note:** Telegram's `timeout=30` long-poll parameter is NORMAL — empty responses are expected. The issue is the HTTP timeout being too tight.

## Complete Startup Checklist

When bringing up a Telegram polling bot on Windows, check in this order:

1. **getMe** — verify token is valid
2. **getWebhookInfo** — ensure no webhook registered (returns 409 if polling)
3. **deleteWebhook** — force polling mode
4. **Run with PYTHONUNBUFFERED=1** first time to catch cp1252/crash errors
5. **Check 35s timeout** in the `urlopen` / `HTTPSConnection` call — set to 180s
6. **Monitor with process(action='poll')** — confirm process stays alive for 30s+

## Bot Startup Verification Script

Use this standalone test to verify a bot token before wiring it into a full application:

```bash
# Replace with actual token
TOKEN="123456:ABC-DEF1234"

# Test getMe
python -c "
import urllib.request, json
r = json.loads(urllib.request.urlopen(f'https://api.telegram.org/bot$TOKEN/getMe', timeout=10).read())
print('OK' if r.get('ok') else 'FAIL:', r)
"

# Test getUpdates (polling mode)
python -c "
import urllib.request, json
r = json.loads(urllib.request.urlopen(f'https://api.telegram.org/bot$TOKEN/getUpdates?offset=0&timeout=5', timeout=10).read())
print('OK' if r.get('ok') else 'FAIL:', r)
"

# Check webhook
python -c "
import urllib.request, json
r = json.loads(urllib.request.urlopen(f'https://api.telegram.org/bot$TOKEN/getWebhookInfo', timeout=10).read())
print(r)
"
```

## Pitfalls Summary

| Issue | Signal | Fix |
|-------|--------|-----|
| 401 Unauthorized | getMe fails | Replace token from @BotFather |
| 409 Conflict | getUpdates fails | kill stale process + deleteWebhook |
| cp1252 crash | Process exits silently on Windows | Remove emoji from print() or set PYTHONIOENCODING=utf-8 |
| 35s timeout | Bot runs but never receives messages | Change urlopen timeout to 180s |
| Emoji in API calls | 🟢 Fine | Only print() on Windows is affected |
