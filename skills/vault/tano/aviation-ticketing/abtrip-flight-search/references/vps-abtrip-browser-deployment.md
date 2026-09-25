# VPS abtrip_browser.py Deployment

## Paths

| Environment | Path |
|-------------|------|
| **VPS** (43.156.72.127) | `/opt/hermes/ticketing-agent/backend/abtrip_browser.py` |
| **Local** (Windows) | `D:\AI Store\Hermes Agent\abtrip_browser.py` |

## Deployment Flow

All patches are written on local Windows, then SCP'd to VPS:

```bash
# Write patch script locally
# Write a script like patch_abtrip2.py that reads the file on VPS, modifies it, writes back

# SCP to VPS
scp -i ~/.ssh/hermes_key_vps.pem "C:\Users\Nguyen Ngoc Tan\patch_abtrip2.py" ubuntu@43.156.72.127:/tmp/patch_abtrip2.py

# Run on VPS
ssh -i ~/.ssh/hermes_key_vps.pem ubuntu@43.156.72.127 "cd /opt/hermes/ticketing-agent/backend && python3 /tmp/patch_abtrip2.py"
```

## Key Files on VPS

- `/opt/hermes/ticketing-agent/backend/ai_agent.py` — AI agent (includes system prompt + tools)
- `/opt/hermes/ticketing-agent/backend/abtrip_browser.py` — Playwright browser automation (search + book)
- `/opt/hermes/ticketing-agent/.hermes-knowledge.md` — Aviation knowledge base (11 sections)
- `/opt/hermes/ticketing-agent/backend/main.py` — FastAPI app entry point

## Backup Files (ai_agent.py)

| Backup | Status |
|--------|--------|
| `.bak` | Original (41426 bytes, 783 lines) |
| `.bak_patched` | After v22 patch (required + knowledge tools + else + system prompt) |
| `.bak2` | After subsequent patch flex attempt |
| `.bak3` | Latest pre-patch |

## Patch Script History (this session)

| Script | Status | Description |
|--------|--------|-------------|
| patch_v1 → v19 | ❌ Failed | Multiple attempts to patch ai_agent.py with knowledge tools |
| patch_v20 | ❌ Failed | Missing newline in flex handler |
| patch_v21 | ❌ Failed | Indentation error |
| patch_v22 | ✅ Passed | MINIMAL: required fields + 4 knowledge tools + else fallback + system prompt |
| patch_prompt.py | ❌ Failed | File had syntax error from subsequent flex patch |
| patch_prompt2.py | ✅ Passed | System prompt: auto DOB+email, ask gender+phone |
| patch_playwright.py | ✅ Passed | Fixed `_try_flight_select` JS escape issue |
| patch_select.py | ✅ Passed | Replaced `_try_flight_select` with 3-method approach |
| patch_bookflow.py | ❌ Failed | Indentation error after book_flight |
| patch_abtrip.py | ❌ Failed | Python script had f-string collision |
| patch_abtrip2.py | ✅ Passed | Clean rewrite of book_flight |

## Restart Flow

```bash
# Kill old uvicorn (if any)
pkill -f "uvicorn backend.main" 2>/dev/null

# Start new
cd /opt/hermes/ticketing-agent
nohup venv/bin/uvicorn backend.main:app --host 0.0.0.0 --port 8080 > hotline.log 2>&1 &

# Verify
sleep 3
curl -s -o /dev/null -w '%{http_code}' http://127.0.0.1:8080/
# Should return 200
```

## SSH Config

```bash
ssh -i ~/.ssh/hermes_key_vps.pem ubuntu@43.156.72.127
```

Add `-o ServerAliveInterval=2 -o ServerAliveCountMax=10` for unreliable connections (MaxStartups issue).
