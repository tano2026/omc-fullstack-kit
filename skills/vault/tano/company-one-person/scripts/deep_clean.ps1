# Deep clean ổ C — dọn cache tool để giải phóng dung lượng
# Chạy: powershell -ExecutionPolicy Bypass -File deep_clean.ps1

Write-Host "=== Dọn .gemini ==="
$g = "$env:USERPROFILE\.gemini"
if (Test-Path $g) {
    $sz = (Get-ChildItem $g -Recurse -Force -ErrorAction SilentlyContinue | Measure-Object -Property Length -Sum -ErrorAction SilentlyContinue).Sum
    Write-Host "Before: $([math]::Round($sz/1GB, 2))GB"
    Remove-Item $g -Recurse -Force -ErrorAction SilentlyContinue
    Write-Host "Removed"
}

Write-Host "=== Dọn .cursor cache ==="
$c = "$env:USERPROFILE\.cursor"
if (Test-Path $c) {
    $sz = (Get-ChildItem $c -Recurse -Force -ErrorAction SilentlyContinue | Measure-Object -Property Length -Sum -ErrorAction SilentlyContinue).Sum
    Write-Host "Before: $([math]::Round($sz/1GB, 2))GB"
    Remove-Item "$c\Cache" -Recurse -Force -ErrorAction SilentlyContinue
    Remove-Item "$c\machineid" -Recurse -Force -ErrorAction SilentlyContinue
    Remove-Item "$c\logs" -Recurse -Force -ErrorAction SilentlyContinue
    Write-Host "Cursor cache/logs removed"
}

Write-Host "=== Dọn .vscode extensions ==="
$v = "$env:USERPROFILE\.vscode"
if (Test-Path $v) {
    Remove-Item "$v\extensions\*" -Recurse -Force -ErrorAction SilentlyContinue
    Write-Host "VSCode extensions removed (can reinstall)"
}

Write-Host "=== Dọn npm cache ==="
npm cache clean --force 2>$null
Write-Host "npm cache cleaned"

Write-Host "=== Check result ==="
$d = Get-CimInstance Win32_LogicalDisk -Filter "DeviceID='C:'"
$free_gb = [math]::Round($d.FreeSpace / 1GB, 1)
Write-Host "C: Free: ${free_gb}GB"
