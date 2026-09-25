# Disk Inspection Checklist

## Quick-start template (.ps1 script)

When running a disk inspection, write this to `C:\Users\Nguyen Ngoc Tan\_diskcheck.ps1`, run it, then delete it:

```powershell
$results = @()
Get-ChildItem "$env:LOCALAPPDATA" -Directory | ForEach-Object {
    $size = (Get-ChildItem $_.FullName -Recurse -ErrorAction SilentlyContinue | 
             Measure-Object -Property Length -Sum -ErrorAction SilentlyContinue).Sum
    if ($size -gt 50MB) {
        $results += [PSCustomObject]@{ Folder = $_.Name; SizeMB = [math]::Round($size / 1MB, 1) }
    }
}
$results | Sort-Object SizeMB -Descending | Format-Table -AutoSize
```

## Known findings from Jul 2026 inspection

| Item | Size (first) | Size (after restart) | Verdict |
|------|-------------|----------------------|---------|
| Temp | 2.3 GB | — | Deleted (safe) |
| npm-cache | 3.4 GB | — | Deleted (regenerates) |
| ms-playwright | 1.9 GB | — | Deleted (browser test binaries) |
| ms-playwright-go | 96 MB | — | Deleted |
| Package Cache | 165 MB | — | Deleted (installer cache) |
| CapCut (portable) | 4.7 GB | — | Deleted (user approved, reinstalled to D) |
| Windows Store Packages | 13.3 GB | — | Kept — needs Disk Cleanup > System Files |
| Google Chrome | 3.9 GB | — | Kept (user wants cache/profile) |
| CocCoc | 1 GB | — | Kept |
| Perplexity/Comet | 1.3 GB | — | Kept |

## Jul 22 inspection — sorted findings

```
Packages              13312.9 MB  (13 GB)
CapCut                 4692.4 MB  (4.7 GB) — portable app
Google                 3919.7 MB  (3.9 GB)
npm-cache              3411.6 MB  (3.4 GB)
Temp                   2259.9 MB  (2.3 GB)
ms-playwright          1858.7 MB  (1.9 GB)
Perplexity             1341.8 MB  (1.3 GB)
CocCoc                 1041.0 MB  (1 GB)
Package Cache           165.1 MB
ms-playwright-go         96.6 MB
Ollama                    0.7 MB
```

## Process storm findings (same session)

When user asked "sao nó chạy gì mà khiếp nhỉ" — found:

| Process | Count | RAM total | Verdict |
|---------|-------|-----------|---------|
| comet.exe | ~20 instances | ~1.5-2 GB | Abnormal — memory leak |
| claude.exe | ~12 instances | ~1.5 GB | Abnormal — orphaned processes |
| Antigravity.exe | 6 instances | ~650 MB | Abnormal |
| language_server.exe | 1 | 462 MB | Normal (Antigravity bundle) |

Root cause: Hermes Desktop (Electron) + Perplexity Comet spawning subprocesses without cleanup. Resolution: full restart.

## C: drive baseline progression

| Date | Free | Used% | Action |
|------|------|-------|--------|
| Pre-cleanup | 4.3 GB | 98% | Full disk alert |
| After restart | 15 GB | 92% | Cleared process storms |
| After cache cleanup | 21.7 GB | 87% | Temp + npm + playwright |
| After CapCut removal | 27 GB | 85% | Portable app deleted |

## Total: ~22.7 GB reclaimed from a single session
