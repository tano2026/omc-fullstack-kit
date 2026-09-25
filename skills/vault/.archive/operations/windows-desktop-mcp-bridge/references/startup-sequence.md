# Desktop Control MCP — Startup Sequence

## Two-Terminal Protocol

Both components must be running for Hermes to use the 6 MCP tools.

### Terminal #1: Desktop Executor (HTTP Server)
```powershell
cd "D:\AI Store\Hermes Agent"
python desktop_executor.py
# Expected output: [*] Desktop OS Agent is listening on http://127.0.0.1:19999
```
**Keep this terminal open.** Closing it kills the HTTP server.

### Terminal #2: Desktop Control MCP (FastMCP stdio)
Open a **second** PowerShell terminal:
```powershell
cd "D:\AI Store\Hermes Agent"
python desktop_control_mcp.py
```
The script runs silently — no output means it's listening for MCP requests.

### Terminal #3: Hermes Session (optional)
If starting fresh, open a third terminal for Hermes CLI:
```powershell
cd "D:\AI Store\Hermes Agent"
python -m hermes
```

## Quick Verify
```powershell
# Check Desktop Executor is alive
curl -s http://127.0.0.1:19999/health

# Check Hermes MCP is registered
hermes mcp list | grep desktop-control
```

## Shutdown Sequence
1. Ctrl+C on Terminal #2 (desktop_control_mcp.py)
2. Ctrl+C on Terminal #1 (desktop_executor.py)
3. Verify ports freed: `netstat -ano | findstr :19999`
