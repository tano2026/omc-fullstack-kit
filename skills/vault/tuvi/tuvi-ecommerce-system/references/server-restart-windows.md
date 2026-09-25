# Server Management on Windows

> Created: 20/07/2026 | Related: `tuvi-ecommerce-system` skill

## Port Conflict Resolution

When `netstat -ano | grep 8139` shows LISTENING on a stale PID:

```bash
# 1. Find the PID holding the port
netstat -ano | grep "LISTEN.*8139"
# Output: TCP 0.0.0.0:8139 ... LISTENING 29244

# 2. Kill it
taskkill //F //PID 29244

# 3. Wait for TIME_WAIT to clear (usually 1-3s on Windows)
sleep 3

# 4. Verify port is free
netstat -ano | grep "LISTEN.*8139" || echo "Port ready"

# 5. Restart
python restart_server.py
```

### Restart server script (`restart_server.py`)

The script kills old process + starts new one. Simple implementation:

```python
import subprocess, sys, os

os.chdir(os.path.dirname(__file__))
proc = subprocess.Popen(
    [sys.executable, "backend/main.py"],
    stdout=subprocess.PIPE, stderr=subprocess.PIPE
)
print(f"✅ Server started PID={proc.pid} port 8139")
```

⚠️ Does NOT auto-kill old process — do that manually via `taskkill //F //PID <pid>` first.

## VERIFY ALL TESTS AFTER RESTART

Run ALL of these after every restart, not just one:

```bash
# 1. Health
curl -s http://localhost:8139/api/health

# 2. Demo (real MCP)
curl -s -X POST http://localhost:8139/api/demo -H "Content-Type: application/json" \
  -d '{"year":1984,"month":5,"day":1,"hour":9,"gender":"male"}'

# 3. Products
curl -s http://localhost:8139/api/products

# 4. Payment (both gateways)
curl -s -X POST http://localhost:8139/api/payment/momo -H "Content-Type: application/json" \
  -d '{"product_id":"PDF01","customer_name":"Test","customer_phone":"0900000000","customer_email":"t@t.com","birth_year":1984,"birth_month":5,"birth_day":1,"birth_hour":9,"gender":"male"}'

curl -s -X POST http://localhost:8139/api/payment/vnpay -H "Content-Type: application/json" \
  -d '{"product_id":"PDF01","customer_name":"Test","customer_phone":"0900000000","customer_email":"t@t.com","birth_year":1984,"birth_month":5,"birth_day":1,"birth_hour":9,"gender":"male"}'

# 5. Frontend
curl -s http://localhost:8139/ | head -5
```

## TIME_WAIT behavior on Windows

After killing a process, existing TCP connections enter TIME_WAIT (~30-60s on Windows). They show in `netstat` output but do NOT block new LISTEN on the same port — only a new LISTENING entry blocks. If restart fails with "address in use", there's a stale LISTENING PID that needs taskkill.

## Subagent code verification

When a subagent (delegate_task) modifies files, ALWAYS re-verify:
1. The file exists at the expected path
2. The file contains expected content (grep for a key string)
3. The server restarts and tests pass (full test battery above)

Subagents cannot verify server-side behavior — that's the parent's job.
