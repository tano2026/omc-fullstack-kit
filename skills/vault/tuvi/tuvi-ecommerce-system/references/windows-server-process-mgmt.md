# Windows Server Process Management — Python FastAPI on Port 8139

## Problem

Python servers started via Hermes `terminal(background=True)` die when the calling shell exits. You can't rely on the background process staying alive across turns. PID tracking is unreliable because Hermes doesn't persist process metadata.

## Kill Pattern

```bash
# Step 1: Find what's holding the port
netstat -ano | grep 8139 | grep LISTEN
# Output: TCP 0.0.0.0:8139 0.0.0.0:0 LISTENING 26552
#                                                                 ^^^^^ = PID

# Step 2: Kill it (two methods)
# Method A — taskkill (reliable on Windows)
taskkill //F //PID 26552

# Method B — bash kill via MSYS
kill -9 26552 2>/dev/null

# Step 3: Verify port is free
netstat -ano | grep 8139 | grep LISTEN || echo "Port is free"
```

## Restart Pattern

### Python script approach (preferred — avoids shell escaping issues):
```python
# restart_server.py
import subprocess, sys, os, time

cmd = [sys.executable, "backend/main.py"]
proc = subprocess.Popen(cmd, cwd=os.path.dirname(__file__),
    stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)

time.sleep(3)
if proc.poll() is None:
    print(f"✅ Server started PID={proc.pid} port 8139")
else:
    out = proc.stdout.read()
    print(f"❌ Server failed:\n{out}")
```

## Common Pitfalls

1. **PID 0 in netstat output** — port is closed/not listening, no kill needed
2. **"Access denied" on taskkill** — run shell as admin, or use `-9` SIGKILL
3. **Server exits immediately after start** — check `sys.path` and import errors in stderr
4. **Port shown as LISTENING but server unreachable** — could be a zombie process, kill and restart
5. **Double import of `os`/`sys`** — common after patching main.py, causes NameError on restart
