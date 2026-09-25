---
name: windows-desktop-mcp-bridge
category: operations
description: Set up and use a Desktop Executor + MCP bridge to give Hermes Agent direct Windows filesystem access — read/write files, list directories, run commands, and take screenshots outside the restricted workspace sandbox.
---

# Windows Desktop MCP Bridge

A two-component system that bridges Hermes Agent to the Windows desktop environment, bypassing the sandboxed workspace restriction.

## Architecture

```
┌───────────────────────────┐       HTTP       ┌──────────────────────┐
│  Hermes Agent (MCP)       │ ──────────────►  │  Desktop Executor    │
│  desktop_control_mcp.py   │  POST / :19999   │  desktop_executor.py │
│  ┌──────────────────┐     │                  │  ┌────────────────┐  │
│  │ FastMCP stdio    │     │                  │  │ Windows API    │  │
│  │ 6 MCP tools      │     │                  │  │ os, subprocess │  │
│  └──────────────────┘     │                  │  │ pyautogui      │  │
└───────────────────────────┘                  └────────────────────┘
```

### Components

| Component | File | Role |
|-----------|------|------|
| **Desktop Executor** | `desktop_executor.py` | HTTP server listening on `127.0.0.1:19999`. Receives JSON actions from Hermes and executes them on Windows via Python stdlib (`os`, `subprocess`, `pyautogui`). |
| **Desktop Control MCP** | `desktop_control_mcp.py` | FastMCP server (stdio mode). Exposes 6 MCP tools to Hermes that send HTTP requests to the Desktop Executor. |

### Default Path

Both files live under `D:\AI Store\Hermes Agent\`.

## Available MCP Tools

| Tool | Description | Use case |
|------|-------------|----------|
| `remote_read_file(filepath)` | Read any local file with UTF-8 encoding | Read Postman collections, config files, project files on D: drive |
| `remote_write_file(filepath, content)` | Write/overwrite any file, auto-create parent dirs | Create docker-compose, .env, code files directly into project dirs |
| `remote_list_dir(dirpath)` | List files/dirs with size and type classification | Explore project structure on any drive |
| `remote_screenshot()` | Take screenshot of current Windows desktop | Visual QA, debugging UI issues |
| `remote_run_command(command)` | Run CMD/PowerShell commands on Windows | Execute git commands, check processes, deploy |
| `remote_type_text(text)` | Simulate keyboard input on Windows | Fill forms, automate Windows desktop apps |

## Setup & Startup Sequence

### Step 1: Start Desktop Executor
```powershell
cd "D:\AI Store\Hermes Agent"
python desktop_executor.py
# Output: [*] Desktop OS Agent is listening on http://127.0.0.1:19999
```
**Keep this terminal open** — it's the HTTP server that processes all file/command requests.

### Step 2: Register MCP Server in Hermes Config
The MCP server must be registered in `~/.hermes/config.yaml` under `mcp_servers`:

```yaml
mcp_servers:
  desktop-control:
    command: d:\AI Store\Hermes Agent\venv\Scripts\python.exe
    args:
    - d:\AI Store\Hermes Agent\desktop_control_mcp.py
    timeout: 30
    description: "Điều khiển máy tính Windows - đọc/ghi file, chụp màn hình, chạy lệnh"
```

⚠️ **Cannot edit config.yaml directly from Hermes** — use `hermes config set` CLI or edit manually.

### Step 3: Reload MCP in Hermes
```powershell
hermes mcp reload
# Or restart Hermes session to pick up new MCP tools
```

### Step 4: Verify
```powershell
hermes mcp list
# Should show: desktop-control
```

## When to Use (vs Built-in Tools)

| Scenario | Use | Why |
|----------|-----|-----|
| Read file on D: drive (outside Hermes workspace) | `remote_read_file` | Hermes `read_file` blocked outside sandbox |
| Write file to Git repo on D: drive | `remote_write_file` | Direct path access |
| Explore project folder structure | `remote_list_dir` | Faster than guessing paths |
| Run git commands | `remote_run_command` | Full Windows terminal access |
| Take screenshot | `remote_screenshot` | Visual context without browser tool |

## Pitfalls & Troubleshooting

### 🔴 "Can't open file" error
```
python: can't open file 'C:\\WINDOWS\\system32\\desktop_executor.py': [Errno 2]
```
**Fix:** You're in the wrong directory. Navigate to the file's location first:
```powershell
cd "D:\AI Store\Hermes Agent"
python desktop_executor.py
```

### 🔴 MCP tools not appearing in Hermes
**Cause:** The MCP server (`desktop_control_mcp.py`) wasn't registered in `config.yaml` or wasn't reloaded.
**Fix:**
1. Check config: `hermes config get mcp_servers.desktop-control`
2. If missing, add via `hermes config set mcp_servers.desktop-control.command ...`
3. Reload: `hermes mcp reload`

### 🔴 "Connection refused" errors
**Cause:** `desktop_executor.py` is not running in its terminal.
**Fix:** Open a new terminal and start it:
```powershell
cd "D:\AI Store\Hermes Agent"
python desktop_executor.py
```
Keep the terminal window open — closing it kills the HTTP server.

### 🔴 Port 19999 already in use
```powershell
netstat -ano | findstr :19999
taskkill /F /PID <PID>
```

## References & See Also

- `references/startup-sequence.md` — Exact startup checklist (terminal #1 + terminal #2)
