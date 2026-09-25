# Clean C Drive — safe cache/temp cleanup script
# Run: powershell.exe -ExecutionPolicy Bypass -File clean_c_drive.ps1
# SAFE TARGETS only: temp dirs, package caches, browser caches, dev tool caches
# Will NOT touch app binaries, user profiles, or personal data

Write-Host "=== DON DEP O C: Safe Cache/Temp Cleanup ===" -ForegroundColor Cyan
Write-Host ""

$totalFreed = 0
$targets = @{}

# --- User Temp ---
if (Test-Path "$env:TEMP") {
    $size = (Get-ChildItem "$env:TEMP\*" -Recurse -ErrorAction SilentlyContinue | 
             Measure-Object -Property Length -Sum -ErrorAction SilentlyContinue).Sum
    $targets["User Temp"] = @{Path="$env:TEMP\*"; Size=$size}
}

# --- npm cache ---
if (Test-Path "$env:LOCALAPPDATA\npm-cache") {
    $size = (Get-ChildItem "$env:LOCALAPPDATA\npm-cache\*" -Recurse -ErrorAction SilentlyContinue | 
             Measure-Object -Property Length -Sum -ErrorAction SilentlyContinue).Sum
    $targets["npm-cache"] = @{Path="$env:LOCALAPPDATA\npm-cache\*"; Size=$size}
}

# --- .npm/_cacache ---
if (Test-Path "$env:USERPROFILE\.npm\_cacache") {
    $size = (Get-ChildItem "$env:USERPROFILE\.npm\_cacache\*" -Recurse -ErrorAction SilentlyContinue | 
             Measure-Object -Property Length -Sum -ErrorAction SilentlyContinue).Sum
    $targets[".npm cache"] = @{Path="$env:USERPROFILE\.npm\_cacache\*"; Size=$size}
}

# --- ms-playwright ---
if (Test-Path "$env:LOCALAPPDATA\ms-playwright") {
    $size = (Get-ChildItem "$env:LOCALAPPDATA\ms-playwright\*" -Recurse -ErrorAction SilentlyContinue | 
             Measure-Object -Property Length -Sum -ErrorAction SilentlyContinue).Sum
    $targets["ms-playwright"] = @{Path="$env:LOCALAPPDATA\ms-playwright\*"; Size=$size}
}

# --- ms-playwright-go ---
if (Test-Path "$env:LOCALAPPDATA\ms-playwright-go") {
    $size = (Get-ChildItem "$env:LOCALAPPDATA\ms-playwright-go\*" -Recurse -ErrorAction SilentlyContinue | 
             Measure-Object -Property Length -Sum -ErrorAction SilentlyContinue).Sum
    $targets["ms-playwright-go"] = @{Path="$env:LOCALAPPDATA\ms-playwright-go\*"; Size=$size}
}

# --- Package Cache ---
if (Test-Path "$env:LOCALAPPDATA\Package Cache") {
    $size = (Get-ChildItem "$env:LOCALAPPDATA\Package Cache\*" -Recurse -ErrorAction SilentlyContinue | 
             Measure-Object -Property Length -Sum -ErrorAction SilentlyContinue).Sum
    $targets["Package Cache"] = @{Path="$env:LOCALAPPDATA\Package Cache\*"; Size=$size}
}

# --- Windows Temp ---
$winTemp = "$env:SystemRoot\Temp"
if (Test-Path $winTemp) {
    $size = (Get-ChildItem "$winTemp\*" -Recurse -ErrorAction SilentlyContinue | 
             Measure-Object -Property Length -Sum -ErrorAction SilentlyContinue).Sum
    $targets["Windows Temp"] = @{Path="$winTemp\*"; Size=$size}
}

# --- pip cache ---
if (Test-Path "$env:LOCALAPPDATA\pip\Cache") {
    $size = (Get-ChildItem "$env:LOCALAPPDATA\pip\Cache\*" -Recurse -ErrorAction SilentlyContinue | 
             Measure-Object -Property Length -Sum -ErrorAction SilentlyContinue).Sum
    $targets["pip Cache"] = @{Path="$env:LOCALAPPDATA\pip\Cache\*"; Size=$size}
}

# --- uv cache ---
if (Test-Path "$env:LOCALAPPDATA\uv-cache") {
    $size = (Get-ChildItem "$env:LOCALAPPDATA\uv-cache\*" -Recurse -ErrorAction SilentlyContinue | 
             Measure-Object -Property Length -Sum -ErrorAction SilentlyContinue).Sum
    $targets["uv-cache"] = @{Path="$env:LOCALAPPDATA\uv-cache\*"; Size=$size}
}

# --- Pre-clean summary ---
Write-Host "Items to clean:" -ForegroundColor Yellow
foreach ($item in $targets.Keys) {
    $sizeMB = [math]::Round($targets[$item].Size / 1MB, 1)
    Write-Host "  $item`: $sizeMB MB"
    $totalFreed += $targets[$item].Size
}
Write-Host ""
Write-Host "Total to free: $([math]::Round($totalFreed/1MB,1)) MB" -ForegroundColor Cyan

# --- Delete ---
foreach ($item in $targets.Keys) {
    Write-Host ">>> Deleting $item..." -NoNewline
    Remove-Item $targets[$item].Path -Recurse -Force -ErrorAction SilentlyContinue
    Write-Host " Done!" -ForegroundColor Green
}

Write-Host ""
Write-Host "=== Cleanup Complete ===" -ForegroundColor Cyan

# --- Disk status ---
$disk = Get-CimInstance Win32_LogicalDisk -Filter "DeviceID='C:'"
$freeGB = [math]::Round($disk.FreeSpace / 1GB, 1)
$usedGB = [math]::Round(($disk.Size - $disk.FreeSpace) / 1GB, 1)
$totalGB = [math]::Round($disk.Size / 1GB, 1)
$pct = [math]::Round($disk.FreeSpace / $disk.Size * 100, 0)
Write-Host "O C: ${freeGB}GB free / ${totalGB}GB (${pct}% free)" -ForegroundColor Green
