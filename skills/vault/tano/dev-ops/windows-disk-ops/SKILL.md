---
name: windows-disk-ops
category: dev-ops
description: Class-level operations for Windows disk space inspection and cleanup. Covers bash (git-bash/MSYS) and PowerShell strategies for checking C drive usage, identifying large cache/temp dirs, and safely reclaiming space on Windows hosts. Also covers system health (CPU, RAM, uptime) via PowerShell Get-CimInstance replacement for deprecated WMIC.
tags: [windows, disk, cleanup, temp, cache, powershell, system-health, wmic]
---

# Windows Disk & Process Operations

> **Class-level skill** for diagnosing Windows disk space AND runaway processes from within Hermes Agent. Covers the multi-tool strategy needed because `du` is slow on Windows via git-bash, and PowerShell has path-escaping issues from MSYS.

## When to Use

- User reports "o C day" / disk full / low disk space
- User asks "don dep o C" / "xem dung luong o C"
- User asks "sao no chay gi ma khiep nhi" / "may dang chay gi do nang" / system feels slow
- Routine system health audit
- Before installing large software packages

---

## Part 1: Process Triage ("máy chạy gì mà khiếp nhỉ")

When the user reports the system feels sluggish, check for **process storms** first — multiple instances of the same app is a common sign of a memory leak or runaway spawn.

### Quick process dump by count + RAM

```bash
powershell.exe -Command "Get-Process | Group-Object Name | Where-Object Count -gt 2 | Select-Object @{N='Process';E={$_.Name}}, @{N='Instances';E={$_.Count}}, @{N='TotalRAM_MB';E={[math]::Round(($_.Group | Measure-Object WorkingSet -Sum).Sum/1MB,1)}} | Sort-Object TotalRAM_MB -Descending | Format-Table -AutoSize"
```

This catches process storms: Comet (Perplexity) with 20+ instances, Antigravity with 6+, Claude with 12+ — each eating hundreds of MB.

### RAM + CPU top hitters

```bash
powershell.exe -Command "Get-Process | Sort-Object WorkingSet -Descending | Select-Object -First 15 Name, Id, @{N='RAM_MB';E={[math]::Round($_.WorkingSet/1MB,1)}}, @{N='CPU_s';E={[math]::Round($_.TotalProcessorTime.TotalSeconds,0)}} | Format-Table -AutoSize"
```

### Common process storm suspects on this system

| Process | Origin | Danger signal |
|---------|--------|--------------|
| `comet.exe` | Perplexity Comet | **5+ instances** = abnormal (memory leak) |
| `Antigravity.exe` | Antigravity app | **3+ instances** = abnormal |
| `claude.exe` | Claude Desktop (Hermes Desktop Electron) | **8+ instances** = memory leak / orphaned processes |
| `language_server.exe` | Bundled with Antigravity | Single instance, ~460 MB RAM — normal

**Resolution**: If process storm confirmed, recommend restart first.
```bash
shutdown /r /t 60 /c "Restart theo yeu cau"
```

---

## Part 2: Disk Space Inspection

**Three approaches, use in order:**

### Approach 1: Quick check -- PowerShell via CIM (fastest)

```bash
powershell.exe -Command "Get-CimInstance Win32_LogicalDisk -Filter \"DeviceID='C:'\" | Select-Object DeviceID, @{N='SizeGB';E={[math]::Round($_.Size/1GB,1)}}, @{N='FreeGB';E={[math]::Round($_.FreeSpace/1GB,1)}}, @{N='Used%';E={[math]::Round(($_.Size-$_.FreeSpace)/$_.Size*100,0)}}"
```

### Approach 2: Top space hogs scan — write .ps1 file (detailed analysis)

