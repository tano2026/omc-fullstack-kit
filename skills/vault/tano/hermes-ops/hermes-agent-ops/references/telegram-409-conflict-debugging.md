# Telegram 409 Conflict — Full Debugging Protocol

## The 409 Conflict

```
Conflict: terminated by other getUpdates request; make sure that only one bot instance is running
```

**Meaning:** Two+ processes are polling the same Telegram bot token simultaneously. Telegram only allows one active polling connection per token.

## Symptom Pattern

Gateway log (`~/AppData/Local/hermes/logs/gateway.log`) shows an infinite loop:

```
WARNING — Telegram polling conflict (1/5) — previous session still held open.
Waiting 20s for it to expire.
INFO — Telegram polling resumed after conflict retry 1/5
WARNING — Telegram polling conflict (1/5) — ...repeat forever
```

## Diagnostic: Find ALL processes connected to Telegram

```powershell
# Find every process connected to Telegram's server
Get-NetTCPConnection -RemoteAddress 149.154.166.110 |
    Select-Object OwningProcess,LocalPort,State
```

Telegram's server IP is `149.154.166.110`. Any process showing `Established` here is polling a bot.

## Identify Each PID

```powershell
# General
Get-Process -Id <PID> | Select-Object Id,ProcessName,StartTime

# For Python — full command line (which script is it running?)
(Get-WmiObject Win32_Process -Filter 'ProcessId=<PID>').CommandLine

# For any process — parent process ID (who spawned it?)
(Get-CimInstance Win32_Process -Filter 'ProcessId=<PID>').ParentProcessId
```

### Typical Culprits

| Process | PID Pattern | What It Is |
|---------|-------------|------------|
| `pythonw.exe -m hermes_cli.main gateway run` | spawned by `hermes gateway start` | Standalone Hermes gateway |
| `python main.py` | loop in `run_command_center.bat` | CEO bot (TanoAgencyCEO startup) |
| `node.exe` | child of Hermes.exe | Hermes Desktop internal gateway |
| `python ... dashboard` | spawned by `hermes dashboard` | Dashboard process, NOT polling Telegram |

## Resolution

### Step 1: Kill ALL conflicting processes

Use PowerShell `Stop-Process -Force` (more reliable than `taskkill`):

```powershell
# Kill specific PIDs
Stop-Process -Id <PID> -Force

# Or kill by name
Stop-Process -Name node -Force
Get-Process -Name Hermes | Stop-Process -Force
```

### Step 2: Check for auto-restart

Processes can respawn from:

1. **Windows Startup folder** — `C:\Users\<user>\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup\`
   - `Hermes_Gateway.cmd` — auto-starts standalone gateway on login
   - `TanoAgencyCEO.lnk` — auto-starts CEO bot via `run_command_center.bat` loop
   - `OpenClaw Gateway.lnk` — auto-starts OpenClaw gateway (different bot, usually no conflict)
2. **Registry Run** — `HKCU:\Software\Microsoft\Windows\CurrentVersion\Run`
3. **Task Scheduler** — `Get-ScheduledTask | Where-Object {$_.TaskName -match 'hermes'}`

To stop auto-restart permanently, remove the startup file:
```bash
rm -f "/c/Users/<user>/AppData/Roaming/Microsoft/Windows/Start Menu/Programs/Startup/Hermes_Gateway.cmd"
```

### Step 3: Read shortcut targets

```powershell
$wshell = New-Object -ComObject WScript.Shell
$sc = $wshell.CreateShortcut('C:\Users\<user>\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup\<file>.lnk')
Write-Output "Target: $($sc.TargetPath)"
Write-Output "Args: $($sc.Arguments)"
Write-Output "Dir: $($sc.WorkingDirectory)"
```

### Step 4: Start clean

Only ONE process should poll the bot token:
- **Option A**: Standalone gateway only (`hermes gateway start` after killing Hermes Desktop)
- **Option B**: Hermes Desktop only (no standalone gateway)
- **Option C**: Different bot tokens for different instances

## Quick Reference: All Telegram-related PIDs

```powershell
# Find ALL python processes with bot/gateway in command line
Get-WmiObject Win32_Process -Filter 'Name LIKE "%python%"' |
    Where-Object { $_.CommandLine -match 'gateway|hermes_cli|main\.py' } |
    ForEach-Object { Write-Output "PID: $($_.ProcessId) - $($_.CommandLine)" }

# Find all Hermes Desktop processes
Get-Process -Name Hermes

# Find all Node.js processes (Hermes Desktop backend)
Get-Process -Name node
```

## Pitfalls

- `hermes gateway status` reports "running" even when a 409 conflict loop is happening — it shows PID is alive, not that polling works. Always check the **gateway log** for `Conflict` messages.
- Killing `main.py` (CEO bot) alone is futile — the `run_command_center.bat` loop (parent `cmd.exe`) restarts it in 5 seconds. Find and kill the parent `cmd.exe` or remove the startup `.lnk`. The full chain is: `cmd.exe PID:N → python main.py PID:M` (PIDs vary by session). Kill the parent (cmd.exe) to prevent respawn.
- **Python version mismatch**: `hermes gateway stop` may return `"No gateway running"` despite a live gateway PID (visible via `Get-Process`). The gateway can run under a **different Python** (e.g. Python 3.11) than the `hermes` CLI (e.g. Python 3.14) — the CLI's process scanner only finds processes matching its own Python. If `hermes gateway stop` fails but the PID still exists, fall back to `Stop-Process -Id <PID> -Force`.
- Hermes Desktop (Electron) spawns **5+ `Hermes.exe` + `node.exe` background processes** from the same launch session. Closing the window doesn't kill them — use `Get-Process -Name Hermes | Stop-Process -Force` or exit from system tray icon.
- Killing `node.exe` alone is ineffective — `Hermes.exe` respawns it. Kill `Hermes.exe` processes first.
- Token revocation via @BotFather doesn't kill the rogue instance immediately — it deauthorizes it. The rogue instance will fail on its next poll.