**NEVER pass inline PowerShell with file paths containing spaces from MSYS.** The space in `C:\Users\Nguyen Ngoc Tan\` breaks argument parsing. Always write a `.ps1` script and run with `-File`.

#### Option A: Auto-discover ALL directories >50MB under AppData/Local

```powershell
$results = @()
Get-ChildItem "$env:LOCALAPPDATA" -Directory | ForEach-Object {
    $size = (Get-ChildItem $_.FullName -Recurse -ErrorAction SilentlyContinue | Measure-Object -Property Length -Sum -ErrorAction SilentlyContinue).Sum
    if ($size -gt 50MB) {
        $results += [PSCustomObject]@{ Folder = $_.Name; SizeMB = [math]::Round($size / 1MB, 1) }
    }
}
$results | Sort-Object SizeMB -Descending | Format-Table -AutoSize
```

#### Option B: Known large cache/temp targets (faster, no recursion over full drive)

```powershell
$targets = @(
    "$env:LOCALAPPDATA\Temp",
    "$env:LOCALAPPDATA\Packages",
    "$env:LOCALAPPDATA\CapCut",
    "$env:LOCALAPPDATA\Google",
    "$env:LOCALAPPDATA\npm-cache",
    "$env:LOCALAPPDATA\ms-playwright",
    "$env:LOCALAPPDATA\Perplexity",
    "$env:LOCALAPPDATA\CocCoc",
    "$env:LOCALAPPDATA\Package Cache",
    "$env:LOCALAPPDATA\Docker",
    "$env:LOCALAPPDATA\.cache",
    "$env:LOCALAPPDATA\pip\Cache",
    "$env:LOCALAPPDATA\uv-cache",
    "$env:LOCALAPPDATA\Microsoft\Windows\INetCache",
    "C:\Windows\Temp",
    "C:\Windows\SoftwareDistribution\Download"
)
foreach ($p in $targets) {
    if (Test-Path $p) {
        $size = (Get-ChildItem $p -Recurse -ErrorAction SilentlyContinue | Measure-Object -Property Length -Sum -ErrorAction SilentlyContinue).Sum
        if ($size -gt 0) {
            [PSCustomObject]@{ Path = $p; SizeMB = [math]::Round($size / 1MB, 1) }
        }
    }
} | Sort-Object SizeMB -Descending | Format-Table -AutoSize
```

Run:
```bash
powershell.exe -ExecutionPolicy Bypass -File "C:\Users\Nguyen Ngoc Tan\_diskcheck.ps1"
```

**Delete the temp script** after use:
```bash
rm -f "C:\Users\Nguyen Ngoc Tan\_diskcheck.ps1"
```

### Approach 3: Python `os.scandir` scan (when `du` fails on saturated disk)

**When disk is critically full (< 1GB free), `du` becomes nearly useless** — even single-directory scans timeout at 120s due to I/O saturation. Switch to Python `execute_code` with `os.scandir`:

```python
import os

def get_size(path):
    total = 0
    try:
        with os.scandir(path) as it:
            for entry in it:
                try:
                    if entry.is_file(follow_symlinks=False):
                        total += entry.stat().st_size
                    elif entry.is_dir(follow_symlinks=False):
                        total += get_size(entry.path)
                except (PermissionError, OSError):
                    pass
    except (PermissionError, OSError):
        pass
    return total

# Scan specific targets (NOT full drives)
targets = [
    r"C:\Users\Nguyen Ngoc Tan\AppData\Local\hermes",
    r"C:\Users\Nguyen Ngoc Tan\AppData\Local\Google",
    r"C:\Users\Nguyen Ngoc Tan\AppData\Local\uv",
    # ...add more as needed
]
for t in targets:
    if os.path.exists(t):
        size = get_size(t)
        print(f"{size/1e9:7.2f} GB  {t}")
```

See `references/python-disk-scan.py` for the full reusable scanner.

### Approach 4: `du` via git-bash (only when disk has >1GB free)

Use for small targeted queries only when disk isn't saturated:
```bash
du -sh --threshold=100M "/c/Users/Nguyen Ngoc Tan/.cache"/*/  2>/dev/null | sort -rh
du -sh --threshold=200M "/c/Users/Nguyen Ngoc Tan/Downloads"/*.exe 2>/dev/null | sort -rh
```

**DO NOT** run `du` on root (`/`) or entire user directories -- it will timeout after 180s even on a healthy disk.

---

## Related References

- `references/python-disk-scan.py` — Reusable Python scanner for saturated disks
- `references/hermes-disk-cleanup.md` — Hermes AppData can grow to 100+ GB; safe cleanup guide
- `references/disk-inspection-checklist.md` — Pre-existing disk inspection checklist

---

## Safe Cleanup Targets

### Can delete without user confirmation (cache/temp that auto-regenerates):

| Path | Typical Size | Notes |
|------|-------------|-------|
| `Temp` (both Windows + User) | 500-2000 MB | Safe to clear entirely |
| `npm-cache` | 1-4 GB | Regenerates on install |
| `ms-playwright` | 1-2 GB | Browser binaries, rerun `playwright install` if needed |
| `ms-playwright-go` | 50-100 MB | Go Playwright binaries, same pattern |
| `Package Cache` | 100-200 MB | Windows installer cache |
| `pip\\Cache` | 200-500 MB | Pip cache, regenerated |
| `uv-cache` | 200-500 MB | UV package cache |
| **hemes AppData** | 5-200 GB | `AppData/Local/hermes/` — sessions/, plugins/, skills/, audio_cache/, cron/ state. See `references/hermes-disk-cleanup.md`. |
| **npm global packages** | 1-8 GB | `AppData/Roaming/npm/node_modules/` — global npm installs (omniroute, n8n, openclaw, etc.) |
| **uv cache** | 1-15 GB | `AppData/Local/uv/` — Python package cache. `uv cache clean` |
| **Google/Chrome** | 2-10 GB | `AppData/Local/Google/` — browser cache + profiles |
| **Yarn cache** | 1-3 GB | `AppData/Local/Yarn/` — `yarn cache clean` |
| **Perplexity Comet** | 1-3 GB | `AppData/Local/Perplexity/` — AI app data |
| `Explorer` (thumbnail cache) | 20-30 MB | Thumbnails |
| `Recent` (recent files list) | 2-5 MB | File shortcuts |
| `crashdumps` | 100-500 MB | Crash dump files |

### Needs user confirmation (app data or large-install):

| Item | Typical Size | Notes |
|------|-------------|-------|
| **CapCut** | 3-5 GB | Full app — uninstall from C, reinstall to D |
| **CocCoc** | ~1 GB | Coccoc browser — reinstall to D |
| **Perplexity/Comet** | 1-2 GB | App data — check if user still needs it |
| **Google Chrome** | 3-5 GB | Browser profile: cache can be cleared, profile data kept |
| **Packages** (Windows Store) | 10-15 GB | Use Disk Cleanup > Clean up system files > Delivery Optimization |
| **npm-cache** | 3-4 GB | Confirm npm isn't mid-project |

### Detecting portable vs installed apps

Some apps live in `AppData/Local` as portable installs without Windows registration — they won't show up in `Get-WmiObject Win32_Product` or `Get-AppxPackage`. Detect them by:

```powershell
# Check if it's a registered install
$wmi = Get-WmiObject Win32_Product | Where-Object {$_.Name -like '*CapCut*'}
# Check if it's a Store app
$store = Get-AppxPackage *CapCut*
# If both empty but dir exists in AppData/Local → portable app
if (!$wmi -and !$store -and (Test-Path "$env:LOCALAPPDATA\CapCut")) {
    "Portable app — delete folder to remove"
}
```

Portable apps often have a `uninst.exe` in their folder but it rarely runs silently. Folder deletion is the reliable fallback (after user confirmation).

---

## App Reinstallation Pattern (move to D)

When moving an app from C to D drive to free space:
1. Suggest the user uninstall via Settings > Apps > Installed Apps
2. Reinstall with custom path to D:\
3. For portable apps: move the folder + update shortcuts manually

Common apps found on C on this machine that can move: CapCut, CocCoc, Perplexity/Comet, Google Chrome, Claude Desktop, Antigravity.

---

## Reusable Cleanup Script

A self-contained PowerShell script `scripts/clean_c_drive.ps1` ships with this skill. It safely clears all cache/temp targets (Temp, npm-cache, ms-playwright, Package Cache, pip cache, uv cache) with pre-clean summary and post-clean disk status.

Run directly:
```bash
powershell.exe -ExecutionPolicy Bypass -File "C:\Users\Nguyen Ngoc Tan\AppData\Local\hermes\skills\tano\dev-ops\windows-disk-ops\scripts\clean_c_drive.ps1"
```

The script targets only auto-regenerating caches — it won't touch app binaries, user profiles, or personal data. Pair with user confirmation for app-level items (CapCut, CocCoc, etc.) before running.

## Downloads Inspection Pattern

```bash
du -sh --threshold=100M "/c/Users/Nguyen Ngoc Tan/Downloads"/*.exe "/c/Users/Nguyen Ngoc Tan/Downloads"/*.zip 2>/dev/null | sort -rh | head -20
```

Common duplicate patterns:
- `file.zip` + `file (1).zip` (download duplicates)
- `folder/` + `folder.zip` (already extracted)

---

## Pitfalls

- **Disk I/O saturation:** When disk is 100% full (< 1GB free), `du` becomes nearly useless — even single-directory scans timeout at 120s. Switch to Python `os.scandir` scanning (Approach 3). The disk is thrashing trying to find free blocks for directory traversal.
- **`AppData/Local/hermes` unchecked growth:** Hermes Agent's AppData directory can silently grow to 100+ GB from session history, audio cache, skill artifacts, and plugin data. Always include it in disk scans — it's not in the default known-targets list.
- **PowerShell + MSYS path escaping**: File paths with spaces are NOT safe as inline arguments to `powershell.exe -Command`. Always write a `.ps1` script and run with `-File`.
- **`du` on Windows via git-bash is SLOW** on deep trees. Never `du -sh /` or `du -sh /c/Users/` — will timeout.
- **Process storms** (many instances of same app) are often the real cause of "máy chậm" complaints, not full disk. Always check processes first with the triage commands in Part 1.
- **Restart is the best first fix** for process storms — propose it before manual process killing.
- **Delete temp scripts** after use — dont leave `.ps1` files on the users system.
- **User home directory** — this user is `Nguyen Ngoc Tan` (NOT the hostname). Use the home dir from the persona header.
- **Always confirm before deleting** — present a summary table with sizes, ask a yes/no question before acting. The user wants to decide what goes to D vs what gets cleaned.
- **WMIC is DEPRECATED** on modern Windows 10/11 (build 26200+). Use PowerShell `Get-CimInstance` instead:
  ```powershell
  Get-CimInstance Win32_LogicalDisk -Filter 'DriveType=3' | ConvertTo-Json
  Get-CimInstance Win32_OperatingSystem
  Get-CimInstance Win32_Processor
  ```
